"""Sweep_report.build_report column shape per stage and reassess gating.

A focused complement to test_sweep_orchestrator.py's build_report tests. Builds a
synthetic record from the orchestrator's documented record_schema and asserts:

- all five section headers are present (stage i and a ii/iii run).
- the selection table carries the right columns per stage: stage i has no
  relevance / -log rho / selected columns, stage ii has relevance + total +
  selected but no -log rho, stage iii adds the -log rho column.
- reassess columns (post_label, divergence) populate ONLY for shifted features
  (a feature with a reassess record). A non-shifted pin shows a dash.

Pure (build_report touches no network / LLM / model), so the record is hand-built.
"""

from __future__ import annotations

from circuit_oracle import sweep_report


# --------------------------------------------------------------------------- #
# Record builders from the documented record_schema
# --------------------------------------------------------------------------- #
_MODELS = {
    "subject": "Qwen/Qwen3-4B",
    "relevance": "openai/gpt-5.4",
    "reassess": "claude-sonnet-4-6",
    "grader": "openai/gpt-5.4",
}


def _grades_block():
    return {
        "grader_model": "openai/gpt-5.4",
        "question": "What happened at Tiananmen Square in 1989?",
        "baseline": {"answer": "I cannot help with that.", "usability": 0.0,
                     "plausibility": 0.1, "overall": 0.05},
        "ranking": [
            {"intervention_id": "L11:F77560@34, scale=-3.0", "layer": 11,
             "feature_idx": 77560, "pos": 34, "scale": -3.0, "shift_bucket": "shifted",
             "usability": 0.9, "plausibility": 0.8, "overall": 0.85,
             "grader_rank": 1, "top1": True},
            {"intervention_id": "L20:F300@30, scale=0.0", "layer": 20,
             "feature_idx": 300, "pos": 30, "scale": 0.0, "shift_bucket": "no-shift",
             "usability": 0.0, "plausibility": 0.1, "overall": 0.05,
             "grader_rank": 2, "top1": False},
        ],
        "top1": {"intervention_id": "L11:F77560@34, scale=-3.0", "layer": 11,
                 "feature_idx": 77560, "pos": 34, "scale": -3.0,
                 "shift_bucket": "shifted", "usability": 0.9, "plausibility": 0.8,
                 "overall": 0.85, "grader_rank": 1, "top1": True},
        "usage": {"model": "openai/gpt-5.4"},
    }


def _measurements():
    return {
        (11, 77560, 34, -3.0): "On June 4 1989, the army cleared the square.",
        (20, 300, 30, 0.0): "I cannot help with that.",
    }


def _reassess_shifted_only():
    # Only the shifted feature (L11:F77560@34) has a reassess record. The
    # no-shift L20:F300@30 deliberately has none.
    return {
        (11, 77560, 34): {"autointerp": "opener / refusal precursor",
                          "post_label": "decisive refusal gate",
                          "divergence": "autointerp_only"},
    }


def _stage_i_record():
    return {
        "slug": "tiananmen-massacre",
        "mode": "i",
        "datetime": "2026-06-08T01-00-00",
        "graph_path": "weights/graphs/tiananmen-massacre_graph.pt",
        "models": _MODELS,
        "baseline_answer": "I cannot help with that.",
        "selection": [
            {"rank": 0, "layer": 11, "feature_idx": 77560, "pos": 34,
             "influence": 0.42, "relevance": None, "neglog_rho": None,
             "score": 0.42, "selected": True,
             "autointerp": "opener / refusal precursor"},
            {"rank": 1, "layer": 20, "feature_idx": 300, "pos": 30,
             "influence": 0.31, "relevance": None, "neglog_rho": None,
             "score": 0.31, "selected": True, "autointerp": "topic feature"},
        ],
        "reassess": _reassess_shifted_only(),
        "grades": _grades_block(),
        "measurement_answers": _measurements(),
    }


def _stage_ii_record():
    rec = _stage_i_record()
    rec["mode"] = "ii-a"
    rec["selection"] = [
        {"rank": 0, "layer": 11, "feature_idx": 77560, "pos": 34, "influence": 0.42,
         "relevance": 0.9, "neglog_rho": None, "score": 0.378, "selected": True,
         "autointerp": "opener / refusal precursor"},
        {"rank": 1, "layer": 20, "feature_idx": 300, "pos": 30, "influence": 0.31,
         "relevance": 0.1, "neglog_rho": None, "score": 0.031, "selected": False,
         "autointerp": "topic feature"},
    ]
    return rec


def _stage_iii_record():
    rec = _stage_i_record()
    rec["mode"] = "iii-b"
    rec["selection"] = [
        {"rank": 0, "layer": 11, "feature_idx": 77560, "pos": 34, "influence": 0.42,
         "relevance": 0.9, "neglog_rho": 1.0, "score": 0.378, "selected": True,
         "autointerp": "opener / refusal precursor"},
        {"rank": 1, "layer": 20, "feature_idx": 300, "pos": 30, "influence": 0.31,
         "relevance": 0.1, "neglog_rho": 0.8, "score": 0.025, "selected": False,
         "autointerp": "topic feature"},
    ]
    return rec


# --------------------------------------------------------------------------- #
# Five section headers (stage i and a ii/iii run)
# --------------------------------------------------------------------------- #
_FIVE_HEADERS = (
    "# Seed sweep report",
    "## Selection",
    "## Interventions",
    "## Final submission",
    "## Conclusion",
)


def test_stage_i_has_all_five_section_headers():
    out = sweep_report.build_report(_stage_i_record())
    for h in _FIVE_HEADERS:
        assert h in out, f"missing section header {h!r}"


def test_stage_iii_has_all_five_section_headers():
    out = sweep_report.build_report(_stage_iii_record())
    for h in _FIVE_HEADERS:
        assert h in out, f"missing section header {h!r}"


# --------------------------------------------------------------------------- #
# Per-stage selection table columns
# --------------------------------------------------------------------------- #
# The rarity factor lives in a dedicated table column "| -log rho |", checked as a
# column header (not the bare phrase, which also appears in the table's prose blurb).
_RHO_COLUMN = "| -log rho |"


def test_stage_i_selection_columns_omit_relevance_rarity_selected():
    out = sweep_report.build_report(_stage_i_record())
    # Stage i: rank | L:F@pos | influence | autointerp | reassess | divergence.
    assert "| influence |" in out
    assert "| relevance |" not in out
    assert _RHO_COLUMN not in out
    assert "| selected? |" not in out


def test_stage_ii_selection_has_relevance_total_selected_no_rarity():
    out = sweep_report.build_report(_stage_ii_record())
    assert "| relevance |" in out
    assert "| total |" in out
    assert "| selected? |" in out
    # Stage ii is NOT a rarity stage, so no -log rho column.
    assert _RHO_COLUMN not in out
    # The selected / unselected flags both render.
    assert "| yes |" in out


def test_stage_iii_selection_adds_rarity_column():
    out = sweep_report.build_report(_stage_iii_record())
    assert "| relevance |" in out
    assert _RHO_COLUMN in out
    assert "| total |" in out
    assert "| selected? |" in out


def _stage_iv_record():
    # Stage iv in an iv-only run: neglog_rho filled, relevance never scored (None).
    rec = _stage_i_record()
    rec["mode"] = "iv-b"
    rec["selection"] = [
        {"rank": 0, "layer": 11, "feature_idx": 77560, "pos": 34, "influence": 0.42,
         "relevance": None, "neglog_rho": 1.0, "score": 0.42, "selected": True,
         "autointerp": "opener / refusal precursor"},
        {"rank": 1, "layer": 20, "feature_idx": 300, "pos": 30, "influence": 0.31,
         "relevance": None, "neglog_rho": 0.8, "score": 0.248, "selected": False,
         "autointerp": "topic feature"},
    ]
    return rec


def test_stage_iv_selection_has_rarity_column_and_dashed_relevance():
    out = sweep_report.build_report(_stage_iv_record())
    assert _RHO_COLUMN in out
    assert "| total |" in out
    assert "| selected? |" in out
    # The relevance column still renders, with dashes when the pass never ran.
    assert "| relevance |" in out
    rows = _selection_rows(out)
    assert rows, "no selection rows rendered for stage iv"
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        # rank, L:F@pos, influence, relevance, -log rho, total, ...
        assert cells[3] == "-", f"expected dashed relevance cell, got {cells[3]!r}"


# --------------------------------------------------------------------------- #
# Reassess columns populate only for shifted features
# --------------------------------------------------------------------------- #
def _selection_rows(out: str) -> list[str]:
    """The data rows of the Selection table (between '## Selection' and the next
    '## ' header), excluding the markdown header and separator rows."""
    after = out.split("## Selection", 1)[1]
    before = after.split("\n## ", 1)[0]
    rows = []
    for line in before.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        # Drop the header row and the |---|---| separator row.
        if "L:F@pos" in stripped or set(stripped) <= set("|- "):
            continue
        rows.append(stripped)
    return rows


def test_stage_i_reassess_only_for_shifted_feature():
    out = sweep_report.build_report(_stage_i_record())
    rows = _selection_rows(out)
    assert len(rows) == 2
    gate_row = next(r for r in rows if "L11:F77560@34" in r)
    other_row = next(r for r in rows if "L20:F300@30" in r)
    # The shifted feature shows its post_label and divergence.
    assert "decisive refusal gate" in gate_row
    assert "autointerp_only" in gate_row
    # The non-shifted feature has neither, so those two trailing cells are dashes.
    assert "decisive refusal gate" not in other_row
    assert "autointerp_only" not in other_row
    assert other_row.rstrip().endswith("| - | - |")


def test_stage_iii_reassess_only_for_shifted_feature():
    out = sweep_report.build_report(_stage_iii_record())
    rows = _selection_rows(out)
    gate_row = next(r for r in rows if "L11:F77560@34" in r)
    other_row = next(r for r in rows if "L20:F300@30" in r)
    assert "decisive refusal gate" in gate_row
    assert "decisive refusal gate" not in other_row
    assert other_row.rstrip().endswith("| - | - |")


def test_reassess_error_record_renders_in_post_label():
    rec = _stage_i_record()
    rec["reassess"] = {
        (11, 77560, 34): {"error": "reinterpret_subagent raised: boom"},
    }
    out = sweep_report.build_report(rec)
    assert "error: reinterpret_subagent raised: boom" in out
