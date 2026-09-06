# Circuit Oracle Report
**Date:** 2026-07-28 07:24:23 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven by content-bearing features about the premise (an "abbey" entity with "steepled" attributes) flowing through late-layer abstract representations, not by negation-word artifacts.

**Confidence:** 7

**Reasoning:**

The circuit traces from the input premise to the probe output via two parallel content paths, with no negation-word features (e.g., "not", "lacks", "is not") appearing anywhere in the top driving features.

**Content paths driving the probe toward "contradiction":**

1. **"abbey" entity path** (pos 10): `Emb: abbey (pos 10)` → L0:F9026 (direct_effect 37.5, activation 27.4) → L0:F11835 → L4:F13244 → L17:F451 (direct_effect 0.12, activation 55.3) → **Probe output**. The L4:F13244 feature at pos 10 has its top upstream as the `abbey` embedding (9.06), confirming it encodes the entity.

2. **"first glimpse of the" phrase path**: `Emb: of (pos 4)` → L0:F2848 (de 35.25) + `Emb: the (pos 5)` → L0:F3820 (de 34.25) → L4:F3833 (de 0.14, activation 14.4) → L6:F5342 (de 0.12) → L8:F8406 → L17:F451 → output.

**What the late-layer feature (L17:F451) encodes:** It sits at pos 1 (after `<bos>`), meaning it reads the premise summary. Its upstream is dominated by mid-layer entity/phrase features rather than negation words — none of its top upstreams (L14:F2510, L13:F8128, L15:F751, L10:F14174, L6:F14585, L11:F11186) trace to `not`/`lacks`/`is not` embeddings in the explored paths.

**"Negation-word" hypothesis check:** The negation words in the second sentence ("not", "lacks", "is not", "you will not") occupy positions 26-34, yet only L0:F7710 at pos 21 (`you`) appears in the top features, and it has a *negative* direct_effect (-0.11) — pushing *against* the probe. No feature at the actual negation-token positions (26-34) appears in the top 20. The strong positive drivers are at premise positions 1-10 describing the *content* of the first sentence.

**Conclusion:** The user's concern is partially supported at the surface — L0 surface features (F2848 "of", F3820 "the", F7710 "you") are function-word/token-level, which could be mistaken for "spurious" features. However, these feed into mid-layer phrase/entity detectors (L4:F3833 "first glimpse of", L4:F13244 "abbey", L6:F5342 phrase) that clearly encode premise content. The dominant late-layer driver (L17:F451) receives its signal from these content-bearing mid-layer features, not from negation tokens. The probe is reading premise content (abbey + descriptive attributes) to detect contradiction, not a "not/lacks" surface pattern.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Late-layer L17 feature (abstract premise representation) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | L8 feature on 'That' (suppresses contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L6:F5342](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) | 4 | L6 feature: 'first glimpse' phrase detector | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 4 | L4 feature: 'first glimpse of' phrase detector | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 3 | L4 feature: 'first glimpse of' phrase detector | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 9 | L4 features: 'steepled' word-form (negative toward probe) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F4605](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) | 10 | L4 features: 'steepled' word-form (negative toward probe) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4605) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 9 | L4 features: 'steepled' word-form (negative toward probe) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L4:F2581](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) | 2 | L4 features: 'steepled' word-form (negative toward probe) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2581) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | L4 features: 'steepled' word-form (negative toward probe) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 10 | L4 feature: 'abbey' entity (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | L0 features: 'of the' function-word bigram | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | L0 features: 'of the' function-word bigram | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 30 | L0 features: 'of the' function-word bigram | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 10 | L0 feature: 'abbey' entity (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F11835](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) | 10 | L0 feature: 'abbey' entity (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11835) |
| [L0:F9854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9854) | 2 | L0 feature: 'abbey' entity (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9854) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 21 | L0 feature: 'you' token (pos 21, negative) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L2:F8046](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) | 1 | L2 feature (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8046) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:8406 de=-0.164 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2848@4` | ❌ error | — | — | Trace the path upstream from L0:F2848 at position 4. What does this feature enco… |
| SA-2 | `L0:F3820@5` | ❌ error | — | — | Trace the path upstream from L0:F3820 at position 5. What does this feature enco… |
| SA-3 | `L4:F3833@4` | ❌ error | — | — | Trace the path upstream from L4:F3833 at position 4. What does this feature enco… |
| SA-4 | `L17:F451@1` | ❌ error | — | — | Trace the path upstream from L17:F451 at position 1. This is a late-layer featur… |
| SA-5 | `L0:F9026@10` | ❌ error | — | — | Trace the path upstream from L0:F9026 at position 10. What does this feature enc… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2848@4, k=10 → Emb:" of"@4 (de=35.25) +9 more |
| 2 | `get_upstream_features` | L0:F3820@5, k=10 → Emb:" the"@5 (de=34.25) +9 more |
| 3 | `get_upstream_features` | L4:F3833@4, k=10 → Emb:" glimpse"@3 (de=7.03) +9 more |
| 4 | `get_upstream_features` | L17:F451@1, k=10 → L16:F10989 (de=-12.31) +9 more |
| 5 | `get_upstream_features` | L0:F9026@10, k=10 → Emb:" abbey"@10 (de=37.50) +9 more |
| 6 | `get_upstream_features` | L8:F8406@1, k=10 → Emb:"<bos>"@0 (de=10.69) +9 more |
| 7 | `get_upstream_features` | L6:F5342@4, k=10 → Emb:" first"@2 (de=12.06) +9 more |
| 8 | `get_upstream_features` | L4:F13244@10, k=10 → Emb:" abbey"@10 (de=9.06) +9 more |
| 9 | `get_upstream_features` | L4:F4605@9, k=10 → Emb:"led"@9 (de=6.44) +9 more |
| 10 | `get_upstream_features` | L0:F7710@21, k=10 → Emb:" you"@21 (de=42.25) +9 more |

### Build

`build_circuit` → 19 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 14,830 | 4,728 | 34,860 | 0 | $0.0122 | — | — |
| **Total** | | **14,830** | **4,728** | **34,860** | **0** | **$0.0122** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 57s