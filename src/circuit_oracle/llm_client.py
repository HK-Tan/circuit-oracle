"""Unified LLM client that speaks the OpenAI chat-completions protocol exclusively.

Why one protocol. No run in this project ever called the Anthropic API directly.
Every real run went through OpenRouter, and OpenRouter serves the OpenAI-compatible
`/v1/chat/completions` endpoint alongside everything else. Speaking only that
protocol gives a single code path that reaches OpenRouter, a Modal vLLM server, or
any other OpenAI-compatible endpoint, with nothing but a base_url between them.

Why the rest of the package does not change. Everything downstream (orchestrator.py,
subagent.py, judge_rubric.py, feature_relevance.py, control.py, autointerp.py) reads
an Anthropic-shaped response, `response.content` as a list of blocks with `.type` in
{"text", "tool_use"}, `response.stop_reason`, `response.usage.input_tokens`. That
surface is preserved here by the small adapter classes below (`TextBlock`,
`ToolUseBlock`, `Usage`, `LLMResponse`), so the wire format changed and nothing else
did. Messages and tool schemas are converted on the way in, the completion is
converted back on the way out.

Provider routing (see `LLMClient.__init__`):
  openrouter  -> https://openrouter.ai/api/v1, key from OPENROUTER_API_KEY
  anthropic   -> RETIRED, raises. It was a silent alias for the OpenRouter endpoint
                 and hid a preflight that asked for an unused ANTHROPIC_API_KEY.
  kilo        -> https://api.kilo.ai/api/gateway/v1, key from KILO_API_KEY or
                 KILOCODE_API_KEY (a second aggregator, same slugs, own prices)
  anything else, or an explicit base_url -> that base_url, key from api_key or
                 LLM_API_KEY, falling back to "EMPTY" (vLLM accepts any token)
LLM_BASE_URL overrides the provider default so entry scripts need no edit.
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import openai

logger = logging.getLogger(__name__)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Providers served over OpenRouter. A frozenset rather than a bare string because
# the surrounding code treats gateway membership as a set test, and because the
# retired "anthropic" alias used to live here.
_OPENROUTER_PROVIDERS = frozenset({"openrouter"})

# provider="anthropic" used to be the default and silently resolved to OpenRouter,
# because no run in this project ever called the Anthropic API directly. It is now
# a hard error rather than an alias. A silent alias is exactly the failure mode
# that let llm_judge preflight ANTHROPIC_API_KEY, a credential the client never
# sends, and let a routing pin build a duplicate client against the same URL.
# Nothing here can distinguish "meant OpenRouter" from "meant the direct Anthropic
# API and this run is quietly wrong", so it refuses to guess.
_RETIRED_PROVIDERS = {
    "anthropic": (
        "provider='anthropic' is retired. This client speaks the OpenAI "
        "chat-completions protocol only, and every run in this project has always "
        "gone through OpenRouter, so 'anthropic' was a silent alias for it. Pass "
        "provider='openrouter' (or 'kilo'). For a genuinely direct Anthropic "
        "endpoint, pass base_url= explicitly."
    ),
}

# Aggregator gateways other than OpenRouter. Value is (base_url, env var names in
# priority order). Kilo mirrors OpenRouter's `vendor/model` slug convention and
# serves the same OpenAI-compatible /v1/chat/completions route, so nothing below
# the base_url changes. It is a price-comparison and redundancy option, not a
# default: verified 2026-07-26 that all five JUDGE_PANEL slugs are listed there,
# with identical prices on the three closed models and a premium on the two
# open-weight ones (kimi-k2.6 +24%, glm-5.2 +109%), because an aggregator's
# open-weight price is a single host rather than a cheapest-of-many.
_GATEWAYS: dict[str, tuple[str, tuple[str, ...]]] = {
    "kilo": ("https://api.kilo.ai/api/gateway/v1", ("KILO_API_KEY", "KILOCODE_API_KEY")),
}


# The argparse `choices` list every entry script should use for --provider, so
# adding a third gateway is one edit here rather than a hunt through the scripts.
# Sorted with the default first: "openrouter" is what every run has used.
PROVIDER_CHOICES: list[str] = [*sorted(_OPENROUTER_PROVIDERS), *sorted(_GATEWAYS)]


def gateway_api_key(provider: str) -> str:
    """First non-empty env key registered for a gateway provider ("" if none).

    Callers that preflight credentials before spending (build_prompt_set's judge
    stage) must not hardcode OPENROUTER_API_KEY now that the same calls can route
    through a second gateway.
    """
    if provider in _OPENROUTER_PROVIDERS:
        return os.environ.get("OPENROUTER_API_KEY", "").strip()
    for name in _GATEWAYS.get(provider, (None, ()))[1]:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""


def api_key_names(provider: str) -> str:
    """Human-readable env var name(s) for a provider, for error messages."""
    if provider in _OPENROUTER_PROVIDERS:
        return "OPENROUTER_API_KEY"
    return " or ".join(_GATEWAYS.get(provider, (None, ("LLM_API_KEY",)))[1])


# Models pinned to one gateway regardless of the run's configured provider.
#
# gpt-oss-120b is the subagent / relevance / autointerp-labeler backend and by
# far the highest call-count role in a run. OpenRouter serves it off Groq (see
# OPENROUTER_MODEL_ROUTING below) at a latency the other gateways do not match,
# and those are exactly the fan-out hot paths, so flipping the main models to a
# second gateway must NOT drag it along. The split is per model, not per run.
#
# This is a routing decision, not a hint: the pin selects which gateway is
# CALLED. OPENROUTER_MODEL_ROUTING only says which host OpenRouter should pick
# once the request is already going there, and it is dropped on any other
# endpoint, so without this map a --provider kilo run would send gpt-oss-120b
# to Kilo and silently lose Groq.
#
# Override with CIRCUIT_ORACLE_MODEL_PINS ("model=provider,..."), or set that
# env var to empty to disable pinning entirely.
_DEFAULT_MODEL_PINS: dict[str, str] = {
    "openai/gpt-oss-120b": "openrouter",
    # gemma-4-31b-it (arm 3) pinned 2026-07-28 for throughput. Measured on the
    # SAME prompt at 400 max_tokens, ~260 completion tokens each:
    #   kilo                22.0 tok/s
    #   openrouter default  34.2 tok/s  (CoreWeave)
    #   openrouter cerebras 389.0 tok/s  <- 17.7x kilo
    #   openrouter sambanova 47.1 tok/s
    # The routing object below only reaches OpenRouter (it is dropped on any
    # other endpoint), so the pin is what makes the ordering effective at all.
    "google/gemma-4-31b-it": "openrouter",
}


def model_pins() -> dict[str, str]:
    """Current {model_id: provider} pin map, with the env override applied."""
    raw = os.environ.get("CIRCUIT_ORACLE_MODEL_PINS")
    if raw is None:
        return dict(_DEFAULT_MODEL_PINS)
    pins: dict[str, str] = {}
    known = set(_OPENROUTER_PROVIDERS) | set(_GATEWAYS)
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        if "=" not in item:
            raise ValueError(
                "CIRCUIT_ORACLE_MODEL_PINS entries must be 'model=provider', "
                f"got {item!r}"
            )
        model, provider = (part.strip() for part in item.split("=", 1))
        if provider not in known:
            raise ValueError(
                f"CIRCUIT_ORACLE_MODEL_PINS names unknown provider {provider!r} "
                f"(known: {', '.join(sorted(known))})"
            )
        pins[model] = provider
    return pins


def provider_for(model: str, default_provider: str) -> str:
    """Gateway that should serve ``model`` given the run's configured default."""
    return model_pins().get(model, default_provider)


def check_provider(provider: str) -> None:
    """Raise on a retired provider name instead of silently redirecting it."""
    if provider in _RETIRED_PROVIDERS:
        raise ValueError(f"LLMClient: {_RETIRED_PROVIDERS[provider]}")


def preflight_providers(models, default_provider: str) -> None:
    """Raise before any billable work if a routed model has no API key.

    Routing is resolved per model, so a ``--provider kilo`` run that still sends
    gpt-oss-120b through OpenRouter needs BOTH keys. Say so up front rather than
    dying mid-batch on an opaque 401 after the GPU work is already paid for.
    ``models`` is the set of model ids the run will actually call (orchestrator,
    subagent, relevance, grader).

    Two things it must NOT do. It must not demand a gateway key when
    LLM_BASE_URL points the run at some other OpenAI-compatible server (a Modal
    vLLM): LLMClient disables pinning in that case and authenticates with
    LLM_API_KEY, falling back to "EMPTY", so demanding OPENROUTER_API_KEY there
    would block a run that needs no such key. And it must not silently accept a
    retired provider name, which reaches here from entry scripts because
    argparse does not validate a `default=` against `choices=`, so
    LLM_PROVIDER=anthropic in the environment sails past the flag. Reporting
    that as a missing LLM_API_KEY would bury the real cause.
    """
    check_provider(default_provider)
    if os.environ.get("LLM_BASE_URL"):
        return
    missing: dict[str, set[str]] = {}
    for model in models:
        if not model:
            continue
        provider = provider_for(model, default_provider)
        if not gateway_api_key(provider):
            missing.setdefault(api_key_names(provider), set()).add(model)
    if missing:
        detail = "; ".join(
            f"{names} (needed by {', '.join(sorted(used))})"
            for names, used in sorted(missing.items())
        )
        # Name the file and the fix, not just the variable. The usual cause is a
        # .env copied from .env.example before a second gateway was in use, so
        # the line is absent rather than empty, and "missing KILO_API_KEY" alone
        # reads like a code bug to someone who has never added that key.
        raise RuntimeError(
            f"missing API key(s) for provider={default_provider!r} routing: "
            f"{detail}. Add the line(s) to the repository-root .env (create it "
            "with `cp .env.example .env` if absent, and see the comments there "
            "for which gateway needs which key), or export them in your shell. "
            "A --provider kilo run needs BOTH keys: openai/gpt-oss-120b is "
            "pinned to OpenRouter regardless of the run's provider."
        )

# OpenRouter provider-routing preferences, sent as the request-body `provider`
# object on every request that actually goes to OpenRouter (never to vLLM or
# other OpenAI-compatible endpoints, which would reject the unknown field).
# https://openrouter.ai/docs/features/provider-routing
#
# require_parameters keeps requests off endpoints that silently lack a
# parameter THE REQUEST ACTUALLY SENDS, nothing more. create_message sends
# tools when the caller passes them, so tool-equipped calls are protected.
# It never sends response_format, so prompt-only JSON callers (judges, the
# grader) get no structured-output filtering from this: they rely on prompt
# discipline plus their own parsers, as they always have. Verified against the
# live catalog 2026-07-26: minimax-m3, gemma-4-31b-it, gpt-oss-120b, and
# glm-5.2 each have at least one endpoint without tool support, and an
# unpinned mid-batch reroute onto one of those looks exactly like a model
# failure.
#
# Per-model pins ride on top. gpt-oss-120b prefers Groq (decided 2026-07-26)
# for throughput and latency on the subagent and autointerp-labeler hot paths,
# which is what `order` expresses. Groq's endpoint carries full 131K context,
# tool calling, and structured output.
#
# allow_fallbacks went False -> True 2026-07-28. Single-host had no escape valve
# under fan-out: at 37 concurrent runs, 62 percent of task-1 runs hit a Groq 429
# and the 4-attempt/7-second retry ladder is too short for a sustained throttle.
# Every other model here already defaults to multi-host. usage["providers"]
# records the actual split per run if it is ever needed.
OPENROUTER_DEFAULT_ROUTING: dict[str, Any] = {"require_parameters": True}
OPENROUTER_MODEL_ROUTING: dict[str, dict[str, Any]] = {
    "openai/gpt-oss-120b": {
        "require_parameters": True,
        "order": ["groq"],
        "allow_fallbacks": True,
    },
    # Arm 3's orchestrator. Cerebras first (389 tok/s measured), then SambaNova
    # (47 tok/s, still 2x kilo). `order` is a PREFERENCE, not a restriction.
    #
    # allow_fallbacks True for the same reason gpt-oss-120b flipped above, and
    # the evidence there is directly on point: a restricted order at 37
    # concurrent put 62 percent of task-1 runs into a 429. Arm 3 runs LAST in
    # the grid, so all 64 workers land on Gemma 4 simultaneously, which is a
    # harder throttle test than that. Restricting to two hosts trades "slower"
    # for "fails", and a run that completes at 34 tok/s beats one that dies at
    # 389. Worst case here is the old speed, not a hole in the grid.
    #
    # PROVENANCE: hosts differ in quantization (Cerebras fp16, SambaNova
    # unknown, CoreWeave bf16), so arm 3 may be served by more than one
    # numerics. usage["providers"] records the actual split per run.
    # Cerebras caps completions at 40960 tokens; the orchestrator asks for 8192
    # (orchestrator.py:937), so the cap is not binding.
    "google/gemma-4-31b-it": {
        "require_parameters": True,
        "order": ["cerebras", "sambanova"],
        "allow_fallbacks": True,
    },
}


def openrouter_provider_routing(model: str) -> dict[str, Any]:
    """The `provider` routing object to send for `model` (OpenRouter only)."""
    return OPENROUTER_MODEL_ROUTING.get(model, OPENROUTER_DEFAULT_ROUTING)


_NONRETRYABLE_STOP_REASONS = frozenset({
    "refusal",         # Anthropic native refusal
    "content_filter",  # OpenRouter-normalized content filter
    "max_tokens",      # hit generation budget, same again on retry
    "stop_sequence",   # user-configured stop string hit
    # Gemini (via OpenRouter) content blocks: deterministic, so retrying wastes
    # calls and then raises. They may arrive as the normalized stop_reason or in
    # the passthrough native_finish_reason. Returning them lets the caller treat
    # the empty completion as the safety signal it is.
    "safety", "prohibited_content", "recitation", "blocklist", "spii", "image_safety",
})

_NONRETRYABLE_STATUS_CODES = frozenset({401, 403, 404, 422})


def _retry_after_seconds(exc: Any) -> float | None:
    """Seconds a 429/503 asked us to wait, or None if it did not ask.

    Reads the two headers the openai SDK reads: `retry-after-ms` (milliseconds,
    preferred because it is more precise) and `Retry-After` (seconds, or an
    HTTP-date). Returns None on anything unparseable rather than guessing, so a
    malformed header falls back to the exponential ladder instead of parking a
    worker for an arbitrary time.

    This exists because the SDK's own Retry-After handling stopped applying when
    max_retries went to 0. Without it a 429 saying "wait 30s" is answered by a
    1s, 2s, 4s ladder that gives up in seven seconds.
    """
    resp = getattr(exc, "response", None)
    headers = getattr(resp, "headers", None)
    if not headers:
        return None

    ms = headers.get("retry-after-ms")
    if ms is not None:
        try:
            v = float(ms) / 1000.0
            return v if v >= 0 else None
        except (TypeError, ValueError):
            pass

    ra = headers.get("retry-after")
    if ra is None:
        return None
    try:
        v = float(ra)
        return v if v >= 0 else None
    except (TypeError, ValueError):
        pass
    # HTTP-date form. Compare against the server's clock via the Date header
    # when present, because our clock and theirs can disagree by more than the
    # delay itself.
    try:
        target = parsedate_to_datetime(ra)
        if target is None:
            return None
        now = parsedate_to_datetime(headers["date"]) if headers.get("date") else (
            datetime.now(timezone.utc))
        if target.tzinfo is None:
            target = target.replace(tzinfo=timezone.utc)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        delta = (target - now).total_seconds()
        return delta if delta >= 0 else None
    # OverflowError is in the list because parsedate_to_datetime raises it on an
    # absurd year ("Fri, 31 Dec 999999999999 23:59:59 GMT"). This helper runs
    # INSIDE create_message's `except openai.APIStatusError` block, where the
    # sibling `except Exception` cannot catch it, so an uncaught raise here
    # aborts the whole call instead of falling back to exponential backoff. A
    # malformed header must never be more fatal than a missing one.
    except (TypeError, ValueError, KeyError, OverflowError):
        return None


def _is_nonretryable_stop(stop: str | None) -> bool:
    """Membership test on the stop reason, insensitive to the separator.

    Gateways disagree on spelling: OpenRouter normalizes to "content_filter",
    Kilo passes through "content-filter". Comparing raw strings meant the hyphen
    form missed the set, so a deterministic safety block was retried 4 times and
    then raised. That is not just wasted calls: the RuntimeError reaches
    grade_completion's `except Exception`, which reports a FAILED cell rather than
    a BLOCKED one, and a failed cell disqualifies the candidate outright instead
    of counting against --max-judge-blocks. judge_rubric.REFUSAL_STOP_REASONS
    already listed both spellings, so the two layers disagreed about the same
    response.
    """
    if not stop:
        return False
    return str(stop).lower().replace("-", "_") in _NONRETRYABLE_STOP_REASONS
# Note: 400 removed because OpenRouter intermittently returns 400 on valid
# requests (transient infrastructure). We retry with backoff.

# OpenAI finish_reason to the Anthropic stop_reason vocabulary the package expects.
# Anything not listed passes through verbatim, which is what keeps the safety-block
# reasons ("content_filter", "safety", ...) visible to _stop_signal and to
# judge_rubric.refusal_reason.
_FINISH_REASON_MAP = {
    "tool_calls": "tool_use",
    "stop": "end_turn",
    "length": "max_tokens",
}

# Provider reasoning blocks. We never send these upstream (the final answer text is
# all the package consumes) and we never build them, so they are dropped on replay.
_REASONING_BLOCK_TYPES = frozenset({"thinking", "redacted_thinking", "reasoning"})


# --- Anthropic-shaped response adapter -------------------------------------------


@dataclass
class TextBlock:
    """A `content` entry the package reads as `block.type == "text"`, `block.text`."""

    text: str
    type: str = "text"


@dataclass
class ToolUseBlock:
    """A `content` entry the package reads as `.type`, `.name`, `.input`, `.id`.

    `input` is the parsed arguments dict, matching what the Anthropic SDK handed
    back, so `execute_tool(ctx, block.name, block.input)` is unchanged.
    """

    id: str
    name: str
    input: dict
    type: str = "tool_use"


@dataclass
class Usage:
    """Anthropic-shaped token counts.

    `input_tokens` follows Anthropic semantics (it EXCLUDES cache reads), because
    `saving.compute_cost` prices input_tokens and cache_read_input_tokens
    separately and would double count otherwise. OpenAI's `prompt_tokens` includes
    cached tokens, so the adapter subtracts them.
    """

    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0


@dataclass
class LLMResponse:
    """Anthropic-shaped completion.

    `finish_reason` and `native_finish_reason` are carried alongside the mapped
    `stop_reason` on purpose. `_stop_signal` here, and `judge_rubric.refusal_reason`
    and `feature_relevance._truncation_reason` downstream, all scan those three
    fields, and a Gemini safety block routed through OpenRouter can sit in
    native_finish_reason while the normalized reason reads benign.
    """

    content: list = field(default_factory=list)
    stop_reason: str | None = None
    usage: Usage = field(default_factory=Usage)
    finish_reason: str | None = None
    native_finish_reason: str | None = None
    model: str | None = None
    # Which host actually served the request. OpenRouter populates a top-level
    # `provider` field on every completion. Multi-host open-weight slugs can
    # differ in quantization across providers, so callers persist this into
    # their usage records to make serving provenance auditable per run.
    provider: str | None = None
    raw: Any = None


# --- request conversion (Anthropic shapes in, OpenAI shapes out) ------------------


def _field(obj: Any, name: str, default: Any = None) -> Any:
    """Read one field off a block that may be a dict or an SDK/dataclass object."""
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _system_text(system: Any) -> str:
    """Flatten a `system` argument into plain text.

    Callers pass either a string or the cache_control text-block list that
    judge_rubric and feature_relevance ask for. Both collapse to the same text,
    since the OpenAI protocol has no prompt-caching marker.
    """
    if system is None:
        return ""
    if isinstance(system, str):
        return system
    if isinstance(system, (list, tuple)):
        parts = []
        for block in system:
            if isinstance(block, str):
                parts.append(block)
                continue
            text = _field(block, "text")
            if text:
                parts.append(text)
        return "\n".join(parts)
    raise TypeError(
        f"LLMClient: unsupported `system` type {type(system).__name__!r} "
        "(expected str or a list of text blocks)"
    )


def _tool_result_text(content: Any) -> str:
    """Flatten a tool_result block's content into the string OpenAI expects."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, (list, tuple)):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
                continue
            text = _field(block, "text")
            parts.append(text if text else json.dumps(block, default=str))
        return "".join(parts)
    return json.dumps(content, default=str)


def _convert_messages(system: Any, messages: list) -> list[dict]:
    """Convert an Anthropic message list into an OpenAI message list.

    Block mapping:
      text        -> the message's `content` string
      tool_use    -> an assistant `tool_calls[]` entry, arguments JSON-encoded
      tool_result -> its own {"role": "tool", "tool_call_id": ..., "content": ...}
                     message, emitted BEFORE any residual text of the same turn so
                     it still directly follows the assistant turn it answers
    Blocks arrive either as dicts (built by orchestrator.py and subagent.py) or as
    the `TextBlock` / `ToolUseBlock` objects this module handed back on the previous
    turn and the caller replayed into history.
    """
    out: list[dict] = []
    system_text = _system_text(system)
    if system_text:
        out.append({"role": "system", "content": system_text})

    for message in messages:
        role = _field(message, "role")
        content = _field(message, "content")
        if not role:
            raise ValueError(f"LLMClient: message without a role: {message!r}")

        if isinstance(content, str):
            out.append({"role": role, "content": content})
            continue
        if content is None:
            raise ValueError(f"LLMClient: message with no content: {message!r}")

        text_parts: list[str] = []
        tool_calls: list[dict] = []
        tool_messages: list[dict] = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)
                continue
            btype = _field(block, "type")
            if btype == "text":
                text_parts.append(_field(block, "text") or "")
            elif btype == "tool_use":
                tool_calls.append({
                    "id": _field(block, "id"),
                    "type": "function",
                    "function": {
                        "name": _field(block, "name"),
                        "arguments": json.dumps(_field(block, "input") or {}),
                    },
                })
            elif btype == "tool_result":
                tool_messages.append({
                    "role": "tool",
                    "tool_call_id": _field(block, "tool_use_id"),
                    "content": _tool_result_text(_field(block, "content")),
                })
            elif btype in _REASONING_BLOCK_TYPES:
                continue
            else:
                logger.warning(
                    "LLMClient: dropping unsupported content block type %r on replay",
                    btype,
                )

        text = "".join(text_parts)
        primary: dict | None = None
        if tool_calls:
            if role != "assistant":
                raise ValueError(
                    f"LLMClient: tool_use blocks on a {role!r} message, "
                    "only assistant turns may carry tool calls"
                )
            # OpenAI wants null content when a turn is tool calls only.
            primary = {"role": role, "content": text or None, "tool_calls": tool_calls}
        elif text:
            primary = {"role": role, "content": text}

        if role == "assistant":
            if primary is not None:
                out.append(primary)
            out.extend(tool_messages)
        else:
            out.extend(tool_messages)
            if primary is not None:
                out.append(primary)

    return out


def _convert_tools(tools: list) -> list[dict]:
    """Convert Anthropic tool schemas {name, description, input_schema} to OpenAI.

    A schema already in OpenAI shape passes through untouched, so a caller that
    builds native function specs is not mangled.
    """
    converted = []
    for tool in tools:
        if _field(tool, "type") == "function" and _field(tool, "function") is not None:
            converted.append(tool)
            continue
        name = _field(tool, "name")
        if not name:
            raise ValueError(f"LLMClient: tool schema without a name: {tool!r}")
        converted.append({
            "type": "function",
            "function": {
                "name": name,
                "description": _field(tool, "description") or "",
                "parameters": _field(tool, "input_schema")
                or {"type": "object", "properties": {}},
            },
        })
    return converted


# --- response conversion (OpenAI completion in, Anthropic shape out) --------------


def _parse_tool_arguments(raw: Any, tool_name: str) -> dict:
    """Parse a tool call's `arguments` into the dict the package expects.

    An argless tool (batched_anchor_sweep) legitimately arrives as "" or "{}".
    Malformed JSON raises, which lands in the retry loop, because a mangled tool
    call is usually a transient generation artifact and a silent {} would run the
    tool with wrong arguments.
    """
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    text = str(raw).strip()
    if not text:
        return {}
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError(
            f"LLMClient: tool call {tool_name!r} arguments parsed to "
            f"{type(parsed).__name__}, expected an object"
        )
    return parsed


def _message_text(message: Any) -> str:
    """Concatenate a completion message's text, tolerating a content-parts list."""
    content = _field(message, "content")
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, (list, tuple)):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
                continue
            text = _field(part, "text")
            if text:
                parts.append(text)
        return "".join(parts)
    return str(content)


def _adapt_usage(completion: Any) -> Usage:
    """Build Anthropic-shaped token counts from an OpenAI usage block."""
    raw = _field(completion, "usage")
    if raw is None:
        return Usage()
    prompt_tokens = _field(raw, "prompt_tokens", 0) or 0
    completion_tokens = _field(raw, "completion_tokens", 0) or 0
    details = _field(raw, "prompt_tokens_details")
    cache_read = (_field(details, "cached_tokens", 0) or 0) if details is not None else 0
    # OpenAI counts cached tokens inside prompt_tokens, Anthropic does not count
    # them inside input_tokens. saving.compute_cost prices the two separately, so
    # subtract to keep the cost arithmetic (and the printed per-turn numbers)
    # comparable with every historical run.
    input_tokens = max(prompt_tokens - cache_read, 0)
    return Usage(
        input_tokens=input_tokens,
        output_tokens=completion_tokens,
        cache_creation_input_tokens=0,  # no OpenAI-protocol equivalent
        cache_read_input_tokens=cache_read,
    )


def _adapt_response(completion: Any) -> LLMResponse:
    """Convert an OpenAI chat completion into the Anthropic-shaped response object."""
    usage = _adapt_usage(completion)
    model = _field(completion, "model")
    provider = _field(completion, "provider")
    choices = _field(completion, "choices") or []
    if not choices:
        # A 200 with no choices is the transient empty completion the retry loop
        # exists for. Return it empty rather than raising, so the loop can decide.
        return LLMResponse(content=[], stop_reason=None, usage=usage, model=model,
                           provider=provider, raw=completion)

    choice = choices[0]
    message = _field(choice, "message")
    finish_reason = _field(choice, "finish_reason")
    native_finish_reason = _field(choice, "native_finish_reason")

    blocks: list = []
    text = _message_text(message) if message is not None else ""
    if text:
        blocks.append(TextBlock(text=text))

    tool_calls = (_field(message, "tool_calls") if message is not None else None) or []
    for i, call in enumerate(tool_calls):
        function = _field(call, "function")
        name = _field(function, "name") or ""
        if not name:
            raise ValueError(f"LLMClient: tool call {i} has no function name")
        call_id = _field(call, "id")
        if not call_id:
            # Some OpenAI-compatible servers omit the id. We mint one, and because
            # the id we send back on replay is the one we minted, the round trip
            # stays consistent.
            call_id = f"call_{i}"
            logger.warning(
                "LLMClient: tool call %r arrived without an id, using %r", name, call_id
            )
        blocks.append(ToolUseBlock(
            id=call_id,
            name=name,
            input=_parse_tool_arguments(_field(function, "arguments"), name),
        ))

    stop_reason = None
    if finish_reason is not None:
        key = str(finish_reason).lower()
        stop_reason = _FINISH_REASON_MAP.get(key, str(finish_reason))
    # Some OpenAI-compatible servers (notably vLLM tool-call parsers) report
    # finish_reason "stop" even when tool_calls are present. Ending the turn there
    # would silently drop the calls, so the presence of tool calls wins.
    if tool_calls and stop_reason == "end_turn":
        stop_reason = "tool_use"

    return LLMResponse(
        content=blocks,
        stop_reason=stop_reason,
        usage=usage,
        finish_reason=str(finish_reason) if finish_reason is not None else None,
        native_finish_reason=(
            str(native_finish_reason) if native_finish_reason is not None else None
        ),
        model=model,
        provider=provider,
        raw=completion,
    )


# --- client ----------------------------------------------------------------------


class LLMClient:
    """OpenAI-protocol client that hands back Anthropic-shaped responses."""

    MAX_RETRIES = 3
    BACKOFF_BASE_SECONDS = 1.0
    # Ceiling on how long a server's Retry-After can park one attempt. Matches
    # the openai SDK's own cap, so honoring the header here reproduces what the
    # SDK did before max_retries went to 0. Four attempts x 60s stays inside the
    # launcher's 3600s per-run reap.
    MAX_RETRY_AFTER_SECONDS = 60.0

    def __init__(self, provider: str = "openrouter", api_key: str | None = None,
                 base_url: str | None = None):
        """Build a client.

        `provider` and `api_key` keep position 1 and 2, because every call site in
        the repo passes them by those names. `base_url` is new and optional. The
        default was "anthropic" while that name silently aliased OpenRouter; it is
        now "openrouter", which is the endpoint those runs were always using.

        Resolution order for the endpoint is explicit `base_url`, then the
        LLM_BASE_URL environment variable (the global override, so entry scripts
        need no edit), then the provider default.
        """
        check_provider(provider)
        self.provider = provider
        resolved_base_url = base_url or os.environ.get("LLM_BASE_URL") or None

        if resolved_base_url is None and provider in _OPENROUTER_PROVIDERS:
            resolved_base_url = OPENROUTER_BASE_URL

        if resolved_base_url is None and provider in _GATEWAYS:
            resolved_base_url = _GATEWAYS[provider][0]

        if resolved_base_url is None:
            raise ValueError(
                f"LLMClient: provider {provider!r} has no default endpoint. Pass "
                "base_url= or set LLM_BASE_URL."
            )

        # Key selection follows the RESOLVED endpoint, never the declared provider.
        # LLM_BASE_URL and an explicit base_url= can redirect a provider="kilo"
        # client at a Modal vLLM server or anything else, and picking the key off
        # `provider` there would hand KILO_API_KEY to whatever host that variable
        # names. Deriving it from the URL means a redirected client falls through
        # to the LLM_API_KEY branch, which is the correct credential for the host
        # actually being talked to.
        normalized = resolved_base_url.rstrip("/")
        is_openrouter = normalized == OPENROUTER_BASE_URL
        gateway_at = next(
            (p for p, (url, _) in _GATEWAYS.items() if normalized == url.rstrip("/")),
            None,
        )
        if (provider in _GATEWAYS or provider in _OPENROUTER_PROVIDERS) \
                and not is_openrouter and gateway_at is None:
            logger.warning(
                "LLMClient: provider=%r but the endpoint resolved to %s (base_url= "
                "or LLM_BASE_URL wins). Using LLM_API_KEY for that host, not %s.",
                provider, resolved_base_url, api_key_names(provider)
            )
        if is_openrouter:
            key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
            if not key:
                logger.warning(
                    "LLMClient: no OpenRouter API key (pass api_key= or set "
                    "OPENROUTER_API_KEY). Calls will fail with a 401."
                )
        elif gateway_at is not None:
            key = api_key or gateway_api_key(gateway_at)
            if not key:
                logger.warning(
                    "LLMClient: no %s API key (pass api_key= or set %s). Calls "
                    "will fail with a 401.", gateway_at, api_key_names(gateway_at)
                )
        else:
            # Modal vLLM and friends. vLLM accepts any bearer token, so "EMPTY" is
            # the conventional placeholder rather than a silent fallback.
            key = api_key or os.environ.get("LLM_API_KEY") or "EMPTY"

        self.base_url = resolved_base_url
        # Only OpenRouter understands the `provider` routing object. vLLM and
        # other OpenAI-compatible endpoints must not receive it.
        self._is_openrouter = is_openrouter
        # Per-model pins (model_pins) send some models to a different gateway
        # than this client's own. They are honored only when the endpoint came
        # from the provider default: an explicit base_url or LLM_BASE_URL means
        # the operator pointed this run at one specific server (a Modal vLLM,
        # say), and quietly calling out to OpenRouter behind that instruction
        # would be wrong. Delegates are built lazily, one per routed provider.
        self._pinning_enabled = base_url is None and not os.environ.get("LLM_BASE_URL")
        self._delegates: dict[str, LLMClient] = {}
        # Explicit timeout and max_retries=0, because the two retry ladders used
        # to MULTIPLY. create_message already retries MAX_RETRIES+1 = 4 times and
        # already catches APITimeoutError, while the SDK default max_retries=2
        # added 3 more tries INSIDE each of those, invisibly. At the default
        # read=600s the worst case was 4 x 3 x 600s = 2 hours on one call, with
        # nothing logged, which is what a "hung first call" looked like: 11 runs
        # in the secret-elicitation grid sat silent until the launcher's 3600s ceiling
        # reaped them, and one that hung 37 minutes while running SOLO completed
        # in 71s on a plain retry.
        #
        # Retrying in one place instead of two bounds that at 4 x 600s and makes
        # every attempt visible, since create_message prints its ladder and the
        # SDK's inner one printed nothing.
        #
        # read stays at 600s ON PURPOSE. It must clear honest work: max_tokens
        # is 8192 (orchestrator.py) and a loaded endpoint can drop to ~20 tok/s,
        # so a legitimate generation can run ~410s. Shortening read to "fix" the
        # hang would truncate real completions instead, which fails silently and
        # is far worse than waiting. connect is raised 5s -> 10s because a cold
        # gateway under a 64-way opening burst can exceed 5s to first byte and
        # that surfaced as spurious retries.
        self._client = openai.OpenAI(
            base_url=resolved_base_url,
            api_key=key,
            timeout=openai.Timeout(connect=10.0, read=600.0, write=120.0, pool=120.0),
            max_retries=0,
        )

    def _backend_for(self, model: str) -> tuple[Any, bool]:
        """(SDK handle, is_openrouter) that should serve ``model``.

        Usually this client's own. A pinned model (model_pins) is served by a
        lazily built delegate for its gateway instead, so one run can send its
        orchestrator to Kilo while gpt-oss-120b keeps going to OpenRouter/Groq.
        The returned flag travels with the handle because the `provider` routing
        object is OpenRouter-only and must follow the destination actually
        called, not the run's configured provider.
        """
        if not self._pinning_enabled:
            return self._client, self._is_openrouter
        routed = provider_for(model, self.provider)
        if routed == self.provider:
            return self._client, self._is_openrouter
        delegate = self._delegates.get(routed)
        if delegate is None:
            # The delegate's own provider equals the pin target, so its
            # _backend_for short-circuits above and this cannot recurse.
            delegate = LLMClient(provider=routed)
            self._delegates[routed] = delegate
            logger.info(
                "LLMClient: %s is pinned to provider %r, routing it to %s while "
                "this run's default provider is %r.",
                model, routed, delegate.base_url, self.provider,
            )
        return delegate._client, delegate._is_openrouter

    def create_message(self, *, model, system, messages, tools=None, max_tokens=4096,
                       temperature: float | None = None,
                       cache_control_breakpoint: str | None = None):
        """Create a message with retry on transient empty responses.

        Some upstreams (notably minimax via OpenRouter) intermittently return 200
        responses with no content blocks or zero tokens, a well-documented
        infrastructure transience covered by OpenRouter's Zero Completion Insurance.
        We retry these with exponential backoff.

        We do NOT retry when the empty response carries a legitimate stop signal
        (refusal, content_filter, max_tokens, stop_sequence), these will not resolve
        on retry. We also do NOT retry on client-side HTTP errors (auth, not found,
        policy block), they are deterministic.

        `cache_control_breakpoint` is an Anthropic prompt-caching concept with no
        OpenAI-protocol equivalent, so it is accepted and ignored. Callers keep
        passing it (judge_rubric, feature_relevance) and nothing breaks. OpenRouter
        and vLLM auto-cache long constant prefixes anyway, so no caching is lost.
        """
        del cache_control_breakpoint  # accepted for signature compatibility, no-op

        resolved_model = self.resolve_model(model)
        backend, is_openrouter = self._backend_for(resolved_model)
        kwargs: dict[str, Any] = {
            "model": resolved_model,
            "max_tokens": max_tokens,
            "messages": _convert_messages(system, messages),
        }
        if tools:
            kwargs["tools"] = _convert_tools(tools)
        # Drop a redundant temperature=1.0 on OpenRouter, because sending it costs
        # routability and buys nothing. 1.0 is the API default, and the
        # require_parameters filter below removes every endpoint that does not
        # ADVERTISE a parameter the request sends. OpenAI's reasoning endpoints do
        # not advertise `temperature`, so an explicit 1.0 leaves zero eligible
        # endpoints and OpenRouter answers 404 "No endpoints found that can handle
        # the requested parameters" rather than falling back.
        #
        # Observed 2026-07-28: all 87 grade_completion calls on openai/gpt-5.4 died
        # this way, leaving a finished run with every score null. openai/gpt-5.6-terra
        # (arm 4) fails identically. minimax-m3 and gemma-4-31b-it do not.
        # The orchestrator path was unaffected only because it never sends temperature.
        #
        # Scoped to OpenRouter and to exactly 1.0 on purpose. Kilo and custom
        # LLM_BASE_URL endpoints keep an explicit 1.0, since their sampling default
        # is not ours to assume. A NON-default temperature is still always sent, and
        # still 404s on an endpoint that cannot honor it, which is correct: silently
        # sampling at 1.0 when 0.0 was requested (feature_relevance.py) would be a
        # worse failure than a loud one.
        if temperature is not None and not (is_openrouter and temperature == 1.0):
            kwargs["temperature"] = temperature
        if is_openrouter:
            kwargs["extra_body"] = {
                "provider": openrouter_provider_routing(resolved_model)
            }

        last_diagnostic = None
        retry_after = None  # seconds the server ASKED for, honored below
        for attempt in range(self.MAX_RETRIES + 1):
            retry_after = None
            try:
                completion = backend.chat.completions.create(**kwargs)
                response = _adapt_response(completion)
                if _has_useful_content(response):
                    return response
                stop = _stop_signal(response)
                if _is_nonretryable_stop(stop):
                    print(
                        f"[LLMClient] non-retryable empty response "
                        f"(model={resolved_model}, stop_reason={stop!r}) - returning to caller"
                    )
                    return response
                n_blocks = len(response.content or [])
                error = _field(completion, "error")
                error_note = f", error={error!r}" if error else ""
                last_diagnostic = (
                    f"empty response (stop_reason={stop!r}, "
                    f"content_blocks={n_blocks}{error_note})"
                )
            except openai.APIStatusError as e:
                if e.status_code in _NONRETRYABLE_STATUS_CODES:
                    raise
                retry_after = _retry_after_seconds(e)
                last_diagnostic = f"{type(e).__name__} ({e.status_code}): {e}"
            except (openai.APIConnectionError, openai.APITimeoutError) as e:
                # Transport-level transience (DNS, reset, read timeout). Retry.
                last_diagnostic = f"{type(e).__name__}: {e}"
            except Exception as e:
                status = getattr(e, "status_code", None)
                if status in _NONRETRYABLE_STATUS_CODES:
                    raise
                last_diagnostic = f"{type(e).__name__}: {e}"

            if attempt < self.MAX_RETRIES:
                sleep_s = self.BACKOFF_BASE_SECONDS * (2 ** attempt)
                # Honor Retry-After when the server sent one. Our ladder is
                # 1+2+4 = 7 seconds total, so a 429 carrying "Retry-After: 30"
                # would otherwise burn all four attempts inside seven seconds
                # and fail a request the server was willing to serve. The SDK
                # used to do this for us; it stopped being ours for free when
                # max_retries went to 0 to keep the two ladders from
                # multiplying, so it has to live here now.
                waited_for_server = False
                if retry_after is not None:
                    sleep_s = max(sleep_s, min(retry_after, self.MAX_RETRY_AFTER_SECONDS))
                    waited_for_server = True
                print(
                    f"[LLMClient retry {attempt + 1}/{self.MAX_RETRIES}] "
                    f"model={resolved_model} - {last_diagnostic} - sleeping {sleep_s:.1f}s"
                    + (" (server Retry-After)" if waited_for_server else "")
                )
                time.sleep(sleep_s)

        raise RuntimeError(
            f"LLMClient.create_message failed after {self.MAX_RETRIES + 1} attempts "
            f"(model={resolved_model}): {last_diagnostic}"
        )

    def resolve_model(self, model: str) -> str:
        """Prefix a bare model name for an aggregator gateway if needed.

        Kilo shares OpenRouter's `vendor/model` slug convention, so a legacy call
        site passing a bare "claude-sonnet-5" needs the same normalization on
        either route. Every JUDGE_PANEL slug is already qualified, so this only
        matters to the older bare-name call sites.
        """
        if "/" not in model and (self.provider == "openrouter"
                                 or self.provider in _GATEWAYS):
            return f"anthropic/{model}"
        return model


def _stop_signal(response):
    """Lowercased stop reason from whichever field the provider populated.

    We map finish_reason into the Anthropic stop_reason vocabulary, OpenRouter
    passes the underlying model's reason through native_finish_reason, and the raw
    finish_reason is kept too. A safety block (e.g. Gemini SAFETY) can land in
    native_finish_reason while stop_reason reads a benign "end_turn", so we prefer
    the first field naming a known non-retryable reason, and otherwise fall back to
    the first populated field (preserving the prior diagnostic, which reported
    stop_reason).
    """
    fallback = None
    for attr in ("stop_reason", "native_finish_reason", "finish_reason"):
        v = getattr(response, attr, None)
        if v:
            lv = str(v).lower()
            if lv in _NONRETRYABLE_STOP_REASONS:
                return lv
            if fallback is None:
                fallback = lv
    return fallback


def _has_useful_content(response) -> bool:
    """Return True if the response contains at least one tool_use block or non-empty text.

    Empty responses (content=[], or all text blocks whitespace-only) indicate
    an upstream drop rather than a legitimate stop.
    """
    content = getattr(response, "content", None)
    if not content:
        return False
    for block in content:
        btype = getattr(block, "type", None)
        if btype == "tool_use":
            return True
        if btype == "text" and (getattr(block, "text", "") or "").strip():
            return True
    return False


def shorten_model_name(model: str) -> str:
    """Derive a short directory-friendly model name.

    Examples:
        claude-opus-4-6 -> opus-4-6
        anthropic/claude-sonnet-4-6 -> sonnet-4-6
        openai/gpt-4o -> gpt-4o
        google/gemini-2.5-flash -> gemini-2.5-flash

    Raises on a missing name rather than producing a "None" directory. An arm
    that declares ``subagent_model=None`` means "this arm runs no subagents", so
    the caller must keep RunConfig's default, not forward the None.
    """
    if not isinstance(model, str) or not model:
        raise ValueError(
            f"shorten_model_name needs a model name, got {model!r}. If this came "
            "from an ArmSpec with subagent_model=None, keep the RunConfig default "
            "instead of forwarding the None."
        )
    # Strip provider prefix
    if "/" in model:
        model = model.split("/", 1)[1]
    # Strip claude- prefix
    if model.startswith("claude-"):
        model = model[len("claude-"):]
    return model
