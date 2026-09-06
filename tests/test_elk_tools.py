"""The three grafted observational tools, on synthetic graphs with a fake FeatureCache.

Covers merge-specs.md spec B section 4.7 items 2, 3 and 4. Nothing here touches
the network, the disk, or a real transcoder feature directory.
"""

from __future__ import annotations

import math

import pytest
import torch

from circuit_oracle import elk_tools

from conftest import FAKE_FEATURES_DIR, make_ctx, make_graph


# The exact key sets spec B section 4.7 pins.
RANK_SEGMENT_KEYS = {
    "layer",
    "feature_idx",
    "mean_diff",
    "activation_frequency",
    "base_density",
    "score",
    "top_logits",
}
VOTE_TALLY_KEYS = {"tally", "total_matched_votes", "n_sibling_graphs", "settings"}
SOURCE_INFLUENCE_KEYS = {
    "depth",
    "source_positions",
    "S_pct_of_total",
    "R_pct_of_total",
    "S_over_R",
    "S_signed_raw",
    "R_signed_raw",
    "top_source_features",
    "note",
}


@pytest.fixture()
def elk_ctx(fake_feature_cache):
    """Target graph plus one sibling whose activations are uniformly weaker.

    Same four (layer, pos, feature) coordinates in both graphs, so every feature
    has a positive diff and nothing is dropped for being sibling-dominated.
    """
    sibling = make_graph(activations=[1.0, 1.0, 2.5, 0.5])
    return make_ctx(
        sibling_graphs=[sibling],
        autointerp_features_dir=FAKE_FEATURES_DIR,
        candidate_words=["apple", "banana"],
        base_feature_density={(0, 10): 0.002},
    )


# ---------------------------------------------------------------------------
# rank_segment_features
# ---------------------------------------------------------------------------


def test_rank_segment_features_key_set(elk_ctx):
    rows = elk_tools.rank_segment_features(
        elk_ctx, seg_start=0, seg_end=3, k=10, min_layer=0
    )
    assert isinstance(rows, list) and rows, f"expected non-empty ranking, got {rows!r}"
    for row in rows:
        assert set(row) == RANK_SEGMENT_KEYS


def test_rank_segment_features_ranks_by_score(elk_ctx):
    rows = elk_tools.rank_segment_features(
        elk_ctx, seg_start=0, seg_end=3, k=10, min_layer=0
    )
    scores = [r["score"] for r in rows]
    assert scores == sorted(scores, reverse=True)
    # Feature (layer 0, idx 10) has the biggest diff, the rarest activation
    # frequency AND the only base-density multiplier, so it must lead.
    assert (rows[0]["layer"], rows[0]["feature_idx"]) == (0, 10)


def test_rank_segment_features_applies_base_density_multiplier(elk_ctx):
    """base_density is an extra IDF factor, present only for the one feature the
    density table covers. The others carry base_density=None and drop the factor."""
    rows = elk_tools.rank_segment_features(
        elk_ctx, seg_start=0, seg_end=3, k=10, min_layer=0
    )
    by_key = {(r["layer"], r["feature_idx"]): r for r in rows}
    assert by_key[(0, 10)]["base_density"] == pytest.approx(0.002)
    assert by_key[(1, 30)]["base_density"] is None
    # mean_diff for (0, 10) is (5.0 - 1.0) / seg_len, seg_len = 3.
    assert by_key[(0, 10)]["mean_diff"] == pytest.approx(4.0 / 3.0, abs=1e-4)
    expected = (4.0 / 3.0) * -math.log(0.001) * -math.log(0.002 + 1e-6)
    assert by_key[(0, 10)]["score"] == pytest.approx(expected, rel=1e-3)


def test_rank_segment_features_min_layer_filters(elk_ctx):
    rows = elk_tools.rank_segment_features(
        elk_ctx, seg_start=0, seg_end=3, k=10, min_layer=1
    )
    assert rows and all(r["layer"] >= 1 for r in rows)


def test_rank_segment_features_requires_siblings(fake_feature_cache):
    ctx = make_ctx(autointerp_features_dir=FAKE_FEATURES_DIR)
    out = elk_tools.rank_segment_features(ctx, seg_start=0, seg_end=3, min_layer=0)
    assert "error" in out and "sibling_graphs" in out["error"]


def test_rank_segment_features_requires_features_dir():
    ctx = make_ctx(sibling_graphs=[make_graph()])
    out = elk_tools.rank_segment_features(ctx, seg_start=0, seg_end=3, min_layer=0)
    assert "error" in out and "autointerp_features_dir" in out["error"]


def test_rank_segment_features_rejects_empty_segment(elk_ctx):
    out = elk_tools.rank_segment_features(elk_ctx, seg_start=2, seg_end=2, min_layer=0)
    assert "error" in out


# ---------------------------------------------------------------------------
# get_candidate_vote_tally
# ---------------------------------------------------------------------------


def test_vote_tally_key_set_and_counts(elk_ctx):
    out = elk_tools.get_candidate_vote_tally(elk_ctx, min_layer=0, top_k_per_pos=30)
    assert set(out) == VOTE_TALLY_KEYS
    assert out["n_sibling_graphs"] == 1
    assert out["settings"] == {"min_layer": 0, "top_k_per_pos": 30}

    votes = {row["candidate"]: row["matched_votes"] for row in out["tally"]}
    # "apple" is promoted by feature (0, 10) at pos 0 and by (1, 30) at pos 1,
    # "banana" only by (0, 20) at pos 1.
    #
    # (0, 10) contributes TWO apple votes, not one. Its top_logits carry both
    # "apple" and "apples", the stemmer maps them to "apple" and "appl"
    # respectively (the suffix rule strips "es", not "s", from a 6-character
    # token), and the per-feature dedup key is the stem, not the candidate. So a
    # feature promoting several surface forms of one candidate votes once per
    # form. That is verbatim pre-merge base behavior and it produced the
    # published ELK numbers, so this test pins it rather than calling it a bug.
    assert votes == {"apple": 3, "banana": 1}
    assert out["total_matched_votes"] == 4
    # Sorted by vote count, descending.
    assert [r["candidate"] for r in out["tally"]] == ["apple", "banana"]


def test_vote_tally_contributing_features_shape(elk_ctx):
    out = elk_tools.get_candidate_vote_tally(elk_ctx, min_layer=0, top_k_per_pos=30)
    apple = next(r for r in out["tally"] if r["candidate"] == "apple")
    # One row per vote (see the stem-dedup note above), capped at 6 by the tool.
    assert len(apple["contributing_features"]) == 3
    for c in apple["contributing_features"]:
        assert set(c) == {"layer", "pos", "feature_idx", "matched_stem", "top_logits"}
        assert c["matched_stem"] in ("apple", "appl")
    assert {(c["layer"], c["feature_idx"]) for c in apple["contributing_features"]} == {
        (0, 10),
        (1, 30),
    }


def test_vote_tally_requires_candidate_words(fake_feature_cache):
    ctx = make_ctx(
        sibling_graphs=[make_graph(activations=[1.0, 1.0, 2.5, 0.5])],
        autointerp_features_dir=FAKE_FEATURES_DIR,
    )
    out = elk_tools.get_candidate_vote_tally(ctx, min_layer=0)
    assert "error" in out and "candidate_words" in out["error"]


def test_vote_tally_requires_siblings(fake_feature_cache):
    ctx = make_ctx(
        autointerp_features_dir=FAKE_FEATURES_DIR, candidate_words=["apple"]
    )
    out = elk_tools.get_candidate_vote_tally(ctx, min_layer=0)
    assert "error" in out and "sibling_graphs" in out["error"]


# ---------------------------------------------------------------------------
# _require_siblings (the half-healthy-run guard)
# ---------------------------------------------------------------------------


def test_require_siblings_error_when_empty():
    """A run with no sibling graphs must fail per call, not return a plausible
    empty ranking. Empty results would read as "no diff-specific features", which
    is a scientific claim, not a configuration error."""
    ctx = make_ctx()
    assert ctx.sibling_graphs == []
    out = elk_tools._require_siblings(ctx)
    assert isinstance(out, dict) and "error" in out
    assert "sibling_graphs" in out["error"]


def test_require_siblings_none_when_present():
    ctx = make_ctx(sibling_graphs=[make_graph()])
    assert elk_tools._require_siblings(ctx) is None


# ---------------------------------------------------------------------------
# get_source_influence
# ---------------------------------------------------------------------------


def test_source_influence_key_set_and_percentage_bound():
    ctx = make_ctx()
    out = elk_tools.get_source_influence(ctx, source_positions=[0], depth=2)
    assert set(out) == SOURCE_INFLUENCE_KEYS
    assert len(SOURCE_INFLUENCE_KEYS) == 9
    assert out["depth"] == 2
    assert out["source_positions"] == [0]
    # S is the signed influence landing on the source positions, R is the single
    # strongest non-source position. Positions partition the non-logit nodes, so
    # the two percentages can never jointly exceed the whole influence mass.
    assert out["S_pct_of_total"] + out["R_pct_of_total"] <= 100.0


@pytest.mark.parametrize("depth", [1, 2, 3])
def test_source_influence_percentage_bound_holds_at_every_depth(depth):
    ctx = make_ctx()
    out = elk_tools.get_source_influence(ctx, source_positions=[0, 1], depth=depth)
    assert out["depth"] == depth
    assert out["source_positions"] == [0, 1]
    assert out["S_pct_of_total"] + out["R_pct_of_total"] <= 100.0


def test_source_influence_top_features_shape():
    ctx = make_ctx()
    out = elk_tools.get_source_influence(ctx, source_positions=[0, 1], depth=2)
    assert len(out["top_source_features"]) <= 6
    for row in out["top_source_features"]:
        assert set(row) == {"layer", "feature_idx", "pos", "signed_contrib_pct"}
        assert row["pos"] in (0, 1)


def test_source_influence_rejects_empty_and_non_integer_positions():
    ctx = make_ctx()
    assert "error" in elk_tools.get_source_influence(ctx, source_positions=[])
    out = elk_tools.get_source_influence(ctx, source_positions=["not-an-int"])
    assert "error" in out


def test_source_influence_degenerate_graph_errors():
    """An all-zero adjacency carries no influence mass. Fail loud rather than
    divide by zero and report 0 percent."""
    n_nodes = 4 + 2 * 3 + 3 + 2
    ctx = make_ctx(make_graph(adjacency=torch.zeros(n_nodes, n_nodes)))
    out = elk_tools.get_source_influence(ctx, source_positions=[0], depth=2)
    assert "error" in out
