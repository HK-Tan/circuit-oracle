"""intervene_feature(scale=-4) parity vs the corresponding batched row.

Asserts that the retained scale -4 escape hatch (`intervene_feature`) yields per-row
output equivalent to what a batched sweep row would produce at scale -4 if it were
included. Catches drift between the single-call escape path and the batched backend.

Position semantics: the intervention broadcasts across all
positions (`pos: slice(None, None)`). Both sides of the parity comparison must use
broadcast, otherwise the magnitudes diverge (single-position vs full-context kicks).
"""
from __future__ import annotations

import pytest
from numpy.testing import assert_allclose


def test_escape_hatch_parity(baseline_ctx):
    # Test-pattern rule: feature_intervention* are bound methods on
    # ReplacementModel, not module-level functions.
    from circuit_oracle.tools import (
        _apply_multiplicative_steering,
        _resolve_anchor_position,
        _run,
        _topk_from_logits,
        intervene_feature,
    )

    layer = 1
    feature_idx = 3

    # The escape hatch only opens once PIN -> ANCHOR has run (_check_chain_complete),
    # so stand the chain up first. Pinning the feature under test at the position
    # the resolver already picks keeps the numeric path identical to the unpinned
    # one: this arranges the precondition, it does not move the anchor.
    anchor_pos = _resolve_anchor_position(baseline_ctx, layer, feature_idx)
    baseline_ctx.pinned_features = {
        (layer, feature_idx, anchor_pos): "escape-hatch parity probe"
    }
    baseline_ctx.anchor_sweep_done = True

    # The batched row the escape hatch has to agree with: SAME multiplicative
    # steering `new_act = baseline + (factor - 1) × max(10, baseline)` and the
    # SAME broadcast position (`slice(None, None)`). If either side drifts back
    # to single-position semantics the magnitudes diverge and this test fires.
    baseline_act = float(
        baseline_ctx.baseline_activations[layer, anchor_pos, feature_idx].item()
    )
    target_value = _apply_multiplicative_steering(baseline_act, -4.0)
    intervention_row = [(layer, slice(None, None), feature_idx, target_value)]
    batched = baseline_ctx.replacement_model.feature_intervention_batched(
        inputs=baseline_ctx.baseline_prompt, intervention_lists=[intervention_row]
    )

    # Backend parity, at full numeric tightness. The escape hatch measures
    # through the single-prompt `_run`; the sweep rows go through
    # `feature_intervention_batched`. Same row, same numbers.
    single = _run(
        intervention_row,
        baseline_ctx.baseline_prompt,
        freeze_attn=True,
        model=baseline_ctx.replacement_model,
        retry_label="parity",
    )
    assert_allclose(single[0], batched.logits[0], rtol=1e-5)

    # Tool-level parity: what intervene_feature actually reports to the agent is
    # the top-5 read off that same intervened forward. `answer_max_tokens` is
    # capped here only because the toy model's positional table holds 32 slots
    # and the greedy decode extends the context one token per step.
    escape = intervene_feature(
        baseline_ctx,
        layer=layer,
        feature_idx=feature_idx,
        scale=-4.0,
        answer_max_tokens=8,
    )
    assert escape["intervention"]["new_activation"] == target_value
    assert escape["top5_after"] == _topk_from_logits(
        batched.logits[0][-1, :], baseline_ctx.tokenizer
    )


@pytest.mark.parametrize(
    "pinned, sweep_done, missing",
    [
        ({}, False, ["pin_features", "batched_anchor_sweep"]),
        ({(1, 3, 0): "hypothesis"}, False, ["batched_anchor_sweep"]),
        ({}, True, ["pin_features"]),
    ],
)
def test_escape_hatch_refuses_to_open_before_the_chain(
    baseline_ctx, pinned, sweep_done, missing
):
    """The guard the parity test above has to arrange around.

    intervene_feature is a factor=-4 saturation probe for AFTER the deterministic
    sweep, not a way around it. When pin_features fails, the agent used to fall
    through to one-shot interventions (the 2026-05-15 transcript), so an
    incomplete chain has to raise and name what is missing.
    """
    from circuit_oracle.tools import intervene_feature

    baseline_ctx.pinned_features = pinned
    baseline_ctx.anchor_sweep_done = sweep_done

    with pytest.raises(RuntimeError) as excinfo:
        intervene_feature(baseline_ctx, layer=1, feature_idx=3, scale=-4.0)

    message = str(excinfo.value)
    assert "intervene_feature" in message
    # Assert on the Missing: list, not on bare substrings: every step name also
    # appears in the remediation sentence, so a substring check would pass even
    # when the guard blames the wrong step.
    assert f"Missing: {missing}" in message
