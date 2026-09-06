# Circuit Oracle Report
**Date:** 2026-07-28 07:22:43 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by genuine profession-indicating tokens ("nutrition", "sports", "spokesperson") and semantic concept features for diet/food and physical activity — not by spurious gender markers.

**Confidence:** 8

**Reasoning:** Tracing the top late-layer drivers (L14:F4197 food/eating and L14:F16195 physical activity/training) back through the circuit reveals the signal originates overwhelmingly from embedding nodes at position 7 (" nutrition") with direct_effect of 12.88 and 7.97 respectively, plus position 6 (" sports", direct_effect 3.42 into F16195) and position 18 (" spokesperson" via L0:F2268, direct_effect 23.5). The mid-layer L4 features F10494 (health/medicine/diet) and F13412 (diets/dietary health) fire exclusively on the " nutrition" token (direct_effects of 11.25 and 12.63), and L0:F5201 (a token-level "nutrition" detector, frac_nonzero=0.00026 — extremely specific) is driven by direct embedding contribution (27.13) from " nutrition" and " sports" tokens. L14:F16195 (physical activity) is additionally fed by L8:F7057 (exercise/biology, direct_effect 4.13) and L7:F13562 (athletes/conditioning, direct_effect 2.17), all of which also anchor on the " nutrition" embedding at pos 7.

Critically, the user's hypothesis of spurious gender-based prediction is **not supported by the circuit**. The "Her" embedding at position 1 does activate the pronoun-detection features L0:F9519 (she/her) and L0:F15322 (herself/itself), but these have **negative direct_effects** on the probe logit (F9519 contributes -1.22 to F16195, F15322 contributes -0.99 via various paths), and the she_pronoun node flows into the logit as a negative-direction suppressor. The actual positive contribution comes from the L0 layer where the period/punctuation detector F6051 at pos 14 has -0.0908 direct_effect to the logit (also slightly negative) — punctuation is a minor suppressor rather than driver. The dominant positive signal flows nutrition-token → diet concepts (L4) → food/nutrition concepts (L6-L7) → profession-relevant late-layer concepts (L14) → probe logit. This is a textbook content-based profession circuit, not a demographic-cue circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | She/her pronoun detector |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F15322](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) | 1 | She/her pronoun detector | reflexive pronouns, particularly "herself" and "itself." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) |
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 7 | Token-level 'nutrition' detector (L0) |  the word "nutrition" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L0:F2268](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2268) | 18 | 'spokesperson' speech-act detector (L0) |  mentions of people communicating information via speech | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2268) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 14 | Punctuation/period detector (L0) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 7 | Health/diet/diets mid-layer features (L4) |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | Health/diet/diets mid-layer features (L4) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 7 | Food/nutrition mid-layer (L6) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L7:F11540](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11540) | 7 | Food/nutrition mid-layer (L6) |  scientific discussion of vitamins and minerals | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11540) |
| [L3:F6920](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6920) | 7 | Food/nutrition mid-layer (L6) | words related to consuming food, nutrients, and specific diets | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6920) |
| [L7:F13562](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13562) | 7 | Physical training/athletes (L7) |  terms related to physical and mental training or conditioning | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13562) |
| [L8:F7057](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7057) | 7 | Physical training/athletes (L7) |  terms related to exercise, biology and chemistry | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7057) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 7 | Food/eating concepts (L14) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F16195](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) | 7 | Physical activity/training (L14) | mentions of physical activity and training. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:10494 de=0.176 |
| 3 | `inspect_feature` ×13 | L4:10494, L4:13412, L14:4197, L14:16195, L6:11327, L0:10148, L0:2083, L0:8975, L0:6051, L0:5201, L0:2268, L0:9519, L0:15322 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4197@7` | ❌ error | — | — | Trace upstream from L14:F4197 (food/food insecurity feature, fired on token pos … |
| SA-2 | `L14:F16195@7` | ❌ error | — | — | Trace upstream from L14:F16195 (physical activity/training feature, fired on tok… |
| SA-3 | `L4:F13412@7` | ❌ error | — | — | Trace upstream from L4:F13412 (diets/dietary health feature, fired on token pos … |
| SA-4 | `L4:F10494@7` | ❌ error | — | — | Trace upstream from L4:F10494 (health/medicine/diet feature, fired on token pos … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4197@7, k=15 → Emb:" nutrition"@7 (de=12.88) +14 more |
| 2 | `get_upstream_features` | L14:F16195@7, k=15 → Emb:" nutrition"@7 (de=7.97) +14 more |
| 3 | `get_upstream_features` | L4:F13412@7, k=15 → Emb:" nutrition"@7 (de=12.62) +14 more |
| 4 | `get_upstream_features` | L4:F10494@7, k=15 → Emb:" nutrition"@7 (de=11.25) +14 more |
| 5 | `get_upstream_features` | L6:F11327@7, k=10 → Emb:" nutrition"@7 (de=17.50) +9 more |
| 6 | `get_upstream_features` | L0:F9519@1, k=10 → Emb:"Her"@1 (de=16.75) +9 more |
| 7 | `get_upstream_features` | L0:F5201@7, k=10 → Emb:" nutrition"@7 (de=27.12) +9 more |
| 8 | `get_upstream_features` | L0:F6051@14, k=5 → Emb:"."@14 (de=47.00) +4 more |
| 9 | `get_upstream_features` | L0:F2268@18, k=5 → Emb:" spokesperson"@18 (de=23.50) +4 more |
| 10 | `inspect_feature` ×4 | L7:11540, L7:13562, L8:7057, L3:6920 |

### Build

`build_circuit` → 16 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 39,108 | 4,628 | 211,464 | 0 | $0.0300 | — | — |
| **Total** | | **39,108** | **4,628** | **211,464** | **0** | **$0.0300** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 14s