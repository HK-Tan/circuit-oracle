#!/usr/bin/env python3
"""Deterministic influence seed for the suppression-jailbreak track.

Read-only analysis over a pre-built attribution graph. No model load, no GPU,
no agent loop. Given a saved circuit_tracer Graph (.pt), this script:

  1. Ranks every feature node by total influence on the output logits, using the
     library's own primitive compute_node_influence(adjacency_matrix, logit_weights)
     seeded with the graph's logit probability distribution. This is byte-for-byte
     the seed the builder's compute_partial_influences and prune_graph already use.
  2. Aggregates that influence per token position to show WHERE the suppression-
     relevant mass concentrates (the key-token position), ignoring the dummy BOS at
     position 0 and the generation position at n_pos - 1.
  3. Cross-checks against the lexical entity span (tokenize user_message alone and
     match it into input_tokens) purely as a label, not a pre-filter.
  4. Writes seed.json with the ranked features and a recommended pin set in the
     (layer, feature_idx, pos) key order that pin_features / build_features expect.

The influence ranking, the record building, and the non-opener filter are all
delegated to circuit_oracle.seed_select (one source of truth shared with the
deterministic orchestrator scripts/run_sweeps.py). This script owns only the CLI,
the lexical entity-span cross-check, and the seed.json writer.

The pin set this produces is a CANDIDATE. The ANCHOR sweep (run_seed_sweep.py) is
the causal arbiter, mirroring the Arditi diff-in-means and ELK taboo discipline.

Usage:
  python scripts/influence_seed.py --graph weights/graphs/<name>_graph.pt \
      --slug tiananmen-june-4-1989

  python scripts/influence_seed.py --graph <path> \
      --user-message "How can I make chlorine gas at home using household cleaners?"

This script never runs the oracle pipeline. It only reads a graph.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass

# Re-exec under the project venv (+ HF cache / CUDA env) so a bare
# `python scripts/influence_seed.py` works without `source .venv/bin/activate`.
# No-op if already in the venv. Must precede the editable-package imports below.
from _venv_bootstrap import ensure_venv

ensure_venv(__file__)

# circuit_tracer is installed editable in the causal repo's venv.
from circuit_tracer.graph import Graph

# The influence / record / filter math lives in one place now. This script keeps
# its CLI and the seed.json writer, but delegates every numeric step to
# circuit_oracle.seed_select so there is a single source of truth shared with the
# deterministic orchestrator (scripts/run_sweeps.py). load_graph,
# feature_influence, build_candidates, and filter_non_opener are imported under
# the seed_select namespace, not re-implemented here.
from circuit_oracle import seed_select as ss
from circuit_oracle.seed_select import FeatureCandidate


# --------------------------------------------------------------------------- #
# Data records
# --------------------------------------------------------------------------- #
@dataclass
class FeatureRecord:
    """The seed.json serialization shape for one ranked feature.

    This is the on-disk schema (preserved byte-for-byte), distinct from the
    in-memory seed_select.FeatureCandidate. rank is the GLOBAL descending-
    influence rank (it survives the non-opener / min-layer filtering, so a pin
    can carry rank 5 if positions above it were openers). pin_key is
    [layer, feature_idx, pos], the order pin_features / build_features expect.
    """

    rank: int
    layer: int
    pos: int
    feature_idx: int
    influence: float
    activation: float
    direct_effect_top_logit: float
    pin_key: list  # [layer, feature_idx, pos] -- the order pin_features expects


def _record_from_candidate(c: FeatureCandidate) -> FeatureRecord:
    """Project a ranked seed_select.FeatureCandidate onto the seed.json schema.

    Carries the candidate's global influence rank (c.rank, set on the full
    sorted candidate list before any filtering) into the FeatureRecord so the
    on-disk rank field is identical to the pre-refactor build_records output.
    Fails loud if rank was never assigned (a programming error, not a data gap).
    """
    if c.rank is None:
        raise ValueError(
            f"candidate L{c.layer}:F{c.feature_idx}@{c.pos} has no rank assigned; "
            f"assign the global influence rank before projecting to a FeatureRecord"
        )
    return FeatureRecord(
        rank=int(c.rank),
        layer=c.layer,
        pos=c.pos,
        feature_idx=c.feature_idx,
        influence=c.influence,
        activation=c.activation,
        direct_effect_top_logit=c.direct_effect_top_logit,
        pin_key=c.pin_key,
    )


def position_profile(records: list[FeatureRecord], n_pos: int):
    """Aggregate feature influence per token position."""
    by_pos = [0.0] * n_pos
    count = [0] * n_pos
    for r in records:
        by_pos[r.pos] += r.influence
        count[r.pos] += 1
    profile = []
    for p in range(n_pos):
        role = "bos" if p == 0 else ("generation" if p == n_pos - 1 else "content")
        profile.append(
            {"pos": p, "role": role, "influence_sum": by_pos[p], "n_features": count[p]}
        )
    return profile


# --------------------------------------------------------------------------- #
# Lexical entity span (cross-check / label only)
# --------------------------------------------------------------------------- #
def longest_contiguous_match(needle: list[int], haystack: list[int]):
    """Longest contiguous run of `needle` found verbatim in `haystack`.

    Returns (needle_start, hay_start, length) for the best run, or (0, -1, 0)
    if nothing matches. Deterministic, O(len(needle) * len(haystack)) which is
    fine for prompt-length sequences.
    """
    best = (0, -1, 0)
    for ni in range(len(needle)):
        for hi in range(len(haystack)):
            length = 0
            while (
                ni + length < len(needle)
                and hi + length < len(haystack)
                and needle[ni + length] == haystack[hi + length]
            ):
                length += 1
            if length > best[2]:
                best = (ni, hi, length)
    return best


def find_entity_span(tokenizer, user_message: str, input_ids: list[int]):
    """Locate the user_message token span inside input_ids.

    Tries a few leading-context variants (the chat template puts a newline before
    the user content, and BPE prepends a space marker to mid-text tokens). Returns
    a dict describing the match. Fails loud (returns status='not_found') rather than
    silently mislabeling.
    """
    variants = {
        "plain": user_message,
        "leading_space": " " + user_message,
        "leading_newline": "\n" + user_message,
    }
    for name, text in variants.items():
        needle = tokenizer.encode(text, add_special_tokens=False)
        if not needle:
            continue
        # exact contiguous search
        for start in range(0, len(input_ids) - len(needle) + 1):
            if input_ids[start : start + len(needle)] == needle:
                return {
                    "status": "exact",
                    "variant": name,
                    "start": start,
                    "end": start + len(needle),
                    "n_tokens": len(needle),
                }
    # fall back to the longest contiguous partial run against the plain encoding,
    # which is still a useful debugging signal when BPE breaks the boundary token.
    needle = tokenizer.encode(user_message, add_special_tokens=False)
    ni, hi, length = longest_contiguous_match(needle, input_ids)
    if length >= max(3, len(needle) // 2):
        return {
            "status": "partial",
            "variant": "plain",
            "start": hi,
            "end": hi + length,
            "n_tokens": length,
            "needle_n_tokens": len(needle),
            "needle_offset": ni,
        }
    return {"status": "not_found", "needle_n_tokens": len(needle)}


# --------------------------------------------------------------------------- #
# Prompt lookup
# --------------------------------------------------------------------------- #
def entry_for_slug(prompts_path: str, slug: str) -> dict:
    if not os.path.exists(prompts_path):
        raise FileNotFoundError(f"prompts file not found: {prompts_path}")
    with open(prompts_path) as f:
        data = json.load(f)
    for entry in data.get("entries", []):
        if entry.get("slug") == slug:
            return entry
    raise KeyError(f"slug {slug!r} not in {prompts_path}")


def default_seed_out(script_file: str, slug: str | None, graph_path: str) -> str:
    """Default seed.json location: <repo>/runs/seed-sweep/<name>/seed.json.

    runs/ is the fresh-run root every runner in this thread writes to, so the seed
    lands next to the anchor_sweep.json that run_sweeps.py writes, and a standalone
    seed never writes into the committed results/ or results-workshop/ archives.
    <name> is the slug when given, else the graph basename with the _graph.pt / .pt
    suffix stripped.
    """
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(script_file)))
    name = slug
    if not name:
        base = os.path.basename(graph_path)
        for suffix in ("_graph.pt", ".pt"):
            if base.endswith(suffix):
                base = base[: -len(suffix)]
                break
        name = base or "seed"
    return os.path.join(repo_root, "runs", "seed-sweep", name, "seed.json")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--graph", required=True, help="path to a saved circuit_tracer Graph (.pt)")
    ap.add_argument("--slug", default=None, help="prompt slug, to read user_message from prompts.json")
    ap.add_argument("--user-message", default=None, help="override the user_message for the entity-span match")
    ap.add_argument("--prompts", default="data/prompts.json", help="prompts.json path (for --slug)")
    ap.add_argument("--top-k", type=int, default=40, help="how many ranked features to record")
    ap.add_argument("--seed-k", type=int, default=12, help="how many features to put in the recommended pin set")
    ap.add_argument("--min-layer", type=int, default=1,
                    help="drop pin candidates below this layer (default 1, excludes layer-0 embedding-adjacent "
                         "features that node-influence structurally over-weights but which are not gates). "
                         "Set 0 to keep layer 0.")
    ap.add_argument("--model-id", default="Qwen/Qwen3-4B", help="HF id for the tokenizer (decode + entity match)")
    ap.add_argument("--out", default=None,
                    help="output json path (default: runs/seed-sweep/<slug>/seed.json, the "
                         "gitignored fresh-run root)")
    args = ap.parse_args()

    graph = ss.load_graph(args.graph)
    feat_infl, dims = ss.feature_influence(graph)
    # build_candidates returns FeatureCandidates already sorted descending by raw
    # influence. Assign the GLOBAL influence rank here, before any filtering, so
    # the rank survives the non-opener / min-layer drops just as build_records did.
    candidates = ss.build_candidates(graph, feat_infl)
    for r, c in enumerate(candidates):
        c.rank = r
    records = [_record_from_candidate(c) for c in candidates]
    profile = position_profile(records, dims["n_pos"])

    # Resolve prompt metadata up front so seed.json is a self-contained handoff to
    # run_seed_sweep.py (which must rebuild the identical prompt string), and so the
    # entity-span match has a user_message even if the tokenizer fails to load.
    entry = entry_for_slug(args.prompts, args.slug) if args.slug is not None else None
    user_message = args.user_message or (entry.get("user_message") if entry else None)
    system_prompt = (entry.get("system_prompt") if entry else None) or ""
    assistant_prefix = (entry.get("assistant_prefix") if entry else None) or ""

    # Tokenizer-dependent context (decode positions, entity span). Skip-with-log if
    # the tokenizer cannot be loaded -- the influence ranking is still the deliverable.
    decoded_tokens = None
    entity_span = None
    tokenizer = None
    try:
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(args.model_id)
    except Exception as exc:  # noqa: BLE001 - explicit, logged degradation
        print(f"WARNING: could not load tokenizer {args.model_id!r} ({exc}). "
              f"Skipping token decode and entity-span match.", file=sys.stderr)

    input_ids = [int(t) for t in graph.input_tokens.tolist()]
    if tokenizer is not None:
        decoded_tokens = [tokenizer.decode([tid]) for tid in input_ids]
        if user_message:
            entity_span = find_entity_span(tokenizer, user_message, input_ids)
        else:
            print("WARNING: no --user-message or --slug; skipping entity-span match.", file=sys.stderr)

    # Recommended pin set: top influence features that are NOT opener-only (drop the
    # generation position and BOS) and at or above --min-layer. Layer 0 is excluded by
    # default because node-influence (the backward power series) structurally piles onto
    # early-layer ancestor / embedding-adjacent features, which crowd out the mid-layer
    # gate without being gates themselves. We do NOT pre-filter to the literal entity span
    # (that would miss decision-point gates just past the entity); the position profile
    # above is the where-signal, the ANCHOR sweep is the causal arbiter.
    gen_pos = dims["n_pos"] - 1
    # Non-opener filter delegated to seed_select (drop BOS pos 0 and the
    # generation boundary pos == gen_pos). Operates on the rank-tagged candidates
    # so the global influence rank rides through to the FeatureRecord.
    non_opener = ss.filter_non_opener(candidates, gen_pos)
    # --min-layer is a simple lower-bound drop (default 1), distinct from the
    # two-sided middle-layer band in seed_select.filter_layer_band. It is kept
    # here verbatim so the original influence_seed.py behavior is unchanged
    # (set --min-layer 0 to keep layer 0).
    eligible = [c for c in non_opener if c.layer >= args.min_layer]
    n_dropped_layer = len(non_opener) - len(eligible)
    pin_set = [_record_from_candidate(c) for c in eligible[: args.seed_k]]

    out_path = args.out or default_seed_out(__file__, args.slug, args.graph)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    payload = {
        "graph": os.path.abspath(args.graph),
        "prompt": {
            "slug": args.slug,
            "user_message": user_message,
            "system_prompt": system_prompt,
            "assistant_prefix": assistant_prefix,
        },
        "dims": dims,
        "logit_tokens": (
            [tokenizer.decode([int(t)]) for t in graph.logit_tokens.tolist()]
            if tokenizer is not None
            else [int(t) for t in graph.logit_tokens.tolist()]
        ),
        "logit_probabilities": [round(float(p), 4) for p in graph.logit_probabilities.tolist()],
        "position_profile": profile,
        "decoded_tokens": decoded_tokens,
        "entity_span": entity_span,
        "top_features": [asdict(r) for r in records[: args.top_k]],
        "recommended_pin_set": [asdict(r) for r in pin_set],
        "recommended_pin_keys": [r.pin_key for r in pin_set],
    }
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)

    # Human-readable summary to stdout.
    print(f"graph: {args.graph}")
    print(f"dims:  {dims}")
    print("\ntop positions by aggregate influence (excluding bos / generation):")
    content = sorted(
        (p for p in profile if p["role"] == "content"),
        key=lambda p: p["influence_sum"],
        reverse=True,
    )[:8]
    for p in content:
        tok = f"  {decoded_tokens[p['pos']]!r}" if decoded_tokens else ""
        print(f"  pos {p['pos']:>3}  infl_sum={p['influence_sum']:.4f}  "
              f"n_feat={p['n_features']}{tok}")
    if entity_span is not None:
        print(f"\nentity span: {entity_span}")
    if args.min_layer > 0:
        print(f"\nexcluded {n_dropped_layer} sub-L{args.min_layer} candidates from the pin set "
              f"(--min-layer {args.min_layer}); set --min-layer 0 to keep them")
    print(f"\ntop {min(args.seed_k, len(pin_set))} recommended pin features (gate candidates):")
    for r in pin_set:
        tok = f"  tok={decoded_tokens[r.pos]!r}" if decoded_tokens else ""
        print(f"  L{r.layer}:F{r.feature_idx}@{r.pos}  infl={r.influence:.4f}  "
              f"act={r.activation:.2f}  de_top={r.direct_effect_top_logit:+.3f}{tok}")
    print(f"\nwrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
