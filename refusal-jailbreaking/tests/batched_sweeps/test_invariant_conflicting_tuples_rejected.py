"""conflicting tuples in the same batch row are rejected loudly.

Asserts the build-time invariant in the harness: within one layer's tuple list,
each `(row_idx, feature_idx)` pair must be unique. Repeating the same row x feature with
conflicting values must raise ValueError instead of silently last-write-wins.
"""
from __future__ import annotations

import pytest


def test_invariant_conflicting_tuples_rejected(tiny_model, baseline_ctx):
    # Test-pattern rule: feature_intervention* are bound methods on
    # ReplacementModel, not module-level functions.
    # Same row, same (layer, feature_idx, pos), but two different values:
    intervention_lists = [
        [
            {"layer": 1, "feature_idx": 3, "pos": 5, "value": -1.0},
            {"layer": 1, "feature_idx": 3, "pos": 5, "value": -3.0},
        ],
    ]

    with pytest.raises(ValueError, match=r"conflicting"):
        tiny_model.replacement_model.feature_intervention_batched(
            inputs="hello", intervention_lists=intervention_lists
        )
