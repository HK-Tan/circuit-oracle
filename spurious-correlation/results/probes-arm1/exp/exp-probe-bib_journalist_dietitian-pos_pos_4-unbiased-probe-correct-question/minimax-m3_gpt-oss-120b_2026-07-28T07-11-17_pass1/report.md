# Circuit Oracle Report
**Date:** 2026-07-28 07:11:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "Dietitian" is driven by genuine diet/nutrition vocabulary (Diet, Nutrition, Nutritional, Sports Nutrition) flowing through mid-layer food-context features — not by the "She/her" pronoun.

**Confidence:** 8

**Reasoning:** The top features driving the probe are all semantically coherent with the dietetics profession: L4:13412 "terms related to diets and dietary health" (direct_effect 0.154, fires at positions 21, 36, 37, 55, 64), L19:1589 "scientific/nutritional studies context" (direct_effect 0.064 at pos 21, 0.044 at pos 50, 0.043 at pos 9), L6:11327 "food or nutrition" (0.068 at pos 21), L14:4197 "food insecurity/food context" (0.059 at pos 21, 0.047 at pos 9), and L2:2589 "medical professionals and specialties" (0.059 at pos 37, fired by the "titian" subword of "Dietitian"). All five positive driver supernodes are substantively about nutrition/diet/medical specialty.

The user's concern about gender markers is partly supported but largely overstated. L0:9519 detects "She/her" pronouns and does contribute a negative direct_effect (-0.05 at pos 1) — but this is a *suppressive* (anti-Dietitian) contribution, not a supporting one. The L0:14824 "has" feature (-0.12 at pos 2) is similarly suppressive. Both push the score *down* on the female pronoun token. The "from" token detector L0:8974 (-0.05 at pos 11) is also suppressive. None of these syntactic/gender features positively drive the probe — they all inhibit it. The only positive non-diet feature is the general-purpose "in" preposition detector L0:8061 (-0.041, also suppressive).

Tracing confirms the positive path is anchored in genuine profession vocabulary: the token "Nutrition" (pos 50, 64) and "Nutritional" (pos 9) embed directly into L19:1589 (direct_effect 29.5, 26.1) and L4:13412 (direct_effect 10.0), "Die"+"titian" at pos 36-37 feed L2:2589 (the medical-specialty suffix detector that fires on "Dietitian" → "tician/etician"-style endings; direct_effect 19.1 from "titian"), and "Sports" at pos 63 feeds exercise/sports features (L1:15310, L1:6461) which in turn reinforce L4:13412. The signal flows: token embeddings → L1-L4 diet/sports subword detectors → L6 food vocabulary → L14 food context → L19 nutritional-study context → probe output. None of the positive edges pass through a gender/pronominal feature. The probe is using the actual semantic content of the profession — dietitian-specific vocabulary and the word "Dietitian" itself (via its "titian" subword activating the medical-specialty detector).

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | Embedding for token "She" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 36 | Emb: Die (pos 36) | Embedding for token "She" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 37 | Emb: titian (pos 37) | Embedding for token "She" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: Nutritional (pos 9) | Embedding for token "She" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 50 | Emb: nutrition (pos 50) | Embedding for token "She" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 63 | Emb: Sports (pos 63) | Embedding for token "She" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 64 | Emb: Nutrition (pos 64) | Embedding for token "She" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | She/Her pronoun feature (L0:9519) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 2 | 'has' word feature (L0:14824) | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L1:F15310](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15310) | 64 | Exercise / sports language (L1:15310, L1:6461, L1:165) | words related to physical exercise | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15310) |
| [L1:F6461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) | 64 | Exercise / sports language (L1:15310, L1:6461, L1:165) | technical language around physical activity, muscle function, and related studies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) |
| [L1:F165](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/165) | 64 | Exercise / sports language (L1:15310, L1:6461, L1:165) | names of sports teams and words related to sports statistics, contracts, and betting | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/165) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 37 | Medical professional/specialty suffix (L2:2589) |  words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 21 | Subword/scientific notation patterns (L3:11774, L3:10028) | what appears to be a smattering of strings related to scientific notation, live radio, and roman numerals | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 21 | Subword/scientific notation patterns (L3:11774, L3:10028) | words or short phrases that include "made of/from", and words ending with "ice", "ita", "ons", "ura", and "mor" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | Diet/food terms (L4:13412, L4:9554) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | Diet/food terms (L4:13412, L4:9554) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 36 | Diet/food terms (L4:13412, L4:9554) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 37 | Diet/food terms (L4:13412, L4:9554) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | Diet/food terms (L4:13412, L4:9554) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 64 | Diet/food terms (L4:13412, L4:9554) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 21 | Diet/food terms (L4:13412, L4:9554) |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 64 | Diet/food terms (L4:13412, L4:9554) |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 21 | Food/nutrition vocabulary (L6:11327) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 37 | Food/nutrition vocabulary (L6:11327) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 21 | Food-insecurity/food context (L14:4197) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | Food-insecurity/food context (L14:4197) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 21 | Scientific/nutritional study context (L19:1589) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 50 | Scientific/nutritional study context (L19:1589) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 9 | Scientific/nutritional study context (L19:1589) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 21 | Probe classification score | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:13412 de=0.154 |
| 3 | `inspect_feature` ×11 | L4:13412, L19:1589, L6:11327, L14:4197, L0:14824, L2:2589, L0:8974, L0:9519, L0:8061, L0:9888, L4:10494 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13412@21` | ✅ reported | 9 | 17 | Trace the L4:13412 (terms related to diets and dietary health) feature upstream.… |
| SA-2 | `L19:F1589@21` | ✅ reported | 7 | 10 | Trace the L19:1589 (scientific/nutritional studies context) feature upstream. Wh… |
| SA-3 | `L6:F11327@21` | ✅ reported | 4 | 9 | Trace the L6:11327 (words related to food or nutrition) feature upstream. What t… |
| SA-4 | `L14:F4197@21` | ✅ reported | 4 | 8 | Trace the L14:4197 (words related to food insecurity) feature upstream. What tok… |
| SA-5 | `L0:F9519@1` | ✅ reported | 3 | 2 | Trace the L0:9519 (pronoun "she" / "her") feature upstream. This is a negative d… |
| SA-6 | `L19:F1589@50` | ✅ reported | 3 | 8 | Trace the L19:1589 (scientific/nutritional studies) feature at pos 50 upstream. … |
| SA-7 | `L19:F1589@9` | ✅ reported | 6 | 8 | Trace the L19:1589 (scientific/nutritional studies) feature at pos 9 upstream. W… |
| SA-8 | `L4:F13412@64` | ✅ reported | 3 | 3 | Trace the L4:13412 feature at pos 64 upstream. What token is at pos 64 and what … |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 3 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 4 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 5 | `get_upstream_features` | L3:F10028@21, k=10 | Emb:" Die"@20 (de=6.94) +9 more |
| 6 | `get_upstream_features` | L3:F11774@21, k=10 | Emb:" Die"@20 (de=5.88) +9 more |
| 7 | `inspect_feature` | L2, F7473 | " capitalized two letter prefixes or suffixes" |
| 8 | `get_upstream_features` | L2:F7473@21, k=10 | Emb:" Die"@20 (de=19.00) +9 more |
| 9 | `inspect_feature` | L2, F1984 | " strings of letters that appear to be fragments of names, especially p" |
| 10 | `inspect_feature` | L2, F4472 | " LaTeX math expressions" |
| 11 | `get_upstream_features` | L2:F1984@21, k=10 | Emb:"te"@21 (de=10.44) +9 more |
| 12 | `inspect_feature` | L3, F7212 | " words with the character sequence "eti" in them" |
| 13 | `inspect_feature` | L0, F8585 | "the substring 'tam' or 'tab', sometimes in a medical context" |

**Findings:** The L4:13412 diet‑related feature is primarily driven by surface diet vocabulary (tokens like "diet", "diets", "DIET", "dieting") coming from the input embeddings (e.g., the token "Die" and the token "Nutritional" at earlier positions). Upstream, a cascade of lower‑layer features contributes: L3:10028 detects word endings typical of food‑related terms; L3:7212 captures the substring "eti" which in…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@21, k=10 | L4:F13412 (de=10.69) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 5 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 6 | `get_upstream_features` | L6:F11327@21, k=10 | L4:F13412 (de=5.88) +9 more |
| 7 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 8 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 9 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 10 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 11 | `get_upstream_features` | L3:F11774@21, k=10 | Emb:" Die"@20 (de=5.88) +9 more |
| 12 | `inspect_feature` | L17, F7545 | "mentions of architecture, design, nurses and healthcare." |

**Findings:** The high‑level L19:1589 feature that signals a scientific/nutritional study context is built from several mid‑level food‑related features. The strongest upstream driver is L4:13412, a diet‑health term detector, which itself receives strong excitation from L3:11774 (scientific‑notation detector) and direct token embeddings such as "Die" (pos 20) and "Nutritional" (pos 9). Additional contributors in…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@21, k=10 | L4:F13412 (de=5.88) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 5 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 6 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |

**Findings:** The food/nutrition feature (L6:11327) is driven primarily by a diet‑health feature in layer 4 (L4:13412) and a food‑rations feature (L4:9554), both of which receive strong positive influence from the input token "Die" (embedding). Additional modest contributions come from a scientific‑notation feature (L3:11774) and other mid‑layer features. Since we have reached a lower‑third layer (layer 4) and …

</details>

<details>
<summary><b>SA-4</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 2 | `get_upstream_features` | L14:F4197@21, k=10 | L6:F11327 (de=7.72) +9 more |
| 3 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 4 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 5 | `get_upstream_features` | L6:F11327@21, k=10 | L4:F13412 (de=5.88) +9 more |
| 6 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 7 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |

**Findings:** Tracing from L14:F4197 (food‑insecurity detector) shows its strongest upstream drivers are lower‑layer food‑related features: L6:11327 (generic food/nutrition), L4:13412 (diet‑health terms) and L4:9554 (rations/feeding). These are further driven by deeper features (e.g., L3:11774, L3:10028) and ultimately by raw token embeddings such as "Die". The trace reaches layer ≤8 and includes a positive emb…

</details>

<details>
<summary><b>SA-5</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 2 | `get_upstream_features` | L0:F9519@1, k=10 | Emb:"She"@1 (de=15.75) +9 more |

**Findings:** The L0:F9519 feature (detecting "she/her") receives its primary drive from the raw token embedding of the word "She" (direct_effect 15.75) and a minor contribution from the <bos> embedding (direct_effect 1.19). Both upstream nodes are embeddings, and the path already satisfies the required lower‑third layer condition (layer 0). No additional non‑embedding upstream features with positive direct eff…

</details>

<details>
<summary><b>SA-6</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@50, k=10 | Emb:" nutrition"@50 (de=29.50) +9 more |
| 3 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 4 | `get_upstream_features` | L6:F11327@50, k=10 | Emb:" nutrition"@50 (de=19.50) +9 more |
| 5 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 6 | `get_upstream_features` | L14:F4197@50, k=10 | Emb:" nutrition"@50 (de=14.44) +9 more |
| 7 | `get_upstream_features` | L6:F11327@50, k=10 | Emb:" nutrition"@50 (de=19.50) +9 more |
| 8 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |

**Findings:** The L19:1589 nutrition‑study feature is primarily driven by the literal input token " nutrition" at position 50. The embedding of that token contributes a large positive direct effect (29.5) directly to the target feature and also feeds upstream food‑related features at layers 14 and 6, which themselves amplify the signal. A secondary minor driver is the token "titian" at position 37, but its effe…

</details>

<details>
<summary><b>SA-7</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@9, k=15 | Emb:" Nutritional"@9 (de=26.12) +14 more |
| 3 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 4 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 5 | `get_upstream_features` | L14:F4197@9, k=15 | Emb:" Nutritional"@9 (de=14.44) +14 more |
| 6 | `get_upstream_features` | L6:F11327@9, k=10 | Emb:" Nutritional"@9 (de=16.75) +9 more |
| 7 | `inspect_feature` | L17, F14680 | "nutrition, food, and diets" |
| 8 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 9 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |

**Findings:** The L19:1589 scientific/nutritional‑studies feature is driven primarily by the raw token embedding " Nutritional" at position 9 (direct_effect ≈ 26). This embedding excites mid‑layer food‑insecurity (L14:4197) and early‑layer generic food/nutrition detectors (L6:11327), which in turn feed the target. Additional contribution comes from a deeper nutrition‑specific detector (L17:14680). All discovere…

</details>

<details>
<summary><b>SA-8</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_top_logits` | k=5 | "" (100%) |
| 3 | `get_upstream_features` | L4:F13412@64, k=10 | Emb:" Nutrition"@64 (de=10.00) +9 more |
| 4 | `inspect_feature` | L1, F15310 | " words related to physical exercise" |
| 5 | `get_upstream_features` | L1:F15310@64, k=10 | Emb:" Sports"@63 (de=8.31) +9 more |
| 6 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |
| 7 | `get_upstream_features` | L1:F6461@64, k=10 | Emb:" Sports"@63 (de=11.75) +9 more |
| 8 | `inspect_feature` | L2, F2589 | " words related to medical professionals and medical specialties" |
| 9 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |

**Findings:** L4:13412 at position 64 is a diet‑related detector. The token at that position is " Nutrition" (including leading space) and provides a strong direct effect (~10) to the feature. Upstream, two lower‑layer (≤8) exercise‑related features—L1:15310 and L1:6461—also drive it positively, each receiving large excitatory input from the token " Sports" at position 63. This satisfies the required terminatio…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-9 | `L2:F2589@37` | ❌ error | — | — | Trace the L2:2589 (medical professionals/specialties) feature at pos 37 upstream… |

### Re-dispatch (round 3): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-10 | `L4:F10494@64` | ✅ reported | 5 | 4 | Trace the L4:10494 (health, medicine, diet, drugs) feature at pos 64 upstream. W… |

<details>
<summary><b>SA-10</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F10494 | " words related to health, medicine, diet, drugs, age groups, and excer" |
| 2 | `get_upstream_features` | L4:F10494@64, k=10 | Emb:" Nutrition"@64 (de=6.91) +9 more |
| 3 | `inspect_feature` | L1, F6461 | " technical language around physical activity, muscle function, and rel" |
| 4 | `get_upstream_features` | L1:F6461@64, k=10 | Emb:" Sports"@63 (de=11.75) +9 more |
| 5 | `inspect_feature` | L1, F165 | " names of sports teams and words related to sports statistics, contrac" |
| 6 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 7 | `inspect_feature` | L1, F15310 | " words related to physical exercise" |
| 8 | `get_upstream_features` | L0:F9026@64, k=10 | Emb:" Nutrition"@64 (de=24.75) +9 more |
| 9 | `get_upstream_features` | L1:F165@64, k=10 | Emb:" Sports"@63 (de=9.81) +9 more |

**Findings:** The health/medicine feature (L4:10494) is primarily driven by the token embedding Nutrition at position 64 (direct_effect ≈ 6.9) and also receives a boost from the Sports token at position 63 (direct_effect ≈ 2.4). Upstream, the strongest positive contributors are mid‑layer features: L1:6461 (exercise‑physiology), L1:165 (sports‑statistics), L1:15310 (general exercise wording), and L0:9026 (techni…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×2 | L2:2589, L4:9554 |
| 2 | `get_upstream_features` | L2:F2589@37, k=5 → Emb:"titian"@37 (de=19.12) +4 more |
| 3 | `get_upstream_features` | L0:F14824@2, k=5 → Emb:" has"@2 (de=32.75) +4 more |

### Build

`build_circuit` → 17 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 55,804 | 5,460 | 170,181 | 0 | $0.0335 | — | — |
| SA-4 | openai/gpt-oss-120b | 71,839 | 5,927 | 14,304 | 0 | $0.0145 | ✅ 4F/8E | Trace the L14:4197 (words related to food insecurity) featur… |
| SA-3 | openai/gpt-oss-120b | 49,674 | 4,049 | 7,584 | 0 | $0.0100 | ✅ 4F/9E | Trace the L6:11327 (words related to food or nutrition) feat… |
| SA-2 | openai/gpt-oss-120b | 155,222 | 9,627 | 28,960 | 0 | $0.0295 | ✅ 7F/10E | Trace the L19:1589 (scientific/nutritional studies context) … |
| SA-1 | openai/gpt-oss-120b | 187,556 | 11,935 | 11,200 | 0 | $0.0355 | ✅ 9F/17E | Trace the L4:13412 (terms related to diets and dietary healt… |
| SA-5 | openai/gpt-oss-120b | 6,974 | 1,096 | 8,608 | 0 | $0.0018 | ✅ 3F/2E | Trace the L0:9519 (pronoun "she" / "her") feature upstream. … |
| SA-7 | openai/gpt-oss-120b | 113,931 | 7,761 | 7,968 | 0 | $0.0219 | ✅ 6F/8E | Trace the L19:1589 (scientific/nutritional studies) feature … |
| SA-6 | openai/gpt-oss-120b | 67,235 | 5,034 | 10,720 | 0 | $0.0133 | ✅ 3F/8E | Trace the L19:1589 (scientific/nutritional studies) feature … |
| SA-8 | openai/gpt-oss-120b | 89,414 | 6,001 | 13,344 | 0 | $0.0172 | ✅ 3F/3E | Trace the L4:13412 feature at pos 64 upstream. What token is… |
| SA-10 | openai/gpt-oss-120b | 105,848 | 6,304 | 15,168 | 0 | $0.0199 | ✅ 5F/4E | Trace the L4:10494 (health, medicine, diet, drugs) feature a… |
| **Total** | | **903,497** | **63,194** | **288,037** | **0** | **$0.1971** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 12m 24s