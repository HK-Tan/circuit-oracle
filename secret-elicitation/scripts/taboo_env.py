"""The one .env loader every secret-elicitation entry script uses.

Nothing in this task's Python is launched through a shell wrapper, so each
entry script has to read the repo-root .env itself. The two graph builders used
to skip that step, which meant a GRAPH_STORE or an HF_TOKEN that lived only in
.env was silently ignored on the build path while the runners honoured it. The
build then wrote its graphs to the thread root instead of the network volume
and the runners looked for them on the volume and found nothing.

Both functions live here rather than in a runner so the builders can import
them without importing a runner (the runners already import
build_taboo_graphs, so the arrow only points one way).

    ORACLE_ENV_FILE   path to the KEY=VALUE file to read, when it is not the
                      repo-root .env
"""

from __future__ import annotations

import os
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def default_env_path() -> Path:
    """Where to look for a .env holding API keys and store paths.

    Override with $ORACLE_ENV_FILE, otherwise a .env at the repo root.
    """
    override = os.environ.get("ORACLE_ENV_FILE")
    return Path(override) if override else _REPO_ROOT / ".env"


def load_env_file(path: Path) -> None:
    """Seed os.environ from a KEY=VALUE file. Missing file is not an error.

    setdefault, not assignment, so anything already exported in the shell wins
    over the file.
    """
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
