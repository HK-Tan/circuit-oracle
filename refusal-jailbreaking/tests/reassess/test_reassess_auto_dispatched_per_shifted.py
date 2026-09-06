"""REASSESS auto-dispatch fires once per shifted feature.

at any scale, harness fan-outs reinterpret_subagent ...").

Set up 5 pinned features. Monkeypatch `circuit_oracle.tools.shift_bucket` so
that features at indices 0, 2, 4 are flagged 'shifted' (across all 4 of their
scales) and features 1, 3 are 'no-shift'. The mock subagent must be called
exactly 3 times (one per shifted feature, irrespective of how many scales
shifted within that feature).

Test-pattern rule: tests MUST use monkeypatch.setattr on
shift_bucket. The previous `ctx._test_*` attribute pattern is forbidden
because it would require production code to know about test seams.

Fails if reinterpret_subagent stops being dispatched inside
batched_anchor_sweep.
"""
from __future__ import annotations

import json

import pytest

from circuit_oracle.tools import batched_anchor_sweep, pin_features  # noqa: F401


CANNED_RECORD = json.dumps(
    {
        "autointerp": "stub",
        "pre_label": "stub-pre",
        "post_label": "stub-post",
        "divergence": "none",
    }
)


def _shift_bucket_by_feature_index(shifted_feature_indices, n_scales=4):
    """Build a `shift_bucket` replacement that returns 'shifted' for calls
    whose feature index (call_count // n_scales) is in the given set.

    Assumes the harness iterates feature-outer, scale-inner, calling
    shift_bucket once per (feature, scale). Phase 1's batched_anchor_sweep
    is the load-bearing contract here, if it iterates differently, this
    test will surface that.
    """
    state = {"call_count": 0}
    shifted = set(shifted_feature_indices)

    def fake(*args, **kwargs):
        idx = state["call_count"] // n_scales
        state["call_count"] += 1
        return "shifted" if idx in shifted else "no-shift"

    return fake


def test_reassess_called_once_per_shifted_feature(
    monkeypatch, baseline_ctx, mock_subagent_client
):
    """3 shifted features + 2 no-shift -> exactly 3 subagent calls."""
    mock_subagent_client.set_response(json.loads(CANNED_RECORD))

    pinned = {
        (0, 0, 0): "hypothesis A",
        (0, 1, 0): "hypothesis B",
        (0, 2, 0): "hypothesis C",
        (0, 3, 0): "hypothesis D",
        (0, 4, 0): "hypothesis E",
    }
    # pin_features is exercised elsewhere. Here we drive ctx directly, to keep
    # this test independent of its implementation details.
    baseline_ctx.pinned_features = pinned

    monkeypatch.setattr(
        "circuit_oracle.tools.shift_bucket",
        _shift_bucket_by_feature_index({0, 2, 4}),
    )

    batched_anchor_sweep(baseline_ctx)

    assert len(mock_subagent_client.calls) == 3, (
        f"reinterpret_subagent must dispatch exactly once per shifted feature; "
        f"expected 3, got {len(mock_subagent_client.calls)}."
    )


def test_reassess_not_called_when_no_features_shifted(
    monkeypatch, baseline_ctx, mock_subagent_client
):
    """All-no-shift sweep must not dispatch any subagents."""
    mock_subagent_client.set_response(json.loads(CANNED_RECORD))

    pinned = {
        (0, 0, 0): "h",
        (0, 1, 0): "h",
    }
    baseline_ctx.pinned_features = pinned

    monkeypatch.setattr(
        "circuit_oracle.tools.shift_bucket",
        lambda *a, **k: "no-shift",
    )

    batched_anchor_sweep(baseline_ctx)

    assert len(mock_subagent_client.calls) == 0, (
        f"No shifted features -> 0 reinterpret_subagent calls; "
        f"got {len(mock_subagent_client.calls)}."
    )
