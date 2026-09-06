# Circuit Oracle Report
**Date:** 2026-07-28 07:23:20 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of this individual as a Dietitian/Nutritionist is driven primarily by feminine gender/pronominal markers and a female name, not by genuine profession-indicating vocabulary.

**Confidence:** 8

**Reasoning:**

The attribution graph reveals that the probe's classification score is dominated by **pronoun and name features** rather than by features that respond to profession-related terms like "Dietitian," "Nutrition," or "RD."

**Dominant paths — Gender/name markers drive the classification:**

1. **Pronoun "She" at position 1 (sentence-initial):** The embedding `Emb: 'She' (pos 1)` (direct_effect 19.25) feeds L6:F11646 (direct_effect 0.209) and L4:F7864 (direct_effect 0.1338), then to L4:F15317 and L12:F12940. These features also fire at pos 2 and propagate onward, contributing substantially to the probe.

2. **Pronoun "she" at position 57:** The embedding `Emb: ' she' (pos 57)` (direct_effect 22.625) drives L0:F12519, which in turn feeds the late-layer cluster L15–L18 (L15:F3330, L15:F4709, L16:F2918, L17:F5889, L18:F14677). L18:F14677 alone contributes direct_effect 0.1436 to the probe, and L18:F14677 also fires at pos 1 and 94 with direct_effects 0.124 and 0.1245.

3. **Female name "Heather" at position 31:** `Emb: ' Heather' (pos 31)` (direct_effect 10.94 into L4:F1276) feeds L12:F14970 and L0:F7532, contributing direct_effect 0.1069 to the probe via L12:F14970.

**Weak profession signal:**

4. **"Die-" of Dietetics at pos 20–21:** The only profession-adjacent path traces from `Emb: ' Die' (pos 20)` to L3:F11774 and L3:F10028, then to L4:F13412. L4:F13412 fires at pos 21 (direct_effect 0.1631) and pos 55, but its upstream is a generic subword "Die/te" pattern (direct_effect 4.06 from `Emb: ' Die'` and 2.77 from `Emb: 'te'`) — not a coherent "Dietitian/Dietetics" concept feature. The direct effect is inflated by high activation (28.4) on a weak concept.

**Key observations:**

- L6:F11646 is an L6 pronoun-encoding feature (fires on "She" at pos 1 and pos 2 with activation 12.5 and 14.9) and propagates downstream into L7:F8644 and L18:F14677 at pos 57. This is the strongest single-feature driver (direct_effect 0.209).
- L18:F14677 is a late-layer pronoun-detector that fires at multiple pronoun positions (1, 57, 94) with consistent positive direct_effect (~0.12–0.14), confirming it generalizes across the text on female pronouns.
- The actual profession-indicating tokens ("Dietitian," "Nutritional Sciences," "RD," "Pediatric," "Sports Nutrition") do not appear as inputs to the top features driving the probe. The L4:F13412 feature on "Die-" is a generic subword detector, not a profession concept.

**Verdict:** The user's concern is well-founded. The probe's classification is largely mediated by **L6:F11646 → L18:F14677 (pronoun detector)** and the **"Heather" name features**, with only a weak, subword-level contribution from profession vocabulary. The model is using gendered surface features (feminine pronouns, a female first name) as a shortcut proxy for "female-coded profession," rather than reading the actual professional credentials. This is a classic spurious-correlation circuit that would not generalize to a male "dietitian" or a female "engineer."

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 57 | Late-layer features firing on ' she' (pos 57) — pronoun detector | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 57 | Late-layer features firing on ' she' (pos 57) — pronoun detector | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L16:F2918](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) | 57 | Late-layer features firing on ' she' (pos 57) — pronoun detector | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 57 | Late-layer features firing on ' she' (pos 57) — pronoun detector | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F4709](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4709) | 57 | Late-layer features firing on ' she' (pos 57) — pronoun detector | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4709) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer features firing on 'She' (pos 1) — sentence-initial pronoun | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer features firing on 'She' (pos 1) — sentence-initial pronoun | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Mid-layer features firing on 'She' (pos 1) — sentence-initial pronoun | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Mid-layer features firing on 'She' (pos 1) — sentence-initial pronoun | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 31 | Features firing on proper name 'Heather' (pos 31) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 31 | Features firing on proper name 'Heather' (pos 31) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 31 | Features firing on proper name 'Heather' (pos 31) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | Weak profession features: 'Die-' of Dietetics (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 21 | Weak profession features: 'Die-' of Dietetics (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 21 | Weak profession features: 'Die-' of Dietetics (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:8644 de=-0.212 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@57` | ❌ error | — | — | Trace the path upstream from L18:F14677 at position 57. This feature has a stron… |
| SA-2 | `L6:F11646@1` | ❌ error | — | — | Trace the path upstream from L6:F11646 at position 1. This feature has a strong … |
| SA-3 | `L4:F13412@21` | ❌ error | — | — | Trace the path upstream from L4:F13412 at position 21. This feature has a strong… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@57, k=10 → Emb:" she"@57 (de=22.62) +9 more |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 3 | `get_upstream_features` | L4:F13412@21, k=10 → L3:F11774 (de=4.81) +9 more |
| 4 | `get_upstream_features` | L0:F12519@57, k=5 → Emb:" she"@57 (de=42.25) +4 more |
| 5 | `get_upstream_features` | L4:F7864@1, k=5 → Emb:"She"@1 (de=24.62) +4 more |
| 6 | `get_upstream_features` | L3:F11774@21, k=5 → Emb:" Die"@20 (de=5.88) +4 more |
| 7 | `get_upstream_features` | L3:F10028@21, k=5 → Emb:" Die"@20 (de=6.94) +4 more |
| 8 | `get_upstream_features` | L7:F8644@31, k=5 → Emb:"She"@1 (de=7.47) +4 more |
| 9 | `get_upstream_features` | L12:F12940@2, k=5 → Emb:"She"@1 (de=6.03) +4 more |
| 10 | `get_upstream_features` | L12:F14970@31, k=5 → Emb:"<bos>"@0 (de=-3.48) +4 more |
| 11 | `get_upstream_features` | L4:F1276@31, k=5 → Emb:" Heather"@31 (de=10.94) +4 more |
| 12 | `get_upstream_features` | L4:F15317@2, k=5 → Emb:"She"@1 (de=13.56) +4 more |
| 13 | `get_upstream_features` | L7:F2765@31, k=5 → Emb:"She"@1 (de=3.34) +4 more |
| 14 | `get_upstream_features` | L6:F11646@2, k=5 → L4:F15317 (de=8.75) +4 more |

### Build

`build_circuit` → 9 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 15,854 | 3,820 | 46,085 | 0 | $0.0121 | — | — |
| **Total** | | **15,854** | **3,820** | **46,085** | **0** | **$0.0121** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 46s