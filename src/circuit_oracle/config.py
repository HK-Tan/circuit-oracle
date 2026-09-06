"""Configuration dataclasses for circuit oracle runs."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from .constants import DEFAULT_SUBAGENT_MODEL


def _default_graph_cache_dir() -> str:
    """Graph store default, honoring GRAPH_STORE (same convention as
    refusal-jailbreaking/scripts/build_graph.py: graphs live in
    $GRAPH_STORE/graphs when the env var is set, in the CWD-relative
    weights/graphs otherwise). Read at RunConfig instantiation, not import,
    so pod launchers that export the var after import still win. An explicit
    --graph-dir flag on the entry script overrides both."""
    root = os.environ.get("GRAPH_STORE")
    return os.path.join(root, "graphs") if root else "weights/graphs"


PreHypothesisMap = dict[tuple[int, int, int], str]
"""Per-feature prior-belief map keyed by ``(layer, feature_idx, pos)``.

Written by ``pin_features`` into ``ctx.pinned_features`` and read by
``batched_anchor_sweep`` (which fails loud if the map is missing) and by
the REASSESS subagent (which surfaces the agent's pre-intervention prior
in the triple-label record's ``pre_label`` field).
"""


@dataclass
class ToolContext:
    """Runtime context passed to tool functions (replaces globals)."""
    graph: Any
    tokenizer: Any
    neuronpedia_model_id: str = "qwen3-4b"
    neuronpedia_sae_id: str = "{layer}-transcoder-hp"
    # Optional sibling graphs used by cross-graph-diff tools (e.g. base vs
    # taboo, biased vs unbiased probe). Tools that need them assert non-empty.
    sibling_graphs: list[Any] = field(default_factory=list)
    # Closed candidate set for classification-style tools (e.g. Taboo's
    # 20-word menu). Set by the host script, not passed through LLM args,
    # to prevent the orchestrator from hallucinating its own list.
    candidate_words: list[str] = field(default_factory=list)
    # {(layer, feature_idx) -> density in (0,1]} calibrated on a broader
    # baseline pool (e.g. base model across multiple prompts). Used by
    # segment-aggregation tools as an extra IDF multiplier so cross-prompt
    # scaffold features are stripped on top of same-prompt diff subtraction.
    base_feature_density: dict = field(default_factory=dict)
    # Base URL for Neuronpedia-shaped feature lookups. Override to point at a
    # local FastAPI shim (see scripts/run_autointerp_server.py) when the upstream
    # transcoder set isn't on Neuronpedia.
    neuronpedia_base_url: str = "https://www.neuronpedia.org"

    # inspect_feature selection mode:
    #   "auto": try Neuronpedia first, fall back to local autointerp on failure/empty.
    #   "neuronpedia": Neuronpedia only.
    #   "local": local autointerp only.
    # Default is "neuronpedia" (not base's "auto") so a causal run cannot silently
    # take the local-autointerp branch. Both ELK entry scripts pass this explicitly.
    feature_source: Literal["auto", "neuronpedia", "local"] = "neuronpedia"

    # Local autointerp config, required when feature_source != "neuronpedia".
    autointerp_features_dir: str | None = None
    autointerp_cache_dir: str | None = None
    autointerp_model: str = "openai/gpt-oss-120b"
    autointerp_api_key: str | None = None  # falls back to OPENROUTER_API_KEY env var
    # How get_top_features and get_upstream_features order their top-k.
    #
    # False (default, every mode) ranks by |direct_effect|. Transcoder activations
    # are nonnegative, so an edge's sign comes entirely from decoder/encoder
    # direction alignment, which makes a negative edge a real inhibitory
    # connection rather than a sign artifact. The graph was itself pruned by
    # absolute influence (circuit_tracer.graph.normalize_matrix takes .abs()
    # before computing node and edge influence), so magnitude here matches the
    # criterion that decided which nodes exist in the .pt at all. The sign is
    # never hidden either way, since every returned row carries its signed
    # direct_effect.
    #
    # True ranks by signed direct_effect, surfacing positive drivers first and
    # burying inhibitory edges. Kept as an explicit ablation knob, and
    # deliberately not tied to run mode.
    rank_signed: bool = False
    replacement_model: Any = None  # ReplacementModel used during graph build, needed to run feature_intervention
    baseline_activations: Any = None  # per-layer transcoder activations for the prompt, shape [n_layers, seq_len, d_transcoder]
    baseline_answer: Optional[str] = None  # greedy decoded answer under no intervention; all interventions compare against this
    baseline_prompt: Optional[str] = None  # exact prompt string used at graph-build time, replayed by intervene_feature/intervene_supernode
    system_prompt: str = ""  # subject-model system prompt (RunConfig.system_prompt), stashed at ctx-build so the REASSESS prompt's (3)/(4) context block carries it in both the committed ANCHOR and discovery reassess paths (huge-refactor.md B5)
    baseline_top5: Optional[dict] = None  # cached top-5 next-token logits at last prompt position; None means uncached (raise loud in _measure_intervention; tolerant fallback in batched sweeps)
    # VERIFY-phase intervention bookkeeping. Populated by intervene_feature / intervene_supernode
    # for dedup and history. The legacy `anchor_passed` / `anchor_pass_called` fields and their
    # gates were removed once `batched_anchor_sweep` took over Phase 1 deterministically.
    single_factors: dict = field(default_factory=dict)  # {(layer, feat_idx): set[float]}, every factor applied to this single feature (any scale, used for replicate dedup)
    depth_factors: dict = field(default_factory=dict)  # {(layer, feat_idx): set[float]}, factors applied in depth phase only (-2/-3/-4)
    supernode_factors: dict = field(default_factory=dict)  # {frozenset((layer, feat_idx), ...): set[float]}, factors applied to each supernode
    intervention_history: list = field(default_factory=list)  # append-only ledger of every measurement (singles, supernodes)
    # Three-tool chain state (changes.md sec 2.2). Populated as side effects
    # of build_circuit -> pin_features -> batched_anchor_sweep.
    build_features: set = field(default_factory=set)  # canonical {(layer, feat_idx, pos)} set from build_circuit
    pinned_features: dict = field(default_factory=dict)  # {(layer, feat_idx, pos) -> pre_hypothesis: str} from pin_features
    inspect_cache: dict = field(default_factory=dict)  # {(layer, feat_idx, pos) -> inspect_feature blob}; reused across reinterpret_subagent calls
    # REASSESS triple-label records keyed by (layer, feature_idx, pos), written by the
    # auto-dispatched reinterpret_subagent inside batched_anchor_sweep; persisted into oracle_result.json.
    reassess_records: dict = field(default_factory=dict)
    # Reassess-subagent backend, stashed at run start by run_circuit_oracle so the
    # auto-dispatched reinterpret_subagent can reach the run's LLM client + configured
    # subagent model (gpt-oss-120b). None in the test path, where the mock fixture
    # installs subagent._SUBAGENT_CLIENT instead. (Part A of huge-refactor.md.)
    subagent_client: Any = None
    subagent_model: str = DEFAULT_SUBAGENT_MODEL
    # Causal-by-default discovery log (Part B of huge-refactor.md): one ungraded row per
    # discovery-time causal hit (a feature whose scale=-1 ablation shifted the output),
    # written by the causal pass on get_top_features / get_upstream_features. Each row is
    # {feature: [layer, feature_idx, pos], autointerp, post_label, divergence,
    # oracle_pinned: None, became_win: None}; the pinned/win fields are joined post-hoc by
    # the analysis script. Surfaced into oracle_result.json["discovery_reassess"].
    discovery_reassess: list = field(default_factory=list)
    # Set True at the end of batched_anchor_sweep. The escape hatches
    # (intervene_feature / intervene_supernode) refuse to run until this is
    # True, since per spec they're saturation tests AFTER the sweep, not
    # bypasses for the chain.
    anchor_sweep_done: bool = False
    # Discovery-annotation mode for _causal_discovery_annotate. "full" (default)
    # writes the shift bucket plus, for shifted rows, the label channels
    # (autointerp / post_label / divergence via the reassess fan-out).
    # "shift_only" (refusal arm 2, the no-inspect arm) keeps the shift
    # measurement and withholds every label-bearing channel, since the reassess
    # needs an autointerp label to diverge from. Unknown values raise inside
    # the annotate pass.
    discovery_annotation: str = "full"


@dataclass
class RunConfig:
    """Configuration for a single circuit oracle run."""
    prompt_name: str
    system_prompt: str
    user_message: str
    assistant_prefix: str = ""
    question: str | None = None  # if set, appended to oracle query to direct analysis
    # Run identity for the ablation grid, persisted into
    # oracle_result.json. task is the prompt-registry key
    # (refusal | elk | probes | hallucination), arm is the arms.py registry key.
    # Both stay None on ad-hoc runs.
    task: str | None = None
    arm: str | None = None
    # 1-based repeat-pass index for the arm-1 5x repeat, persisted into
    # oracle_result.json and stamped into the run directory name. None on a
    # single-pass run, which keeps the legacy directory layout byte-identical.
    pass_index: int | None = None
    experiment_prefix: str = "circuit"
    orchestrator_model: str = "claude-opus-4-6"
    subagent_model: str = DEFAULT_SUBAGENT_MODEL
    provider: str = "openrouter"
    max_subagent_hops: int = 12  # generous ceiling; subagents stop early when they reach early layers or direct_effect decays
    model_name: str = "Qwen/Qwen3-4B"
    transcoder_name: str = "mwhanna/qwen3-4b-transcoders"
    graph_cache_dir: str = field(default_factory=_default_graph_cache_dir)
    verbose: bool = True
    # Neuronpedia identifiers, used to build per-feature dashboard URLs in reports.
    # Must match ToolContext.neuronpedia_model_id / neuronpedia_sae_id for the model + transcoder pair.
    neuronpedia_model_id: str = "qwen3-4b"
    neuronpedia_sae_id: str = "{layer}-transcoder-hp"
