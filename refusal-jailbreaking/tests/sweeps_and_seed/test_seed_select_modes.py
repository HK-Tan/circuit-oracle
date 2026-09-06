"""Seed_select rank() across all seven modes plus the rarity gate value.

A focused complement to test_seed_select.py. Where that module checks each helper,
this one nails the scope items called out explicitly:

- rank() on one shared synthetic candidate set for every one of the seven modes
  (i, ii-a, ii-b, iii-a, iii-b, iv-a, iv-b), asserting the exact per-stage score
  formula. Stage iv must score WITHOUT relevance (its whole point is no
  selection-time LLM call), so its tests run on a relevance-free pool.
- the -b (and stage i) band modes drop out-of-band layers while -a modes keep them.
- attach_neglog_rho around the real gate value rho == 0.00277, with the clamp into
  [1e-6, 1] and the per-pool max-normalize, and the fail-loud on a None frac_nonzero.

CPU only, no graph load, no network, no LLM. Candidates are hand-built.
"""

from __future__ import annotations

import math

import pytest

from circuit_oracle import seed_select as ss
from circuit_oracle.seed_select import FeatureCandidate


# n_layers == 36 -> band keeps layers 7..28 inclusive (the real subject model).
N_LAYERS = 36


def _cand(layer, influence, feature_idx, *, pos=5, relevance=None,
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


def _shared_pool():
    """One pool exercised by every mode.

    Feature 100: in band (L11), modest influence, high relevance, rare.
    Feature 200: OUT of band (L2), high influence, mid relevance, common-ish.
    Feature 300: in band (L20), high influence, low relevance, rare.
    Every candidate carries relevance + neglog_rho so all five modes can score.
    """
    return [
        _cand(11, 2.0, 100, relevance=0.9, neglog_rho=1.0),   # in band
        _cand(2, 5.0, 200, relevance=0.5, neglog_rho=0.2),    # out of band (low)
        _cand(20, 4.0, 300, relevance=0.1, neglog_rho=0.8),   # in band
    ]


def _by_id(top):
    return {c.feature_idx: c for c in top}


# --------------------------------------------------------------------------- #
# Per-stage score formula on a shared pool
# --------------------------------------------------------------------------- #
def test_mode_i_score_is_influence_and_band_drops_out_of_band():
    top = ss.rank(_shared_pool(), "i", n_layers=N_LAYERS, top_k=20)
    ids = [c.feature_idx for c in top]
    # Out-of-band L2 (feature 200) is dropped, even though it has the top influence.
    assert 200 not in ids
    # In-band features ordered by raw influence: 300 (4.0) then 100 (2.0).
    assert ids == [300, 100]
    byid = _by_id(top)
    assert byid[300].score == pytest.approx(4.0)
    assert byid[100].score == pytest.approx(2.0)


def test_mode_ii_a_score_is_influence_times_relevance_no_band():
    top = ss.rank(_shared_pool(), "ii-a", n_layers=N_LAYERS, top_k=20)
    byid = _by_id(top)
    # No band: the out-of-band L2 feature is kept.
    assert 200 in byid
    assert byid[100].score == pytest.approx(2.0 * 0.9)   # 1.8
    assert byid[200].score == pytest.approx(5.0 * 0.5)   # 2.5
    assert byid[300].score == pytest.approx(4.0 * 0.1)   # 0.4
    # Ranked by score desc: 200 (2.5) > 100 (1.8) > 300 (0.4).
    assert [c.feature_idx for c in top] == [200, 100, 300]


def test_mode_ii_b_band_drops_out_of_band_then_influence_times_relevance():
    top = ss.rank(_shared_pool(), "ii-b", n_layers=N_LAYERS, top_k=20)
    ids = [c.feature_idx for c in top]
    assert 200 not in ids               # out of band dropped
    byid = _by_id(top)
    assert byid[100].score == pytest.approx(1.8)
    assert byid[300].score == pytest.approx(0.4)
    assert ids == [100, 300]            # 1.8 > 0.4


def test_mode_iii_a_score_is_influence_times_relevance_times_rarity_no_band():
    top = ss.rank(_shared_pool(), "iii-a", n_layers=N_LAYERS, top_k=20)
    byid = _by_id(top)
    assert 200 in byid                                       # no band
    assert byid[100].score == pytest.approx(2.0 * 0.9 * 1.0)  # 1.8
    assert byid[200].score == pytest.approx(5.0 * 0.5 * 0.2)  # 0.5
    assert byid[300].score == pytest.approx(4.0 * 0.1 * 0.8)  # 0.32
    assert [c.feature_idx for c in top] == [100, 200, 300]


def test_mode_iii_b_band_then_full_product():
    top = ss.rank(_shared_pool(), "iii-b", n_layers=N_LAYERS, top_k=20)
    ids = [c.feature_idx for c in top]
    assert 200 not in ids               # out of band dropped
    byid = _by_id(top)
    assert byid[100].score == pytest.approx(2.0 * 0.9 * 1.0)  # 1.8
    assert byid[300].score == pytest.approx(4.0 * 0.1 * 0.8)  # 0.32
    assert ids == [100, 300]


def test_mode_iv_a_score_is_influence_times_rarity_no_relevance_needed():
    # Stage iv's defining property: it scores WITHOUT relevance. Strip relevance
    # from every candidate so a hidden relevance dependency would fail loud.
    pool = [
        _cand(11, 2.0, 100, neglog_rho=1.0),
        _cand(2, 5.0, 200, neglog_rho=0.2),
        _cand(20, 4.0, 300, neglog_rho=0.8),
    ]
    top = ss.rank(pool, "iv-a", n_layers=N_LAYERS, top_k=20)
    byid = _by_id(top)
    assert 200 in byid                                   # no band
    assert byid[100].score == pytest.approx(2.0 * 1.0)   # 2.0
    assert byid[200].score == pytest.approx(5.0 * 0.2)   # 1.0
    assert byid[300].score == pytest.approx(4.0 * 0.8)   # 3.2
    assert [c.feature_idx for c in top] == [300, 100, 200]


def test_mode_iv_b_band_then_influence_times_rarity():
    pool = [
        _cand(11, 2.0, 100, neglog_rho=1.0),
        _cand(2, 5.0, 200, neglog_rho=0.2),
        _cand(20, 4.0, 300, neglog_rho=0.8),
    ]
    top = ss.rank(pool, "iv-b", n_layers=N_LAYERS, top_k=20)
    ids = [c.feature_idx for c in top]
    assert 200 not in ids               # out of band dropped
    byid = _by_id(top)
    assert byid[100].score == pytest.approx(2.0)
    assert byid[300].score == pytest.approx(3.2)
    assert ids == [300, 100]


def test_mode_iv_fails_loud_on_missing_rarity():
    pool = [_cand(11, 2.0, 100, relevance=0.9, neglog_rho=None)]
    with pytest.raises(ValueError, match=r"neglog_rho is None .* stage 'iv-a'"):
        ss.rank(pool, "iv-a", n_layers=N_LAYERS)


def test_b_modes_drop_out_of_band_a_modes_keep_it():
    pool = _shared_pool()
    for a_mode in ("ii-a", "iii-a", "iv-a"):
        ids = [c.feature_idx for c in ss.rank(pool, a_mode, n_layers=N_LAYERS)]
        assert 200 in ids, f"{a_mode} (no band) should keep out-of-band L2"
    for b_mode in ("i", "ii-b", "iii-b", "iv-b"):
        ids = [c.feature_idx for c in ss.rank(pool, b_mode, n_layers=N_LAYERS)]
        assert 200 not in ids, f"{b_mode} (band) should drop out-of-band L2"


# --------------------------------------------------------------------------- #
# attach_neglog_rho around the real gate value (rho == 0.00277)
# --------------------------------------------------------------------------- #
def test_attach_neglog_rho_gate_value_is_pool_max():
    # The verified gate L11:F77560 has frac_nonzero 0.00277 (the rarest here), so
    # after per-pool normalize its neglog_rho is exactly 1.0.
    pool = [
        _cand(11, 1.0, 77560, frac_nonzero=0.00277),   # the gate, rarest
        _cand(20, 1.0, 300, frac_nonzero=0.05),
        _cand(14, 1.0, 1234, frac_nonzero=0.3),
    ]
    ss.attach_neglog_rho(pool)
    raw_gate = -math.log(0.00277)
    assert pool[0].neglog_rho == pytest.approx(1.0)
    # The other two are raw/raw_gate, strictly between 0 and 1, monotone in rarity.
    assert pool[1].neglog_rho == pytest.approx(-math.log(0.05) / raw_gate)
    assert pool[2].neglog_rho == pytest.approx(-math.log(0.3) / raw_gate)
    assert pool[0].neglog_rho > pool[1].neglog_rho > pool[2].neglog_rho > 0.0


def test_attach_neglog_rho_clamps_zero_into_1e_minus_6():
    # frac_nonzero == 0.0 must clamp to 1e-6 (not -inf), giving the max raw weight.
    pool = [
        _cand(11, 1.0, 1, frac_nonzero=0.0),       # clamps to 1e-6
        _cand(20, 1.0, 2, frac_nonzero=0.00277),   # the gate value
    ]
    ss.attach_neglog_rho(pool)
    raw_max = -math.log(1e-6)
    assert pool[0].neglog_rho == pytest.approx(1.0)
    assert pool[1].neglog_rho == pytest.approx(-math.log(0.00277) / raw_max)


def test_attach_neglog_rho_raises_on_none_frac_nonzero():
    pool = [
        _cand(11, 1.0, 77560, pos=34, frac_nonzero=None),   # None -> fail loud
        _cand(20, 1.0, 300, frac_nonzero=0.05),
    ]
    with pytest.raises(ValueError, match=r"frac_nonzero is None for feature L11:F77560@34"):
        ss.attach_neglog_rho(pool)
