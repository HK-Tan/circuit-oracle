"""Materialize the AdvBench + Alpaca contrastive train+val pools for the Arditi
refusal-direction baseline.

Local-runnable (no GPU). Needs internet for HuggingFace.

    python -m baselines.arditi.fetch_data --seed 42 --n-train 128 --n-val 32

Output: baselines/arditi/data/refusal_train.json (contains train AND val splits)

Faithful to Arditi's `pipeline/run_pipeline.py:28-33` which samples train and
val from SEPARATE dataset splits (`split='train'` vs `split='val'`), disjoint
by construction. AdvBench/Alpaca on HF are single-split, so we approximate
this by sampling n_train + n_val items disjointly from one shuffled pool.

Both n_train and n_val are PRE-FILTER caps (matching Arditi). The behavior
filter in extract_direction.py drops prompts whose baseline behavior
contradicts their label, so the post-filter pools are typically a few
prompts smaller than the caps.

Not redistributed. The harmless side is alpaca-cleaned under CC BY-NC 4.0, so
refusal_train.json is absent from a fresh checkout and this script is what puts
it there. See data/SOURCES.md for the per-source licences.

Note on out-of-sample evaluation: the 40 AdvBench entries in the eval set are
drawn from the complement of this file by construction, in
scripts/build_prompt_set.py. The 10 older locked entries are not deduped against
the train pool, because they sit on a different distribution from AdvBench and
each training prompt contributes 1/128 (about 0.8%) to the diff-in-mean anyway.
To audit overlap, compare refusal_train.json against data/prompts.json.
"""

from __future__ import annotations

import argparse
import json
import os
import random

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(REPO_ROOT, "baselines", "arditi", "data")


def fetch_refusal(seed: int, n_train: int, n_val: int) -> dict:
    """Build train+val contrastive pools from AdvBench (harmful) and Alpaca (harmless).

    Train and val are disjoint slices of the same shuffled pool, mirroring
    Arditi's split='train' vs split='val' separation. n_train and n_val are
    BOTH pre-filter caps; the behavior filter at extract time may drop a few
    prompts from each.
    """
    from datasets import load_dataset

    advbench = load_dataset("walledai/AdvBench", split="train")
    harmful_pool = [row["prompt"] for row in advbench]

    alpaca = load_dataset("yahma/alpaca-cleaned", split="train")
    harmless_pool = [row["instruction"] for row in alpaca if not (row["input"] or "").strip()]

    rng = random.Random(seed)
    rng.shuffle(harmful_pool)
    rng.shuffle(harmless_pool)

    needed = n_train + n_val
    if len(harmful_pool) < needed:
        raise RuntimeError(f"AdvBench has {len(harmful_pool)} prompts, need {needed} (train+val)")
    if len(harmless_pool) < needed:
        raise RuntimeError(f"Alpaca has {len(harmless_pool)} prompts, need {needed} (train+val)")

    print(f"Harmful pool:  {len(harmful_pool)} → train[:{n_train}] + val[{n_train}:{needed}]")
    print(f"Harmless pool: {len(harmless_pool)} → train[:{n_train}] + val[{n_train}:{needed}]")

    return {
        "metadata": {
            "regime": "refusal",
            "harmful_source": "walledai/AdvBench",
            "harmless_source": "yahma/alpaca-cleaned (empty-input subset)",
            "seed": seed,
            "n_train": n_train,
            "n_val": n_val,
        },
        "harmful_train":  harmful_pool[:n_train],
        "harmful_val":    harmful_pool[n_train:needed],
        "harmless_train": harmless_pool[:n_train],
        "harmless_val":   harmless_pool[n_train:needed],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--n-train", dest="n_train", type=int, default=128,
                    help="pre-filter train cap per side (Arditi default 128)")
    ap.add_argument("--n-val", dest="n_val", type=int, default=32,
                    help="pre-filter val cap per side (Arditi default 32)")
    args = ap.parse_args()

    os.makedirs(DATA_DIR, exist_ok=True)
    out = fetch_refusal(args.seed, args.n_train, args.n_val)
    path = os.path.join(DATA_DIR, "refusal_train.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {path} "
          f"({args.n_train} harmful_train + {args.n_train} harmless_train + "
          f"{args.n_val} harmful_val + {args.n_val} harmless_val)")


if __name__ == "__main__":
    main()
