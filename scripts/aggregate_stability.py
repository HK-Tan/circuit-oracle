#!/usr/bin/env python3
"""Traversal-stability aggregator for the arm-1 repeat passes.

One script for both the refusal and the probes task, so do not write a second
one. It runs post hoc over saved run artifacts, no harness involvement and no
re-runs. All inputs already exist in every run directory.

What it computes, per slug across that slug's repeat passes, then averaged:

  pinned-feature Jaccard      from pinned_ids.json          (committed indicator)
  inspected-feature Jaccard   from oracle_result.json        (committed indicator)
  tool-call count mean and SD from oracle_result.json
  top-1 committed-intervention agreement (refusal only)
                              from judge_scores.json best_intervention
  flagged spurious-set and causal-set Jaccard (probes only)
                              from judge_feature_counts.json
  verdict flip rate (probes only, the canonical `dominant` rule)
                              from judge_feature_counts.json
                              Pairwise: the fraction of pass PAIRS that
                              disagree, matching the Jaccards above. The
                              plurality-dissent version is reported alongside
                              as `verdict_modal_dissent`, and is a different
                              (smaller) quantity, not an alternative name.

Feature identity, decided 2026-07-27:
  Three levels are reported side by side, because raw Jaccard undersells the
  "destinations agree" half of the claim when equivalent features substitute.
    feature : (layer, feature_idx), position dropped, pseudo-nodes (layer < 0)
              dropped. The committed lower bound on mechanistic agreement.
    layer   : the set of layers touched. Destination agreement one level up.
    band    : early/mid/late thirds of the subject depth (needs --n-layers).
  Supernode-level identity was considered and rejected: supernodes are
  run-specific groupings, so there is no cross-run identity to compare.

Refusal verdict flip rate is deliberately absent. The win / softened /
no-shift verdict comes from the external judge stage over committed picks,
not from any per-run artifact, so bucketing a score here would invent
thresholds the judges own. Top-1 agreement plus the top-1 overall-score SD
are the per-artifact stand-ins.

Pass identity: `pass_index` in oracle_result.json wins (written by the
runners with --pass-index), then a `_pass<N>` directory suffix, then
timestamp order with a warning (legacy layout). Duplicate pass indices
keep the latest run directory and warn, which is the retried-pass case.

Usage:
    python scripts/aggregate_stability.py --track refusal \
        --runs-root refusal-jailbreaking/runs/refusal-arm1 [--out stability.json]
    python scripts/aggregate_stability.py --track probes \
        --runs-root spurious-correlation/runs/probes-arm1

Point --runs-root at ONE arm's output root, and at a fresh repeat batch under
<task>/runs/. Mixing arms in one root would average across configurations and
mean nothing.

The committed <task>/results/ archives are sampled: three slugs per arm keep
their oracle_result.json and the rest keep only report.md, so pointing this
script at results/ cannot reproduce the stability table. It warns when it sees
that shape.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

TRACK_DEFAULT_N_LAYERS = {"refusal": 36, "probes": 26}

_FLAGGED_ID_RE = re.compile(r"^L(\d+):F(\d+)$")
_PASS_SUFFIX_RE = re.compile(r"_pass(\d+)$")


# ---------------------------------------------------------------------------
# Per-artifact parsers. Each returns plain sets so the math below is uniform.
# ---------------------------------------------------------------------------

def parse_pinned(pinned_ids_path: Path, n_layers: int | None = None) -> set[tuple[int, int]]:
    """(layer, feature_idx) pairs from pinned_ids.json.

    Entries are "layer_feature_pos" strings. Position is dropped (one feature
    pinned at two positions is one mechanism) and pseudo-nodes are dropped.

    Pseudo-nodes sit at BOTH ends of the layer range, which the layer < 0 test
    alone does not catch. Token nodes are negative, but the logit/probe node is
    encoded as layer == n_layers, one past the last real transcoder layer. On
    gemma-2-2b (26 layers, valid 0..25) that is the single node `26_0`, found in
    119 of 8695 pinned entries across the arm-1 repeat passes on 2026-07-28, and
    it was being counted as if it were a transcoder feature.

    Excluding it RAISES the stability numbers (feature 0.504 -> 0.511, layer
    0.722 -> 0.754, band 0.857 -> 0.959), because a node present in only one
    pass of a pair contributes pure disagreement, and in the coarse band
    representation it drags in a whole band.

    n_layers=None keeps the old behaviour (no upper bound) so a caller that does
    not know the subject depth still parses rather than silently over-filtering.
    """
    data = json.loads(pinned_ids_path.read_text())
    out: set[tuple[int, int]] = set()
    for entry in data.get("pinnedIds", []):
        parts = entry.split("_")
        if len(parts) != 3:
            raise ValueError(f"unparseable pinned id {entry!r} in {pinned_ids_path}")
        layer, feature = int(parts[0]), int(parts[1])
        if layer < 0:
            continue
        if n_layers is not None and layer >= n_layers:
            continue
        out.add((layer, feature))
    return out


def parse_inspected(oracle_result: dict) -> set[tuple[int, int]]:
    """(layer, feature_idx) pairs handed to inspect_feature."""
    out: set[tuple[int, int]] = set()
    for call in oracle_result.get("tool_calls", []):
        if call.get("tool") != "inspect_feature":
            continue
        inp = call.get("input", {})
        if "layer" in inp and "feature_idx" in inp:
            out.add((int(inp["layer"]), int(inp["feature_idx"])))
    return out


def parse_flagged(judge_feature_counts: dict) -> tuple[set, set, str | None, int]:
    """(spurious set, causal set, dominant verdict, n_non_feature) from the probes judge file.

    The judge echoes whatever id the report cited, and reports legitimately
    cite non-transcoder graph nodes: embeddings ("Emb: 'His' (pos 1)"), the
    output node, the probe direction. Those have no (layer, feature) identity,
    so they are excluded from the feature Jaccard by design and counted so the
    exclusion is visible rather than silent (329 such ids across the archived
    run files, surveyed 2026-07-27).
    """
    n_skipped = 0

    def ids(key: str) -> set[tuple[int, int]]:
        nonlocal n_skipped
        out = set()
        for row in judge_feature_counts.get(key) or []:
            m = _FLAGGED_ID_RE.match(str(row.get("id", "")))
            if not m:
                n_skipped += 1
                continue
            out.add((int(m.group(1)), int(m.group(2))))
        return out

    spurious, causal = ids("spurious_features"), ids("causal_features")
    return spurious, causal, judge_feature_counts.get("dominant"), n_skipped


def top1_features(judge_scores: dict) -> frozenset[tuple[int, int]] | None:
    """Feature-level identity of the run's committed top-1 intervention.

    Single interventions give a one-element set, supernodes the set of member
    features. None when the grader recorded no best_intervention.
    """
    best = judge_scores.get("best_intervention")
    if not best:
        return None
    iv = best.get("intervention", {})
    if iv.get("type") == "single":
        return frozenset({(int(iv["layer"]), int(iv["feature_idx"]))})
    if iv.get("type") == "supernode":
        return frozenset(
            (int(f["layer"]), int(f["feature_idx"])) for f in iv.get("features", [])
        )
    return None


def top1_overall(judge_scores: dict) -> float | None:
    best = judge_scores.get("best_intervention")
    if not best:
        return None
    val = (best.get("aggregate") or {}).get("overall_mean")
    return float(val) if val is not None else None


# ---------------------------------------------------------------------------
# Identity coarsening and set math
# ---------------------------------------------------------------------------

def to_layers(features: set[tuple[int, int]]) -> set[int]:
    return {layer for layer, _ in features}


def to_bands(features: set[tuple[int, int]], n_layers: int) -> set[int]:
    """Early/mid/late thirds. Band index 0, 1, or 2."""
    return {min(2, layer * 3 // n_layers) for layer, _ in features}


def jaccard(a: set, b: set) -> float:
    """|a & b| / |a | b|. Two empty sets agree perfectly by convention."""
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def mean_pairwise_jaccard(sets: list[set]) -> float | None:
    pairs = list(itertools.combinations(sets, 2))
    if not pairs:
        return None
    return sum(jaccard(a, b) for a, b in pairs) / len(pairs)


def sample_sd(values: list[float]) -> float | None:
    """SD with ddof=1, matching 'SD estimated from the reruns directly'."""
    if len(values) < 2:
        return None
    mean = sum(values) / len(values)
    return math.sqrt(sum((v - mean) ** 2 for v in values) / (len(values) - 1))


# ---------------------------------------------------------------------------
# Run discovery
# ---------------------------------------------------------------------------

@dataclass
class RunRecord:
    run_dir: Path
    slug: str
    pass_index: int | None
    has_pinned: bool = False
    pinned: set = field(default_factory=set)
    inspected: set = field(default_factory=set)
    n_tool_calls: int = 0
    spurious: set | None = None
    causal: set | None = None
    dominant: str | None = None
    top1: frozenset | None = None
    top1_score: float | None = None


def _resolve_pass_index(run_dir: Path, oracle_result: dict) -> int | None:
    if oracle_result.get("pass_index") is not None:
        return int(oracle_result["pass_index"])
    m = _PASS_SUFFIX_RE.search(run_dir.name)
    if m:
        return int(m.group(1))
    return None


def load_run(run_dir: Path, warnings: list[str],
             n_layers: int | None = None) -> RunRecord | None:
    result_path = run_dir / "oracle_result.json"
    try:
        oracle_result = json.loads(result_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        warnings.append(f"SKIP {run_dir}: unreadable oracle_result.json ({exc})")
        return None

    slug = run_dir.parent.name
    rec = RunRecord(
        run_dir=run_dir,
        slug=slug,
        pass_index=_resolve_pass_index(run_dir, oracle_result),
        inspected=parse_inspected(oracle_result),
        n_tool_calls=len(oracle_result.get("tool_calls", [])),
    )

    pinned_path = run_dir / "pinned_ids.json"
    if pinned_path.exists():
        rec.has_pinned = True
        rec.pinned = parse_pinned(pinned_path, n_layers)
    else:
        warnings.append(f"{run_dir}: no pinned_ids.json, pinned Jaccard skips this pass")

    counts_path = run_dir / "judge_feature_counts.json"
    if counts_path.exists():
        rec.spurious, rec.causal, rec.dominant, n_pseudo = parse_flagged(
            json.loads(counts_path.read_text())
        )
        if n_pseudo:
            warnings.append(
                f"{run_dir}: {n_pseudo} flagged id(s) are pseudo-nodes "
                f"(embedding/output/probe), excluded from the feature Jaccard"
            )

    scores_path = run_dir / "judge_scores.json"
    if scores_path.exists():
        scores = json.loads(scores_path.read_text())
        rec.top1 = top1_features(scores)
        rec.top1_score = top1_overall(scores)

    return rec


def discover_runs(runs_root: Path, warnings: list[str],
                  n_layers: int | None = None) -> dict[str, list[RunRecord]]:
    """Group run directories by slug (the exp-* directory name).

    Within a slug, duplicate pass indices keep the lexicographically latest
    run directory (timestamps sort correctly), which is the retried-pass case.
    Runs with no pass index at all are ordered by directory name and warned
    about, so the legacy layout still parses.
    """
    groups: dict[str, list[RunRecord]] = {}
    result_paths = sorted(runs_root.rglob("oracle_result.json"))

    # A sampled archive keeps report.md for every run but oracle_result.json for
    # only a few, and stability needs the latter for every pass. Say so rather
    # than quietly averaging whatever survived.
    n_reports = sum(1 for _ in runs_root.rglob("report.md"))
    if n_reports > len(result_paths):
        warnings.append(
            f"{n_reports} report.md file(s) under {runs_root} but only "
            f"{len(result_paths)} oracle_result.json. This looks like a sampled "
            f"archive, not a full repeat batch, so the numbers below cover only "
            f"the runs that kept their artifacts"
        )

    for result_path in result_paths:
        rec = load_run(result_path.parent, warnings, n_layers)
        if rec is not None:
            groups.setdefault(rec.slug, []).append(rec)

    for slug, recs in groups.items():
        recs.sort(key=lambda r: r.run_dir.name)
        indexed = [r for r in recs if r.pass_index is not None]
        if indexed and len(indexed) < len(recs):
            warnings.append(
                f"{slug}: {len(recs) - len(indexed)} run(s) without a pass index "
                f"alongside indexed ones, all are included"
            )
        if not indexed and len(recs) > 1:
            warnings.append(
                f"{slug}: no pass indices recorded, using directory-name order "
                f"(legacy layout)"
            )
        by_index: dict[int, RunRecord] = {}
        keep: list[RunRecord] = []
        for r in recs:
            if r.pass_index is None:
                keep.append(r)
                continue
            if r.pass_index in by_index:
                warnings.append(
                    f"{slug}: duplicate pass {r.pass_index}, keeping "
                    f"{r.run_dir.name} over {by_index[r.pass_index].run_dir.name}"
                )
            by_index[r.pass_index] = r
        keep.extend(by_index.values())
        keep.sort(key=lambda r: (r.pass_index if r.pass_index is not None else -1,
                                 r.run_dir.name))
        groups[slug] = keep
    return groups


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate_slug(recs: list[RunRecord], track: str, n_layers: int) -> dict:
    out: dict = {
        "n_passes": len(recs),
        "pass_indices": [r.pass_index for r in recs],
        "run_dirs": [str(r.run_dir) for r in recs],
    }

    # An empty pinned set from a real file counts (the agent pinned nothing,
    # which is signal). A missing file does not.
    pinned = [r.pinned for r in recs if r.has_pinned]
    out["pinned_jaccard_feature"] = mean_pairwise_jaccard(pinned)
    out["pinned_jaccard_layer"] = mean_pairwise_jaccard([to_layers(s) for s in pinned])
    out["pinned_jaccard_band"] = mean_pairwise_jaccard(
        [to_bands(s, n_layers) for s in pinned]
    )

    inspected = [r.inspected for r in recs]
    out["inspected_jaccard_feature"] = mean_pairwise_jaccard(inspected)

    counts = [float(r.n_tool_calls) for r in recs]
    out["tool_calls_mean"] = sum(counts) / len(counts)
    out["tool_calls_sd"] = sample_sd(counts)

    if track == "probes":
        flagged = [r for r in recs if r.spurious is not None]
        if len(flagged) >= 2:
            out["spurious_jaccard_feature"] = mean_pairwise_jaccard(
                [r.spurious for r in flagged]
            )
            out["causal_jaccard_feature"] = mean_pairwise_jaccard(
                [r.causal for r in flagged]
            )
        verdicts = [r.dominant for r in recs if r.dominant is not None]
        if verdicts:
            out["verdicts"] = verdicts
            # Pairwise disagreement, the fraction of pass PAIRS whose verdicts
            # differ. Deliberately the same shape as every Jaccard above, which
            # is also mean-pairwise, so one slug's indicators are all reading
            # the same kind of quantity. For [A, A, B] this is 2/3.
            pairs = list(itertools.combinations(verdicts, 2))
            if pairs:
                out["verdict_flip_rate"] = sum(a != b for a, b in pairs) / len(pairs)
            # Secondary and NOT the headline: fraction of passes dissenting
            # from the plurality verdict. Same data, smaller number (1/3 for
            # the case above). Reported so the two are never confused.
            modal = max(set(verdicts), key=verdicts.count)
            out["verdict_modal_dissent"] = 1.0 - verdicts.count(modal) / len(verdicts)

    if track == "refusal":
        tops = [r.top1 for r in recs if r.top1 is not None]
        pairs = list(itertools.combinations(tops, 2))
        if pairs:
            out["top1_agreement"] = sum(a == b for a, b in pairs) / len(pairs)
        scores = [r.top1_score for r in recs if r.top1_score is not None]
        if len(scores) >= 2:
            out["top1_overall_sd"] = sample_sd(scores)

    return out


def aggregate(groups: dict[str, list[RunRecord]], track: str, n_layers: int) -> dict:
    slugs: dict[str, dict] = {}
    skipped: list[str] = []
    for slug, recs in sorted(groups.items()):
        if len(recs) < 2:
            skipped.append(slug)
            continue
        slugs[slug] = aggregate_slug(recs, track, n_layers)

    def mean_of(key: str) -> float | None:
        vals = [s[key] for s in slugs.values() if s.get(key) is not None]
        return sum(vals) / len(vals) if vals else None

    overall_keys = [
        "pinned_jaccard_feature", "pinned_jaccard_layer", "pinned_jaccard_band",
        "inspected_jaccard_feature", "tool_calls_sd",
        "spurious_jaccard_feature", "causal_jaccard_feature",
        "verdict_flip_rate", "verdict_modal_dissent",
        "top1_agreement", "top1_overall_sd",
    ]
    return {
        "track": track,
        "n_layers": n_layers,
        "n_slugs": len(slugs),
        "skipped_single_pass_slugs": skipped,
        "overall": {k: mean_of(k) for k in overall_keys},
        "per_slug": slugs,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _fmt(v: float | None) -> str:
    return f"{v:.3f}" if isinstance(v, float) else "-"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--track", required=True, choices=("refusal", "probes"))
    parser.add_argument("--runs-root", required=True, type=Path,
                        help="ONE arm's output root, walked recursively")
    parser.add_argument("--n-layers", type=int, default=None,
                        help="Subject depth for the band identity "
                             "(default 36 refusal, 26 probes)")
    parser.add_argument("--out", type=Path, default=None,
                        help="Write the full result as JSON here")
    args = parser.parse_args()

    n_layers = args.n_layers or TRACK_DEFAULT_N_LAYERS[args.track]
    if not args.runs_root.is_dir():
        sys.exit(f"--runs-root {args.runs_root} is not a directory")

    warnings: list[str] = []
    groups = discover_runs(args.runs_root, warnings, n_layers)
    if not groups:
        sys.exit(f"no oracle_result.json found under {args.runs_root}")
    result = aggregate(groups, args.track, n_layers)
    result["warnings"] = warnings

    # Every indicator here is pairwise across passes, so one pass per slug gives
    # an empty table rather than a table of zeros. Fail instead of printing it.
    if result["n_slugs"] == 0:
        for w in warnings:
            print(f"  warning: {w}", file=sys.stderr)
        sys.exit(
            f"no slug under {args.runs_root} has 2 or more passes "
            f"({len(groups)} slug(s) found, all single-pass). Stability is a "
            f"pairwise measure, so point --runs-root at a repeat batch such as "
            f"<task>/runs/<arm> from a run with --repeats."
        )

    print(f"track={args.track}  n_layers={n_layers}  root={args.runs_root}")
    print(f"slugs with >=2 passes: {result['n_slugs']}   "
          f"single-pass (skipped): {len(result['skipped_single_pass_slugs'])}")
    for w in warnings:
        print(f"  warning: {w}")
    header = ("slug", "n", "pin-F", "pin-L", "pin-B", "insp-F", "tc-SD",
              "top1", "flip")
    print(f"\n{header[0]:52s} {header[1]:>2s} " + " ".join(f"{h:>6s}" for h in header[2:]))
    for slug, s in result["per_slug"].items():
        row = [
            _fmt(s.get("pinned_jaccard_feature")),
            _fmt(s.get("pinned_jaccard_layer")),
            _fmt(s.get("pinned_jaccard_band")),
            _fmt(s.get("inspected_jaccard_feature")),
            _fmt(s.get("tool_calls_sd")),
            _fmt(s.get("top1_agreement")),
            _fmt(s.get("verdict_flip_rate")),
        ]
        print(f"{slug[:52]:52s} {s['n_passes']:>2d} " + " ".join(f"{v:>6s}" for v in row))
    print("\noverall (mean of per-slug values):")
    for k, v in result["overall"].items():
        if v is not None:
            print(f"  {k:28s} {v:.3f}")

    if args.out:
        args.out.write_text(json.dumps(result, indent=2))
        print(f"\nwritten to {args.out}")


if __name__ == "__main__":
    main()
