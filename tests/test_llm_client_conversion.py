"""The LLMClient conversion layer, with no network.

LLMClient was rewritten to speak the OpenAI /v1/chat/completions protocol
exclusively, while the whole package downstream still reads an Anthropic-shaped
response (response.content blocks with .type in {text, tool_use},
response.stop_reason, response.usage.input_tokens). The conversion happens at the
client boundary, in four pure helpers, so the tests below call those helpers
directly and only ever monkeypatch the openai client object.

  _convert_tools     Anthropic tool schema  -> OpenAI function schema
  _convert_messages  Anthropic content blocks -> OpenAI messages
  _adapt_usage       OpenAI usage block     -> Anthropic-shaped token counts
  _adapt_response    OpenAI completion dict -> LLMResponse

The helpers read fields with a dict-or-attribute accessor (`_field`), so a plain
dict standing in for an SDK object exercises the same code path a live
completion would.
"""

from __future__ import annotations

import json

import pytest

from circuit_oracle import llm_client as lc


# ---------------------------------------------------------------------------
# Tool schema conversion
# ---------------------------------------------------------------------------


def test_convert_tools_wraps_anthropic_schemas():
    anthropic_schema = {
        "name": "inspect_feature",
        "description": "Look up a feature.",
        "input_schema": {
            "type": "object",
            "properties": {"layer": {"type": "integer"}},
            "required": ["layer"],
        },
    }
    out = lc._convert_tools([anthropic_schema])
    assert len(out) == 1
    assert out[0]["type"] == "function"
    fn = out[0]["function"]
    assert fn["name"] == "inspect_feature"
    assert fn["description"] == "Look up a feature."
    # input_schema becomes parameters, contents untouched.
    assert fn["parameters"] == anthropic_schema["input_schema"]


def test_convert_tools_converts_the_real_tool_list():
    from circuit_oracle.tool_schemas import TOOLS

    out = lc._convert_tools(TOOLS)
    assert len(out) == len(TOOLS)
    assert [t["function"]["name"] for t in out] == [t["name"] for t in TOOLS]
    for t in out:
        assert t["type"] == "function"
        assert t["function"]["parameters"]["type"] == "object"


def test_convert_tools_passes_native_openai_schemas_through():
    native = {"type": "function", "function": {"name": "x", "parameters": {}}}
    assert lc._convert_tools([native]) == [native]


def test_convert_tools_fails_loud_on_a_nameless_schema():
    with pytest.raises(ValueError, match="without a name"):
        lc._convert_tools([{"description": "no name here"}])


def test_missing_input_schema_becomes_an_empty_object_schema():
    out = lc._convert_tools([{"name": "batched_anchor_sweep", "description": "argless"}])
    assert out[0]["function"]["parameters"] == {"type": "object", "properties": {}}


# ---------------------------------------------------------------------------
# Message conversion
# ---------------------------------------------------------------------------


def test_system_becomes_the_first_message():
    out = lc._convert_messages("BE HELPFUL", [{"role": "user", "content": "hi"}])
    assert out[0] == {"role": "system", "content": "BE HELPFUL"}
    assert out[1] == {"role": "user", "content": "hi"}


def test_system_cache_control_block_list_is_flattened():
    system = [
        {"type": "text", "text": "part one"},
        {"type": "text", "text": "part two", "cache_control": {"type": "ephemeral"}},
    ]
    out = lc._convert_messages(system, [{"role": "user", "content": "hi"}])
    assert out[0] == {"role": "system", "content": "part one\npart two"}


def test_tool_use_block_becomes_an_assistant_tool_call():
    messages = [
        {"role": "user", "content": "trace it"},
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "calling now"},
                {
                    "type": "tool_use",
                    "id": "toolu_1",
                    "name": "inspect_feature",
                    "input": {"layer": 7, "feature_idx": 42},
                },
            ],
        },
    ]
    out = lc._convert_messages(None, messages)
    assistant = out[1]
    assert assistant["role"] == "assistant"
    assert assistant["content"] == "calling now"
    call = assistant["tool_calls"][0]
    assert call["type"] == "function"
    assert call["id"] == "toolu_1"
    assert call["function"]["name"] == "inspect_feature"
    assert json.loads(call["function"]["arguments"]) == {"layer": 7, "feature_idx": 42}


def test_tool_only_assistant_turn_sends_null_content():
    messages = [
        {
            "role": "assistant",
            "content": [
                {"type": "tool_use", "id": "t1", "name": "batched_anchor_sweep", "input": {}}
            ],
        }
    ]
    out = lc._convert_messages(None, messages)
    assert out[0]["content"] is None
    assert json.loads(out[0]["tool_calls"][0]["function"]["arguments"]) == {}


def test_tool_result_becomes_its_own_tool_message():
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "tool_result", "tool_use_id": "toolu_1", "content": "{\"label\": \"x\"}"},
                {"type": "text", "text": "what next?"},
            ],
        }
    ]
    out = lc._convert_messages(None, messages)
    # The tool message must come FIRST, so it still directly follows the
    # assistant turn it answers. OpenAI rejects the other order.
    assert out[0] == {
        "role": "tool",
        "tool_call_id": "toolu_1",
        "content": '{"label": "x"}',
    }
    assert out[1] == {"role": "user", "content": "what next?"}


def test_round_trips_the_blocks_the_adapter_itself_produced():
    """The orchestrator replays response.content straight back into history, so
    the TextBlock / ToolUseBlock objects this module hands out must convert."""
    content = [
        lc.TextBlock(text="thinking out loud"),
        lc.ToolUseBlock(id="call_0", name="get_top_logits", input={"k": 5}),
    ]
    out = lc._convert_messages(None, [{"role": "assistant", "content": content}])
    assert out[0]["content"] == "thinking out loud"
    assert out[0]["tool_calls"][0]["function"]["name"] == "get_top_logits"


def test_reasoning_blocks_are_dropped_on_replay():
    """Some upstreams emit reasoning blocks as output and then reject them as
    input, which breaks the multi-turn subagent loop."""
    content = [
        {"type": "thinking", "thinking": "hidden"},
        {"type": "text", "text": "visible"},
    ]
    out = lc._convert_messages(None, [{"role": "assistant", "content": content}])
    assert out == [{"role": "assistant", "content": "visible"}]


def test_tool_calls_on_a_non_assistant_turn_fail_loud():
    messages = [
        {"role": "user", "content": [{"type": "tool_use", "id": "t", "name": "n", "input": {}}]}
    ]
    with pytest.raises(ValueError, match="only assistant turns"):
        lc._convert_messages(None, messages)


def test_message_without_a_role_fails_loud():
    with pytest.raises(ValueError, match="without a role"):
        lc._convert_messages(None, [{"content": "orphan"}])


# ---------------------------------------------------------------------------
# Response adaptation
# ---------------------------------------------------------------------------


def _completion(*, text=None, tool_calls=None, finish_reason="stop", usage=None,
                native_finish_reason=None):
    """An OpenAI-shaped chat completion as a plain dict."""
    message: dict = {"role": "assistant", "content": text}
    if tool_calls is not None:
        message["tool_calls"] = tool_calls
    choice: dict = {"index": 0, "message": message, "finish_reason": finish_reason}
    if native_finish_reason is not None:
        choice["native_finish_reason"] = native_finish_reason
    return {
        "id": "chatcmpl-1",
        "model": "openai/gpt-5.4",
        "choices": [choice],
        "usage": usage if usage is not None else {"prompt_tokens": 100, "completion_tokens": 20},
    }


def test_adapt_response_text_block():
    resp = lc._adapt_response(_completion(text="hello there"))
    assert len(resp.content) == 1
    block = resp.content[0]
    assert block.type == "text"
    assert block.text == "hello there"
    assert resp.stop_reason == "end_turn"
    assert resp.model == "openai/gpt-5.4"


def test_adapt_response_tool_use_block():
    completion = _completion(
        text="running the sweep",
        tool_calls=[
            {
                "id": "call_abc",
                "type": "function",
                "function": {
                    "name": "intervene_feature",
                    "arguments": '{"layer": 17, "feature_idx": 83241, "scale": -1}',
                },
            }
        ],
        finish_reason="tool_calls",
    )
    resp = lc._adapt_response(completion)
    types = [b.type for b in resp.content]
    assert types == ["text", "tool_use"]
    tool_block = resp.content[1]
    assert tool_block.name == "intervene_feature"
    assert tool_block.id == "call_abc"
    assert tool_block.input == {"layer": 17, "feature_idx": 83241, "scale": -1}
    # tool_calls maps into the Anthropic vocabulary the whole package branches on.
    assert resp.stop_reason == "tool_use"


def test_argless_tool_call_with_empty_arguments():
    completion = _completion(
        tool_calls=[
            {"id": "c1", "type": "function",
             "function": {"name": "batched_anchor_sweep", "arguments": ""}}
        ],
        finish_reason="tool_calls",
    )
    resp = lc._adapt_response(completion)
    assert resp.content[0].input == {}


def test_malformed_tool_arguments_raise():
    """A mangled tool call is a transient generation artifact. A silent {} would
    run the tool with wrong arguments instead."""
    completion = _completion(
        tool_calls=[
            {"id": "c1", "type": "function",
             "function": {"name": "pin_features", "arguments": "{not json"}}
        ],
        finish_reason="tool_calls",
    )
    with pytest.raises(json.JSONDecodeError):
        lc._adapt_response(completion)


def test_tool_calls_win_over_a_stop_finish_reason():
    """Some OpenAI-compatible servers (vLLM tool parsers) report finish_reason
    "stop" while returning tool calls. Ending the turn there would drop them."""
    completion = _completion(
        tool_calls=[
            {"id": "c1", "type": "function",
             "function": {"name": "get_top_logits", "arguments": "{}"}}
        ],
        finish_reason="stop",
    )
    assert lc._adapt_response(completion).stop_reason == "tool_use"


def test_unmapped_finish_reasons_pass_through():
    """content_filter and the Gemini safety reasons must stay visible, the retry
    loop and judge_rubric both branch on them."""
    resp = lc._adapt_response(_completion(text="", finish_reason="content_filter"))
    assert resp.stop_reason == "content_filter"
    assert resp.finish_reason == "content_filter"
    resp = lc._adapt_response(
        _completion(text="", finish_reason="stop", native_finish_reason="SAFETY")
    )
    assert resp.native_finish_reason == "SAFETY"
    assert lc._stop_signal(resp) == "safety"


def test_length_maps_to_max_tokens():
    assert lc._adapt_response(_completion(text="cut off", finish_reason="length")).stop_reason == "max_tokens"


def test_empty_choices_returns_an_empty_response_not_an_exception():
    resp = lc._adapt_response({"choices": [], "usage": None})
    assert resp.content == []
    assert resp.stop_reason is None
    assert lc._has_useful_content(resp) is False


def test_tool_call_without_an_id_gets_one_minted():
    completion = _completion(
        tool_calls=[{"type": "function",
                     "function": {"name": "get_top_logits", "arguments": "{}"}}],
        finish_reason="tool_calls",
    )
    assert lc._adapt_response(completion).content[0].id == "call_0"


def test_tool_call_without_a_name_fails_loud():
    completion = _completion(
        tool_calls=[{"id": "c1", "type": "function", "function": {"arguments": "{}"}}],
        finish_reason="tool_calls",
    )
    with pytest.raises(ValueError, match="no function name"):
        lc._adapt_response(completion)


# ---------------------------------------------------------------------------
# Usage accounting
# ---------------------------------------------------------------------------


def test_usage_exposes_the_anthropic_field_names():
    usage = lc._adapt_response(_completion(text="x")).usage
    assert usage.input_tokens == 100
    assert usage.output_tokens == 20
    assert usage.cache_read_input_tokens == 0
    assert usage.cache_creation_input_tokens == 0


def test_cached_tokens_are_subtracted_from_input_tokens():
    """OpenAI counts cached tokens inside prompt_tokens, Anthropic does not count
    them inside input_tokens, and saving.compute_cost prices the two separately.
    Without the subtraction every cached run is billed twice on paper."""
    completion = _completion(
        text="x",
        usage={
            "prompt_tokens": 1000,
            "completion_tokens": 50,
            "prompt_tokens_details": {"cached_tokens": 400},
        },
    )
    usage = lc._adapt_response(completion).usage
    assert usage.input_tokens == 600
    assert usage.cache_read_input_tokens == 400
    assert usage.output_tokens == 50


def test_missing_usage_block_is_zeroed_not_crashed():
    usage = lc._adapt_usage({"choices": []})
    assert (usage.input_tokens, usage.output_tokens) == (0, 0)


# ---------------------------------------------------------------------------
# Construction (openai client monkeypatched, no call ever made)
# ---------------------------------------------------------------------------


class _FakeOpenAI:
    instances: list = []

    def __init__(self, base_url=None, api_key=None, **kwargs):
        self.base_url = base_url
        self.api_key = api_key
        _FakeOpenAI.instances.append(self)


@pytest.fixture()
def fake_openai(monkeypatch):
    _FakeOpenAI.instances = []
    monkeypatch.setattr(lc.openai, "OpenAI", _FakeOpenAI)
    monkeypatch.delenv("LLM_BASE_URL", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    return _FakeOpenAI


def test_default_provider_resolves_to_openrouter(fake_openai):
    client = lc.LLMClient()
    assert client.provider == "openrouter"
    assert client.base_url == lc.OPENROUTER_BASE_URL
    assert fake_openai.instances[-1].api_key == "sk-test"


def test_explicit_base_url_wins(fake_openai):
    client = lc.LLMClient(provider="vllm", base_url="http://127.0.0.1:8000/v1")
    assert client.base_url == "http://127.0.0.1:8000/v1"
    # vLLM accepts any bearer token, and "EMPTY" is the conventional placeholder.
    assert fake_openai.instances[-1].api_key == "EMPTY"


def test_env_override_is_used_when_no_base_url_is_passed(fake_openai, monkeypatch):
    monkeypatch.setenv("LLM_BASE_URL", "http://modal.example/v1")
    assert lc.LLMClient().base_url == "http://modal.example/v1"


def test_unknown_provider_without_an_endpoint_fails_loud(fake_openai):
    with pytest.raises(ValueError, match="no default endpoint"):
        lc.LLMClient(provider="mystery")


def test_resolve_model_only_prefixes_for_aggregator_gateways(fake_openai):
    """Bare Anthropic names get a vendor prefix on the gateways that use the
    vendor/model convention, and are left alone on a vLLM server, where the model
    id is whatever that server was launched with."""
    assert lc.LLMClient(provider="openrouter").resolve_model("claude-opus-4-6") == (
        "anthropic/claude-opus-4-6"
    )
    assert lc.LLMClient(provider="openrouter").resolve_model("openai/gpt-5.4") == "openai/gpt-5.4"
    vllm = lc.LLMClient(provider="vllm", base_url="http://127.0.0.1:8000/v1")
    assert vllm.resolve_model("claude-opus-4-6") == "claude-opus-4-6"


def test_create_message_converts_both_directions_without_a_socket(fake_openai):
    """One end-to-end pass through create_message with a stubbed transport.

    Asserts the request carries OpenAI-shaped messages and function tools, and
    that what comes back is the Anthropic-shaped object the package reads.
    """
    captured: dict = {}
    completion = _completion(
        text="done",
        tool_calls=[
            {"id": "c1", "type": "function",
             "function": {"name": "get_top_logits", "arguments": '{"k": 3}'}}
        ],
        finish_reason="tool_calls",
    )

    class _Completions:
        def create(self, **kwargs):
            captured.update(kwargs)
            return completion

    client = lc.LLMClient()
    client._client.chat = type("_Chat", (), {"completions": _Completions()})()

    resp = client.create_message(
        model="openai/gpt-5.4",
        system="SYSTEM",
        messages=[{"role": "user", "content": "go"}],
        tools=[{"name": "get_top_logits", "description": "d",
                "input_schema": {"type": "object", "properties": {}}}],
        max_tokens=256,
        cache_control_breakpoint="system",  # Anthropic-only concept, accepted and ignored
    )

    assert captured["messages"][0] == {"role": "system", "content": "SYSTEM"}
    assert captured["tools"][0]["type"] == "function"
    assert "cache_control_breakpoint" not in captured
    assert [b.type for b in resp.content] == ["text", "tool_use"]
    assert resp.content[1].input == {"k": 3}
    assert resp.stop_reason == "tool_use"
    assert resp.usage.input_tokens == 100


# ---------------------------------------------------------------------------
# OpenRouter provider routing
# ---------------------------------------------------------------------------


def _capture_create_message(client, model):
    """Run one create_message through a stubbed transport, return the kwargs."""
    captured: dict = {}
    completion = _completion(text="ok", finish_reason="stop")

    class _Completions:
        def create(self, **kwargs):
            captured.update(kwargs)
            return completion

    client._client.chat = type("_Chat", (), {"completions": _Completions()})()
    client.create_message(
        model=model, system="S",
        messages=[{"role": "user", "content": "go"}], max_tokens=16,
    )
    return captured


def test_openrouter_requests_carry_require_parameters(fake_openai):
    """Every OpenRouter request routes only to endpoints supporting what we send.

    Several hosts serve minimax-m3 / gemma-4-31b-it / glm-5.2 without tool
    support, so an unfiltered reroute mid-batch kills the agentic loop in a way
    that looks like a model failure.
    """
    captured = _capture_create_message(lc.LLMClient(), "openai/gpt-5.4")
    assert captured["extra_body"]["provider"] == {"require_parameters": True}


def test_gpt_oss_prefers_groq_but_may_fall_back(fake_openai):
    """gpt-oss-120b (subagent + autointerp labeler) prefers Groq and is allowed
    to fall back.

    allow_fallbacks went False -> True 2026-07-28 because a single-host pin has
    no escape valve when that host throttles, and 62 percent of runs in the
    task-1 grid hit a Groq 429 at 37 concurrent runs. `order` is what keeps Groq
    the first choice, so the latency argument for the pin still holds on the
    calls Groq accepts.
    """
    captured = _capture_create_message(
        lc.LLMClient(provider="openrouter"), "openai/gpt-oss-120b"
    )
    assert captured["extra_body"]["provider"] == {
        "require_parameters": True,
        "order": ["groq"],
        "allow_fallbacks": True,
    }


def test_non_openrouter_endpoints_never_see_the_provider_field(fake_openai):
    """vLLM and friends reject unknown body fields, so no extra_body off OpenRouter."""
    client = lc.LLMClient(provider="vllm", base_url="http://127.0.0.1:8000/v1")
    captured = _capture_create_message(client, "openai/gpt-oss-120b")
    assert "extra_body" not in captured


def test_serving_provider_is_carried_on_the_response():
    """OpenRouter names the host that served each completion, and callers persist
    it into usage records, so the adapter must not drop it."""
    completion = _completion(text="ok")
    completion["provider"] = "Groq"
    assert lc._adapt_response(completion).provider == "Groq"
    # Absent (e.g. vLLM) stays None rather than crashing or inventing a value.
    assert lc._adapt_response(_completion(text="ok")).provider is None


# --- the Kilo gateway -----------------------------------------------------------

def test_kilo_provider_resolves_to_the_kilo_gateway(fake_openai, monkeypatch):
    """Kilo is a second aggregator carrying the same slugs at its own prices, so
    the only thing that may differ from an OpenRouter client is the base_url and
    the credential."""
    monkeypatch.setenv("KILO_API_KEY", "sk-kilo")
    client = lc.LLMClient(provider="kilo")
    assert client.base_url == "https://api.kilo.ai/api/gateway/v1"
    assert fake_openai.instances[-1].api_key == "sk-kilo"


def test_kilo_falls_back_to_the_kilocode_key_name(fake_openai, monkeypatch):
    """KILOCODE_API_KEY is what the Kilo Code editor extension exports, so a user
    who already has that set should not have to duplicate it."""
    monkeypatch.delenv("KILO_API_KEY", raising=False)
    monkeypatch.setenv("KILOCODE_API_KEY", "sk-fallback")
    lc.LLMClient(provider="kilo")
    assert fake_openai.instances[-1].api_key == "sk-fallback"


def test_kilo_requests_never_carry_the_openrouter_provider_object(fake_openai,
                                                                  monkeypatch):
    """`provider` routing is an OpenRouter body field. Kilo mimics OpenRouter's
    slugs but is a different service, so sending it risks a rejected request or,
    worse, a silently ignored routing pin that changes which host answers.

    The model here must be UNPINNED (a judge slug, not gpt-oss-120b), or
    _backend_for hands the call to an OpenRouter delegate and the assertion would
    be testing the wrong endpoint.
    """
    monkeypatch.setenv("KILO_API_KEY", "sk-kilo")
    captured = _capture_create_message(lc.LLMClient(provider="kilo"), "z-ai/glm-5.2")
    assert "extra_body" not in captured


def test_no_judge_slug_is_pinned_away_from_the_run_gateway(monkeypatch):
    """--judge-provider kilo has to mean the whole panel actually reaches Kilo.
    A pin on any judge slug would silently split the panel across gateways and
    make the cost comparison meaningless."""
    monkeypatch.delenv("CIRCUIT_ORACLE_MODEL_PINS", raising=False)
    from circuit_oracle.judge_rubric import JUDGE_PANEL
    for model, _ in JUDGE_PANEL:
        assert lc.provider_for(model, "kilo") == "kilo", model


def test_a_redirected_gateway_client_does_not_leak_its_key(fake_openai, monkeypatch):
    """LLM_BASE_URL outranks the provider default, so provider='kilo' can end up
    pointed at a Modal vLLM server. Picking the key off the declared provider
    would hand KILO_API_KEY to whatever host that variable names."""
    monkeypatch.setenv("KILO_API_KEY", "sk-kilo")
    monkeypatch.setenv("LLM_BASE_URL", "http://127.0.0.1:8000/v1")
    client = lc.LLMClient(provider="kilo")
    assert client.base_url == "http://127.0.0.1:8000/v1"
    assert fake_openai.instances[-1].api_key == "EMPTY", "not the Kilo credential"

    monkeypatch.setenv("LLM_API_KEY", "sk-vllm")
    lc.LLMClient(provider="kilo")
    assert fake_openai.instances[-1].api_key == "sk-vllm"


def test_bare_model_names_are_qualified_on_either_gateway(fake_openai, monkeypatch):
    """Kilo shares OpenRouter's vendor/model convention, so the legacy bare-name
    call sites need the same normalization on both routes."""
    monkeypatch.setenv("KILO_API_KEY", "sk-kilo")
    assert lc.LLMClient(provider="kilo").resolve_model(
        "claude-sonnet-5") == "anthropic/claude-sonnet-5"
    assert lc.LLMClient(provider="kilo").resolve_model(
        "z-ai/glm-5.2") == "z-ai/glm-5.2", "already qualified, left alone"


def test_gateway_key_lookup_reports_the_names_it_checked(monkeypatch):
    """The preflight in build_prompt_set's judge stage names the variable to
    export, so an empty lookup and the message must agree on which one."""
    monkeypatch.delenv("KILO_API_KEY", raising=False)
    monkeypatch.delenv("KILOCODE_API_KEY", raising=False)
    assert lc.gateway_api_key("kilo") == ""
    assert lc.api_key_names("kilo") == "KILO_API_KEY or KILOCODE_API_KEY"
    assert lc.api_key_names("openrouter") == "OPENROUTER_API_KEY"
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or")
    assert lc.gateway_api_key("openrouter") == "sk-or"


# --- the retired anthropic alias ------------------------------------------------

def test_provider_anthropic_is_retired_and_fails_loud(fake_openai):
    """It used to be the DEFAULT and silently resolved to OpenRouter. Nothing here
    can tell "meant OpenRouter" from "meant the direct Anthropic API and this run
    is quietly wrong", so it refuses to guess. The alias is what let llm_judge
    preflight ANTHROPIC_API_KEY, a credential this client never sends."""
    with pytest.raises(ValueError, match="retired"):
        lc.LLMClient(provider="anthropic")
    assert "openrouter" in str(
        pytest.raises(ValueError, lc.LLMClient, "anthropic").value
    ), "the error must name the replacement"
    assert "anthropic" not in lc.PROVIDER_CHOICES


def test_the_default_provider_is_now_openrouter(fake_openai):
    """The endpoint every existing run was already reaching, just named honestly."""
    client = lc.LLMClient()
    assert client.provider == "openrouter"
    assert client.base_url == lc.OPENROUTER_BASE_URL
    assert fake_openai.instances[-1].api_key == "sk-test"


def test_the_gpt_oss_pin_builds_no_delegate_on_an_openrouter_run(fake_openai,
                                                                 monkeypatch):
    """The pin names the run's own gateway, so it must be a no-op rather than a
    duplicate client against the identical URL, on the highest-call-count model."""
    monkeypatch.delenv("CIRCUIT_ORACLE_MODEL_PINS", raising=False)
    client = lc.LLMClient()
    handle, is_openrouter = client._backend_for("openai/gpt-oss-120b")
    assert handle is client._client and is_openrouter
    assert client._delegates == {}


def test_a_kilo_run_still_sends_the_pinned_model_to_openrouter(fake_openai, monkeypatch):
    """The point of the pin: flipping the main models to Kilo must not drag
    gpt-oss-120b off Groq, because that is the fan-out hot path."""
    monkeypatch.delenv("CIRCUIT_ORACLE_MODEL_PINS", raising=False)
    monkeypatch.setenv("KILO_API_KEY", "sk-kilo")
    client = lc.LLMClient(provider="kilo")
    handle, is_openrouter = client._backend_for("openai/gpt-oss-120b")
    assert handle is not client._client and is_openrouter
    assert client._delegates["openrouter"].base_url == lc.OPENROUTER_BASE_URL
    # An unpinned model stays on the run's own gateway.
    assert client._backend_for("z-ai/glm-5.2")[0] is client._client


def test_a_hyphenated_content_filter_is_not_retried(fake_openai):
    """Kilo passes through stop_reason 'content-filter'; OpenRouter normalizes to
    'content_filter'. Matching the raw string missed the hyphen form, so a
    deterministic safety block was retried 4 times and then RAISED. The raise
    reaches grade_completion's `except Exception`, which records a FAILED judge
    cell rather than a BLOCKED one, and a failed cell disqualifies the candidate
    outright instead of counting against --max-judge-blocks."""
    for spelling in ("content-filter", "content_filter", "CONTENT-FILTER"):
        assert lc._is_nonretryable_stop(spelling), spelling
    assert not lc._is_nonretryable_stop(None)
    assert not lc._is_nonretryable_stop("end_turn")

    calls = []
    client = lc.LLMClient(provider="openrouter", api_key="k")

    class _Completions:
        def create(self, **kw):
            calls.append(kw)
            return _completion(text="", finish_reason="content-filter")

    client._client.chat = type("_Chat", (), {"completions": _Completions()})()
    response = client.create_message(
        model="anthropic/claude-sonnet-5", system="S",
        messages=[{"role": "user", "content": "go"}], max_tokens=16,
    )
    assert len(calls) == 1, "a deterministic block must not be retried"
    assert lc._stop_signal(response) == "content-filter"


def test_a_blocked_judge_cell_is_counted_as_blocked_not_failed():
    """The end of the chain the retry bug broke: judge_rubric must recognise the
    returned empty response as a safety block and hand back the placeholder."""
    from circuit_oracle.judge_rubric import is_refusal_stop
    assert is_refusal_stop(lc._adapt_response(
        _completion(text="", finish_reason="content-filter")))
