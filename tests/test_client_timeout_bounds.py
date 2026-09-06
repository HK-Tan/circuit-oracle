"""The SDK handle must not run its own retry ladder underneath ours.

Found while running the secret-elicitation grid on 2026-07-28. Eleven runs logged zero tool
calls and hung until the launcher's 3600s ceiling reaped them, and one that hung
37 minutes while running SOLO completed in 71 seconds on a plain retry, which
rules out concurrency as the cause.

The mechanism is multiplication. `create_message` retries MAX_RETRIES+1 = 4
times and already catches APITimeoutError. The SDK default `max_retries=2` added
3 more attempts INSIDE each of those, and logged none of them. At the SDK default
read timeout of 600s the worst case for a single call was 4 x 3 x 600s = 2 hours
of silence.

Both properties below fail silently if broken: the run still completes, it just
takes an order of magnitude longer and prints nothing while doing it.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from circuit_oracle.llm_client import LLMClient

_CLIENT_PY = Path(__file__).resolve().parents[1] / "src" / "circuit_oracle" / "llm_client.py"


def _openai_call_kwargs() -> dict[str, ast.expr]:
    """Keyword arguments of the `openai.OpenAI(...)` construction."""
    tree = ast.parse(_CLIENT_PY.read_text())
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr == "OpenAI":
            return {kw.arg: kw.value for kw in node.keywords if kw.arg}
    pytest.fail("no openai.OpenAI(...) construction found in llm_client.py")


def test_sdk_retries_are_disabled_so_the_ladders_do_not_multiply():
    """max_retries must be explicitly 0.

    Leaving it at the SDK default silently triples every attempt our own loop
    makes, and the inner attempts print nothing, so a stuck call is
    indistinguishable from a slow one.
    """
    kwargs = _openai_call_kwargs()
    assert "max_retries" in kwargs, (
        "openai.OpenAI(...) does not set max_retries, so it inherits the SDK "
        "default of 2 and multiplies create_message's own 4-attempt ladder")
    node = kwargs["max_retries"]
    assert isinstance(node, ast.Constant) and node.value == 0, (
        f"max_retries must be 0 (create_message owns retries), got {ast.dump(node)}")


def test_timeout_is_explicit():
    """An explicit Timeout, not the SDK default.

    The default is not wrong so much as invisible: nothing in the repo recorded
    what it was, so the 2-hour worst case above was not derivable by reading
    this file.
    """
    kwargs = _openai_call_kwargs()
    assert "timeout" in kwargs, "openai.OpenAI(...) must set an explicit timeout"


def test_read_timeout_still_clears_an_honest_long_generation():
    """read must stay well above the longest legitimate completion.

    max_tokens is 8192 and a loaded endpoint can fall to ~20 tok/s, so honest
    work can occupy ~410s. Shortening read to chase the hang would truncate real
    completions, which fails SILENTLY and is strictly worse than waiting. This
    test exists to stop exactly that "fix".
    """
    kwargs = _openai_call_kwargs()
    timeout = kwargs["timeout"]
    assert isinstance(timeout, ast.Call), "expected a Timeout(...) call"
    vals = {kw.arg: kw.value.value for kw in timeout.keywords
            if isinstance(kw.value, ast.Constant)}
    assert "read" in vals, "Timeout must name its read budget explicitly"
    assert vals["read"] >= 500, (
        f"read={vals['read']}s is below the ~410s an honest 8192-token "
        "generation can take at ~20 tok/s under load. Shortening read truncates "
        "real completions instead of fixing the hang")
    # And it must stay under the launcher ceiling, or the launcher is the only
    # thing bounding a stuck call, which is what happened.
    assert vals["read"] <= 900, (
        f"read={vals['read']}s x 4 attempts exceeds the 3600s launcher timeout, "
        "so a stuck call would again be reaped by the launcher rather than by "
        "the client")


def test_worst_case_single_call_stays_under_the_launcher_ceiling():
    """4 attempts x read must fit inside the launcher's 3600s reap."""
    kwargs = _openai_call_kwargs()
    vals = {kw.arg: kw.value.value for kw in kwargs["timeout"].keywords
            if isinstance(kw.value, ast.Constant)}
    attempts = LLMClient.MAX_RETRIES + 1
    backoff = sum(LLMClient.BACKOFF_BASE_SECONDS * (2 ** i)
                  for i in range(LLMClient.MAX_RETRIES))
    worst = attempts * vals["read"] + backoff
    assert worst < 3600, (
        f"worst case {worst:.0f}s ({attempts} attempts x {vals['read']}s + "
        f"{backoff:.0f}s backoff) exceeds the launcher's 3600s timeout")


def test_connect_timeout_survives_a_concurrent_opening_burst():
    """connect must exceed the SDK's 5s default.

    A cold gateway hit by 64 workers at once can take more than 5s to first
    byte, which surfaced as spurious connection retries during the grid.
    """
    kwargs = _openai_call_kwargs()
    vals = {kw.arg: kw.value.value for kw in kwargs["timeout"].keywords
            if isinstance(kw.value, ast.Constant)}
    assert vals.get("connect", 0) > 5.0, (
        "connect should exceed the SDK's 5s default so a 64-way opening burst "
        "does not read as a connection failure")


def test_create_message_still_catches_transport_timeouts():
    """Disabling SDK retries is only safe because our loop catches them here.

    If this handler ever stops covering APITimeoutError, max_retries=0 turns a
    transient read timeout into a hard failure instead of a retry.
    """
    src = _CLIENT_PY.read_text()
    assert "openai.APITimeoutError" in src and "openai.APIConnectionError" in src, (
        "create_message must catch APITimeoutError and APIConnectionError, "
        "otherwise max_retries=0 makes transient transport errors fatal")
