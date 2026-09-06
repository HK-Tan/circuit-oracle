"""Serialize GPU sections so many oracle runs can share ONE model copy.

WHY THIS EXISTS
---------------
A single oracle run is API-bound, not compute-bound. Measured on the 2026-07-28
chlorine trial: 2473 s wall clock, 19 serial orchestrator turns, 53 tool calls.
Almost all of that is waiting on a reasoning model over HTTP, and the GPU sits
idle for the large majority of it.

So the cheap way to run 50 prompts is not 50 GPUs. It is N concurrent agentic
loops sharing one model copy, with the short GPU sections queued behind a lock.
The model plus its 36 layers of transcoders costs 36.4 GB (measured, of which
the 4B model itself is only ~8 GB), so one process per prompt means 50 copies of
that. Threading against one copy turns a ~50-GPU job into a ~6-GPU job.

WHAT BREAKS WITHOUT IT
----------------------
Every intervention path bottoms out in ``with self.hooks(hooks)``
(circuit_tracer/replacement_model/batched.py). That context manager mutates the
hook registry of the SHARED model. Two threads inside it interleave their hooks
and produce wrong activations WITHOUT RAISING: a full batch that completes,
saves, and is silently wrong. That is the worst failure mode available here,
which is why this is mandatory for concurrency rather than an optimization.

TWO GRANULARITIES, FOR TWO DIFFERENT REASONS
--------------------------------------------
1. COARSE, at the three GPU funnels in tools.py (``_run``,
   ``_run_batched_intervention``, ``_decode_one_chunk``). This exists for
   MEMORY, not correctness. A 68-row anchor sweep decoding 800 tokens holds
   roughly 8 GB of KV cache (36 layers x 8 KV heads x 128 dim x 2 x 2 bytes x
   800 tokens x 68 rows). Locking only at the model-method level would be
   perfectly correct, because ``decode_step_batched`` rebuilds its hooks per
   call and the KV cache travels as an argument, but it would let N threads
   each sit mid-sweep holding one. Thirteen threads would be ~104 GB and an
   OOM. Holding the lock across a whole chunk means exactly one KV cache is
   ever live.

2. FINE, wrapping the model's own entry points (``install_gpu_lock``). This
   exists for CORRECTNESS, as the backstop. Guarding the resource is complete
   by construction because every path to the GPU goes through the model object.
   Guarding call sites is complete only until someone adds a tool. The lock is
   re-entrant, so a fine acquisition nested inside a coarse one is free.

WHAT IS DELIBERATELY *NOT* GUARDED
----------------------------------
``inspect_feature`` (Neuronpedia HTTP, 24 calls in the trial) and every subagent
or orchestrator LLM call. Holding a GPU lock across a network call would
serialize the very thing concurrency exists to overlap and would convert this
from a speedup into a slowdown. That is why the coarse locks live at three
named funnels inside tools.py rather than around ``execute_tool``, which
dispatches HTTP-bound tools through the same door as GPU-bound ones.

SINGLE-THREADED RUNS ARE UNAFFECTED
-----------------------------------
Until ``install_gpu_lock`` is called, ``active()`` returns a no-op lock whose
``hold()`` is an empty context manager. Existing single-run invocations and the
whole test suite therefore keep their current behaviour and cost.
"""
from __future__ import annotations

import contextlib
import threading
import time
from functools import wraps

__all__ = [
    "GPU_METHODS",
    "GpuLock",
    "NullGpuLock",
    "active",
    "install_gpu_lock",
    "uninstall_gpu_lock",
]


# Model entry points wrapped by ``install_gpu_lock``. Every one of these either
# runs a forward pass or mutates hook state on the shared model.
#
# ``forward`` and ``generate`` are inherited from HookedTransformer, so patching
# them lands on the ReplacementModel subclass and does not leak into every other
# HookedTransformer in the process.
#
# A name missing from the class RAISES rather than being skipped. Skipping would
# silently leave a GPU path unguarded after an upstream rename, which reintroduces
# exactly the silent-wrong-answer failure this module exists to prevent.
GPU_METHODS: tuple[str, ...] = (
    "forward",
    "generate",
    "feature_intervention",
    "feature_intervention_generate",
    "feature_intervention_batched",
    "prefill_batched",
    "decode_step_batched",
    "get_activations",
    "setup_attribution",
    "setup_intervention_with_freeze",
)


class NullGpuLock:
    """No-op stand-in used whenever no real lock has been installed.

    Keeps the call sites in tools.py unconditional. A single-threaded run pays
    one attribute lookup and an empty ``with`` block per GPU section.
    """

    enabled = False

    @contextlib.contextmanager
    def hold(self, label: str = ""):
        yield

    def stats(self) -> dict:
        return {"held_s": 0.0, "wait_s": 0.0, "calls": 0}

    def totals(self) -> dict:
        return {"held_s": 0.0, "wait_s": 0.0, "calls": 0}

    def reset_thread(self) -> None:
        pass


class GpuLock:
    """A re-entrant GPU mutex that also measures contention.

    ``wait_s`` is the number that sizes a cluster. It is time a run spent
    blocked waiting for another run's GPU section, so it says directly whether
    adding GPUs would help. ``held_s`` is time actually spent inside a GPU
    section, which is what divides across cards.

    Re-entrancy is required, not cosmetic: ``feature_intervention_batched``
    calls ``self(...)`` which reaches the guarded ``forward``, and
    ``_decode_one_chunk`` calls the guarded ``prefill_batched``. A plain Lock
    would self-deadlock on the first sweep.

    Timing caveat: CUDA kernels are launched asynchronously, so ``perf_counter``
    measures Python-side occupancy, not pure GPU busy time. The decode loop
    synchronizes every step (it reads token IDs back to choose the next input),
    so for the paths that matter here the two are close. Treat these numbers as
    "how long this thread owned the GPU section", which is the quantity the
    queue math actually needs.
    """

    enabled = True

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._local = threading.local()
        # Guarded by self._lock: every write below happens while held.
        self._totals = {"held_s": 0.0, "wait_s": 0.0, "calls": 0}
        self._peak_waiters = 0
        self._waiters = 0
        self.guarded_methods: tuple[str, ...] = ()

    # -- per-thread bookkeeping ------------------------------------------

    def _stats(self) -> dict:
        s = getattr(self._local, "stats", None)
        if s is None:
            s = {"held_s": 0.0, "wait_s": 0.0, "calls": 0, "depth": 0}
            self._local.stats = s
        return s

    def stats(self) -> dict:
        """Snapshot for the CALLING thread (i.e. for one run)."""
        s = self._stats()
        return {"held_s": s["held_s"], "wait_s": s["wait_s"], "calls": s["calls"]}

    def reset_thread(self) -> None:
        self._local.stats = {"held_s": 0.0, "wait_s": 0.0, "calls": 0, "depth": 0}

    def totals(self) -> dict:
        """Snapshot across all threads, plus the high-water mark of waiters."""
        with self._lock:
            out = dict(self._totals)
            out["peak_waiters"] = self._peak_waiters
        return out

    # -- the guard --------------------------------------------------------

    @contextlib.contextmanager
    def hold(self, label: str = ""):
        st = self._stats()

        # Already ours further up the stack. Do not double-count the time, and
        # do not touch the waiter gauge: this acquisition cannot block.
        if st["depth"] > 0:
            st["depth"] += 1
            try:
                yield
            finally:
                st["depth"] -= 1
            return

        t0 = time.perf_counter()
        self._waiters += 1  # racy by one, gauge only, never used for control flow
        try:
            self._lock.acquire()
        finally:
            self._waiters -= 1
        t1 = time.perf_counter()

        waited = t1 - t0
        st["wait_s"] += waited
        st["calls"] += 1
        st["depth"] = 1
        self._totals["wait_s"] += waited
        self._totals["calls"] += 1
        self._peak_waiters = max(self._peak_waiters, self._waiters + 1)
        try:
            yield
        finally:
            held = time.perf_counter() - t1
            st["held_s"] += held
            st["depth"] = 0
            self._totals["held_s"] += held
            self._lock.release()


# ---------------------------------------------------------------------------
# Module-level active lock
# ---------------------------------------------------------------------------
# A singleton rather than a parameter threaded through every call because the
# thing being protected IS a singleton: one process holds one model on one GPU.
# Passing it explicitly would mean touching every tool signature for a value
# that can only ever have one correct binding.

_ACTIVE: GpuLock | NullGpuLock = NullGpuLock()
_INSTALL_LOCK = threading.Lock()


def active() -> GpuLock | NullGpuLock:
    """The installed lock, or a no-op one when running single-threaded."""
    return _ACTIVE


def install_gpu_lock(model, *, methods: tuple[str, ...] = GPU_METHODS) -> GpuLock:
    """Wrap ``model``'s GPU entry points and make the lock globally active.

    Idempotent: calling twice returns the same lock and does not double-wrap.
    Patches the CLASS rather than the instance because ``nn.Module.__call__``
    resolves ``forward`` through the type, and because exactly one model
    instance exists per process anyway.

    Raises AttributeError if any name in ``methods`` is absent, on the theory
    that an upstream rename must fail loudly here rather than quietly leave a
    GPU path unguarded.
    """
    global _ACTIVE
    with _INSTALL_LOCK:
        cls = type(model)

        missing = [m for m in methods if not hasattr(cls, m)]
        if missing:
            raise AttributeError(
                f"install_gpu_lock: {cls.__name__} has no {missing}. The "
                f"circuit_tracer model API changed, so GPU_METHODS in "
                f"circuit_oracle/gpu_lock.py is stale and at least one GPU path "
                f"would run unguarded. Fix the list before running concurrently."
            )

        existing = getattr(cls, "_circuit_oracle_gpu_lock", None)
        if existing is not None:
            _ACTIVE = existing
            return existing

        lock = GpuLock()
        wrapped: list[str] = []
        # Remember whether each name was DEFINED on this class or inherited.
        # Uninstall has to undo the two cases differently: an inherited method
        # must be deleted so lookup falls back to the parent, but a class-owned
        # method must be restored, because deleting it would remove the real
        # implementation from the class permanently.
        originals: dict[str, tuple[bool, object]] = {}
        for name in methods:
            fn = getattr(cls, name)
            if getattr(fn, "_gpu_guarded", False):
                continue
            originals[name] = (name in cls.__dict__, cls.__dict__.get(name))
            setattr(cls, name, _guard(fn, lock, name))
            wrapped.append(name)

        lock.guarded_methods = tuple(wrapped)
        cls._circuit_oracle_gpu_originals = originals
        cls._circuit_oracle_gpu_lock = lock
        _ACTIVE = lock
        return lock


def uninstall_gpu_lock(model) -> None:
    """Undo ``install_gpu_lock``. For tests, so class patching does not leak."""
    global _ACTIVE
    with _INSTALL_LOCK:
        cls = type(model)
        originals: dict = getattr(cls, "_circuit_oracle_gpu_originals", {})
        for name in getattr(getattr(cls, "_circuit_oracle_gpu_lock", None),
                            "guarded_methods", ()):
            fn = cls.__dict__.get(name)
            if fn is None or not getattr(fn, "_gpu_guarded", False):
                continue
            was_owned, original = originals.get(name, (False, None))
            if was_owned:
                # Defined on THIS class. Put the real implementation back.
                # Deleting instead would strip feature_intervention,
                # setup_attribution and friends off the class for good.
                setattr(cls, name, original)
            else:
                # Inherited (forward, generate). Delete so lookup falls back to
                # the parent rather than pinning a copy onto the subclass.
                delattr(cls, name)
        for attr in ("_circuit_oracle_gpu_lock", "_circuit_oracle_gpu_originals"):
            if attr in cls.__dict__:
                delattr(cls, attr)
        _ACTIVE = NullGpuLock()


def _guard(fn, lock: GpuLock, label: str):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with lock.hold(label):
            return fn(*args, **kwargs)

    wrapper._gpu_guarded = True
    return wrapper
