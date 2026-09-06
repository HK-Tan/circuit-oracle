# Circuit Oracle Report
**Date:** 2026-07-28 07:21:27 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a coherent nutrition/food-content circuit, not by gender markers; the female-pronoun features have a *negative* direct effect on the probe, while food/nutrition vocabulary features have a large *positive* effect.

**Confidence:** 8

**Reasoning:** The user's concern is that the probe might rely on spurious gender features. The circuit refutes this. At the final layer the largest positive direct-effect features are content-driven: L19:F1589 ("nutritional/scientific studies context", direct_effect +0.084) and L15:F2510 ("food preparation/consumption, kitchen/cook", +0.065). At L14, F4197 ("food / food-insecurity vocabulary", +0.137) and at L6, F11327 ("food or nutrition phrases", +0.141) are the top positive drivers. All four of these features have *promoted tokens* like `▁food`, `▁nutrition`, `▁diet`, `▁cooking`, `▁kitchen`, `▁meal` — they encode the topic of nutrition, not gender. The "she/her" features behave oppositely: L0:F9519 (she/her pronoun, pos 1) and L0:F14824 (the word "has", pos 2) carry *negative* direct effects (−0.056 and −0.098) on the probe, and the more abstract L6:F11646 (female-pronoun feature at pos 1) also inhibits the probe (−0.064). The hierarchy bottoms out cleanly in token embeddings — `▁nutrition` at pos 13 is the single largest upstream source for every food feature, with direct_effects of 21 → L6:F11327, 14.3 → L14:F4197, and 31.25 → L19:F1589. `▁cook` at pos 17 (28.9) drives L15:F2510. The pronoun `She` at pos 1 (15.75) drives the she/her feature but that branch runs *inhibitory* into the probe. So the signal flow is: token embeddings (`▁nutrition`, `▁cook`, `▁diet`) → low-layer food/diet features (L4:F13412, F9554, F10494) → L6 food-feature (F11327) → L14 food-feature (F4197) → L19 nutrition-studies feature (F1589) → probe logit. The user's hypothesis of gender-based spurious correlation is not supported by this graph; the probe picks up on the genuine profession-indicating topic vocabulary, and the female-pronoun signal actually pushes *against* the predicted class.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 13 | Late-layer: nutritional/scientific studies context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 28 | Late-layer: nutritional/scientific studies context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L15:F2510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) | 17 | Mid-layer: food preparation/cooking vocabulary |  words and phrases related to food preparation and consumption, along with some words relating to the digestive system and eating disorders | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 13 | Mid-layer: food / food-insecurity vocabulary |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Low-mid layer: food/nutrition word feature |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 28 | Low-mid layer: food/nutrition word feature |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Low layer: female pronoun / she-her feature | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Low layer: dietary-health / pattern vocabulary |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 28 | Low layer: dietary-health / pattern vocabulary |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 13 | Low layer: dietary-health / pattern vocabulary | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Low layer: dietary-health / pattern vocabulary | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L1:F728](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/728) | 8 | Low layer: word 'learn' (educational verb) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/728) |
| [L1:F815](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/815) | 4 | Low layer: word 'passion' | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/815) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | Embedding layer: she / her pronoun feature |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L1:F7244](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) | 1 | Embedding layer: she / her pronoun feature | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 2 | Embedding layer: 'has' token feature | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 7 | Embedding layer: 'others' token feature |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 9 | Embedding layer: 'about' token feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 16 | Embedding layer: 'to' token feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 22 | Embedding layer: '.' punctuation feature | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token ' Base' is not one of the top-k next-token candidates  |
| 3 | `get_top_features` | 20 features; top: L6:11327 de=0.141 |
| 4 | `inspect_feature` ×8 | L6:11327, L14:4197, L4:13412, L19:1589, L15:2510, L0:14824, L0:2349, L0:9519 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11327@13` | ❌ error | — | — | Trace the food/nutrition feature at L6:F11327 upstream. What tokens in the input… |
| SA-2 | `L14:F4197@13` | ❌ error | — | — | Trace the food-related feature at L14:F4197 upstream. What tokens in the input d… |
| SA-3 | `L19:F1589@13` | ❌ error | — | — | Trace the nutritional/scientific studies feature at L19:F1589 upstream. Is this … |
| SA-4 | `L4:F13412@13` | ❌ error | — | — | Trace the diet/nutrition feature at L4:F13412 upstream. What input tokens trigge… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11327@13, k=15 → Emb:" nutrition"@13 (de=21.00) +14 more |
| 2 | `get_upstream_features` | L14:F4197@13, k=15 → Emb:" nutrition"@13 (de=14.31) +14 more |
| 3 | `get_upstream_features` | L19:F1589@13, k=15 → Emb:" nutrition"@13 (de=31.25) +14 more |
| 4 | `get_upstream_features` | L4:F13412@13, k=15 → Emb:" nutrition"@13 (de=14.06) +14 more |
| 5 | `get_upstream_features` | L0:F9519@1, k=10 → Emb:"She"@1 (de=15.75) +9 more |
| 6 | `get_upstream_features` | L0:F14824@2, k=10 → Emb:" has"@2 (de=32.75) +9 more |
| 7 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 8 | `get_upstream_features` | L15:F2510@17, k=12 → Emb:" cook"@17 (de=28.88) +11 more |
| 9 | `get_upstream_features` | L0:F2238@9, k=10 → Emb:" about"@9 (de=34.25) +9 more |
| 10 | `get_upstream_features` | L0:F8444@16, k=10 → Emb:" to"@16 (de=40.50) +9 more |
| 11 | `get_upstream_features` | L0:F6051@22, k=10 → Emb:"."@22 (de=47.00) +9 more |
| 12 | `get_upstream_features` | L0:F2349@7, k=10 → Emb:" others"@7 (de=41.25) +9 more |
| 13 | `get_upstream_features` | L1:F728@8, k=10 → Emb:" learn"@8 (de=21.50) +9 more |
| 14 | `get_upstream_features` | L1:F815@4, k=10 → Emb:" passion"@4 (de=26.38) +9 more |
| 15 | `get_upstream_features` | L1:F7244@1, k=10 → Emb:"She"@1 (de=13.56) +9 more |
| 16 | `get_upstream_features` | L4:F10494@13, k=10 → Emb:" nutrition"@13 (de=13.12) +9 more |
| 17 | `get_upstream_features` | L4:F9554@13, k=10 → Emb:" nutrition"@13 (de=15.88) +9 more |

### Build

`build_circuit` → 26 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 28,624 | 5,621 | 146,051 | 0 | $0.0241 | — | — |
| **Total** | | **28,624** | **5,621** | **146,051** | **0** | **$0.0241** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 20s