"""The shared traversal-stability aggregator.

Synthetic fixtures pin the math and the grouping rules. Two live tests then run
discovery over the real archived artifacts, so the parser meets real schemas
here rather than mid-run.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import aggregate_stability as agg  # noqa: E402  (path set above)


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------

def make_run(
    root: Path,
    slug: str,
    run_name: str,
    *,
    pass_index=None,
    pinned=None,
    inspected=(),
    n_extra_calls: int = 0,
    flagged=None,
    dominant=None,
    top1=None,
    top1_overall=None,
) -> Path:
    run_dir = root / slug / run_name
    run_dir.mkdir(parents=True)

    tool_calls = [
        {"tool": "inspect_feature", "input": {"layer": l, "feature_idx": f}, "output": "x"}
        for l, f in inspected
    ]
    tool_calls += [{"tool": "get_top_features", "input": {}, "output": []}] * n_extra_calls
    (run_dir / "oracle_result.json").write_text(json.dumps({
        "pass_index": pass_index,
        "tool_calls": tool_calls,
    }))

    if pinned is not None:
        (run_dir / "pinned_ids.json").write_text(json.dumps({
            "pinnedIds": [f"{l}_{f}_{p}" for l, f, p in pinned],
        }))

    if flagged is not None or dominant is not None:
        spurious, causal = flagged or ((), ())
        (run_dir / "judge_feature_counts.json").write_text(json.dumps({
            "spurious_features": [{"id": f"L{l}:F{f}"} for l, f in spurious],
            "causal_features": [{"id": f"L{l}:F{f}"} for l, f in causal],
            "dominant": dominant,
        }))

    if top1 is not None:
        if len(top1) == 1:
            (l, f), = top1
            iv = {"type": "single", "layer": l, "position": 0, "feature_idx": f, "scale": -2}
        else:
            iv = {"type": "supernode",
                  "features": [{"layer": l, "position": 0, "feature_idx": f} for l, f in top1]}
        (run_dir / "judge_scores.json").write_text(json.dumps({
            "best_intervention": {
                "intervention": iv,
                "aggregate": {"overall_mean": top1_overall},
            },
        }))
    return run_dir


# ---------------------------------------------------------------------------
# Parsers and math
# ---------------------------------------------------------------------------

def test_parse_pinned_drops_positions_and_pseudo_nodes(tmp_path: Path) -> None:
    p = tmp_path / "pinned_ids.json"
    p.write_text(json.dumps({"pinnedIds": [
        "-1_-1_29", "-1_-1_23",      # token pseudo-nodes, dropped
        "0_4958_29", "0_4958_23",    # one feature at two positions, one entry
        "13_3295_29",
    ]}))
    assert agg.parse_pinned(p) == {(0, 4958), (13, 3295)}


def test_parse_pinned_drops_logit_node_at_n_layers(tmp_path: Path) -> None:
    """Pseudo-nodes sit at BOTH ends of the layer range.

    Token nodes are negative and were already dropped. The logit/probe node is
    encoded as layer == n_layers (26_0 on gemma-2-2b, which has layers 0..25)
    and was being counted as a real transcoder feature.
    """
    p = tmp_path / "pinned_ids.json"
    p.write_text(json.dumps({"pinnedIds": [
        "-1_-1_29",      # token pseudo-node, dropped either way
        "0_4958_29",
        "25_77_3",       # last REAL layer, must survive
        "26_0_0",        # logit/probe pseudo-node, one past the end
    ]}))
    # Without n_layers the old behaviour is preserved, so a caller that does not
    # know the subject depth does not silently over-filter.
    assert agg.parse_pinned(p) == {(0, 4958), (25, 77), (26, 0)}
    # With it, the upper pseudo-node goes and the boundary layer stays.
    assert agg.parse_pinned(p, n_layers=26) == {(0, 4958), (25, 77)}


def test_jaccard_and_empty_convention() -> None:
    assert agg.jaccard({1, 2}, {2, 3}) == pytest.approx(1 / 3)
    assert agg.jaccard(set(), set()) == 1.0
    assert agg.jaccard({1}, set()) == 0.0


def test_band_identity_thirds() -> None:
    feats = {(0, 1), (11, 2), (12, 3), (23, 4), (24, 5), (35, 6)}
    assert agg.to_bands(feats, 36) == {0, 1, 2}
    assert agg.to_bands({(11, 1)}, 36) == {0}
    assert agg.to_bands({(12, 1)}, 36) == {1}
    assert agg.to_bands({(24, 1)}, 36) == {2}
    # 26-layer subject (probes): 8 and 9 straddle the first cut
    assert agg.to_bands({(8, 1)}, 26) == {0}
    assert agg.to_bands({(9, 1)}, 26) == {1}


def test_sample_sd_matches_hand_value() -> None:
    assert agg.sample_sd([1.0, 2.0, 3.0]) == pytest.approx(1.0)
    assert agg.sample_sd([4.0]) is None


def test_parse_flagged_excludes_pseudo_nodes_with_count() -> None:
    d = {
        "spurious_features": [{"id": "L0:F4958"}, {"id": "Emb: 'His' (pos 1)"}],
        "causal_features": [{"id": "L5:F14591"}, {"id": "Probe Classification Score"}],
        "dominant": "spurious",
    }
    spurious, causal, dominant, n_skipped = agg.parse_flagged(d)
    assert spurious == {(0, 4958)}
    assert causal == {(5, 14591)}
    assert dominant == "spurious"
    assert n_skipped == 2


def test_top1_single_and_supernode() -> None:
    single = {"best_intervention": {"intervention":
              {"type": "single", "layer": 24, "position": 35, "feature_idx": 91636, "scale": -2}}}
    assert agg.top1_features(single) == frozenset({(24, 91636)})
    sup = {"best_intervention": {"intervention":
           {"type": "supernode", "features": [
               {"layer": 24, "position": 35, "feature_idx": 91636},
               {"layer": 17, "position": 35, "feature_idx": 83241}]}}}
    assert agg.top1_features(sup) == frozenset({(24, 91636), (17, 83241)})
    assert agg.top1_features({}) is None


# ---------------------------------------------------------------------------
# Grouping rules
# ---------------------------------------------------------------------------

def test_duplicate_pass_index_keeps_latest(tmp_path: Path) -> None:
    make_run(tmp_path, "exp-s-a", "o_s_2026-01-01T00-00-00_pass1",
             pass_index=1, pinned=[(5, 100, 0)])
    make_run(tmp_path, "exp-s-a", "o_s_2026-01-02T00-00-00_pass1",
             pass_index=1, pinned=[(5, 200, 0)])
    warnings: list[str] = []
    groups = agg.discover_runs(tmp_path, warnings)
    assert len(groups["exp-s-a"]) == 1
    assert groups["exp-s-a"][0].pinned == {(5, 200)}
    assert any("duplicate pass 1" in w for w in warnings)


def test_pass_index_from_result_beats_dirname(tmp_path: Path) -> None:
    make_run(tmp_path, "exp-s-b", "o_s_2026-01-01T00-00-00_pass3", pass_index=2)
    warnings: list[str] = []
    groups = agg.discover_runs(tmp_path, warnings)
    assert groups["exp-s-b"][0].pass_index == 2


def test_unindexed_runs_warn_and_order_by_name(tmp_path: Path) -> None:
    make_run(tmp_path, "exp-s-c", "o_s_2026-01-02T00-00-00", pinned=[(1, 1, 0)])
    make_run(tmp_path, "exp-s-c", "o_s_2026-01-01T00-00-00", pinned=[(1, 2, 0)])
    warnings: list[str] = []
    groups = agg.discover_runs(tmp_path, warnings)
    assert [r.run_dir.name for r in groups["exp-s-c"]] == [
        "o_s_2026-01-01T00-00-00", "o_s_2026-01-02T00-00-00"]
    assert any("no pass indices" in w for w in warnings)


# ---------------------------------------------------------------------------
# End-to-end aggregation
# ---------------------------------------------------------------------------

def test_refusal_aggregation_hand_computed(tmp_path: Path) -> None:
    """3 passes, every number below is hand-derivable."""
    common = dict(inspected=[(10, 1), (11, 2)], n_extra_calls=3)
    make_run(tmp_path, "exp-s-x", "r1_pass1", pass_index=1,
             pinned=[(5, 100, 0), (10, 200, 0)], top1=[(5, 100)],
             top1_overall=0.6, **common)
    make_run(tmp_path, "exp-s-x", "r2_pass2", pass_index=2,
             pinned=[(5, 100, 0), (10, 300, 0)], top1=[(5, 100)],
             top1_overall=0.8, **common)
    make_run(tmp_path, "exp-s-x", "r3_pass3", pass_index=3,
             pinned=[(5, 100, 0)], top1=[(6, 500)],
             top1_overall=0.7, inspected=[(10, 1)], n_extra_calls=3)

    warnings: list[str] = []
    groups = agg.discover_runs(tmp_path, warnings)
    result = agg.aggregate(groups, "refusal", 36)
    s = result["per_slug"]["exp-s-x"]

    # pinned feature-level pairs: (12: 1/3), (13: 1/2), (23: 1/2) -> mean 4/9
    assert s["pinned_jaccard_feature"] == pytest.approx(4 / 9)
    # layers {5,10},{5,10},{5}: pairs 1, 1/2, 1/2 -> 2/3
    assert s["pinned_jaccard_layer"] == pytest.approx(2 / 3)
    # bands (36 layers): 5 -> 0, 10 -> 0, so {0},{0},{0} -> 1.0
    assert s["pinned_jaccard_band"] == pytest.approx(1.0)
    # inspected {A,B},{A,B},{A}: 1, 1/2, 1/2 -> 2/3
    assert s["inspected_jaccard_feature"] == pytest.approx(2 / 3)
    # tool calls 5,5,4 -> sd = sqrt(1/3)
    assert s["tool_calls_sd"] == pytest.approx(math.sqrt(1 / 3))
    # top1 pairs: eq, ne, ne -> 1/3
    assert s["top1_agreement"] == pytest.approx(1 / 3)
    assert s["top1_overall_sd"] == pytest.approx(0.1)
    assert "verdict_flip_rate" not in s


def test_probes_aggregation_flip_rate(tmp_path: Path) -> None:
    for i, dom in enumerate(["spurious", "spurious", "mixed"], 1):
        make_run(tmp_path, "exp-p-y", f"r{i}_pass{i}", pass_index=i,
                 pinned=[(3, 8011, 0)],
                 flagged=([(0, 4958)], [(5, 14591)]), dominant=dom)
    groups = agg.discover_runs(tmp_path, [])
    result = agg.aggregate(groups, "probes", 26)
    s = result["per_slug"]["exp-p-y"]
    # [spurious, spurious, mixed]: 3 pairs, 2 of them disagree
    assert s["verdict_flip_rate"] == pytest.approx(2 / 3)
    # the plurality-dissent quantity is a different, smaller number
    assert s["verdict_modal_dissent"] == pytest.approx(1 / 3)
    assert s["spurious_jaccard_feature"] == pytest.approx(1.0)
    assert s["causal_jaccard_feature"] == pytest.approx(1.0)
    assert "top1_agreement" not in s


def test_verdict_flip_rate_is_pairwise_not_modal(tmp_path: Path) -> None:
    """Regression pin (codex review 2026-07-27). The two quantities differ and
    the pairwise one is the headline, matching the Jaccards."""
    # 4 passes, 2-2 split: every one of the 6 pairs but the 2 same-label pairs
    # disagrees -> 4/6. Modal dissent would read 1/2.
    for i, dom in enumerate(["spurious", "spurious", "causal", "causal"], 1):
        make_run(tmp_path, "exp-p-split", f"r{i}_pass{i}", pass_index=i,
                 pinned=[(3, 1, 0)], flagged=([(0, 1)], []), dominant=dom)
    s = agg.aggregate(agg.discover_runs(tmp_path, []), "probes", 26)["per_slug"]["exp-p-split"]
    assert s["verdict_flip_rate"] == pytest.approx(4 / 6)
    assert s["verdict_modal_dissent"] == pytest.approx(1 / 2)


def test_unanimous_verdicts_have_zero_flip_rate(tmp_path: Path) -> None:
    for i in range(1, 4):
        make_run(tmp_path, "exp-p-same", f"r{i}_pass{i}", pass_index=i,
                 pinned=[(3, 1, 0)], flagged=([(0, 1)], []), dominant="spurious")
    s = agg.aggregate(agg.discover_runs(tmp_path, []), "probes", 26)["per_slug"]["exp-p-same"]
    assert s["verdict_flip_rate"] == 0.0
    assert s["verdict_modal_dissent"] == 0.0


def test_single_pass_slugs_are_skipped_not_averaged(tmp_path: Path) -> None:
    make_run(tmp_path, "exp-s-solo", "r1", pinned=[(1, 1, 0)])
    make_run(tmp_path, "exp-s-duo", "r1_pass1", pass_index=1, pinned=[(1, 1, 0)])
    make_run(tmp_path, "exp-s-duo", "r2_pass2", pass_index=2, pinned=[(1, 1, 0)])
    result = agg.aggregate(agg.discover_runs(tmp_path, []), "refusal", 36)
    assert result["skipped_single_pass_slugs"] == ["exp-s-solo"]
    assert list(result["per_slug"]) == ["exp-s-duo"]


def test_missing_pinned_file_excluded_but_empty_set_counts(tmp_path: Path) -> None:
    make_run(tmp_path, "exp-s-z", "r1_pass1", pass_index=1, pinned=[])
    make_run(tmp_path, "exp-s-z", "r2_pass2", pass_index=2, pinned=[])
    make_run(tmp_path, "exp-s-z", "r3_pass3", pass_index=3, pinned=None)
    warnings: list[str] = []
    result = agg.aggregate(agg.discover_runs(tmp_path, warnings), "refusal", 36)
    # Two real empty files agree perfectly, the missing one is excluded
    assert result["per_slug"]["exp-s-z"]["pinned_jaccard_feature"] == 1.0
    assert any("no pinned_ids.json" in w for w in warnings)


# ---------------------------------------------------------------------------
# Live validation against archived runs
# ---------------------------------------------------------------------------

T3_ARCHIVE = REPO / "refusal-jailbreaking" / "results-workshop"
T1_ARCHIVE = REPO / "spurious-correlation" / "results-workshop"


def _archived_groups(root: Path) -> dict:
    """Discover runs under an archive, or skip.

    The committed archives are sampled: only a few runs per arm keep the full
    run directory, so the number of oracle_result.json files there is not fixed
    and a checkout may hold none at all. These tests exist to run the parser
    against real schemas, so they take whatever is present and skip when there
    is nothing.
    """
    if not root.is_dir():
        pytest.skip(f"archived runs absent: {root}")
    warnings: list[str] = []
    groups = agg.discover_runs(root, warnings)
    if not groups:
        pytest.skip(f"no oracle_result.json under {root}")
    return groups


def test_live_refusal_archive() -> None:
    groups = _archived_groups(T3_ARCHIVE)
    result = agg.aggregate(groups, "refusal", 36)
    # Every discovered slug is either averaged or recorded as single-pass.
    assert result["n_slugs"] + len(result["skipped_single_pass_slugs"]) == len(groups)
    for s in result["per_slug"].values():
        assert 0.0 <= s["pinned_jaccard_feature"] <= 1.0
        assert 0.0 <= s["inspected_jaccard_feature"] <= 1.0


def test_live_probes_archive() -> None:
    """The archived probes runs are one run per slug, except a few multi-run
    slugs in the opus-sonnet/ exploratory subtree (different subagents, not
    repeat passes), which as a fixture exercises the probes pairwise path on
    real files. Numbers from those groups are cross-config and not quotable."""
    groups = _archived_groups(T1_ARCHIVE)
    result = agg.aggregate(groups, "probes", 26)
    # Single-pass slugs are skipped, not averaged into the report.
    assert result["n_slugs"] + len(result["skipped_single_pass_slugs"]) == len(groups)
    for s in result["per_slug"].values():
        for key in ("pinned_jaccard_feature", "inspected_jaccard_feature",
                    "spurious_jaccard_feature", "causal_jaccard_feature",
                    "verdict_flip_rate"):
            v = s.get(key)
            assert v is None or 0.0 <= v <= 1.0
