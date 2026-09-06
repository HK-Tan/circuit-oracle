# Circuit Oracle Report
**Date:** 2026-07-28 07:24:52 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven principally by genuine nutrition/dietetics evidence—especially *eat*, *Nutrition*, and *Dietetics*—with a smaller generic “clients” professional-context cue, not by gender markers.

**Confidence:** 9/10

**Reasoning:** The saved circuit identifies two positive routes into the **Output: profession-classification probe score** rather than a next-token logit.

1. **Direct client-professional-context route.**  
   **Emb: clients (pos 5)** excites L6:6115 at that position (upstream direct effect **+25.63**). L6:6115 is a relatively selective feature (frac_nonzero **0.02267**) whose activating examples consistently contain “clients”; its promoted tokens are *clients, Clients, clientele, customers*. It contributes **+0.1279** directly to the probe. This is generic evidence that the author has a client-facing professional role, but it does not identify nutrition specifically. Crucially, it is neither a gender feature nor driven primarily by “She,” “her,” or the name Sarah.

2. **Food/eating-to-nutrition route.**  
   **Emb: eat (pos 9)** is a major source. It directly excites L6:11327 by **+22.13** and L14:4197 by **+17.88**:
   - L4:1626 is a selective food-consumption detector (frac_nonzero **0.00455**), promotes *eat/eating/eaten*, and feeds the food/eating representation.
   - L6:11327 (frac_nonzero **0.01166**) represents food/nutrition language, promotes *foods, food, eating, meals*, and has a direct probe effect of **+0.1187** at position 9.
   - L14:4197 (frac_nonzero **0.0152**) is broadly food-related (headline label “food insecurity,” but its actual examples and promoted tokens show a food/meal/eating detector). It has direct probe effect **+0.1221** at pos 9. Thus its interpretation should not be over-specialized to food insecurity.

3. **Explicit nutrition/dietetics route—the dominant profession-specific mechanism.**  
   The final integrator is L19:1589 at the “Dietetics” position (pos 23), which contributes **+0.1089** directly to the probe (and **+0.0874**, **+0.0801** at nearby occurrences). This feature is semantically well aligned with nutrition science: it is selective (frac_nonzero **0.03796**), its top examples contain *nutrition, nutritional,* and *dietary*, and it promotes *diet, food, nutrition, dietary,* and *meals*.

   Its strongest positive inputs are:
   - L4:13412 at pos 23 (**+10.38**): a diet/dietary-health feature, frac_nonzero **0.01216**, with *diet* among promoted tokens and activating examples containing *dieticians*, *diet*, and healthy eating patterns.
   - **Emb: Die (pos 22)**, the first subtoken of “Dietetics” (**+8.69**).
   - **Emb: Nutrition (pos 20)** (**+8.19**).
   - L6:11327 at pos 23 (**+5.97**) and L14:4197 at pos 23 (**+4.44**).
   - L17:7545 at pos 23 (**+9.94**), a sparse feature (frac_nonzero **0.00449**) that includes healthcare/nurse contexts. This is a secondary generic health-profession cue, not the central evidence.

   L4:13412 itself is directly grounded in **Nutrition** (**+4.16**) and **Die** (**+4.22**), alongside early contextual features. This supports a clean lexical-semantic path from the explicit credential phrase “Academy of Nutrition and Dietetics” into the probe.

Overall, the probe’s classification is primarily supported by coherent, profession-relevant content: food/nutrition language, healthy eating, and the explicit institutional/disciplinary phrase **“Academy of Nutrition and Dietetics.”** The probe does use a generic client-facing cue from *clients*, and a weaker healthcare-associated cue from L17:7545, so it is not exclusively credential-based. But the attribution evidence does **not** support the concern that gender markers are the primary mechanism: “her” is only a tiny upstream contributor to L6:6115 (**+0.93**) and “She” does not appear among the important positive circuit sources.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F6115](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) | 5 | Client-facing professional-context detector |  words related to commercial activity and customers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) |
| [L4:F1626](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1626) | 9 | Food/eating semantic detectors |  phrases that occur in the context of food consumption. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1626) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 9 | Food/eating semantic detectors |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | Food/eating semantic detectors |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 23 | Nutrition/dietetics terms and nutritional-study context |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 23 | Nutrition/dietetics terms and nutritional-study context |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 23 | Nutrition/dietetics terms and nutritional-study context |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 23 | Nutrition/dietetics terms and nutritional-study context | mentions of architecture, design, nurses and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 23 | Nutrition/dietetics terms and nutritional-study context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:6115 de=0.128 |
| 3 | `inspect_feature` ×5 | L6:6115, L4:13412, L14:4197, L6:11327, L19:1589 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@23` | ❌ error | — | — | Trace this strongly probe-positive path upstream to embeddings. Determine whethe… |
| SA-2 | `L14:F4197@9` | ❌ error | — | — | Trace this strongly probe-positive path upstream to embeddings. Assess professio… |
| SA-3 | `L6:F6115@5` | ❌ error | — | — | Trace this early strongly probe-positive path upstream to embeddings. Identify e… |
| SA-4 | `L4:F13412@23` | ❌ error | — | — | Trace this repeated strongly probe-positive feature upstream to embeddings. Dete… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F1589@23, k=15 → L4:F13412 (de=10.38) +14 more |
| 2 | `get_upstream_features` | L14:F4197@9, k=15 → Emb:" eat"@9 (de=17.88) +14 more |
| 3 | `get_upstream_features` | L6:F6115@5, k=15 → Emb:" clients"@5 (de=25.62) +14 more |
| 4 | `get_upstream_features` | L4:F13412@23, k=15 → L3:F11774 (de=4.72) +14 more |
| 5 | `get_upstream_features` | L6:F11327@9, k=15 → Emb:" eat"@9 (de=22.12) +14 more |
| 6 | `inspect_feature` ×5 | L17:7545, L3:11774, L3:10028, L4:1626, L4:9554 |

### Build

`build_circuit` → 8 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 19,938 | 2,383 | 66,007 | 0 | $0.1021 | — | — |
| **Total** | | **19,938** | **2,383** | **66,007** | **0** | **$0.1021** | | |

**Oracle wall-clock time:** 0m 36s