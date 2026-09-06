"""batched_anchor_sweep raises if pin_features was not called first.

Asserts the prerequisite chain in the harness: calling
`batched_anchor_sweep` before `pin_features` has populated `ctx.pinned_features`
raises ValueError with a message that tells the agent to call pin_features first.
"""
from __future__ import annotations

import pytest


def test_batched_anchor_sweep_requires_pin(baseline_ctx):
    from circuit_oracle.tools import batched_anchor_sweep

    # `ctx.pinned_features` not populated (no pin_features call).
    with pytest.raises(ValueError, match=r"call pin_features first"):
        batched_anchor_sweep(baseline_ctx)
