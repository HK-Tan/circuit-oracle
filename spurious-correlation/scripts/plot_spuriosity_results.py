#!/usr/bin/env python3
"""Plot detection accuracy for the Circuit Oracle vs. the two
cosine-similarity baselines, one grouped bar chart, grouped by dataset with
an Overall group. Biased and unbiased probes are pooled into a single
per-dataset accuracy (each still scored by its own correctness rule --
dominant == "spurious" for biased, dominant in {causal, mixed} for unbiased
-- but combined into one number rather than shown as two separate panels).

Usage:
    python spurious-correlation/scripts/plot_spuriosity_results.py

Reads:
  - Circuit Oracle: the five `judge_feature_counts.json` passes under each
    experiment directory in `results/probes-arm1/exp/`, averaged into a
    5-pass mean per dataset. This is the same data `eval_oracle_feature_counts.py
    --results-dir results/probes-arm1 --all-runs` would judge from; the
    committed judge verdicts are read directly rather than re-run.
  - Trans-cos / SAE-cos: the committed judge verdicts in
    `probe_artifacts/sae_analysis/`, scored the same way
    `eval_sae_judge_spuriosity.py` does (regex-parsed YES/NO verdict).

No API calls, no GPU. Writes to `runs/figures/spuriosity_results.pdf` by
default; pass --out to write elsewhere (e.g. to overwrite the paper's
`images/spuriosity_results.pdf` directly).
"""

from __future__ import annotations

import argparse
import glob
import json
import re
from collections import defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_TASK_ROOT = _HERE.parent

DATASETS = ["bib_nurse_professor", "bib_journalist_dietitian", "civil_comments", "multinli"]
DATASET_LABELS = {
    "bib_nurse_professor": "BiB-N/P",
    "bib_journalist_dietitian": "BiB-J/D",
    "civil_comments": "CC",
    "multinli": "MNLI",
}

EXP_RE = re.compile(
    r"exp-probe-(.+?)-(pos_pos|neg_neg)_\d+-(biased|unbiased)-probe-correct-question"
)


def oracle_accuracy(results_dir: Path) -> dict[str, dict[str, tuple[int, int]]]:
    """5-pass mean accuracy per dataset per probe_type, from committed judge verdicts."""
    per_ds = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    exp_root = results_dir / "exp"
    for exp_dir in sorted(glob.glob(str(exp_root / "*"))):
        m = EXP_RE.match(Path(exp_dir).name)
        if not m:
            continue
        dataset, _subgroup, probe_type = m.groups()
        for pass_dir in glob.glob(exp_dir + "/*_pass*"):
            jf = Path(pass_dir) / "judge_feature_counts.json"
            if not jf.exists():
                continue
            d = json.loads(jf.read_text())
            dom = d.get("dominant")
            if dom is None:
                continue
            correct = (dom == "spurious") if probe_type == "biased" else (dom in ("causal", "mixed"))
            cell = per_ds[dataset][probe_type]
            cell[0] += int(correct)
            cell[1] += 1
    return {ds: {pt: tuple(v) for pt, v in pts.items()} for ds, pts in per_ds.items()}


def baseline_accuracy(analysis_dir: Path, feat_type: str) -> dict[str, dict[str, tuple[int, int]]]:
    """Accuracy per dataset per ranking, from the committed SAE/transcoder judge verdicts.

    Mirrors eval_sae_judge_spuriosity.py's YES/NO regex parse: a biased
    ranking is correct on YES, an unbiased ranking is correct on NO.
    """
    glob_pat = "*-transcoder-*.json" if feat_type == "plt" else "*-sae-*.json"
    per_ds = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for f in sorted(analysis_dir.glob(glob_pat)):
        m = re.match(r"(.+?)-(pos_pos|neg_neg)_\d+-(?:transcoder|sae)-(biased|unbiased)", f.stem)
        if not m:
            continue
        dataset, _subgroup, ranking = m.groups()
        d = json.loads(f.read_text())
        analysis = d.get("analysis", "")
        vm = re.search(r"Verdict[:\s]+\**(YES|NO)\**", analysis, re.IGNORECASE)
        verdict = vm.group(1).upper() if vm else None
        if verdict is None:
            wm = re.search(r"\b(YES|NO)\b", analysis)
            verdict = wm.group(1).upper() if wm else None
        if verdict is None:
            continue
        correct = (verdict == "YES") if ranking == "biased" else (verdict == "NO")
        cell = per_ds[dataset][ranking]
        cell[0] += int(correct)
        cell[1] += 1
    return {ds: {pt: tuple(v) for pt, v in pts.items()} for ds, pts in per_ds.items()}


def _pct(cell: tuple[int, int] | None) -> float:
    if not cell or cell[1] == 0:
        return 0.0
    return 100.0 * cell[0] / cell[1]


def _combined(per_ds: dict, ds: str) -> tuple[int, int]:
    """Pool biased + unbiased tallies for one dataset into a single cell."""
    c = n = 0
    for probe_type in ("biased", "unbiased"):
        cell = per_ds.get(ds, {}).get(probe_type)
        if cell:
            c += cell[0]
            n += cell[1]
    return c, n


def _combined_overall(per_ds: dict) -> tuple[int, int]:
    c = n = 0
    for ds in DATASETS:
        dc, dn = _combined(per_ds, ds)
        c += dc
        n += dn
    return c, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", default=str(_TASK_ROOT / "results" / "probes-arm1"))
    ap.add_argument("--analysis-dir", default=str(_TASK_ROOT / "probe_artifacts" / "sae_analysis"))
    ap.add_argument("--out", default=None,
                     help="Output path. Default: <task root>/runs/figures/spuriosity_results.pdf")
    args = ap.parse_args()

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        raise SystemExit("plot_spuriosity_results needs matplotlib and numpy installed.")

    oracle = oracle_accuracy(Path(args.results_dir))
    trans = baseline_accuracy(Path(args.analysis_dir), "plt")
    sae = baseline_accuracy(Path(args.analysis_dir), "sae")

    methods = [("Circuit Oracle", oracle, "#1f77b4"),
               ("Trans-cos", trans, "#ff7f0e"),
               ("SAE-cos", sae, "#2ca02c")]

    groups = [DATASET_LABELS[d] for d in DATASETS] + ["Overall"]
    n_groups = len(groups)
    n_methods = len(methods)

    fig, ax = plt.subplots(1, 1, figsize=(6, 3.5))
    bar_w = 0.7 / n_methods
    x = np.arange(n_groups, dtype=float)

    for i, (label, data, color) in enumerate(methods):
        heights = [_pct(_combined(data, ds)) for ds in DATASETS]
        heights.append(_pct(_combined_overall(data)))
        offset = (i - (n_methods - 1) / 2) * bar_w
        bars = ax.bar(x + offset, heights, bar_w, label=label, color=color,
                      edgecolor="black", linewidth=0.4)
        for bar, h in zip(bars, heights):
            ax.annotate(f"{h:.0f}", xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 2), textcoords="offset points", rotation=0,
                        ha="center", va="bottom", fontsize=10)
    ax.axvline(x=n_groups - 1.5, color="gray", linestyle=":", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(groups, rotation=0, ha="center", fontsize=12)
    ax.set_title("Spurious correlation detection accuracy", fontsize=13)
    ax.set_ylim(0, 115)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels([f"{y}%" for y in [0, 20, 40, 60, 80, 100]], fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    ax.set_ylabel("Accuracy (%)", fontsize=12)
    ax.legend(loc="lower right", fontsize=11, frameon=True)
    fig.tight_layout()

    out = Path(args.out) if args.out else _TASK_ROOT / "runs" / "figures" / "spuriosity_results.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
