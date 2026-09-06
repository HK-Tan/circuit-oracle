"""Anchor-sweep guard fires when pin_features ran but batched_anchor_sweep did not.

The agent must call `batched_anchor_sweep` after `pin_features`. The
argless sweep is the trigger for the auto-dispatched REASSESS fan-out
(Section 2.4); skipping it means no triple-label records are produced
and the paper's load-bearing artifact (`autointerp_and_pre` divergence
count) is missing.

Guard contract this test pins:

    from circuit_oracle.orchestrator import check_anchor_sweep_guard
    result = check_anchor_sweep_guard(transcript)
    # result.fired: bool
    # result.message: str (mentions "batched_anchor_sweep" when fired)

Fails with ImportError if the guard helper is missing.
"""
from __future__ import annotations

import pytest


def test_anchor_sweep_guard_fires_when_pinned_but_no_sweep():
    """pin_features called but no subsequent batched_anchor_sweep must fire the guard."""
    from circuit_oracle.orchestrator import check_anchor_sweep_guard

    build_features = [(1, 5, 7), (2, 11, 7)]
    transcript = [
        {
            "tool": "build_circuit",
            "input": {"nodes": []},
            "output": {"ok": True},
        },
        {
            "tool": "pin_features",
            "input": {
                "pre_hypotheses": {
                    "(1, 5, 7)": "refusal-affect softener",
                    "(2, 11, 7)": "negation gate",
                }
            },
            "output": {"ok": True},
        },
        # No batched_anchor_sweep call here.
    ]
    result = check_anchor_sweep_guard(transcript)
    assert result.fired is True, (
        "Anchor-sweep guard must fire when pin_features ran but "
        "batched_anchor_sweep did not."
    )
    assert "batched_anchor_sweep" in result.message, (
        "Guard message must reference `batched_anchor_sweep`. "
        "Got: " + repr(result.message)
    )
