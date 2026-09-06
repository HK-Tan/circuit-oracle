"""batched_supernode_sweep rejects calls with fewer than 3 tuples.

Asserts the Phase 3 contract in the harness: each `batched_supernode_sweep`
call must include at least 3 supernode tuples. A call with 2 tuples raises ValueError.
"""
from __future__ import annotations

import pytest


def test_batched_supernode_sweep_min_3_tuples(baseline_ctx):
    from circuit_oracle.tools import batched_supernode_sweep

    tuples = [
        {
            "features": [(1, 5, 4), (1, 7, 4)],
            "rationale": "affect cluster",
        },
        {
            "features": [(0, 1, 3), (1, 5, 4)],
            "rationale": "cross-route negation x affect",
        },
    ]

    with pytest.raises(ValueError, match=r"3"):
        batched_supernode_sweep(baseline_ctx, tuples=tuples)
