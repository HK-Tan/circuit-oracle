# Circuit Oracle Report
**Date:** 2026-07-28 07:24:54 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s positive profession score is driven chiefly by genuine nutrition/dietetics and sports-training evidence—especially the tokens **“nutrition”** and **“sports”**—rather than by the gender marker **“Her.”**

**Confidence:** 8/10

**Reasoning:** The synthetic output label is the probe direction, not a next-token prediction. Its strongest positive direct drivers are low/mid-layer semantic features centered at position 7, the token **“ nutrition”**:

- **Health/diet lexical detectors**:  
  - L4:F10494 at pos 7, direct effect **+0.1758**, is a selective health/medicine/diet/exercise feature (fraction nonzero **0.01174**).  
  - L4:F13412 at pos 7, 13, and 26, with the strongest instance **+0.1416** at pos 7, detects diet and dietary-health terminology (fraction nonzero **0.01216**; promoted tokens include **“diet,” “diets,” “dieting”**).  
  These are not generic gender features: their activating examples and promoted tokens consistently concern diet, health professionals, eating patterns, and dietary needs.

- **Food/nutrition concept detector**: L6:F11327 at pos 7 contributes **+0.0820** directly to the probe and detects food/nutrition language (fraction nonzero **0.01166**; promoted tokens include **“food,” “foods,” “eating,” “meals”**). It receives positive signal from L4:F13412 (**+2.3125** upstream effect), forming a coherent diet/nutrition pathway.

- **Late food-related detector**: L14:F4197 at pos 7 contributes **+0.1006**. Although its automated label is “food insecurity,” its actual decoder preferences are broadly food-related—**food, foods, edible, foodstuffs**—and it is strongly driven by the literal embedding **“ nutrition”** (**+12.875**) plus the nutrition detector L6:F11327 (**+3.4062**) and L4:F13412 (**+1.2578**). Thus, in this context it is best interpreted as a broad food/nutrition semantic feature, not evidence of food insecurity.

- **Late activity/training detector**: L14:F16195 at pos 7 contributes **+0.0854** and represents physical activity/training (fraction nonzero **0.01514**; promoted tokens include **“muscle,” “muscles,” “gyms,” “muscular”**). It receives strong positive evidence from **“ nutrition”** (**+7.9688**) and **“ sports”** (**+3.4219**), and also from the earlier health/diet features L4:F10494 (**+1.2891**) and L4:F13412 (**+1.1562**). This is an appropriate conjunction for *sports nutrition*, rather than a demographic shortcut.

The recorded circuit is therefore:

`Emb: nutrition (pos 7)` and `Emb: sports (pos 6)` → **Health/diet lexical detectors** (L4:F10494; L4:F13412) → **Food/nutrition concept detector** (L6:F11327) → **Late food-related detector** (L14:F4197) and, jointly with sports, → **Late activity/training detector** (L14:F16195) → **Output: synthetic profession-probe score**.

There is a small upstream connection from the embedding **“Her”** to L4:F13412 (**+0.4902**), but it is tiny relative to the direct **“nutrition”** evidence into the same feature (**+12.625**) and does not form a positive gender-based branch into the final circuit. In fact, **“Her”** is *negative* for the activity feature L14:F16195 (**−1.2188**). The evidence therefore does **not** support the concern that this classification is primarily driven by gender. It is mainly a lexical-semantic shortcut based on explicit nutrition/diet and sports/exercise cues—which is profession-relevant here, though still more topic detection than a robust representation of occupational role.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 7 | Health/diet lexical detectors |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | Health/diet lexical detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Health/diet lexical detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 26 | Health/diet lexical detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 7 | Food/nutrition concept detector |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 7 | Late food-related detector |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F16195](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) | 7 | Late activity/training detector | mentions of physical activity and training. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:10494 de=0.176 |
| 3 | `inspect_feature` ×5 | L4:10494, L4:13412, L14:4197, L14:16195, L6:11327 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F10494@7` | ❌ error | — | — | Trace this strong positive driver of the synthetic profession-probe score to emb… |
| SA-2 | `L4:F13412@7` | ❌ error | — | — | Trace this strong positive driver, including its occurrences at positions 7, 13,… |
| SA-3 | `L14:F4197@7` | ❌ error | — | — | Trace this late positive probe driver upstream to embeddings, identify its seman… |
| SA-4 | `L14:F16195@7` | ❌ error | — | — | Trace this late positive probe driver upstream to embeddings, identify evidence … |
| SA-5 | `L6:F11327@7` | ❌ error | — | — | Trace this positive driver upstream to embeddings. Characterize whether it is pr… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F10494@7, k=12 → Emb:" nutrition"@7 (de=11.25) +11 more |
| 2 | `get_upstream_features` | L4:F13412@7, k=12 → Emb:" nutrition"@7 (de=12.62) +11 more |
| 3 | `get_upstream_features` | L14:F4197@7, k=12 → Emb:" nutrition"@7 (de=12.88) +11 more |
| 4 | `get_upstream_features` | L14:F16195@7, k=12 → Emb:" nutrition"@7 (de=7.97) +11 more |
| 5 | `get_upstream_features` | L6:F11327@7, k=12 → Emb:" nutrition"@7 (de=17.50) +11 more |

### Build

`build_circuit` → 7 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 12,584 | 2,367 | 44,312 | 0 | $0.0780 | — | — |
| **Total** | | **12,584** | **2,367** | **44,312** | **0** | **$0.0780** | | |

**Oracle wall-clock time:** 0m 38s