# Circuit Oracle Report
**Date:** 2026-07-28 07:24:10 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven almost entirely by the embedding of the negation word " not" at position 21, which propagates through a dedicated chain of pos-21 features in layers 0–4 (notably L0:4958 with direct_effect=33.75 from " not", then L2:12021, L3:8011, L3:1101, L4:4492) up to late-layer features L16:12358 and L15:2080 that feed the probe — confirming the user's suspicion of a negation-token shortcut.

**Confidence:** 9

**Reasoning:** The circuit overwhelmingly routes through the token " not" (pos 21). Its raw embedding has direct_effect 19 onto L16:12358, 19.125 onto L4:4492, 21.75 onto L3:8011, 13.6875 onto L3:1101, 23.125 onto L2:12021, and 33.75 onto L0:4958 — the single largest upstream edge in the entire graph. A column of pos-21 negation-sensitive features (L0:4958, L0:9646, L0:15454, L0:7257, L1:5108, L1:14233, L2:12021, L3:8011, L3:1101, L4:4492, L4:2422) propagates this signal up, peaking at L16:12358 (direct_effect=0.3359 to the probe) and L15:2080. By contrast, semantic content tokens like " fire" (L2:4819, direct_effect=0.2617), " they" (L0:3498, direct_effect=−0.7852), " about" (L0:2238), " to" (L0:8444), and " the" (L0:3820) contribute mixed-sign, smaller-magnitude effects and are not organized into a coherent semantic path — they look like background noise rather than a structured "what was done vs. what was forbidden" comparison. There is no feature representing the contrast between the premise action ("setting fire to massive tracts of forest") and the negation clause ("not allowed to deforest for agricultural purposes"); instead, the detector simply fires on the presence of the negation word "not" and propagates that single lexical cue to the probe. This is a textbook spurious correlation: the contradiction probe has learned to key on the negation marker rather than on the semantic incompatibility between the two sentences, and the user concern is well-supported.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 21 | L15-16: late-layer pos-21 features (L15:2080, L16:12358) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 3 | L15-16: late-layer pos-21 features (L15:2080, L16:12358) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 11 | L15-16: late-layer pos-21 features (L15:2080, L16:12358) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 21 | L2-4: mid-layer pos-21 negation features (L2:12021, L3:8011, L3:1101, L4:4492, L4:2422) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 21 | L2-4: mid-layer pos-21 negation features (L2:12021, L3:8011, L3:1101, L4:4492, L4:2422) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 21 | L2-4: mid-layer pos-21 negation features (L2:12021, L3:8011, L3:1101, L4:4492, L4:2422) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 21 | L2-4: mid-layer pos-21 negation features (L2:12021, L3:8011, L3:1101, L4:4492, L4:2422) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 21 | L2-4: mid-layer pos-21 negation features (L2:12021, L3:8011, L3:1101, L4:4492, L4:2422) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 21 | L0-1: low-level features for 'not' (L0:4958, L0:9646, L0:15454, L0:7257, L1:5108, L1:14233) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F9646](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9646) | 21 | L0-1: low-level features for 'not' (L0:4958, L0:9646, L0:15454, L0:7257, L1:5108, L1:14233) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9646) |
| [L0:F15454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) | 21 | L0-1: low-level features for 'not' (L0:4958, L0:9646, L0:15454, L0:7257, L1:5108, L1:14233) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) |
| [L0:F7257](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7257) | 21 | L0-1: low-level features for 'not' (L0:4958, L0:9646, L0:15454, L0:7257, L1:5108, L1:14233) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7257) |
| [L1:F5108](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) | 21 | L0-1: low-level features for 'not' (L0:4958, L0:9646, L0:15454, L0:7257, L1:5108, L1:14233) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 21 | L0-1: low-level features for 'not' (L0:4958, L0:9646, L0:15454, L0:7257, L1:5108, L1:14233) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | Other content features (L0:3498 'they', L0:3820 'the', L0:2238 'about', L0:8444 'to', L2:4819 'fire', L2:2952) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 6 | Other content features (L0:3498 'they', L0:3820 'the', L0:2238 'about', L0:8444 'to', L2:4819 'fire', L2:2952) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | Other content features (L0:3498 'they', L0:3820 'the', L0:2238 'about', L0:8444 'to', L2:4819 'fire', L2:2952) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 13 | Other content features (L0:3498 'they', L0:3820 'the', L0:2238 'about', L0:8444 'to', L2:4819 'fire', L2:2952) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | Other content features (L0:3498 'they', L0:3820 'the', L0:2238 'about', L0:8444 'to', L2:4819 'fire', L2:2952) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L2:F2952](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) | 4 | Other content features (L0:3498 'they', L0:3820 'the', L0:2238 'about', L0:8444 'to', L2:4819 'fire', L2:2952) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3498 de=-0.785 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@21` | ❌ error | — | — | Trace this feature upstream. It's a late-layer feature at position 21 (likely th… |
| SA-2 | `L4:F4492@21` | ❌ error | — | — | Trace this mid-layer feature at position 21 upstream. What input tokens drive it… |
| SA-3 | `L0:F3498@2` | ❌ error | — | — | Trace this early-layer feature at position 2 upstream. Position 2 is the word "t… |
| SA-4 | `L2:F4819@12` | ❌ error | — | — | Trace this feature at position 12 upstream. Position 12 is likely in the second … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F12358@21, k=10 → Emb:" not"@21 (de=19.00) +9 more |
| 2 | `get_upstream_features` | L4:F4492@21, k=10 → Emb:" not"@21 (de=19.12) +9 more |
| 3 | `get_upstream_features` | L2:F4819@12, k=10 → Emb:" fire"@12 (de=32.00) +9 more |
| 4 | `get_upstream_features` | L0:F3498@2, k=10 → Emb:" they"@2 (de=42.75) +9 more |
| 5 | `get_upstream_features` | L3:F8011@21, k=10 → Emb:" not"@21 (de=21.75) +9 more |
| 6 | `get_upstream_features` | L3:F1101@21, k=10 → Emb:" not"@21 (de=13.69) +9 more |
| 7 | `get_upstream_features` | L0:F3820@6, k=8 → Emb:" the"@6 (de=34.25) +7 more |
| 8 | `get_upstream_features` | L0:F8444@13, k=8 → Emb:" to"@13 (de=41.00) +7 more |
| 9 | `get_upstream_features` | L0:F2238@4, k=8 → Emb:" about"@4 (de=35.00) +7 more |
| 10 | `get_upstream_features` | L15:F2080@3, k=8 → Emb:" set"@3 (de=44.50) +7 more |
| 11 | `get_upstream_features` | L2:F12021@21, k=8 → Emb:" not"@21 (de=23.12) +7 more |
| 12 | `get_upstream_features` | L0:F4958@21, k=8 → Emb:" not"@21 (de=33.75) +7 more |
| 13 | `get_upstream_features` | L2:F2952@4, k=8 → Emb:" set"@3 (de=13.50) +7 more |

### Build

`build_circuit` → 11 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 15,037 | 3,801 | 42,740 | 0 | $0.0116 | — | — |
| **Total** | | **15,037** | **3,801** | **42,740** | **0** | **$0.0116** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 45s