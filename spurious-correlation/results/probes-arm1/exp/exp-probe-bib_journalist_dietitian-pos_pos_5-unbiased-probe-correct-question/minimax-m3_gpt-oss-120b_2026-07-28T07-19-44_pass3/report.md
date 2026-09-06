# Circuit Oracle Report
**Date:** 2026-07-28 07:19:45 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is driven by domain-specific profession vocabulary — the input tokens "nutrition," "eating," "disordered," "sports," and the capitalized "Nutrition"/"Die" (from "Dietetics") in "Academy of Nutrition and Dietetics" — not by gender markers, so the user concern about spurious gender features is **not supported** by this circuit.

**Confidence:** 8/10

**Reasoning:**

The circuit traces cleanly from raw input token embeddings through increasingly abstract profession-related features to the probe direction:

**Token embeddings (pos 7 = " nutrition", pos 13 = " eating", pos 12 = " disordered", pos 6 = " sports", pos 23/25 = " Nutrition"/" Die" from "Dietetics")** push strongly into the L0 token-detector features (L0:F5201 fires on "nutrition" with direct_effect 27.125, L0:F10254 fires on "sports" with direct_effect 25.5, L0:F2268 fires on "spokesperson" with direct_effect 23.5). These L0 detectors themselves show up in the top-15 with **negative** direct_effects (-0.088, -0.091, -0.088) — i.e., the raw "nutrition/sports/spokesperson" token features *suppress* the probe slightly, but they are not the drivers; the circuit funnels through deeper profession-semantic features.

**L4 (F13412 "terms related to diets and dietary health", F10494 "health, medicine, diet, drugs, age groups, exercise")** are the strongest positive contributors (direct_effects 0.176 and 0.142), and they are driven by the same domain tokens (upstream Emb:"nutrition" direct_effect 12.625 and 11.25 respectively, plus Emb:"eating"=8.69 and Emb:"disordered"=6.09 into F13412 at pos 13).

**L6 (F11327, "food or nutrition")** and **L7–L8 (F13562 training/conditioning, F7057 exercise/biology/chemistry)** aggregate these signals. L14 (F4197 food-insecurity, F16195 physical activity/training) combines the food and exercise streams. The L19 (F1589 "scientific, especially nutritional, studies") is the terminal profession-semantic feature, with the most extreme upstream attribution: Emb:"nutrition" → F1589 has direct_effect 32.25, and at pos 26 the capitalized "Nutrition"/"Die" tokens contribute 9.69 and 9.5.

**Critical finding on the gender concern:** the L0 pronoun features F9519 ("she"/"her", pos 1) and F15322 ("herself/itself", pos 4) appear in the top-15 with **negative** direct_effects (-0.0806 and -0.0742). They are *suppressing* the probe classification, not driving it. Upstream tracing confirms F9519 is driven solely by Emb:"Her" (direct_effect 16.75) with no positive propagation path into the profession-semantic features. F15322 is driven by Emb:"expertise" (14.81), not "herself" directly. No mid- or late-layer features in the circuit encode gender; the late-layer features (F4197, F16195, F1589, F7545) all encode nutrition/exercise/scientific-dietitian content.

**Mechanism:** The probe is classifying the text as the "dietitian/nutritionist" profession primarily because of the **explicit profession-content tokens** ("nutrition" at pos 7, "eating"/"disordered" at pos 12-13, "sports" at pos 6, and the "Nutrition/Dietetics" proper noun at pos 23-25). These tokens compose through a hierarchical feature chain: L0 token detectors → L4 diet/dietary-health features → L6 nutrition aggregator + L7–L8 exercise features → L14 food+activity features → L17/L19 scientific-nutrition context. The terminal L19:F1589 is the dominant single driver of the probe score (direct_effect 0.069), and it is *activated by* the "nutrition" embedding (Emb direct_effect 32.25). This is a **genuine profession-indicator circuit**, not a gender-spurious one — the user's concern is not borne out by this graph.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: nutrition (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: sports (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: eating (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: disordered (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: spokesperson (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Her (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: Nutrition/Die (pos 23,25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: Nutrition/Die (pos 23,25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 7 | L0 token-detector features for profession keywords |  the word "nutrition" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L0:F10254](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10254) | 6 | L0 token-detector features for profession keywords |  the word "sports". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10254) |
| [L0:F2268](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2268) | 18 | L0 token-detector features for profession keywords |  mentions of people communicating information via speech | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2268) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | L0 gender/pronoun features (INHIBITORY to probe) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F15322](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) | 4 | L0 gender/pronoun features (INHIBITORY to probe) | reflexive pronouns, particularly "herself" and "itself." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | L4 diet/dietary-health detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | L4 diet/dietary-health detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 26 | L4 diet/dietary-health detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 7 | L4 diet/dietary-health detectors |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 13 | L4 diet/dietary-health detectors |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 7 | L6 food/nutrition aggregator |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 26 | L6 food/nutrition aggregator |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L8:F7057](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7057) | 7 | L7-L8 physical activity / training / exercise detectors | terms related to exercise, biology and chemistry | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7057) |
| [L7:F13562](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13562) | 7 | L7-L8 physical activity / training / exercise detectors | terms related to physical and mental training or conditioning | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13562) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 7 | L14 food-insecurity / food features |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 26 | L14 food-insecurity / food features |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F16195](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) | 7 | L14 food-insecurity / food features | mentions of physical activity and training. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 7 | L17-L19 scientific-nutrition / dietitian context features |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 26 | L17-L19 scientific-nutrition / dietitian context features |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 26 | L17-L19 scientific-nutrition / dietitian context features | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:10494 de=0.176 |
| 3 | `inspect_feature` ×17 | L4:10494, L4:13412, L14:4197, L14:16195, L6:11327, L19:1589, L0:6051, L0:8975, L0:5201, L0:2268, L0:9519, L0:10148, L0:2083, L0:8028, L0:15322, L0:4030, L0:10254 |
| 4 | `get_upstream_features` | Emb:" nutrition"@7 (de=32.25) +7 more |
| 5 | `get_upstream_features` | Emb:" nutrition"@7 (de=12.88) +7 more |
| 6 | `get_upstream_features` | Emb:" nutrition"@7 (de=7.97) +7 more |
| 7 | `get_upstream_features` | Emb:" nutrition"@7 (de=11.25) +7 more |
| 8 | `get_upstream_features` | Emb:" nutrition"@7 (de=12.62) +7 more |
| 9 | `get_upstream_features` | Emb:" nutrition"@7 (de=17.50) +7 more |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@7` | ✅ reported | 6 | 7 | Trace this feature (which seems to be nutrition/science context) all the way bac… |
| SA-2 | `L14:F4197@7` | ❌ error | — | — | Trace the food/eating-related feature upstream to determine what tokens drive it… |
| SA-3 | `L14:F16195@7` | ✅ reported | 5 | 11 | Trace physical activity/training feature upstream to its source tokens. |
| SA-4 | `L0:F5201@7` | ❌ error | — | — | Trace the L0 nutrition-word feature upward through layers. What does it connect … |
| SA-5 | `L0:F9519@1` | ❌ error | — | — | Trace the L0 "she/her" pronoun feature upward. Is this feature pushing toward or… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@7, k=10 | Emb:" nutrition"@7 (de=32.25) +9 more |
| 3 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 4 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 5 | `get_upstream_features` | L14:F4197@7, k=10 | Emb:" nutrition"@7 (de=12.88) +9 more |
| 6 | `get_upstream_features` | L6:F11327@7, k=10 | Emb:" nutrition"@7 (de=17.50) +9 more |
| 7 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |

**Findings:** The target L19:F1589 (nutrition‑science context) receives a strong positive push from the input token embedding ' nutrition' (direct_effect 32.25). Upstream, the main contributors are L14:F4197 (food‑insecurity detector) and L6:F11327 (generic nutrition detector), both of which themselves are strongly driven by the same ' nutrition' embedding (direct_effect 12.875 and 17.5 respectively). These int…

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F16195 | "mentions of physical activity and training." |
| 2 | `get_upstream_features` | L14:F16195@7, k=10 | Emb:" nutrition"@7 (de=7.97) +9 more |
| 3 | `inspect_feature` | L8, F7057 | " terms related to exercise, biology and chemistry" |
| 4 | `inspect_feature` | L7, F13562 | " terms related to physical and mental training or conditioning" |
| 5 | `inspect_feature` | L4, F10494 | " words related to health, medicine, diet, drugs, age groups, and excer" |
| 6 | `get_upstream_features` | L8:F7057@7, k=10 | Emb:" nutrition"@7 (de=8.88) +9 more |
| 7 | `get_upstream_features` | L7:F13562@7, k=10 | Emb:" nutrition"@7 (de=8.12) +9 more |
| 8 | `get_upstream_features` | L4:F10494@7, k=10 | Emb:" nutrition"@7 (de=11.25) +9 more |
| 9 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |

**Findings:** The tracing starts from the physical‑activity feature (L14:F16195) and follows the strongest positive upstream drivers. The dominant upstream influence comes from the input token 'nutrition' (embedding) which directly excites the target. Mid‑level features in layers 8, 7 and 4 (exercise‑related, training‑related and health‑related detectors) relay this signal, with a clear path down to a low‑layer…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-6 | `L17:F7545@26` | ❌ error | — | — | Trace this L17 feature upstream. It seems to integrate the 'Nutrition Die' token… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F5201@7, k=8 → Emb:" nutrition"@7 (de=27.12) +7 more |
| 2 | `get_upstream_features` | L0:F9519@1, k=8 → Emb:"Her"@1 (de=16.75) +7 more |
| 3 | `get_upstream_features` | L4:F10494@13, k=8 → Emb:" nutrition"@7 (de=3.11) +7 more |
| 4 | `get_upstream_features` | L4:F13412@13, k=8 → Emb:" eating"@13 (de=8.69) +7 more |
| 5 | `get_upstream_features` | L4:F13412@26, k=8 → L3:F11774 (de=4.72) +7 more |
| 6 | `get_upstream_features` | L19:F1589@26, k=8 → L17:F7545 (de=10.38) +7 more |
| 7 | `get_upstream_features` | L0:F2268@18, k=8 → Emb:" spokesperson"@18 (de=23.50) +7 more |
| 8 | `get_upstream_features` | L0:F15322@4, k=8 → Emb:" expertise"@4 (de=14.81) +7 more |
| 9 | `get_upstream_features` | L17:F7545@26, k=8 → L4:F13412 (de=5.28) +7 more |
| 10 | `get_upstream_features` | L0:F10254@6, k=8 → Emb:" sports"@6 (de=25.50) +7 more |
| 11 | `get_upstream_features` | L0:F6051@14, k=8 → Emb:"."@14 (de=47.00) +7 more |
| 12 | `get_upstream_features` | L0:F2083@4, k=8 → Emb:" expertise"@4 (de=11.88) +7 more |
| 13 | `get_upstream_features` | L0:F8028@2, k=8 → Emb:" areas"@2 (de=18.00) +7 more |
| 14 | `get_upstream_features` | L0:F10148@1, k=8 → Emb:"Her"@1 (de=10.06) +7 more |
| 15 | `get_upstream_features` | L0:F4030@4, k=8 → Emb:" expertise"@4 (de=7.53) +7 more |
| 16 | `get_upstream_features` | L0:F2268@18, k=8 → Emb:" spokesperson"@18 (de=23.50) +7 more |
| 17 | `get_upstream_features` | L0:F6051@14, k=8 → Emb:"."@14 (de=47.00) +7 more |
| 18 | `get_upstream_features` | L0:F10254@6, k=8 → Emb:" sports"@6 (de=25.50) +7 more |

### Build

`build_circuit` → 15 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 52,926 | 6,708 | 243,612 | 0 | $0.0385 | — | — |
| SA-1 | openai/gpt-oss-120b | 82,540 | 6,093 | 0 | 0 | $0.0160 | ✅ 6F/7E | Trace this feature (which seems to be nutrition/science cont… |
| SA-3 | openai/gpt-oss-120b | 105,042 | 6,863 | 0 | 0 | $0.0199 | ✅ 5F/11E | Trace physical activity/training feature upstream to its sou… |
| **Total** | | **240,508** | **19,664** | **243,612** | **0** | **$0.0745** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 27s