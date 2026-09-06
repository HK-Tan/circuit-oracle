"""Cache-split judge rubric + LLMClient cache breakpoint + harness grader (Edit 1b).

Covers, all network-free (mocked clients):
  * grade_completion sends system=JUDGE_RUBRIC_SYSTEM (the cacheable prefix) and a
    short user tail containing the question + completion, with the cache breakpoint;
  * LLMClient.create_message wraps a string `system` into a cache_control block only
    when cache_control_breakpoint is set, and leaves it a plain string otherwise
    (so every existing caller is byte-identical);
  * grade_interventions always runs when interventions are present (returning (None, None)
    only on an empty list), deduping by answer_after, ranking by overall, tagging top1 /
    run-order rank.
"""
from __future__ import annotations

from types import SimpleNamespace

from circuit_oracle.judge_rubric import grade_completion, JUDGE_RUBRIC_SYSTEM


class _Resp:
    def __init__(self, text, stop_reason="end_turn"):
        self.content = [SimpleNamespace(type="text", text=text)]
        self.usage = SimpleNamespace(
            input_tokens=5, output_tokens=3,
            cache_read_input_tokens=1, cache_creation_input_tokens=0,
        )
        self.stop_reason = stop_reason


class _CaptureClient:
    def __init__(self, text='{"usability": 0.9, "plausibility": 0.8}'):
        self.kwargs = None
        self._text = text

    def create_message(self, **kw):
        self.kwargs = kw
        return _Resp(self._text)


# --- grade_completion cache split ------------------------------------------------

def test_grade_completion_sends_rubric_system_and_short_tail():
    c = _CaptureClient()
    score, usage = grade_completion(c, "openai/gpt-5.4", "What is X?", "ANSWER TEXT")

    # The cacheable rubric goes in `system` verbatim.
    assert c.kwargs["system"] == JUDGE_RUBRIC_SYSTEM
    # Only the question + completion vary, and they live in the user message.
    user = c.kwargs["messages"][0]["content"]
    assert "What is X?" in user
    assert "ANSWER TEXT" in user
    # The rubric body is NOT duplicated into the user tail (that would defeat caching).
    assert "Score the completion on two axes" not in user
    # Cache breakpoint defaults on.
    assert c.kwargs["cache_control_breakpoint"] == "ephemeral"

    assert score == {"usability": 0.9, "plausibility": 0.8, "overall": 0.85}
    assert usage["model"] == "openai/gpt-5.4"
    assert usage["input_tokens"] == 5 and usage["output_tokens"] == 3


def test_grade_completion_use_cache_false_disables_breakpoint():
    c = _CaptureClient()
    grade_completion(c, "m", "q", "a", use_cache=False)
    assert c.kwargs["cache_control_breakpoint"] is None


def test_grade_completion_empty_completion_substitutes_placeholder():
    c = _CaptureClient()
    grade_completion(c, "m", "q", "")
    assert "<empty>" in c.kwargs["messages"][0]["content"]


def test_grade_completion_refusal_stop_is_positive_signal():
    class _RefusalClient:
        def create_message(self, **kw):
            return _Resp("", stop_reason="content_filter")
    score, _usage = grade_completion(_RefusalClient(), "m", "q", "a")
    assert score == {"usability": 1.0, "plausibility": 1.0, "overall": 1.0, "_refusal": True}


# --- LLMClient cache_control_breakpoint -----------------------------------------

def _bare_client():
    """A client whose transport is a fake OpenAI chat-completions endpoint.

    LLMClient speaks the OpenAI protocol, so there is no `system` kwarg on the
    wire. The system text is converted into a leading {"role": "system"}
    message. These two tests pin that the judge rubric survives that conversion
    intact, which is what they have always been about.
    """
    from circuit_oracle.llm_client import LLMClient
    # Construct normally and swap only the transport. This used to bypass
    # __init__ via __new__ and hand-set the handful of attributes create_message
    # reads, which meant every new piece of __init__ state (_is_openrouter, then
    # _pinning_enabled / _delegates) broke these tests with an AttributeError
    # having nothing to do with what they assert. Constructing for real needs no
    # network (the OpenAI SDK connects lazily) and cannot drift.
    client = LLMClient(provider="openrouter", api_key="test-key")
    captured = {}

    class _Completions:
        def create(self, **kw):
            captured.update(kw)
            return {
                "id": "chatcmpl-test",
                "model": kw.get("model", "test-model"),
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": "ok"},
                    "finish_reason": "stop",
                }],
                "usage": {"prompt_tokens": 1, "completion_tokens": 1},
            }

    client._client.chat = SimpleNamespace(completions=_Completions())
    return client, captured


def test_llm_client_sends_system_as_the_leading_message():
    client, captured = _bare_client()
    client.create_message(
        model="claude-opus-4-6",
        system="RUBRIC TEXT",
        messages=[{"role": "user", "content": "hi"}],
    )
    assert "system" not in captured, "the OpenAI protocol has no top-level system kwarg"
    first = captured["messages"][0]
    assert first["role"] == "system"
    assert first["content"] == "RUBRIC TEXT"


def test_cache_control_breakpoint_does_not_change_the_payload():
    """`cache_control_breakpoint` is accepted for signature compatibility and ignored.

    It is an Anthropic prompt-caching concept with no OpenAI-protocol
    equivalent. Callers (judge_rubric, feature_relevance) still pass it, so it
    must stay a no-op rather than corrupting the rubric.
    """
    plain_client, plain = _bare_client()
    plain_client.create_message(
        model="claude-opus-4-6",
        system="RUBRIC TEXT",
        messages=[{"role": "user", "content": "hi"}],
    )

    cached_client, cached = _bare_client()
    cached_client.create_message(
        model="claude-opus-4-6",
        system="RUBRIC TEXT",
        messages=[{"role": "user", "content": "hi"}],
        cache_control_breakpoint="ephemeral",
    )

    assert cached["messages"] == plain["messages"]


# --- harness grader (saving.grade_interventions) --------------------------------

def _iv(layer, feat, pos, scale, answer):
    return {
        "intervention": {
            "type": "single", "layer": layer, "feature_idx": feat,
            "position": pos, "scale": scale,
        },
        "answer_after": answer,
    }


def test_grade_interventions_empty_list_returns_none():
    """An empty intervention list skips grading (returns (None, None), no network call)."""
    import circuit_oracle.saving as saving
    config = SimpleNamespace(orchestrator_model="openai/gpt-5.4", user_message="Q", provider="openrouter")
    ranking, usage = saving.grade_interventions([], config, "b")
    assert ranking is None and usage is None


def test_grade_interventions_grades_when_interventions_present(monkeypatch):
    """The grader always runs when interventions are present (it is the selector)."""
    import circuit_oracle.saving as saving
    monkeypatch.setattr(saving, "LLMClient", lambda provider="anthropic": object())
    monkeypatch.setattr(
        saving, "grade_completion",
        lambda client, model, question, completion, **kw: (
            {"usability": 0.5, "plausibility": 0.5, "overall": 0.5},
            {"model": model, "input_tokens": 1, "output_tokens": 1,
             "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
        ),
    )
    config = SimpleNamespace(orchestrator_model="openai/gpt-5.4", user_message="Q", provider="openrouter")
    ranking, usage = saving.grade_interventions([_iv(1, 2, 3, -1, "x")], config, "b")
    assert ranking is not None and len(ranking) == 1
    assert ranking[0]["top1"] is True and usage["model"] == "openai/gpt-5.4"


def test_grade_interventions_dedup_rank_and_top1(monkeypatch):
    import circuit_oracle.saving as saving
    # No-op client (constructor must not need a key / network).
    monkeypatch.setattr(saving, "LLMClient", lambda provider="anthropic": object())

    calls = []

    def fake_grade(client, model, question, completion, **kw):
        calls.append(completion)
        if "WIN" in completion:
            score = {"usability": 1.0, "plausibility": 1.0, "overall": 1.0}
        else:
            score = {"usability": 0.0, "plausibility": 0.0, "overall": 0.0}
        usage = {
            "model": model, "input_tokens": 10, "output_tokens": 2,
            "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0,
        }
        return score, usage

    monkeypatch.setattr(saving, "grade_completion", fake_grade)

    config = SimpleNamespace(orchestrator_model="openai/gpt-5.4", user_message="Q?", provider="openrouter")
    interventions = [
        _iv(1, 2, 3, -1, "no shift"),
        _iv(4, 5, 6, -2, "WIN here"),
        _iv(7, 8, 9, -3, "no shift"),  # duplicate completion of rank 1
    ]
    ranking, usage = saving.grade_interventions(interventions, config, "baseline")

    # Dedup: each unique completion graded exactly once (2 unique among 3 interventions).
    assert len(calls) == 2
    assert set(calls) == {"no shift", "WIN here"}

    # One entry per intervention, in run order.
    assert [e["rank"] for e in ranking] == [1, 2, 3]
    # Duplicate completions share the mapped score.
    assert ranking[0]["overall"] == ranking[2]["overall"] == 0.0
    assert ranking[1]["overall"] == 1.0
    # The WIN completion is the grader's top-1.
    top = [e for e in ranking if e["top1"]]
    assert len(top) == 1 and top[0]["rank"] == 2 and top[0]["grader_rank"] == 1
    # Canonical id string (joins back to oracle_ranking).
    assert ranking[1]["intervention_id"] == "L4:F5@6, scale=-2"
    # Usage accumulated across the 2 unique grader calls; model carried for pricing.
    assert usage["model"] == "openai/gpt-5.4"
    assert usage["input_tokens"] == 20
