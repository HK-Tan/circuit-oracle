"""Subagent infrastructure for tracing paths through attribution circuits.

NOTE, this module also owns the **shared tool-execution registry** for the
whole oracle (both the orchestrator at ``orchestrator.py:542`` and the
subagent loop below go through ``execute_tool`` here). The filename suggests
"subagent only", but ``_make_tool_dispatch`` is the single source of truth
for "tool name → Python callable" across both call sites. When adding a new
tool you must update BOTH ``tool_schemas.py:TOOLS`` (the LLM-facing schema)
AND ``_make_tool_dispatch`` below (the runtime dispatch). Updating only the
schema causes the orchestrator to call the tool, hit the dispatch table's
"Unknown tool" branch, and silently fall back to whatever legacy tool the
LLM picks instead.
"""

import json
from typing import Any, Callable, Literal, TypedDict

import torch

from .config import ToolContext


# Reasoning/thinking content-block types returned by reasoning models. Some
# OpenRouter upstreams (notably gpt-oss-120b) emit these as OUTPUT but reject
# them as INPUT (HTTP 400: "messages.N.assistant.reasoning_details ... is
# unsupported"), so echoing them back on the next turn breaks the multi-turn
# subagent loop. The orchestrator only ever receives the structured
# report_findings dict and never sees subagent reasoning, so dropping these
# blocks before replay is lossless for everything downstream.
_REASONING_BLOCK_TYPES = frozenset({"thinking", "redacted_thinking"})


# Substrings that mark a CUDA fault the process cannot continue past. A
# device-side assert (an out-of-bounds advanced index, say) poisons the context:
# every subsequent CUDA call in the process raises, including calls made by
# other concurrent runs sharing the model. Recovery is impossible without
# restarting the process, so these must abort rather than be reported to the
# agent as an ordinary tool failure.
#
# Deliberately does NOT match "CUDA out of memory". OOM leaves the context
# usable and the intervention path already retries it after empty_cache().
_UNRECOVERABLE_CUDA_MARKERS = (
    "device-side assert",
    "cuda error",
    "an illegal memory access",
    "misaligned address",
    "unspecified launch failure",
)


def is_unrecoverable_cuda_error(exc: BaseException) -> bool:
    """True if `exc` indicates a poisoned CUDA context.

    Matched on message text rather than exception type because PyTorch surfaces
    all of these as a bare RuntimeError, and because the assert is asynchronous:
    it is reported by whichever unrelated CUDA call happens to sync next, so the
    exception type carries no information about the real fault.
    """
    if isinstance(exc, torch.cuda.OutOfMemoryError):
        return False
    text = str(exc).lower()
    return any(marker in text for marker in _UNRECOVERABLE_CUDA_MARKERS)


def _without_reasoning(content: Any) -> list:
    """Return ``content`` with reasoning/thinking blocks removed, text+tool_use kept.

    Handles both SDK block objects (``block.type``) and dict-form blocks
    (``block["type"]``). Tool-use detection elsewhere in the loop reads the
    original ``response.content``, so this only affects the replayed history.
    """
    kept = []
    for block in content:
        btype = getattr(block, "type", None)
        if btype is None and isinstance(block, dict):
            btype = block.get("type")
        if btype in _REASONING_BLOCK_TYPES:
            continue
        kept.append(block)
    return kept


class TripleLabelRecord(TypedDict):
    """REASSESS-output triple-label record for one shifted feature.

    Produced by the auto-dispatched ``reinterpret_subagent`` for every
    feature with ``shift_bucket == "shifted"`` at any of the 4 anchor-sweep
    scales. Persisted under ``reassess_records`` in ``oracle_result.json``,
    keyed by ``(layer, feature_idx, pos)``.

    Fields
    ------
    autointerp
        Static feature label from Neuronpedia (cached on
        ``ctx.inspect_cache``).
    pre_label
        The orchestrator's ``pre_hypothesis`` at the ``pin_features``
        step. Reflects pre-intervention reasoning only (cached
        ``inspect_feature`` + DISPATCH traces + BUILD groupings).
    post_label
        The subagent's revised role description after seeing the 4-scale
        intervention shift profile.
    divergence
        Three-way comparison outcome. ``autointerp_and_pre`` flags the
        load-bearing case the paper claims: features whose role wasn't
        predictable from static inspection plus LM reasoning alone, only
        from causal intervention.
    """

    autointerp: str
    pre_label: str
    post_label: str
    divergence: Literal["none", "autointerp_only", "autointerp_and_pre"]
from .constants import DEFAULT_SUBAGENT_MODEL
from .llm_client import LLMClient
from .tool_schemas import TOOLS, REPORT_FINDINGS_TOOL, apply_tool_exclusions_to_prompt
from .tools import (
    get_top_logits,
    get_top_features,
    inspect_feature,
    get_upstream_features,
    build_circuit,
    intervene_feature,
    intervene_supernode,
    pin_features,
    batched_anchor_sweep,
    batched_supernode_sweep,
    _causal_discovery_annotate,
)
from .elk_tools import (
    rank_segment_features,
    get_candidate_vote_tally,
    get_source_influence,
)
from .pipeline import _parse_key


# DEFAULT_SUBAGENT_MODEL is re-exported from .constants for backwards-compat with
# `from circuit_oracle.subagent import DEFAULT_SUBAGENT_MODEL` callers/tests.
# Authoritative definition lives in constants.py so config.py can share it
# without a circular import.

# Retry policy for subagent logical failures (malformed output, max-turn timeout,
# error-dict return). Sits on top of LLMClient's API-level backoff which handles
# transient HTTP. 1 initial attempt + 2 retries = 3 total.
SUBAGENT_MAX_ATTEMPTS = 3


def _extract_features_from_trace_log(trace_log: list[dict[str, Any]]) -> dict:
    """Extract features and edges from trace_log when subagent fails to report.

    Returns dict with discovered_features, discovered_edges (both with source='log_extracted').
    """
    features_seen = {}  # (layer, feature_idx, pos) -> feature dict
    edges_seen = set()  # (from_key, to_key) tuples to dedupe

    discovered_features = []
    discovered_edges = []

    for entry in trace_log:
        tool = entry.get("tool")
        output = entry.get("output")
        inp = entry.get("input", {})

        if not output or "error" in output:
            continue

        if tool == "inspect_feature":
            layer = inp.get("layer")
            feature_idx = inp.get("feature_idx")
            if layer is None or feature_idx is None:
                continue
            # We don't have pos from inspect_feature input, but we can match later
            # For now, store without pos and merge when we see get_upstream_features
            key = (layer, feature_idx)
            if key not in features_seen:
                promoted = output.get("promoted_tokens", [])
                if isinstance(promoted, list) and promoted:
                    promoted = [t.get("token", t) if isinstance(t, dict) else t for t in promoted[:5]]
                features_seen[key] = {
                    "layer": layer,
                    "feature_idx": feature_idx,
                    "label": output.get("label", "unknown"),
                    "frac_nonzero": output.get("frac_nonzero"),
                    "promoted_tokens": promoted,
                    "source": "log_extracted",
                }

        elif tool == "get_upstream_features":
            to_layer = inp.get("layer")
            to_feature_idx = inp.get("feature_idx")
            to_pos = inp.get("pos")
            upstream = output.get("upstream_features", [])

            for up in upstream:
                if up.get("type") == "embedding":
                    continue
                from_layer = up.get("layer")
                from_feature_idx = up.get("feature_idx")
                from_pos = up.get("pos")
                direct_effect = up.get("direct_effect", 0)

                if from_layer is None or from_feature_idx is None:
                    continue

                # Record the upstream feature (basic info, label comes from inspect_feature)
                from_key = (from_layer, from_feature_idx, from_pos)
                if from_key not in features_seen:
                    features_seen[from_key] = {
                        "layer": from_layer,
                        "feature_idx": from_feature_idx,
                        "pos": from_pos,
                        "label": "not_inspected",
                        "source": "log_extracted",
                    }

                # Record edge
                edge_key = (from_key, (to_layer, to_feature_idx, to_pos))
                if edge_key not in edges_seen:
                    edges_seen.add(edge_key)
                    discovered_edges.append({
                        "from_layer": from_layer,
                        "from_feature_idx": from_feature_idx,
                        "from_pos": from_pos,
                        "to_layer": to_layer,
                        "to_feature_idx": to_feature_idx,
                        "to_pos": to_pos,
                        "direct_effect": direct_effect,
                        "source": "log_extracted",
                    })

    # Merge: update features that have pos info from get_upstream_features
    for key, feat in features_seen.items():
        if len(key) == 3:
            # Has pos
            discovered_features.append(feat)
        elif len(key) == 2:
            # From inspect_feature, no pos. Check if we have a matching entry with pos
            layer, feature_idx = key
            matched = False
            for other_key in features_seen:
                if len(other_key) == 3 and other_key[0] == layer and other_key[1] == feature_idx:
                    # Merge label/frac_nonzero/promoted_tokens into the one with pos
                    features_seen[other_key].update({
                        "label": feat.get("label", features_seen[other_key].get("label")),
                        "frac_nonzero": feat.get("frac_nonzero"),
                        "promoted_tokens": feat.get("promoted_tokens"),
                    })
                    matched = True
            if not matched:
                # No pos info available, include anyway with pos=None
                feat["pos"] = None
                discovered_features.append(feat)

    return {
        "discovered_features": discovered_features,
        "discovered_edges": discovered_edges,
    }


SUBAGENT_SYSTEM_PROMPT_TEMPLATE = """You are a circuit tracing subagent analyzing a target language model's internal circuits via its attribution graph.

Your task: {objective}

Starting point: L{layer}:F{feature_idx} at position {pos}

Model has {n_layers} layers. **Lower-third floor: layer ≤ {lower_third_floor}.**

Instructions:
1. First, call inspect_feature on the starting feature (L{layer}, {feature_idx}) to understand what it represents.
2. Call get_upstream_features on the starting feature to find what feeds into it.
3. For the top 2-3 upstream features (by |direct_effect|), call inspect_feature to get their semantic labels, promoted tokens, and frac_nonzero.
4. Record each feature and connection you discover.
5. Pick the most important upstream feature(s) and repeat: call get_upstream_features to trace one more hop upstream.

**Termination condition (do not stop early).** Continue tracing upstream until BOTH of the following are true:
   (a) You have reached at least one feature in the **lower 1/3 of the model's layers** (layer ≤ {lower_third_floor}), AND
   (b) You have surfaced **at least one token-embedding (`Emb:`) connection** with positive direct_effect on the path.
Taking the embedding-shortcut early (e.g. the starting feature → Emb directly) is allowed and should be recorded, but does NOT terminate exploration of other upstream paths from the starting feature. Continue tracing the next-highest positive-direct_effect upstream features until the layer-floor is also met.

**Legitimate early stops** (in addition to reaching {max_hops} hops):
- Remaining upstream direct effects are notably small compared to ones already traced from this candidate. The signal has decayed, deeper tracing won't surface a refusal-relevant feature.
- The graph genuinely has no upstream feature in layers ≤ {lower_third_floor} reachable from the starting feature (every path terminates at embeddings in mid/late layers). State this explicitly in your report's `explanation` so the orchestrator knows the layer-floor was vacuously satisfied.
Otherwise, prefer to descend deeper rather than stopping early. When done, call report_findings with ALL the features and edges you discovered.

Prioritize features with:
- Large positive direct_effect (strong excitatory influence on the target on this prompt). Only trace and report edges where the upstream feature has a *positive* direct_effect to the target. Negative direct_effect means an inhibitory edge, which is off-target for the tone-down-suppressor methodology and should not be listed in `discovered_edges`.
- Connectivity that suggests a refusal/sensitivity role. A feature is suspicious as a refusal-targeting candidate if it is the strongest upstream driver of a confirmed refusal/negation feature, even if its autointerp label looks generic. **Trust the connectivity (high direct_effect + sparse activation feeding a refusal gate) over the label.**
- Top-promoted tokens that include "cannot", "unable", "unknown", "uncertain", "sorry", "decline", or similar. These signal a feature is functionally part of a refusal/sensitivity pathway, regardless of the label.
- Low frac_nonzero, a tiebreaker among refusal-targeting candidates. Sparser features have lower coherence-budget cost when ablated and generalize better. Do NOT pick a feature for sparsity alone; the role evidence comes first.

When you encounter a feature whose label, top-promoted tokens, or upstream/downstream connectivity suggests **negation, refusal, inability, safety, policy, sensitivity, or suppression**, surface it explicitly in your report. These are the candidates the orchestrator wants to consider for causal intervention. Treat the autointerp label as a hypothesis; the top activating examples and connectivity are the actual evidence of what the feature encodes.

**For each feature you report, include an `interpretation` field**. your assessment of what the feature actually does in this context, based on top activating examples, promoted tokens, and connectivity. This may differ from the autointerp label. For example: "Despite generic 'code snippets' label, promoted tokens (safely, unsafe, discreet) and high direct_effect to the refusal gate suggest this is a sensitivity-precursor feature."

IMPORTANT: You MUST end by calling report_findings. Your results are ONLY captured through report_findings. Do not just write text."""


def _make_tool_dispatch(ctx: ToolContext, *, causal_discovery: bool = False):
    """Shared tool-execution registry for orchestrator AND subagent loops.

    Maps the tool *name* string the LLM emits in a ``tool_use`` block to the
    Python callable that actually runs server-side. Used by ``execute_tool``
    below, which is imported by both ``orchestrator.py`` (its main agent
    loop at line 542) and the subagent loop in this same file (line ~420).

    **Two registries, both required.** Adding a new tool means touching two
    files in lockstep:

      1. ``tool_schemas.py:TOOLS``, the LLM-facing JSON schema (what the
         model is told it can call).
      2. ``_make_tool_dispatch`` (this function), the server-side dispatch
         (what Python actually runs when the model emits the name).

    Update only #1 and the orchestrator's LLM will dutifully call the new
    tool, the dispatcher will return ``{"error": "Unknown tool: ..."}``,
    and the LLM will fall back to a legacy tool. (Commit 83666e6 is an
    example of this exact mistake.)

    ``causal_discovery`` (Part B of huge-refactor.md) toggles the causal-by-default
    pass on the two discovery tools. It is ON for the orchestrator's own calls and
    OFF for the subagent loop's calls (subagents trace many upstream hops; running
    an 800-token ablation on every hop would be ruinous). When ON, ``get_top_features``
    and ``get_upstream_features`` results are post-processed by
    ``_causal_discovery_annotate`` (scale=-1 ablation per discovered feature, shift
    classification, shift-gated reinterpretation), which annotates the returned
    feature rows in place and appends to ``ctx.discovery_reassess``.
    """
    def _top_features(args):
        res = get_top_features(ctx, token=args["token"], k=args.get("k", 10))
        if causal_discovery:
            res = _causal_discovery_annotate(ctx, res)
        return res

    def _upstream_features(args):
        res = get_upstream_features(
            ctx, layer=args["layer"], feature_idx=args["feature_idx"], pos=args["pos"], k=args.get("k", 5)
        )
        if causal_discovery:
            res = _causal_discovery_annotate(ctx, res)
        return res

    return {
        "get_top_logits": lambda args: get_top_logits(ctx, k=args.get("k", 5)),
        "get_top_features": _top_features,
        "inspect_feature": lambda args: inspect_feature(ctx, layer=args["layer"], feature_idx=args["feature_idx"]),
        "get_upstream_features": _upstream_features,
        "build_circuit": lambda args: build_circuit(ctx, nodes=args["nodes"], edges=args["edges"]),
        # Escape-hatch single-feature / single-supernode interventions (no agent-facing
        # `position`. The harness broadcasts across all token positions per changes.md §2.2).
        # `hypothesis` is no longer in the schema; .get() preserves backward compatibility if
        # legacy transcripts replay through this dispatcher with the old arg name.
        "intervene_feature": lambda args: intervene_feature(
            ctx,
            layer=args["layer"],
            feature_idx=args["feature_idx"],
            scale=args["scale"],
            hypothesis=args.get("hypothesis"),
        ),
        "intervene_supernode": lambda args: intervene_supernode(
            ctx,
            features=args["features"],
            scale=args["scale"],
            hypothesis=args.get("hypothesis"),
        ),
        # Three-tool chain (changes.md sec 2.2). Mirrors pipeline.py's dispatch:
        # pin_features keys arrive as JSON-string tuples like "(0, 1, 3)" on the wire and
        # are normalized via _parse_key. batched_anchor_sweep is argless. batched_supernode_sweep
        # forwards `tuples` straight through.
        "pin_features": lambda args: pin_features(
            ctx,
            pre_hypotheses={_parse_key(k): v for k, v in (args.get("pre_hypotheses", {}) or {}).items()},
        ),
        "batched_anchor_sweep": lambda args: batched_anchor_sweep(ctx),
        "batched_supernode_sweep": lambda args: batched_supernode_sweep(
            ctx, tuples=(args.get("tuples", []) or []),
        ),
        # Grafted observational tools (ELK / taboo thread), copied from the pre-merge
        # noncausal package. They take only `args`, so the causal_discovery wrapper above
        # (which only wraps the two discovery tools) does not apply to them. Their schemas
        # live in tool_schemas.TOOLS, both registries move in lockstep.
        "rank_segment_features": lambda args: rank_segment_features(
            ctx,
            seg_start=args["seg_start"],
            seg_end=args["seg_end"],
            k=args.get("k", 10),
            min_layer=args.get("min_layer", 20),
            max_layer=args.get("max_layer", 999),
        ),
        "get_candidate_vote_tally": lambda args: get_candidate_vote_tally(
            ctx,
            min_layer=args.get("min_layer", 20),
            top_k_per_pos=args.get("top_k_per_pos", 30),
        ),
        "get_source_influence": lambda args: get_source_influence(
            ctx, source_positions=args["source_positions"], depth=args.get("depth", 2)
        ),
    }


def execute_tool(
    ctx: ToolContext,
    name: str,
    args: dict,
    *,
    causal_discovery: bool = False,
    allowed_tools=None,
):
    """Dispatch a tool call to the corresponding Python function.

    ``causal_discovery`` is forwarded to ``_make_tool_dispatch``. The orchestrator
    loop passes ``causal_discovery=True`` so its discovery calls carry measured
    causal effect; the subagent loop leaves it False (per-hop ablation would be
    ruinous). See Part B of huge-refactor.md.

    ``allowed_tools`` is the tool surface that run actually advertised. Without it
    exclusion was advisory: the dispatch table is global, so a model that named an
    excluded or retired tool anyway got it executed. Nothing stops a model
    emitting a name it was not offered, and the prompts described these tools for
    a long time, so this is a live path rather than a hypothetical. Live callers
    pass their real list; legacy transcript replay omits it and keeps the old
    dispatch-only behaviour.

    Exceptions become an ``{"error": ...}`` dict so the agent can recover, with one
    exception: an unrecoverable CUDA fault is re-raised. See
    ``is_unrecoverable_cuda_error``.
    """
    dispatch = _make_tool_dispatch(ctx, causal_discovery=causal_discovery)
    if allowed_tools is not None and name not in set(allowed_tools):
        return {
            "error": (
                f"Tool {name!r} was not offered in this run and will not be executed. "
                f"Available tools: {sorted(set(allowed_tools))}."
            )
        }
    if name not in dispatch:
        return {"error": f"Unknown tool: {name}"}
    try:
        return dispatch[name](args)
    except Exception as e:
        if is_unrecoverable_cuda_error(e):
            # Do NOT hand this back as a recoverable tool error. A device-side
            # assert poisons the whole CUDA context, so every later GPU call in
            # this process fails too. Swallowing it let the agent keep going and
            # write a confident ANALYZE narrative with no circuit evidence
            # underneath it. Observed 2026-07-28: one poisoned process produced
            # 7 such results, indistinguishable from real ones without reading
            # the logs. Better to lose the run loudly.
            raise
        return {"error": f"{name} failed: {str(e)}"}


def trace_path_subagent(
    ctx: ToolContext,
    client: LLMClient,
    subagent_model: str,
    *,
    direction: str,  # unused: only "upstream" supported
    starting_layer: int,
    starting_feature_idx: int,
    starting_pos: int,
    objective: str,
    max_hops: int = 12,
    verbose: bool = True,
    label: str = "",
    excluded_tools: list[str] | None = None,
):
    """Dispatch a subagent to trace a path through the circuit.

    Returns dict with discovered_features, discovered_edges, explanation, trace_log,
    and usage (token counts for the subagent).

    `excluded_tools` removes the named tools from the subagent's tool list (so the
    orchestrator can, e.g., run an "output-blind" trace by excluding get_top_logits /
    get_top_features). It is unioned with the always-blocked set below.
    """
    # Subagent tools: investigation tools + report_findings. Intervention tools stay orchestrator-only
    # (they are cross-cutting verification moves on the final pinned circuit, not per-path tracing steps).
    blocked = {
        "build_circuit",
        "trace_path_subagent",
        "intervene_feature",
        "intervene_supernode",
        "pin_features",
        "batched_anchor_sweep",
        "batched_supernode_sweep",
    } | set(excluded_tools or [])
    subagent_tools = [t for t in TOOLS if t["name"] not in blocked]
    subagent_tools.append(REPORT_FINDINGS_TOOL)

    n_layers = ctx.graph.cfg.n_layers
    lower_third_floor = n_layers // 3
    system = SUBAGENT_SYSTEM_PROMPT_TEMPLATE.format(
        objective=objective,
        layer=starting_layer,
        feature_idx=starting_feature_idx,
        pos=starting_pos,
        max_hops=max_hops,
        n_layers=n_layers,
        lower_third_floor=lower_third_floor,
    )
    # Same reconciliation the orchestrator does. The subagent's blocked set is
    # wider (it never gets the intervention or circuit-building tools), so its
    # template is the one most likely to drift into describing something it was
    # not handed. Tools the template never mentions produce no block.
    system = apply_tool_exclusions_to_prompt(
        system, [t["name"] for t in subagent_tools]
    )

    messages = [
        {
            "role": "user",
            "content": (
                f"Begin tracing from L{starting_layer}:F{starting_feature_idx} at position "
                f"{starting_pos}. Objective: {objective}"
            ),
        }
    ]
    if not label:
        label = f"L{starting_layer}:F{starting_feature_idx}@{starting_pos}"

    trace_log = []
    max_turns = max_hops * 5
    report_retries = 0
    max_report_retries = 2

    # Track subagent token usage
    subagent_usage = {
        "model": subagent_model,
        "label": label,
        "objective": objective,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }

    if verbose:
        print(f"\n  [{label}] Starting: L{starting_layer}:F{starting_feature_idx} @ pos {starting_pos}")
        print(f"  [{label}] Objective: {objective}")

    for turn in range(max_turns):
        response = client.create_message(
            model=subagent_model,
            max_tokens=4096,
            system=system,
            tools=subagent_tools,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": _without_reasoning(response.content)})

        # Accumulate usage
        usage = response.usage
        subagent_usage["input_tokens"] += usage.input_tokens
        subagent_usage["output_tokens"] += usage.output_tokens
        subagent_usage["cache_creation_input_tokens"] += getattr(usage, "cache_creation_input_tokens", 0) or 0
        subagent_usage["cache_read_input_tokens"] += getattr(usage, "cache_read_input_tokens", 0) or 0
        # Serving provenance, mirrors orchestrator_usage["providers"].
        served_by = getattr(response, "provider", None) or "unknown"
        providers = subagent_usage.setdefault("providers", {})
        providers[served_by] = providers.get(served_by, 0) + 1

        if response.stop_reason == "end_turn":
            has_report = any(b.type == "tool_use" and b.name == "report_findings"
                            for b in response.content)
            if not has_report and report_retries < max_report_retries:
                report_retries += 1
                if verbose:
                    print(f"  [{label}] Ended without report_findings, nudging ({report_retries}/{max_report_retries}, turn {turn+1})")
                messages.append({"role": "user", "content":
                    "You ended without calling report_findings. You MUST call report_findings "
                    "now with all the features and edges you discovered so far. "
                    "Do not respond with text. Call the report_findings tool."
                })
                continue
            text = next((b.text for b in response.content if b.type == "text"), "")
            # Extract from trace_log since subagent failed to report
            extracted = _extract_features_from_trace_log(trace_log)
            nf = len(extracted["discovered_features"])
            ne = len(extracted["discovered_edges"])
            if verbose:
                print(f"  [{label}] Ended without report_findings (turn {turn+1}), extracted {nf} features, {ne} edges from trace_log")
            return {
                "warning": "Subagent ended without calling report_findings (extracted from trace_log)",
                "text": text,
                "trace_log": trace_log,
                "discovered_features": extracted["discovered_features"],
                "discovered_edges": extracted["discovered_edges"],
                "explanation": text[:500] if text else f"(log_extracted: {nf} features, {ne} edges)",
                "usage": subagent_usage,
            }

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if block.name == "report_findings":
                    findings = block.input
                    reported_features = findings.get("discovered_features", [])
                    reported_edges = findings.get("discovered_edges", [])

                    # Tag agent-reported items
                    for f in reported_features:
                        f["source"] = "agent_reported"
                    for e in reported_edges:
                        e["source"] = "agent_reported"

                    # If agent reported empty/sparse, supplement with trace_log extraction
                    if len(reported_features) < 3 and trace_log:
                        extracted = _extract_features_from_trace_log(trace_log)
                        # Add extracted features not already in reported
                        reported_keys = {(f["layer"], f["feature_idx"], f.get("pos")) for f in reported_features}
                        for ef in extracted["discovered_features"]:
                            key = (ef["layer"], ef["feature_idx"], ef.get("pos"))
                            if key not in reported_keys:
                                reported_features.append(ef)
                        # Add extracted edges not already in reported
                        reported_edge_keys = {
                            (e["from_layer"], e["from_feature_idx"], e["to_layer"], e["to_feature_idx"])
                            for e in reported_edges
                        }
                        for ee in extracted["discovered_edges"]:
                            key = (ee["from_layer"], ee["from_feature_idx"], ee["to_layer"], ee["to_feature_idx"])
                            if key not in reported_edge_keys:
                                reported_edges.append(ee)

                    nf = len(reported_features)
                    ne = len(reported_edges)
                    n_extracted = sum(1 for f in reported_features if f.get("source") == "log_extracted")
                    if verbose:
                        extra = f" (+{n_extracted} extracted)" if n_extracted else ""
                        print(f"  [{label}] Done! {nf} features, {ne} edges{extra} (turn {turn+1})")
                    return {
                        "discovered_features": reported_features,
                        "discovered_edges": reported_edges,
                        "explanation": findings.get("explanation", ""),
                        "trace_log": trace_log,
                        "usage": subagent_usage,
                    }
                result = execute_tool(
                    ctx, block.name, block.input,
                    # The subagent's surface is narrower than the orchestrator's
                    # (no circuit building, no interventions, no nested tracing).
                    allowed_tools=[t["name"] for t in subagent_tools],
                )
                trace_log.append({"tool": block.name, "input": block.input, "output": result})
                if verbose:
                    print(f"  [{label} t{turn+1}] {block.name}({json.dumps(block.input, separators=(',',':'))[:80]})")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

        messages.append({"role": "user", "content": tool_results})

    # Extract from trace_log since subagent exceeded max turns
    extracted = _extract_features_from_trace_log(trace_log)
    nf = len(extracted["discovered_features"])
    ne = len(extracted["discovered_edges"])
    if verbose:
        print(f"  [{label}] Exceeded {max_turns} turns, extracted {nf} features, {ne} edges from trace_log")
    return {
        "error": "Subagent exceeded max turns without reporting findings (extracted from trace_log)",
        "trace_log": trace_log,
        "discovered_features": extracted["discovered_features"],
        "discovered_edges": extracted["discovered_edges"],
        "explanation": f"(log_extracted: {nf} features, {ne} edges from {len(trace_log)} tool calls)",
        "usage": subagent_usage,
    }


# ---------------------------------------------------------------------------
# Retry wrapper (changes.md §2.6)
# ---------------------------------------------------------------------------

def _retry_subagent(fn: Callable, *, max_attempts: int = SUBAGENT_MAX_ATTEMPTS, label: str = ""):
    """Call fn() up to max_attempts times. Returns the first non-exception result.

    Logical failures (raised exceptions) are retried. On final exhaustion, the
    last exception is re-raised. Caller decides whether to catch + convert to
    an error dict. Stacks above LLMClient's API-level retry; this layer is for
    logical failures only (malformed output, max-turn timeout, error returns).
    """
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - intentional broad capture for retry
            last_exc = exc
            if attempt < max_attempts:
                continue
    assert last_exc is not None
    raise last_exc


# ---------------------------------------------------------------------------
# reinterpret_subagent (REASSESS), auto-dispatched, NOT agent-callable
# ---------------------------------------------------------------------------

# Module-level seam so tests can monkeypatch the actual Sonnet call. Production
# callers can override via the optional `client` parameter on reinterpret_subagent.
_SUBAGENT_CLIENT: Callable | None = None


def _build_reinterpret_prompt(
    *,
    layer: int,
    feature_idx: int,
    pos: int,
    inspect_blob: dict,
    shift_profile: dict,
    pre_hypothesis: str,
    user_message: str,
    system_prompt: str,
    baseline_answer: str,
    variant: Literal["committed", "discovery"] = "committed",
) -> str:
    """Assemble the reinterpretation context items into a single string.

    ``committed`` (the default, ANCHOR path) feeds the four items from
    changes.md §2.4: cached inspect_feature blob, the multi-scale shift profile,
    the agent's ``pre_hypothesis``, and prompt context, and asks for the 3-way
    ``divergence``. ``discovery`` (Part B) omits item (3), because at discovery time
    nothing is pinned and there is no prior, and asks for the 2-way
    ``divergence`` (``none`` / ``autointerp_only``).
    """
    parts = [
        f"# REASSESS feature L{layer}:F{feature_idx} at pos {pos}",
        "",
        "## (1) Cached inspect_feature blob",
        json.dumps(inspect_blob, default=str, indent=2),
        "",
        "## (2) Intervention shift profile",
        json.dumps(
            {str(scale): payload for scale, payload in shift_profile.items()},
            default=str,
            indent=2,
        ),
        "",
    ]
    if variant == "committed":
        parts += [
            "## (3) Agent's pre_hypothesis",
            pre_hypothesis,
            "",
            "## (4) Prompt context",
            f"system_prompt: {system_prompt}",
            f"user_message: {user_message}",
            f"baseline_answer: {baseline_answer}",
            "",
            "Return ONLY a JSON object with keys autointerp, pre_label, post_label, divergence "
            "(one of 'none', 'autointerp_only', 'autointerp_and_pre').",
        ]
    else:  # discovery
        parts += [
            "## (3) Prompt context",
            f"system_prompt: {system_prompt}",
            f"user_message: {user_message}",
            f"baseline_answer: {baseline_answer}",
            "",
            "This feature was just discovered (nothing is pinned yet, so there is no prior "
            "hypothesis). Compare the static autointerp label in (1) against what its scale=-1 "
            "ablation actually did in (2). Return ONLY a JSON object with keys autointerp, "
            "post_label, divergence (one of 'none', 'autointerp_only'). 'autointerp_only' means "
            "the static label was misleading and the feature's causal role is only clear from the "
            "ablation; 'none' means the label and the ablation agree.",
        ]
    return "\n".join(parts)


def _resolve_subagent_client(client: Callable | None) -> Callable:
    """Find a callable to use as the subagent backend.

    Resolution order: explicit `client` arg -> module-level _SUBAGENT_CLIENT
    monkeypatch -> mock fixture installed by tests (via mock_subagent_client).
    """
    if client is not None:
        return client
    if _SUBAGENT_CLIENT is not None:
        return _SUBAGENT_CLIENT
    raise RuntimeError(
        "reinterpret_subagent requires a callable client. Provide `client=` or "
        "install one via tests' mock_subagent_client fixture."
    )


# System prompt for the one-shot reinterpretation call when the backend is an
# LLMClient (production). The mock test backend ignores it.
_REINTERPRET_SYSTEM = (
    "You are a mechanistic-interpretability reinterpretation subagent. You are given a "
    "transcoder feature's static autointerp evidence and what happened when it was ablated. "
    "Decide the feature's actual causal role. Respond with ONLY a single JSON object, no prose."
)


def _text_from_response(response: Any) -> str:
    """Pull the concatenated text-block content from an Anthropic-style response.

    Reasoning/thinking blocks are skipped (we only want the final answer text),
    which is also where gpt-oss-120b puts its JSON. Falls back to str(response)
    if no text blocks are present.
    """
    content = getattr(response, "content", None)
    if not content:
        return str(response)
    parts = []
    for block in content:
        btype = getattr(block, "type", None)
        if btype is None and isinstance(block, dict):
            btype = block.get("type")
        if btype in _REASONING_BLOCK_TYPES:
            continue
        text = getattr(block, "text", None)
        if text is None and isinstance(block, dict):
            text = block.get("text")
        if text:
            parts.append(text)
    return "".join(parts) if parts else str(response)


def _invoke_subagent_backend(backend: Callable, prompt: str, model: str) -> tuple:
    """Call the reassess backend, adapting an LLMClient to the one-shot contract.

    Returns ``(raw_text, usage_dict_or_None)``. Two backend shapes are supported:
      - An ``LLMClient`` (production, stashed on ``ctx.subagent_client``): detected
        by its ``create_message`` method. We issue a single-turn message and return
        the response's text content plus its token usage (the one LLM channel that
        previously dropped usage from cost accounting). Single-turn, so the
        multi-turn ``reasoning_details`` replay incompatibility (Part C) does not
        apply here.
      - A plain callable ``(prompt, *, model) -> raw`` (tests' mock_subagent_client,
        or any monkeypatched ``_SUBAGENT_CLIENT``): called directly, usage is None.
    """
    if hasattr(backend, "create_message"):
        response = backend.create_message(
            model=model,
            max_tokens=2048,
            system=_REINTERPRET_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        usage = getattr(response, "usage", None)
        usage_dict = None
        if usage is not None:
            usage_dict = {
                "input_tokens": getattr(usage, "input_tokens", 0) or 0,
                "output_tokens": getattr(usage, "output_tokens", 0) or 0,
                "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0) or 0,
                "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0) or 0,
                # Serving provenance, mirrors the multi-turn paths. REASSESS is
                # gpt-oss traffic, the model the Groq pin exists to audit.
                "providers": {(getattr(response, "provider", None) or "unknown"): 1},
            }
        return _text_from_response(response), usage_dict
    return backend(prompt, model=model), None


def _extract_json_object(raw: str) -> str:
    """Return the last balanced ``{...}`` JSON object substring in ``raw``.

    gpt-oss-120b prefixes a reasoning channel (or wraps the object in ```json
    fences / trailing prose) before the final JSON answer, so a strict
    ``json.loads`` over the whole string fails. We scan for balanced braces and
    return the LAST complete object (the model's final answer, after any
    scratch objects in the preamble). Raises ValueError if none is found.
    """
    last = None
    depth = 0
    start = -1
    in_str = False
    escape = False
    for i, ch in enumerate(raw):
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start >= 0:
                    last = raw[start : i + 1]
    if last is None:
        raise ValueError("no balanced JSON object found in reinterpret_subagent output")
    return last


_ALLOWED_DIVERGENCE = ("none", "autointerp_only", "autointerp_and_pre")
_ALLOWED_DIVERGENCE_DISCOVERY = ("none", "autointerp_only")


def _parse_triple_label(
    raw: Any, *, variant: Literal["committed", "discovery"] = "committed"
) -> dict:
    """Coerce the subagent output to a label record dict, raising on malformation.

    ``committed`` (default) requires the full 4-field triple-label record
    (autointerp, pre_label, post_label, divergence) with the 3-way divergence
    enum. ``discovery`` (Part B) drops ``pre_label`` (nothing is pinned at
    discovery) and restricts divergence to the 2-way enum; the returned record
    still carries a ``pre_label`` key set to "" so downstream consumers see one
    shape. Both variants tolerate a reasoning preamble around the JSON object.
    """
    if isinstance(raw, dict):
        parsed = raw
    elif isinstance(raw, str):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            # Tolerant fallback: locate the last balanced {...} (gpt-oss reasoning channel).
            try:
                parsed = json.loads(_extract_json_object(raw))
            except (json.JSONDecodeError, ValueError) as exc:
                raise ValueError(
                    f"reinterpret_subagent output is not valid JSON: {exc}"
                ) from exc
    else:
        raise ValueError(f"reinterpret_subagent output has unsupported type {type(raw).__name__}")

    if variant == "discovery":
        required = ("autointerp", "post_label", "divergence")
        allowed = _ALLOWED_DIVERGENCE_DISCOVERY
    else:
        required = ("autointerp", "pre_label", "post_label", "divergence")
        allowed = _ALLOWED_DIVERGENCE
    missing = [f for f in required if f not in parsed]
    if missing:
        raise ValueError(f"reinterpret_subagent output missing fields: {missing}")
    divergence = str(parsed["divergence"])
    if divergence not in allowed:
        raise ValueError(
            f"reinterpret_subagent 'divergence' must be one of "
            f"{list(allowed)}; got {divergence!r}"
        )
    return {
        "autointerp": str(parsed["autointerp"]),
        "pre_label": str(parsed.get("pre_label", "")),
        "post_label": str(parsed["post_label"]),
        "divergence": divergence,
    }


def reinterpret_subagent(
    ctx: ToolContext,
    *,
    layer: int,
    feature_idx: int,
    pos: int,
    shift_profile: dict,
    user_message: str,
    system_prompt: str,
    client: Callable | None = None,
    subagent_model: str = DEFAULT_SUBAGENT_MODEL,
    variant: Literal["committed", "discovery"] = "committed",
) -> dict:
    """Reinterpret a shifted feature by combining static + causal evidence.

    Reads cached inspect_feature blob from ctx.inspect_cache, the agent's
    pre_hypothesis from ctx.pinned_features (committed variant only), the shift
    profile, and the user/system prompt context. Returns a label record.

    ``variant="committed"`` (default) is the ANCHOR-phase triple-label record
    (autointerp / pre_label / post_label / 3-way divergence). ``variant="discovery"``
    (Part B) is the discovery-phase record produced by the causal-by-default pass:
    no pre_hypothesis exists yet, so pre_label is omitted and divergence is 2-way.

    Auto-dispatched (NOT agent-callable). Wraps the client call with retry-twice
    (3 total attempts) for logical failures; on exhaustion returns an error dict.
    """
    key = (layer, feature_idx, pos)
    inspect_blob = ctx.inspect_cache.get(key)
    if inspect_blob is None:
        # inspect payloads are position-independent (the Neuronpedia autointerp label is a
        # per-feature property), so fall back to the pos-agnostic (layer, feature_idx, None)
        # key written by the oracle's manual inspect_feature (its schema has no pos) and by
        # the discovery auto-fetch. Without this the reassess saw an empty blob whenever the
        # cached pos did not match (huge-refactor.md B4 cache-hit promise).
        inspect_blob = ctx.inspect_cache.get((layer, feature_idx, None), {})
    pinned = getattr(ctx, "pinned_features", {}) or {}
    pre_hypothesis = pinned.get(key, "")
    baseline_answer = getattr(ctx, "baseline_answer", "") or ""

    prompt_body = _build_reinterpret_prompt(
        layer=layer,
        feature_idx=feature_idx,
        pos=pos,
        inspect_blob=inspect_blob,
        shift_profile=shift_profile,
        pre_hypothesis=pre_hypothesis,
        user_message=user_message,
        system_prompt=system_prompt,
        baseline_answer=baseline_answer,
        variant=variant,
    )

    backend = _resolve_subagent_client(client)

    # Token usage accumulates across retry attempts (each attempt is a real billed
    # call). Mock backends report no usage, so the record carries this zeroed dict
    # with the model id, the same shape judge_rubric uses for its zeroed usage.
    usage_acc = {
        "model": subagent_model,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "providers": {},
    }

    def _attempt():
        raw, usage = _invoke_subagent_backend(backend, prompt_body, subagent_model)
        if usage is not None:
            for key in (
                "input_tokens",
                "output_tokens",
                "cache_creation_input_tokens",
                "cache_read_input_tokens",
            ):
                usage_acc[key] += usage.get(key, 0) or 0
            for host, n in (usage.get("providers") or {}).items():
                usage_acc["providers"][host] = usage_acc["providers"].get(host, 0) + n
        return _parse_triple_label(raw, variant=variant)

    try:
        record = _retry_subagent(_attempt, max_attempts=SUBAGENT_MAX_ATTEMPTS,
                                 label=f"reinterpret L{layer}:F{feature_idx}@{pos}")
    except Exception as exc:  # noqa: BLE001
        record = {
            "error": (
                f"reinterpret_subagent failed after {SUBAGENT_MAX_ATTEMPTS} attempts: {exc}"
            ),
            "divergence": "error",
        }
    record["usage"] = usage_acc
    return record
