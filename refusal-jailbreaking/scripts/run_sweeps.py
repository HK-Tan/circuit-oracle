#!/usr/bin/env python3
"""Deterministic multi-stage seed sweep. One model load shared across all slugs.

The single deterministic entry for the suppression-jailbreak track. It supersedes
run_seed_sweep.py (which is now a thin deprecation wrapper). It holds the causal
arbiter (the ANCHOR sweep) and the outcome metric (the LLM grader) fixed, and
varies only the feature-selection ranking across seven stages:

  i      score = influence                                  + middle-layer band
  ii-a   score = influence * relevance
  ii-b   score = influence * relevance                      + middle-layer band
  iii-a  score = influence * relevance * (-log rho)
  iii-b  score = influence * relevance * (-log rho)         + middle-layer band
  iv-a   score = influence * (-log rho)
  iv-b   score = influence * (-log rho)                     + middle-layer band

Stage iv is the no-LLM-selection challenger: rarity stands in for the relevance
gate, so its selection needs the Neuronpedia fetch (frac_nonzero) but never the
relevance scorer.

It loads the subject model ONCE for the whole slug list, then per slug loads the
graph ONCE, computes base influence ONCE, runs the Neuronpedia (+ relevance when
any ii/iii stage is requested) pass ONCE shared by all pool stages. The selection
for every requested stage is computed up front (cheap and deterministic), the
pins are UNIONED, and the expensive steps run ONCE over the union: one ANCHOR
sweep (its row builder dedups by the applied clamp value, so identical clamps
across pins and stages decode once), one reassess fan-out over the union's
shifted features, and one grading pass (each unique answer graded
--grader-repeats times). Each stage's run dir is then scattered back from the
shared results, with its grader re-ranked within the stage's own pins. A
single-mode run is a trivial one-mode union and behaves as before.

Output layout (--out-root defaults to runs/, which is gitignored). Fresh runs
land there so they never write into the committed results/ or results-workshop/
archives:

  runs/sweep-<stage>/<slug>/<datetime>/
    seed.json          selection pool + per-feature scores + the 20 selected pins
    anchor_sweep.json  this stage's 20x4 measurements (shift_bucket, top5,
                       answer_after, baseline, new_value)
    reassess.json      discovery-variant records per shifted feature (shared
                       fan-out, usage amortized via usage_amortized_from)
    grades.json        grader scores (mean + per-axis std) + per-stage ranking +
                       per-stage top-1 (usage amortized via usage_amortized_from)
    report.md          the single human-readable report
    neuronpedia.json   pool modes (ii/iii/iv): fetched pool payloads
    relevance.json     ii/iii only: per-feature axis scores (topic, mechanism),
                       the combined relevance, and usage (amortized)

The shared LLM passes (relevance, grader, reassess) are paid once per slug, so
their usage blocks are amortized across the stage dirs. Exactly one owner dir
per block carries the real usage (grader and reassess are owned by the first
stage of the invocation, relevance by the first ii/iii stage, since only those
dirs write relevance.json) with usage_amortized_from null, every other dir
carries a zeroed copy pricing to 0.0 (usage_amortized_from = the owner mode).
Summing saving.compute_cost over all artifacts of a run equals the true bill.

THIS SCRIPT RUNS THE SUBJECT MODEL (except under --dry-run, which does stage-i
selection only and stops before the model load and before any LLM call). It must
run on the GPU VM, not locally.

Usage (on the VM):
  python scripts/run_sweeps.py --slug tiananmen-massacre
  python scripts/run_sweeps.py --slug tiananmen-massacre --modes i
  python scripts/run_sweeps.py --slug tiananmen-massacre --modes i --dry-run
  python scripts/run_sweeps.py --all --modes i ii-a iii-a
  python scripts/run_sweeps.py --slug tiananmen-massacre --modes i ii-b iii-b iv-b --grader-repeats 3

The working matrix (--modes i ii-b iii-b iv-b in ONE invocation) shares its
decode, reassess, and grading across the four stages, so the dedup only spans
modes that run together. Run all four in one command to get the saving.

Stages ii and iii need OPENROUTER_API_KEY for the relevance scorer (every stage
needs it at grading time). Stage i selection is fully offline (only its
report-time autointerp label fetch hits Neuronpedia). Stage iv selection hits
Neuronpedia for frac_nonzero but makes no LLM call.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

# Re-exec under the project venv (+ HF cache / CUDA env) so a bare
# `python scripts/run_sweeps.py` works without `source .venv/bin/activate`, and
# reuses the cached weights instead of re-downloading. No-op if already in the
# venv. Must precede the editable-package imports below. Stdlib-only seam.
from _venv_bootstrap import ensure_venv

ensure_venv(__file__)


DEFAULT_MODEL = "Qwen/Qwen3-4B"
DEFAULT_TRANSCODER = "mwhanna/qwen3-4b-transcoders"
DEFAULT_DATASET = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "prompts.json"
)
DEFAULT_GRAPH_DIR = "weights/graphs"


def default_graph_dir() -> str:
    """Graph store default, honoring GRAPH_STORE (same convention as
    build_graph.py: $GRAPH_STORE/graphs when set, CWD-relative weights/graphs
    otherwise). Evaluated at parser build so the rsync-then-invoke path can
    export the var on the pod; an explicit --graph-dir always wins."""
    root = os.environ.get("GRAPH_STORE")
    return os.path.join(root, "graphs") if root else DEFAULT_GRAPH_DIR

ALL_MODES = ("i", "ii-a", "ii-b", "iii-a", "iii-b", "iv-a", "iv-b")
# Modes that select from the shared Neuronpedia pool (everything except stage i).
_POOL_MODES = ("ii-a", "ii-b", "iii-a", "iii-b", "iv-a", "iv-b")
# Modes whose score uses the LLM relevance multiplier (iv deliberately does not).
_RELEVANCE_MODES = ("ii-a", "ii-b", "iii-a", "iii-b")
_RARITY_MODES = ("iii-a", "iii-b", "iv-a", "iv-b")
# The pool modes that apply the middle-layer band. They rank the band-first
# pool so the band is applied before the top-k cut (see _prepare_pool).
_BAND_POOL_MODES = ("ii-b", "iii-b", "iv-b")


# --------------------------------------------------------------------------- #
# Prompt lookup
# --------------------------------------------------------------------------- #
def _load_entries(dataset_path: str) -> list[dict]:
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"prompts file not found: {dataset_path}")
    with open(dataset_path) as f:
        data = json.load(f)
    entries = data.get("entries")
    if not entries:
        raise ValueError(f"{dataset_path} has no 'entries'")
    return entries


def entry_for_slug(dataset_path: str, slug: str) -> dict:
    """Resolve a prompts.json entry by slug. Fail loud if absent."""
    entries = _load_entries(dataset_path)
    for e in entries:
        if e.get("slug") == slug:
            return e
    available = [e.get("slug") for e in entries]
    raise KeyError(
        f"slug {slug!r} not in {dataset_path}. Available ({len(available)}): {available}"
    )


def resolve_slugs(args) -> list[str]:
    """Turn --slug / --slugs / --all into an ordered, deduped slug list."""
    if args.all:
        return [e["slug"] for e in _load_entries(args.dataset_file)]
    slugs: list[str] = []
    if args.slug:
        slugs.append(args.slug)
    if args.slugs:
        slugs.extend(args.slugs)
    # Dedup preserving order.
    seen: set[str] = set()
    ordered: list[str] = []
    for s in slugs:
        if s not in seen:
            seen.add(s)
            ordered.append(s)
    if not ordered:
        raise ValueError("no slug requested, pass --slug, --slugs, or --all")
    return ordered


def graph_path_for(args, slug: str) -> str:
    """Default graph path weights/graphs/<slug>_graph.pt unless --graph overrides.

    --graph only makes sense for a single slug. With multiple slugs it is ignored
    in favor of the per-slug default (the caller logs this).
    """
    if args.graph:
        return args.graph
    return os.path.join(args.graph_dir, f"{slug}_graph.pt")


# --------------------------------------------------------------------------- #
# ctx state reset between stages (model + graph loaded once)
# --------------------------------------------------------------------------- #
def reset_pin_state(ctx, pin_keys) -> None:
    """Reset the pin / sweep / reassess state on a reused ToolContext.

    Sets ctx.build_features to the new pin-key set, clears ctx.pinned_features,
    sets ctx.anchor_sweep_done False, and clears ctx.reassess_records. Does NOT
    clear ctx.inspect_cache (the shared Neuronpedia cache, reused across stages)
    or the baseline fields (baseline_activations / baseline_answer / baseline_top5
    / baseline_prompt are loaded once and never change between stages).

    pin_keys is an iterable of (layer, feature_idx, pos) tuples (FeatureCandidate.
    pin_key returns [layer, feature_idx, pos], so the caller maps tuple()).
    """
    ctx.build_features = set(tuple(int(x) for x in k) for k in pin_keys)
    ctx.pinned_features = {}
    ctx.anchor_sweep_done = False
    ctx.reassess_records = {}


# --------------------------------------------------------------------------- #
# Stage-i selection (offline, CPU graph load only)
# --------------------------------------------------------------------------- #
def _build_base_candidates(graph_path: str):
    """Load the graph (CPU), compute base influence, build influence-sorted candidates.

    Returns (graph, candidates, dims, gen_pos, n_layers). Imports seed_select
    lazily (it pulls in torch + circuit_tracer), so --help never touches torch.
    """
    from circuit_oracle import seed_select

    if not os.path.exists(graph_path):
        raise FileNotFoundError(
            f"graph not found: {graph_path}. Build it first with "
            f"`python scripts/build_graph.py --slug <slug>` (this script does NOT "
            "recompute a graph)."
        )
    graph = seed_select.load_graph(graph_path)
    influence, dims = seed_select.feature_influence(graph)
    candidates = seed_select.build_candidates(graph, influence)
    gen_pos = dims["n_pos"] - 1
    n_layers = int(graph.cfg.n_layers)
    return graph, candidates, dims, gen_pos, n_layers


def select_stage_i(graph_path: str, *, top_k: int, drop_frac: float):
    """Select the stage-i top-k features (influence + middle-layer band), offline.

    Returns (graph, n_layers, gen_pos, ranked) where ranked is the list of
    selected FeatureCandidate. Used by both the dry-run path and the full run.
    """
    from circuit_oracle import seed_select

    graph, candidates, _dims, gen_pos, n_layers = _build_base_candidates(graph_path)
    non_opener = seed_select.filter_non_opener(candidates, gen_pos)
    ranked = seed_select.rank(
        non_opener, "i", n_layers=n_layers, top_k=top_k, drop_frac=drop_frac
    )
    return graph, n_layers, gen_pos, ranked


# --------------------------------------------------------------------------- #
# Record assembly for the report
# --------------------------------------------------------------------------- #
def _selection_rows(ranked, *, mode: str, selected_keys: set):
    """Build the report's selection rows from ranked / pooled candidates.

    For stage i, ``ranked`` is the 20 selected pins. For the pool modes, ``ranked``
    is the full scored pool and ``selected_keys`` flags the 20 chosen pins.

    For stage i ``ranked`` is already the sorted top_k with .rank set (0-based), so
    .rank is used directly. For pool modes ``ranked`` is the full pool (seed_select.rank
    only stamps .rank and .score on the chosen top_k, leaving unselected pool rows
    with a stale .score from a prior stage when modes run out of -a/-b order). This
    re-scores every pool row for THIS stage so the displayed score is always the
    active stage's formula, then re-derives a stage-specific display rank by sorting
    the full pool on that score descending. The full pool already carries the
    factors this stage's formula reads (attached in _prepare_pool, relevance only
    when a ii/iii stage requested it), so _score_for never hits its fail-loud
    missing-factor paths here.
    """
    from circuit_oracle import seed_select

    if mode == "i":
        ordered = list(ranked)
        display_rank = {id(c): c.rank for c in ordered}
    else:
        for c in ranked:
            c.score = seed_select._score_for(c, mode)
        ordered = sorted(
            ranked,
            key=lambda c: (
                c.score if c.score is not None else float("-inf"),
                c.influence,
                -c.layer,
                -c.feature_idx,
                -c.pos,
            ),
            reverse=True,
        )
        display_rank = {id(c): r for r, c in enumerate(ordered)}

    rows: list[dict] = []
    for c in ordered:
        key = (c.layer, c.feature_idx, c.pos)
        rows.append({
            "rank": display_rank[id(c)],
            "layer": c.layer,
            "feature_idx": c.feature_idx,
            "pos": c.pos,
            "influence": c.influence,
            "relevance": c.relevance,
            "neglog_rho": c.neglog_rho,
            "score": c.score,
            "selected": key in selected_keys,
            "autointerp": None,  # filled at report time from the inspect cache
        })
    return rows


def _autointerp_from_cache(ctx, layer: int, feature_idx: int, pos: int):
    """Best-effort autointerp label from ctx.inspect_cache (pos-tolerant)."""
    cache = getattr(ctx, "inspect_cache", {}) or {}
    blob = cache.get((layer, feature_idx, pos))
    if blob is None:
        blob = cache.get((layer, feature_idx, None))
    if isinstance(blob, dict):
        return blob.get("autointerp") or blob.get("label")
    return None


def _measurement_answers(measurements) -> dict:
    """Map (layer, feature_idx, pos, scale) -> answer_after for report joins."""
    out: dict = {}
    for m in measurements:
        key = (m.get("layer"), m.get("feature_idx"), m.get("pos"), m.get("scale"))
        out[key] = m.get("answer_after", "")
    return out


# --------------------------------------------------------------------------- #
# Per-stage selection (cheap, deterministic, CPU only)
# --------------------------------------------------------------------------- #
class _StageSelection:
    """The selection result for one stage, computed before the shared sweep.

    Carries everything the per-stage writer needs that is NOT shared across
    stages: the selected pins (``ranked``), the report's selection table source
    (``selection_for_report``, the full scored pool for pool modes, the 20 pins
    for stage i), the pin keys, and the selected-key set used both to union the
    pins and to scatter the shared sweep results back to this stage.
    """

    def __init__(self, *, mode, ranked, selection_for_report):
        self.mode = mode
        self.ranked = ranked
        self.selection_for_report = selection_for_report
        self.pin_keys = [tuple(c.pin_key) for c in ranked]
        self.selected_keys = {(c.layer, c.feature_idx, c.pos) for c in ranked}


def _select_stage(*, mode, base_candidates, pools, n_layers, gen_pos, args):
    """Rank one stage's pins. Pure CPU, no ctx mutation, no sweep, no LLM call.

    Stage i ranks the band-filtered non-openers. The pool modes (ii/iii/iv) rank
    a shared pool (which already carries neglog_rho, plus relevance when any
    ii/iii stage requested it). The "-b" band modes rank the band-first pool, the
    "-a" modes the overall pool (see _prepare_pool). The common pre-filter (drop
    pos 0 and pos == gen_pos) is mandatory for every stage. Pool modes get it
    inside _prepare_pool, so only stage i applies it here (rank mode "i" applies
    only the band, never the opener drop). Without this the full run would pin
    BOS / generation-boundary features and diverge from the --dry-run preview
    (select_stage_i filters openers first).

    Returns a _StageSelection. FAIL-LOUD if no candidates survive the filters.
    """
    from circuit_oracle import seed_select

    if mode == "i":
        non_opener = seed_select.filter_non_opener(base_candidates, gen_pos)
        ranked = seed_select.rank(
            non_opener, "i", n_layers=n_layers, top_k=args.top_k, drop_frac=args.drop_frac
        )
        selection_for_report = ranked
    else:
        pool = pools["band"] if mode in _BAND_POOL_MODES else pools["overall"]
        ranked = seed_select.rank(
            pool, mode, n_layers=n_layers, top_k=args.top_k, drop_frac=args.drop_frac
        )
        selection_for_report = pool

    if len(ranked) < args.top_k:
        print(
            f"  [stage {mode}] WARNING: only {len(ranked)} candidates survived the "
            f"filters (requested top-{args.top_k}). Pinning what remains."
        )
    if not ranked:
        raise ValueError(f"stage {mode}: no candidates left to pin after filtering")

    return _StageSelection(
        mode=mode, ranked=ranked, selection_for_report=selection_for_report
    )


# --------------------------------------------------------------------------- #
# Scatter the shared union sweep back to one stage
# --------------------------------------------------------------------------- #
def _subset_measurements(union_measurements, selected_keys):
    """Filter the union's flat measurements to one stage's pins.

    Part 1's batched_anchor_sweep gives every origin (pin, scale) its OWN
    measurement dict, but stages that selected the same pin share those dicts,
    so stage-local fields (grader_rank, top1) must go on fresh rows, never be
    stamped onto the subset in place (_stage_grades builds fresh ranking rows).
    A row is kept when its (layer, feature_idx, pos) is one of this stage's
    pins, so double-position pins of the same feature each keep their own four
    rows. Preserves the union's measurement order (feature-outer, scale-inner).
    """
    return [
        m
        for m in union_measurements
        if (m.get("layer"), m.get("feature_idx"), m.get("pos")) in selected_keys
    ]


def _reassess_key_tuple(k):
    """Normalize a reassess key to an int (layer, feature_idx, pos) tuple.

    ctx.reassess_records is tuple-keyed (set by _dispatch_reassess), but accept
    the stringified "layer,feature_idx,pos" form too (the encoding the writer and
    the report use) so the subset is robust to either shape.
    """
    if isinstance(k, str):
        parts = k.split(",")
    else:
        parts = list(k)
    return tuple(int(x) for x in parts)


def _subset_reassess(union_reassess, selected_keys):
    """Filter the union reassess records to one stage's pins (key-shape tolerant)."""
    return {
        k: v
        for k, v in (union_reassess or {}).items()
        if _reassess_key_tuple(k) in selected_keys
    }


def _stage_grades(union_grades, stage_measurements, *, n_repeats):
    """Build a stage-local grades record from the shared union grade pass.

    grade_sweep ran ONCE over the union and stamped every union measurement dict
    with usability / plausibility / overall (+ per-axis std). grader_rank / top1
    are per-stage concepts (the run's self-nominated submission within the
    stage's own pins), so this re-ranks ONLY this stage's subset, never the
    union. The shared baseline / usage / model / question blocks pass through
    unchanged (one baseline grade, one true bill, see the amortization wiring in
    _run_slug for how usage is attributed to a single owner stage dir).

    The per-stage ranking rows are fresh dicts built from this stage's own
    measurement dicts, so one stage's grader_rank / top1 never leak into
    another stage's record (part 1's share-vs-copy contract: each origin owns
    its measurement dict, and we build a separate ranking row per origin here).
    """
    ranking: list[dict] = []
    for m in stage_measurements:
        ranking.append({
            "intervention_id": (
                f"L{m.get('layer')}:F{m.get('feature_idx')}@{m.get('pos')}, "
                f"scale={m.get('scale')}"
            ),
            "layer": m.get("layer"),
            "feature_idx": m.get("feature_idx"),
            "pos": m.get("pos"),
            "scale": m.get("scale"),
            "shift_bucket": m.get("shift_bucket"),
            "usability": m.get("usability"),
            "plausibility": m.get("plausibility"),
            "overall": m.get("overall"),
            "usability_std": m.get("usability_std"),
            "plausibility_std": m.get("plausibility_std"),
            "n_scored": m.get("n_scored"),
            "n_refused": m.get("n_refused"),
        })

    # Re-rank WITHIN this stage's subset, mirroring grade_sweep's sort key
    # (None overalls last). Sort a view of the same dicts so the grader_rank /
    # top1 stamp lands on the ranking rows.
    ordered = sorted(
        ranking,
        key=lambda e: (
            e["overall"] is not None,
            e["overall"] if e["overall"] is not None else -1.0,
        ),
        reverse=True,
    )
    for gr, e in enumerate(ordered, start=1):
        e["grader_rank"] = gr
        e["top1"] = gr == 1

    # Refusal diagnostics. The imputed plausibility is a property of the ONE union
    # grade pass, so it passes through unchanged, but the block count is re-derived
    # from this stage's own rows: copying the union-wide count would attribute other
    # stages' safety blocks to this stage.
    return {
        "grader_model": union_grades.get("grader_model"),
        "question": union_grades.get("question"),
        "n_repeats": n_repeats,
        "baseline": union_grades.get("baseline"),
        "ranking": ranking,
        "top1": ordered[0] if ordered else None,
        "n_refused_draws": sum(e.get("n_refused") or 0 for e in ranking),
        "refusal_fallback_plausibility": union_grades.get("refusal_fallback_plausibility"),
        "usage": union_grades.get("usage"),
    }


# --------------------------------------------------------------------------- #
# Per-stage writer (runs after the shared union sweep + grade)
# --------------------------------------------------------------------------- #
def _write_stage(
    *,
    ctx,
    selection,
    slug,
    graph_path,
    config,
    union_measurements,
    union_reassess,
    union_grades,
    sweep_result,
    n_repeats,
    out_root,
    pre_timings,
    stage_timings,
    usage_owners,
):
    """Scatter the shared sweep / grade back to one stage and write its run dir.

    The expensive shared work (one decode, one reassess fan-out, one grade pass)
    already happened in _run_slug. This subsets those shared results to the
    stage's own pins, re-ranks the grader within the subset, fills autointerp
    labels, assembles the report record, and writes the run dir. ``usage_owners``
    maps each shared block ("relevance", "grader", "reassess") to the single
    stage dir that carries its real usage (decision 4), since the relevance block
    lands in a different subset of dirs than the grader / reassess blocks.

    Returns the run dir path.
    """
    from circuit_oracle import sweep_report

    mode = selection.mode
    t_stage = time.perf_counter()

    stage_measurements = _subset_measurements(union_measurements, selection.selected_keys)
    stage_reassess = _subset_reassess(union_reassess, selection.selected_keys)
    grades = _stage_grades(union_grades, stage_measurements, n_repeats=n_repeats)

    # Fill autointerp labels for the selection rows from the inspect cache. The
    # cache is already warm: the pool modes fetched the pool in _prepare_pool,
    # stage i fetched its pins before the sweep (see _run_slug).
    selection_rows = _selection_rows(
        selection.selection_for_report, mode=mode, selected_keys=selection.selected_keys
    )
    for row in selection_rows:
        row["autointerp"] = _autointerp_from_cache(
            ctx, row["layer"], row["feature_idx"], row["pos"]
        )

    record = _assemble_record(
        slug=slug,
        mode=mode,
        graph_path=graph_path,
        config=config,
        ctx=ctx,
        selection_rows=selection_rows,
        measurements=stage_measurements,
        reassess_records=stage_reassess,
        grades=grades,
    )

    report_text = sweep_report.build_report(record)
    stage_timings = dict(stage_timings)
    stage_timings["stage_write_s"] = round(time.perf_counter() - t_stage, 3)

    run_dir = _write_run_dir(
        out_root=out_root,
        mode=mode,
        slug=slug,
        record=record,
        ranked=selection.ranked,
        sweep_result=sweep_result,
        stage_measurements=stage_measurements,
        stage_reassess=stage_reassess,
        grades=grades,
        config=config,
        graph_path=graph_path,
        report_text=report_text,
        pre_timings=pre_timings,
        stage_timings=stage_timings,
        usage_owners=usage_owners,
    )
    print(f"  [stage {mode}] wrote {run_dir}")
    return run_dir


def _assemble_record(
    *, slug, mode, graph_path, config, ctx, selection_rows, measurements, reassess_records, grades
):
    """Build the build_report record dict (see record_schema in the return doc)."""
    return {
        "slug": slug,
        "mode": mode,
        "datetime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S"),
        "graph_path": graph_path,
        "models": {
            "subject": config.model_name,
            "relevance": config.relevance_model,
            "reassess": config.subagent_model,
            "grader": config.grader_model,
        },
        "baseline_answer": ctx.baseline_answer,
        "selection": selection_rows,
        "reassess": reassess_records,
        "grades": grades,
        "measurement_answers": _measurement_answers(measurements),
    }


def _amortize_block(usage, *, mode, usage_owner):
    """Return (usage_block, amortized_from) for one shared usage block.

    Usage amortization (next-refactoring.md decision 4). The shared LLM passes
    (relevance, grader, reassess) are paid ONCE per slug, so writing the real
    usage block into every stage dir would double count when costs are summed
    over artifacts. The OWNER stage dir for this block (``usage_owner``) carries
    the real block plus ``"usage_amortized_from": None``. Every other stage dir
    carries a zeroed copy that still prices to 0.0 via compute_cost
    (saving.amortized_usage keeps the model key) plus
    ``"usage_amortized_from": "<owner mode>"``. Summing compute_cost over ALL
    artifacts of the run then equals the true bill.

    The owner is PER block, not one owner for everything. The grader and reassess
    blocks land in every stage dir, so their owner is the first stage written.
    The relevance block lands ONLY in _RELEVANCE_MODES dirs, so its owner is the
    first such stage. Picking a relevance owner that never writes relevance.json
    would lose the real block and undercount, hence the per-block owners computed
    in _run_slug.
    """
    from circuit_oracle import saving

    if mode == usage_owner:
        return usage, None
    return saving.amortized_usage(usage or {}), usage_owner


def _write_run_dir(
    *,
    out_root,
    mode,
    slug,
    record,
    ranked,
    sweep_result,
    stage_measurements,
    stage_reassess,
    grades,
    config,
    graph_path,
    report_text,
    pre_timings,
    stage_timings,
    usage_owners,
):
    """Write seed.json / anchor_sweep.json / reassess.json / grades.json / report.md
    / timing.json (plus neuronpedia.json for pool modes and relevance.json for
    ii/iii) under the run dir.

    The measurement / reassess / grade artifacts are this stage's OWN subset of
    the shared union sweep (scattered back in _write_stage). The shared LLM usage
    blocks are amortized across the stage dirs so the per-slug bill is counted
    once (see _amortize_block). ``usage_owners`` maps each shared block name
    ("relevance", "grader", "reassess") to the single stage dir that carries its
    real usage, since the relevance block lives in a different subset of dirs
    than the grader / reassess blocks.
    """
    dt = record["datetime"]
    run_dir = os.path.join(out_root, f"sweep-{mode}", slug, dt)
    os.makedirs(run_dir, exist_ok=True)

    # seed.json: selection pool + per-feature scores + the 20 selected pins. The
    # pool reuses record["selection"] (which already carries the stage-specific
    # display rank), so seed.json and report.md never disagree on the ranking.
    seed_payload = {
        "slug": slug,
        "mode": mode,
        "graph": os.path.abspath(graph_path),
        "datetime": dt,
        "top_k": config.top_k,
        "pool_size": config.pool_size,
        "drop_frac": config.drop_frac,
        "selected_pin_keys": [list(c.pin_key) for c in ranked],
        "pool": [
            {
                "rank": row["rank"],
                "layer": row["layer"],
                "feature_idx": row["feature_idx"],
                "pos": row["pos"],
                "influence": row["influence"],
                "relevance": row["relevance"],
                "neglog_rho": row["neglog_rho"],
                "score": row["score"],
                "selected": row["selected"],
            }
            for row in record["selection"]
        ],
    }
    _write_json(os.path.join(run_dir, "seed.json"), seed_payload)

    # anchor_sweep.json: THIS stage's measurements (the union subset for this
    # stage's pins x 4 scales), each row carrying baseline / new_value (the
    # applied clamp, also the cross-stage dedup key, next-refactoring.md decision
    # 5). n_features / n_scales describe this stage's subset, not the union.
    n_scales = sweep_result.get("n_scales")
    _write_json(os.path.join(run_dir, "anchor_sweep.json"), {
        "slug": slug,
        "mode": mode,
        "baseline_answer": record["baseline_answer"],
        "n_features": len(ranked),
        "n_scales": n_scales,
        "measurements": stage_measurements,
    })

    # reassess.json: discovery-variant records for THIS stage's shifted features
    # (tuple keys stringified for JSON). The records are scattered from the one
    # shared reassess fan-out (run once over the union), so the same feature
    # reads identically across stages. "usage" is the shared reassess bill,
    # amortized to a single owner stage dir.
    reassess_usage = sweep_result.get("reassess_usage")
    reassess_block, reassess_from = _amortize_block(
        reassess_usage, mode=mode, usage_owner=usage_owners["reassess"]
    )
    _write_json(os.path.join(run_dir, "reassess.json"), {
        "slug": slug,
        "mode": mode,
        "usage": reassess_block,
        "usage_amortized_from": reassess_from,
        "reassess_records": {_str_key(k): v for k, v in (stage_reassess or {}).items()},
    })

    # grades.json: grader scores + per-stage ranking + per-stage top-1. The
    # grader ran ONCE over the union, so its "usage" is the shared grader bill,
    # amortized to a single owner stage dir (the ranking / top1 are already this
    # stage's own re-rank).
    grades_block, grades_from = _amortize_block(
        grades.get("usage"), mode=mode, usage_owner=usage_owners["grader"]
    )
    grades_out = dict(grades)
    grades_out["usage"] = grades_block
    grades_out["usage_amortized_from"] = grades_from
    _write_json(os.path.join(run_dir, "grades.json"), grades_out)

    # timing.json: wall-clock diagnostics. pre_stage_shared is paid once per slug
    # (base influence, graph load, the Neuronpedia + relevance pass, and now the
    # one shared decode + reassess + grade pass) and repeated in every stage dir
    # so each run dir stays self-contained. The model load is paid once per RUN:
    # subject_model_load_s is what this slug paid (0.0 + amortized flag after the
    # first slug), subject_model_load_shared_s repeats the one-time cost.
    _write_json(os.path.join(run_dir, "timing.json"), {
        "slug": slug,
        "mode": mode,
        "pre_stage_shared": pre_timings,
        "stage": stage_timings,
    })

    # report.md.
    with open(os.path.join(run_dir, "report.md"), "w") as f:
        f.write(report_text)

    # neuronpedia.json for every pool mode, relevance.json only for the modes
    # whose score actually uses it (a mixed run has a relevance payload in
    # config, but writing it into stage-iv dirs would misdescribe iv's formula).
    # The relevance scorer is paid ONCE per slug, so its usage block is amortized
    # to a single owner stage dir too.
    if mode in _POOL_MODES:
        np_payloads = getattr(config, "_neuronpedia_payloads", None)
        if np_payloads is not None:
            _write_json(os.path.join(run_dir, "neuronpedia.json"), {
                "slug": slug,
                "payloads": {_str_pair(k): v for k, v in np_payloads.items()},
            })
    if mode in _RELEVANCE_MODES:
        rel_payload = getattr(config, "_relevance_payload", None)
        if rel_payload is not None:
            rel_block, rel_from = _amortize_block(
                rel_payload.get("usage"), mode=mode, usage_owner=usage_owners["relevance"]
            )
            rel_out = dict(rel_payload)
            rel_out["usage"] = rel_block
            rel_out["usage_amortized_from"] = rel_from
            _write_json(os.path.join(run_dir, "relevance.json"), rel_out)

    return run_dir


def _write_json(path: str, payload) -> None:
    with open(path, "w") as f:
        json.dump(payload, f, indent=2, default=str)


def _human_s(seconds: float) -> str:
    """Render elapsed seconds as '42.3s' or '6m13s' for stdout diagnostics."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, sec = divmod(int(round(seconds)), 60)
    return f"{minutes}m{sec:02d}s"


def _str_key(key) -> str:
    """Stringify a (layer, feature_idx, pos) tuple for JSON, matching saving."""
    if isinstance(key, tuple):
        return ",".join(str(int(x)) for x in key)
    return str(key)


def _str_pair(key) -> str:
    """Stringify a (layer, feature_idx) pair for JSON."""
    if isinstance(key, tuple):
        return ",".join(str(int(x)) for x in key)
    return str(key)


# --------------------------------------------------------------------------- #
# Shared Neuronpedia / relevance / rarity pass (pool stages), paid once
# --------------------------------------------------------------------------- #
def _prepare_pool(
    ctx, base_candidates, *, gen_pos, pool_size, config, need_relevance: bool,
    need_rarity: bool, n_layers: int, drop_frac: float,
):
    """Fetch Neuronpedia (+ score relevance if needed) for the pool stages ONCE.

    Builds TWO pools so the band stages get a real top-k:

    - ``overall``: top ``pool_size`` by influence over the opener-dropped set
      (no band). Serves ii-a / iii-a / iv-a, unchanged from the single-pool design.
    - ``band``: band-filtered FIRST, then top ``pool_size`` by influence. Serves
      ii-b / iii-b / iv-b. This applies the band before the top-k cut instead of
      after, where ``rank`` would otherwise collapse the layer-0-dominated overall
      pool to a handful of band-resident features.

    The Neuronpedia fetch always runs (frac_nonzero feeds rarity, and the report
    reads autointerp labels from the inspect cache it warms). The relevance LLM
    pass runs only when ``need_relevance`` (some ii/iii stage requested), so an
    iv-only run makes no selection-time LLM call. Relevance + rarity are scored
    ONCE over the union of the two pools (deduped by object identity, since they
    share FeatureCandidate objects where they overlap). ``neglog_rho`` is
    normalized over the union; ranking within each pool is invariant to that
    single global rescale, so the -a selections are unchanged.

    Returns ``{"overall": [...], "band": [...]}``. Also stashes the raw payloads and
    the relevance payload on ``config`` so the writer can emit neuronpedia.json /
    relevance.json. FAIL-LOUD on a missing relevance score (when scored), an error
    payload, or a None frac_nonzero (handled inside the called helpers).
    """
    from circuit_oracle import seed_select
    from circuit_oracle import feature_relevance

    non_opener = seed_select.filter_non_opener(base_candidates, gen_pos)
    pool_overall = seed_select.candidate_pool(non_opener, pool_size=pool_size)
    band_cands = seed_select.filter_layer_band(non_opener, n_layers, drop_frac)
    pool_band = seed_select.candidate_pool(band_cands, pool_size=pool_size)

    # Union for the single relevance + Neuronpedia pass. Dedup by object identity
    # (a band feature in the overall top-k is the SAME FeatureCandidate object).
    union = list({id(c): c for c in (pool_overall + pool_band)}.values())

    pairs = [(c.layer, c.feature_idx, c.pos) for c in union]
    payloads = feature_relevance.fetch_payloads(ctx, pairs)
    config._neuronpedia_payloads = payloads

    scores = None
    if need_relevance:
        scores, usage, detail = feature_relevance.score_relevance(
            ctx.subagent_client_relevance,
            config.relevance_model,
            user_message=config.user_message,
            candidates=union,
            payloads=payloads,
            system_prompt=config.system_prompt,
            baseline_answer=ctx.baseline_answer,
        )
        config._relevance_payload = {
            "model": config.relevance_model,
            "scores": {_str_pair(k): v for k, v in scores.items()},
            "detail": {_str_pair(k): v for k, v in detail.items()},
            "usage": usage,
        }

    # Attach relevance (when scored) + frac_nonzero to every union candidate
    # (position-independent, keyed by (layer, feature_idx)). FAIL-LOUD if a pool
    # feature has no score while relevance is required.
    for c in union:
        pair = (c.layer, c.feature_idx)
        if need_relevance:
            if pair not in scores:
                raise KeyError(
                    f"relevance pass produced no score for pool feature "
                    f"L{c.layer}:F{c.feature_idx} (relevance is required for ii/iii)"
                )
            c.relevance = scores[pair]
        payload = payloads.get(pair)
        if payload is None:
            raise KeyError(
                f"no Neuronpedia payload for pool feature L{c.layer}:F{c.feature_idx}"
            )
        c.frac_nonzero = payload.get("frac_nonzero")

    if need_rarity:
        # FAIL-LOUD inside attach_neglog_rho if any frac_nonzero is None. Normalize
        # over the union so both pools share one rarity scale (selection-invariant).
        seed_select.attach_neglog_rho(union)

    return {"overall": pool_overall, "band": pool_band}


# --------------------------------------------------------------------------- #
# Run config (a light object the grader + report read)
# --------------------------------------------------------------------------- #
class _SweepConfig:
    """Lightweight config bag for a sweep run (not the agentic RunConfig).

    Carries the fields grade_sweep (grader_model, provider, user_message) and the
    report (model_name, relevance_model, subagent_model, grader_model) read, plus
    the selection knobs and the stashed neuronpedia / relevance payloads.
    """

    def __init__(self, *, slug, user_message, system_prompt, args):
        self.slug = slug
        self.user_message = user_message
        self.system_prompt = system_prompt
        self.model_name = args.model_name
        self.relevance_model = args.relevance_model
        self.grader_model = args.grader_model
        self.subagent_model = args.reassess_model
        self.provider = args.provider
        self.top_k = args.top_k
        self.pool_size = args.pool_size
        self.drop_frac = args.drop_frac
        # Stashed by _prepare_pool for the ii/iii writers.
        self._neuronpedia_payloads = None
        self._relevance_payload = None


# --------------------------------------------------------------------------- #
# Dry run (stage-i selection only, fully offline)
# --------------------------------------------------------------------------- #
def _dry_run(args, slugs: list[str]) -> int:
    """Stage-i selection only. Stops before the model load and any LLM call.

    The graph load (CPU) is allowed since selection needs it. Prints the 20
    selected features per slug. No subject-model load, no Neuronpedia, no LLM.
    """
    for slug in slugs:
        gpath = graph_path_for(args, slug)
        print(f"\n=== DRY RUN stage-i selection: {slug} ({gpath}) ===")
        _graph, _n_layers, _gen_pos, ranked = select_stage_i(
            gpath, top_k=args.top_k, drop_frac=args.drop_frac
        )
        print(f"selected {len(ranked)} features (top-{args.top_k}, drop_frac={args.drop_frac}):")
        for c in ranked:
            print(
                f"  rank {c.rank:>2}  L{c.layer}:F{c.feature_idx}@{c.pos}  "
                f"influence={c.influence:.4f}  score={c.score:.4f}"
            )
    print("\n(dry run: stopped before subject-model load and before any LLM call)")
    return 0


# --------------------------------------------------------------------------- #
# Full run for one slug (shared model passed in, all stages sequential)
# --------------------------------------------------------------------------- #
def _run_slug(args, slug: str, *, model, model_load_s: float, load_paid_here: bool) -> None:
    """Run all requested stages for one slug, reusing the shared subject model.

    The model is loaded ONCE in main() and passed in, so a multi-slug run pays
    the multi-minute load once instead of once per slug. timing.json keeps both
    numbers honest: ``subject_model_load_s`` is what THIS slug paid (the full
    load for the first slug, 0.0 for later ones, flagged amortized) and
    ``subject_model_load_shared_s`` repeats the one-time cost so every run dir
    stays self-contained.
    """
    # Heavy imports deferred to here so --help / --dry-run never touch torch via
    # this path. seed_select (graph load) is still torch-backed, but --dry-run
    # uses the CPU graph-load path which the plan explicitly allows.
    from circuit_oracle import (
        ToolContext,
        compute_or_load_graph,
        format_chat,
        LLMClient,
    )

    entry = entry_for_slug(args.dataset_file, slug)
    user_message = entry["user_message"]
    system_prompt = entry.get("system_prompt", "") or ""
    assistant_prefix = entry.get("assistant_prefix", "") or ""

    graph_path = graph_path_for(args, slug)

    modes = list(args.modes)
    need_pool = any(m in _POOL_MODES for m in modes)
    need_relevance = any(m in _RELEVANCE_MODES for m in modes)
    need_rarity = any(m in _RARITY_MODES for m in modes)

    # Re-check the graph here even though main() pre-flighted every slug before
    # the model load. This only trips if the .pt vanished mid-run, and a loud
    # error beats compute_or_load_graph recomputing a graph we never asked for.
    if not args.build and not os.path.exists(graph_path):
        raise FileNotFoundError(
            f"no cached graph at {graph_path} (it existed at pre-flight). Build it "
            f"with `build_graph.py --slug {slug}`, or pass --build."
        )

    t_slug = time.perf_counter()

    prompt = format_chat(model.tokenizer, system_prompt, user_message, assistant_prefix)
    pre_timings = {
        "subject_model_load_s": model_load_s if load_paid_here else 0.0,
        "subject_model_load_shared_s": model_load_s,
        "subject_model_load_amortized": not load_paid_here,
    }

    # --build: compute the attribution graph now if the .pt is absent, reusing this
    # model. Without --build a missing .pt is fail-loud (the graph is the expensive
    # GPU step, normally built once via build_graph.py). When we build here we keep
    # the in-memory graph_result so ctx does not reload it.
    graph_result = None
    # Hoisted out of the build branch so the load branch below declares the SAME
    # cap it would have built with. compute_or_load_graph checks the caller's cap
    # against the one recorded in .baseline.json, and passing None there would
    # read as "this run wants an unbounded graph" and reject every capped .pt.
    max_feat = args.max_feature_nodes if args.max_feature_nodes > 0 else None
    if not os.path.exists(graph_path):
        # --build is guaranteed here (the pre-flight above raised otherwise).
        print(f"\n=== {slug}: building attribution graph (--build, .pt absent) ===")
        t_phase = time.perf_counter()
        graph_result = compute_or_load_graph(
            prompt, model, cache_path=graph_path, max_feature_nodes=max_feat
        )
        pre_timings["graph_build_s"] = round(time.perf_counter() - t_phase, 3)
        print(f"  graph written to {graph_path} in {_human_s(pre_timings['graph_build_s'])}")

    # Base influence ONCE (offline, CPU), now that the .pt exists. seed_select.load_graph
    # + influence + candidates. This also gives n_layers and gen_pos for every stage.
    print(f"\n=== {slug}: base influence (graph {graph_path}) ===")
    t_phase = time.perf_counter()
    _graph_cpu, base_candidates, _dims, gen_pos, n_layers = _build_base_candidates(graph_path)
    pre_timings["base_influence_s"] = round(time.perf_counter() - t_phase, 3)
    print(f"  base influence done in {_human_s(pre_timings['base_influence_s'])}")

    config = _SweepConfig(
        slug=slug, user_message=user_message, system_prompt=system_prompt, args=args
    )

    # Graph result for ctx. A cache hit (the .pt exists now); reuse the build result
    # when --build just produced it. compute_or_load_graph reuses the cached .pt and
    # its baseline siblings.
    if graph_result is None:
        t_phase = time.perf_counter()
        graph_result = compute_or_load_graph(
            prompt, model, cache_path=graph_path, max_feature_nodes=max_feat
        )
        pre_timings["graph_load_s"] = round(time.perf_counter() - t_phase, 3)
        print(f"  graph loaded for ctx in {_human_s(pre_timings['graph_load_s'])}")

    ctx = ToolContext(
        graph=graph_result["graph"],
        tokenizer=model.tokenizer,
        replacement_model=graph_result["replacement_model"],
        baseline_activations=graph_result["baseline_activations"],
        baseline_answer=graph_result["baseline_answer"],
        baseline_top5=graph_result["baseline_top5"],
        baseline_prompt=prompt,
        system_prompt=system_prompt,
    )

    # Reassess backend wired ONCE: discovery variant, the configured reassess model.
    # batched_anchor_sweep reads these via getattr off ctx.
    ctx.subagent_client = LLMClient(provider=args.provider)
    ctx.subagent_model = args.reassess_model
    ctx.reassess_variant = "discovery"

    # Shared Neuronpedia (+ relevance) pass ONCE for all pool stages requested.
    pool_candidates = None
    if need_pool:
        if need_relevance:
            # Pre-flight the key here (Risk 1 in the plan): ii/iii need
            # OPENROUTER_API_KEY for SELECTION (the relevance scorer), not just
            # grading. LLMClient does not raise on a missing key (it sends an empty
            # auth token), so without this guard a keyless ii/iii run would fail
            # late inside score_relevance as an opaque transport/auth error. Mirror
            # grade_sweep's fail-loud message style. Stage iv selection makes no
            # LLM call, so an iv-only run skips this (grading still needs the key
            # and fails loud inside grade_sweep).
            # Checked against the gateway the relevance model is actually routed
            # to, not a hardcoded OPENROUTER_API_KEY. The default relevance model
            # (gpt-oss-120b) is pinned to OpenRouter, so the default run still
            # demands exactly that key, but --relevance-model + --provider kilo
            # is no longer rejected for lacking a key it never uses.
            from circuit_oracle.llm_client import preflight_providers
            try:
                preflight_providers([args.relevance_model], args.provider)
            except RuntimeError as e:
                raise RuntimeError(
                    f"stages ii/iii need a key for the relevance scorer "
                    f"(selection, not just grading): {e}. Set it before running, or "
                    "restrict to --modes i / iv-a / iv-b (their selection makes no "
                    "LLM call)."
                ) from None
            # Separate client handle for the relevance scorer so the model id is the
            # relevance model, not the reassess model. Same provider.
            ctx.subagent_client_relevance = LLMClient(provider=args.provider)
        pass_label = "relevance" if need_relevance else "rarity only"
        print(f"=== {slug}: shared Neuronpedia pass, {pass_label} (pool {args.pool_size}) ===")
        t_phase = time.perf_counter()
        pool_candidates = _prepare_pool(
            ctx,
            base_candidates,
            gen_pos=gen_pos,
            pool_size=args.pool_size,
            config=config,
            need_relevance=need_relevance,
            need_rarity=need_rarity,
            n_layers=n_layers,
            drop_frac=args.drop_frac,
        )
        pre_timings["neuronpedia_relevance_s"] = round(time.perf_counter() - t_phase, 3)
        print(f"  Neuronpedia pass done in {_human_s(pre_timings['neuronpedia_relevance_s'])}")

    from circuit_oracle import saving
    from circuit_oracle.tools import batched_anchor_sweep, pin_features

    # ---------------------------------------------------------------------- #
    # Unified cross-stage sweep pass (next-refactoring.md). Selection is cheap
    # and deterministic, so compute every requested stage's pins FIRST, union
    # the pins, and pay the expensive steps (one decode, one reassess fan-out,
    # one grading pass) ONCE over the union. Each stage's artifacts then scatter
    # back from the shared results. A single-mode run is a trivial one-mode
    # union and behaves exactly as before.
    # ---------------------------------------------------------------------- #

    # 1. Select all requested stages (CPU only, no ctx mutation, no LLM call).
    t_phase = time.perf_counter()
    selections = [
        _select_stage(
            mode=mode,
            base_candidates=base_candidates,
            pools=pool_candidates,
            n_layers=n_layers,
            gen_pos=gen_pos,
            args=args,
        )
        for mode in modes
    ]
    # Union the pin keys across stages, deduped, in first-seen order. Two pins of
    # the same feature at different positions are kept distinct (the double-dose
    # upweighting, decision 1). The union is what gets pinned and swept once.
    union_pin_keys: list[tuple] = []
    seen_pins: set = set()
    for sel in selections:
        for k in sel.pin_keys:
            if k not in seen_pins:
                seen_pins.add(k)
                union_pin_keys.append(k)
    pre_timings["selection_s"] = round(time.perf_counter() - t_phase, 3)
    n_union = len(union_pin_keys)
    n_total = sum(len(sel.pin_keys) for sel in selections)
    print(
        f"  selected {len(modes)} stage(s), {n_total} pins total, "
        f"{n_union} unique after union"
    )

    # 2. Pin the union once. pin_features strict-rejects unless the pre_hypotheses
    # keys match ctx.build_features exactly, so pass a placeholder map keyed by
    # exactly the union pin keys (the discovery reassess never shows the text).
    reset_pin_state(ctx, union_pin_keys)
    pre_hypotheses = {
        k: "deterministic seed pin (no agent triage)" for k in ctx.build_features
    }
    pin_result = pin_features(ctx, pre_hypotheses=pre_hypotheses)
    print(f"  pinned {pin_result['n_features']} union features")

    # 2b. Warm the Neuronpedia inspect cache for any union pins NOT already
    # fetched by _prepare_pool. The discovery reassess (auto-fanned-out inside
    # batched_anchor_sweep) reads ctx.inspect_cache, and the selection rows read
    # autointerp labels from it. The pool modes warmed their pool in
    # _prepare_pool, but stage i selects offline, so a union that includes stage
    # i must fetch its pins here. Fetch only the missing ones (fetch_payloads is
    # idempotent on the cache). FAIL-LOUD on a Neuronpedia error.
    if "i" in modes:
        from circuit_oracle import feature_relevance

        cache = getattr(ctx, "inspect_cache", {}) or {}
        missing_pairs = [
            (layer, feat, pos)
            for (layer, feat, pos) in union_pin_keys
            if (layer, feat, pos) not in cache and (layer, feat, None) not in cache
        ]
        if missing_pairs:
            t_phase = time.perf_counter()
            feature_relevance.fetch_payloads(ctx, missing_pairs)
            pre_timings["autointerp_fetch_s"] = round(time.perf_counter() - t_phase, 3)

    # 3. ONE ANCHOR sweep over the union (the row builder dedups by applied clamp
    # value internally, so identical clamps across pins / stages decode once).
    # ctx already carries subagent_client / subagent_model / reassess_variant, so
    # the one reassess fan-out runs over the union's shifted features inside.
    print(f"  running shared ANCHOR sweep over {n_union} union features x 4 scales ...")
    t_phase = time.perf_counter()
    sweep_result = batched_anchor_sweep(
        ctx, user_message=config.user_message, system_prompt=config.system_prompt
    )
    sweep_s = round(time.perf_counter() - t_phase, 3)
    pre_timings["anchor_sweep_s"] = sweep_s
    pre_timings["anchor_decode_s"] = sweep_result["timings"]["decode_s"]
    pre_timings["anchor_reassess_s"] = sweep_result["timings"]["reassess_s"]
    print(
        f"  shared ANCHOR done in {_human_s(sweep_s)} "
        f"(GPU decode {_human_s(pre_timings['anchor_decode_s'])} over "
        f"{sweep_result['n_decoded_rows']}/{sweep_result['n_origin_rows']} rows, "
        f"reassess LLM {_human_s(pre_timings['anchor_reassess_s'])})"
    )
    reassess_usage = sweep_result.get("reassess_usage") or {}
    reassess_cost = saving.compute_cost(reassess_usage)
    has_reassess_tokens = bool(
        reassess_usage.get("input_tokens") or reassess_usage.get("output_tokens")
    )
    if reassess_cost is not None and has_reassess_tokens:
        print(
            f"  reassess usage: in {reassess_usage.get('input_tokens', 0):,} "
            f"out {reassess_usage.get('output_tokens', 0):,} "
            f"(~${reassess_cost:.4f}, {reassess_usage.get('model')})"
        )
    union_measurements = sweep_result["measurements"]
    union_reassess = ctx.reassess_records or {}

    # 4. ONE grading pass over the union (baseline + every unique answer_after),
    # each unique answer graded --grader-repeats times. grade_sweep mutates the
    # union measurement dicts in place (each origin owns its dict, part 1's
    # share-vs-copy contract), so the per-stage scatter re-ranks safely.
    t_phase = time.perf_counter()
    union_grades = saving.grade_sweep(
        union_measurements,
        ctx.baseline_answer,
        config,
        question=config.user_message,
        n_repeats=args.grader_repeats,
    )
    pre_timings["grade_s"] = round(time.perf_counter() - t_phase, 3)
    grade_cost = saving.compute_cost(union_grades.get("usage") or {})
    print(
        f"  shared grading done in {_human_s(pre_timings['grade_s'])} "
        f"(repeats={args.grader_repeats}"
        + (f", ~${grade_cost:.4f}" if grade_cost is not None else "")
        + ")"
    )

    # 5. Scatter the shared results back into each stage's run dir. The shared
    # LLM usage blocks (relevance, grader, reassess) are amortized to a single
    # owner stage dir each, so summing compute_cost over all artifacts equals the
    # true per-slug bill (decision 4). The grader and reassess blocks land in
    # every stage dir, so their owner is the first stage run. The relevance block
    # lands ONLY in _RELEVANCE_MODES dirs, so its owner is the first such stage
    # (picking a non-relevance owner would write the real relevance block
    # nowhere and undercount). No relevance owner exists when no ii/iii stage was
    # requested, in which case no relevance.json is written anyway.
    relevance_owner = next((m for m in modes if m in _RELEVANCE_MODES), None)
    usage_owners = {
        "grader": modes[0],
        "reassess": modes[0],
        "relevance": relevance_owner,
    }
    for sel in selections:
        print(f"\n--- {slug}: stage {sel.mode} ---")
        _write_stage(
            ctx=ctx,
            selection=sel,
            slug=slug,
            graph_path=graph_path,
            config=config,
            union_measurements=union_measurements,
            union_reassess=union_reassess,
            union_grades=union_grades,
            sweep_result=sweep_result,
            n_repeats=args.grader_repeats,
            out_root=args.out_root,
            pre_timings=pre_timings,
            stage_timings={},
            usage_owners=usage_owners,
        )

    print(f"\n=== {slug}: all stages done in {_human_s(time.perf_counter() - t_slug)} ===")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    # Lazy, matching this file's convention for package imports (see the
    # `from circuit_oracle import seed_select` lines inside the stage helpers):
    # the package pulls torch, and the parser is built before ensure_venv's work
    # is needed. One list of gateways for every entry script, so adding a third
    # is an edit in llm_client rather than a hunt through the runners.
    from circuit_oracle.llm_client import PROVIDER_CHOICES

    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--slug", default=None, help="single prompt slug")
    ap.add_argument("--slugs", nargs="+", default=None, help="multiple prompt slugs")
    ap.add_argument("--all", action="store_true", help="every slug in --dataset-file")
    ap.add_argument("--dataset-file", default=DEFAULT_DATASET,
                    help=f"prompts JSON (default: {DEFAULT_DATASET})")
    ap.add_argument("--graph", default=None,
                    help="explicit graph .pt (single-slug only, default "
                         "weights/graphs/<slug>_graph.pt, fail loud if missing)")
    ap.add_argument("--graph-dir", default=default_graph_dir(),
                    help=f"dir for the default per-slug graph (default $GRAPH_STORE/graphs "
                         f"when GRAPH_STORE is set, else {DEFAULT_GRAPH_DIR})")
    ap.add_argument("--modes", nargs="+", default=list(ALL_MODES), choices=list(ALL_MODES),
                    help="sweep stages to run (default: all seven)")
    ap.add_argument("--top-k", type=int, default=20, help="features pinned per stage")
    ap.add_argument("--pool-size", type=int, default=50,
                    help="Neuronpedia + relevance fetch set for the pool stages (ii/iii/iv)")
    ap.add_argument("--drop-frac", type=float, default=0.20,
                    help="fraction of layers dropped at each end for the middle-layer band")
    # gpt-oss-120b is the standard "everything else" model (2026-07-26). The
    # grader stays gpt-5.4 deliberately: it is the oracle-model stand-in on the
    # deterministic path, mirroring the agentic self-grading design.
    ap.add_argument("--relevance-model", default="openai/gpt-oss-120b")
    ap.add_argument("--grader-model", default="openai/gpt-5.4")
    ap.add_argument("--grader-repeats", type=int, default=3,
                    help="independent temperature-1.0 grader draws per unique answer "
                         "(default 3). The per-axis MEAN is the score and the per-axis "
                         "std is stored. 1 reproduces the old single-draw behavior. "
                         "Cost scales roughly linearly in this count.")
    # Default matches the agentic pipeline subagent (scripts/run_all.py DEFAULT_SUBAGENT).
    # subagent.py already strips the gpt-oss-120b harmony reasoning channel and parses
    # the JSON from it, and saving.compute_cost prices openai/gpt-oss-120b.
    ap.add_argument("--reassess-model", default="openai/gpt-oss-120b")
    ap.add_argument("--provider", default=os.environ.get("LLM_PROVIDER", "openrouter"),
                    choices=PROVIDER_CHOICES,
                    help="gateway for the relevance / reassess / grader calls "
                         "(default: $LLM_PROVIDER or openrouter). openai/gpt-oss-120b "
                         "stays on OpenRouter either way, see llm_client._DEFAULT_MODEL_PINS")
    ap.add_argument("--model-name", default=DEFAULT_MODEL)
    ap.add_argument("--transcoder-name", default=DEFAULT_TRANSCODER)
    ap.add_argument("--out-root", default="runs",
                    help="root for the sweep run dirs. Fresh runs land in runs/ so they never "
                         "touch the committed results/ or results-workshop/ archives")
    ap.add_argument("--build", action="store_true",
                    help="build the attribution graph .pt now if it is missing, instead of "
                         "failing loud. Reuses the one model load for build + sweep, so a "
                         "single command (and a single GPU session) covers both steps. "
                         "Equivalent to running build_graph.py first.")
    # 8192 is the current refusal generation, matching build_graph.py's
    # DEFAULT_MAX_FEATURE_NODES (the authority) and run_all.py. This used to
    # default to 10000, the generation the earlier sweeps were built in, which
    # meant the same slug built through this wrapper and through build_graph.py
    # produced two non-comparable graphs. All three now agree. Pass
    # --max-feature-nodes 10000 to rebuild in the earlier generation.
    ap.add_argument("--max-feature-nodes", type=int, default=8192,
                    help="cap on feature nodes baked into the .pt when --build builds it "
                         "(default 8192, matches build_graph.py / run_all.py; 0 = unbounded). "
                         "The earlier sweeps were built at 10000, so pass that explicitly to "
                         "compare within that generation. "
                         "Ignored when the .pt already exists.")
    ap.add_argument("--dry-run", action="store_true",
                    help="stage-i selection only, stops before the model load and any LLM call")
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    # Pre-flight --grader-repeats before any GPU work. grade_sweep also raises on
    # a non-positive count, but only in step 4 of the unified pass (after the
    # model load, the shared decode, and the reassess fan-out), so a typo like
    # --grader-repeats 0 would otherwise burn the whole per-slug GPU and reassess
    # bill before failing. Mirror the early OPENROUTER_API_KEY / graph preflights.
    if not isinstance(args.grader_repeats, int) or args.grader_repeats < 1:
        raise ValueError(
            f"--grader-repeats must be a positive int, got {args.grader_repeats!r}"
        )

    # Dedup repeated --modes entries (order preserving, mirrors resolve_slugs).
    # A duplicate mode would satisfy mode == usage_owner twice, writing the real
    # shared usage blocks into two dirs and breaking the amortization invariant.
    deduped_modes = list(dict.fromkeys(args.modes))
    if len(deduped_modes) != len(args.modes):
        print(f"WARNING: duplicate --modes entries collapsed to {deduped_modes}")
        args.modes = deduped_modes

    slugs = resolve_slugs(args)

    if args.graph and len(slugs) > 1:
        print(
            "WARNING: --graph is set with multiple slugs, ignoring it and using the "
            "per-slug default weights/graphs/<slug>_graph.pt for each."
        )
        args.graph = None

    if args.dry_run:
        return _dry_run(args, slugs)

    # Pre-flight EVERY slug's graph before the one model load. Without --build a
    # missing .pt is fatal, and discovering that on slug 7 of 20 after hours of
    # sweeps is the worst possible time. --build handles missing graphs itself.
    if not args.build:
        missing = [s for s in slugs if not os.path.exists(graph_path_for(args, s))]
        if missing:
            raise FileNotFoundError(
                f"no cached graph for {len(missing)} of {len(slugs)} slug(s): "
                f"{missing}. Build them first with build_graph.py, or pass --build "
                f"to build them in this run."
            )

    # Subject model loaded ONCE for the whole slug list and threaded into every
    # _run_slug, so a 20-slug run pays the multi-minute load once. Heavy import
    # deferred so --help / --dry-run never touch torch.
    from circuit_oracle import load_model

    print(
        f"Loading subject model {args.model_name} + {args.transcoder_name} "
        f"(shared across {len(slugs)} slug(s)) ..."
    )
    t_load = time.perf_counter()
    model = load_model(args.model_name, args.transcoder_name)
    model_load_s = round(time.perf_counter() - t_load, 3)
    print(f"  model ready in {_human_s(model_load_s)}")

    for i, slug in enumerate(slugs):
        _run_slug(
            args, slug, model=model, model_load_s=model_load_s, load_paid_here=(i == 0)
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
