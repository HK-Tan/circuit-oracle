"""Supernode guard fires when only one batched_supernode_sweep call ran.

The orchestrator must call `batched_supernode_sweep` at least twice (Round 1
and Round 2). Round 2 must be informed by Round 1 shift profiles, which
requires two distinct rounds to exist.

Guard contract this test pins:

    from circuit_oracle.orchestrator import check_supernode_guard
    result = check_supernode_guard(transcript)
    # result.fired: bool
    # result.message: str (mentions "batched_supernode_sweep" when fired)

Fails with ImportError if the guard helper is missing.
"""
from __future__ import annotations

import pytest


def _three_tuples_with_rationale():
    """Helper: a well-formed `tuples` payload with 3 valid entries."""
    return [
        {
            "features": [{"layer": 1, "feature_idx": 5, "pos": 7, "value": -10.0}],
            "rationale": "Negation gate alone.",
        },
        {
            "features": [{"layer": 2, "feature_idx": 11, "pos": 7, "value": -10.0}],
            "rationale": "Affect softener alone.",
        },
        {
            "features": [
                {"layer": 1, "feature_idx": 5, "pos": 7, "value": -10.0},
                {"layer": 2, "feature_idx": 11, "pos": 7, "value": -10.0},
            ],
            "rationale": "Cross-route: negation + affect.",
        },
    ]


def test_supernode_guard_fires_on_only_one_round():
    """Single batched_supernode_sweep call must fire the guard (need >=2 rounds)."""
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
            "input": {"tuples": _three_tuples_with_rationale()},
            "output": {"measurements": []},
        },
        # Only one batched_supernode_sweep call.
    ]
    result = check_supernode_guard(transcript)
    assert result.fired is True, (
        "Supernode guard must fire when fewer than 2 batched_supernode_sweep "
        "calls were made."
    )
    assert "batched_supernode_sweep" in result.message, (
        "Guard message must reference `batched_supernode_sweep`. "
        "Got: " + repr(result.message)
    )
