"""A redundant temperature=1.0 must not reach OpenRouter, and must reach everyone else.

OpenRouter's ``require_parameters`` filter (injected on every OpenRouter request by
``OPENROUTER_DEFAULT_ROUTING``) drops any endpoint that does not ADVERTISE a
parameter the request sends. OpenAI's reasoning endpoints do not advertise
``temperature``, so an explicit 1.0 leaves zero eligible endpoints and OpenRouter
answers 404 rather than falling back.

Verified live 2026-07-28 against the real API:

    model                   require_params+temp   require_params, no temp
    openai/gpt-5.4          404                   OK
    openai/gpt-5.6-terra    404                   OK        <- arm 4
    minimax/minimax-m3      OK                    OK
    google/gemma-4-31b-it   OK                    OK

All 87 grader calls in the 2026-07-28 chlorine run died this way. The normalization
lives in the transport rather than in judge_rubric so it covers every caller, and it
is scoped to OpenRouter because Kilo and custom endpoints have their own sampling
defaults that are not ours to assume.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from circuit_oracle import llm_client as lc


def _capture(provider: str, model: str, temperature):
    """Return the kwargs create_message actually hands the backend."""
    client = lc.LLMClient.__new__(lc.LLMClient)
    backend = MagicMock()
    seen: dict = {}

    def _create(**kwargs):
        seen.update(kwargs)
        resp = MagicMock()
        resp.content = [MagicMock(type="text", text="ok")]
        resp.stop_reason = "end_turn"
        return resp

    backend.chat.completions.create.side_effect = _create
    is_or = provider == "openrouter"

    with patch.object(lc.LLMClient, "resolve_model", lambda self, m: m), \
         patch.object(lc.LLMClient, "_backend_for", lambda self, m: (backend, is_or)), \
         patch.object(lc, "_adapt_response", lambda c: c), \
         patch.object(lc, "_has_useful_content", lambda r: True):
        lc.LLMClient.create_message(
            client,
            model=model,
            system="rubric",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=16,
            temperature=temperature,
        )
    return seen


# ---------------------------------------------------------------------------
# OpenRouter: the default is dropped, anything else survives
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("default", [1.0, 1])
def test_openrouter_drops_the_default_temperature(default):
    """int 1 counts too: 1 == 1.0 is True, and callers do pass ints."""
    kwargs = _capture("openrouter", "openai/gpt-5.6-terra", default)
    assert "temperature" not in kwargs, (
        "an explicit default temperature reached OpenRouter, which 404s on OpenAI "
        "endpoints under require_parameters"
    )


def test_openrouter_still_sends_a_non_default_temperature():
    """A caller asking for 0.0 must get 0.0 or a loud failure, never a silent 1.0.

    feature_relevance.py sends 0.0 deliberately. Swallowing that would change the
    sampling semantics of a scoring path, which is worse than a 404.
    """
    assert _capture("openrouter", "openai/gpt-5.4", 0.0)["temperature"] == 0.0


def test_openrouter_does_not_special_case_near_one():
    """No tolerance window. 0.999999999 is a real request, not a rounded 1.0."""
    assert _capture("openrouter", "openai/gpt-5.4", 0.999999999)["temperature"] == 0.999999999


def test_none_is_omitted_rather_than_sent_as_null():
    """The pre-existing `is not None` guard must survive the new condition."""
    assert "temperature" not in _capture("openrouter", "openai/gpt-5.4", None)


# ---------------------------------------------------------------------------
# Everyone else keeps an explicit 1.0
# ---------------------------------------------------------------------------


def test_non_openrouter_backends_keep_an_explicit_default():
    """Kilo and custom LLM_BASE_URL endpoints have their own sampling defaults.

    Dropping the field there would silently hand sampling policy to whatever the
    gateway happens to do, which is exactly the assumption this scoping avoids.
    """
    assert _capture("kilo", "openai/gpt-5.4", 1.0)["temperature"] == 1.0


def test_the_routing_body_is_still_attached_on_openrouter():
    """Sanity: dropping temperature must not disturb require_parameters itself."""
    kwargs = _capture("openrouter", "openai/gpt-5.4", 1.0)
    assert kwargs["extra_body"]["provider"]["require_parameters"] is True


def test_no_routing_body_off_openrouter():
    assert "extra_body" not in _capture("kilo", "openai/gpt-5.4", 1.0)
