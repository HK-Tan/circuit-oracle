"""Value-key dedup inside batched_anchor_sweep (CPU only, no GPU).

The unified sweep pass decodes each unique applied clamp once and scatters the
shared answer back to every origin (feature, scale). The dedup key is
(layer, feature_idx, round(new_value, 6)). These tests monkeypatch the GPU
decode and the reassess fan-out so the pure dedup / scatter-back logic is
exercised without a model forward.

Two collisions are forced:
  - the SAME (layer, feature_idx) pinned at two positions, both with baseline
    >= BASELINE_FLOOR, collides at scale 0 (the steering rule yields exactly
    0.0 for both),
  - and again at a deeper scale when the two dose grids cross (a 20-baseline at
    scale -3 and a 30-baseline at scale -2 both clamp to -60.0).
A third feature with baseline < BASELINE_FLOOR does NOT collide at scale 0
(its scale-0 clamp is baseline - BASELINE_FLOOR, a distinct negative value).
"""
from __future__ import annotations

import torch

from circuit_oracle import tools as tools_mod
from circuit_oracle.tools import batched_anchor_sweep


# Pin keys. A and B are the same (layer, feature_idx) at two positions.
_KEY_A = (0, 1, 2)   # baseline 20.0 (>= floor)
_KEY_B = (0, 1, 5)   # baseline 30.0 (>= floor), same feature as A, diff pos
_KEY_C = (1, 3, 2)   # baseline 4.0  (< floor)


def _install_baselines(ctx):
    """Controlled baseline_activations so the clamp grid is deterministic."""
    acts = torch.zeros((2, 6, 4), dtype=torch.float32)
    acts[0, 2, 1] = 20.0   # A
    acts[0, 5, 1] = 30.0   # B
    acts[1, 2, 3] = 4.0    # C
    ctx.baseline_activations = acts
    ctx.pinned_features = {_KEY_A: "a", _KEY_B: "b", _KEY_C: "c"}


def _stub_decode_and_reassess(monkeypatch, captured):
    """Replace the GPU decode and reassess fan-out with deterministic stubs.

    The decode stub records the unique rows it was handed and returns one
    answer per unique row ("ans{u}") plus a [B, 1, 1] step-0 logits tensor so
    step0_logits[u, -1, :] indexes cleanly.
    """
    def fake_decode(ctx, interventions_per_row, answer_max_tokens=800):
        captured["unique_rows"] = list(interventions_per_row)
        n = len(interventions_per_row)
        answers = [f"ans{u}" for u in range(n)]
        step0 = torch.zeros((n, 1, 1), dtype=torch.float32)
        return answers, step0

    monkeypatch.setattr(tools_mod, "_batched_greedy_decode", fake_decode)
    # top5 is irrelevant to dedup, so return a trivial marker.
    monkeypatch.setattr(
        tools_mod, "_topk_from_logits",
        lambda logits, tokenizer, k=5: {"_stub": True},
    )
    # No reassess fan-out. Annotate buckets to "no-shift" and return {}.
    def fake_reassess(ctx, measurements_by_feature, **kwargs):
        for per_scale in measurements_by_feature.values():
            for m in per_scale.values():
                m["shift_bucket"] = "no-shift"
        return {}

    monkeypatch.setattr(tools_mod, "_dispatch_reassess", fake_reassess)


def test_value_key_dedup_collapses_collisions(baseline_ctx, monkeypatch):
    _install_baselines(baseline_ctx)
    captured: dict = {}
    _stub_decode_and_reassess(monkeypatch, captured)

    result = batched_anchor_sweep(baseline_ctx)

    # 3 features x 4 scales origins.
    assert result["n_origin_rows"] == 12
    # Unique clamps: feature (0,1) has {0,-20,-40,-60,-30,-90} = 6,
    # feature (1,3) has {-6,-16,-26,-36} = 4. Total 10.
    assert result["n_decoded_rows"] == 10
    assert len(captured["unique_rows"]) == 10

    # Every unique decode row is one intervention 4-tuple with a slice(None,None).
    for row in captured["unique_rows"]:
        assert len(row) == 1
        layer, pos_slice, feat, val = row[0]
        assert pos_slice == slice(None, None)
        assert isinstance(val, float)

    # The applied clamp values seen by decode, per (layer, feature_idx).
    clamps_by_feat: dict = {}
    for row in captured["unique_rows"]:
        layer, _, feat, val = row[0]
        clamps_by_feat.setdefault((layer, feat), set()).add(round(val, 6))
    assert clamps_by_feat[(0, 1)] == {0.0, -20.0, -40.0, -60.0, -30.0, -90.0}
    assert clamps_by_feat[(1, 3)] == {-6.0, -16.0, -26.0, -36.0}


def test_scale_zero_collision_only_when_both_baselines_at_floor(
    baseline_ctx, monkeypatch
):
    _install_baselines(baseline_ctx)
    captured: dict = {}
    _stub_decode_and_reassess(monkeypatch, captured)

    result = batched_anchor_sweep(baseline_ctx)
    measurements = result["measurements"]

    # Index by (layer, feature_idx, pos, scale).
    by_key = {
        (m["layer"], m["feature_idx"], m["pos"], m["scale"]): m
        for m in measurements
    }
    # 12 origins survive in the flat list (dedup is decode-only).
    assert len(by_key) == 12

    a0 = by_key[(0, 1, 2, 0.0)]
    b0 = by_key[(0, 1, 5, 0.0)]
    c0 = by_key[(1, 3, 2, 0.0)]

    # A and B both clamp to exactly 0.0 at scale 0 (both baselines >= floor),
    # so they share the decoded answer.
    assert a0["new_value"] == 0.0
    assert b0["new_value"] == 0.0
    assert a0["answer_after"] == b0["answer_after"]

    # C's baseline is below the floor, so its scale-0 clamp is 4 - 10 = -6.0,
    # distinct, and it does NOT share A/B's scale-0 answer.
    assert c0["new_value"] == -6.0
    assert c0["answer_after"] != a0["answer_after"]

    # Deep-scale cross collision: A at scale -3 (-60.0) and B at scale -2 (-60.0)
    # share the same clamp and therefore the same decoded answer.
    a_m3 = by_key[(0, 1, 2, -3.0)]
    b_m2 = by_key[(0, 1, 5, -2.0)]
    assert a_m3["new_value"] == -60.0
    assert b_m2["new_value"] == -60.0
    assert a_m3["answer_after"] == b_m2["answer_after"]


def test_baseline_and_new_value_recorded_on_every_row(baseline_ctx, monkeypatch):
    _install_baselines(baseline_ctx)
    captured: dict = {}
    _stub_decode_and_reassess(monkeypatch, captured)

    result = batched_anchor_sweep(baseline_ctx)
    for m in result["measurements"]:
        assert "baseline" in m and m["baseline"] is not None
        assert "new_value" in m and m["new_value"] is not None
        # baseline matches the pin's installed value.
        if (m["layer"], m["feature_idx"], m["pos"]) == _KEY_A:
            assert m["baseline"] == 20.0
        if (m["layer"], m["feature_idx"], m["pos"]) == _KEY_C:
            assert m["baseline"] == 4.0
