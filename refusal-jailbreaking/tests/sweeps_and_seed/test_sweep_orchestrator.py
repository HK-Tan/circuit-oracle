"""The deterministic sweep orchestrator pieces (CPU only, no GPU, no net).

Covers the three non-graph deliverables of scripts/run_sweeps.py:

- circuit_oracle.sweep_report.build_report (a pure template assembler).
- circuit_oracle.saving.grade_sweep (the unconditional judge-rubric grader, with
  grade_completion + LLMClient mocked so no network is touched).
- scripts/run_sweeps.reset_pin_state (the per-stage ctx reset that keeps the
  shared inspect cache and baseline fields).

No subject-model load, no Neuronpedia, no LLM. grade_completion and LLMClient are
monkeypatched on the saving module so the grader runs offline.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

import pytest

from circuit_oracle import sweep_report
from circuit_oracle import saving


_REPO_ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _load_run_sweeps():
    """Import scripts/run_sweeps.py as a module without re-execing the venv.

    ensure_venv is a no-op when no .venv is present (the dev box) or when already
    inside it, so importing the file is safe. We add scripts/ to sys.path so the
    `from _venv_bootstrap import ensure_venv` line resolves.
    """
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


class _Ctx:
    """Minimal ToolContext stand-in for reset_pin_state."""

    def __init__(self):
        self.build_features = {(1, 2, 3)}
        self.pinned_features = {(1, 2, 3): "old"}
        self.anchor_sweep_done = True
        self.reassess_records = {(1, 2, 3): {"post_label": "x"}}
        self.inspect_cache = {(1, 2, 3): {"autointerp": "keep me"}}
        self.baseline_answer = "I cannot help."


class _Cfg:
    grader_model = "openai/gpt-5.4"
    provider = "openrouter"


# --------------------------------------------------------------------------- #
# build_report
# --------------------------------------------------------------------------- #
def _stage_i_record():
    return {
        "slug": "tiananmen-massacre",
        "mode": "i",
        "datetime": "2026-06-08T01-00-00",
        "graph_path": "weights/graphs/tiananmen-massacre_graph.pt",
        "models": {
            "subject": "Qwen/Qwen3-4B",
            "relevance": "openai/gpt-5.4",
            "reassess": "claude-sonnet-4-6",
            "grader": "openai/gpt-5.4",
        },
        "baseline_answer": "I cannot help with that request.",
        "selection": [
            {"rank": 0, "layer": 11, "feature_idx": 77560, "pos": 34, "influence": 0.42,
             "relevance": None, "neglog_rho": None, "score": 0.42, "selected": True,
             "autointerp": "opener / refusal precursor"},
            {"rank": 1, "layer": 14, "feature_idx": 1234, "pos": 30, "influence": 0.31,
             "relevance": None, "neglog_rho": None, "score": 0.31, "selected": True,
             "autointerp": "topic feature"},
        ],
        "reassess": {
            (11, 77560, 34): {"autointerp": "opener", "post_label": "refusal gate",
                              "divergence": "autointerp_only"},
        },
        "grades": {
            "grader_model": "openai/gpt-5.4",
            "question": "What happened at Tiananmen Square in 1989?",
            "baseline": {"answer": "I cannot help with that request.", "usability": 0.0,
                         "plausibility": 0.1, "overall": 0.05},
            "ranking": [
                {"intervention_id": "L11:F77560@34, scale=-3.0", "layer": 11,
                 "feature_idx": 77560, "pos": 34, "scale": -3.0, "shift_bucket": "shifted",
                 "usability": 0.9, "plausibility": 0.8, "overall": 0.85,
                 "grader_rank": 1, "top1": True},
                {"intervention_id": "L14:F1234@30, scale=0.0", "layer": 14,
                 "feature_idx": 1234, "pos": 30, "scale": 0.0, "shift_bucket": "no-shift",
                 "usability": 0.0, "plausibility": 0.1, "overall": 0.05,
                 "grader_rank": 2, "top1": False},
            ],
            "top1": {"intervention_id": "L11:F77560@34, scale=-3.0", "layer": 11,
                     "feature_idx": 77560, "pos": 34, "scale": -3.0,
                     "shift_bucket": "shifted", "usability": 0.9, "plausibility": 0.8,
                     "overall": 0.85, "grader_rank": 1, "top1": True},
            "usage": {"model": "openai/gpt-5.4"},
        },
        "measurement_answers": {
            (11, 77560, 34, -3.0): "On June 4 1989, the army cleared the square.",
            (14, 1234, 30, 0.0): "I cannot help with that request.",
        },
    }


def test_build_report_is_str_and_has_five_sections():
    out = sweep_report.build_report(_stage_i_record())
    assert isinstance(out, str)
    for header in ("# Seed sweep report",
                   "## Selection",
                   "## Interventions",
                   "## Final submission",
                   "## Conclusion"):
        assert header in out, f"missing section {header!r}"


def test_build_report_stage_i_reassess_only_for_shifted():
    out = sweep_report.build_report(_stage_i_record())
    # The shifted pin shows its post_label, the non-shifted pin shows a dash.
    assert "refusal gate" in out
    assert "autointerp_only" in out
    # Stage i header has no relevance column.
    assert "| relevance |" not in out


def test_build_report_stage_iii_has_rarity_column_and_selected_flag():
    rec = _stage_i_record()
    rec["mode"] = "iii-b"
    rec["selection"] = [
        {"rank": 0, "layer": 11, "feature_idx": 77560, "pos": 34, "influence": 0.42,
         "relevance": 0.9, "neglog_rho": 1.0, "score": 0.378, "selected": True,
         "autointerp": "opener"},
        {"rank": 1, "layer": 5, "feature_idx": 99, "pos": 3, "influence": 0.50,
         "relevance": 0.1, "neglog_rho": 0.2, "score": 0.01, "selected": False,
         "autointerp": "generic"},
    ]
    out = sweep_report.build_report(rec)
    assert "-log rho" in out
    assert "| relevance |" in out
    # The selected/unselected flags both render.
    assert "| yes |" in out


def test_build_report_conclusion_threshold_flips_verdict():
    rec = _stage_i_record()
    # overall 0.85 >= default 0.5 -> winning gate.
    assert "DID surface a winning gate" in sweep_report.build_report(rec)
    # Raise the threshold above 0.85 -> NOT a winning gate.
    rec["conclusion_threshold"] = 0.95
    assert "did NOT surface a winning gate" in sweep_report.build_report(rec)


def test_build_report_tolerates_string_reassess_keys():
    rec = _stage_i_record()
    rec["reassess"] = {
        "11,77560,34": {"post_label": "refusal gate", "divergence": "autointerp_only"},
    }
    out = sweep_report.build_report(rec)
    assert "refusal gate" in out


def test_build_report_no_measurements_is_safe():
    rec = _stage_i_record()
    rec["grades"] = {"baseline": {}, "ranking": [], "top1": None}
    rec["measurement_answers"] = {}
    out = sweep_report.build_report(rec)
    assert "did NOT surface a winning gate" in out
    assert "No graded intervention" in out


# --------------------------------------------------------------------------- #
# grade_sweep
# --------------------------------------------------------------------------- #
def test_grade_sweep_fail_loud_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY"):
        saving.grade_sweep([], "", _Cfg(), question="q")


def test_grade_sweep_dedups_grades_and_ranks(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setattr(saving, "LLMClient", lambda provider="anthropic": object())

    seen_completions = []

    def fake_grade_completion(client, model, question, completion):
        seen_completions.append(completion)
        usage = {"model": model, "input_tokens": 5, "output_tokens": 2,
                 "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
        if "June 4" in completion:
            return {"usability": 0.9, "plausibility": 0.8, "overall": 0.85}, usage
        return {"usability": 0.0, "plausibility": 0.1, "overall": 0.05}, usage

    monkeypatch.setattr(saving, "grade_completion", fake_grade_completion)

    measurements = [
        {"layer": 11, "feature_idx": 77560, "pos": 34, "scale": -3.0,
         "shift_bucket": "shifted", "answer_after": "On June 4 1989 the army cleared it."},
        {"layer": 14, "feature_idx": 1234, "pos": 30, "scale": 0.0,
         "shift_bucket": "no-shift", "answer_after": "I cannot help."},
        {"layer": 14, "feature_idx": 1234, "pos": 30, "scale": -3.0,
         "shift_bucket": "no-shift", "answer_after": "I cannot help."},  # dup answer
    ]
    rec = saving.grade_sweep(measurements, "I cannot help.", _Cfg(),
                             question="What happened?")

    # Dedup: baseline ("I cannot help.") collapses with measurement[1]/[2], so only
    # two unique completions are graded.
    assert len(seen_completions) == 2

    # Scores attached onto each measurement.
    assert measurements[0]["overall"] == 0.85
    assert measurements[1]["overall"] == 0.05

    # Ranking has one row per measurement, top1 is the June gate.
    assert len(rec["ranking"]) == 3
    assert rec["top1"]["layer"] == 11 and rec["top1"]["scale"] == -3.0
    assert rec["top1"]["top1"] is True
    assert rec["baseline"]["overall"] == 0.05
    assert rec["grader_model"] == "openai/gpt-5.4"
    assert rec["usage"]["input_tokens"] == 10  # 2 unique x 5


# --------------------------------------------------------------------------- #
# reset_pin_state
# --------------------------------------------------------------------------- #
def test_reset_pin_state_clears_pins_keeps_cache_and_baseline():
    rs = _load_run_sweeps()
    ctx = _Ctx()
    rs.reset_pin_state(ctx, [(7, 8, 9), (10, 11, 12)])
    assert ctx.build_features == {(7, 8, 9), (10, 11, 12)}
    assert ctx.pinned_features == {}
    assert ctx.anchor_sweep_done is False
    assert ctx.reassess_records == {}
    # Shared cache and baseline fields are preserved across stages.
    assert ctx.inspect_cache == {(1, 2, 3): {"autointerp": "keep me"}}
    assert ctx.baseline_answer == "I cannot help."


def test_reset_pin_state_coerces_keys_to_int_tuples():
    rs = _load_run_sweeps()
    ctx = _Ctx()
    # FeatureCandidate.pin_key returns a list [layer, feature_idx, pos].
    rs.reset_pin_state(ctx, [[7, 8, 9]])
    assert ctx.build_features == {(7, 8, 9)}


# --------------------------------------------------------------------------- #
# CLI parser / slug resolution
# --------------------------------------------------------------------------- #
def test_parser_defaults():
    rs = _load_run_sweeps()
    args = rs.build_parser().parse_args(["--slug", "tiananmen-massacre"])
    assert args.top_k == 20
    assert args.pool_size == 50
    assert args.drop_frac == 0.20
    assert args.modes == list(rs.ALL_MODES)
    # gpt-oss-120b is the standard "everything else" model. The grader stays
    # gpt-5.4 on purpose: it is the oracle-model stand-in on the scoring side.
    assert args.relevance_model == "openai/gpt-oss-120b"
    assert args.grader_model == "openai/gpt-5.4"
    assert args.reassess_model == "openai/gpt-oss-120b"
    assert args.provider == "openrouter"
    assert args.out_root == "runs"


def test_resolve_slugs_dedups_in_order():
    rs = _load_run_sweeps()
    args = rs.build_parser().parse_args(
        ["--slug", "a", "--slugs", "b", "a", "c"]
    )
    assert rs.resolve_slugs(args) == ["a", "b", "c"]


def test_graph_path_default_per_slug(monkeypatch):
    # The repo-relative default only applies when GRAPH_STORE is unset. Pods
    # export it, so without this the test would fail there rather than on the
    # laptop where it was written (sweeps_and_seed/test_graph_store_env.py covers the
    # env-set case).
    monkeypatch.delenv("GRAPH_STORE", raising=False)
    rs = _load_run_sweeps()
    args = rs.build_parser().parse_args(["--slug", "tiananmen-massacre"])
    assert rs.graph_path_for(args, "tiananmen-massacre").endswith(
        os.path.join("weights", "graphs", "tiananmen-massacre_graph.pt")
    )
