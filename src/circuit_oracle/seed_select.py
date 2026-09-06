"""Pure-CPU feature ranking library for the deterministic seed sweep.

One source of truth for the influence math behind the suppression-jailbreak
seed sweep. The score for each feature node is the row-normalized transitive
total effect on the output logit (circuit_tracer.graph.compute_node_influence),
seeded with the graph's logit probability distribution. This module lifts that
math out of scripts/influence_seed.py so the deterministic orchestrator
(scripts/run_sweeps.py) and the standalone seed script share one implementation.

No HTTP, no LLM, no subject-model load. The only IO is loading the saved
attribution graph (.pt) via load_graph. The relevance and rarity multipliers
are filled in by the orchestrator (from feature_relevance + Neuronpedia) and
read back here, so this module never reaches the network.

Ranking stages (see the plan, "Ranking math (exact)"):

  i      score = influence                                  + middle-layer band
  ii-a   score = influence * relevance
  ii-b   score = influence * relevance                      + middle-layer band
  iii-a  score = influence * relevance * neglog_rho
  iii-b  score = influence * relevance * neglog_rho         + middle-layer band
  iv-a   score = influence * neglog_rho
  iv-b   score = influence * neglog_rho                     + middle-layer band

Stage iv is the no-LLM challenger: rarity stands in for the relevance gate, so
selection never calls the relevance scorer (Neuronpedia still supplies
frac_nonzero).

Fail-loud everywhere. A missing relevance (ii/iii), a missing neglog_rho
(iii/iv), or a None frac_nonzero in the pool raises with the offending feature
named. No silent fallbacks, no fabricated defaults.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Optional

import torch

# circuit_tracer is installed editable in the causal repo's venv.
from circuit_tracer.graph import Graph, compute_node_influence


# Stage identifiers accepted by rank(). The "-b" modes apply the layer band.
RANK_MODES = ("i", "ii-a", "ii-b", "iii-a", "iii-b", "iv-a", "iv-b")
_BAND_MODES = ("i", "ii-b", "iii-b", "iv-b")
_RELEVANCE_MODES = ("ii-a", "ii-b", "iii-a", "iii-b")
_RARITY_MODES = ("iii-a", "iii-b", "iv-a", "iv-b")


# --------------------------------------------------------------------------- #
# Candidate record
# --------------------------------------------------------------------------- #
@dataclass
class FeatureCandidate:
    """One feature node, with the influence-derived base fields and the
    later-filled selection fields.

    The base fields (layer, pos, feature_idx, influence, activation,
    direct_effect_top_logit) come straight from the graph. The orchestrator
    fills relevance and frac_nonzero from the Neuronpedia + relevance pass,
    attach_neglog_rho fills neglog_rho, and rank fills score and rank.

    pin_key returns [layer, feature_idx, pos], the key order pin_features and
    ctx.build_features expect (NOT layer, pos, feature_idx).
    """

    layer: int
    pos: int
    feature_idx: int
    influence: float
    activation: float
    direct_effect_top_logit: float
    # Later-filled selection fields.
    relevance: Optional[float] = None
    frac_nonzero: Optional[float] = None
    neglog_rho: Optional[float] = None
    score: Optional[float] = None
    rank: Optional[int] = None

    @property
    def pin_key(self) -> list:
        return [self.layer, self.feature_idx, self.pos]


# --------------------------------------------------------------------------- #
# Graph loading and base influence
# --------------------------------------------------------------------------- #
def load_graph(path: str) -> Graph:
    """Load a saved circuit_tracer Graph (.pt) onto CPU. Fail loud if absent."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"graph not found: {path}")
    return Graph.from_pt(path, map_location="cpu")


def feature_influence(graph: Graph):
    """Return (feat_influence[n_features], dims).

    Seeds logit_weights with the graph's logit probability distribution and runs
    compute_node_influence. Casts to float32 for a stable CPU computation (the
    saved adjacency is often bf16). This is byte-for-byte the seed the builder's
    compute_partial_influences and prune_graph already use.

    dims carries n_nodes, n_features, n_pos, n_logits. gen_pos is dims["n_pos"]
    minus 1 (computed by the caller, matching influence_seed.py).
    """
    adj = graph.adjacency_matrix.float()
    n_nodes = adj.shape[0]
    n_logits = len(graph.logit_tokens)
    n_features = len(graph.selected_features)
    n_pos = len(graph.input_tokens)

    if n_logits <= 0:
        raise ValueError("graph has no logit nodes, cannot seed influence")

    logit_weights = torch.zeros(n_nodes, dtype=torch.float32)
    logit_weights[-n_logits:] = graph.logit_probabilities.float()

    node_influence = compute_node_influence(adj, logit_weights)
    feat_influence = node_influence[:n_features]

    dims = {
        "n_nodes": int(n_nodes),
        "n_features": int(n_features),
        "n_pos": int(n_pos),
        "n_logits": int(n_logits),
    }
    return feat_influence, dims


def build_candidates(graph: Graph, influence: torch.Tensor) -> list[FeatureCandidate]:
    """Map each feature column back to (layer, pos, feature_idx) and build
    candidates sorted descending by raw influence.

    Reuses the selected_features -> active_features mapping from
    influence_seed.build_records. selected_features[i] indexes into
    active_features, whose rows are (layer, pos, feature_idx) triples, and into
    activation_values. direct_effect_top_logit is the column entry of the top-1
    logit row (row -n_logits of the adjacency matrix).
    """
    n_features = len(graph.selected_features)
    n_logits = len(graph.logit_tokens)
    # Direct effect to the top-1 logit (logit rank 0 lives at row -n_logits).
    top_logit_row = graph.adjacency_matrix.float()[-n_logits]

    order = torch.argsort(influence, descending=True)
    cands: list[FeatureCandidate] = []
    for i in order.tolist():
        active_idx = int(graph.selected_features[i])
        layer, pos, feature_idx = (int(x) for x in graph.active_features[active_idx].tolist())
        cands.append(
            FeatureCandidate(
                layer=layer,
                pos=pos,
                feature_idx=feature_idx,
                influence=float(influence[i]),
                activation=float(graph.activation_values[active_idx]),
                direct_effect_top_logit=float(top_logit_row[i]),
            )
        )
    return cands


# --------------------------------------------------------------------------- #
# Filters
# --------------------------------------------------------------------------- #
def filter_non_opener(cands: list[FeatureCandidate], gen_pos: int) -> list[FeatureCandidate]:
    """Drop the BOS position (pos 0) and the generation boundary (pos == gen_pos).

    gen_pos is dims["n_pos"] - 1 (the caller computes it). Order is preserved.
    """
    return [c for c in cands if c.pos != 0 and c.pos != gen_pos]


def layer_band_bounds(n_layers: int, drop_frac: float = 0.20) -> tuple[int, int]:
    """Inclusive keep-bounds for the middle-layer band.

    Drops the bottom and top drop_frac of the layer index range. With layer
    indices spanning 0..(n_layers - 1):

        lo = ceil(drop_frac * (n_layers - 1))
        hi = floor((1 - drop_frac) * (n_layers - 1))

    Keep layers lo..hi inclusive. For n_layers == 36 and drop_frac == 0.20 this
    is lo = ceil(0.20 * 35) = 7 and hi = floor(0.80 * 35) = 28, so the gate at
    L11 survives. Read n_layers from graph.cfg.n_layers upstream, never hardcode.
    """
    span = n_layers - 1
    lo = math.ceil(drop_frac * span)
    hi = math.floor((1.0 - drop_frac) * span)
    return lo, hi


def filter_layer_band(
    cands: list[FeatureCandidate], n_layers: int, drop_frac: float = 0.20
) -> list[FeatureCandidate]:
    """Keep only candidates whose layer is inside the middle-layer band.

    The band can drop a real gate (that is the point of comparing i vs ii-a /
    iii-a). Order is preserved.
    """
    lo, hi = layer_band_bounds(n_layers, drop_frac)
    return [c for c in cands if lo <= c.layer <= hi]


# --------------------------------------------------------------------------- #
# Pool and rarity weight
# --------------------------------------------------------------------------- #
def candidate_pool(cands: list[FeatureCandidate], pool_size: int = 50) -> list[FeatureCandidate]:
    """Top-N candidates by raw influence (the ii/iii Neuronpedia + relevance set).

    Assumes cands is already influence-sorted descending (build_candidates output).
    A gate buried below pool_size cannot be rescued by ii/iii reweighting, so the
    orchestrator exposes pool_size.
    """
    return cands[:pool_size]


def attach_neglog_rho(pool: list[FeatureCandidate]) -> list[FeatureCandidate]:
    """Fill neglog_rho on every pool candidate from frac_nonzero (corpus rarity).

    rho = frac_nonzero clamped into [1e-6, 1], raw = -log(clamp(rho)) in [0, 13.8],
    then neglog_rho = raw / max(raw) over the pool so values land in [0, 1] and the
    three factors are all unit-interval multipliers (stage iii is a clean refinement
    of stage ii). Mutates and returns the same list.

    The lower bound is 0, not a strict positive: a feature with frac_nonzero == 1.0
    (fires on every token) clamps to rho == 1, raw == -log(1) == 0, so its
    neglog_rho is exactly 0 and its stage-iii score is zeroed out. That is by design
    (a feature firing everywhere is maximally generic, so rarity says ignore it), and
    the report's selection table makes any such zeroed feature visible. No epsilon
    floor is applied (that would be a fabricated default).

    Fail loud (raise) if any frac_nonzero is None, naming the offending feature.
    A degenerate all-zero raw vector (every rho clamped to 1) also raises, since a
    zero divisor would otherwise fabricate NaN weights.
    """
    raws: list[float] = []
    for c in pool:
        if c.frac_nonzero is None:
            raise ValueError(
                f"frac_nonzero is None for feature L{c.layer}:F{c.feature_idx}@{c.pos}, "
                f"cannot compute the -log(rho) rarity weight (abort the rarity stage, no default)"
            )
        rho = min(max(float(c.frac_nonzero), 1e-6), 1.0)
        raws.append(-math.log(rho))

    max_raw = max(raws)
    if max_raw <= 0.0:
        raise ValueError(
            "all pool frac_nonzero values clamp to rho == 1 (raw -log(rho) is all zero), "
            "cannot normalize the rarity weight"
        )

    for c, raw in zip(pool, raws):
        c.neglog_rho = raw / max_raw
    return pool


# --------------------------------------------------------------------------- #
# Ranking
# --------------------------------------------------------------------------- #
def _score_for(c: FeatureCandidate, mode: str) -> float:
    """Per-stage score for one candidate. Fail loud on missing factors."""
    score = c.influence
    if mode in _RELEVANCE_MODES:
        if c.relevance is None:
            raise ValueError(
                f"relevance is None for feature L{c.layer}:F{c.feature_idx}@{c.pos}, "
                f"required for stage {mode!r} (run the relevance pass first, no default)"
            )
        score = score * c.relevance
    if mode in _RARITY_MODES:
        if c.neglog_rho is None:
            raise ValueError(
                f"neglog_rho is None for feature L{c.layer}:F{c.feature_idx}@{c.pos}, "
                f"required for stage {mode!r} (call attach_neglog_rho first, no default)"
            )
        score = score * c.neglog_rho
    return score


def rank(
    cands: list[FeatureCandidate],
    mode: str,
    *,
    n_layers: int,
    top_k: int = 20,
    drop_frac: float = 0.20,
) -> list[FeatureCandidate]:
    """Score, sort, and return the top_k candidates for a sweep stage.

    mode in {"i", "ii-a", "ii-b", "iii-a", "iii-b", "iv-a", "iv-b"}:
      i      score = influence,                              band first
      ii-a   score = influence * relevance
      ii-b   score = influence * relevance,                  band first
      iii-a  score = influence * relevance * neglog_rho
      iii-b  score = influence * relevance * neglog_rho,      band first
      iv-a   score = influence * neglog_rho
      iv-b   score = influence * neglog_rho,                  band first

    The "-b" modes (and stage i) apply filter_layer_band before scoring. Sets
    .score and .rank (0-based, post-sort) on each returned candidate and returns
    the top_k. If fewer than top_k candidates survive the band, returns what
    remains (does NOT pad). The orchestrator logs the short count.

    Fail loud on an unknown mode, a missing relevance (ii/iii), or a missing
    neglog_rho (iii/iv). Pass n_layers from graph.cfg.n_layers, never hardcode.
    """
    if mode not in RANK_MODES:
        raise ValueError(f"unknown rank mode {mode!r}, expected one of {RANK_MODES}")

    pool = cands
    if mode in _BAND_MODES:
        pool = filter_layer_band(pool, n_layers, drop_frac)

    scored = list(pool)
    for c in scored:
        c.score = _score_for(c, mode)

    # Sort descending by score. ties broken by influence then by pin_key for a
    # deterministic order (no reliance on input order under equal scores).
    scored.sort(
        key=lambda c: (c.score, c.influence, -c.layer, -c.feature_idx, -c.pos),
        reverse=True,
    )

    top = scored[:top_k]
    for r, c in enumerate(top):
        c.rank = r
    return top
