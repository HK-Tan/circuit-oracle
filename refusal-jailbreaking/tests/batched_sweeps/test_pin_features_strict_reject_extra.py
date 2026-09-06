"""pin_features rejects pre_hypotheses with any key not in build_features.

Asserts the strict-reject behavior in the harness: if the agent's
`pre_hypotheses` dict contains a key not present in `ctx.build_features`, the call
raises ValueError naming the unexpected key.
"""
from __future__ import annotations

import pytest


def test_pin_features_strict_reject_extra(baseline_ctx):
    from circuit_oracle.tools import build_circuit, pin_features

    nodes = [
        {"layer": 0, "feature_idx": 1, "pos": 3, "label": "a"},
        {"layer": 1, "feature_idx": 5, "pos": 4, "label": "b"},
    ]
    build_circuit(baseline_ctx, nodes=nodes, edges=[])

    # Extra (1, 99, 4) key not in build_features.
    pre_hypotheses = {
        (0, 1, 3): "input opener token",
        (1, 5, 4): "refusal-affect softener",
        (1, 99, 4): "ghost feature not in build_circuit",
    }

    with pytest.raises(ValueError, match=r"\(1, 99, 4\)"):
        pin_features(baseline_ctx, pre_hypotheses=pre_hypotheses)
