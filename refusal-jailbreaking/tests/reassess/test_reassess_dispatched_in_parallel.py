"""REASSESS fan-out runs in parallel via ThreadPoolExecutor.

pattern as orchestrator.py:530-542 for trace_path_subagent").

If reinterpret_subagent is dispatched serially for N=3 shifted features and
each subagent takes ~0.5s, total wall-clock is ~1.5s. Under parallel
ThreadPoolExecutor dispatch, total wall-clock should be ~0.5s. We assert
elapsed < 1.0s as a generous parallelism floor.

Test-pattern rule: tests MUST use monkeypatch.setattr on
shift_bucket. The previous `ctx._test_*` attribute pattern is forbidden
because it would require production code to know about test seams.

Fails if the dispatch path stops being parallel.
"""
from __future__ import annotations

import json
import time

import pytest

from circuit_oracle.tools import batched_anchor_sweep  # noqa: F401


CANNED_RECORD = {
    "autointerp": "stub",
    "pre_label": "stub-pre",
    "post_label": "stub-post",
    "divergence": "none",
}


def test_reassess_dispatch_is_parallel(
    monkeypatch, baseline_ctx, mock_subagent_client
):
    """3 shifted features with 0.5s mock latency must finish in ~0.5s, not ~1.5s."""

    # Wrap the mock client so each call sleeps 0.5s before returning. The
    # _MockSubagentClient still records calls in `.calls`.
    original_call = mock_subagent_client.__class__.__call__

    def slow_call(self, *args, **kwargs):
        time.sleep(0.5)
        return original_call(self, *args, **kwargs)

    monkeypatch.setattr(
        mock_subagent_client.__class__, "__call__", slow_call
    )
    mock_subagent_client.set_response(CANNED_RECORD)

    pinned = {
        (0, 0, 0): "hypothesis A",
        (0, 1, 0): "hypothesis B",
        (0, 2, 0): "hypothesis C",
    }
    baseline_ctx.pinned_features = pinned

    # All 3 features shifted -> 3 parallel dispatches.
    monkeypatch.setattr(
        "circuit_oracle.tools.shift_bucket",
        lambda *a, **k: "shifted",
    )

    start = time.monotonic()
    batched_anchor_sweep(baseline_ctx)
    elapsed = time.monotonic() - start

    n_calls = len(mock_subagent_client.calls)
    assert n_calls == 3, (
        f"Sanity: expected 3 subagent calls, got {n_calls}"
    )
    assert elapsed < 1.0, (
        f"reinterpret_subagent dispatch was not parallel: expected ~0.5s "
        f"under ThreadPoolExecutor, got {elapsed:.2f}s "
        f"(serial would be ~{0.5 * n_calls:.1f}s)."
    )
