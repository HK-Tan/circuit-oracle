"""Supernode guard fires when any tuple has an empty rationale.

plus Section 2.2 ("a free-text rationale per tuple").

The rationale is the agent's free-text justification for grouping the
features in a supernode tuple. An empty rationale defeats the purpose of
the cognitive-commit design: the harness has no record of WHY the agent
believes those features share a role. The guard must catch this even when
round and tuple-count requirements are otherwise satisfied.

Guard contract assumed for this test: see `test_guards_supernode_min_rounds.py`.

Fails with ImportError if the guard helper is missing.
"""
from __future__ import annotations

import pytest


def _three_tuples_one_empty_rationale():
    """Two well-formed tuples plus one with rationale=''."""
    return [
        {
            "features": [{"layer": 1, "feature_idx": 5, "pos": 7, "value": -10.0}],
            "rationale": "Negation gate alone.",
        },
        {
            "features": [{"layer": 2, "feature_idx": 11, "pos": 7, "value": -10.0}],
            "rationale": "",  # empty rationale -- must trip the guard
        },
        {
            "features": [
                {"layer": 1, "feature_idx": 5, "pos": 7, "value": -10.0},
                {"layer": 2, "feature_idx": 11, "pos": 7, "value": -10.0},
            ],
            "rationale": "Cross-route union.",
        },
    ]


def test_supernode_guard_fires_on_empty_rationale_tuple():
    """One tuple with empty rationale across two otherwise-valid rounds must fire the guard."""
    from circuit_oracle.orchestrator import check_supernode_guard

    tuples = _three_tuples_one_empty_rationale()
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
            "input": {"tuples": tuples},
            "output": {"measurements": []},
        },
        {
            "tool": "batched_supernode_sweep",
            "input": {"tuples": tuples},
            "output": {"measurements": []},
        },
    ]
    result = check_supernode_guard(transcript)
    assert result.fired is True, (
        "Supernode guard must fire when any tuple has rationale='' "
        "."
    )
    assert "rationale" in result.message.lower(), (
        "Guard message must mention the empty rationale so the agent knows "
        "what to fix. Got: " + repr(result.message)
    )
