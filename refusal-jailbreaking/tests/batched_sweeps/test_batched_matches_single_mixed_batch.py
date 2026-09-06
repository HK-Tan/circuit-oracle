"""mixed batch with some 1-tuple rows and some 3-tuple rows.

Asserts that a single batched forward where row 0 has one intervention but row 1 has
three (ragged per-row interventions) still produces per-row results identical to
independent single calls. Catches bugs where rows leak interventions across the batch
dimension.
"""
from __future__ import annotations

import pytest
from numpy.testing import assert_allclose


def test_batched_matches_single_mixed_batch(tiny_model, baseline_ctx):
    # Test-pattern rule: feature_intervention* are bound methods on
    # ReplacementModel, not module-level functions.
    intervention_lists = [
        [{"layer": 1, "feature_idx": 3, "pos": 5, "value": -1.0}],
        [
            {"layer": 0, "feature_idx": 2, "pos": 3, "value": -2.0},
            {"layer": 1, "feature_idx": 5, "pos": 4, "value": -2.0},
            {"layer": 1, "feature_idx": 6, "pos": 4, "value": -2.0},
        ],
        [{"layer": 0, "feature_idx": 1, "pos": 2, "value": 0.0}],
        [
            {"layer": 1, "feature_idx": 2, "pos": 5, "value": -3.0},
            {"layer": 1, "feature_idx": 7, "pos": 5, "value": -3.0},
            {"layer": 0, "feature_idx": 4, "pos": 3, "value": -3.0},
        ],
    ]

    batched = tiny_model.replacement_model.feature_intervention_batched(
        inputs="hello", intervention_lists=intervention_lists
    )

    for row_idx, single_list in enumerate(intervention_lists):
        single = tiny_model.replacement_model.feature_intervention(
            inputs="hello", interventions=single_list
        )
        # batched.logits is [B, T, V]; single.logits is [1, T, V].
        assert_allclose(batched.logits[row_idx], single.logits[0], rtol=1e-5)
