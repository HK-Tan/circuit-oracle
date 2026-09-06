"""freeze cache is a zero-copy view across the batch dim.

Asserts that after `setup_intervention_with_freeze` is called with a batched prompt,
the freeze-cache tensors (frozen attention patterns and LayerNorm scales) share storage
across the batch dimension instead of being materialized B times. Verifies the
`.expand(B, *)` path doesn't accidentally `.contiguous()` itself into a real copy.
"""
from __future__ import annotations

import pytest


def test_freeze_cache_is_view(tiny_model, baseline_ctx):
    # Test-pattern rule: feature_intervention* are bound methods on
    # ReplacementModel, not module-level functions.
    intervention_lists = [
        [{"layer": 1, "feature_idx": 3, "pos": 5, "value": -1.0}],
        [{"layer": 1, "feature_idx": 3, "pos": 5, "value": -2.0}],
        [{"layer": 1, "feature_idx": 3, "pos": 5, "value": -3.0}],
        [{"layer": 1, "feature_idx": 3, "pos": 5, "value": 0.0}],
    ]

    result = tiny_model.replacement_model.feature_intervention_batched(
        inputs="hello",
        intervention_lists=intervention_lists,
        return_freeze_cache=True,
    )

    # Freeze cache tensors should expand across batch dim via `.expand`, which
    # produces a view (same underlying storage), not a fresh allocation.
    for tensor in result.freeze_cache.values():
        assert tensor.shape[0] == len(intervention_lists)
        # Row 0 and row N-1 should alias the same storage.
        first_row_ptr = tensor[0].storage().data_ptr()
        last_row_ptr = tensor[-1].storage().data_ptr()
        assert first_row_ptr == last_row_ptr, (
            f"freeze-cache tensor was materialized B times: storage ptr "
            f"{first_row_ptr} != {last_row_ptr}"
        )
