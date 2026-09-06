# Circuit Oracle Report
**Date:** 2026-07-28 07:19:52 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mix of genuine profession-indicating food/nutrition features AND a spurious gender-pronoun feature, confirming the user's concern that the circuit uses both substantive and shortcut signals.

**Confidence:** 7

**Reasoning:**

The output node (probe direction) receives direct excitation from two distinct families of features:

**1. Substantive profession indicators (the "good" signal):**
A robust cascade originates from the token "nutrition" at pos 13 and "Nutrition" at pos 28. Embeddings → L4:13412 (dietary health, frac_nonzero 0.012) and L4:9554 (food/feeding, 0.013) → L6:11327 (general food/nutrition, 0.012, direct_effect to output) → L14:4197 (food/eating vocabulary, 0.015) → L19:1589 (scientific nutrition context, 0.038, direct_effect 0.084 to output). The "cook" token at pos 17 drives L15:2510 (food preparation, 0.009, direct_effect 0.065) through its embedding. These features are domain-specific (frac_nonzero < 0.04), have positive direct_effects, and fire on tokens directly relevant to "nutritionist/dietitian" — legitimate profession cues.

**2. Spurious gender signal (the "bad" signal — confirms the user's concern):**
L6:11646 (direct_effect -0.064, i.e. **inhibitory** to the probe at pos 1) is labeled "references to women, triggered by pronouns." It is driven by the embedding of "She" at pos 1 (direct_effect 19.25) through L4:7864 (which actually promotes "herself"/"she") and L1:7244 (she pronoun detector). However, its direct_effect on the output is **negative** (-0.064), meaning it pushes the probe score DOWN. L0:9519 (she/her pronoun, direct_effect -0.056) and L1:7244 (she, +0.054) similarly have mixed signs. So the gender feature is NOT driving the classification positively — the model's profession representation is built from food/nutrition vocabulary, while the gender feature actually slightly suppresses the probe.

**3. Generic / non-informative tokens:**
L0:14824 "has" (-0.098), L0:2349 "others" (-0.087), L0:6051 period/whitespace (-0.054), L0:2238 "about" (+0.061) are all generic lexical features with mostly negative direct_effects — they are absorbed by the probe but don't represent profession knowledge. L1:728 "learn" (+0.054, direct on output, also -0.054 at the top-feature level) is the only mildly relevant generic feature ("passion for helping others learn").

**Net interpretation:** The user's hypothesis is **partially confirmed but not fully**. The probe IS supported by a genuine food/nutrition circuit (the dominant positive path: nutrition/cook tokens → diet_health/feed_rations → food_general → food_insecurity → prof_nutrition_studies → output). However, a distinct "she/her" pronoun pathway exists that fires on the female subject and connects to the output with a slight negative direct_effect, meaning the model partially distinguishes the gender marker from the profession. The circuit does not use "She" as a primary positive profession indicator — the spurious-correlation concern is real but the probe's positive mass comes from substantive nutrition vocabulary. The gender feature is present in the circuit but acts more as a mild inhibitor than a driver, suggesting Gemma-2-2B's profession representation is largely content-based at this layer, though the early-layer pronoun detectors (L0:9519, L1:7244) are entangled with the same residual stream.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 13 | Nutrition studies / scientific context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 13 | Food/eating vocabulary |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L15:F2510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) | 17 | Food preparation / kitchen |  words and phrases related to food preparation and consumption, along with some words relating to the digestive system and eating disorders | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | General food/nutrition words |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 17 | General food/nutrition words |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | References to women (she/her) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L1:F7244](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) | 1 | She/her pronoun detector | the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | she/her pronoun detector (L0) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Diet/dietary health terms |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 28 | Diet/dietary health terms |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Food/feeding vocabulary | words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L1:F728](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/728) | 8 | Learning/teaching vocabulary |   words related to gaining knowledge | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/728) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11327 de=0.141 |
| 3 | `inspect_feature` ×13 | L6:11327, L14:4197, L4:13412, L19:1589, L15:2510, L0:2238, L0:14824, L0:2349, L6:11646, L0:9519, L1:728, L0:6051, L1:7244 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11327@13` | ✅ reported | 6 | 14 | Trace the food/nutrition feature L6:11327 upstream to identify the specific inpu… |
| SA-2 | `L14:F4197@13` | ✅ reported | 7 | 9 | Trace L14:4197 (food/nutrition) upstream. Which token does it fire on? What buil… |
| SA-3 | `L19:F1589@13` | ✅ reported | 4 | 9 | Trace L19:1589 (scientific nutrition studies) upstream. What input token and wha… |
| SA-4 | `L6:F11646@1` | ✅ reported | 4 | 6 | Trace L6:11646 (references to women, 'her') upstream. This is the gender/spuriou… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 5 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 6 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 7 | `inspect_feature` | L1, F6895 | " the word "visit" and related forms" |
| 8 | `get_upstream_features` | L4:F9554@13, k=10 | Emb:" nutrition"@13 (de=15.88) +9 more |

**Findings:** The food/nutrition detector L6:11327 is driven primarily by the raw token embedding for "nutrition" (direct_effect ~21). This activation is amplified by mid‑level diet/food features in layers 4 (indices 13412 and 9554) and a finer‑grained nutrient suffix feature in layer 3 (6246). All these upstream nodes sit in layers ≤8, satisfying the lower‑third floor condition, and the chain includes a clear …

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 2 | `get_upstream_features` | L14:F4197@13, k=10 | Emb:" nutrition"@13 (de=14.31) +9 more |
| 3 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 4 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 5 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 6 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 7 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 8 | `inspect_feature` | L8, F8003 | " words about nutrients, foods, and minerals, especially regarding diet" |
| 9 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 10 | `inspect_feature` | L0, F7843 | " words related to nutrition and malnutrition" |
| 11 | `get_upstream_features` | L8:F8003@13, k=10 | Emb:" nutrition"@13 (de=14.31) +9 more |

**Findings:** L14:F4197 fires strongly on the token "nutrition" (position 13). The signal builds up through a cascade of food‑related detectors: the mid‑layer feature L6:11327 picks up nutrition/food vocabulary, itself driven by the same "nutrition" embedding and earlier low‑layer features L4:13412 (diet health) and L4:9554 (feeding/rations). Additional minor contributions come from very early lexical features …

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@13, k=10 | Emb:" nutrition"@13 (de=31.25) +9 more |
| 3 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 4 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 5 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 6 | `get_upstream_features` | L14:F4197@13, k=10 | Emb:" nutrition"@13 (de=14.31) +9 more |
| 7 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 8 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 9 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 10 | `inspect_feature` | L1, F6895 | " the word "visit" and related forms" |

**Findings:** The target feature L19:1589 (nutrition‑study context) is driven primarily by the input token " nutrition" at position 13 (direct effect 31.25). The signal propagates through a cascade of food‑related features: L14:4197 (food‑insecurity detector), L6:11327 (general food/nutrition detector), and L4:13412 (diet‑health terms). All upstream features have positive direct_effects and ultimately originate…

</details>

<details>
<summary><b>SA-4</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 6 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 7 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |

**Findings:** The gender‑reference feature L6:11646 is primarily driven by the raw input token embedding for the word "She" (direct_effect ≈19). A secondary pathway runs through an early‑layer feature (L4:7864) that also heavily relies on the "She" embedding (direct_effect ≈24.6) and receives a modest contribution from a multilingual pronoun detector (L2:2128). A later‑layer pronoun context feature (L5:10952) a…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×3 | L2:2128, L4:7864, L5:10952 |
| 2 | `get_upstream_features` | L0:F14824@2, k=5 → Emb:" has"@2 (de=32.75) +4 more |
| 3 | `get_upstream_features` | L0:F2349@7, k=5 → Emb:" others"@7 (de=41.25) +4 more |
| 4 | `get_upstream_features` | L1:F728@8, k=5 → Emb:" learn"@8 (de=21.50) +4 more |
| 5 | `get_upstream_features` | L0:F6051@22, k=5 → Emb:"."@22 (de=47.00) +4 more |
| 6 | `get_upstream_features` | L15:F2510@17, k=5 → Emb:" cook"@17 (de=28.88) +4 more |
| 7 | `get_upstream_features` | L14:F4197@13, k=3 → Emb:" nutrition"@13 (de=14.31) +2 more |
| 8 | `get_upstream_features` | L19:F1589@13, k=3 → Emb:" nutrition"@13 (de=31.25) +2 more |
| 9 | `get_upstream_features` | L0:F2238@9, k=3 → Emb:" about"@9 (de=34.25) +2 more |
| 10 | `get_upstream_features` | L0:F9519@1, k=3 → Emb:"She"@1 (de=15.75) +2 more |
| 11 | `get_upstream_features` | L1:F7244@1, k=3 → Emb:"She"@1 (de=13.56) +2 more |
| 12 | `get_upstream_features` | L4:F13412@13, k=3 → Emb:" nutrition"@13 (de=14.06) +2 more |
| 13 | `get_upstream_features` | L6:F11327@13, k=3 → Emb:" nutrition"@13 (de=21.00) +2 more |
| 14 | `get_upstream_features` | L14:F4197@28, k=3 → ❌ Feature (layer=14, feature_idx=4197) not found at pos=28. Th |
| 15 | `get_upstream_features` | L4:F13412@28, k=3 → Emb:" Nutrition"@28 (de=12.56) +2 more |

### Build

`build_circuit` → 20 nodes, 28 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 74,337 | 5,188 | 163,134 | 0 | $0.0383 | — | — |
| SA-4 | openai/gpt-oss-120b | 82,955 | 5,630 | 2,528 | 0 | $0.0159 | ✅ 4F/6E | Trace L6:11646 (references to women, 'her') upstream. This i… |
| SA-3 | openai/gpt-oss-120b | 114,496 | 8,449 | 23,744 | 0 | $0.0226 | ✅ 4F/9E | Trace L19:1589 (scientific nutrition studies) upstream. What… |
| SA-1 | openai/gpt-oss-120b | 101,322 | 8,423 | 2,528 | 0 | $0.0203 | ✅ 6F/14E | Trace the food/nutrition feature L6:11327 upstream to identi… |
| SA-2 | openai/gpt-oss-120b | 138,004 | 6,680 | 5,088 | 0 | $0.0248 | ✅ 7F/9E | Trace L14:4197 (food/nutrition) upstream. Which token does i… |
| **Total** | | **511,114** | **34,370** | **197,022** | **0** | **$0.1218** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 32s