"""
Evaluate the judge's spuriosity verdicts from judge_sae_features.py.

For each result JSON in probe_artifacts/sae_analysis/, which holds both feature
types (see ANALYSIS_DIRS):
  - biased ranking  → judge should say YES (spurious features present)
  - unbiased ranking → judge should say NO  (no spurious features)

Prints a report and appends it to spurious-correlation/runs/spuriosity/judge_eval.md.
It reads the committed verdicts in probe_artifacts/sae_analysis/ by default and
never writes into them. probe_artifacts/spuriosity/judge_eval.md is the archived
report behind the published baseline and is left alone.

Usage:
    python spurious-correlation/scripts/eval_sae_judge_spuriosity.py
    python spurious-correlation/scripts/eval_sae_judge_spuriosity.py --type plt
    python spurious-correlation/scripts/eval_sae_judge_spuriosity.py --type sae
    python spurious-correlation/scripts/eval_sae_judge_spuriosity.py --dataset bib_journalist_dietitian
"""

import argparse
import json
import re
import sys
from pathlib import Path

# This file lives in spurious-correlation/scripts/, so the task root (which holds
# probe_artifacts/sae_analysis/ and probe_artifacts/spuriosity/) is one level up.
_HERE      = Path(__file__).resolve().parent
_TASK_ROOT = _HERE.parent
# The report is appended to, so it must not default into the committed
# probe_artifacts/spuriosity/ archive. runs/ is gitignored.
OUT_MD  = _TASK_ROOT / "runs" / "spuriosity" / "judge_eval.md"

# Both feature types share one verdict directory. They are told apart by the glob
# below, not by the path. The default is the committed archive, which is what
# reproduces the published baseline. --analysis-dir repoints it, and a fresh
# judge run lands in runs/sae_analysis/ (judge_sae_features.py --out-dir), so
# pass --analysis-dir spurious-correlation/runs/sae_analysis to score a re-judge.
# Without that flag the re-run and the scorer disagree silently and the eval
# keeps reporting the older numbers.
ANALYSIS_DIRS = {
    "plt": _TASK_ROOT / "probe_artifacts" / "sae_analysis",
    "sae": _TASK_ROOT / "probe_artifacts" / "sae_analysis",
}

ANALYSIS_GLOB = {
    "plt": "*-transcoder-*.json",
    "sae": "*-sae-*.json",
}


# ── Verdict parsing ────────────────────────────────────────────────────────────

def parse_verdict(analysis: str) -> str | None:
    """
    Extract YES or NO from the LLM analysis text.
    Looks for 'Verdict: YES/NO' first, then falls back to the first YES/NO word.
    Returns 'YES', 'NO', or None if unparseable.
    """
    m = re.search(r"Verdict[:\s]+\**(YES|NO)\**", analysis, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    m = re.search(r"\b(YES|NO)\b", analysis)
    if m:
        return m.group(1).upper()
    return None


# ── Loading ────────────────────────────────────────────────────────────────────

def load_results(feat_type: str) -> list[dict]:
    d = ANALYSIS_DIRS[feat_type]
    if not d.exists():
        return []
    results = []
    for path in sorted(d.glob(ANALYSIS_GLOB[feat_type])):
        with open(path) as f:
            data = json.load(f)
        verdict = parse_verdict(data.get("analysis", ""))
        ranking = data.get("ranking", "unknown")
        expected = "YES" if ranking == "biased" else "NO"
        correct  = verdict == expected if verdict else None
        results.append({
            "path":     path,
            "stem":     path.stem,                     # e.g. bib_journalist_dietitian-pos_pos_1-transcoder-biased
            "dataset":  data.get("dataset", "unknown"),
            "prompt":   data.get("prompt", ""),
            "ranking":  ranking,
            "verdict":  verdict,
            "expected": expected,
            "correct":  correct,
            "feat_type": feat_type,
        })
    return results


# ── Output ─────────────────────────────────────────────────────────────────────

_lines: list[str] = []

def emit(line: str = "") -> None:
    print(line, flush=True)
    _lines.append(line)


# ── Report helpers ─────────────────────────────────────────────────────────────

def prompt_tag(stem: str) -> str:
    """Extract the short prompt tag from the file stem, e.g. 'pos_pos_1'."""
    parts = stem.rsplit("-", 1)[0]  # strip trailing -biased/-unbiased
    # stem: {dataset}-{tag}-{feat_type}-{ranking}  or  {dataset}-{tag}-{feat_type}
    # remove dataset prefix and feat_type suffix
    m = re.search(r"-((?:pos|neg)_(?:pos|neg)_\d+)", parts)
    if m:
        return m.group(1)
    return parts


def verdict_mark(correct: bool | None) -> str:
    if correct is True:
        return "✓"
    if correct is False:
        return "✗"
    return "?"


def report_dataset_type(dataset: str, feat_type: str, rows: list[dict]) -> None:
    emit(f"## {dataset}, {feat_type}")
    emit()

    # Group by prompt tag, then split biased/unbiased
    by_tag: dict[str, dict] = {}
    for r in rows:
        tag = prompt_tag(r["stem"])
        by_tag.setdefault(tag, {})
        by_tag[tag][r["ranking"]] = r

    col_w = 12
    header = f"  {'Prompt':<18} {'Biased':>{col_w}} {'Unbiased':>{col_w}}  {'B✓':>4}  {'U✓':>4}"
    emit(header)
    emit("  " + "-" * (len(header) - 2))

    b_correct_total = b_total = u_correct_total = u_total = 0

    for tag in sorted(by_tag):
        b = by_tag[tag].get("biased")
        u = by_tag[tag].get("unbiased")

        b_str = (b["verdict"] or "?") if b else "-"
        u_str = (u["verdict"] or "?") if u else "-"
        bm    = verdict_mark(b["correct"] if b else None)
        um    = verdict_mark(u["correct"] if u else None)

        emit(f"  {tag:<18} {b_str:>{col_w}} {u_str:>{col_w}}  {bm:>4}  {um:>4}")

        if b:
            b_total += 1
            if b["correct"]:
                b_correct_total += 1
        if u:
            u_total += 1
            if u["correct"]:
                u_correct_total += 1

    emit()
    b_pct = 100 * b_correct_total / b_total if b_total else 0
    u_pct = 100 * u_correct_total / u_total if u_total else 0
    emit(f"  Biased   accuracy: {b_correct_total}/{b_total}  ({b_pct:.1f}%)   (expected YES, spurious signal present)")
    emit(f"  Unbiased accuracy: {u_correct_total}/{u_total}  ({u_pct:.1f}%)   (expected NO, no spurious signal)")
    emit()


def report_summary(all_results: list[dict]) -> None:
    emit("## Summary")
    emit()

    col_w = 12
    header = f"  {'Dataset':<32} {'Type':<6} {'Biased':>{col_w}} {'Unbiased':>{col_w}}"
    emit(header)
    emit("  " + "-" * (len(header) - 2))

    total_b_correct = total_b = total_u_correct = total_u = 0

    seen: set[tuple] = set()
    for r in all_results:
        key = (r["dataset"], r["feat_type"])
        if key in seen:
            continue
        seen.add(key)

        subset = [x for x in all_results if x["dataset"] == r["dataset"] and x["feat_type"] == r["feat_type"]]
        b_sub = [x for x in subset if x["ranking"] == "biased"]
        u_sub = [x for x in subset if x["ranking"] == "unbiased"]

        bc = sum(x["correct"] or False for x in b_sub)
        uc = sum(x["correct"] or False for x in u_sub)

        b_str = f"{bc}/{len(b_sub)} ({100*bc/len(b_sub):.0f}%)" if b_sub else "-"
        u_str = f"{uc}/{len(u_sub)} ({100*uc/len(u_sub):.0f}%)" if u_sub else "-"
        emit(f"  {r['dataset']:<32} {r['feat_type']:<6} {b_str:>{col_w}} {u_str:>{col_w}}")

        total_b_correct += bc
        total_b         += len(b_sub)
        total_u_correct += uc
        total_u         += len(u_sub)

    emit()
    b_pct = 100 * total_b_correct / total_b if total_b else 0
    u_pct = 100 * total_u_correct / total_u if total_u else 0
    emit(f"  Overall biased   accuracy: {total_b_correct}/{total_b}  ({b_pct:.1f}%)")
    emit(f"  Overall unbiased accuracy: {total_u_correct}/{total_u}  ({u_pct:.1f}%)")
    emit()


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    global OUT_MD
    parser = argparse.ArgumentParser()
    parser.add_argument("--type",    choices=["plt", "sae", "all"], default="all")
    parser.add_argument("--dataset", default=None, help="Filter to one dataset slug")
    parser.add_argument("--analysis-dir", default=None,
                        help="Directory of judge verdicts to score "
                             "(default probe_artifacts/sae_analysis, the committed "
                             "archive). Match this to judge_sae_features.py --out-dir, "
                             "which defaults to runs/sae_analysis.")
    parser.add_argument("--out-md", default=None,
                        help=f"Report file to APPEND to (default {OUT_MD}).")
    args = parser.parse_args()

    if args.analysis_dir:
        d = Path(args.analysis_dir).resolve()
        if not d.is_dir():
            parser.error(f"--analysis-dir does not exist: {d}")
        ANALYSIS_DIRS["plt"] = d
        ANALYSIS_DIRS["sae"] = d

    if args.out_md:
        OUT_MD = Path(args.out_md).resolve()

    types_to_run = ["plt", "sae"] if args.type == "all" else [args.type]

    all_results: list[dict] = []
    for ft in types_to_run:
        rows = load_results(ft)
        if args.dataset:
            rows = [r for r in rows if r["dataset"] == args.dataset]
        all_results.extend(rows)

    if not all_results:
        print("No result files found.", file=sys.stderr)
        sys.exit(1)

    emit("# Judge Spuriosity Evaluation")
    emit()
    emit("Verdict key: **YES** = spurious features present, **NO** = no spurious features")
    emit("Correct (✓): biased ranking → YES, unbiased ranking → NO")
    emit()

    # Report per (dataset, feat_type)
    seen: set[tuple] = set()
    for r in all_results:
        key = (r["dataset"], r["feat_type"])
        if key in seen:
            continue
        seen.add(key)
        subset = [x for x in all_results if x["dataset"] == r["dataset"] and x["feat_type"] == r["feat_type"]]
        report_dataset_type(r["dataset"], r["feat_type"], subset)

    report_summary(all_results)

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with OUT_MD.open("a") as f:
        f.write("\n".join(_lines) + "\n")
    print(f"Written to {OUT_MD}", flush=True)


if __name__ == "__main__":
    main()
