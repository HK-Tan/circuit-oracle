"""Subagent retry-twice exhaustion surfaces an error result.

When all 3 attempts fail (retry-twice exhausted), the wrapper must NOT crash
the harness; it must return an error result (or raise a wrapped exception)
that makes the retry count visible. The orchestrator can then skip the
feature without aborting the entire anchor sweep.

Fails until the retry wrapper exists and handles exhaustion gracefully.
"""
from __future__ import annotations

import pytest

from circuit_oracle.subagent import reinterpret_subagent  # noqa: F401


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


def test_retry_exhaustion_returns_error_result(baseline_ctx, mock_subagent_client):
    """3 raises in a row -> error surfaced with retry count, no propagation."""

    def always_raises(*args, **kwargs):
        raise RuntimeError("simulated persistent failure")

    mock_subagent_client.side_effect = always_raises

    layer, feature_idx, pos = 24, 91636, 5
    baseline_ctx.inspect_cache[(layer, feature_idx, pos)] = {"autointerp": "el"}
    baseline_ctx.pinned_features = {(layer, feature_idx, pos): "h"}

    error_text: str = ""
    result = None
    try:
        result = reinterpret_subagent(
            ctx=baseline_ctx,
            layer=layer,
            feature_idx=feature_idx,
            pos=pos,
            shift_profile=_trivial_shift_profile(),
            user_message="Tell me about X.",
            system_prompt="You are helpful.",
        )
    except Exception as exc:  # noqa: BLE001 - wrapper may opt to raise instead
        error_text = str(exc)

    # 3 total attempts (1 + 2 retries).
    assert mock_subagent_client.call_count == 3, (
        f"retry-twice should consume exactly 3 attempts; "
        f"got {mock_subagent_client.call_count}"
    )

    # Either a result dict tagged as error, or a wrapped exception. Whichever
    # the wrapper picks, the retry count must be visible in the surfaced text.
    if result is not None:
        assert isinstance(result, dict), (
            f"on exhaustion, reinterpret_subagent should return an error dict, "
            f"got {type(result).__name__}"
        )
        assert result.get("error") or result.get("divergence") == "error", (
            f"error result must signal failure (e.g. 'error' key or "
            f"divergence='error'); got {result}"
        )
        surfaced = str(result)
    else:
        surfaced = error_text

    assert "3" in surfaced or "retry" in surfaced.lower() or "attempt" in surfaced.lower(), (
        f"surfaced failure should mention retry count or attempts; got: {surfaced!r}"
    )
