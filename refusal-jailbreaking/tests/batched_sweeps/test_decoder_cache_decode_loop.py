"""Stage 4: _get_decoder_vectors is called once per forward pass (not per hook firing).

Asserts that across 1 prefill_batched + 5 decode_step_batched calls, the total
number of `_get_decoder_vectors` calls equals exactly 6 (once per forward pass
per layer-with-interventions), not 6 x n_hook_firings_per_forward.

The savings come from collapsing N hook firings within a single forward into
one fetch, not from sharing across forwards. Each prefill_batched and
decode_step_batched call gets its own hook list and its own cache fill.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import torch

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from transformer_lens import HookedTransformerConfig
from circuit_tracer.replacement_model import ReplacementModel
from circuit_tracer.transcoder import SingleLayerTranscoder, TranscoderSet

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


_PROMPT = torch.tensor([[1, 2, 3, 4, 5]], dtype=torch.long)
# A single-row intervention at layer 1 (so only layer 1 triggers the delta hook).
_INTERVENTION_ROW = [(1, slice(None, None), 3, -1.0)]
_N_DECODE_STEPS = 5


def test_decoder_cache_decode_loop_one_call_per_forward():
    """1 prefill + 5 decode steps: _get_decoder_vectors called exactly 6 times per layer.

    Each prefill_batched and decode_step_batched rebuilds its hook list and its
    per-sub-batch decoder cache, so each forward gets exactly one
    _get_decoder_vectors call per layer-with-interventions. The total count
    is 6 (not 6 * n_hook_firings_per_forward or 6 * n_layers).
    """
    model = _build_tiny_replacement_model()

    call_counter: dict[int, int] = {}
    original_get_decoder_vectors = model.transcoders._get_decoder_vectors

    def counting_get_decoder_vectors(layer_id, feat_ids=None):
        call_counter[layer_id] = call_counter.get(layer_id, 0) + 1
        return original_get_decoder_vectors(layer_id, feat_ids)

    model.transcoders._get_decoder_vectors = counting_get_decoder_vectors

    intervention_lists = [_INTERVENTION_ROW]

    # Prefill (1 forward pass).
    logits_pf, kv_cache = model.prefill_batched(
        _PROMPT,
        intervention_lists,
        freeze_attention=False,
    )

    # 5 decode steps (5 forward passes).
    last_tok = int(logits_pf[0, -1, :].argmax().item())
    for _ in range(_N_DECODE_STEPS):
        new_tok = torch.tensor([[last_tok]], dtype=torch.long)
        dec_logits = model.decode_step_batched(new_tok, intervention_lists, kv_cache)
        last_tok = int(dec_logits[0, 0, :].argmax().item())

    # Only layer 1 has interventions, so only layer 1 should have been called.
    # It should have been called exactly 6 times (1 prefill + 5 decode steps).
    n_forwards = 1 + _N_DECODE_STEPS  # 6

    assert 1 in call_counter, (
        f"_get_decoder_vectors was never called for layer 1 (the intervention layer). "
        f"call_counter={call_counter}"
    )
    assert call_counter[1] == n_forwards, (
        f"Expected {n_forwards} calls to _get_decoder_vectors for layer 1 "
        f"(one per forward pass), got {call_counter[1]}. "
        f"Full counter: {call_counter}"
    )

    # Layer 0 has no interventions; it should not have been called at all.
    assert call_counter.get(0, 0) == 0, (
        f"_get_decoder_vectors was called {call_counter.get(0, 0)} times for layer 0, "
        f"but layer 0 has no interventions. "
        f"Full counter: {call_counter}"
    )
