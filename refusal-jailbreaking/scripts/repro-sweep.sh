#!/usr/bin/env bash
# repro-sweep.sh, the deterministic influence-sweep refusal path (no agent loop)
# over the 50-prompt set, i.e. data/prompts.json.
#
# Thin wrapper. It pins the dataset, the working stage matrix, and --build, then
# forwards everything else to scripts/drun.sh run_sweeps.py (which activates
# .venv, sources .env, sets HF_HOME + the CUDA allocator, then execs
# scripts/run_sweeps.py). Every run_sweeps.py flag still works, and a flag
# repeated after this script's own wins, so --modes / --grader-repeats /
# --dry-run can all be overridden from the command line.
#
# Slug selection is the one flag that cannot simply be repeated, because
# resolve_slugs() lets --all win over --slug. So --all is added only when the
# caller named no slug selector of their own. Pass --slug / --slugs to run a
# subset, pass nothing to run all 50.
#
# Why the other pins: i ii-b iii-b iv-b is the working matrix (running the four
# stages in ONE invocation shares the decode, reassess, and grading passes, so
# four stages cost about as much as one). --build computes a missing graph .pt
# inside the same model load and is a no-op when the .pt is already cached, so
# one command covers both a fresh VM and a warm one.
#
# Requires a GPU VM plus HF_TOKEN, and OPENROUTER_API_KEY for the ii/iii
# relevance scorer and for grading (every stage grades).
#
# Generation note: --build bakes --max-feature-nodes into any graph it creates.
# All three builders (run_sweeps.py, run_all.py, build_graph.py) now default to
# 8192. Earlier sweeps were built at 10000, so a fresh batch is not directly
# comparable to those numbers unless you pass --max-feature-nodes 10000.
#
# Output note: fresh runs land in runs/sweep-<stage>/<slug>/<datetime>/
# (run_sweeps.py --out-root default, gitignored), so a replication never writes
# into the committed results/ or results-workshop/ archives. Score a fresh batch
# with `python -m baselines.arditi.exp_judge --exp-dir runs`.
#
# Usage (from anywhere, the script cd's to the repo root itself):
#   bash scripts/repro-sweep.sh                             # all 50 prompts, 4 stages
#   bash scripts/repro-sweep.sh --slug tiananmen-massacre   # one slug
#   bash scripts/repro-sweep.sh --modes i --dry-run         # offline selection preview
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SLUG_SELECTOR="--all"
for arg in "$@"; do
    case "$arg" in
        --slug|--slugs|--all) SLUG_SELECTOR=""; break ;;
    esac
done

exec bash scripts/drun.sh run_sweeps.py \
    --dataset-file data/prompts.json \
    ${SLUG_SELECTOR} \
    --modes i ii-b iii-b iv-b \
    --grader-repeats 3 \
    --build \
    "$@"
