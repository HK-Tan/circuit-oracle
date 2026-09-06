#!/usr/bin/env bash
# Arditi refusal-direction baseline: pipeline runner.
#
# Assumes you've already done:
#   git clone <this repository> && cd circuit-oracle/refusal-jailbreaking
#   bash scripts/setup.sh                       # venv + deps + Qwen3-4B weights + .env
#
# Then run this script from the refusal-jailbreaking/ directory:
#   bash baselines/arditi/runpod_setup.sh                                  # all slugs in data/prompts.json
#   bash baselines/arditi/runpod_setup.sh --slugs molotov-cocktail         # single slug
#   bash baselines/arditi/runpod_setup.sh --slugs molotov-cocktail mdma-manufacture
#   bash baselines/arditi/runpod_setup.sh --skip-fetch --skip-judge        # GPU-only stages
#
# Stages:
#   1. fetch-data        [LOCAL-OK]   AdvBench + Alpaca contrastive pools
#   2. extract-direction [GPU]        diff-in-mean, layer/pos sweep
#   3. apply-direction   [GPU]        baseline + ablated for every eval slug
#   4. llm-judge         [LOCAL-OK]   multi-judge continuous scoring
set -e

# Run from the project root regardless of where you invoke from.
cd "$(dirname "$0")/../.."

VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "ERROR: $VENV_DIR not found. Run 'bash scripts/setup.sh' from the" >&2
    echo "       refusal-jailbreaking/ directory first." >&2
    exit 1
fi
if [ ! -f .env ]; then
    echo "ERROR: .env not found. Run 'bash scripts/setup.sh' first." >&2
    exit 1
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
set -a
# shellcheck disable=SC1091
source .env
set +a

export HF_HOME=./weights/hf_cache
# Same allocator setting as scripts/run.sh, avoids fragmentation on long sweeps.
export PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True"

# --- args ------------------------------------------------------------------

N_TRAIN=128
N_VAL=32
SEED=42
SKIP_FETCH=0
SKIP_EXTRACT=0
SKIP_APPLY=0
SKIP_JUDGE=0
SLUGS=()  # space-separated, project convention

# Parse leading flags. Anything after `--slugs` and before the next `--flag`
# accumulates into SLUGS.
while [[ $# -gt 0 ]]; do
    case "$1" in
        --n|--n-train) N_TRAIN="$2"; shift 2 ;;
        --n-val) N_VAL="$2"; shift 2 ;;
        --seed) SEED="$2"; shift 2 ;;
        --skip-fetch) SKIP_FETCH=1; shift ;;
        --skip-extract) SKIP_EXTRACT=1; shift ;;
        --skip-apply) SKIP_APPLY=1; shift ;;
        --skip-judge) SKIP_JUDGE=1; shift ;;
        --slugs)
            shift
            while [[ $# -gt 0 && "$1" != --* ]]; do
                SLUGS+=("$1")
                shift
            done
            ;;
        -h|--help)
            grep '^#' "$0" | head -25
            exit 0
            ;;
        *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
done

# --- 1. fetch (local-OK) ---------------------------------------------------

if [ "$SKIP_FETCH" = "0" ]; then
    if [ -f baselines/arditi/data/refusal_train.json ]; then
        echo "[1/4] refusal_train.json exists, skipping fetch (delete to force re-fetch)"
    else
        echo "[1/4] fetch-data (n_train=$N_TRAIN, n_val=$N_VAL) ..."
        python -m baselines.arditi.fetch_data --seed "$SEED" \
            --n-train "$N_TRAIN" --n-val "$N_VAL"
    fi
else
    echo "[1/4] skipped (--skip-fetch)"
fi

# --- 2. extract direction (GPU) -------------------------------------------

if [ "$SKIP_EXTRACT" = "0" ]; then
    echo ""
    echo "[2/4] extract-direction ..."
    python -m baselines.arditi.extract_direction
else
    echo "[2/4] skipped (--skip-extract)"
fi

# --- 3. apply direction (GPU) ---------------------------------------------

if [ "$SKIP_APPLY" = "0" ]; then
    echo ""
    if [ ${#SLUGS[@]} -gt 0 ]; then
        echo "[3/4] apply-direction (slugs=${SLUGS[*]}) ..."
        python -m baselines.arditi.apply_direction --slugs "${SLUGS[@]}"
    else
        echo "[3/4] apply-direction (all eval slugs) ..."
        python -m baselines.arditi.apply_direction
    fi
else
    echo "[3/4] skipped (--skip-apply)"
fi

# --- 4. judge (local-OK) ---------------------------------------------------

if [ "$SKIP_JUDGE" = "0" ]; then
    echo ""
    if [ ${#SLUGS[@]} -gt 0 ]; then
        echo "[4/4] llm-judge (slugs=${SLUGS[*]}) ..."
        python -m baselines.arditi.llm_judge --slugs "${SLUGS[@]}"
    else
        echo "[4/4] llm-judge (all runs under runs/) ..."
        python -m baselines.arditi.llm_judge
    fi
else
    echo "[4/4] skipped (--skip-judge)"
fi

echo ""
echo "============================================"
echo "  Arditi baseline pipeline done."
echo "  Direction:  weights/arditi/refusal/"
echo "  Runs:       baselines/arditi/runs/"
echo "  Summary:    baselines/arditi/runs/judge_summary.md"
echo "============================================"
