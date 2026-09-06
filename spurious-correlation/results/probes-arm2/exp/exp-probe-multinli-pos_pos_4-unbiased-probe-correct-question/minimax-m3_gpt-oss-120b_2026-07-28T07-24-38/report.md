# Circuit Oracle Report
**Date:** 2026-07-28 07:24:38 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This attribution graph reveals that a contradiction-classification probe on Gemma-2-2B is driven by a mix of genuinely semantic negation features and shallow function-word / structural cues, with the content ("map", "tours", "usually") contributing little — confirming the user's hypothesis that the probe leans on spurious, surface-level signals.

**Confidence:** 8

**Reasoning:**

The probe's contradiction score is built from three supernodes, all dominated by Layer 0–3 features with trivially traceable embedding origins (every path bottoms out at raw token embeddings within one hop).

1. **L2_no_one_pos16_17 (negation phrase).** The most semantically meaningful signal. L2:F13586 at pos 17 (" one") has direct_effect −0.21, but L0:F4438 (pos 17, act 29.9) and L0:F11351 (pos 17, act 27.9) are huge " one" detectors, and their biggest upstream is Emb:'No' (pos 16) — e.g., F4438 receives 29.4 from "No" and 14.4 from " one". This is a real co-occurrence pattern encoding the negation phrase **"No one"** — the single most important semantic cue for contradiction here.

2. **L0_function_words_neg (the spurious signals).** The user's concern is well-founded. Seven of the top features are extremely shallow:
   - F8974 on " from" (de=−0.41) — pure function word.
   - F7321 on " so" (de=+0.38) — the contrastive conjunction "so you'll have to…".
   - F6051 on "." (de=−0.19) — sentence-end punctuation.
   - F2238 on " about" (de=−0.19), F306 on " tourist" (de=+0.19), F7204, F8444.
   
   These are Layer-0 lexical detectors with massive activations (17–40) and large signed direct effects. They fire on generic English connectives, articles, and punctuation, not on any contradiction-specific semantic content. The probe has latched onto " so" (the pivot that introduces the corrective clause) and "No" as cheap heuristics.

3. **L1_to_L3_tours_usually (content words — weakest).** Features for "tours" (F14413, F6872, F9924, F10891, F8380), "usually" (F8159, F10901, F2854, F3507, F6518, F12167, F5495), "map" (F474, F12851, F5038, F6495, F6356), and "Pick" (F10904) are spread across L0–L3 but their direct effects are small (−0.14 to −0.21). Tracing upstream, F6872, F9924, F10891, F8380 all bottom at Emb:'tours' with de 5–20, and the "usually" cluster (F2854, F3507, F6518, F12167) bottoms at Emb:'usually' (de 12–20). F10901 (L3, pos 19, "usually") has de=−0.14, contributing mildly toward contradiction — likely because "usually" weakens the first sentence's guarantee.

**Verdict on the user's hypothesis:** Confirmed. The contradiction probe is only partially driven by the genuinely semantic "No one is usually at the tourist office" negation. The dominant features in the circuit are **shallow Layer-0 lexical detectors for function words and punctuation** (" from", " so", ".", " about") that have no entailment-relevant content. These are precisely the kind of spurious shortcuts NLI probes are known to exploit — the contradiction label correlates statistically with the presence of corrective connectives and negation-adjacent tokens, and the probe has learned that association rather than the underlying semantic inconsistency. A robust probe would weight L2:F13586 / F4438 (the "No one" composite) far more heavily than the function-word cluster.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F13586](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) | 17 | Early features encoding 'No one' (negation phrase) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | Early features encoding 'No one' (negation phrase) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F11769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) | 2 | Early features encoding 'No one' (negation phrase) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 17 | Early features encoding 'No one' (negation phrase) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L0:F11351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11351) | 17 | Early features encoding 'No one' (negation phrase) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11351) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 5 | Function-word features driving contradiction (period, ' from', ' so', ' about') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F7321](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) | 25 | Function-word features driving contradiction (period, ' from', ' so', ' about') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | Function-word features driving contradiction (period, ' from', ' so', ' about') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 12 | Function-word features driving contradiction (period, ' from', ' so', ' about') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F306](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) | 7 | Function-word features driving contradiction (period, ' from', ' so', ' about') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) |
| [L0:F7204](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) | 9 | Function-word features driving contradiction (period, ' from', ' so', ' about') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 30 | Function-word features driving contradiction (period, ' from', ' so', ' about') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L1:F8159](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) | 19 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) |
| [L3:F10901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10901) | 19 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10901) |
| [L0:F10904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) | 1 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) |
| [L1:F474](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/474) | 4 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/474) |
| [L1:F6872](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6872) | 14 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6872) |
| [L0:F9924](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9924) | 14 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9924) |
| [L0:F10891](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10891) | 14 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10891) |
| [L0:F8380](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8380) | 14 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8380) |
| [L0:F12851](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12851) | 4 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12851) |
| [L0:F2854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2854) | 19 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2854) |
| [L0:F3507](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3507) | 19 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3507) |
| [L0:F6518](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6518) | 19 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6518) |
| [L0:F12167](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12167) | 19 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12167) |
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 4 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L0:F6495](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6495) | 4 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6495) |
| [L0:F6356](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6356) | 4 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6356) |
| [L2:F8478](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8478) | 5 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8478) |
| [L2:F5495](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5495) | 19 | Content-word features ('tours', 'usually', 'map', 'Pick') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5495) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:8974 de=-0.408 |
| 3 | `get_upstream_features` | Emb:" from"@5 (de=38.75) +7 more |
| 4 | `get_upstream_features` | Emb:" so"@25 (de=40.50) +7 more |
| 5 | `get_upstream_features` | Emb:"Pick"@1 (de=50.00) +7 more |
| 6 | `get_upstream_features` | Emb:"."@15 (de=46.25) +7 more |
| 7 | `get_upstream_features` | Emb:" about"@12 (de=35.00) +7 more |
| 8 | `get_upstream_features` | Emb:" tourist"@7 (de=22.00) +7 more |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F7321@25` | ❌ error | — | — | Trace what drives L0:F7321 at pos 25 (the " so" feature pushing positively). Doe… |
| SA-2 | `L0:F2238@12` | ❌ error | — | — | Trace what drives L0:F2238 at pos 12 (the " about" feature pushing negatively). … |
| SA-3 | `L0:F306@7` | ❌ error | — | — | Trace what drives L0:F306 at pos 7 (the " tourist" feature pushing positively). … |
| SA-4 | `L0:F6051@15` | ❌ error | — | — | Trace L0:F6051 at pos 15 (the "." feature pushing negatively). Is this a sentenc… |
| SA-5 | `L2:F13586@17` | ❌ error | — | — | Trace L2:F13586 at pos 17. What is the token and upstream signal? |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F13586@17, k=6 → Emb:" No"@16 (de=14.00) +5 more |
| 2 | `get_upstream_features` | L2:F11769@2, k=6 → Emb:" up"@2 (de=19.50) +5 more |
| 3 | `get_upstream_features` | L2:F14413@14, k=6 → Emb:" tours"@14 (de=28.38) +5 more |
| 4 | `get_upstream_features` | L3:F10901@19, k=6 → Emb:" usually"@19 (de=23.50) +5 more |
| 5 | `get_upstream_features` | L1:F8159@19, k=6 → Emb:" usually"@19 (de=24.25) +5 more |
| 6 | `get_upstream_features` | L0:F10904@1, k=6 → Emb:"Pick"@1 (de=13.38) +5 more |
| 7 | `get_upstream_features` | L1:F474@4, k=6 → Emb:" map"@4 (de=16.12) +5 more |
| 8 | `get_upstream_features` | L0:F4438@17, k=4 → Emb:" No"@16 (de=29.38) +3 more |
| 9 | `get_upstream_features` | L0:F11351@17, k=4 → Emb:" one"@17 (de=38.50) +3 more |
| 10 | `get_upstream_features` | L1:F6872@14, k=4 → Emb:" tours"@14 (de=20.62) +3 more |
| 11 | `get_upstream_features` | L0:F12851@4, k=4 → Emb:" map"@4 (de=14.19) +3 more |
| 12 | `get_upstream_features` | L0:F2854@19, k=4 → Emb:" usually"@19 (de=19.62) +3 more |
| 13 | `get_upstream_features` | L2:F5495@19, k=4 → Emb:" usually"@19 (de=31.25) +3 more |
| 14 | `get_upstream_features` | L0:F9924@14, k=3 → Emb:" tours"@14 (de=15.19) +2 more |
| 15 | `get_upstream_features` | L0:F10891@14, k=3 → Emb:" tours"@14 (de=18.12) +2 more |
| 16 | `get_upstream_features` | L0:F8380@14, k=3 → Emb:" tours"@14 (de=5.22) +2 more |
| 17 | `get_upstream_features` | L0:F4438@17, k=3 → Emb:" No"@16 (de=29.38) +2 more |
| 18 | `get_upstream_features` | L0:F9653@14, k=3 → Emb:" tours"@14 (de=13.38) +2 more |
| 19 | `get_upstream_features` | L0:F12167@19, k=3 → Emb:" usually"@19 (de=19.25) +2 more |
| 20 | `get_upstream_features` | L0:F3507@19, k=3 → Emb:" usually"@19 (de=15.62) +2 more |
| 21 | `get_upstream_features` | L0:F6518@19, k=3 → Emb:" usually"@19 (de=12.31) +2 more |

### Build

`build_circuit` → 16 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 14,165 | 5,608 | 58,575 | 0 | $0.0145 | — | — |
| **Total** | | **14,165** | **5,608** | **58,575** | **0** | **$0.0145** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 14s