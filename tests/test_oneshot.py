"""Arm-3 one-shot pipeline (circuit_oracle.oneshot).

The pure functions (JSON parse, intervention validation, rendering) are tested
directly. run_oneshot_oracle is tested with the three tools.* calls
monkeypatched and a fake client, so the orchestration, the mode gate, the
proposal validation, and the result shape are all exercised with no graph, no
model, and no network.
"""
from __future__ import annotations

import json
import types

import pytest

from circuit_oracle import oneshot


# ── Pure functions ───────────────────────────────────────────────────────────

def test_parse_oneshot_json_tolerates_prose():
    text = 'Sure! Here is my answer:\n{"verdict": "spurious"}\nHope that helps.'
    assert oneshot.parse_oneshot_json(text) == {"verdict": "spurious"}


def test_parse_oneshot_json_returns_none_on_garbage():
    assert oneshot.parse_oneshot_json("no json here") is None
    assert oneshot.parse_oneshot_json("{not valid}") is None
    assert oneshot.parse_oneshot_json('["a list"]') is None


def test_validate_interventions_accepts_offered_and_whitelisted():
    offered = {(24, 91636), (17, 83241)}
    proposals = [
        {"layer": 24, "feature_idx": 91636, "scale": -2, "hypothesis": "gate"},
        {"layer": 17, "feature_idx": 83241, "scale": 0},
    ]
    accepted, rejected = oneshot.validate_interventions(proposals, offered)
    assert len(accepted) == 2
    assert rejected == []
    assert accepted[0]["hypothesis"] == "gate"


def test_validate_interventions_rejects_off_menu_feature():
    offered = {(24, 91636)}
    accepted, rejected = oneshot.validate_interventions(
        [{"layer": 1, "feature_idx": 2, "scale": -1}], offered
    )
    assert accepted == []
    assert "not in the offered list" in rejected[0]["reason"]


def test_validate_interventions_rejects_bad_scale():
    offered = {(24, 91636)}
    for bad in (-5, 1, 2, 0.5, "x"):
        accepted, rejected = oneshot.validate_interventions(
            [{"layer": 24, "feature_idx": 91636, "scale": bad}], offered
        )
        assert accepted == [], bad
        assert "scale" in rejected[0]["reason"], bad


def test_validate_interventions_enforces_cap():
    offered = {(0, i) for i in range(20)}
    proposals = [{"layer": 0, "feature_idx": i, "scale": -1} for i in range(20)]
    accepted, rejected = oneshot.validate_interventions(proposals, offered, max_interventions=8)
    assert len(accepted) == 8
    assert all("over the" in r["reason"] for r in rejected)


def test_validate_interventions_non_list_is_rejected_not_crash():
    accepted, rejected = oneshot.validate_interventions("nope", {(0, 0)})
    assert accepted == []
    assert rejected and "not a list" in rejected[0]["reason"]


# ── Silent-coercion holes (codex review 2026-07-27) ──────────────────────────

def test_json_false_is_not_scale_zero():
    """bool is a subclass of int in Python, so `scale: false` would otherwise
    validate as a real zero-ablation nobody proposed."""
    offered = {(24, 91636)}
    accepted, rejected = oneshot.validate_interventions(
        [{"layer": 24, "feature_idx": 91636, "scale": False}], offered
    )
    assert accepted == []
    assert "scale" in rejected[0]["reason"]


def test_bool_layer_is_rejected():
    accepted, rejected = oneshot.validate_interventions(
        [{"layer": True, "feature_idx": 91636, "scale": -1}], {(1, 91636)}
    )
    assert accepted == []
    assert "exact integers" in rejected[0]["reason"]


def test_non_integral_float_does_not_truncate_into_the_offered_list():
    """int(12.9) == 12 would match an offered feature the model never named."""
    offered = {(12, 500)}
    accepted, rejected = oneshot.validate_interventions(
        [{"layer": 12.9, "feature_idx": 500, "scale": -1}], offered
    )
    assert accepted == []
    assert "exact integers" in rejected[0]["reason"]


def test_integral_float_is_accepted():
    """-2.0 and 12.0 are exactly integers, so they are proposals, not typos."""
    offered = {(12, 500)}
    accepted, rejected = oneshot.validate_interventions(
        [{"layer": 12.0, "feature_idx": 500.0, "scale": -2.0}], offered
    )
    assert rejected == []
    assert accepted == [{"layer": 12, "feature_idx": 500, "scale": -2, "hypothesis": ""}]


def test_saturation_scale_is_capped_at_one():
    """-4 is the escape hatch. The prompt says 'at most once'; enforce it."""
    offered = {(0, i) for i in range(5)}
    proposals = [{"layer": 0, "feature_idx": i, "scale": -4} for i in range(5)]
    accepted, rejected = oneshot.validate_interventions(proposals, offered)
    assert len(accepted) == 1
    assert len(rejected) == 4
    assert all("saturation escape hatch" in r["reason"] for r in rejected)


def test_saturation_cap_does_not_limit_workhorse_scales():
    offered = {(0, i) for i in range(5)}
    proposals = ([{"layer": 0, "feature_idx": i, "scale": -3} for i in range(4)]
                 + [{"layer": 0, "feature_idx": 4, "scale": -4}])
    accepted, rejected = oneshot.validate_interventions(proposals, offered)
    assert len(accepted) == 5
    assert rejected == []


# ── Fakes ────────────────────────────────────────────────────────────────────

class FakeCtx:
    """Only attribute the oneshot code touches is passed to tools.*, which we
    monkeypatch, so this can be empty."""


class FakeClient:
    def __init__(self, reply: str):
        self.reply = reply
        self.calls = []

    def create_message(self, *, model, system, messages, max_tokens):
        self.calls.append({"model": model, "system": system, "messages": messages})
        block = types.SimpleNamespace(text=self.reply)
        usage = types.SimpleNamespace(input_tokens=100, output_tokens=50)
        return types.SimpleNamespace(content=[block], usage=usage)


FAKE_FEATURES = [
    {"layer": 24, "feature_idx": 91636, "pos": 35, "activation": 11.9, "direct_effect": -0.42},
    {"layer": 17, "feature_idx": 83241, "pos": 35, "activation": 8.1, "direct_effect": 0.31},
]


@pytest.fixture
def patched_tools(monkeypatch):
    """Patch the three graph tools the oneshot driver calls."""
    monkeypatch.setattr(oneshot.tools, "get_top_logits",
                        lambda ctx, k: [{"token": "In", "probability": 0.9},
                                        {"token": "I", "probability": 0.07}])
    monkeypatch.setattr(oneshot.tools, "get_top_features",
                        lambda ctx, token, k: list(FAKE_FEATURES))
    monkeypatch.setattr(oneshot.tools, "inspect_feature",
                        lambda ctx, layer, feature_idx: {
                            "layer": layer, "feature_idx": feature_idx,
                            "label": f"label-{layer}-{feature_idx}"})
    executed = []
    monkeypatch.setattr(oneshot.tools, "intervene_feature",
                        lambda ctx, layer, feature_idx, scale, hypothesis=None: (
                            executed.append((layer, feature_idx, scale)) or
                            {"answer_after": "surfaced", "intervention":
                             {"type": "single", "layer": layer, "position": 35,
                              "feature_idx": feature_idx, "scale": scale}}))
    return executed


# ── End to end ───────────────────────────────────────────────────────────────

def test_probes_oneshot_records_page_and_verdict(patched_tools):
    reply = json.dumps({
        "analysis": "L24:F91636 is a negation cue",
        "verdict": "spurious",
        "spurious_features": ["L24:F91636"],
        "causal_features": [],
    })
    result = oneshot.run_oneshot_oracle(
        FakeCtx(), FakeClient(reply), "Is this spurious?",
        orchestrator_model="test/model", task="probes", mode="observational",
        verbose=False,
    )
    tools_used = [c["tool"] for c in result["tool_calls"]]
    assert tools_used.count("get_top_logits") == 1
    assert tools_used.count("get_top_features") == 1
    assert tools_used.count("inspect_feature") == 2  # one per feature
    assert "intervene_feature" not in tools_used     # observational executes nothing
    assert result["turns"] == 1
    assert result["oneshot"]["parse_ok"] is True
    assert "spurious" in result["response"]


def test_probes_oneshot_never_executes_even_if_model_proposes(patched_tools):
    reply = json.dumps({
        "analysis": "x", "verdict": "causal",
        "interventions": [{"layer": 24, "feature_idx": 91636, "scale": -2}],
    })
    result = oneshot.run_oneshot_oracle(
        FakeCtx(), FakeClient(reply), "q",
        orchestrator_model="m", task="probes", mode="observational", verbose=False,
    )
    assert patched_tools == []
    assert result["oneshot"]["n_executed"] == 0
    assert any("observational run executes nothing" in r["reason"]
               for r in result["oneshot"]["rejected"])


def test_refusal_oneshot_executes_valid_interventions(patched_tools):
    reply = json.dumps({
        "analysis": "reverse the refusal gate at L24:F91636",
        "interventions": [
            {"layer": 24, "feature_idx": 91636, "scale": -2, "hypothesis": "gate"},
            {"layer": 99, "feature_idx": 1, "scale": -1},   # off menu, rejected
        ],
    })
    result = oneshot.run_oneshot_oracle(
        FakeCtx(), FakeClient(reply), "elicit",
        orchestrator_model="m", task="refusal", mode="causal", verbose=False,
    )
    assert patched_tools == [(24, 91636, -2)]
    assert result["oneshot"]["n_executed"] == 1
    assert any("not in the offered list" in r["reason"]
               for r in result["oneshot"]["rejected"])
    interventions = [c for c in result["tool_calls"] if c["tool"] == "intervene_feature"]
    assert len(interventions) == 1
    assert interventions[0]["input"]["scale"] == -2


def test_errored_intervention_is_not_counted_as_executed(monkeypatch, patched_tools):
    """A harness-rejected intervention is skipped by _collect_interventions, so
    counting it would put a phantom intervention in the report with no saved
    record behind it."""
    monkeypatch.setattr(oneshot.tools, "intervene_feature",
                        lambda ctx, layer, feature_idx, scale, hypothesis=None: {
                            "error": "feature not active at any position"})
    reply = json.dumps({
        "analysis": "x",
        "interventions": [{"layer": 24, "feature_idx": 91636, "scale": -2}],
    })
    result = oneshot.run_oneshot_oracle(
        FakeCtx(), FakeClient(reply), "q",
        orchestrator_model="m", task="refusal", mode="causal", verbose=False,
    )
    assert result["oneshot"]["n_executed"] == 0
    assert len(result["oneshot"]["failed"]) == 1
    assert "not active" in result["oneshot"]["failed"][0]["error"]
    assert "Failed in the harness" in result["response"]
    # the attempt is still in the tool-call log, where _collect_interventions
    # will skip it on the "error" key
    assert any(c["tool"] == "intervene_feature" for c in result["tool_calls"])


def test_refusal_oneshot_parse_error_is_survivable(patched_tools):
    result = oneshot.run_oneshot_oracle(
        FakeCtx(), FakeClient("the model rambled and produced no JSON"), "q",
        orchestrator_model="m", task="refusal", mode="causal", verbose=False,
    )
    assert patched_tools == []
    assert result["oneshot"]["parse_ok"] is False
    assert "PARSE ERROR" in result["response"]
    # the evidence page is still recorded
    assert any(c["tool"] == "get_top_features" for c in result["tool_calls"])


def test_result_shape_matches_agentic_contract(patched_tools):
    reply = json.dumps({"analysis": "x", "verdict": "mixed",
                        "spurious_features": [], "causal_features": []})
    result = oneshot.run_oneshot_oracle(
        FakeCtx(), FakeClient(reply), "q",
        orchestrator_model="m", task="probes", mode="observational", verbose=False,
    )
    for key in ("response", "tool_calls", "usage", "turns"):
        assert key in result
    assert set(result["usage"]) == {"orchestrator", "subagents"}
    # subagents must be a list: save_run_results iterates it as one
    assert result["usage"]["subagents"] == []
    assert result["usage"]["orchestrator"]["output_tokens"] == 50


def test_unknown_task_raises(patched_tools):
    with pytest.raises(ValueError, match="probes.*refusal|refusal"):
        oneshot.run_oneshot_oracle(
            FakeCtx(), FakeClient("{}"), "q",
            orchestrator_model="m", task="elk", mode="observational", verbose=False,
        )
