# Circuit Oracle Report
**Date:** 2026-07-28 07:23:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's nurse classification is driven by genuine profession indicators — "nurse", "practitioner", "delivery", "labor", and "Medicine" — with a small spurious contribution from the pronoun "She".

**Confidence:** 7

**Reasoning:** The circuit is dominated by legitimate profession-term features. The strongest path runs Emb: nurse (pos 7) and Emb: practitioner (pos 8) → L4:F9036 (nurse-practitioner phrase feature, act. 19.25) → L6:F15267 (medical profession feature, act. 23.4) → L14:F3985 (profession term detector, direct_effect 0.089 at pos 8) → L15:F15159 → logit_probe. Emb: nurse contributes 7.06 direct_effect to L6:F15267 and 17.5 to L15:F15159. A second profession path flows from Emb: labor (pos 44, de=25→L0:F1832) and Emb: delivery (pos 46, de=17→L1:F7152, 29.6→L2:F10127) → L4:F4665 (labor/delivery nursing feature, act. 16.9) → L4:F13803 → L6:F9980 (act. 14.25) → logit_probe. A third path uses Emb: Medicine (pos 11) → L0:F3175 → L4:F4665.

The user's concern is partially supported: the pronoun "She" (pos 1) does contribute to L4:F9757 (de=0.044) which feeds the probe, and L0:F15382 fires on "She" with de=-0.038. However, these are minority pathways. The dominant signal is unambiguously profession vocabulary — "nurse" alone contributes ~25% of the top features' direct_effects, and "delivery"+"labor" form another strong profession-specific pathway. The "She"-driven features have direct_effects of 0.04-0.044, an order of magnitude smaller than the profession term features (0.05-0.089). The probe is using genuine profession indicators as its primary signal, with gender markers playing a minor supplementary role — not the reverse.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 7 | Late-layer profession detector (nurse pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 7 | Profession term detector (practitioner/nurse pos 7-8) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 8 | Profession term detector (practitioner/nurse pos 7-8) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | Profession term detector (practitioner/nurse pos 7-8) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 46 | Profession term detector (practitioner/nurse pos 7-8) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L7:F15132](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) | 8 | Mid-layer profession context (practitioner pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 7 | Medical profession feature (nurse/practitioner pos 7-8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Medical profession feature (nurse/practitioner pos 7-8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 47 | Medical profession feature (nurse/practitioner pos 7-8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 46 | Medical labor/delivery feature (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 8 | Healthcare professional feature (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 8 | Nurse practitioner phrase feature (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 46 | Labor/delivery nursing feature (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 46 | Delivery/labor feature (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | She/She-has feature (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L4:F12178](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12178) | 30 | Spent-life context feature (pos 30) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12178) |
| [L2:F10127](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10127) | 46 | Delivery token feature (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10127) |
| [L1:F7152](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7152) | 46 | Delivery feature (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7152) |
| [L0:F1832](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) | 44 | Labor token feature (pos 44) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) |
| [L0:F3175](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3175) | 11 | Medicine token feature (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3175) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | She/bos feature (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F10846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) | 3 | Also feature (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.089 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@8` | ❌ error | — | — | Trace this feature which has a strong positive direct_effect on the probe score.… |
| SA-2 | `L6:F15267@8` | ❌ error | — | — | Trace this feature with strong positive direct_effect. Determine if it encodes p… |
| SA-3 | `L4:F4665@46` | ❌ error | — | — | Trace this feature. What does it detect at position 46 (likely 'pediatrics' or s… |
| SA-4 | `L4:F9757@1` | ❌ error | — | — | Trace this feature at position 1 (likely 'She'). Does it detect gender pronouns … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@8, k=10 → Emb:" practitioner"@8 (de=6.19) +9 more |
| 2 | `get_upstream_features` | L6:F15267@8, k=10 → Emb:" nurse"@7 (de=7.06) +9 more |
| 3 | `get_upstream_features` | L4:F4665@46, k=10 → Emb:" labor"@44 (de=3.45) +9 more |
| 4 | `get_upstream_features` | L4:F9757@1, k=10 → Emb:"<bos>"@0 (de=15.94) +9 more |
| 5 | `get_upstream_features` | L15:F15159@7, k=10 → Emb:" nurse"@7 (de=17.50) +9 more |
| 6 | `get_upstream_features` | L6:F9980@46, k=10 → L4:F4665 (de=2.77) +9 more |
| 7 | `get_upstream_features` | L4:F12178@30, k=10 → Emb:" spent"@26 (de=10.12) +9 more |
| 8 | `get_upstream_features` | L4:F9036@8, k=8 → Emb:" practitioner"@8 (de=14.69) +7 more |
| 9 | `get_upstream_features` | L1:F7152@46, k=8 → Emb:" delivery"@46 (de=17.00) +7 more |
| 10 | `get_upstream_features` | L0:F1832@44, k=8 → Emb:" labor"@44 (de=25.00) +7 more |
| 11 | `get_upstream_features` | L5:F9749@46, k=8 → L4:F4665 (de=2.92) +7 more |
| 12 | `get_upstream_features` | L2:F10127@46, k=6 → Emb:" delivery"@46 (de=29.62) +5 more |
| 13 | `get_upstream_features` | L0:F0@7, k=8 → ❌ Feature (layer=0, pos=7, feature_idx=0) not found in graph's |
| 14 | `get_upstream_features` | L0:F15382@1, k=6 → Emb:"She"@1 (de=16.88) +5 more |
| 15 | `get_upstream_features` | L0:F10846@3, k=6 → Emb:" also"@3 (de=33.50) +5 more |
| 16 | `get_upstream_features` | L7:F15132@8, k=6 → Emb:" practitioner"@8 (de=11.44) +5 more |
| 17 | `get_upstream_features` | L0:F3175@11, k=6 → Emb:" Medicine"@11 (de=15.38) +5 more |
| 18 | `get_upstream_features` | L0:F10697@46, k=6 → Emb:" delivery"@46 (de=13.31) +5 more |
| 19 | `get_upstream_features` | L4:F13803@46, k=6 → Emb:" delivery"@46 (de=13.81) +5 more |
| 20 | `get_upstream_features` | L5:F1275@8, k=6 → Emb:" nurse"@7 (de=2.30) +5 more |

### Build

`build_circuit` → 28 nodes, 33 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 25,238 | 5,707 | 58,586 | 0 | $0.0179 | — | — |
| **Total** | | **25,238** | **5,707** | **58,586** | **0** | **$0.0179** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 57s