#!/usr/bin/env python3
"""Run circuit_oracle on pre-computed probe attribution graphs.

Each graph in probe_circuits/*.pt was built using google/gemma-2-2b with
gemma-scope transcoders, attributing toward a linear probe direction (not a
next-token logit).  The oracle analyses which transcoder features causally
drive the probe score.

The default selection is the full reported set of 80 graphs (the 40 prompts in
prompts.json, times biased and unbiased, method "correct"). Every flag below
narrows that set, and --all-in-store widens it to whatever the graph store holds.

Usage (from anywhere):
    python spurious-correlation/scripts/run_oracle_on_probes.py
    python spurious-correlation/scripts/run_oracle_on_probes.py --arm probes-arm2
    python spurious-correlation/scripts/run_oracle_on_probes.py --slugs bib_journalist_dietitian-pos_pos_1-biased-probe-correct
    python spurious-correlation/scripts/run_oracle_on_probes.py --concern "What features encode gender bias?"
    python spurious-correlation/scripts/run_oracle_on_probes.py --dataset bib_journalist_dietitian
    python spurious-correlation/scripts/run_oracle_on_probes.py --probe-type unbiased --method correct

Graphs are read from $GRAPH_STORE/probe_circuits (default: spurious-correlation/).
Results are written to spurious-correlation/runs/ by default (or runs/<arm>
under --arm). The committed spurious-correlation/results/ and
spurious-correlation/results-workshop/ directories are read-only archives and
no command writes into them.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# This file lives in spurious-correlation/scripts/, so the task root (which holds
# prompts.json and the results directories) is one level up and the repo root is two.
_HERE = Path(__file__).resolve().parent
_TASK_ROOT = _HERE.parent
_REPO_ROOT = _TASK_ROOT.parent

from circuit_oracle import (  # noqa: E402
    ToolContext,
    LLMClient,
    RunConfig,
    run_circuit_oracle,
    save_run_results,
)
from circuit_oracle.arms import NO_SUBAGENT, arm_names, resolve_arm  # noqa: E402
from circuit_oracle.oneshot import run_oneshot_oracle  # noqa: E402
from circuit_oracle.llm_client import (  # noqa: E402
    PROVIDER_CHOICES,
    preflight_providers,
)


from transformers import AutoTokenizer  # noqa: E402
from circuit_tracer.graph import Graph  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

def load_repo_env() -> None:
    """Fold the repo-root .env into os.environ, without overriding the shell.

    main() calls this before build_parser(), because several argparse defaults
    read os.environ (--provider takes LLM_PROVIDER). Loading it later meant a
    value set only in .env was documented but ignored. Absent .env is fine when
    the keys are already exported.
    """
    env_path = _REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


# Attribution graphs live in the graph store (a network-volume mount in
# production, the task root by default). Resolved per call, not cached in a
# module constant: main() reads the repo-root .env, so a GRAPH_STORE set there
# is not in os.environ yet at import time.
def probe_circuits_dir() -> Path:
    return Path(os.environ.get("GRAPH_STORE", str(_TASK_ROOT))) / "probe_circuits"


MODEL_NAME = "google/gemma-2-2b"

# Models behind the reported task-1 numbers. Named constants rather than
# argparse defaults so --arm can tell "the user asked for this model" from
# "nobody said anything" and reject only the former.
# minimax-m3 is what probes-arm1 uses, so a bare invocation with no --arm now
# reproduces arm 1 instead of a model that sits outside the grid entirely.
DEFAULT_ORCHESTRATOR = "minimax/minimax-m3"
# gpt-oss-120b, not deepseek-v3.2: it is the standard "everything else" model
# across the three tasks, and every probes ArmSpec already carries
# subagent_model=GPT_OSS, so this only matters on a bare no --arm run.
DEFAULT_SUBAGENT = "openai/gpt-oss-120b"

# The prompt manifest that defines the reported slug set (dataset -> subgroup -> prompts).
PROMPTS_JSON = _TASK_ROOT / "prompts.json"

# The reported runs all use the mean-pooled probe-layer injection ("correct").
REPORTED_METHOD = "correct"

# These .pt files are raw nn.Module probe checkpoints, not Graph objects.
EXCLUDE_PREFIXES = ("probe_layer",)

# DATASET_DESCRIPTIONS = {
#     "bib_journalist_dietitian": "BiasInBios: dietitian (positive class) vs journalist (negative class)",
#     "bib_nurse_professor": "BiasInBios: nurse (positive class) vs professor (negative class)",
#     "bib_surgeon_teacher": "BiasInBios: teacher (positive class) vs surgeon (negative class)",
#     "civil_comments": "CivilComments: toxicity classification",
#     "multinli": "MultiNLI: natural language inference (contradiction vs entailment)",
# }

# PROBE_DESCRIPTIONS = {
#     "biased": (
#         "biased probe (trained on ambiguous data where the true label is perfectly "
#         "correlated with a spurious feature, so the probe can exploit both)"
#     ),
#     "unbiased": (
#         "unbiased probe (trained on balanced data where the true label is decorrelated "
#         "from any spurious feature, forcing the probe to rely on causal features only)"
#     ),
# }

# METHOD_DESCRIPTIONS = {
#     "simple": (
#         "CustomTarget approximation. The probe direction is injected at the final "
#         "layer as if it were a logit target, so attribution flows through all layers"
#     ),
#     "correct": (
#         "mean-pooled injection at the probe layer (layer 22). Attribution is injected "
#         "at the residual stream of the layer where the probe actually reads, so only "
#         "features in layers 0-22 are attributed"
#     ),
# }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_slug(slug: str) -> dict:
    """Decompose a graph slug into dataset / probe_type / method.

    Examples:
        bib_journalist_dietitian-biased-probe-correct  →  biased / correct
        civil_comments-unbiased-probe-simple           →  unbiased / simple
    """
    for probe_type in ("biased", "unbiased"):
        marker = f"-{probe_type}-probe-"
        if marker in slug:
            dataset, method = slug.split(marker, 1)
            return {"dataset": dataset, "probe_type": probe_type, "method": method}
    return {"dataset": slug, "probe_type": "unknown", "method": "unknown"}


def build_oracle_query(slug: str, graph: Graph, tokenizer, concern: str | None = None) -> str:
    """Construct the natural-language query sent to the oracle orchestrator."""
    # meta = parse_slug(slug)

    # Reconstruct input text
    try:
        input_text = graph.input_string or tokenizer.decode(
            graph.input_tokens.tolist(), skip_special_tokens=True
        )
    except Exception:
        input_text = "(could not decode input tokens)"
    short_input = input_text[:400] + ("..." if len(input_text) > 400 else "")

    # dataset_desc = DATASET_DESCRIPTIONS.get(meta["dataset"], meta["dataset"])
    # probe_desc = PROBE_DESCRIPTIONS.get(meta["probe_type"], meta["probe_type"])
    # method_desc = METHOD_DESCRIPTIONS.get(meta["method"], meta["method"])

    query = (
        "This is a Gemma-2-2B probe attribution graph. The attribution target is the "
        "score of a linear classification probe trained on a layer's residual stream "
        "activations. The probe's weight vector is injected as the output direction, "
        "so the circuit traces which transcoder features causally drive the probe's "
        "classification score, not a next-token prediction.\n\n"
        # f"Probe: {probe_desc}\n"
        # f"Attribution method: {method_desc}\n\n"
        f"Input text:\n{short_input}\n\n"
        "The attribution graph shows which transcoder features causally drive this "
        "probe's classification score.  The output node represents the probe direction "
        "rather than a vocabulary token, so get_top_logits will return a synthetic "
        "probe label. Use it as the starting point and call get_top_features on "
        "whatever target it returns.\n\n"
        "Analyze the attribution circuit to determine what mechanism drives this "
        "probe's classification."
    )

    if concern:
        query += f"\n\nUser concern: {concern}"

    return query


def reported_slugs() -> list[str]:
    """The 80 graph slugs behind the reported task-1 numbers, derived from prompts.json.

    One slug per (dataset, subgroup, prompt index, probe type), method fixed to
    REPORTED_METHOD. Datasets with no prompts (bib_surgeon_teacher, dropped after
    probe-quality screening) contribute nothing.
    """
    manifest = json.loads(PROMPTS_JSON.read_text())
    slugs: list[str] = []
    for dataset, subgroups in manifest.items():
        for subgroup, prompts in subgroups.items():
            for idx in range(1, len(prompts) + 1):
                for probe_type in ("biased", "unbiased"):
                    slugs.append(
                        f"{dataset}-{subgroup}_{idx}-{probe_type}-probe-{REPORTED_METHOD}"
                    )
    return sorted(slugs)


def discover_graphs(
    probe_type: str | None = None,
    dataset: str | None = None,
    method: str | None = None,
    slugs: list[str] | None = None,
    all_in_store: bool = False,
) -> list[Path]:
    """Return sorted list of graph .pt paths matching the given filters.

    Selection source, in order of precedence. Explicit --slugs wins, then
    --all-in-store globs whatever the graph store holds, otherwise the default
    is the reported 80-slug set from prompts.json. The filters narrow whichever
    source was chosen.
    """
    if slugs:
        paths = [probe_circuits_dir() / f"{s}.pt" for s in slugs]
        missing = [p for p in paths if not p.exists()]
        if missing:
            for p in missing:
                print(f"ERROR: graph file not found: {p}")
            sys.exit(1)
        return paths

    if all_in_store:
        candidates = sorted(
            p for p in probe_circuits_dir().glob("*.pt")
            if not any(p.name.startswith(prefix) for prefix in EXCLUDE_PREFIXES)
        )
    else:
        candidates = [probe_circuits_dir() / f"{s}.pt" for s in reported_slugs()]

    if probe_type:
        candidates = [p for p in candidates if f"-{probe_type}-probe-" in p.stem]
    if dataset:
        candidates = [p for p in candidates if p.stem.startswith(dataset)]
    if method:
        candidates = [p for p in candidates if p.stem.endswith(f"-{method}")]

    # Fail loud on a graph store that does not hold the requested reported set,
    # rather than silently running a subset.
    if not all_in_store:
        missing = [p for p in candidates if not p.exists()]
        if missing:
            print(
                f"ERROR: {len(missing)} of {len(candidates)} reported graphs are missing "
                f"from {probe_circuits_dir()} (build them first, or set GRAPH_STORE)."
            )
            for p in missing[:10]:
                print(f"  missing: {p.name}")
            if len(missing) > 10:
                print(f"  ... and {len(missing) - 10} more")
            sys.exit(1)

    return candidates


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def positive_int(value: str) -> int:
    """argparse type for a 1-based index. Rejects 0 and negatives, so a
    `_pass0` directory cannot make a 5-pass repeat look like 6."""
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError(f"must be 1 or greater, got {n}")
    return n


def build_parser() -> argparse.ArgumentParser:
    """The CLI surface, split out of main() so tests can exercise the real
    parser rather than a re-declaration of it."""
    parser = argparse.ArgumentParser(
        description="Run circuit_oracle on pre-computed probe attribution graphs"
    )
    # ── Graph selection ──────────────────────────────────────────────────────
    # Default (no flags) = the reported 80 slugs derived from prompts.json.
    parser.add_argument(
        "--slugs", nargs="*", default=None,
        help="Specific graph slugs to run (without .pt extension). "
             "Overrides the reported default set.",
    )
    parser.add_argument(
        "--all-in-store", action="store_true",
        help="Select every graph in the store instead of the reported 80. "
             "Superset mode, not the reported configuration.",
    )
    parser.add_argument(
        "--dataset", default=None,
        help="Filter by dataset prefix (e.g. bib_journalist_dietitian, civil_comments)",
    )
    parser.add_argument(
        "--probe-type", default=None, choices=["biased", "unbiased"],
        help="Filter by probe type",
    )
    parser.add_argument(
        "--method", default=None, choices=["simple", "correct"],
        help="Filter by attribution method",
    )
    # ── Analysis ─────────────────────────────────────────────────────────────
    parser.add_argument(
        "--concern", type=str, default=None,
        help="Override the per-dataset analysis concern "
             "(e.g. 'What features encode gender bias?')",
    )
    # ── Models (defaults reproduce the reported task-1 configuration) ────────
    parser.add_argument(
        "--arm", default=None,
        help="Arm registry key (circuit_oracle.arms), e.g. probes-arm2. Owns the "
             "orchestrator, subagent, and tool surface, so it conflicts with "
             "--orchestrator-model / --subagent-model, and it sends output to "
             "runs/<arm>/ unless --output-dir says otherwise. Probes arms "
             f"only: {', '.join(arm_names(task='probes'))}.",
    )
    parser.add_argument("--orchestrator-model", default=None,
                        help=f"Orchestrator model ID (default: {DEFAULT_ORCHESTRATOR}; "
                             f"conflicts with --arm)")
    parser.add_argument("--subagent-model", default=None,
                        help=f"Subagent model ID (default: {DEFAULT_SUBAGENT}; "
                             f"conflicts with --arm)")
    parser.add_argument(
        "--provider",
        default=os.environ.get("LLM_PROVIDER", "openrouter"),
        choices=PROVIDER_CHOICES,
    )
    parser.add_argument("--max-hops", type=int, default=12)
    # ── Output ───────────────────────────────────────────────────────────────
    parser.add_argument(
        "--output-dir", default=None,
        help="Output directory name (relative to spurious-correlation/). Defaults to "
             "runs/ (runs/<arm> under --arm), which is gitignored, so a replication "
             "can never overwrite the committed results/ or results-workshop/ "
             "archives behind the published numbers.",
    )
    parser.add_argument("--pass-index", type=positive_int, default=None,
                        help="1-based index of this repeat pass, recorded in oracle_result.json "
                             "and in the run directory name. Task 1's 5x repeat has the identical "
                             "layout to task 3's, where a second-resolution timestamp is otherwise "
                             "the only thing separating passes.")
    parser.add_argument("--quiet", action="store_true")
    return parser


def main():
    # BEFORE build_parser(), so LLM_PROVIDER and friends set in .env reach the
    # argparse defaults that read them.
    load_repo_env()
    parser = build_parser()
    args = parser.parse_args()

    # Resolve the arm. --arm owns the model and tool knobs, so combining it with
    # the ad-hoc flags is a contradiction and dies here rather than letting one
    # side silently win (a mislabeled run poisons a whole 80-graph batch).
    arm = None
    if args.arm is not None:
        try:
            # This runner serves both pipelines: the agentic loop and the
            # arm-3 one-shot (run_oneshot_oracle), dispatched at the oracle
            # call site on arm.pipeline. Foreign tasks still die here.
            arm = resolve_arm(args.arm, task="probes",
                              pipeline=("agentic", "oneshot"))
        except ValueError as e:
            parser.error(str(e))
        for flag, val in (
            ("--orchestrator-model", args.orchestrator_model),
            ("--subagent-model", args.subagent_model),
        ):
            if val is not None:
                parser.error(f"{flag} conflicts with --arm (the arm owns it)")
        orchestrator = arm.orchestrator_model
        subagent = arm.subagent_model or DEFAULT_SUBAGENT
        excluded_tools = list(arm.excluded_tools)
    else:
        orchestrator = args.orchestrator_model or DEFAULT_ORCHESTRATOR
        subagent = args.subagent_model or DEFAULT_SUBAGENT
        excluded_tools = []

    # One directory per arm. The saved leaf is {orchestrator}_{subagent}_{ts},
    # so arms 1, 2 and 3 (same models, different tool surface) would otherwise
    # be distinguishable only by reading oracle_result.json.
    if args.output_dir is not None:
        output_rel = args.output_dir
    elif arm is not None:
        output_rel = f"runs/{arm.name}"
    else:
        output_rel = "runs"

    # Discover graphs
    graph_paths = discover_graphs(
        probe_type=args.probe_type,
        dataset=args.dataset,
        method=args.method,
        slugs=args.slugs,
        all_in_store=args.all_in_store,
    )
    if not graph_paths:
        print("No graph files matched the given filters.")
        available = sorted(p.stem for p in probe_circuits_dir().glob("*.pt")
                           if not any(p.name.startswith(x) for x in EXCLUDE_PREFIXES))
        print(f"Available slugs ({len(available)}):")
        for s in available:
            print(f"  {s}")
        sys.exit(1)

    print(f"Found {len(graph_paths)} graph(s) to process.")
    if arm is not None:
        print(f"Arm: {arm.name} ({arm.description})")
    print(f"Orchestrator: {orchestrator}")
    print(f"Subagent: {subagent}")
    if excluded_tools:
        print(f"Excluded tools: {excluded_tools}")

    # Every gateway this run will actually call must be credentialed BEFORE the
    # circuit work. Routing is per model, so a --provider kilo run still needs
    # OPENROUTER_API_KEY for the pinned openai/gpt-oss-120b subagent, and saying
    # so here beats a 401 partway through the probe list. NO_SUBAGENT is a
    # provenance placeholder, not a model, so it is dropped. This MUST stay
    # after load_repo_env() at the top of main(): the keys it checks for are the
    # ones .env just supplied.
    preflight_providers(
        [m for m in (orchestrator, subagent) if m != NO_SUBAGENT], args.provider
    )

    # Load Gemma tokenizer (no need for the full model, only token decoding is needed).
    print(f"\nLoading tokenizer ({MODEL_NAME})...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    print("Tokenizer ready.")

    # Create LLM client and output directory.
    client = LLMClient(provider=args.provider)
    output_dir = _TASK_ROOT / output_rel
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output: {output_dir}")

    verbose = not args.quiet

    # ── Process each graph ─────────────────────────────────────────────────────
    for graph_path in graph_paths:
        _lines = []

        def emit(line=""):
            # print(line, flush=True)
            _lines.append(str(line))

        slug = graph_path.stem
        emit(f"\n{'='*60}")
        emit(f"Graph: {slug}")
        emit(f"{'='*60}")

        emit(f"Loading {graph_path.name}...")
        graph = Graph.from_pt(str(graph_path))
        n_nodes = graph.adjacency_matrix.shape[0]
        n_sel = len(graph.selected_features)
        n_logits = len(graph.logit_tokens)
        emit(f"  {n_nodes} nodes | {n_sel} selected features | {n_logits} logit target(s)")

        print("SLUG:", slug)
        # NOTE (deviation from the workshop-paper run): each branch below used to end in a
        # trailing comma, which made `concern` a 1-tuple, so the query and
        # RunConfig.question carried the Python repr "('...',)" instead of the string.
        # The commas are removed here. The wording is otherwise verbatim.
        if args.concern:
            concern = args.concern
        elif 'bib' in slug:
            concern = "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."
        elif 'civil' in slug:
            concern = "The circuit use spurious features (e.g.,\"an identity group\" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."
        else:
            concern = "The circuit use spurious features (e.g.,\"negation words\" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."
        print("Concern:", concern)
        ctx = ToolContext(
            graph=graph,
            tokenizer=tokenizer,
            neuronpedia_model_id="gemma-2-2b",
            neuronpedia_sae_id="{layer}-gemmascope-transcoder-16k",
        )

        query = build_oracle_query(slug, graph, tokenizer, concern=concern)
        if verbose:
            emit(f"\nQuery preview (first 300 chars):\n{query[:300]}...\n")

        # mode="observational" turns off the three causal phases (intervention
        # tools, end-of-turn PIN / ANCHOR / SUPERNODE guards, causal-by-default
        # discovery ablation), which need a ReplacementModel this run does not have.
        # task="probes" resolves the RESTORED generic mech-interp prompt (the one
        # the published 2026-04-06 runs actually used, recovered blob-level from
        # git history on 2026-07-26) with its Qwen3-4B / layer-36 structure block
        # parameterized to this graph's layer count. The previous behavior here
        # (passing no system_prompt and inheriting OBSERVATIONAL_SYSTEM_PROMPT)
        # asked a Gemma-2-2B probe oracle for a hallucination score, and the old
        # comment claiming that prompt produced the published task-1 number was
        # wrong. Without --arm no excluded_tools is passed, because the base
        # package exposed its full tool list to probe runs and the mode gate
        # already strips the five causal tools; the ablation arms narrow it.
        if arm is not None and arm.pipeline == "oneshot":
            # Arm 3: the same first page of evidence (top logits, top-k
            # features by |direct_effect|, one round of labels), one
            # completion, no traversal. Result shape matches
            # run_circuit_oracle so everything downstream is unchanged.
            result = run_oneshot_oracle(
                ctx,
                client,
                query,
                orchestrator_model=orchestrator,
                task="probes",
                mode="observational",
                verbose=verbose,
            )
        else:
            result = run_circuit_oracle(
                ctx,
                client,
                query,
                orchestrator_model=orchestrator,
                subagent_model=subagent,
                max_subagent_hops=args.max_hops,
                verbose=verbose,
                mode="observational",
                task="probes",
                excluded_tools=excluded_tools or None,
            )

        emit(f"\n{'='*60}")
        emit(f"ORACLE ANALYSIS ({slug})")
        emit(f"{'='*60}")
        emit(result["response"])

        # Build a RunConfig so save_run_results can create the standard report.
        meta = parse_slug(slug)
        cfg = RunConfig(
            prompt_name=slug,
            system_prompt="",
            user_message=(
                f"Dataset: {meta['dataset']} | "
                f"Probe: {meta['probe_type']} | "
                f"Method: {meta['method']}"
            ),
            question=concern,
            experiment_prefix="probe",
            orchestrator_model=orchestrator,
            subagent_model=subagent,
            provider=args.provider,
            # Provenance into oracle_result.json, so a results directory can be
            # attributed to an arm without re-deriving it from the models.
            task="probes",
            arm=arm.name if arm is not None else None,
            pass_index=args.pass_index,
            # Must mirror the ToolContext ids above, otherwise every Neuronpedia
            # link in report.md would point at the refusal-track qwen3-4b default.
            neuronpedia_model_id="gemma-2-2b",
            neuronpedia_sae_id="{layer}-gemmascope-transcoder-16k",
        )

        exp_dir = save_run_results(
            result,
            cfg,
            prompt=graph.input_string or "",
            base_dir=str(output_dir),
        )
        emit(f"Results saved to: {exp_dir}")

        log_path = Path(exp_dir) / "run.log"
        log_path.write_text("\n".join(_lines) + "\n")
        print(f"Log written to: {log_path}", flush=True)


if __name__ == "__main__":
    main()
