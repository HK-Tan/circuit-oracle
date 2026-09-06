"""K features x 4 scales batched matches per-row single calls.

Asserts that a batch built from K distinct features at scales {0, -1, -2, -3} produces
the same per-row logits as making 4K independent `feature_intervention` calls on the
tiny toy fixture. Catches scale-aware indexing bugs in `calculate_delta_hook`.
"""
from __future__ import annotations

import pytest
from numpy.testing import assert_allclose


def test_batched_matches_single_multi_scale(tiny_model, baseline_ctx):
    # Test-pattern rule: feature_intervention* are bound methods on
    # ReplacementModel, not module-level functions.
    features = [
        {"layer": 0, "feature_idx": 2, "pos": 3},
        {"layer": 1, "feature_idx": 5, "pos": 4},
        {"layer": 1, "feature_idx": 7, "pos": 2},
    ]
    scales = [0.0, -1.0, -2.0, -3.0]

    intervention_lists = []
    for feat in features:
        for scale in scales:
            intervention_lists.append([{**feat, "value": scale}])

    batched = tiny_model.replacement_model.feature_intervention_batched(
        inputs="hello", intervention_lists=intervention_lists
    )

    for row_idx, single_list in enumerate(intervention_lists):
        single = tiny_model.replacement_model.feature_intervention(
            inputs="hello", interventions=single_list
        )
        # batched.logits is [B, T, V]; single.logits is [1, T, V].
        assert_allclose(batched.logits[row_idx], single.logits[0], rtol=1e-5)
