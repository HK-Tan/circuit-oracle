"""Re-exec a CLI script under the project's .venv if it is not already active.

build_graph.py / influence_seed.py / run_seed_sweep.py import circuit_tracer and
circuit_oracle, which setup.sh installs EDITABLE into .venv ("uv pip install -e ."),
so they only resolve under .venv/bin/python. run.sh handles this by sourcing
.venv/bin/activate before calling python. These standalone scripts are usually
launched as a bare `python scripts/X.py`, which picks the SYSTEM interpreter and
dies with ModuleNotFoundError: No module named 'circuit_tracer'. ensure_venv()
transparently re-execs the same argv under .venv/bin/python so either launch
style works without remembering to activate.

Stdlib-only on purpose: this module must import and run BEFORE the editable
packages are imported, under whatever interpreter started the process.

Not replicated here: run.sh also exports LD_LIBRARY_PATH=<torch>/lib so PyTorch
prefers its bundled CUDA libs over any system ones. We do not, because computing
it reliably needs torch already imported. If the heavy attribution build
(build_graph.py) ever hits a CUDA-lib / linker error, build that one graph via
`bash scripts/run.sh --slugs <slug> --keep-graphs`, which sets it defensively.
"""

import os
import sys


def ensure_venv(script_file: str) -> None:
    """Re-exec `script_file` under <repo>/.venv/bin/python if not already there.

    Also pins the same env vars run.sh exports (HF cache dir, CUDA allocator), so
    the standalone scripts reuse the graph build's downloads instead of re-fetching.

    No-op on the venv switch when already running under that venv, or when the
    venv is absent (the later third-party import then fails loud, pointing at
    setup.sh). The env vars are set in all cases.
    """
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(script_file)))

    # Match run.sh's `export HF_HOME=./weights/hf_cache`. Without this, the bare
    # `python scripts/X.py` falls back to ~/.cache/huggingface and RE-DOWNLOADS the
    # subject model + the 36 transcoder shards (~60 GB) that the graph build
    # already cached under weights/hf_cache. huggingface_hub reads HF_HOME at
    # import, so this must run before the heavy imports (it does: ensure_venv is
    # called before them). os.execv carries the updated environ into the re-exec.
    os.environ.setdefault("HF_HOME", os.path.join(repo_root, "weights", "hf_cache"))

    # Honored lazily by torch's CUDA caching allocator (read at first allocation,
    # not at process start), so this takes effect even on the no-re-exec path.
    # Matches run.sh: lets attribution's big one-shot backward buffers be returned
    # to the driver instead of pinned behind the allocator's fixed slabs.
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

    venv_dir = os.path.join(repo_root, ".venv")
    venv_py = os.path.join(venv_dir, "bin", "python")

    # sys.prefix is the active environment's root. Under this venv (whether
    # activated or launched as .venv/bin/python) it equals venv_dir; under the
    # system interpreter it does not. Comparing prefixes is reliable even though
    # venv pythons are symlinks to the base interpreter (so comparing the
    # executables themselves via realpath would wrongly match).
    if os.path.abspath(sys.prefix) == os.path.abspath(venv_dir):
        return
    if not os.path.exists(venv_py):
        return  # no project venv to switch to; let the real import fail loud

    # Replace this process with the venv interpreter running the same command.
    os.execv(venv_py, [venv_py, os.path.abspath(script_file), *sys.argv[1:]])
