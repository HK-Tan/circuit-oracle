#!/usr/bin/env python3
"""
Run circuit_extraction.py on every prompt listed in prompts.json for a given
dataset, both subgroups, one invocation per prompt. Each invocation writes a
biased and an unbiased .pt, so the 40 prompts in the manifest produce the 80
graphs run_oracle_on_probes.reported_slugs() expects.

Usage:
    python spurious-correlation/scripts/run_extraction_batch.py --dataset bib_nurse_professor
    python spurious-correlation/scripts/run_extraction_batch.py --dataset bib_journalist_dietitian --skip-existing
    python spurious-correlation/scripts/run_extraction_batch.py --dataset civil_comments --tags neg_neg_1 pos_pos_2
    python spurious-correlation/scripts/run_extraction_batch.py --verify-store   # no GPU, checks all 80

Each run appends stdout/stderr to spurious-correlation/runs/build_logs/
<dataset>.log.<n>, where <n> is the next available integer. runs/ is
gitignored, so a build never writes into the committed result archives.
"""
import json
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

import dotenv

# This file lives in spurious-correlation/scripts/, next to circuit_extraction.py.
# The task root (which holds prompts.json and the default graph store) is one level up.
SCRIPT_DIR = Path(__file__).resolve().parent
TASK_ROOT = SCRIPT_DIR.parent
REPO_ROOT = TASK_ROOT.parent
# ANALYSIS_MD = TASK_ROOT / "probe_artifacts" / "spuriosity" / "analysis_2.md"
# Analysis 1[:5]+3+2
DATASET_JSON = TASK_ROOT / "prompts.json"
EXTRACTION_SCRIPT = SCRIPT_DIR / "circuit_extraction.py"

# Load the repo-root .env BEFORE resolving GRAPH_STORE. The child
# circuit_extraction.py does the same and then writes to
# $GRAPH_STORE/probe_circuits, so a GRAPH_STORE that lives only in .env and not
# in the exported environment would put the child's writes somewhere this parent
# never looks: --skip-existing would rebuild everything and the completeness
# check below would report all 80 graphs missing on a build that actually
# succeeded. Absent .env is fine when the variables are already exported.
dotenv.load_dotenv(REPO_ROOT / ".env")

# Must match the graph store circuit_extraction.py writes to, otherwise
# --skip-existing would look in the wrong place and rebuild everything.
PROBE_CIRCUITS_DIR = Path(os.environ.get("GRAPH_STORE", str(TASK_ROOT))) / "probe_circuits"

# Build logs go under the task's gitignored runs/ directory, not next to the
# graphs. The graph store is often a network-volume mount, and the logs are
# small text files that belong with the other throwaway run output.
LOGS_DIR = TASK_ROOT / "runs" / "build_logs"

VALID_DATASETS = [
    "bib_nurse_professor",
    "bib_journalist_dietitian",
    "bib_surgeon_teacher",
    "civil_comments",
    "multinli",
]


# ---------------------------------------------------------------------------
# analysis.md parser
# ---------------------------------------------------------------------------

def parse_dataset_prompts(dataset: str) -> dict[str, list[str]]:
    """
    Read the prompt manifest (prompts.json) and return
    {'neg_neg': [...prompts...], 'pos_pos': [...prompts...]}
    for the given dataset.

    neg_neg = subgroup with (target=0, spurious=0)
    pos_pos = subgroup with (target=1, spurious=1)
    """
    prompt_dataset = json.load(open(DATASET_JSON, "r"))
    result = prompt_dataset[dataset]
    return result
    # Load existing data from JSON if it exists
    # existing: dict[str, dict[str, list[str]]] = {}
    # if DATASET_JSON.exists():
    #     with open(DATASET_JSON, 'r') as f:
    #         existing = json.load(f)

    # text = ANALYSIS_MD.read_text()
    # lines = text.split('\n')

    # result: dict[str, list[str]] = {'neg_neg': [], 'pos_pos': []}
    # in_dataset = False
    # current_key: str | None = None
    # in_top_prompts = False
    # in_quoted = False
    # current_prompt_lines: list[str] = []

    # for line in lines:

    #     # ── Dataset section header (## dataset) ────────────────────────────
    #     if line.startswith('## '):
    #         in_dataset = (line[3:].strip() == dataset)
    #         current_key = None
    #         in_top_prompts = False
    #         in_quoted = False
    #         current_prompt_lines = []
    #         continue

    #     if not in_dataset:
    #         continue

    #     # ── Subgroup header (### ...) ───────────────────────────────────────
    #     if line.startswith('### '):
    #         m = re.search(r'\(target=(\d+), spurious=(\d+)\)', line)
    #         if m:
    #             tv, sv = int(m.group(1)), int(m.group(2))
    #             current_key = {(0, 0): 'neg_neg', (1, 1): 'pos_pos'}.get((tv, sv))
    #         else:
    #             current_key = None
    #         in_top_prompts = False
    #         in_quoted = False
    #         current_prompt_lines = []
    #         continue

    #     # ── Top prompts subsection (#### Top N prompts …) ──────────────────
    #     if line.startswith('#### Top ') and 'prompts' in line:
    #         in_top_prompts = True
    #         in_quoted = False
    #         current_prompt_lines = []
    #         continue

    #     # Stop at the next section header of any level
    #     if line.startswith('###') or line.startswith('##'):
    #         in_top_prompts = False
    #         continue

    #     if not in_top_prompts or current_key is None:
    #         continue

    #     # ── Inside a Top-N prompts block ────────────────────────────────────
    #     stripped = line.strip()

    #     if in_quoted:
    #         # Continuing a multi-line quoted prompt
    #         current_prompt_lines.append(line)
    #         if stripped.endswith('"'):
    #             full = '\n'.join(current_prompt_lines).strip()
    #             if full.startswith('"') and full.endswith('"'):
    #                 full = full[1:-1]
    #             result[current_key].append(full)
    #             current_prompt_lines = []
    #             in_quoted = False
    #     else:
    #         if stripped.startswith('"'):
    #             if stripped.endswith('"') and len(stripped) > 1:
    #                 # Single-line quoted prompt
    #                 result[current_key].append(stripped[1:-1])
    #             else:
    #                 # Start of a multi-line prompt
    #                 in_quoted = True
    #                 current_prompt_lines = [stripped]
    # # Merge with existing data, deduplicating prompts
    # if dataset in existing:
    #     for key in ('neg_neg', 'pos_pos'):
    #         existing_prompts = existing[dataset].get(key, [])
    #         seen = set(existing_prompts)
    #         merged = list(existing_prompts)
    #         for prompt in result[key]:
    #             if prompt not in seen:
    #                 merged.append(prompt)
    #                 seen.add(prompt)
    #         result[key] = merged

    # # Write back
    # existing[dataset] = result
    # with open(DATASET_JSON, 'w') as f:
    #     json.dump(existing, f, indent=2)

    # return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def next_log_number(dataset: str) -> int:
    """Return the next unused log number for the given dataset."""
    existing = list(LOGS_DIR.glob(f"{dataset}.log.*"))
    nums: list[int] = []
    for p in existing:
        try:
            nums.append(int(p.name.rsplit('.', 1)[-1]))
        except ValueError:
            pass
    return (max(nums) + 1) if nums else 1


def claim_log_path(dataset: str, start: int) -> tuple[Path, int]:
    """Atomically claim an unused log path, returning it and the number used.

    Scanning for a free number and then opening it is a race, and build_shards.py
    makes that race reachable: a balanced shard split puts prompts from the same
    dataset on different GPUs, so several processes create
    `<dataset>.log.<n>` concurrently and two of them can settle on the same n,
    with the later `open(..., 'w')` truncating the earlier one's log. Creating
    with 'x' and retrying makes the claim atomic. Only the log file is affected,
    never a .pt, but a build log that silently loses half its prompts is exactly
    what you need when something goes wrong at 3am on a rented card.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    n = max(start, next_log_number(dataset))
    while True:
        path = LOGS_DIR / f"{dataset}.log.{n}"
        try:
            path.touch(exist_ok=False)
        except FileExistsError:
            n += 1
            continue
        return path, n


# The reported task-1 store: 40 prompts in prompts.json, each built against the
# biased and the unbiased probe. The verifier derives its file list from the
# manifest and then requires the derivation to land exactly here, so a
# truncated or edited manifest fails loudly instead of quietly lowering the
# bar (the debug-slice bug shipped 20 graphs while everyone believed 80).
EXPECTED_TOTAL_GRAPHS = 80


def expected_graph_files(dataset: str, tag: str, circuits_dir: Path | None = None) -> list[Path]:
    """The two .pt paths one (dataset, tag) pair must produce."""
    base = PROBE_CIRCUITS_DIR if circuits_dir is None else circuits_dir
    return [
        base / f"{dataset}-{tag}-{probe}-probe-correct.pt"
        for probe in ("biased", "unbiased")
    ]


def output_exists(dataset: str, tag: str) -> bool:
    """True if both biased and unbiased correct .pt files already exist.

    Existence plus non-empty, not integrity. `Graph.to_pt` is a direct
    `torch.save` with no temp-file-then-rename, so an interrupted write can
    leave a truncated `.pt` that passes this check. The zero-byte case is the
    common one and is caught here; a partial-but-nonzero file is not. Making
    the child's write atomic is the real fix and is out of scope for this
    script.
    """
    return all(
        p.is_file() and p.stat().st_size > 0
        for p in expected_graph_files(dataset, tag)
    )


def verify_store(circuits_dir: Path | None = None) -> tuple[int, list[Path]]:
    """Walk the full manifest across every dataset and check the 80-graph store.

    Returns ``(n_expected, missing)`` where ``missing`` lists every expected
    .pt that is absent or zero bytes. Raises if the manifest does not derive
    exactly EXPECTED_TOTAL_GRAPHS, because a shrunken manifest passing its own
    shrunken bar is the failure mode this verifier exists to close.
    """
    expected: list[Path] = []
    for dataset in VALID_DATASETS:
        prompts = parse_dataset_prompts(dataset)
        for tag, _prompt in build_runs(prompts):
            expected.extend(expected_graph_files(dataset, tag, circuits_dir))
    if len(set(expected)) != len(expected):
        # Not reachable from a well-formed manifest (JSON keys are unique and
        # tags are enumerate-derived), so this is a guard on the guard: without
        # it, "80 expected" could in principle be 80 references to fewer than
        # 80 distinct files, and the count would certify a store that is not
        # complete.
        duplicates = sorted({p.name for p in expected if expected.count(p) > 1})
        raise AssertionError(
            f"the expected-graph list contains duplicate paths ({duplicates[:5]}), "
            f"so the count does not certify distinct graphs. Check VALID_DATASETS "
            f"and prompts.json for repeated entries."
        )
    if len(expected) != EXPECTED_TOTAL_GRAPHS:
        raise AssertionError(
            f"prompts.json derives {len(expected)} graphs, not the reported "
            f"{EXPECTED_TOTAL_GRAPHS}. The manifest changed. Reconcile before "
            f"building anything."
        )
    missing = [p for p in expected if not (p.is_file() and p.stat().st_size > 0)]
    return len(expected), missing


def build_runs(prompts: dict[str, list[str]]) -> list[tuple[str, str]]:
    """Every (tag, prompt) pair for one dataset, in run order.

    Tags are **1-based over the full per-subgroup list**, because that is what
    `run_oracle_on_probes.reported_slugs()` derives the canonical 80-slug set
    from, and the tag becomes part of the output `.pt` filename.

    The slice and the offset are coupled. An earlier revision sliced
    `pos_pos[5:10]` and enumerated from 6, which was internally *consistent*
    (it labeled `prompts[5]` as `pos_pos_6`, correctly) but built only 20 of the
    80 graphs. Widening one without the other would relabel every prompt by the
    offset under a filename that still looks valid, which is silent corruption
    rather than a loud shortfall. Change both or neither.

    No per-dataset branching is needed or wanted. BiasInBios carries 5 in each
    cell, CivilComments and MultiNLI carry 10 in `pos_pos` and none in
    `neg_neg` (their `neg_neg` cell has no spurious signal to lean on, see
    `spurious_probes.tex`), and `bib_surgeon_teacher` carries none at all
    (dropped after probe-quality screening). An empty cell is zero iterations.
    """
    runs: list[tuple[str, str]] = []
    for subgroup in ("pos_pos", "neg_neg"):
        for i, prompt in enumerate(prompts[subgroup], 1):
            runs.append((f"{subgroup}_{i}", prompt))
    return runs


# ---------------------------------------------------------------------------
# Per-prompt extraction runner
# ---------------------------------------------------------------------------

def run_extraction(
    dataset: str,
    prompt_tag: str,
    prompt: str,
    log_path: Path,
    skip_neuronpedia: bool = False,
) -> int:
    """
    Invoke circuit_extraction.py for one (dataset, prompt_tag, prompt) triple.
    Streams combined stdout+stderr to the console and appends to log_path.
    Returns the subprocess exit code.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with open(log_path, 'w') as log_f:
        log_f.write(f"# Dataset:    {dataset}\n")
        log_f.write(f"# Tag:        {prompt_tag}\n")
        short = prompt[:120] + ('…' if len(prompt) > 120 else '')
        log_f.write(f"# Prompt:     {short}\n")
        log_f.write("=" * 60 + "\n\n")
        log_f.flush()

        cmd = [
            sys.executable, str(EXTRACTION_SCRIPT),
            "--dataset",    dataset,
            "--prompt-tag", prompt_tag,
            "--prompt",     prompt,
        ]
        if skip_neuronpedia:
            cmd.append("--skip-neuronpedia")

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=str(TASK_ROOT),
        )
        for line in proc.stdout:
            sys.stdout.write(line)
            log_f.write(line)
        proc.wait()

    return proc.returncode


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch circuit extraction on the neg_neg / pos_pos prompts in prompts.json",
    )
    parser.add_argument(
        '--dataset', choices=VALID_DATASETS,
        help="Dataset slug to process (required unless --verify-store)",
    )
    parser.add_argument(
        '--skip-existing', action='store_true',
        help="Skip runs where output .pt files already exist in probe_circuits/",
    )
    parser.add_argument(
        '--tags', nargs='+', metavar='TAG',
        help="Only run specific tags, e.g. --tags neg_neg_1 pos_pos_3",
    )
    parser.add_argument(
        '--verify-store', action='store_true',
        help="No build. Walk the full manifest across every dataset and fail "
             "unless all 80 reported graphs are present and non-empty. Run "
             "this before tearing the GPU down.",
    )
    parser.add_argument(
        '--skip-neuronpedia', action='store_true',
        help="Forwarded to circuit_extraction.py. Skips the stdout-only "
             "per-feature explanation fetch, which is tens of minutes of paid "
             "GPU time spent on HTTP across a full build. Graphs are identical "
             "either way.",
    )
    args = parser.parse_args()

    if args.verify_store:
        if args.dataset or args.tags:
            parser.error("--verify-store checks the whole store; it takes no "
                         "--dataset or --tags")
        n_expected, missing = verify_store()
        if missing:
            print(f"STORE INCOMPLETE: {len(missing)} of {n_expected} graph(s) "
                  f"missing or empty under {PROBE_CIRCUITS_DIR}:", flush=True)
            for p in missing:
                print(f"  {p.name}", flush=True)
            sys.exit(1)
        print(f"STORE OK: all {n_expected} graphs present and non-empty under "
              f"{PROBE_CIRCUITS_DIR}.", flush=True)
        return

    if not args.dataset:
        parser.error("--dataset is required unless --verify-store is given")

    # ── Parse prompts ────────────────────────────────────────────────────────
    print(f"Reading prompts.json for dataset: {args.dataset}", flush=True)
    prompts = parse_dataset_prompts(args.dataset)

    pos_pos = prompts['pos_pos']
    neg_neg = prompts['neg_neg']
    print(f"  pos_pos prompts found: {len(pos_pos)}", flush=True)
    print(f"  neg_neg prompts found: {len(neg_neg)}", flush=True)
    print(f"  graphs expected: {2 * (len(pos_pos) + len(neg_neg))} "
          f"(biased + unbiased per prompt)", flush=True)

    if not neg_neg and not pos_pos:
        # Not an error. bib_surgeon_teacher is deliberately empty (it Fails
        # probe-quality screening, spurious_probes_appendix.tex) and stays in
        # VALID_DATASETS so a loop over all five is legal. --dataset is
        # constrained by `choices`, so a typo cannot reach here.
        print(
            f"'{args.dataset}' has no prompts in the manifest, so it contributes 0 "
            "graphs. That is the intended state for a dataset dropped after "
            "probe-quality screening. Nothing to do.",
            flush=True,
        )
        return

    # ── Build run list ───────────────────────────────────────────────────────
    all_runs = build_runs(prompts)
    runs = list(all_runs)

    if args.tags:
        known = {tag for tag, _ in all_runs}
        unknown = sorted(set(args.tags) - known)
        if unknown:
            # Previously these were silently dropped by the filter, so a typo
            # produced an empty run list and a "completed successfully" exit 0.
            print(
                f"ERROR: --tags {unknown} do not exist for '{args.dataset}'. "
                f"Known tags: {sorted(known)}",
                flush=True,
            )
            sys.exit(1)
        allowed = set(args.tags)
        runs = [(tag, p) for tag, p in runs if tag in allowed]
        print(f"Filtered to {len(runs)} run(s) by --tags", flush=True)

    # ── Run ──────────────────────────────────────────────────────────────────
    print(f"\nStarting {len(runs)} extraction(s) for '{args.dataset}':\n", flush=True)

    log_num = next_log_number(args.dataset)
    errors: list[str] = []

    for tag, prompt in runs:
        short = prompt[:80].replace('\n', ' ') + ('…' if len(prompt) > 80 else '')
        print(f"[{tag}] prompt: {short!r}", flush=True)

        if args.skip_existing and output_exists(args.dataset, tag):
            print(f"  → skipping (output {args.dataset}-{tag}*.pt files already exist)\n", flush=True)
            continue

        # Claimed atomically, since concurrent shards on the same dataset would
        # otherwise race for the same number and truncate each other's log.
        log_path, log_num = claim_log_path(args.dataset, log_num)
        # Absolute, since GRAPH_STORE can put the log outside TASK_ROOT.
        print(f"  → log: {log_path}", flush=True)

        rc = run_extraction(args.dataset, tag, prompt, log_path,
                            skip_neuronpedia=args.skip_neuronpedia)
        log_num += 1

        if rc != 0:
            print(f"  → FAILED (exit code {rc})\n", flush=True)
            errors.append(tag)
        else:
            print(f"  → OK\n", flush=True)

    # ── Verify ───────────────────────────────────────────────────────────────
    # Every tag this invocation was responsible for must have left 2 .pt files
    # (biased + unbiased). Under --tags that is the selected subset, otherwise
    # it is the whole manifest, so the *scope* narrows with --tags but the check
    # never switches off. A child can exit 0 without writing both files, and
    # --skip-existing can hide a half-built pair, so a nonzero return code is
    # not sufficient evidence on its own.
    #
    # This exists because the debug-slice bug was silent at build time: it
    # printed "pos_pos prompts found: 0", exited 0, and the 60 missing graphs
    # only surfaced much later in run_oracle_on_probes.py's reported-set check,
    # after the GPU had been paid for and torn down.
    expected = [tag for tag, _ in runs]
    n_expected = 2 * len(expected)
    scope = f"the {len(expected)} selected tag(s)" if args.tags else "the full manifest"
    print(f"\nVerifying {n_expected} graph(s) for '{args.dataset}' ({scope})...", flush=True)
    missing = [tag for tag in expected if not output_exists(args.dataset, tag)]
    if missing:
        print(
            f"ERROR: {len(missing)} of {len(expected)} prompt(s) are missing, empty, or "
            f"have only one of the two .pt files under {PROBE_CIRCUITS_DIR}: {missing}",
            flush=True,
        )
        errors.extend(tag for tag in missing if tag not in errors)
    else:
        print(f"OK: all {n_expected} .pt file(s) present and non-empty.", flush=True)

    # The completeness claim ("all 80") is only meaningful on an unfiltered run.
    if not args.tags and len(all_runs) != len(runs):  # pragma: no cover - defensive
        raise AssertionError("unfiltered run must verify every tag")

    # ── Summary ──────────────────────────────────────────────────────────────
    if errors:
        print(f"Finished with errors in tags: {errors}", flush=True)
        sys.exit(1)
    else:
        print("All extractions completed successfully.", flush=True)


if __name__ == '__main__':
    # prompt_data = {}
    # for dataset in VALID_DATASETS:
    #     print(f"Parsing analysis.md for dataset: {dataset}", flush=True)
    #     prompts = parse_dataset_prompts(dataset)
    #     prompt_data[dataset] = prompts
    #     prompts['pos_pos']=prompts['pos_pos']
    #     prompts['neg_neg']=prompts['neg_neg']
    #     print(f"  pos_pos prompts found: {len(prompts['pos_pos'])}", flush=True)
    #     print(f"  neg_neg prompts found: {len(prompts['neg_neg'])}", flush=True)

    # with open(DATASET_JSON, 'w') as f:
    #     json.dump(prompt_data, f, indent=4)
    # print(f"Wrote {DATASET_JSON}")

    
    main()
