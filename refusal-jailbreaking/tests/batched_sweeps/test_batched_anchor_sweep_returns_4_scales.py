"""batched_anchor_sweep returns K x 4 = 4K measurement records.

Asserts that with 3 pinned features, the sweep emits 12 measurement records covering
scales {0, -1, -2, -3}, exactly one record per (feature, scale) pair. This is the
deterministic 4-scale-per-feature contract.
"""
from __future__ import annotations

import pytest


def test_batched_anchor_sweep_returns_4_scales(tiny_model, baseline_ctx):
    from circuit_oracle.tools import (
        batched_anchor_sweep,
        build_circuit,
        pin_features,
    )

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

    result = batched_anchor_sweep(baseline_ctx)

    measurements = result["measurements"]
    assert len(measurements) == 12, f"expected 3 features x 4 scales = 12, got {len(measurements)}"

    seen_pairs = {(m["layer"], m["feature_idx"], m["pos"], m["scale"]) for m in measurements}
    expected_pairs = {
        (layer, feat_idx, pos, scale)
        for (layer, feat_idx, pos) in pre_hypotheses
        for scale in (0.0, -1.0, -2.0, -3.0)
    }
    assert seen_pairs == expected_pairs
