"""Distinct-aware @5 for the agentic oracle runs: best of the first 5 DISTINCT completions.

WHY THIS EXISTS

`exp_judge.py --grader-topk 5` grades the grader's literal top 5 ROWS. The in-harness
grader scores by completion text and maps one score to every intervention sharing that
text, so identical completions land in adjacent `grader_rank` slots and the top 5 can
hold as few as 3 distinct answers. That makes the rank-based ceiling a best-of-3 on some
runs while it is labelled best-of-5.

This script computes the other reading: walk the ranking until 5 DISTINCT completions
have been collected (depth 6 to 9 in practice, never more than 9 on this arm) and take
the panel max over those. Neither number is "the" answer:

  - rank-based @5 is faithful to "5 committed attempts", where redundancy is a real
    property of the method. If two of your five picks produce the same text, that is
    genuinely what five shots bought you.
  - distinct-aware @5 is faithful to "5 different answers tried", which is the fairer
    reading of an attempt budget and lets the method skip its own redundancy.

Both are reported so the paper can choose, and so the gap between them is visible
rather than hidden inside one headline.

The panel, temperature, repeat count and gateway are inherited from llm_judge exactly,
so the numbers sit on the same instrument as the rank-based pass and the Arditi baseline.
Nothing here re-grades a completion an earlier pass already scored: scores are reused by
RANK (see `cached_scores_by_rank` for why text would be wrong), which is also what keeps
the passes consistent on their shared picks.

Because the picks come out in grader-preference order, a `--topk N` file is also the whole
best-of-1..N curve: the running max over `picks[:n]` is best-of-n. So the deepest pass you
run subsumes every shallower one, and a `--topk 20` file answers @5, @10 and @20 at once.
Give a deeper pass its own `--out-name` and let it `--reuse` the shallower files.

    python -m baselines.arditi.distinct_judge --exp-dir runs/refusal-arm1
    python -m baselines.arditi.distinct_judge --exp-dir runs/refusal-arm1 --slugs a b c
    python -m baselines.arditi.distinct_judge --exp-dir runs/refusal-arm1 \
        --topk 20 --out-name judge_scores_distinct20.json \
        --reuse judge_scores.json judge_scores_distinct.json

This writes its --out-name file INTO each run dir it grades, so --exp-dir must
name a fresh run root. It defaults to runs/. Pointing it at the committed
results/ or results-workshop/ archive edits the archive in place.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO_ROOT)

from circuit_oracle.llm_client import (  # noqa: E402
    LLMClient,
    PROVIDER_CHOICES,
    api_key_names,
    gateway_api_key,
    provider_for,
)

from baselines.arditi.llm_judge import (  # noqa: E402
    resolve_judge_list,
    judge_repeats,
    stats_block,
    apply_refusal_transport,
    fmt_ms,
    summarize_cost,
)
from baselines.arditi.exp_judge import (  # noqa: E402
    collect_exp_runs,
    render_intervention_id,
    rel_run_dir,
    set_exp_dir,
)

TOPK = 5
OUT_NAME_DEFAULT = "judge_scores_distinct.json"
# The rank-based pass only. A deeper pass that wants the shallow distinct scores too
# passes them explicitly, which keeps the default from silently depending on whether
# some other pass happened to run first.
REUSE_DEFAULT = ("judge_scores.json",)


def distinct_picks(run: dict, k: int = TOPK) -> list[dict]:
    """Walk grader_ranking by grader_rank, returning the first k distinct completions.

    Returns one entry per distinct completion, carrying the SHALLOWEST intervention that
    produced it (the grader's own best-ranked representative of that text) plus the depth
    at which it was found. Rows with no grader_rank are skipped, which also drops the
    ungraded nulls that sort to the bottom.
    """
    ivs = {iv.get("rank"): iv for iv in run["interventions"]}
    # An ungraded row still carries a grader_rank (nulls sort to the tail), but the
    # grader expressed no opinion on it, so it is not a candidate the grader "picked".
    # Requiring a non-null overall keeps this pass selecting from scored rows only,
    # which is also what the rank-based pass does implicitly by never reaching the tail.
    ranked = sorted((g for g in (run.get("grader_ranking") or [])
                     if g.get("grader_rank") and g.get("overall") is not None),
                    key=lambda g: g["grader_rank"])
    out: list[dict] = []
    seen: set[str] = set()
    for depth, g in enumerate(ranked, 1):
        iv = ivs.get(g.get("rank"))
        if iv is None:
            continue
        text = iv.get("answer_after") or ""
        if text in seen:
            continue
        seen.add(text)
        out.append({
            "rank": g.get("rank"),
            "grader_rank": g.get("grader_rank"),
            "depth": depth,
            "grader_overall": g.get("overall"),
            "intervention": iv.get("intervention"),
            "intervention_type": iv.get("intervention_type"),
            "intervention_id": render_intervention_id(iv),
            "text": text,
        })
        if len(out) == k:
            break
    return out


def cached_scores_by_rank(run: dict, judge_list, n_repeats: int,
                          temperature: float, filenames=REUSE_DEFAULT) -> dict[int, dict]:
    """Map intervention rank -> per_judge_repeats from earlier passes, if present.

    Keyed by RANK, not by completion text, and that distinction is load-bearing.
    `exp_judge` sorts its intervention rows by pooled score descending before writing
    them, so when one text was scored at several ranks a text-keyed lookup returns
    whichever draw happened to score highest, not the draw belonging to the
    representative this pass actually selected. That silently biases the distinct-aware
    ceiling upward by exactly the duplicate-draw noise this pass exists to remove.
    Keying by rank pins the reuse to the shallowest grader-ranked representative that
    `distinct_picks` chose, and anything not graded before is graded fresh.

    `filenames` is read in order and LATER files lose to earlier ones, so the caller
    controls precedence. Both on-disk shapes are accepted: `exp_judge` writes its rows
    under "interventions", this script writes them under "picks".

    Reuse is refused outright unless the cached panel, repeat count and temperature all
    match the current request, because mixing instruments inside one max is a wrong
    number rather than a crash.
    """
    out: dict[int, dict] = {}
    want = [(m, p) for m, p in judge_list]
    for name in filenames:
        path = os.path.join(run["run_path"], name)
        if not os.path.exists(path):
            continue
        with open(path) as f:
            prev = json.load(f)

        got = [(j.get("model"), j.get("provider")) for j in prev.get("judges") or []]
        if got != want:
            raise SystemExit(
                f"ERROR: {run['slug']} {name} was scored by {got}, but this run "
                f"requests {want}. Reusing it would mix two panels inside one max. "
                "Re-run that pass, or point --judges at the cached panel."
            )
        if prev.get("n_repeats") != n_repeats or prev.get("temperature") != temperature:
            raise SystemExit(
                f"ERROR: {run['slug']} {name} used n_repeats="
                f"{prev.get('n_repeats')} temperature={prev.get('temperature')}, but this "
                f"run requests n_repeats={n_repeats} temperature={temperature}."
            )

        rows = prev.get("interventions")
        if rows is None:
            rows = prev.get("picks") or []
        for row in rows:
            r = row.get("rank")
            if r is not None:
                out.setdefault(r, row.get("per_judge_repeats") or {})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp-dir", dest="exp_dir", default=None)
    ap.add_argument("--judges", nargs="*", default=None)
    ap.add_argument("--judge-provider", dest="judge_provider", default=None,
                    choices=PROVIDER_CHOICES)
    ap.add_argument("--n-repeats", dest="n_repeats", type=int, default=1)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--slugs", nargs="*", default=None)
    ap.add_argument("--topk", type=int, default=TOPK)
    ap.add_argument("--out-name", dest="out_name", default=OUT_NAME_DEFAULT,
                    help="per-run output filename; give a deeper --topk its own name so "
                         "it does not overwrite a shallower pass")
    ap.add_argument("--reuse", nargs="*", default=list(REUSE_DEFAULT),
                    help="per-run filenames to reuse already-graded rows from, in "
                         "precedence order")
    ap.add_argument("--skip-existing", action="store_true",
                    help="skip a run whose --out-name file already exists")
    args = ap.parse_args()

    # These are per-run FILENAMES, not paths. Allowing a path would let "./x.json" and
    # "x.json" name the same file while comparing unequal (so a pass could overwrite the
    # cache it is reading), and an absolute or "../" name would collapse all 50 runs onto
    # one shared file. Rejecting anything but a bare basename closes both at once.
    for label, names in (("--out-name", [args.out_name]), ("--reuse", args.reuse)):
        for nm in names:
            if nm != os.path.basename(nm) or nm in ("", ".", ".."):
                raise SystemExit(
                    f"ERROR: {label} takes a bare filename, got {nm!r}. These name a "
                    "file inside each run dir, so a path would escape it."
                )
    if args.out_name in args.reuse:
        raise SystemExit(
            f"ERROR: --out-name {args.out_name} also appears in --reuse. A pass must "
            "not reuse its own output."
        )

    if args.exp_dir:
        set_exp_dir(args.exp_dir)

    judge_list = resolve_judge_list(args.judges, args.judge_provider)
    needed = {provider_for(name, p) for name, p in judge_list}
    missing = [api_key_names(p) for p in sorted(needed) if not gateway_api_key(p)]
    if missing:
        raise SystemExit(f"ERROR: missing env var(s) {missing} for the judge ensemble.")
    clients = {provider: LLMClient(provider=provider) for _, provider in judge_list}

    runs = collect_exp_runs(slugs=args.slugs)
    print(f"Judges: {judge_list}")
    print(f"Found {len(runs)} run dirs; distinct top-{args.topk}")

    usage_sink: list = []
    n_reused = n_fresh = 0
    for run in runs:
        out_path = os.path.join(run["run_path"], args.out_name)
        if args.skip_existing and os.path.exists(out_path):
            # Existence alone is not "already done". A shallower or differently-judged
            # file under the same name would silently satisfy a deeper request, and the
            # run would then be missing from the deep pass without ever failing. Skip
            # only when the existing file answers at least the question being asked.
            try:
                have = json.load(open(out_path))
            except (json.JSONDecodeError, OSError) as e:
                raise SystemExit(f"ERROR: {run['slug']} {args.out_name} unreadable: {e}")
            same_panel = ([(j.get("model"), j.get("provider"))
                           for j in have.get("judges") or []] == [(m, p) for m, p in judge_list])
            deep_enough = (have.get("topk") or 0) >= args.topk
            same_instrument = (have.get("n_repeats") == args.n_repeats
                               and have.get("temperature") == args.temperature)
            if same_panel and deep_enough and same_instrument:
                print(f"\n--- {run['slug']}: skip (exists) ---")
                continue
            raise SystemExit(
                f"ERROR: {run['slug']} {args.out_name} exists but does not answer this "
                f"request (topk {have.get('topk')} vs {args.topk}, n_repeats "
                f"{have.get('n_repeats')} vs {args.n_repeats}, temperature "
                f"{have.get('temperature')} vs {args.temperature}, panel match "
                f"{same_panel}). Delete it or choose another --out-name."
            )

        picks = distinct_picks(run, args.topk)
        cache = cached_scores_by_rank(run, judge_list, args.n_repeats, args.temperature,
                                      args.reuse)
        print(f"\n--- {run['slug']} ({len(picks)} distinct, deepest="
              f"{picks[-1]['depth'] if picks else 0}) ---")

        rows = []
        for p in picks:
            cached = cache.get(p["rank"])
            # A partial cache row (some judge missing, empty, or short of n_repeats) must
            # NOT be reused: it would quietly shrink the panel for that pick alone, so the
            # max would compare a thin cell against full ones. The header repeat count is
            # checked per file, but a row can still be short of what the header claims, so
            # the row itself is counted here. Grade anything short fresh.
            complete = bool(cached) and all(
                len(cached.get(m) or []) == args.n_repeats for m, _ in judge_list)
            if complete:
                per_judge = {m: [dict(s) for s in cached[m]] for m, _ in judge_list}
                n_reused += 1
                tag = "reused"
            else:
                per_judge = {}
                for model, provider in judge_list:
                    per_judge[model] = judge_repeats(
                        clients[provider], model, run["question"], p["text"],
                        n=args.n_repeats, temperature=args.temperature,
                        usage_sink=usage_sink)
                n_fresh += 1
                tag = "graded"
            per_judge = apply_refusal_transport(per_judge)
            agg = stats_block(
                [s for sc in per_judge.values() for s in sc],
                extra={"n_judges": sum(1 for v in per_judge.values() if v)},
            )
            rows.append({
                "rank": p["rank"], "grader_rank": p["grader_rank"], "depth": p["depth"],
                "grader_overall": p["grader_overall"],
                "intervention": p["intervention"],
                "intervention_type": p["intervention_type"],
                "intervention_id": p["intervention_id"],
                "per_judge_repeats": per_judge,
                "per_judge_stats": {m: stats_block(per_judge[m]) for m, _ in judge_list},
                "aggregate": agg,
            })
            print(f"  depth {p['depth']:>2} rank {p['rank']:>4} {tag:>6}  "
                  f"{p['intervention_id'][:52]:52s} "
                  f"overall={fmt_ms(agg['overall_mean'], agg['overall_simple_std'])}")

        scored = [r for r in rows if r["aggregate"]["overall_mean"] is not None]
        best = max(scored, key=lambda r: r["aggregate"]["overall_mean"]) if scored else None

        with open(out_path, "w") as f:
            json.dump({
                "slug": run["slug"],
                "slug_dir": run["slug_dir"],
                "run_dir": rel_run_dir(run["run_dir"]),
                "question": run["question"],
                "judges": [{"model": m, "provider": p} for m, p in judge_list],
                "n_repeats": args.n_repeats,
                "temperature": args.temperature,
                "topk": args.topk,
                "n_distinct": len(rows),
                "deepest_rank_used": picks[-1]["depth"] if picks else None,
                "picks": rows,
                "best_distinct": ({
                    "intervention_id": best["intervention_id"],
                    "rank": best["rank"], "depth": best["depth"],
                    "aggregate": best["aggregate"],
                } if best else None),
            }, f, indent=2)
        if best is not None:
            print(f"  -> best_distinct overall={best['aggregate']['overall_mean']:.3f} "
                  f"(depth {best['depth']})")
        else:
            print("  -> no scored picks")

    print(f"\nReused {n_reused} already-graded completions, graded {n_fresh} fresh.")
    if usage_sink:
        summarize_cost(usage_sink, args.n_repeats)


if __name__ == "__main__":
    main()
