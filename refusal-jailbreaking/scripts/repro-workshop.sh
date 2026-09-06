#!/usr/bin/env bash
# repro-workshop.sh, the agentic (orchestrator-in-the-loop) refusal path over the
# 10 slugs behind the workshop paper, i.e. data/prompts_workshop.json.
#
# Thin wrapper. It only pins the dataset and forwards everything else to
# scripts/run.sh (which activates .venv, sources .env, sets HF_HOME + the CUDA
# allocator, then execs scripts/run_all.py). Every run_all.py flag still works,
# and a flag repeated after this script's own wins, so you can override the
# dataset, orchestrator, or slug subset from the command line.
#
# Archive note: the workshop artifacts are in results-workshop/ and were produced
# by the openai/gpt-5.4 orchestrator with the openai/gpt-oss-120b subagent.
# run_all.py's orchestrator default is now openai/gpt-5.6-terra, so reproducing
# the workshop numbers needs `--orchestrator openai/gpt-5.4` passed explicitly.
# FRESH runs land in runs/exp/ (run_all.py's --out-root default, plus the "exp"
# segment save_run_results inserts) and belong to the current generation, so
# compare them with other fresh runs, not against results-workshop/ numbers. To
# grade them, `python -m baselines.arditi.exp_judge --exp-dir runs --source
# agentic`, which descends into the exp/ level automatically.
#
# One cost gotcha inherited from run_all.py. Its --max-feature-nodes default
# governs the generation of the graphs it builds, so check that value against
# the generation you intend to compare within before starting a batch. Graphs
# are now KEPT by default (--no-keep-graphs restores the old delete-on-exit),
# so a re-run of the same slug is a cache hit rather than a fresh build.
#
# Requires a GPU VM plus OPENROUTER_API_KEY and HF_TOKEN. The subject model and
# its transcoders cost 36.4 GB per copy, so an 80 GB card is the target.
#
# Usage (from anywhere, the script cd's to the repo root itself):
#   bash scripts/repro-workshop.sh                                # all 10 slugs
#   bash scripts/repro-workshop.sh --slugs tiananmen-massacre     # one slug
#   bash scripts/repro-workshop.sh --dry-run                      # resolve entries only
#   bash scripts/repro-workshop.sh --orchestrator openai/gpt-5.4  # the workshop model
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

exec bash scripts/run.sh --dataset-file data/prompts_workshop.json "$@"
