#!/usr/bin/env python3
"""Phase 0: pre-build attribution graphs for many slugs, one model load.

WHY THIS EXISTS (vs build_graph.py, singular)
---------------------------------------------
``build_graph.py`` builds one slug per invocation. Loading Qwen3-4B plus its 36
layers of transcoders costs 36.4 GB and a couple of minutes, so shelling out to
it 50 times pays that cost 50 times. This loads the model once and walks a list.

WHY PHASE 0 IS SEPARATE FROM THE ORACLE RUNS
--------------------------------------------
The two phases have opposite bottlenecks and must not be mixed:

  phase 0 (this script)  pure GPU, no API calls. Embarrassingly parallel across
                         cards, and the only genuinely compute-bound part.
  phase 1 (run_all.py)   API-bound. ~19 serial orchestrator turns per prompt over
                         ~41 min, GPU idle most of it, so N runs share one model
                         copy behind the GPU lock (--workers N).

Running them together means every concurrent worker cache-misses and builds its
own graph at once, which serializes on the GPU lock and thrashes. Build first,
then run phase 1 with ``--require-graph`` so a missing graph fails loudly instead
of silently costing an hour of attribution mid-batch.

SHARDING ACROSS A CLUSTER
-------------------------
``--shard i/N`` takes every N-th slug starting at i (stride, not block), so an
uneven per-slug build time spreads evenly rather than piling onto one card::

    # on card 0 of 6                    # on card 5 of 6
    python scripts/build_graphs.py --shard 0/6
    python scripts/build_graphs.py --shard 5/6

WRITE TO CONTAINER DISK, TRANSFER AT THE END
--------------------------------------------
Point ``--graph-dir`` / ``$GRAPH_STORE`` at container disk, never at a MooseFS
network volume during the build. Silent write corruption there has produced
truncated .pt files that pass a size check, so copy up afterwards and verify with
scripts/verify_graphs.py, which actually loads each graph.

Usage:
  python scripts/build_graphs.py                       # every slug in prompts.json
  python scripts/build_graphs.py --shard 2/6           # this card's stride
  python scripts/build_graphs.py --slugs a b c         # explicit list
  python scripts/build_graphs.py --rebuild             # ignore existing cache
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

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
GRAPH_STORE = Path(os.environ.get("GRAPH_STORE", str(_REPO / "weights")))
DEFAULT_GRAPH_DIR = str(GRAPH_STORE / "graphs")
DEFAULT_MAX_FEATURE_NODES = 8192

# A cache hit needs ALL THREE files. The graph alone is not enough: run_all.py's
# require_cached_graph checks the siblings too, so a directory holding only the
# .pt would pass a naive existence check here and then fail the batch later.
CACHE_SUFFIXES = ("", ".baseline.pt", ".baseline.json")


def is_cached(cache_path: str) -> bool:
    return all(os.path.exists(cache_path + s) for s in CACHE_SUFFIXES)


def parse_shard(spec: str) -> tuple[int, int]:
    """Parse ``i/N`` with loud validation. A silently-misparsed shard would
    leave a hole in the graph set that only surfaces an hour later."""
    try:
        i_str, n_str = spec.split("/", 1)
        i, n = int(i_str), int(n_str)
    except ValueError:
        raise SystemExit(f"--shard must look like i/N (got {spec!r})")
    if n < 1 or not (0 <= i < n):
        raise SystemExit(f"--shard {spec!r} invalid: need 0 <= i < N and N >= 1")
    return i, n


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--dataset-file", type=Path, default=DEFAULT_DATASET)
    ap.add_argument("--slugs", nargs="*", default=None,
                    help="explicit slugs (default: every entry in the dataset)")
    ap.add_argument("--shard", default=None,
                    help="i/N stride shard for multi-GPU pre-build, e.g. 2/6")
    ap.add_argument("--graph-dir", default=DEFAULT_GRAPH_DIR,
                    help=f"output dir (default {DEFAULT_GRAPH_DIR}; container disk, "
                         "NOT a network volume, during the build)")
    ap.add_argument("--model-name", default=DEFAULT_MODEL)
    ap.add_argument("--transcoder-name", default=DEFAULT_TRANSCODER)
    ap.add_argument("--max-feature-nodes", type=int, default=DEFAULT_MAX_FEATURE_NODES,
                    help=f"feature-node cap (default {DEFAULT_MAX_FEATURE_NODES}; the "
                         "archived sweep-era graphs used 10000, never mix generations)")
    ap.add_argument("--rebuild", action="store_true",
                    help="rebuild even when all three cache files are present")
    args = ap.parse_args()

    data = json.loads(Path(args.dataset_file).read_text(encoding="utf-8"))
    entries = data["entries"]
    by_slug = {e["slug"]: e for e in entries}

    if args.slugs:
        missing = [s for s in args.slugs if s not in by_slug]
        if missing:
            raise SystemExit(
                f"slugs not in {args.dataset_file}: {missing}. "
                f"Available ({len(by_slug)}): {sorted(by_slug)}"
            )
        selected = [by_slug[s] for s in args.slugs]
    else:
        selected = list(entries)

    if args.shard:
        i, n = parse_shard(args.shard)
        selected = selected[i::n]
        print(f"Shard {i}/{n}: {len(selected)} of {len(entries)} slugs")

    if not selected:
        raise SystemExit("no slugs selected")

    os.makedirs(args.graph_dir, exist_ok=True)
    max_feat = args.max_feature_nodes if args.max_feature_nodes > 0 else None

    todo, already = [], []
    for e in selected:
        path = os.path.join(args.graph_dir, f"{e['slug']}_graph.pt")
        (already if (is_cached(path) and not args.rebuild) else todo).append((e, path))

    print(f"Graph dir: {args.graph_dir}")
    print(f"To build: {len(todo)}   already cached: {len(already)}")
    if not todo:
        print("Nothing to do.")
        return 0

    print(f"Loading model {args.model_name} + {args.transcoder_name} ...")
    model = load_model(args.model_name, args.transcoder_name)

    built, failed = [], []
    batch_started = time.time()
    for idx, (entry, cache_path) in enumerate(todo, start=1):
        slug = entry["slug"]
        print(f"\n[{idx}/{len(todo)}] {slug}", flush=True)
        started = time.time()
        try:
            if args.rebuild:
                # compute_or_load_graph LOADS when the cache is complete, so
                # without this --rebuild silently returned the old graph and
                # then reported the slug as "built". Clearing the triple first
                # is what actually forces attribution to re-run, and it is the
                # only way to recover from a corrupt cache.
                for suffix in CACHE_SUFFIXES:
                    stale = cache_path + suffix
                    if os.path.exists(stale):
                        os.remove(stale)

            prompt = format_chat(
                model.tokenizer,
                entry.get("system_prompt", "") or "",
                entry["user_message"],
                entry.get("assistant_prefix", "") or "",
            )
            result = compute_or_load_graph(
                prompt, model, cache_path=cache_path, max_feature_nodes=max_feat,
            )
            graph = result["graph"]
            elapsed = time.time() - started

            # Verify the siblings landed. compute_or_load_graph writing only the
            # .pt would produce a "built" graph that fails --require-graph later,
            # on a different pod, after the volume transfer.
            absent = [s for s in CACHE_SUFFIXES if not os.path.exists(cache_path + s)]
            if absent:
                raise RuntimeError(
                    f"graph built but sibling artifacts missing: "
                    f"{[cache_path + s for s in absent]}"
                )

            size_mb = sum(
                os.path.getsize(cache_path + s) for s in CACHE_SUFFIXES
            ) / (1024 * 1024)
            print(f"  ok {graph.adjacency_matrix.shape[0]} nodes, "
                  f"{len(graph.selected_features)} features, "
                  f"{size_mb:.0f} MB, {elapsed:.0f}s", flush=True)
            built.append(slug)
        except Exception:
            # Keep going. One bad prompt should not cost the other 49 their
            # build, but the non-zero exit below makes sure a wrapper script
            # cannot mistake a partial graph set for a complete one.
            print(traceback.format_exc(), flush=True)
            print(f"  FAILED {slug}", flush=True)
            failed.append(slug)

    print(f"\n{'=' * 60}")
    print(f"Built {len(built)}, failed {len(failed)}, skipped {len(already)} "
          f"in {(time.time() - batch_started) / 60:.1f}m")
    print(f"{'=' * 60}")
    if failed:
        print(f"FAILED slugs: {failed}")
        return 1
    print("\nnext: copy the graph dir to the network volume, then verify with")
    print(f"  python scripts/verify_graphs.py --graph-dir {args.graph_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
