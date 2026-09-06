# Circuit Oracle Report
**Date:** 2026-07-28 08:39:28 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classification score is driven by a combination of gender-specific markers and nutrition-related concepts, with female gender indicators providing the strongest causal push.

**Confidence:** 9/10

**Reasoning:**
The attribution circuit reveals two primary parallel paths driving the probe's score: a dominant **Gender Pathway** and a secondary **Nutrition Pathway**.

1.  **Gender Pathway (Strongest Driver):** The signal originates from the input token "She" (`Emb: She (pos 0)`). This signal flows through a hierarchy of female-specific detectors:
    *   **Low-layer:** `L4:F7864` acts as an initial bridge.
    *   **Mid-layer:** `L6:F11646` and `L12:F12940` explicitly detect female pronouns ("she", "her").
    *   **High-layer:** `L18:F14677` integrates these signals into a general "woman/girl" entity representation.
    This pathway has a very high direct effect on the `Probe_Score`, indicating that the probe relies heavily on the subject's gender as a proxy for the classification.

2.  **Nutrition Pathway (Contextual Driver):** The signal originates from the token "nutrition" (`Emb: nutrition (pos 13)`). It flows through:
    *   **Low-layer:** Nutrient-specific detectors `L0:F5201` and `L3:F6246`.
    *   **Mid-layer:** Concept features `L4:F13412`, `L4:F9554`, and `L6:F11327` which encode "dietary health" and "food/nutrition".
    While this path provides positive evidence, its direct effect on the final score is lower than that of the gender markers.

**Conclusion on Spuriousness:** The user's concern is validated. While the model does detect profession-relevant keywords (nutrition, diet), the strongest causal drivers of the probe's classification are the female gender markers (`L18:F14677`, `L12:F12940`, `L6:F11646`). This suggests the probe is using gender as a spurious feature to predict the profession.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Low-layer Gender Bridge (L4:F7864) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer Female Pronoun Detectors (L6, L12) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer Female Pronoun Detectors (L6, L12) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-layer Female Pronoun Detectors (L6, L12) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | High-layer Female Entity Detectors (L18:F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 23 | High-layer Female Entity Detectors (L18:F14677) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L3:F6246](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) | 13 | Low-layer Nutrient Detectors (L0, L3) | the word "Nutrients" and words containing "ure". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) |
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 13 | Low-layer Nutrient Detectors (L0, L3) | the word "nutrition" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Mid-layer Nutrition/Food Concept (L4, L6) | terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Mid-layer Nutrition/Food Concept (L4, L6) | words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Mid-layer Nutrition/Food Concept (L4, L6) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 3 | `get_top_features` | 15 features; top: L6:11646 de=0.357 |
| 4 | `inspect_feature` ×5 | L6:11646, L12:12940, L18:14677, L4:15317, L4:7864 |
| 5 | `get_top_logits` | "" (100%) |
| 6 | `get_top_features` | 15 features; top: L6:11646 de=0.357 |
| 7 | `inspect_feature` ×7 | L6:11646, L12:12940, L18:14677, L4:15317, L4:7864, L10:14965, L6:11327 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11327@11` | ✅ reported | 5 | 5 | Trace the signal originating from 'nutrition', 'healthy', 'cook' and 'meals' to … |
| SA-2 | `L18:F14677@0` | ✅ reported | 5 | 10 | Trace the signal from 'She' and 'her' to see how they feed into the gender-relat… |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@11, k=15 | ❌ Feature (layer=6, feature_idx=11327) not found at pos=11. Th |
| 3 | `get_upstream_features` | L6:F11327@13, k=15 | Emb:" nutrition"@13 (de=21.00) +14 more |
| 4 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 5 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 6 | `inspect_feature` | L1, F6895 | " the word "visit" and related forms" |
| 7 | `get_upstream_features` | L4:F13412@13, k=15 | Emb:" nutrition"@13 (de=14.06) +14 more |
| 8 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 9 | `get_upstream_features` | L3:F6246@13, k=15 | Emb:" nutrition"@13 (de=12.25) +14 more |
| 10 | `get_upstream_features` | L4:F9554@13, k=10 | Emb:" nutrition"@13 (de=15.88) +9 more |
| 11 | `inspect_feature` | L0, F5201 | " the word "nutrition"" |
| 12 | `get_upstream_features` | L6:F11327@11, k=15 | ❌ Feature (layer=6, feature_idx=11327) not found at pos=11. Th |
| 13 | `inspect_feature` | L0, F7843 | " words related to nutrition and malnutrition" |

**Findings:** The trace shows that the token embedding for the word "nutrition" (position 13) provides a strong positive direct effect (21.0) directly to the target food‑concept feature L6:F11327. In addition, the same embedding excites two intermediate mid‑layer features (L4:F13412 and L4:F9554), which themselves feed positive signal into L6:F11327. Both intermediate features are themselves driven by a lower‑l…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@0, k=10 | ❌ Feature (layer=18, feature_idx=14677) not found at pos=0. Th |
| 3 | `get_upstream_features` | L18:F14677@1, k=10 | Emb:"She"@1 (de=27.12) +9 more |
| 4 | `get_upstream_features` | L18:F14677@2, k=10 | Emb:"She"@1 (de=10.56) +9 more |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 7 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 8 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 9 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 10 | `get_upstream_features<|channel|>commentary` | {'feature_idx': 12940, 'layer': 12, 'pos': 2, 'k': 10} | ❌ Tool 'get_upstream_features<\|channel\|>commentary' was not of |
| 11 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |

**Findings:** The pronoun token 'She' first excites low‑layer bridge feature L4:F7864, which forwards the signal to the core gender detector L6:F11646 (layer ≤8). Both lower‑layer nodes drive the higher‑layer gender feature L18:F14677, establishing a clear path from the input token embedding to the final gender‑related representation.

</details>

### Build

`build_circuit` → 8 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 230,472 | 1,740 | 6 | 0 | $0.0330 | — | — |
| SA-2 | openai/gpt-oss-120b | 117,235 | 8,451 | 22,752 | 0 | $0.0230 | ✅ 5F/10E | Trace the signal from 'She' and 'her' to see how they feed i… |
| SA-1 | openai/gpt-oss-120b | 154,724 | 10,423 | 35,392 | 0 | $0.0300 | ✅ 5F/5E | Trace the signal originating from 'nutrition', 'healthy', 'c… |
| **Total** | | **502,431** | **20,614** | **58,150** | **0** | **$0.0860** | | |

**Oracle wall-clock time:** 8m 46s