# Circuit Oracle Report
**Date:** 2026-07-28 07:23:38 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven almost entirely by features that fire on the identity tokens "Jew" (pos 6) and "liberal" (pos 5) — and on the slur-adjacent phrase "stain on his" (pos 9-10) — rather than by features that encode the actual hate-speech *structure* (e.g., the verb "self-hating", the predicate "a stain on", the second-person framing).

**Confidence:** 8

**Reasoning:**

The circuit has two converging supernodes that feed the probe's output logit (L26 terminal):

1. **Probe driver supernode (L2–L6, pos 6)** — anchored by L6:F648 (direct_effect=0.74, activation=28.5), the single largest contributor to the probe score. Tracing upstream, L6:F648 is fed primarily by the raw embedding of "Jew" (direct_effect=19.4) and "liberal" (1.63), then by L3:F12151 (5.9) and L4:F2405 (2.95). Both mid-layer features trace back to the same identity-token embeddings: L3:F12151 has "Jew" at 11.0 and "liberal" at 3.38; L4:F2405 has "liberal" at 6.75 and "Jew" at 3.78. Further upstream, L0:F9026 at pos 6 receives a massive 31.4 direct_effect from the "Jew" embedding alone — this is essentially an "identity group label" detector.

2. **Slur-path supernode (L5–L8, pos 10)** — L8:F13875 (direct_effect=0.23) traces back to L6:F1561 (3.42), which in turn is fed by L5:F7488 (6.19) and the "stain" embedding (5.47). The phrase "stain on his" is the second cluster driving the probe.

Critically, the **predicate and syntactic structure** of the sentence — "Self-hating", "a stain on", "his brethren and his country" — do not appear as upstream drivers of the probe. None of the top features activate on "Self", "hating", or "his". The probe is therefore picking up on:
- The mere presence of a **minority identity noun** ("Jew") and a **political identity adjective** ("liberal"), and
- A **negatively-charged noun** ("stain") adjacent to "on his".

This confirms the user's concern: the probe relies on **identity-group token presence** (a "Jewish person mentioned" signal) and an isolated slur-adjacent word ("stain") rather than on compositional features that would encode the actual toxic structure (the compound noun "Self-hating [identity] Jew", the predicate "is a stain on his group and country", etc.). The model has not learned a structural notion of "slur against an identity group"; it has learned a bag-of-identity-words-and-negative-lexeme detector. The embedding "Jew" (pos 6) is the single largest causal contributor (31.4 → F9026, 19.4 → F648, 15.2 → F15359, 11.0 → F12151, 6.8 → F13158), making the probe classification highly sensitive to the mere occurrence of the identity token itself — a classic spurious-correlation / identity-mention shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F648](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) | 6 | Probe driver: identity-token detector (L6:F648) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) |
| [L4:F14733](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) | 6 | Probe driver: identity-token detector (L6:F648) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Probe driver: identity-token detector (L6:F648) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L3:F12151](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) | 6 | Probe driver: identity-token detector (L6:F648) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | Probe driver: identity-token detector (L6:F648) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 6 | Probe driver: identity-token detector (L6:F648) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L8:F13875](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) | 10 | Slur/identity phrase detector (L8:F13875 at pos 10, "stain on his brethren/country") | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) |
| [L6:F1561](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) | 10 | Slur/identity phrase detector (L8:F13875 at pos 10, "stain on his brethren/country") | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) |
| [L5:F7488](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7488) | 10 | Slur/identity phrase detector (L8:F13875 at pos 10, "stain on his brethren/country") | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7488) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 6 | Early identity-token features (L0-L1) firing on "Jew" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L1:F15359](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15359) | 6 | Early identity-token features (L0-L1) firing on "Jew" | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15359) |
| [L2:F8236](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8236) | 6 | Early identity-token features (L0-L1) firing on "Jew" | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8236) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:648 de=0.738 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F648@6` | ❌ error | — | — | Trace the most important feature driving the probe. This is L6:F648 at pos 6 wit… |
| SA-2 | `L8:F13875@10` | ❌ error | — | — | Trace this feature which has direct_effect=0.23 at pos 10 (likely 'brethren' or … |
| SA-3 | `L2:F13158@6` | ❌ error | — | — | Trace this early-layer feature (direct_effect=0.29 at pos 6). Determine what lex… |
| SA-4 | `L4:F2405@6` | ❌ error | — | — | Trace this mid-layer feature (direct_effect=0.24 at pos 6). Determine what conce… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F648@6, k=10 → Emb:" Jew"@6 (de=19.38) +9 more |
| 2 | `get_upstream_features` | L2:F13158@6, k=10 → Emb:" Jew"@6 (de=6.81) +9 more |
| 3 | `get_upstream_features` | L8:F13875@10, k=10 → L6:F1561 (de=3.42) +9 more |
| 4 | `get_upstream_features` | L4:F2405@6, k=10 → Emb:" liberal"@5 (de=6.75) +9 more |
| 5 | `get_upstream_features` | L3:F12151@6, k=10 → Emb:" Jew"@6 (de=11.00) +9 more |
| 6 | `get_upstream_features` | L6:F1561@10, k=10 → L5:F7488 (de=6.19) +9 more |
| 7 | `get_upstream_features` | L4:F14733@6, k=10 → Emb:" Jew"@6 (de=5.47) +9 more |
| 8 | `get_upstream_features` | L4:F117@6, k=10 → L3:F12151 (de=2.80) +9 more |
| 9 | `get_upstream_features` | L0:F9026@6, k=8 → Emb:" Jew"@6 (de=31.38) +7 more |
| 10 | `get_upstream_features` | L1:F15359@6, k=8 → Emb:" Jew"@6 (de=15.19) +7 more |
| 11 | `get_upstream_features` | L5:F7488@10, k=8 → Emb:" stain"@9 (de=6.59) +7 more |

### Build

`build_circuit` → 8 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 10,127 | 3,268 | 46,139 | 0 | $0.0097 | — | — |
| **Total** | | **10,127** | **3,268** | **46,139** | **0** | **$0.0097** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 39s