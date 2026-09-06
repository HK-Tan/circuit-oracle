"""Arm 2's shift-only discovery annotation (the label-leak fix).

The "traversal, no inspect" arm keeps the causal shift
measurement (a measurement, not an interpretation) but must not receive the
label channels. ctx.discovery_annotation = "shift_only" makes
_causal_discovery_annotate stop after writing the shift bucket: no
inspect_feature auto-fetch, no reassess fan-out, no autointerp / post_label /
divergence fields, nothing appended to ctx.discovery_reassess.
"""

from __future__ import annotations

import pytest

from circuit_oracle.tools import (
    _causal_discovery_annotate,
    get_top_features,
    get_top_logits,
)


def _first_token(ctx) -> str:
    logits = get_top_logits(ctx, k=5)
    assert logits, "tiny fixture should expose at least one top logit token"
    return logits[0]["token"]


def test_shift_only_keeps_the_measurement_and_withholds_every_label_channel(
    monkeypatch, baseline_ctx
):
    # Force every measured feature to count as shifted, the case where the full
    # mode would fan out the reassess and write the three label fields.
    monkeypatch.setattr("circuit_oracle.tools.shift_bucket", lambda *a, **k: "shifted")

    backend_calls: list[str] = []

    def fake_backend(prompt, *, model):
        backend_calls.append(model)
        return "{}"

    baseline_ctx.subagent_client = fake_backend
    baseline_ctx.discovery_annotation = "shift_only"

    token = _first_token(baseline_ctx)
    feats = get_top_features(baseline_ctx, token=token, k=3)
    assert isinstance(feats, list) and feats

    annotated = _causal_discovery_annotate(baseline_ctx, feats)
    assert annotated is feats, "annotation happens in place and returns the same list"

    for row in feats:
        assert row.get("shift") == "shifted", row
        for leak in ("autointerp", "post_label", "divergence"):
            assert leak not in row, f"label channel {leak!r} leaked in shift_only mode"

    assert baseline_ctx.discovery_reassess == []
    assert backend_calls == [], "reassess fan-out must not run in shift_only mode"


def test_unknown_annotation_mode_fails_loud(monkeypatch, baseline_ctx):
    monkeypatch.setattr("circuit_oracle.tools.shift_bucket", lambda *a, **k: "no_shift")
    baseline_ctx.discovery_annotation = "labels-off"

    token = _first_token(baseline_ctx)
    feats = get_top_features(baseline_ctx, token=token, k=2)
    assert isinstance(feats, list) and feats

    with pytest.raises(ValueError, match="discovery_annotation"):
        _causal_discovery_annotate(baseline_ctx, feats)


@pytest.mark.parametrize(
    "result",
    [
        {"error": "no such token"},   # error dict from the discovery tool
        [],                           # no feature rows
        [{"type": "embedding", "pos": 0, "direct_effect": 0.1}],  # embedding rows only
        "not a list at all",
    ],
    ids=["error-dict", "empty", "embedding-only", "not-a-list"],
)
def test_a_bad_annotation_mode_raises_even_on_the_early_return_paths(
    baseline_ctx, result
):
    """Validation has to come before the early returns.

    Each of these results skips the causal pass. If the mode were only checked
    further down, a typo would raise on some discovery calls and pass silently on
    others, so whether the run leaked labels would depend on what the tool
    happened to return.
    """
    baseline_ctx.discovery_annotation = "labels-off"
    with pytest.raises(ValueError, match="discovery_annotation"):
        _causal_discovery_annotate(baseline_ctx, result)
