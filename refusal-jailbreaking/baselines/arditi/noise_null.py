"""Noise-only reference curve (H0) for the best-of-N figure.

WHY THIS EXISTS

Best-of-N is a maximum, and a maximum over noisy measurements rises with N even when
every candidate is identical. For exchangeable draws with per-draw SD sigma the free
lunch is roughly `E[max_N] - mu ~= sigma * sqrt(2 ln N)`, which at N=20 is comparable to
the entire measured @1 -> @5 effect. So an uncontrolled best-of-N curve cannot be read as
"more attempts find better jailbreaks": part of the climb is the judge panel rolling dice.

This script measures that pure-noise climb directly. It takes a handful of completions
spanning the score range, scores each one `--repeats` independent times on the SAME panel,
and writes the running max over those repeats. The item never changes, so every bit of the
rise is noise.

WHAT THIS CURVE IS NOT

It is **not** a correction to subtract from the observed curve. Subtracting it would
overcorrect, because for real candidates

    max_i (mu_i + eps_i)  !=  (max_i mu_i) + (max_i eps_i).

When one candidate is genuinely better than the rest it wins on nearly every draw, so
noise adds almost nothing to the max. The identical-candidate case is the WORST case, so
this curve is an upper bound on how much of a rise noise can explain, and its honest use
is as the H0 reference plotted underneath the observed curve: "this is the climb you would
see if every candidate were equally good".

The actual winner's-curse correction is cross-fitting over judges (select the argmax with
four judges, score it with the held-out fifth), which makes selection and evaluation
independent and costs no API calls. That lives in the results generator, not here. This
script calibrates sigma and supplies the H0 band.

Pairing matters: a null "draw" is one score per judge, and the panel overall is the mean
across judges, exactly as in the real pipeline. So repeat index i is paired ACROSS judges
to form draw i, and refusal transport is applied within that draw (a refusal is imputed
from the judges that did score in the same draw, never from a different draw).

    python -m baselines.arditi.noise_null --exp-dir runs/refusal-arm1 \
        --n-completions 10 --repeats 20

--exp-dir is read-only here. The null lands under runs/noise_null/ unless --out
says otherwise, so pointing --exp-dir at the committed results/ or
results-workshop/ archive still writes nothing into it.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics as st
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
    apply_refusal_transport,
    summarize_cost,
)
import baselines.arditi.exp_judge as _exp_judge  # noqa: E402
from baselines.arditi.exp_judge import (  # noqa: E402
    collect_exp_runs,
    render_intervention_id,
    set_exp_dir,
)
from baselines.arditi.distinct_judge import distinct_picks


def stratified_sample(runs: list[dict], n: int, topk: int) -> list[dict]:
    """Pick n completions spread evenly across the observed grader-score range.

    Sampling the top of the ranking only would understate the null, because a completion
    pinned near the ceiling cannot rise much no matter how noisy the panel is. Spreading
    over the range keeps the null representative of the candidates the real curve maxes
    over. Selection uses the grader's own score, not the panel's, so this pass never
    peeks at the quantity it is about to measure.
    """
    pool = []
    for run in runs:
        for p in distinct_picks(run, topk):
            if p["grader_overall"] is not None:
                pool.append({"slug": run["slug"], "run_path": run["run_path"],
                             "question": run["question"], **p})
    if n < 1:
        raise SystemExit(f"ERROR: --n-completions must be at least 1, got {n}.")
    if not pool:
        raise SystemExit("ERROR: no scored picks found to sample from.")
    if n > len(pool):
        raise SystemExit(
            f"ERROR: asked for {n} completions but only {len(pool)} scored picks exist. "
            "Lower --n-completions or raise --topk."
        )
    pool.sort(key=lambda p: p["grader_overall"])
    # Even quantile spacing over the sorted pool, endpoints included. Spacing is at
    # least 1 whenever n <= len(pool), so these indices are already distinct. A single
    # completion takes the MEDIAN rather than the minimum, since the bottom of the range
    # is the least representative point to calibrate noise at.
    if n == 1:
        idx = [(len(pool) - 1) // 2]
    else:
        idx = [round(i * (len(pool) - 1) / (n - 1)) for i in range(n)]
    return [pool[i] for i in idx]


def draw_overalls(per_judge: dict, judge_list, n_draws: int) -> list[float]:
    """Collapse per-judge repeat lists into one panel overall per draw index."""
    out = []
    for i in range(n_draws):
        drawn = {}
        for model, _ in judge_list:
            scores = per_judge.get(model) or []
            drawn[model] = [scores[i]] if i < len(scores) else []
        drawn = apply_refusal_transport(drawn)
        vals = [(float(s["usability"]) + float(s["plausibility"])) / 2
                for scs in drawn.values() for s in scs
                if s.get("usability") is not None and s.get("plausibility") is not None]
        if vals:
            out.append(st.mean(vals))
    return out


def running_max(vals: list[float]) -> list[float]:
    out, best = [], None
    for v in vals:
        best = v if best is None else max(best, v)
        out.append(best)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp-dir", dest="exp_dir", default=None)
    ap.add_argument("--judges", nargs="*", default=None)
    ap.add_argument("--judge-provider", dest="judge_provider", default=None,
                    choices=PROVIDER_CHOICES)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--repeats", type=int, default=20,
                    help="independent panel draws per completion; sets the null's max N")
    ap.add_argument("--n-completions", dest="n_completions", type=int, default=10)
    ap.add_argument("--topk", type=int, default=20,
                    help="depth of the distinct pool the sample is drawn from")
    ap.add_argument("--out", default=None,
                    help="output json (default runs/noise_null/<exp-dir name>.json, "
                         "under the gitignored fresh-run root, never inside --exp-dir)")
    args = ap.parse_args()

    if args.exp_dir:
        set_exp_dir(args.exp_dir)

    judge_list = resolve_judge_list(args.judges, args.judge_provider)
    needed = {provider_for(name, p) for name, p in judge_list}
    missing = [api_key_names(p) for p in sorted(needed) if not gateway_api_key(p)]
    if missing:
        raise SystemExit(f"ERROR: missing env var(s) {missing} for the judge ensemble.")
    clients = {provider: LLMClient(provider=provider) for _, provider in judge_list}

    runs = collect_exp_runs()
    sample = stratified_sample(runs, args.n_completions, args.topk)
    print(f"Judges: {judge_list}")
    print(f"Null: {len(sample)} completions x {args.repeats} draws x {len(judge_list)} "
          f"judges = {len(sample) * args.repeats * len(judge_list)} calls")

    usage_sink: list = []
    items = []
    for c in sample:
        per_judge = {}
        for model, provider in judge_list:
            per_judge[model] = judge_repeats(
                clients[provider], model, c["question"], c["text"],
                n=args.repeats, temperature=args.temperature, usage_sink=usage_sink)
        overalls = draw_overalls(per_judge, judge_list, args.repeats)
        if not overalls:
            print(f"  {c['slug']} rank {c['rank']}: no usable draws, dropped")
            continue
        rmax = running_max(overalls)
        items.append({
            "slug": c["slug"], "rank": c["rank"], "depth": c["depth"],
            "intervention_id": render_intervention_id(
                {"intervention": c["intervention"],
                 "intervention_type": c["intervention_type"]}),
            "grader_overall": c["grader_overall"],
            "draw_overalls": overalls,
            "running_max": rmax,
            "mean": st.mean(overalls),
            "sd": st.stdev(overalls) if len(overalls) > 1 else 0.0,
        })
        print(f"  {c['slug'][:34]:34s} rank {c['rank']:>4}  mean={items[-1]['mean']:.3f} "
              f"sd={items[-1]['sd']:.3f}  max@{len(rmax)}={rmax[-1]:.3f} "
              f"(+{rmax[-1] - items[-1]['mean']:.3f})")

    if not items:
        raise SystemExit("ERROR: every sampled completion failed to score.")

    # The null curve is the mean across completions of (running max at N) - (that
    # completion's own mean). Centring per completion first is what makes it a pure
    # noise quantity: the level of any one completion is irrelevant, only the climb is.
    # Read as an UPPER BOUND on the noise share of an observed rise, never subtracted
    # from it (see the module docstring).
    n_max = min(len(it["running_max"]) for it in items)
    curve = [st.mean([it["running_max"][i] - it["mean"] for it in items])
             for i in range(n_max)]
    print("\nnoise-only inflation (H0: all candidates equal), E[max_N] - mu:")
    for n in (1, 2, 5, 10, 20):
        if n <= n_max:
            print(f"  N={n:>2}  +{curve[n - 1]:.4f}")

    # Never inside --exp-dir. That directory is often one of the committed
    # archives (results/, results-workshop/), which no command writes to.
    if args.out:
        out_path = os.path.abspath(args.out)
    else:
        name = os.path.basename(os.path.normpath(_exp_judge.EXP_DIR)) or "noise_null"
        out_path = os.path.join(REPO_ROOT, "runs", "noise_null", f"{name}.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({
            "judges": [{"model": m, "provider": p} for m, p in judge_list],
            "temperature": args.temperature,
            "repeats": args.repeats,
            "n_completions": len(items),
            "pooled_sd": st.mean([it["sd"] for it in items]),
            "curve_excess_over_mean": curve,
            "items": items,
        }, f, indent=2)
    print(f"\nwrote {out_path}")
    if usage_sink:
        summarize_cost(usage_sink, args.repeats)


if __name__ == "__main__":
    main()
