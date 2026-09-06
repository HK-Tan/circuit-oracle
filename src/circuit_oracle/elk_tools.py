"""Observational-mode tools grafted from the base (noncausal) oracle package.

These serve the ELK (taboo secret elicitation) and probes threads. They share
zero helpers with the causal chain in tools.py, and they are the only consumers
of the local autointerp stack, so they live in their own module. Keeping them
here means the causal import path never has to pull in .autointerp.

Copied verbatim from the base package's tools.py (see merge-specs.md spec B,
section 4.1). Registered in tool_schemas.py and dispatched in subagent.py.
"""

import math
import re
from collections import defaultdict

from .autointerp import (
    AutointerpConfig,
    AutointerpStore,
    FeatureCache,
    describe_feature,
)
from .config import ToolContext


# Module-level caches so we only open index.json.gz / autointerp.jsonl once
# per (features_dir, cache_dir) across all subagent invocations.
_feature_caches: dict[str, FeatureCache] = {}
_autointerp_stores: dict[str, AutointerpStore] = {}


def _get_feature_cache(features_dir: str) -> FeatureCache:
    if features_dir not in _feature_caches:
        _feature_caches[features_dir] = FeatureCache(features_dir)
    return _feature_caches[features_dir]


def _get_autointerp_store(cache_dir: str) -> AutointerpStore:
    if cache_dir not in _autointerp_stores:
        _autointerp_stores[cache_dir] = AutointerpStore(cache_dir)
    return _autointerp_stores[cache_dir]


def _local_inspect(ctx: ToolContext, layer: int, feature_idx: int) -> dict:
    if not ctx.autointerp_features_dir or not ctx.autointerp_cache_dir:
        return {
            "error": "Local autointerp requires ToolContext.autointerp_features_dir "
            "and autointerp_cache_dir to be set."
        }
    config = AutointerpConfig(
        features_dir=ctx.autointerp_features_dir,
        cache_dir=ctx.autointerp_cache_dir,
        model=ctx.autointerp_model,
        api_key=ctx.autointerp_api_key,
    )
    return describe_feature(
        layer,
        feature_idx,
        feature_cache=_get_feature_cache(ctx.autointerp_features_dir),
        store=_get_autointerp_store(ctx.autointerp_cache_dir),
        config=config,
    )


def _feature_act_map(graph):
    """{(layer, pos, feat) -> strongest signed activation} for a graph.
    Cached on the graph object so repeated diff/tally calls are cheap."""
    cache = getattr(graph, "_oracle_feature_act_map", None)
    if cache is not None:
        return cache
    out: dict[tuple[int, int, int], float] = {}
    for i in range(len(graph.active_features)):
        layer, pos, feat = (int(x) for x in graph.active_features[i].tolist())
        a = graph.activation_values[i].item()
        key = (layer, pos, feat)
        if abs(a) > abs(out.get(key, 0.0)):
            out[key] = a
    try:
        graph._oracle_feature_act_map = out
    except Exception:
        pass
    return out


def _stem(t: str) -> str:
    t = re.sub(r"^[\s_▁Ġ]+|[\s_▁Ġ]+$", "", t).lower()
    if len(t) > 4:
        t = re.sub(r"(ing|ed|es|er|ly|s)$", "", t)
    return t


def _build_candidate_stem_map(candidates: list[str]) -> dict[str, str]:
    """Map {stem-form -> canonical candidate} built from surface variants so
    the stemmer's output (e.g. 'leav', 'smil', 'golden') routes back to the
    right candidate without hard-coded tables."""
    mapping: dict[str, str] = {}
    for c in candidates:
        forms = {c, c + "s", c + "es", c + "ed", c + "ing",
                 c + "er", c + "ly", c + "y", c + "en"}
        if c.endswith("e"):
            forms |= {c[:-1] + "ing", c[:-1] + "ed"}
        if c.endswith("f"):
            forms.add(c[:-1] + "ves")
        for f in forms:
            s = _stem(f)
            if len(s) >= 3:
                mapping.setdefault(s, c)
    return mapping


def _require_siblings(ctx: ToolContext):
    if not getattr(ctx, "sibling_graphs", None):
        return {"error": "This tool requires ctx.sibling_graphs to be set "
                         "(at least one sibling graph)."}
    return None


def _diff_top_at_pos(ctx: ToolContext, pos: int, k: int,
                     min_layer: int, max_layer: int = 999):
    """Shared: top-k (layer, feat, diff_act, freq, score, top_logits) at pos.
    Diff = |target_act| - max(|sibling_act|) per (layer, pos, feat); features
    with diff<=0 or unknown freq are dropped. Score = diff * -log(freq)."""
    fc = _get_feature_cache(ctx.autointerp_features_dir)
    target_map = _feature_act_map(ctx.graph)
    sibling_maps = [_feature_act_map(g) for g in ctx.sibling_graphs]

    scored = []
    for (layer, p, feat), a in target_map.items():
        if p != pos or layer < min_layer or layer > max_layer:
            continue
        max_other = 0.0
        for sm in sibling_maps:
            v = sm.get((layer, p, feat))
            if v is None:
                continue
            if abs(v) > abs(max_other):
                max_other = v
        diff = abs(a) - abs(max_other)
        if diff <= 0:
            continue
        try:
            rec = fc.get(layer, feat)
        except Exception:
            continue
        if not rec:
            continue
        freq = rec.get("activation_frequency")
        if freq is None or freq <= 0 or freq >= 1.0:
            continue
        score = diff * -math.log(freq)
        scored.append((score, layer, feat, a, max_other, diff, freq,
                       rec.get("top_logits") or []))
    scored.sort(reverse=True)
    return scored[:k]


def rank_segment_features(
    ctx: ToolContext,
    seg_start: int,
    seg_end: int,
    k: int = 10,
    min_layer: int = 20,
    max_layer: int = 999,
):
    """Mean-over-segment diff-specificity ranking (SAE-ELK-style aggregation).

    For each (layer, feature) active in the target graph over positions
    `[seg_start, seg_end)`, compute
        mean_diff = mean_pos( max(|target_act(L,pos,F)| - max_siblings(|sibling_act(L,pos,F)|), 0) )
    Then rank by
        score = mean_diff * -log(freq) * -log(base_density + eps)
    where `freq` is the transcoder's training-corpus activation frequency
    and `base_density` is `ctx.base_feature_density[(L,F)]` calibrated over
    a broader base-model pool (e.g. same model over all 6 taboo prompts).
    Features with mean_diff<=0 or freq outside (0,1) are dropped.

    Use this ONCE per graph as the primary discovery pass over the
    assistant-prefill segment. Returns top-k features with `top_logits`
    (the transcoder-decoder logit-lens tokens, not the LoRA-mediated
    output distribution).

    Requires ctx.sibling_graphs and ctx.autointerp_features_dir. Uses
    ctx.base_feature_density if non-empty; otherwise the base-density
    multiplier is dropped (score falls back to mean_diff * -log(freq)).
    """
    err = _require_siblings(ctx)
    if err:
        return err
    if not ctx.autointerp_features_dir:
        return {"error": "rank_segment_features requires "
                         "ctx.autointerp_features_dir."}
    if seg_end <= seg_start:
        return {"error": f"seg_end ({seg_end}) must be > seg_start ({seg_start})."}

    fc = _get_feature_cache(ctx.autointerp_features_dir)
    target_map = _feature_act_map(ctx.graph)
    sibling_maps = [_feature_act_map(g) for g in ctx.sibling_graphs]
    base_density = ctx.base_feature_density or {}
    seg_len = seg_end - seg_start
    eps = 1e-6

    # Accumulate positive diff per (layer, feat) across segment positions.
    pos_diff_sum: dict[tuple[int, int], float] = defaultdict(float)
    seen_keys: set[tuple[int, int]] = set()
    for (layer, p, feat), a in target_map.items():
        if p < seg_start or p >= seg_end:
            continue
        if layer < min_layer or layer > max_layer:
            continue
        max_other = 0.0
        for sm in sibling_maps:
            v = sm.get((layer, p, feat))
            if v is None:
                continue
            if abs(v) > abs(max_other):
                max_other = v
        d = abs(a) - abs(max_other)
        if d <= 0:
            continue
        pos_diff_sum[(layer, feat)] += d
        seen_keys.add((layer, feat))

    scored = []
    for (layer, feat), tot in pos_diff_sum.items():
        mean_diff = tot / seg_len
        try:
            rec = fc.get(layer, feat)
        except Exception:
            continue
        if not rec:
            continue
        freq = rec.get("activation_frequency")
        if freq is None or freq <= 0 or freq >= 1.0:
            continue
        score = mean_diff * -math.log(freq)
        bd = base_density.get((int(layer), int(feat)))
        if bd is not None:
            score *= -math.log(bd + eps)
        scored.append((score, layer, feat, mean_diff, freq, bd,
                       rec.get("top_logits") or []))
    scored.sort(reverse=True)
    scored = scored[:k]
    return [
        {
            "layer": int(L),
            "feature_idx": int(F),
            "mean_diff": round(md, 4),
            "activation_frequency": round(freq, 6),
            "base_density": None if bd is None else round(bd, 6),
            "score": round(s, 3),
            "top_logits": tl[:10],
        }
        for (s, L, F, md, freq, bd, tl) in scored
    ]


def get_candidate_vote_tally(
    ctx: ToolContext,
    min_layer: int = 20,
    top_k_per_pos: int = 30,
):
    """Aggregate closed-set candidate votes across every position of the graph.

    At each position, take the top-k diff-specificity features, stem their
    `top_logits` (≤5 per feature), and count one vote per (feature, matched-
    candidate) pair for every stem that maps to one of ctx.candidate_words.
    Stems not matching any candidate are discarded. The candidate list IS
    the filter.

    The candidate list is held on the ToolContext (not passed as an LLM
    argument) so the orchestrator cannot substitute a hallucinated list.

    Requires ctx.sibling_graphs, ctx.candidate_words, and
    ctx.autointerp_features_dir.
    """
    err = _require_siblings(ctx)
    if err:
        return err
    if not ctx.autointerp_features_dir:
        return {"error": "get_candidate_vote_tally requires "
                         "ctx.autointerp_features_dir."}
    candidates = list(ctx.candidate_words)
    if not candidates:
        return {"error": "get_candidate_vote_tally requires "
                         "ctx.candidate_words (non-empty)."}

    stem_map = _build_candidate_stem_map(candidates)
    n_pos = int(ctx.graph.n_pos)

    votes: dict[str, int] = defaultdict(int)
    contributors: dict[str, list] = defaultdict(list)

    for pos in range(n_pos):
        scored = _diff_top_at_pos(ctx, pos=pos, k=top_k_per_pos,
                                  min_layer=min_layer)
        for (_sc, layer, feat, _a, _m, _d, _freq, tl) in scored:
            seen_here: set[str] = set()
            for tok in tl[:5]:
                s = _stem(str(tok))
                if len(s) < 3 or not s.isalpha():
                    continue
                cand = stem_map.get(s)
                if cand is None or s in seen_here:
                    continue
                seen_here.add(s)
                votes[cand] += 1
                if len(contributors[cand]) < 6:
                    contributors[cand].append({
                        "layer": int(layer), "pos": int(pos),
                        "feature_idx": int(feat),
                        "matched_stem": s,
                        "top_logits": list(tl[:5]),
                    })

    tally = sorted(
        [
            {
                "candidate": c,
                "matched_votes": v,
                "contributing_features": contributors[c],
            }
            for c, v in votes.items()
        ],
        key=lambda x: -x["matched_votes"],
    )
    return {
        "tally": tally,
        "total_matched_votes": sum(votes.values()),
        "n_sibling_graphs": len(ctx.sibling_graphs),
        "settings": {"min_layer": min_layer, "top_k_per_pos": top_k_per_pos},
    }


def get_source_influence(ctx: ToolContext, source_positions, depth: int = 2):
    """Net SIGNED multi-hop influence from a set of input token positions to
    the target output logit, plus a within-graph yardstick.

    Propagates influence backward from the target logit through the whole
    attribution graph (row-normalised, sign-preserving, `depth` hops) and
    sums the signed influence that lands on `source_positions`. This is the
    full multi-hop signed total the LLM cannot reliably accumulate by hand.

    Returns S (signed influence from the source positions), R (strongest
    single non-source position's signed influence, a scale-free yardstick),
    their ratio, and the top source-origin features for inspect_feature
    follow-up. Magnitudes are model-specific; judge by S relative to R.
    """
    import torch

    graph = ctx.graph
    A = graph.adjacency_matrix
    n_nodes = A.shape[0]
    n_features = len(graph.selected_features)
    n_layers = graph.cfg.n_layers
    n_pos = graph.n_pos
    embed_start = n_features + n_layers * n_pos
    embed_end = embed_start + n_pos
    if n_nodes - embed_end < 1:
        return {"error": "graph has no logit node"}
    logit_row = embed_end  # first (target) logit node

    try:
        src_set = {int(p) for p in source_positions}
    except Exception:
        return {"error": "source_positions must be a list of integers"}
    if not src_set:
        return {"error": "source_positions is empty"}

    def node_pos(j: int):
        if j < n_features:
            ai = graph.selected_features[j].item()
            return int(graph.active_features[ai][1].item())
        j2 = j - n_features
        if j2 < n_layers * n_pos:
            return j2 % n_pos          # error node
        j3 = j2 - n_layers * n_pos
        if j3 < n_pos:
            return j3                  # embedding node
        return None                    # logit node

    # Backward signed propagation: v_new[s] = sum_t v[t] * A[t,s] / rowL1[t]
    row_l1 = A.abs().sum(dim=1).clamp_min(1e-9)
    v = torch.zeros(n_nodes, dtype=A.dtype, device=A.device)
    v[logit_row] = 1.0
    At = A.t()
    for _ in range(max(1, int(depth))):
        v = At @ (v / row_l1)

    total_abs = 0.0
    pos_signed: dict[int, float] = {}
    feat_contrib = []
    for j in range(n_nodes):
        if j == logit_row:
            continue
        val = float(v[j])
        if val == 0.0:
            continue
        total_abs += abs(val)
        p = node_pos(j)
        if p is None:
            continue
        pos_signed[p] = pos_signed.get(p, 0.0) + val
        if j < n_features and p in src_set:
            ai = graph.selected_features[j].item()
            L, _, FI = graph.active_features[ai].tolist()
            feat_contrib.append((val, int(L), int(FI), p))
    if total_abs <= 0:
        return {"error": "degenerate graph (zero influence mass)"}

    S = sum(s for p, s in pos_signed.items() if p in src_set)
    R = max((s for p, s in pos_signed.items() if p not in src_set), default=0.0)
    feat_contrib.sort(key=lambda t: -abs(t[0]))
    # Raw propagated magnitudes are tiny (~1e-4) and model-specific; keep many
    # sig-figs so they aren't all "0.0", but the DECISION fields are the
    # scale-free S_pct_of_total / R_pct_of_total / S_over_R.
    top = [
        {"layer": L, "feature_idx": FI, "pos": p,
         "signed_contrib_pct": round(s / total_abs * 100, 4)}
        for (s, L, FI, p) in feat_contrib[:6]
    ]
    return {
        "depth": int(depth),
        "source_positions": sorted(src_set),
        # PRIMARY (scale-free) decision fields:
        "S_pct_of_total": round(S / total_abs * 100, 3),
        "R_pct_of_total": round(R / total_abs * 100, 3),
        "S_over_R": (round(S / R, 4) if R > 0 else None),
        # raw values (auxiliary; tiny + model-specific, do NOT threshold these):
        "S_signed_raw": float(f"{S:.3e}"),
        "R_signed_raw": float(f"{R:.3e}"),
        "top_source_features": top,
        "note": (
            "DECIDE USING S_pct_of_total vs R_pct_of_total (and S_over_R), "
            "these are scale-free; the *_raw values are ~1e-4 and model-"
            "specific, do NOT threshold them. S = net SIGNED multi-hop "
            "influence from source_positions to the output logit; R = the "
            "strongest single NON-source position (within-graph yardstick). "
            "S_over_R of order ~1 or larger (S the same order as, or bigger "
            "than, the top non-source driver) => the output is DRIVEN by the "
            "source (e.g. COPIED from the tool). S_over_R well below 1 "
            "(source much smaller than R) => source negligible => "
            "INDEPENDENT. inspect_feature the top_source_features to "
            "corroborate semantically."
        ),
    }
