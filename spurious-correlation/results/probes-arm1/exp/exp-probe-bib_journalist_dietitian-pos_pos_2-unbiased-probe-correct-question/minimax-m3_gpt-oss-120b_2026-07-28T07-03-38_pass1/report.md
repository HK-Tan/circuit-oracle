# Circuit Oracle Report
**Date:** 2026-07-28 07:03:38 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "nutritionist" is driven by genuine domain-vocabulary features (nutrition, diet, food-preparation, scientific-nutrition-study context) — and NOT by gender markers, which in fact *suppress* the probe score. The user's concern about spurious gender-feature use is not supported by this circuit.

**Confidence:** 8

**Reasoning:**

**Positive (probe-supporting) paths** — all grounded in *content words*, not pronouns:
- **Emb " nutrition" (pos 13)** is the dominant driver. It feeds a clean hierarchy: L0:F5201 (pure "nutrition" token detector, frac=0.00026) → L3:F6246 (morpheme "Nutrients"/"-ure", frac=0.00389) → L4 supernode (F13412 diets, F10494 health/medicine/diet, F9554 food/rations, all pos 13) → L6:F11327 (food/nutrition vocabulary, frac=0.0117) → L14:F4197 (food/food-insecurity language, frac=0.015) → L19:F1589 (scientific-nutrition study context, frac=0.038). The L19 feature promotes "diet/food/nutrition/feeding" and is the single largest direct contributor to the probe (+0.084), and its causal backbone is the literal "nutrition" token — exactly the kind of profession-defining keyword the user wants to see.
- **Emb " cook" (pos 17)** drives a parallel path: L4:F14942 (cooking/kitchen/chef, frac=0.005) → L7:F6434 (kitchen, frac=0.0037) → L15:F2510 (food preparation/consumption, frac=0.0087, direct effect +0.065). This encodes the *activity* component of the profession (teaching people to cook healthy meals).
- Supporting token-level signal from "passion" (L1:F815) and "learn" (L1:F728) feed the "teaching/educator" aspect.

**Negative (probe-suppressing) path — the gender-marker path:**
- **Emb "She" (pos 1)** activates L0:F9519/F14824 ("she"/"her"/"has"), L1:F7244 (she), L2:F2128 (multilingual pronouns, but **suppresses** "himself"/"који" in its decoder and promotes "she" — it's a "she" feature in this context), L4:F7864 (code/XML feature co-firing on "She" — its autointerp label is code, but the promoted-token list is "she/herself", confirming it acts as a feminine-pronoun detector on this input), L5:F10952 (3rd-person pronouns), L6:F11646 ("references to women…triggered by pronouns and titles", frac=0.020). The promoted tokens of F11646 are "herself / she / her / 但她 / Autorin" — unambiguously a feminine-reference feature.
- F11646 has a **negative** direct effect on the probe (−0.064). So the gender signal flows in *opposition* to the nutritionist classification.

**Why this answers the user's concern:** The probe is *not* using "She" as a shortcut for "nutritionist." The feminine-pronoun chain runs through a distinct parallel pathway and lands on F11646 with a *suppressive* sign. A profession-classifier that relied on gender would push the probe *up* on "She" — here, "She" pushes it *down*. The probe is instead reading off (a) the token "nutrition" itself, (b) downstream food/diet/cooking vocabulary, and (c) a high-level scientific-nutrition-study concept. The concern about spurious gender-feature use is, on the evidence of this circuit, misplaced: gender markers act as a *mild* anti-signal here, not a positive one.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 13 | Token detector: "nutrition" |  the word "nutrition" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 7 | Token detector: "others" |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | Token detector: "she"/"her" |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 2 | Token detector: "she"/"her" | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L1:F815](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/815) | 4 | Token detector: "passion" |  the word "passion" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/815) |
| [L1:F7244](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) | 1 | Token detector: "she" | the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | Generic pronoun detector (he/him/she) |  pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, *ele*, and *ela* across multiple languages. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L3:F6246](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) | 13 | Morpheme detector: "Nutrients"/"-ure" |  the word "Nutrients" and words containing "ure". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) |
| [L1:F728](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/728) | 8 | Knowledge-gaining verbs |   words related to gaining knowledge | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/728) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Diet/dietary health terms |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 13 | Diet/dietary health terms |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Diet/dietary health terms |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F14942](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14942) | 17 | Cooking/kitchen/chef context | mentions of cooking, kitchens, chefs, and associated locations. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14942) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Code/XML feature co-firing on "She" | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | 3rd-person pronouns | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Food/nutrition vocabulary |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 28 | Food/nutrition vocabulary |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | References to women (She/her titles) — SUPPRESSES probe |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F6434](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/6434) | 17 | Kitchen-specific context |  words related to kitchens | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/6434) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 13 | Food/food-insecurity language |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L15:F2510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) | 17 | Food preparation/consumption |  words and phrases related to food preparation and consumption, along with some words relating to the digestive system and eating disorders | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 13 | Scientific-nutrition study context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 28 | Scientific-nutrition study context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11327 de=0.141 |
| 3 | `inspect_feature` ×17 | L6:11327, L14:4197, L4:13412, L19:1589, L15:2510, L0:14824, L0:2349, L6:11646, L0:9519, L1:728, L0:6051, L1:7244, L0:8444, L0:2238, L4:10494, L4:9554, L1:815 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@13` | ✅ reported | 8 | 11 | Trace L19:F1589 (a context of scientific nutritional studies) at pos 13 back thr… |
| SA-2 | `L14:F4197@13` | ✅ reported | 4 | 6 | Trace L14:F4197 (food/food insecurity words) at pos 13 back through the circuit … |
| SA-3 | `L15:F2510@17` | ✅ reported | 5 | 4 | Trace L15:F2510 (food preparation/cooking words) at pos 17 back through the circ… |
| SA-4 | `L6:F11327@13` | ✅ reported | 6 | 11 | Trace L6:F11327 (food/nutrition related words) at pos 13 back through the circui… |
| SA-5 | `L6:F11646@1` | ✅ reported | 4 | 6 | Trace L6:F11646 (references to women, feminine pronouns) at pos 1 — this is a NE… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@13, k=10 | Emb:" nutrition"@13 (de=31.25) +9 more |
| 3 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 4 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 5 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 6 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 7 | `get_upstream_features` | L14:F4197@13, k=10 | Emb:" nutrition"@13 (de=14.31) +9 more |

**Findings:** The target L19:F1589 is driven primarily by the token embedding for "nutrition" at position 13. This signal propagates through a hierarchy of nutrition-related features (layers 14 → 6 → 4) before reaching the high-level scientific‑nutrition context. The path includes a lower-third feature (layer 4) and positive-effect embeddings, fulfilling the required termination conditions.

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 2 | `get_upstream_features` | L14:F4197@13, k=10 | Emb:" nutrition"@13 (de=14.31) +9 more |
| 3 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 4 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 5 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 6 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 7 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 8 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 9 | `inspect_feature` | L1, F6895 | " the word "visit" and related forms" |
| 10 | `get_upstream_features` | L4:F9554@13, k=10 | Emb:" nutrition"@13 (de=15.88) +9 more |
| 11 | `inspect_feature` | L8, F8003 | " words about nutrients, foods, and minerals, especially regarding diet" |
| 12 | `inspect_feature` | L7, F311 | " terms related to diet and race" |

**Findings:** Tracing from L14:F4197 (food‑insecurity detector) reveals that its strongest excitatory drivers are lower‑layer features that respond to generic nutrition vocabulary. The most direct upstream source is the input token embedding " nutrition" at position 13, which positively excites a layer‑6 feature (F11327) specialized for food/nutrition words. That feature, in turn, significantly boosts the targe…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F2510 | " words and phrases related to food preparation and consumption, along " |
| 2 | `get_upstream_features` | L15:F2510@17, k=10 | Emb:" cook"@17 (de=28.88) +9 more |
| 3 | `inspect_feature` | L4, F14942 | "mentions of cooking, kitchens, chefs, and associated locations." |
| 4 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 5 | `get_upstream_features` | L4:F14942@17, k=10 | Emb:" cook"@17 (de=22.50) +9 more |
| 6 | `inspect_feature` | L7, F6434 | " words related to kitchens" |
| 7 | `get_upstream_features` | L6:F11327@17, k=10 | Emb:" cook"@17 (de=16.25) +9 more |

**Findings:** The target feature L15:F2510 (food‑preparation detector) receives its strongest positive influence from the input token embedding 'cook' at position 17 (direct_effect ~28.9). Upstream, a mid‑layer cooking‑specific feature in layer 4 (F14942) contributes a sizable positive effect (4.4) and itself is driven mainly by the same 'cook' embedding (direct_effect 22.5). Further upstream features in layers…

</details>

<details>
<summary><b>SA-4</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 5 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 6 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 7 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 8 | `inspect_feature` | L1, F6895 | " the word "visit" and related forms" |
| 9 | `get_upstream_features` | L4:F9554@13, k=10 | Emb:" nutrition"@13 (de=15.88) +9 more |
| 10 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 11 | `get_upstream_features` | L3:F6246@13, k=10 | Emb:" nutrition"@13 (de=12.25) +9 more |
| 12 | `inspect_feature` | L0, F7843 | " words related to nutrition and malnutrition" |
| 13 | `inspect_feature` | L0, F5201 | " the word "nutrition"" |
| 14 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** The target L6:F11327 is driven primarily by the embedding of the token "nutrition" (direct effect 21.0).  Mid‑layer features in layers 4 and 3 also source most of their influence from the same embedding, forming a cascade that ends in a pure token detector (L0:F5201) which fires on the word "nutrition" itself.  All discovered upstream nodes are in the lower third of the model (layer ≤8) and includ…

</details>

<details>
<summary><b>SA-5</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |
| 6 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 7 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 8 | `get_upstream_features` | L2:F2128@1, k=10 | Emb:"She"@1 (de=20.25) +9 more |
| 9 | `inspect_feature` | L0, F15382 | "mentions of a female person." |

**Findings:** The gender‑feature L6:F11646 (detects references to women) is driven primarily by the input token "She" at position 1, which exerts a large positive direct effect. The signal propagates through a chain of pronoun‑detecting features in lower layers (L5:F10952, L4:F7864, L2:F2128), all of which are also highly activated by "She". Since we have reached features in layers <=8 and identified direct emb…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L4:14942, L7:6434, L3:6246, L0:5201, L4:7864, L5:10952, L2:2128 |

### Build

`build_circuit` → 25 nodes, 27 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 90,614 | 5,649 | 108,855 | 0 | $0.0405 | — | — |
| SA-3 | openai/gpt-oss-120b | 62,941 | 4,072 | 7,584 | 0 | $0.0120 | ✅ 5F/4E | Trace L15:F2510 (food preparation/cooking words) at pos 17 b… |
| SA-5 | openai/gpt-oss-120b | 86,467 | 6,761 | 12,640 | 0 | $0.0172 | ✅ 4F/6E | Trace L6:F11646 (references to women, feminine pronouns) at … |
| SA-1 | openai/gpt-oss-120b | 75,026 | 6,522 | 10,240 | 0 | $0.0153 | ✅ 8F/11E | Trace L19:F1589 (a context of scientific nutritional studies… |
| SA-2 | openai/gpt-oss-120b | 144,296 | 6,445 | 15,200 | 0 | $0.0257 | ✅ 4F/6E | Trace L14:F4197 (food/food insecurity words) at pos 13 back … |
| SA-4 | openai/gpt-oss-120b | 193,692 | 12,114 | 30,688 | 0 | $0.0368 | ✅ 6F/11E | Trace L6:F11327 (food/nutrition related words) at pos 13 bac… |
| **Total** | | **653,036** | **41,563** | **185,207** | **0** | **$0.1476** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 47s