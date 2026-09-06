"""LOAD-BEARING: batched single-feature intervention matches single-call result.

Asserts that one row of `feature_intervention_batched` with a single intervention tuple
is fp32-close to the corresponding `feature_intervention` single-call output on the
tiny toy fixture. If this passes, the per-row indexing in `calculate_delta_hook` is
mathematically correct on at least the simplest batch shape.
"""
from __future__ import annotations

import pytest
from numpy.testing import assert_allclose


def test_batched_matches_single_one_feature(tiny_model, baseline_ctx):
    # `feature_intervention_batched` is not yet a method on ReplacementModel, # AttributeError if it is missing. Per the test-pattern rules,
    # feature_intervention* are bound methods, not module functions.
    intervention = [{"layer": 1, "feature_idx": 3, "pos": 5, "value": 0.0}]

    batched = tiny_model.replacement_model.feature_intervention_batched(
        inputs="hello", intervention_lists=[intervention]
    )
    single = tiny_model.replacement_model.feature_intervention(
        inputs="hello", interventions=intervention
    )

    # batched.logits is [B, T, V]; single.logits is [1, T, V] (matches the
    # real ReplacementModel). Index both down to the shared [T, V] body.
    assert_allclose(batched.logits[0], single.logits[0], rtol=1e-5)
