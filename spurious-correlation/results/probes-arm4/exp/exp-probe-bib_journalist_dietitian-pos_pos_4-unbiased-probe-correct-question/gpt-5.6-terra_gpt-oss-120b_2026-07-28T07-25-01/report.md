# Circuit Oracle Report
**Date:** 2026-07-28 07:25:01 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s positive profession-classification score is driven chiefly by explicit dietetics/dietitian and nutrition-domain evidence—not by the female pronouns or name in the biography.

**Confidence:** 8/10

**Reasoning:** The saved circuit shows a coherent profession-semantic pathway from the text’s dietetics credentials into the probe direction.

- The strongest repeated direct driver is **L4:F13412**, the selective dietary-health feature (frac_nonzero **0.01216**; promotes *diet*, *diets*, *dieting*). It positively drives the probe at several relevant positions: pos 21 (**+0.1543**), 55 (**+0.1172**), 22 (**+0.0889**), 37 (**+0.0845**), and 36 (**+0.0591**). This repetition is exactly what is expected when the biography supplies multiple related occupation cues: “Dietetics,” “Dietitian,” “nutrition,” and specialist areas.

- The circuit traces this signal to the explicit credential tokens. **Emb: “Die / te” (Dietetics, pos 20–21)** directly excites L4:F13412 at pos 21 (**+4.0625** from “Die”), while **Emb: “Nutritional” (pos 9)** also contributes (**+1.4531**). Source influence confirms that the Dietetics token span is a major source: positions 20–21 provide **6.802%** of total signed graph influence, versus **2.883%** for the strongest non-source comparison position (**S/R = 2.36**).

- A separate explicit-title route begins at **Emb: “Die / titian” (Dietitian, pos 36–37)**. It strongly activates **L2:F2589**, a medical-professional/specialty detector (frac_nonzero **0.00848**, promotes *experts* and *specialists*): the “titian” subtoken at pos 37 has a very large upstream effect of **+19.125**. This feature directly raises the probe score by **+0.0591**. The source-span influence for positions 36–37 is also substantial (**5.637%**, **S/R = 1.55**), corroborating that the literal job title matters.

- The early dietary evidence is composed into broader food/nutrition semantics by **L6:F11327** (frac_nonzero **0.01166**; food/nutrition feature; direct effect **+0.0679**) and **L14:F4197** (frac_nonzero **0.0152**; food-related feature; direct effects **+0.0588** at pos 21 and **+0.0471** at pos 9). Both receive strong positive input from L4:F13412: respectively **+5.875** and **+5.0625**.

- These pathways converge at the major higher-level driver, **L19:F1589**, a nutritional-science/studies feature (frac_nonzero **0.03796**; promotes *diet*, *food*, *nutrition*, *dietary*, *eating*). At pos 21 it directly increases the probe score by **+0.0640**, with another positive instance at pos 50 (**+0.0439**). Its upstream evidence includes L4:F13412 (**+10.6875**), L6:F11327 (**+8.4375**), L14:F4197 (**+8.375**), and the Dietetics token embedding itself (**+7.1875**). Thus, the circuit is not merely lexical matching on the title: it aggregates a diet/nutrition domain representation into a profession-relevant concept.

Regarding the user’s concern, the inspected high-impact positive features do **not** represent female gender, pronouns, or names. The initial phrase “She has” is not supportive: **L0:F14824** detects “has” and has a **negative** direct effect (**−0.1211**). No high-ranked positive feature was found to encode “she,” “Heather,” or a feminine demographic marker. There are generic or imperfect features in the route—e.g. L14:F4197 fires broadly for food, including food insecurity, and L17:F7545 mixes healthcare/nursing with unrelated architecture/design examples—but the strongest evidence and source attribution are anchored in the genuine terms **“Dietetics,” “Dietitian,” “Nutritional Sciences,”** and repeated nutrition content.

Therefore, this probe appears predominantly to use legitimate occupation/domain indicators. Its likely limitation is **domain-level overgeneralization**—classifying food/nutrition or healthcare-related text as this profession—not reliance on gender.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 37 | Explicit medical-profession detector |  words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | Early diet/dietary-health detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | Early diet/dietary-health detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 36 | Early diet/dietary-health detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 37 | Early diet/dietary-health detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | Early diet/dietary-health detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 21 | Early diet/dietary-health detectors |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 21 | Food/nutrition semantic context |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 21 | Food-related domain abstraction |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | Food-related domain abstraction |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 21 | Nutritional-science context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 50 | Nutritional-science context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:13412 de=0.154 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13412@21` | ❌ error | — | — | Determine semantic role of repeated L4:F13412, especially whether it encodes gen… |
| SA-2 | `L19:F1589@21` | ❌ error | — | — | Trace this major late profession-score driver upstream. Identify semantic conten… |
| SA-3 | `L14:F4197@21` | ❌ error | — | — | Trace L14:F4197 source and determine whether it carries profession evidence or d… |
| SA-4 | `L6:F11327@21` | ❌ error | — | — | Trace this direct probe-driving feature upstream, characterize its semantic feat… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L4:13412, L19:1589, L14:4197, L6:11327, L0:14824, L2:2589 |
| 2 | `get_upstream_features` | L4:F13412@21, k=15 → L3:F11774 (de=4.81) +14 more |
| 3 | `get_upstream_features` | L19:F1589@21, k=15 → L4:F13412 (de=10.69) +14 more |
| 4 | `get_upstream_features` | L14:F4197@21, k=15 → L6:F11327 (de=7.72) +14 more |
| 5 | `get_upstream_features` | L6:F11327@21, k=15 → L4:F13412 (de=5.88) +14 more |
| 6 | `get_upstream_features` | L2:F2589@37, k=15 → Emb:"titian"@37 (de=19.12) +14 more |
| 7 | `inspect_feature` ×4 | L3:11774, L3:10028, L4:9554, L17:7545 |
| 8 | `get_source_influence` | {'source_positions': [36, 37], 'depth': 2} → {'depth': 2, 'source_positions': [36, 37], 'S_pct_of_total': 5.637, 'R_pct_of_to |
| 9 | `get_source_influence` | {'source_positions': [20, 21], 'depth': 2} → {'depth': 2, 'source_positions': [20, 21], 'S_pct_of_total': 6.802, 'R_pct_of_to |
| 10 | `get_source_influence` | {'source_positions': [9], 'depth': 2} → {'depth': 2, 'source_positions': [9], 'S_pct_of_total': 2.883, 'R_pct_of_total': |
| 11 | `get_source_influence` | {'source_positions': [1], 'depth': 2} → {'depth': 2, 'source_positions': [1], 'S_pct_of_total': -0.767, 'R_pct_of_total' |

### Build

`build_circuit` → 9 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 25,437 | 2,724 | 71,698 | 0 | $0.1224 | — | — |
| **Total** | | **25,437** | **2,724** | **71,698** | **0** | **$0.1224** | | |

**Oracle wall-clock time:** 0m 44s