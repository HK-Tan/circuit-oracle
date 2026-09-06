"""Grader repeats and usage amortization (CPU only, no network).

grade_completion and LLMClient are monkeypatched on the saving module so no
network is touched. Covers:
  - n_repeats=1 reproduces the single-draw behavior (std 0.0),
  - n_repeats averaging (per-axis mean is the score, overall from the means,
    per-axis population std stored), usage accrues across ALL draws,
  - a None draw among the repeats fails loud,
  - the amortized_usage helper zeros counts but keeps the model key so
    compute_cost prices it at 0.0 (not None).
"""
from __future__ import annotations

import threading

import pytest

from circuit_oracle import saving


class _Cfg:
    grader_model = "openai/gpt-5.4"
    provider = "openrouter"


def _measurements():
    return [
        {"layer": 11, "feature_idx": 77560, "pos": 34, "scale": -3.0,
         "shift_bucket": "shifted", "answer_after": "On June 4 1989 the army cleared it."},
        {"layer": 14, "feature_idx": 1234, "pos": 30, "scale": 0.0,
         "shift_bucket": "no-shift", "answer_after": "I cannot help."},
    ]


def test_n_repeats_default_one_reproduces_single_draw(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setattr(saving, "LLMClient", lambda provider="anthropic": object())

    calls = []

    def fake_grade_completion(client, model, question, completion):
        calls.append(completion)
        usage = {"model": model, "input_tokens": 5, "output_tokens": 2,
                 "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
        if "June 4" in completion:
            return {"usability": 0.9, "plausibility": 0.8, "overall": 0.85}, usage
        return {"usability": 0.0, "plausibility": 0.1, "overall": 0.05}, usage

    monkeypatch.setattr(saving, "grade_completion", fake_grade_completion)

    measurements = _measurements()
    rec = saving.grade_sweep(measurements, "I cannot help.", _Cfg(),
                             question="What happened?")

    # 2 unique completions (baseline collapses with measurement[1]), graded once each.
    assert len(calls) == 2
    assert rec["n_repeats"] == 1
    assert measurements[0]["overall"] == 0.85
    assert measurements[0]["usability_std"] == 0.0
    assert measurements[0]["plausibility_std"] == 0.0
    assert measurements[0]["n_repeats"] == 1
    # usage over 2 unique x 1 draw x 5 input tokens.
    assert rec["usage"]["input_tokens"] == 10
    assert rec["baseline"]["usability_std"] == 0.0


def test_n_repeats_averages_mean_and_std(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setattr(saving, "LLMClient", lambda provider="anthropic": object())

    # For the June completion, cycle usability draws 0.8, 0.9, 1.0 (mean 0.9)
    # and plausibility 0.6, 0.8, 1.0 (mean 0.8). For the baseline, constant 0.0/0.1.
    june_cycle = [
        {"usability": 0.8, "plausibility": 0.6, "overall": 0.7},
        {"usability": 0.9, "plausibility": 0.8, "overall": 0.85},
        {"usability": 1.0, "plausibility": 1.0, "overall": 1.0},
    ]
    # Atomic cycle index: grade_sweep grades on a ThreadPoolExecutor, so a
    # non-atomic read-then-increment could serve a duplicate draw and skip
    # another, shifting the asserted mean / std. The lock makes each of the 3
    # June draws serve exactly once.
    state = {"june_i": 0}
    lock = threading.Lock()

    def fake_grade_completion(client, model, question, completion):
        usage = {"model": model, "input_tokens": 5, "output_tokens": 2,
                 "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
        if "June 4" in completion:
            with lock:
                idx = state["june_i"] % len(june_cycle)
                state["june_i"] += 1
            score = june_cycle[idx]
            return dict(score), usage
        return {"usability": 0.0, "plausibility": 0.1, "overall": 0.05}, usage

    monkeypatch.setattr(saving, "grade_completion", fake_grade_completion)

    measurements = _measurements()
    rec = saving.grade_sweep(measurements, "I cannot help.", _Cfg(),
                             question="What happened?", n_repeats=3)

    assert rec["n_repeats"] == 3
    june = measurements[0]
    # Mean usability 0.9, mean plausibility 0.8, overall (0.9+0.8)/2 = 0.85.
    assert june["usability"] == 0.9
    assert june["plausibility"] == 0.8
    assert june["overall"] == 0.85
    # Population std of {0.8,0.9,1.0} is ~0.0816.
    assert june["usability_std"] == pytest.approx(0.0816, abs=1e-3)
    assert june["plausibility_std"] == pytest.approx(0.1633, abs=1e-3)

    # Usage accrues across ALL draws: 2 unique x 3 draws x 5 input tokens = 30.
    assert rec["usage"]["input_tokens"] == 30


def test_none_draw_fails_loud(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setattr(saving, "LLMClient", lambda provider="anthropic": object())

    def fake_grade_completion(client, model, question, completion):
        usage = {"model": model, "input_tokens": 5, "output_tokens": 2,
                 "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
        # Always None -> a parse/transport failure.
        return None, usage

    monkeypatch.setattr(saving, "grade_completion", fake_grade_completion)

    with pytest.raises(RuntimeError, match="None score"):
        saving.grade_sweep(_measurements(), "I cannot help.", _Cfg(),
                           question="q", n_repeats=3)


def test_invalid_n_repeats_fails_loud(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setattr(saving, "LLMClient", lambda provider="anthropic": object())
    monkeypatch.setattr(saving, "grade_completion",
                        lambda *a, **k: ({"usability": 0.5, "plausibility": 0.5, "overall": 0.5}, {}))
    with pytest.raises(ValueError, match="n_repeats"):
        saving.grade_sweep(_measurements(), "", _Cfg(), question="q", n_repeats=0)


def test_amortized_usage_zeros_counts_keeps_model_prices_to_zero():
    real = {
        "model": "openai/gpt-5.4",
        "input_tokens": 1000,
        "output_tokens": 500,
        "cache_read_input_tokens": 200,
        "cache_creation_input_tokens": 100,
    }
    zeroed = saving.amortized_usage(real)
    assert zeroed["model"] == "openai/gpt-5.4"
    assert zeroed["input_tokens"] == 0
    assert zeroed["output_tokens"] == 0
    assert zeroed["cache_read_input_tokens"] == 0
    assert zeroed["cache_creation_input_tokens"] == 0
    # The original is not mutated.
    assert real["input_tokens"] == 1000

    # Amortization invariant: real cost + zeroed cost == real cost.
    real_cost = saving.compute_cost(real)
    zeroed_cost = saving.compute_cost(zeroed)
    assert real_cost > 0
    assert zeroed_cost == 0.0  # priced, not None (model key preserved)
    assert real_cost + zeroed_cost == pytest.approx(real_cost)
