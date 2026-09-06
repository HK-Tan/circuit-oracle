#!/usr/bin/env python3
"""Download the subject model and transcoders the refusal task needs.

Fetches Qwen/Qwen3-4B and mwhanna/qwen3-4b-transcoders into
refusal-jailbreaking/weights/hf_cache/, and creates weights/graphs/ for the
attribution output. This is tens of gigabytes, so it never starts without
--yes or an interactive confirmation.

Set HF_HOME first to download somewhere else, and HF_TOKEN if the repos need
authentication.
"""
import argparse
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_DEFAULT_HF_HOME = os.path.join(_REPO, "weights", "hf_cache")

# Sizes are approximate and are printed only so the confirmation prompt can say
# what the download costs. Qwen3-4B is ~4B parameters in bf16. The transcoder
# figure is the post-ignore size documented in IGNORE_PATTERNS below.
MODELS = [
    ("Qwen/Qwen3-4B", "instruction-tuned subject model", "~8 GB"),
    ("mwhanna/qwen3-4b-transcoders", "transcoders", "~60 GB"),
]
APPROX_TOTAL = "~68 GB"

# The transcoder repos carry a `features/` directory (44 GB on
# mwhanna/qwen3-4b-transcoders) that no code path reads. hf_utils.py fetches only
# layer_*.safetensors, and autointerp labels come live from the Neuronpedia API.
# Skipping it takes the repo from 104.5 GB to 60.4 GB. circuit_tracer's own
# hf_utils already avoids this, so only this script needed the guard.
IGNORE_PATTERNS = ["features/*"]


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__.strip().split("\n\n")[0],
        epilog="Nothing is downloaded until you confirm.",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="skip the confirmation prompt and start the download",
    )
    return parser.parse_args(argv)


def describe(dest: str) -> None:
    """Print what would be fetched and where, before anything is fetched."""
    print("[download_weights] Will download:")
    for repo_id, description, size in MODELS:
        print(f"[download_weights]   {repo_id:32s} {size:>8s}  ({description})")
    print(f"[download_weights] Approximate total: {APPROX_TOTAL}")
    print(f"[download_weights] Destination (HF_HOME): {dest}")
    print(f"[download_weights] Graph output dir: {os.path.join(_REPO, 'weights', 'graphs')}")


def confirmed(assume_yes: bool) -> bool:
    if assume_yes:
        return True
    if not sys.stdin.isatty():
        print("[download_weights] Refusing to download without confirmation. "
              "Re-run with --yes.", file=sys.stderr)
        return False
    reply = input("[download_weights] Proceed with the download? [y/N] ").strip().lower()
    return reply in ("y", "yes")


def download_weights() -> None:
    # Imported here, after HF_HOME is set, because huggingface_hub reads the
    # cache location at import time.
    import huggingface_hub

    token = os.environ.get("HF_TOKEN") or None

    # Absolute, so a run from any cwd populates the same tree HF_HOME points at.
    os.makedirs(os.environ["HF_HOME"], exist_ok=True)
    os.makedirs(os.path.join(_REPO, "weights", "graphs"), exist_ok=True)

    for repo_id, description, _size in MODELS:
        print(f"\n[download_weights] Downloading {description}: {repo_id} ...")
        ignore = IGNORE_PATTERNS if "transcoders" in repo_id else None
        if ignore:
            print(f"[download_weights]   skipping {ignore} (unread, saves ~44 GB)")
        local_dir = huggingface_hub.snapshot_download(
            repo_id=repo_id,
            token=token,
            ignore_patterns=ignore,
        )
        print(f"[download_weights] {repo_id} saved to: {local_dir}")

    print("\n[download_weights] All downloads complete.")
    print("[download_weights] weights/graphs/ directory is ready for circuit output.")


def main(argv=None) -> int:
    args = parse_args(argv)

    # Resolve to an absolute path so the script works from any working directory.
    dest = os.environ.get("HF_HOME") or _DEFAULT_HF_HOME
    describe(dest)
    if not confirmed(args.yes):
        return 1

    os.environ["HF_HOME"] = dest
    download_weights()
    return 0


if __name__ == "__main__":
    sys.exit(main())
