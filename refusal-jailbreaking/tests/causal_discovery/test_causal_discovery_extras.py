"""Extra guards surfaced by the validation workflow.

Covers spec points that previously had no automated coverage:
- #4 / B8: orchestrator-only scoping. execute_tool with the default causal_discovery=False
  (the subagent loop's value) must NOT run the causal pass (no per-hop 800-token ablation);
  with causal_discovery=True (the orchestrator loop) it must.
- #5 / B1: both discovery tools are wired through the causal pass, and embedding rows
  (type=="embedding", emitted by get_upstream_features) are skipped by the annotate pass.
- #10 / B2,#6: the discovery batched decode uses answer_max_tokens=800 (uniform with committed).
- #2 / B4: the discovery auto-fetch caches inspect_feature under the pos-agnostic
  (layer, feature_idx, None) key the oracle's later manual inspect_feature hits.
- #8 / B5: the run's system_prompt (stashed on ctx) reaches the discovery reassess prompt.

Tiny CPU fixture; Neuronpedia HTTP and the subagent backend are mocked, no network.
"""
from __future__ import annotations

import json

import pytest

import circuit_oracle.subagent as subagent
import circuit_oracle.tools as tools
from circuit_oracle.subagent import execute_tool
from circuit_oracle.tools import _causal_discovery_annotate, get_top_features, get_top_logits


_DISCOVERY_JSON = json.dumps({
    "autointerp": "Code/technical snippets",
    "post_label": "illicit-request / sensitivity detector",
    "divergence": "autointerp_only",
})


def _first_token(ctx) -> str:
    logits = get_top_logits(ctx, k=5)
    assert logits, "tiny fixture should expose at least one top logit token"
    return logits[0]["token"]


def _stub_inspect(monkeypatch):
    monkeypatch.setattr(
        "circuit_oracle.tools._fetch_inspect_payload",
        lambda ctx, layer, feature_idx: {
            "label": "Code/technical snippets",
            "autointerp": "Code/technical snippets",
            "top_activating_examples": [],
            "promoted_tokens": ["unsafe"],
            "suppressed_tokens": [],
            "frac_nonzero": 0.001,
        },
    )


# --- #4: orchestrator-only scoping via execute_tool's causal_discovery flag ----

def test_execute_tool_subagent_path_skips_causal_pass(monkeypatch, baseline_ctx):
    """Default causal_discovery=False (subagent loop) leaves rows unannotated and
    discovery_reassess empty - the cost-safety property (no per-hop 800-token ablation)."""
    calls = {"n": 0}

    def spy(ctx, result, **kw):
        calls["n"] += 1
        return result

    monkeypatch.setattr(subagent, "_causal_discovery_annotate", spy)

    token = _first_token(baseline_ctx)
    rows = execute_tool(baseline_ctx, "get_top_features", {"token": token, "k": 3})  # default False
    assert calls["n"] == 0, "subagent-path discovery must NOT trigger the causal pass"
    assert isinstance(rows, list) and rows
    for r in rows:
        assert "shift" not in r
    assert baseline_ctx.discovery_reassess == []


def test_execute_tool_orchestrator_path_runs_causal_pass(monkeypatch, baseline_ctx):
    """causal_discovery=True (orchestrator loop) runs the annotate pass on get_top_features."""
    calls = {"n": 0}
    real = tools._causal_discovery_annotate

    def spy(ctx, result, **kw):
        calls["n"] += 1
        return real(ctx, result, **kw)

    monkeypatch.setattr(subagent, "_causal_discovery_annotate", spy)
    monkeypatch.setattr("circuit_oracle.tools.shift_bucket", lambda *a, **k: "no-shift")

    token = _first_token(baseline_ctx)
    rows = execute_tool(baseline_ctx, "get_top_features", {"token": token, "k": 3}, causal_discovery=True)
    assert calls["n"] == 1, "orchestrator-path discovery MUST trigger the causal pass"
    for r in rows:
        assert r.get("shift") == "no-shift"


def test_execute_tool_wires_upstream_features_through_causal_pass(monkeypatch, baseline_ctx):
    """B1 scope=BOTH: get_upstream_features results also flow through the causal pass.

    get_upstream_features is stubbed (the toy graph need not support real upstream tracing)
    so the test isolates the dispatch wiring, not the tool internals."""
    canned = [{"layer": 0, "feature_idx": 0, "pos": 0, "activation": 1.0,
               "direct_effect": 0.5, "type": "feature"}]
    monkeypatch.setattr(subagent, "get_upstream_features", lambda ctx, **kw: list(canned))
    seen = {"res": None}

    def spy(ctx, result, **kw):
        seen["res"] = result
        return result

    monkeypatch.setattr(subagent, "_causal_discovery_annotate", spy)
    execute_tool(baseline_ctx, "get_upstream_features",
                 {"layer": 0, "feature_idx": 0, "pos": 0, "k": 5}, causal_discovery=True)
    assert seen["res"] == canned, "get_upstream_features result must flow through the causal pass"


# --- #5: embedding rows are skipped by the annotate pass -----------------------

def test_causal_discovery_skips_embedding_rows(monkeypatch, baseline_ctx):
    """An embedding row (type=='embedding', as get_upstream_features appends) is never
    ablated/annotated, and contributes no discovery_reassess record."""
    _stub_inspect(monkeypatch)
    monkeypatch.setattr("circuit_oracle.tools.shift_bucket", lambda *a, **k: "shifted")
    baseline_ctx.subagent_client = lambda prompt, *, model: _DISCOVERY_JSON

    token = _first_token(baseline_ctx)
    feats = get_top_features(baseline_ctx, token=token, k=2)
    n_feats = len(feats)
    embed_row = {"type": "embedding", "token": "hello", "pos": 0, "direct_effect": 0.42}
    result = feats + [embed_row]

    _causal_discovery_annotate(baseline_ctx, result)

    assert "shift" not in embed_row, "embedding rows must not be annotated/ablated"
    assert "divergence" not in embed_row
    # one discovery_reassess row per FEATURE (embedding excluded)
    assert len(baseline_ctx.discovery_reassess) == n_feats


# --- #10: uniform 800-token discovery decode -----------------------------------

def test_discovery_decode_uses_800_tokens(monkeypatch, baseline_ctx):
    seen = []
    real = tools._batched_greedy_decode

    def spy(ctx, interventions_per_row, *, answer_max_tokens):
        seen.append(answer_max_tokens)
        return real(ctx, interventions_per_row, answer_max_tokens=answer_max_tokens)

    monkeypatch.setattr(tools, "_batched_greedy_decode", spy)
    monkeypatch.setattr("circuit_oracle.tools.shift_bucket", lambda *a, **k: "no-shift")

    token = _first_token(baseline_ctx)
    feats = get_top_features(baseline_ctx, token=token, k=2)
    _causal_discovery_annotate(baseline_ctx, feats)
    assert seen == [800], f"discovery decode must use answer_max_tokens=800; saw {seen}"


# --- #2: pos-agnostic inspect auto-fetch (B4 cache-hit) ------------------------

def test_discovery_autofetch_caches_pos_agnostic_key(monkeypatch, baseline_ctx):
    """The shifted-feature auto-fetch caches under (layer, feature_idx, None), the same
    key the oracle's later manual inspect_feature (schema has no pos) hits."""
    _stub_inspect(monkeypatch)
    monkeypatch.setattr("circuit_oracle.tools.shift_bucket", lambda *a, **k: "shifted")
    baseline_ctx.subagent_client = lambda prompt, *, model: _DISCOVERY_JSON

    token = _first_token(baseline_ctx)
    feats = get_top_features(baseline_ctx, token=token, k=1)
    assert feats
    layer, fidx = int(feats[0]["layer"]), int(feats[0]["feature_idx"])

    _causal_discovery_annotate(baseline_ctx, feats)
    assert (layer, fidx, None) in baseline_ctx.inspect_cache, (
        "discovery auto-fetch must cache the pos-agnostic key the oracle's manual inspect hits"
    )


# --- #8: ctx.system_prompt threaded into the discovery reassess prompt ---------

def test_discovery_reassess_prompt_carries_ctx_system_prompt(monkeypatch, baseline_ctx):
    _stub_inspect(monkeypatch)
    monkeypatch.setattr("circuit_oracle.tools.shift_bucket", lambda *a, **k: "shifted")
    captured = {}

    def fake_backend(prompt, *, model):
        captured["prompt"] = prompt
        return _DISCOVERY_JSON

    baseline_ctx.subagent_client = fake_backend
    baseline_ctx.system_prompt = "SECRET-SYSTEM-PROMPT-MARKER"

    token = _first_token(baseline_ctx)
    feats = get_top_features(baseline_ctx, token=token, k=1)
    assert feats
    _causal_discovery_annotate(baseline_ctx, feats)
    assert "SECRET-SYSTEM-PROMPT-MARKER" in captured.get("prompt", ""), (
        "the run's system_prompt (stashed on ctx) must reach the discovery reassess prompt"
    )
