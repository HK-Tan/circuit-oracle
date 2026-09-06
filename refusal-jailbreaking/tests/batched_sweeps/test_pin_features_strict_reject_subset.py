"""pin_features rejects pre_hypotheses missing any build_features key.

Asserts the strict-reject behavior in the harness: if the agent's
`pre_hypotheses` dict is a strict subset of `ctx.build_features`, `pin_features`
raises ValueError that names the missing keys (so the agent can amend either side).
"""
from __future__ import annotations

import pytest


def test_pin_features_strict_reject_subset(baseline_ctx):
    from circuit_oracle.tools import build_circuit, pin_features

    nodes = [
        {"layer": 0, "feature_idx": 1, "pos": 3, "label": "a"},
        {"layer": 1, "feature_idx": 5, "pos": 4, "label": "b"},
        {"layer": 1, "feature_idx": 7, "pos": 4, "label": "c"},
    ]
    build_circuit(baseline_ctx, nodes=nodes, edges=[])

    # Missing the (1, 7, 4) key.
    pre_hypotheses = {
        (0, 1, 3): "input opener token",
        (1, 5, 4): "refusal-affect softener",
    }

    with pytest.raises(ValueError, match=r"\(1, 7, 4\)"):
        pin_features(baseline_ctx, pre_hypotheses=pre_hypotheses)
