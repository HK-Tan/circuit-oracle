#!/usr/bin/env python3
"""
Balanced multi-GPU launcher for the task-1 graph build.

The build is embarrassingly parallel: attribution for one (prompt, probe) pair is
a pure function of the model, the transcoders, the probe vector and the prompt,
with no cross-prompt state and one output file per prompt. So the only real
question is how to cut the 40 prompts into N piles of equal WORK, and the answer
is not "one dataset per GPU": prompt length varies about 4x across the manifest,
so a per-dataset split leaves bib_nurse_professor running roughly 40 minutes
while civil_comments finishes in 17.

    per-dataset split, 4 GPUs -> 2.7x
    balanced split,    4 GPUs -> 4.0x

Both need zero changes to the build itself. run_extraction_batch.py already takes
--tags, so a balanced split is just a different argument list.

Usage (from the repository root, on the build pod):

    python spurious-correlation/scripts/build_shards.py --shards 4 --dry-run
    python spurious-correlation/scripts/build_shards.py --shards 4
    python spurious-correlation/scripts/build_shards.py --shards 4 --no-warm   # caches already hot

Everything is --skip-existing by default, so re-running after a crash rebalances
whatever is left rather than starting over.

Per-shard logs land in spurious-correlation/runs/build_logs/shard<N>.out, which
is gitignored. The graphs themselves go to $GRAPH_STORE/probe_circuits.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Same directory as the batch runner, whose manifest parsing and store paths we
# reuse rather than duplicate. Importing it also loads the repo-root .env, which
# is what resolves GRAPH_STORE.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_extraction_batch as reb

BATCH_SCRIPT = Path(__file__).resolve().parent / "run_extraction_batch.py"

# ── Cost model ───────────────────────────────────────────────────────────────
# Per prompt, in seconds. Only RELATIVE values matter here, since all this does
# is decide which pile a prompt lands in.
#
#   FIXED_S      one model load, one dataset load, two Phase-0 transcoder passes,
#                and (unless --skip-neuronpedia) the explanation fetch. Paid once
#                per prompt regardless of length, because the build spawns one
#                subprocess per prompt.
#   PER_CHAR_S   Phase 1 forward plus the Phase 4 backward passes, for BOTH
#                graphs. Linear in n_pos at fixed max_feature_nodes, since the
#                pass count is mfn/batch_size and each pass runs over a
#                batch x n_pos retained graph.
#   SAVE_S_PER_GB  torch.save of a dense adjacency matrix, whose size follows the
#                graph size law, N = mfn + (n_layers+1)*n_pos + 1 at 4N^2 bytes.
#                Quadratic in n_pos, so it is not negligible on the long bios.
#
# Characters stand in for tokens on purpose: the balance only needs a monotone
# proxy, and tokenizing here would make the planner depend on a gated HF download
# just to decide a partition. Calibrate FIXED_S and PER_CHAR_S off the warm-up
# run's log if the shards finish visibly unevenly.
FIXED_S = 65.0
PER_CHAR_S = 0.275          # about 1.1 s per token over two graphs, at ~4 chars/token
SAVE_S_PER_GB = 1.0
MAX_FEATURE_NODES = 4096    # must match circuit_extraction.MAX_FEATURE_NODES
N_LAYERS = 26               # gemma-2-2b


def prompt_cost(text: str) -> float:
    """Estimated seconds to build both graphs for one prompt."""
    n_tok = len(text) // 4 + 2
    n_nodes = MAX_FEATURE_NODES + (N_LAYERS + 1) * n_tok + 1
    save_gb = 2 * 4 * n_nodes * n_nodes / 1e9
    return FIXED_S + PER_CHAR_S * len(text) + SAVE_S_PER_GB * save_gb


def collect_items(skip_existing: bool = True) -> list[tuple[str, str, str, float]]:
    """Every (dataset, tag, prompt, cost) still to build, most expensive first.

    Sorting matters: the greedy partition below is longest-processing-time-first,
    which is the standard 4/3-approximation for this problem and in practice lands
    within a percent of perfect on a spread like ours.
    """
    items: list[tuple[str, str, str, float]] = []
    for dataset in reb.VALID_DATASETS:
        prompts = reb.parse_dataset_prompts(dataset)
        for tag, text in reb.build_runs(prompts):
            if skip_existing and reb.output_exists(dataset, tag):
                continue
            items.append((dataset, tag, text, prompt_cost(text)))
    items.sort(key=lambda it: -it[3])
    return items


def plan_shards(items, n_shards: int) -> list[list[tuple[str, str, str, float]]]:
    """Greedy longest-processing-time-first partition into n_shards piles."""
    if n_shards < 1:
        raise ValueError(f"n_shards must be >= 1, got {n_shards}")
    shards: list[list] = [[] for _ in range(n_shards)]
    loads = [0.0] * n_shards
    for item in items:
        j = loads.index(min(loads))
        shards[j].append(item)
        loads[j] += item[3]
    return shards


def shard_commands(shard, skip_neuronpedia: bool, skip_existing: bool) -> list[list[str]]:
    """One run_extraction_batch.py invocation per dataset present in this shard.

    Grouped by dataset because --dataset selects the probe pair and the adapter,
    so it cannot be mixed within a single invocation. Order is by descending cost
    so the expensive work starts first and a late failure costs less.
    """
    by_dataset: dict[str, list[tuple[str, float]]] = {}
    for dataset, tag, _text, cost in shard:
        by_dataset.setdefault(dataset, []).append((tag, cost))

    cmds: list[list[str]] = []
    for dataset in sorted(by_dataset, key=lambda d: -sum(c for _, c in by_dataset[d])):
        tags = [t for t, _ in sorted(by_dataset[dataset], key=lambda tc: -tc[1])]
        cmd = [sys.executable, str(BATCH_SCRIPT), "--dataset", dataset, "--tags", *tags]
        if skip_existing:
            cmd.append("--skip-existing")
        if skip_neuronpedia:
            cmd.append("--skip-neuronpedia")
        cmds.append(cmd)
    return cmds


def run_shard(gpu_id: int, cmds: list[list[str]], log_dir: Path) -> int:
    """Run one shard's invocations sequentially, pinned to one GPU."""
    env = dict(os.environ)
    env["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
    log_path = log_dir / f"shard{gpu_id}.out"
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w") as log_f:
        for cmd in cmds:
            log_f.write(f"\n$ CUDA_VISIBLE_DEVICES={gpu_id} {' '.join(cmd)}\n")
            log_f.flush()
            rc = subprocess.run(cmd, env=env, stdout=log_f, stderr=subprocess.STDOUT,
                                check=False).returncode
            if rc != 0:
                print(f"[gpu{gpu_id}] FAILED rc={rc}: {' '.join(cmd[-6:])}", flush=True)
                return rc
    print(f"[gpu{gpu_id}] done, log at {log_path}", flush=True)
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--shards", type=int, default=1,
                    help="Number of parallel shards, normally the GPU count")
    ap.add_argument("--gpu-ids", type=int, nargs="+", default=None,
                    help="Explicit CUDA device ids, default 0..shards-1")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the plan and the predicted per-shard minutes, run nothing")
    ap.add_argument("--no-warm", action="store_true",
                    help="Skip the single-prompt warm-up. Only safe when the HF and "
                         "dataset caches are already populated on this pod.")
    ap.add_argument("--with-neuronpedia", action="store_true",
                    help="Keep the stdout-only per-feature explanation fetch. Off by "
                         "default on a sharded build, where it is pure GPU idle time.")
    ap.add_argument("--rebuild-existing", action="store_true",
                    help="Plan every prompt, not only the missing ones. The build is "
                         "nondeterministic, so this makes NEW graphs rather than "
                         "reproducing the old ones. Almost never what you want.")
    args = ap.parse_args()

    gpu_ids = args.gpu_ids if args.gpu_ids is not None else list(range(args.shards))
    if len(gpu_ids) != args.shards:
        ap.error(f"--gpu-ids has {len(gpu_ids)} entries but --shards is {args.shards}")

    skip_existing = not args.rebuild_existing
    skip_neuronpedia = not args.with_neuronpedia

    items = collect_items(skip_existing=skip_existing)
    if not items:
        print("Nothing to build, every graph in the manifest is already present.", flush=True)
        return

    total = sum(c for *_, c in items)
    print(f"Graph store:  {reb.PROBE_CIRCUITS_DIR}", flush=True)
    print(f"To build:     {len(items)} prompts ({2 * len(items)} graphs)", flush=True)
    print(f"Serial estimate: {total / 60:.0f} min\n", flush=True)

    # The warm-up is a real build of the cheapest prompt, run alone. It populates
    # the HF model cache, the transcoder shards and the HF datasets cache, so the
    # fan-out does not have N processes racing for the same cold downloads and
    # their file locks. It is not wasted work: the graph it produces is one of the
    # 80, and --skip-existing means the fan-out simply skips it. It is also the
    # calibration point, so read peak VRAM and the phase timings out of its log
    # before trusting any estimate in this file.
    if not args.no_warm and args.shards > 1 and not args.dry_run:
        w_dataset, w_tag, _w_text, w_cost = items[-1]
        print(f"Warm-up (cold caches, calibration): {w_dataset} {w_tag}, "
              f"~{w_cost / 60:.1f} min", flush=True)
        warm_cmd = [sys.executable, str(BATCH_SCRIPT), "--dataset", w_dataset,
                    "--tags", w_tag, "--skip-existing"]
        if skip_neuronpedia:
            warm_cmd.append("--skip-neuronpedia")
        rc = subprocess.run(warm_cmd, check=False,
                            env={**os.environ, "CUDA_VISIBLE_DEVICES": str(gpu_ids[0])})
        if rc.returncode != 0:
            print(f"Warm-up failed (rc={rc.returncode}). Not fanning out.", flush=True)
            sys.exit(rc.returncode)
        items = collect_items(skip_existing=skip_existing)

    shards = plan_shards(items, args.shards)
    plans = [(gpu, shard, shard_commands(shard, skip_neuronpedia, skip_existing))
             for gpu, shard in zip(gpu_ids, shards)]

    print("Plan:", flush=True)
    for gpu, shard, cmds in plans:
        load = sum(c for *_, c in shard) / 60
        print(f"  gpu{gpu}: {len(shard):2d} prompts, ~{load:5.1f} min, "
              f"{len(cmds)} invocation(s)", flush=True)
        for dataset, tag, _t, _c in sorted(shard):
            print(f"       {dataset}:{tag}", flush=True)
    wall = max((sum(c for *_, c in s) for s in shards), default=0.0) / 60
    print(f"\nPredicted wall clock: {wall:.0f} min "
          f"({total / 60 / wall:.2f}x on {args.shards} GPU(s))", flush=True)

    if args.dry_run:
        print("\n--dry-run, nothing executed.", flush=True)
        return

    log_dir = reb.LOGS_DIR
    with ThreadPoolExecutor(max_workers=args.shards) as pool:
        rcs = list(pool.map(lambda p: run_shard(p[0], p[2], log_dir), plans))

    # The per-shard runs each verify their own tags. This is the whole-store
    # check, which is the one that has to pass before the GPU is torn down.
    print("\nVerifying the full 80-graph store...", flush=True)
    verify = subprocess.run([sys.executable, str(BATCH_SCRIPT), "--verify-store"], check=False)
    if any(rcs) or verify.returncode != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
