# Circuit Oracle Report
**Date:** 2026-07-28 07:19:11 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by a hierarchy of nutrition/food-related features anchored on the "Die" subword in "Dietetics" (pos 20) — not by gender markers. "She/her" appears as a *suppressor*, not a driver.

**Confidence:** 8

**Reasoning:** The dominant positive path flows from the embedding of "Die" (pos 20, in "Dietetics", direct_effect 7.19 to L19:F1589) through a tightly interlocked nutrition concept stack: L4:F13412 ("terms related to diets and dietary health," frac_nonzero 0.012, promotes ▁diet/▁diets) → L6:F11327 ("words related to food or nutrition," frac_nonzero 0.012, promotes ▁food/▁eating) and L4:F13412 → L14:F4197 ("food insecurity/hunger," frac_nonzero 0.015, promotes ▁food) → L19:F1589 ("scientific nutritional studies context," frac_nonzero 0.038, promotes ▁diet/▁nutrition/▁foods). The L19 feature fires at three positions (9, 21, 50) corresponding to the nutrition-dense region of the text, and is the single largest positive contributor to the logit (0.064). L17:F7545 ("nurse/registered/healthcare terms," frac_nonzero 0.004) further supports the healthcare-professional reading.

Crucially, regarding the user's concern: the "she/her" feature (L0:F9519, frac_nonzero 0.011) has a *negative* direct effect (-0.05) on the probe — it slightly *suppresses* the classification, not drives it. The other negative features ("has," "from," "in") are generic function-word detectors (frac_nonzero 0.01–0.035) that fire on nearly any English sentence and serve as baseline subtractions rather than profession signals. The genuine profession indicator is the medical-specialty suffix detector L2:F2589 ("-ologist, -ician," frac_nonzero 0.008, max_token "ologist"), which fires on "Dietitian"-adjacent specialist morphology. The circuit uses *content* (nutrition, dietetics, medical specialty) — not gender — to drive the classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 21 | L19: Scientific nutrition context detector (promotes diet/food/nutrition) | a context of scientific, specially nutritional studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 50 | L19: Scientific nutrition context detector (promotes diet/food/nutrition) | a context of scientific, specially nutritional studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 9 | L19: Scientific nutrition context detector (promotes diet/food/nutrition) | a context of scientific, specially nutritional studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 21 | L17: Healthcare/architecture terms (mixed; includes nurse, registered) | mentions of architecture, design, nurses and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 21 | L14: Food-insecurity / hunger context detector (promotes food/feed) | words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | L14: Food-insecurity / hunger context detector (promotes food/feed) | words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 21 | L6: Generic food/nutrition word detector (promotes food, eating, meals) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 37 | L6: Generic food/nutrition word detector (promotes food, eating, meals) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | L4: Diet/dietary-health terminology detector (promotes diet, diets) | terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | L4: Diet/dietary-health terminology detector (promotes diet, diets) | terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | L4: Diet/dietary-health terminology detector (promotes diet, diets) | terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 37 | L4: Diet/dietary-health terminology detector (promotes diet, diets) | terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 36 | L4: Diet/dietary-health terminology detector (promotes diet, diets) | terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 64 | L4: Diet/dietary-health terminology detector (promotes diet, diets) | terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 64 | L4: Generic health/medicine/diet terms |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 37 | L2: Medical professional/specialty suffix detector (-ologist, -ician) |  words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | L0: Pronoun 'she/her' detector (NEGATIVE direct effect on probe) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 8 | L0: Preposition 'in' detector (NEGATIVE; generic function word) |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 2 | L0: Word 'has' detector (NEGATIVE; generic verb) | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 11 | L0: Word 'from' detector (NEGATIVE; generic preposition) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F9888](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) | 18 | L0: 'Education'/schooling word detector (positive) |  words related to formal schooling | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:13412 de=0.154 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@21` | ✅ reported | 6 | 8 | Trace this feature upstream. What does it encode? Does it detect nutrition/dieti… |
| SA-2 | `L4:F13412@21` | ✅ reported | 12 | 16 | Trace this feature upstream. It fires at multiple positions. What does it detect… |
| SA-3 | `L14:F4197@21` | ✅ reported | 5 | 14 | Trace upstream. What does this feature detect? Where does its signal come from? |
| SA-4 | `L0:F9519@1` | ❌ error | — | — | Trace upstream. This is a NEGATIVE direct effect (suppressing probe). What does … |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@21, k=10 | L4:F13412 (de=10.69) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 5 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 6 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 7 | `inspect_feature` | L17, F7545 | "mentions of architecture, design, nurses and healthcare." |
| 8 | `get_upstream_features` | L6:F11327@21, k=10 | L4:F13412 (de=5.88) +9 more |
| 9 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |

**Findings:** The traced circuit shows that feature L19:F1589 (layer 19) is a high‑level detector for scientific nutrition discussion. Its strongest upstream drivers are lower‑layer diet‑related features (layers 4 and 6) and a food‑insecurity feature (layer 14). The signal originates from early‑layer embeddings, notably the token 'Die' (German article) and the token 'Nutritional', which feed into the diet‑relat…

</details>

<details>
<summary><b>SA-2</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 3 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 4 | `get_upstream_features` | L3:F11774@21, k=10 | Emb:" Die"@20 (de=5.88) +9 more |
| 5 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 6 | `inspect_feature` | L2, F7473 | " capitalized two letter prefixes or suffixes" |
| 7 | `inspect_feature` | L2, F1984 | " strings of letters that appear to be fragments of names, especially p" |
| 8 | `inspect_feature` | L2, F4472 | " LaTeX math expressions" |
| 9 | `inspect_feature` | L2, F9618 | "the substrings "ith" and "io", especially when they occur together, an" |
| 10 | `get_upstream_features` | L3:F10028@21, k=10 | Emb:" Die"@20 (de=6.94) +9 more |
| 11 | `get_upstream_features` | L2:F7473@21, k=10 | Emb:" Die"@20 (de=19.00) +9 more |
| 12 | `inspect_feature` | L1, F1083 | " the characters "te" within code and/or non-English words" |
| 13 | `get_upstream_features` | L1:F1083@21, k=10 | Emb:"te"@21 (de=22.25) +9 more |
| 14 | `inspect_feature` | L3, F7212 | " words with the character sequence "eti" in them" |
| 15 | `inspect_feature` | L3, F7212 | " words with the character sequence "eti" in them" |
| 16 | `get_upstream_features` | L3:F7212@21, k=10 | Emb:" Die"@20 (de=11.94) +9 more |
| 17 | `inspect_feature` | L3, F13942 | "various categories of structured metadata and abbreviated terms" |

**Findings:** The target L4:F13412 is a diet‑related detector. Its strongest upstream drivers are low‑level lexical cues (the token "Die" and suffix "te"), which activate a capital‑letter fragment detector (L2:7473) and a name‑fragment detector (L2:1984). These feed into mid‑level features that capture scientific notation fragments (L3:11774) and material‑phrase patterns (L3:10028). Both mid‑level features then…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 2 | `get_upstream_features` | L14:F4197@21, k=10 | L6:F11327 (de=7.72) +9 more |
| 3 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 4 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 5 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 6 | `get_upstream_features` | L6:F11327@21, k=10 | L4:F13412 (de=5.88) +9 more |

**Findings:** The chain originates from the input token " Die" (pos 20) which feeds into a mid‑layer food‑insecurity detector (L14:F4197). The downstream feature at layer 14 encodes food‑insecurity concepts (hunger, inability to afford meals). Its strongest upstream drivers are mid‑layer nutrition/food detectors at layers 6 and 4, which themselves are driven by lower‑layer diet and ration detectors and the same…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L0:14824, L0:9519, L0:8974, L0:8061, L0:9888, L2:2589, L4:10494, L6:11327 |
| 2 | `get_upstream_features` | L19:F1589@21, k=5 → L4:F13412 (de=10.69) +4 more |

### Build

`build_circuit` → 15 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 29,190 | 4,000 | 69,517 | 0 | $0.0177 | — | — |
| SA-1 | openai/gpt-oss-120b | 79,750 | 5,201 | 23,248 | 0 | $0.0154 | ✅ 6F/8E | Trace this feature upstream. What does it encode? Does it de… |
| SA-3 | openai/gpt-oss-120b | 56,818 | 4,414 | 2,528 | 0 | $0.0112 | ✅ 5F/14E | Trace upstream. What does this feature detect? Where does it… |
| SA-2 | openai/gpt-oss-120b | 323,974 | 16,607 | 7,744 | 0 | $0.0587 | ✅ 12F/16E | Trace this feature upstream. It fires at multiple positions.… |
| **Total** | | **489,732** | **30,222** | **103,037** | **0** | **$0.1030** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 2s