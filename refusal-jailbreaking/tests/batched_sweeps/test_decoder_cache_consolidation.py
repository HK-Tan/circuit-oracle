"""Stage 4: decoder vectors are fetched at most once per layer per sub-batch.

Asserts that when `feature_intervention_batched` is called with multiple rows
touching the same layer, `_get_decoder_vectors` is called exactly once for
that layer, with the sorted union of unique feature ids. This replaces the
now-vacuous `test_decoder_prefetch_consolidation.py` which counted calls to
the removed `_load_decoder_vector` symbol.
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


def test_decoder_cache_consolidation_one_call_per_layer():
    """feature_intervention_batched calls _get_decoder_vectors exactly once for
    layer 1 when 4 rows touch layer 1 feature 3 and 2 rows touch layer 1 feature 7.

    The call must supply the sorted union [3, 7], not one call per (layer, feature_idx).
    This is the disk-I/O reduction lock-in test: replacing the per-hook-firing
    fetch with a once-per-sub-batch cache means 1 safetensors open per layer,
    regardless of how many times the hook fires.
    """
    model = _build_tiny_replacement_model()

    calls: list[dict] = []
    original_get_decoder_vectors = model.transcoders._get_decoder_vectors

    def counting_get_decoder_vectors(layer_id, feat_ids=None):
        calls.append({"layer_id": layer_id, "feat_ids": feat_ids})
        return original_get_decoder_vectors(layer_id, feat_ids)

    model.transcoders._get_decoder_vectors = counting_get_decoder_vectors

    # 4 rows touch layer 1 feature 3, 2 additional rows touch layer 1 feature 7.
    # All at position 2 (in-range for our 5-token prompt).
    intervention_lists = [
        [{"layer": 1, "feature_idx": 3, "pos": 2, "value": 0.0}],
        [{"layer": 1, "feature_idx": 3, "pos": 2, "value": -1.0}],
        [{"layer": 1, "feature_idx": 3, "pos": 2, "value": -2.0}],
        [{"layer": 1, "feature_idx": 3, "pos": 2, "value": -3.0}],
        [{"layer": 1, "feature_idx": 7, "pos": 2, "value": -1.0}],
        [{"layer": 1, "feature_idx": 7, "pos": 2, "value": -2.0}],
    ]

    model.feature_intervention_batched(
        inputs=_PROMPT,
        intervention_lists=intervention_lists,
        freeze_attention=False,
        return_activations=False,
    )

    # Filter to calls for layer 1 only.
    layer1_calls = [c for c in calls if c["layer_id"] == 1]

    assert len(layer1_calls) == 1, (
        f"Expected exactly 1 call to _get_decoder_vectors for layer 1, "
        f"got {len(layer1_calls)}: {layer1_calls}"
    )

    # The single call must supply the sorted union of unique feature ids: [3, 7].
    feat_ids_arg = layer1_calls[0]["feat_ids"]
    if isinstance(feat_ids_arg, torch.Tensor):
        feat_ids_list = feat_ids_arg.tolist()
    else:
        feat_ids_list = list(feat_ids_arg)

    assert feat_ids_list == [3, 7], (
        f"Expected _get_decoder_vectors(layer=1, feat_ids=[3, 7]), "
        f"got feat_ids={feat_ids_list}"
    )
