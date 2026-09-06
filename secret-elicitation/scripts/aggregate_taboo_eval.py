#!/usr/bin/env python3
"""Aggregate per-arm taboo eval.json files into the table the paper needs.

Reads the `eval.json` that `eval_oracle_taboo.py` (closed) and
`eval_oracle_taboo_no_options.py` (open) write into each arm directory, and
emits one combined view:

  1. A headline accuracy table across every arm and protocol.
  2. For arms run with repeats, a per-pass breakdown with mean +/- SD, plus
     two stability numbers described below.

Usage:

    python secret-elicitation/scripts/aggregate_taboo_eval.py \
        --results-root secret-elicitation/results \
        --out-json secret-elicitation/runs/aggregate.json \
        --out-md   secret-elicitation/runs/aggregate.md

Why SD across passes and not a bootstrap over items: the 5 passes re-run the
oracle against a FIXED attribution graph per slug, so the spread between them
isolates orchestrator nondeterminism, which is the quantity we care about
here. An item-level bootstrap would instead measure how much the 8 secret
words happen to differ, which is a different claim.

Two stability numbers, because they answer different questions:

  answer_flip_rate  Fraction of items whose ANSWER is not identical across all
                    passes. Sensitive to the oracle changing its mind even when
                    both answers are wrong, which is the honest read on
                    run-to-run determinism.
  verdict_flip_rate Fraction of items whose CORRECTNESS is not constant across
                    passes (right on some passes, wrong on others). This is the
                    number that bounds how much a single-pass accuracy figure
                    can move by luck.

A high answer_flip_rate with a low verdict_flip_rate means the oracle is
consistently wrong in varying ways, which reads very differently from the two
moving together. Reporting only one of them hides that.
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_THREAD = _HERE.parent

PASS_RE = re.compile(r"_pass(?P<n>\d+)$")


def pass_index(run: str) -> int | None:
    """Pass number from a run directory name, or None for a single-pass arm."""
    m = PASS_RE.search(run)
    return int(m.group("n")) if m else None


def is_open(summary: dict) -> bool:
    """Open-protocol evals carry a top-k ladder; closed ones carry `accuracy`."""
    return "top10_recall" in summary


def answer_of(grade: dict, open_mode: bool) -> str | None:
    """The oracle's committed answer, on a common scale across protocols.

    Closed mode commits one word. Open mode commits a ranked shortlist, whose
    rank-1 lemma is the comparable commitment. Comparing whole shortlists would
    conflate "changed its mind" with "reordered ranks 7 through 10", which is
    not what a flip is meant to capture.
    """
    if open_mode:
        sl = grade.get("shortlist") or []
        return (sl[0] or "").strip().lower() or None if sl else None
    g = grade.get("guess")
    return (g or "").strip().lower() or None


def correct_of(grade: dict) -> bool:
    return bool(grade.get("correct"))


def load_arms(root: Path) -> dict[str, dict]:
    arms: dict[str, dict] = {}
    for ev in sorted(root.glob("*/eval.json")):
        try:
            arms[ev.parent.name] = json.loads(ev.read_text())
        except (OSError, json.JSONDecodeError) as e:
            print(f"warning: skipping {ev} ({e})")
    return arms


def per_pass_stats(grades: list[dict], open_mode: bool) -> dict | None:
    """Per-pass accuracy and the two flip rates, or None for single-pass arms."""
    by_pass: dict[int, list[dict]] = defaultdict(list)
    for g in grades:
        p = pass_index(g["run"])
        if p is None:
            return None
        by_pass[p].append(g)
    if len(by_pass) < 2:
        return None

    accs = {p: sum(correct_of(g) for g in gs) / len(gs) for p, gs in sorted(by_pass.items())}
    vals = list(accs.values())

    # Group by item (one exp = one (secret, prompt) cell) and compare across passes.
    by_item: dict[str, dict[int, dict]] = defaultdict(dict)
    for g in grades:
        by_item[g["exp"]][pass_index(g["run"])] = g

    # Only items observed in every pass can flip; a partial item would otherwise
    # report a spurious "no flip" from a single observation.
    n_passes = len(by_pass)
    full = {k: v for k, v in by_item.items() if len(v) == n_passes}

    answer_flips = 0
    verdict_flips = 0
    modal_agreements = []
    # Open mode only: how much of the whole 10-lemma shortlist survives between
    # passes, not just its rank-1 entry. This is the Jaccard the probes track
    # uses for feature sets, applied to the object this track actually emits.
    # It is the number that separates "swapped ranks 1 and 2" from "returned a
    # completely different ten words", which answer_flip_rate alone cannot.
    jaccards = []
    distinct_top1 = []
    for item in full.values():
        answers = [answer_of(g, open_mode) for g in item.values()]
        verdicts = [correct_of(g) for g in item.values()]
        if len(set(answers)) > 1:
            answer_flips += 1
        if len(set(verdicts)) > 1:
            verdict_flips += 1
        modal_agreements.append(Counter(answers).most_common(1)[0][1] / len(answers))
        if open_mode:
            sets = [
                {(w or "").strip().lower() for w in (g.get("shortlist") or []) if w}
                for g in item.values()
            ]
            sets = [s for s in sets if s]
            pairs = [
                len(a & b) / len(a | b)
                for a, b in itertools.combinations(sets, 2)
                if a | b
            ]
            if pairs:
                jaccards.append(statistics.mean(pairs))
            distinct_top1.append(len({a for a in answers if a}))

    # Sample SD (n-1). The 5 passes are a sample of the run-to-run distribution,
    # not the whole population of possible runs.
    sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
    n = len(vals)
    sem = sd / (n ** 0.5) if n else 0.0
    # t critical value at 95%, two-sided, for the small pass counts we actually
    # run. With n=5 that is t(4)=2.776, NOT 1.96: using the normal quantile at
    # n=5 understates the interval by about 40%, which is exactly the direction
    # that would make a noisy arm look reproducible.
    T95 = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571, 7: 2.447,
           8: 2.365, 9: 2.306, 10: 2.262}
    tcrit = T95.get(n, 1.96)
    return {
        "n_passes": n_passes,
        "per_pass_accuracy": accs,
        "mean": statistics.mean(vals),
        "sd": sd,
        "sem": sem,
        "ci95_halfwidth": tcrit * sem,
        "ci95_t_critical": tcrit,
        "min": min(vals),
        "max": max(vals),
        "n_items_all_passes": len(full),
        "n_items_dropped_partial": len(by_item) - len(full),
        "answer_flip_rate": answer_flips / len(full) if full else None,
        "verdict_flip_rate": verdict_flips / len(full) if full else None,
        "mean_modal_agreement": statistics.mean(modal_agreements) if modal_agreements else None,
        "shortlist_jaccard": statistics.mean(jaccards) if jaccards else None,
        "shortlist_jaccard_median": statistics.median(jaccards) if jaccards else None,
        "mean_distinct_top1": statistics.mean(distinct_top1) if distinct_top1 else None,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-root", default=str(_THREAD / "results"),
                    help="Directory holding <arm>/eval.json subdirectories. "
                         "Reads only. Point --out-json / --out-md at runs/ so "
                         "the aggregate does not land back in the archive.")
    ap.add_argument("--out-json", default=None)
    ap.add_argument("--out-md", default=None)
    args = ap.parse_args()

    root = Path(args.results_root).resolve()
    arms = load_arms(root)
    if not arms:
        print(f"no <arm>/eval.json found under {root}")
        return 1

    report: dict[str, dict] = {}
    md: list[str] = [f"# Taboo (ELK) eval aggregate\n",
                     f"Source: `{root.name}/`, {len(arms)} arm(s).\n"]

    md.append("## Headline\n")
    md.append("| arm | protocol | n | headline | top-5 | top-3 | top-1 | any-of-N | all-of-N | abstained |")
    md.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")

    print(f"{'arm':<18}{'proto':<8}{'n':>5}{'headline':>10}{'top1':>8}"
          f"{'any/N':>8}{'all/N':>8}{'abst':>6}")
    print("-" * 72)

    for name, d in sorted(arms.items()):
        s = d["summary"]
        open_mode = is_open(s)
        pw = s["per_word_top10"] if open_mode else s["per_word"]
        headline = s["top10_recall"] if open_mode else s["accuracy"]
        top1 = s.get("top1_recall")
        proto = "open" if open_mode else "closed"
        nsec = s["n_secrets"]

        report[name] = {
            "protocol": proto,
            "n": s["total"],
            "headline": headline,
            "headline_metric": "top10_recall" if open_mode else "exact_accuracy",
            "top5_recall": s.get("top5_recall"),
            "top3_recall": s.get("top3_recall"),
            "top1_recall": top1,
            "any_of_n": pw["any_of_n"],
            "all_of_n": pw["all_of_n"],
            "n_secrets": nsec,
            "abstained": s["abstained"],
            "judge_model": d.get("judge_model"),
            "repeats": per_pass_stats(d["grades"], open_mode),
        }

        def pct(x):
            return f"{x*100:.1f}%" if isinstance(x, (int, float)) else "-"

        md.append(f"| {name} | {proto} | {s['total']} | **{pct(headline)}** | "
                  f"{pct(s.get('top5_recall'))} | {pct(s.get('top3_recall'))} | "
                  f"{pct(top1)} | {pw['any_of_n']}/{nsec} | {pw['all_of_n']}/{nsec} | "
                  f"{s['abstained']} |")
        print(f"{name:<18}{proto:<8}{s['total']:>5}{pct(headline):>10}{pct(top1):>8}"
              f"{str(pw['any_of_n'])+'/'+str(nsec):>8}"
              f"{str(pw['all_of_n'])+'/'+str(nsec):>8}{s['abstained']:>6}")

    md.append("\nHeadline is exact-match accuracy for closed mode and top-10 recall for open mode. "
              "`any-of-N` counts secret words recovered on at least one prompt, `all-of-N` on every prompt.\n")

    # Repeat / stability section, only for arms that actually have passes.
    rep = {k: v for k, v in report.items() if v["repeats"]}
    if rep:
        md.append("## Run-to-run stability (repeated arms)\n")
        md.append("| arm | passes | mean | SD | 95% CI | min | max | answer flip | verdict flip | modal agree |")
        md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        print(f"\n{'--- stability ---'}")
        for name, v in sorted(rep.items()):
            r = v["repeats"]
            md.append(f"| {name} | {r['n_passes']} | {r['mean']*100:.1f}% | "
                      f"±{r['sd']*100:.1f} | ±{r['ci95_halfwidth']*100:.1f} | "
                      f"{r['min']*100:.1f}% | {r['max']*100:.1f}% | "
                      f"{r['answer_flip_rate']*100:.1f}% | {r['verdict_flip_rate']*100:.1f}% | "
                      f"{r['mean_modal_agreement']*100:.1f}% |")
            print(f"{name:<18} mean={r['mean']*100:5.1f}% SD=±{r['sd']*100:4.1f} "
                  f"SEM=±{r['sem']*100:.2f} 95%CI=±{r['ci95_halfwidth']*100:.2f} "
                  f"range=[{r['min']*100:.1f}, {r['max']*100:.1f}]")
            print(f"{'':<18} answer_flip={r['answer_flip_rate']*100:.1f}%  "
                  f"verdict_flip={r['verdict_flip_rate']*100:.1f}%")
            if r["shortlist_jaccard"] is not None:
                print(f"{'':<18} shortlist Jaccard={r['shortlist_jaccard']:.3f} "
                      f"(median {r['shortlist_jaccard_median']:.3f}), "
                      f"distinct rank-1 answers per item={r['mean_distinct_top1']:.2f}/"
                      f"{r['n_passes']}")
                md.append(f"\n`{name}` shortlist stability: mean pairwise Jaccard "
                          f"**{r['shortlist_jaccard']:.3f}** (median "
                          f"{r['shortlist_jaccard_median']:.3f}), "
                          f"{r['mean_distinct_top1']:.2f} distinct rank-1 answers per item "
                          f"out of {r['n_passes']} passes.\n")
            per = ", ".join(f"p{p}={a*100:.1f}%" for p, a in r["per_pass_accuracy"].items())
            print(f"{'':<18} per-pass: {per}")
            md.append(f"\n`{name}` per-pass: {per}\n")
            if r["n_items_dropped_partial"]:
                note = (f"{r['n_items_dropped_partial']} item(s) missing from at least one pass "
                        f"were excluded from the flip rates.")
                print(f"{'':<18} NOTE: {note}")
                md.append(f"> {note}\n")

        md.append("\n**answer flip** is the share of items whose rank-1 answer is not identical on "
                  "every pass. **verdict flip** is the share whose correctness changes. Answer flip "
                  "well above verdict flip means the oracle is stably wrong in varying ways.\n")

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(report, indent=2) + "\n")
        print(f"\nwrote {args.out_json}")
    if args.out_md:
        Path(args.out_md).write_text("\n".join(md) + "\n")
        print(f"wrote {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
