"""Reassess_records persisted into oracle_result.json.

After batched_anchor_sweep with auto-REASSESS fan-out, oracle_result.json
written by the saving module must contain a `reassess_records` top-level key
keyed by stringified (layer, feature_idx, pos) tuples (or a JSON-safe encoded
form), one entry per shifted feature.

Test-pattern rule: tests MUST use monkeypatch.setattr on
shift_bucket. The previous `ctx._test_*` attribute pattern is forbidden
because it would require production code to know about test seams.

Fails if saving.py stops carrying reassess records through.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from circuit_oracle.tools import batched_anchor_sweep  # noqa: F401
from circuit_oracle.saving import save_oracle_result  # noqa: F401


CANNED_RECORD = {
    "autointerp": "stub",
    "pre_label": "stub-pre",
    "post_label": "stub-post",
    "divergence": "autointerp_only",
}


def _shift_bucket_by_feature_index(shifted_feature_indices, n_scales=4):
    """Same pattern as test_reassess_auto_dispatched_per_shifted.py."""
    state = {"call_count": 0}
    shifted = set(shifted_feature_indices)

    def fake(*args, **kwargs):
        idx = state["call_count"] // n_scales
        state["call_count"] += 1
        return "shifted" if idx in shifted else "no-shift"

    return fake


def test_oracle_result_contains_reassess_records(
    monkeypatch, baseline_ctx, mock_subagent_client, tmp_path
):
    """oracle_result.json must contain a reassess_records section with all shifted features."""
    mock_subagent_client.set_response(CANNED_RECORD)

    pinned = {
        (0, 0, 0): "hypothesis A",
        (0, 1, 0): "hypothesis B",
        (0, 2, 0): "hypothesis C",
        (0, 3, 0): "hypothesis D",
    }
    # Features at indices 0, 2, 3 are shifted; index 1 is no-shift.
    shifted_keys = [(0, 0, 0), (0, 2, 0), (0, 3, 0)]
    baseline_ctx.pinned_features = pinned

    monkeypatch.setattr(
        "circuit_oracle.tools.shift_bucket",
        _shift_bucket_by_feature_index({0, 2, 3}),
    )

    batched_anchor_sweep(baseline_ctx)

    # Saving step writes oracle_result.json into the tmp_path output dir.
    out_dir = tmp_path / "run-output"
    out_dir.mkdir()
    save_oracle_result(ctx=baseline_ctx, output_dir=out_dir)

    result_path = out_dir / "oracle_result.json"
    assert result_path.exists(), (
        f"save_oracle_result did not write {result_path}. "
        "saving.py must persist the run state."
    )

    blob = json.loads(result_path.read_text())
    assert "reassess_records" in blob, (
        f"oracle_result.json missing 'reassess_records' key; got top-level keys {list(blob)}"
    )

    records = blob["reassess_records"]
    # records keyed by stringified tuples or any reversible encoding; we check
    # coverage by parsing each key back to (layer, feature_idx, pos).
    assert len(records) == len(shifted_keys), (
        f"reassess_records must have one entry per shifted feature: "
        f"expected {len(shifted_keys)}, got {len(records)}"
    )

    # Confirm every shifted key has a corresponding record.
    def _normalize(key) -> tuple[int, int, int]:
        if isinstance(key, str):
            parts = key.replace("(", "").replace(")", "").split(",")
            return tuple(int(p.strip()) for p in parts[:3])  # type: ignore[return-value]
        return tuple(key)  # type: ignore[return-value]

    record_keys = {_normalize(k) for k in records}
    assert record_keys == set(shifted_keys), (
        f"reassess_records keys {sorted(record_keys)} != shifted features {sorted(shifted_keys)}"
    )


def test_reassess_records_fields_populated(
    monkeypatch, baseline_ctx, mock_subagent_client, tmp_path
):
    """Each persisted record must contain the four triple-label fields."""
    mock_subagent_client.set_response(CANNED_RECORD)

    baseline_ctx.pinned_features = {(0, 0, 0): "h"}

    monkeypatch.setattr(
        "circuit_oracle.tools.shift_bucket",
        lambda *a, **k: "shifted",
    )

    batched_anchor_sweep(baseline_ctx)

    out_dir = tmp_path / "run-output"
    out_dir.mkdir()
    save_oracle_result(ctx=baseline_ctx, output_dir=out_dir)

    blob = json.loads((out_dir / "oracle_result.json").read_text())
    records = blob["reassess_records"]
    assert records, "reassess_records is empty"
    sample = next(iter(records.values()))
    for field in ("autointerp", "pre_label", "post_label", "divergence"):
        assert field in sample, (
            f"persisted reassess record missing field {field!r}; got keys {list(sample)}"
        )
