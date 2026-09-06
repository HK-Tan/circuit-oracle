"""One-shot: add `n_refusals: 0` to every stats block in a pre-refusal-aware
Arditi judge_summary.json so the schema matches the post-fix output from
llm_judge.py / exp_judge.py.

Safe to re-run, it is idempotent. Only patches dicts that have `n_calls` but
no `n_refusals`. Operates in place.

Why this is safe without re-running the actual judge calls: the legacy run
predates the `stop_reason in {refusal, content_filter}` detection in
judge_one. Every stats block in the legacy file shows `n_calls = N_JUDGES *
N_REPEATS`, which proves no judge call returned an empty refusal-shaped
response (those would have dropped to None and reduced n_calls). So every
legacy stats block had exactly zero refusals, so this records rather
than infers.

Usage:
    python -m baselines.arditi._patch_legacy_refusal_schema
    python -m baselines.arditi._patch_legacy_refusal_schema path/to/other.json
"""

from __future__ import annotations

import argparse
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_PATH = os.path.join(REPO_ROOT, "baselines", "arditi", "runs", "judge_summary.json")


def patch(obj):
    """Recursively walk dict/list. Add `n_refusals: 0` to any dict containing
    `n_calls` but missing `n_refusals`. Returns the count of dicts patched.
    """
    n = 0
    if isinstance(obj, dict):
        if "n_calls" in obj and "n_refusals" not in obj:
            obj["n_refusals"] = 0
            n += 1
        for v in obj.values():
            n += patch(v)
    elif isinstance(obj, list):
        for v in obj:
            n += patch(v)
    return n


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.strip().split("\n\n")[0].replace("\n", " "),
    )
    parser.add_argument(
        "path",
        help=f"judge_summary.json to patch in place. The committed archive copy is "
             f"{DEFAULT_PATH}. Pass it explicitly only if you mean to rewrite it.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    path = parse_args(argv).path
    if not os.path.exists(path):
        raise SystemExit(f"ERROR: no file at {path}")
    with open(path) as f:
        data = json.load(f)
    n_patched = patch(data)
    if n_patched == 0:
        print(f"Nothing to patch in {path}")
        return
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Patched {n_patched} stats block(s) with n_refusals=0 in {path}")


if __name__ == "__main__":
    main()
