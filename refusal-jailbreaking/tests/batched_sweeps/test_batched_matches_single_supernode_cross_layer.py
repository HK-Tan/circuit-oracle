"""batched supernode spanning two layers x 4 scales matches per-row singles.

Asserts that a supernode whose features span two layers (so interventions register in
`interventions_by_layer` under multiple keys) still produces per-row outputs identical
to the equivalent single calls. Catches multi-layer hook fan-out bugs.
"""
from __future__ import annotations

import pytest
from numpy.testing import assert_allclose


def test_batched_matches_single_supernode_cross_layer(tiny_model, baseline_ctx):
    # Test-pattern rule: feature_intervention* are bound methods on
    # ReplacementModel, not module-level functions.
    supernode = [
        {"layer": 0, "feature_idx": 1, "pos": 3},
        {"layer": 0, "feature_idx": 5, "pos": 3},
        {"layer": 1, "feature_idx": 2, "pos": 4},
        {"layer": 1, "feature_idx": 7, "pos": 4},
    ]
    scales = [0.0, -1.0, -2.0, -3.0]

    intervention_lists = []
    for scale in scales:
        intervention_lists.append([{**f, "value": scale} for f in supernode])

    batched = tiny_model.replacement_model.feature_intervention_batched(
        inputs="hello", intervention_lists=intervention_lists
    )

    for row_idx, single_list in enumerate(intervention_lists):
        single = tiny_model.replacement_model.feature_intervention(
            inputs="hello", interventions=single_list
        )
        # batched.logits is [B, T, V]; single.logits is [1, T, V].
        assert_allclose(batched.logits[row_idx], single.logits[0], rtol=1e-5)
