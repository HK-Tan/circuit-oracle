"""Tool functions for the circuit oracle agent.

Each function operates on a ToolContext (graph + tokenizer) instead of globals.
"""

import ast
import concurrent.futures
import json
import os
import time
import logging
from functools import wraps
import requests
import torch
import torch.nn.functional as F
from typing import Literal, TypedDict

from .config import ToolContext
from .constants import DEFAULT_SUBAGENT_MODEL
from .gpu_lock import active as _gpu
from . import fanout
from circuit_tracer.replacement_model import _compact_kv_cache

logger = logging.getLogger(__name__)


def _fanout_slotted(fn):
    """Wrap a subagent call so it occupies one process-wide fan-out slot.

    Each REASSESS pool sizes itself to its own work, which is correct for one
    run and badly wrong for a dozen: the ceiling becomes N x pool_size. The
    limit is global and defaults to unbounded, so serial runs are unaffected.
    See circuit_oracle/fanout.py.
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        with fanout.slot():
            return fn(*args, **kwargs)

    return inner


# Sub-batch size for _batched_greedy_decode. Caps peak VRAM during batched
# anchor / supernode sweeps. Default 80 collapses the deterministic seed sweep
# (top_k=20 features x 4 scales = 80 rows) into a single chunk on an 80 GB GPU,
# so the run_sweeps anchor pass is one prefill + one decode loop instead of two.
# The agentic anchor sweep (K_pinned ~9-12 x 4 = 36-48 rows) and every supernode
# round (3-8 tuples x 4 scales = 12-32 rows) already fit well under this. Stage 3
# (KV cache) and Stage 4 (decoder vector closure) cut the per-row decode footprint
# and remove the prompt re-forward that previously dominated working memory, so an
# 80-row chunk fits 80 GB. Override at process start with the env var
# CIRCUIT_ORACLE_SUB_BATCH (drop to 48 / 16-24 if an 80-row anchor pass or a
# supernode sweep packing many cross-route tuples spanning 15+ distinct layers
# OOMs, raise further on >80 GB GPUs). Not exposed in any tool schema; the model
# has no knob.
BATCHED_DECODE_SUB_BATCH = max(1, int(os.environ.get("CIRCUIT_ORACLE_SUB_BATCH") or 80))


class InterventionTuple(TypedDict):
    """A single feature intervention coordinate plus its target activation.

    Mirrors the 4-tuple ``(layer, pos, feature_idx, value)`` shape consumed
    by ``circuit_tracer.replacement_model.feature_intervention`` today, but
    promoted to a ``TypedDict`` so batched callers can serialize / mock the
    payload without importing ``torch`` or the replacement model.

    Fields
    ------
    layer
        Transcoder layer index the feature lives on.
    feature_idx
        Feature index inside that layer's transcoder dictionary.
    pos
        Token position the intervention applies at (frozen-attention runs
        leave the prompt identical across the batch, so this is per-tuple,
        not per-row).
    value
        Target post-intervention activation. The orchestrator-facing
        multiplicative scale rule is applied upstream; by the time a tuple
        reaches the backend, ``value`` is the literal activation to write.
    """

    layer: int
    feature_idx: int
    pos: int
    value: float


class MeasurementResult(TypedDict):
    """One measurement row returned by the batched sweeps.

    Produced server-side by the harness after each ``(feature, scale)`` or
    ``(supernode_tuple, scale)`` row in a batched forward pass. The
    ``shift_bucket`` field is annotated by ``tools.shift_bucket`` and decides
    whether REASSESS fan-out fires for the underlying feature.

    Fields
    ------
    scale
        Multiplicative scale applied to the baseline activation for this
        row. The 4-scale sweep uses ``{0, -1, -2, -3}``.
    top5_before
        Pre-intervention top-5 next-token distribution at the last prompt
        position. Shape: ``{token_string: {"prob": float}}``.
    top5_after
        Post-intervention top-5 distribution, same shape as
        ``top5_before``.
    answer_after
        Decoded continuation under intervention (post-EOS trim already
        applied per row).
    shift_bucket
        Two-bucket classifier output. ``"shifted"`` triggers REASSESS
        fan-out for the underlying feature; ``"no-shift"`` does not.
    """

    scale: float
    top5_before: dict[str, dict[str, float]]
    top5_after: dict[str, dict[str, float]]
    answer_after: str
    shift_bucket: Literal["no-shift", "shifted"]


def get_top_logits(ctx: ToolContext, k: int = 5):
    """Return the top-k output tokens and probabilities from the attribution graph."""
    n = min(k, len(ctx.graph.logit_tokens))
    results = []
    for i in range(n):
        token_str = ctx.tokenizer.decode(ctx.graph.logit_tokens[i].item())
        prob = ctx.graph.logit_probabilities[i].item()
        results.append({"token": token_str, "probability": round(prob, 4)})
    return results


def get_top_features(ctx: ToolContext, token: str, k: int = 15):
    """Return the top-k features driving a target output token's logit."""
    graph = ctx.graph
    logit_idx = None
    for i in range(len(graph.logit_tokens)):
        decoded = ctx.tokenizer.decode(graph.logit_tokens[i].item())
        if decoded.strip() == token.strip():
            logit_idx = i
            break
    if logit_idx is None:
        available = [ctx.tokenizer.decode(t.item()) for t in graph.logit_tokens]
        return {
            "error": (
                f"Token '{token}' is not one of the top-k next-token candidates captured in "
                f"this attribution graph. Available: {available}. The graph only has attribution "
                f"for the first predicted token. Later tokens in the autoregressive continuation "
                f"(e.g. 'cannot', 'provide' after 'I cannot provide...') are not available here. "
                f"Either pick a token from the available list, or trace upstream from one of "
                f"those tokens to find features that gate the refusal opener."
            )
        }

    n_features = len(graph.selected_features)
    n_logits = len(graph.logit_tokens)

    logit_row = graph.adjacency_matrix[-n_logits + logit_idx]
    feature_effects = logit_row[:n_features]

    # Rank by |direct_effect| in every mode (ToolContext.rank_signed, default
    # False). Activations are nonnegative, so an edge's sign is pure direction
    # alignment and a negative edge is real inhibition, not an artifact. The graph
    # was pruned by absolute influence upstream, so magnitude here matches the
    # criterion that decided which nodes exist. Every row still carries its signed
    # direct_effect, so a driver stays distinguishable from a suppressor.
    topk = min(k, n_features)
    if getattr(ctx, "rank_signed", False):
        _, top_indices = feature_effects.topk(topk)
    else:
        abs_effects = feature_effects.abs()
        _, top_indices = abs_effects.topk(topk)

    results = []
    for idx in top_indices:
        idx = idx.item()
        active_idx = graph.selected_features[idx].item()
        layer, pos, feature_idx = graph.active_features[active_idx].tolist()
        activation = graph.activation_values[active_idx].item()
        direct_effect = feature_effects[idx].item()
        results.append({
            "layer": int(layer),
            "feature_idx": int(feature_idx),
            "pos": int(pos),
            "activation": round(activation, 4),
            "direct_effect": round(direct_effect, 4),
        })
    return results


_PUBLIC_NEURONPEDIA = "https://www.neuronpedia.org"


def _http_inspect_payload(ctx: ToolContext, layer: int, feature_idx: int) -> dict:
    """Hit the Neuronpedia-shaped backend once and normalize into the cache payload shape.

    The host comes from ctx.neuronpedia_base_url, so this serves both public
    Neuronpedia and a local autointerp shim (see autointerp_server.py).

    This is the HTTP half only. Callers go through _fetch_inspect_payload, which
    is the routing seam tests patch.
    """
    sae_id = ctx.neuronpedia_sae_id.format(layer=layer)
    base = (getattr(ctx, "neuronpedia_base_url", None) or _PUBLIC_NEURONPEDIA).rstrip("/")
    url = f"{base}/api/feature/{ctx.neuronpedia_model_id}/{sae_id}/{feature_idx}"
    # Public Neuronpedia serves a static record, so 15s is plenty. A local shim
    # may synthesize the description with an LLM call on a cache miss, which does
    # not finish in 15s, so give it 60.
    timeout = 15 if base == _PUBLIC_NEURONPEDIA else 60
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Neuronpedia API error: {str(e)}"}

    data = resp.json()

    label = "No explanation available"
    if data.get("explanations") and len(data["explanations"]) > 0:
        label = data["explanations"][0].get("description", label)

    top_examples = []
    acts = sorted(
        data.get("activations") or [],
        key=lambda a: a.get("maxValue", 0),
        reverse=True,
    )
    for act in acts[:10]:
        tokens = act.get("tokens", [])
        values = act.get("values", [])
        text = "".join(tokens)[:200]
        max_val = max(values) if values else 0
        max_idx = values.index(max_val) if values else 0
        max_token = tokens[max_idx] if max_idx < len(tokens) else ""
        top_examples.append({
            "text_snippet": text,
            "max_activation": round(max_val, 3),
            "max_token": max_token,
        })

    pos_tokens = data.get("pos_str", [])[:10]
    neg_tokens = data.get("neg_str", [])[:10]

    return {
        "label": label,
        "autointerp": label,
        "top_activating_examples": top_examples,
        "promoted_tokens": pos_tokens,
        "suppressed_tokens": neg_tokens,
        "frac_nonzero": data.get("frac_nonzero"),
    }


def _local_inspect_payload(ctx: ToolContext, layer: int, feature_idx: int) -> dict:
    """The local autointerp record, adapted to the payload shape this module returns."""
    # Imported here rather than at module level so the causal path never pulls in
    # the .autointerp stack (which is only reachable through this branch).
    from .elk_tools import _local_inspect

    rec = _local_inspect(ctx, layer, feature_idx)
    if "error" in rec:
        return rec
    label = rec.get("label") or "No explanation available"
    # Two shape rules, both load-bearing. First, layer and feature_idx are dropped
    # (the local record carries them, but inspect_feature already spreads its own
    # values in, and leaving these would let the payload override the caller).
    # Second, "autointerp" is added (the local record never has it, and it is read
    # by feature_relevance.py and by the pinned-feature report tables in saving.py).
    return {
        "label": label,
        "autointerp": label,
        "top_activating_examples": rec.get("top_activating_examples", []),
        "promoted_tokens": rec.get("promoted_tokens", []),
        "suppressed_tokens": rec.get("suppressed_tokens", []),
        "frac_nonzero": rec.get("frac_nonzero"),
        "source": rec.get("source", "local_autointerp"),
    }


def _fetch_inspect_payload(ctx: ToolContext, layer: int, feature_idx: int) -> dict:
    """Route a feature lookup to the backend ctx.feature_source selects.

    Kept under the original name so inspect_feature and feature_relevance.py
    (which both call this) need no edit.
    """
    mode = getattr(ctx, "feature_source", "neuronpedia")
    if mode == "local":
        return _local_inspect_payload(ctx, layer, feature_idx)
    payload = _http_inspect_payload(ctx, layer, feature_idx)
    if mode == "neuronpedia":
        return payload
    # auto
    if "error" not in payload and payload.get("label") not in (None, "", "No explanation available"):
        return payload
    local = _local_inspect_payload(ctx, layer, feature_idx)
    return payload if "error" in local else local


def check_feature_backend(ctx: ToolContext) -> None:
    """Fail loud at run start if the configured feature backend is not serving.

    Known failure mode: a dead local autointerp shim leaves inspect_feature blind
    while rank_segment_features (direct features/ reads) keeps working, so the run
    looks half-healthy instead of failing.
    """
    mode = getattr(ctx, "feature_source", "neuronpedia")
    base = (getattr(ctx, "neuronpedia_base_url", None) or _PUBLIC_NEURONPEDIA).rstrip("/")

    # Only a shim serves /healthz, public Neuronpedia does not, so probe nothing
    # when the host is the public default. Do not probe /api/feature either, since
    # on a cold cache that triggers a real LLM call on the shim.
    if mode != "local" and base != _PUBLIC_NEURONPEDIA:
        try:
            resp = requests.get(f"{base}/healthz", timeout=10)
            resp.raise_for_status()
            body = resp.json()
        except Exception as e:
            raise RuntimeError(
                f"Autointerp shim at {base} is unreachable ({type(e).__name__}: {e}). "
                f"Start it with `python scripts/run_autointerp_server.py "
                f"--features-dir ... --cache-dir ...` or set feature_source='local'."
            ) from e
        if not body.get("ok"):
            raise RuntimeError(f"Autointerp shim at {base} returned an unhealthy /healthz: {body!r}")

    features_dir = getattr(ctx, "autointerp_features_dir", None)
    if features_dir:
        index_path = os.path.join(features_dir, "index.json.gz")
        if not os.path.exists(index_path):
            raise RuntimeError(
                f"autointerp_features_dir={features_dir!r} has no index.json.gz. "
                f"The direct feature-dir tools (rank_segment_features, "
                f"get_candidate_vote_tally) will fail."
            )
    elif mode == "local":
        raise RuntimeError("feature_source='local' requires ToolContext.autointerp_features_dir.")


def inspect_feature(ctx: ToolContext, layer: int, feature_idx: int, pos: int | None = None):
    """Look up a transcoder feature on Neuronpedia and return its autointerp label and top examples.

    Populates ctx.inspect_cache keyed by (layer, feature_idx, pos). Subsequent calls
    for the same key skip the backend hit (per-call cache).
    """
    key = (layer, feature_idx, pos)
    cached = ctx.inspect_cache.get(key)
    if cached is not None and "error" not in cached:
        return {"layer": layer, "feature_idx": feature_idx, **cached}

    payload = _fetch_inspect_payload(ctx, layer, feature_idx)
    if "error" not in payload:
        ctx.inspect_cache[key] = payload
    return {"layer": layer, "feature_idx": feature_idx, **payload}


# ---------------------------------------------------------------------------
# inspect_cache JSON (de)serialization
# ---------------------------------------------------------------------------

_INSPECT_CACHE_KEY_SEP = ":"


def _encode_cache_key(key: tuple[int, int, int]) -> str:
    layer, feature_idx, pos = key
    return f"{int(layer)}{_INSPECT_CACHE_KEY_SEP}{int(feature_idx)}{_INSPECT_CACHE_KEY_SEP}{int(pos)}"


def _decode_cache_key(s: str) -> tuple[int, int, int]:
    parts = s.split(_INSPECT_CACHE_KEY_SEP)
    if len(parts) != 3:
        raise ValueError(f"malformed inspect_cache key {s!r}; expected 'layer:feature_idx:pos'")
    return (int(parts[0]), int(parts[1]), int(parts[2]))


_TUPLE_TAG = "__tuple__"


def _encode_value(v):
    """Recursively tag tuples so JSON round-trip is lossless."""
    if isinstance(v, tuple):
        return [_TUPLE_TAG, *[_encode_value(x) for x in v]]
    if isinstance(v, list):
        return [_encode_value(x) for x in v]
    if isinstance(v, dict):
        return {k: _encode_value(x) for k, x in v.items()}
    return v


def _decode_value(v):
    if isinstance(v, list):
        if v and v[0] == _TUPLE_TAG:
            return tuple(_decode_value(x) for x in v[1:])
        return [_decode_value(x) for x in v]
    if isinstance(v, dict):
        return {k: _decode_value(x) for k, x in v.items()}
    return v


def dump_inspect_cache(cache: dict) -> str:
    """Serialize an inspect_cache dict (tuple keys) to a JSON string.

    Keys ``(layer, feature_idx, pos)`` are flattened to ``"layer:feature_idx:pos"``
    strings so the result is a plain JSON object. Tuple-valued payloads are
    tagged so the round-trip is lossless.
    """
    encoded = {_encode_cache_key(k): _encode_value(v) for k, v in cache.items()}
    return json.dumps(encoded, sort_keys=True)


def load_inspect_cache(blob: str) -> dict:
    """Inverse of dump_inspect_cache. Returns the dict with tuple keys restored."""
    raw = json.loads(blob)
    if not isinstance(raw, dict):
        raise ValueError(f"inspect_cache blob must decode to a dict, got {type(raw).__name__}")
    return {_decode_cache_key(k): _decode_value(v) for k, v in raw.items()}


# ---------------------------------------------------------------------------
# shift_bucket: server-side two-bucket classifier for batched anchor sweep
# ---------------------------------------------------------------------------

def shift_bucket(top5_before: dict, top5_after: dict, threshold: float = 0.05) -> str:
    """Classify an intervention measurement as "shifted" or "no-shift".

    Two-bucket rule (changes.md §2.3). Top-1 token swap is always "shifted".
    Same top-1 token with probability drop >= threshold is "shifted".
    Else "no-shift". Pure, stateless. Threshold is calibratable against
    drafts/exp-* records.
    """
    before_top1, before_data = max(top5_before.items(), key=lambda x: x[1]["prob"])
    after_top1, _ = max(top5_after.items(), key=lambda x: x[1]["prob"])
    if before_top1 != after_top1:
        return "shifted"
    after_prob_for_before_top1 = top5_after.get(before_top1, {"prob": 0.0})["prob"]
    if before_data["prob"] - after_prob_for_before_top1 >= threshold:
        return "shifted"
    return "no-shift"


def get_upstream_features(ctx: ToolContext, layer: int, feature_idx: int, pos: int, k: int = 10):
    """Return the top-k upstream features that feed into the given feature."""
    graph = ctx.graph
    n_features = len(graph.selected_features)

    target_row = None
    for i in range(n_features):
        active_idx = graph.selected_features[i].item()
        feat = graph.active_features[active_idx].tolist()
        if int(feat[0]) == layer and int(feat[1]) == pos and int(feat[2]) == feature_idx:
            target_row = i
            break

    if target_row is None:
        # Find which positions this feature IS active at, so the agent can retry
        available_positions = []
        for i in range(n_features):
            active_idx = graph.selected_features[i].item()
            feat = graph.active_features[active_idx].tolist()
            if int(feat[0]) == layer and int(feat[2]) == feature_idx:
                available_positions.append(int(feat[1]))
        if available_positions:
            return {
                "error": f"Feature (layer={layer}, feature_idx={feature_idx}) not found at pos={pos}. "
                f"This feature is active at pos={available_positions}. Retry with one of those positions."
            }
        return {
            "error": f"Feature (layer={layer}, pos={pos}, feature_idx={feature_idx}) "
            "not found in graph's selected features."
        }

    row = graph.adjacency_matrix[target_row].clone()
    # Matrix entries are activation-scaled direct effects (a_s × jacobian).
    # Positive = upstream excites target, negative = upstream inhibits target.
    # Activations are nonnegative, so the sign is carried entirely by the
    # jacobian term (decoder/encoder direction alignment). A negative entry is
    # therefore a genuine inhibitory edge, not a sign artifact of the activation.
    feature_effects = row[:n_features]
    # Zeroed rather than removed, so indices stay aligned with graph.selected_features.
    # Under magnitude ranking a zero sorts last, so the target cannot rank itself.
    feature_effects[target_row] = 0

    # Rank by |direct_effect| in every mode (ToolContext.rank_signed, default
    # False), matching the absolute-influence criterion circuit_tracer already
    # used to prune the graph. Inhibitory upstream edges stay in the top-k, which
    # matters most where suppression is the object of study. Every returned row
    # carries its signed direct_effect, so nothing about the sign is hidden.
    topk = min(k, n_features - 1)
    if getattr(ctx, "rank_signed", False):
        _, top_indices = feature_effects.topk(topk)
    else:
        abs_weights = feature_effects.abs()
        _, top_indices = abs_weights.topk(topk)

    results = []
    for idx in top_indices:
        idx = idx.item()
        active_idx = graph.selected_features[idx].item()
        src_layer, src_pos, src_feature_idx = graph.active_features[active_idx].tolist()
        direct_effect = feature_effects[idx].item()
        upstream_activation = graph.activation_values[active_idx].item()
        results.append({
            "type": "feature",
            "layer": int(src_layer),
            "feature_idx": int(src_feature_idx),
            "pos": int(src_pos),
            "direct_effect": round(direct_effect, 4),
            "activation": round(upstream_activation, 4),
        })

    # Embedding node columns. Same convention: positive = the token's embedding
    # excites the target, negative = inhibits.
    n_layers = graph.cfg.n_layers
    embed_start = n_features + n_layers * graph.n_pos
    embed_end = embed_start + graph.n_pos
    embed_effects = row[embed_start:embed_end]

    for pos_idx in range(graph.n_pos):
        w = embed_effects[pos_idx].item()
        if w == 0:
            continue
        token_str = ctx.tokenizer.decode(graph.input_tokens[pos_idx].item())
        results.append({
            "type": "embedding",
            "token": token_str,
            "pos": int(pos_idx),
            "direct_effect": round(w, 4),
        })

    # Final ordering follows the same rule as the top-k selection above, so the
    # merged feature and embedding rows stay consistent with it. Default sorts by
    # |direct_effect| (the published probes and ELK runs ranked the same quantity
    # under its old name edge_weight).
    if getattr(ctx, "rank_signed", False):
        results.sort(key=lambda r: r["direct_effect"], reverse=True)
    else:
        results.sort(key=lambda r: abs(r["direct_effect"]), reverse=True)
    return results[:k]


def _logit_layer(ctx: ToolContext) -> int:
    """The layer index the output logit node sits at, i.e. the subject's n_layers.

    Read from the graph rather than assumed, so the number the validator enforces
    is the same one the system prompt and the build_circuit tool description
    quote. Raises rather than guessing: a wrong logit layer rejects legitimate
    circuits, and the graph is always present by the time build_circuit runs.
    """
    n = getattr(getattr(getattr(ctx, "graph", None), "cfg", None), "n_layers", None)
    if n is None:
        raise RuntimeError(
            "build_circuit needs ctx.graph.cfg.n_layers to know which layer the "
            "output logit node sits at. Build or load the graph first."
        )
    return int(n)


def build_circuit(ctx: ToolContext, *, nodes, edges):
    """Store the agent's curated circuit and pin the canonical build feature set.

    Accepts two node shapes for backward compatibility:
      - the original supernode-grouped shape with `id`, `label`, `layer`,
        `features=[{layer, feature_idx, pos}, ...]`
      - the flat per-feature shape `{layer, feature_idx, pos, label?}` used
        by the batched-sweep tests

    Side effect: writes `ctx.build_features` = set of `(layer, feature_idx, pos)`
    tuples for every concrete feature pinned by the call. This set is the
    strict-reject key set that `pin_features` validates against.
    """
    # The featureless-node exemption is per subject model: embeddings sit at
    # layer 0, output logits at n_layers (36 on Qwen3-4B, 26 on Gemma-2-2B).
    # This used to be hardcoded to 36, which silently made the logit exemption
    # unreachable on any other subject once the system prompt started naming the
    # real layer count.
    logit_layer = _logit_layer(ctx)
    flat_features: set[tuple[int, int, int]] = set()
    for n in nodes:
        # Flat-shape node: top-level layer/feature_idx/pos.
        if "feature_idx" in n and "pos" in n:
            flat_features.add((int(n["layer"]), int(n["feature_idx"]), int(n["pos"])))
            continue
        # Supernode shape: features list under "features".
        sub_feats = n.get("features") or []
        for f in sub_feats:
            flat_features.add((int(f["layer"]), int(f["feature_idx"]), int(f["pos"])))
        # The supernode-shape validation only applies when "features" is the
        # source-of-truth field; flat-shape nodes don't have an `id`.
        if "id" in n:
            if not sub_feats and n.get("layer") not in (0, logit_layer):
                return {
                    "error": f"Node '{n.get('id', '?')}' must have at least one feature "
                    f"(unless it is an output logit node with layer={logit_layer} "
                    "or an embedding node with layer=0)"
                }

    # Edge validation only applies to the supernode-id form. Flat-feature
    # edges use coordinate tuples and aren't checked here.
    if all("id" in n for n in nodes):
        node_ids = {n["id"] for n in nodes}
        for e in edges:
            frm, to = e.get("from"), e.get("to")
            if frm not in node_ids or to not in node_ids:
                return {"error": f"Edge references unknown node: {e}"}

    ctx.build_features = flat_features

    result = {"nodes": nodes, "edges": edges, "status": "circuit_saved"}

    # Depth check only meaningful in the supernode-shape form.
    if all("id" in n for n in nodes):
        has_embedding = any(
            n.get("layer") == 0 and not n.get("features")
            for n in nodes
        )
        has_early = any(
            n.get("layer", 99) <= 3
            for n in nodes
        )
        if not has_embedding:
            if has_early:
                result["warning"] = (
                    "Circuit reaches early layers but not token embedding nodes. "
                    "Consider tracing to embedding nodes to identify which specific "
                    "input tokens drive the prediction."
                )
            else:
                result["warning"] = (
                    "Circuit does not reach early layers (0-3) or token embedding nodes. "
                    "Consider tracing deeper to identify which input tokens drive the prediction."
                )

    return result


ALLOWED_SCALES = (-4, -3, -2, -1, 0, 0.5, 2)
BASELINE_FLOOR = 10.0  # minimum effective baseline for multiplicative steering


def _apply_multiplicative_steering(baseline_act: float, factor: float) -> float:
    """Translate `factor` to a target activation per changes.md sec 2.6.

    `new_act = baseline + (factor - 1) × max(BASELINE_FLOOR, baseline)`.
    Shared by intervene_feature, intervene_supernode, and the batched sweep
    tools so `scale=-4` means the same magnitude everywhere.
    """
    effective_baseline = max(BASELINE_FLOOR, float(baseline_act))
    return float(baseline_act) + (float(factor) - 1.0) * effective_baseline


def _validate_feature_coord(ctx: ToolContext, layer, feature_idx, pos=None):
    """Bounds-check an agent-supplied (layer, feature_idx, pos) before it reaches CUDA.

    Every one of these arrives as free-form JSON from a model, and the
    intervention path feeds them to advanced indexing on the GPU. A stray value
    there does not raise a clean IndexError; it trips a device-side assert in
    IndexKernel.cu, which poisons the CUDA context for the whole process and
    takes down every concurrent run sharing the model. That happened on
    2026-07-28 and cost a 7-slug shard. Cheap to check host-side, so check.

    A negative index is rejected rather than wrapped. Python's negative-index
    convention is actively harmful here: writing at `[..., -5]` lands at
    `d_transcoder - 5`, but the id recorded for the searchsorted lookup stays
    -5, so the two disagree and the lookup runs off the end of the table.
    """
    n_layers, n_pos, d_transcoder = None, None, None
    acts = getattr(ctx, "baseline_activations", None)
    if acts is not None and getattr(acts, "ndim", 0) == 3:
        n_layers, n_pos, d_transcoder = (int(x) for x in acts.shape)

    layer = int(layer)
    feature_idx = int(feature_idx)
    if layer < 0 or (n_layers is not None and layer >= n_layers):
        raise ValueError(
            f"layer {layer} is out of range for this model "
            f"(valid 0..{(n_layers - 1) if n_layers is not None else 'n_layers-1'})."
        )
    if feature_idx < 0 or (d_transcoder is not None and feature_idx >= d_transcoder):
        raise ValueError(
            f"feature_idx {feature_idx} is out of range for layer {layer} "
            f"(valid 0..{(d_transcoder - 1) if d_transcoder is not None else 'd_transcoder-1'})."
        )
    if pos is not None:
        pos = int(pos)
        if pos < 0 or (n_pos is not None and pos >= n_pos):
            raise ValueError(
                f"pos {pos} is out of range for this prompt "
                f"(valid 0..{(n_pos - 1) if n_pos is not None else 'seq_len-1'})."
            )
    return layer, feature_idx, (None if pos is None else int(pos))


def _validate_scale(scale):
    if scale not in ALLOWED_SCALES:
        raise ValueError(
            f"factor must be one of {ALLOWED_SCALES}; got {scale!r}. "
            "MULTIPLICATIVE STEERING: new_act = baseline + (factor - 1) × effective_baseline, "
            "where effective_baseline = max(10, baseline). Negative/zero = reverse/ablate "
            "(refusal/suppression). factor > 1 = amplify (diagnostic only). "
            "Phase 1 (deterministic {0, -1, -2, -3} sweep) is run via batched_anchor_sweep; "
            "this single-call escape hatch is typically used for `scale=-4` saturation tests."
        )


def _record_single(ctx: ToolContext, layer: int, feature_idx: int, scale: float, result: dict) -> None:
    """Append to history, update single-feature dedup index."""
    key = (layer, feature_idx)
    ctx.single_factors.setdefault(key, set()).add(scale)
    if scale in (-2, -3, -4):
        ctx.depth_factors.setdefault(key, set()).add(scale)
    ctx.intervention_history.append({
        "type": "single",
        "layer": layer,
        "feature_idx": feature_idx,
        "scale": scale,
    })


def _supernode_key(features: list) -> frozenset:
    return frozenset((f["layer"], f["feature_idx"]) for f in features)


def _record_supernode(ctx: ToolContext, features: list, scale: float, result: dict) -> None:
    key = _supernode_key(features)
    ctx.supernode_factors.setdefault(key, set()).add(scale)
    ctx.intervention_history.append({
        "type": "supernode",
        "features": sorted([(f["layer"], f["feature_idx"]) for f in features]),
        "scale": scale,
    })


def _topk_from_logits(last_token_logits, tokenizer, k=5):
    probs = F.softmax(last_token_logits.float(), dim=-1)
    top_vals, top_ids = probs.topk(k)
    return {
        tokenizer.decode([tid.item()]): {"prob": round(p.item(), 6)}
        for tid, p in zip(top_ids, top_vals)
    }


def _baseline_active_positions(ctx, layer, feature_idx, top_n=10):
    """Positions where this feature fires in baseline (diagnostic for persistence scope).

    Transcoder features are sparse, so most positions are 0. Returns up to top_n
    nonzero (pos, activation) records sorted by |activation| descending, plus the
    total nonzero count.
    """
    acts = ctx.baseline_activations[layer, :, feature_idx]
    if acts.is_sparse:
        acts = acts.to_dense()
    nonzero = (acts != 0).nonzero().flatten()
    total = int(nonzero.numel())
    if total == 0:
        return {"total_active_positions": 0, "positions": []}
    vals = acts[nonzero]
    order = vals.abs().argsort(descending=True)[:top_n]
    return {
        "total_active_positions": total,
        "positions": [
            {"pos": int(nonzero[i].item()), "activation": round(acts[nonzero[i]].item(), 6)}
            for i in order
        ],
    }


def _check_chain_complete(ctx, fn_name):
    """Refuse to run intervene_feature / intervene_supernode unless the
    PIN -> ANCHOR chain is complete. Per changes.md sec 2.2, the single-call
    escape hatches are factor=-4 saturation tests AFTER the deterministic
    sweep, not bypasses. Without this guard the agent can fall through to
    one-shot interventions when pin_features fails (which is exactly the
    failure mode observed in the 2026-05-15 transcript).
    """
    pinned = getattr(ctx, "pinned_features", None) or {}
    sweep_done = bool(getattr(ctx, "anchor_sweep_done", False))
    if not pinned or not sweep_done:
        missing = []
        if not pinned:
            missing.append("pin_features")
        if not sweep_done:
            missing.append("batched_anchor_sweep")
        raise RuntimeError(
            f"{fn_name} is an escape hatch for factor=-4 saturation tests "
            f"AFTER the chain completes. Missing: {missing}. Run "
            f"build_circuit -> pin_features -> batched_anchor_sweep -> "
            f"batched_supernode_sweep first; then use {fn_name} for any "
            f"follow-up scale=-4 probes."
        )


def _check_intervention_ctx(ctx, fn_name):
    if ctx.replacement_model is None:
        raise RuntimeError(
            f"ctx.replacement_model is None. Populate it at graph-build time before calling {fn_name}."
        )
    if ctx.baseline_activations is None:
        raise RuntimeError(
            f"ctx.baseline_activations is None. Populate it at graph-build time before calling {fn_name}."
        )
    if ctx.baseline_answer is None:
        raise RuntimeError(
            f"ctx.baseline_answer is None. Populate it at graph-build time before calling {fn_name}."
        )
    prompt = getattr(ctx, "baseline_prompt", None)
    if prompt is None:
        raise RuntimeError(
            f"ctx.baseline_prompt not set. Wire this field in the graph-build caller before using {fn_name}."
        )
    return prompt


def _run(interventions_list, prompt_arg, freeze_attn=True, *, model=None,
         retry_label: str = "single", **kwargs):
    """Single-prompt forward with OOM retry. Lifted to module scope so the
    The batched-sweep tests can monkeypatch it to count baseline-forward calls
    (test_batched_anchor_sweep_uses_baseline_cache).
    """
    if model is None:
        raise RuntimeError("_run requires a model kwarg")
    delays = [1, 2, 4]
    last_exc: Exception | None = None
    for attempt, delay in enumerate([0] + delays):
        if delay:
            # Backoff sleeps OUTSIDE the GPU lock. Sleeping while holding it
            # would stall every other run for up to 7 s over a fault that is
            # not theirs.
            time.sleep(delay)
        try:
            # One GPU section per attempt, not one per retry loop, for the same
            # reason. See circuit_oracle/gpu_lock.py.
            with _gpu().hold("_run"):
                logits, _ = model.feature_intervention(
                    prompt_arg, interventions_list,
                    freeze_attention=freeze_attn,
                    return_activations=False,
                )
            return logits
        except torch.cuda.OutOfMemoryError as exc:
            last_exc = exc
            logger.warning("OOM on %s attempt %d; retrying.", retry_label, attempt + 1)
    assert last_exc is not None
    raise last_exc


def _measure_intervention(ctx, intervention_tuples, prompt, answer_max_tokens, retry_label):
    """Run before/after measurement for a list of (layer, pos, feature_idx, new_value) tuples.

    `pos` may be an int (single position) or a `slice` for broadcast steering.
    We use `slice(None, None)` so the kick applies at every position in the full
    context (prompt tokens included) on every generation step, mirroring the
    Arditi/Cyberey "every position, every layer" convention. This also cancels
    any firings of the pinned feature at earlier prompt positions that would
    otherwise propagate refusal signal forward via self-attention.

    Decode is delegated to `_batched_greedy_decode` at B=1, so the escape hatches
    (`intervene_feature`, `intervene_supernode`) and the deterministic sweeps
    (`batched_anchor_sweep`, `batched_supernode_sweep`) share exactly one
    KV-cached implementation. The `intervene_feature` docstring has claimed this
    since the batched refactor landed; until now the claim was false.

    Two things changed with that delegation, both deliberate.

    First, cost. The loop this replaces re-forwarded the entire growing context
    every step with no KV cache, which is O(N^2): at answer_max_tokens=800 on a
    ~30-token prompt it does on the order of 340k token-forwards where the cached
    path does about 830. A run whose agent fires a handful of post-chain escape
    hatches paid tens of minutes for them.

    Second, and this is a semantics change rather than an optimization, the
    attention regime after the first generated token. The old loop re-forwarded
    the whole sequence with freeze_attention=False from step 1 on, so the prompt's
    own K/V were recomputed under natural attention. The cached path freezes
    attention at the prefill only and keeps those prompt K/V for the rest of the
    generation. That is what `circuit_tracer.feature_intervention_generate` does
    ("freeze_attention applies only to the first token generated"), and more
    importantly it is what the sweeps already do. Since the escape hatch exists to
    run a scale=-4 follow-up on a row the sweep produced at scale=-3, the two must
    share an attention regime or the comparison confounds scale with regime.
    Greedy decoding can amplify a small logit reordering into a different answer,
    so escape-hatch measurements taken before this change are not comparable
    token-for-token with ones taken after.

    The old loop also rebuilt its context by concatenating *decoded strings* and
    re-tokenizing the result every step. Byte-level BPE is not stable under that
    concatenation: two generated tokens that decode to "a" and "a" re-encode as the
    single token "aa", so the context could silently walk off the token sequence
    the model actually generated. The cached path appends token ids.

    Returns (top5_before, top5_after, answer_after, inference_time_s).
    """
    tokenizer = ctx.tokenizer

    t0 = time.perf_counter()

    # Baseline top-5 was cached on ctx at graph-build time. Reading instead of
    # recomputing saves one frozen-attention forward per intervened call.
    if ctx.baseline_top5 is None:
        raise RuntimeError(
            "ctx.baseline_top5 is None. compute_or_load_graph must populate it "
            "at graph-build time before any intervention call."
        )
    top5_before = ctx.baseline_top5

    # _batched_greedy_decode resolves the prompt from ctx.baseline_prompt rather
    # than from an argument. Every caller today reaches here via
    # _check_intervention_ctx, which returns exactly that attribute, so the two
    # always agree. Assert it rather than assume it: a future caller passing a
    # different prompt would otherwise be silently measured against the baseline
    # prompt, and the answer_after it got back would look perfectly plausible.
    ctx_prompt = getattr(ctx, "baseline_prompt", None)
    if prompt is not ctx_prompt and prompt != ctx_prompt:
        raise RuntimeError(
            f"_measure_intervention got a prompt that is not ctx.baseline_prompt, "
            f"but the decode path reads ctx.baseline_prompt. Refusing to measure "
            f"against a different prompt than the caller asked for ({retry_label})."
        )

    # OOM retry, preserved from the _run loop this replaces. Each attempt restarts
    # from the prefill because a decode-step OOM can leave the KV cache partially
    # mutated, and _batched_greedy_decode builds a fresh cache per call. Unlike the
    # old loop this drops the allocator cache before retrying, so a retry has a
    # reason to succeed where the first attempt failed.
    delays = [1, 2, 4]
    last_exc: Exception | None = None
    for attempt, delay in enumerate([0] + delays):
        if delay:
            time.sleep(delay)
        try:
            answers, step0_logits = _batched_greedy_decode(
                ctx, [list(intervention_tuples)], answer_max_tokens=answer_max_tokens,
            )
            break
        except torch.cuda.OutOfMemoryError as exc:
            last_exc = exc
            logger.warning("OOM on %s attempt %d; retrying.", retry_label, attempt + 1)
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    else:
        assert last_exc is not None
        raise last_exc

    # step0_logits is [B=1, T_prompt, V] from the frozen-attention prefill, so
    # [0, -1, :] is the next-token distribution the old freeze_attn=True forward
    # reported. The two are not guaranteed bit-identical: this goes through the
    # batched hook path (index_put_(accumulate=True) rather than index_add_) and
    # hands forward() an empty KV cache, so near-tied logits can reorder.
    top5_after = _topk_from_logits(step0_logits[0, -1, :], tokenizer)
    answer_after = answers[0]

    inference_time_s = round(time.perf_counter() - t0, 3)

    return top5_before, top5_after, answer_after, inference_time_s


def _resolve_anchor_position(ctx: ToolContext, layer: int, feature_idx: int) -> int:
    """Return the anchor / bookkeeping position for (layer, feature_idx).

    Used only to look up the baseline activation that feeds the
    multiplicative-steering rule. The intervention itself broadcasts across
    every token position via `pos: slice(None, None)` per changes.md §2.2.

    Resolution order:
      1. If pinned: the `pos` recorded in `ctx.pinned_features` at
         `pin_features` time (the position with the strongest baseline
         activation in the attribution graph).
      2. Otherwise: the argmax over `ctx.baseline_activations[layer, :, feature_idx]`.
    """
    for (l, f, pos), _ in (ctx.pinned_features or {}).items():
        if int(l) == int(layer) and int(f) == int(feature_idx):
            return int(pos)
    acts = ctx.baseline_activations[int(layer), :, int(feature_idx)]
    if acts.is_sparse:
        acts = acts.to_dense()
    return int(acts.argmax().item())


def intervene_feature(
    ctx: ToolContext,
    layer: int,
    feature_idx: int,
    scale: float,
    *,
    hypothesis: str | None = None,
    answer_max_tokens: int = 800,
) -> dict:
    """Single-feature escape-hatch intervention (changes.md §2.2 / §2.6).

    Routes through `feature_intervention_batched` with B=1 so the result is
    bit-equivalent to the corresponding row of `batched_anchor_sweep` /
    `batched_supernode_sweep` at the same `scale`. Typically used for
    `scale=-4` saturation tests on a feature whose -3 row still leaked
    suppression.

    Position semantics (changes.md §2.2 "broadcast across all positions"):
    the intervention is applied at every token position via
    `pos: slice(None, None)`. No agent-facing `position` argument. The
    harness looks up the baseline activation at the feature's anchor /
    bookkeeping position via `_resolve_anchor_position`.

    `hypothesis` is kept as an optional diagnostic-only kwarg (so legacy
    transcripts replaying through this function don't drop the field on
    the floor). It is not part of the agent-facing schema.
    """
    _validate_scale(scale)
    _check_chain_complete(ctx, "intervene_feature")
    answer_max_tokens = min(answer_max_tokens, 800)
    prompt = _check_intervention_ctx(ctx, "intervene_feature")

    anchor_pos = _resolve_anchor_position(ctx, int(layer), int(feature_idx))
    baseline_activation = float(
        ctx.baseline_activations[int(layer), anchor_pos, int(feature_idx)].item()
    )
    new_value = _apply_multiplicative_steering(baseline_activation, scale)

    # Canonical 4-tuple shape matching circuit_tracer.replacement_model's
    # `for layer, pos, feature_idx, value in row:` unpack. `pos: slice(None, None)`
    # broadcasts the kick across every token position in the full context
    # (Arditi 2024 / Cyberey 2025 convention; see changes.md §2.2).
    intervention_tuples = [(int(layer), slice(None, None), int(feature_idx), new_value)]

    top5_before, top5_after, answer_after, inference_time_s = _measure_intervention(
        ctx, intervention_tuples, prompt, answer_max_tokens,
        retry_label=f"intervene_feature L{int(layer)}:F{int(feature_idx)} scale={scale}",
    )

    return {
        "hypothesis": hypothesis or "",
        "intervention": {
            "type": "single",
            "layer": int(layer),
            "position": int(anchor_pos),  # anchor/bookkeeping only; broadcast across all positions
            "feature_idx": int(feature_idx),
            "scale": float(scale),
            "baseline_activation": baseline_activation,
            "new_activation": new_value,
        },
        "top5_before": top5_before,
        "top5_after": top5_after,
        "answer_before": ctx.baseline_answer,
        "answer_after": answer_after,
        "inference_time_s": inference_time_s,
    }


def intervene_supernode(
    ctx: ToolContext,
    features: list,
    scale: float,
    *,
    hypothesis: str | None = None,
    answer_max_tokens: int = 800,
) -> dict:
    """Escape-hatch group intervention on 2+ features at one scale.

    Each feature dict has keys 'layer' and 'feature_idx'. The agent does not
    pass `position`; the harness resolves each feature's anchor / bookkeeping
    position via `_resolve_anchor_position` (the pinned `pos` if pinned, else
    the max-activation position from `ctx.baseline_activations`). The
    intervention itself broadcasts across every token position (`pos:
    slice(None, None)`), matching changes.md §2.2 'Position semantics'.

    MULTIPLICATIVE STEERING applied identically to every feature in the group:
    `new_act = baseline + (factor - 1) × effective_baseline`, where
    `effective_baseline = max(BASELINE_FLOOR, baseline)`.

    Typical use is a `scale=-4` saturation test on a tuple whose -3 row in
    `batched_supernode_sweep` still leaked suppression. Phase 3 of VERIFY
    is normally driven by the batched sweep; this single-shot path exists
    for one-off probes outside the deterministic sweep grid.
    """
    _validate_scale(scale)
    _check_chain_complete(ctx, "intervene_supernode")
    if not features:
        raise ValueError(
            "features must be a non-empty list of {'layer', 'feature_idx'} dicts."
        )
    # Schema requires minItems=2; defensive server-side guard in case the schema is bypassed.
    if len(features) < 2:
        raise ValueError(
            "intervene_supernode requires at least 2 features. For a single-feature intervention, "
            "use intervene_feature."
        )
    answer_max_tokens = min(answer_max_tokens, 800)

    prompt = _check_intervention_ctx(ctx, "intervene_supernode")

    # Dedupe by (layer, feature_idx). Resolve each feature's anchor/bookkeeping
    # position internally; intervention broadcasts across all positions.
    canonical: dict[tuple[int, int], dict] = {}
    duplicates: list[dict] = []
    for feat in features:
        layer = int(feat["layer"])
        feature_idx = int(feat["feature_idx"])
        anchor_pos = _resolve_anchor_position(ctx, layer, feature_idx)
        baseline_activation = float(
            ctx.baseline_activations[layer, anchor_pos, feature_idx].item()
        )
        candidate = {
            "layer": layer,
            "position": anchor_pos,
            "feature_idx": feature_idx,
            "baseline_activation": baseline_activation,
        }
        key = (layer, feature_idx)
        existing = canonical.get(key)
        if existing is None:
            canonical[key] = candidate
        else:
            duplicates.append({**candidate, "dropped_reason": "duplicate_layer_feature"})

    # Defense: if duplicate (layer, feature_idx) inputs collapsed the canonical set to
    # fewer than 2 unique features, this is no longer a supernode. Reject rather than
    # silently running it as a single-feature steer.
    if len(canonical) < 2:
        return {
            "error": (
                "supernode_collapsed: after deduping by (layer, feature_idx), only "
                f"{len(canonical)} unique feature(s) remain. A supernode requires at least "
                "2 distinct (layer, feature_idx) pairs. Use intervene_feature for a single "
                "feature, or rebuild the supernode with semantically complementary features."
            ),
            "intervention": {
                "type": "supernode",
                "scale": scale,
                "features": [{"layer": e["layer"], "feature_idx": e["feature_idx"]} for e in canonical.values()],
            },
            "deduplicated_features": duplicates,
        }

    intervention_tuples = []
    feature_records = []
    for entry in canonical.values():
        layer = entry["layer"]
        position = entry["position"]
        feature_idx = entry["feature_idx"]
        baseline_activation = entry["baseline_activation"]
        new_activation = _apply_multiplicative_steering(baseline_activation, scale)
        # Canonical 4-tuple shape; pos=slice(None, None) broadcasts across positions.
        intervention_tuples.append((layer, slice(None, None), feature_idx, new_activation))
        feature_records.append({
            "layer": layer,
            "position": position,  # anchor/bookkeeping only; broadcast across all positions
            "feature_idx": feature_idx,
            "baseline_activation": baseline_activation,
            "new_activation": new_activation,
            "baseline_active_positions": _baseline_active_positions(ctx, layer, feature_idx),
        })

    top5_before, top5_after, answer_after, inference_time_s = _measure_intervention(
        ctx, intervention_tuples, prompt, answer_max_tokens,
        retry_label=f"intervene_supernode ({len(feature_records)} features) scale={scale}",
    )

    result = {
        "hypothesis": hypothesis or "",
        "intervention": {
            "type": "supernode",
            "features": feature_records,
            "scale": scale,
        },
        "top5_before": top5_before,
        "top5_after": top5_after,
        "answer_before": ctx.baseline_answer,
        "answer_after": answer_after,
        "inference_time_s": inference_time_s,
    }
    if duplicates:
        result["deduplicated_features"] = duplicates
        result["deduplication_note"] = (
            f"{len(duplicates)} entry/entries with duplicate (layer, feature_idx) were dropped. "
            "The intervention broadcasts across all positions, so duplicates add no information."
        )
    # Record using the canonical (deduped) feature set so dedup checks see the same key
    # the agent submitted.
    canonical_features = [{"layer": e["layer"], "feature_idx": e["feature_idx"]} for e in canonical.values()]
    _record_supernode(ctx, canonical_features, scale, result)
    return result


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Three-tool chain (changes.md sec 2.2): pin_features -> batched_anchor_sweep
# ---------------------------------------------------------------------------


SWEEP_SCALES: tuple[float, ...] = (0.0, -1.0, -2.0, -3.0)


def _stringify_feature_key(k) -> str:
    # Inverse of _parse_feature_key. JSON object keys must be strings, so
    # tuple-keyed dicts returned by tools (measurements_by_feature,
    # reassess_records) are rendered as "(layer, feature_idx, pos)" before
    # serialization. Symmetric with the pin_features input shape.
    l, f, p = k
    return f"({int(l)}, {int(f)}, {int(p)})"


def _parse_feature_key(k) -> tuple[int, int, int]:
    # JSON object keys must be strings, so the agent encodes the
    # (layer, feature_idx, pos) tuple as a string literal like
    # "(10, 85272, 34)" or "[10, 85272, 34]". Parse it back to a tuple.
    if isinstance(k, tuple):
        parsed = k
    elif isinstance(k, list):
        parsed = tuple(k)
    elif isinstance(k, str):
        try:
            parsed = ast.literal_eval(k)
        except (ValueError, SyntaxError) as e:
            raise ValueError(
                f"pin_features key {k!r} is not a parseable tuple/list literal "
                "(expected e.g. \"(10, 85272, 34)\")"
            ) from e
    else:
        raise ValueError(
            f"pin_features key {k!r} has unsupported type {type(k).__name__}"
        )
    if not isinstance(parsed, (tuple, list)) or len(parsed) != 3:
        raise ValueError(
            f"pin_features key {k!r} did not parse to a 3-element (layer, feature_idx, pos)"
        )
    return tuple(int(x) for x in parsed)


def pin_features(ctx: ToolContext, *, pre_hypotheses: dict) -> dict:
    """Pin the BUILD-set features with per-feature pre-intervention hypotheses.

    Strict-reject contract from changes.md sec 2.2: the agent-supplied
    ``pre_hypotheses`` keys must match ``ctx.build_features`` exactly. A
    subset misses a feature the agent should be confronting; a superset
    introduces a feature not in the pinned circuit. Both cases raise
    ``ValueError`` with the offending keys named.
    """
    if not isinstance(pre_hypotheses, dict):
        raise ValueError("pre_hypotheses must be a dict of (layer, feature_idx, pos) -> str")
    build_features = getattr(ctx, "build_features", None)
    if not build_features:
        raise ValueError("call build_circuit first to populate ctx.build_features")

    parsed_items = [(_parse_feature_key(k), v) for k, v in pre_hypotheses.items()]
    submitted = {k for k, _ in parsed_items}
    expected = set(build_features)
    missing = expected - submitted
    extra = submitted - expected
    if missing or extra:
        # Show the agent the literal JSON shape that would have been accepted.
        # The 2026-05-15 transcript showed agents flailing for ~12 turns
        # because the error described what was wrong but never the right
        # shape. A literal example collapses retry count to ~1-2.
        example_keys = sorted(expected)[:2] or [(0, 0, 0)]
        example = {
            "pre_hypotheses": {
                _stringify_feature_key(k): "<one-sentence prior belief about this feature's role>"
                for k in example_keys
            }
        }
        example_json = json.dumps(example, indent=2)
        if missing:
            raise ValueError(
                f"pin_features is missing keys present in build_features: {sorted(missing)}. "
                "Every BUILD-pinned feature must be paired with a pre_hypothesis. "
                f"Required JSON shape (all {len(expected)} build_features keys must appear "
                f"with non-empty hypotheses):\n{example_json}"
            )
        # extra (no missing): keys submitted that aren't in build_features
        raise ValueError(
            f"pin_features got keys not present in build_features: {sorted(extra)}. "
            "Either add them to build_circuit or drop them from pre_hypotheses. "
            f"Required JSON shape:\n{example_json}"
        )

    ctx.pinned_features = dict(parsed_items)
    return {"status": "pinned", "n_features": len(ctx.pinned_features)}


def _run_batched_intervention(
    ctx: ToolContext,
    interventions_per_row: list[list[tuple]],
    batch_size: int = 16,
):
    """Shared backend for the batched sweeps.

    Submits ``interventions_per_row`` as a single batched call to
    ``feature_intervention_batched`` (or chunks at ``batch_size`` if the
    list is longer). Returns the concatenated per-row logits tensor.

    Rows are sequences of canonical 4-tuples
    ``(layer, pos, feature_idx, value)`` matching the real model's unpack
    order at `circuit_tracer.replacement_model._get_feature_intervention_hooks_batched`.
    """
    model = ctx.replacement_model
    if model is None:
        raise RuntimeError("ctx.replacement_model is None.")
    prompt = getattr(ctx, "baseline_prompt", None)
    if prompt is None:
        raise RuntimeError("ctx.baseline_prompt not set.")

    all_logits = []
    for start in range(0, len(interventions_per_row), batch_size):
        chunk = interventions_per_row[start : start + batch_size]
        # Per CHUNK, not around the whole loop: a long row list would otherwise
        # hold the GPU for the full sweep and starve every other run. Chunk
        # boundaries are safe hand-off points because nothing carries over
        # between them but the logits list, which lives here on the stack.
        with _gpu().hold("_run_batched_intervention"):
            result = model.feature_intervention_batched(
                inputs=prompt, intervention_lists=chunk,
            )
        all_logits.append(result.logits)
    if not all_logits:
        return None
    return torch.cat(all_logits, dim=0) if len(all_logits) > 1 else all_logits[0]


def _decode_one_chunk(
    model,
    prompt,
    tokenizer,
    eos_id,
    interventions_per_row: list[list[tuple]],
    answer_max_tokens: int,
) -> tuple[list[str], torch.Tensor]:
    """GPU-locked entry point for the batched decode.

    This is THE lock that bounds peak VRAM under concurrency. One chunk holds a
    KV cache of roughly

        n_layers x n_kv_heads x d_head x 2 (K,V) x 2 bytes x n_tokens x B

    which on Qwen3-4B at B=68 and 800 tokens is about 8 GB. Locking only at the
    model-method level would be equally CORRECT, because decode_step_batched
    rebuilds its hooks per call and the KV cache travels as an argument rather
    than living on the model. But it would let every concurrent run sit
    mid-decode holding one of those caches, so a dozen runs would want ~100 GB
    and OOM. Holding across the whole chunk means exactly one KV cache is live
    at a time, which is what lets a single 80 GB card host a dozen runs.

    Held across the ENTIRE chunk on purpose. The cache is created by
    prefill_batched inside and dies when the call returns, so releasing partway
    would hand off with the cache still allocated and defeat the point.

    Kept as a thin wrapper so the name stays importable and patchable for the
    batched_sweeps tests that call it directly. See circuit_oracle/gpu_lock.py.
    """
    with _gpu().hold("_decode_one_chunk"):
        return _decode_one_chunk_impl(
            model, prompt, tokenizer, eos_id, interventions_per_row, answer_max_tokens,
        )


def _decode_one_chunk_impl(
    model,
    prompt,
    tokenizer,
    eos_id,
    interventions_per_row: list[list[tuple]],
    answer_max_tokens: int,
) -> tuple[list[str], torch.Tensor]:
    """Single-chunk decode shared by _batched_greedy_decode (no chunking).

    Uses KV-cached prefill + per-step decode for efficiency. EOS pruning runs
    in lockstep with cache compaction: rows that emit EOS are dropped from the
    active batch immediately (and from the KV cache) so subsequent steps run at
    a smaller B. Per-row outputs are semantically identical to the pre-KV-cache
    implementation.

    Decode steps run with n_pos=1 (one new token per step). The
    slice(None, None) intervention semantics still hold: the steering kick is
    applied at pos=0 of the single-token input on every decode step, which is
    the only position present. This matches the broadcast-across-all-positions
    semantics for the generated tokens.

    Returns (per-row decoded strings, step-0 logits at the LAST prompt position
    only, shaped [B_chunk, 1, V]). Callers index [..., -1, :], which selects the
    same values it did when the full [B_chunk, T_prompt, V] was returned.
    """
    # Edge case: empty chunk. Nothing to run, so return early with an empty
    # tensor sentinel; callers gate on the answers list being empty.
    if not interventions_per_row:
        return [], torch.empty(0)

    B0 = len(interventions_per_row)

    # ------------------------------------------------------------------
    # Prefill (step 0): full-prompt forward at the original chunk size B0.
    # Captured here, before any compaction. The KV cache is also populated
    # here and will be used for all subsequent decode steps.
    #
    # This local is the FULL [B0, T_prompt, V] because the decode loop below
    # needs it. Only the last position is returned to callers, sliced and
    # cloned at the return statement. See the note there.
    # ------------------------------------------------------------------
    step0_logits, kv_cache = model.prefill_batched(
        prompt,
        interventions_per_row,
        freeze_attention=True,
        return_activations=False,
    )

    # Resolve prompt token IDs to compute effective_steps.
    if isinstance(prompt, str):
        if hasattr(model, "ensure_tokenized"):
            prompt_ids = model.ensure_tokenized(prompt)
        elif hasattr(model, "_tokenize"):
            prompt_ids = model._tokenize(prompt)[0]
        else:
            raise RuntimeError("model exposes neither ensure_tokenized nor _tokenize")
    else:
        prompt_ids = prompt.squeeze(0) if prompt.ndim == 2 else prompt

    # Respect the model's position-embedding capacity if advertised.
    # effective_steps is constant for the whole chunk (computed from original
    # prompt length, as before).
    n_ctx = getattr(getattr(model, "cfg", None), "n_ctx", None)
    if n_ctx is None:
        inner = getattr(model, "model", None)
        n_ctx = getattr(inner, "max_seq_len", None)
    effective_steps = answer_max_tokens
    if n_ctx is not None:
        T_prompt = int(prompt_ids.shape[-1])
        effective_steps = min(answer_max_tokens, n_ctx - T_prompt - 1)

    # ------------------------------------------------------------------
    # Identify which rows EOSed on their first generated token (step 0).
    # Those get answers[""] immediately and never enter the decode loop.
    # ------------------------------------------------------------------
    step0_next_ids = step0_logits[:, -1, :].argmax(dim=-1)  # [B0]

    # Per-original-row state.
    answers: list[str | None] = [None] * B0
    generated: dict[int, list[int]] = {i: [] for i in range(B0)}

    # active_to_original maps compacted batch index -> original row index.
    active_to_original: list[int] = []
    active_next_ids_list: list[int] = []

    for orig in range(B0):
        tok = int(step0_next_ids[orig].item())
        if eos_id is not None and tok == eos_id:
            # Finalized immediately with empty answer (EOS on first token).
            answers[orig] = ""
        else:
            generated[orig].append(tok)
            active_to_original.append(orig)
            active_next_ids_list.append(tok)

    # Compact kv_cache and interventions_per_row to the active set only.
    # This must happen before entering the decode loop.
    if len(active_to_original) < B0:
        _compact_kv_cache(kv_cache, active_to_original)
        interventions_per_row = [interventions_per_row[orig] for orig in active_to_original]

    # ------------------------------------------------------------------
    # Decode loop. Runs steps 1 .. effective_steps-1. At each step:
    #   1. Call decode_step_batched with the last generated token per row.
    #      n_pos=1 per step; intervention still fires at pos=0.
    #   2. Argmax last-position logits.
    #   3. Rows whose new token == eos_id are finalized and dropped.
    #   4. Surviving rows append the new token to generated[orig].
    #   5. Cache, interventions_per_row, and active_to_original are ALL
    #      compacted with the same keep_local -- in lockstep.
    # Loop exits when active_to_original is empty or effective_steps reached.
    # ------------------------------------------------------------------
    for _step in range(1, effective_steps):
        if not active_to_original:
            break

        # Build [B_active, 1] tensor of the last generated token per active row.
        next_ids = torch.tensor(
            [[generated[orig][-1]] for orig in active_to_original],
            dtype=torch.long,
        )
        # decode_step_batched expects shape [B_active, 1].
        logits = model.decode_step_batched(
            next_ids, interventions_per_row, kv_cache
        )
        new_ids = logits[:, 0, :].argmax(dim=-1)  # [B_active]

        # Determine which compacted-batch rows survive (did not emit EOS).
        keep_local: list[int] = []
        for local_idx, orig in enumerate(active_to_original):
            tok = int(new_ids[local_idx].item())
            if eos_id is not None and tok == eos_id:
                # Finalize this row now.
                answers[orig] = tokenizer.decode(generated[orig], skip_special_tokens=True)
            else:
                generated[orig].append(tok)
                keep_local.append(local_idx)

        # Compact ALL active state with the same keep_local -- in lockstep.
        # GUARD: kv_cache, interventions_per_row, active_to_original must all
        # shrink together or the next decode step attends the wrong K/V row.
        _compact_kv_cache(kv_cache, keep_local)
        active_to_original = [active_to_original[i] for i in keep_local]
        interventions_per_row = [interventions_per_row[i] for i in keep_local]

        # Post-compaction assertion: all three must agree on batch size.
        B_active = len(active_to_original)
        assert (
            len(interventions_per_row) == B_active
            and (
                not kv_cache.entries
                or kv_cache.entries[0].past_keys.shape[0] == B_active
            )
        ), (
            f"Compaction sync error at step {_step}: "
            f"active_to_original={B_active}, "
            f"interventions_per_row={len(interventions_per_row)}, "
            f"cache_batch={kv_cache.entries[0].past_keys.shape[0] if kv_cache.entries else 'N/A'}"
        )

    # ------------------------------------------------------------------
    # Finalize any rows still active when the loop exits (max-tokens cap
    # reached without EOS). Decode from their accumulated generated tokens.
    # ------------------------------------------------------------------
    for orig in active_to_original:
        answers[orig] = tokenizer.decode(generated[orig], skip_special_tokens=True)

    # At this point answers[i] is set for every i in 0..B0-1.
    #
    # Return ONLY the last prompt position, as [B0, 1, V] rather than
    # [B0, T_prompt, V]. Every consumer indexes [..., -1, :] and always has
    # (_measure_intervention, batched_anchor_sweep, batched_supernode_sweep,
    # _causal_discovery_annotate), so the other T_prompt-1 positions are dead
    # weight. Keeping the singleton time dim means -1 still selects the same
    # row and no call site changes.
    #
    # This matters for concurrency, not for a serial run. At vocab 151643 and
    # B=68 the full tensor is ~620 MB, and it stays live across the reassess
    # fan-out, which is a network round trip per shifted feature. With a dozen
    # concurrent runs that is several GB of pure waste held while nothing is
    # computing. The GPU lock bounds how many KV caches exist at once, but it
    # cannot bound a result the caller is still holding.
    #
    # .clone() is load-bearing: a bare slice is a VIEW that keeps the entire
    # [B0, T_prompt, V] storage alive, which would make this a no-op.
    return answers, step0_logits[:, -1:, :].clone()  # type: ignore[return-value]


def _batched_greedy_decode(
    ctx: ToolContext,
    interventions_per_row: list[list[tuple]],
    answer_max_tokens: int = 100,
) -> tuple[list[str], torch.Tensor]:
    """Ragged greedy decode for a batch of interventions, sub-batched.

    Splits ``interventions_per_row`` into chunks of ``BATCHED_DECODE_SUB_BATCH``
    rows and runs each chunk through ``_decode_one_chunk`` in turn. Sub-batching
    caps peak VRAM (the freeze cache, KV cache, and transcoder activations all
    scale with chunk size). Each chunk re-runs ``feature_intervention_batched``
    with its own freeze cache, so per-row semantics are unchanged.

    Returns (per-row decoded strings concatenated across chunks, step-0 logits
    concatenated along batch dim, shaped [B_total, 1, V] since _decode_one_chunk
    returns only the last prompt position). Frees the CUDA allocator cache
    between chunks so the next chunk starts with maximum headroom.
    """
    model = ctx.replacement_model
    if model is None:
        raise RuntimeError("ctx.replacement_model is None.")
    prompt = getattr(ctx, "baseline_prompt", None)
    if prompt is None:
        raise RuntimeError("ctx.baseline_prompt not set.")
    tokenizer = ctx.tokenizer
    eos_id = getattr(tokenizer, "eos_token_id", None)

    B_total = len(interventions_per_row)
    sub_batch = max(1, BATCHED_DECODE_SUB_BATCH)

    all_answers: list[str] = []
    all_step0_logits: list[torch.Tensor] = []

    for chunk_start in range(0, B_total, sub_batch):
        chunk = interventions_per_row[chunk_start:chunk_start + sub_batch]
        chunk_answers, chunk_step0 = _decode_one_chunk(
            model, prompt, tokenizer, eos_id, chunk, answer_max_tokens,
        )
        all_answers.extend(chunk_answers)
        all_step0_logits.append(chunk_step0)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    if len(all_step0_logits) == 1:
        step0_logits = all_step0_logits[0]
    else:
        step0_logits = torch.cat(all_step0_logits, dim=0)

    return all_answers, step0_logits


def batched_anchor_sweep(ctx: ToolContext, *,
                          user_message: str = "", system_prompt: str = "") -> dict:
    """Argless deterministic 4-scale sweep over ``ctx.pinned_features``.

    Builds ``K features x 4 scales = 4K`` ORIGIN rows over scales
    ``{0, -1, -2, -3}``. Rows are deduped by the applied clamp value
    ``(layer, feature_idx, round(new_value, 6))`` before the batched forward,
    so identical clamps decode once and the shared answer scatters back to
    every origin (next-refactoring.md decision 2). The returned ``measurements``
    list still has one row per origin (feature, scale). Auto-dispatches
    ``reinterpret_subagent`` on every feature with at least one shifted scale
    (changes.md sec 2.4) and returns the per-feature/scale measurements
    plus the reassess records.

    Iteration order is **feature-outer, scale-inner** (load-bearing for
    the REASSESS auto-dispatch fan-out). The dedup is decode-only and never
    reorders or drops feature cells, so the reassess fan-out is unaffected.

    Position semantics (changes.md sec 2.2 'broadcast across all positions'):
    each row's intervention is constructed as
    ``(layer, slice(None, None), feature_idx, new_value)`` so the kick applies
    at every token position. The pinned-feature ``pos`` slot is used only
    to read the baseline activation for the multiplicative-steering rule.
    """
    pinned = getattr(ctx, "pinned_features", None)
    if not pinned:
        raise ValueError("call pin_features first; ctx.pinned_features is empty")

    # Free any allocator-cached memory left over from prior tool calls
    # (BUILD attribution, trace_path subagents). These can hold ~20-30 GB of
    # cached intermediates that aren't reachable but block new allocations.
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # Build (feature, scale) ORIGIN rows. Feature-outer, scale-inner is
    # load-bearing for the reassess fan-out below (it iterates
    # measurements_by_feature in the same order). Every pinned key gets all 4
    # scales unconditionally, including duplicate-position pins of the same
    # feature (the double-lottery upweighting, next-refactoring.md decision 1).
    #
    # Decode is deduped by the APPLIED clamp value, not by (pin, scale).
    # Greedy decode is deterministic, so two origin rows that produce the same
    # (layer, feature_idx, round(new_value, 6)) decode to byte-identical
    # answers and identical step-0 logits. We therefore decode each unique row
    # once and scatter the shared result back to every origin (decision 2).
    #
    # Two origins collide whenever:
    #   - the same pin key appears with the same scale (cross-stage union), or
    #   - two pins of the same (layer, feature_idx) at different positions hit
    #     the same clamp. At scale 0 this happens whenever both baselines are
    #     >= BASELINE_FLOOR, since the steering rule then yields exactly 0.0
    #     for both. When one baseline < BASELINE_FLOOR the scale-0 clamp is
    #     baseline - BASELINE_FLOOR (negative, distinct) so there is no collision.
    pinned_ordered = list(pinned.keys())

    # Parallel per-origin arrays, all the same length and order.
    origin_keys: list[tuple[tuple[int, int, int], float]] = []  # (pin_key, scale)
    origin_baselines: list[float] = []
    origin_new_values: list[float] = []

    # Deduped decode rows plus the origin -> unique-row index map.
    unique_rows: list[list[tuple]] = []
    unique_index_by_dedup_key: dict[tuple[int, int, float], int] = {}
    origin_to_unique: list[int] = []

    for key in pinned_ordered:
        layer, feature_idx, pos = key
        baseline = float(ctx.baseline_activations[layer, pos, feature_idx].item())
        for scale in SWEEP_SCALES:
            new_value = _apply_multiplicative_steering(baseline, float(scale))
            origin_keys.append((key, float(scale)))
            origin_baselines.append(baseline)
            origin_new_values.append(float(new_value))

            dedup_key = (int(layer), int(feature_idx), round(float(new_value), 6))
            unique_idx = unique_index_by_dedup_key.get(dedup_key)
            if unique_idx is None:
                unique_idx = len(unique_rows)
                unique_index_by_dedup_key[dedup_key] = unique_idx
                unique_rows.append([
                    (int(layer), slice(None, None), int(feature_idx), float(new_value))
                ])
            origin_to_unique.append(unique_idx)

    t_decode = time.perf_counter()
    # Decode only the unique rows (auto-chunked at BATCHED_DECODE_SUB_BATCH).
    answers, step0_logits = _batched_greedy_decode(
        ctx, unique_rows, answer_max_tokens=800
    )
    decode_s = round(time.perf_counter() - t_decode, 3)

    # Baseline top-5 served from the graph-build cache.
    baseline_top5 = getattr(ctx, "baseline_top5", None) or _topk_from_logits_default(ctx)

    tokenizer = ctx.tokenizer
    # Precompute top5_after per UNIQUE row once, then scatter to origins.
    unique_top5_after: list[dict] = [
        # step0_logits are [B, T, V], so step0_logits[u, -1, :] is the
        # single-token logits for unique row u.
        _topk_from_logits(step0_logits[u, -1, :], tokenizer)
        for u in range(len(unique_rows))
    ]

    # Rebuild the full feature-keyed map (K features x 4 scales, every origin
    # present) by scattering each origin to its unique decoded result. This map
    # drives _dispatch_reassess, which iterates feature-outer, scale-inner and
    # calls shift_bucket once per (feature, scale) cell. Dedup happens only at
    # decode, so reassess still sees every feature with all 4 scales.
    measurements_by_feature: dict = {}
    for origin_idx, (key, scale) in enumerate(origin_keys):
        unique_idx = origin_to_unique[origin_idx]
        per_scale = measurements_by_feature.setdefault(tuple(key), {})
        per_scale[float(scale)] = {
            "top5_before": baseline_top5,
            "top5_after": unique_top5_after[unique_idx],
            "answer_after": answers[unique_idx],
            "baseline": origin_baselines[origin_idx],
            "new_value": origin_new_values[origin_idx],
        }

    t_reassess = time.perf_counter()
    reassess_records = _dispatch_reassess(
        ctx,
        measurements_by_feature,
        user_message=user_message or getattr(ctx, "baseline_prompt", "") or "",
        # Thread the run's subject system prompt (stashed on ctx at build time) when the
        # caller did not pass one. The orchestrator dispatches this argless, so without
        # this the committed reassess prompt's system_prompt field was always empty (B5).
        system_prompt=system_prompt or getattr(ctx, "system_prompt", "") or "",
    )
    reassess_s = round(time.perf_counter() - t_reassess, 3)

    # Aggregate the reassess fan-out's token usage (per-record usage is attached by
    # reinterpret_subagent, including across its internal retries). This was the one
    # LLM channel with no usage on disk, so cost reconstruction undercounted it.
    reassess_usage = {
        "model": getattr(ctx, "subagent_model", DEFAULT_SUBAGENT_MODEL),
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "providers": {},
    }
    for record in reassess_records.values():
        rec_usage = record.get("usage") or {}
        for key in (
            "input_tokens",
            "output_tokens",
            "cache_creation_input_tokens",
            "cache_read_input_tokens",
        ):
            reassess_usage[key] += rec_usage.get(key, 0) or 0
        for host, n in (rec_usage.get("providers") or {}).items():
            reassess_usage["providers"][host] = reassess_usage["providers"].get(host, 0) + n

    # Also emit a flat measurements list for callers that prefer that shape
    # (existing batched-sweep tests, grade_sweep, saving). One row per origin
    # (feature, scale), so duplicate-position pins keep all their rows. Each
    # row carries baseline and new_value (the applied clamp, also the dedup
    # key) so the artifact is auditable without the graph (decision 5).
    measurements: list[dict] = []
    for key, per_scale in measurements_by_feature.items():
        layer, feature_idx, pos = key
        for scale, rec in per_scale.items():
            measurements.append({
                "layer": int(layer),
                "feature_idx": int(feature_idx),
                "pos": int(pos),
                "scale": float(scale),
                "baseline": rec.get("baseline"),
                "new_value": rec.get("new_value"),
                "top5_before": rec["top5_before"],
                "top5_after": rec["top5_after"],
                "answer_after": rec.get("answer_after", ""),
                "shift_bucket": rec.get("shift_bucket", "no-shift"),
            })

    # Mark the chain as advanced past ANCHOR so the escape hatches
    # (intervene_feature / intervene_supernode) unlock. Per changes.md §2.2
    # they are factor=-4 saturation tests AFTER the sweep, not bypasses.
    ctx.anchor_sweep_done = True

    return {
        "measurements": measurements,
        "measurements_by_feature": {
            _stringify_feature_key(k): v
            for k, v in measurements_by_feature.items()
        },
        "reassess_records": {
            _stringify_feature_key(k): v for k, v in reassess_records.items()
        },
        "n_features": len(pinned_ordered),
        "n_scales": len(SWEEP_SCALES),
        # Origin rows (n_features x n_scales) vs the unique rows actually
        # decoded after value-key dedup. n_decoded_rows is at most n_origin_rows,
        # and the gap is the GPU decode saved by sharing identical clamps across
        # pins and stages (next-refactoring.md decision 2).
        "n_origin_rows": len(origin_keys),
        "n_decoded_rows": len(unique_rows),
        # Wall-clock split: GPU batched decode vs the reassess LLM fan-out. Both
        # happen inside this one tool call, so without the split a slow ANCHOR
        # phase is ambiguous between the two.
        "timings": {"decode_s": decode_s, "reassess_s": reassess_s},
        # Summed token usage of the reassess fan-out, in compute_cost shape.
        "reassess_usage": reassess_usage,
    }


def _topk_from_logits_default(ctx: ToolContext, k: int = 5) -> dict:
    """Compute baseline top-5 from the toy model when ctx.baseline_top5 is empty.

    The graph build populates ``ctx.baseline_top5`` so this
    fallback is rarely hit. The fallback path also avoids a `_run([], ...)`
    call (which the cache test explicitly forbids); it goes through
    ``get_activations`` (no interventions) instead and pulls the last
    position's logits.
    """
    model = ctx.replacement_model
    prompt = ctx.baseline_prompt
    if model is None or prompt is None:
        return {}
    logits, _ = model.get_activations(prompt)
    return _topk_from_logits(logits[0, -1, :], ctx.tokenizer, k=k)


def batched_supernode_sweep(ctx: ToolContext, *, tuples: list) -> dict:
    """Phase 3 supernode sweep (changes.md sec 2.2).

    Each element of ``tuples`` is ``{"features": [(layer, feat_idx, pos), ...],
    "rationale": str}``. The sweep applies ``len(tuples) x 4 scales`` rows.
    Requires at least 3 tuples per call (the harness floor; 2 calls per run
    is enforced at the orchestrator level).
    """
    if not isinstance(tuples, list):
        raise ValueError("tuples must be a list")
    if len(tuples) < 3:
        raise ValueError(
            f"batched_supernode_sweep requires at least 3 tuples per call; got {len(tuples)}"
        )

    # Free allocator-cached memory from earlier tool calls before the sweep.
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    interventions_per_row: list[list[tuple]] = []
    row_meta: list[tuple[int, float]] = []
    for tup_idx, tup in enumerate(tuples):
        feats = tup.get("features") or []
        if not feats:
            raise ValueError(f"tuple {tup_idx} has empty features list")
        for scale in SWEEP_SCALES:
            row: list[tuple] = []
            for f in feats:
                if isinstance(f, dict):
                    layer = int(f["layer"])
                    feature_idx = int(f["feature_idx"])
                    # `pos` from the agent (if present) is treated as anchor /
                    # bookkeeping for the baseline-activation lookup; the
                    # intervention itself broadcasts across all positions.
                    anchor_pos = int(f["pos"]) if "pos" in f else _resolve_anchor_position(
                        ctx, layer, feature_idx)
                else:
                    layer, feature_idx, anchor_pos = int(f[0]), int(f[1]), int(f[2])
                # Host-side bounds check. These coords are agent-authored and go
                # straight into GPU advanced indexing; an out-of-range one trips
                # a device-side assert that poisons the context for every
                # concurrent run in this process, not just this one.
                layer, feature_idx, anchor_pos = _validate_feature_coord(
                    ctx, layer, feature_idx, anchor_pos)
                baseline = float(ctx.baseline_activations[layer, anchor_pos, feature_idx].item())
                new_value = _apply_multiplicative_steering(baseline, scale)
                # Canonical 4-tuple; pos=slice(None, None) broadcasts.
                row.append((layer, slice(None, None), feature_idx, float(new_value)))
            interventions_per_row.append(row)
            row_meta.append((tup_idx, float(scale)))

    answers, step0_logits = _batched_greedy_decode(
        ctx, interventions_per_row, answer_max_tokens=800
    )
    baseline_top5 = getattr(ctx, "baseline_top5", None) or _topk_from_logits_default(ctx)
    tokenizer = ctx.tokenizer

    measurements: list[dict] = []
    for row_idx, (tup_idx, scale) in enumerate(row_meta):
        # step0_logits are [B, T, V]; step0_logits[row_idx] is [T, V].
        top5_after = _topk_from_logits(step0_logits[row_idx, -1, :], tokenizer)
        bucket = shift_bucket(baseline_top5, top5_after)
        measurements.append({
            "tuple_idx": tup_idx,
            "rationale": tuples[tup_idx].get("rationale", ""),
            "features": tuples[tup_idx].get("features", []),
            "scale": scale,
            "top5_before": baseline_top5,
            "top5_after": top5_after,
            "answer_after": answers[row_idx],
            "shift_bucket": bucket,
        })

    return {
        "measurements": measurements,
        "n_tuples": len(tuples),
        "n_scales": len(SWEEP_SCALES),
    }


def _dispatch_reassess(
    ctx: ToolContext,
    measurements_by_feature: dict,
    *,
    user_message: str,
    system_prompt: str,
    baseline_answer: str = "",
) -> dict:
    """Annotate shift buckets and fan-out reinterpret_subagent on shifted features.

    Takes a feature-keyed measurement map produced by batched_anchor_sweep
    (the batched sweep produces this from real forward passes, and the
    REASSESS tests build it directly to exercise the dispatch logic).
    Iterates feature-outer, scale-inner -- this order is load-bearing for
    test_reassess_auto_dispatched_per_shifted, which counts shift_bucket
    calls in a specific order to identify which feature is shifted.

    For each (feature, scale), calls shift_bucket and writes the result back into
    the per-scale measurement dict in place. Features with shift_bucket == "shifted"
    at any scale are dispatched to reinterpret_subagent concurrently. Returns
    the {feature_key: triple_label_record} map, also written into ctx.reassess_records.

    Side effects:
    - mutates measurements_by_feature[feature_key][scale]["shift_bucket"]
    - updates ctx.reassess_records

    `baseline_answer` overrides ctx.baseline_answer when provided (BC's real path
    decodes a baseline per call); empty string falls back to ctx.baseline_answer.
    """
    # Import lazily so subagent.py can import from tools without a circular ref.
    from .subagent import reinterpret_subagent

    shifted_features: list[tuple] = []
    for feature_key, per_scale in measurements_by_feature.items():
        any_shifted = False
        for scale, measurement in per_scale.items():
            top5_before = measurement.get("top5_before", {})
            top5_after = measurement.get("top5_after", {})
            bucket = shift_bucket(top5_before, top5_after)
            measurement["shift_bucket"] = bucket
            if bucket == "shifted":
                any_shifted = True
        if any_shifted:
            shifted_features.append(feature_key)

    if baseline_answer:
        ctx.baseline_answer = baseline_answer

    reassess_records: dict = {}
    if shifted_features:
        max_workers = max(1, len(shifted_features))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_key = {}
            for feature_key in shifted_features:
                layer, feature_idx, pos = feature_key
                future = executor.submit(
                    _fanout_slotted(reinterpret_subagent),
                    ctx=ctx,
                    layer=layer,
                    feature_idx=feature_idx,
                    pos=pos,
                    shift_profile=measurements_by_feature[feature_key],
                    user_message=user_message,
                    system_prompt=system_prompt,
                    # Part A: the run's LLM client + configured subagent model, stashed on
                    # ctx by run_circuit_oracle. None in the test path, where
                    # reinterpret_subagent falls back to the monkeypatched _SUBAGENT_CLIENT.
                    client=getattr(ctx, "subagent_client", None),
                    subagent_model=getattr(ctx, "subagent_model", DEFAULT_SUBAGENT_MODEL),
                    # Default "committed" preserves the agentic pipeline (pre-hypothesis
                    # divergence). The deterministic orchestrator sets
                    # ctx.reassess_variant = "discovery" to request the no-pre-hypothesis path.
                    variant=getattr(ctx, "reassess_variant", "committed"),
                )
                future_to_key[future] = feature_key
            for future in concurrent.futures.as_completed(future_to_key):
                feature_key = future_to_key[future]
                try:
                    record = future.result()
                except Exception as exc:  # noqa: BLE001 - reinterpret_subagent already retries internally
                    record = {"error": f"reinterpret_subagent raised: {exc}"}
                reassess_records[feature_key] = record

    ctx.reassess_records.update(reassess_records)
    return reassess_records


# ---------------------------------------------------------------------------
# Part B (huge-refactor.md): causal-by-default discovery at scale=-1.
#
# Every feature surfaced by get_top_features / get_upstream_features (on the
# orchestrator path only) carries its measured scale=-1 causal effect, so
# selection no longer depends on the oracle nominating the right gate by
# autointerp label + direct_effect. This subsumes the retired
# screen_upstream_causality tool: discovery is now causal by default.
# ---------------------------------------------------------------------------

DISCOVERY_SCALE: float = -1.0


def _causal_discovery_annotate(
    ctx: ToolContext,
    result,
    *,
    user_message: str = "",
    system_prompt: str = "",
):
    """Annotate a discovery-tool result with measured scale=-1 causal effect.

    ``result`` is whatever ``get_top_features`` / ``get_upstream_features`` returned:
    either a list of node dicts (feature rows ``{layer, feature_idx, pos, ...}`` and,
    for upstream, embedding rows) or an error dict. Embedding rows and error dicts are
    passed through untouched.

    For each feature row the harness:
      1. builds one single-feature scale=-1 intervention (multiplicative steering,
         broadcast across positions), and generates the AR completion at
         answer_max_tokens=800 for all rows in one batched greedy decode;
      2. classifies the shift with ``shift_bucket`` and writes ``shift`` onto the row;
      3. for SHIFTED rows only, auto-fetches ``inspect_feature`` (populating
         ``ctx.inspect_cache``) and dispatches the discovery-variant reassess, then
         writes a compact verdict (``autointerp`` / ``post_label`` / ``divergence``)
         onto the row and appends a row to ``ctx.discovery_reassess``.

    Evidence, NOT a filter: a feature that does not shift alone is kept (distributed
    gates only release when co-ablated). The raw 800-token completion stays inside the
    harness and is never returned to the oracle. These probes are not recorded as
    interventions (no ``ctx.intervention_history`` / ``ctx.single_factors`` /
    ``ctx.reassess_records`` mutation) and the harness grader never sees them.

    ``ctx.discovery_annotation`` selects how much of step 3 runs: ``"full"`` is the
    default, ``"shift_only"`` (arm 2) keeps the measurement and withholds every
    label channel. Validated first, before any early return, so a typo cannot pass
    silently on the rows that happen to skip the causal pass.
    """
    annotation = getattr(ctx, "discovery_annotation", "full")
    if annotation not in ("full", "shift_only"):
        raise ValueError(
            f"unknown discovery_annotation: {annotation!r} (expected 'full' or "
            "'shift_only'). An unrecognized value would silently fall through to "
            "full labelling, which is the label leak arm 2 exists to avoid."
        )
    if isinstance(result, dict):  # error dict from the discovery tool
        return result
    if not isinstance(result, list):
        return result

    # Feature rows only (skip embedding rows from get_upstream_features and anything
    # without the (layer, feature_idx, pos) coordinate).
    feats = [
        r for r in result
        if isinstance(r, dict)
        and r.get("type") != "embedding"
        and "feature_idx" in r and "pos" in r and "layer" in r
    ]
    if not feats:
        return result

    # The causal pass needs the intervention context. In production these are wired at
    # graph-build time; if any is missing (a misconfigured ctx), skip the pass and
    # return plain discovery rather than crashing the orchestrator turn.
    if ctx.replacement_model is None or ctx.baseline_activations is None:
        logger.warning("causal discovery pass skipped: intervention context not wired on ctx")
        return result

    interventions_per_row: list[list[tuple]] = []
    for r in feats:
        layer, fidx, pos = int(r["layer"]), int(r["feature_idx"]), int(r["pos"])
        baseline = float(ctx.baseline_activations[layer, pos, fidx].item())
        new_value = _apply_multiplicative_steering(baseline, DISCOVERY_SCALE)
        interventions_per_row.append([
            (layer, slice(None, None), fidx, float(new_value))
        ])

    answers, step0_logits = _batched_greedy_decode(
        ctx, interventions_per_row, answer_max_tokens=800
    )
    baseline_top5 = getattr(ctx, "baseline_top5", None) or _topk_from_logits_default(ctx)
    tokenizer = ctx.tokenizer

    # Classify each feature; collect the shifted ones for reassess fan-out.
    shifted: list[tuple[dict, dict, str]] = []  # (row, shift_profile, answer)
    for idx, r in enumerate(feats):
        top5_after = _topk_from_logits(step0_logits[idx, -1, :], tokenizer)
        bucket = shift_bucket(baseline_top5, top5_after)
        r["shift"] = bucket
        if bucket == "shifted":
            profile = {
                DISCOVERY_SCALE: {
                    "top5_before": baseline_top5,
                    "top5_after": top5_after,
                    "answer_after": answers[idx],
                    "shift_bucket": bucket,
                }
            }
            shifted.append((r, profile, answers[idx]))

    if annotation == "shift_only":
        # Arm 2 (traversal, no inspect): keep the shift measurement, withhold
        # the label channels. The reassess fan-out needs an autointerp label to
        # diverge from, so it is skipped along with the three label fields it
        # would write onto shifted rows (and nothing lands in
        # ctx.discovery_reassess for this run).
        return result

    if not shifted:
        return result

    # Discovery-variant reassess for shifted features. Auto-fetch inspect_feature first
    # (the discovery tools don't carry the autointerp label, so there is nothing to
    # diverge from without it), then dispatch the 2-way reinterpretation.
    from .subagent import reinterpret_subagent  # lazy: avoid tools<->subagent cycle

    eff_user_message = user_message or getattr(ctx, "baseline_prompt", "") or ""
    # Thread the run's subject system prompt (stashed on ctx) when none was passed, so the
    # discovery reassess prompt carries it symmetrically with the committed path (B5).
    eff_system_prompt = system_prompt or getattr(ctx, "system_prompt", "") or ""

    def _reassess_one(row: dict, profile: dict):
        layer, fidx, pos = int(row["layer"]), int(row["feature_idx"]), int(row["pos"])
        # Populate ctx.inspect_cache under the pos-agnostic (layer, feature_idx, None) key
        # (inspect payloads are position-independent). This is the same key the oracle's
        # later manual inspect_feature uses (its schema has no pos), so that call is a cache
        # hit (B4); reinterpret_subagent falls back to this key when its (l,f,pos) read misses.
        inspect_feature(ctx, layer, fidx)
        rec = reinterpret_subagent(
            ctx,
            layer=layer,
            feature_idx=fidx,
            pos=pos,
            shift_profile=profile,
            user_message=eff_user_message,
            system_prompt=eff_system_prompt,
            client=getattr(ctx, "subagent_client", None),
            subagent_model=getattr(ctx, "subagent_model", DEFAULT_SUBAGENT_MODEL),
            variant="discovery",
        )
        return row, rec

    records: list[tuple[dict, dict]] = []
    max_workers = max(1, len(shifted))
    slotted = _fanout_slotted(_reassess_one)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(slotted, row, profile) for (row, profile, _) in shifted]
        for fut in concurrent.futures.as_completed(futures):
            try:
                records.append(fut.result())
            except Exception as exc:  # noqa: BLE001 - reinterpret_subagent retries internally
                logger.warning("discovery reassess raised: %s", exc)

    # Annotate rows + append discovery_reassess log rows (main thread; no shared mutation).
    for row, rec in records:
        layer, fidx, pos = int(row["layer"]), int(row["feature_idx"]), int(row["pos"])
        autointerp = rec.get("autointerp", "")
        post_label = rec.get("post_label", "")
        divergence = rec.get("divergence", "error")
        # Inline compact verdict for the oracle (raw completion withheld).
        row["autointerp"] = autointerp
        row["post_label"] = post_label
        row["divergence"] = divergence
        # Ungraded evidence log. oracle_pinned / became_win are unknown at discovery
        # (a win is decided later by ANALYZE); written null and joined post-hoc.
        ctx.discovery_reassess.append({
            "feature": [layer, fidx, pos],
            "autointerp": autointerp,
            "post_label": post_label,
            "divergence": divergence,
            "oracle_pinned": None,
            "became_win": None,
            # Token usage of this reinterpret call (accumulated across retries),
            # so the discovery channel is costable like the ANCHOR channel.
            "usage": rec.get("usage"),
        })

    return result
