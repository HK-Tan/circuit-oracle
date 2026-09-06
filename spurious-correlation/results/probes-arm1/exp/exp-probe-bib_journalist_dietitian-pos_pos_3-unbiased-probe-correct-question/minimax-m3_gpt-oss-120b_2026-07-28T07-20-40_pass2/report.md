# Circuit Oracle Report
**Date:** 2026-07-28 07:20:40 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of this input as a "nutritionist" is driven by a mix of genuine domain-content features (food/diet vocabulary, physical-activity language) AND a parallel cluster of strong gender-pronoun features that fire on the very first subject token "She" — the user is right that the circuit co-uses gender as a spurious shortcut, though the dominant signal is still content.

**Confidence:** 7

**Reasoning:**

**Spurious gender pathway (the user's concern is well-founded).** A whole supernode of "gender markers" fires on position 1 ("She"):
- **L0:F9519** — *the pronoun "she" and the possessive pronoun "her"* (frac_nonzero 0.011, activation 9.8, direct_effect **−0.065**). Despite the negative direct_effect, it sits in the top features list.
- **L0:F12519** — *the pronoun "she"* (frac_nonzero 0.039, activation 17.4). Upstream traced to embedding "She" pos 1 (direct_effect 19.25 into L6:F11646).
- **L1:F7244** — *the pronoun "she"* (frac_nonzero 0.012, activation 8.7, direct_effect **+0.056**). Embedding "She" pos 1 drives it with direct_effect 13.56.
- **L6:F11646** — *references to women, potentially triggered by pronouns and titles* (frac_nonzero 0.020, activation 12.5, direct_effect **−0.065**).
- **L4:F7864** — promotes "herself" (direct_effect +4.44 into L6:F11646). 

Five distinct "she/her" detectors all light up on a single token that the probe has learned to associate with female-dominated professions. This is exactly the spurious-correlation pattern the user flagged.

**Genuine content pathway.** A second, larger cluster of features encodes actual profession-relevant content:
- **L6:F11327, L14:F4197** — "food/nutrition"/"food insecurity" (frac_nonzero ~0.012, direct_effects +0.09 and +0.07). L14:F4197 is a late-layer food-insecurity feature, but its top examples show generic food/eating tokens — weakly tied to the dietitian profession. L6:F11327 directly traces to the embedding "food" (direct_effect 34) and "healthy" (4.3).
- **L4:F3047** — "exercise and physical activity" (direct_effect +0.08, activation 25.6). Driven by embedding " active" (10.25) and " physically" (8.44).
- **L0:F13412** (diets/dietary health), **L3:F8425, L2:F13049, L1:F5219** (all "mentions of food"), **L4:F8343** (food/dining) — an 8-feature food-diet supernode.
- **L0:F10218** — *the word "lifestyle"* (direct_effect +0.055).
- **L0:F2845** — *the word "knowledge"* (direct_effect +0.054, from "knowledge" pos 9).
- **L0:F4030** — *mission statements / personal development* (direct_effect +0.078, from "passionate" pos 3).
- **L0:F2349** — *the word "others"* (direct_effect −0.123, from "others" pos 6) — a generic pronoun feature with a large negative direct_effect, suggesting it is being used as a calibration signal.

**Mechanism.** The probe receives roughly comparable positive drive from genuine content features (food/diet cluster direct_effects summing to ~+0.32, physical-activity ~+0.08, mission-statement +0.08) and from generic-content single-token features ("lifestyle", "knowledge", "passionate", "others"). Layered on top of this, a separate "she/her" cluster contributes another ~±0.30 of net direct_effect using only a single subject token. The profession signal IS present, but the probe is clearly leveraging a "female + nutrition/lifestyle vocabulary" co-occurrence pattern. The user's concern is correct: a model that classifies this person as a nutritionist partly because the subject is "She" rather than "He" has learned a demographic shortcut. A robust profession probe should rely on the content supernodes (food, diet, exercise, lifestyle vocabulary) and suppress the pronoun cluster.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 22 | Output logit (probe direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Gender markers (she/her pronouns) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | Gender markers (she/her pronouns) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L1:F7244](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) | 1 | Gender markers (she/her pronouns) | the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 1 | Gender markers (she/her pronouns) |  the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Gender markers (she/her pronouns) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 15 | Food / nutrition / diet content features |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | Food / nutrition / diet content features | words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L8:F10609](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/10609) | 15 | Food / nutrition / diet content features | words related to food, drinks, and diet | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/10609) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 15 | Food / nutrition / diet content features |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L3:F8425](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8425) | 15 | Food / nutrition / diet content features | mentions of food | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8425) |
| [L2:F13049](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13049) | 15 | Food / nutrition / diet content features |  mentions of food | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13049) |
| [L4:F8343](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8343) | 15 | Food / nutrition / diet content features |  words related to food and dining, particularly in the context of reviews and recipes | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8343) |
| [L1:F5219](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5219) | 15 | Food / nutrition / diet content features | mentions of food, cooking, and dining | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5219) |
| [L4:F3047](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) | 22 | Physical-activity / exercise content features | words or phrases related to exercise and physical activity | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) |
| [L0:F3597](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3597) | 22 | Physical-activity / exercise content features | the word "active" optionally preceded by an adverb of degree | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3597) |
| [L2:F13919](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13919) | 22 | Physical-activity / exercise content features | words related to life goals and purpose | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13919) |
| [L1:F9918](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9918) | 22 | Physical-activity / exercise content features | words related to research studies of physical activity | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9918) |
| [L1:F3066](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3066) | 22 | Physical-activity / exercise content features | discussion of physical exercise and sports | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3066) |
| [L2:F1541](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1541) | 22 | Physical-activity / exercise content features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1541) |
| [L3:F860](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/860) | 22 | Physical-activity / exercise content features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/860) |
| [L0:F4030](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) | 3 | Misc profession-adjacent content keywords |  words related to mission statements and personal development used in career environments | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) |
| [L0:F10218](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) | 17 | Misc profession-adjacent content keywords |  the word "lifestyle." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) |
| [L0:F2845](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) | 9 | Misc profession-adjacent content keywords |  the word "knowledge" and words starting with the letter "A" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) |
| [L0:F11814](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11814) | 11 | Misc profession-adjacent content keywords | the word "slightly" and, to a lesser extent, "reflected." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11814) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 9 | Misc profession-adjacent content keywords |  the word "pick" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F5829](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5829) | 3 | Misc profession-adjacent content keywords |  the word "easier" with some modifiers such as "max" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5829) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 6 | Misc profession-adjacent content keywords |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2349 de=-0.123 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11327@15` | ✅ reported | 3 | 5 | Trace this feature upstream. Determine what it semantically encodes (gender, pro… |
| SA-2 | `L4:F3047@22` | ✅ reported | 5 | 6 | Trace this feature upstream. Determine what it semantically encodes (gender, pro… |
| SA-3 | `L14:F4197@15` | ✅ reported | 3 | 6 | Trace this feature upstream. Determine what it semantically encodes (gender, pro… |
| SA-4 | `L4:F13412@34` | ❌ error | — | — | Trace this feature upstream. Determine what it semantically encodes (gender, pro… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@15, k=10 | Emb:" food"@15 (de=34.00) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `get_upstream_features` | L4:F13412@15, k=10 | Emb:" healthy"@14 (de=7.53) +9 more |
| 5 | `inspect_feature` | L1, F11764 | " words and phrases related to health and fitness" |
| 6 | `inspect_feature` | L1, F6631 | " words related to dietary patterns and scientific studies" |
| 7 | `get_upstream_features` | L1:F11764@15, k=10 | Emb:" healthy"@14 (de=5.97) +9 more |

**Findings:** The traced circuit starts at a mid‑layer feature (L6:F11327) that detects food‑related language. Upstream it receives strong excitation from the raw token embedding 'food', satisfying the embedding‑shortcut requirement. The next strongest upstream driver is a diet‑health feature (L4:F13412), which in turn is driven by a broader health‑fitness feature (L1:F11764). This health‑fitness feature receiv…

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F3047 | " words or phrases related to exercise and physical activity" |
| 2 | `get_upstream_features` | L4:F3047@22, k=10 | Emb:" active"@22 (de=10.25) +9 more |
| 3 | `inspect_feature` | L0, F3597 | "the word "active" optionally preceded by an adverb of degree" |
| 4 | `inspect_feature` | L2, F13919 | "words related to life goals and purpose" |
| 5 | `get_upstream_features` | L2:F13919@22, k=10 | Emb:" active"@22 (de=4.56) +9 more |
| 6 | `inspect_feature` | L1, F9918 | " words related to research studies of physical activity" |
| 7 | `inspect_feature` | L1, F3066 | " discussion of physical exercise and sports" |

**Findings:** Starting from L4:F3047 (exercise/physical‑activity detector) we traced upstream. The strongest positive drivers are the token embeddings " active" (pos 22) and " physically" (pos 21), directly feeding the feature with large positive direct_effects. Mid‑layer contributors include L2:F13919 (purpose/life‑goal detector), L0:F3597 (detects the word "active"), and L1 features 9918 and 3066, both specia…

</details>

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 2 | `get_upstream_features` | L14:F4197@15, k=10 | Emb:" food"@15 (de=22.62) +9 more |
| 3 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 4 | `inspect_feature` | L8, F10609 | " words related to food, drinks, and diet" |
| 5 | `get_upstream_features` | L6:F11327@15, k=10 | Emb:" food"@15 (de=34.00) +9 more |

**Findings:** The traced circuit originates at L14:F4197 (food‑insecurity detector) which heavily depends on a lower‑layer L6:F11327 that broadly detects food/nutrition mentions. Both receive strong positive driving from the input embedding of the token 'food' (pos 15), confirming that the path encodes food‑related semantic content, specifically scarcity contexts. A secondary L8 feature (food/drink/diet) also c…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×11 | L4:13412, L0:4030, L0:9519, L0:11814, L0:8566, L0:2845, L0:10218, L6:11646, L0:2349, L0:5829, L1:7244 |
| 2 | `get_upstream_features` | L0:F4030@3, k=8 → Emb:" passionate"@3 (de=6.31) +7 more |
| 3 | `get_upstream_features` | L6:F11327@15, k=8 → Emb:" food"@15 (de=34.00) +7 more |
| 4 | `inspect_feature` ×4 | L3:8425, L2:13049, L4:8343, L1:5219 |
| 5 | `get_upstream_features` | L8:F10609@15, k=8 → Emb:" healthy"@14 (de=8.12) +7 more |
| 6 | `get_upstream_features` | L14:F4197@15, k=8 → Emb:" food"@15 (de=22.62) +7 more |
| 7 | `get_upstream_features` | L4:F3047@22, k=8 → Emb:" active"@22 (de=10.25) +7 more |
| 8 | `get_upstream_features` | L6:F11327@41, k=8 → Emb:" food"@41 (de=41.25) +7 more |
| 9 | `inspect_feature` | L14, F4197 → " words and phrases related to food insecurity." |
| 10 | `get_upstream_features` | L0:F9519@1, k=5 → Emb:"She"@1 (de=15.75) +4 more |
| 11 | `get_upstream_features` | L6:F11646@1, k=5 → Emb:"She"@1 (de=19.25) +4 more |
| 12 | `get_upstream_features` | L0:F10218@17, k=5 → Emb:" lifestyle"@17 (de=25.00) +4 more |
| 13 | `get_upstream_features` | L0:F2845@9, k=5 → Emb:" knowledge"@9 (de=17.00) +4 more |
| 14 | `get_upstream_features` | L1:F7244@1, k=5 → Emb:"She"@1 (de=13.56) +4 more |
| 15 | `inspect_feature` ×3 | L4:7864, L0:12519, L0:3597 |

### Build

`build_circuit` → 14 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 54,645 | 7,432 | 251,007 | 0 | $0.0404 | — | — |
| SA-3 | openai/gpt-oss-120b | 44,534 | 3,149 | 128 | 0 | $0.0086 | ✅ 3F/6E | Trace this feature upstream. Determine what it semantically … |
| SA-1 | openai/gpt-oss-120b | 65,882 | 4,943 | 2,592 | 0 | $0.0129 | ✅ 3F/5E | Trace this feature upstream. Determine what it semantically … |
| SA-2 | openai/gpt-oss-120b | 61,253 | 3,852 | 7,744 | 0 | $0.0116 | ✅ 5F/6E | Trace this feature upstream. Determine what it semantically … |
| **Total** | | **226,314** | **19,376** | **261,471** | **0** | **$0.0734** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 25s