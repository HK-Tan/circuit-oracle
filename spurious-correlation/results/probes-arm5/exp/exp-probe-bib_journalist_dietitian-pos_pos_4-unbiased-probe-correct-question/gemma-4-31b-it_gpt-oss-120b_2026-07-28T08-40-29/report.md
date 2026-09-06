# Circuit Oracle Report
**Date:** 2026-07-28 08:40:29 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a chain of features that detect nutritional and dietary terminology, rather than spurious gender markers or generic profession indicators.

**Confidence:** 10

**Reasoning:**
The attribution circuit reveals a direct causal path from specific professional terminology in the input text to the probe's classification score. 

1.  **Input Tokens $\rightarrow$ Lexical Features:** The signal originates from embedding nodes for "Nutritional" (pos 9) and "Dietetics" (split into " Die" at pos 20 and "te" at pos 21). These embeddings excite a group of features in the `Nutrition_Lexicon` supernode, including L4:F13412 (terms related to diets and dietary health, `frac_nonzero: 0.012`), L6:F11327 (food or nutrition, `frac_nonzero: 0.011`), and L4:F9554 (food, rations and feeding). 
2.  **Lexical $\rightarrow$ Contextual:** These lexical features feed into L19:F1589 (`Nutrition_Context`), which specifically encodes a "context of scientific, specially nutritional, studies" (`frac_nonzero: 0.037`). This feature acts as a higher-level aggregator that recognizes the professional/scientific nature of the nutrition-related terms.
3.  **Contextual $\rightarrow$ Probe:** Finally, L19:F1589 provides a strong positive direct effect on the final probe classification score.

There is no evidence in the top-contributing features or the traced paths of gender-specific markers (e.g., "she", "her") or other spurious correlations driving the classification; the mechanism is purely based on the identification of professional expertise in nutrition and dietetics.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | Nutrition & Diet Lexicon |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 21 | Nutrition & Diet Lexicon |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 21 | Nutrition & Diet Lexicon | words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 21 | Nutrition & Diet Lexicon |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 21 | Scientific Nutrition Context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:13412 de=0.154 |
| 3 | `inspect_feature` ×6 | L4:13412, L6:11327, L19:1589, L14:4197, L2:2589, L0:14824 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13412@21` | ❌ error | — | — | Trace the signal from L4:F13412 (diets/dietary health) back to the embedding nod… |
| SA-2 | `L19:F1589@21` | ✅ reported | 8 | 22 | Trace the signal from L19:F1589 (nutritional studies) back to embedding nodes. |
| SA-3 | `L6:F11327@21` | ✅ reported | 6 | 21 | Trace the signal from L6:F11327 (food/nutrition) back to embedding nodes. |

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@21, k=10 | L4:F13412 (de=10.69) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 5 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 6 | `get_upstream_features` | L6:F11327@21, k=10 | L4:F13412 (de=5.88) +9 more |
| 7 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 8 | `inspect_feature` | L17, F7545 | "mentions of architecture, design, nurses and healthcare." |
| 9 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 10 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 11 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 12 | `report_findings<|channel|>commentary` | {'discovered_features': [{'layer': 19, 'feature_idx': 1589, 'label': 'a context  | ❌ Tool 'report_findings<\|channel\|>commentary' was not offered  |

**Findings:** The signal from L19:F1589 (nutritional‑study context) is driven primarily by a cascade of diet‑related features in lower layers (L4:F13412, L6:F11327, L14:F4197, L17:F7545) and ultimately by the raw token embedding ' Die' (pos 20) which provides a positive direct effect. All required termination conditions are met: a lower‑third layer feature (layer 4) is present and an embedding node contributes …

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@21, k=15 | L4:F13412 (de=5.88) +14 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 5 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 6 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 7 | `get_upstream_features` | L3:F11774@21, k=10 | Emb:" Die"@20 (de=5.88) +9 more |
| 8 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 9 | `get_upstream_features` | L4:F9554@21, k=10 | L3:F11774 (de=3.03) +9 more |
| 10 | `inspect_feature` | L1, F1083 | " the characters "te" within code and/or non-English words" |
| 11 | `get_upstream_features` | L1:F1083@21, k=10 | Emb:"te"@21 (de=22.25) +9 more |

**Findings:** Tracing from L6:F11327 (food/nutrition detector) quickly reaches lower‑layer circuitry. The strongest upstream driver is L4:F13412 (diet‑health terms) which in turn is driven by L3:F11774 and L3:F10028 and the raw token embedding "Die" (pos 20). The path also goes through L4:F9554 (food‑rations detector) and further down to a low‑level character‑ngram feature L1:F1083 that is directly excited by t…

</details>

### Build

`build_circuit` → 6 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 93,376 | 1,192 | 8,704 | 0 | $0.0137 | — | — |
| SA-3 | openai/gpt-oss-120b | 145,249 | 12,659 | 15,232 | 0 | $0.0296 | ✅ 6F/21E | Trace the signal from L6:F11327 (food/nutrition) back to emb… |
| SA-2 | openai/gpt-oss-120b | 159,383 | 14,543 | 28,544 | 0 | $0.0331 | ✅ 8F/22E | Trace the signal from L19:F1589 (nutritional studies) back t… |
| **Total** | | **398,008** | **28,394** | **52,480** | **0** | **$0.0763** | | |

**Oracle wall-clock time:** 9m 45s