"""The three GPU funnels in tools.py must actually take the coarse lock.

test_gpu_lock.py proves the lock serializes. This proves it is WIRED IN, which is
the part a refactor silently drops. Without these, deleting a ``with _gpu().hold``
from tools.py leaves 806 green tests and an OOM on the first concurrent batch.

The coarse locks exist for MEMORY, not correctness: one 68-row anchor sweep
decoding 800 tokens holds ~8 GB of KV cache, so N concurrent runs each sitting
mid-decode would want N x 8 GB. See circuit_oracle/gpu_lock.py.
"""
from __future__ import annotations

import contextlib

import pytest
import torch

from circuit_oracle import tools


class _Recorder:
    """Stands in for the active GpuLock and records which sections were held."""

    enabled = True

    def __init__(self):
        self.labels: list[str] = []
        self.depth = 0
        self.max_depth = 0

    @contextlib.contextmanager
    def hold(self, label: str = ""):
        self.labels.append(label)
        self.depth += 1
        self.max_depth = max(self.max_depth, self.depth)
        try:
            yield
        finally:
            self.depth -= 1


@pytest.fixture
def recorder(monkeypatch):
    rec = _Recorder()
    monkeypatch.setattr(tools, "_gpu", lambda: rec)
    return rec


def test_decode_one_chunk_holds_the_lock_for_the_whole_chunk(recorder, monkeypatch):
    """The KV-cache lock. Losing this is the OOM."""
    seen_depth = []

    def fake_impl(*_args, **_kwargs):
        # The cache is live at this point, so the lock must be held right here,
        # not merely acquired somewhere around the call.
        seen_depth.append(recorder.depth)
        return (["out"], torch.empty(0))

    monkeypatch.setattr(tools, "_decode_one_chunk_impl", fake_impl)
    out = tools._decode_one_chunk(object(), "prompt", object(), 0, [[]], 8)

    assert out[0] == ["out"]
    assert recorder.labels == ["_decode_one_chunk"]
    assert seen_depth == [1], "lock was not held while the KV cache was live"


def test_run_batched_intervention_locks_once_per_chunk(recorder):
    """Per chunk, not around the whole loop: a long row list would otherwise
    hold the GPU for an entire sweep and starve every other run."""
    class _Model:
        def feature_intervention_batched(self, inputs, intervention_lists):
            assert recorder.depth == 1, "forward ran outside the lock"
            n = len(intervention_lists)
            return type("R", (), {"logits": torch.zeros(n, 2)})()

    ctx = type("Ctx", (), {"replacement_model": _Model(), "baseline_prompt": "p"})()
    rows = [[] for _ in range(5)]
    out = tools._run_batched_intervention(ctx, rows, batch_size=2)

    assert out.shape[0] == 5
    # 5 rows at batch_size 2 is three chunks, so three separate acquisitions.
    assert recorder.labels == ["_run_batched_intervention"] * 3
    assert recorder.max_depth == 1


def test_run_holds_the_lock_around_the_forward(recorder):
    class _Model:
        def feature_intervention(self, *_a, **_k):
            assert recorder.depth == 1, "forward ran outside the lock"
            return torch.zeros(1, 2), None

    tools._run([], "prompt", model=_Model())
    assert recorder.labels == ["_run"]


def test_run_does_not_sleep_while_holding_the_lock(recorder, monkeypatch):
    """Backoff must happen OUTSIDE the GPU section.

    Sleeping under the lock would stall every other concurrent run for up to 7s
    over an OOM that is not theirs.
    """
    slept_at_depth = []
    monkeypatch.setattr(tools.time, "sleep", lambda s: slept_at_depth.append(recorder.depth))

    calls = {"n": 0}

    class _Model:
        def feature_intervention(self, *_a, **_k):
            calls["n"] += 1
            if calls["n"] == 1:
                raise torch.cuda.OutOfMemoryError("boom")
            return torch.zeros(1, 2), None

    tools._run([], "prompt", model=_Model())

    assert calls["n"] == 2, "the OOM retry did not happen"
    assert slept_at_depth == [0], "backoff slept while holding the GPU lock"


def test_single_threaded_runs_pay_no_lock(monkeypatch):
    """The default active() is a no-op, so existing serial behaviour is unchanged."""
    from circuit_oracle import gpu_lock as gl

    assert gl.active().enabled is False
    with gl.active().hold("anything"):
        pass
