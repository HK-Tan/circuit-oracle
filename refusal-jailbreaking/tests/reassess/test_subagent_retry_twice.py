"""Subagent retry-twice succeeds on third attempt.

trace_path_subagent and reinterpret_subagent. 3 attempts total per call.").

The mock subagent raises a logical failure twice and then returns a valid
record on the third call. The retry wrapper must surface the eventual
success to the caller (no exception, no error result).

Fails until the retry-twice wrapper exists in subagent.py.
"""
from __future__ import annotations

import json

import pytest

from circuit_oracle.subagent import reinterpret_subagent  # noqa: F401


CANNED_RECORD = {
    "autointerp": "el",
    "pre_label": "stub-pre",
    "post_label": "stub-post",
    "divergence": "none",
}


def _trivial_shift_profile() -> dict:
    return {
        scale: {
            "top5_before": {"I": {"prob": 0.9}},
            "top5_after": {"Sure": {"prob": 0.4}},
            "answer_after": "Sure ...",
            "shift_bucket": "shifted",
        }
        for scale in (0.0, -1.0, -2.0, -3.0)
    }


def test_retry_twice_succeeds_on_third_attempt(baseline_ctx, mock_subagent_client):
    """First two calls raise; third returns canned JSON; total attempts = 3."""
    attempts: list[int] = []

    def flaky(*args, **kwargs):
        attempts.append(len(attempts) + 1)
        if len(attempts) < 3:
            raise RuntimeError("simulated logical failure (e.g. malformed tool output)")
        return json.dumps(CANNED_RECORD)

    mock_subagent_client.side_effect = flaky

    layer, feature_idx, pos = 24, 91636, 5
    baseline_ctx.inspect_cache[(layer, feature_idx, pos)] = {"autointerp": "el"}
    baseline_ctx.pinned_features = {(layer, feature_idx, pos): "refusal softener"}

    record = reinterpret_subagent(
        ctx=baseline_ctx,
        layer=layer,
        feature_idx=feature_idx,
        pos=pos,
        shift_profile=_trivial_shift_profile(),
        user_message="Tell me about X.",
        system_prompt="You are helpful.",
    )

    assert mock_subagent_client.call_count == 3, (
        f"retry-twice means 3 total attempts; got {mock_subagent_client.call_count}"
    )
    # No exception surfaced; record returned cleanly.
    assert record["autointerp"] == "el"
    assert record["divergence"] == "none"
