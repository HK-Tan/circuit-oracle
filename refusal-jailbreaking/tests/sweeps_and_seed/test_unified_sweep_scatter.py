"""Unified cross-stage sweep scatter-back (CPU only, no network).

Covers the Part-2 orchestration helpers in scripts/run_sweeps.py that scatter
ONE shared union sweep / grade pass back into each stage's artifacts:

  - _subset_measurements keeps only a stage's own pins and keeps double-position
    pins of the same feature distinct,
  - _subset_reassess filters the union reassess records (tuple-keyed) to a stage,
  - _stage_grades re-ranks the grader WITHIN one stage's subset (grader_rank /
    top1 are per-stage and never leak across stages),
  - _amortize_block applies the usage-amortization rule (owner keeps the real
    block, later dirs get a zeroed copy pointing at the owner) and the
    sum-over-artifacts cost invariant holds.

All helpers operate on plain dicts, so no model, no GPU, and no network.
"""
from __future__ import annotations

import importlib.util
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


def _union_measurements():
    """A small union: feature A at two positions (double pin) plus feature B.

    Each origin (layer, feature_idx, pos, scale) has its OWN dict (part 1's
    share-vs-copy contract), carrying the grade fields a shared grade_sweep pass
    would have attached.
    """
    rows = []
    # Feature A pinned at pos 34 and pos 26 (double-position pin of the same
    # feature). Two scales each for brevity.
    for pos in (34, 26):
        for scale, overall in ((0.0, 0.20), (-3.0, 0.90)):
            rows.append({
                "layer": 11, "feature_idx": 77560, "pos": pos, "scale": scale,
                "baseline": 12.0, "new_value": 0.0 if scale == 0.0 else -34.0,
                "shift_bucket": "shifted" if scale == -3.0 else "no-shift",
                "answer_after": f"A@{pos} s{scale}",
                "usability": overall, "plausibility": overall,
                "overall": overall, "usability_std": 0.01,
                "plausibility_std": 0.01, "n_repeats": 5,
            })
    # Feature B pinned at pos 30, one of its scales scores highest overall.
    for scale, overall in ((0.0, 0.10), (-3.0, 0.95)):
        rows.append({
            "layer": 14, "feature_idx": 1234, "pos": 30, "scale": scale,
            "baseline": 8.0, "new_value": 0.0 if scale == 0.0 else -20.0,
            "shift_bucket": "shifted" if scale == -3.0 else "no-shift",
            "answer_after": f"B s{scale}",
            "usability": overall, "plausibility": overall,
            "overall": overall, "usability_std": 0.02,
            "plausibility_std": 0.02, "n_repeats": 5,
        })
    return rows


def test_subset_measurements_keeps_double_position_pins_distinct():
    rs = _load_run_sweeps()
    union = _union_measurements()

    # Stage that selected ONLY feature A at pos 34 (not pos 26) and feature B.
    selected = {(11, 77560, 34), (14, 1234, 30)}
    subset = rs._subset_measurements(union, selected)

    # A@34 (2 scales) + B (2 scales) = 4 rows, A@26 dropped.
    assert len(subset) == 4
    positions = {(m["layer"], m["feature_idx"], m["pos"]) for m in subset}
    assert positions == {(11, 77560, 34), (14, 1234, 30)}
    # The returned dicts are the SAME objects as in the union (not copies), so a
    # shared grade pass's in-place fields are visible.
    assert subset[0] is union[0]


def test_subset_measurements_returns_distinct_objects_across_stages():
    rs = _load_run_sweeps()
    union = _union_measurements()
    stage_a = rs._subset_measurements(union, {(11, 77560, 34)})
    stage_b = rs._subset_measurements(union, {(11, 77560, 26)})
    # Disjoint pins -> disjoint dict objects, so a per-stage grader_rank stamp on
    # one stage's ranking rows never reaches the other.
    a_ids = {id(m) for m in stage_a}
    b_ids = {id(m) for m in stage_b}
    assert a_ids.isdisjoint(b_ids)


def test_subset_reassess_filters_by_stage_pins():
    rs = _load_run_sweeps()
    union_reassess = {
        (11, 77560, 34): {"post_label": "refusal opener", "divergence": "low"},
        (11, 77560, 26): {"post_label": "refusal opener", "divergence": "low"},
        (14, 1234, 30): {"post_label": "topic", "divergence": "high"},
    }
    selected = {(11, 77560, 34), (14, 1234, 30)}
    subset = rs._subset_reassess(union_reassess, selected)
    assert set(subset.keys()) == {(11, 77560, 34), (14, 1234, 30)}
    # String-keyed unions are coerced to int tuples before the membership test.
    str_keyed = {"11,77560,34": {"post_label": "x"}, "11,77560,26": {"post_label": "y"}}
    subset2 = rs._subset_reassess(str_keyed, {(11, 77560, 34)})
    assert list(subset2.keys()) == ["11,77560,34"]


def test_stage_grades_reranks_within_subset():
    rs = _load_run_sweeps()
    union = _union_measurements()
    union_grades = {
        "grader_model": "openai/gpt-5.4",
        "question": "What happened?",
        "n_repeats": 5,
        "baseline": {"answer": "I cannot help.", "usability": 0.05,
                     "plausibility": 0.05, "overall": 0.05,
                     "usability_std": 0.0, "plausibility_std": 0.0},
        "ranking": [],  # union ranking is global, ignored by the per-stage rebuild
        "top1": None,
        "usage": {"model": "openai/gpt-5.4", "input_tokens": 30,
                  "output_tokens": 12, "cache_read_input_tokens": 0,
                  "cache_creation_input_tokens": 0},
    }

    # Stage A-only subset: A@34 two scales. Its own top-1 is the -3.0 scale (0.90),
    # NOT feature B (0.95) which belongs to a different stage.
    stage_a = rs._subset_measurements(union, {(11, 77560, 34)})
    grades_a = rs._stage_grades(union_grades, stage_a, n_repeats=5)
    assert len(grades_a["ranking"]) == 2
    assert grades_a["top1"]["grader_rank"] == 1
    assert grades_a["top1"]["overall"] == 0.90
    assert grades_a["top1"]["feature_idx"] == 77560
    # Shared blocks pass through unchanged.
    assert grades_a["baseline"]["overall"] == 0.05
    assert grades_a["n_repeats"] == 5
    assert grades_a["usage"]["input_tokens"] == 30

    # Stage B-only subset: its own top-1 is B at -3.0 (0.95).
    stage_b = rs._subset_measurements(union, {(14, 1234, 30)})
    grades_b = rs._stage_grades(union_grades, stage_b, n_repeats=5)
    assert grades_b["top1"]["feature_idx"] == 1234
    assert grades_b["top1"]["overall"] == 0.95

    # The two stages each have an independent grader_rank 1 (no leak).
    a_ranks = {r["grader_rank"] for r in grades_a["ranking"]}
    b_ranks = {r["grader_rank"] for r in grades_b["ranking"]}
    assert 1 in a_ranks and 1 in b_ranks


def test_stage_grades_ranking_rows_carry_join_keys_and_std():
    rs = _load_run_sweeps()
    union = _union_measurements()
    union_grades = {
        "grader_model": "m", "question": "q", "n_repeats": 5,
        "baseline": {}, "ranking": [], "top1": None, "usage": {},
    }
    stage = rs._subset_measurements(union, {(14, 1234, 30)})
    grades = rs._stage_grades(union_grades, stage, n_repeats=5)
    row = grades["ranking"][0]
    # The report joins ranking -> measurement_answers on these four keys.
    for k in ("layer", "feature_idx", "pos", "scale"):
        assert k in row
    assert "usability_std" in row and "plausibility_std" in row
    assert "shift_bucket" in row


def test_amortize_block_owner_vs_later():
    rs = _load_run_sweeps()
    real = {"model": "openai/gpt-5.4", "input_tokens": 1000, "output_tokens": 500,
            "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}

    # Owner stage keeps the real block, marker None.
    block, marker = rs._amortize_block(real, mode="i", usage_owner="i")
    assert block is real
    assert marker is None

    # A later stage gets a zeroed copy pointing at the owner.
    block2, marker2 = rs._amortize_block(real, mode="ii-b", usage_owner="i")
    assert marker2 == "i"
    assert block2["model"] == "openai/gpt-5.4"
    assert block2["input_tokens"] == 0
    assert block2["output_tokens"] == 0
    # The real block was not mutated.
    assert real["input_tokens"] == 1000


def test_amortization_cost_invariant_over_artifacts():
    """Summing compute_cost over every stage dir's copy equals the true bill."""
    rs = _load_run_sweeps()
    real = {"model": "openai/gpt-5.4", "input_tokens": 4000, "output_tokens": 2000,
            "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    true_cost = saving.compute_cost(real)
    assert true_cost > 0

    modes = ["i", "ii-b", "iii-b", "iv-b"]
    owner = modes[0]
    total = 0.0
    for mode in modes:
        block, _marker = rs._amortize_block(real, mode=mode, usage_owner=owner)
        cost = saving.compute_cost(block)
        # Every block prices (never None), so no artifact is silently dropped.
        assert cost is not None
        total += cost
    assert total == true_cost


def test_relevance_owner_is_first_relevance_mode_not_modes_zero():
    """The relevance block owner must be a stage that WRITES relevance.json.

    When modes[0] is stage i (no relevance.json), assigning the relevance block
    to modes[0] would write the real block nowhere. The owner is instead the
    first _RELEVANCE_MODES stage, and the invariant still holds over the dirs
    that actually carry a relevance.json (ii/iii).
    """
    rs = _load_run_sweeps()
    modes = ["i", "ii-b", "iii-b", "iv-b"]
    relevance_owner = next((m for m in modes if m in rs._RELEVANCE_MODES), None)
    # Stage i is modes[0] but is NOT the relevance owner.
    assert relevance_owner == "ii-b"
    assert relevance_owner != modes[0]

    real = {"model": "openai/gpt-5.4", "input_tokens": 3000, "output_tokens": 1000,
            "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    true_cost = saving.compute_cost(real)

    # Only ii-b and iii-b write relevance.json. Sum over THOSE dirs.
    total = 0.0
    for mode in ("ii-b", "iii-b"):
        block, marker = rs._amortize_block(real, mode=mode, usage_owner=relevance_owner)
        if mode == relevance_owner:
            assert marker is None
        else:
            assert marker == relevance_owner
        total += saving.compute_cost(block)
    assert total == true_cost
