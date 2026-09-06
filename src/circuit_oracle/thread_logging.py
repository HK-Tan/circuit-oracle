"""Route stdout to a per-thread sink so concurrent runs do not interleave.

Running N oracle prompts concurrently in one process makes the terminal useless
without this. Every run prints its own progress (graph shape, baseline answer,
per-turn tool calls, sweep tables), so 13 concurrent runs produce 13 interleaved
streams with no way to tell which run emitted which line. A run that misbehaves
becomes invisible, which is the opposite of what you want from the first big
concurrent batch.

So each run's chatter goes to its own file and the console keeps only the
start/finish lines.

Implemented as ONE ``sys.stdout`` replacement holding a ``threading.local``
sink, rather than ``contextlib.redirect_stdout``. That helper swaps a
process-global, so with threads every run would be fighting over the same
binding and the last writer would win. ``print`` resolves ``sys.stdout`` at call
time, so installing the replacement once at startup covers every later print,
including the ones inside the library.

stderr is deliberately NOT routed. Tracebacks and warnings should stay visible
on the console during a long unattended batch.
"""
from __future__ import annotations

import contextlib
import sys
import threading

__all__ = ["ThreadRoutedStream", "install"]


class ThreadRoutedStream:
    """A stdout stand-in that sends writes to the calling thread's sink.

    Threads with no sink set (the main thread, most notably) fall through to the
    original stream, so behaviour outside a routed block is unchanged.
    """

    def __init__(self, base):
        self.base = base
        self._local = threading.local()

    # -- routing ---------------------------------------------------------

    def _target(self):
        return getattr(self._local, "sink", None) or self.base

    @contextlib.contextmanager
    def route_to(self, path):
        """Send this thread's stdout to ``path`` for the duration of the block.

        Line-buffered so a killed or hung batch still leaves a readable partial
        log on disk. That matters more here than write throughput: these logs
        exist to be tailed while a multi-hour run is in flight.
        """
        previous = getattr(self._local, "sink", None)
        with open(path, "w", buffering=1, encoding="utf-8") as fh:
            self._local.sink = fh
            try:
                yield fh
            finally:
                self._local.sink = previous

    # -- file API --------------------------------------------------------

    def write(self, s):
        return self._target().write(s)

    def flush(self):
        target = self._target()
        # A sink closed by an unwinding route_to must not turn a real failure
        # into a confusing ValueError from the logging teardown path.
        with contextlib.suppress(ValueError):
            return target.flush()

    def writelines(self, lines):
        return self._target().writelines(lines)

    def isatty(self):
        # False even when the base IS a tty, because a routed thread is writing
        # to a file. Progress-bar libraries check this to decide whether to emit
        # carriage returns, which would corrupt a log file.
        return False

    def fileno(self):
        return self._target().fileno()

    def writable(self):
        return True

    def readable(self):
        return False

    def seekable(self):
        return False

    @property
    def encoding(self):
        return getattr(self._target(), "encoding", "utf-8")

    @property
    def errors(self):
        return getattr(self._target(), "errors", None)


def install() -> ThreadRoutedStream:
    """Replace ``sys.stdout`` with a routed stream, idempotently."""
    if isinstance(sys.stdout, ThreadRoutedStream):
        return sys.stdout
    stream = ThreadRoutedStream(sys.stdout)
    sys.stdout = stream
    return stream
