#!/usr/bin/env python3
"""Launch the local autointerp FastAPI shim that mimics Neuronpedia.

Default config targets the qwen3-8b-transcoders feature cache used by the
ELK / taboo experiments. Override paths via flags or AUTOINTERP_* env vars.

Paths, in precedence order (flag, then env var, then the documented default):
    --features-dir  AUTOINTERP_FEATURES_DIR  <HF cache>/hub/models--mwhanna--qwen3-8b-transcoders/snapshots/<rev>/features
    --cache-dir     AUTOINTERP_CACHE_DIR     <repo>/secret-elicitation/autointerp_cache
    --model         AUTOINTERP_MODEL         openai/gpt-oss-120b

The features default follows HF_HOME when it is set (the VM setup scripts point
it at the shared weights tree), otherwise the standard ~/.cache/huggingface.
The revision below is the pinned snapshot the ELK features dump was produced
from, so a different revision on disk needs --features-dir.

Example:
    OPENROUTER_API_KEY=sk-or-... python scripts/run_autointerp_server.py
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# This file is <repo>/scripts/run_autointerp_server.py, so the repo root is one
# level up, not two. It used to sit one directory deeper and therefore used
# parents[2]. The move to the repo-root scripts/ folder made that one level too
# high, which silently pointed the label cache at a sibling of the repo instead
# of secret-elicitation/autointerp_cache.
_REPO = Path(__file__).resolve().parents[1]

# Pinned revision of mwhanna/qwen3-8b-transcoders that the ELK features dump came
# from. Recorded here as provenance, not as a guess about what is on disk.
_TRANSCODER_REV = "dc677109cde096a85d03fff4f73a3ec88e7e2105"


def load_env_file(path: Path) -> None:
    """Seed os.environ from a KEY=VALUE file. Missing file is not an error.

    setdefault, not assignment, so anything already exported in the shell wins
    over the file.
    """
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v)


# Loaded here, at import, BEFORE the DEFAULT_* constants below read os.environ.
# Those constants are the argparse defaults, so loading .env inside main() meant
# HF_HOME and the AUTOINTERP_* variables only worked when already exported.
load_env_file(_REPO / ".env")

_HF_HOME = Path(os.environ.get("HF_HOME") or (Path.home() / ".cache" / "huggingface"))

DEFAULT_FEATURES_DIR = os.environ.get("AUTOINTERP_FEATURES_DIR") or str(
    _HF_HOME / "hub" / "models--mwhanna--qwen3-8b-transcoders"
    / "snapshots" / _TRANSCODER_REV / "features"
)
DEFAULT_CACHE_DIR = os.environ.get("AUTOINTERP_CACHE_DIR") or str(
    _REPO / "secret-elicitation" / "autointerp_cache"
)
# gpt-oss-120b is the standard "everything else" model (decided 2026-07-26,
# it is already the subagent everywhere). The earlier cache was labeled with
# minimax/minimax-m2.7, so labels regenerated under this default are a new
# provenance. Point --cache-dir at a fresh directory rather than mixing two
# labelers in one autointerp.jsonl (the cache key is (layer, feature) and does
# not include the model).
DEFAULT_MODEL = os.environ.get("AUTOINTERP_MODEL") or "openai/gpt-oss-120b"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--features-dir", default=DEFAULT_FEATURES_DIR,
                   help="feature dump the shim reads (env: AUTOINTERP_FEATURES_DIR)")
    p.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR,
                   help="autointerp label cache, created if missing (env: AUTOINTERP_CACHE_DIR)")
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help="Autointerp LLM (OpenRouter model id, env: AUTOINTERP_MODEL).")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--reload", action="store_true")
    args = p.parse_args()

    if not os.environ.get("OPENROUTER_API_KEY"):
        print("ERROR: OPENROUTER_API_KEY not set (env or .env).", file=sys.stderr)
        return 1

    # Fail loud here rather than per request. A missing feature dump would
    # otherwise turn every inspect_feature call into a 404 while the rest of the
    # run looks healthy.
    if not Path(args.features_dir).is_dir():
        print(
            f"ERROR: features dir not found: {args.features_dir}\n"
            "Pass --features-dir or set AUTOINTERP_FEATURES_DIR.",
            file=sys.stderr,
        )
        return 1

    Path(args.cache_dir).mkdir(parents=True, exist_ok=True)
    os.environ["AUTOINTERP_FEATURES_DIR"] = args.features_dir
    os.environ["AUTOINTERP_CACHE_DIR"] = args.cache_dir
    os.environ["AUTOINTERP_MODEL"] = args.model

    import uvicorn
    print(
        f"Serving local autointerp on http://{args.host}:{args.port}\n"
        f"  features_dir = {args.features_dir}\n"
        f"  cache_dir    = {args.cache_dir}\n"
        f"  model        = {args.model}\n"
        f"Point ToolContext.neuronpedia_base_url at this server."
    )
    uvicorn.run(
        "circuit_oracle.autointerp_server:create_app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        factory=True,
        workers=8
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
