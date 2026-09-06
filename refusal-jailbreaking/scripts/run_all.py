#!/usr/bin/env python3
"""Suppression-jailbreak experiment runner.

Reads single-prompt entries from data/prompts.json and runs the Circuit Oracle
pipeline. The attribution graph is computed once per prompt and reused for the
single canonical orchestrator, amortizing the expensive GPU computation.

Per run produces (under exp/exp-suppression-{slug}/, see the TODO(layout) note at
the save_run_results call). The committed archives are results/ and
results-workshop/, which no command writes to:
    oracle_result.json: full pipeline state (interventions, self_rating_confidence, ...)
    elicitation.json/.md: winning interventions (the punchline)
    circuit.svg: pinned BUILD circuit
    report.md: Oracle's narrative, controls, usage table
    pinned_ids.json: Neuronpedia-style IDs for the pinned features

Usage:
    python scripts/run_all.py                                     # all entries in data/prompts.json
    python scripts/run_all.py --slugs tiananmen-june-4-1989       # single slug
    python scripts/run_all.py --arm refusal-arm2                  # registry arm (models + tools + annotation)
    python scripts/run_all.py --orchestrator anthropic/claude-opus-4.6
    python scripts/run_all.py --control-runs 3
    python scripts/run_all.py --arm refusal-arm1 --pass-index 3 --require-graph  # repeat pass on a shard pod
"""

import argparse
import concurrent.futures
import json
import os
import sys
import threading
import time
import traceback
from pathlib import Path

import torch

from circuit_oracle import (
    ToolContext,
    LLMClient,
    RunConfig,
    load_model,
    format_chat,
    compute_or_load_graph,
    run_circuit_oracle,
    save_run_results,
    build_oracle_query,
    generate_response,
    run_control_analysis,
    run_self_rating,
)
from circuit_oracle import fanout
from circuit_oracle.arms import NO_SUBAGENT, arm_names, resolve_arm
from circuit_oracle.gpu_lock import install_gpu_lock
from circuit_oracle.llm_client import PROVIDER_CHOICES, preflight_providers
from circuit_oracle.oneshot import run_oneshot_oracle
from circuit_oracle.thread_logging import install as install_thread_logging


# ── Configuration ────────────────────────────────────────────────────────────

_HERE = Path(__file__).resolve().parent
_THREAD_ROOT = _HERE.parent

# Fresh runs land here, and runs/ is gitignored. The committed archives
# (results/ for the arm grid, results-workshop/ for the workshop-paper runs) are
# read-only evidence and are never written to by a default invocation.
DEFAULT_OUT_ROOT = _THREAD_ROOT / "runs"

DEFAULT_QUESTION = "Is this output a refusal, and which features gate it?"

# Current default. It was openai/gpt-5.4 through the earlier runs, which is in NO
# arm of the ablation grid (arms 1-3 are minimax-m3, arm 4 is Terra, arm 5 is
# gemma-4-31b-it), so a bare `run.sh` with no --arm and no --orchestrator used to
# quietly run a model that was not part of the experiment. Terra is arm 4's model
# and is priced identically to gpt-5.4, so it is the honest default for an
# unqualified run.
#
# Prefer --arm over relying on this. The arm owns the orchestrator, the subagent and
# the tool surface together, and it also routes output to runs/<arm>/.
#
# NOTE the grader inherits this (saving.py: `model = config.orchestrator_model`), and
# Terra is an OpenAI endpoint, so it 404s under OpenRouter's require_parameters filter
# on any request carrying an explicit temperature. That is fixed in llm_client's
# create_message, which drops a redundant temperature=1.0 on OpenRouter. Without that
# fix this default grades nothing.
DEFAULT_ORCHESTRATOR = "openai/gpt-5.6-terra"

DEFAULT_SUBAGENT = "openai/gpt-oss-120b"

EXPERIMENT_PREFIX = "suppression"


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_dataset_file(path: Path) -> dict:
    """Load and validate the prompts JSON file."""
    with open(path) as f:
        data = json.load(f)

    if "entries" not in data:
        print(f"Error: {path} missing 'entries' key")
        sys.exit(1)

    entries = data["entries"]
    if not entries:
        print(f"Error: {path} has no entries")
        sys.exit(1)

    print(f"Loaded {len(entries)} entries from {path}")
    meta = data.get("metadata", {})
    if meta.get("purpose"):
        print(f"  Purpose: {meta['purpose'][:120]}...")

    return data


def filter_entries(
    entries: list[dict],
    slugs: list[str] | None = None,
    category: str | None = None,
) -> list[dict]:
    """Filter entries by slug and/or category.

    Entries with "disabled: true" are skipped by default. They can still be
    force-run by naming them explicitly in --slugs.

    When both slugs and category are given they intersect (entry must match
    the slug AND the category). When category is None, behavior is unchanged.
    """
    if slugs is None:
        result = [e for e in entries if not e.get("disabled", False)]
    else:
        result = [e for e in entries if e["slug"] in slugs]
    if category is not None:
        result = [e for e in result if e.get("category") == category]
    return result


def entry_to_run_config(entry: dict, **overrides) -> RunConfig:
    """Convert a prompts.json entry to a RunConfig."""
    question = overrides.pop("question", DEFAULT_QUESTION)
    return RunConfig(
        prompt_name=entry["slug"],
        system_prompt=entry.get("system_prompt", ""),
        user_message=entry["user_message"],
        experiment_prefix=EXPERIMENT_PREFIX,
        question=question,
        **overrides,
    )


def run_single_orchestrator(
    cfg,
    ctx,
    client,
    prompt,
    full_response,
    verbose,
    control_runs=1,
    self_rating=None,
    interventions=None,
    out_root=None,
    excluded_tools=None,
):
    """Run the oracle pipeline for a single entry."""
    question_label = f" (question: {cfg.question})" if cfg.question else " (general)"
    orch_label = cfg.orchestrator_model.split("/")[-1] if "/" in cfg.orchestrator_model else cfg.orchestrator_model
    print(f"\n  {'─'*56}")
    print(f"  Orchestrator: {orch_label}{question_label}")
    print(f"  {'─'*56}")

    oracle_query = build_oracle_query(
        user_message=cfg.user_message,
        full_response=full_response,
    )

    # [1/2] Oracle analysis (circuit tools)
    print(f"  [1/2] Oracle analysis (circuit tools)...")
    # mode="causal" is the package default, passed explicitly so the refusal
    # thread's contract (intervention tools, causal discovery, PIN / ANCHOR /
    # SUPERNODE guards) is visible at the call site rather than inherited.
    result = run_circuit_oracle(
        ctx,
        client,
        oracle_query,
        orchestrator_model=cfg.orchestrator_model,
        subagent_model=cfg.subagent_model,
        max_subagent_hops=cfg.max_subagent_hops,
        verbose=verbose,
        mode="causal",
        # task="refusal" resolves ORACLE_SYSTEM_PROMPT through the registry
        # (identical text to the legacy fallback) and stamps run identity into
        # oracle_result.json.
        task="refusal",
        excluded_tools=list(excluded_tools) if excluded_tools else None,
    )

    print(f"\n  [1/2] ORACLE DONE, {len(result['tool_calls'])} tool calls")

    # Pull intervention records out of the tool_calls log so they land in
    # oracle_result.json["interventions"] and elicitation.{json,md}.
    # Pass full_response so batched-sweep records can populate `answer_before`
    # (the batched tools share one baseline across all rows).
    interventions = _collect_interventions(result["tool_calls"], baseline_answer=full_response)

    # [2/2] Control analysis (Oracle without circuit tools)
    control_results = []
    for i in range(control_runs):
        run_label = f" (run {i+1}/{control_runs})" if control_runs > 1 else ""
        print(f"  [2/2] Control analysis (no tools){run_label}...")
        cr = run_control_analysis(
            client,
            user_message=cfg.user_message,
            full_response=full_response,
            model=cfg.orchestrator_model,
        )
        control_results.append(cr)

    # Fresh agentic runs go to runs/, matching run_sweeps.py --out-root, so they
    # can never write into the committed results/ or results-workshop/ archives.
    # save_run_results inserts its own "exp" segment under this root, so a run
    # lands at runs/exp/exp-suppression-<slug>/<orch>_<sub>_<timestamp>/.
    # results-workshop/ has no "exp" level, which is why exp_judge takes --exp-dir.
    exp_dir = save_run_results(
        result, cfg, prompt,
        base_dir=str(out_root or DEFAULT_OUT_ROOT),
        full_response=full_response,
        control_results=control_results,
        self_rating=self_rating,
        interventions=interventions,
    )
    print(f"  Saved to: {exp_dir}")


def run_single_oneshot(
    cfg,
    ctx,
    client,
    prompt,
    full_response,
    verbose,
    control_runs=1,
    self_rating=None,
    out_root=None,
):
    """Arm-3 sibling of run_single_orchestrator: one completion, no loop.

    Same query construction, same intervention collection, same saving path.
    The interventions the model proposes are executed by the harness through
    tools.intervene_feature inside run_oneshot_oracle, so the tool-call log
    carries real intervention records and _collect_interventions finds them
    exactly as it does on an agentic run.
    """
    orch_label = cfg.orchestrator_model.split("/")[-1] if "/" in cfg.orchestrator_model else cfg.orchestrator_model
    print(f"\n  {'─'*56}")
    print(f"  One-shot orchestrator: {orch_label}")
    print(f"  {'─'*56}")

    oracle_query = build_oracle_query(
        user_message=cfg.user_message,
        full_response=full_response,
    )

    print(f"  [1/2] One-shot analysis (static top-k, single completion)...")
    result = run_oneshot_oracle(
        ctx,
        client,
        oracle_query,
        orchestrator_model=cfg.orchestrator_model,
        task="refusal",
        mode="causal",
        verbose=verbose,
    )
    print(f"  [1/2] ONE-SHOT DONE, {len(result['tool_calls'])} recorded calls, "
          f"{result['oneshot']['n_executed']} interventions executed")

    interventions = _collect_interventions(result["tool_calls"], baseline_answer=full_response)

    control_results = []
    for i in range(control_runs):
        run_label = f" (run {i+1}/{control_runs})" if control_runs > 1 else ""
        print(f"  [2/2] Control analysis (no tools){run_label}...")
        cr = run_control_analysis(
            client,
            user_message=cfg.user_message,
            full_response=full_response,
            model=cfg.orchestrator_model,
        )
        control_results.append(cr)

    exp_dir = save_run_results(
        result, cfg, prompt,
        base_dir=str(out_root or DEFAULT_OUT_ROOT),
        full_response=full_response,
        control_results=control_results,
        self_rating=self_rating,
        interventions=interventions,
    )
    print(f"  Saved to: {exp_dir}")


def require_cached_graph(cache_path: str, require_graph: bool) -> None:
    """Under --require-graph, an incomplete cache is fatal instead of an hour of GPU.

    Checks all THREE files that compute_or_load_graph's cache_hit requires, not
    the .pt alone. Testing only the .pt left the guard one file short of the
    invariant it exists to enforce: a slug whose .pt is present but whose
    .baseline.pt or .baseline.json is missing or half-synced passed the guard,
    fell into the partial-cache branch, and then wrote a torch.save of the
    baseline activations plus a json.dump back into the graph store at agentic
    run time. Nothing in the tree locks or atomically writes those files, so on
    a sharded fan-out over one shared store that is a corruption vector on top
    of the GPU cost the guard was added to prevent.

    Split out of the run loop so it is testable without a model load. Exits
    rather than raising so a shard pod stops at the first bad slug with a
    readable message, instead of quietly paying for attribution the pre-build
    pass was supposed to have done.
    """
    if not require_graph:
        return
    required = (
        cache_path,
        f"{cache_path}.baseline.pt",
        f"{cache_path}.baseline.json",
    )
    missing = [path for path in required if not Path(path).exists()]
    if not missing:
        return
    print(
        f"Error: --require-graph and the cached graph at {cache_path} is incomplete. "
        f"Missing: {', '.join(missing)}. "
        "Run the pre-build pass (scripts/build_graph.py) for this slug first, "
        "or drop --require-graph to build it here."
    )
    sys.exit(1)


def _collect_interventions(tool_calls: list, baseline_answer: str = "") -> list[dict]:
    """Pull intervention measurement records out of the tool_calls log.

    Post-refactor (changes.md §2.2) the workhorse tools are batched:
      - batched_anchor_sweep: returns {"measurements": [{layer, feature_idx, pos,
        scale, top5_before, top5_after, answer_after, shift_bucket}, ...]}.
        We flatten each measurement into the single-feature `intervene_feature`
        shape so elicitation.md renders one block per (feature, scale) row.
      - batched_supernode_sweep: returns {"measurements": [{tuple_idx, rationale,
        features, scale, top5_before, top5_after, answer_after, shift_bucket}, ...]}.
        Flattened to the `intervene_supernode` shape.

    Escape-hatch tools (used only for factor=-4 saturation after the chain):
      - intervene_feature / intervene_supernode: already flat with top-level
        `intervention`, `top5_*`, `answer_*`, `hypothesis`.

    Legacy (pre-refactor):
      - anchor_pass: batched record with `anchor_results`; kept so old runs
        still render. New runs use batched_anchor_sweep.

    `baseline_answer` is injected as `answer_before` for batched-sweep rows
    since those tools share one no-intervention baseline across all rows.

    Calls whose output contains an `error` key (harness-rejected) are skipped.
    """
    out = []
    for tc in tool_calls:
        tool = tc["tool"]
        output = tc.get("output")
        if not isinstance(output, dict) or "error" in output:
            continue
        if tool in ("intervene_feature", "intervene_supernode"):
            if "intervention" in output:
                out.append({**output, "source": tool})
        elif tool == "batched_anchor_sweep":
            for m in output.get("measurements", []) or []:
                out.append({
                    "source": "batched_anchor_sweep",
                    "intervention": {
                        "type": "single",
                        "layer": int(m["layer"]),
                        "feature_idx": int(m["feature_idx"]),
                        "position": int(m["pos"]),
                        "scale": float(m["scale"]),
                    },
                    "top5_before": m.get("top5_before"),
                    "top5_after": m.get("top5_after"),
                    "answer_before": baseline_answer,
                    "answer_after": m.get("answer_after", ""),
                    "hypothesis": "",
                    "shift_bucket": m.get("shift_bucket"),
                })
        elif tool == "batched_supernode_sweep":
            for m in output.get("measurements", []) or []:
                norm_feats = []
                for f in m.get("features") or []:
                    if isinstance(f, dict):
                        pos = f.get("pos", f.get("position", 0))
                        norm_feats.append({
                            "layer": int(f.get("layer")),
                            "feature_idx": int(f.get("feature_idx")),
                            "position": int(pos),
                        })
                    else:
                        norm_feats.append({
                            "layer": int(f[0]),
                            "feature_idx": int(f[1]),
                            "position": int(f[2]) if len(f) > 2 else 0,
                        })
                out.append({
                    "source": "batched_supernode_sweep",
                    "intervention": {
                        "type": "supernode",
                        "features": norm_feats,
                        "scale": float(m["scale"]),
                    },
                    "top5_before": m.get("top5_before"),
                    "top5_after": m.get("top5_after"),
                    "answer_before": baseline_answer,
                    "answer_after": m.get("answer_after", ""),
                    "hypothesis": m.get("rationale", ""),
                    "shift_bucket": m.get("shift_bucket"),
                })
        elif tool == "anchor_pass":
            answer_before = output.get("answer_before")
            hypothesis = output.get("hypothesis")
            for per_feature in output.get("anchor_results", []) or []:
                flat = dict(per_feature)
                flat.setdefault("answer_before", answer_before)
                flat.setdefault("hypothesis", hypothesis)
                flat.setdefault("source", "anchor_pass")
                out.append(flat)
    return out


# ── Main ─────────────────────────────────────────────────────────────────────

def positive_int(value: str) -> int:
    """argparse type for a 1-based index. Rejects 0 and negatives.

    `--pass-index 0` would otherwise produce a `_pass0` directory that reads as
    a real pass and quietly makes a 5-pass repeat look like 6.
    """
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError(f"must be 1 or greater, got {n}")
    return n


def timing_filename(tag: str | None = None) -> str:
    """Filename for this process's GPU timing summary.

    A multi-GPU node runs one process per card, and they are meant to share one
    out-root: the slug shards are disjoint and every other output is already
    keyed by slug, so nothing else collides. This file was the exception. At a
    fixed name the last process to finish silently erased the other five, which
    loses exactly the gpu_held_s / gpu_wait_s measurement the batch exists to
    produce, and loses it without an error.

    The discriminator is derived rather than passed because a flag you have to
    remember is a flag that reintroduces the bug. CUDA_VISIBLE_DEVICES is what
    actually differs between the processes; the pid covers a single-GPU node
    where it is unset. Deliberately NOT pid-suffixed in the normal case, so a
    re-run of one shard overwrites its own stale file instead of leaving a
    partial batch behind for the collection step to average in.
    """
    # An empty tag is treated as absent, not as a valid discriminator: an
    # explicit --timing-tag "" or an exported-but-blank CUDA_VISIBLE_DEVICES
    # would otherwise give every process the same name, which is the original
    # bug wearing a different mask.
    if not (tag or "").strip():
        dev = os.environ.get("CUDA_VISIBLE_DEVICES", "").strip()
        tag = f"gpu{dev}" if dev else f"pid{os.getpid()}"
    safe = "".join(c if (c.isalnum() or c in "._-") else "_" for c in tag)
    return f"gpu_timing.{safe}.json"


def build_parser() -> argparse.ArgumentParser:
    """The CLI surface, split out of main() so tests can exercise the real
    parser rather than a re-declaration of it (a copy would let a default flip
    back without failing anything)."""
    parser = argparse.ArgumentParser(
        description="Run suppression-jailbreak experiments via the Circuit Oracle"
    )
    parser.add_argument(
        "--dataset-file", type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "prompts.json",
        help="Path to prompts JSON (default: data/prompts.json)"
    )
    parser.add_argument(
        "--arm", default=None,
        help="Arm registry key (circuit_oracle.arms), e.g. refusal-arm2. Owns the "
             "orchestrator, subagent, tool surface, and discovery-annotation mode, "
             "so it conflicts with --orchestrator / --subagent-model / "
             "--excluded-tools, and it sends output to runs/<arm>/ "
             "unless --out-root says otherwise. Refusal arms only: "
             f"{', '.join(arm_names(task='refusal'))}."
    )
    parser.add_argument(
        "--orchestrator", default=None,
        help=f"Orchestrator model ID (default: {DEFAULT_ORCHESTRATOR}; "
             f"conflicts with --arm)"
    )
    parser.add_argument(
        "--subagent-model", default=None,
        help=f"Subagent model ID (default: {DEFAULT_SUBAGENT}; conflicts with --arm)"
    )
    parser.add_argument(
        "--excluded-tools", nargs="*", default=None,
        help="Tool names to remove from the orchestrator's and subagents' tool "
             "lists (conflicts with --arm, which carries its own list)"
    )
    parser.add_argument(
        "--graph-dir", default=None,
        help="Graph store directory (default: $GRAPH_STORE/graphs when GRAPH_STORE "
             "is set, else weights/graphs)"
    )
    parser.add_argument(
        "--provider", default=os.environ.get("LLM_PROVIDER", "openrouter"),
        choices=PROVIDER_CHOICES,
    )
    parser.add_argument("--slugs", nargs="*", help="Filter by entry slug")
    parser.add_argument(
        "--category", choices=["censorship", "refusal"], default=None,
        help="Only run prompts in this category",
    )
    parser.add_argument("--limit", type=int, default=None,
                        help="Run only the first N entries after filtering")
    parser.add_argument("--max-hops", type=int, default=12)
    parser.add_argument("--control-runs", type=int, default=1,
                        help="Independent Oracle-without-tools control runs (default: 1)")
    parser.add_argument("--self-rating-samples", type=int, default=5,
                        help="Subject-model self-confidence samples (default: 5). Set 0 to disable.")
    parser.add_argument("--self-rating-temperature", type=float, default=0.7,
                        help="Sampling temperature for self-rating (default: 0.7)")
    parser.add_argument("--keep-graphs", action=argparse.BooleanOptionalAction, default=True,
                        help="Keep the cached attribution graph (.pt) after the run completes "
                             "(default ON). The 5x repeat and the multi-arm grid must reuse ONE "
                             "graph per slug: nothing in the attribution path is seeded, so two "
                             "builds of the same prompt can hand the oracle different feature "
                             "sets, which contaminates exactly the stability numbers the repeat "
                             "exists to measure. Pass --no-keep-graphs for the old disk-saving "
                             "behaviour.")
    parser.add_argument("--require-graph", action="store_true",
                        help="Fail loud if the cached .pt is missing instead of building it. "
                             "Use on shard pods after the pre-build pass so no shard silently "
                             "spends an hour on attribution.")
    parser.add_argument("--pass-index", type=positive_int, default=None,
                        help="1-based index of this repeat pass, recorded in oracle_result.json "
                             "and in the run directory name. Without it the only discriminator "
                             "between repeat passes is a second-resolution timestamp, so a "
                             "crashed-and-retried pass leaves an unmarked sibling directory that "
                             "a glob-and-average silently folds in.")
    parser.add_argument("--max-feature-nodes", type=int, default=8192,
                        help="Cap on feature nodes per attribution graph (default 8192, 0 means unbounded). "
                             "The archived sweep-era graphs were built at 10000, so numbers from the two "
                             "generations must not be mixed inside one comparison.")
    parser.add_argument("--out-root", type=Path, default=None,
                        help="Root for fresh run output (default runs/, which is gitignored). The "
                             "committed archives live in results/ and results-workshop/ and are "
                             "never written to.")
    parser.add_argument("--timing-tag", default=None,
                        help="Override the discriminator in this process's gpu_timing.<tag>.json. "
                             "Rarely needed: it defaults to CUDA_VISIBLE_DEVICES, which already "
                             "differs across the one-process-per-card launch. Pass it only when two "
                             "processes share a card and would otherwise write the same file.")
    parser.add_argument(
        "--workers", type=positive_int, default=1,
        help="Concurrent prompts per process (default 1, the historical serial "
             "behaviour). A run is API-bound, ~19 serial orchestrator turns over "
             "~41 min, so the GPU idles through most of it and N runs can share "
             "ONE model copy with their GPU sections queued behind a lock. That is "
             "what makes 50 prompts a ~6-GPU job instead of a ~50-GPU one, since "
             "the model plus transcoders costs 36.4 GB per copy. Above 1 this "
             "installs the GPU lock, routes each run's stdout to its own run.log, "
             "and reports lock contention at the end. Pair with --require-graph: "
             "concurrent cache-miss graph builds are the one genuinely GPU-bound "
             "part and will thrash.",
    )
    parser.add_argument(
        "--subagent-concurrency", type=positive_int, default=32,
        help="Process-wide ceiling on in-flight REASSESS subagent calls when "
             "--workers > 1 (default 32). Each run's fan-out pool sizes itself "
             "to its own shifted-feature count, so without a global cap N runs "
             "put N x ~10 calls in flight and the Groq-pinned subagent throttles. "
             "Ignored at --workers 1, which keeps the historical unbounded "
             "behaviour.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print resolved entry metadata without loading the model or running any LLM calls.",
    )
    parser.add_argument("--quiet", action="store_true")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    verbose = not args.quiet

    # Resolve the arm. --arm owns the model and tool knobs, so combining it
    # with the ad-hoc flags is a contradiction and dies here rather than
    # silently letting one side win (a mislabeled run poisons a whole batch).
    arm = None
    if args.arm is not None:
        try:
            # This runner serves both pipelines: the agentic loop and the
            # arm-3 one-shot (run_oneshot_oracle), dispatched below on
            # arm.pipeline. Foreign tasks still die here.
            arm = resolve_arm(args.arm, task="refusal",
                              pipeline=("agentic", "oneshot"))
        except ValueError as e:
            parser.error(str(e))
        for flag, val in (
            ("--orchestrator", args.orchestrator),
            ("--subagent-model", args.subagent_model),
            ("--excluded-tools", args.excluded_tools),
        ):
            if val is not None:
                parser.error(f"{flag} conflicts with --arm (the arm owns it)")
        orchestrator = arm.orchestrator_model
        subagent = arm.subagent_model
        excluded_tools = list(arm.excluded_tools)
    else:
        orchestrator = args.orchestrator or DEFAULT_ORCHESTRATOR
        subagent = args.subagent_model or DEFAULT_SUBAGENT
        excluded_tools = list(args.excluded_tools or [])

    # One directory per arm. The saved leaf is {orchestrator}_{subagent}_{ts},
    # so arms 1 and 2 (same models, different tool surface) would otherwise be
    # distinguishable only by reading oracle_result.json. The 5x repeat of
    # arm 1 does share a directory, which is what a repeat means.
    if args.out_root is not None:
        out_root = args.out_root
    elif arm is not None:
        out_root = DEFAULT_OUT_ROOT / arm.name
    else:
        out_root = DEFAULT_OUT_ROOT

    # Load prompts
    data = load_dataset_file(args.dataset_file)
    all_entries = data["entries"]

    # Filter
    selected = filter_entries(all_entries, slugs=args.slugs, category=args.category)

    if args.limit is not None and args.limit > 0:
        selected = selected[: args.limit]

    if not selected:
        if args.category is not None:
            print(f"No entries matched filters (category={args.category!r} produced an empty selection).")
        else:
            print("No entries matched filters.")
        all_slugs = [e["slug"] for e in all_entries]
        print(f"Available slugs ({len(all_slugs)}): {all_slugs}")
        sys.exit(1)

    print(f"\nEntries: {len(selected)}")
    if arm is not None:
        print(f"Arm: {arm.name} ({arm.description})")
    print(f"Orchestrator: {orchestrator}")
    print(f"Subagent: {subagent}")
    if excluded_tools:
        print(f"Excluded tools: {excluded_tools}")
    print(f"Provider: {args.provider}")
    print(f"Output root: {out_root}")
    if args.pass_index is not None:
        print(f"Pass index: {args.pass_index}")
    print(f"Keep graphs: {args.keep_graphs}")

    if args.dry_run:
        print("\n" + "=" * 72)
        print("DRY RUN, no model loaded, no LLM calls made.")
        print("=" * 72)
        for idx, entry in enumerate(selected):
            print(f"\n[{idx + 1}/{len(selected)}] {entry['slug']}")
            print(f"  system_prompt: {entry.get('system_prompt')!r}")
            print(f"  user_message:  {entry.get('user_message')!r}")
            if entry.get("notes"):
                print(f"  notes:         {entry['notes'][:120]}")
        print("\n" + "=" * 72)
        return

    # Every gateway this run will actually call must be credentialed BEFORE the
    # model load. Routing is per model, so a --provider kilo run still needs
    # OPENROUTER_API_KEY for the pinned openai/gpt-oss-120b subagent: without
    # this the graph build is paid for and then the first subagent call 401s.
    # NO_SUBAGENT is a provenance placeholder, not a model, so it is dropped.
    preflight_providers(
        [m for m in (orchestrator, subagent) if m != NO_SUBAGENT], args.provider
    )

    # --require-graph means fail FAST, so verify the WHOLE selection here rather
    # than per entry. Two reasons the per-entry check is not enough under
    # --workers > 1: require_cached_graph raises SystemExit, which derives from
    # BaseException and slips past the per-entry `except Exception`, and by the
    # time a worker reaches it the pool has already submitted every other entry,
    # so the batch runs on for hours and then dies without writing
    # gpu_timing.json or the failure summary. Checking here also means a missing
    # graph costs neither the 36 GB model load nor an API dollar.
    if args.require_graph:
        incomplete = []
        for entry in selected:
            cfg = entry_to_run_config(entry)
            if args.graph_dir:
                cfg.graph_cache_dir = args.graph_dir
            base = f"{cfg.graph_cache_dir}/{cfg.prompt_name}_graph.pt"
            absent = [p for p in (base, f"{base}.baseline.pt", f"{base}.baseline.json")
                      if not Path(p).exists()]
            if absent:
                incomplete.append((entry["slug"], absent))
        if incomplete:
            print(f"\nError: --require-graph, and {len(incomplete)} of "
                  f"{len(selected)} selected prompts have an incomplete graph cache:")
            for slug, absent in incomplete:
                print(f"  {slug}: missing {', '.join(Path(p).name for p in absent)}")
            print("\nRun the phase-0 pre-build first:")
            print("  python scripts/build_graphs.py            # or --shard i/N per card")
            sys.exit(1)
        print(f"Graph cache verified for all {len(selected)} prompts.")

    # Load model once (expensive GPU operation)
    print("\nLoading model...")
    model = load_model("Qwen/Qwen3-4B", "mwhanna/qwen3-4b-transcoders")

    # Create LLM client
    client = LLMClient(provider=args.provider)

    # ── Concurrency ──────────────────────────────────────────────────────
    # Only engaged above --workers 1, so the serial path keeps its exact
    # current behaviour and cost. See circuit_oracle/gpu_lock.py for why
    # sharing one model copy across threads is safe and why it is the
    # difference between a ~6-GPU job and a ~50-GPU one.
    concurrent_mode = args.workers > 1
    gpu = install_gpu_lock(model) if concurrent_mode else None
    routed = install_thread_logging() if concurrent_mode else None
    console = routed.base if routed is not None else sys.stdout

    if concurrent_mode:
        # Bound the NESTED fan-out. Each run's REASSESS pool sizes itself to its
        # own shifted-feature count, so without a global ceiling 13 runs at
        # ~9-12 features each put 120-160 subagent calls in flight at once, and
        # gpt-oss-120b is pinned to Groq, which throttles hard. Capping per pool
        # would not help: the ceiling would still be workers x pool_size.
        fanout.set_limit(args.subagent_concurrency)
        print(f"Subagent fan-out capped at {args.subagent_concurrency} in flight.")

    log_dir = out_root / "logs"
    if concurrent_mode:
        log_dir.mkdir(parents=True, exist_ok=True)

    tally_lock = threading.Lock()
    timings: list[dict] = []
    failures: list[dict] = []

    def _console(msg: str) -> None:
        """Write past any per-thread stdout routing, to the real terminal."""
        print(msg, file=console, flush=True)

    def _run_one_inner(idx, entry):
        print(f"\n{'='*60}")
        print(f"[{idx+1}/{len(selected)}] {entry['slug']}")
        print(f"  Prompt: {entry['user_message']}")
        print(f"{'='*60}")

        cache_path = None
        try:
            cfg = entry_to_run_config(entry)
            cfg.orchestrator_model = orchestrator
            cfg.subagent_model = subagent
            cfg.provider = args.provider
            cfg.max_subagent_hops = args.max_hops
            cfg.verbose = verbose
            cfg.task = "refusal"
            cfg.arm = arm.name if arm is not None else None
            cfg.pass_index = args.pass_index
            if args.graph_dir:
                # Flag > GRAPH_STORE env > weights/graphs (the env default is
                # resolved inside RunConfig's graph_cache_dir factory).
                cfg.graph_cache_dir = args.graph_dir

            prompt = format_chat(
                model.tokenizer,
                cfg.system_prompt,
                cfg.user_message,
                cfg.assistant_prefix,
            )

            candidate_cache_path = f"{cfg.graph_cache_dir}/{cfg.prompt_name}_graph.pt"
            require_cached_graph(candidate_cache_path, args.require_graph)
            # Bound only after the guard passes. The finally block keys its
            # delete on cache_path, so binding before the guard meant that
            # --require-graph --no-keep-graphs against a partial cache would
            # report the missing baseline sibling and then delete the one .pt
            # the operator was trying to protect, on the way out through the
            # SystemExit.
            cache_path = candidate_cache_path
            max_feat = args.max_feature_nodes if args.max_feature_nodes > 0 else None
            # Held across the WHOLE call, not left to the per-method guard.
            # setup_attribution "precomputes the transcoder activations and error
            # vectors, saving them" onto the model, and the attribution pass then
            # reads that saved state. It is the one multi-call sequence in the
            # pipeline that carries state between GPU calls, so two threads
            # building graphs at once would read each other's activations. On the
            # cache-hit path (the intended one, see --require-graph) this is a
            # fast load and the hold is cheap.
            if gpu is None:
                graph_result = compute_or_load_graph(
                    prompt, model, cache_path=cache_path, max_feature_nodes=max_feat,
                )
            else:
                with gpu.hold("compute_or_load_graph"):
                    graph_result = compute_or_load_graph(
                        prompt, model, cache_path=cache_path, max_feature_nodes=max_feat,
                    )
            graph = graph_result["graph"]

            print(
                f"Graph: {graph.adjacency_matrix.shape[0]} nodes, "
                f"{len(graph.selected_features)} features, "
                f"{len(graph.logit_tokens)} logits"
            )

            ctx = ToolContext(
                graph=graph,
                tokenizer=model.tokenizer,
                replacement_model=graph_result["replacement_model"],
                baseline_activations=graph_result["baseline_activations"],
                baseline_answer=graph_result["baseline_answer"],
                baseline_top5=graph_result["baseline_top5"],
                baseline_prompt=prompt,
                system_prompt=cfg.system_prompt,
                discovery_annotation=arm.annotation if arm is not None else "full",
            )

            # Generate full model response ONCE
            full_response = generate_response(prompt, model, max_new_tokens=800)
            print(f"Base model response: {full_response}")

            # Self-rating: subject model "are you sure?" confidence on its own response.
            self_rating = None
            if args.self_rating_samples > 0:
                print(f"Self-rating: sampling {args.self_rating_samples} confidence scores from Qwen3-4B...")
                self_rating = run_self_rating(
                    model,
                    system_prompt=cfg.system_prompt,
                    user_message=cfg.user_message,
                    qwen_answer=full_response,
                    n_samples=args.self_rating_samples,
                    temperature=args.self_rating_temperature,
                )
                mean_str = f"{self_rating['mean']:.2f}" if self_rating["mean"] is not None else "n/a"
                print(
                    f"  self mean={mean_str} "
                    f"parseable={self_rating['parseable_count']}/{self_rating['n_attempts']} "
                    f"({self_rating['elapsed_seconds']:.1f}s)"
                )

            if arm is not None and arm.pipeline == "oneshot":
                run_single_oneshot(
                    cfg, ctx, client, prompt,
                    full_response,
                    verbose,
                    control_runs=args.control_runs,
                    self_rating=self_rating,
                    out_root=out_root,
                )
            else:
                run_single_orchestrator(
                    cfg, ctx, client, prompt,
                    full_response,
                    verbose,
                    control_runs=args.control_runs,
                    self_rating=self_rating,
                    out_root=out_root,
                    excluded_tools=excluded_tools,
                )
        finally:
            if cache_path and not args.keep_graphs:
                graph_file = Path(cache_path)
                if graph_file.exists():
                    size_mb = graph_file.stat().st_size / (1024 * 1024)
                    graph_file.unlink()
                    print(f"  Deleted cached graph: {graph_file.name} ({size_mb:.1f} MB)")

    def _run_one(indexed):
        """Per-entry wrapper: log routing, timing, and failure isolation."""
        idx, entry = indexed
        slug = entry["slug"]
        if gpu is not None:
            gpu.reset_thread()
        started = time.time()
        _console(f"[{idx+1}/{len(selected)}] START  {slug}")
        try:
            if routed is None:
                _run_one_inner(idx, entry)
            else:
                with routed.route_to(log_dir / f"{slug}.log"):
                    _run_one_inner(idx, entry)
        except (Exception, SystemExit):
            # One bad prompt must not discard the other 49. The slug is recorded
            # and main() exits non-zero at the end with the full list. Dying on
            # the spot would throw away hours of good runs; continuing WITHOUT
            # the non-zero exit would be the silent-partial-batch failure this
            # codebase refuses everywhere else.
            #
            # SystemExit is caught explicitly because several helpers call
            # sys.exit() rather than raising, and SystemExit derives from
            # BaseException. Letting one escape a worker would tear the batch
            # down past the summary and the timing file. KeyboardInterrupt is
            # deliberately NOT caught, so Ctrl-C still stops everything.
            detail = traceback.format_exc()
            # Append to the run log explicitly. By the time we get here the
            # routed block has already exited and closed the sink, so a plain
            # print() would reach only the console and the per-run log would end
            # mid-sentence with no explanation.
            if routed is not None:
                with open(log_dir / f"{slug}.log", "a", encoding="utf-8") as fh:
                    fh.write("\n" + detail)
            _console(f"[{idx+1}/{len(selected)}] FAILED {slug}\n{detail}")
            with tally_lock:
                failures.append({
                    "slug": slug,
                    "error": detail.strip().splitlines()[-1],
                })
            return

        elapsed = time.time() - started
        rec = {"slug": slug, "wall_s": round(elapsed, 1)}
        suffix = ""
        if gpu is not None:
            st = gpu.stats()
            rec["gpu_held_s"] = round(st["held_s"], 1)
            rec["gpu_wait_s"] = round(st["wait_s"], 1)
            rec["gpu_calls"] = st["calls"]
            suffix = f"  gpu_held={rec['gpu_held_s']}s gpu_wait={rec['gpu_wait_s']}s"
        with tally_lock:
            timings.append(rec)
        _console(f"[{idx+1}/{len(selected)}] DONE   {slug}  "
                 f"wall={elapsed / 60:.1f}m{suffix}")

    work = list(enumerate(selected))
    batch_started = time.time()

    if concurrent_mode:
        _console(f"\nRunning {len(work)} prompts, {args.workers} at a time.")
        _console(f"Per-run logs: {log_dir}/<slug>.log")
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=args.workers, thread_name_prefix="oracle"
        ) as pool:
            list(pool.map(_run_one, work))
    else:
        for item in work:
            _run_one(item)

    # Once, after every run has finished. The serial loop used to do this per
    # entry, which under concurrency would free blocks that other in-flight runs
    # are about to reuse and force them to re-allocate mid-sweep.
    #
    # Guarded, and deliberately BEFORE the timing summary is written. An
    # asynchronous device-side assert from anywhere in the batch is reported by
    # whichever CUDA call syncs next, and empty_cache() is usually that call. On
    # 2026-07-28 it raised here and killed the process before the summary was
    # written, destroying the gpu_held / gpu_wait measurement for a whole shard
    # whose 7 runs had all completed. The cache is being dropped at process exit
    # anyway, so failing to free it changes nothing that matters.
    try:
        torch.cuda.empty_cache()
    except RuntimeError as exc:
        _console(f"WARNING: empty_cache() failed, continuing to write timings: {exc}")

    batch_wall = time.time() - batch_started

    _console(f"\n{'='*60}")
    _console(f"Done: {len(timings)} ok, {len(failures)} failed, "
             f"batch wall {batch_wall / 60:.1f}m")

    if gpu is not None:
        totals = gpu.totals()
        # The two numbers that size the cluster. gpu_held summed over runs is the
        # serialized work one card must get through, so held_total / target_wall
        # is the GPU count. gpu_wait is time runs spent blocked on each other,
        # which says directly whether adding cards would help: near zero means
        # the batch is API-bound and more GPUs buy nothing.
        _console(f"GPU held total {totals['held_s'] / 60:.1f}m, "
                 f"wait total {totals['wait_s'] / 60:.1f}m, "
                 f"peak waiters {totals['peak_waiters']}, "
                 f"{totals['calls']} sections")
        if timings:
            mean_held = sum(t.get("gpu_held_s", 0.0) for t in timings) / len(timings)
            _console(f"Mean GPU per run {mean_held / 60:.2f}m. To finish "
                     f"{len(selected)} runs inside 1h needs about "
                     f"{max(1, round(mean_held * len(selected) / 3600 + 0.5))} GPU(s) "
                     f"of queue capacity.")
        summary = {
            "workers": args.workers,
            "batch_wall_s": round(batch_wall, 1),
            "n_ok": len(timings),
            "n_failed": len(failures),
            "gpu_totals": totals,
            # Recorded inside the file too, so a collection step can still tell
            # the shards apart after the files are gathered and renamed.
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "pid": os.getpid(),
            "runs": sorted(timings, key=lambda r: r["slug"]),
            "failures": failures,
        }
        timing_path = out_root / timing_filename(args.timing_tag)
        timing_path.parent.mkdir(parents=True, exist_ok=True)
        timing_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        _console(f"Timing summary: {timing_path}")

    _console(f"{'='*60}")

    if failures:
        # Non-zero exit so a shard pod's wrapper script cannot mistake a
        # partially-failed batch for a clean one.
        raise SystemExit(
            f"{len(failures)} of {len(selected)} runs FAILED: "
            + ", ".join(f["slug"] for f in failures)
        )


if __name__ == "__main__":
    main()
