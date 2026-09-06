"""Feature_relevance fetch + LLM dual-axis relevance scorer (CPU, no net).

Covers circuit_oracle.feature_relevance, the Neuronpedia batch fetch plus the
per-feature relevance fan-out used by the multi-stage seed sweep before pinning.
No network and no model: tools._fetch_inspect_payload is monkeypatched to return
canned payloads (so fetch_payloads never hits Neuronpedia), and the LLMClient is
a capture stub returning canned JSON replies (so score_relevance never hits an
API).

Plan coverage ("Verification" and the feature_relevance design):
- fetch_payloads dedups by (layer, feature_idx), writes ctx.inspect_cache under
  (layer, feature_idx, pos) for every pos seen, and fails loud on an error payload.
- score_relevance fans out ONE call per distinct feature (not a batched judge),
  parses the two axis scores, clamps each to [0, 1], combines them as
  relevance = max(topic, mechanism) WITHOUT telling the model, retries logical
  failures per feature, and fails loud after the retry budget.
"""

from __future__ import annotations

import re
from types import SimpleNamespace

import pytest

from circuit_oracle import feature_relevance as fr
from circuit_oracle import tools as ct_tools


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
class _Ctx:
    """Minimal ToolContext stand-in carrying only what fetch_payloads reads."""

    def __init__(self):
        self.neuronpedia_model_id = "qwen3-4b"
        self.neuronpedia_sae_id = "{layer}-transcoder-hp"
        self.inspect_cache: dict = {}


def _payload(autointerp="topic feature", frac_nonzero=0.01, max_token="square"):
    """A canned inspect payload mirroring tools._fetch_inspect_payload's shape."""
    return {
        "label": autointerp,
        "autointerp": autointerp,
        "top_activating_examples": [
            {"text_snippet": "Tiananmen square 1989", "max_activation": 3.2,
             "max_token": max_token},
            {"text_snippet": "the square was cleared", "max_activation": 2.1,
             "max_token": "cleared"},
        ],
        "promoted_tokens": ["square", "massacre"],
        "suppressed_tokens": ["sorry"],
        "frac_nonzero": frac_nonzero,
    }


class _FanoutClient:
    """Stand-in for LLMClient.create_message, one canned reply per feature.

    ``replies`` is either a single string (returned for every call) or a list of
    strings consumed in call order (for retry tests), or a dict mapping
    feature_idx (parsed back out of the user content's Feature JSON) to the
    canned reply text (for fan-out tests).
    """

    def __init__(self, replies, stop_reason=None):
        self._replies = replies
        self._stop_reason = stop_reason
        self.calls: list[dict] = []

    def _text_for(self, kw) -> str:
        if isinstance(self._replies, str):
            return self._replies
        if isinstance(self._replies, list):
            return self._replies[min(len(self.calls) - 1, len(self._replies) - 1)]
        content = kw["messages"][0]["content"]
        m = re.search(r'"feature_idx":\s*(\d+)', content)
        assert m, f"no feature_idx in user content: {content[:200]!r}"
        return self._replies[int(m.group(1))]

    def create_message(self, **kw):
        self.calls.append(kw)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=self._text_for(kw))],
            stop_reason=self._stop_reason,
            usage=SimpleNamespace(
                input_tokens=42, output_tokens=8,
                cache_read_input_tokens=0, cache_creation_input_tokens=0,
            ),
        )


# --------------------------------------------------------------------------- #
# fetch_payloads
# --------------------------------------------------------------------------- #
def test_fetch_payloads_dedups_by_layer_feature(monkeypatch):
    ctx = _Ctx()
    calls: list[tuple[int, int]] = []

    def fake_fetch(c, layer, feature_idx):
        calls.append((layer, feature_idx))
        return _payload(autointerp=f"L{layer}F{feature_idx}")

    monkeypatch.setattr(ct_tools, "_fetch_inspect_payload", fake_fetch)

    # The same (layer, feature_idx) appears at two positions, plus one other pair.
    pairs = [(11, 77560, 34), (11, 77560, 30), (14, 1234, 30)]
    payloads = fr.fetch_payloads(ctx, pairs)

    # Two distinct (layer, feature_idx) pairs, fetched exactly once each.
    assert sorted(calls) == [(11, 77560), (14, 1234)]
    assert set(payloads.keys()) == {(11, 77560), (14, 1234)}


def test_fetch_payloads_writes_cache_per_position(monkeypatch):
    ctx = _Ctx()
    monkeypatch.setattr(ct_tools, "_fetch_inspect_payload",
                        lambda c, l, f: _payload())

    pairs = [(11, 77560, 34), (11, 77560, 30), (14, 1234, 30)]
    fr.fetch_payloads(ctx, pairs)

    # The cache is keyed by (layer, feature_idx, pos) for EVERY position seen.
    assert (11, 77560, 34) in ctx.inspect_cache
    assert (11, 77560, 30) in ctx.inspect_cache
    assert (14, 1234, 30) in ctx.inspect_cache
    # Both positions of the shared pair point at the same payload object.
    assert ctx.inspect_cache[(11, 77560, 34)] is ctx.inspect_cache[(11, 77560, 30)]


def test_fetch_payloads_empty_pairs_returns_empty(monkeypatch):
    ctx = _Ctx()
    monkeypatch.setattr(ct_tools, "_fetch_inspect_payload",
                        lambda c, l, f: _payload())
    assert fr.fetch_payloads(ctx, []) == {}
    assert ctx.inspect_cache == {}


def test_fetch_payloads_fails_loud_on_error_payload(monkeypatch):
    ctx = _Ctx()

    def fake_fetch(c, layer, feature_idx):
        if (layer, feature_idx) == (11, 77560):
            return {"error": "Neuronpedia API error: 404 not found"}
        return _payload()

    monkeypatch.setattr(ct_tools, "_fetch_inspect_payload", fake_fetch)

    with pytest.raises(RuntimeError, match=r"L11:F77560"):
        fr.fetch_payloads(ctx, [(11, 77560, 34), (14, 1234, 30)])


# --------------------------------------------------------------------------- #
# score_relevance
# --------------------------------------------------------------------------- #
def _two_candidates():
    a = SimpleNamespace(layer=17, feature_idx=83241)
    b = SimpleNamespace(layer=14, feature_idx=1234)
    payloads = {
        (17, 83241): _payload(autointerp="code snippets", max_token="cannot"),
        (14, 1234): _payload(autointerp="topic feature", max_token="square"),
    }
    return [a, b], payloads


def test_score_relevance_fans_out_one_call_per_feature_and_maxes():
    cands, payloads = _two_candidates()
    # The refusal-gate shape (topic-generic, mechanism-specific) and the
    # topic-feature shape (topic-specific, mechanism-silent).
    client = _FanoutClient({
        83241: '{"topic_relevance": 0.1, "mechanism_relevance": 0.9}',
        1234: '{"topic_relevance": 0.8, "mechanism_relevance": 0.0}',
    })

    scores, usage, detail = fr.score_relevance(
        client, "openai/gpt-5.4",
        user_message="What happened at Tiananmen in 1989?",
        candidates=cands, payloads=payloads,
    )

    # Exactly one call PER feature (a fan-out, not one batched judge call).
    assert len(client.calls) == 2
    # relevance = max(topic, mechanism), computed harness-side.
    assert scores[(17, 83241)] == pytest.approx(0.9)
    assert scores[(14, 1234)] == pytest.approx(0.8)
    # The detail record carries both axes for the run artifacts.
    assert detail[(17, 83241)] == {
        "topic_relevance": 0.1, "mechanism_relevance": 0.9, "relevance": 0.9,
    }
    assert detail[(14, 1234)]["topic_relevance"] == pytest.approx(0.8)
    # Usage accumulates across every per-feature call.
    assert usage["model"] == "openai/gpt-5.4"
    assert usage["input_tokens"] == 84 and usage["output_tokens"] == 16
    # The model is asked for both axes but never told about the max combination.
    for kw in client.calls:
        assert "topic_relevance" in kw["system"]
        assert "mechanism_relevance" in kw["system"]
        assert "max" not in kw["system"].lower()
        assert "max(" not in kw["messages"][0]["content"]


def test_score_relevance_dedups_duplicate_pairs():
    # The same (layer, feature_idx) at two positions is scored exactly once.
    a = SimpleNamespace(layer=11, feature_idx=77560)
    b = SimpleNamespace(layer=11, feature_idx=77560)
    payloads = {(11, 77560): _payload()}
    client = _FanoutClient('{"topic_relevance": 0.6, "mechanism_relevance": 0.2}')

    scores, _usage, _detail = fr.score_relevance(
        client, "openai/gpt-5.4",
        user_message="q", candidates=[a, b], payloads=payloads,
    )
    assert len(client.calls) == 1
    assert scores[(11, 77560)] == pytest.approx(0.6)


def test_score_relevance_parses_fenced_json_and_clamps_per_axis():
    cands, payloads = _two_candidates()
    # Out-of-range values must clamp into [0, 1] per axis. Reply is fenced.
    client = _FanoutClient(
        "Here are the scores:\n```json\n"
        '{"topic_relevance": -0.5, "mechanism_relevance": 1.7}\n```'
    )
    scores, _usage, detail = fr.score_relevance(
        client, "openai/gpt-5.4",
        user_message="q", candidates=cands, payloads=payloads,
    )
    for pair in ((17, 83241), (14, 1234)):
        assert detail[pair]["topic_relevance"] == 0.0
        assert detail[pair]["mechanism_relevance"] == 1.0
        assert scores[pair] == 1.0


def test_score_relevance_retry_then_succeed():
    a = SimpleNamespace(layer=17, feature_idx=83241)
    payloads = {(17, 83241): _payload()}
    # First reply is prose (logical failure), second is valid. The per-feature
    # retry recovers without raising.
    client = _FanoutClient([
        "I refuse to return JSON, here is prose instead.",
        '{"topic_relevance": 0.0, "mechanism_relevance": 0.9}',
    ])
    scores, usage, _detail = fr.score_relevance(
        client, "openai/gpt-5.4",
        user_message="q", candidates=[a], payloads=payloads,
    )
    assert len(client.calls) == 2
    assert scores[(17, 83241)] == pytest.approx(0.9)
    # Both attempts bill: usage accumulates across retries too.
    assert usage["input_tokens"] == 84


def test_score_relevance_fails_loud_after_retry_budget():
    a = SimpleNamespace(layer=17, feature_idx=83241)
    payloads = {(17, 83241): _payload()}
    client = _FanoutClient("I refuse to return JSON, here is prose instead.")
    with pytest.raises(ValueError, match=r"L17:F83241.*after 3 attempts"):
        fr.score_relevance(
            client, "openai/gpt-5.4",
            user_message="q", candidates=[a], payloads=payloads,
        )
    assert len(client.calls) == 3


def test_score_relevance_fails_loud_on_missing_axis():
    a = SimpleNamespace(layer=17, feature_idx=83241)
    payloads = {(17, 83241): _payload()}
    client = _FanoutClient('{"topic_relevance": 0.5}')
    with pytest.raises(ValueError, match=r"mechanism_relevance"):
        fr.score_relevance(
            client, "openai/gpt-5.4",
            user_message="q", candidates=[a], payloads=payloads,
        )


def test_score_relevance_fails_loud_on_empty_response():
    a = SimpleNamespace(layer=17, feature_idx=83241)
    payloads = {(17, 83241): _payload()}
    client = _FanoutClient("")
    with pytest.raises(ValueError, match=r"empty relevance response"):
        fr.score_relevance(
            client, "openai/gpt-5.4",
            user_message="q", candidates=[a], payloads=payloads,
        )
    assert len(client.calls) == 3


def test_score_relevance_safety_block_fails_fast_without_retries():
    # An empty reply with a refusal stop reason is a deterministic provider
    # block. It must raise immediately (1 call, no retry burn) and must NOT
    # produce any placeholder score.
    a = SimpleNamespace(layer=17, feature_idx=83241)
    payloads = {(17, 83241): _payload()}
    client = _FanoutClient("", stop_reason="content_filter")
    with pytest.raises(fr.RelevanceScoringBlocked, match=r"L17:F83241.*safety filter"):
        fr.score_relevance(
            client, "openai/gpt-5.4",
            user_message="q", candidates=[a], payloads=payloads,
        )
    assert len(client.calls) == 1


def test_score_relevance_max_tokens_truncation_fails_fast():
    # A reasoning model that burns the whole max_tokens budget before any text
    # also reproduces deterministically, so no retries either.
    a = SimpleNamespace(layer=17, feature_idx=83241)
    payloads = {(17, 83241): _payload()}
    client = _FanoutClient("", stop_reason="max_tokens")
    with pytest.raises(fr.RelevanceScoringBlocked, match=r"max_tokens before any text"):
        fr.score_relevance(
            client, "openai/gpt-5.4",
            user_message="q", candidates=[a], payloads=payloads,
        )
    assert len(client.calls) == 1


def test_parse_dual_scores_tolerates_prose_with_stray_braces():
    # Prose braces around the object must not break extraction (the naive
    # first-{ to last-} slice would capture the prose braces and fail).
    topic, mechanism = fr._parse_dual_scores(
        'Result {below}: {"topic_relevance": 0.9, "mechanism_relevance": 0.3} '
        "(clamped {x})"
    )
    assert topic == pytest.approx(0.9)
    assert mechanism == pytest.approx(0.3)


def test_score_relevance_fails_loud_on_missing_payload():
    cands, payloads = _two_candidates()
    payloads.pop((14, 1234))  # drop one candidate's payload
    client = _FanoutClient('{"topic_relevance": 0.5, "mechanism_relevance": 0.5}')
    with pytest.raises(KeyError, match=r"L14:F1234"):
        fr.score_relevance(
            client, "openai/gpt-5.4",
            user_message="q", candidates=cands, payloads=payloads,
        )


def test_score_relevance_empty_candidates_no_calls():
    client = _FanoutClient('{"topic_relevance": 0.5, "mechanism_relevance": 0.5}')
    scores, usage, detail = fr.score_relevance(
        client, "openai/gpt-5.4",
        user_message="q", candidates=[], payloads={},
    )
    assert scores == {} and detail == {}
    assert client.calls == []
    assert usage["input_tokens"] == 0
