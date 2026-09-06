# Contrastive pair sources

`refusal_train.json` is built by `python -m baselines.arditi.fetch_data` and is **not** shipped with this repository. Licences differ per source: AdvBench is MIT, alpaca-cleaned is CC BY-NC 4.0, so the merged file is not redistributed and has to be rebuilt locally before `extract_direction.py` or `scripts/build_prompt_set.py candidates` will run.

## What we use

| Side | Source | Licence | n train | n val |
|---|---|---|---|---|
| Harmful (suppressed) | AdvBench from `walledai/AdvBench` on HuggingFace, `prompt` column | MIT | 128 | 32 |
| Harmless (complied)  | Alpaca-Cleaned (`yahma/alpaca-cleaned`), instructions with empty `input` | CC BY-NC 4.0 | 128 | 32 |

Selection: `seed=42` deterministic shuffle of each pool, take the first 128 for train and the next 32 for val, disjoint by construction.

## What Arditi actually uses (full recipe)

The Arditi paper's harmful pool is broader than just AdvBench. From their `dataset/generate_datasets.ipynb`:

| Source | n | Notes |
|---|---|---|
| AdvBench | up to 128 | `harmful_behaviors.csv`, original `goal` column (HF mirror `walledai/AdvBench` renamed it to `prompt`) |
| MaliciousInstruct | up to 128 | Princeton-SysML benchmark |
| TDC2023 | up to 128 | CAIS Trojan Detection Challenge dev+test |

The three sources are concatenated and deduped, then capped at `n_train=128` total. For harmless, Arditi uses `tatsu-lab/alpaca` (we use `yahma/alpaca-cleaned`, near-identical).

### Why we use AdvBench only

- AdvBench alone has 520 prompts, so at n=128 with seed=42 that is a 24% subsample, plenty of phrasing diversity.
- One source keeps `fetch_data.py` simple, with no inter-source dedup logic and fewer dataset dependencies.
- The diff-in-mean direction is empirically robust to harmful-pool composition (Arditi's ablations show similar directions across pool subsets).

If extraction underperforms (for example the chosen direction gives a weak refusal-drop on val), expand `fetch_data.py:fetch_refusal()` to load and concatenate MaliciousInstruct + TDC2023:

```python
malicious = load_dataset("walledai/MaliciousInstruct", split="train")
tdc = load_dataset("walledai/TDC23-RedTeaming", split="dev")  # check exact slug on HF
harmful_pool = (
    [r["prompt"] for r in advbench]
    + [r["prompt"] for r in malicious]
    + [r["prompt"] for r in tdc]
)
```

Then dedup and shuffle.

## Out-of-sample discipline

The 40 AdvBench entries in the eval set are drawn from the complement of this file by construction. `scripts/build_prompt_set.py candidates` computes AdvBench (520) minus `harmful_train + harmful_val` (160) and samples only from the remaining 360, and `tests/prompt_set/test_prompt_sourcing.py` asserts the disjointness whenever the file is present.

The 10 locked entries are older, LLM-generated prompts on a different distribution from AdvBench, so verbatim overlap is unlikely, and each training prompt contributes 1/128 (about 0.8%) to the diff-in-mean anyway. Proximity is measured and recorded rather than filtered. See the docstring of `scripts/build_prompt_set.py` for why.

## Eval set

The 50 eval prompts live at `refusal-jailbreaking/data/prompts.json` and are never read into the training pool. `apply_direction.py` reads that file directly.

## Reproducibility

```bash
python -m baselines.arditi.fetch_data --seed 42 --n-train 128 --n-val 32
```

Deterministic given the seed and the upstream dataset versions. If AdvBench or Alpaca update, the materialized `refusal_train.json` drifts, and the sourcing tests in `tests/prompt_set/test_prompt_sourcing.py` are what catch it.
