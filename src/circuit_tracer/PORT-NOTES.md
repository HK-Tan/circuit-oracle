# circuit_tracer forward port (batched-intervention delta onto pinned upstream)

Candidate tree produced 2026-07-25. Deliverable is the `circuit_tracer/` directory in
this folder. `_provenance/` is review material, do not copy it into the repo.

## 1. The pin

| item | value |
|---|---|
| upstream repo | https://github.com/safety-research/circuit-tracer (MIT) |
| pinned tag | `v0.5.0` |
| pinned commit | `4bb8c0ea10bde09727e14565ec8469656880da53` (2026-04-18, "Add support for loading local CLT features in attribution graphs (#93)") |
| previous fork base | `e49c213cf5238af7543b7d433d5ed5ca7b597e79` (2025-12-26, parent of the v0.3.0 release) |

### Why v0.5.0 and not something newer

Spec A section 4c predicted v0.5.0. Verified against the clone rather than trusted:

* `Graph.__init__` at v0.5.0 is
  `(input_string, input_tokens, active_features, adjacency_matrix, cfg, selected_features,
  activation_values, logit_targets, logit_probabilities, scan=None, vocab_size=None)`
  (`graph.py:32-43`). It still takes `scan`, not `scan_name`. `scan` is renamed at
  `1bbfc6b`, which lands after v0.5.0, so v0.5.1 and v0.5.2 would break
  `spurious-correlation/circuit_extraction.py:825` (`scan=model.scan`).
* All five symbols the build scripts need are present at v0.5.0:
  `circuit_tracer/utils/create_graph_files.py`, `circuit_tracer/attribution/targets.py`
  (`LogitTarget`, `CustomTarget`), `circuit_tracer/utils/demo_utils.py` (`get_top_features`),
  `circuit_tracer.graph.compute_partial_influences` (`graph.py:361`),
  `Graph.logit_token_ids` (`graph.py:103-104`).
* `attribute()` at v0.5.0 (`attribution/attribute.py:20-31`) accepts exactly what
  `secret-elicitation/build_taboo_graphs.py:161-170` passes
  (`prompt, model, max_n_logits, desired_logit_prob, batch_size, max_feature_nodes,
  offload, verbose`).
* `ReplacementModel.from_pretrained(..., backend="transformerlens", ...)` exists
  (`replacement_model/replacement_model.py:25-31`), so
  `build_taboo_graphs.py:138-147` and the `assert model.backend == "transformerlens"` in
  `circuit_extraction.py` both work. `self.backend` is set in
  `_configure_replacement_model`.
* `Graph.logit_tokens` survives as a deprecated property (`graph.py:118-133`, emits
  `DeprecationWarning`), which is what every oracle-side reader uses today.

v0.5.1 / v0.5.2 were rejected only because of the `scan` to `scan_name` rename. If the
probes script is updated to `scan_name`, the pin can move forward later.

## 2. What changed relative to the pin

Full unified diff at `_provenance/delta_vs_pin.diff`. Three files, nothing else:

| file | change |
|---|---|
| `circuit_tracer/replacement_model/batched.py` | NEW, 656 lines, all ours. The whole batched delta. |
| `circuit_tracer/replacement_model/replacement_model_transformerlens.py` | 5 in-place patches, each tagged `BATCHED PORT (n of 5)`. +42 / -3 lines. |
| `circuit_tracer/replacement_model/__init__.py` | re-exports the batched names so `from circuit_tracer.replacement_model import _compact_kv_cache` keeps resolving. |
| `circuit_tracer/LICENSE` | upstream `LICENSE` moved from the repo root into the package dir, matching the layout of the tree it replaces. Byte-identical to upstream. |

Everything else is byte-identical to `v0.5.0`, including `frontend/` (with `assets/`),
`__main__.py`, and the nnsight backend modules, so the tree stays internally closed and a
future rebase is a plain `git diff` against a new tag.

### `batched.py` contents (ported from the fork's `replacement_model.py`)

| ported item | fork location |
|---|---|
| `BatchedInterventionBackend` (Protocol) | `replacement_model.py:32-76` |
| `BatchedInterventionResult` (dataclass) | `replacement_model.py:80-96` |
| `_normalize_intervention_row` | `replacement_model.py:99-119` |
| `_compact_kv_cache` | `replacement_model.py:162-217` |
| `_get_feature_intervention_hooks_batched` | `replacement_model.py:879-1079` |
| `feature_intervention_batched` | `replacement_model.py:1082-1140` |
| `prefill_batched` | `replacement_model.py:1143-1228` |
| `decode_step_batched` | `replacement_model.py:1231-1318` |

The four methods live on `BatchedInterventionMixin`, mixed in ahead of
`HookedTransformer`. Every line of executable code is byte-for-byte the fork's. Two
docstring-only edits: a dangling `see changes.md sec 2.2` pointer was dropped (that file
does not exist in this repo), and comment punctuation was normalized to house style (no
em-dashes, no semicolons). `calculate_delta_hook` was NOT ported, it is upstream code
(spec A section 2b correction).

### The 5 in-place patches

1. `TransformerLensReplacementModel(BatchedInterventionMixin, HookedTransformer)`. The
   mixin adds methods only, no `__init__` and no state, so construction and TransformerLens
   hook setup are untouched. Verified MRO
   `[TransformerLensReplacementModel, BatchedInterventionMixin, HookedTransformer, HookedRootModule]`.
2. `setup_intervention_with_freeze`, cast every `hook_pattern` entry of `freeze_cache` to
   `self.cfg.device` / `self.cfg.dtype` so TransformerLens's downstream `.to()` is a no-op
   and the `.expand()` view survives. Inert for the single-row path. (fork
   `replacement_model.py:653-662`)
3. `freeze_hook`, broadcast a `B=1` freeze cache to the live batch as a stride-only view.
   (fork `replacement_model.py:664-677`)
4. NEW, not in the fork. `_get_activation_caching_hooks`,
   `transcoder_acts[self.zero_positions] = 0` becomes
   `transcoder_acts[..., self.zero_positions, :] = 0`. This line does not exist at the fork
   base, upstream added it at v0.3.0. `.squeeze(0)` leaves a `[n_pos, d_transcoder]` tensor
   at B=1 but a `[B, n_pos, d_transcoder]` tensor when the batched path runs the forward at
   B>1, so upstream's form zeroes batch row 0 instead of position 0. The `[..., pos, :]`
   form is identical for the 2-D case and correct for the 3-D one. Proven load-bearing
   below.
5. `feature_intervention`, 3 lines calling `_normalize_intervention_row` at the boundary.
   (fork `replacement_model.py:1360-1362`)

### The reverse dependency is gone

The fork had `if TYPE_CHECKING: from circuit_oracle.tools import InterventionTuple` at
`replacement_model.py:9-10`, a reverse dependency circuit_tracer to circuit_oracle.
`batched.py` does not import anything from `circuit_oracle`. The Protocol annotates rows as
`Sequence[Sequence[Any]]` and a comment records that a row is either the canonical 4-tuple
or the dict form the oracle calls `InterventionTuple`. `batched.py` uses
`from __future__ import annotations` plus a TYPE_CHECKING-only import of the `Intervention`
alias from `replacement_model_transformerlens`, so there is no runtime import cycle and no
duplicated alias. circuit_tracer is a standalone library again.

### `utils/__init__.py`

No change needed. Upstream v0.5.0 already ships the `create_graph_files` re-export in its
own form (`from circuit_tracer.utils.create_graph_files import create_graph_files as
create_graph_files`, `__all__ = ["create_graph_files", "get_default_device"]`). The fork's
removal of that re-export is simply not carried forward.

## 3. Checks run (no GPU, no weights, no attribution)

| check | result |
|---|---|
| `python3 -m py_compile` on all 33 `.py` files | pass |
| `import circuit_tracer` | pass |
| `from circuit_tracer import ReplacementModel, attribute, Graph` | pass |
| `from circuit_tracer.utils import create_graph_files` | pass |
| `from circuit_tracer.attribution.targets import LogitTarget, CustomTarget` | pass |
| `from circuit_tracer.utils.demo_utils import get_top_features` | pass |
| `from circuit_tracer.graph import Graph, compute_partial_influences` | pass |
| `from circuit_tracer.graph import Graph, compute_node_influence` (oracle `seed_select.py:44`) | pass |
| `from circuit_tracer.replacement_model import _compact_kv_cache` (oracle `tools.py:19`) | pass |
| `from circuit_tracer.replacement_model import ReplacementModel, BatchedInterventionResult, BatchedInterventionBackend` (tests) | pass |
| `from circuit_tracer.attribution.attribute import attribute` (oracle `graph_compute.py:13`) | pass |
| `from circuit_tracer.transcoder import SingleLayerTranscoder, TranscoderSet` (tests) | pass |
| `from circuit_tracer.frontend.graph_models import ...` | pass |
| all 4 batched methods present on `TransformerLensReplacementModel` | pass |
| AST walk, 155 internal `circuit_tracer.*` import references | 152 resolve, 3 fail only because `nnsight` is not installed here (`attribution/attribute.py`, `attribution/attribute_nnsight.py`, `attribution/context_nnsight.py`, all lazily imported) |
| CPU smoke (`_provenance/smoke_cpu.py`, tiny random-init model, no downloads) | pass, see below |

`_provenance/smoke_cpu.py` output:

```
construction OK, type = TransformerLensReplacementModel
MRO = ['TransformerLensReplacementModel', 'BatchedInterventionMixin', 'HookedTransformer', 'HookedRootModule']
batched logits shape (2, 5, 50)
max |batched[0] - single(row0)| = 4.768e-07
max |batched[1] - single(row1)| = 2.980e-07
max |dict-form - tuple-form| = 0.000e+00
prefill logits (2, 5, 50) cache batch 2
decode step logits (2, 1, 50)
after compact, cache batch 1
decode step after compaction (1, 1, 50)
SMOKE OK
```

Both new-behavior patches were shown to be load-bearing by reverting them on a scratch copy
and re-running the same smoke:

* without patch 3, `AssertionError: Activations shape torch.Size([2, 4, 5, 5]) does not
  match cached values shape torch.Size([1, 4, 5, 5]) at hook blocks.0.attn.hook_pattern`.
* without patch 4, the run completes but batched rows silently diverge from the
  single-prompt path by `2.1e-2` and `2.0e-1` instead of `5e-7`.

## 4. Open items that can only be settled on GPU

* Real-model numerical parity of `feature_intervention_batched` against B single
  `feature_intervention` calls on Qwen3-4B with the real transcoders, at the sub-batch
  sizes the oracle uses (`CIRCUIT_ORACLE_SUB_BATCH`, default 80).
* v0.5.0 changed upstream behavior in ways that affect the causal path and cannot be
  checked here. They are upstream's, not the port's, and the decision to rebase forward
  accepts them:
  * `ensure_tokenized` now passes `add_special_tokens=False` and asserts a
    `<bos><start_of_turn>user\n` prefix for gemma-3-it models.
  * `_configure_replacement_model` sets `self.zero_positions` and
    `_get_activation_caching_hooks` zeroes position 0 of the cached transcoder
    activations. The base-era file did not. Interventions whose `pos` covers position 0
    therefore compute their delta against 0 rather than the true activation, in both the
    single and the batched path.
  * `setup_attribution` zeroes error vectors at `self.zero_positions` rather than at
    position 0 only.
  * `_get_feature_intervention_hooks` registers intervention hooks only on
    `intervention_range` layers, where the base-era registered on all layers. Our batched
    analogue still registers on all layers and gates inside the hook, which is the fork's
    behavior, preserved deliberately.
  * `feature_intervention_generate` now returns 2-D logits (`(seq_len, vocab_size)`).
* Every graph must be rebuilt. v0.5.0 `Graph.to_pt` writes `logit_targets` and
  `vocab_size` (`graph.py:135-153`), the fork wrote `logit_tokens` and no `vocab_size`, and
  `from_pt` cannot read the other era's file. No `.pt` is committed, so nothing is
  invalidated, but builders and runners must both be on this tracer.
* `transformer_lens` floor. `batched.py` imports
  `transformer_lens.cache.key_value_cache.TransformerLensKeyValueCache`. Present in 3.2.1
  (the version installed here). The pyproject pin must have a floor that guarantees it,
  `transformer-lens>=2.16.0` does not.

## 5. Third-party deps this tree needs

Neither pyproject declares them today. Hard, module-level: `torch`, `transformer_lens`,
`transformers`, `einops`, `safetensors`, `numpy`, `pyyaml`, `huggingface_hub`, `tqdm`,
`pydantic` (`frontend/graph_models.py`), `IPython` (`utils/demo_utils.py` imports
`IPython.display` at module level and `spurious-correlation/circuit_extraction.py:14`
imports `demo_utils` at module level). Optional, lazily imported: `nnsight` (nnsight
backend), `fastapi` plus `uvicorn` (`frontend/local_server.py`, only reached through
`python -m circuit_tracer start-server`).

## 6. Swap-in

```bash
# from the repository root, with $PORT_DIR pointing at the staged forward-port
rm -rf src/circuit_tracer
cp -R "$PORT_DIR/circuit_tracer" src/circuit_tracer
```

Do not copy `_provenance/` or `PORT-NOTES.md` unless you want them in the repo.

## 7. README attribution sentence (replaces spec A section 3's draft)

> `src/circuit_tracer/` vendors
> [circuit-tracer](https://github.com/safety-research/circuit-tracer) (MIT, Copyright (c)
> 2024 Michael Hanna and Mateusz Piotrowski) at upstream tag `v0.5.0`
> (`4bb8c0ea10bde09727e14565ec8469656880da53`). Every file is byte-identical to that tag
> except three. We add `replacement_model/batched.py`, a batched-row intervention backend
> (`feature_intervention_batched`, `_get_feature_intervention_hooks_batched` with per-row
> delta indexing, `prefill_batched` / `decode_step_batched` for KV-cached steered
> generation, `_compact_kv_cache`, `BatchedInterventionResult`), mixed into
> `TransformerLensReplacementModel`; we patch
> `replacement_model/replacement_model_transformerlens.py` in five places (all tagged
> `BATCHED PORT`), of which two are batch-broadcast fixes to the frozen-attention hook and
> the activation cache and one is a dict-row normalization at the `feature_intervention`
> boundary; and we re-export the batched names from `replacement_model/__init__.py`. The
> upstream LICENSE is included verbatim.
