"""Assert the cached baseline is byte-identical to a fresh recomputation.

`_measure_intervention` reads `ctx.baseline_top5` and never re-runs the
empty-intervention forward, so there is no cache flag to toggle off inside the
function. Instead we compare two flows directly:

  - Flow A (fresh):   compute top5_before through model.feature_intervention([], ...),
                      exactly the call _measure_intervention used to issue. This is
                      the ground-truth "no cache" value.
  - Flow B (cached):  call _measure_intervention, which reads ctx.baseline_top5.

Both flows must produce byte-identical fp32 top5 dicts, the same keys in the
same order with probability floats equal to repr. If they diverge, the cache
stores something different from a fresh forward and the optimization is unsafe.
"""
from __future__ import annotations

import pytest


def test_cached_baseline_matches_recomputed_baseline(baseline_ctx):
    """top5_before from the cached flow must equal top5_before from a fresh forward."""
    from circuit_oracle import tools

    # The fixture must have populated ctx.baseline_top5. This IS the cached
    # value, persisted at graph-build time.
    assert baseline_ctx.baseline_top5 is not None, (
        "baseline_ctx fixture must populate ctx.baseline_top5 before this test runs."
    )

    intervention_tuples = [(0, slice(None, None), 0, 0.0)]

    # Flow A - fresh recompute through the code path _measure_intervention used
    # to use: model.feature_intervention([], prompt, freeze_attention=True).
    # This is the byte-identity ground truth. We do not mutate ctx.baseline_top5.
    fresh_logits, _ = baseline_ctx.replacement_model.feature_intervention(
        baseline_ctx.baseline_prompt,
        [],
        freeze_attention=True,
        return_activations=False,
    )
    top5_before_recomputed = tools._topk_from_logits(
        fresh_logits[0, -1, :], baseline_ctx.tokenizer
    )

    # Flow B - cached read via _measure_intervention, which reads
    # ctx.baseline_top5 instead of re-running the empty-intervention forward.
    top5_before_cached, _, _, _ = tools._measure_intervention(
        baseline_ctx,
        intervention_tuples,
        prompt=baseline_ctx.baseline_prompt,
        answer_max_tokens=2,
        retry_label="cached",
    )

    # Byte-identity check: keys in same order, prob floats equal under repr().
    assert list(top5_before_cached.keys()) == list(top5_before_recomputed.keys()), (
        "Cached and recomputed top5_before have different token order:\n"
        f"  cached:     {list(top5_before_cached.keys())}\n"
        f"  recomputed: {list(top5_before_recomputed.keys())}"
    )
    for token in top5_before_cached:
        cached_prob = top5_before_cached[token]["prob"]
        recomputed_prob = top5_before_recomputed[token]["prob"]
        assert repr(cached_prob) == repr(recomputed_prob), (
            f"Probability for {token!r} differs between cache and recompute: "
            f"cached={cached_prob!r} vs recomputed={recomputed_prob!r}. "
            "the baseline cache must be byte-identical to a fresh forward."
        )


def test_cached_baseline_matches_ctx_field(baseline_ctx):
    """The top5_before returned by _measure_intervention must equal ctx.baseline_top5 exactly."""
    from circuit_oracle import tools

    intervention_tuples = [(0, slice(None, None), 0, 0.0)]
    top5_before, _, _, _ = tools._measure_intervention(
        baseline_ctx,
        intervention_tuples,
        prompt=baseline_ctx.baseline_prompt,
        answer_max_tokens=2,
        retry_label="check",
    )

    assert top5_before == baseline_ctx.baseline_top5, (
        "top5_before returned by _measure_intervention must equal ctx.baseline_top5. "
        f"Got top5_before={top5_before!r}, ctx.baseline_top5={baseline_ctx.baseline_top5!r}."
    )
