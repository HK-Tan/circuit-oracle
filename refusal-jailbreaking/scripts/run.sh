#!/usr/bin/env bash
# Suppression-jailbreak experiments via the Circuit Oracle.
#
# Reads single-prompt entries from data/prompts.json and runs the Circuit
# Oracle with a single canonical orchestrator (run_all.py's DEFAULT_ORCHESTRATOR,
# currently openai/gpt-5.6-terra). Prefer --arm, which pins the orchestrator, the
# subagent and the tool surface together.
#
# Usage:
#   bash scripts/run.sh                                       # all entries
#   bash scripts/run.sh --slugs chlorine-gas-household-cleaners  # single slug
#   bash scripts/run.sh --arm refusal-arm1                    # a grid arm
#   bash scripts/run.sh --orchestrator openai/gpt-5.6-terra
#   bash scripts/run.sh --control-runs 3
#   bash scripts/run.sh --self-rating-samples 0               # disable subject self-rating
#   bash scripts/run.sh --dry-run                             # smoke-test entry resolution
set -e

# Captured before `source "$ENV_FILE"` below, which runs under `set -a` and can
# itself define HF_HOME. Without this, an operator pointing the weights cache at
# a specific disk (`HF_HOME=/root/hf bash scripts/run.sh`) was silently overridden
# and 64 GB landed somewhere else. Precedence: caller > .env > repo-relative default.
_CALLER_HF_HOME="${HF_HOME:-}"

VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
  echo "Error: Virtual environment not found. Run 'bash setup.sh' first."
  exit 1
fi

# Canonical .env is the repo-root one, shared with spurious-correlation/ and
# secret-elicitation/. A thread-local refusal-jailbreaking/.env still wins, for
# pods provisioned under the older layout.
if [ -f .env ]; then
  ENV_FILE=".env"
elif [ -f ../.env ]; then
  ENV_FILE="../.env"
else
  echo "Error: no .env found at ./.env or ../.env. Run 'bash scripts/setup.sh' first."
  exit 1
fi

# Activate venv
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

_RUN_THREAD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export HF_HOME="${_CALLER_HF_HOME:-${HF_HOME:-$_RUN_THREAD_DIR/weights/hf_cache}}"
echo "HF_HOME=$HF_HOME"

# Use expandable virtual segments instead of fixed-size cudaMalloc slabs.
# Phase 3 of attribute() retains a 30+ GB forward graph, then asks for ~49 GB
# of backward buffers in one shot; with the default allocator the cached
# blocks pinned behind live tensors can't be returned to the driver, so the
# request fails even when total free + cached > 49 GB.
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Ensure PyTorch uses its own bundled CUDA libs instead of system CUDA libs
export LD_LIBRARY_PATH=$(python -c "import torch; print(torch.__path__[0])")/lib:${LD_LIBRARY_PATH:-}

# Unbuffered stdout. Python block-buffers when stdout is a pipe or a log file, so
# every print() in run_all.py / the orchestrator was invisible for the life of the
# run and only tqdm (stderr) showed. That is what made the 2026-07-28 hang
# undiagnosable in real time, and across a sharded fan-out it makes per-shard
# progress unreadable.
export PYTHONUNBUFFERED=1

python scripts/run_all.py "$@"
