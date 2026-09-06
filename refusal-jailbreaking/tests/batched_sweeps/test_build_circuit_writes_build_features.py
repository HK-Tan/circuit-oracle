"""build_circuit populates ctx.build_features as a side effect.

Asserts that after calling `build_circuit(nodes, edges)`, the canonical pinned-feature
set (the keys for pin_features) is available on `ctx.build_features`. This replaces the
post-hoc `_collect_pinned_features` extraction in saving.py.
"""
from __future__ import annotations

import pytest


def test_build_circuit_writes_build_features(baseline_ctx):
    from circuit_oracle.tools import build_circuit

    nodes = [
        {"layer": 0, "feature_idx": 1, "pos": 3, "label": "a"},
        {"layer": 1, "feature_idx": 5, "pos": 4, "label": "b"},
        {"layer": 1, "feature_idx": 7, "pos": 4, "label": "c"},
    ]
    edges = [
        {"from": (0, 1, 3), "to": (1, 5, 4)},
        {"from": (1, 5, 4), "to": (1, 7, 4)},
    ]

    build_circuit(baseline_ctx, nodes=nodes, edges=edges)

    assert hasattr(baseline_ctx, "build_features")
    assert baseline_ctx.build_features == {
        (0, 1, 3),
        (1, 5, 4),
        (1, 7, 4),
    }
