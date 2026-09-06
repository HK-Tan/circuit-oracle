"""Parallel launcher for the task-1 arm fan-out.

`run_oracle_on_probes.py` is a sequential loop over graphs, so the whole
720-run grid takes about 99 hours in one process. The runs are almost entirely
blocked on API latency rather than on CPU, so the fix is process-level
concurrency, and it needs no change to the runner because `--slugs` already
selects a single graph.

**Why one process per run and not one process per shard.** A static partition
of 720 items over N workers has a makespan set by the slowest *shard*, and the
per-run spread here is wide (the archived timings run roughly 3x from the
fastest graph to the slowest). A dynamic queue with one subprocess per item
makes the makespan the slowest *single run* instead, which is the same lesson
`secret-elicitation/scripts/taboo_shard.py` records for task 2. The cost is
one interpreter start per run, roughly 10 s against a 500 s run, so about 2
percent. Crash isolation comes free: one bad graph kills one item, not a shard.

**Thread oversubscription is the trap that will actually bite.** Torch defaults
its BLAS pools to the core count, so 200 processes on a 32-vCPU box would each
spawn 32 threads and spend their time in the scheduler. Every child is pinned
to a single thread below, which is correct here because the parallelism is
across runs and each run's linear algebra is a small part of its wall clock.

Run `--dry-run` first to see the plan, and `--pilot N` to time a small sample
before committing the full grid. Cost is read back out of each run's
`oracle_result.json`, so the pilot answers "what does the fan-out cost" with a
measurement rather than an estimate.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_TASK_ROOT = Path(__file__).resolve().parent.parent
_REPO_ROOT = _TASK_ROOT.parent

sys.path.insert(0, str(_REPO_ROOT / "src"))

from circuit_oracle.arms import arm_names  # noqa: E402
from circuit_oracle.llm_client import PROVIDER_CHOICES  # noqa: E402

PROMPTS_JSON = _TASK_ROOT / "prompts.json"
RUNNER = _TASK_ROOT / "scripts" / "run_oracle_on_probes.py"
REPORTED_METHOD = "correct"

# Arm 1 is the only arm that repeats, decided 2026-07-26. Within-config
# variance is a property of the pipeline rather than of each arm, so repeating
# every arm would multiply cost by 5 to answer a question 5 times.
REPEAT_ARM = "probes-arm1"
DEFAULT_REPEATS = 5

# Pinning every child to one BLAS thread. See the module docstring.
SINGLE_THREAD_ENV = {
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
    "TOKENIZERS_PARALLELISM": "false",
}


def reported_slugs() -> list[str]:
    """The 80 graph slugs, derived from prompts.json the same way the runner
    derives them. Kept as an independent derivation rather than an import so a
    drift between launcher and runner shows up as a missing-graph error from
    the runner instead of a silently shorter fan-out here."""
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


def work_items(arms: list[str], slugs: list[str], repeats: int) -> list[dict]:
    """One entry per (arm, slug, pass). Arm 1 carries a 1-based pass index,
    every other arm runs once with no index, which keeps the single-pass
    directory layout byte-identical to the legacy one."""
    items: list[dict] = []
    for arm in arms:
        passes = range(1, repeats + 1) if arm == REPEAT_ARM else [None]
        for pass_index in passes:
            for slug in slugs:
                items.append({"arm": arm, "slug": slug, "pass_index": pass_index})
    return items


def exp_dir_for(item: dict, output_root: Path) -> Path:
    """The experiment directory a run writes into, mirroring
    `saving.save_run_results`. The leaf below it is timestamped, so this is the
    parent that holds every attempt at one (arm, slug)."""
    return output_root / item["arm"] / "exp" / f"exp-probe-{item['slug']}-question"


def leaf_is_pass(leaf_name: str, pass_index: int | None) -> bool:
    """Does this run directory belong to the given pass?

    `exp_dir_for` deliberately has no pass in it, because `saving.py:1255` puts
    the pass in the *leaf* as a `_pass{N}` suffix and every pass of one
    (arm, slug) shares a parent. So anything selecting a specific pass has to
    filter leaves, and both `item_done` and `item_cost` must filter the same
    way or they disagree about which run they are talking about.
    """
    if pass_index is None:
        # Single-pass arm. Any completed leaf without a pass suffix counts.
        return "_pass" not in leaf_name
    return leaf_name.endswith(f"_pass{pass_index}")


def item_done(item: dict, output_root: Path) -> bool:
    """True when a completed run for this exact (arm, slug, pass) already
    exists, so a re-run after a crash resumes instead of duplicating.

    A run counts as complete only when `oracle_result.json` is present. A
    directory alone means the run was interrupted partway, and treating that as
    done would silently shrink the grid.
    """
    parent = exp_dir_for(item, output_root)
    if not parent.is_dir():
        return False
    return any(
        leaf.is_dir()
        and (leaf / "oracle_result.json").is_file()
        and leaf_is_pass(leaf.name, item["pass_index"])
        for leaf in parent.iterdir()
    )


def item_cost(item: dict, output_root: Path) -> float | None:
    """Read `total_cost_usd` back out of the newest completed leaf, so the
    pilot reports measured dollars rather than a priced estimate."""
    parent = exp_dir_for(item, output_root)
    if not parent.is_dir():
        return None
    best: tuple[float, float] | None = None
    for leaf in sorted(parent.iterdir()):
        # Pass-aware, or a 5x-repeat arm reports whichever sibling pass
        # happened to finish last. Passes of one slug run concurrently, so the
        # newest leaf is frequently NOT this item, and the pilot would then
        # price the grid off a leaf it never ran.
        if not leaf_is_pass(leaf.name, item["pass_index"]):
            continue
        result = leaf / "oracle_result.json"
        if not result.is_file():
            continue
        try:
            payload = json.loads(result.read_text())
        except json.JSONDecodeError:
            continue
        cost = payload.get("total_cost_usd")
        if cost is None:
            continue
        stamp = result.stat().st_mtime
        if best is None or stamp > best[0]:
            best = (stamp, float(cost))
    return best[1] if best else None


def arm_output_rel(item: dict, output_root: Path) -> str:
    """The `--output-dir` value for one item, which MUST include the arm.

    The runner only derives `runs/<arm>` when `--output-dir` is absent, so a
    bare `runs`
    overrides the per-arm split and drops every arm into one directory. Arms 1,
    2 and 3 share both models, so their leaves would then differ only by a
    second-resolution timestamp, which is the exact collision the per-arm
    directory exists to prevent. It also desynchronizes `exp_dir_for` below,
    which is what the resume check reads.
    """
    base = (output_root.relative_to(_TASK_ROOT)
            if output_root.is_relative_to(_TASK_ROOT) else output_root)
    return str(Path(base) / item["arm"])


def build_command(item: dict, provider: str, output_root: Path,
                  extra: list[str]) -> list[str]:
    cmd = [
        sys.executable, str(RUNNER),
        "--arm", item["arm"],
        "--slugs", item["slug"],
        "--provider", provider,
        "--output-dir", arm_output_rel(item, output_root),
        "--quiet",
    ]
    if item["pass_index"] is not None:
        cmd += ["--pass-index", str(item["pass_index"])]
    return cmd + extra


def run_item(item: dict, provider: str, output_root: Path, log_dir: Path,
             extra: list[str], timeout: int) -> dict:
    """Run one graph through one arm as its own process."""
    cmd = build_command(item, provider, output_root, extra)
    env = dict(os.environ)
    env.update(SINGLE_THREAD_ENV)
    tag = item["arm"] + "-" + item["slug"]
    if item["pass_index"] is not None:
        tag += f"-pass{item['pass_index']}"
    log_path = log_dir / f"{tag}.log"

    started = time.time()
    try:
        with log_path.open("w") as fh:
            proc = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT,
                                  cwd=str(_TASK_ROOT), env=env, timeout=timeout)
        code = proc.returncode
        note = ""
    except subprocess.TimeoutExpired:
        code = -1
        note = f"timeout after {timeout}s"
    elapsed = time.time() - started

    return {
        **item,
        "seconds": round(elapsed, 1),
        "returncode": code,
        "ok": code == 0,
        "note": note,
        "log": str(log_path),
        "cost_usd": item_cost(item, output_root) if code == 0 else None,
    }


def project_grid(ok: list[dict], grid_counts: dict[str, int]) -> tuple[float, float, list[str]]:
    """Project total seconds and dollars for the whole grid, weighted by arm.

    A flat mean over the sampled runs is wrong here and it is wrong in the
    expensive direction. Arm 1 is 400 of the 720 cells because it repeats 5x,
    and on the first pilot it was also both the slowest arm (237 s against a
    20 s one-shot) and a mid-priced one. Averaging the five arms equally and
    multiplying by 720 therefore understated wall clock by about 30 percent.
    Weight each arm's own sampled mean by how many cells that arm actually has.

    Returns (seconds, dollars, warnings). An arm with no sample contributes
    nothing, so both figures are floors and the caller is told which arms are
    missing.
    """
    per_arm: dict[str, list[dict]] = {}
    for r in ok:
        per_arm.setdefault(r["arm"], []).append(r)

    seconds = 0.0
    dollars = 0.0
    no_time, no_cost = [], []
    for arm, n in grid_counts.items():
        sample = per_arm.get(arm, [])
        if not sample:
            no_time.append(arm)
            no_cost.append(arm)
            continue
        seconds += n * sum(s["seconds"] for s in sample) / len(sample)
        priced = [s["cost_usd"] for s in sample if s["cost_usd"] is not None]
        if priced:
            dollars += n * sum(priced) / len(priced)
        else:
            no_cost.append(arm)

    warnings = []
    if no_time:
        warnings.append(f"no timing sample for {sorted(no_time)}, projection is a floor")
    if no_cost:
        warnings.append(f"no cost recorded for {sorted(no_cost)}, cost is a floor")
    return seconds, dollars, warnings


def summarize(records: list[dict], jobs: int, grid_counts: dict[str, int]) -> str:
    ok = [r for r in records if r["ok"]]
    bad = [r for r in records if not r["ok"]]
    total_cells = sum(grid_counts.values())
    lines = [f"completed {len(ok)}/{len(records)} ({len(bad)} failed)"]
    if ok:
        times = sorted(r["seconds"] for r in ok)
        lines.append(
            f"per run seconds: min {times[0]:.0f}  median {times[len(times) // 2]:.0f}  "
            f"mean {sum(times) / len(times):.0f}  max {times[-1]:.0f}"
        )
        for arm in sorted(grid_counts):
            sample = [r for r in ok if r["arm"] == arm]
            if not sample:
                continue
            secs = sum(s["seconds"] for s in sample) / len(sample)
            priced = [s["cost_usd"] for s in sample if s["cost_usd"] is not None]
            cost = f"${sum(priced) / len(priced):.4f}" if priced else "no cost"
            lines.append(f"  {arm}: {secs:.0f}s  {cost}  (n={len(sample)}, "
                         f"{grid_counts[arm]} cells in grid)")

        seconds, dollars, warns = project_grid(ok, grid_counts)
        lines.append(f"grid-weighted {total_cells}-run projection: "
                     f"{seconds / 3600:.1f} serial hours, ${dollars:.2f}")
        for w in warns:
            lines.append(f"  WARNING: {w}")
        # The number the plan turns on. Makespan for a dynamic queue is about
        # (total serial seconds / jobs), floored by the slowest single run.
        for target_min in (30, 60):
            lines.append(
                f"to finish {total_cells} runs in {target_min} min: "
                f"about {seconds / (target_min * 60):.0f} concurrent workers"
            )
        lines.append(f"floor set by the slowest single run: {times[-1] / 60:.1f} min")
    for r in bad[:10]:
        lines.append(f"  FAILED rc={r['returncode']} {r['arm']} {r['slug']} {r['note']}")
    if len(bad) > 10:
        lines.append(f"  ... and {len(bad) - 10} more failures")
    lines.append(f"jobs={jobs}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--arms", default=None,
                    help="Comma separated arm names. Default is all five probes arms.")
    ap.add_argument("--slugs", nargs="*", default=None,
                    help="Restrict to these graph slugs. Default is the reported 80.")
    ap.add_argument("--repeats", type=int, default=DEFAULT_REPEATS,
                    help=f"Passes for {REPEAT_ARM} (default {DEFAULT_REPEATS}). "
                         "Set 1 to drop the stability repeats.")
    ap.add_argument("--jobs", type=int, default=32,
                    help="Concurrent runs. This is the whole lever on wall clock.")
    # choices= is not cosmetic here: this launcher forwards --provider verbatim
    # to 720 subprocesses, so an unknown gateway would surface as 720 identical
    # failures deep in the fan-out instead of one argparse error at launch.
    ap.add_argument("--provider", default="openrouter", choices=PROVIDER_CHOICES)
    ap.add_argument("--output-dir", default="runs",
                    help="Relative to spurious-correlation/. Defaults to the "
                         "gitignored runs/, never the committed results/ or "
                         "results-workshop/ archives.")
    ap.add_argument("--log-dir", default=None,
                    help="Default <output-dir>/logs.")
    ap.add_argument("--pilot", type=int, default=0,
                    help="Run only the first N items of the plan, one per arm where "
                         "possible, to measure time and cost before committing.")
    ap.add_argument("--timeout", type=int, default=3600,
                    help="Per-run timeout in seconds.")
    ap.add_argument("--no-skip-existing", action="store_true",
                    help="Re-run items that already have a completed result.")
    ap.add_argument("--no-warmup", action="store_true",
                    help="Skip the single warm-up run. Only safe when the HF tokenizer "
                         "cache is already populated on this box.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the plan and exit without spending anything.")
    ap.add_argument("extra", nargs="*", default=[],
                    help="Extra flags forwarded verbatim to the runner.")
    args = ap.parse_args()

    arms = ([a.strip() for a in args.arms.split(",")] if args.arms
            else list(arm_names(task="probes")))
    slugs = args.slugs if args.slugs else reported_slugs()
    output_root = (_TASK_ROOT / args.output_dir).resolve()
    log_dir = Path(args.log_dir) if args.log_dir else output_root / "logs"

    items = work_items(arms, slugs, args.repeats)
    total = len(items)

    if not args.no_skip_existing:
        pending = [i for i in items if not item_done(i, output_root)]
        already = total - len(pending)
    else:
        pending = items
        already = 0

    if args.pilot:
        # One per arm first, so the pilot prices every model rather than
        # sampling the cheapest arm five times.
        by_arm: dict[str, list[dict]] = {}
        for i in pending:
            by_arm.setdefault(i["arm"], []).append(i)
        interleaved: list[dict] = []
        depth = 0
        while len(interleaved) < args.pilot and any(
                len(v) > depth for v in by_arm.values()):
            for arm in arms:
                bucket = by_arm.get(arm, [])
                if len(bucket) > depth and len(interleaved) < args.pilot:
                    interleaved.append(bucket[depth])
            depth += 1
        pending = interleaved

    print(f"arms:      {', '.join(arms)}")
    print(f"slugs:     {len(slugs)}")
    print(f"repeats:   {args.repeats} on {REPEAT_ARM}")
    print(f"grid:      {total} runs")
    detail = []
    if not args.no_skip_existing:
        detail.append(f"{already} already complete")
    else:
        detail.append("skip-existing off")
    if args.pilot:
        detail.append(f"truncated to a {args.pilot}-run pilot")
    print(f"pending:   {len(pending)} runs ({', '.join(detail)})")
    print(f"jobs:      {args.jobs}")
    print(f"output:    {output_root}")
    print(f"provider:  {args.provider}")

    if args.dry_run:
        for i in pending[:20]:
            suffix = f" pass{i['pass_index']}" if i["pass_index"] is not None else ""
            print(f"  {i['arm']}  {i['slug']}{suffix}")
        if len(pending) > 20:
            print(f"  ... and {len(pending) - 20} more")
        return 0

    if not pending:
        print("nothing to do")
        return 0

    log_dir.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    lock = threading.Lock()
    started_at = time.time()
    # Captured before the warm-up pops an item, so the progress counter counts
    # against the whole batch rather than the post-warm-up remainder.
    to_run = len(pending)

    # Warm the caches with one run before fanning out, the same gate
    # build_shards.py uses on the GPU build. The runner loads the gated
    # google/gemma-2-2b tokenizer, so N cold processes would race the same HF
    # download and its lock file. The warm-up is not wasted work, it is a real
    # item and counts toward the grid. A failure here is fatal on purpose:
    # whatever broke would otherwise break all N.
    if not args.no_warmup and len(pending) > 1 and args.jobs > 1:
        first = pending.pop(0)
        print(f"warm-up: {first['arm']}  {first['slug']}", flush=True)
        rec = run_item(first, args.provider, output_root, log_dir,
                       list(args.extra), args.timeout)
        records.append(rec)
        status = "ok" if rec["ok"] else f"FAILED rc={rec['returncode']}"
        print(f"warm-up {status} in {rec['seconds']:.0f}s", flush=True)
        if not rec["ok"]:
            print(f"aborting before fan-out, see {rec['log']}")
            return 1

    def work(item: dict) -> None:
        # Nothing may escape. list(pool.map(...)) re-raises the first exception
        # from any worker, which would discard the records of every run that
        # already succeeded, and the manifest is only written after the pool
        # drains. One unlucky OSError would cost the whole fan-out's bookkeeping.
        try:
            rec = run_item(item, args.provider, output_root, log_dir,
                           list(args.extra), args.timeout)
        except Exception as e:  # noqa: BLE001 - deliberately broad, see above
            rec = {**item, "seconds": 0.0, "returncode": -2, "ok": False,
                   "note": f"launcher error: {type(e).__name__}: {e}",
                   "log": "", "cost_usd": None}
        with lock:
            records.append(rec)
            done = len(records)
            state = "ok " if rec["ok"] else "FAIL"
            print(f"[{done}/{to_run}] {state} {rec['seconds']:6.0f}s  "
                  f"{rec['arm']}  {rec['slug']}", flush=True)

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        list(pool.map(work, pending))

    wall = time.time() - started_at
    print()
    print(f"wall clock: {wall / 60:.1f} min")
    # Weight by the FULL grid, not by what this invocation ran. A --pilot 5 is
    # sampling 5 cells to predict all 720, so the projection has to know the
    # real composition.
    grid_counts: dict[str, int] = {}
    for i in items:
        grid_counts[i["arm"]] = grid_counts.get(i["arm"], 0) + 1
    print(summarize(records, args.jobs, grid_counts))

    manifest = log_dir / "launcher_records.json"
    prior = []
    if manifest.is_file():
        try:
            prior = json.loads(manifest.read_text())
        except json.JSONDecodeError:
            prior = []
    manifest.write_text(json.dumps(prior + records, indent=1))
    print(f"records: {manifest}")

    return 1 if any(not r["ok"] for r in records) else 0


if __name__ == "__main__":
    sys.exit(main())
