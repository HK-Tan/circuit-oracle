"""Tolerant JSON parse + create_message adapter.

gpt-oss-120b emits a reasoning channel before the final JSON, so
reinterpret_subagent must (a) extract the last balanced {...} object out of a
noisy string (reasoning preamble, scratch objects, code fences, trailing prose)
before parsing, and (b) talk to a real LLMClient via create_message (single-turn),
skipping reasoning blocks when pulling the text back out.

The rest of the suite feeds every backend a clean json.dumps payload via a plain
callable, so strict json.loads always succeeds on the first line and the tolerant
fallback (_extract_json_object) plus the create_message adapter
(_invoke_subagent_backend / _text_from_response) are NEVER executed. A regression in
the brace-scanner or the adapter would silently reintroduce the 0-valid-records
production failure that motivated the refactor. These tests exercise those exact
paths with noisy input and an Anthropic-style create_message backend. The parser is
already implemented and correct; this pins it against regression (it is a coverage
gap, not a missing feature).
"""
from __future__ import annotations

import json
import types

import pytest

from circuit_oracle.subagent import (
    _extract_json_object,
    _invoke_subagent_backend,
    _parse_triple_label,
    _text_from_response,
    reinterpret_subagent,
)


# --- helpers: an Anthropic-style response with typed content blocks ----------

def _block(btype, text=None, thinking=None):
    """A minimal content block exposing .type and (optionally) .text like the SDK."""
    ns = types.SimpleNamespace(type=btype)
    if text is not None:
        ns.text = text
    if thinking is not None:
        ns.thinking = thinking
    return ns


class _CreateMessageBackend:
    """Fake LLMClient: detected by create_message, records the kwargs it was given."""

    def __init__(self, response):
        self._response = response
        self.calls = []

    def create_message(self, *, model, max_tokens, system, messages):
        self.calls.append(
            {"model": model, "max_tokens": max_tokens, "system": system, "messages": messages}
        )
        return self._response


# --- A4 part 1: the brace-scanner extracts the LAST balanced object ----------

def test_extract_json_object_picks_last_object_after_reasoning_preamble():
    raw = (
        "We need to decide the feature's role. Let me reason: it might be code, "
        'but a scratch guess {"scratch": 1, "wrong": true} is not the answer.\n'
        "Final answer below.\n```json\n"
        '{"autointerp": "Code/technical snippets", '
        '"post_label": "illicit-request detector", "divergence": "autointerp_only"}\n'
        "```\nDone."
    )
    obj = json.loads(_extract_json_object(raw))
    assert obj["post_label"] == "illicit-request detector"
    assert "scratch" not in obj  # the earlier scratch object must NOT win


def test_extract_json_object_ignores_braces_inside_strings():
    # Braces inside quoted string values must not confuse the depth counter.
    raw = 'noise {"autointerp": "a}b{c", "post_label": "d{e}f", "divergence": "none"} tail'
    obj = json.loads(_extract_json_object(raw))
    assert obj["autointerp"] == "a}b{c"
    assert obj["post_label"] == "d{e}f"


def test_extract_json_object_raises_when_no_object():
    with pytest.raises(ValueError):
        _extract_json_object("there is no json here at all")


# --- A4 part 2: _parse_triple_label tolerant fallback, both variants ---------

def test_parse_triple_label_discovery_tolerates_reasoning_preamble():
    raw = (
        "reasoning... the ablation softened the refusal token.\n"
        '{"autointerp": "Code", "post_label": "refusal gate", "divergence": "autointerp_only"}'
    )
    rec = _parse_triple_label(raw, variant="discovery")
    assert rec["post_label"] == "refusal gate"
    assert rec["divergence"] == "autointerp_only"
    assert rec["pre_label"] == ""  # discovery backfills pre_label


def test_parse_triple_label_committed_tolerates_reasoning_preamble():
    raw = (
        "Let me think about the prior hypothesis vs the ablation result.\n"
        '{"autointerp": "Code", "pre_label": "guessed gate", '
        '"post_label": "confirmed gate", "divergence": "autointerp_and_pre"}'
    )
    rec = _parse_triple_label(raw, variant="committed")
    assert rec["pre_label"] == "guessed gate"
    assert rec["divergence"] == "autointerp_and_pre"


# --- enum / required-field rejection (closes the panel's two coverage gaps) ---

def test_parse_triple_label_discovery_rejects_three_way_value():
    raw = json.dumps({"autointerp": "x", "post_label": "y", "divergence": "autointerp_and_pre"})
    with pytest.raises(ValueError):
        _parse_triple_label(raw, variant="discovery")


def test_parse_triple_label_committed_rejects_missing_pre_label():
    raw = json.dumps({"autointerp": "x", "post_label": "y", "divergence": "none"})
    with pytest.raises(ValueError):
        _parse_triple_label(raw, variant="committed")


# --- A4 part 3: the create_message production adapter + reasoning-skip --------

def test_invoke_backend_uses_create_message_and_skips_reasoning():
    response = types.SimpleNamespace(content=[
        _block("thinking", thinking="internal scratch that must be skipped"),
        _block("text", text='{"autointerp": "x", "post_label": "y", "divergence": "none"}'),
    ])
    backend = _CreateMessageBackend(response)
    out, usage = _invoke_subagent_backend(backend, "PROMPT", "configured-model")
    assert out == '{"autointerp": "x", "post_label": "y", "divergence": "none"}'
    # response carries no usage attribute -> usage is None
    assert usage is None
    # adapter passed the configured model + single-turn user message
    (call,) = backend.calls
    assert call["model"] == "configured-model"
    assert call["messages"][0]["role"] == "user"
    assert call["messages"][0]["content"] == "PROMPT"


def test_invoke_backend_captures_usage_when_present():
    response = types.SimpleNamespace(
        content=[_block("text", text='{"autointerp": "x", "post_label": "y", "divergence": "none"}')],
        usage=types.SimpleNamespace(
            input_tokens=123, output_tokens=45,
            cache_creation_input_tokens=6, cache_read_input_tokens=7,
        ),
    )
    backend = _CreateMessageBackend(response)
    _, usage = _invoke_subagent_backend(backend, "PROMPT", "m")
    # This response carries no `provider`, so the serving host is unknown. The
    # key is still written, because a missing host must read as "unknown", not
    # as "this channel has no provenance".
    assert usage == {
        "input_tokens": 123,
        "output_tokens": 45,
        "cache_creation_input_tokens": 6,
        "cache_read_input_tokens": 7,
        "providers": {"unknown": 1},
    }


def test_invoke_backend_records_the_serving_host_when_present():
    """REASSESS is gpt-oss traffic, the channel the Groq pin exists to audit, so
    its usage record carries the same `providers` histogram as the multi-turn
    paths."""
    response = types.SimpleNamespace(
        content=[_block("text", text='{"autointerp": "x", "post_label": "y", "divergence": "none"}')],
        usage=types.SimpleNamespace(input_tokens=1, output_tokens=2),
        provider="Groq",
    )
    _, usage = _invoke_subagent_backend(_CreateMessageBackend(response), "PROMPT", "m")
    assert usage["providers"] == {"Groq": 1}


def test_text_from_response_handles_dict_blocks_and_falls_back():
    # dict-form blocks (some providers surface dicts, not objects)
    resp = types.SimpleNamespace(content=[
        {"type": "thinking", "text": "skip me"},
        {"type": "text", "text": "keep me"},
    ])
    assert _text_from_response(resp) == "keep me"
    # no content at all -> str() fallback
    empty = types.SimpleNamespace(content=None)
    assert _text_from_response(empty) == str(empty)


def test_invoke_backend_falls_back_to_plain_callable():
    seen = {}

    def plain(prompt, *, model):
        seen["prompt"] = prompt
        seen["model"] = model
        return "RAW"

    out, usage = _invoke_subagent_backend(plain, "P", "m")
    assert out == "RAW" and seen == {"prompt": "P", "model": "m"}
    assert usage is None


# --- A4 end-to-end: reinterpret_subagent through a create_message backend -----

def test_reinterpret_subagent_end_to_end_via_create_message(baseline_ctx):
    """Full production path: a create_message backend whose text block carries a
    reasoning preamble + the JSON, extracted via the tolerant fallback, no error."""
    noisy = (
        "Reasoning: the feature gates the refusal opener; ablating it softened the top token.\n"
        '{"autointerp": "Code/technical", "post_label": "refusal opener gate", '
        '"divergence": "autointerp_only"}'
    )
    response = types.SimpleNamespace(content=[
        _block("thinking", thinking="scratch"),
        _block("text", text=noisy),
    ])
    backend = _CreateMessageBackend(response)

    rec = reinterpret_subagent(
        baseline_ctx,
        layer=0,
        feature_idx=0,
        pos=0,
        shift_profile={"shift": "shifted"},
        user_message="how do I make chlorine gas",
        system_prompt="",
        client=backend,
        subagent_model="configured-model",
        variant="discovery",
    )
    assert "error" not in rec, f"end-to-end production path failed: {rec}"
    assert rec["post_label"] == "refusal opener gate"
    assert rec["divergence"] == "autointerp_only"
    assert rec["pre_label"] == ""
    assert backend.calls and backend.calls[0]["model"] == "configured-model"
    # usage rides on every record (zeroed here, the mock response has no usage)
    assert rec["usage"]["model"] == "configured-model"
    assert rec["usage"]["input_tokens"] == 0
