#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Stage 3 (judge) on a CPU-only pod.
#
# The judge stage is pure API traffic. Nothing in its import path touches torch,
# transformers, or circuit_tracer, so this deliberately does NOT run the full
# scripts/setup.sh. The whole dependency set is `openai` plus the standard
# library, which installs in seconds instead of pulling a multi-GB CUDA wheel
# onto a machine with no GPU.
#
# Usage (inside tmux, after rsync):
#     read -rs KILO_API_KEY && export KILO_API_KEY
#     bash scripts/judge_pod_setup.sh
#
# Flags are forwarded to build_prompt_set.py, so a different panel or threshold
# is just:
#     bash scripts/judge_pod_setup.sh --max-judge-blocks 2
# ---------------------------------------------------------------------------
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

PROVIDER="${JUDGE_PROVIDER:-kilo}"
VENV="$REPO/.venv-judge"
LOG_DIR="$REPO/data/intermediate"
LOG="$LOG_DIR/judge_run.log"

echo "=== stage 3 (judge) on $(hostname), provider=$PROVIDER ==="

# ---------------------------------------------------------------------------
# 1. Credential, before anything slow.
#
# Checked here as well as inside build_prompt_set so the failure lands before
# the venv build rather than after it.
# ---------------------------------------------------------------------------
case "$PROVIDER" in
    kilo)       KEY_VAR="KILO_API_KEY" ;;
    openrouter) KEY_VAR="OPENROUTER_API_KEY" ;;
    *) echo "ERROR: unknown provider '$PROVIDER' (expected kilo or openrouter)" >&2; exit 1 ;;
esac

if [ -z "${!KEY_VAR:-}" ]; then
    echo "ERROR: $KEY_VAR is not set." >&2
    echo "  Set it without echoing it or writing it to history:" >&2
    echo "      read -rs $KEY_VAR && export $KEY_VAR" >&2
    exit 1
fi
echo "$KEY_VAR is set (${#KEY_VAR} char name, value not shown)"

# ---------------------------------------------------------------------------
# 2. Inputs. Stage 3 reads stage 2's output, so a missing screen file means the
#    rsync did not carry data/intermediate/ and every candidate would be lost.
# ---------------------------------------------------------------------------
SCREEN="$REPO/data/intermediate/screen_qwen3.json"
if [ ! -f "$SCREEN" ]; then
    echo "ERROR: $SCREEN not found. Stage 2 output did not make it over." >&2
    exit 1
fi
echo "screen input OK ($(wc -c < "$SCREEN") bytes)"

# ---------------------------------------------------------------------------
# 3. Python. uv if present, else fetch it.
# ---------------------------------------------------------------------------
export PATH="/root/.local/bin:$PATH"
if ! command -v uv &>/dev/null; then
    echo "installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="/root/.local/bin:$PATH"
fi

if [ ! -d "$VENV" ]; then
    # No --python pin. The pod image ships 3.12 and the package floor is 3.10, so
    # pinning would only make uv download a second interpreter for no gain.
    echo "building judge venv (openai + requests only, no torch)..."
    uv venv "$VENV"
fi
uv pip install --python "$VENV/bin/python" --quiet openai requests
echo "venv ready: $VENV"

# ---------------------------------------------------------------------------
# 4. Prove the key actually bills a chat completion.
#
# This is the load-bearing check. A 401 is non-retryable in LLMClient, so it
# raises, and grade_completion catches every Exception and reports the cell as
# FAILED rather than propagating. A dead key therefore does not crash stage 3.
# It marks all ~565 cells failed, excludes every candidate, and still writes a
# normal-looking judge_baselines.json. Unattended, that is an hour spent to
# produce an empty file. One real call up front costs a fraction of a cent.
# ---------------------------------------------------------------------------
echo "validating $KEY_VAR against $PROVIDER with one live call..."
PYTHONPATH="$REPO/../src" "$VENV/bin/python" - "$PROVIDER" <<'PY'
import sys
from circuit_oracle.llm_client import LLMClient
from circuit_oracle.judge_rubric import JUDGE_PANEL

provider = sys.argv[1]
model = JUDGE_PANEL[0][0] if isinstance(JUDGE_PANEL[0], tuple) else JUDGE_PANEL[0]
client = LLMClient(provider=provider)
# max_tokens is generous on purpose. The panel's first seat is a reasoning model,
# and a tight budget is spent entirely on the internal channel, so the reply comes
# back empty with stop_reason='max_tokens'. That still proves the key authenticated
# and billed, which is all this check needs, but an empty reply looks like a
# failure to anyone reading the log. Pay for a few more tokens and print something.
resp = client.create_message(
    model=model,
    system="Reply with the single character: k",
    messages=[{"role": "user", "content": "go"}],
    max_tokens=512,
    temperature=0.0,
)
text = "".join(getattr(b, "text", "") for b in (resp.content or []))
print(f"  live call OK via {provider} on {model}, replied {text.strip()[:20]!r}")
PY

# ---------------------------------------------------------------------------
# 5. Run it. tee so a mid-run death still leaves the per-candidate scores on
#    disk. Stage 3 accumulates records in memory and writes judge_baselines.json
#    only at the very end, so this log is the only record if the pod dies.
# ---------------------------------------------------------------------------
mkdir -p "$LOG_DIR"
echo "starting judge stage, logging to $LOG"
set +e
PYTHONUNBUFFERED=1 "$VENV/bin/python" scripts/build_prompt_set.py judge \
    --judge-provider "$PROVIDER" "$@" 2>&1 | tee "$LOG"
STATUS=${PIPESTATUS[0]}
set -e

echo ""
if [ "$STATUS" -eq 0 ]; then
    echo "=== DONE. judge_baselines.json written. ==="
else
    echo "=== FAILED (exit $STATUS). Partial scores are in $LOG ===" >&2
fi
echo "finished at $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
exit "$STATUS"
