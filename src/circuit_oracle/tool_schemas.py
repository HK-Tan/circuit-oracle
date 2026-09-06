"""Anthropic tool definitions (JSON schema) for the circuit oracle agent.

IMPORTANT, adding a new tool here is only HALF the work. Every entry in
``TOOLS`` below also needs a matching entry in ``subagent.py``'s
``_make_tool_dispatch`` (the server-side ``name -> Python callable`` table
shared by both the orchestrator and the subagent loops). If you add the
schema here without registering the dispatch, the orchestrator's LLM will
call the new tool, ``execute_tool`` will return ``{"error": "Unknown tool:
..."}``, and the LLM will silently fall back to a legacy tool, no loud
failure at startup.
"""

import re

INTERVENE_FEATURE_SCHEMA = {
    "name": "intervene_feature",
    "description": (
        "Escape-hatch causal intervention on a single transcoder feature, persistent across "
        "generation. Use sparingly. Phase 1 of VERIFY is handled deterministically by the "
        "harness-driven `batched_anchor_sweep` (scales {0, -1, -2, -3}); this tool exists for "
        "saturation tests at `scale=-4` on a feature whose -3 row still leaked suppression.\n\n"
        "MULTIPLICATIVE STEERING: new_act = baseline + (factor - 1) × effective_baseline, where "
        "effective_baseline = max(10, baseline) for factor ≤ 0. Sign convention: NEGATIVE/ZERO "
        "= reverse or ablate (refusal/negation/suppression); POSITIVE < 1 = reduce; POSITIVE > 1 "
        "= amplify (diagnostic only).\n\n"
        "BROADCASTING (important): the intervention is applied at EVERY token position in the "
        "full context (`pos: slice(None, None)` at the hook level). The harness reads the "
        "feature's anchor / bookkeeping position from `ctx.pinned_features` (or the "
        "max-activation position from `ctx.baseline_activations` if the feature isn't pinned) "
        "for the multiplicative-steering baseline lookup. The agent does not pass a `position`; "
        "see changes.md §2.2 'Position semantics (broadcast across all positions)'.\n\n"
        "Returns top-5 next-token probabilities before/after AND a greedy-decoded answer string."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "layer": {
                "type": "integer",
                "description": "Layer index of the feature (0-based).",
            },
            "feature_idx": {
                "type": "integer",
                "description": "Transcoder feature index within the layer.",
            },
            "scale": {
                "type": "number",
                "enum": [-4, -3, -2, -1, 0, 0.5, 2],
                "description": (
                    "MULTIPLICATIVE FACTOR. new_act = baseline + (factor - 1) × effective_baseline. "
                    "For factor ≤ 0, effective_baseline = max(10, baseline). "
                    "-4 = saturation test (escape-hatch escalation after -3 leaked). "
                    "Other factors {-3,-2,-1,0,0.5,2} are typically reached through the batched "
                    "sweeps; use this tool only for one-off saturation or amplification probes."
                ),
            },
        },
        "required": ["layer", "feature_idx", "scale"],
    },
}


INTERVENE_SUPERNODE_SCHEMA = {
    "name": "intervene_supernode",
    "description": (
        "Escape-hatch causal intervention on a group of features (a supernode) at one factor. "
        "Phase 3 of VERIFY is normally driven by `batched_supernode_sweep`; this tool exists "
        "for saturation tests at `scale=-4` on a tuple whose -3 row still leaked suppression.\n\n"
        "MULTIPLICATIVE STEERING: new_act = baseline + (factor - 1) × effective_baseline, "
        "applied per-feature. Returns the same before/after shape as `intervene_feature`.\n\n"
        "BROADCASTING (important): each feature's intervention is applied at EVERY token "
        "position in the full context (`pos: slice(None, None)` at the hook level). The harness "
        "reads each feature's anchor / bookkeeping position from `ctx.pinned_features` (or the "
        "max-activation position from `ctx.baseline_activations` if the feature isn't pinned) "
        "for the multiplicative-steering baseline lookup. The agent does not pass any "
        "`position`; a feature here is one unique `(layer, feature_idx)` pair. See changes.md "
        "§2.2 'Position semantics (broadcast across all positions)'."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "features": {
                "type": "array",
                "minItems": 2,
                "items": {
                    "type": "object",
                    "properties": {
                        "layer": {"type": "integer"},
                        "feature_idx": {"type": "integer"},
                    },
                    "required": ["layer", "feature_idx"],
                },
                "description": (
                    "Group of features to intervene on jointly. Pick 2+ features that you "
                    "have a reason to believe gate the same suppression behavior. One factor "
                    "applies to all. Each entry is a `{layer, feature_idx}` dict; no position "
                    "argument (the intervention broadcasts across all positions)."
                ),
            },
            "scale": {
                "type": "number",
                "enum": [-4, -3, -2, -1, 0, 0.5, 2],
                "description": (
                    "MULTIPLICATIVE FACTOR applied to every feature in the group. "
                    "new_act = baseline + (factor - 1) × effective_baseline, where "
                    "effective_baseline = max(10, baseline) for factor ≤ 0. "
                    "-4 = saturation test (typical escape-hatch use)."
                ),
            },
        },
        "required": ["features", "scale"],
    },
}

PIN_FEATURES_SCHEMA = {
    "name": "pin_features",
    "description": (
        "Commit a one-sentence prior-belief hypothesis for EVERY feature in the "
        "circuit you just built. Each key is the (layer, feature_idx, pos) triple "
        "from build_circuit, stringified as a Python tuple literal. Subset or "
        "superset of build_features raises an error listing the offending keys. "
        "After this succeeds, call the argless `batched_anchor_sweep()`.\n\n"
        "WORKED EXAMPLE (UNRELATED DOMAIN, illustrates JSON shape only, do not "
        "transfer this domain or vocabulary into your actual hypotheses). Suppose "
        "an unrelated experiment built a circuit for the prompt 'The capital of "
        "France is' with three pinned features at (L=4,F=12000,pos=2), "
        "(L=15,F=44000,pos=5), and (L=28,F=99000,pos=5). The pin_features call "
        "would look like:\n"
        "{\n"
        "  \"pre_hypotheses\": {\n"
        "    \"(4, 12000, 2)\": \"Early-layer geography-token detector firing on the "
        "word 'capital'; carries the 'we are being asked about a capital city' frame.\",\n"
        "    \"(15, 44000, 5)\": \"Mid-layer France-related entity feature; binds the "
        "country mention to a country-specific representation.\",\n"
        "    \"(28, 99000, 5)\": \"Late-layer city-name promoter; biases the next "
        "token toward city tokens rather than other completions.\"\n"
        "  }\n"
        "}\n\n"
        "Write your own hypotheses for whatever domain your actual circuit is in, "
        "grounded in the trace_path subagent reports. Hypotheses can be uncertain "
        "('likely', 'possibly'); do not trust the autointerp label, which is often "
        "misleading."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "pre_hypotheses": {
                "type": "object",
                "description": (
                    "Object whose keys are stringified (layer, feature_idx, pos) "
                    "triples like \"(10, 85272, 34)\" (list form \"[10, 85272, 34]\" "
                    "also accepted) and whose values are non-empty one-sentence "
                    "hypotheses. ONE key per feature in build_features, no more, "
                    "no fewer. See the tool description for a worked example."
                ),
                "additionalProperties": {"type": "string"},
            },
        },
        "required": ["pre_hypotheses"],
    },
}


BATCHED_ANCHOR_SWEEP_SCHEMA = {
    "name": "batched_anchor_sweep",
    "description": (
        "Argless. Reads `ctx.pinned_features` and runs a deterministic K×4 sweep "
        "over scales {0, -1, -2, -3} on every pinned feature. Returns per-(feature, "
        "scale) measurements with a server-side `shift_bucket` annotation. Raises "
        "ValueError(\"call pin_features first\") if the pinned set is empty."
    ),
    "input_schema": {"type": "object", "properties": {}},
}


BATCHED_SUPERNODE_SWEEP_SCHEMA = {
    "name": "batched_supernode_sweep",
    "description": (
        "Phase 3 of VERIFY. Agent-driven supernode sweep: T tuples × 4 scales rows "
        "in one batched call. Required ≥3 tuples per call; the orchestrator enforces "
        "≥2 calls per run."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "tuples": {
                "type": "array",
                "minItems": 3,
                "items": {
                    "type": "object",
                    "properties": {
                        "features": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "layer": {"type": "integer"},
                                    "feature_idx": {"type": "integer"},
                                    "pos": {"type": "integer"},
                                },
                                "required": ["layer", "feature_idx", "pos"],
                            },
                        },
                        "rationale": {"type": "string"},
                    },
                    "required": ["features", "rationale"],
                },
            },
        },
        "required": ["tuples"],
    },
}


TOOLS = [
    {
        "name": "get_top_logits",
        "description": (
            "Returns the top-k next-token candidates (and probabilities) at the single "
            "prediction position captured by this attribution graph. Only ~95% of probability "
            "mass is retained, so often just 1-3 tokens are available.\n\n"
            "Output fields:\n"
            "- token: the decoded vocabulary token\n"
            "- probability: softmax probability (0-1)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "k": {
                    "type": "integer",
                    "description": "Number of top tokens to return (default 5)",
                }
            },
        },
    },
    {
        "name": "get_top_features",
        "description": (
            "Returns the top-k transcoder features by direct effect on `token`'s logit at the "
            "single prediction position captured by this attribution graph. `token` must be one "
            "of the tokens returned by `get_top_logits`. To walk one hop upstream from any of "
            "these features, use `get_upstream_features`.\n\n"
            "Output fields:\n"
            "- layer: transformer layer (0-35) where the feature lives\n"
            "- feature_idx: index within the transcoder at that layer\n"
            "- pos: input-prompt token position where the feature fires\n"
            "- activation: magnitude of the feature's activation value\n"
            "- direct_effect: signed contribution to the target token's logit. Positive pushes "
            "toward the token, negative pushes away. Key metric for importance."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "description": "The target output token to analyze (must be one of the tokens returned by get_top_logits, e.g. 'Base', 'Basket')",
                },
                "k": {
                    "type": "integer",
                    "description": "Number of top features to return (default 15)",
                },
            },
            "required": ["token"],
        },
    },
    {
        "name": "inspect_feature",
        "description": (
            "Looks up a transcoder feature on Neuronpedia and returns its autointerp label, "
            "top activating examples, and promoted/suppressed tokens. Use this to understand "
            "what a feature represents semantically.\n\n"
            "Output fields:\n"
            "- label: auto-generated natural language description of what this feature detects "
            "(e.g. 'basketball-related terms', 'quotation marks in dialogue'). Treat this label "
            "as a hypothesis. The top activating examples are the actual evidence.\n"
            "- top_activating_examples: 3 text snippets from evaluation data where this feature "
            "fired most strongly. Each has text_snippet, max_activation, and max_token (the "
            "specific token that triggered it). Examine these to decide what role the feature is "
            "actually playing here; do not just trust the headline label.\n"
            "- promoted_tokens: top 10 vocabulary tokens whose output logits INCREASE when this "
            "feature fires (computed by projecting the feature's decoder vector onto the "
            "unembedding matrix). These reveal what the feature 'wants to say'.\n"
            "- suppressed_tokens: top 10 vocabulary tokens whose output logits DECREASE when "
            "this feature fires. These reveal what the feature inhibits.\n"
            "- frac_nonzero: fraction of tokens in the evaluation dataset where this feature "
            "fires (0-1). LOW values (e.g. 0.001) mean the feature is highly specific and "
            "selective. It only fires in rare contexts. HIGH values (e.g. 0.5+) mean the "
            "feature is generic and fires broadly. CAVEAT: low frac_nonzero indicates the "
            "feature is specific in feature-space, but specificity is NOT the same as "
            "entity-specificity, a low-frac_nonzero feature can be very specific to a category "
            "(e.g., a country, a profession) without being specific to any individual entity. "
            "Decide what the feature actually encodes by examining the top_activating_examples "
            "directly, not by reading frac_nonzero alone."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "layer": {
                    "type": "integer",
                    "description": "The transformer layer of the feature",
                },
                "feature_idx": {
                    "type": "integer",
                    "description": "The feature index within the transcoder",
                },
            },
            "required": ["layer", "feature_idx"],
        },
    },
    {
        "name": "get_upstream_features",
        "description": (
            "Returns the top-k upstream nodes that feed into a given feature, "
            "ranked by signed direct_effect (most positive first; the activation-scaled "
            "contribution to the target on this input). Use this to trace the circuit "
            "backward and understand where the signal originates. Inhibitory edges "
            "(negative direct_effect) fall to the bottom and are off-target for the "
            "tone-down-suppressor methodology.\n\n"
            "Results may include two types of nodes:\n"
            "1. Transcoder features (type='feature'): with layer, feature_idx, pos, "
            "direct_effect, activation\n"
            "2. Embedding nodes (type='embedding'): raw token embeddings from the input, "
            "with token (decoded string), pos, direct_effect. These represent the bottom "
            "of the circuit, the raw input token representations before any transformer "
            "layers.\n\n"
            "Output fields:\n"
            "- type: 'feature' or 'embedding'\n"
            "- layer: transformer layer of the upstream feature (type='feature' only)\n"
            "- feature_idx: index within the upstream transcoder (type='feature' only)\n"
            "- token: decoded input token string (type='embedding' only)\n"
            "- pos: token position\n"
            "- direct_effect: the upstream node's activation-scaled contribution to the "
            "target feature on this input (= activation × Jacobian sensitivity, "
            "pre-computed by circuit_tracer's backward attribution). Positive = excites "
            "the downstream feature. Negative = inhibits. **This is the ranking metric.** "
            "Same quantity that get_top_features returns under the same name.\n"
            "- activation: the upstream feature's activation magnitude at that position "
            "(type='feature' only). Diagnostic only. Use direct_effect as the importance "
            "metric, not activation."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "layer": {
                    "type": "integer",
                    "description": "The transformer layer of the target feature",
                },
                "feature_idx": {
                    "type": "integer",
                    "description": "The feature index of the target feature",
                },
                "pos": {
                    "type": "integer",
                    "description": "The token position of the target feature",
                },
                "k": {
                    "type": "integer",
                    "description": "Number of top upstream features to return (default 10). Trace deeper by chaining calls. The natural floor is the embedding nodes (type='embedding'), so widen k freely if no embedding nodes appear yet.",
                },
            },
            "required": ["layer", "feature_idx", "pos"],
        },
    },
    {
        "name": "build_circuit",
        "description": (
            "Declare your final attribution circuit. Can be called multiple times (each call "
            "overwrites the previous circuit). Record which features and connections form the "
            "circuit supporting your conclusion. Group related features into supernodes with "
            "descriptive labels. Every node must reference at least one concrete feature, except "
            "token-embedding nodes (Emb: convention, layer=0, features=[]) and output logit nodes "
            "(layer=36, features=[]). If the result includes a 'warning' field, consider tracing "
            "deeper and calling again.\n\n"
            "IMPORTANT. Edge direction convention: edges represent signal flow direction "
            "(forward through the network). 'from' is the upstream/earlier-layer node and "
            "'to' is the downstream/later-layer node. For example, an edge from an early-layer "
            "entity recognition node to a late-layer output-driving node means the entity "
            "signal feeds into the output."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nodes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "Short unique ID for referencing in edges",
                            },
                            "label": {
                                "type": "string",
                                "description": "Human-readable label for this supernode",
                            },
                            "layer": {
                                "type": "integer",
                                "description": "Layer for visual layout (dominant layer of grouped features)",
                            },
                            "features": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "layer": {"type": "integer"},
                                        "feature_idx": {"type": "integer"},
                                        "pos": {"type": "integer"},
                                    },
                                    "required": ["layer", "feature_idx", "pos"],
                                },
                                "description": "Concrete features grouped into this supernode",
                            },
                        },
                        "required": ["id", "label", "layer", "features"],
                    },
                },
                "edges": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "from": {
                                "type": "string",
                                "description": "Upstream node ID (earlier layer)",
                            },
                            "to": {
                                "type": "string",
                                "description": "Downstream node ID (later layer)",
                            },
                        },
                        "required": ["from", "to"],
                    },
                    "description": (
                        "List of edges between supernodes (or supernodes and the output "
                        "logit terminal). Topology only. Only include an edge if there is "
                        "a positive direct_effect between at least one feature in the "
                        "upstream supernode and one feature in the downstream supernode."
                    ),
                },
            },
            "required": ["nodes", "edges"],
        },
    },
    {
        "name": "trace_path_subagent",
        "description": (
            "Dispatch a subagent to deeply trace a path through the attribution "
            "circuit. The subagent gets its own context window and will independently call "
            "get_upstream_features and inspect_feature across multiple hops to trace upstream "
            "from the starting feature. Returns all discovered features (with labels, "
            "frac_nonzero, promoted tokens, and the subagent's interpretation) and edges.\n\n"
            "Use this instead of manually calling get_upstream_features + inspect_feature "
            "repeatedly. Each subagent can trace ~4-5 hops deep. Dispatch multiple subagents "
            "in parallel to trace different paths simultaneously.\n\n"
            "Output fields:\n"
            "- discovered_features: list of features found along the path. Each has layer, "
            "feature_idx, pos, label, interpretation, frac_nonzero, promoted_tokens, and "
            "source ('agent_reported' or 'log_extracted'). Features with source='log_extracted' "
            "were explored by the subagent but not explicitly reported. They may have "
            "label='not_inspected' if the subagent never called inspect_feature on them. "
            "For these, call inspect_feature yourself to get semantic info.\n"
            "- discovered_edges: list of connections between features with their direct_effect\n"
            "- explanation: the subagent's summary of what this path represents"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": ["upstream"],
                    "description": "Tracing direction (currently only 'upstream' is supported)",
                },
                "starting_layer": {
                    "type": "integer",
                    "description": "Layer of the feature to start tracing from",
                },
                "starting_feature_idx": {
                    "type": "integer",
                    "description": "Feature index to start tracing from",
                },
                "starting_pos": {
                    "type": "integer",
                    "description": "Token position of the starting feature",
                },
                "objective": {
                    "type": "string",
                    "description": "What the subagent should investigate",
                },
                "max_hops": {
                    "type": "integer",
                    "description": "Maximum number of upstream hops (default 12)",
                },
            },
            "required": [
                "direction",
                "starting_layer",
                "starting_feature_idx",
                "starting_pos",
                "objective",
            ],
        },
    },
    # Three grafted observational tools (ELK / taboo thread). Schemas copied
    # verbatim from the pre-merge noncausal package. Their dispatch entries live
    # in subagent._make_tool_dispatch, both registries move in lockstep.
    {
        "name": "rank_segment_features",
        "description": (
            "Mean-over-segment diff-specificity ranking. One call ranks "
            "every feature active in the target graph over positions "
            "[seg_start, seg_end) by "
            "`mean(max(|target_act|-max_sibling(|sibling_act|), 0)) * "
            "-log(activation_frequency) * -log(base_density+eps)`. The "
            "base_density multiplier (from ctx.base_feature_density, "
            "calibrated on a broader baseline pool such as same-model "
            "graphs over multiple prompts) strips features that fire "
            "densely on the baseline even after same-prompt sibling "
            "subtraction, the cross-prompt analogue of TF-IDF.\n\n"
            "Use this as the PRIMARY discovery pass over the assistant-"
            "prefill segment; a single call typically surfaces the "
            "secret-bearing features. Returns top-k with `top_logits` "
            "from the transcoder's decoder (NOT the model's output "
            "distribution, so immune to LoRA output suppression).\n\n"
            "Output fields:\n"
            "- layer, feature_idx\n"
            "- mean_diff: mean positive diff over segment\n"
            "- activation_frequency: transcoder global firing rate\n"
            "- base_density: firing rate in the baseline pool (null if "
            "ctx.base_feature_density not supplied)\n"
            "- score: ranking key\n"
            "- top_logits: top promoted vocabulary tokens"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "seg_start": {
                    "type": "integer",
                    "description": "First position of the segment (inclusive).",
                },
                "seg_end": {
                    "type": "integer",
                    "description": "Last position of the segment (exclusive).",
                },
                "k": {"type": "integer", "description": "Features to return (default 10)."},
                "min_layer": {"type": "integer", "description": "Lower bound on layer (default 20)."},
                "max_layer": {"type": "integer", "description": "Upper bound on layer (default 999)."},
            },
            "required": ["seg_start", "seg_end"],
        },
    },
    {
        "name": "get_candidate_vote_tally",
        "description": (
            "Closed-set classification over all positions in one call. "
            "For each position, takes the top-k diff-specificity features, "
            "stems each feature's top_logits, and counts a vote for any "
            "candidate whose surface form (or common morphological variant) "
            "matches a stem. Stems that don't match any candidate are "
            "discarded. The candidate list IS the filter.\n\n"
            "Returns a tally sorted by matched votes with a handful of "
            "contributing (layer, pos, feature_idx) entries per candidate "
            "so you can drill down with inspect_feature / get_upstream_features "
            "to verify. This is typically the FIRST tool to call on a taboo- "
            "or probe-style graph with a fixed candidate menu.\n\n"
            "Output fields:\n"
            "- tally: list of {candidate, matched_votes, contributing_features[]}\n"
            "- total_matched_votes, n_sibling_graphs, settings"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "min_layer": {
                    "type": "integer",
                    "description": "Ignore features below this layer (default 20).",
                },
                "top_k_per_pos": {
                    "type": "integer",
                    "description": "Per-position feature cap (default 30).",
                },
            },
        },
    },
    {
        "name": "get_source_influence",
        "description": (
            "Computes the NET SIGNED multi-hop influence flowing from a set of "
            "input token positions to the target output logit, by propagating "
            "backward through the ENTIRE attribution graph (sign-preserving, "
            "row-normalised, `depth` hops). This is the full multi-hop signed "
            "total you cannot reliably accumulate by hand with "
            "get_upstream_features. Call this instead of doing it manually.\n\n"
            "Output fields:\n"
            "- S_pct_of_total: PRIMARY, net signed share (%) of the graph's "
            "total influence carried from `source_positions` to the logit\n"
            "- S_over_Rsum / S_over_R / R_pct_of_total: auxiliary scale-free "
            "ratios (context only, not the primary readout)\n"
            "- S_signed_raw / R_signed_raw: raw propagated values (~1e-4, "
            "model-specific, auxiliary only, do NOT threshold these)\n"
            "- top_source_features: source-position features contributing "
            "most (layer, feature_idx, pos, signed_contrib_pct), pass to "
            "inspect_feature for a NARRATIVE check only\n"
            "- note: how to read it\n\n"
            "Interpretation: judge S_pct_of_total. SOFT empirical reference "
            "(not a hard cutoff, not model-tuned): source-driven/COPIED cases "
            "tend to carry a substantial signed share (order of ~10% or "
            "more) while independent cases carry only low single digits. "
            "Both classes usually have value detectors on the source tokens, "
            "so autointerp corroborates the story but the signed share "
            "decides."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "source_positions": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": (
                        "Input token positions to measure influence FROM "
                        "(e.g. the tool_response value token positions)."
                    ),
                },
                "depth": {
                    "type": "integer",
                    "description": "Number of backward hops to accumulate (default 2; do not override unless asked).",
                },
            },
            "required": ["source_positions"],
        },
    },
    # INTERVENE_FEATURE_SCHEMA / INTERVENE_SUPERNODE_SCHEMA are deliberately not
    # offered to the agent; see RETIRED_TOOL_NAMES below. The schemas and their
    # Python functions stay defined so legacy transcripts still replay and the
    # parity tests still have something to call. Re-adding them here is all it
    # takes to bring them back, and apply_tool_exclusions_to_prompt then stops
    # stripping their prompt entries automatically.
    PIN_FEATURES_SCHEMA,
    BATCHED_ANCHOR_SWEEP_SCHEMA,
    BATCHED_SUPERNODE_SWEEP_SCHEMA,
]


CAUSAL_ONLY_TOOLS = frozenset({
    "intervene_feature",
    "intervene_supernode",
    "pin_features",
    "batched_anchor_sweep",
    "batched_supernode_sweep",
})


# Retired from the agent-facing surface, kept importable for legacy transcript
# replay and the parity tests. The harness owns intervention execution now: the
# agent proposes feature sets through batched_supernode_sweep and the harness
# runs T x 4 rows in one batched call, and batched_anchor_sweep is argless. The
# single-call tools were the pre-refactor design where the agent executed one
# intervention at a time, and they were the only path that reached the
# non-KV-cached decode. Their one unique capability was factor=-4 saturation,
# which the fixed harness factor set {0, -1, -2, -3} does not cover.
RETIRED_TOOL_NAMES = frozenset({"intervene_feature", "intervene_supernode"})

# Every tool name a prompt might legitimately mention, retired ones included.
# The prompt-exclusion pass below diffs against this, so a tool that was dropped
# from TOOLS is still recognized as "advertised but unavailable" rather than
# going unnoticed.
ALL_KNOWN_TOOL_NAMES = frozenset(t["name"] for t in TOOLS) | RETIRED_TOOL_NAMES


def _bullet_subject(line: str) -> str | None:
    """The tool a list bullet is the inventory entry *for*, or None.

    Deliberately narrow. Only a bullet that opens with the bare tool name counts,
    because the prompts mention tools in three structurally different ways and
    only one of them is safe to delete:

      - `inspect_feature(layer, feature_idx)`. Neuronpedia label, ...   <- entry
      - Call `inspect_feature` to get the semantic label ...             <- instruction
      - Neuronpedia labels and inspect_feature top prompts are ...       <- advice
      - trace_path_subagent: ... independently calls ... inspect_feature <- another tool's entry

    Only the first is this tool's inventory entry. Deleting the third would drop
    unrelated guidance and deleting the fourth would remove a tool that IS
    offered, so both must survive. The leading-lowercase match is what separates
    them: prose bullets here start with a capitalized word.
    """
    match = re.match(r"^\s*[-*+]\s+(.*)$", line)
    if not match:
        return None
    rest = match.group(1).lstrip("`*_ ")
    name = re.match(r"([a-z_][a-z0-9_]*)", rest)
    return name.group(1) if name else None


# Separators between a tool bullet's subject and its description. Everything
# before the first one is the subject span; everything after is prose.
_BULLET_SUBJECT_SEPARATORS = (". ", " - ", ":")


def _bullet_subject_span(line: str) -> str:
    """The part of a bullet that names its subject(s), excluding the description.

    A bullet can name several tools for two very different reasons, and deleting
    on the wrong one loses information:

      - `intervene_feature` / `intervene_supernode`. Escape hatches ...
            two CO-SUBJECTS, both retired, so the whole line goes

      - get_candidate_vote_tally(...): ... when rank_segment_features alone is
        ambiguous ...
            one subject plus a CROSS-REFERENCE to a tool that is still offered

    An earlier version required every tool named anywhere on the line to be
    unavailable, which kept the second line alive whenever its cross-referenced
    tool survived. That is exactly the open-ELK arms, which exclude
    get_candidate_vote_tally and were still being handed its inventory entry.
    Splitting at the description separator tells co-subjects from mentions.
    """
    body = re.sub(r"^\s*[-*+]\s+", "", line)
    cut = len(body)
    for sep in _BULLET_SUBJECT_SEPARATORS:
        found = body.find(sep)
        if found != -1:
            cut = min(cut, found)
    return body[:cut]


def apply_tool_exclusions_to_prompt(
    prompt: str, offered_tool_names, *, all_known_names=None
) -> str:
    """Reconcile a system prompt with the tool surface the run actually offers.

    ``excluded_tools`` only ever filtered the JSON schema list. The prompts are
    static text, so an excluded tool stayed advertised: refusal-arm2 and
    probes-arm2 drop inspect_feature while their prompt still says "Call
    `inspect_feature` to get the semantic label", and the ELK arms do the same
    through their own exclusion lists. An agent told to call a tool it was not
    given either wastes turns or invents the result.

    Two passes, in order of confidence:

    1. Delete tool-inventory bullets for unavailable tools (see ``_bullet_subject``
       for why only that shape qualifies). A bullet is deleted only when every
       tool in its *subject span* is unavailable, so a combined entry documenting
       an offered tool survives while a cross-reference in the description does
       not save an entry that should go (see ``_bullet_subject_span``).
    2. Append an authoritative block naming what is unavailable. Prose mentions
       and imperative instructions are not safely removable by pattern, so they
       are overridden explicitly instead of surgically edited. A stated
       contradiction that resolves one way beats silent misdirection.

    Only tools the prompt actually mentions are named, so a run never carries a
    block about tools it was never told about. Returns ``prompt`` unchanged when
    there is nothing to reconcile, which is the common case.
    """
    known = frozenset(all_known_names if all_known_names is not None else ALL_KNOWN_TOOL_NAMES)
    unavailable = known - set(offered_tool_names)
    mentioned = sorted(
        name for name in unavailable
        if re.search(rf"\b{re.escape(name)}\b", prompt)
    )
    if not mentioned:
        return prompt

    mentioned_set = set(mentioned)
    kept = []
    for line in prompt.splitlines():
        subject = _bullet_subject(line)
        if subject in mentioned_set:
            span = _bullet_subject_span(line)
            co_subjects = {n for n in known if re.search(rf"\b{re.escape(n)}\b", span)}
            if co_subjects <= mentioned_set:
                continue
        kept.append(line)

    return "\n".join(kept).rstrip() + (
        "\n\n## Tools not available in this run\n\n"
        f"These tools are NOT available and must not be called: "
        f"{', '.join(f'`{n}`' for n in mentioned)}. "
        "This overrides any earlier text in this prompt that describes them or "
        "tells you to use them. Complete the task with the tools you were given, "
        "and do not report a result you would have obtained from a missing tool.\n"
    )


_LOGIT_LAYER_ANCHOR = "output logit nodes (layer=36, features=[])"


def _retarget_logit_layer(tools: list, n_layers: int) -> list:
    """Rewrite the build_circuit description so it quotes this subject's n_layers.

    The canonical text says layer=36 (Qwen3-4B, the causal track). On a subject
    with a different depth the description has to move with the prompt and the
    build_circuit validator, or the agent is told to declare a logit node the
    validator will reject. Anchor-checked: a silent no-op here would reintroduce
    exactly that mismatch.
    """
    out = []
    for tool in tools:
        if tool["name"] != "build_circuit":
            out.append(tool)
            continue
        description = tool["description"]
        if _LOGIT_LAYER_ANCHOR not in description:
            raise RuntimeError(
                "build_circuit description no longer contains the logit-layer "
                f"anchor {_LOGIT_LAYER_ANCHOR!r}; update _retarget_logit_layer."
            )
        out.append({
            **tool,
            "description": description.replace(
                _LOGIT_LAYER_ANCHOR,
                _LOGIT_LAYER_ANCHOR.replace("layer=36", f"layer={n_layers}"),
            ),
        })
    return out


def build_orchestrator_tools(
    *, causal: bool = True, excluded_tools=None, n_layers: int | None = None
) -> list:
    """Tool list for the orchestrator loop.

    Returns the base ``TOOLS`` list minus anything blocked. The orchestrator and
    subagents share the same schema set, the difference is at dispatch time
    (``execute_tool(..., causal_discovery=True)`` for the orchestrator), where
    discovery tools run the causal-by-default pass. (The former flag-gated
    ``screen_upstream_causality`` tool was retired in huge-refactor.md Part B,
    causal discovery is now on by default.)

    ``causal=False`` (observational mode, probes and ELK) drops the intervention
    schemas, which have no ReplacementModel behind them on those threads.
    ``CAUSAL_ONLY_TOOLS`` names five, but two are retired from ``TOOLS``, so three
    are actually dropped. ``excluded_tools`` is the per-run narrowing the entry scripts pass.
    The default stays ``causal=True`` so an argless call keeps returning the full
    causal surface.

    ``n_layers`` retargets the build_circuit logit-layer convention at the subject
    model. Omit it and the description keeps the Qwen3-4B default of 36.
    """
    blocked = set(excluded_tools or [])
    unknown = blocked - {t["name"] for t in TOOLS}
    if unknown:
        raise ValueError(
            f"excluded_tools names no such tool: {sorted(unknown)}. Known tools: "
            f"{sorted(t['name'] for t in TOOLS)}. A stale name here is a silent "
            "no-op, which is how a retired tool stayed in the ELK exclusion lists."
        )
    if not causal:
        blocked |= CAUSAL_ONLY_TOOLS
    tools = [t for t in TOOLS if t["name"] not in blocked]
    if n_layers is not None and int(n_layers) != 36:
        tools = _retarget_logit_layer(tools, int(n_layers))
    return tools


REPORT_FINDINGS_TOOL = {
    "name": "report_findings",
    "description": (
        "Report all features and connections you discovered along this tracing path. "
        "You MUST call this when you are done tracing to return your results to the orchestrator.\n\n"
        "IMPORTANT: Each entry in discovered_features and discovered_edges must be a JSON object, "
        "NOT a string. For example:\n"
        '  discovered_features: [{"layer": 7, "feature_idx": 97156, "pos": 26, "label": "Jordan", '
        '"interpretation": "Entity recognition for the basketball player"}]\n'
        '  discovered_edges: [{"from_layer": 4, "from_feature_idx": 144556, "from_pos": 26, '
        '"to_layer": 7, "to_feature_idx": 97156, "to_pos": 26, "direct_effect": 1.23}]'
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "discovered_features": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "layer": {"type": "integer"},
                        "feature_idx": {"type": "integer"},
                        "pos": {"type": "integer"},
                        "label": {
                            "type": "string",
                            "description": "Semantic label from inspect_feature (the autointerp hypothesis)",
                        },
                        "interpretation": {
                            "type": "string",
                            "description": (
                                "YOUR interpretation of what this feature does in context, based on "
                                "top activating examples, promoted tokens, and connectivity. This may "
                                "differ from the autointerp label. E.g., 'Despite generic label, "
                                "promoted tokens (cannot, unable) suggest this is a negation gate.'"
                            ),
                        },
                        "frac_nonzero": {
                            "type": "number",
                            "description": "Sparsity from inspect_feature",
                        },
                        "promoted_tokens": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Top promoted tokens from inspect_feature",
                        },
                    },
                    "required": ["layer", "feature_idx", "pos", "label", "interpretation"],
                },
                "description": "All features discovered during tracing",
            },
            "discovered_edges": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "from_layer": {"type": "integer"},
                        "from_feature_idx": {"type": "integer"},
                        "from_pos": {"type": "integer"},
                        "to_layer": {"type": "integer"},
                        "to_feature_idx": {"type": "integer"},
                        "to_pos": {"type": "integer"},
                        "direct_effect": {
                            "type": "number",
                            "description": (
                                "The direct_effect value from get_upstream_features "
                                "between the two features."
                            ),
                        },
                    },
                    "required": [
                        "from_layer",
                        "from_feature_idx",
                        "from_pos",
                        "to_layer",
                        "to_feature_idx",
                        "to_pos",
                        "direct_effect",
                    ],
                },
                "description": "All edges (connections) discovered during tracing",
            },
            "explanation": {
                "type": "string",
                "description": "Brief summary of what this path represents and key findings",
            },
        },
        "required": ["discovered_features", "discovered_edges", "explanation"],
    },
}
