"""Batched feature interventions for the TransformerLens replacement model.

This module is the forward-port of the batched-intervention delta the circuit
oracle causal track runs on. Upstream circuit-tracer exposes a single-row
``feature_intervention`` only. The causal sweep needs ``B`` independent
intervention rows evaluated in one forward pass over a shared prompt, so this
module adds

* ``BatchedInterventionMixin``, four methods mixed into
  ``TransformerLensReplacementModel`` (``_get_feature_intervention_hooks_batched``,
  ``feature_intervention_batched``, ``prefill_batched``, ``decode_step_batched``),
* ``BatchedInterventionResult``, the return type of ``feature_intervention_batched``,
* ``BatchedInterventionBackend``, the structural (Protocol) contract that both the
  real model and the CPU toy fixture in the test suite satisfy,
* ``_normalize_intervention_row``, the dict-row to 4-tuple boundary conversion,
* ``_compact_kv_cache``, in-place KV-cache batch-dim compaction after EOS pruning.

Everything in this file is ours, not upstream. The upstream file
``replacement_model_transformerlens.py`` carries only five small in-place
patches, each tagged with a ``BATCHED PORT (n of 5)`` comment.

Provenance: ported from the pre-v0.3.0 single-file fork
(``circuit_tracer/replacement_model.py``, upstream base ``e49c213c``) onto the
pinned upstream ``v0.5.0`` (``4bb8c0ea10bde09727e14565ec8469656880da53``), which
restructured ``replacement_model.py`` into a package. See PORT-NOTES.md.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from functools import partial
from typing import TYPE_CHECKING, Any, Protocol

import torch
import torch.nn.functional as F
from transformer_lens.cache.key_value_cache import TransformerLensKeyValueCache

# Type-only import of the canonical 4-tuple alias. ``from __future__ import
# annotations`` makes every annotation below a string, so this never runs and
# never creates an import cycle with replacement_model_transformerlens.
#
# A row entry is either that 4-tuple ``(layer, pos, feature_idx, value)`` or the
# dict form with keys ``{"layer", "pos", "feature_idx", "value"}``, which is
# structurally the ``InterventionTuple`` TypedDict declared in
# ``circuit_oracle.tools``. The oracle type is deliberately NOT imported here
# (the pre-port fork did import it under TYPE_CHECKING, giving circuit_tracer a
# reverse dependency on circuit_oracle). circuit_tracer stays standalone.
if TYPE_CHECKING:
    from circuit_tracer.replacement_model.replacement_model_transformerlens import (
        Intervention,
    )


class BatchedInterventionBackend(Protocol):
    """The batched intervention surface used by the circuit oracle causal track.

    A conforming backend accepts a single prompt (or a single tokenized
    input tensor, both shapes are honoured by the existing single-prompt
    path) and a list of per-row intervention lists. Row ``b`` of the
    returned logits is the post-intervention next-token distribution
    obtained by applying ``intervention_lists[b]`` on top of the frozen
    base forward.

    The protocol is structural. The concrete implementation is
    ``BatchedInterventionMixin`` below (real GPU path). Tests use a
    CPU toy-model fixture in ``tests/fixtures``.

    Parameters
    ----------
    inputs
        The shared prompt for all batch rows. The frozen-attention path
        depends on this being identical across rows.
    intervention_lists
        ``B`` lists of intervention rows (4-tuples, or the dict form the
        oracle calls ``InterventionTuple``). Length determines the batch
        size, and per-row indexing inside ``calculate_delta_hook_batched`` is
        what makes row ``b`` see only its own interventions.
    constrained_layers
        Same semantics as the single-prompt path.
    freeze_attention
        Whether to freeze attention patterns and LayerNorm denominators.
        Must be ``True`` for the batched sweep to remain mathematically
        equivalent to ``B`` single-prompt calls with the same prompt.
    apply_activation_function, sparse, return_activations
        Pass-throughs to the underlying replacement-model call.
    """

    def __call__(
        self,
        inputs: Any,
        intervention_lists: Sequence[Sequence[Any]],
        *,
        constrained_layers: range | None = None,
        freeze_attention: bool = True,
        apply_activation_function: bool = True,
        sparse: bool = False,
        return_activations: bool = True,
    ) -> tuple[Any, Any | None]: ...


@dataclass
class BatchedInterventionResult:
    """Return type of ``feature_intervention_batched``.

    ``logits`` has shape ``[B, T, V]``. ``activation_cache`` is the stacked
    feature-activation tensor (across rows) when ``return_activations=True``,
    otherwise ``None``. The two trailing optional fields are populated only by
    the toy fixture (which covers cases the real GPU path does not):
    ``freeze_cache`` carries the per-layer attention pattern dict for the
    freeze-aliasing test, and ``answer_after`` carries per-row decoded
    continuations for the ragged-decode test. The real
    ``feature_intervention_batched`` leaves them as ``None``.
    """

    logits: torch.Tensor
    activation_cache: torch.Tensor | None
    freeze_cache: dict | None = None
    answer_after: list[str] | None = None


def _normalize_intervention_row(row):
    """Normalize a row to canonical 4-tuples ``(layer, pos, feature_idx, value)``.

    The internal hook-builder path iterates 4-tuples
    (``_get_feature_intervention_hooks_batched`` / ``_get_feature_intervention_hooks``),
    so dict-form callers (tests, and programmatic callers using the
    ``InterventionTuple`` TypedDict in ``circuit_oracle.tools``) must be
    normalized at the boundary. Kept module-level so the toy fixture and
    ``circuit_oracle.tools`` can re-use the same shape conversion if desired.
    """
    out = []
    for tup in row:
        if isinstance(tup, dict):
            layer = tup["layer"]
            feature_idx = tup["feature_idx"]
            pos = tup["pos"]
            value = tup["value"]
            out.append((layer, pos, feature_idx, value))
        else:
            out.append(tuple(tup))
    return out


def _compact_kv_cache(
    cache: "TransformerLensKeyValueCache",
    keep_local: "list[int]",
) -> None:
    """Compact a KV cache in place by retaining only the rows in ``keep_local``.

    After EOS pruning removes rows from the active batch, the cache's batch
    dimension must shrink in lockstep with ``interventions_per_row``,
    and ``active_to_original``. This helper applies the same ``keep_local``
    index list to every per-layer K/V tensor.

    Mutates ``cache`` in place. The caller is responsible for compacting all
    other per-batch state (``interventions_per_row``,
    ``active_to_original``) with the same ``keep_local`` list before or after
    calling this function, and for asserting that all three stay in sync.

    Pseudocode::

        for entry in cache.entries:          # one entry per transformer layer
            entry.past_keys   = entry.past_keys[keep_local]    # [B', T, H, D]
            entry.past_values = entry.past_values[keep_local]  # [B', T, H, D]
        cache.previous_attention_mask = cache.previous_attention_mask[keep_local]

    where ``B' = len(keep_local) <= B``.

    Parameters
    ----------
    cache:
        A ``TransformerLensKeyValueCache`` whose ``.entries`` list has one
        ``TransformerLensKeyValueCacheEntry`` per model layer. Each entry
        stores ``past_keys`` and ``past_values`` tensors of shape
        ``[batch, pos_so_far, n_heads, d_head]``.
    keep_local:
        Indices (into the current batch dimension) of rows to retain. Must
        be a subset of ``range(batch_size)``.
    """
    if not keep_local:
        # Compact to empty. Replace each tensor with a zero-row slice so
        # subsequent assertions on cache.entries[0].past_keys.shape[0]
        # return 0 rather than crashing on an empty index list.
        for entry in cache.entries:
            entry.past_keys = entry.past_keys[:0]
            entry.past_values = entry.past_values[:0]
        if cache.previous_attention_mask.numel() > 0:
            cache.previous_attention_mask = cache.previous_attention_mask[:0]
        return

    for entry in cache.entries:
        entry.past_keys = entry.past_keys[keep_local]
        entry.past_values = entry.past_values[keep_local]

    # Also compact the attention mask that the library maintains alongside
    # K/V. It has shape [batch, pos_so_far] and must stay aligned with the
    # entries.
    if cache.previous_attention_mask.shape[0] > 0:
        cache.previous_attention_mask = cache.previous_attention_mask[keep_local]


class BatchedInterventionMixin:
    """Batched-intervention methods mixed into ``TransformerLensReplacementModel``.

    Mixed in ahead of ``HookedTransformer`` in the MRO. It defines no
    ``__init__`` and no state of its own, so instantiation and TransformerLens
    hook setup are untouched. Every method below assumes the host class
    provides the standard replacement-model surface (``self.cfg``,
    ``self.transcoders``, ``self.feature_output_hook``, ``self.hooks``,
    ``self.ensure_tokenized``, ``self.setup_intervention_with_freeze``,
    ``self._get_activation_caching_hooks``).
    """


    def _get_feature_intervention_hooks_batched(
        self,
        inputs: str | torch.Tensor,
        intervention_lists: Sequence[Sequence[Intervention]],
        constrained_layers: range | None = None,
        freeze_attention: bool = True,
        apply_activation_function: bool = True,
        sparse: bool = False,
        return_activations: bool = True,
    ):
        """Batched analogue of _get_feature_intervention_hooks.

        Generalizes `layer_deltas` from [n_layers, n_pos, d_model] to
        [B, n_layers, n_pos, d_model] and indexes per-row inside
        calculate_delta_hook so row b sees only intervention_lists[b]'s
        interventions, never the union across rows.

        Freeze-cache tensors are expanded via .expand(B, *tensor.shape[1:])
        (a zero-memory view), safe because the prompt is identical across
        rows and the attention pattern is read-only.
        """
        B = len(intervention_lists)

        # Build-time invariant: within one row, each (layer, feature_idx, pos)
        # pair must be unique. Repeat with conflicting values is loud.
        for row_idx, row in enumerate(intervention_lists):
            seen: dict[tuple, float] = {}
            for layer, pos, feature_idx, value in row:
                pos_key = pos if isinstance(pos, int) else (
                    ("slice", pos.start, pos.stop, pos.step)
                    if isinstance(pos, slice) else str(pos)
                )
                key = (int(layer), int(feature_idx), pos_key)
                v = float(value) if not isinstance(value, torch.Tensor) else float(value.item())
                if key in seen and seen[key] != v:
                    raise ValueError(
                        f"conflicting intervention tuples in row {row_idx}: "
                        f"(layer={layer}, feature_idx={feature_idx}, pos={pos}) "
                        f"appears with both value={seen[key]} and value={v}"
                    )
                seen[key] = v

        # Group interventions per row, per layer (mirrors the single-prompt
        # path's interventions_by_layer dict, lifted by a row dim).
        per_row_by_layer: list[dict[int, list]] = [defaultdict(list) for _ in range(B)]
        for b, row in enumerate(intervention_lists):
            for layer, pos, feature_idx, value in row:
                per_row_by_layer[b][int(layer)].append((pos, feature_idx, value))
        union_by_layer: dict[int, list] = defaultdict(list)
        for b, row in enumerate(intervention_lists):
            for layer, pos, feature_idx, value in row:
                union_by_layer[int(layer)].append((b, pos, feature_idx, value))

        # Build per-layer decoder vector cache. One safetensors open per layer
        # per sub-batch, regardless of how many times the hook fires later.
        # Sorted, deduplicated feature ids are required by searchsorted in the hook.
        unique_feat_ids_by_layer: dict[int, torch.Tensor] = {}
        decoder_vectors_by_layer: dict[int, torch.Tensor] = {}
        for layer, union in union_by_layer.items():
            feat_set = sorted({int(fid) for (_b, _pos, fid, _v) in union})
            unique = torch.tensor(feat_set, dtype=torch.long)
            unique_feat_ids_by_layer[layer] = unique
            decoder_vectors_by_layer[layer] = self.transcoders._get_decoder_vectors(
                layer, unique
            )

        if (freeze_attention or constrained_layers) and any(intervention_lists):
            original_activations, freeze_hooks = self.setup_intervention_with_freeze(
                inputs, constrained_layers=constrained_layers
            )
            # original_activations: [n_layers, n_pos, d_transcoder]. Expand to
            # [B, n_layers, n_pos, d_transcoder] as a view (zero-memory).
            original_activations = original_activations.unsqueeze(0).expand(
                B, *original_activations.shape
            )
            n_pos = original_activations.size(2)
        else:
            original_activations, freeze_hooks = None, []
            if isinstance(inputs, torch.Tensor):
                n_pos = inputs.size(-1) if inputs.ndim == 1 else inputs.size(1)
            else:
                n_pos = len(self.tokenizer(inputs).input_ids)

        layer_deltas = torch.zeros(
            [B, self.cfg.n_layers, n_pos, self.cfg.d_model],
            dtype=self.cfg.dtype,
            device=self.cfg.device,
        )

        activation_cache, activation_hooks = self._get_activation_caching_hooks(
            apply_activation_function=apply_activation_function,
            sparse=sparse,
            append=False,
        )

        if not return_activations:
            new_activation_hooks = []
            if not constrained_layers:
                for loc, hook in activation_hooks:
                    layer = int(loc.split(".")[1])
                    if layer in union_by_layer:
                        new_activation_hooks.append((loc, hook))
            activation_hooks = new_activation_hooks

        def calculate_delta_hook_batched(
            activations, hook, layer: int, union_for_layer,
            unique_feat_ids: torch.Tensor, cached_decoder_vectors: torch.Tensor
        ):
            if constrained_layers:
                transcoder_activations = original_activations[:, layer]
            else:
                tc_acts = activation_cache[layer]
                if tc_acts.is_sparse:
                    tc_acts = tc_acts.to_dense()
                if not apply_activation_function:
                    tc_acts = self.transcoders.apply_activation_function(
                        layer, tc_acts.unsqueeze(0)
                    ).squeeze(0)
                # tc_acts comes from a single-prompt-shaped cache, so broadcast
                # across the batch dim. Safe because the prompt is identical.
                if tc_acts.ndim == 2:
                    tc_acts = tc_acts.unsqueeze(0).expand(B, *tc_acts.shape)
                transcoder_activations = tc_acts

            activation_deltas = torch.zeros_like(transcoder_activations)
            for row_idx, pos, feature_idx, value in union_for_layer:
                activation_deltas[row_idx, pos, feature_idx] = (
                    value - transcoder_activations[row_idx, pos, feature_idx]
                )

            # nonzero indices: (B, pos, feature_idx) coords across the batch.
            row_idxs, poss, feature_idxs = activation_deltas.nonzero(as_tuple=True)
            new_values = activation_deltas[row_idxs, poss, feature_idxs]

            # Index into the per-sub-batch cache. searchsorted maps each value in
            # the nonzero feature_idxs back to its row in unique_feat_ids_by_layer[layer].
            positions = torch.searchsorted(unique_feat_ids.to(feature_idxs.device), feature_idxs)
            decoder_vectors = cached_decoder_vectors[positions]

            if decoder_vectors.ndim == 2:
                scaled = decoder_vectors * new_values.unsqueeze(1)
                # Accumulate into layer_deltas[row_idx, layer, pos] per nonzero.
                # index_put_ with accumulate=True is the per-row analogue of
                # index_add_ used by the single-prompt path.
                layer_deltas[:, layer].index_put_(
                    (row_idxs, poss), scaled, accumulate=True
                )
            else:
                scaled = decoder_vectors * new_values.unsqueeze(-1).unsqueeze(-1)
                scaled = scaled.transpose(0, 1)  # [n_remaining_layers, n_active, d_model]
                n_remaining_layers = scaled.shape[0]
                for ri in range(n_remaining_layers):
                    layer_offset = self.cfg.n_layers - n_remaining_layers + ri
                    layer_deltas[:, layer_offset].index_put_(
                        (row_idxs, poss), scaled[ri], accumulate=True
                    )

        def intervention_hook_batched(activations, hook, layer: int):
            new_acts = activations
            if layer in intervention_range:
                # activations: [B, n_pos, d_model], layer_deltas[:, layer]: same.
                new_acts = new_acts + layer_deltas[:, layer]
            layer_deltas[:, layer] *= 0
            return new_acts

        delta_hooks = [
            (
                f"blocks.{layer}.{self.feature_output_hook}",
                partial(
                    calculate_delta_hook_batched,
                    layer=layer,
                    union_for_layer=union,
                    unique_feat_ids=unique_feat_ids_by_layer[layer],
                    cached_decoder_vectors=decoder_vectors_by_layer[layer],
                ),
            )
            for layer, union in union_by_layer.items()
        ]

        intervention_range = constrained_layers if constrained_layers else range(self.cfg.n_layers)
        intervention_hooks = [
            (f"blocks.{layer}.{self.feature_output_hook}",
             partial(intervention_hook_batched, layer=layer))
            for layer in range(self.cfg.n_layers)
        ]

        all_hooks = freeze_hooks + activation_hooks + delta_hooks + intervention_hooks
        cached_logits = [None]

        def logit_cache_hook(activations, hook):
            if self.cfg.output_logits_soft_cap > 0.0:
                logits = self.cfg.output_logits_soft_cap * F.tanh(
                    activations / self.cfg.output_logits_soft_cap
                )
            else:
                logits = activations.clone()
            cached_logits[0] = logits

        all_hooks.append(("unembed.hook_post", logit_cache_hook))

        return all_hooks, cached_logits, activation_cache

    @torch.no_grad
    def feature_intervention_batched(
        self,
        inputs: str | torch.Tensor,
        intervention_lists: Sequence[Sequence[Intervention]],
        *,
        constrained_layers: range | None = None,
        freeze_attention: bool = True,
        apply_activation_function: bool = True,
        sparse: bool = False,
        return_activations: bool = True,
    ) -> BatchedInterventionResult:
        """Batched feature intervention symmetric with `feature_intervention`.

        Each row b of `intervention_lists` runs as if it were a separate
        `feature_intervention(inputs, intervention_lists[b], ...)` call. The
        prompt is shared across the batch (frozen-attention path requires
        this), and per-row indexing inside the delta hook keeps rows isolated.

        For B=1 the result is logits[0] equal to the single-prompt path's
        logits (modulo numerical noise from the broadcast).

        Normalizes dict-form rows (`{"layer", "feature_idx", "pos", "value"}`,
        the `InterventionTuple` TypedDict shape) to canonical 4-tuples at
        the boundary so internal hook builders see only tuples.
        """
        intervention_lists = [
            _normalize_intervention_row(row) for row in intervention_lists
        ]
        hooks, _, activation_cache = self._get_feature_intervention_hooks_batched(
            inputs,
            intervention_lists,
            constrained_layers=constrained_layers,
            freeze_attention=freeze_attention,
            apply_activation_function=apply_activation_function,
            sparse=sparse,
            return_activations=return_activations,
        )

        B = len(intervention_lists)
        if isinstance(inputs, torch.Tensor):
            if inputs.ndim == 1:
                batched_inputs = inputs.unsqueeze(0).expand(B, -1)
            else:
                batched_inputs = inputs.expand(B, -1)
        else:
            tokens = self.ensure_tokenized(inputs)
            batched_inputs = tokens.unsqueeze(0).expand(B, -1)

        with self.hooks(hooks):  # type: ignore
            logits = self(batched_inputs)

        if return_activations:
            activation_cache = torch.stack(activation_cache)
        else:
            activation_cache = None

        return BatchedInterventionResult(
            logits=logits, activation_cache=activation_cache
        )

    @torch.no_grad
    def prefill_batched(
        self,
        inputs: str | torch.Tensor,
        intervention_lists: Sequence[Sequence[Intervention]],
        *,
        freeze_attention: bool = True,
        return_activations: bool = False,
    ) -> tuple[torch.Tensor, TransformerLensKeyValueCache]:
        """Run a batched prefill forward with interventions and populate a KV cache.

        This is the first half of the KV-cached decode path. The full prompt is
        forwarded once under the batched intervention hooks, populating a
        ``TransformerLensKeyValueCache`` that can be passed to subsequent
        ``decode_step_batched`` calls. Using ``freeze_attention=True`` (the
        default) ensures the prefill matches the attribution-graph's frozen
        attention pattern, exactly as ``feature_intervention_batched`` does for
        step 0 in the decode loop.

        Parameters
        ----------
        inputs:
            Shared prompt for all batch rows (string or 1-D / 2-D token tensor).
        intervention_lists:
            ``B`` per-row intervention lists. Each row is a sequence of
            ``(layer, pos, feature_idx, value)`` tuples.
        freeze_attention:
            Whether to freeze attention patterns and LayerNorm denominators via
            ``setup_intervention_with_freeze``. Defaults to ``True`` to match
            the measurement-correctness requirement at the prompt forward.
        return_activations:
            Passed through to the hook builder. ``False`` by default because
            ``_decode_one_chunk`` never needs activations at decode time.

        Returns
        -------
        logits:
            Shape ``[B, T_prompt, V]``.
        cache:
            Populated ``TransformerLensKeyValueCache`` with K/V tensors of
            shape ``[B, T_prompt, n_heads, d_head]`` at every layer.
        """
        intervention_lists = [
            _normalize_intervention_row(row) for row in intervention_lists
        ]
        B = len(intervention_lists)

        hooks, _, _ = self._get_feature_intervention_hooks_batched(
            inputs,
            intervention_lists,
            freeze_attention=freeze_attention,
            apply_activation_function=True,
            sparse=False,
            return_activations=return_activations,
        )

        if isinstance(inputs, torch.Tensor):
            if inputs.ndim == 1:
                batched_inputs = inputs.unsqueeze(0).expand(B, -1)
            else:
                batched_inputs = inputs.expand(B, -1)
        else:
            tokens = self.ensure_tokenized(inputs)
            batched_inputs = tokens.unsqueeze(0).expand(B, -1)

        cache = TransformerLensKeyValueCache.init_cache(
            self.cfg, self.cfg.device, batch_size=B
        )

        # HookedTransformer.forward requires an explicit attention_mask when
        # past_kv_cache is not None and no tokenizer is attached to the model
        # (the library tries to compute the mask from the tokenizer and raises
        # ValueError if it is absent). We construct a full-ones mask here
        # because the shared prompt has no padding.
        T_prompt = batched_inputs.shape[1]
        attention_mask = torch.ones(
            B, T_prompt, dtype=torch.long, device=batched_inputs.device
        )

        with self.hooks(hooks):  # type: ignore
            logits = self.forward(
                batched_inputs,
                attention_mask=attention_mask,
                past_kv_cache=cache,
            )

        return logits, cache

    @torch.no_grad
    def decode_step_batched(
        self,
        new_token_ids: torch.Tensor,
        intervention_lists: Sequence[Sequence[Intervention]],
        past_kv_cache: TransformerLensKeyValueCache,
    ) -> torch.Tensor:
        """Run one batched decode step with a single new token per row.

        Feeds a ``[B, 1]`` token tensor through every layer. The KV projections
        for the new token are appended to ``past_kv_cache`` in place, and each
        layer then attends the new query against the full cached K/V. The
        intervention delta hook still fires here because ``pos =
        slice(None, None)`` broadcasts over the single position in the input,
        applying the persistent steering kick at every generated token.

        ``freeze_attention`` is always ``False`` here. The frozen-attention
        pattern is a prompt-only ``[1, T_prompt, T_prompt]`` square, it has no
        rows/columns for the new decode positions and cannot safely be used
        beyond the prefill step.

        Parameters
        ----------
        new_token_ids:
            Shape ``(B, 1)``. Validated loudly on mismatch.
        intervention_lists:
            ``B`` per-row intervention lists. Must have the same length ``B``
            as the batch dimension of ``past_kv_cache``.
        past_kv_cache:
            KV cache populated by a preceding ``prefill_batched`` call (or a
            prior ``decode_step_batched`` call). Mutated in place by appending
            the new token's K/V at every layer.

        Returns
        -------
        logits:
            Shape ``[B, 1, V]``.
        """
        intervention_lists = [
            _normalize_intervention_row(row) for row in intervention_lists
        ]
        B = len(intervention_lists)

        # Loud shape validation -- a silent mismatch would cause the wrong
        # row's query to attend the wrong row's cached K/V.
        if new_token_ids.shape != (B, 1):
            raise ValueError(
                f"decode_step_batched: expected new_token_ids.shape == ({B}, 1), "
                f"got {tuple(new_token_ids.shape)}. "
                f"Ensure B matches len(intervention_lists) and the cache's batch dim."
            )

        cache_batch = past_kv_cache.entries[0].past_keys.shape[0] if past_kv_cache.entries else B
        if cache_batch != B:
            raise ValueError(
                f"decode_step_batched: cache batch dim is {cache_batch} but "
                f"len(intervention_lists) == {B}. Call _compact_kv_cache before "
                f"compacting intervention_lists, or vice versa."
            )

        # Build hooks with freeze_attention=False. No frozen-attention pattern
        # is registered, attention runs naturally against the cache's K/V.
        # The intervention delta hook still fires: pos=slice(None, None) maps
        # to pos=0 on the single-token input, applying the steering kick.
        hooks, _, _ = self._get_feature_intervention_hooks_batched(
            new_token_ids,
            intervention_lists,
            freeze_attention=False,
            apply_activation_function=True,
            sparse=False,
            return_activations=False,
        )

        # Explicit all-ones attention mask for the single new token. This is
        # required because HookedTransformer.forward needs a tokenizer to
        # auto-compute the mask when past_kv_cache is provided, and the
        # ReplacementModel may not have one attached in all test scenarios.
        attention_mask = torch.ones(
            B, 1, dtype=torch.long, device=new_token_ids.device
        )

        with self.hooks(hooks):  # type: ignore
            logits = self.forward(
                new_token_ids,
                attention_mask=attention_mask,
                past_kv_cache=past_kv_cache,
            )

        return logits
