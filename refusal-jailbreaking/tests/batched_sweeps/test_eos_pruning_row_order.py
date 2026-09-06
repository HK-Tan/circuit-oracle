"""EOS pruning in _decode_one_chunk preserves per-row output.

Three cases test that EOS pruning does not regress row order or answer
correctness:

1. Uniform-length rows (B=4, identical interventions): each row's answer
   equals the single-row reference decode. Catches "I broke the easy case."

2. Mixed-length rows (B=3): row 1 EOSes at step 0, row 0 and row 2 run to
   the token cap. Assert row 1 = "", row 0 and row 2 match single-row
   reference decodes, step0_logits has shape [3, T_prompt, V]. Catches
   row-order regressions and step-0 EOS handling.

3. All-EOS at step 0 (B=2): both rows produce "" and the function returns
   cleanly. Catches premature crash when the active set empties after step 0.

All tests run on CPU against the tiny-model fixture. No GPU, timing, or VRAM
assertions.
"""
from __future__ import annotations

import pytest
import torch

from circuit_oracle.tools import _decode_one_chunk


# Intervention that forces EOS (token 0) at step 0 under the tiny model.
# Verified empirically: layer=0, feature=28, factor=-5.0 makes argmax(logits[-1]) == 0.
_EOS_AT_STEP0 = [(0, slice(None, None), 28, -5.0)]


def _single_row_answer(ctx, interventions, max_tokens: int) -> str:
    """Reference single-row decode via _decode_one_chunk with a 1-row chunk."""
    model = ctx.replacement_model
    tokenizer = ctx.tokenizer
    eos_id = getattr(tokenizer, "eos_token_id", None)
    answers, _ = _decode_one_chunk(
        model, ctx.baseline_prompt, tokenizer, eos_id, [interventions], max_tokens
    )
    return answers[0]


# ---------------------------------------------------------------------------
# Test 1: Uniform-length rows
# ---------------------------------------------------------------------------

def test_uniform_rows_b4_match_single_call(baseline_ctx):
    """B=4 identical rows: each answer equals the single-row reference.

    Uses empty-intervention rows so all rows are guaranteed to generate
    the same sequence (the tiny model is deterministic). Catches regressions
    in the basic case where no row ever EOSes early.
    """
    ctx = baseline_ctx
    model = ctx.replacement_model
    tokenizer = ctx.tokenizer
    eos_id = getattr(tokenizer, "eos_token_id", None)
    max_tokens = 8

    interventions_list = [[], [], [], []]
    answers, step0_logits = _decode_one_chunk(
        model, ctx.baseline_prompt, tokenizer, eos_id, interventions_list, max_tokens
    )

    # Reference: single-row decode for the same intervention.
    reference = _single_row_answer(ctx, [], max_tokens)

    assert len(answers) == 4, f"Expected 4 answers, got {len(answers)}"
    assert step0_logits.shape[0] == 4, (
        f"step0_logits batch dim should be 4, got {step0_logits.shape[0]}"
    )
    for i, ans in enumerate(answers):
        assert ans == reference, (
            f"Row {i} answer {ans!r} != single-row reference {reference!r}"
        )


# ---------------------------------------------------------------------------
# Test 2: Mixed-length rows including one early-EOS (at step 0)
# ---------------------------------------------------------------------------

def test_mixed_eos_row1_step0(baseline_ctx):
    """B=3: row 1 EOSes at step 0, rows 0 and 2 run to max-tokens cap.

    Assertions:
      - answers[1] == "" (EOS on first generated token -> empty string)
      - answers[0] and answers[2] match their respective single-row decodes
      - step0_logits.shape == [3, T_prompt, V]

    This catches row-order regressions (active_to_original bookkeeping) and
    step-0 EOS handling (row never enters the decode loop).
    """
    ctx = baseline_ctx
    model = ctx.replacement_model
    tokenizer = ctx.tokenizer
    eos_id = getattr(tokenizer, "eos_token_id", None)
    max_tokens = 8

    # Row 0: no intervention (runs to cap).
    # Row 1: EOS-at-step-0 intervention (immediately finalized).
    # Row 2: no intervention (runs to cap).
    interventions_list = [
        [],
        _EOS_AT_STEP0,
        [],
    ]
    answers, step0_logits = _decode_one_chunk(
        model, ctx.baseline_prompt, tokenizer, eos_id, interventions_list, max_tokens
    )

    assert len(answers) == 3, f"Expected 3 answers, got {len(answers)}"

    # step0_logits must cover all B0=3 rows (shape invariant for callers).
    assert step0_logits.shape[0] == 3, (
        f"step0_logits batch dim should be 3, got {step0_logits.shape[0]}"
    )

    # Row 1: EOS at step 0 -> empty string answer.
    assert answers[1] == "", (
        f"Row 1 (EOS at step 0) expected '', got {answers[1]!r}"
    )

    # Rows 0 and 2: compare against single-row reference.
    ref_normal = _single_row_answer(ctx, [], max_tokens)
    assert answers[0] == ref_normal, (
        f"Row 0 answer {answers[0]!r} != single-row reference {ref_normal!r}"
    )
    assert answers[2] == ref_normal, (
        f"Row 2 answer {answers[2]!r} != single-row reference {ref_normal!r}"
    )


# ---------------------------------------------------------------------------
# Test 3: All rows EOS at step 0
# ---------------------------------------------------------------------------

def test_all_eos_at_step0(baseline_ctx):
    """B=2 where every row EOSes at step 0.

    Assertions:
      - Both answers are "".
      - Function returns cleanly (no crash from empty active set after step 0).
      - step0_logits has batch dim 2.
    """
    ctx = baseline_ctx
    model = ctx.replacement_model
    tokenizer = ctx.tokenizer
    eos_id = getattr(tokenizer, "eos_token_id", None)
    max_tokens = 8

    interventions_list = [_EOS_AT_STEP0, _EOS_AT_STEP0]
    answers, step0_logits = _decode_one_chunk(
        model, ctx.baseline_prompt, tokenizer, eos_id, interventions_list, max_tokens
    )

    assert len(answers) == 2, f"Expected 2 answers, got {len(answers)}"
    assert step0_logits.shape[0] == 2, (
        f"step0_logits batch dim should be 2, got {step0_logits.shape[0]}"
    )
    assert answers[0] == "", f"Row 0 expected '', got {answers[0]!r}"
    assert answers[1] == "", f"Row 1 expected '', got {answers[1]!r}"
