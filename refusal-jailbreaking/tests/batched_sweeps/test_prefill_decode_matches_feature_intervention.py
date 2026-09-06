"""Stage 2 tests: prefill_batched + decode_step_batched + _compact_kv_cache.

Three CPU-only tests against a real (tiny) ReplacementModel built from a
HookedTransformerConfig with 2 layers, d_model=32, n_heads=2, vocab=100.

These tests do NOT go through _decode_one_chunk; they exercise the new
methods directly. They are independent of the baseline_ctx / tiny_model
fixtures, which use TinyReplacementModel and have no KV cache plumbing.

Numerical note: the cached and non-cached paths share the same weight matrix
reads and the same floating-point ops in the MLP and attention blocks, so
in practice we observe bit-identical argmax results on CPU float32.  We only
assert argmax equality (not logit equality) to remain tolerant of any future
hardware or precision changes.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import torch

# Make src/ importable so we can import circuit_tracer directly.
_REPO_ROOT = Path(__file__).resolve().parents[3]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from transformer_lens import HookedTransformerConfig
from circuit_tracer.replacement_model import ReplacementModel, _compact_kv_cache
from circuit_tracer.transcoder import SingleLayerTranscoder, TranscoderSet


# ---------------------------------------------------------------------------
# Shared tiny-model config and factory
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
    """Construct a deterministic ReplacementModel small enough to run on CPU.

    The model uses:
      - 2 transformer layers
      - d_model = 32, n_heads = 2, d_head = 16, d_mlp = 64
      - vocab = 100, n_ctx = 64
      - ReLU activation (simplest; no JumpReLU threshold to tune)
      - feature_input_hook = 'hook_resid_mid'
      - feature_output_hook = 'hook_mlp_out'

    A fresh TranscoderSet with random (seed-initialized) weights is built
    alongside the model so the transcoder encoder/decoder paths actually fire
    and produce non-trivial deltas when interventions are applied.
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
        # Give each transcoder deterministic, non-zero weights so interventions
        # produce visible effects in the logits.
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


# Shared prompt token IDs: fixed, small, in-vocab.
_PROMPT = torch.tensor([[1, 2, 3, 4, 5]], dtype=torch.long)

# A non-trivial single-row intervention: zero-out feature 3 at layer 0
# across all positions.  The -1.0 value is a significant negative steering
# kick that changes the logit distribution noticeably.
_INTERVENTION_ROW0 = [(0, slice(None, None), 3, -1.0)]


# ---------------------------------------------------------------------------
# Helper: run non-cached reference with feature_intervention_batched
# ---------------------------------------------------------------------------

def _noncached_token_sequence(
    model: ReplacementModel,
    prompt: torch.Tensor,
    interventions: list,
    n_decode: int,
    freeze_attention: bool = False,
) -> list[int]:
    """Greedy decode via repeated feature_intervention_batched (no KV cache).

    Mirrors the existing _decode_one_chunk step logic exactly:
      - First call: prompt tokens, freeze_attention=freeze_attention.
      - Subsequent calls: growing token sequence, freeze_attention=False.

    Returns the list of n_decode+1 generated token IDs (one from the prefill
    logits and n_decode from subsequent steps).
    """
    result = model.feature_intervention_batched(
        inputs=prompt,
        intervention_lists=[interventions],
        freeze_attention=freeze_attention,
        return_activations=False,
    )
    first_id = int(result.logits[0, -1, :].argmax().item())
    generated = [first_id]

    current = torch.cat([prompt, torch.tensor([[first_id]], dtype=torch.long)], dim=1)
    for _ in range(n_decode):
        result = model.feature_intervention_batched(
            inputs=current,
            intervention_lists=[interventions],
            freeze_attention=False,
            return_activations=False,
        )
        nid = int(result.logits[0, -1, :].argmax().item())
        generated.append(nid)
        current = torch.cat([current, torch.tensor([[nid]], dtype=torch.long)], dim=1)

    return generated


# ---------------------------------------------------------------------------
# Test 1: B=1 cached path matches non-cached path on first 5 generated tokens
# ---------------------------------------------------------------------------

def test_b1_matches_no_cache():
    """B=1 prefill+decode produces the same argmax token sequence as feature_intervention_batched.

    Tolerance: argmax equality on the first 5 generated tokens. We do not
    require logit-level equality because the cached and non-cached attention
    computations differ in op order (cached path appends K/V incrementally;
    non-cached path recomputes the full sequence each step).
    """
    N_DECODE = 4  # 1 from prefill + 4 decode steps = 5 tokens total

    model = _build_tiny_replacement_model()

    # --- Non-cached reference ---
    ref_ids = _noncached_token_sequence(
        model, _PROMPT, _INTERVENTION_ROW0, n_decode=N_DECODE, freeze_attention=False
    )

    # --- Cached path ---
    logits_pf, cache = model.prefill_batched(
        _PROMPT,
        [_INTERVENTION_ROW0],
        freeze_attention=False,
    )
    cached_ids = [int(logits_pf[0, -1, :].argmax().item())]

    for _ in range(N_DECODE):
        new_tok = torch.tensor([[cached_ids[-1]]], dtype=torch.long)
        dec_logits = model.decode_step_batched(
            new_tok, [_INTERVENTION_ROW0], cache
        )
        cached_ids.append(int(dec_logits[0, 0, :].argmax().item()))

    assert len(cached_ids) == 5, f"Expected 5 generated IDs, got {len(cached_ids)}"
    assert cached_ids == ref_ids[:5], (
        f"Cached path token sequence {cached_ids} != "
        f"non-cached reference {ref_ids[:5]}"
    )


# ---------------------------------------------------------------------------
# Test 2: B=3 row-order invariant
# ---------------------------------------------------------------------------

def test_b3_row_order_preserved():
    """B=3 prefill+decode: each row's output matches the corresponding B=1 reference.

    Uses three different interventions so each row genuinely differs.
    If cache compaction reorders rows, or the intervention list and cache
    batch dimension diverge, at least one row's argmax sequence will mismatch
    its B=1 reference.
    """
    N_DECODE = 4
    MODEL = _build_tiny_replacement_model()

    intervention_lists = [
        [(0, slice(None, None), 3, -1.0)],   # row 0: layer-0 feature steer
        [(1, slice(None, None), 5, -2.0)],   # row 1: layer-1 feature steer
        [],                                   # row 2: identity (no intervention)
    ]

    # --- B=1 references, one per row ---
    ref_sequences = []
    for ivlist in intervention_lists:
        ref_ids = _noncached_token_sequence(
            MODEL, _PROMPT, ivlist, n_decode=N_DECODE, freeze_attention=False
        )
        ref_sequences.append(ref_ids)

    # --- B=3 cached path ---
    prompt_b3 = _PROMPT.expand(3, -1)  # [3, T_prompt]
    logits_pf, cache = MODEL.prefill_batched(
        prompt_b3,
        intervention_lists,
        freeze_attention=False,
    )

    assert logits_pf.shape == (3, _PROMPT.shape[1], _D_VOCAB), (
        f"Unexpected prefill logits shape: {logits_pf.shape}"
    )
    assert cache.entries[0].past_keys.shape[0] == 3, (
        f"Cache batch dim should be 3, got {cache.entries[0].past_keys.shape[0]}"
    )

    # Collect first generated token per row from prefill logits.
    batched_ids = [[int(logits_pf[b, -1, :].argmax().item())] for b in range(3)]

    for _ in range(N_DECODE):
        # Build [B, 1] tensor of last generated tokens for each row.
        new_toks = torch.tensor(
            [[batched_ids[b][-1]] for b in range(3)], dtype=torch.long
        )
        dec_logits = MODEL.decode_step_batched(new_toks, intervention_lists, cache)
        assert dec_logits.shape == (3, 1, _D_VOCAB), (
            f"Unexpected decode logits shape: {dec_logits.shape}"
        )
        for b in range(3):
            batched_ids[b].append(int(dec_logits[b, 0, :].argmax().item()))

    # Assert per-row equality against B=1 references.
    for b in range(3):
        assert batched_ids[b] == ref_sequences[b][:5], (
            f"Row {b}: batched sequence {batched_ids[b]} != "
            f"reference {ref_sequences[b][:5]}"
        )


# ---------------------------------------------------------------------------
# Test 3: _compact_kv_cache helper correctness
# ---------------------------------------------------------------------------

def test_compact_kv_cache_helper():
    """_compact_kv_cache(cache, [0, 2]) on a B=3 cache yields B'=2 with correct rows.

    Manually populate a cache via prefill at B=3, apply compaction, and
    verify:
      1. Every layer's K and V tensors have batch_dim == 2 after compaction.
      2. The surviving rows at positions 0 and 1 of the compacted cache
         equal the original rows 0 and 2 of the pre-compaction cache.
    """
    model = _build_tiny_replacement_model()

    intervention_lists = [
        [(0, slice(None, None), 3, -1.0)],   # row 0
        [(1, slice(None, None), 5, -2.0)],   # row 1 (will be dropped)
        [],                                   # row 2
    ]

    prompt_b3 = _PROMPT.expand(3, -1)
    _, cache = model.prefill_batched(
        prompt_b3,
        intervention_lists,
        freeze_attention=False,
    )

    # Snapshot original K/V for rows 0 and 2 before compaction.
    original_keys = [
        entry.past_keys.clone() for entry in cache.entries
    ]
    original_vals = [
        entry.past_values.clone() for entry in cache.entries
    ]

    # Compact: keep rows 0 and 2 (drop row 1).
    _compact_kv_cache(cache, keep_local=[0, 2])

    for layer_idx, entry in enumerate(cache.entries):
        # Shape check: batch dim must shrink to 2.
        assert entry.past_keys.shape[0] == 2, (
            f"Layer {layer_idx}: expected batch_dim == 2 after compact, "
            f"got {entry.past_keys.shape[0]}"
        )
        assert entry.past_values.shape[0] == 2, (
            f"Layer {layer_idx}: expected batch_dim == 2 after compact (values), "
            f"got {entry.past_values.shape[0]}"
        )

        # Content check: compacted row 0 == original row 0.
        assert torch.equal(entry.past_keys[0], original_keys[layer_idx][0]), (
            f"Layer {layer_idx}: compacted row 0 keys differ from original row 0"
        )
        assert torch.equal(entry.past_values[0], original_vals[layer_idx][0]), (
            f"Layer {layer_idx}: compacted row 0 values differ from original row 0"
        )

        # Content check: compacted row 1 == original row 2.
        assert torch.equal(entry.past_keys[1], original_keys[layer_idx][2]), (
            f"Layer {layer_idx}: compacted row 1 keys differ from original row 2"
        )
        assert torch.equal(entry.past_values[1], original_vals[layer_idx][2]), (
            f"Layer {layer_idx}: compacted row 1 values differ from original row 2"
        )
