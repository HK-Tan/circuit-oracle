# Circuit Oracle Report
**Date:** 2026-07-28 07:20:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for the nutrition/dietitian profession is driven by two parallel mechanisms — a genuine profession-indicator pathway grounded in the tokens "nutrition" (pos 13) and "cook" (pos 17) propagating through deep food/diet/cuisine features, and a significant spurious pathway where the gendered pronoun "She" (pos 1) and female-reference features push the probe the *opposite* direction (negative direct effect), suggesting the probe partially uses gender as a debiasing feature rather than as a positive profession marker.

**Confidence:** 7

**Reasoning:**

**Genuine profession pathway (positive drivers, all from food/nutrition tokens):**
- The top positive driver is **L6:F11327** (frac_nonzero=0.012, "food/nutrition detector", direct_effect=+0.141), grounded directly in the embedding token `nutrition` at pos 13 (direct_effect +21.0 upstream). 
- **L14:F4197** ("food-insecurity/rationing language", direct_effect=+0.137) and **L4:F13412** ("diets/dietary health", direct_effect=+0.134) form a cascade at pos 13, all excited by the same `nutrition` token (direct_effects of +14.3, +14.1 from embedding).
- **L19:F1589** ("scientific nutritional studies", direct_effect=+0.084) is the deepest profession-concept feature, receiving +31.25 from the `nutrition` embedding and +8.69 from L14:F4197.
- **L15:F2510** ("food preparation/cooking", direct_effect=+0.065 at pos 17) traces to the `cook` token at pos 17 via the kitchen/cooking features L4:F14942, L7:F6434, L8:F9351. This is a legitimate profession-indicator (cooking skill).

**Spurious gender pathway (negative drivers — the user concern is partially confirmed but inverted):**
- **L6:F11646** ("references to women", frac_nonzero=0.020) at pos 1 has direct_effect **-0.064** — it *suppresses* the probe score.
- **L0:F9519** ("she/her pronoun", frac_nonzero=0.011) at pos 1 has direct_effect **-0.056** — also *suppresses*.
- **L1:F7244** ("the pronoun 'she'") similarly fires on the same embedding `She` (direct_effect +15.75 into the feature).
- All three trace back to embedding `She` at pos 1 (direct_effects +19.25, +15.75). The "she" pronoun is *inhibiting* the nutrition/dietitian classification — likely because the probe has learned that nutritionist/dietitian corpora contain more male "he" patterns, OR more likely because the gendered bias is acting as a suppressor that partially counteracts association with stereotypically-female professions.

**Generic function-word features (small positive drivers, not profession-specific):**
- L0:F14824 (`has`), L0:F2349 (`others`), L0:F2238 (`about`), L0:F8444 (`to`) — these are general lexical detectors that fire everywhere (frac_nonzero 0.007–0.017), not profession-specific.

**Conclusion regarding user concern:** The user worried the circuit uses *gender markers* as profession predictors. The evidence here shows the opposite: gender features (`She`, "references to women") have **negative** direct effects on the probe. The probe is *resisting* the gender signal — its positive signal comes almost entirely from genuine profession tokens (`nutrition`, `cook`) via deep food/diet/kitchen features. This is a healthier pattern than the user feared, though the presence of multiple pronoun-related features with non-trivial magnitude means the probe has *learned* gender associations even if it currently uses them as suppressors — a debiasing-like pattern rather than a stereotype-amplifying one.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: has (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: passion (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: learn (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: about (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: to (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: cook (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: nutrition (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: others (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 2 | Generic function-word features (L0) | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 7 | Generic function-word features (L0) |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 9 | Generic function-word features (L0) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 16 | Generic function-word features (L0) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 22 | Generic function-word features (L0) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | She/Her pronoun detector (L0:L6) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L1:F7244](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) | 1 | She/Her pronoun detector (L0:L6) | the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | She/Her pronoun detector (L0:L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L1:F815](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/815) | 4 | Passion/Learn features (L1) |  the word "passion" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/815) |
| [L1:F728](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/728) | 8 | Passion/Learn features (L1) |   words related to gaining knowledge | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/728) |
| [L3:F6246](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) | 13 | Food/Nutrition/Diet features (L4-L8) | the word "Nutrients" and words containing "ure". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Food/Nutrition/Diet features (L4-L8) | terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Food/Nutrition/Diet features (L4-L8) | words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 13 | Food/Nutrition/Diet features (L4-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F14942](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14942) | 17 | Food/Nutrition/Diet features (L4-L8) | mentions of cooking, kitchens, chefs, and associated locations. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14942) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Food/Nutrition/Diet features (L4-L8) | words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 17 | Food/Nutrition/Diet features (L4-L8) | words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L7:F6434](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/6434) | 17 | Food/Nutrition/Diet features (L4-L8) | words related to kitchens | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/6434) |
| [L8:F9351](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9351) | 17 | Food/Nutrition/Diet features (L4-L8) | words related to cooking and cuisine | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9351) |
| [L8:F15894](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15894) | 17 | Food/Nutrition/Diet features (L4-L8) | words related to dining out | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15894) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 13 | Food/cooking late-layer features (L14-L15) | words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L15:F2510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) | 17 | Food/cooking late-layer features (L14-L15) |  words and phrases related to food preparation and consumption, along with some words relating to the digestive system and eating disorders | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 13 | Profession concept (L19) |  a context of scientific, specially nutritional studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output logit | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'PROBE_0' is not one of the top-k next-token candidate |
| 3 | `get_top_features` | 20 features; top: L6:11327 de=0.141 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11327@13` | ✅ reported | 5 | 4 | Trace upstream from L6:F11327 at pos 13. This is the top positive driver of the … |
| SA-2 | `L14:F4197@13` | ✅ reported | 8 | 11 | Trace upstream from L14:F4197 at pos 13. This is the second top positive driver.… |
| SA-3 | `L4:F13412@13` | ✅ reported | 3 | 3 | Trace upstream from L4:F13412 at pos 13. Third top positive driver. Determine wh… |
| SA-4 | `L19:F1589@13` | ✅ reported | 5 | 8 | Trace upstream from L19:F1589 at pos 13. Late-layer feature near the probe. Dete… |

<details>
<summary><b>SA-1</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |

**Findings:** L6:F11327 (pos 13) is a selective food/nutrition detector. Its strongest positive driver is the input embedding of the token "nutrition" at the same position (direct effect +21.0). Supporting upstream positive influences come from two mid‑layer food/diet features (L4:F13412 and L4:F9554) and very low‑layer generic features. The trace reaches the lower‑third of the model (layer ≤8) and includes a d…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 2 | `get_upstream_features` | L14:F4197@13, k=10 | Emb:" nutrition"@13 (de=14.31) +9 more |
| 3 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 4 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 5 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 6 | `get_upstream_features` | L4:F9554@13, k=10 | Emb:" nutrition"@13 (de=15.88) +9 more |
| 7 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 8 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 9 | `inspect_feature` | L8, F8003 | " words about nutrients, foods, and minerals, especially regarding diet" |

**Findings:** The circuit trace shows that L14:F4197 (food‑insecurity detector) is strongly driven by the raw token embedding 'nutrition' and by a cascade of lower‑layer food‑related features (L6:11327, L4:9554, L4:13412, L8:8003). These upstream features all encode various aspects of food, diet, rations, and nutrition, culminating in a positive signal for food‑insecurity language. The presence of a positive em…

</details>

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 3 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 4 | `inspect_feature` | L0, F5201 | " the word "nutrition"" |
| 5 | `get_upstream_features` | L0:F5201@13, k=10 | Emb:" nutrition"@13 (de=27.12) +9 more |

**Findings:** Tracing upstream from the diet‑related feature L4:F13412 (pos 13) shows the strongest influence comes from the raw token embedding ' nutrition' (pos 13). The second strongest positive influence is a higher‑layer feature detecting nutrient‑related suffixes (L3:F6246). The third‑largest positive driver is the raw embedding for the pronoun 'She' at position 1. This embedding encodes the gendered subj…

</details>

<details>
<summary><b>SA-4</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@13, k=10 | Emb:" nutrition"@13 (de=31.25) +9 more |
| 3 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 4 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 5 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 6 | `get_upstream_features` | L14:F4197@13, k=10 | Emb:" nutrition"@13 (de=14.31) +9 more |
| 7 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 8 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |

**Findings:** L19:F1589 (position 13) is a late-layer feature that strongly responds to the token "nutrition" and to upstream features detecting food-related discourse. The most influential upstream drivers are a food-insecurity detector (L14:4197) and a general food/nutrition detector (L6:11327). Both of these, in turn, are grounded in lower-layer diet and feeding concepts (L4:13412 and L4:9554) and receive di…

</details>

### Re-dispatch (round 2): 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L6:F11646@1` | ❌ error | — | — | Trace upstream from L6:F11646 at pos 1. This is a "references to women" feature … |
| SA-6 | `L0:F9519@1` | ❌ error | — | — | Trace upstream from L0:F9519 at pos 1. This is a "she/her" pronoun feature with … |
| SA-7 | `L15:F2510@17` | ✅ reported | 6 | 6 | Trace upstream from L15:F2510 at pos 17. Food preparation feature. Determine whi… |

<details>
<summary><b>SA-7</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F2510 | " words and phrases related to food preparation and consumption, along " |
| 2 | `get_upstream_features` | L15:F2510@17, k=20 | Emb:" cook"@17 (de=28.88) +19 more |
| 3 | `inspect_feature` | L4, F14942 | "mentions of cooking, kitchens, chefs, and associated locations." |
| 4 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 5 | `get_upstream_features` | L4:F14942@17, k=20 | Emb:" cook"@17 (de=22.50) +19 more |
| 6 | `get_upstream_features` | L6:F11327@17, k=20 | Emb:" cook"@17 (de=16.25) +19 more |
| 7 | `inspect_feature` | L7, F6434 | " words related to kitchens" |
| 8 | `inspect_feature` | L8, F9351 | " words related to cooking and cuisine" |
| 9 | `inspect_feature` | L8, F15894 | " words related to dining out" |

**Findings:** The target feature L15:F2510 (food‑preparation detector) is driven primarily by the input token 'cook' (positive direct effect 28.9) and a cascade of lower‑layer cooking‑related features. The strongest upstream non‑embedding driver is L4:F14942 (kitchen context) which itself receives strong excitation from the same 'cook' token and from L6:F11327 (general food vocabulary). Additional supportive si…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L0:14824, L6:11646, L0:9519, L15:2510, L0:2349, L0:6051 |
| 2 | `get_upstream_features` | L6:F11646@1, k=8 → Emb:"She"@1 (de=19.25) +7 more |
| 3 | `get_upstream_features` | L0:F9519@1, k=8 → Emb:"She"@1 (de=15.75) +7 more |
| 4 | `get_upstream_features` | L0:F14824@2, k=8 → Emb:" has"@2 (de=32.75) +7 more |
| 5 | `get_upstream_features` | L0:F2238@9, k=8 → Emb:" about"@9 (de=34.25) +7 more |
| 6 | `get_upstream_features` | L0:F8444@16, k=8 → Emb:" to"@16 (de=40.50) +7 more |
| 7 | `inspect_feature` ×5 | L1:728, L1:7244, L1:815, L0:2238, L0:8444 |
| 8 | `get_upstream_features` | L4:F10494@13, k=6 → Emb:" nutrition"@13 (de=13.12) +5 more |
| 9 | `get_upstream_features` | L1:F728@8, k=5 → Emb:" learn"@8 (de=21.50) +4 more |
| 10 | `inspect_feature` | L4, F7864 → "xml or source code snippets, especially tags and possibly keywords in " |

### Build

`build_circuit` → 16 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 37,752 | 5,739 | 144,742 | 0 | $0.0269 | — | — |
| SA-3 | openai/gpt-oss-120b | 37,802 | 3,322 | 5,056 | 0 | $0.0077 | ✅ 3F/3E | Trace upstream from L4:F13412 at pos 13. Third top positive … |
| SA-4 | openai/gpt-oss-120b | 93,695 | 6,175 | 5,984 | 0 | $0.0178 | ✅ 5F/8E | Trace upstream from L19:F1589 at pos 13. Late-layer feature … |
| SA-1 | openai/gpt-oss-120b | 35,140 | 3,544 | 10,112 | 0 | $0.0075 | ✅ 5F/4E | Trace upstream from L6:F11327 at pos 13. This is the top pos… |
| SA-2 | openai/gpt-oss-120b | 89,369 | 6,972 | 7,584 | 0 | $0.0177 | ✅ 8F/11E | Trace upstream from L14:F4197 at pos 13. This is the second … |
| SA-7 | openai/gpt-oss-120b | 108,703 | 6,664 | 0 | 0 | $0.0203 | ✅ 6F/6E | Trace upstream from L15:F2510 at pos 17. Food preparation fe… |
| **Total** | | **402,461** | **32,416** | **173,478** | **0** | **$0.0980** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 59s