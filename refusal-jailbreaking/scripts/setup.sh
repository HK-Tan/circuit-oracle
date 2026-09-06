#!/usr/bin/env bash
set -e

# ---------------------------------------------------------------------------
# Circuit Oracle setup
#
# INTERACTIVE. Step 4 prompts for API keys with `read -p`, so run this from a
# real terminal. With stdin redirected (`bash scripts/setup.sh </dev/null`) the
# read returns non-zero and `set -e` kills the script mid-setup.
# ---------------------------------------------------------------------------
echo ""
echo "============================================"
echo "  Circuit Oracle setup"
echo "============================================"
echo ""

VENV_DIR=".venv"

# Captured before anything sources .env. Sourcing assigns into this shell, so a
# caller's exported HF_HOME would otherwise be overwritten by a value in .env
# and the precedence would invert. A pod launcher that exports HF_HOME to point
# the cache at a network volume expects its own value to win.
_CALLER_HF_HOME="${HF_HOME:-}"

# One .env for the whole release. There is a single package at the repo root, and
# spurious-correlation/ and secret-elicitation/ both read the repo-root .env, so
# this thread writes and reads that same file. A thread-local
# refusal-jailbreaking/.env still wins on a VM provisioned under the older
# layout, so re-running setup there does not strand its keys.
if [ -f ".env" ]; then
    ENV_FILE=".env"
else
    ENV_FILE="../.env"
fi

export PATH="$HOME/.local/bin:$PATH"

# ---------------------------------------------------------------------------
# 0. Install tmux (so long runs survive SSH disconnects)
# ---------------------------------------------------------------------------
if ! command -v tmux &>/dev/null; then
    echo "Installing tmux..."
    if command -v apt-get &>/dev/null; then
        apt-get update -qq && apt-get install -y -qq tmux
    elif command -v yum &>/dev/null; then
        yum install -y tmux
    elif command -v brew &>/dev/null; then
        brew install tmux
    else
        echo "WARN: no known package manager (apt/yum/brew) found; skipping tmux install." >&2
    fi
fi

if command -v tmux &>/dev/null; then
    echo "tmux $(tmux -V | awk '{print $2}') detected, OK"
fi

# ---------------------------------------------------------------------------
# 1. Install uv (fast Python package installer)
# ---------------------------------------------------------------------------
if ! command -v uv &>/dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "uv $(uv --version) detected, OK"
echo ""

# ---------------------------------------------------------------------------
# 2. Create virtual environment (isolates from system packages)
# ---------------------------------------------------------------------------
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    uv venv "$VENV_DIR" --python 3.12
fi

# Activate the venv for the rest of this script
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
echo "Virtual environment active: $(which python)"
echo ""

# ---------------------------------------------------------------------------
# 3. Install the package
# ---------------------------------------------------------------------------
echo "Installing PyTorch CUDA 12.8 stack..."
uv pip install \
    torch==2.7.1+cu128 \
    torchvision==0.22.1+cu128 \
    torchaudio==2.7.1+cu128 \
    --index-url https://download.pytorch.org/whl/cu128
echo ""

# The oracle package now lives at the repo root (src/circuit_oracle and
# src/circuit_tracer serve all three threads), so install it from one level up,
# not from this folder. Bare "torch" in its dependencies is already satisfied by
# the CUDA wheel above, so this step does not reinstall torch.
ORACLE_PKG_DIR="${ORACLE_PKG_DIR:-..}"
if [ ! -f "$ORACLE_PKG_DIR/pyproject.toml" ]; then
    echo "ERROR: no pyproject.toml at $ORACLE_PKG_DIR (run this from refusal-jailbreaking/, or set ORACLE_PKG_DIR)." >&2
    exit 1
fi

echo "Installing circuit-oracle (editable) from $ORACLE_PKG_DIR ..."
uv pip install -e "$ORACLE_PKG_DIR"
echo ""

# ---------------------------------------------------------------------------
# 4. API key setup
# ---------------------------------------------------------------------------

# Prompt for a key, showing the last 4 chars of the existing value as a default.
# Pressing Enter at the prompt keeps the existing value.
# Args: $1 = prompt text, $2 = current value, $3 = name of variable to assign.
prompt_key() {
    local prompt_text="$1"
    local current_value="$2"
    local var_name="$3"
    local new_value
    if [ -n "$current_value" ]; then
        local masked="...${current_value: -4}"
        read -p "${prompt_text} [press Enter to keep ${masked}]: " new_value
    else
        read -p "${prompt_text}: " new_value
    fi
    if [ -n "$new_value" ]; then
        printf -v "$var_name" '%s' "$new_value"
    else
        printf -v "$var_name" '%s' "$current_value"
    fi
}

DO_KEY_SETUP=0
EXISTING_OR_KEY=""
EXISTING_HF=""

if [ ! -f "$ENV_FILE" ]; then
    echo "No .env file found. Let's set up your API keys (will be written to $ENV_FILE)."
    echo ""
    DO_KEY_SETUP=1
else
    echo "Found existing .env at $ENV_FILE."
    # Load existing values so we can offer them as defaults below.
    set -a
    # shellcheck disable=SC1091
    source "$ENV_FILE"
    set +a
    EXISTING_OR_KEY="${OPENROUTER_API_KEY:-}"
    EXISTING_HF="${HF_TOKEN:-}"
    read -p "Update API keys? (y/N): " UPDATE_KEYS
    UPDATE_KEYS=${UPDATE_KEYS:-N}
    if [[ "$UPDATE_KEYS" =~ ^[Yy] ]]; then
        DO_KEY_SETUP=1
    else
        echo "Keeping existing $ENV_FILE."
    fi
fi

if [ "$DO_KEY_SETUP" = "1" ]; then
    # One required key. The merged LLMClient speaks the OpenAI
    # /v1/chat/completions protocol only, and provider="anthropic" (once a silent
    # alias for OpenRouter) is now retired and raises, so OPENROUTER_API_KEY is the
    # only LLM key a default run needs. This prompt used to offer an "anthropic
    # only" path that stored ANTHROPIC_API_KEY and left OPENROUTER_API_KEY empty,
    # which yielded a config that passed setup and then 401d on the first call.
    # KILO_API_KEY is optional and only used by --provider kilo.
    echo ""
    echo "LLM access is a single OpenRouter key (one key reaches the Anthropic,"
    echo "OpenAI, Google, xAI and MiniMax models this project uses)."
    echo ""
    echo "  Claude models are reached through OpenRouter with this same key, so"
    echo "  no Anthropic key is needed (--provider anthropic is retired)."
    echo "  To spend Kilo credits on the main models, set KILO_API_KEY too and"
    echo "  pass --provider kilo; gpt-oss-120b stays on OpenRouter either way."
    echo "  To use a self-hosted vLLM server instead, set LLM_BASE_URL (and"
    echo "  LLM_API_KEY if it checks tokens)."
    echo ""
    prompt_key "Enter your OpenRouter API key" "$EXISTING_OR_KEY" OPENROUTER_API_KEY
    LLM_PROVIDER="openrouter"

    prompt_key "Enter your HuggingFace token" "$EXISTING_HF" HF_TOKEN

    # The redirection below truncates $ENV_FILE, so every key setup does not
    # manage is destroyed unless it is carried forward. KILO_API_KEY is the live
    # example, since losing it breaks every --provider kilo run and the failure
    # surfaces much later as a missing-key error on the first LLM call rather
    # than here, but LLM_BASE_URL, LLM_API_KEY, GRAPH_STORE and HF_HOME have the
    # same exposure. Preserve every line except the three keys this block
    # rewrites, rather than enumerating survivors one at a time and rediscovering
    # the bug with the next key someone adds. Read into a variable first, because
    # the redirection empties the file before the block body runs.
    _PRESERVED_ENV=""
    if [ -f "$ENV_FILE" ]; then
        _PRESERVED_ENV="$(grep -vE '^[[:space:]]*(LLM_PROVIDER|OPENROUTER_API_KEY|HF_TOKEN)=' "$ENV_FILE" || true)"
    fi
    {
        echo "LLM_PROVIDER=${LLM_PROVIDER}"
        echo "OPENROUTER_API_KEY=${OPENROUTER_API_KEY}"
        echo "HF_TOKEN=${HF_TOKEN}"
        if [ -n "$_PRESERVED_ENV" ]; then
            printf '%s\n' "$_PRESERVED_ENV"
        fi
    } > "$ENV_FILE"

    echo ""
    echo "API keys saved to $ENV_FILE"
fi

echo ""

# ---------------------------------------------------------------------------
# 5. Source .env and export HF_HOME
# ---------------------------------------------------------------------------
# shellcheck disable=SC1091
set -a
source "$ENV_FILE"
set +a

# Respect an inherited HF_HOME so a pod launcher can point the cache at a
# network volume or a shared disk. The old unconditional assignment silently
# overrode the caller, which sent a 68.5 GB download to the wrong filesystem
# with nothing in the log to say the caller's value had been discarded.
# The default is absolute and matches download_weights.py's own fallback, so
# the cache no longer moves when setup is invoked from another directory.
_SETUP_THREAD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export HF_HOME="${_CALLER_HF_HOME:-${HF_HOME:-$_SETUP_THREAD_DIR/weights/hf_cache}}"
echo "HF_HOME=$HF_HOME"

# ---------------------------------------------------------------------------
# 6. Download model weights
# ---------------------------------------------------------------------------
echo "Downloading model weights..."
# --yes because setup.sh has already announced the download, and the script
# otherwise refuses to start when stdin is not a terminal.
python scripts/download_weights.py --yes

# ---------------------------------------------------------------------------
# 7. Done
# ---------------------------------------------------------------------------
echo ""
echo "============================================"
echo "  Setup complete!"
echo ""
echo "  Run experiments with:"
echo "    bash scripts/run.sh"
echo "============================================"
echo ""
