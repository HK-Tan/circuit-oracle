# Circuit Oracle Report
**Date:** 2026-07-28 07:22:37 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a two-track circuit: a genuine-content track built from nutrition/diet/exercise expertise features (L2 "healthy", L4 "exercise and physical activity", L4 "diets and dietary health", L6 "food/nutrition", L14 "food insecurity") composed from tokens like "healthy", "food", "lifestyle", "physically active", "dieting", and a spurious gender track that uses the pronoun "She" (L0:F9519 direct_effect −0.065, L1:F7244 direct_effect +0.056) plus a cluster of generic word-identity features (F2349 "others", F2845 "knowledge", F5829 "easier", F2238 "about", F11814 "slightly", F4030 "mission/personal development", F8566 "pick") drawn from the introductory sentence.

**Confidence:** 8

**Reasoning:** The gender/spurious cluster is suspicious in three ways. First, two dedicated "she/her" pronoun features (L0:F9519 frac_nonzero 0.0112 and L1:F7244 frac_nonzero 0.0119) appear in the top 20 with opposite signs — F9519 suppresses the score (direct_effect −0.065) while F7244 raises it (+0.056), so the model is *explicitly* using feminine-pronoun information as a feature, not as a side effect. Second, the surrounding "early_gender_softener" supernode is overwhelmingly composed of bare word-identity detectors for the sentence "She is passionate about empowering others with the knowledge and confidence to make healthy food…" — "others" (F2349, direct_effect −0.062), "knowledge" (F2845, +0.054), "easier" (F5829, −0.059), "about" (F2238, +0.053), "slightly" (F11814, +0.057), "pick" (F8566, −0.062), "passionate"/"mission" (F4030, +0.078) — which are context-free lexical lookups, not profession indicators. These features carry non-trivial mass (each |direct_effect| ≈ 0.05–0.08) and together rival the genuine profession-content features in total weight. Third, the genuine profession content is real but narrower: L2:F6341 "healthy" (frac_nonzero 0.0039, embedded at pos 14), L4:F3047 "exercise/physical activity" (frac_nonzero 0.0067, pos 22), L4:F13412 "diets and dietary health" (frac_nonzero 0.0122, pos 34), L0:F10218 "lifestyle" (frac_nonzero 0.0167, pos 17), L6:F11327 "food/nutrition" (frac_nonzero 0.0117), L14:F4197 "food insecurity" (frac_nonzero 0.0152) — all confirmed to be specific (low frac_nonzero) domain-of-expertise features, with traced embeddings from "healthy", "food", "lifestyle", "physically", "active", "dieting" as their source. The user is correct: the probe classification is partially driven by spurious surface features (the opening "She" pronoun and surrounding generic word detectors) alongside genuine profession-content features, so the probe is not purely profession-driven.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) — feminine pronoun (gender marker) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: passionate (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: about (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: others (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: knowledge (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: confidence (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: healthy (pos 14) — profession-related content token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: food (pos 15) — profession-related content token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: lifestyle (pos 17) — profession-related content token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: physically (pos 21) — profession-related content token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: active (pos 22) — profession-related content token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 34 | Emb: dieting (pos 34) — profession-related content token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 32 | Emb: believe (pos 32) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | Early-layer feminine-gender & interpersonal tokens (L0–L1) — gender marker, NOT profession content |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L1:F7244](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) | 1 | Early-layer feminine-gender & interpersonal tokens (L0–L1) — gender marker, NOT profession content | the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 6 | Early-layer feminine-gender & interpersonal tokens (L0–L1) — gender marker, NOT profession content |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L0:F2845](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) | 9 | Early-layer feminine-gender & interpersonal tokens (L0–L1) — gender marker, NOT profession content |  the word "knowledge" and words starting with the letter "A" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) |
| [L0:F5829](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5829) | 3 | Early-layer feminine-gender & interpersonal tokens (L0–L1) — gender marker, NOT profession content |  the word "easier" with some modifiers such as "max" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5829) |
| [L0:F11814](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11814) | 11 | Early-layer feminine-gender & interpersonal tokens (L0–L1) — gender marker, NOT profession content | the word "slightly" and, to a lesser extent, "reflected." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11814) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | Early-layer feminine-gender & interpersonal tokens (L0–L1) — gender marker, NOT profession content |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F4030](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) | 3 | Early-layer feminine-gender & interpersonal tokens (L0–L1) — gender marker, NOT profession content |  words related to mission statements and personal development used in career environments | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) |
| [L2:F6341](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6341) | 14 | Mid-layer profession-content features (L2–L4) — nutrition/exercise/diet expertise signals |  the word "healthy" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6341) |
| [L4:F3047](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) | 22 | Mid-layer profession-content features (L2–L4) — nutrition/exercise/diet expertise signals |  words or phrases related to exercise and physical activity | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 34 | Mid-layer profession-content features (L2–L4) — nutrition/exercise/diet expertise signals |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L0:F10218](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) | 17 | Mid-layer profession-content features (L2–L4) — nutrition/exercise/diet expertise signals |  the word "lifestyle." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | Late-layer nutrition-specialist feature (L6) — food/nutrition domain |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 15 | Late-layer food-insecurity / nutrition feature (L14) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2349 de=-0.123 |
| 3 | `inspect_feature` ×19 | L6:11327, L4:3047, L0:4030, L14:4197, L0:2349, L0:11646, L0:9519, L0:8566, L0:5829, L0:11814, L0:10218, L0:2845, L0:2238, L1:7244, L4:13412, L0:6051, L0:8444, L2:6341, L0:9927 |
| 4 | `get_upstream_features` | Emb:" food"@15 (de=34.00) +9 more |
| 5 | `get_upstream_features` | Emb:" food"@15 (de=22.62) +9 more |
| 6 | `get_upstream_features` | Emb:" active"@22 (de=10.25) +9 more |
| 7 | `get_upstream_features` | Emb:" dieting"@34 (de=18.25) +9 more |
| 8 | `get_upstream_features` | Emb:" healthy"@14 (de=29.25) +9 more |
| 9 | `get_upstream_features` | Emb:"She"@1 (de=15.75) +9 more |
| 10 | `get_upstream_features` | Emb:" lifestyle"@17 (de=25.00) +9 more |
| 11 | `get_upstream_features` | Emb:" passionate"@3 (de=6.31) +9 more |
| 12 | `get_upstream_features` | ❌ Feature (layer=0, pos=1, feature_idx=11646) not found in gra |
| 13 | `get_upstream_features` | Emb:" others"@6 (de=41.00) +9 more |
| 14 | `get_upstream_features` | Emb:" knowledge"@9 (de=17.00) +4 more |
| 15 | `get_upstream_features` | Emb:" about"@4 (de=34.50) +4 more |
| 16 | `get_upstream_features` | Emb:" passionate"@3 (de=15.00) +4 more |
| 17 | `get_upstream_features` | Emb:"She"@1 (de=13.56) +4 more |
| 18 | `get_upstream_features` | Emb:" confidence"@11 (de=13.81) +4 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4197@15` | ❌ error | — | — | Trace the food-related path. This feature is "words and phrases related to food … |
| SA-2 | `L4:F13412@34` | ❌ error | — | — | Trace the diet-related path. This feature is "terms related to diets and dietary… |
| SA-3 | `L4:F3047@22` | ❌ error | — | — | Trace the exercise/physical-activity path. This feature is "words or phrases rel… |

### Build

`build_circuit` → 18 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,046 | 5,714 | 240,648 | 0 | $0.0366 | — | — |
| **Total** | | **51,046** | **5,714** | **240,648** | **0** | **$0.0366** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 13s