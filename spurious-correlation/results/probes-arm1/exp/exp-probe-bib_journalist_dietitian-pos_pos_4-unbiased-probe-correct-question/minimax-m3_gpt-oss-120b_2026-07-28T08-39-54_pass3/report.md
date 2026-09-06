# Circuit Oracle Report
**Date:** 2026-07-28 08:39:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "dietitian" classification is driven by genuine nutrition/diet content tokens ("Nutritional" pos 9, "Dietetics" pos 20, "RD" pos 55, "nutrition" pos 50), flowing through a clean hierarchy of nutrition-terminology features — not by gender markers.

**Confidence:** 9

**Reasoning:** The user's concern about spurious gender features is **not supported** by this circuit. Tracing the top driver L19:F1589 ("nutritional/scientific study context," direct_effect=0.064) upstream reveals a coherent nutrition-terminology pipeline:

**Token-embedding inputs (pos 9, 20, 50, 55, 37, 21)** feed strongly into early-layer features. Key excitatory edges include "Nutritional" → L17:F14680 (direct_effect=26.1), "nutrition" → L19:F1589 (29.5), "RD" → L4:F13412 (11.3), and "Dietetics" → L3:F11774 → L4:F13412 (5.9). These embeddings are content-bearing profession terms.

**Early-layer features (L2–L4)** consolidate these into domain concepts: L2:F2589 (medical professional/specialty term, frac_nonzero=0.008), L3:F11774/F10028 (morphological patterns on nutrition words), and L4:F13412 ("diets and dietary health," frac_nonzero=0.012) — all highly sparse and content-specific.

**Mid-layer features (L6, L14, L17, L18)** abstract further: L6:F11327 (food/nutrition concept, frac_nonzero=0.012), L14:F4197 (food-related context, frac_nonzero=0.015), L17:F14680 (nutrition/food/diets, frac_nonzero=0.010), L18:F6105 (eating/health, frac_nonzero=0.007).

**L19:F1589** integrates all paths and directly drives the probe (direct_effect=0.064). It promotes diet/nutrition tokens, not gender terms.

**Crucially, gender-related features appear in the suppressive path, not the excitatory one:** L0:F9519 ("she/her" pronoun) has direct_effect=-0.121 (position 2) — actively *reducing* the probe score. L0:F14824 ("has") at pos 2 also inhibits (-0.121). The negative-direct-effect features (L0:F8974 "from", L0:F8061 "in", L0:F9519 "she/her") are off-target for the tone-down-suppressor methodology and represent background, not causal drivers.

The excitatory circuit is purely content-driven by profession-relevant nutrition terminology. The "She" pronoun at position 1 ("She has a Bachelor's degree...") does NOT drive the classification — it is actually a suppressor on this input.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: 'Dietetics' (pos 20) - 'Die' token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: 'Nutritional' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 55 | Emb: 'RD' (pos 55) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 50 | Emb: 'nutrition' (pos 50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: 'te' (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 37 | Emb: 'titian' pediatric (pos 37) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 21 | L3 morphological/pattern detectors |  what appears to be a smattering of strings related to scientific notation, live radio, and roman numerals | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 21 | L3 morphological/pattern detectors | words or short phrases that include "made of/from", and words ending with "ice", "ita", "ons", "ura", and "mor" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | L4 diet/food/nutrition term detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | L4 diet/food/nutrition term detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 37 | L4 diet/food/nutrition term detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 36 | L4 diet/food/nutrition term detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 64 | L4 diet/food/nutrition term detectors |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 21 | L4 diet/food/nutrition term detectors |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 64 | L4 diet/food/nutrition term detectors |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 21 | L6 food/nutrition concept detector |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 37 | L6 food/nutrition concept detector |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 37 | L2 medical professional/specialty detector |  words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 55 | L2 medical professional/specialty detector |  words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 21 | L14 food-related context |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | L14 food-related context |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 9 | L17 nutrition/food/diets concept | nutrition, food, and diets | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 50 | L17 nutrition/food/diets concept | nutrition, food, and diets | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 9 | L18 eating/health concept | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 50 | L18 eating/health concept | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 21 | L19 nutritional/scientific study context (top driver) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 9 | L19 nutritional/scientific study context (top driver) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 50 | L19 nutritional/scientific study context (top driver) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (dietitian/nutrition) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:13412 de=0.154 |
| 3 | `inspect_feature` ×4 | L4:13412, L0:14824, L6:11327, L19:1589 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@21` | ✅ reported | 6 | 8 | Trace from L19:F1589 ("nutritional studies context") upstream. This is the most … |
| SA-2 | `L6:F11327@21` | ✅ reported | 5 | 6 | Trace from L6:F11327 ("food or nutrition") upstream. What input tokens and earli… |
| SA-3 | `L4:F13412@21` | ✅ reported | 3 | 11 | Trace from L4:F13412 ("diets and dietary health") at pos 21 upstream. This featu… |
| SA-4 | `L14:F4197@21` | ❌ error | — | — | Trace from L14:F4197 at pos 21 upstream. What does this feature encode and what … |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@21, k=10 | L4:F13412 (de=10.69) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 5 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 6 | `get_upstream_features` | L6:F11327@21, k=10 | L4:F13412 (de=5.88) +9 more |
| 7 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 8 | `get_upstream_features` | L14:F4197@21, k=10 | L6:F11327 (de=7.72) +9 more |
| 9 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 10 | `inspect_feature` | L17, F7545 | "mentions of architecture, design, nurses and healthcare." |
| 11 | `get_upstream_features` | L3:F11774@21, k=10 | Emb:" Die"@20 (de=5.88) +9 more |
| 12 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 13 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |

**Findings:** The target L19:F1589 (nutritional‑studies context) is primarily driven by low‑layer diet‑related features. A positive embedding for the token "Die" (position 20) directly excites L4:F13412 (diet terms) and L6:F11327 (food terms). These lower‑third features strongly push the target (direct effects ~10.7 and ~8.4). Additional pathways from L14:F4197 (food‑insecurity), L4:F9554 (food‑rations), and a …

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@21, k=10 | L4:F13412 (de=5.88) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 5 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 6 | `get_upstream_features` | L3:F11774@21, k=10 | Emb:" Die"@20 (de=5.88) +9 more |
| 7 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 8 | `get_upstream_features` | L4:F9554@21, k=10 | L3:F11774 (de=3.03) +9 more |
| 9 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 10 | `inspect_feature` | L1, F1083 | " the characters "te" within code and/or non-English words" |
| 11 | `inspect_feature` | L2, F1984 | " strings of letters that appear to be fragments of names, especially p" |

**Findings:** The nutrition detector (L6:F11327) receives its strongest excitatory drive from two mid‑layer diet features (L4:F13412 and L4:F9554). Both of these are fed by a lower‑layer feature L3:F11774, which is itself strongly activated by the input token " Die" at position 20 (positive direct effect >5). Additional reinforcement comes from L3:F10028, which reacts to suffixes common in food words and is dri…

</details>

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 3 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 4 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 5 | `get_upstream_features` | L3:F11774@21, k=10 | Emb:" Die"@20 (de=5.88) +9 more |

**Findings:** The diet‑related feature (L4:F13412) is driven primarily by raw input tokens. The strongest excitatory upstream nodes are the embedding for the token " Die" (pos 20) and the embedding for "te" (pos 21), both feeding positively into the diet feature via large direct_effect values. Mid‑level pattern features (L3:F11774, L3:F10028) also contribute, detecting numeric‑style strings and suffixes common …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L14:4197, L2:2589, L4:10494, L0:8974, L0:9519, L0:9888, L0:8061 |
| 2 | `get_upstream_features` | L19:F1589@9, k=15 → Emb:" Nutritional"@9 (de=26.12) +14 more |
| 3 | `get_upstream_features` | L19:F1589@50, k=10 → Emb:" nutrition"@50 (de=29.50) +9 more |
| 4 | `get_upstream_features` | L4:F13412@55, k=10 → Emb:" RD"@55 (de=11.31) +9 more |
| 5 | `inspect_feature` ×5 | L17:14680, L18:6105, L4:9554, L3:11774, L3:10028 |

### Build

`build_circuit` → 15 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 61,842 | 10,837 | 177,838 | 0 | $0.0422 | — | — |
| SA-3 | openai/gpt-oss-120b | 48,667 | 4,498 | 7,584 | 0 | $0.0101 | ✅ 3F/11E | Trace from L4:F13412 ("diets and dietary health") at pos 21 … |
| SA-1 | openai/gpt-oss-120b | 162,588 | 11,018 | 34,048 | 0 | $0.0315 | ✅ 6F/8E | Trace from L19:F1589 ("nutritional studies context") upstrea… |
| SA-2 | openai/gpt-oss-120b | 114,091 | 7,686 | 20,224 | 0 | $0.0220 | ✅ 5F/6E | Trace from L6:F11327 ("food or nutrition") upstream. What in… |
| **Total** | | **387,188** | **34,039** | **239,694** | **0** | **$0.1059** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 9m 16s