# Circuit Oracle Report
**Date:** 2026-07-28 07:24:33 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven primarily by negation-cue features ("No" at pos 30, "No one" phrase at pos 30-31) routed through a 16-layer deep positional chain, with secondary contributions from the topic word "Conspiracy" and a scattered set of generic lexical position-detectors that don't carry semantic contradiction content.

**Confidence:** 7

**Reasoning:**

The attribution graph's largest direct effects on the probe output are the late-layer features at position 30, where the token " No" appears: L16:F11298 (+0.2402), L15:F13061 (+0.21), and L14:F336 (+0.1963). Tracing each of these upstream reveals they all share the same dominant input — the `Emb: No (pos 30)` token embedding, with direct_effect ≈ 33.75 to L14:F336, 12.0 to L16:F11298, and 12.69 to L15:F13061. This is the textbook signature of a "negation token detector" supernode: the circuit has built a near-exclusive pathway from the literal word "No" up through mid-layer features (L13:F10768, L12:F8719, L6:F15886) and early-layer positional features (L0:F1143 at pos 30, L2:F2771, L3:F3266) to the probe.

A second, related pathway is the "No one…" phrase detector at pos 31 (`phrase_pos31`, L4:F15764 +0.291, L2:F8837, F8142, F13586, L0:F4438), which directly reads `Emb: No (pos 30)` and `Emb: one (pos 31)`. This phrase feature also feeds into the late-layer negation features at pos 30, amplifying the negation signal.

The third path is the "Conspiracy" word detector (`conspiracy_pos`) at pos 1-2: L5:F559 (+0.2695) and L3:F9739 (+0.2002), driven by `Emb: Cons (pos 1)` and `Emb: piracy (pos 2)`. This supernode directly promotes the contradiction score, consistent with the probe having learned that "conspiracy" content correlates with the contradiction label in training data.

The remaining top features are diffuse lexical position detectors: L0:F3635 on "that" (pos 12), L0:F14574 on "your" (pos 18, direct_effect=−0.35, so actually pushing AWAY from the target — these two are inhibiting), L0:F11375 on "is" (pos 7), L2:F16230/F7725 on "chip"/"Card" (pos 11/6), L2:F16028/L1:F13684 on "theorists" (pos 3), and L0:F2115 on "piracy" (pos 2). These have small direct effects (~0.2) and fire on generic function-word tokens; they contribute marginally and are not semantic contradiction features.

**Assessment of the user's concern is partially validated:** the dominant signal driving the probe IS the negation-word "No" plus the "Conspiracy" topic — a lexical/spurious-cue signal rather than a deep semantic understanding of the premise/hypothesis contradiction. The "your" feature even provides the strongest negative push (−0.35). The "No one thinks Mastercard is up to anything nefarious" surface structure is exactly the kind of lexical cue an NLI probe can shortcut on. However, "Conspiracy" and "nefarious" being content-bearing topic words means the circuit isn't *purely* spurious — it mixes negation-lexicon detectors with topic-word detectors, both of which are shallow lexical rather than semantic mechanisms.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 30 | Late-layer negation detector (pos 30 'No' / 'No one') | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 30 | Late-layer negation detector (pos 30 'No' / 'No one') | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 30 | Late-layer negation detector (pos 30 'No' / 'No one') | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L13:F10768](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) | 30 | Mid-layer negation / clause-final features (pos 30) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) |
| [L12:F8719](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) | 30 | Mid-layer negation / clause-final features (pos 30) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) |
| [L6:F15886](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15886) | 30 | Mid-layer negation / clause-final features (pos 30) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15886) |
| [L0:F1143](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) | 30 | Early-layer 'No' / position-30 detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) |
| [L2:F2771](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) | 30 | Early-layer 'No' / position-30 detectors | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) |
| [L3:F3266](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) | 30 | Early-layer 'No' / position-30 detectors | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) |
| [L0:F14862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) | 30 | Early-layer 'No' / position-30 detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) |
| [L0:F10636](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10636) | 30 | Early-layer 'No' / position-30 detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10636) |
| [L4:F15764](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) | 31 | 'No one ...' phrase feature (pos 31 'one') | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 31 | 'No one ...' phrase feature (pos 31 'one') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L2:F8142](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8142) | 31 | 'No one ...' phrase feature (pos 31 'one') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8142) |
| [L2:F13586](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) | 31 | 'No one ...' phrase feature (pos 31 'one') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 31 | 'No one ...' phrase feature (pos 31 'one') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L5:F559](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) | 2 | 'Conspiracy' word feature (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | 'Conspiracy' word feature (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L0:F14625](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) | 1 | 'Conspiracy' word feature (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) |
| [L0:F44](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) | 1 | 'Conspiracy' word feature (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) |
| [L0:F2115](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) | 2 | 'Conspiracy' word feature (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) |
| [L2:F16028](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) | 3 | Structural lexical features (pos 3 'theorists', 7 'is', 12 'that', 18 'your') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | Structural lexical features (pos 3 'theorists', 7 'is', 12 'that', 18 'your') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | Structural lexical features (pos 3 'theorists', 7 'is', 12 'that', 18 'your') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F14574](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) | 18 | Structural lexical features (pos 3 'theorists', 7 'is', 12 'that', 18 'your') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Structural lexical features (pos 3 'theorists', 7 'is', 12 'that', 18 'your') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L0:F351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) | 11 | Structural lexical features (pos 3 'theorists', 7 'is', 12 'that', 18 'your') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) |
| [L1:F13292](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) | 11 | Structural lexical features (pos 3 'theorists', 7 'is', 12 'that', 18 'your') | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) |
| [L2:F7725](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) | 6 | Structural lexical features (pos 3 'theorists', 7 'is', 12 'that', 18 'your') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) |
| [L1:F13684](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) | 3 | Structural lexical features (pos 3 'theorists', 7 'is', 12 'that', 18 'your') | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) |
| [L10:F16373](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/16373) | 7 | Structural lexical features (pos 3 'theorists', 7 'is', 12 'that', 18 'your') | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/16373) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'contradiction' is not one of the top-k next-token can |
| 3 | `get_top_features` | 20 features; top: L0:44 de=-0.527 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F11298@30` | ❌ error | — | — | Trace the path upstream from L16:F11298 at pos 30 — what does this feature encod… |
| SA-2 | `L15:F13061@30` | ❌ error | — | — | Trace the path upstream from L15:F13061 at pos 30 — what does this feature encod… |
| SA-3 | `L4:F15764@31` | ❌ error | — | — | Trace the path upstream from L4:F15764 at pos 31 — what does this feature encode… |
| SA-4 | `L5:F559@2` | ❌ error | — | — | Trace the path upstream from L5:F559 at pos 2 (the "Conspiracy" token position) … |
| SA-5 | `L10:F16373@7` | ❌ error | — | — | Trace the path upstream from L10:F16373 at pos 7 (likely "MasterCard" position) … |
| SA-6 | `L14:F336@30` | ❌ error | — | — | Trace the path upstream from L14:F336 at pos 30 — what does this feature encode? |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F11298@30, k=12 → L15:F13061 (de=14.00) +11 more |
| 2 | `get_upstream_features` | L15:F13061@30, k=12 → L14:F336 (de=13.00) +11 more |
| 3 | `get_upstream_features` | L4:F15764@31, k=12 → Emb:" one"@31 (de=10.75) +11 more |
| 4 | `get_upstream_features` | L5:F559@2, k=12 → Emb:"piracy"@2 (de=6.72) +11 more |
| 5 | `get_upstream_features` | L14:F336@30, k=10 → Emb:" No"@30 (de=33.75) +9 more |
| 6 | `get_upstream_features` | L10:F16373@7, k=10 → Emb:" theorists"@3 (de=1.91) +9 more |
| 7 | `get_upstream_features` | L0:F11375@7, k=10 → Emb:" is"@7 (de=31.38) +9 more |
| 8 | `get_upstream_features` | L0:F3635@12, k=10 → Emb:" that"@12 (de=41.00) +9 more |
| 9 | `get_upstream_features` | L0:F14574@18, k=10 → Emb:" your"@18 (de=45.25) +9 more |
| 10 | `get_upstream_features` | L0:F14625@1, k=10 → Emb:"Cons"@1 (de=17.88) +9 more |
| 11 | `get_upstream_features` | L2:F16230@11, k=10 → Emb:" chip"@11 (de=27.00) +9 more |
| 12 | `get_upstream_features` | L2:F16028@3, k=10 → Emb:" theorists"@3 (de=11.75) +9 more |
| 13 | `get_upstream_features` | L0:F351@11, k=10 → Emb:" chip"@11 (de=19.25) +9 more |
| 14 | `get_upstream_features` | L3:F9739@2, k=10 → Emb:"Cons"@1 (de=8.75) +9 more |
| 15 | `get_upstream_features` | L2:F8142@31, k=10 → Emb:" No"@30 (de=14.62) +9 more |
| 16 | `get_upstream_features` | L2:F7725@6, k=10 → Emb:"Card"@6 (de=25.62) +9 more |
| 17 | `get_upstream_features` | L1:F13292@11, k=10 → Emb:" chip"@11 (de=17.00) +9 more |
| 18 | `get_upstream_features` | L0:F2115@2, k=10 → Emb:"piracy"@2 (de=12.88) +9 more |
| 19 | `get_upstream_features` | L0:F14574@18, k=8 → Emb:" your"@18 (de=45.25) +7 more |
| 20 | `get_upstream_features` | L1:F13684@3, k=8 → Emb:" theorists"@3 (de=10.12) +7 more |
| 21 | `get_upstream_features` | L0:F44@1, k=8 → Emb:"Cons"@1 (de=22.38) +7 more |
| 22 | `get_upstream_features` | L2:F8837@31, k=8 → Emb:" No"@30 (de=19.75) +7 more |
| 23 | `get_upstream_features` | L2:F13586@31, k=8 → Emb:" No"@30 (de=16.00) +7 more |

### Build

`build_circuit` → 17 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 15,964 | 5,619 | 78,046 | 0 | $0.0162 | — | — |
| **Total** | | **15,964** | **5,619** | **78,046** | **0** | **$0.0162** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 18s