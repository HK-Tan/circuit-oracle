# Circuit Oracle Report
**Date:** 2026-07-28 08:39:08 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a circuit that detects nutrition and cooking-related terminology, originating directly from the input tokens " nutrition" and " cook".

**Confidence:** 10/10

**Reasoning:**
The attribution circuit demonstrates that the probe relies on genuine profession-related indicators rather than spurious gender markers. The signal flows from two primary input sources:
1.  **Nutrition Path:** The embedding for " nutrition" (pos 13) feeds into a hierarchy of features:
    *   **Low-layer terms:** Features like L3:F6246 (nutrients/nutrition) and L4:F13412 (dietary health) detect the specific vocabulary.
    *   **Mid-layer context:** L6:F11327 (food/nutrition phrases) aggregates these signals.
    *   **High-layer semantics:** This further feeds into L14:F4197 (food insecurity/meals) and L19:F1589 (scientific nutritional studies), which provide the high-level semantic context that drives the probe's score.
2.  **Cooking Path:** The embedding for " cook" (pos 17) drives L4:F14942 (cooking/kitchens) and L15:F2510 (food preparation), which directly contribute to the final classification score.

No gender-related features or embeddings (e.g., "She", "her") were found in the positive attribution paths. The mechanism is purely based on the semantic detection of nutrition and culinary expertise.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L3:F6246](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) | 13 | Nutrition Terms (L3-4) | the word "Nutrients" and words containing "ure". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Nutrition Terms (L3-4) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Nutrition Terms (L3-4) | words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Food/Nutrition Context (L6) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 13 | Advanced Nutrition/Scientific Context (L14-19) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 13 | Advanced Nutrition/Scientific Context (L14-19) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L4:F14942](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14942) | 17 | Cooking/Kitchen Context (L4-15) | mentions of cooking, kitchens, chefs, and associated locations. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14942) |
| [L15:F2510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) | 17 | Cooking/Kitchen Context (L4-15) |  words and phrases related to food preparation and consumption, along with some words relating to the digestive system and eating disorders | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 3 | `get_top_features` | 10 features; top: L6:11327 de=0.141 |
| 4 | `inspect_feature` ×5 | L6:11327, L14:4197, L4:13412, L19:1589, L15:2510 |
| 5 | `get_top_logits` | "" (100%) |
| 6 | `get_top_features` | 15 features; top: L6:11327 de=0.141 |
| 7 | `inspect_feature` ×5 | L6:11327, L14:4197, L4:13412, L19:1589, L15:2510 |
| 8 | `get_top_logits` | "" (100%) |
| 9 | `get_top_features` | 10 features; top: L6:11327 de=0.141 |
| 10 | `inspect_feature` ×5 | L6:11327, L14:4197, L4:13412, L19:1589, L15:2510 |
| 11 | `get_top_logits` | "" (100%) |
| 12 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 13 | `get_top_features` | 10 features; top: L6:11327 de=0.141 |

### Dispatch: 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11327@13` | ✅ reported | 8 | 21 | Trace the path from L6:F11327, L14:F4197, L4:F13412, L19:F1589, and L15:F2510 to… |

<details>
<summary><b>SA-1</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 5 | `get_upstream_features` | L14:F4197@13, k=10 | Emb:" nutrition"@13 (de=14.31) +9 more |
| 6 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 7 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 8 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 9 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 10 | `get_upstream_features` | L19:F1589@13, k=10 | Emb:" nutrition"@13 (de=31.25) +9 more |
| 11 | `inspect_feature` | L15, F2510 | " words and phrases related to food preparation and consumption, along " |
| 12 | `get_upstream_features` | L15:F2510@13, k=10 | ❌ Feature (layer=15, feature_idx=2510) not found at pos=13. Th |
| 13 | `get_upstream_features` | L15:F2510@17, k=10 | Emb:" cook"@17 (de=28.88) +9 more |
| 14 | `inspect_feature` | L4, F14942 | "mentions of cooking, kitchens, chefs, and associated locations." |
| 15 | `get_upstream_features` | L4:F14942@17, k=10 | Emb:" cook"@17 (de=22.50) +9 more |

**Findings:** All traced paths from the target features converge on nutrition‑related token embeddings (" nutrition" or "cook"). The strongest positive upstream drivers are low‑layer embeddings (layer ≤ 8) feeding into mid‑layer features that specialize on food, diet, and food‑insecurity language. No gender‑related tokens appear in any positive‑effect upstream chain; the signal originates exclusively from nutri…

</details>

### Build

`build_circuit` → 7 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 478,000 | 1,496 | 67,584 | 0 | $0.0685 | — | — |
| SA-1 | openai/gpt-oss-120b | 254,796 | 15,927 | 24,448 | 0 | $0.0481 | ✅ 8F/21E | Trace the path from L6:F11327, L14:F4197, L4:F13412, L19:F15… |
| **Total** | | **732,796** | **17,423** | **92,032** | **0** | **$0.1166** | | |

**Oracle wall-clock time:** 8m 24s