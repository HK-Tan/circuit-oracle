"""Supernode guard fires when a call has fewer than 3 tuples.

Each `batched_supernode_sweep` call must include at least 3 distinct tuples.
A call with only 2 tuples does not probe enough distributed-suppression
hypotheses to qualify for Round 1 or Round 2.

Guard contract assumed for this test: see `test_guards_supernode_min_rounds.py`.

Fails with ImportError if the guard helper is missing.
"""
from __future__ import annotations

import pytest


def _two_tuples_only():
    """Helper: an under-spec'd tuples payload with only 2 entries."""
    return [
        {
            "features": [{"layer": 1, "feature_idx": 5, "pos": 7, "value": -10.0}],
            "rationale": "Negation gate alone.",
        },
        {
            "features": [{"layer": 2, "feature_idx": 11, "pos": 7, "value": -10.0}],
            "rationale": "Affect softener alone.",
        },
    ]


def test_supernode_guard_fires_when_call_has_two_tuples():
    """Two batched_supernode_sweep calls each with only 2 tuples must fire the guard."""
    from circuit_oracle.orchestrator import check_supernode_guard

    transcript = [
        {"tool": "build_circuit", "input": {"nodes": []}, "output": {"ok": True}},
        {
            "tool": "pin_features",
            "input": {"pre_hypotheses": {"(1, 5, 7)": "x", "(2, 11, 7)": "y"}},
            "output": {"ok": True},
        },
        {
            "tool": "batched_anchor_sweep",
            "input": {},
            "output": {"measurements": []},
        },
        {
            "tool": "batched_supernode_sweep",
            "input": {"tuples": _two_tuples_only()},
            "output": {"measurements": []},
        },
        {
            "tool": "batched_supernode_sweep",
            "input": {"tuples": _two_tuples_only()},
            "output": {"measurements": []},
        },
    ]
    result = check_supernode_guard(transcript)
    assert result.fired is True, (
        "Supernode guard must fire when any batched_supernode_sweep call has "
        "fewer than 3 tuples."
    )
    assert (
        "tuples" in result.message.lower()
        or "batched_supernode_sweep" in result.message
    ), (
        "Guard message must indicate the per-call tuple minimum. "
        "Got: " + repr(result.message)
    )
