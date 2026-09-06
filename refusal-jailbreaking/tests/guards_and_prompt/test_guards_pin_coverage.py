"""Pin-coverage guard fires when the agent never calls pin_features.

Guard contract this test pins:

    from circuit_oracle.orchestrator import check_pin_coverage_guard
    result = check_pin_coverage_guard(transcript, build_features=[...])
    # result.fired: bool
    # result.message: str (mentions "pin_features" when fired)

The transcript schema is a list of dicts shaped like the existing
`all_tool_calls` ledger built inside `run_circuit_oracle`:

    [{"tool": "build_circuit", "input": {...}, "output": {...}}, ...]

The `build_features` argument is the canonical pinned-feature set the
new `build_circuit` writes onto `ctx.build_features`. Passing it explicitly here avoids depending on a live `ToolContext`.

Fails with ImportError if the guard helper is missing.
"""
from __future__ import annotations

import pytest


def test_pin_coverage_guard_fires_when_no_pin_features_call():
    """Transcript with build_circuit but no pin_features call must fire the guard."""
    from circuit_oracle.orchestrator import check_pin_coverage_guard

    build_features = [(1, 5, 7), (2, 11, 7), (3, 33, 7)]
    transcript = [
        {
            "tool": "build_circuit",
            "input": {"nodes": [{"label": "Refusal gate", "features": []}]},
            "output": {"ok": True},
        },
        # No pin_features call anywhere after build_circuit.
    ]
    result = check_pin_coverage_guard(transcript, build_features=build_features)
    assert result.fired is True, (
        "Pin-coverage guard must fire when pin_features was never called "
        "after build_circuit."
    )
    assert "pin_features" in result.message, (
        "Guard message must reference `pin_features` so the nudge tells the "
        "agent which tool to call. Got: " + repr(result.message)
    )
