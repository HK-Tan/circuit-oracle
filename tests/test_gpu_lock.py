"""The GPU lock must actually serialize, must not deadlock, and must fail loud.

These three properties are what let N oracle runs share one model copy. Losing
any of them silently is the failure mode that matters: interleaved hooks on the
shared model produce WRONG activations without raising, so a corrupted batch
completes, saves, and looks fine. See circuit_oracle/gpu_lock.py.
"""
from __future__ import annotations

import threading
import time

import pytest

from circuit_oracle import gpu_lock as gl


@pytest.fixture(autouse=True)
def _clean_active():
    """install_gpu_lock patches a CLASS, so leakage between tests is real."""
    yield
    gl._ACTIVE = gl.NullGpuLock()


class _Overlap:
    """Records the high-water mark of threads inside `work` at once."""

    def __init__(self, dwell=0.02):
        self._n = 0
        self._dwell = dwell
        self._guard = threading.Lock()
        self.max_overlap = 0

    def work(self, *_args, **_kwargs):
        with self._guard:
            self._n += 1
            self.max_overlap = max(self.max_overlap, self._n)
        time.sleep(self._dwell)
        with self._guard:
            self._n -= 1
        return "ok"


def _hammer(fn, n=8):
    threads = [threading.Thread(target=fn) for _ in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# ---------------------------------------------------------------------------
# It serializes
# ---------------------------------------------------------------------------


def test_unguarded_calls_really_do_overlap():
    """Control. Without this the serialization test below could pass vacuously."""
    probe = _Overlap()

    class M:
        forward = staticmethod(probe.work)

    _hammer(M().forward)
    assert probe.max_overlap > 1, "the probe cannot detect overlap at all"


def test_guarded_calls_never_overlap():
    probe = _Overlap()

    class M:
        forward = staticmethod(probe.work)

    model = M()
    try:
        gl.install_gpu_lock(model, methods=("forward",))
        _hammer(model.forward)
    finally:
        gl.uninstall_gpu_lock(model)
    assert probe.max_overlap == 1, (
        f"{probe.max_overlap} threads were inside a GPU section at once; "
        "concurrent hook mutation silently corrupts activations"
    )


# ---------------------------------------------------------------------------
# It does not deadlock on nesting
# ---------------------------------------------------------------------------


def test_reentrant_nested_guarded_calls_do_not_deadlock():
    """feature_intervention_batched calls forward. A plain Lock would hang here.

    Run in a worker with a join timeout so a regression fails the test instead
    of wedging the whole pytest process.
    """
    class M:
        def inner(self):
            return 1

        def outer(self):
            return self.inner() + 1

    model = M()
    out = []
    try:
        gl.install_gpu_lock(model, methods=("inner", "outer"))
        t = threading.Thread(target=lambda: out.append(model.outer()))
        t.start()
        t.join(timeout=5)
        assert not t.is_alive(), "nested guarded call deadlocked (non-reentrant lock?)"
    finally:
        gl.uninstall_gpu_lock(model)
    assert out == [2]


def test_nesting_does_not_double_count_held_time():
    """Otherwise the per-run GPU total, which sizes the cluster, is inflated."""
    class M:
        def inner(self):
            time.sleep(0.05)

        def outer(self):
            self.inner()

    model = M()
    try:
        lock = gl.install_gpu_lock(model, methods=("inner", "outer"))
        model.outer()
        stats = lock.stats()
    finally:
        gl.uninstall_gpu_lock(model)
    # One accounted section, not two, and ~0.05s not ~0.10s.
    assert stats["calls"] == 1
    assert 0.04 <= stats["held_s"] < 0.09


# ---------------------------------------------------------------------------
# It measures contention
# ---------------------------------------------------------------------------


def test_blocked_threads_record_wait_time():
    """gpu_wait is the number that says whether more GPUs would help."""
    class M:
        def forward(self):
            time.sleep(0.05)

    model = M()
    try:
        lock = gl.install_gpu_lock(model, methods=("forward",))
        _hammer(model.forward, n=4)
        totals = lock.totals()
    finally:
        gl.uninstall_gpu_lock(model)
    # Four 50ms sections serialized: the last to arrive waits ~150ms, so the
    # summed wait across threads is well above one section.
    assert totals["held_s"] >= 0.19
    assert totals["wait_s"] > 0.05
    assert totals["peak_waiters"] > 1


# ---------------------------------------------------------------------------
# It fails loud
# ---------------------------------------------------------------------------


def test_missing_method_raises_rather_than_being_skipped():
    """An upstream rename must not quietly leave a GPU path unguarded."""
    class M:
        def forward(self):
            pass

    with pytest.raises(AttributeError, match="prefill_batched"):
        gl.install_gpu_lock(M(), methods=("forward", "prefill_batched"))


def test_a_failed_install_does_not_become_the_active_lock():
    """The raise must leave the process in its previous state, not half-armed."""
    class M:
        def forward(self):
            pass

    before = gl.active()
    with pytest.raises(AttributeError):
        gl.install_gpu_lock(M(), methods=("forward", "nope"))
    assert gl.active() is before


# ---------------------------------------------------------------------------
# Install / uninstall lifecycle
# ---------------------------------------------------------------------------


def test_active_is_a_noop_until_installed():
    """Single-threaded runs and the whole test suite must be unaffected."""
    assert gl.active().enabled is False
    with gl.active().hold("x"):
        pass


def test_install_is_idempotent():
    class M:
        def forward(self):
            pass

    model = M()
    try:
        first = gl.install_gpu_lock(model, methods=("forward",))
        second = gl.install_gpu_lock(model, methods=("forward",))
        assert first is second
        assert gl.active() is first
        # Not double-wrapped: one call is one accounted section.
        model.forward()
        assert first.stats()["calls"] == 1
    finally:
        gl.uninstall_gpu_lock(model)


def test_uninstall_restores_inherited_methods_to_the_parent():
    """forward/generate are inherited. Uninstall must DELETE the subclass
    override, not leave a copy pinned onto the subclass."""
    class Base:
        def forward(self):
            return "base"

    class Sub(Base):
        pass

    model = Sub()
    gl.install_gpu_lock(model, methods=("forward",))
    assert "forward" in Sub.__dict__
    gl.uninstall_gpu_lock(model)
    assert "forward" not in Sub.__dict__
    assert model.forward() == "base"
    assert gl.active().enabled is False
