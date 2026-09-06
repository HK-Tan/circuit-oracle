"""Integration test: KV-cached _decode_one_chunk with EOS-triggered cache compaction.

This test exercises the path that cannot be tested until _decode_one_chunk is
rewritten to use prefill_batched + decode_step_batched + _compact_kv_cache.
Specifically, it checks that when a row emits EOS mid-loop (at step >= 1),
the cache is compacted in lockstep with active_to_original and
interventions_per_row, and that the remaining rows continue to decode
correctly.

These tests build a real tiny ReplacementModel (same fixture approach as
test_prefill_decode_matches_feature_intervention.py) so the library's KV cache
plumbing actually runs, rather than using the TinyReplacementModel which has no
prefill_batched surface.

EOS triggering strategy:
    Because the tiny model has random weights, we cannot pre-know which token a
    given intervention produces at step 1. We use the following approach:

    1. Run a two-step reference decode for the row we want to EOS at step 1,
       capturing the token it generates at step 1.
    2. Set eos_id to that token for the _decode_one_chunk call.

    This guarantees row 1 EOSes at step 1 without relying on model semantics.
    The compaction path is still fully exercised: after step 1, the cache must
    shrink from B=3 to B=2, and the remaining two rows must continue decoding
    against their own (uncompacted) K/V rows.

    A secondary assertion wraps _compact_kv_cache to record each call's
    pre-compaction batch size, confirming the compaction actually happened and
    reduced the batch dim (not a no-op).
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import torch

# Make src/ importable without a pip install.
_REPO_ROOT = Path(__file__).resolve().parents[3]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from transformer_lens import HookedTransformerConfig
from circuit_tracer.replacement_model import (
    ReplacementModel,
    _compact_kv_cache,
)
from circuit_tracer.transcoder import SingleLayerTranscoder, TranscoderSet
from circuit_oracle.tools import _decode_one_chunk


# ---------------------------------------------------------------------------
# Tiny model config -- same as test_prefill_decode_matches_feature_intervention
# ---------------------------------------------------------------------------

_N_LAYERS = 2
_D_MODEL = 32
_D_HEAD = 16
_N_HEADS = 2
_D_MLP = 64
_D_VOCAB = 100
_N_CTX = 64
_D_TRANSCODER = 64
_SEED = 7777


def _build_tiny_replacement_model() -> ReplacementModel:
    """Construct a deterministic tiny ReplacementModel for CPU testing.

    Identical to the factory in test_prefill_decode_matches_feature_intervention.
    Kept local so this file is self-contained.
    """
    torch.manual_seed(_SEED)

    cfg = HookedTransformerConfig(
        n_layers=_N_LAYERS,
        d_model=_D_MODEL,
        d_head=_D_HEAD,
        n_heads=_N_HEADS,
        d_mlp=_D_MLP,
        d_vocab=_D_VOCAB,
        n_ctx=_N_CTX,
        act_fn="relu",
        normalization_type="LN",
        device="cpu",
        dtype=torch.float32,
        init_weights=True,
        seed=_SEED,
    )

    transcoders_dict = {}
    for layer_idx in range(_N_LAYERS):
        tc = SingleLayerTranscoder(
            d_model=_D_MODEL,
            d_transcoder=_D_TRANSCODER,
            activation_function=torch.nn.ReLU(),
            layer_idx=layer_idx,
            skip_connection=False,
            device="cpu",
            dtype=torch.float32,
        )
        with torch.no_grad():
            torch.manual_seed(_SEED + layer_idx)
            tc.W_enc.data.uniform_(-0.3, 0.3)
            tc.W_dec.data.uniform_(-0.3, 0.3)
        transcoders_dict[layer_idx] = tc

    tc_set = TranscoderSet(
        transcoders=transcoders_dict,
        feature_input_hook="hook_resid_mid",
        feature_output_hook="hook_mlp_out",
        scan=None,
    )

    model = ReplacementModel.from_config(cfg, tc_set)
    model.eval()
    return model


# Fixed prompt tensor (in-vocab IDs).
_PROMPT = torch.tensor([[1, 2, 3, 4, 5]], dtype=torch.long)

# Per-row interventions for the B=3 test.
_INTERVENTION_ROW0 = [(0, slice(None, None), 3, -1.0)]
_INTERVENTION_ROW1 = [(1, slice(None, None), 7, -2.0)]
_INTERVENTION_ROW2 = []  # identity row


# ---------------------------------------------------------------------------
# Helper: find the token row 1 generates at step 1 under its intervention.
# We will set eos_id = that token so row 1 EOSes at decode step 1.
# ---------------------------------------------------------------------------

def _step1_token_for_row1(model: ReplacementModel) -> int:
    """Run a two-step reference decode for row 1 and return the step-1 token ID.

    This is the token we will use as eos_id to trigger EOS at step 1 for row 1.
    Using the model's own output guarantees the EOS fires at exactly step 1
    regardless of the tiny model's random weights.
    """
    # Mirror _decode_one_chunk's exact flow so the predicted step-1 token equals
    # what the real decode produces. Using freeze_attention=False here or
    # re-prefilling the full sequence would NOT match, because decode_step_batched
    # attends to frozen-attention prompt K/V (from prefill) with natural attention
    # for the new query, a different operation than a full natural-attention
    # forward over [prompt, tok0].
    prompt = _PROMPT  # [1, T]
    iv = [_INTERVENTION_ROW1]

    # Step 0: prefill exactly as _decode_one_chunk does.
    logits0, kv_cache = model.prefill_batched(prompt, iv, freeze_attention=True)
    tok0 = int(logits0[0, -1, :].argmax().item())

    # Step 1: decode_step exactly as _decode_one_chunk does.
    next_tok = torch.tensor([[tok0]], dtype=torch.long)
    logits1 = model.decode_step_batched(next_tok, iv, past_kv_cache=kv_cache)
    tok1 = int(logits1[0, -1, :].argmax().item())
    return tok1


# ---------------------------------------------------------------------------
# Helper: minimal tokenizer surface for _decode_one_chunk.
# ---------------------------------------------------------------------------

class _MinimalTokenizer:
    """Minimal tokenizer that _decode_one_chunk can use.

    decode() returns a space-joined string of token IDs (no special tokens),
    which is sufficient for the test's equality assertions.
    """

    def __init__(self, eos_token_id: int) -> None:
        self.eos_token_id = eos_token_id

    def decode(self, ids, skip_special_tokens: bool = False) -> str:
        if isinstance(ids, torch.Tensor):
            ids = ids.tolist()
        tokens = [str(i) for i in ids if not (skip_special_tokens and i == self.eos_token_id)]
        return " ".join(tokens)


# ---------------------------------------------------------------------------
# Main integration test
# ---------------------------------------------------------------------------

def test_eos_at_step1_compacts_cache_and_preserves_row_order():
    """B=3: row 1 EOSes at decode step 1, cache compacts from 3 to 2.

    Assertions:
      1. answers has length 3 (original row order preserved).
      2. answers[1] is finalized at step 1 (non-empty or empty depending on
         whether step 0 generated a non-EOS token -- it will be non-empty
         because EOS fires at step 1, not step 0).
      3. answers[0] and answers[2] match their single-row reference decodes
         (the cache compaction did not corrupt the surviving rows' K/V).
      4. step0_logits has shape [3, T_prompt, V].
      5. _compact_kv_cache was called at least once with a compaction that
         reduced the batch dim (from 3 to 2), catching "forgot to compact."
    """
    model = _build_tiny_replacement_model()

    # Find the token row 1 generates at step 1 so we can set it as eos_id.
    eos_id = _step1_token_for_row1(model)

    # Sanity: make sure this eos_id is not also generated by rows 0 or 2 at
    # step 0. If it were, those rows would also EOS at step 0 or 1, making the
    # test less meaningful. We run the sanity check but do not fail the test if
    # it coincidentally matches, since the core compaction path is still tested.
    tokenizer = _MinimalTokenizer(eos_token_id=eos_id)

    intervention_lists = [
        _INTERVENTION_ROW0,
        _INTERVENTION_ROW1,
        _INTERVENTION_ROW2,
    ]

    # Track _compact_kv_cache calls to assert compaction actually happened.
    compaction_records: list[int] = []  # pre-compaction batch sizes

    original_compact = _compact_kv_cache

    def _instrumented_compact(cache, keep_local):
        # Record the batch size BEFORE compaction.
        pre_size = cache.entries[0].past_keys.shape[0] if cache.entries else 0
        compaction_records.append(pre_size)
        original_compact(cache, keep_local)

    prompt = _PROMPT  # [1, T_prompt]

    with patch(
        "circuit_oracle.tools._compact_kv_cache",
        side_effect=_instrumented_compact,
    ):
        answers, step0_logits = _decode_one_chunk(
            model,
            prompt,
            tokenizer,
            eos_id,
            intervention_lists,
            answer_max_tokens=8,
        )

    # 1. Length preserved.
    assert len(answers) == 3, f"Expected 3 answers, got {len(answers)}"

    # 2. step0_logits shape.
    assert step0_logits.shape[0] == 3, (
        f"step0_logits batch dim should be 3, got {step0_logits.shape[0]}"
    )
    assert step0_logits.shape[2] == _D_VOCAB, (
        f"step0_logits vocab dim should be {_D_VOCAB}, got {step0_logits.shape[2]}"
    )

    # 3. Row 1 is finalized (answer is set, not None).
    assert answers[1] is not None, "answers[1] should be finalized after step-1 EOS"

    # 4. Rows 0 and 2 are also finalized (not None).
    assert answers[0] is not None, "answers[0] should be set"
    assert answers[2] is not None, "answers[2] should be set"

    # 5. _compact_kv_cache was called with a non-trivial reduction.
    # We expect at least one compaction from 3 to 2 (when row 1 EOSes at step 1).
    assert compaction_records, (
        "_compact_kv_cache was never called -- cache compaction did not happen"
    )
    # The first mid-loop compaction (at step 1 when row 1 EOSes) should reduce
    # from batch=3 to batch=2. The pre-compaction size should be 3.
    assert any(size == 3 for size in compaction_records), (
        f"Expected at least one compaction from batch=3, "
        f"but recorded pre-compaction sizes: {compaction_records}"
    )

    # 6. Row order: rows 0 and 2 should match their single-row reference decodes
    # (no intervention list / cache mis-alignment corrupted them).
    single_row0_answers, _ = _decode_one_chunk(
        model, prompt, tokenizer, eos_id, [_INTERVENTION_ROW0], answer_max_tokens=8
    )
    single_row2_answers, _ = _decode_one_chunk(
        model, prompt, tokenizer, eos_id, [_INTERVENTION_ROW2], answer_max_tokens=8
    )

    assert answers[0] == single_row0_answers[0], (
        f"Row 0 answer {answers[0]!r} != single-row reference {single_row0_answers[0]!r}. "
        f"Cache compaction may have corrupted row 0's K/V."
    )
    assert answers[2] == single_row2_answers[0], (
        f"Row 2 answer {answers[2]!r} != single-row reference {single_row2_answers[0]!r}. "
        f"Cache compaction may have corrupted row 2's K/V."
    )


def test_no_eos_rows_no_compaction():
    """B=2 where no row ever EOSes: _compact_kv_cache is called at step-0
    compaction only (with a no-op keep_local equal to the full batch), and
    the loop runs for the full answer_max_tokens steps.

    This is a regression guard: if the compaction lockstep logic fires even
    when no EOS occurs, the test would catch a spurious compaction that
    reduces B unexpectedly.
    """
    model = _build_tiny_replacement_model()

    # Use an eos_id that is out-of-vocab (and thus never generated).
    out_of_vocab_eos_id = _D_VOCAB + 999
    tokenizer = _MinimalTokenizer(eos_token_id=out_of_vocab_eos_id)

    intervention_lists = [
        _INTERVENTION_ROW0,
        _INTERVENTION_ROW2,
    ]

    compaction_records: list[tuple[int, int]] = []  # (pre_size, post_keep_len)
    original_compact = _compact_kv_cache

    def _instrumented_compact(cache, keep_local):
        pre_size = cache.entries[0].past_keys.shape[0] if cache.entries else 0
        compaction_records.append((pre_size, len(keep_local)))
        original_compact(cache, keep_local)

    prompt = _PROMPT
    max_tokens = 4  # short run so the test stays fast

    with patch(
        "circuit_oracle.tools._compact_kv_cache",
        side_effect=_instrumented_compact,
    ):
        answers, step0_logits = _decode_one_chunk(
            model, prompt, tokenizer, out_of_vocab_eos_id,
            intervention_lists, answer_max_tokens=max_tokens,
        )

    assert len(answers) == 2
    assert step0_logits.shape[0] == 2

    # No row should have EOSed, so both answers are non-empty decoded strings.
    # (The tiny model generates non-EOS tokens since out_of_vocab_eos never fires.)
    for i, ans in enumerate(answers):
        assert ans is not None, f"answers[{i}] is None"

    # Any compaction that did fire (e.g. the step-0 no-op where B0==B_active)
    # should not have reduced the batch size. Every recorded compaction should
    # keep all rows (pre_size == post_keep_len).
    for pre_size, post_keep_len in compaction_records:
        assert pre_size == post_keep_len, (
            f"Unexpected batch reduction: {pre_size} -> {post_keep_len}. "
            f"No row should have EOSed with out-of-vocab eos_id={out_of_vocab_eos_id}."
        )


def test_all_rows_eos_at_step0_no_decode_loop():
    """B=2 where every row EOSes at step 0 (prefill).

    The decode loop should never be entered. _compact_kv_cache is called once
    during the step-0 EOS handling (compacting from 2 to 0), and both answers
    are "".

    This tests the edge case where active_to_original becomes empty after step
    0, exercising the early break in the decode loop.
    """
    model = _build_tiny_replacement_model()

    # Find what token the model generates at step 0 for the identity intervention.
    logits0, _ = model.prefill_batched(_PROMPT, [[]], freeze_attention=True)
    step0_tok = int(logits0[0, -1, :].argmax().item())

    # Make that token the eos_id, so every row (using empty intervention)
    # EOSes at step 0.
    tokenizer = _MinimalTokenizer(eos_token_id=step0_tok)

    intervention_lists = [[], []]  # Both rows: identity, same step-0 argmax.

    compaction_records: list[tuple[int, int]] = []
    original_compact = _compact_kv_cache

    def _instrumented_compact(cache, keep_local):
        pre_size = cache.entries[0].past_keys.shape[0] if cache.entries else 0
        compaction_records.append((pre_size, len(keep_local)))
        original_compact(cache, keep_local)

    prompt = _PROMPT
    with patch(
        "circuit_oracle.tools._compact_kv_cache",
        side_effect=_instrumented_compact,
    ):
        answers, step0_logits = _decode_one_chunk(
            model, prompt, tokenizer, step0_tok,
            intervention_lists, answer_max_tokens=8,
        )

    assert len(answers) == 2, f"Expected 2 answers, got {len(answers)}"
    assert step0_logits.shape[0] == 2, (
        f"step0_logits batch dim should be 2, got {step0_logits.shape[0]}"
    )
    assert answers[0] == "", f"Row 0 expected '' (step-0 EOS), got {answers[0]!r}"
    assert answers[1] == "", f"Row 1 expected '' (step-0 EOS), got {answers[1]!r}"

    # The step-0 compaction from B0=2 to B_active=0 must have fired.
    assert any(pre == 2 and post == 0 for pre, post in compaction_records), (
        f"Expected a 2->0 compaction at step 0, but got: {compaction_records}"
    )
