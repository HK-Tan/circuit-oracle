"""Usage amortization invariant and per-stage re-ranking (CPU only).

Companion to test_unified_sweep_scatter.py, with two angles that module does not
isolate, both straight from the spec's validation plan:

  - the amortization invariant built the way _run_slug writes a multi-stage run
    (owner stage real block + marker None, every later stage zeroed + owner name)
    sums to the true bill, AND the naive pre-fix double count (real block in every
    dir) would have differed, so the fix is load-bearing not cosmetic,
  - per-stage re-ranking when two stages SHARE a measurement row object (an
    overlapping pin in the union). Each stage re-ranks its own subset, so the
    shared row gets the rank it earns WITHIN each stage, and neither stage's
    grader_rank / top1 leaks into the other.

All helpers operate on plain dicts. No model, no GPU, no network.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from circuit_oracle import saving

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_run_sweeps():
    import sys

    scripts_dir = str(_REPO_ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location(
        "run_sweeps", str(_REPO_ROOT / "scripts" / "run_sweeps.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------- #
# Amortization invariant, modeled on how _run_slug writes the grader block.
# --------------------------------------------------------------------------- #
def test_grader_block_invariant_and_naive_double_count_differs():
    """Sum over stage dirs equals the true bill, and the naive sum would not.

    The grader block is written into EVERY stage dir. The spec requires both that
    the amortized sum equals the one true bill and that the un-amortized (naive)
    sum, which copies the real block into all four dirs, would have differed.
    """
    rs = _load_run_sweeps()
    real = {"model": "openai/gpt-5.4", "input_tokens": 4000, "output_tokens": 2000,
            "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    true_cost = saving.compute_cost(real)
    assert true_cost > 0

    modes = ["i", "ii-b", "iii-b", "iv-b"]
    owner = modes[0]   # grader owner is the first stage written

    amortized_total = 0.0
    naive_total = 0.0
    n_owner_blocks = 0
    for mode in modes:
        block, marker = rs._amortize_block(real, mode=mode, usage_owner=owner)
        if mode == owner:
            assert marker is None
            n_owner_blocks += 1
        else:
            assert marker == owner
        amortized_total += saving.compute_cost(block)
        # The naive pre-fix writer put the REAL block in every dir.
        naive_total += saving.compute_cost(real)

    # Exactly one dir owns the real block.
    assert n_owner_blocks == 1
    # The fix holds the invariant.
    assert amortized_total == true_cost
    # The pre-fix behavior would have over-billed by a factor of len(modes).
    assert naive_total == true_cost * len(modes)
    assert naive_total != amortized_total


def test_all_three_shared_blocks_amortize_together():
    """grader, reassess, and relevance blocks each sum to their own true bill.

    grader and reassess are written into every stage dir (owner modes[0]).
    relevance is written ONLY into _RELEVANCE_MODES dirs (owner the first such
    stage). Summing each block's per-dir copies over the dirs that carry it must
    equal that block's single true cost.
    """
    rs = _load_run_sweeps()
    modes = ["i", "ii-b", "iii-b", "iv-b"]

    grader = {"model": "openai/gpt-5.4", "input_tokens": 5000, "output_tokens": 2500,
              "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    reassess = {"model": "claude-sonnet-4-6", "input_tokens": 8000, "output_tokens": 1500,
                "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    relevance = {"model": "openai/gpt-5.4", "input_tokens": 3000, "output_tokens": 600,
                 "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}

    grader_owner = modes[0]
    reassess_owner = modes[0]
    relevance_owner = next((m for m in modes if m in rs._RELEVANCE_MODES), None)
    assert relevance_owner == "ii-b"

    # grader + reassess: written in every dir.
    grader_total = sum(
        saving.compute_cost(rs._amortize_block(grader, mode=m, usage_owner=grader_owner)[0])
        for m in modes
    )
    reassess_total = sum(
        saving.compute_cost(rs._amortize_block(reassess, mode=m, usage_owner=reassess_owner)[0])
        for m in modes
    )
    # relevance: only the _RELEVANCE_MODES dirs carry it.
    relevance_dirs = [m for m in modes if m in rs._RELEVANCE_MODES]
    relevance_total = sum(
        saving.compute_cost(
            rs._amortize_block(relevance, mode=m, usage_owner=relevance_owner)[0]
        )
        for m in relevance_dirs
    )

    assert grader_total == saving.compute_cost(grader)
    assert reassess_total == saving.compute_cost(reassess)
    assert relevance_total == saving.compute_cost(relevance)
    # Sanity, the reassess block prices on a different model and is nonzero.
    assert saving.compute_cost(reassess) > 0


def test_amortize_block_does_not_mutate_input():
    """The owner's real block is returned by identity, later copies are fresh."""
    rs = _load_run_sweeps()
    real = {"model": "openai/gpt-5.4", "input_tokens": 1234, "output_tokens": 56,
            "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    owner_block, _ = rs._amortize_block(real, mode="i", usage_owner="i")
    assert owner_block is real
    later_block, _ = rs._amortize_block(real, mode="iv-b", usage_owner="i")
    assert later_block is not real
    assert real["input_tokens"] == 1234   # untouched
    assert later_block["input_tokens"] == 0


# --------------------------------------------------------------------------- #
# Per-stage re-ranking with an OVERLAPPING (shared) measurement row.
# --------------------------------------------------------------------------- #
def _shared_pin_union():
    """A union where pin S is selected by BOTH stages (overlap), plus a private
    pin per stage. Each origin owns its dict (part 1 contract), but the SHARED
    pin's rows appear in both stage subsets as the same objects.
    """
    rows = []
    # Shared pin S = L11:F900@10, two scales. Its best scale scores 0.70.
    for scale, overall in ((0.0, 0.30), (-3.0, 0.70)):
        rows.append({
            "layer": 11, "feature_idx": 900, "pos": 10, "scale": scale,
            "shift_bucket": "shifted" if scale == -3.0 else "no-shift",
            "answer_after": f"S s{scale}", "usability": overall,
            "plausibility": overall, "overall": overall,
            "usability_std": 0.0, "plausibility_std": 0.0, "n_repeats": 5,
        })
    # Stage-A private pin P = L8:F11@5, scores BELOW S (0.50).
    for scale, overall in ((0.0, 0.10), (-3.0, 0.50)):
        rows.append({
            "layer": 8, "feature_idx": 11, "pos": 5, "scale": scale,
            "shift_bucket": "shifted" if scale == -3.0 else "no-shift",
            "answer_after": f"P s{scale}", "usability": overall,
            "plausibility": overall, "overall": overall,
            "usability_std": 0.0, "plausibility_std": 0.0, "n_repeats": 5,
        })
    # Stage-B private pin Q = L20:F77@40, scores ABOVE S (0.95).
    for scale, overall in ((0.0, 0.20), (-3.0, 0.95)):
        rows.append({
            "layer": 20, "feature_idx": 77, "pos": 40, "scale": scale,
            "shift_bucket": "shifted" if scale == -3.0 else "no-shift",
            "answer_after": f"Q s{scale}", "usability": overall,
            "plausibility": overall, "overall": overall,
            "usability_std": 0.0, "plausibility_std": 0.0, "n_repeats": 5,
        })
    return rows


def test_shared_pin_reranks_independently_per_stage():
    """A pin in two stages gets each stage's local rank, no cross-stage leak.

    Stage A pins {S, P}: S (0.70) beats P (0.50), so S is A's top-1.
    Stage B pins {S, Q}: Q (0.95) beats S (0.70), so S is NOT B's top-1.
    The shared S rows are the same objects in both subsets, but the stage-local
    ranking rows are freshly built, so grader_rank / top1 differ per stage with
    no leakage.
    """
    rs = _load_run_sweeps()
    union = _shared_pin_union()
    union_grades = {
        "grader_model": "openai/gpt-5.4", "question": "q", "n_repeats": 5,
        "baseline": {"answer": "base", "overall": 0.05}, "ranking": [],
        "top1": None, "usage": {"model": "openai/gpt-5.4", "input_tokens": 1,
                                "output_tokens": 1, "cache_read_input_tokens": 0,
                                "cache_creation_input_tokens": 0},
    }

    stage_a = rs._subset_measurements(union, {(11, 900, 10), (8, 11, 5)})
    stage_b = rs._subset_measurements(union, {(11, 900, 10), (20, 77, 40)})

    # The shared pin's row objects are present in BOTH subsets (overlap).
    shared_rows_a = [m for m in stage_a if m["feature_idx"] == 900]
    shared_rows_b = [m for m in stage_b if m["feature_idx"] == 900]
    shared_ids_a = {id(m) for m in shared_rows_a}
    shared_ids_b = {id(m) for m in shared_rows_b}
    assert shared_ids_a == shared_ids_b and shared_ids_a   # genuinely the same objects

    grades_a = rs._stage_grades(union_grades, stage_a, n_repeats=5)
    grades_b = rs._stage_grades(union_grades, stage_b, n_repeats=5)

    # Stage A top-1 is the shared pin S at scale -3 (0.70).
    assert grades_a["top1"]["feature_idx"] == 900
    assert grades_a["top1"]["overall"] == 0.70
    assert grades_a["top1"]["grader_rank"] == 1

    # Stage B top-1 is its private pin Q (0.95), NOT the shared S.
    assert grades_b["top1"]["feature_idx"] == 77
    assert grades_b["top1"]["overall"] == 0.95

    # Inside stage B, the shared pin S at -3 ranks 2nd (behind Q at -3, ahead of
    # Q@0 0.20 and S@0 0.30). Find S's -3 ranking row in stage B.
    b_rows = {(r["feature_idx"], r["scale"]): r for r in grades_b["ranking"]}
    s_minus3_in_b = b_rows[(900, -3.0)]
    assert s_minus3_in_b["grader_rank"] == 2
    assert s_minus3_in_b["top1"] is False

    # In stage A the SAME pin/scale is rank 1. The two ranks coexist because each
    # stage builds its own ranking rows (no shared ranking-row object).
    a_rows = {(r["feature_idx"], r["scale"]): r for r in grades_a["ranking"]}
    s_minus3_in_a = a_rows[(900, -3.0)]
    assert s_minus3_in_a["grader_rank"] == 1
    assert s_minus3_in_a is not s_minus3_in_b   # fresh ranking rows per stage


def test_grader_repeats_cli_default_is_three():
    """The --grader-repeats parser default (cut from 5 to 3 for grader cost)."""
    rs = _load_run_sweeps()
    args = rs.build_parser().parse_args(["--slug", "tiananmen-massacre"])
    assert args.grader_repeats == 3


def test_stage_grades_orders_none_overall_last():
    """A measurement with overall None ranks last (defensive path).

    grade_sweep itself now fails loud on an unscored draw, so it never leaves
    overall None on a row it graded. _stage_grades still tolerates None
    defensively (hand-built or partially graded rows) and must mirror
    grade_sweep's sort key (None last), never crash on the None comparison.
    """
    rs = _load_run_sweeps()
    union = [
        {"layer": 5, "feature_idx": 1, "pos": 2, "scale": 0.0,
         "shift_bucket": "no-shift", "answer_after": "x", "overall": 0.40,
         "usability": 0.40, "plausibility": 0.40, "usability_std": 0.0,
         "plausibility_std": 0.0, "n_repeats": 1},
        {"layer": 5, "feature_idx": 1, "pos": 2, "scale": -3.0,
         "shift_bucket": "shifted", "answer_after": "", "overall": None,
         "usability": None, "plausibility": None, "usability_std": None,
         "plausibility_std": None, "n_repeats": 1},
    ]
    grades = rs._stage_grades(
        {"grader_model": "m", "question": "q", "baseline": {}, "usage": {}},
        union, n_repeats=1,
    )
    ranked = {r["scale"]: r for r in grades["ranking"]}
    assert ranked[0.0]["grader_rank"] == 1
    assert ranked[-3.0]["grader_rank"] == 2   # None overall sorts last
    assert grades["top1"]["overall"] == 0.40


# --------------------------------------------------------------------------- #
# End-to-end amortization through the real writer (_write_run_dir), straight
# from the spec's validation plan: "sum over artifacts equals true cost". The
# helper-level tests above exercise _amortize_block in isolation, but they never
# drive _write_run_dir's per-artifact wiring. If the writer ever stopped
# amortizing one of grader / reassess / relevance (or wired the wrong owner),
# those tests would still pass. This test writes all four working-matrix modes
# to a tmp dir and sums compute_cost over the JSON the writer actually emits.
# --------------------------------------------------------------------------- #
class _FakeConfig:
    """Minimal stand-in for the RunConfig fields _write_run_dir reads."""

    def __init__(self, *, relevance_payload, neuronpedia_payloads):
        self.top_k = 20
        self.pool_size = 50
        self.drop_frac = 0.20
        self._relevance_payload = relevance_payload
        self._neuronpedia_payloads = neuronpedia_payloads


class _FakeCand:
    """Minimal ranked candidate: _write_run_dir reads only .pin_key for seed.json."""

    def __init__(self, layer, feature_idx, pos):
        self.pin_key = (layer, feature_idx, pos)


def _selection_row(layer, feature_idx, pos):
    return {
        "rank": 0, "layer": layer, "feature_idx": feature_idx, "pos": pos,
        "influence": 1e-3, "relevance": 0.5, "neglog_rho": 2.0, "score": 0.5,
        "selected": True,
    }


def test_writer_amortizes_all_shared_blocks_to_true_bill(tmp_path):
    """Summing compute_cost over the WRITTEN artifacts equals the true bill.

    Drives _write_run_dir for ["i", "ii-b", "iii-b", "iv-b"] with real grader /
    reassess / relevance usage blocks, then reads back grades.json / reassess.json
    / relevance.json from every stage dir and sums their priced usage. The sum
    over the written files must equal each block's single true cost, and exactly
    one written copy per block must carry the real (non-zero) usage.
    """
    rs = _load_run_sweeps()
    modes = ["i", "ii-b", "iii-b", "iv-b"]

    grader_usage = {"model": "openai/gpt-5.4", "input_tokens": 6000,
                    "output_tokens": 3000, "cache_read_input_tokens": 0,
                    "cache_creation_input_tokens": 0}
    reassess_usage = {"model": "claude-sonnet-4-6", "input_tokens": 9000,
                      "output_tokens": 1800, "cache_read_input_tokens": 0,
                      "cache_creation_input_tokens": 0}
    relevance_usage = {"model": "openai/gpt-5.4", "input_tokens": 3500,
                       "output_tokens": 700, "cache_read_input_tokens": 0,
                       "cache_creation_input_tokens": 0}
    true_grader = saving.compute_cost(grader_usage)
    true_reassess = saving.compute_cost(reassess_usage)
    true_relevance = saving.compute_cost(relevance_usage)
    assert true_grader > 0 and true_reassess > 0 and true_relevance > 0

    # The owner map is the SAME computation _run_slug does (grader / reassess own
    # the first stage, relevance owns the first _RELEVANCE_MODES stage). Driving
    # the real writer is what closes the gap, so we feed it the same map and let
    # it decide which dir gets the real block.
    relevance_owner = next((m for m in modes if m in rs._RELEVANCE_MODES), None)
    assert relevance_owner == "ii-b"
    usage_owners = {"grader": modes[0], "reassess": modes[0],
                    "relevance": relevance_owner}

    relevance_payload = {"some": "payload", "usage": relevance_usage}
    neuronpedia_payloads = {(11, 900): {"label": "x"}}
    config = _FakeConfig(relevance_payload=relevance_payload,
                         neuronpedia_payloads=neuronpedia_payloads)

    # One pin, one scale, shared across the modes (the union subset content does
    # not matter here, only the usage wiring does).
    selection_rows = [_selection_row(11, 900, 10)]
    measurement = {
        "layer": 11, "feature_idx": 900, "pos": 10, "scale": -3.0,
        "shift_bucket": "shifted", "answer_after": "topic surfaced",
        "baseline": 12.0, "new_value": 0.0,
        "usability": 0.7, "plausibility": 0.7, "overall": 0.7,
        "usability_std": 0.0, "plausibility_std": 0.0, "n_repeats": 5,
    }
    grades = {
        "grader_model": "openai/gpt-5.4", "question": "q", "n_repeats": 5,
        "baseline": {"answer": "base", "overall": 0.05},
        "ranking": [], "top1": None, "usage": grader_usage,
    }
    sweep_result = {"n_scales": 4, "reassess_usage": reassess_usage}

    written = {}
    for mode in modes:
        record = {
            "datetime": f"2026-06-12T00-00-0{modes.index(mode)}",
            "slug": "tiananmen-massacre", "mode": mode,
            "baseline_answer": "base",
            "selection": [dict(r, rank=0) for r in selection_rows],
        }
        run_dir = rs._write_run_dir(
            out_root=str(tmp_path),
            mode=mode,
            slug="tiananmen-massacre",
            record=record,
            ranked=[_FakeCand(11, 900, 10)],   # len() for n_features, .pin_key for seed.json
            sweep_result=sweep_result,
            stage_measurements=[dict(measurement)],
            stage_reassess={},
            grades=grades,
            config=config,
            graph_path=str(tmp_path / "graph.pt"),
            report_text="# report\n",
            pre_timings={},
            stage_timings={},
            usage_owners=usage_owners,
        )
        written[mode] = Path(run_dir)

    def _block(mode, fname):
        return json.loads((written[mode] / fname).read_text())

    # Grader: written in every dir. Sum over all four equals the true bill.
    grader_blocks = [_block(m, "grades.json")["usage"] for m in modes]
    grader_total = sum(saving.compute_cost(b) for b in grader_blocks)
    assert grader_total == true_grader
    grader_real = [b for b in grader_blocks if saving.compute_cost(b) > 0]
    assert len(grader_real) == 1
    assert _block(modes[0], "grades.json")["usage_amortized_from"] is None
    assert _block(modes[1], "grades.json")["usage_amortized_from"] == modes[0]

    # Reassess: written in every dir.
    reassess_blocks = [_block(m, "reassess.json")["usage"] for m in modes]
    reassess_total = sum(saving.compute_cost(b) for b in reassess_blocks)
    assert reassess_total == true_reassess
    assert len([b for b in reassess_blocks if saving.compute_cost(b) > 0]) == 1
    assert _block(modes[0], "reassess.json")["usage_amortized_from"] is None
    assert _block(modes[3], "reassess.json")["usage_amortized_from"] == modes[0]

    # Relevance: written ONLY in the _RELEVANCE_MODES dirs (ii-b, iii-b here).
    rel_modes = [m for m in modes if m in rs._RELEVANCE_MODES]
    assert rel_modes == ["ii-b", "iii-b"]
    for m in modes:
        exists = (written[m] / "relevance.json").exists()
        assert exists == (m in rel_modes)
    rel_blocks = [_block(m, "relevance.json")["usage"] for m in rel_modes]
    rel_total = sum(saving.compute_cost(b) for b in rel_blocks)
    assert rel_total == true_relevance
    assert len([b for b in rel_blocks if saving.compute_cost(b) > 0]) == 1
    assert _block("ii-b", "relevance.json")["usage_amortized_from"] is None
    assert _block("iii-b", "relevance.json")["usage_amortized_from"] == "ii-b"

    # The grand total over EVERY shared usage block across all written artifacts
    # equals the sum of the three true bills (no double counting anywhere).
    grand_total = grader_total + reassess_total + rel_total
    assert grand_total == true_grader + true_reassess + true_relevance
