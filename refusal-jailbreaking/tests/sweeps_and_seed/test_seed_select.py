"""Deterministic seed-select ranking library (CPU only).

Covers circuit_oracle.seed_select, the pure ranking lib behind the multi-stage
seed sweep. No HTTP, no LLM, no subject-model load. The graph-consuming helpers
(feature_influence, build_candidates) are exercised against a lightweight fake
graph object that mirrors the circuit_tracer Graph attribute surface
(adjacency_matrix, logit_tokens, logit_probabilities, input_tokens,
selected_features, active_features, activation_values). The filter / pool /
rarity / rank helpers are exercised against hand-built FeatureCandidate lists.

Plan coverage ("Verification"):
- layer_band_bounds(36) == (7, 28) and never hardcodes n_layers.
- the per-stage rank() score on synthetic candidates.
- the -log(rho) clamp + normalize on a synthetic pool, plus the fail-loud paths.
"""

from __future__ import annotations

import math

import pytest
import torch

from circuit_oracle import seed_select as ss
from circuit_oracle.seed_select import FeatureCandidate


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
class _FakeGraph:
    """Minimal stand-in for circuit_tracer.graph.Graph.

    Only the attributes feature_influence / build_candidates read are populated.
    Built so feature i has a strictly larger logit-probability mass than feature
    i+1 once influence flows through a diagonal adjacency, giving a known
    descending influence order.
    """

    def __init__(self, n_features: int, n_pos: int, layers, positions, feat_ids):
        n_logits = 2
        n_nodes = n_features + n_logits
        # Diagonal adjacency: each logit row points to one feature with a clean
        # weight so influence ordering is deterministic and easy to reason about.
        adj = torch.zeros(n_nodes, n_nodes, dtype=torch.float32)
        # logit rows are the last n_logits rows. Give the top-1 logit (row
        # -n_logits) a descending edge onto each feature column.
        for j in range(n_features):
            adj[-n_logits, j] = float(n_features - j)  # feature 0 strongest
        self.adjacency_matrix = adj
        self.logit_tokens = torch.tensor([0, 1], dtype=torch.long)
        self.logit_probabilities = torch.tensor([1.0, 0.0], dtype=torch.float32)
        self.input_tokens = torch.zeros(n_pos, dtype=torch.long)
        self.selected_features = torch.arange(n_features, dtype=torch.long)
        # active_features rows are (layer, pos, feature_idx).
        self.active_features = torch.tensor(
            list(zip(layers, positions, feat_ids)), dtype=torch.long
        )
        self.activation_values = torch.arange(1, n_features + 1, dtype=torch.float32)


def _cand(layer, influence, *, pos=5, feature_idx=1000, relevance=None,
          frac_nonzero=None, neglog_rho=None) -> FeatureCandidate:
    return FeatureCandidate(
        layer=layer,
        pos=pos,
        feature_idx=feature_idx,
        influence=influence,
        activation=1.0,
        direct_effect_top_logit=0.0,
        relevance=relevance,
        frac_nonzero=frac_nonzero,
        neglog_rho=neglog_rho,
    )


# --------------------------------------------------------------------------- #
# layer_band_bounds
# --------------------------------------------------------------------------- #
def test_layer_band_bounds_36_is_7_28():
    assert ss.layer_band_bounds(36) == (7, 28)


def test_layer_band_bounds_reads_n_layers():
    # Bounds scale with n_layers, never hardcoded to 36.
    assert ss.layer_band_bounds(10) == (math.ceil(0.20 * 9), math.floor(0.80 * 9))
    assert ss.layer_band_bounds(10) == (2, 7)
    lo, hi = ss.layer_band_bounds(100)
    assert (lo, hi) == (math.ceil(0.20 * 99), math.floor(0.80 * 99)) == (20, 79)


def test_layer_band_bounds_custom_drop_frac():
    # drop_frac flows through both bounds.
    assert ss.layer_band_bounds(36, drop_frac=0.10) == (
        math.ceil(0.10 * 35),
        math.floor(0.90 * 35),
    )


# --------------------------------------------------------------------------- #
# pin_key ordering
# --------------------------------------------------------------------------- #
def test_pin_key_order_is_layer_feature_pos():
    c = _cand(layer=11, influence=1.0, pos=34, feature_idx=77560)
    assert c.pin_key == [11, 77560, 34]


# --------------------------------------------------------------------------- #
# feature_influence + build_candidates against a fake graph
# --------------------------------------------------------------------------- #
def test_feature_influence_dims_and_order():
    g = _FakeGraph(
        n_features=4,
        n_pos=6,
        layers=[3, 11, 20, 30],
        positions=[1, 2, 3, 4],
        feat_ids=[10, 20, 30, 40],
    )
    infl, dims = ss.feature_influence(g)
    assert dims == {"n_nodes": 6, "n_features": 4, "n_pos": 6, "n_logits": 2}
    # Feature 0 has the strongest edge so the largest influence.
    assert infl.shape[0] == 4
    assert torch.argmax(infl).item() == 0


def test_build_candidates_sorted_desc_and_mapped():
    g = _FakeGraph(
        n_features=4,
        n_pos=6,
        layers=[3, 11, 20, 30],
        positions=[1, 2, 3, 4],
        feat_ids=[10, 20, 30, 40],
    )
    infl, _ = ss.feature_influence(g)
    cands = ss.build_candidates(g, infl)
    assert len(cands) == 4
    # Descending influence.
    inf_vals = [c.influence for c in cands]
    assert inf_vals == sorted(inf_vals, reverse=True)
    # First candidate maps to feature 0's (layer, pos, feature_idx).
    top = cands[0]
    assert (top.layer, top.pos, top.feature_idx) == (3, 1, 10)
    assert top.pin_key == [3, 10, 1]


def test_feature_influence_fails_loud_on_no_logits():
    g = _FakeGraph(4, 6, [3, 11, 20, 30], [1, 2, 3, 4], [10, 20, 30, 40])
    g.logit_tokens = torch.tensor([], dtype=torch.long)
    with pytest.raises(ValueError, match="no logit nodes"):
        ss.feature_influence(g)


# --------------------------------------------------------------------------- #
# filter_non_opener
# --------------------------------------------------------------------------- #
def test_filter_non_opener_drops_bos_and_generation():
    gen_pos = 9
    cands = [
        _cand(5, 1.0, pos=0),       # BOS
        _cand(5, 1.0, pos=3),       # keep
        _cand(5, 1.0, pos=9),       # generation boundary
        _cand(5, 1.0, pos=5),       # keep
    ]
    kept = ss.filter_non_opener(cands, gen_pos)
    assert [c.pos for c in kept] == [3, 5]


# --------------------------------------------------------------------------- #
# filter_layer_band
# --------------------------------------------------------------------------- #
def test_filter_layer_band_keeps_7_to_28_for_36_layers():
    cands = [
        _cand(0, 1.0),    # drop (below 7)
        _cand(6, 1.0),    # drop (below 7)
        _cand(7, 1.0),    # keep (lo inclusive)
        _cand(11, 1.0),   # keep (the gate)
        _cand(28, 1.0),   # keep (hi inclusive)
        _cand(29, 1.0),   # drop (above 28)
        _cand(35, 1.0),   # drop
    ]
    kept = ss.filter_layer_band(cands, n_layers=36)
    assert sorted(c.layer for c in kept) == [7, 11, 28]


# --------------------------------------------------------------------------- #
# candidate_pool
# --------------------------------------------------------------------------- #
def test_candidate_pool_takes_top_n():
    cands = [_cand(5, float(100 - i), feature_idx=i) for i in range(100)]
    pool = ss.candidate_pool(cands, pool_size=50)
    assert len(pool) == 50
    assert pool[0].feature_idx == 0
    assert pool[-1].feature_idx == 49


# --------------------------------------------------------------------------- #
# attach_neglog_rho
# --------------------------------------------------------------------------- #
def test_attach_neglog_rho_clamp_and_normalize():
    pool = [
        _cand(5, 1.0, feature_idx=1, frac_nonzero=0.00277),   # rarest -> max raw
        _cand(5, 1.0, feature_idx=2, frac_nonzero=0.5),
        _cand(5, 1.0, feature_idx=3, frac_nonzero=1.0),       # common -> raw 0
    ]
    ss.attach_neglog_rho(pool)
    # All in (0, 1], max normalized to exactly 1.0.
    vals = [c.neglog_rho for c in pool]
    assert all(0.0 <= v <= 1.0 for v in vals)
    assert pool[0].neglog_rho == pytest.approx(1.0)  # rarest is the max
    # rho == 1.0 -> raw -log(1) == 0 -> normalized 0.
    assert pool[2].neglog_rho == pytest.approx(0.0)
    # Monotone: rarer features carry strictly larger weight.
    assert pool[0].neglog_rho > pool[1].neglog_rho > pool[2].neglog_rho


def test_attach_neglog_rho_clamps_below_1e_minus_6():
    pool = [
        _cand(5, 1.0, feature_idx=1, frac_nonzero=0.0),       # clamps to 1e-6
        _cand(5, 1.0, feature_idx=2, frac_nonzero=1e-9),      # clamps to 1e-6 too
        _cand(5, 1.0, feature_idx=3, frac_nonzero=0.5),
    ]
    ss.attach_neglog_rho(pool)
    raw_max = -math.log(1e-6)
    assert pool[0].neglog_rho == pytest.approx(1.0)
    assert pool[1].neglog_rho == pytest.approx(1.0)
    assert pool[2].neglog_rho == pytest.approx(-math.log(0.5) / raw_max)


def test_attach_neglog_rho_fails_loud_on_none():
    pool = [
        _cand(5, 1.0, feature_idx=7, frac_nonzero=0.5),
        _cand(11, 1.0, feature_idx=77560, pos=34, frac_nonzero=None),
    ]
    with pytest.raises(ValueError, match=r"L11:F77560@34"):
        ss.attach_neglog_rho(pool)


def test_attach_neglog_rho_fails_loud_on_all_common():
    # Every rho clamps to 1 -> raw all zero -> cannot normalize.
    pool = [_cand(5, 1.0, feature_idx=i, frac_nonzero=1.0) for i in range(3)]
    with pytest.raises(ValueError, match="all zero"):
        ss.attach_neglog_rho(pool)


# --------------------------------------------------------------------------- #
# rank
# --------------------------------------------------------------------------- #
def test_rank_stage_i_uses_influence_and_band():
    cands = [
        _cand(0, 100.0, feature_idx=1),    # huge influence, but out of band
        _cand(11, 10.0, feature_idx=2),    # in band
        _cand(20, 5.0, feature_idx=3),     # in band
        _cand(35, 50.0, feature_idx=4),    # out of band
    ]
    top = ss.rank(cands, "i", n_layers=36, top_k=20)
    # Band drops layers 0 and 35, leaving 11 and 20 ordered by influence.
    assert [c.feature_idx for c in top] == [2, 3]
    assert [c.rank for c in top] == [0, 1]
    assert top[0].score == 10.0


def test_rank_stage_ii_a_multiplies_relevance_no_band():
    cands = [
        _cand(0, 10.0, feature_idx=1, relevance=0.1),    # 1.0, kept (no band)
        _cand(11, 5.0, feature_idx=2, relevance=0.9),    # 4.5
        _cand(35, 8.0, feature_idx=3, relevance=1.0),    # 8.0
    ]
    top = ss.rank(cands, "ii-a", n_layers=36, top_k=20)
    # ii-a has no band, sort by influence * relevance: 8.0, 4.5, 1.0.
    assert [c.feature_idx for c in top] == [3, 2, 1]
    assert top[0].score == pytest.approx(8.0)
    assert top[1].score == pytest.approx(4.5)


def test_rank_stage_ii_b_applies_band():
    cands = [
        _cand(0, 10.0, feature_idx=1, relevance=1.0),    # out of band
        _cand(11, 5.0, feature_idx=2, relevance=0.9),    # in band, 4.5
        _cand(20, 6.0, feature_idx=3, relevance=0.5),    # in band, 3.0
    ]
    top = ss.rank(cands, "ii-b", n_layers=36, top_k=20)
    assert [c.feature_idx for c in top] == [2, 3]


def test_rank_stage_iii_a_multiplies_rarity():
    cands = [
        _cand(11, 5.0, feature_idx=2, relevance=1.0, neglog_rho=1.0),   # 5.0
        _cand(20, 6.0, feature_idx=3, relevance=1.0, neglog_rho=0.5),   # 3.0
    ]
    top = ss.rank(cands, "iii-a", n_layers=36, top_k=20)
    assert [c.feature_idx for c in top] == [2, 3]
    assert top[0].score == pytest.approx(5.0)
    assert top[1].score == pytest.approx(3.0)


def test_rank_top_k_truncates_without_padding():
    cands = [_cand(11, float(10 - i), feature_idx=i) for i in range(10)]
    top = ss.rank(cands, "i", n_layers=36, top_k=3)
    assert len(top) == 3
    assert [c.feature_idx for c in top] == [0, 1, 2]


def test_rank_short_count_returns_what_remains():
    # Only 2 in-band candidates, top_k=20 -> returns 2, does not pad.
    cands = [
        _cand(0, 10.0, feature_idx=1),    # out of band
        _cand(11, 5.0, feature_idx=2),    # in band
        _cand(20, 6.0, feature_idx=3),    # in band
        _cand(35, 9.0, feature_idx=4),    # out of band
    ]
    top = ss.rank(cands, "i", n_layers=36, top_k=20)
    assert len(top) == 2


def test_rank_fails_loud_on_unknown_mode():
    with pytest.raises(ValueError, match="unknown rank mode"):
        ss.rank([_cand(11, 1.0)], "bogus", n_layers=36)


def test_rank_fails_loud_on_missing_relevance():
    cands = [_cand(11, 1.0, feature_idx=42, relevance=None)]
    with pytest.raises(ValueError, match=r"relevance is None for feature L11:F42"):
        ss.rank(cands, "ii-a", n_layers=36)


def test_rank_fails_loud_on_missing_neglog_rho():
    cands = [_cand(11, 1.0, feature_idx=42, relevance=0.5, neglog_rho=None)]
    with pytest.raises(ValueError, match=r"neglog_rho is None for feature L11:F42"):
        ss.rank(cands, "iii-a", n_layers=36)
