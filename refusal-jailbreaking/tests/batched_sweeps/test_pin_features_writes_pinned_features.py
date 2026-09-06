"""pin_features writes ctx.pinned_features mapping verbatim.

Asserts that a successful `pin_features` call populates `ctx.pinned_features` with a
dict `(layer, feature_idx, pos) -> pre_hypothesis` exactly equal to the agent-supplied
input. This is the canonical handoff to `batched_anchor_sweep`.
"""
from __future__ import annotations

import pytest


def test_pin_features_writes_pinned_features(baseline_ctx):
    from circuit_oracle.tools import build_circuit, pin_features

    nodes = [
        {"layer": 0, "feature_idx": 1, "pos": 3, "label": "a"},
        {"layer": 1, "feature_idx": 5, "pos": 4, "label": "b"},
        {"layer": 1, "feature_idx": 7, "pos": 4, "label": "c"},
    ]
    build_circuit(baseline_ctx, nodes=nodes, edges=[])

    pre_hypotheses = {
        (0, 1, 3): "input opener token",
        (1, 5, 4): "refusal-affect softener",
        (1, 7, 4): "topic-routing gate",
    }
    pin_features(baseline_ctx, pre_hypotheses=pre_hypotheses)

    assert hasattr(baseline_ctx, "pinned_features")
    assert baseline_ctx.pinned_features == pre_hypotheses
