"""Concurrent runs must not interleave their stdout into one unreadable stream.

With --workers N every run prints its own progress, so without per-thread routing
N runs produce N interleaved streams and a misbehaving run is invisible. See
circuit_oracle/thread_logging.py.
"""
from __future__ import annotations

import io
import sys
import threading

import pytest

from circuit_oracle.thread_logging import ThreadRoutedStream, install


def test_unrouted_threads_fall_through_to_the_base_stream():
    base = io.StringIO()
    stream = ThreadRoutedStream(base)
    print("hello", file=stream)
    assert base.getvalue() == "hello\n"


def test_a_routed_thread_writes_to_its_file_and_not_the_console(tmp_path):
    base = io.StringIO()
    stream = ThreadRoutedStream(base)
    target = tmp_path / "run.log"

    with stream.route_to(target):
        print("into the file", file=stream)

    assert target.read_text() == "into the file\n"
    assert base.getvalue() == "", "routed output leaked to the console"


def test_concurrent_threads_do_not_cross_contaminate(tmp_path):
    """The property the whole module exists for."""
    base = io.StringIO()
    stream = ThreadRoutedStream(base)
    started = threading.Barrier(4)

    def worker(name):
        with stream.route_to(tmp_path / f"{name}.log"):
            started.wait()          # force real interleaving
            for i in range(50):
                print(f"{name}-{i}", file=stream)

    threads = [threading.Thread(target=worker, args=(n,))
               for n in ("alpha", "beta", "gamma", "delta")]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for name in ("alpha", "beta", "gamma", "delta"):
        lines = (tmp_path / f"{name}.log").read_text().splitlines()
        assert lines == [f"{name}-{i}" for i in range(50)], (
            f"{name}.log contains another thread's output or lost its own"
        )
    assert base.getvalue() == ""


def test_the_sink_is_restored_after_the_block(tmp_path):
    base = io.StringIO()
    stream = ThreadRoutedStream(base)
    with stream.route_to(tmp_path / "a.log"):
        pass
    print("back on console", file=stream)
    assert base.getvalue() == "back on console\n"


def test_nested_routing_restores_the_outer_sink(tmp_path):
    base = io.StringIO()
    stream = ThreadRoutedStream(base)
    outer, inner = tmp_path / "outer.log", tmp_path / "inner.log"

    with stream.route_to(outer):
        print("o1", file=stream)
        with stream.route_to(inner):
            print("i1", file=stream)
        print("o2", file=stream)

    assert outer.read_text() == "o1\no2\n"
    assert inner.read_text() == "i1\n"


def test_routing_is_restored_even_when_the_block_raises(tmp_path):
    base = io.StringIO()
    stream = ThreadRoutedStream(base)
    with pytest.raises(RuntimeError):
        with stream.route_to(tmp_path / "boom.log"):
            raise RuntimeError("boom")
    print("still fine", file=stream)
    assert base.getvalue() == "still fine\n"


def test_isatty_is_false_so_progress_bars_do_not_corrupt_a_log():
    class _Tty(io.StringIO):
        def isatty(self):
            return True

    assert ThreadRoutedStream(_Tty()).isatty() is False


def test_install_is_idempotent_and_does_not_double_wrap():
    original = sys.stdout
    try:
        first = install()
        second = install()
        assert first is second
        assert first.base is original, "double-wrapped: base is a routed stream"
    finally:
        sys.stdout = original
