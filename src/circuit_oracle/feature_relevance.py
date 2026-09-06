"""Neuronpedia batch fetch plus an LLM dual-axis relevance scorer for seed selection.

Two responsibilities, both used by the deterministic multi-stage seed-sweep
(stages ii and iii) before pinning the top features.

1. ``fetch_payloads`` pulls Neuronpedia inspect payloads for a pool of candidate
   features in parallel, reusing ``tools._fetch_inspect_payload`` (the documented
   HTTP seam) so behavior matches ``inspect_feature``. It dedups by
   ``(layer, feature_idx)`` (payloads are position-independent) and writes each
   payload into ``ctx.inspect_cache`` keyed by ``(layer, feature_idx, pos)`` for
   every position seen, so the later discovery-variant reassess agent gets a cache
   hit instead of a second backend round-trip.

2. ``score_relevance`` fans out ONE ``LLMClient.create_message`` call PER distinct
   pool feature (the same per-item fan-out the harness grader uses in
   ``saving.grade_interventions``, not a single batched judge call). Each call
   scores the feature on two independent axes in ``[0, 1]``: ``topic_relevance``
   (does the feature carry the subject matter of the question) and
   ``mechanism_relevance`` (does the feature look like part of the refusal /
   suppression machinery). The scorer model returns both axis scores and is never
   told how they are combined. The harness combines them as
   ``relevance = max(topic, mechanism)``, so a feature passes the gate by being
   either topic-specific (a Tiananmen content feature) or mechanism-specific (a
   refusal gate whose autointerp label looks generic). That disjunction matches
   the two shapes the winning interventions actually take.

FAIL-LOUD throughout. A Neuronpedia ``{"error": ...}`` payload, a missing
payload for a candidate, or a per-feature reply that stays unparseable after
the retry budget raises with a message naming the offending feature or the raw
text. A deterministic provider block (the scorer model's safety filter firing,
or the reply hitting max_tokens before any text) raises IMMEDIATELY without
burning retries, since re-asking the identical request cannot resolve it. There
are no silent fallbacks and no fabricated defaults. A blocked feature gets no
made-up score, the run aborts and the error names the feature and the stop
reason.
"""

from __future__ import annotations

import concurrent.futures
import json
import re
from typing import Any, Iterable

from .judge_rubric import refusal_reason


# ---------------------------------------------------------------------------
# Neuronpedia batch fetch
# ---------------------------------------------------------------------------

def fetch_payloads(
    ctx,
    pairs: Iterable[tuple[int, int, int]],
    max_workers: int = 8,
) -> dict[tuple[int, int], dict]:
    """Fetch Neuronpedia inspect payloads for a pool of candidate features.

    Args:
        ctx: the run ToolContext (carries ``neuronpedia_model_id`` /
            ``neuronpedia_sae_id`` and ``inspect_cache``).
        pairs: iterable of ``(layer, feature_idx, pos)`` triples. The pool may
            list the same ``(layer, feature_idx)`` at several positions. Payloads
            are position-independent (the autointerp label is a per-feature
            property), so the backend is hit once per distinct
            ``(layer, feature_idx)``.
        max_workers: thread-pool width for the concurrent fetch.

    Returns:
        ``{(layer, feature_idx): payload}`` for every distinct pair fetched.

    Side effect:
        Writes each payload into ``ctx.inspect_cache`` keyed by
        ``(layer, feature_idx, pos)`` for EVERY position seen for that pair,
        matching ``inspect_feature`` so the reassess agent gets a cache hit.

    FAIL-LOUD: if any payload comes back as an ``{"error": ...}`` dict (a feature
    Neuronpedia has never seen, or a transport error), raise naming the feature.
    """
    # Lazy import so this module stays importable on CPU without torch /
    # circuit_tracer (tools.py imports both at module top). Referencing the
    # module attribute (not a bound name) keeps monkeypatching
    # tools._fetch_inspect_payload visible at call time.
    from . import tools

    # Collect distinct (layer, feature_idx) and remember every pos seen per pair.
    positions_by_pair: dict[tuple[int, int], set[int]] = {}
    for layer, feature_idx, pos in pairs:
        key = (int(layer), int(feature_idx))
        positions_by_pair.setdefault(key, set()).add(int(pos))

    def _fetch(pair: tuple[int, int]) -> tuple[tuple[int, int], dict]:
        layer, feature_idx = pair
        payload = tools._fetch_inspect_payload(ctx, layer, feature_idx)
        return pair, payload

    payloads: dict[tuple[int, int], dict] = {}
    distinct_pairs = list(positions_by_pair.keys())
    if not distinct_pairs:
        return payloads

    workers = max(1, min(max_workers, len(distinct_pairs)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(_fetch, p) for p in distinct_pairs]
        for fut in concurrent.futures.as_completed(futures):
            pair, payload = fut.result()
            payloads[pair] = payload

    # FAIL-LOUD on any error payload, naming the feature.
    for (layer, feature_idx), payload in payloads.items():
        if isinstance(payload, dict) and "error" in payload:
            raise RuntimeError(
                f"Neuronpedia fetch failed for L{layer}:F{feature_idx} "
                f"(pool relevance fetch): {payload['error']}"
            )

    # Write into ctx.inspect_cache keyed by (layer, feature_idx, pos) for every
    # pos seen, matching inspect_feature so the reassess agent gets a cache hit.
    for (layer, feature_idx), payload in payloads.items():
        for pos in positions_by_pair[(layer, feature_idx)]:
            ctx.inspect_cache[(layer, feature_idx, pos)] = payload

    return payloads


# ---------------------------------------------------------------------------
# LLM dual-axis relevance scorer (one call per feature, fanned out)
# ---------------------------------------------------------------------------

# Per-feature retry budget for logical failures (unparseable reply, missing or
# non-numeric axis score, empty response). Transport-level transience is already
# retried inside LLMClient.create_message, so this layer only re-asks on bad
# content. Mirrors subagent.SUBAGENT_MAX_ATTEMPTS.
_RELEVANCE_MAX_ATTEMPTS = 3

# Thread-pool width for the per-feature fan-out. Matches the harness grader
# (saving._GRADER_MAX_WORKERS) and the Neuronpedia fetch above.
_RELEVANCE_MAX_WORKERS = 8

# Stop reasons that mean the reply was truncated before any text (a reasoning
# model burned the whole max_tokens budget on internal channels). Like a safety
# block, this reproduces deterministically on an identical re-ask, so it is
# raised immediately instead of burning the retry budget.
_TRUNCATION_STOP_REASONS = ("max_tokens", "length")


class RelevanceScoringBlocked(RuntimeError):
    """The relevance model deterministically returned no text for a feature.

    Raised when the reply is empty AND carries a stop reason that re-asking the
    byte-identical request cannot fix: a provider safety block (see
    ``judge_rubric.refusal_reason``) or a max_tokens truncation. Deliberately
    NOT a ValueError, so the per-feature retry loop never catches it. There is
    no placeholder score (a fabricated relevance would silently skew
    selection), the run fails loud naming the feature and the stop reason.
    """


def _truncation_reason(response) -> str | None:
    """Return the matched truncation stop reason (lowercased) or None."""
    for attr in ("stop_reason", "finish_reason", "native_finish_reason"):
        v = getattr(response, attr, None)
        if v and str(v).lower() in _TRUNCATION_STOP_REASONS:
            return str(v).lower()
    return None


_RELEVANCE_SYSTEM = (
    "You score a single transcoder feature on two independent axes, each on a "
    "scale from 0 to 1. You receive the user's question, optional prompt "
    "context, and one feature described by its autointerp label, example top "
    "tokens, and promoted/suppressed token lists.\n"
    "\n"
    "topic_relevance: how strongly the feature represents topic or content "
    "that bears on the subject of the question (the entity, event, claim, or "
    "domain being asked about). 0 = generic. Generic means format or syntax "
    "or role tokens, assistant-persona, or activating context that is "
    "off-topic for the question.\n"
    "\n"
    "mechanism_relevance: how strongly the feature looks like part of the "
    "model's refusal or suppression machinery (the mechanism that gates, "
    "refuses, censors, or sanitizes the response), regardless of topic. "
    "Evidence includes refusal or inability language (cannot, unable, sorry, "
    "decline), safety, policy, legality, harm, or sensitivity detection, "
    "censorship or topic gating, apology or affect framing, and substitution "
    "of sanitized boilerplate in place of an answer. Promoted and suppressed "
    "tokens are strong evidence here. A feature whose label looks generic can "
    "still score high if its promoted tokens read as refusal or safety "
    "vocabulary. 0 = no sign of any such role.\n"
    "\n"
    "Score the two axes independently. A feature can be high on one and low "
    "on the other, high on both, or low on both.\n"
    "Do NOT reward or penalize how rare or frequently-firing the feature is "
    "(rarity is scored separately, which avoids double counting).\n"
    "Return STRICTLY a JSON object "
    '{"topic_relevance": <number in [0, 1]>, "mechanism_relevance": <number '
    "in [0, 1]>}. Return nothing but the JSON object."
)


def _example_tokens(payload: dict) -> list[str]:
    """Pull the up-to-10 example max_token strings from an inspect payload.

    The payload shape comes from tools._fetch_inspect_payload: a list of
    {text_snippet, max_activation, max_token} under top_activating_examples.
    """
    examples = payload.get("top_activating_examples") or []
    tokens: list[str] = []
    for ex in examples[:10]:
        tok = ex.get("max_token")
        if tok is not None:
            tokens.append(tok)
    return tokens


def _build_candidate_items(candidates, payloads: dict[tuple[int, int], dict]) -> list[dict]:
    """Build the compact per-feature JSON items sent to the relevance model.

    ``candidates`` is an iterable of objects (FeatureCandidate) or dicts carrying
    ``layer`` and ``feature_idx``. The list index becomes the stable ``idx`` used
    in error messages. FAIL-LOUD if a candidate has no payload in ``payloads``.
    """
    items: list[dict] = []
    for idx, cand in enumerate(candidates):
        layer = int(_attr(cand, "layer"))
        feature_idx = int(_attr(cand, "feature_idx"))
        payload = payloads.get((layer, feature_idx))
        if payload is None:
            raise KeyError(
                f"score_relevance: no Neuronpedia payload for candidate "
                f"L{layer}:F{feature_idx} (idx={idx}). Fetch the pool first."
            )
        items.append({
            "idx": idx,
            "layer": layer,
            "feature_idx": feature_idx,
            "autointerp": payload.get("autointerp"),
            "top_tokens": _example_tokens(payload),
            "promoted": payload.get("promoted_tokens") or [],
            "suppressed": payload.get("suppressed_tokens") or [],
        })
    return items


def _attr(obj, name: str):
    """Read ``name`` from a dataclass-like object or a dict."""
    if isinstance(obj, dict):
        return obj[name]
    return getattr(obj, name)


def _extract_text(response) -> str:
    """Concatenate the text blocks of an Anthropic-style response."""
    parts: list[str] = []
    for block in (getattr(response, "content", None) or []):
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", "") or "")
    return "".join(parts)


def _last_json_object(text: str) -> dict | None:
    """Return the LAST parseable JSON object in ``text``, or None.

    Scans every ``{`` with ``json.JSONDecoder.raw_decode``, so prose around the
    object (even prose containing stray braces) and reasoning-channel scratch
    objects before the final answer are both tolerated. The last object wins,
    matching subagent._extract_json_object's convention for reasoning models.
    """
    decoder = json.JSONDecoder()
    last: dict | None = None
    idx = text.find("{")
    while idx != -1:
        try:
            obj, end = decoder.raw_decode(text[idx:])
        except json.JSONDecodeError:
            idx = text.find("{", idx + 1)
            continue
        if isinstance(obj, dict):
            last = obj
        idx = text.find("{", idx + end)
    return last


def _parse_dual_scores(text: str) -> tuple[float, float]:
    """Parse one model reply into a clamped (topic, mechanism) score pair.

    Tolerates a fenced ```json block or surrounding prose (including prose with
    stray braces) by taking the last parseable JSON object. FAIL-LOUD
    (ValueError) if no object is parseable, if either axis key is missing, or if
    a value is non-numeric. Each axis score is clamped to ``[0, 1]``.
    """
    candidate = text.strip()
    fenced = re.search(r"```(?:json)?\s*(.+?)```", candidate, re.S | re.I)
    if fenced:
        candidate = fenced.group(1).strip()
    parsed = _last_json_object(candidate)
    if parsed is None:
        raise ValueError(
            f"could not parse a JSON object from the model reply. "
            f"Raw text: {text[:500]!r}"
        )
    values: list[float] = []
    for key in ("topic_relevance", "mechanism_relevance"):
        if key not in parsed:
            raise ValueError(
                f"model reply is missing {key!r}. Raw text: {text[:500]!r}"
            )
        try:
            val = float(parsed[key])
        except (TypeError, ValueError):
            raise ValueError(
                f"non-numeric {key}: {parsed[key]!r}. Raw text: {text[:500]!r}"
            )
        values.append(min(1.0, max(0.0, val)))
    return values[0], values[1]


def score_relevance(
    client,
    model: str,
    *,
    user_message: str,
    candidates,
    payloads: dict[tuple[int, int], dict],
    system_prompt: str | None = None,
    baseline_answer: str | None = None,
    max_workers: int = _RELEVANCE_MAX_WORKERS,
) -> tuple[dict[tuple[int, int], float], dict, dict[tuple[int, int], dict]]:
    """Score each pool feature on the topic and mechanism axes, one call per feature.

    ONE ``LLMClient.create_message`` call PER distinct ``(layer, feature_idx)``
    (NOT a single batched call over the whole pool), fanned out on a thread pool
    the same way the harness grader fans out ``grade_completion`` calls. Each
    feature is sent as ``{layer, feature_idx, autointerp, top_tokens, promoted,
    suppressed}``, where ``top_tokens`` is the up-to-10 example ``max_token``
    strings from the Neuronpedia payload. The system rubric asks for two
    independent axis scores (``topic_relevance`` and ``mechanism_relevance``) and
    explicitly ignores rarity (rarity enters separately in stage iii, which avoids
    double counting). The model is never told how the axes are combined. The
    combination happens here: ``relevance = max(topic, mechanism)``.

    Args:
        client: an LLMClient (or anything exposing ``create_message``).
        model: the relevance model id (e.g. ``openai/gpt-oss-120b``).
        user_message: the subject-model user prompt being analyzed.
        candidates: iterable of FeatureCandidate-like objects (or dicts) carrying
            ``layer`` and ``feature_idx``. Duplicate ``(layer, feature_idx)``
            pairs (the same feature at several positions) are scored once.
        payloads: ``{(layer, feature_idx): payload}`` from ``fetch_payloads``.
        system_prompt: optional subject-model system prompt for added context.
        baseline_answer: optional baseline (refusal) completion for added context.
        max_workers: thread-pool width for the fan-out.

    Returns:
        ``(scores, usage, detail)`` where ``scores`` is
        ``{(layer, feature_idx): relevance in [0, 1]}`` with
        ``relevance = max(topic, mechanism)``, ``usage`` is the token-accounting
        dict accumulated over every per-feature call including retries (carries
        ``model`` so ``saving.compute_cost`` can price it), and ``detail`` is
        ``{(layer, feature_idx): {topic_relevance, mechanism_relevance,
        relevance}}`` for the run artifacts.

    FAIL-LOUD: raises if a candidate has no payload, or if any single feature's
    reply stays unparseable (or empty, or missing an axis) after
    ``_RELEVANCE_MAX_ATTEMPTS`` attempts, naming the feature. Two failure kinds
    skip the retry loop and propagate immediately: transport errors raised by
    ``create_message`` (LLMClient already retries transient ones internally),
    and ``RelevanceScoringBlocked`` for a deterministic provider block (the
    scorer model's safety filter firing, or a max_tokens truncation before any
    text), where re-asking the identical request cannot change the outcome.
    There is no placeholder score for a blocked feature, a fabricated relevance
    would silently skew selection.
    """
    candidates = list(candidates)
    items = _build_candidate_items(candidates, payloads)

    # Dedup by (layer, feature_idx). The pool may list the same feature at
    # several positions and the axis scores are position-independent, so each
    # distinct pair is scored exactly once.
    items_by_pair: dict[tuple[int, int], dict] = {}
    for item in items:
        items_by_pair.setdefault((item["layer"], item["feature_idx"]), item)

    context_lines = [f"User question:\n{user_message}"]
    if system_prompt:
        context_lines.append(f"\nSubject-model system prompt:\n{system_prompt}")
    if baseline_answer:
        context_lines.append(f"\nBaseline answer (no intervention):\n{baseline_answer}")
    context_block = "\n".join(context_lines)

    def _score_one(item: dict) -> tuple[tuple[int, int], float, float, list]:
        feature_json = json.dumps(
            {k: item[k] for k in (
                "layer", "feature_idx", "autointerp", "top_tokens",
                "promoted", "suppressed",
            )},
            ensure_ascii=False,
        )
        user_content = (
            f"{context_block}\n\n"
            f"Score the following feature on the two axes (topic_relevance, "
            f"mechanism_relevance) with respect to the user question. Return "
            f"STRICTLY one JSON object.\n\n"
            f"Feature (JSON):\n{feature_json}"
        )
        usages: list[Any] = []
        last_exc: Exception | None = None
        for _attempt in range(_RELEVANCE_MAX_ATTEMPTS):
            response = client.create_message(
                model=model,
                system=_RELEVANCE_SYSTEM,
                messages=[{"role": "user", "content": user_content}],
                # Reasoning models burn tokens on internal channels before the
                # JSON answer. 4096 is headroom, only generated tokens bill.
                max_tokens=4096,
                temperature=0.0,
                # The rubric is constant across the whole fan-out, so mark it
                # cacheable (no-op on OpenRouter/OpenAI, which auto-cache).
                cache_control_breakpoint="ephemeral",
            )
            usages.append((
                getattr(response, "usage", None),
                # Serving provenance (OpenRouter host), counted per attempt.
                getattr(response, "provider", None),
            ))
            try:
                text = _extract_text(response)
                if not text.strip():
                    # An empty reply with a safety-block or truncation stop
                    # reason reproduces deterministically on an identical
                    # re-ask. RelevanceScoringBlocked is a RuntimeError, so
                    # it escapes the ValueError retry catch immediately. No
                    # placeholder score, fail loud naming the feature.
                    blocked = refusal_reason(response)
                    truncated = _truncation_reason(response)
                    if blocked or truncated:
                        kind = (
                            "the scorer model's safety filter blocked the call"
                            if blocked
                            else "the reply hit max_tokens before any text"
                        )
                        raise RelevanceScoringBlocked(
                            f"score_relevance: no text for "
                            f"L{item['layer']}:F{item['feature_idx']}, "
                            f"{kind} (stop_reason="
                            f"{(blocked or truncated)!r}). Retrying the "
                            f"identical request cannot resolve a "
                            f"deterministic block, aborting without burning "
                            f"retries. Try a different --relevance-model."
                        )
                    raise ValueError(
                        "empty relevance response (no text blocks)"
                    )
                topic, mechanism = _parse_dual_scores(text)
                return (item["layer"], item["feature_idx"]), topic, mechanism, usages
            except ValueError as exc:
                last_exc = exc
        raise ValueError(
            f"score_relevance: L{item['layer']}:F{item['feature_idx']} failed "
            f"after {_RELEVANCE_MAX_ATTEMPTS} attempts: {last_exc}"
        ) from last_exc

    usage = {
        "model": model,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
        # Serving provenance: host -> call count across the scoring fan-out.
        "providers": {},
    }
    scores: dict[tuple[int, int], float] = {}
    detail: dict[tuple[int, int], dict] = {}

    pairs = list(items_by_pair.keys())
    if not pairs:
        return scores, usage, detail

    workers = max(1, min(max_workers, len(pairs)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(_score_one, items_by_pair[p]) for p in pairs]
        for fut in concurrent.futures.as_completed(futures):
            pair, topic, mechanism, usages = fut.result()
            relevance = max(topic, mechanism)
            scores[pair] = relevance
            detail[pair] = {
                "topic_relevance": topic,
                "mechanism_relevance": mechanism,
                "relevance": relevance,
            }
            for u, served_by in usages:
                key = served_by or "unknown"
                usage["providers"][key] = usage["providers"].get(key, 0) + 1
                if u is None:
                    continue
                usage["input_tokens"] += getattr(u, "input_tokens", 0) or 0
                usage["output_tokens"] += getattr(u, "output_tokens", 0) or 0
                usage["cache_read_input_tokens"] += (
                    getattr(u, "cache_read_input_tokens", 0) or 0
                )
                usage["cache_creation_input_tokens"] += (
                    getattr(u, "cache_creation_input_tokens", 0) or 0
                )

    return scores, usage, detail
