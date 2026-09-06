#!/usr/bin/env python3
"""Build (and cache) the attribution graph for a prompt. No agent loop, no LLM.

The graph-only first step of the deterministic suppression path. It runs the
expensive part of run_all.py (the attribution computation) and NOTHING else, so
you do not pay for a full gpt-5.4 orchestrator run + self-rating + control just
to obtain a .pt.

It writes the same three artifacts compute_or_load_graph always writes, which is
all the downstream deterministic scripts consume (paths shown for the default
graph store, see GRAPH_STORE below):

  weights/graphs/<slug>_graph.pt               # attribution graph  (influence_seed.py)
  weights/graphs/<slug>_graph.pt.baseline.pt   # baseline activations (run_seed_sweep.py)
  weights/graphs/<slug>_graph.pt.baseline.json # baseline_answer + top5

Pipeline order:
  build_graph.py  ->  influence_seed.py (reads .pt, writes seed.json)
                  ->  run_seed_sweep.py (reads seed.json + .pt, runs ANCHOR sweep)

THIS SCRIPT RUNS THE SUBJECT MODEL. It must run on the GPU VM, not locally.

Usage (on the VM):
  python scripts/build_graph.py --slug tiananmen-massacre
  python scripts/build_graph.py --slug tiananmen-massacre --max-feature-nodes 0   # unbounded
  python scripts/build_graph.py --user-message "..." --slug my-adhoc-prompt

The feature-node cap is FROZEN into the saved .pt at build time. influence_seed
and run_seed_sweep just read whatever was saved, so build with the cap you want
ranked (default 8192, 0 = unbounded).

ERA WARNING on the cap: the archived sweep-era refusal graphs (and the numbers
derived from them) were built at 10000. New builds default to 8192, so an 8192
graph and a 10000 graph belong to two different generations and their numbers
must never be mixed inside one comparison. Re-derive a whole comparison within
one generation, or pass --max-feature-nodes 10000 to rebuild in the old one.

If the .pt already exists it is reused (cache hit), so re-running is cheap and
idempotent. Delete the .pt to force a rebuild.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Re-exec under the project venv (+ HF cache / CUDA env) so a bare
# `python scripts/build_graph.py` works without `source .venv/bin/activate`, and
# reuses the cached weights instead of re-downloading. No-op if already in the
# venv. Must precede the editable-package imports below.
from _venv_bootstrap import ensure_venv

ensure_venv(__file__)

from circuit_oracle import (
    compute_or_load_graph,
    format_chat,
    load_model,
)


DEFAULT_MODEL = "Qwen/Qwen3-4B"
DEFAULT_TRANSCODER = "mwhanna/qwen3-4b-transcoders"
_REPO = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = _REPO / "data" / "prompts.json"

# Graph store. Defaults to the repo-local weights/ tree (unchanged behavior when
# run from the repo root). Set GRAPH_STORE to a shared mount (for example a
# RunPod network volume) to keep the .pt cache off the repo and share it across
# pods, then graphs land in $GRAPH_STORE/graphs.
GRAPH_STORE = Path(os.environ.get("GRAPH_STORE", str(_REPO / "weights")))
DEFAULT_GRAPH_DIR = str(GRAPH_STORE / "graphs")

# Feature-node cap for NEW builds. 8192 is the current refusal generation. The
# archived sweep-era graphs were built at 10000, so do not mix numbers derived
# from the two generations inside one comparison.
DEFAULT_MAX_FEATURE_NODES = 8192


def entry_for_slug(dataset_path: Path, slug: str) -> dict:
    """Resolve a prompts.json entry by slug. Fail loud if absent."""
    with open(dataset_path) as f:
        data = json.load(f)
    entries = data.get("entries")
    if not entries:
        raise ValueError(f"{dataset_path} has no 'entries'")
    for e in entries:
        if e.get("slug") == slug:
            return e
    available = [e.get("slug") for e in entries]
    raise KeyError(f"slug {slug!r} not in {dataset_path}. Available ({len(available)}): {available}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", required=True,
                    help="prompt slug (used to name the cache file; looked up in --dataset-file unless --user-message is given)")
    ap.add_argument("--dataset-file", type=Path, default=DEFAULT_DATASET,
                    help=f"prompts JSON (default: {DEFAULT_DATASET})")
    ap.add_argument("--user-message", default=None,
                    help="override: use this user message instead of the prompts.json entry (ad-hoc prompt)")
    ap.add_argument("--system-prompt", default=None,
                    help="override: system prompt (only with --user-message; default empty)")
    ap.add_argument("--assistant-prefix", default=None,
                    help="override: assistant prefix (only with --user-message; default empty)")
    ap.add_argument("--graph-dir", default=DEFAULT_GRAPH_DIR,
                    help=f"directory for the cached .pt (default: {DEFAULT_GRAPH_DIR}, "
                         "override the base with the GRAPH_STORE env var)")
    ap.add_argument("--model-name", default=DEFAULT_MODEL)
    ap.add_argument("--transcoder-name", default=DEFAULT_TRANSCODER)
    ap.add_argument("--max-feature-nodes", type=int, default=DEFAULT_MAX_FEATURE_NODES,
                    help=f"cap on feature nodes baked into the .pt (default "
                         f"{DEFAULT_MAX_FEATURE_NODES}, the current refusal generation. The "
                         "archived sweep-era graphs used 10000, never mix the two in one "
                         "comparison. 0 = unbounded)")
    args = ap.parse_args()

    if args.user_message is not None:
        system_prompt = args.system_prompt or ""
        user_message = args.user_message
        assistant_prefix = args.assistant_prefix or ""
        print(f"Ad-hoc prompt for slug {args.slug!r} (not read from {args.dataset_file})")
    else:
        entry = entry_for_slug(args.dataset_file, args.slug)
        system_prompt = entry.get("system_prompt", "") or ""
        user_message = entry["user_message"]
        assistant_prefix = entry.get("assistant_prefix", "") or ""
        print(f"Resolved slug {args.slug!r} from {args.dataset_file}")
    print(f"  user_message: {user_message!r}")
    if system_prompt:
        print(f"  system_prompt: {system_prompt!r}")

    cache_path = os.path.join(args.graph_dir, f"{args.slug}_graph.pt")
    max_feat = args.max_feature_nodes if args.max_feature_nodes > 0 else None
    cap_msg = "unbounded" if max_feat is None else str(max_feat)

    if os.path.exists(cache_path):
        print(f"Cache present at {cache_path} (will reuse, not rebuild). Delete it to force a rebuild.")

    print(f"Loading model {args.model_name} + {args.transcoder_name} ...")
    model = load_model(args.model_name, args.transcoder_name)

    prompt = format_chat(model.tokenizer, system_prompt, user_message, assistant_prefix)
    print(f"Building attribution graph (feature-node cap: {cap_msg}) -> {cache_path}")
    graph_result = compute_or_load_graph(
        prompt, model, cache_path=cache_path, max_feature_nodes=max_feat,
    )
    graph = graph_result["graph"]

    print(
        f"\nGraph: {graph.adjacency_matrix.shape[0]} nodes, "
        f"{len(graph.selected_features)} features, {len(graph.logit_tokens)} logits"
    )
    print(f"baseline answer: {(graph_result['baseline_answer'] or '')[:160]!r}")
    print("\nartifacts written:")
    for suffix in ("", ".baseline.pt", ".baseline.json"):
        p = cache_path + suffix
        ok = "ok" if os.path.exists(p) else "MISSING"
        print(f"  [{ok}] {p}")
    print(f"\nnext: python scripts/influence_seed.py --graph {cache_path} --slug {args.slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
