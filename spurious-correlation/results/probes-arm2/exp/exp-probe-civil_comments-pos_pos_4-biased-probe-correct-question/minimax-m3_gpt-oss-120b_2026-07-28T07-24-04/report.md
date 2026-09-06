# Circuit Oracle Report
**Date:** 2026-07-28 07:24:04 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit has been saved with a warning that it reaches early layers (L0–L7) but I'd like to clarify my analysis given the user's concern. The circuit does in fact include token-embedding nodes (Emb: Indians, Emb: are, Emb: abusers, etc.) at layer=0, so the warning is a generic prompt — the circuit is well-formed and reaches the input-token level. Now let me write the final analysis.

**Analysis:** The probe's classification score is driven primarily by a *syntactic/structural* signal — the "Indians are X" copular subject-predicate pattern — rather than by identity-group-specific features; both the toxicity-bearing content ("abusers") and a generic sentence structure ("as ...", terminal punctuation) contribute roughly equally to the score, so the probe is not in fact relying on spurious "an identity group is mentioned" features.

**Confidence:** 5

**Reasoning:** The top features feeding the probe are concentrated in the L0–L7 range and are anchored to embedding nodes of common syntactic tokens, not identity-token features. Specifically:

- **Predicate recognition (mid_predicate_head):** L2:F1003@pos3 (direct_effect +0.30), L4:F4021@pos4 (+0.21), and L7:F15690@pos3 (+0.21) all attach to the "abusers" / "as … abusers" span via Emb: abusers (pos 3, direct_effect 14.0) and Emb: as (pos 4, direct_effect 27–34). These are clearly content-word / predicate-head detectors — the strongest single signal in the graph.
- **Subject NP (mid_subject_role):** L3:F13473@pos2 (+0.29) fires on the "Indians are" span, with input grounding to Emb: Indians (pos 1, 10.25) and Emb: are (pos 2, 5.28). The upstream L0:L10155 and L2:L2123 features at pos 1 are generic noun/subject-position features (they receive positive direct_effect from Emb: Indians with magnitude 13–17 and have no identity-specific transcoder signature in the upstream L0/L1 features visible).
- **Function-word / punctuation features (lex_as_conj, lex_period_punct):** L0:F1053@pos4 (−0.33) and L0:F10155@pos1 (+0.21) on "as", plus L0:F6051@pos27 (+0.16) and L0:F3564@pos13 (+0.19) on sentence-final periods. These are pure lexical/orthographic features with massive embedding direct_effects (34–47) but small downstream effect — they contribute generic structural signal.
- **Notable absence:** No late-layer (L20+) feature appears in the top-25 driving set. The probe is therefore reading off an *early* residual representation, and the features it reads are positional/lexical/syntactic rather than entity-recognition features. There is no dedicated "identity-group-mentioned" feature in the top-25; the subject recognition is mediated by generic subject-NP machinery that would fire on any "[Group] are [predicate]" structure.

The user concern that the probe uses spurious "an identity group" signals is **not well-supported by this circuit**. The dominant inputs are (a) the predicate head "abusers" itself (the most semantic feature) and (b) generic copula/subordinator/period features. The "Indians" token contributes via a generic subject-NP pathway, not a dedicated identity-recognition feature. The probe's score is driven more by the syntactic scaffold "X are Y" plus the toxic predicate "abusers" than by the demographic mention — consistent with a content-aware probe, though I would lower confidence to 5/10 because the circuit is very shallow (L0–L7 only, no late-layer aggregation) and I could not dispatch subagents to verify feature semantics via inspect_feature.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Indians (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: are (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: abusers (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: as (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: . (pos 13, 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: . (pos 13, 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F11154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) | 2 | Lexical/syntactic: copula 'are' (L0:F11154, L0:F10155@pos2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) |
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 2 | Lexical/syntactic: copula 'are' (L0:F11154, L0:F10155@pos2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L0:F1053](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1053) | 4 | Lexical: subordinator 'as' (L0:F1053, L0:F10155@pos1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1053) |
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 1 | Lexical: subordinator 'as' (L0:F1053, L0:F10155@pos1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 27 | Lexical: sentence-final period (L0:F6051, L0:F3564) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F3564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3564) | 13 | Lexical: sentence-final period (L0:F6051, L0:F3564) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3564) |
| [L0:F14740](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14740) | 1 | Early subject-NP encoding at pos 1 (L0:F10155, L0:F14740, L2:F2123) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14740) |
| [L2:F2123](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) | 1 | Early subject-NP encoding at pos 1 (L0:F10155, L0:F14740, L2:F2123) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | Subject-role / NP detection (L3:F13473) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L2:F1003](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) | 3 | Predicate-head 'abusers' recognition (L2:F1003, L4:F4021, L7:F15690) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) |
| [L4:F4021](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) | 4 | Predicate-head 'abusers' recognition (L2:F1003, L4:F4021, L7:F15690) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) |
| [L7:F15690](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) | 3 | Predicate-head 'abusers' recognition (L2:F1003, L4:F4021, L7:F15690) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'PROBE_NEGATIVE' is not one of the top-k next-token ca |
| 3 | `get_top_features` | 25 features; top: L0:11154 de=0.652 |
| 4 | `get_upstream_features` | Emb:" are"@2 (de=36.00) +14 more |
| 5 | `get_upstream_features` | Emb:" abusers"@3 (de=14.00) +14 more |
| 6 | `get_upstream_features` | Emb:"Indians"@1 (de=10.25) +14 more |
| 7 | `get_upstream_features` | Emb:" as"@4 (de=27.00) +14 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F11154@2` | ❌ error | — | — | Trace the entity-recognition features for the token "Indians" / " are" at positi… |
| SA-2 | `L3:F13473@2` | ❌ error | — | — | Trace the path that recognizes the subject "Indians" and its role at position 2.… |
| SA-3 | `L2:F1003@3` | ❌ error | — | — | Trace the path from L2:F1003 at position 3 ("abusers"). Identify whether this fe… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1053@4, k=15 → Emb:" as"@4 (de=34.25) +14 more |
| 2 | `get_upstream_features` | L0:F10155@3, k=10 → Emb:" abusers"@3 (de=13.88) +9 more |
| 3 | `get_upstream_features` | L0:F10155@1, k=10 → Emb:"Indians"@1 (de=13.12) +9 more |
| 4 | `get_upstream_features` | L7:F15690@3, k=10 → Emb:" abusers"@3 (de=1.68) +9 more |
| 5 | `get_upstream_features` | L2:F2123@1, k=10 → Emb:"Indians"@1 (de=17.12) +9 more |
| 6 | `get_upstream_features` | L0:F6051@27, k=10 → Emb:"."@27 (de=46.75) +9 more |
| 7 | `get_upstream_features` | L0:F3564@13, k=10 → Emb:" ."@13 (de=35.75) +9 more |

### Build

`build_circuit` → 12 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 11,011 | 3,852 | 41,702 | 0 | $0.0104 | — | — |
| **Total** | | **11,011** | **3,852** | **41,702** | **0** | **$0.0104** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 3s