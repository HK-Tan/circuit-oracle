"""A process-wide cap on concurrent subagent calls.

WHY
---
The REASSESS fan-out sizes its pool to the work: ``max_workers =
max(1, len(shifted_features))`` in tools.py, once for the anchor sweep and once
for causal discovery. That is fine for ONE run, where a typical sweep dispatches
9 to 12 subagents and ``build_features`` has no hard cap.

Under ``--workers N`` it stops being fine. Each of N concurrent runs opens its
own unbounded pool, so 13 runs at 9-12 shifted features each is already 117-156
simultaneous subagent calls, plus up to 8 more grader threads per run that is
finishing. Capping each pool individually does not help, because the ceiling is
still ``N x cap``. The bound has to be global.

The trial run made 111 subagent calls for one prompt, and ``gpt-oss-120b`` is
pinned to Groq, which throttles hard. Hitting a rate limit mid-batch is not a
clean failure: it surfaces as retries and partial results scattered across runs
that each look individually plausible.

DEFAULT IS UNBOUNDED
--------------------
``set_limit`` is called only by the concurrent runner. Until then ``slot()`` is
an empty context manager, so single-run invocations and the test suite behave
and cost exactly as before.
"""
from __future__ import annotations

import contextlib
import threading

__all__ = ["set_limit", "get_limit", "slot"]

_lock = threading.Lock()
_limit: int | None = None
_sem: threading.BoundedSemaphore | None = None


def set_limit(n: int | None) -> None:
    """Set the global ceiling on in-flight subagent calls (None = unbounded).

    Call once at process start, before any run begins. Changing it while calls
    are in flight would leave threads blocked on a semaphore nothing releases,
    so a second call with a different value raises rather than silently
    swapping the object out from under them.
    """
    global _limit, _sem
    with _lock:
        if _sem is not None and n != _limit:
            raise RuntimeError(
                f"fanout limit already set to {_limit}; refusing to change it to "
                f"{n} while calls may be in flight. Set it once at process start."
            )
        _limit = n
        _sem = threading.BoundedSemaphore(n) if n is not None and n > 0 else None


def get_limit() -> int | None:
    return _limit


@contextlib.contextmanager
def slot():
    """Occupy one subagent slot for the duration of the block."""
    sem = _sem
    if sem is None:
        yield
        return
    sem.acquire()
    try:
        yield
    finally:
        sem.release()
