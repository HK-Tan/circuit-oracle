#!/usr/bin/env python3
"""Parallel launcher for the task-2 (taboo / ELK) arm fan-out.

Both taboo runners are sequential loops over graphs, so the 672-run phase 2
grid takes about 55 hours in one process. The runs are almost entirely blocked
on API latency rather than on CPU, so the fix is process-level concurrency.

**One process per graph, not per secret.** `--words blue` welds 6 runs into one
process, and the makespan of a fan-out is then the slowest *shard* rather than
the slowest *run*. Measured on the 240 archived results, the worst word-shard
(`open blue`) is 47.3 min of serial work while the worst single run is 15.4
min, so per-word sharding flatlines at 47.3 min no matter how many workers you
add. `taboo_shard.add_shard_args` exists to make `--words X --prompts N` name
exactly one graph, which is what this launcher fans out over.

**Two prerequisites this launcher enforces, because both fail silently.**

1. The base-density cache must be warmed once with `--prepare-only` before the
   fan-out. Otherwise every one of N processes loads all 6 base sibling graphs
   (~350 MB each, ~2.1 GB resident, held for the process lifetime) to compute
   an identical table. At 0.7 GB per run a 256 GB box holds 365 concurrent
   runs; at 2.8 GB it holds 91, which is below the ~114 the 30-minute target
   needs. The launcher warms it and refuses to fan out if it cannot.

2. The autointerp shim must be answering. Qwen3-8B is not on Neuronpedia, so
   `inspect_feature` routes through a local FastAPI shim. `inspect_feature` is
   56.8% of every tool call on this track and no archived run skipped it, but a
   dead shim does NOT crash a run: the agent gets an error back, shrugs, and
   answers from the ranking alone. That is 672 quietly degraded runs that all
   report success. So the shim is preflighted, loudly, once.

**Thread oversubscription is the trap that will actually bite.** Torch sizes
its BLAS pools to the core count, per process, with no idea siblings exist, so
114 processes on a 32-vCPU box would each start a 32-thread pool and 3648
threads would fight over 32 cores. Every child is pinned to one thread below.
The parallelism here is across runs, and each run's linear algebra (the one
real burst is `Graph.from_pt`) is a small part of its wall clock. This mirrors
`spurious-correlation/scripts/run_arms.py`. It does NOT apply to task 3, which
runs one process per pod.

Run `--dry-run` first to see the plan, then `--pilot N` to measure time and
cost on a small sample before committing the grid. Cost is read back out of
each run's `oracle_result.json`, so the pilot answers "what will this cost"
with a measurement rather than a price list.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_THREAD = _HERE.parent            # secret-elicitation/
_REPO_ROOT = _THREAD.parent       # the repository root

sys.path.insert(0, str(_REPO_ROOT / "src"))
sys.path.insert(0, str(_HERE))

from circuit_oracle.arms import arm_names  # noqa: E402
from circuit_oracle.llm_client import PROVIDER_CHOICES  # noqa: E402

import taboo_shard  # noqa: E402
from taboo_words import REPORTED_WORDS  # noqa: E402

N_PROMPTS = 6                     # len(PROMPT_PAIRS), not imported to keep torch out
RUNNERS = {
    "closed": _HERE / "run_oracle_on_taboo.py",
    "open": _HERE / "run_oracle_on_taboo_no_options.py",
}

# Arm 1 is the only arm that repeats, decided 2026-07-26. Within-config variance
# is a property of the pipeline rather than of each arm, so repeating every arm
# would multiply cost by 5 to answer one question 5 times.
REPEAT_ARM_PREFIX = "elk-arm1"
DEFAULT_REPEATS = 5

DEFAULT_AUTOINTERP_URL = os.environ.get("AUTOINTERP_BASE_URL", "http://127.0.0.1:8765")

# Pinning every child to one BLAS thread. See the module docstring.
SINGLE_THREAD_ENV = {
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
    "TOKENIZERS_PARALLELISM": "false",
}


def protocol_of(arm: str) -> str:
    """`elk-arm2-open` -> `open`. The protocol picks the runner script."""
    tail = arm.rsplit("-", 1)[-1]
    if tail not in RUNNERS:
        raise ValueError(f"cannot read a protocol off arm {arm!r} (expected a "
                         f"-closed or -open suffix)")
    return tail


def work_items(arms: list[str], words: list[str], prompts: list[int],
               repeats: int) -> list[dict]:
    """One entry per (arm, word, prompt, pass). Only arm 1 carries a pass
    index; every other arm runs once with none, which keeps its directory
    layout byte-identical to a single-pass run."""
    items: list[dict] = []
    for arm in arms:
        passes = (range(1, repeats + 1)
                  if arm.startswith(REPEAT_ARM_PREFIX) else [None])
        for pass_index in passes:
            for word in words:
                for prompt in prompts:
                    items.append({"arm": arm, "word": word, "prompt": prompt,
                                  "pass_index": pass_index})
    return items


def output_root_for(arm: str, output_dir: str) -> Path:
    return _THREAD / output_dir / arm


def exp_dir_for(item: dict, output_dir: str) -> Path:
    """The experiment directory a run writes into, mirroring the name the
    runner builds: it strips the `qwen3-8b-taboo-` prefix off the graph slug
    and `save_run_results` appends `-question` because `config.question` is
    set. So `qwen3-8b-taboo-04-blue.pt` lands in `exp-taboo-04-blue-question`.
    The leaf below this is timestamped and pass-suffixed."""
    stem = f"{item['prompt']:02d}-{item['word']}"
    return (output_root_for(item["arm"], output_dir) / "exp"
            / f"exp-taboo-{stem}-question")


def leaf_is_pass(leaf_name: str, pass_index: int | None) -> bool:
    """Does this run directory belong to the given pass?

    `exp_dir_for` has no pass in it, because `saving.py:1255` puts the pass in
    the *leaf* as a `_pass{N}` suffix and every pass of one (arm, graph) shares
    a parent. Anything selecting a specific pass must filter leaves, and
    `item_done` and `item_cost` must filter identically or they disagree about
    which run they are describing.
    """
    if pass_index is None:
        return "_pass" not in leaf_name
    return leaf_name.endswith(f"_pass{pass_index}")


def item_done(item: dict, output_dir: str) -> bool:
    """True when a completed run for this exact (arm, graph, pass) exists, so a
    re-run after a crash resumes instead of duplicating.

    A run counts as complete only when `oracle_result.json` is present. A bare
    directory means the run was interrupted partway, and treating that as done
    would silently shrink the grid."""
    parent = exp_dir_for(item, output_dir)
    if not parent.is_dir():
        return False
    return any(
        leaf.is_dir()
        and (leaf / "oracle_result.json").is_file()
        and leaf_is_pass(leaf.name, item["pass_index"])
        for leaf in parent.iterdir()
    )


def item_cost(item: dict, output_dir: str) -> float | None:
    """Read `total_cost_usd` back out of this item's newest completed leaf, so
    the pilot reports measured dollars rather than a priced estimate."""
    parent = exp_dir_for(item, output_dir)
    if not parent.is_dir():
        return None
    best: tuple[float, float] | None = None
    for leaf in sorted(parent.iterdir()):
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


def build_command(item: dict, args, density_cache: str | None) -> list[str]:
    runner = RUNNERS[protocol_of(item["arm"])]
    cmd = [
        sys.executable, str(runner),
        "--arm", item["arm"],
        "--words", item["word"],
        "--prompts", str(item["prompt"]),
        "--provider", args.provider,
        "--output-dir", f"{args.output_dir}/{item['arm']}",
        "--quiet",
    ]
    if density_cache:
        cmd += ["--base-density-cache", density_cache]
    if item["pass_index"] is not None:
        cmd += ["--pass-index", str(item["pass_index"])]
    return cmd + list(args.extra)


def run_item(item: dict, args, density_cache: str | None, log_dir: Path) -> dict:
    """Run one graph through one arm as its own process."""
    cmd = build_command(item, args, density_cache)
    env = dict(os.environ)
    env.update(SINGLE_THREAD_ENV)
    tag = f"{item['arm']}-{item['prompt']:02d}-{item['word']}"
    if item["pass_index"] is not None:
        tag += f"-pass{item['pass_index']}"
    log_path = log_dir / f"{tag}.log"

    started = time.time()
    try:
        with log_path.open("w") as fh:
            proc = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT,
                                  cwd=str(_THREAD), env=env, timeout=args.timeout)
        code, note = proc.returncode, ""
    except subprocess.TimeoutExpired:
        code, note = -1, f"timeout after {args.timeout}s"
    elapsed = time.time() - started

    return {
        **item,
        "seconds": round(elapsed, 1),
        "returncode": code,
        "ok": code == 0,
        "note": note,
        "log": str(log_path),
        "cost_usd": item_cost(item, args.output_dir) if code == 0 else None,
    }


def preflight_autointerp(url: str) -> None:
    """Fail loud if the shim is not answering.

    A dead shim does not crash a run. `inspect_feature` returns an error and
    the agent answers from the ranking alone, so the whole grid completes,
    reports success, and is quietly worse. That is the single most expensive
    silent failure available on this track, given inspect is 56.8% of tool
    calls here and no archived run skipped it.
    """
    try:
        with urllib.request.urlopen(f"{url.rstrip('/')}/healthz", timeout=10) as r:
            payload = json.loads(r.read())
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
        raise SystemExit(
            f"autointerp shim is not answering at {url} ({type(e).__name__}: {e}).\n"
            f"Start it first:\n"
            f"    AUTOINTERP_FEATURES_DIR=<...>/transcoder-features/features \\\n"
            f"    AUTOINTERP_CACHE_DIR=<a FRESH dir> \\\n"
            f"    python scripts/run_autointerp_server.py\n"
            f"Pass --no-autointerp-check only if you genuinely intend to run blind."
        ) from e
    print(f"autointerp: ok  model={payload.get('model')}  "
          f"cache={payload.get('cache_dir')}")


def warm_density_cache(args, cache_path: str) -> None:
    """Build the shared base-density table once, before anything fans out.

    Without this every process races to build the same table from the same 6
    base graphs, which is both the thundering herd and the RAM blow-up this
    cache exists to prevent."""
    if Path(cache_path).exists():
        print(f"density cache: reusing {cache_path}")
        return
    print(f"density cache: building {cache_path} (loads 6 base graphs once)...",
          flush=True)
    cmd = [sys.executable, str(RUNNERS["closed"]), "--prepare-only",
           "--base-density-cache", cache_path]
    env = dict(os.environ)
    env.update(SINGLE_THREAD_ENV)
    started = time.time()
    proc = subprocess.run(cmd, cwd=str(_THREAD), env=env)
    if proc.returncode != 0 or not Path(cache_path).exists():
        raise SystemExit(
            f"failed to build the base-density cache (rc={proc.returncode}). "
            f"Fanning out now would make every worker load all 6 base graphs, "
            f"which does not fit in RAM at the target concurrency."
        )
    print(f"density cache: built in {time.time() - started:.0f}s")


def summarize(records: list[dict], jobs: int, grid: int) -> str:
    ok = [r for r in records if r["ok"]]
    bad = [r for r in records if not r["ok"]]
    lines = [f"completed {len(ok)}/{len(records)} ({len(bad)} failed)"]
    if ok:
        times = sorted(r["seconds"] for r in ok)
        mean = sum(times) / len(times)
        lines.append(
            f"per run seconds: min {times[0]:.0f}  median {times[len(times) // 2]:.0f}  "
            f"mean {mean:.0f}  max {times[-1]:.0f}"
        )
        for proto in ("closed", "open"):
            sub = sorted(r["seconds"] for r in ok if protocol_of(r["arm"]) == proto)
            if sub:
                lines.append(f"  {proto:6s} n={len(sub):3d} mean {sum(sub) / len(sub):5.0f}s "
                             f"max {sub[-1]:5.0f}s")
        costs = [r["cost_usd"] for r in ok if r["cost_usd"] is not None]
        if costs:
            per = sum(costs) / len(costs)
            lines.append(f"per run cost: mean ${per:.4f} over {len(costs)} runs "
                         f"({grid}-run grid projects to ${per * grid:.2f})")
        else:
            lines.append("per run cost: no total_cost_usd found in any result")
        # The two floors. Adding workers only ever attacks the first one.
        for target_min in (30, 60):
            need = mean * grid / (target_min * 60)
            lines.append(f"to finish {grid} runs in {target_min} min at mean "
                         f"{mean:.0f}s: about {need:.0f} concurrent workers")
        lines.append(f"floor set by the slowest single run: {times[-1] / 60:.1f} min")
    for r in bad[:10]:
        lines.append(f"  FAILED rc={r['returncode']} {r['arm']} "
                     f"{r['prompt']:02d}-{r['word']} {r['note']}")
    if len(bad) > 10:
        lines.append(f"  ... and {len(bad) - 10} more failures")
    lines.append(f"jobs={jobs}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--arms", default=None,
                    help="Comma separated arm names. Default is all six elk arms "
                         "(3 orchestrators x closed/open).")
    ap.add_argument("--words", default="reported8",
                    help="reported8 (default, the 8 secrets behind the numbers in "
                         "results/), all20 (the full 20-word menu, which is what "
                         "the 120-run workshop-paper figure used), or a "
                         "comma-separated subset.")
    ap.add_argument("--prompts", default="all",
                    help=f"Prompt indices 1..{N_PROMPTS}, or 'all'.")
    ap.add_argument("--repeats", type=int, default=DEFAULT_REPEATS,
                    help=f"Passes for {REPEAT_ARM_PREFIX}-* (default {DEFAULT_REPEATS}). "
                         "Set 1 to drop the stability repeats.")
    ap.add_argument("--jobs", type=int, default=32,
                    help="Concurrent runs. This is the whole lever on wall clock. "
                         "About 114 hits 30 min on the 672-run grid, and needs "
                         "~80 GB of RAM at 0.7 GB per run.")
    # choices= is not cosmetic: this launcher forwards --provider verbatim to
    # hundreds of subprocesses, so an unknown gateway must die here, once.
    #
    # Kilo is a second gateway mirroring OpenRouter's vendor/model slugs, so pass
    # --provider kilo to use it instead. Either way gpt-oss-120b stays pinned to
    # OpenRouter by _DEFAULT_MODEL_PINS, so a kilo run still needs
    # OPENROUTER_API_KEY.
    ap.add_argument("--provider", default="openrouter", choices=PROVIDER_CHOICES)
    ap.add_argument("--output-dir", default="runs",
                    help="Relative to secret-elicitation/. Each arm gets a "
                         "subdirectory. Defaults to the gitignored runs/, never "
                         "the committed results/ or results-workshop/ archives.")
    ap.add_argument("--log-dir", default=None,
                    help="Default <output-dir>/logs.")
    ap.add_argument("--density-cache", default=None,
                    help="Base-density cache path. Default <GRAPH_STORE>/graphs/"
                         "base_density.json.gz. Built once before the fan-out.")
    ap.add_argument("--autointerp-url", default=DEFAULT_AUTOINTERP_URL)
    ap.add_argument("--no-autointerp-check", action="store_true",
                    help="Skip the shim preflight. Only correct if you intend to "
                         "run without feature labels.")
    ap.add_argument("--pilot", type=int, default=0,
                    help="Run only the first N items, one per arm where possible, "
                         "to measure time and cost before committing the grid.")
    ap.add_argument("--timeout", type=int, default=3600,
                    help="Per-run timeout in seconds.")
    ap.add_argument("--no-skip-existing", action="store_true",
                    help="Re-run items that already have a completed result.")
    ap.add_argument("--no-warmup", action="store_true",
                    help="Skip the single warm-up run. Only safe when the HF "
                         "tokenizer cache is already populated on this box.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the plan and exit without spending anything.")
    ap.add_argument("extra", nargs="*", default=[],
                    help="Extra flags forwarded verbatim to the runner.")
    args = ap.parse_args()

    arms = ([a.strip() for a in args.arms.split(",")] if args.arms
            else list(arm_names(task="elk")))
    known = set(arm_names(task="elk"))
    for arm in arms:
        # Fail here, not in 672 subprocesses. Both checks matter: an unknown
        # arm name and a name whose protocol suffix cannot be read pick
        # different wrong runners downstream.
        if arm not in known:
            ap.error(f"unknown elk arm {arm!r}. Known: {', '.join(sorted(known))}")
        try:
            protocol_of(arm)
        except ValueError as e:
            ap.error(str(e))

    if args.words == "reported8":
        words = list(REPORTED_WORDS)
    elif args.words == "all20":
        from taboo_words import CANDIDATE_WORDS
        words = list(CANDIDATE_WORDS)
    else:
        words = [w.strip() for w in args.words.split(",") if w.strip()]
    prompts = taboo_shard.resolve_prompts(args.prompts, N_PROMPTS)

    log_dir = (Path(args.log_dir) if args.log_dir
               else _THREAD / args.output_dir / "logs")
    density_cache = args.density_cache or str(
        Path(os.environ.get("GRAPH_STORE", str(_THREAD))) / "graphs"
        / "base_density.json.gz")

    items = work_items(arms, words, prompts, args.repeats)
    grid = len(items)

    if not args.no_skip_existing:
        pending = [i for i in items if not item_done(i, args.output_dir)]
        already = grid - len(pending)
    else:
        pending, already = items, 0

    if args.pilot:
        # One per arm first, so the pilot prices every orchestrator rather than
        # sampling the cheapest arm N times.
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
    print(f"words:     {len(words)}  prompts: {prompts}")
    print(f"repeats:   {args.repeats} on {REPEAT_ARM_PREFIX}-*")
    print(f"grid:      {grid} runs")
    detail = [f"{already} already complete"] if not args.no_skip_existing else \
             ["skip-existing off"]
    if args.pilot:
        detail.append(f"truncated to a {args.pilot}-run pilot")
    print(f"pending:   {len(pending)} runs ({', '.join(detail)})")
    print(f"jobs:      {args.jobs}")
    print(f"output:    {_THREAD / args.output_dir}")
    print(f"provider:  {args.provider}")
    print(f"density:   {density_cache}")

    if args.dry_run:
        for i in pending[:20]:
            suffix = f" pass{i['pass_index']}" if i["pass_index"] is not None else ""
            print(f"  {i['arm']}  {i['prompt']:02d}-{i['word']}{suffix}")
        if len(pending) > 20:
            print(f"  ... and {len(pending) - 20} more")
        return 0

    if not pending:
        print("nothing to do")
        return 0

    if not args.no_autointerp_check:
        preflight_autointerp(args.autointerp_url)
    warm_density_cache(args, density_cache)

    log_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    lock = threading.Lock()
    started_at = time.time()
    to_run = len(pending)

    # Warm the caches with one real run before fanning out. Every process calls
    # AutoTokenizer.from_pretrained("Qwen/Qwen3-8B"), so N cold processes would
    # race the same HF download and its lock file. It is not wasted work, it is
    # a real item and counts toward the grid. A failure here is fatal on
    # purpose: whatever broke would otherwise break all N.
    if not args.no_warmup and len(pending) > 1 and args.jobs > 1:
        first = pending.pop(0)
        print(f"warm-up: {first['arm']}  {first['prompt']:02d}-{first['word']}",
              flush=True)
        rec = run_item(first, args, density_cache, log_dir)
        records.append(rec)
        status = "ok" if rec["ok"] else f"FAILED rc={rec['returncode']}"
        print(f"warm-up {status} in {rec['seconds']:.0f}s", flush=True)
        if not rec["ok"]:
            print(f"aborting before fan-out, see {rec['log']}")
            return 1

    def work(item: dict) -> None:
        # Nothing may escape. list(pool.map(...)) re-raises the first worker
        # exception, which would discard the records of every run that already
        # succeeded, and the manifest is written only after the pool drains.
        try:
            rec = run_item(item, args, density_cache, log_dir)
        except Exception as e:  # noqa: BLE001 - deliberately broad, see above
            rec = {**item, "seconds": 0.0, "returncode": -2, "ok": False,
                   "note": f"launcher error: {type(e).__name__}: {e}",
                   "log": "", "cost_usd": None}
        with lock:
            records.append(rec)
            state = "ok " if rec["ok"] else "FAIL"
            print(f"[{len(records)}/{to_run}] {state} {rec['seconds']:6.0f}s  "
                  f"{rec['arm']}  {rec['prompt']:02d}-{rec['word']}", flush=True)

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        list(pool.map(work, pending))

    print()
    print(f"wall clock: {(time.time() - started_at) / 60:.1f} min")
    print(summarize(records, args.jobs, grid))

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
    raise SystemExit(main())
