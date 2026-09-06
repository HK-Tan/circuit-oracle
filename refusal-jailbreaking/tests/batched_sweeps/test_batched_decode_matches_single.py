"""batched greedy decode matches single-call decode semantics.

The batched decode omits the EOS-break and instead
strips EOS per row in post-processing. For B=1 with an early EOS the visible
string must be identical to the single-call EOS-break path.
"""
from __future__ import annotations

import pytest

from circuit_oracle.tools import _batched_greedy_decode


def _single_call_decode(ctx, interventions, answer_max_tokens):
    """Reference single-call decode matching _measure_intervention semantics.

    Step 0: freeze_attention=True. Step 1+: freeze_attention=False.
    EOS-break on first EOS token (the single-call convention).
    Returns the decoded answer string.
    """
    model = ctx.replacement_model
    tokenizer = ctx.tokenizer
    prompt = ctx.baseline_prompt
    eos_id = getattr(tokenizer, "eos_token_id", None)

    result0 = model.feature_intervention_batched(
        inputs=prompt,
        intervention_lists=[interventions],
        freeze_attention=True,
    )
    step0_logits = result0.logits

    generated_ids = []
    next_id = int(step0_logits[0, -1, :].argmax().item())
    if eos_id is not None and next_id == eos_id:
        return tokenizer.decode(generated_ids, skip_special_tokens=True)
    generated_ids.append(next_id)

    if hasattr(model, "ensure_tokenized"):
        prompt_ids = model.ensure_tokenized(prompt)
    else:
        prompt_ids = model._tokenize(prompt)[0]
    current = prompt_ids.unsqueeze(0)

    import torch
    current = torch.cat([current, torch.tensor([[next_id]], dtype=torch.long)], dim=1)

    for _step in range(1, answer_max_tokens):
        result = model.feature_intervention_batched(
            inputs=current,
            intervention_lists=[interventions],
            freeze_attention=False,
        )
        next_id = int(result.logits[0, -1, :].argmax().item())
        if eos_id is not None and next_id == eos_id:
            break
        generated_ids.append(next_id)
        current = torch.cat([current, torch.tensor([[next_id]], dtype=torch.long)], dim=1)

    return tokenizer.decode(generated_ids, skip_special_tokens=True)


def test_batched_decode_b1_matches_single_call(baseline_ctx):
    """B=1: batched decode after EOS-strip must equal single-call EOS-break decode."""
    ctx = baseline_ctx
    interventions = [(1, slice(None, None), 3, -1.0)]

    single_answer = _single_call_decode(ctx, interventions, answer_max_tokens=8)
    batched_answers, _ = _batched_greedy_decode(
        ctx, [interventions], answer_max_tokens=8
    )

    assert batched_answers[0] == single_answer, (
        f"B=1 batched decode {batched_answers[0]!r} != single-call {single_answer!r}"
    )


def test_batched_decode_b3_each_row_matches_single_call(baseline_ctx):
    """B=3: each row's decoded string equals its single-call equivalent."""
    ctx = baseline_ctx
    intervention_lists = [
        [(1, slice(None, None), 3, -1.0)],
        [(1, slice(None, None), 5, -2.0)],
        [(0, slice(None, None), 1, -3.0)],
    ]

    batched_answers, _ = _batched_greedy_decode(
        ctx, intervention_lists, answer_max_tokens=8
    )

    for row_idx, row_interventions in enumerate(intervention_lists):
        single_answer = _single_call_decode(ctx, row_interventions, answer_max_tokens=8)
        assert batched_answers[row_idx] == single_answer, (
            f"Row {row_idx}: batched {batched_answers[row_idx]!r} != single {single_answer!r}"
        )
