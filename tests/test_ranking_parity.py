"""Ranking parity between causal and observational mode.

This is the test that protects the published task-1 (spurious probes) and task-2
(secret elicitation) numbers.

The two forks ranked discovery results differently. The causal trunk takes
feature_effects.topk (signed, so only positive drivers surface) and the base
package took feature_effects.abs().topk (magnitude, so inhibitory features stay
visible). Every published probes and ELK number came out of the magnitude
ranking. Collapsing the two branches would silently change which features the
oracle ever sees, and inhibitory features are a plausible spurious-feature
carrier. The switch is one ToolContext field, rank_signed, set by
run_circuit_oracle from its mode argument.

See merge-specs.md spec B section 3 (get_top_features, get_upstream_features).
"""

from __future__ import annotations

import pytest
import torch

from circuit_oracle.tools import get_top_features, get_upstream_features

from conftest import ACTIVE_FEATURES, N_LAYERS, N_LOGITS, N_POS, make_ctx, make_graph


N_FEATURES = len(ACTIVE_FEATURES)
N_NODES = N_FEATURES + N_LAYERS * N_POS + N_POS + N_LOGITS
EMBED_START = N_FEATURES + N_LAYERS * N_POS

# Feature index 20 (row 2 of ACTIVE_FEATURES) is the strongly inhibitory one.
# It is the largest effect by magnitude and the smallest by sign, so it is in the
# top-2 under magnitude ranking and out of it under signed ranking.
INHIBITORY_FEATURE_IDX = 20


def _parity_ctx(rank_signed: bool):
    """Graph whose logit row and whose row 0 both carry one dominant NEGATIVE edge."""
    adj = torch.zeros(N_NODES, N_NODES)
    # Row 0 feeds get_upstream_features for the feature at (layer 1, pos 2, idx 100).
    # Column j is the upstream feature at ACTIVE_FEATURES[j].
    adj[0, 0] = 0.0     # self edge, zeroed by the tool anyway
    adj[0, 1] = 2.0     # feature_idx 10
    adj[0, 2] = -8.0    # feature_idx 20, dominant by magnitude only
    adj[0, 3] = 1.0     # feature_idx 30
    # Embedding columns left at zero, so no embedding rows join the ranking and
    # the assertion is about features only.

    # The first logit node's row feeds get_top_features. Index -N_LOGITS is the
    # first logit node, which is what the tool indexes for logit_idx 0.
    adj[-N_LOGITS, 0] = 5.0    # feature_idx 100
    adj[-N_LOGITS, 1] = 3.0    # feature_idx 10
    adj[-N_LOGITS, 2] = -9.0   # feature_idx 20, dominant by magnitude only
    adj[-N_LOGITS, 3] = 1.0    # feature_idx 30
    return make_ctx(make_graph(adjacency=adj), rank_signed=rank_signed)


# ---------------------------------------------------------------------------
# get_top_features
# ---------------------------------------------------------------------------


def test_top_features_signed_ranking_drops_the_inhibitory_feature():
    ctx = _parity_ctx(rank_signed=True)
    rows = get_top_features(ctx, token="Sorry", k=2)
    idxs = [r["feature_idx"] for r in rows]
    assert INHIBITORY_FEATURE_IDX not in idxs
    assert idxs == [100, 10]
    assert [r["direct_effect"] for r in rows] == [5.0, 3.0]


def test_top_features_magnitude_ranking_keeps_the_inhibitory_feature():
    ctx = _parity_ctx(rank_signed=False)
    rows = get_top_features(ctx, token="Sorry", k=2)
    idxs = [r["feature_idx"] for r in rows]
    assert INHIBITORY_FEATURE_IDX in idxs
    assert set(idxs) == {20, 100}
    by_idx = {r["feature_idx"]: r["direct_effect"] for r in rows}
    assert by_idx[20] == -9.0


def test_top_features_row_keys_are_identical_in_both_modes():
    """Only the ordering flips. The row schema must not, several evaluators read
    these keys straight out of the saved transcript."""
    signed = get_top_features(_parity_ctx(True), token="Sorry", k=4)
    magnitude = get_top_features(_parity_ctx(False), token="Sorry", k=4)
    keys = {"layer", "feature_idx", "pos", "activation", "direct_effect"}
    assert all(set(r) == keys for r in signed + magnitude)
    # Same four features at k = n_features, different order.
    assert {r["feature_idx"] for r in signed} == {r["feature_idx"] for r in magnitude}


# ---------------------------------------------------------------------------
# get_upstream_features
# ---------------------------------------------------------------------------


def test_upstream_signed_ranking_drops_the_inhibitory_feature():
    ctx = _parity_ctx(rank_signed=True)
    rows = get_upstream_features(ctx, layer=1, feature_idx=100, pos=2, k=2)
    idxs = [r["feature_idx"] for r in rows]
    assert INHIBITORY_FEATURE_IDX not in idxs
    assert idxs == [10, 30]
    assert [r["direct_effect"] for r in rows] == [2.0, 1.0]


def test_upstream_magnitude_ranking_keeps_the_inhibitory_feature():
    ctx = _parity_ctx(rank_signed=False)
    rows = get_upstream_features(ctx, layer=1, feature_idx=100, pos=2, k=2)
    idxs = [r["feature_idx"] for r in rows]
    assert INHIBITORY_FEATURE_IDX in idxs
    # Magnitude ordering puts the -8.0 edge first.
    assert idxs == [20, 10]
    assert rows[0]["direct_effect"] == -8.0


def test_upstream_row_keys_are_identical_in_both_modes():
    signed = get_upstream_features(_parity_ctx(True), layer=1, feature_idx=100, pos=2, k=3)
    magnitude = get_upstream_features(_parity_ctx(False), layer=1, feature_idx=100, pos=2, k=3)
    keys = {"type", "layer", "feature_idx", "pos", "direct_effect", "activation"}
    assert all(set(r) == keys for r in signed + magnitude)
    # The two feature SETS are not asserted equal here, and deliberately so. The
    # target's own row entry is zeroed rather than removed from the candidate
    # pool, so once k reaches n_features - 1 the signed branch pulls the 0.0 self
    # edge into the top-k while the magnitude branch sorts it last. That is
    # pre-existing behavior in both forks, not something the merge introduced.
    assert all(r["type"] == "feature" for r in signed + magnitude)


def test_upstream_self_edge_is_zeroed_not_excluded():
    """Pin the quirk the previous test works around, so a future change to it is
    a deliberate decision rather than a surprise."""
    rows = get_upstream_features(_parity_ctx(True), layer=1, feature_idx=100, pos=2, k=3)
    self_rows = [r for r in rows if r["feature_idx"] == 100]
    assert len(self_rows) == 1
    assert self_rows[0]["direct_effect"] == 0.0


# ---------------------------------------------------------------------------
# The switch itself
# ---------------------------------------------------------------------------


def test_default_context_ranks_by_magnitude():
    """Magnitude is the default in every mode, matching the absolute-influence
    criterion circuit_tracer already used to prune the graph."""
    ctx = _parity_ctx(rank_signed=False)
    assert ctx.rank_signed is False
    fresh = make_ctx()
    assert fresh.rank_signed is False


def test_missing_rank_signed_attribute_falls_back_to_magnitude(monkeypatch):
    """Both tools read the field with getattr(..., False). A stub or an older
    context without the field must fall back to the default, not to signed."""

    class _Bare:
        """Context stand-in with no rank_signed attribute at all."""

        def __init__(self, real):
            self.graph = real.graph
            self.tokenizer = real.tokenizer

    ctx = _Bare(_parity_ctx(rank_signed=False))
    assert not hasattr(ctx, "rank_signed")
    rows = get_top_features(ctx, token="Sorry", k=2)
    # |-9.0| > 5.0 > 3.0, so the inhibitory feature leads under magnitude.
    assert [r["feature_idx"] for r in rows] == [20, 100]


@pytest.mark.parametrize("mode", ["causal", "observational"])
def test_mode_does_not_touch_rank_signed(mode):
    """Ranking is independent of mode, checked without an LLM call.

    Magnitude ranking applies to every task, so run_circuit_oracle must not
    silently flip it when the mode changes. Choosing signed ranking has to be an
    explicit ctx.rank_signed = True rather than a side effect of picking a task.
    """
    from circuit_oracle import orchestrator as orch

    class _Stop(Exception):
        pass

    class _Client:
        def create_message(self, **kwargs):
            raise _Stop()

    ctx = make_ctx()
    assert ctx.rank_signed is False
    with pytest.raises(_Stop):
        orch.run_circuit_oracle(ctx, _Client(), "q", mode=mode, verbose=False)
    assert ctx.rank_signed is False

    # An explicitly requested ablation survives the run just the same.
    ctx_abl = make_ctx()
    ctx_abl.rank_signed = True
    with pytest.raises(_Stop):
        orch.run_circuit_oracle(ctx_abl, _Client(), "q", mode=mode, verbose=False)
    assert ctx_abl.rank_signed is True
