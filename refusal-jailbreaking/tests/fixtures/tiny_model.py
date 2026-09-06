"""Toy 2-layer transformer + 2-layer toy transcoder for CPU-only tests.

Designed to be interface-compatible with the bits of circuit_tracer that
`circuit_oracle.tools._measure_intervention` actually touches, without
requiring transformer_lens, transformers, or any HuggingFace model.

What we mock:
    * A `TinyTokenizer` with a tiny deterministic char vocab.
    * A `TinyReplacementModel` exposing `.feature_intervention(prompt,
      interventions, freeze_attention, return_activations)` with the
      same `(logits, None)` return shape as the real one.
    * A `TinyGraph` duck-typed to match `circuit_tracer.graph.Graph`, same attribute names so tools.get_top_logits / get_top_features /
      get_upstream_features all run unchanged.

The transformer is intentionally trivial (random fixed-seed weights, no
real semantics). Its only job is to be *responsive* to transcoder feature
interventions so the determinism family of tests can compare
batched-vs-single outputs to fp32 tolerance.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Sequence, Tuple, Union

import torch
import torch.nn.functional as F
from typing import NamedTuple

# Allow `from tests.fixtures.tiny_model import ...` from the repo root even
# when the package isn't `pip install -e .`'d. Prepends `src/` so
# `circuit_oracle.config` and `circuit_tracer.replacement_model` both
# resolve.
_REPO_ROOT = Path(__file__).resolve().parents[3]
_SRC = _REPO_ROOT / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

# Single-source the batched-return dataclass from the real model so the
# toy's contract can't drift. The real `feature_intervention_batched`
# populates `logits` and `activation_cache`; the toy additionally
# populates `freeze_cache` (per-layer attention patterns for the
# freeze-aliasing test) and `answer_after` (ragged-decode strings).
from circuit_tracer.replacement_model import BatchedInterventionResult

# --- Configuration knobs (kept small so end-to-end runs in <5s on CPU) -----

D_MODEL = 32
D_TRANSCODER = 64
N_LAYERS = 2
N_HEADS = 2
VOCAB_SIZE = 16
MAX_SEQ_LEN = 32
SEED = 1234
DEFAULT_PROMPT = "hello"

InterventionTuple = Tuple[int, Union[int, slice], int, float]


# ---------------------------------------------------------------------------
# Fake KV-cache for TinyReplacementModel
#
# _decode_one_chunk now calls model.prefill_batched(...) and
# model.decode_step_batched(...) instead of feature_intervention_batched.
# The tiny model does not have a real KV cache, so we provide a lightweight
# stand-in that satisfies the _compact_kv_cache interface and the assertions
# inside _decode_one_chunk:
#
#   cache.entries[0].past_keys.shape[0] == B_active
#   cache.previous_attention_mask.shape[0] == B_active
#
# CRITICAL design: token IDs are stored INSIDE `past_keys` using shape
# [B, T, 1, 1] where past_keys[b, t, 0, 0] encodes the token ID at position t
# for row b. This means when _compact_kv_cache does
#   entry.past_keys = entry.past_keys[keep_local]
# the token ID state for surviving rows is correctly compacted in lockstep,
# without any separate accumulated_ids tensor that could drift out of sync.
#
# decode_step_batched extracts the accumulated sequence from
# cache.entries[0].past_keys[:, :, 0, 0].long(), appends the new token, runs
# a full re-forward (no real KV cache, just re-compute everything), updates
# past_keys with the new accumulated sequence, and returns logits[:, -1:, :].
# ---------------------------------------------------------------------------

@dataclass
class _TinyKVCacheEntry:
    """Minimal cache entry for TinyReplacementModel.

    past_keys encodes the accumulated token sequence:
        past_keys[b, t, 0, 0] = float(token_id_at_position_t_for_row_b)
    After _compact_kv_cache applies entry.past_keys = entry.past_keys[keep_local],
    the surviving rows retain their correct token ID sequences.
    """
    past_keys: torch.Tensor    # shape [B, T, 1, 1], encodes token IDs as float
    past_values: torch.Tensor  # shape [B, T, 1, 1], unused dummy


@dataclass
class _TinyKVCache:
    """Fake KV cache for TinyReplacementModel.

    All sequence state lives inside entries[*].past_keys so that
    _compact_kv_cache (the real function from circuit_tracer.replacement_model)
    correctly compacts the token ID state in lockstep with active_to_original.
    """
    entries: List[_TinyKVCacheEntry]
    previous_attention_mask: torch.Tensor  # shape [B, T], all ones

    @classmethod
    def build(cls, accumulated_ids: torch.Tensor) -> "_TinyKVCache":
        """Build a _TinyKVCache from accumulated token IDs [B, T]."""
        B, T = accumulated_ids.shape
        # Encode token IDs as float in past_keys. Use N_LAYERS entries to
        # mirror the real cache; _decode_one_chunk's assertion checks [0].
        keys = accumulated_ids.float().unsqueeze(-1).unsqueeze(-1)  # [B, T, 1, 1]
        entries = [
            _TinyKVCacheEntry(
                past_keys=keys.clone(),
                past_values=torch.zeros(B, T, 1, 1),
            )
            for _ in range(N_LAYERS)
        ]
        mask = torch.ones(B, T, dtype=torch.long)
        return cls(entries=entries, previous_attention_mask=mask)

    def get_accumulated_ids(self) -> torch.Tensor:
        """Recover accumulated token IDs from entries[0].past_keys."""
        return self.entries[0].past_keys[:, :, 0, 0].long()  # [B, T]

    def update_with_new_token(self, new_ids: torch.Tensor) -> None:
        """Append [B, 1] new token IDs and update all entries and the mask."""
        old_ids = self.get_accumulated_ids()  # [B, T]
        full_ids = torch.cat([old_ids, new_ids], dim=1)  # [B, T+1]
        B, T1 = full_ids.shape
        keys = full_ids.float().unsqueeze(-1).unsqueeze(-1)  # [B, T+1, 1, 1]
        for entry in self.entries:
            entry.past_keys = keys.clone()
            entry.past_values = torch.zeros(B, T1, 1, 1)
        self.previous_attention_mask = torch.ones(B, T1, dtype=torch.long)


# ---------------------------------------------------------------------------
# Batched-API helpers
# ---------------------------------------------------------------------------


class SingleInterventionResult(NamedTuple):
    """Result of feature_intervention on the toy model.

    NamedTuple so existing `logits, acts = model.feature_intervention(...)`
    unpacking still works (tools.py uses it) while tests can access
    `result.logits` directly.
    """

    logits: torch.Tensor
    activations: object


def _normalize_intervention_row(row) -> list[Tuple[int, Union[int, slice], int, float]]:
    """Normalize a row to canonical 4-tuples ``(layer, pos, feature_idx, value)``.

    Accepts both dict form ``{"layer", "feature_idx", "pos", "value"}`` and
    tuple form. The internal code path here and on the real model expects
    tuples (see ``circuit_tracer.replacement_model._get_feature_intervention_hooks_batched``
    line 755), so we normalize once at the public boundary and keep the toy
    no more permissive than reality.
    """
    out: list[Tuple[int, Union[int, slice], int, float]] = []
    for tup in row:
        if isinstance(tup, dict):
            layer = int(tup["layer"])
            feature_idx = int(tup["feature_idx"])
            pos = tup["pos"]
            value = float(tup["value"])
            if isinstance(pos, int):
                pos = int(pos)
            out.append((layer, pos, feature_idx, value))
        else:
            layer, pos, feature_idx, value = tup
            layer = int(layer)
            feature_idx = int(feature_idx)
            if isinstance(pos, int):
                pos = int(pos)
            value = float(value)
            out.append((layer, pos, feature_idx, value))
    return out


def _validate_no_conflicting_tuples(intervention_lists) -> None:
    """Build-time invariant of the batched hook builder.

    Within one row, each (layer, feature_idx, pos) coordinate may appear at
    most once. Duplicates with conflicting values are rejected loudly so
    silent last-write-wins cannot happen. Assumes rows have already been
    normalized to canonical 4-tuples by `_normalize_intervention_row`.
    """
    for row_idx, row in enumerate(intervention_lists):
        seen: dict[tuple, float] = {}
        for layer, pos, feature_idx, value in row:
            pos_key = pos if isinstance(pos, int) else (
                ("slice", pos.start, pos.stop, pos.step)
                if isinstance(pos, slice) else str(pos)
            )
            key = (int(layer), int(feature_idx), pos_key)
            v = float(value)
            if key in seen and seen[key] != v:
                raise ValueError(
                    f"conflicting intervention tuples in row {row_idx}: "
                    f"(layer={layer}, feature_idx={feature_idx}, pos={pos}) "
                    f"appears with both value={seen[key]} and value={v}"
                )
            seen[key] = v




# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

class TinyTokenizer:
    """Char-level tokenizer over a 16-char vocab. Token 0 is reserved for EOS."""

    def __init__(self) -> None:
        chars = list("abcdefghijklmno")  # 15 printable chars + EOS = 16
        self.eos_token_id = 0
        self.bos_token_id = None
        self.pad_token_id = 0
        self.vocab = {"<eos>": 0}
        for i, ch in enumerate(chars, start=1):
            self.vocab[ch] = i
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        self.vocab_size = len(self.vocab)

    def encode(self, text: str) -> List[int]:
        ids = []
        for ch in text:
            ids.append(self.vocab.get(ch, 1))  # unknown -> 'a'
        return ids

    def __call__(self, text: str, return_tensors: str | None = None):
        ids = self.encode(text)
        if return_tensors == "pt":
            return {"input_ids": torch.tensor([ids], dtype=torch.long)}
        return {"input_ids": ids}

    def decode(self, ids, skip_special_tokens: bool = False) -> str:
        if isinstance(ids, torch.Tensor):
            ids = ids.tolist()
        if isinstance(ids, int):
            ids = [ids]
        out = []
        for tid in ids:
            tok = self.inv_vocab.get(int(tid), "?")
            if skip_special_tokens and tok in ("<eos>",):
                continue
            if tok == "<eos>":
                out.append("")
            else:
                out.append(tok)
        return "".join(out)


# ---------------------------------------------------------------------------
# Toy transformer + transcoder
# ---------------------------------------------------------------------------

class _TinyAttention(torch.nn.Module):
    """Single-head-style attention (multi-head folded into one for simplicity)."""

    def __init__(self, d_model: int, n_heads: int) -> None:
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.qkv = torch.nn.Linear(d_model, 3 * d_model, bias=False)
        self.out = torch.nn.Linear(d_model, d_model, bias=False)

    def forward(self, x: torch.Tensor, frozen_pattern: torch.Tensor | None = None) -> torch.Tensor:
        # x: [B, T, D]
        B, T, D = x.shape
        qkv = self.qkv(x)  # [B, T, 3D]
        q, k, v = qkv.chunk(3, dim=-1)
        scale = D ** -0.5
        scores = (q @ k.transpose(-2, -1)) * scale  # [B, T, T]
        mask = torch.triu(torch.ones(T, T, device=x.device, dtype=torch.bool), diagonal=1)
        scores = scores.masked_fill(mask, float("-inf"))
        if frozen_pattern is not None:
            pattern = frozen_pattern
        else:
            pattern = F.softmax(scores, dim=-1)
        out = pattern @ v
        return self.out(out), pattern


class _TinyTranscoder(torch.nn.Module):
    """Sparse-ish overcomplete projection. Acts as the MLP for a layer.

    Encoder: d_model -> d_transcoder with ReLU. Decoder: d_transcoder -> d_model.
    The encoder output is what `feature_intervention` patches.
    """

    def __init__(self, d_model: int, d_transcoder: int) -> None:
        super().__init__()
        self.encoder = torch.nn.Linear(d_model, d_transcoder, bias=True)
        self.decoder = torch.nn.Linear(d_transcoder, d_model, bias=False)

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        return F.relu(self.encoder(x))

    def decode(self, feats: torch.Tensor) -> torch.Tensor:
        return self.decoder(feats)

    def forward(self, x: torch.Tensor, patch: torch.Tensor | None = None) -> Tuple[torch.Tensor, torch.Tensor]:
        feats = self.encode(x)
        if patch is not None:
            feats = patch  # full override (already merged with baseline by caller)
        return self.decode(feats), feats


class TinyTransformer(torch.nn.Module):
    """A toy 2-layer transformer whose MLPs are replaced by transcoders.

    Hardcoded to N_LAYERS = 2, D_MODEL = 32, D_TRANSCODER = 64, VOCAB = 16.
    Weights live in float64 so the batched-vs-single determinism family of
    tests sees results equal to <1e-5 rtol regardless of which BLAS kernel
    torch picks for the different batch shapes.
    """

    def __init__(self, d_model: int = D_MODEL, d_transcoder: int = D_TRANSCODER,
                 n_layers: int = N_LAYERS, n_heads: int = N_HEADS,
                 vocab_size: int = VOCAB_SIZE, max_seq_len: int = MAX_SEQ_LEN,
                 seed: int = SEED) -> None:
        super().__init__()
        gen = torch.Generator().manual_seed(seed)
        # Fresh seed so weight init is deterministic and not contaminated by
        # any prior torch.manual_seed calls in the test runner.
        torch.manual_seed(seed)
        self.cfg = _TinyCfg(n_layers=n_layers, d_model=d_model,
                            d_transcoder=d_transcoder, vocab_size=vocab_size)
        self.d_model = d_model
        self.d_transcoder = d_transcoder
        self.n_layers = n_layers
        self.vocab_size = vocab_size
        self.max_seq_len = max_seq_len

        self.embed = torch.nn.Embedding(vocab_size, d_model)
        self.pos_embed = torch.nn.Embedding(max_seq_len, d_model)
        self.layers = torch.nn.ModuleList([
            torch.nn.ModuleDict({
                "attn": _TinyAttention(d_model, n_heads),
                "ln1": torch.nn.LayerNorm(d_model),
                "ln2": torch.nn.LayerNorm(d_model),
                "transcoder": _TinyTranscoder(d_model, d_transcoder),
            }) for _ in range(n_layers)
        ])
        self.ln_final = torch.nn.LayerNorm(d_model)
        self.unembed = torch.nn.Linear(d_model, vocab_size, bias=False)

        # Re-init weights with the same generator so re-instantiating the
        # model gives byte-identical weights every time.
        with torch.no_grad():
            for p in self.parameters():
                p.uniform_(-0.5, 0.5, generator=gen)

        # Convert all weights and buffers to float64. Single-vs-batched
        # matmul kernels can differ in fp32 accumulation order by ~1e-7
        # absolute and ~1e-4 relative when one input is small; that's
        # tighter than the test rtol=1e-5. fp64 closes the gap.
        self.to(torch.float64)

        self.eval()
        # Disable grad globally on the toy, it's only ever used at inference.
        for p in self.parameters():
            p.requires_grad_(False)

    def _forward_residual(self, input_ids: torch.Tensor,
                          interventions_by_layer: dict[int, list[InterventionTuple]] | None,
                          freeze_attention: bool,
                          capture_acts: bool,
                          frozen_attn_patterns: list[torch.Tensor] | None = None,
                          ) -> Tuple[torch.Tensor, list[torch.Tensor], list[torch.Tensor]]:
        """One full forward. Returns (logits, captured_acts, captured_patterns).

        interventions_by_layer: dict mapping layer -> list of (pos_spec, feature_idx, new_value).
            pos_spec may be int or slice. For each (layer, pos, feat_idx),
            the post-relu transcoder activation at that position is set to
            new_value before the decoder is applied.
        """
        B, T = input_ids.shape
        positions = torch.arange(T, device=input_ids.device).unsqueeze(0).expand(B, T)
        x = self.embed(input_ids) + self.pos_embed(positions)

        captured_acts: list[torch.Tensor] = []
        captured_patterns: list[torch.Tensor] = []
        for layer_idx, block in enumerate(self.layers):
            # Attention
            normed = block["ln1"](x)
            given_pattern = (frozen_attn_patterns[layer_idx]
                             if (freeze_attention and frozen_attn_patterns is not None)
                             else None)
            attn_out, pattern = block["attn"](normed, frozen_pattern=given_pattern)
            captured_patterns.append(pattern)
            x = x + attn_out

            # MLP = transcoder. Compute pre-intervention activations.
            normed2 = block["ln2"](x)
            feats = block["transcoder"].encode(normed2)  # [B, T, d_transcoder]
            if capture_acts:
                captured_acts.append(feats.detach().clone())
            if interventions_by_layer and layer_idx in interventions_by_layer:
                for pos_spec, feature_idx, new_value in interventions_by_layer[layer_idx]:
                    # Broadcast the new value across rows; pos_spec may be int or slice.
                    feats[:, pos_spec, feature_idx] = float(new_value)
            mlp_out = block["transcoder"].decode(feats)
            x = x + mlp_out

        x = self.ln_final(x)
        logits = self.unembed(x)
        return logits, captured_acts, captured_patterns

    def _batched_forward(
        self,
        batched_ids: torch.Tensor,
        per_row_by_layer: list[dict[int, list[InterventionTuple]]],
        freeze_attention: bool,
        frozen_attn_patterns: list[torch.Tensor] | None,
    ) -> Tuple[torch.Tensor, list[torch.Tensor], list[torch.Tensor]]:
        """Forward pass with per-row interventions applied via per-row indexing.

        Mirrors the real replacement model's contract: row b sees only per_row_by_layer[b]'s
        interventions, never the union across rows.
        """
        B, T = batched_ids.shape
        positions = torch.arange(T, device=batched_ids.device).unsqueeze(0).expand(B, T)
        x = self.embed(batched_ids) + self.pos_embed(positions)

        captured_acts: list[torch.Tensor] = []
        captured_patterns: list[torch.Tensor] = []
        for layer_idx, block in enumerate(self.layers):
            normed = block["ln1"](x)
            given_pattern = (frozen_attn_patterns[layer_idx]
                             if (freeze_attention and frozen_attn_patterns is not None)
                             else None)
            attn_out, pattern = block["attn"](normed, frozen_pattern=given_pattern)
            captured_patterns.append(pattern)
            x = x + attn_out

            normed2 = block["ln2"](x)
            feats = block["transcoder"].encode(normed2)  # [B, T, d_transcoder]
            captured_acts.append(feats.detach().clone())
            # Per-row indexing: feats[b] sees only row b's interventions.
            for b in range(B):
                row_layer_tuples = per_row_by_layer[b].get(layer_idx, [])
                for pos_spec, feature_idx, new_value in row_layer_tuples:
                    feats[b, pos_spec, feature_idx] = float(new_value)
            mlp_out = block["transcoder"].decode(feats)
            x = x + mlp_out

        x = self.ln_final(x)
        logits = self.unembed(x)
        return logits, captured_acts, captured_patterns


@dataclass
class _TinyCfg:
    n_layers: int
    d_model: int
    d_transcoder: int
    vocab_size: int
    device: str = "cpu"


# ---------------------------------------------------------------------------
# Graph stand-in
# ---------------------------------------------------------------------------

@dataclass
class TinyGraph:
    """Duck-typed to circuit_tracer.graph.Graph for the attrs tools.py reads.

    Layout mirrors the real Graph:
        nodes = [active_features..., error_nodes..., embed_nodes..., logit_nodes...]
    """
    input_string: str
    input_tokens: torch.Tensor
    active_features: torch.Tensor      # [n_active, 3] (layer, pos, feature_idx)
    adjacency_matrix: torch.Tensor     # [n_nodes, n_nodes]
    cfg: _TinyCfg
    logit_tokens: torch.Tensor
    logit_probabilities: torch.Tensor
    selected_features: torch.Tensor    # indices into active_features
    activation_values: torch.Tensor    # [n_active]
    scan: str | None = "tiny-fixture"
    n_pos: int = 0

    def __post_init__(self):
        self.n_pos = int(self.input_tokens.shape[0])


# ---------------------------------------------------------------------------
# Replacement-model stand-in
# ---------------------------------------------------------------------------

class TinyReplacementModel:
    """Wraps TinyTransformer with the small slice of ReplacementModel API used
    by `circuit_oracle.tools._measure_intervention`:

        * `.tokenizer`
        * `.cfg.device`
        * `.feature_intervention(prompt, interventions, freeze_attention=, return_activations=)`
          -> (logits, activations_or_None)
        * `.get_activations(prompt)` -> (logits, baseline_activations [n_layers, T, d_transcoder])
        * `.generate(input_ids, max_new_tokens=, ...)` -> output_ids
    """

    def __init__(self, transformer: TinyTransformer, tokenizer: TinyTokenizer) -> None:
        self.model = transformer
        self.tokenizer = tokenizer
        self.cfg = transformer.cfg
        self._frozen_pattern_cache: dict[str, list[torch.Tensor]] = {}

    # -- helpers -----------------------------------------------------------

    def _tokenize(self, prompt: str | torch.Tensor) -> torch.Tensor:
        """Tokenize, prepending a BOS-style token to mirror ReplacementModel.

        The real model prepends a special token via `ensure_tokenized` so
        that position 0 is BOS and content tokens start at position 1. The
        toy mirrors this so tests authored against the real-model convention
        (e.g. `pos=5` on a 5-char prompt) hit valid positions.
        """
        if isinstance(prompt, torch.Tensor):
            if prompt.ndim == 1:
                return prompt.unsqueeze(0)
            return prompt
        ids = self.tokenizer.encode(prompt)
        bos = self.tokenizer.eos_token_id
        if bos is not None and (not ids or ids[0] != bos):
            ids = [bos] + ids
        return torch.tensor([ids], dtype=torch.long)

    def _interventions_by_layer(self, interventions
                                ) -> dict[int, list[Tuple[Any, int, float]]]:
        """Group canonical 4-tuples into a per-layer dict.

        Mirrors `circuit_tracer.replacement_model._get_feature_intervention_hooks`
        line 602-604. Accepts only canonical 4-tuples
        ``(layer, pos, feature_idx, value)``, dict-form input must be
        normalized by ``_normalize_intervention_row`` first (the public
        entry points do this for you).
        """
        by_layer: dict[int, list[Tuple[Any, int, float]]] = {}
        for layer, pos_spec, feature_idx, value in interventions:
            by_layer.setdefault(int(layer), []).append(
                (pos_spec, int(feature_idx), float(value))
            )
        return by_layer

    def _get_frozen_pattern(self, prompt: str | torch.Tensor) -> list[torch.Tensor]:
        """Cache the attention pattern from a clean forward, keyed by prompt string."""
        key = prompt if isinstance(prompt, str) else "tensor:" + str(prompt.tolist())
        if key in self._frozen_pattern_cache:
            return self._frozen_pattern_cache[key]
        input_ids = self._tokenize(prompt)
        with torch.no_grad():
            _, _, patterns = self.model._forward_residual(
                input_ids, interventions_by_layer=None, freeze_attention=False,
                capture_acts=False,
            )
        cached = [p.detach().clone() for p in patterns]
        self._frozen_pattern_cache[key] = cached
        return cached

    # -- public API used by tools.py --------------------------------------

    def feature_intervention(self, inputs, interventions,
                             freeze_attention: bool = True,
                             return_activations: bool = True,
                             **_ignored):
        """Single-prompt intervention.

        Returns logits shape `[1, T, V]` (matches the real ReplacementModel)
        and optional activations stacked as `[n_layers, T, d_transcoder]`.

        Normalizes the input row to canonical 4-tuples
        ``(layer, pos, feature_idx, value)`` at the boundary so all internal
        code paths see only tuples, no more permissive than the real model.
        """
        input_ids = self._tokenize(inputs)
        normalized = _normalize_intervention_row(interventions)
        by_layer = self._interventions_by_layer(normalized)
        frozen = self._get_frozen_pattern(inputs) if freeze_attention else None
        with torch.no_grad():
            logits, acts, _ = self.model._forward_residual(
                input_ids, interventions_by_layer=by_layer,
                freeze_attention=freeze_attention,
                capture_acts=return_activations,
                frozen_attn_patterns=frozen,
            )
        if return_activations:
            stacked = torch.stack([a[0] for a in acts], dim=0)
            return SingleInterventionResult(logits=logits, activations=stacked)
        return SingleInterventionResult(logits=logits, activations=None)

    def feature_intervention_batched(
        self,
        inputs,
        intervention_lists,
        *,
        freeze_attention: bool = True,
        return_activations: bool = False,
        return_freeze_cache: bool = False,
        answer_max_tokens: int | None = None,
        **_ignored,
    ):
        """Batched per-row intervention symmetric with feature_intervention.

        Each row b sees only intervention_lists[b] applied to the shared prompt.
        Frozen attention pattern is expanded across the batch via .expand() so
        the freeze cache aliases storage across rows.
        """
        # Normalize at the boundary: convert dict-form or tuple-form rows to
        # canonical 4-tuples ``(layer, pos, feature_idx, value)``. After this
        # point the internal code path (validate / prefetch / per-layer
        # grouping) sees only tuples, matching the real model invariant.
        normalized_lists = [_normalize_intervention_row(row) for row in intervention_lists]

        # Build-time invariant: within one row, each (layer, feature_idx, pos)
        # pair must be unique. Repeats with conflicting values are loud errors.
        _validate_no_conflicting_tuples(normalized_lists)

        input_ids = self._tokenize(inputs)  # [1, T]
        B = len(normalized_lists)
        # Expand the prompt across the batch dim as a view. .expand is a
        # zero-copy stride-aware broadcast, exactly the storage-aliasing path
        # the freeze-cache test asserts.
        batched_ids = input_ids.expand(B, -1)

        per_row_by_layer: list[dict[int, list]] = []
        for row in normalized_lists:
            per_row_by_layer.append(self._interventions_by_layer(row))

        frozen_pattern: list[torch.Tensor] | None = None
        if freeze_attention:
            single_frozen = self._get_frozen_pattern(inputs)
            # Each layer's pattern is [1, T, T]; expand across B as a view.
            frozen_pattern = [p.expand(B, *p.shape[1:]) for p in single_frozen]

        freeze_cache: dict[str, torch.Tensor] = {}
        if freeze_attention and return_freeze_cache:
            for i, p in enumerate(frozen_pattern):  # type: ignore[arg-type]
                freeze_cache[f"layer.{i}.hook_pattern"] = p

        # One batched residual forward, per-row intervention applied inside.
        # Output `logits` is `[B, T, V]`, matching the real
        # `ReplacementModel.feature_intervention_batched` contract. The
        # single-prompt path returns `[1, T, V]`, so per-row parity tests
        # compare `batched.logits[row_idx]` against `single.logits[0]`.
        with torch.no_grad():
            logits, _, _ = self.model._batched_forward(
                batched_ids,
                per_row_by_layer=per_row_by_layer,
                freeze_attention=freeze_attention,
                frozen_attn_patterns=frozen_pattern,
            )

        # Optional ragged decode: each row continues independently to
        # answer_max_tokens. EOS-break is removed; per-row EOS trim happens
        # in post-processing.
        answer_after: list[str] | None = None
        if answer_max_tokens is not None:
            answer_after = self._batched_decode(
                batched_ids, per_row_by_layer, answer_max_tokens
            )

        # `activation_cache=None`: the toy's batched path doesn't expose
        # feature activations (the real model's analogue is populated only
        # when `return_activations=True`, which this toy path never sets).
        return BatchedInterventionResult(
            logits=logits,
            activation_cache=None,
            freeze_cache=freeze_cache if return_freeze_cache else {},
            answer_after=answer_after,
        )

    def prefill_batched(
        self,
        inputs,
        intervention_lists,
        *,
        freeze_attention: bool = True,
        return_activations: bool = False,
        **_ignored,
    ):
        """KV-cache prefill stub for TinyReplacementModel.

        Runs the same batched forward as feature_intervention_batched, then
        wraps the prompt token IDs in a _TinyKVCache so that decode_step_batched
        can recover the accumulated sequence from the cache entries. The token
        IDs are encoded as float in entries[*].past_keys so that
        _compact_kv_cache (the real function) correctly compacts the sequence
        state in lockstep with active_to_original.

        Returns (logits [B, T_prompt, V], _TinyKVCache).
        """
        normalized_lists = [_normalize_intervention_row(row) for row in intervention_lists]
        _validate_no_conflicting_tuples(normalized_lists)

        if isinstance(inputs, torch.Tensor):
            if inputs.ndim == 1:
                input_ids = inputs.unsqueeze(0)
            elif inputs.shape[0] == 1:
                # [1, T] -- single shared prompt
                input_ids = inputs
            else:
                # [B, T] -- already batched (may happen in tests that expand prompt)
                input_ids = inputs[:1]  # use first row as the shared prompt
        else:
            input_ids = self._tokenize(inputs)  # [1, T]

        B = len(normalized_lists)
        batched_ids = input_ids.expand(B, -1).contiguous()

        per_row_by_layer: list[dict[int, list]] = [
            self._interventions_by_layer(row) for row in normalized_lists
        ]
        frozen_pattern: list[torch.Tensor] | None = None
        if freeze_attention:
            single_frozen = self._get_frozen_pattern(
                inputs if isinstance(inputs, str) else input_ids
            )
            frozen_pattern = [p.expand(B, *p.shape[1:]) for p in single_frozen]

        with torch.no_grad():
            logits, _, _ = self.model._batched_forward(
                batched_ids,
                per_row_by_layer=per_row_by_layer,
                freeze_attention=freeze_attention,
                frozen_attn_patterns=frozen_pattern,
            )

        # Build the fake KV cache. Token IDs are stored in past_keys so that
        # _compact_kv_cache compacts them correctly.
        kv_cache = _TinyKVCache.build(batched_ids)
        return logits, kv_cache

    def decode_step_batched(
        self,
        new_token_ids: torch.Tensor,
        intervention_lists,
        past_kv_cache: "_TinyKVCache",
        **_ignored,
    ) -> torch.Tensor:
        """KV-cache decode step stub for TinyReplacementModel.

        Recovers the full accumulated sequence from past_kv_cache.entries[0].past_keys,
        appends new_token_ids, runs a full re-forward (no actual KV reuse -- this
        is a correctness-only shim), updates the cache with the extended sequence,
        and returns logits of shape [B, 1, V].

        Note: After _compact_kv_cache(kv_cache, keep_local) is called by
        _decode_one_chunk, the accumulated sequence in entries[0].past_keys is
        already correctly compacted, so the B here matches the compacted batch.
        """
        normalized_lists = [_normalize_intervention_row(row) for row in intervention_lists]
        B = len(normalized_lists)

        # Recover accumulated sequence from the cache (token IDs stored as float).
        accumulated_ids = past_kv_cache.get_accumulated_ids()  # [B, T_so_far]
        full_ids = torch.cat([accumulated_ids, new_token_ids], dim=1)  # [B, T_so_far+1]

        per_row_by_layer: list[dict[int, list]] = [
            self._interventions_by_layer(row) for row in normalized_lists
        ]

        with torch.no_grad():
            logits, _, _ = self.model._batched_forward(
                full_ids,
                per_row_by_layer=per_row_by_layer,
                freeze_attention=False,
                frozen_attn_patterns=None,
            )

        # Update the cache to include the new token's position.
        past_kv_cache.update_with_new_token(new_token_ids)

        # Return only the last position's logits, shape [B, 1, V].
        return logits[:, -1:, :]

    def _batched_decode(
        self,
        batched_ids: torch.Tensor,
        per_row_by_layer: list[dict[int, list]],
        answer_max_tokens: int,
    ) -> list[str]:
        """Greedy ragged decode with per-row interventions, no early EOS break.

        Always decodes to answer_max_tokens; EOS trim happens per row at the
        end so the batch can run unsplit.
        """
        B, _ = batched_ids.shape
        cur = batched_ids.clone()
        # Track per-row whether EOS was hit; once hit, no further tokens are
        # appended for that row's answer string (but the batch keeps stepping).
        eos_pos = [None] * B
        per_row_generated: list[list[int]] = [[] for _ in range(B)]

        eos_id = self.tokenizer.eos_token_id
        for step in range(answer_max_tokens):
            with torch.no_grad():
                logits, _, _ = self.model._batched_forward(
                    cur,
                    per_row_by_layer=per_row_by_layer,
                    freeze_attention=False,
                    frozen_attn_patterns=None,
                )
            next_ids = logits[:, -1, :].argmax(dim=-1)  # [B]
            cur = torch.cat([cur, next_ids.unsqueeze(-1)], dim=1)
            for b in range(B):
                if eos_pos[b] is not None:
                    continue
                tok = int(next_ids[b].item())
                if eos_id is not None and tok == eos_id:
                    eos_pos[b] = step
                    continue
                per_row_generated[b].append(tok)

        return [
            self.tokenizer.decode(ids, skip_special_tokens=True)
            for ids in per_row_generated
        ]

    def get_activations(self, prompt):
        return self.feature_intervention(prompt, interventions=[],
                                         freeze_attention=False,
                                         return_activations=True)

    def generate(self, input_ids: torch.Tensor, max_new_tokens: int = 20,
                 stop_at_eos: bool = True, **_ignored) -> torch.Tensor:
        cur = input_ids
        for _ in range(max_new_tokens):
            with torch.no_grad():
                logits, _, _ = self.model._forward_residual(
                    cur, interventions_by_layer=None,
                    freeze_attention=False, capture_acts=False,
                )
            nxt = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            cur = torch.cat([cur, nxt], dim=1)
            if stop_at_eos and int(nxt.item()) == self.tokenizer.eos_token_id:
                break
        return cur


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def _build_tiny_graph(model: TinyReplacementModel, prompt: str,
                      n_active: int = 8, n_logits: int = 5) -> TinyGraph:
    """Run one clean forward, harvest the top transcoder activations as
    `active_features`, and assemble a Graph-shaped object."""
    tokenizer = model.tokenizer
    input_ids = model._tokenize(prompt)[0]
    n_pos = int(input_ids.shape[0])
    cfg = model.cfg

    # Capture per-layer transcoder activations.
    _, baseline_acts = model.get_activations(prompt)  # [n_layers, T, d_transcoder]

    # Pick the top-n_active (layer, pos, feature_idx) cells by activation magnitude.
    flat = baseline_acts.abs().reshape(-1)
    top_vals, top_idx = flat.topk(min(n_active, flat.numel()))
    active_features = []
    activation_values = []
    n_layers, T, d_trans = baseline_acts.shape
    for ti, tv in zip(top_idx.tolist(), top_vals.tolist()):
        layer = ti // (T * d_trans)
        rest = ti % (T * d_trans)
        pos = rest // d_trans
        feat = rest % d_trans
        active_features.append([layer, pos, feat])
        activation_values.append(baseline_acts[layer, pos, feat].item())

    active_features_t = torch.tensor(active_features, dtype=torch.long)
    activation_values_t = torch.tensor(activation_values, dtype=torch.float32)
    selected_features = torch.arange(len(active_features), dtype=torch.long)

    # Logit tokens: top-k argmax from final-position logits.
    with torch.no_grad():
        logits, _, _ = model.model._forward_residual(
            input_ids.unsqueeze(0), interventions_by_layer=None,
            freeze_attention=False, capture_acts=False,
        )
    last_logits = logits[0, -1, :]
    probs = F.softmax(last_logits, dim=-1)
    top_probs, top_ids = probs.topk(min(n_logits, probs.numel()))

    # Adjacency matrix layout: [feats, errors, embeds, logits].
    n_feats = len(active_features)
    n_errors = cfg.n_layers * n_pos
    n_embeds = n_pos
    n_logit_nodes = int(top_ids.numel())
    n_nodes = n_feats + n_errors + n_embeds + n_logit_nodes
    # Random but reproducible adjacency. The tests for upstream tracing
    # just need non-zero entries with a definite ordering.
    gen = torch.Generator().manual_seed(SEED + 7)
    adj = torch.empty(n_nodes, n_nodes).uniform_(-1.0, 1.0, generator=gen)
    # Zero the diagonal, features shouldn't be their own upstreams.
    adj.fill_diagonal_(0.0)

    return TinyGraph(
        input_string=prompt,
        input_tokens=input_ids,
        active_features=active_features_t,
        adjacency_matrix=adj,
        cfg=cfg,
        logit_tokens=top_ids.detach().clone(),
        logit_probabilities=top_probs.detach().clone(),
        selected_features=selected_features,
        activation_values=activation_values_t,
    )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def build_tiny_fixture(prompt: str = DEFAULT_PROMPT, seed: int = SEED) -> Any:
    """Build a fully populated ToolContext for the toy model.

    Returns a `ToolContext` (real one from `circuit_oracle.config`) with:
        * `.replacement_model` = TinyReplacementModel
        * `.tokenizer`        = TinyTokenizer
        * `.graph`            = TinyGraph
        * `.baseline_activations`, `.baseline_answer`, `.baseline_prompt`
    """
    from circuit_oracle.config import ToolContext  # late import; only needed when called

    tokenizer = TinyTokenizer()
    transformer = TinyTransformer(seed=seed)
    rmodel = TinyReplacementModel(transformer, tokenizer)
    graph = _build_tiny_graph(rmodel, prompt)

    # Baseline activations + greedy answer for downstream cache tests.
    _, baseline_acts = rmodel.get_activations(prompt)
    input_ids = rmodel._tokenize(prompt)
    out_ids = rmodel.generate(input_ids, max_new_tokens=8, stop_at_eos=True)
    new_ids = out_ids[0, input_ids.shape[1]:]
    baseline_answer = tokenizer.decode(new_ids, skip_special_tokens=True)

    # Baseline top-5 next-token distribution at the last prompt position,
    # frozen-attention forward (matches tools._topk_from_logits exactly).
    logits, _ = rmodel.feature_intervention(
        prompt, [], freeze_attention=True, return_activations=False,
    )
    probs = F.softmax(logits[0, -1, :].float(), dim=-1)
    top_p, top_i = probs.topk(5)
    baseline_top5 = {
        tokenizer.decode([int(tid.item())]): {"prob": round(float(p.item()), 6)}
        for tid, p in zip(top_i, top_p)
    }

    ctx = ToolContext(
        graph=graph,
        tokenizer=tokenizer,
        neuronpedia_model_id="tiny-toy",
        neuronpedia_sae_id="{layer}-toy-transcoder",
        replacement_model=rmodel,
        baseline_activations=baseline_acts,
        baseline_answer=baseline_answer,
        baseline_prompt=prompt,
        baseline_top5=baseline_top5,
    )
    return ctx


# ---------------------------------------------------------------------------
# Golden capture
# ---------------------------------------------------------------------------

def capture_golden(prompt: str = DEFAULT_PROMPT, seed: int = SEED) -> dict:
    """Run the toy model once and return baseline outputs in the schema
    expected by golden.json: baseline_top5, baseline_answer, baseline_activations.
    """
    ctx = build_tiny_fixture(prompt=prompt, seed=seed)
    rmodel = ctx.replacement_model
    tokenizer = ctx.tokenizer

    # Top-5 next-token distribution at the last prompt position (frozen-attn
    # forward to match how `_measure_intervention` computes baselines).
    logits, _ = rmodel.feature_intervention(prompt, interventions=[],
                                            freeze_attention=True,
                                            return_activations=False)
    probs = F.softmax(logits[0, -1, :].float(), dim=-1)
    top_p, top_i = probs.topk(5)
    baseline_top5 = {
        tokenizer.decode([int(tid.item())]): {"prob": round(float(p.item()), 6)}
        for tid, p in zip(top_i, top_p)
    }

    acts = ctx.baseline_activations  # [n_layers, T, d_transcoder]
    return {
        "prompt": prompt,
        "seed": seed,
        "baseline_top5": baseline_top5,
        "baseline_answer": ctx.baseline_answer,
        "baseline_activations": {
            "shape": list(acts.shape),
            "dtype": str(acts.dtype),
            "sum": round(float(acts.sum().item()), 6),
            "abs_mean": round(float(acts.abs().mean().item()), 6),
            "first_row": [round(float(v), 6) for v in acts[0, 0, :8].tolist()],
        },
    }


if __name__ == "__main__":
    # Used by `make_golden` / direct invocation to regenerate golden.json.
    golden = capture_golden()
    path = Path(__file__).with_name("golden.json")
    with open(path, "w") as f:
        json.dump(golden, f, indent=2, sort_keys=True)
    print(f"wrote {path}")
