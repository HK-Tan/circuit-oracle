"""Causal-by-default discovery annotation.

The orchestrator's get_top_features / get_upstream_features
results are post-processed by `_causal_discovery_annotate`, which ablates each
discovered feature at scale=-1, classifies the shift, and (for shifted features only)
auto-fetches inspect_feature + runs the discovery-variant reassess, annotating the
returned feature rows in place and appending an ungraded row to ctx.discovery_reassess.

Replaces the retired screen-tool tests (the screen tool is subsumed by this pass).
Runs on the tiny CPU fixture; the Neuronpedia HTTP fetch and the subagent backend are
mocked so no network is touched.
"""
from __future__ import annotations

import json

import pytest

from circuit_oracle.tools import (
    _causal_discovery_annotate,
    get_top_features,
    get_top_logits,
)


_DISCOVERY_JSON = json.dumps(
    {
        "autointerp": "Code/technical snippets",
        "post_label": "illicit-request / sensitivity detector",
        "divergence": "autointerp_only",
    }
)


def _first_token(ctx) -> str:
    logits = get_top_logits(ctx, k=5)
    assert logits, "tiny fixture should expose at least one top logit token"
    return logits[0]["token"]


def test_causal_discovery_annotates_shifted_features(monkeypatch, baseline_ctx):
    """Forcing a shift -> every feature row gets `shift`, shifted rows get the verdict,
    and ctx.discovery_reassess records one ungraded row per shifted feature."""
    # Avoid the Neuronpedia HTTP hit on the toy fixture.
    monkeypatch.setattr(
        "circuit_oracle.tools._fetch_inspect_payload",
        lambda ctx, layer, feature_idx: {
            "label": "Code/technical snippets",
            "autointerp": "Code/technical snippets",
            "top_activating_examples": [],
            "promoted_tokens": ["unsafe", "discreet"],
            "suppressed_tokens": [],
            "frac_nonzero": 0.001,
        },
    )
    # Force every measured feature to count as shifted so the reassess fans out.
    monkeypatch.setattr("circuit_oracle.tools.shift_bucket", lambda *a, **k: "shifted")

    seen_variants: list[str] = []

    def fake_backend(prompt, *, model):
        # discovery prompt must NOT carry a pre_hypothesis section
        assert "## (3) Agent's pre_hypothesis" not in prompt
        seen_variants.append(model)
        return _DISCOVERY_JSON

    baseline_ctx.subagent_client = fake_backend
    baseline_ctx.subagent_model = "configured-subagent-model"

    token = _first_token(baseline_ctx)
    feats = get_top_features(baseline_ctx, token=token, k=3)
    assert isinstance(feats, list) and feats, f"expected feature list, got {feats!r}"

    annotated = _causal_discovery_annotate(baseline_ctx, feats)
    assert annotated is feats, "annotation happens in place and returns the same list"

    for row in feats:
        assert row.get("shift") == "shifted", f"every row should be annotated shifted: {row}"
        assert row.get("divergence") == "autointerp_only"
        assert row.get("post_label") == "illicit-request / sensitivity detector"

    # One ungraded discovery_reassess row per shifted feature; pinned/win unknown at discovery.
    assert len(baseline_ctx.discovery_reassess) == len(feats)
    for r in baseline_ctx.discovery_reassess:
        assert isinstance(r["feature"], list) and len(r["feature"]) == 3
        assert r["divergence"] == "autointerp_only"
        assert r["oracle_pinned"] is None and r["became_win"] is None
    # The reassess ran on the configured subagent model.
    assert set(seen_variants) == {"configured-subagent-model"}


def test_causal_discovery_no_shift_keeps_rows_no_records(monkeypatch, baseline_ctx):
    """No shift -> rows annotated `no-shift`, no verdict fields, no discovery_reassess rows,
    and the subagent backend is never called (evidence-not-filter: rows are kept)."""
    monkeypatch.setattr("circuit_oracle.tools.shift_bucket", lambda *a, **k: "no-shift")

    called = {"n": 0}

    def fake_backend(prompt, *, model):
        called["n"] += 1
        return _DISCOVERY_JSON

    baseline_ctx.subagent_client = fake_backend
    token = _first_token(baseline_ctx)
    feats = get_top_features(baseline_ctx, token=token, k=3)

    annotated = _causal_discovery_annotate(baseline_ctx, feats)
    assert annotated is feats
    for row in feats:
        assert row.get("shift") == "no-shift"
        assert "divergence" not in row  # no verdict for unshifted rows
    assert baseline_ctx.discovery_reassess == []
    assert called["n"] == 0, "no shift -> no reassess dispatch"


def test_causal_discovery_passthrough_error_dict(baseline_ctx):
    """An error dict from the discovery tool is returned untouched (no causal pass)."""
    err = {"error": "token not found"}
    out = _causal_discovery_annotate(baseline_ctx, err)
    assert out is err
    assert baseline_ctx.discovery_reassess == []
