"""Pin-coverage guard fires when pin_features misses build_features keys.

If `pin_features` is called but its `pre_hypotheses` map does not exactly
cover `ctx.build_features`, the guard must fire. This is the orchestrator-
side end-of-turn safety net behind the tool-level strict reject described
in Section 2.2 ("the agent must amend either side").

Transcript schema and guard signature mirror
`test_guards_pin_coverage.py`. The `pre_hypotheses` payload mirrors the
`PreHypothesisMap` shape from `circuit_oracle.config` (keys are
`(layer, feature_idx, pos)` tuples; values are one-sentence strings).

Fails with ImportError if the guard helper is missing.
"""
from __future__ import annotations

import pytest


def test_pin_coverage_guard_fires_when_pin_features_subset():
    """pin_features missing one of the build_features keys must fire the guard."""
    from circuit_oracle.orchestrator import check_pin_coverage_guard

    build_features = [(1, 5, 7), (2, 11, 7), (3, 33, 7)]
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
                    # Missing (3, 33, 7) on purpose. JSON-style string keys
                    # are how this serializes over the Anthropic tool API,
                    # but the harness recovers the tuple internally.
                    "(1, 5, 7)": "refusal-affect softener",
                    "(2, 11, 7)": "negation gate",
                }
            },
            "output": {"ok": True},
        },
    ]
    result = check_pin_coverage_guard(transcript, build_features=build_features)
    assert result.fired is True, (
        "Pin-coverage guard must fire when pin_features keys are a strict "
        "subset of build_features."
    )
    assert "pin_features" in result.message or "missing" in result.message.lower(), (
        "Guard message should indicate the missing pin coverage. "
        "Got: " + repr(result.message)
    )
