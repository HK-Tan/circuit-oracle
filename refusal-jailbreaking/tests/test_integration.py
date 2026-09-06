"""End-to-end smoke on tiny fixture.

The full pipeline runs SCOUT -> DISPATCH -> MERGE -> BUILD -> pin_features
-> batched_anchor_sweep (with auto-REASSESS fan-out) -> >=2x
batched_supernode_sweep -> ANALYZE on the tiny toy fixture, with all LLM
calls (orchestrator + reinterpret_subagent) mocked.

Verification:
  - oracle_result.json contains a `reassess_records` entry for every
    shifted feature
  - `pinned_features` section matches `build_features` exactly (strict
    coverage from pin_features)
  - at least 2 batched_supernode_sweep rounds recorded

It imports `run_oracle_pipeline`, the wired-up entry point, and drives it
with a mock orchestrator transcript shaped like the well-formed one in
`tests/guards_and_prompt/test_orchestrator_mocked_e2e_no_guards.py`.

Two test-pattern rules apply here:
  - `feature_intervention*` are methods on ReplacementModel, not module
    functions. The pipeline must use bound methods on
    `ctx.replacement_model`.
  - `shift_bucket` is monkeypatched, not stubbed via ctx attributes.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest


CANNED_TRIPLE_LABEL = {
    "autointerp": "stub-autointerp",
    "pre_label": "stub-pre-label",
    "post_label": "stub-post-label",
    "divergence": "autointerp_only",
}


def _mock_orchestrator_transcript(build_features, supernode_tuples):
    """A minimal well-formed transcript the orchestrator emits when driven
    through one canonical pass on the tiny fixture.

    `build_features` is the list of (layer, feature_idx, pos) tuples the
    BUILD step nominates; `pin_features` must cover this set exactly.
    """
    pre_hypotheses = {
        f"({l}, {f}, {p})": f"toy hypothesis for L{l}:F{f}@p{p}"
        for (l, f, p) in build_features
    }
    return [
        {
            "tool": "build_circuit",
            "input": {
                "nodes": [
                    {
                        "label": "Toy suppression circuit",
                        "features": [
                            {"layer": l, "feature_idx": f, "pos": p}
                            for (l, f, p) in build_features
                        ],
                    }
                ]
            },
            "output": {"ok": True},
        },
        {
            "tool": "pin_features",
            "input": {"pre_hypotheses": pre_hypotheses},
            "output": {"ok": True},
        },
        {
            "tool": "batched_anchor_sweep",
            "input": {},
            "output": {"measurements": [], "reassess_records": {}},
        },
        {
            "tool": "batched_supernode_sweep",
            "input": {"tuples": supernode_tuples},
            "output": {"measurements": []},
        },
        {
            "tool": "batched_supernode_sweep",
            "input": {"tuples": supernode_tuples},
            "output": {"measurements": []},
        },
    ]


def test_integration_tiny_fixture_full_pipeline(
    monkeypatch, baseline_ctx, mock_subagent_client, tmp_path
):
    """End-to-end run on tiny fixture must produce the expected artifacts.

    Fails with ImportError if `run_oracle_pipeline` is missing. That is the
    orchestrator entry point exercising the pin_features ->
    batched_anchor_sweep -> batched_supernode_sweep chain.
    """
    from circuit_oracle.pipeline import run_oracle_pipeline  # noqa: F401

    # Force every feature to shift so REASSESS dispatches once per feature.
    monkeypatch.setattr(
        "circuit_oracle.tools.shift_bucket",
        lambda *a, **k: "shifted",
    )
    mock_subagent_client.set_response(CANNED_TRIPLE_LABEL)

    # Three pinned features form a small but realistic BUILD output.
    build_features = [(0, 1, 3), (1, 2, 4), (1, 5, 4)]
    supernode_tuples = [
        {
            "features": [{"layer": l, "feature_idx": f, "pos": p, "value": -10.0}],
            "rationale": f"singleton tuple for L{l}:F{f}",
        }
        for (l, f, p) in build_features
    ] + [
        {
            "features": [
                {"layer": l, "feature_idx": f, "pos": p, "value": -10.0}
                for (l, f, p) in build_features
            ],
            "rationale": "cross-route union of all three pinned features",
        },
    ]
    transcript = _mock_orchestrator_transcript(build_features, supernode_tuples)

    out_dir = tmp_path / "run-output"
    out_dir.mkdir()

    run_oracle_pipeline(
        ctx=baseline_ctx,
        mock_transcript=transcript,
        subagent_client=mock_subagent_client,
        output_dir=out_dir,
    )

    result_path = out_dir / "oracle_result.json"
    assert result_path.exists(), (
        f"Pipeline did not write {result_path}. "
        "the pipeline must call save_oracle_result at the end of ANALYZE."
    )
    blob = json.loads(result_path.read_text())

    # 1. reassess_records keyed by every shifted feature.
    assert "reassess_records" in blob, (
        f"oracle_result.json missing 'reassess_records'; "
        f"top-level keys = {list(blob)}"
    )

    def _normalize(key):
        if isinstance(key, str):
            parts = key.replace("(", "").replace(")", "").split(",")
            return tuple(int(p.strip()) for p in parts[:3])
        return tuple(key)

    record_keys = {_normalize(k) for k in blob["reassess_records"]}
    assert record_keys == set(build_features), (
        f"reassess_records keys {sorted(record_keys)} != "
        f"shifted features (all build_features under monkeypatched "
        f"'shifted') {sorted(build_features)}"
    )

    # 2. pinned_features section matches build_features exactly.
    assert "pinned_features" in blob, (
        f"oracle_result.json missing 'pinned_features'; "
        f"top-level keys = {list(blob)}"
    )
    pinned_keys = {_normalize(k) for k in blob["pinned_features"]}
    assert pinned_keys == set(build_features), (
        f"pinned_features {sorted(pinned_keys)} must match build_features "
        f"{sorted(build_features)} exactly (strict pin_features coverage)."
    )

    # 3. At least 2 supernode rounds recorded.
    supernode_rounds = blob.get("supernode_rounds")
    assert supernode_rounds is not None, (
        "oracle_result.json missing 'supernode_rounds' summary."
    )
    assert len(supernode_rounds) >= 2, (
        f"Pipeline must execute >=2 batched_supernode_sweep rounds; "
        f"got {len(supernode_rounds)}."
    )
