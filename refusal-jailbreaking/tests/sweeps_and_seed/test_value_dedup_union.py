"""Value-key dedup, union and cross-stage repeat angles (CPU only).

Independent companion to test_anchor_dedup.py. Where that module forces the
double-position scale-0 collision and a deep-scale cross collision, this one
exercises three further properties of the unified decode-dedup that the spec's
validation plan calls out:

  - the floor edge case, a baseline EXACTLY at BASELINE_FLOOR still clamps to
    0.0 at scale 0 (so it collides with another at-floor pin), and a baseline
    just BELOW the floor does not,
  - a cross-stage exact repeat of the same pin key (the union folds a pin that
    two stages both selected) decodes once at every scale, not twice,
  - the n_decoded_rows <= n_origin_rows invariant and the measurements_by_feature
    rebuild keeping all 4 scales on every feature (the reassess fan-out must be
    unaffected by the decode-only dedup).

GPU decode and the reassess fan-out are monkeypatched, so nothing here touches a
model forward or the network.
"""
from __future__ import annotations

import torch

from circuit_oracle import tools as tools_mod
from circuit_oracle.tools import batched_anchor_sweep, BASELINE_FLOOR, SWEEP_SCALES


def _stub_decode_and_reassess(monkeypatch, captured):
    """Record the unique decode rows and return one deterministic answer each.

    The answer is keyed on the applied clamp value so two origins that share a
    clamp provably share the same answer string (the dedup contract). No GPU, no
    network.
    """
    def fake_decode(ctx, interventions_per_row, answer_max_tokens=800):
        captured["unique_rows"] = list(interventions_per_row)
        # One answer per UNIQUE row. Make the answer encode the clamp so a shared
        # clamp gives a provably shared answer string.
        answers = []
        for row in interventions_per_row:
            _, _, _, val = row[0]
            answers.append(f"clamp={round(val, 6)}")
        step0 = torch.zeros((len(interventions_per_row), 1, 1), dtype=torch.float32)
        return answers, step0

    monkeypatch.setattr(tools_mod, "_batched_greedy_decode", fake_decode)
    monkeypatch.setattr(
        tools_mod, "_topk_from_logits",
        lambda logits, tokenizer, k=5: {"_stub": True},
    )

    def fake_reassess(ctx, measurements_by_feature, **kwargs):
        for per_scale in measurements_by_feature.values():
            for m in per_scale.values():
                m["shift_bucket"] = "no-shift"
        return {}

    monkeypatch.setattr(tools_mod, "_dispatch_reassess", fake_reassess)


def test_at_floor_baselines_collide_at_scale_zero(baseline_ctx, monkeypatch):
    """Two pins of one feature both AT the floor collapse at scale 0.

    baseline == BASELINE_FLOOR gives new_value = baseline + (0 - 1) * baseline = 0,
    so two at-floor pins of the same feature decode scale 0 once. A third pin one
    unit below the floor does NOT (its scale-0 clamp is baseline - FLOOR < 0).
    """
    acts = torch.zeros((2, 6, 4), dtype=torch.float32)
    acts[0, 2, 1] = float(BASELINE_FLOOR)        # pin D, exactly at floor
    acts[0, 5, 1] = float(BASELINE_FLOOR)        # pin E, exactly at floor, same feature
    acts[1, 3, 2] = float(BASELINE_FLOOR) - 1.0  # pin F, just below floor, diff feature
    baseline_ctx.baseline_activations = acts
    baseline_ctx.pinned_features = {
        (0, 1, 2): "d", (0, 1, 5): "e", (1, 2, 3): "f",
    }

    captured: dict = {}
    _stub_decode_and_reassess(monkeypatch, captured)
    result = batched_anchor_sweep(baseline_ctx)

    by_key = {
        (m["layer"], m["feature_idx"], m["pos"], m["scale"]): m
        for m in result["measurements"]
    }
    d0 = by_key[(0, 1, 2, 0.0)]
    e0 = by_key[(0, 1, 5, 0.0)]
    f0 = by_key[(1, 2, 3, 0.0)]
    assert d0["new_value"] == 0.0
    assert e0["new_value"] == 0.0
    assert d0["answer_after"] == e0["answer_after"]  # shared clamp -> shared answer
    # F just below the floor: scale-0 clamp is (FLOOR - 1) - FLOOR = -1.0, distinct.
    assert f0["new_value"] == -1.0
    assert f0["answer_after"] != d0["answer_after"]


def test_cross_stage_exact_repeat_decodes_once(baseline_ctx, monkeypatch):
    """A pin both stages selected appears once in the union and decodes once.

    The union folds duplicate pins to a single key (a dict cannot hold the key
    twice), so a pin two stages share contributes ONE feature x 4 scales, decoded
    as 4 unique rows. This is the cross-stage-repeat collision the spec names.
    """
    acts = torch.zeros((1, 4, 3), dtype=torch.float32)
    acts[0, 1, 2] = 25.0
    baseline_ctx.baseline_activations = acts
    # The union of two stages that both picked L0:F2@1 is a single key.
    baseline_ctx.pinned_features = {(0, 2, 1): "shared"}

    captured: dict = {}
    _stub_decode_and_reassess(monkeypatch, captured)
    result = batched_anchor_sweep(baseline_ctx)

    # One feature x 4 scales = 4 origins, all 4 clamps distinct, so 4 decoded rows.
    assert result["n_origin_rows"] == 4
    assert result["n_decoded_rows"] == 4
    assert len(captured["unique_rows"]) == 4
    # baseline 25 -> {0, -25, -50, -75}, 4 distinct values.
    clamps = {round(r[0][3], 6) for r in captured["unique_rows"]}
    assert clamps == {0.0, -25.0, -50.0, -75.0}


def test_decoded_never_exceeds_origins_and_all_scales_present(
    baseline_ctx, monkeypatch
):
    """n_decoded_rows <= n_origin_rows, and every feature keeps all 4 scales.

    The decode-only dedup must not drop or reorder feature cells, otherwise the
    reassess fan-out (feature-outer, scale-inner) breaks. Assert the rebuilt
    measurements_by_feature has exactly SWEEP_SCALES per feature.
    """
    acts = torch.zeros((2, 6, 4), dtype=torch.float32)
    acts[0, 2, 1] = 20.0
    acts[0, 5, 1] = 20.0   # same feature, same baseline -> every scale collides
    acts[1, 2, 3] = 7.0
    baseline_ctx.baseline_activations = acts
    baseline_ctx.pinned_features = {
        (0, 1, 2): "a", (0, 1, 5): "b", (1, 3, 2): "c",
    }

    captured: dict = {}
    _stub_decode_and_reassess(monkeypatch, captured)
    result = batched_anchor_sweep(baseline_ctx)

    assert result["n_decoded_rows"] <= result["n_origin_rows"]
    # A and B share an identical baseline, so EVERY one of A's 4 clamps equals
    # B's, collapsing 8 origin rows for feature (0,1) to 4 decoded. Feature (1,3)
    # adds 4 more (distinct from each other and from feature (0,1)). 8 unique.
    assert result["n_decoded_rows"] == 8
    assert result["n_origin_rows"] == 12

    # measurements_by_feature is JSON-stringified by the return. Rebuild from the
    # flat measurements list (12 origins) and assert all 4 scales per feature.
    scales_by_feature: dict = {}
    for m in result["measurements"]:
        k = (m["layer"], m["feature_idx"], m["pos"])
        scales_by_feature.setdefault(k, set()).add(m["scale"])
    assert len(scales_by_feature) == 3  # three pins, none dropped
    for k, scales in scales_by_feature.items():
        assert scales == set(float(s) for s in SWEEP_SCALES), k
