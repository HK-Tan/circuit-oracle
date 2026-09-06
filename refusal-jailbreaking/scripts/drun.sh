#!/usr/bin/env bash
# drun.sh, the deterministic seed-sweep launcher.
#
# Runs the SAME environment preamble as run.sh (activate .venv, source .env if
# present, point HF_HOME at weights/hf_cache so the cached weights are reused
# instead of re-downloaded, set the CUDA allocator + torch's bundled CUDA libs)
# and then execs one of the deterministic scripts. This makes every pipeline step
# a single self-contained command, with no need to `source .venv/bin/activate`
# first and no ~60 GB re-download.
#
# It does NOT run any LLM / agent loop. It is the no-oracle path.
#
# Usage (works from any cwd, the script cd's to the repo root itself):
#   bash scripts/drun.sh build_graph.py    --slug tiananmen-massacre
#   bash scripts/drun.sh influence_seed.py --graph weights/graphs/<slug>_graph.pt --slug <slug>
#       (writes runs/seed-sweep/<slug>/seed.json by default)
#   bash scripts/drun.sh run_sweeps.py --slug <slug> --modes i
#       (the deterministic multi-stage sweep, supersedes the retired run_seed_sweep.py.
#        Writes runs/sweep-<stage>/<slug>/<datetime>/ with seed.json, anchor_sweep.json,
#        reassess.json, grades.json, and report.md. Add --dry-run for an offline,
#        stage-i selection-only preview. Stages ii/iii need OPENROUTER_API_KEY.)
set -e

# Repo root = parent of this script's directory, so relative paths resolve the
# same no matter where drun.sh is invoked from.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if [ "$#" -lt 1 ]; then
    echo "usage: bash scripts/drun.sh <script.py> [args...]" >&2
    echo "  e.g. bash scripts/drun.sh build_graph.py --slug tiananmen-massacre" >&2
    exit 2
fi

# Captured before the .env sourcing below, which runs under `set -a` and can
# itself define HF_HOME. Without this, an operator pointing the weights cache at
# a specific disk (`HF_HOME=/root/hf bash scripts/drun.sh ...`) was silently
# overridden. Precedence: caller > .env > repo-relative default, the same order
# run.sh and setup.sh use.
_CALLER_HF_HOME="${HF_HOME:-}"

if [ ! -d .venv ]; then
    echo "ERROR: .venv not found in $REPO_ROOT. Run 'bash scripts/setup.sh' first." >&2
    exit 1
fi

# 1. Project venv (the editable circuit_tracer / circuit_oracle only resolve here).
# shellcheck disable=SC1091
source .venv/bin/activate

# 2. .env if present. Stage i of run_sweeps needs no API keys, but HF_TOKEN (for
#    gated/throttled downloads) and the run_sweeps stages ii/iii (OPENROUTER_API_KEY
#    for the relevance scorer and grader) read them from here. The canonical file is
#    the repo-root one shared with the other two threads. A thread-local .env
#    still wins, for pods provisioned under the older layout.
for _envf in .env ../.env; do
    if [ -f "$_envf" ]; then
        set -a
        # shellcheck disable=SC1090
        source "$_envf"
        set +a
        break
    fi
done

# 3. Same cache + allocator env run.sh exports, so the setup-time downloads are
#    reused and big attribution buffers can return to the driver.
export HF_HOME="${_CALLER_HF_HOME:-${HF_HOME:-$REPO_ROOT/weights/hf_cache}}"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# 4. Prefer torch's bundled CUDA libs over any system ones (as run.sh does).
TORCH_LIB="$(python -c 'import os, torch; print(os.path.join(os.path.dirname(torch.__file__), "lib"))' 2>/dev/null || true)"
[ -n "$TORCH_LIB" ] && export LD_LIBRARY_PATH="$TORCH_LIB:${LD_LIBRARY_PATH:-}"

SCRIPT="$1"
shift
if [ ! -f "scripts/$SCRIPT" ]; then
    echo "ERROR: scripts/$SCRIPT not found." >&2
    exit 1
fi

exec python "scripts/$SCRIPT" "$@"
