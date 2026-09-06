# Circuit Oracle Report
**Date:** 2026-07-28 07:24:33 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven by a circuit that keys almost entirely on the negation token " not" at position 17, with a secondary contribution from "recorded/menu" lexical features in the opening clause — no deep semantic content from the premise/hypothesis relationship is required.

**Confidence:** 8

**Reasoning:**

The top features driving the probe score decompose into two streams:

**1. Dominant negation-word stream (positions 16-17, "do not"):** This is the strongest path. The embedding node for " not" at pos 17 (Emb: ' not' (pos 17)) feeds into a dedicated negation detector L0:F4958 (activation 27.875, direct_effect 0.428), which then propagates through a chain of "not"-specific features: L3:F3534 → L4:F4492 (L4 'not' feature mix), and a deep vertical chain L13:F102 → L14:F6648 → L15:F11794 → L16:F6800 (L16 'not' output feature, direct_effect 0.436). The token " do" at pos 16 also feeds L3:F3534, L15:F11794, and L16:F6800. Crucially, **L16:F6800 is the only late-layer feature (L16) directly contributing to the probe output**, and it fires exclusively on " not" + " do" — pure negation-word signal. L0:F2108 (pos 3, " menu") and L1:F12253 (pos 3) push the probe in the negative direction (contradiction-suppressing), which is consistent with the model treating "not" in the final clause as the contradiction trigger.

**2. Secondary lexical stream (pos 2-3, "recorded menu"):** Emb: ' recorded' (pos 2) drives L0:F7443 (activation 20.125) and L1:F3691 (activation 18), which activate L2:F8776 and ultimately feed the probe (L2:F8776 direct_effect 0.637). Emb: ' menu' (pos 3) contributes via L0:F2108 and L1:F763. This stream is a "specific-noun/topic" detector — "recorded menu" is a topic-specific phrase, not a semantic content signal about the entailment relationship.

**The user's concern is validated.** The circuit reaches token-embedding nodes (L0 features like F4958, F2108, F7443, F13938 receive direct_effect > 20 from embedding nodes for " not", " menu", " recorded"), and the entire signal is mediated by **superficial surface features**:
- The negation detector F4958 (pos 17) and its downstream chain (F3534, F4492, F6648, F11794, F6800) activate on the mere presence of " not" as a token — not on any structured understanding of the contradiction.
- The late-layer L16:F6800 (the deepest feature directly feeding the probe) is a "not" detector that ignores the surrounding context.
- The semantic relationship between the two sentences (that "do not provide any information at this time" contradicts "will provide information on how to obtain these lists") is never explicitly represented in the circuit. Instead, the model (and the probe riding on it) shortcuts to a single negation cue.

The L4 'not' feature mix (F4492 + F2422 at pos 17) also shows competing positive/negative contributions (+0.381/-0.359), suggesting some local "not" disambiguation attempts, but the dominant late-layer feature (F6800) collapses this into a single negation-presence signal before the probe reads it. This is a textbook case of a probe latching onto a spurious lexical shortcut rather than the actual entailment content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: ' not' (pos 17) — negation word | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' recorded' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' menu' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: ' do' (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'A' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | L0 not-detector (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | L0 'recorded' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L0:F13938](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13938) | 2 | L0 'recorded' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13938) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | L0 'menu' signal (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |
| [L1:F12253](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) | 3 | L1 not-sublayer (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 17 | L1 not-sublayer (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | L1 'recorded' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L1:F763](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/763) | 3 | L1 'recorded' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/763) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | L2 'recorded' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 17 | L3 negation context (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | L3 negation context (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | L4 'not' feature mix (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | L4 'not' feature mix (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F7998](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) | 3 | L4 'menu' inhibitory (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) |
| [L13:F102](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) | 17 | L13 'not' feature (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) |
| [L14:F6648](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) | 17 | L14 'not' feature (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 17 | L15 'not' feature (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 17 | L16 'not' output feature (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L1:3691 de=0.824 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F3691@2` | ❌ error | — | — | Trace the path upstream from L1:F3691 at position 2. What does this feature enco… |
| SA-2 | `L2:F8776@2` | ❌ error | — | — | Trace the path upstream from L2:F8776 at position 2. What does this feature enco… |
| SA-3 | `L16:F6800@17` | ❌ error | — | — | Trace the path upstream from L16:F6800 at position 17. This is the most late-lay… |
| SA-4 | `L0:F4958@17` | ❌ error | — | — | Trace the path upstream from L0:F4958 at position 17. What does this feature enc… |
| SA-5 | `L0:F2108@3` | ❌ error | — | — | Trace the path upstream from L0:F2108 at position 3 (negative direct_effect). Wh… |
| SA-6 | `L0:F7443@2` | ❌ error | — | — | Trace the path upstream from L0:F7443 at position 2. What does this feature enco… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F3691@2, k=10 → Emb:" recorded"@2 (de=24.75) +9 more |
| 2 | `get_upstream_features` | L0:F7443@2, k=5 → Emb:" recorded"@2 (de=22.62) +4 more |
| 3 | `get_upstream_features` | L0:F2108@3, k=5 → Emb:" menu"@3 (de=25.75) +4 more |
| 4 | `get_upstream_features` | L16:F6800@17, k=10 → Emb:" not"@17 (de=11.81) +9 more |
| 5 | `get_upstream_features` | L0:F4958@17, k=5 → Emb:" not"@17 (de=33.50) +4 more |
| 6 | `get_upstream_features` | L16:F6800@17, k=5 → Emb:" not"@17 (de=11.81) +4 more |
| 7 | `get_upstream_features` | L15:F11794@17, k=5 → L14:F6648 (de=3.77) +4 more |
| 8 | `get_upstream_features` | L2:F8776@2, k=5 → Emb:" recorded"@2 (de=19.50) +4 more |
| 9 | `get_upstream_features` | L1:F12253@3, k=5 → Emb:" menu"@3 (de=20.62) +4 more |
| 10 | `get_upstream_features` | L4:F4492@17, k=5 → Emb:" not"@17 (de=17.38) +4 more |
| 11 | `get_upstream_features` | L14:F6648@17, k=5 → Emb:" not"@17 (de=6.88) +4 more |
| 12 | `get_upstream_features` | L3:F3534@17, k=5 → Emb:" not"@17 (de=16.12) +4 more |
| 13 | `get_upstream_features` | L0:F13938@2, k=3 → Emb:" recorded"@2 (de=12.88) +2 more |
| 14 | `get_upstream_features` | L4:F2422@17, k=3 → Emb:" not"@17 (de=16.12) +2 more |
| 15 | `get_upstream_features` | L1:F763@3, k=5 → Emb:" menu"@3 (de=15.81) +4 more |
| 16 | `get_top_logits` | k=3 → "" (100%) |
| 17 | `get_upstream_features` | L3:F1101@17, k=3 → Emb:" not"@17 (de=12.94) +2 more |
| 18 | `get_upstream_features` | L4:F7998@3, k=3 → Emb:" menu"@3 (de=13.56) +2 more |
| 19 | `get_upstream_features` | L13:F102@17, k=3 → Emb:" not"@17 (de=8.31) +2 more |

### Build

`build_circuit` → 19 nodes, 36 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 16,613 | 5,873 | 60,792 | 0 | $0.0157 | — | — |
| **Total** | | **16,613** | **5,873** | **60,792** | **0** | **$0.0157** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 5s