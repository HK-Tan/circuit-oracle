# Circuit Oracle Report
**Date:** 2026-07-28 07:22:29 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "Dietitian/Nutritionist" classification is driven by a tightly clustered **semantically valid** diet/nutrition-content circuit — *not* by gender markers. Every high-impact feature traces back to nutrition vocabulary: "Nutritional", "nutrition", "Dietetics", "Dietitian", "Pediatric", "Nutrition", "Sports", "Health" — and the strongest paths run through the same `Nutritional`/`nutrition`/`Dietetics` token positions that name the profession.

**Confidence:** 8

**Reasoning:**
- **Output-driving features (L14–L19, all positive direct_effect):** L19:F1589 "nutritional/scientific studies" (direct_effect 0.064, activation 63), L4:F13412 "diet/dietary health" (0.154, fires at Dietetics/Health/Public Health Dietitian positions), L6:F11327 "food/nutrition" (0.068), L14:F4197 "food words" (0.059), L17:F7545 "nurses/healthcare" (0.045), L2:F2589 "medical professionals/specialists" (0.059). All are **domain-content features** with low frac_nonzero (0.008–0.038) and high max_token evidence on diet/nutrition tokens.
- **Critical negative evidence for the user's hypothesis:** L0:F9519 "she/her pronoun" appears in the top features with direct_effect **−0.05** (suppressive — it *pushes against* the dietitian classification, not toward it). L0:F14824 "has" (−0.12) and L0:F8061 "in" (−0.041) are also suppressive function-word features. The "Sports" embedding (pos 63) feeds L4:F10494 with a positive sign, but only because it precedes "Nutrition" in "Sports Nutrition", and the same path passes through nutrition-word features. There is no path from the subject's name "Heather" or from feminine-coded tokens that drives the probe.
- **Token-embedding grounding:** The chain reaches embeddings at every key profession name — `Nutritional` (pos 9, direct_effect 1.45→L4:F13412), `nutrition` (pos 50, 29.5→L19:F1589), `Nutrition` (pos 64, 6.9→L4:F10494), `titian` (pos 37, subword of "Dietitian", 14.0→L4:F13412 and 19.1→L2:F2589), `Pediatric` (pos 49, 4.75→L2:F2589), `Health` (pos 35, 2.66→L4:F13412), `Die`/`te`/`tics` (pos 20-22, the "Dietetics" subword tokens).
- **Signal flow:** Embeddings of nutrition/diet terms → L3/L4 morphological & "from"/scientific-notation detectors (L3:F11774, F10028) → L4 diet-term consolidator (F13412) → L6 food/nutrition + L6 academic-disciplines (F4051) → L8/L9 nutrient/eating generalists → L14 food-word feature → L17 high-activation food-nutrition features (F14680, F2063, F7545) → L18/L19 nutritional-context and diet-eat-health features → output logit. The L2 "medical professionals" feature is the only one that could in principle index a *named role*; it fires on "Dietitian"/"Pediatric"/"nutrition" tokens and feeds L4, but its primary evidence is still lexical (nurse/nutritionist suffixes), not gendered.
- **Conclusion:** The probe is classifying on the same linguistic evidence a human reader would use — the repeated appearance of *Nutritional Sciences, Dietetics, Public Health Dietitian, Prenatal and Pediatric nutrition, RD, Sports Nutrition* — via features whose own labels and top-activating examples are all diet/food/nutrition/healthcare. Gender markers like "she" are present in the top-k but are *negative* contributors. The user's concern is not supported by this circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: Nutritional (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: Die (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: te (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: tics (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 37 | Emb: titian (pos 37) — Dietitian | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 35 | Emb: Health (pos 35) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 49 | Emb: Pediatric (pos 49) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 50 | Emb: nutrition (pos 50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 64 | Emb: Nutrition (pos 64) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 63 | Emb: Sports (pos 63) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 37 | L2: medical professionals/specialists tokens |  words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 50 | L2: medical professionals/specialists tokens |  words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 64 | L2: medical professionals/specialists tokens |  words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L0:F9888](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) | 18 | L0: education token feature |  words related to formal schooling | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 21 | L3: morphological/scientific-misc features |  what appears to be a smattering of strings related to scientific notation, live radio, and roman numerals | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 21 | L3: morphological/scientific-misc features | words or short phrases that include "made of/from", and words ending with "ice", "ita", "ons", "ura", and "mor" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 22 | L3: morphological/scientific-misc features |  what appears to be a smattering of strings related to scientific notation, live radio, and roman numerals | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 22 | L3: morphological/scientific-misc features | words or short phrases that include "made of/from", and words ending with "ice", "ita", "ons", "ura", and "mor" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 9 | L4: diet/dietary health tokens |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | L4: diet/dietary health tokens |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | L4: diet/dietary health tokens |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 37 | L4: diet/dietary health tokens |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | L4: diet/dietary health tokens |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 64 | L4: diet/dietary health tokens |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 21 | L4: food/rations/feeding |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 64 | L4: food/rations/feeding |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 9 | L6: food/nutrition words |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 21 | L6: food/nutrition words |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 37 | L6: food/nutrition words |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 50 | L6: food/nutrition words |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F4051](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4051) | 9 | L6: food/nutrition words |  words related to academic disciplines | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4051) |
| [L8:F8003](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8003) | 21 | L8: nutrients/food groups/minerals |  words about nutrients, foods, and minerals, especially regarding dietary studies and children's health. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8003) |
| [L9:F15926](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15926) | 21 | L9: eating/meals | mentions about eating and meals | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15926) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | L14: food/food-insecurity words |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 21 | L14: food/food-insecurity words |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 50 | L14: food/food-insecurity words |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L15:F1771](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1771) | 9 | L15: education/arts/academia | words related to education, the arts, and academia | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1771) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 9 | L17: food/nutrition/diet (high-act) | nutrition, food, and diets | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L17:F2063](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/2063) | 9 | L17: food/nutrition/diet (high-act) | food and nutrition | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/2063) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 21 | L17: food/nutrition/diet (high-act) | mentions of architecture, design, nurses and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 9 | L18: eating & health | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 21 | L18: eating & health | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 50 | L18: eating & health | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 9 | L19: nutritional/scientific studies |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 21 | L19: nutritional/scientific studies |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 50 | L19: nutritional/scientific studies |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:13412 de=0.154 |
| 3 | `inspect_feature` ×11 | L4:13412, L6:11327, L19:1589, L2:2589, L14:4197, L4:10494, L0:14824, L0:8974, L0:9519, L0:9888, L0:8061 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13412@21` | ❌ error | — | — | Trace the L4:F13412 'diets and dietary health' feature at pos 21 (final position… |
| SA-2 | `L19:F1589@21` | ❌ error | — | — | Trace the L19:F1589 'nutritional studies context' feature at pos 21 upstream. Th… |
| SA-3 | `L6:F11327@21` | ❌ error | — | — | Trace the L6:F11327 'food/nutrition words' feature at pos 21 upstream. Reach emb… |
| SA-4 | `L2:F2589@37` | ❌ error | — | — | Trace L2:F2589 'medical professionals and medical specialties' at pos 37 upstrea… |
| SA-5 | `L14:F4197@21` | ❌ error | — | — | Trace L14:F4197 'food/food insecurity' feature at pos 21 upstream. Reach embeddi… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F1589@21, k=15 → L4:F13412 (de=10.69) +14 more |
| 2 | `get_upstream_features` | L6:F11327@21, k=15 → L4:F13412 (de=5.88) +14 more |
| 3 | `get_upstream_features` | L14:F4197@21, k=15 → L6:F11327 (de=7.72) +14 more |
| 4 | `get_upstream_features` | L2:F2589@37, k=15 → Emb:"titian"@37 (de=19.12) +14 more |
| 5 | `get_upstream_features` | L4:F13412@21, k=15 → L3:F11774 (de=4.81) +14 more |
| 6 | `inspect_feature` ×9 | L4:9554, L17:7545, L16:2393, L16:12752, L18:6105, L8:8003, L9:15926, L3:11774, L3:10028 |
| 7 | `get_upstream_features` | L4:F10494@64, k=15 → Emb:" Nutrition"@64 (de=6.91) +14 more |
| 8 | `get_upstream_features` | L4:F13412@22, k=15 → L3:F11774 (de=3.98) +14 more |
| 9 | `get_upstream_features` | L4:F13412@37, k=15 → Emb:"titian"@37 (de=14.00) +14 more |
| 10 | `get_upstream_features` | L19:F1589@9, k=15 → Emb:" Nutritional"@9 (de=26.12) +14 more |
| 11 | `get_upstream_features` | L19:F1589@50, k=15 → Emb:" nutrition"@50 (de=29.50) +14 more |
| 12 | `get_upstream_features` | L2:F2589@21, k=15 → ❌ Feature (layer=2, feature_idx=2589) not found at pos=21. Thi |
| 13 | `get_upstream_features` | L2:F2589@22, k=15 → ❌ Feature (layer=2, feature_idx=2589) not found at pos=22. Thi |
| 14 | `get_upstream_features` | L17:F14680@9, k=15 → Emb:" Nutritional"@9 (de=30.88) +14 more |
| 15 | `get_upstream_features` | L15:F1771@9, k=15 → L6:F4051 (de=4.47) +14 more |
| 16 | `get_upstream_features` | L2:F2589@50, k=15 → Emb:" nutrition"@50 (de=5.28) +14 more |
| 17 | `get_upstream_features` | L2:F2589@64, k=15 → Emb:" Nutrition"@64 (de=3.36) +14 more |
| 18 | `inspect_feature` ×4 | L6:4051, L17:14680, L15:1771, L17:2063 |

### Build

`build_circuit` → 24 nodes, 49 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 67,246 | 12,895 | 366,734 | 0 | $0.0577 | — | — |
| **Total** | | **67,246** | **12,895** | **366,734** | **0** | **$0.0577** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 16s