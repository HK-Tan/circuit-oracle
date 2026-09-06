# Tests for the Arditi-side post-hoc re-imputation path in baselines/arditi/llm_judge.py
# (`_reaggregate_row` / `run_reaggregate`, the no-API `--reaggregate` flag).
#
# These mirror the sweep-side reaggregation tests but cover the Arditi summary schema
# (baseline/ablated per-judge repeats + pooled aggregate). The point of the path: bring a
# settled judge_summary.json onto the current refusal-imputation rule without re-grading,
# so a row with no judge refusals comes back byte-identical and only refusal-affected rows
# move. No judge calls, no API key.
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


def _load_llm_judge():
    """Load baselines/arditi/llm_judge.py as an isolated module.

    The module inserts <repo>/src onto sys.path itself and computes RUNS_DIR from its own
    __file__, so spec-loading the real path resolves both correctly. Tests monkeypatch
    RUNS_DIR onto a tmp dir so the real summary is never touched.
    """
    repo = Path(__file__).resolve().parents[2]
    for p in (str(repo), str(repo / "src")):
        if p not in sys.path:
            sys.path.insert(0, p)
    path = repo / "baselines" / "arditi" / "llm_judge.py"
    spec = importlib.util.spec_from_file_location("arditi_llm_judge_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _g(u, p):
    # A judge repeat that actually scored the completion.
    return {"usability": u, "plausibility": p, "overall": round((u + p) / 2, 2)}


def _r():
    # A stored refused repeat carrying the pre-imputation flat (1,1) fill. The _refusal
    # marker survives in the artifact, which is what lets re-imputation re-find it.
    return {"usability": 1.0, "plausibility": 1.0, "overall": 1.0, "_refusal": True}


def _agg(overall):
    # A complete aggregate stub (the md renderer reads every axis key directly). Only
    # overall_mean is asserted on; the rest just need to be present so an out-of-scope
    # row still renders.
    return {"n_calls": 3, "n_refusals": 0, "n_judges": 3,
            "usability_mean": 1.0, "usability_std": 0.0,
            "plausibility_mean": overall, "plausibility_std": 0.0,
            "overall_mean": overall, "overall_std": 0.0, "overall_simple_std": 0.0}


def _row(slug, ablated_pj, baseline_pj=None):
    baseline_pj = baseline_pj or {m: [_g(0.0, 0.0)] for m in ablated_pj}
    return {
        "slug": slug,
        "baseline_per_judge_repeats": baseline_pj,
        "ablated_per_judge_repeats": ablated_pj,
        "baseline_per_judge_stats": {},
        "ablated_per_judge_stats": {},
        # Stale placeholders the reaggregation overwrites; the 0.667 marks the old laundered
        # value so an out-of-scope row is visibly left alone.
        "baseline_aggregate": _agg(0.0),
        "ablated_aggregate": _agg(0.667),
    }


J3 = ["anthropic/claude-opus-4.6", "google/gemini-3.5-flash", "x-ai/grok-4.3"]


def test_reaggregate_row_reimputes_refuser_from_graders():
    # opus + gemini graded (1,0) HALLUCINATED, grok refused with the stale flat (1,1).
    # Re-imputation drops grok to (1, mean grader plausibility = 0), so the pooled ablated
    # overall settles to the correct 0.5, not the laundered 0.667.
    mod = _load_llm_judge()
    row = _row("airport", {J3[0]: [_g(1.0, 0.0)], J3[1]: [_g(1.0, 0.0)], J3[2]: [_r()]})
    new = mod._reaggregate_row(row, J3)
    assert new["ablated_aggregate"]["overall_mean"] == 0.5
    assert new["ablated_aggregate"]["n_refusals"] == 1
    assert new["ablated_aggregate"]["n_judges"] == 3
    grok = new["ablated_per_judge_repeats"][J3[2]][0]
    assert grok["usability"] == 1.0 and grok["plausibility"] == 0.0
    assert new["ablated_per_judge_repeats"][J3[0]][0]["plausibility"] == 0.0  # grader untouched


def test_reaggregate_row_without_refusal_is_idempotent():
    mod = _load_llm_judge()
    row = _row("tibet", {J3[0]: [_g(1.0, 0.9)], J3[1]: [_g(1.0, 0.8)], J3[2]: [_g(1.0, 0.85)]})
    once = mod._reaggregate_row(row, J3)
    twice = mod._reaggregate_row(once, J3)
    assert once["ablated_aggregate"]["n_refusals"] == 0
    assert once["ablated_aggregate"] == twice["ablated_aggregate"]
    assert once["ablated_per_judge_stats"] == twice["ablated_per_judge_stats"]


def test_run_reaggregate_rewrites_summary_in_place_no_api(tmp_path, monkeypatch):
    mod = _load_llm_judge()
    monkeypatch.setattr(mod, "RUNS_DIR", str(tmp_path))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    summary = {
        "judges": [{"model": m, "provider": "openrouter"} for m in J3],
        "n_repeats": 5, "temperature": 1.0,
        "rows": [_row("airport-bomb-smuggling",
                      {J3[0]: [_g(1.0, 0.0)], J3[1]: [_g(1.0, 0.0)], J3[2]: [_r()]})],
    }
    (tmp_path / "judge_summary.json").write_text(json.dumps(summary))
    args = type("Args", (), dict(slugs=None, category=None))()
    mod.run_reaggregate(args)

    out = json.loads((tmp_path / "judge_summary.json").read_text())
    assert out["rows"][0]["ablated_aggregate"]["overall_mean"] == 0.5
    assert out["rows"][0]["ablated_aggregate"]["n_refusals"] == 1
    assert out["n_repeats"] == 5          # top-level metadata taken from the file, not args
    assert (tmp_path / "judge_summary.md").exists()


def test_run_reaggregate_slug_filter_leaves_others_untouched(tmp_path, monkeypatch):
    mod = _load_llm_judge()
    monkeypatch.setattr(mod, "RUNS_DIR", str(tmp_path))
    summary = {
        "judges": [{"model": m, "provider": "openrouter"} for m in J3],
        "n_repeats": 1, "temperature": 1.0,
        "rows": [
            _row("airport-bomb-smuggling",
                 {J3[0]: [_g(1.0, 0.0)], J3[1]: [_g(1.0, 0.0)], J3[2]: [_r()]}),
            _row("molotov-cocktail",
                 {J3[0]: [_g(1.0, 0.9)], J3[1]: [_g(1.0, 0.9)], J3[2]: [_g(1.0, 0.9)]}),
        ],
    }
    (tmp_path / "judge_summary.json").write_text(json.dumps(summary))
    args = type("Args", (), dict(slugs=["molotov-cocktail"], category=None))()
    mod.run_reaggregate(args)

    rows = {r["slug"]: r for r in json.loads((tmp_path / "judge_summary.json").read_text())["rows"]}
    # out of scope -> the stored placeholder aggregate is preserved verbatim
    assert rows["airport-bomb-smuggling"]["ablated_aggregate"]["overall_mean"] == 0.667
    # in scope, no refusal -> reaggregated to the real pooled value
    assert rows["molotov-cocktail"]["ablated_aggregate"]["overall_mean"] == 0.95


def test_run_reaggregate_no_file_fails_loud(tmp_path, monkeypatch):
    mod = _load_llm_judge()
    monkeypatch.setattr(mod, "RUNS_DIR", str(tmp_path))     # empty, no judge_summary.json
    args = type("Args", (), dict(slugs=None, category=None))()
    with pytest.raises(SystemExit):
        mod.run_reaggregate(args)
