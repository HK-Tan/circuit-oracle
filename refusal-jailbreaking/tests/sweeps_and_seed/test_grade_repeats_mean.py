"""Grade_sweep repeat averaging, independent angles (CPU, no network).

Companion to test_grade_repeats_amortization.py. This module pins down three
properties of the n_repeats averaging that the spec's decision 3 makes binding
and that the other module does not isolate:

  - overall is recomputed from the per-axis MEANS, not averaged from the
    per-draw overall field (a draw set whose per-draw overall disagrees with
    (u+p)/2 proves the recompute),
  - a multi-draw n_repeats=5 path, mean and population std over 5 asymmetric
    draws (the CLI default lives in run_sweeps.build_parser, tested separately),
  - the baseline reference row also carries per-axis std, and usage accrues over
    the baseline draws too (the baseline is one of the unique completions).

grade_completion and LLMClient are monkeypatched on the saving module, so no
network is touched.
"""
from __future__ import annotations

import statistics
import threading

import pytest

from circuit_oracle import saving


class _Cfg:
    grader_model = "openai/gpt-5.4"
    provider = "openrouter"


def _one_measurement(answer):
    return [{
        "layer": 17, "feature_idx": 83241, "pos": 33, "scale": -3.0,
        "shift_bucket": "shifted", "answer_after": answer,
    }]


def test_overall_recomputed_from_means_not_per_draw_overall(monkeypatch):
    """overall must be (mean_u + mean_p)/2, ignoring the draws' overall field.

    Each draw reports a deliberately WRONG overall (99.0). If grade_sweep echoed
    the draw overall it would surface that. The correct value is the mean of the
    two axes, here (0.6 + 0.4)/2 = 0.5.
    """
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setattr(saving, "LLMClient", lambda provider="anthropic": object())

    def fake_grade_completion(client, model, question, completion):
        usage = {"model": model, "input_tokens": 4, "output_tokens": 1,
                 "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
        if completion == "":   # the baseline reference row
            return {"usability": 0.0, "plausibility": 0.0, "overall": 0.0}, usage
        # Constant axes, but a nonsense per-draw overall that must be ignored.
        return {"usability": 0.6, "plausibility": 0.4, "overall": 99.0}, usage

    monkeypatch.setattr(saving, "grade_completion", fake_grade_completion)

    measurements = _one_measurement("topic surfaced")
    rec = saving.grade_sweep(measurements, "", _Cfg(), question="q", n_repeats=3)

    m = measurements[0]
    assert m["usability"] == 0.6
    assert m["plausibility"] == 0.4
    assert m["overall"] == 0.5     # recomputed, not 99.0
    assert m["usability_std"] == 0.0
    assert m["plausibility_std"] == 0.0
    assert rec["top1"]["overall"] == 0.5


def test_five_draws_mean_and_pstdev(monkeypatch):
    """n_repeats=5, asymmetric draw set, mean + population std."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setattr(saving, "LLMClient", lambda provider="anthropic": object())

    u_draws = [0.70, 0.80, 0.90, 1.00, 0.60]   # mean 0.80
    p_draws = [0.50, 0.55, 0.60, 0.65, 0.70]   # mean 0.60
    # grade_sweep grades on a ThreadPoolExecutor, so the read-then-increment on
    # the cycle index must be atomic. Without the lock two workers could read the
    # same index, serve a duplicate draw, and skip another, shifting the asserted
    # mean / std. The lock makes each of the 5 draws serve exactly once.
    state = {"i": 0}
    lock = threading.Lock()

    def fake_grade_completion(client, model, question, completion):
        usage = {"model": model, "input_tokens": 7, "output_tokens": 3,
                 "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
        if completion == "":
            return {"usability": 0.0, "plausibility": 0.0, "overall": 0.0}, usage
        with lock:
            i = state["i"] % 5
            state["i"] += 1
        return {"usability": u_draws[i], "plausibility": p_draws[i],
                "overall": 0.0}, usage

    monkeypatch.setattr(saving, "grade_completion", fake_grade_completion)

    measurements = _one_measurement("On June 4 1989 the army moved in.")
    rec = saving.grade_sweep(measurements, "", _Cfg(), question="q", n_repeats=5)

    m = measurements[0]
    assert rec["n_repeats"] == 5
    assert m["n_repeats"] == 5
    assert m["usability"] == round(statistics.fmean(u_draws), 2) == 0.80
    assert m["plausibility"] == round(statistics.fmean(p_draws), 2) == 0.60
    assert m["overall"] == round((0.80 + 0.60) / 2, 2) == 0.70
    assert m["usability_std"] == pytest.approx(
        round(statistics.pstdev(u_draws), 4), abs=1e-9
    )
    assert m["plausibility_std"] == pytest.approx(
        round(statistics.pstdev(p_draws), 4), abs=1e-9
    )
    # The std is strictly positive here (draws genuinely vary).
    assert m["usability_std"] > 0.0
    assert m["plausibility_std"] > 0.0


def test_baseline_row_gets_std_and_usage_accrues_over_all_completions(monkeypatch):
    """The baseline is one of the unique completions, so it gets std and is billed.

    With one measurement whose answer differs from the baseline, there are 2
    unique completions (measurement answer + baseline). At n_repeats=4 the bill
    is 2 x 4 = 8 draws. The baseline block carries per-axis std too.
    """
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setattr(saving, "LLMClient", lambda provider="anthropic": object())

    base_u = [0.10, 0.20, 0.30, 0.40]   # mean 0.25
    # Atomic cycle index (see test_default_five_draws_mean_and_pstdev): the
    # threaded grader could otherwise serve a duplicate baseline draw.
    base_state = {"i": 0}
    base_lock = threading.Lock()

    def fake_grade_completion(client, model, question, completion):
        usage = {"model": model, "input_tokens": 6, "output_tokens": 2,
                 "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
        if completion == "I cannot help with that.":
            with base_lock:
                i = base_state["i"] % 4
                base_state["i"] += 1
            return {"usability": base_u[i], "plausibility": base_u[i],
                    "overall": 0.0}, usage
        return {"usability": 0.9, "plausibility": 0.9, "overall": 0.0}, usage

    monkeypatch.setattr(saving, "grade_completion", fake_grade_completion)

    measurements = _one_measurement("Here is the answer.")
    rec = saving.grade_sweep(
        measurements, "I cannot help with that.", _Cfg(), question="q", n_repeats=4
    )

    base = rec["baseline"]
    assert base["usability"] == round(statistics.fmean(base_u), 2) == 0.25
    assert base["usability_std"] == pytest.approx(
        round(statistics.pstdev(base_u), 4), abs=1e-9
    )
    assert base["usability_std"] > 0.0
    # 2 unique completions x 4 draws x 6 input tokens = 48.
    assert rec["usage"]["input_tokens"] == 48
    assert rec["usage"]["output_tokens"] == 16
    assert rec["usage"]["model"] == "openai/gpt-5.4"


def test_n_repeats_one_leaves_std_zero(monkeypatch):
    """Single draw means std is exactly 0.0 on the measurement and baseline."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    monkeypatch.setattr(saving, "LLMClient", lambda provider="anthropic": object())
    monkeypatch.setattr(
        saving, "grade_completion",
        lambda *a, **k: (
            {"usability": 0.5, "plausibility": 0.7, "overall": 0.0},
            {"model": "openai/gpt-5.4", "input_tokens": 1, "output_tokens": 1,
             "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
        ),
    )
    measurements = _one_measurement("ans")
    rec = saving.grade_sweep(measurements, "base", _Cfg(), question="q", n_repeats=1)
    assert measurements[0]["overall"] == 0.6   # (0.5 + 0.7)/2
    assert measurements[0]["usability_std"] == 0.0
    assert measurements[0]["plausibility_std"] == 0.0
    assert rec["baseline"]["usability_std"] == 0.0


# --- grader gateway routing -----------------------------------------------------


class _KiloCfg:
    """A --provider kilo sweep. gpt-5.4 is unpinned, so its grader calls really
    do go to Kilo."""
    grader_model = "openai/gpt-5.4"
    provider = "kilo"


def _stub_grading(monkeypatch):
    monkeypatch.setattr(saving, "LLMClient", lambda provider="openrouter": object())
    monkeypatch.setattr(
        saving, "grade_completion",
        lambda client, model, question, completion: (
            {"usability": 0.5, "plausibility": 0.5, "overall": 0.5},
            {"model": model, "input_tokens": 1, "output_tokens": 1,
             "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
        ),
    )


def test_kilo_run_is_not_blocked_by_a_missing_openrouter_key(monkeypatch):
    """The preflight must check the gateway the grader is ROUTED to, not a
    hardcoded OPENROUTER_API_KEY. This used to raise on a correctly credentialed
    Kilo-only run, and (worse) let an OpenRouter-only run through to 401 against
    Kilo, because the check named one gateway and the client built another."""
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("KILO_API_KEY", "dummy")
    _stub_grading(monkeypatch)
    rec = saving.grade_sweep(_one_measurement("x"), "", _KiloCfg(), question="q",
                             n_repeats=1)
    assert rec["top1"]["overall"] == 0.5


def test_missing_key_for_the_routed_gateway_still_fails_loud(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("KILO_API_KEY", raising=False)
    monkeypatch.delenv("KILOCODE_API_KEY", raising=False)
    _stub_grading(monkeypatch)
    with pytest.raises(RuntimeError, match="KILO_API_KEY"):
        saving.grade_sweep(_one_measurement("x"), "", _KiloCfg(), question="q",
                           n_repeats=1)
