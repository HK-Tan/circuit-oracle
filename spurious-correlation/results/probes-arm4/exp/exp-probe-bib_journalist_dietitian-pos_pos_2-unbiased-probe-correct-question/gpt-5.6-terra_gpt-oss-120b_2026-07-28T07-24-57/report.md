# Circuit Oracle Report
**Date:** 2026-07-28 07:24:57 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven primarily by genuine nutrition/diet and cooking evidence—especially the explicit tokens *“nutrition”* and *“cook”*—rather than by the female pronoun *“She.”*

**Confidence:** 8/10

**Reasoning:** The saved circuit shows a coherent content-based route from `Emb: nutrition (pos 13)` through dietary and food-concept features into the synthetic profession-probe output.

- The strongest direct positive score drivers are:
  - **L6:F11327 at pos 13**: direct effect **+0.1406**, a selective food/nutrition detector (`frac_nonzero=0.01166`) promoting *food, foods, eating, meals*. Its upstream attribution is dominated by the raw embedding of **“ nutrition”** (**+21**), with support from dietary feature L4:F13412.
  - **L14:F4197 at pos 13**: **+0.1367**, a food-related context feature (`frac_nonzero=0.0152`) promoting *food/foods*. Although its autointerp headline calls it “food insecurity,” its activating cases and promoted tokens show a broader food/meal semantic direction. It receives strong positive signal from **“nutrition”** (**+14.31**) and from L6:F11327 (**+5.84**).
  - **L4:F13412 at pos 13**: **+0.1338**, a diet/dietary-health feature (`frac_nonzero=0.01216`) promoting *diet, diets, dieting*. It is again driven mostly by **“nutrition”** (**+14.06**).
  - **L19:F1589 at pos 13**: **+0.0840**, a nutritional-science context feature (`frac_nonzero=0.03796`) promoting *diet, food, nutrition, dietary, meals*. Its upstream input includes **“nutrition”** with the largest positive effect (**+31.25**), plus the earlier food/diet pathway: L14:F4197 (**+8.69**), L6:F11327 (**+6.09**), and L4:F13412 (**+2.72**).

- A separate, genuinely relevant cooking route supports the classification:
  - `Emb: cook (pos 17)` excites **L15:F2510** by **+28.88**. This feature is a selective cooking/food-preparation detector (`frac_nonzero=0.00865`) promoting *cook, cooks, cooking, kitchen* and directly raises the probe score by **+0.0649**.
  - Thus, the input’s description of teaching nutrition and cooking healthy meals supplies two semantically aligned sources of occupation evidence.

- The source-influence calculation corroborates this. Position 13 (*nutrition*) carries **+5.196% of total net signed influence**, the largest measured source and the reference maximum; position 17 (*cook*) supplies another **+3.45%**. These are substantial, positive, content-aligned contributions.

**Gender-marker concern:** There is a detectable female-pronoun representation, **L1:F7244 at pos 1**, explicitly labeled *“the pronoun ‘she’”* (`frac_nonzero=0.01185`), and it has a small positive direct effect on the probe (**+0.0535**). Its upstream source is indeed `Emb: She (pos 1)` (**+13.56**). However, this is not the main causal route:

1. The measured total influence from position 1 is **negative** (**−1.783%**), versus **+5.196%** for *nutrition* and **+3.45%** for *cook*.
2. The strongest positive score features are dietary/nutrition features, not gender features.
3. The circuit has a layered semantic progression—dietary-health recognition → food/nutrition concept → food-context aggregation → nutritional-science context—fed directly by the explicit occupation-relevant vocabulary.

So the probe may contain a **minor, locally positive gender-correlated feature**, but this graph does **not** support the claim that its classification is mainly a gender shortcut. The dominant mechanism is a broad nutrition/food/cooking semantic cluster. One limitation is that it identifies a nutrition-related profession domain rather than a uniquely entity-specific job title; it could therefore conflate nutrition professionals with other food-, diet-, or cooking-oriented roles.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Dietary-health recognition |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Dietary-health recognition |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Food/nutrition concept |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 13 | Food-context aggregation |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 13 | Nutritional-science context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L15:F2510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) | 17 | Cooking / food-preparation concept |  words and phrases related to food preparation and consumption, along with some words relating to the digestive system and eating disorders | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) |
| [L1:F7244](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) | 1 | Female-pronoun marker | the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11327 de=0.141 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11327@13` | ❌ error | — | — | Trace this major positive driver of the synthetic profession-probe score upstrea… |
| SA-2 | `L14:F4197@13` | ❌ error | — | — | Trace this major positive driver of the synthetic profession-probe score upstrea… |
| SA-3 | `L4:F13412@13` | ❌ error | — | — | Trace this major positive probe driver upstream to embeddings, emphasizing what … |
| SA-4 | `L19:F1589@13` | ❌ error | — | — | Trace this later positive score driver upstream to embeddings. Characterize the … |
| SA-5 | `L15:F2510@17` | ❌ error | — | — | Trace this positive feature at the 'nutrition' position upstream to embeddings. … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L6:11327, L14:4197, L4:13412, L19:1589, L15:2510 |
| 2 | `get_upstream_features` | L6:F11327@13, k=12 → Emb:" nutrition"@13 (de=21.00) +11 more |
| 3 | `get_upstream_features` | L14:F4197@13, k=12 → Emb:" nutrition"@13 (de=14.31) +11 more |
| 4 | `get_upstream_features` | L4:F13412@13, k=12 → Emb:" nutrition"@13 (de=14.06) +11 more |
| 5 | `get_upstream_features` | L19:F1589@13, k=12 → Emb:" nutrition"@13 (de=31.25) +11 more |
| 6 | `get_upstream_features` | L15:F2510@17, k=12 → Emb:" cook"@17 (de=28.88) +11 more |
| 7 | `inspect_feature` ×6 | L1:7244, L0:14824, L0:2349, L0:2238, L0:6051, L4:9554 |
| 8 | `get_source_influence` | {'source_positions': [13], 'depth': 2} → {'depth': 2, 'source_positions': [13], 'S_pct_of_total': 5.196, 'R_pct_of_total' |
| 9 | `get_source_influence` | {'source_positions': [1], 'depth': 2} → {'depth': 2, 'source_positions': [1], 'S_pct_of_total': -1.783, 'R_pct_of_total' |
| 10 | `get_source_influence` | {'source_positions': [17], 'depth': 2} → {'depth': 2, 'source_positions': [17], 'S_pct_of_total': 3.45, 'R_pct_of_total': |
| 11 | `get_upstream_features` | L1:F7244@1, k=12 → Emb:"She"@1 (de=13.56) +11 more |

### Build

`build_circuit` → 10 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 23,279 | 2,698 | 61,354 | 0 | $0.1140 | — | — |
| **Total** | | **23,279** | **2,698** | **61,354** | **0** | **$0.1140** | | |

**Oracle wall-clock time:** 0m 37s