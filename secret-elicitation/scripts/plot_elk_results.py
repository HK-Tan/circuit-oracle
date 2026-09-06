#!/usr/bin/env python3
"""Plot per-word + overall hit rate for one mode (open or closed) as a grouped
bar chart. Mirrors the visual style of `elk_closed_results.pdf`.

Usage:
    python secret-elicitation/scripts/plot_elk_results.py --mode closed
    python secret-elicitation/scripts/plot_elk_results.py --mode open
    python secret-elicitation/scripts/plot_elk_results.py --mode closed \
        --methods tc_l9 sae_l9 or_c
    python secret-elicitation/scripts/plot_elk_results.py --mode closed \
        --words all20

Reads the same JSON files as `print_table.sh` / `eval_elk_results.py`, and
writes into the thread's gitignored `runs/figures/` folder by default. The
committed `figures/elk_closed_results.pdf` is the published figure and is never
overwritten.

The projection and activation-oracle baseline JSONs come from a separate
harness (`$AO_BASELINES_DIR`, historically /workspace/activation_oracles/
experiments) that is NOT in this repo and is a known unrecoverable hole. A
requested baseline whose file is missing is a hard error, never a silently
dropped series.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np

from eval_elk_results import score_file
from taboo_words import (
    CANDIDATE_WORDS as _CANDIDATE_WORDS,
    REPORTED_WORDS as _REPORTED_WORDS,
)

_HERE = Path(__file__).resolve().parent
_THREAD = _HERE.parent  # secret-elicitation/, the thread root above scripts/
# Baseline JSONs from the activation-oracles harness. Override with
# $AO_BASELINES_DIR, the default is the path they lived at on the VM.
_BLS = Path(
    os.environ.get("AO_BASELINES_DIR", "/workspace/activation_oracles/experiments")
)

# The 8 secrets behind the published closed-mode figure. See taboo_words.py
# for the two checks that pin the list down.
REPORTED_WORDS = _REPORTED_WORDS

# Every trained secret. The archived eval.json files cover all 20, the paper
# figure plots only the 8 above because the baselines stop there.
ALL_WORDS = _CANDIDATE_WORDS

WORD_SETS = {"reported8": REPORTED_WORDS, "all20": ALL_WORDS}

# Default method set per mode, matching the existing `elk_closed_results.pdf`:
# transcoder L9 projection vs SAE L9 projection vs circuit oracle.
DEFAULT_METHODS = {
    "closed": ["tc_l9", "sae_l9", "or_c"],
    "open":   ["tc_l9", "sae_l9", "or_o"],
}

# Map compact method name -> (result file path, pretty label for legend).
def _file_map(mode: str) -> dict[str, tuple[Path, str]]:
    sfx = "_closed" if mode == "closed" else ""
    # Archived arms behind the published figure. Point --methods elsewhere or
    # re-run the evaluators against a fresh run set to plot a replication.
    oracle_path = (
        _THREAD / "results-workshop/closed/eval.json"
        if mode == "closed"
        else _THREAD / "results-workshop/open/eval.json"
    )
    oracle_key = "or_c" if mode == "closed" else "or_o"
    return {
        "ao":     (_BLS / f"ao_elk_results{sfx}.json",                          "AO (LoRA)"),
        "sae_l9":  (_BLS / f"sae_elk_results_layer9_tfidf{sfx}.json",            "SAE-proj (L9)"),
        "sae_l18": (_BLS / f"sae_elk_results_layer18_tfidf{sfx}.json",           "SAE-proj (L18)"),
        "sae_l27": (_BLS / f"sae_elk_results_layer27_tfidf{sfx}.json",           "SAE-proj (L27)"),
        "tc_l9":   (_BLS / f"transcoder_elk_results_layer9_tfidf{sfx}.json",     "Trans-proj (L9)"),
        "tc_l18":  (_BLS / f"transcoder_elk_results_layer18_tfidf{sfx}.json",    "Trans-proj (L18)"),
        "tc_l27":  (_BLS / f"transcoder_elk_results_layer27_tfidf{sfx}.json",    "Trans-proj (L27)"),
        oracle_key: (oracle_path,                                                "Circuit Oracle"),
    }


# Fixed colours so the same method always reads the same colour across plots.
COLORS = {
    "ao":     "#9467bd",
    "tc_l9":  "#ff7f0e", "tc_l18":  "#ff9f4a", "tc_l27":  "#ffb87a",
    "sae_l9": "#2ca02c", "sae_l18": "#5fbf5f", "sae_l27": "#8fd18f",
    "or_o":   "#1f77b4",
    "or_c":   "#1f77b4",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["open", "closed"], required=True)
    ap.add_argument("--words", choices=sorted(WORD_SETS), default="reported8",
                    help="Which secrets to plot. Default 'reported8' is the "
                         "published paper figure, 'all20' is the superset.")
    ap.add_argument("--methods", nargs="+", default=None,
                    help="Compact method names (e.g. tc_l9 sae_l9 or_c). "
                         "Default = transcoder L9, SAE L9, oracle.")
    ap.add_argument("--oracle-metric", default="top10",
                    choices=["top1", "top3", "top5", "top10"],
                    help="Shortlist depth for open-mode oracle eval.json.")
    ap.add_argument("--out", default=None,
                    help="Output path. Default: <thread>/runs/figures/"
                         "elk_{mode}_results.pdf. The committed figures/ copy is "
                         "left alone.")
    args = ap.parse_args()

    # After parse_args, so --help works without the optional plotting stack.
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise SystemExit(
            "plot_elk_results needs the plots extra: pip install 'circuit-oracle[plots]'"
        )

    methods = args.methods or DEFAULT_METHODS[args.mode]
    words = WORD_SETS[args.words]
    fmap = _file_map(args.mode)

    unknown = [k for k in methods if k not in fmap]
    if unknown:
        raise SystemExit(f"unknown method key(s) {unknown}; choices: {sorted(fmap)}")

    # Fail loud on any requested series whose file is absent. Plotting a
    # subset of the requested methods would silently misreport the figure.
    missing = [(k, fmap[k][0]) for k in methods if not fmap[k][0].exists()]
    if missing:
        lines = [f"  {k}: {p}" for k, p in missing]
        raise SystemExit(
            "missing result file(s) for requested methods:\n"
            + "\n".join(lines)
            + f"\n\nBaseline JSONs are read from AO_BASELINES_DIR (currently "
              f"{_BLS}). They were produced by a separate activation-oracles "
              "harness that is not part of this repo, so they are a known "
              "regeneration hole. Point AO_BASELINES_DIR at a directory that "
              "holds them, or pass --methods with only the series you have "
              "(for example --methods or_c)."
        )

    series = []  # list of (method_key, label, {word: (m, n)}, (tm, tn))
    for key in methods:
        path, label = fmap[key]
        _, pw, _ = score_file(path, channel="oracle_response",
                              oracle_metric=args.oracle_metric)
        pw_filtered = {w: pw.get(w, (0, 0)) for w in words}
        tm = sum(m for m, _ in pw_filtered.values())
        tn = sum(n for _, n in pw_filtered.values())
        series.append((key, label, pw_filtered, (tm, tn)))

    groups = words + ["Overall"]
    n_groups = len(groups)
    n_methods = len(series)
    bar_w = 0.86  / n_methods
    x = np.arange(n_groups, dtype=float)

    # Scale width modestly with group count and bump fonts so 20+ groups
    # don't shrink text. Width caps at ~16" so the figure stays printable.
    fig_w = 16
    fig_h = 4 
    rotate = 30 if n_groups > 12 else 0

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    annot_fs = 10
    for i, (key, label, pw, (tm, tn)) in enumerate(series):
        heights = []
        annots = []
        for w in words:
            m, n = pw[w]
            pct = (100 * m / n) if n else 0.0
            heights.append(pct)
            annots.append("")
            # annots.append(f"{m}/{n}" if n else "-")
        overall_pct = (100 * tm / tn) if tn else 0.0
        heights.append(overall_pct)
        annots.append(f"{overall_pct:.1f}%")

        offset = (i - (n_methods - 1) / 2) * bar_w
        bars = ax.bar(x + offset, heights, bar_w,
                      label=label, color=COLORS.get(key, None),
                      edgecolor="black", linewidth=0.4)
        for bar, txt in zip(bars, annots):
            ax.annotate(txt,
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 2), textcoords="offset points", rotation=60,
                        ha="center", va="bottom", fontsize=annot_fs)

    # Vertical separator between per-word groups and the Overall group.
    ax.axvline(x=n_groups - 1.5, color="gray", linestyle=":", linewidth=0.8)

    ax.set_xticks(x)
    ax.set_xticklabels(
        groups, fontsize=12,
        rotation=rotate, ha=("right" if rotate else "center"),
    )
    ax.tick_params(axis="y", labelsize=12)
    ax.set_ylabel("Accuracy (%)", fontsize=13)
    ax.set_ylim(0, 115)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_title(
        f"{args.mode.capitalize()}-mode secret elicitation accuracy on Qwen3-8B taboo LoRAs",
        fontsize=14,
    )
    ax.legend(loc="upper right", frameon=True, fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    # Figures land in the gitignored runs/figures/, not next to the committed
    # elk_closed_results.pdf that the paper ships, so replotting cannot silently
    # replace the published figure.
    out = (
        Path(args.out) if args.out
        else _THREAD / "runs" / "figures" / f"elk_{args.mode}_results.pdf"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
