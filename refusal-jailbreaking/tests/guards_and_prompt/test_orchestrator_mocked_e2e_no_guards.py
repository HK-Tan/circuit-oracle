"""End-to-end transcript that satisfies every guard must run cleanly.

A well-formed transcript has the full chain:

  build_circuit -> pin_features (covers build_features exactly)
                -> batched_anchor_sweep
                -> batched_supernode_sweep round 1 (>=3 tuples, all rationales non-empty)
                -> batched_supernode_sweep round 2 (>=3 tuples, all rationales non-empty)

When every guard helper is given this transcript none of them should fire.
This is the inverse of the other guard tests and protects against
overzealous guards.

Guard contract assumed: the three helpers from the other guard test files.
The guards may also be consolidated into a single `check_guards(transcript, build_features)`
returning a list of fired-guard results; in that case the test should be
trivially adaptable -- assert the returned list is empty.

Fails with ImportError if the guard helper is missing.
"""
from __future__ import annotations

import pytest


def _well_formed_tuples():
    return [
        {
            "features": [{"layer": 1, "feature_idx": 5, "pos": 7, "value": -10.0}],
            "rationale": "Negation gate alone (route=negation).",
        },
        {
            "features": [{"layer": 2, "feature_idx": 11, "pos": 7, "value": -10.0}],
            "rationale": "Affect softener alone (route=affect).",
        },
        {
            "features": [
                {"layer": 1, "feature_idx": 5, "pos": 7, "value": -10.0},
                {"layer": 2, "feature_idx": 11, "pos": 7, "value": -10.0},
                {"layer": 3, "feature_idx": 33, "pos": 7, "value": -10.0},
            ],
            "rationale": (
                "Cross-route union: negation + affect + sensitivity-precursor."
            ),
        },
    ]


def _well_formed_transcript():
    return [
        {
            "tool": "build_circuit",
            "input": {
                "nodes": [
                    {
                        "label": "Suppression circuit",
                        "features": [
                            {"layer": 1, "feature_idx": 5, "pos": 7},
                            {"layer": 2, "feature_idx": 11, "pos": 7},
                            {"layer": 3, "feature_idx": 33, "pos": 7},
                        ],
                    }
                ]
            },
            "output": {"ok": True},
        },
        {
            "tool": "pin_features",
            "input": {
                "pre_hypotheses": {
                    "(1, 5, 7)": "Likely negation/inability gate.",
                    "(2, 11, 7)": "Likely refusal-affect softener.",
                    "(3, 33, 7)": "Likely sensitivity-precursor (cryptic label).",
                }
            },
            "output": {"ok": True},
        },
        {
            "tool": "batched_anchor_sweep",
            "input": {},
            "output": {"measurements": [], "reassess_records": {}},
        },
        {
            "tool": "batched_supernode_sweep",
            "input": {"tuples": _well_formed_tuples()},
            "output": {"measurements": []},
        },
        {
            "tool": "batched_supernode_sweep",
            "input": {"tuples": _well_formed_tuples()},
            "output": {"measurements": []},
        },
    ]


def test_well_formed_transcript_passes_all_guards():
    """A transcript that satisfies every guard must trip none of them."""
    from circuit_oracle.orchestrator import (
        check_anchor_sweep_guard,
        check_pin_coverage_guard,
        check_supernode_guard,
    )

    build_features = [(1, 5, 7), (2, 11, 7), (3, 33, 7)]
    transcript = _well_formed_transcript()

    pin_result = check_pin_coverage_guard(transcript, build_features=build_features)
    assert pin_result.fired is False, (
        "Pin-coverage guard fired on a transcript whose pin_features keys "
        "match build_features exactly. Message: " + repr(pin_result.message)
    )

    anchor_result = check_anchor_sweep_guard(transcript)
    assert anchor_result.fired is False, (
        "Anchor-sweep guard fired on a transcript with batched_anchor_sweep "
        "after pin_features. Message: " + repr(anchor_result.message)
    )

    supernode_result = check_supernode_guard(transcript)
    assert supernode_result.fired is False, (
        "Supernode guard fired on a transcript with 2 rounds of >=3 "
        "well-rationalised tuples. Message: " + repr(supernode_result.message)
    )
