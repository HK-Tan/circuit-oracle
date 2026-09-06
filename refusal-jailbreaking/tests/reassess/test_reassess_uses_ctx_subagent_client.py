"""Batched_anchor_sweep reaches reinterpret_subagent
via ctx.subagent_client when the test-only _SUBAGENT_CLIENT is absent.

The production bug this pins: _dispatch_reassess submitted
reinterpret_subagent with no `client` and no `subagent_model`, and the module-global
_SUBAGENT_CLIENT is installed only by the test fixture, so every reassess in production
raised "reinterpret_subagent requires a callable client" and was caught into an
{"error": ...} record. The triple-label / divergence mechanism produced zero valid
records ever.

The fix stashes the run's LLM client + configured subagent model on ctx
(run_circuit_oracle) and threads them into reinterpret_subagent from _dispatch_reassess.
This test reproduces the production conditions (no _SUBAGENT_CLIENT installed) and asserts
that, with ctx.subagent_client set, the reassess produces a real record rather than the
missing-client error, and that ctx.subagent_model is the model passed to the backend.
"""
from __future__ import annotations

import json

import pytest

from circuit_oracle.tools import batched_anchor_sweep


_CANNED = {
    "autointerp": "stub",
    "pre_label": "stub-pre",
    "post_label": "stub-post",
    "divergence": "autointerp_only",
}


def test_reassess_uses_ctx_subagent_client_when_module_global_absent(
    monkeypatch, baseline_ctx
):
    """No _SUBAGENT_CLIENT, but ctx.subagent_client set -> real record, no missing-client error."""
    # Reproduce production: the test-only module-global backend is NOT installed.
    import circuit_oracle.subagent as _sub
    monkeypatch.setattr(_sub, "_SUBAGENT_CLIENT", None, raising=False)

    seen_models: list[str] = []

    def fake_backend(prompt, *, model):
        seen_models.append(model)
        return json.dumps(_CANNED)

    baseline_ctx.subagent_client = fake_backend
    baseline_ctx.subagent_model = "configured-subagent-model"
    baseline_ctx.pinned_features = {(0, 0, 0): "hypothesis A"}

    # Force the single pinned feature to shift so REASSESS dispatches.
    monkeypatch.setattr(
        "circuit_oracle.tools.shift_bucket",
        lambda *a, **k: "shifted",
    )

    result = batched_anchor_sweep(baseline_ctx)

    records = result["reassess_records"]
    assert len(records) == 1, f"expected one reassess record, got {records}"
    (record,) = records.values()
    assert "error" not in record, (
        "reassess returned an error record despite ctx.subagent_client being set; "
        f"the client wiring (Part A) is broken: {record}"
    )
    assert record["divergence"] == "autointerp_only"
    assert record["post_label"] == "stub-post"

    # The configured subagent model on ctx must be the one passed to the backend.
    assert seen_models == ["configured-subagent-model"], (
        f"reassess must run on ctx.subagent_model; backend saw {seen_models}"
    )


def test_reassess_errors_when_no_client_anywhere(monkeypatch, baseline_ctx):
    """With neither _SUBAGENT_CLIENT nor ctx.subagent_client, reassess yields an error record.

    This is the pre-fix production behavior, pinned as a guard: the harness must
    degrade to an error record (not crash the sweep) when no backend is reachable.
    """
    import circuit_oracle.subagent as _sub
    monkeypatch.setattr(_sub, "_SUBAGENT_CLIENT", None, raising=False)

    # ctx.subagent_client defaults to None on a fresh ToolContext.
    assert getattr(baseline_ctx, "subagent_client", None) is None
    baseline_ctx.pinned_features = {(0, 0, 0): "hypothesis A"}

    monkeypatch.setattr(
        "circuit_oracle.tools.shift_bucket",
        lambda *a, **k: "shifted",
    )

    result = batched_anchor_sweep(baseline_ctx)
    records = result["reassess_records"]
    assert len(records) == 1
    (record,) = records.values()
    assert record.get("divergence") == "error" or "error" in record, (
        f"with no backend, reassess should return an error record; got {record}"
    )
