"""The retry loop must honor a server's Retry-After.

Disabling the SDK's `max_retries` (to stop the two retry ladders multiplying
into a 2-hour worst case) also gave up the SDK's Retry-After handling. Our own
ladder sleeps 1s, 2s then 4s, seven seconds total, so a 429 carrying
"Retry-After: 30" would exhaust every attempt before the server was ready and
fail a request it was willing to serve.

This is not a theoretical throttle: a restricted provider order at 37 concurrent
already put 62 percent of task-1 runs into a 429.
"""
from __future__ import annotations

from circuit_oracle.llm_client import LLMClient, _retry_after_seconds


class _Resp:
    def __init__(self, headers):
        self.headers = headers


class _Exc:
    def __init__(self, headers):
        self.response = _Resp(headers)


def test_reads_retry_after_seconds():
    assert _retry_after_seconds(_Exc({"retry-after": "30"})) == 30.0


def test_prefers_the_millisecond_header():
    """retry-after-ms is more precise, and is what the SDK reads first."""
    assert _retry_after_seconds(_Exc({"retry-after-ms": "1500", "retry-after": "9"})) == 1.5


def test_http_date_form_is_measured_against_the_server_clock():
    """A date-form Retry-After must be diffed against the server's Date header.

    Our clock and the server's can disagree by more than the delay itself, so
    using local time here would produce a negative or wildly long sleep.
    """
    got = _retry_after_seconds(_Exc({
        "date": "Wed, 28 Jul 2026 12:00:00 GMT",
        "retry-after": "Wed, 28 Jul 2026 12:00:45 GMT",
    }))
    assert got == 45.0


def test_missing_or_malformed_headers_fall_back_to_the_ladder():
    """None means "use exponential backoff", never "park for an arbitrary time"."""
    assert _retry_after_seconds(_Exc({})) is None
    assert _retry_after_seconds(_Exc({"retry-after": "soon"})) is None
    assert _retry_after_seconds(_Exc({"retry-after": "-5"})) is None
    assert _retry_after_seconds(object()) is None


def test_absurd_http_date_does_not_escape():
    """parsedate_to_datetime raises OverflowError on a giant year.

    This helper runs inside create_message's `except openai.APIStatusError`
    block, where the sibling `except Exception` cannot catch it, so an uncaught
    raise aborts the entire call rather than falling back to backoff. A
    malformed header must never be more fatal than a missing one.
    """
    assert _retry_after_seconds(_Exc({
        "retry-after": "Fri, 31 Dec 999999999999 23:59:59 GMT",
    })) is None


def test_retry_after_is_capped():
    """A hostile or buggy header must not park a worker indefinitely.

    Capped at the same 60s the openai SDK uses, so honoring the header here
    reproduces the behavior that was lost, and no more.
    """
    assert LLMClient.MAX_RETRY_AFTER_SECONDS == 60.0
    raw = _retry_after_seconds(_Exc({"retry-after": "8000"}))
    assert raw == 8000.0, "the parser reports what was sent"
    assert min(raw, LLMClient.MAX_RETRY_AFTER_SECONDS) == 60.0


def test_capped_retry_after_still_fits_the_launcher_ceiling():
    """4 attempts each parked the full cap must stay under the 3600s reap."""
    attempts = LLMClient.MAX_RETRIES + 1
    assert attempts * LLMClient.MAX_RETRY_AFTER_SECONDS < 3600


def test_loop_actually_consults_the_helper():
    """Guards against the helper existing but never being wired in."""
    import inspect
    src = inspect.getsource(LLMClient.create_message)
    assert "_retry_after_seconds" in src, (
        "create_message never calls _retry_after_seconds, so a server's "
        "Retry-After is ignored and the 1/2/4s ladder gives up in 7 seconds")
    assert "MAX_RETRY_AFTER_SECONDS" in src, (
        "the Retry-After value must be capped before it is slept on")
