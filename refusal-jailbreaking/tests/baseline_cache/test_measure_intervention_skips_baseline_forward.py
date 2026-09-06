"""Assert _measure_intervention skips the baseline forward pass.

`_measure_intervention` used to run `_run([], prompt, freeze_attn=True)` to recompute
baseline_logits on every call. That was replaced with a read from
`ctx.baseline_top5`. The intervened forward still runs, plus the per-token decode.

The checks here are structural: patch the model's forward entry points and count
calls. Two properties are pinned.

1. No baseline-shaped forward (empty intervention list + freeze_attention=True).
   That requirement is backend-independent, so it
   still spies on `feature_intervention`: firing a baseline forward through any
   entry point is the failure, and asserting zero of them everywhere is stricter
   than asserting zero on one.
2. The intervened generation is prefill-once-then-KV-decode, not
   re-forward-the-world. `_measure_intervention` now delegates to
   `_batched_greedy_decode` at B=1, so the backend is `prefill_batched` plus
   `decode_step_batched`, and the old naive loop would show up as many prefills.
"""
from __future__ import annotations

import pytest


def test_measure_intervention_does_not_run_baseline_forward(baseline_ctx, monkeypatch):
    """_measure_intervention must NOT call feature_intervention with an empty intervention list."""
    from circuit_oracle import tools

    calls = []
    original_feature_intervention = baseline_ctx.replacement_model.feature_intervention

    def spy_feature_intervention(prompt_arg, interventions_list, **kwargs):
        calls.append({
            "interventions_list": list(interventions_list),
            "freeze_attention": kwargs.get("freeze_attention"),
        })
        return original_feature_intervention(prompt_arg, interventions_list, **kwargs)

    monkeypatch.setattr(
        baseline_ctx.replacement_model,
        "feature_intervention",
        spy_feature_intervention,
    )

    # One non-trivial intervention so the function has something to do.
    intervention_tuples = [(0, slice(None, None), 0, 0.0)]
    tools._measure_intervention(
        baseline_ctx,
        intervention_tuples,
        prompt=baseline_ctx.baseline_prompt,
        answer_max_tokens=2,
        retry_label="test",
    )

    # Identify baseline-shaped calls (empty interventions list, freeze_attn=True).
    baseline_shaped_calls = [
        c for c in calls
        if len(c["interventions_list"]) == 0 and c["freeze_attention"] is True
    ]
    assert len(baseline_shaped_calls) == 0, (
        f"_measure_intervention fired {len(baseline_shaped_calls)} baseline forward pass(es) "
        "(feature_intervention with empty interventions_list + freeze_attention=True). "
        "it must read ctx.baseline_top5 instead."
    )


def _spy_decode_backend(baseline_ctx, monkeypatch):
    """Record every prefill / decode-step call the KV-cached backend makes.

    _measure_intervention no longer drives generation through
    `feature_intervention`. It delegates to `_batched_greedy_decode` at B=1, whose
    backend is `prefill_batched` once followed by `decode_step_batched` per token.
    Spying on the two batched entry points is what tells prefill-once-then-decode
    apart from re-forward-everything-every-step.
    """
    model = baseline_ctx.replacement_model
    prefills, decode_steps = [], []

    original_prefill = model.prefill_batched
    original_decode_step = model.decode_step_batched

    def spy_prefill(inputs, intervention_lists, **kwargs):
        prefills.append({
            "intervention_lists": [list(row) for row in intervention_lists],
            "freeze_attention": kwargs.get("freeze_attention", True),
        })
        return original_prefill(inputs, intervention_lists, **kwargs)

    def spy_decode_step(new_token_ids, intervention_lists, past_kv_cache):
        decode_steps.append({"shape": tuple(new_token_ids.shape)})
        return original_decode_step(new_token_ids, intervention_lists, past_kv_cache)

    monkeypatch.setattr(model, "prefill_batched", spy_prefill)
    monkeypatch.setattr(model, "decode_step_batched", spy_decode_step)
    return prefills, decode_steps


def test_measure_intervention_still_runs_intervened_frozen_prefill(baseline_ctx, monkeypatch):
    """The intervened, frozen-attention prompt forward must still happen exactly once.

    top5_after is read off this forward, and freezing it is what keeps the reported
    next-token distribution on the same attention pattern the attribution graph was
    built under. The backend moved from feature_intervention to prefill_batched;
    the requirement did not move.
    """
    from circuit_oracle import tools

    prefills, _ = _spy_decode_backend(baseline_ctx, monkeypatch)

    intervention_tuples = [(0, slice(None, None), 0, 0.0)]
    tools._measure_intervention(
        baseline_ctx,
        intervention_tuples,
        prompt=baseline_ctx.baseline_prompt,
        answer_max_tokens=2,
        retry_label="test",
    )

    intervened_frozen = [
        p for p in prefills
        if len(p["intervention_lists"]) == 1
        and len(p["intervention_lists"][0]) > 0
        and p["freeze_attention"] is True
    ]
    assert len(intervened_frozen) == 1, (
        f"_measure_intervention must run exactly one intervened B=1 prefill with "
        f"freeze_attention=True (got {len(intervened_frozen)} of {len(prefills)} "
        f"total prefills: {prefills!r})."
    )


def test_measure_intervention_decodes_with_kv_cache_not_full_reforward(
    baseline_ctx, monkeypatch
):
    """Regression guard on the O(N^2) decode that cost a run tens of minutes.

    The loop this replaced re-forwarded the whole growing context every step. The
    signature of that mistake coming back is more than one prefill, or a decode
    step fed more than the single new token. Pinning both counts means a revert to
    the naive path fails here rather than only showing up as a slow GPU run.

    answer_max_tokens=6 on the toy model, so the budget is one prefill plus at most
    five decode steps, fewer if the row hits EOS early.
    """
    from circuit_oracle import tools

    prefills, decode_steps = _spy_decode_backend(baseline_ctx, monkeypatch)

    tools._measure_intervention(
        baseline_ctx,
        [(0, slice(None, None), 0, 0.0)],
        prompt=baseline_ctx.baseline_prompt,
        answer_max_tokens=6,
        retry_label="test",
    )

    assert len(prefills) == 1, (
        f"Expected exactly one prompt prefill for the whole generation, got "
        f"{len(prefills)}. More than one means the prompt is being re-forwarded "
        f"per step, which is the O(N^2) decode this path was moved off."
    )
    assert decode_steps, "Expected at least one KV-cached decode step, got none."
    assert len(decode_steps) <= 5, (
        f"answer_max_tokens=6 allows at most 5 decode steps after the prefill, got "
        f"{len(decode_steps)}."
    )
    assert all(s["shape"] == (1, 1) for s in decode_steps), (
        f"Every decode step must feed exactly one new token for the single row "
        f"(shape (1, 1)). Got {[s['shape'] for s in decode_steps]}. Any wider "
        f"shape means the context is being replayed instead of cached."
    )


def test_measure_intervention_uses_ctx_baseline_top5(baseline_ctx, monkeypatch):
    """The returned top5_before must equal ctx.baseline_top5 (read, not recomputed)."""
    from circuit_oracle import tools

    sentinel = {"__SENTINEL__": {"prob": 1.0}}
    baseline_ctx.baseline_top5 = sentinel

    intervention_tuples = [(0, slice(None, None), 0, 0.0)]
    top5_before, _top5_after, _ans, _t = tools._measure_intervention(
        baseline_ctx,
        intervention_tuples,
        prompt=baseline_ctx.baseline_prompt,
        answer_max_tokens=2,
        retry_label="test",
    )

    assert top5_before == sentinel, (
        "top5_before must be read from ctx.baseline_top5, not recomputed. "
        f"Expected {sentinel!r}, got {top5_before!r}."
    )
