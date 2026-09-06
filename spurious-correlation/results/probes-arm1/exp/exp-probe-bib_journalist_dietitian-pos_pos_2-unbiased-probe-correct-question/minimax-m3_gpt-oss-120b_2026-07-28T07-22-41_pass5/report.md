# Circuit Oracle Report
**Date:** 2026-07-28 07:22:41 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification score is driven overwhelmingly by genuine profession-specific nutrition/food vocabulary (the "nutrition" token at pos 13 cascades through a deep ~10-layer food-domain feature chain, with "cook" at pos 17 as a secondary anchor), while a parallel "female pronoun" sub-circuit (L0:9519, L6:11646) flowing from the "She" token at pos 1 exerts a SUPPRESSIVE influence on the score rather than a spurious positive one.

**Confidence:** 8

**Reasoning:** The circuit bifurcates cleanly. **Positive (profession-grounded) path:** the Emb " nutrition" node at pos 13 directly contributes via its embedding (direct_effect=+0.1406 seen at L6:11327; massive +31.25 direct from embedding) and seeds a vertically coherent nutrition-domain feature chain — L4:13412 ("diets and dietary health", +0.1338), L4:9554 ("food, rations and feeding", +0.0493), L4:10494 ("health, medicine, diet, drugs", +0.0503) → L6:11327 ("food/nutrition words", +0.1406) → L14:4197 ("food/nutrition words", +0.1367) → L15:12472 (super-activator on "nutrition") → L16:12752 ("diet" in scientific context) → L17:14680 ("nutrition, food, diets") → L18:6105 ("eating and health", promoted token "healthy") → L19:1589 ("scientific/nutritional studies context", +0.084). Each step is a more abstract food/nutrition concept, and the L19 feature's promoted tokens are *diet, food, nutrition, diets, feeding, dietary* — all directly relevant to a nutrition profession. A second positive branch goes Emb " cook" (pos 17) → L15:2510 ("food preparation/cooking/kitchen", +0.0649) → output. **Negative (gender) path:** Emb "She" (pos 1) → L0:9519 ("she/her pronoun", direct_effect=**−0.0562**) → L4:7864 (promoted tokens include "herself", "shes", "she") → L6:11646 ("references to women, pronouns and titles", direct_effect=**−0.064**). The negative sign on these features is the critical finding: the gender/pronoun signal is *inhibiting* the probe score, not driving it spuriously toward the nutrition profession classification. The "She" token actively *suppresses* the score — which is the opposite of a "female → nutrition" spurious correlation. Other weak negative features (L0:2349 "others" at pos 7 −0.087; L0:14824 "has" at pos 2 −0.098; L0:6051 "periods" at pos 22 −0.054) are generic function-word/syntactic features (frac_nonzero 0.011–0.057) that are not profession-specific and not gendered.

**Verdict on the user's concern:** The user's hypothesis is **NOT supported by this circuit**. The profession probe is driven by a deep, well-structured food/nutrition semantic feature chain anchored on the literal "nutrition" and "cook" tokens — i.e., genuine topical indicators of the profession. Female-pronoun features are present in the circuit but contribute *negatively* to the classification score, meaning the probe is not using "She" as a shortcut to predict "nutritionist" — if anything, female references slightly *dampen* the score. This suggests the probe has learned the actual semantic content of the profession rather than a gender stereotype. The only caveat is that with a single input example I cannot verify the probe's behavior across other gendered subjects (e.g., a male nutrition expert), so I cannot fully rule out that "She" might contribute positively on other prompts.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: nutrition (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: cook (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Early-layer nutrition/food vocabulary features |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Early-layer nutrition/food vocabulary features |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 13 | Early-layer nutrition/food vocabulary features |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | L6:11327 - food/nutrition words |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 13 | L14:4197 - food/nutrition words |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F9449](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/9449) | 13 | L14:9449 - weight/diet context |  snippets related to weight and diet | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/9449) |
| [L15:F2510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) | 17 | L15:2510 - food preparation/cooking (pos 17) |  words and phrases related to food preparation and consumption, along with some words relating to the digestive system and eating disorders | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) |
| [L15:F12472](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) | 13 | L15:12472 - super-activator on 'nutrition' | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) |
| [L16:F12752](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) | 13 | L16:12752 - diet context | diet | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 13 | L17:14680 - nutrition/food/diets | nutrition, food, and diets | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 13 | L18:6105 - eating/health | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 13 | L19:1589 - nutritional studies context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female/pronoun references (NEGATIVE) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | L0:9519 - 'she/her' pronoun (NEGATIVE) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 7 | L0:2349 - 'others' word (NEGATIVE) |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 2 | L0:14824 - 'has' word (NEGATIVE) | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 22 | L0:6051 - periods/spaces (NEGATIVE) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 16 | L0:8444 - 'to' word | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11327 de=0.141 |
| 3 | `inspect_feature` ×16 | L6:11327, L14:4197, L4:13412, L19:1589, L15:2510, L0:14824, L0:2349, L6:11646, L0:9519, L1:728, L0:6051, L0:8444, L4:10494, L4:9554, L1:815, L0:2238 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@13` | ❌ error | — | — | Trace the nutrition/food-domain signal that drives the probe positively. Start a… |
| SA-2 | `L6:F11327@13` | ❌ error | — | — | Trace the food/nutrition vocabulary signal. Start at L6:F11327 (food/nutrition w… |
| SA-3 | `L6:F11646@1` | ❌ error | — | — | Trace the female-pronoun / "references to women" signal. Start at L6:F11646 (wom… |
| SA-4 | `L0:F9519@1` | ❌ error | — | — | Trace the "she/her pronoun" feature. Start at L0:F9519 (she/her pronoun, direct_… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F1589@13, k=15 → Emb:" nutrition"@13 (de=31.25) +14 more |
| 2 | `get_upstream_features` | L6:F11327@13, k=15 → Emb:" nutrition"@13 (de=21.00) +14 more |
| 3 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"She"@1 (de=19.25) +14 more |
| 4 | `get_upstream_features` | L14:F4197@13, k=10 → Emb:" nutrition"@13 (de=14.31) +9 more |
| 5 | `get_upstream_features` | L4:F13412@13, k=10 → Emb:" nutrition"@13 (de=14.06) +9 more |
| 6 | `get_upstream_features` | L4:F7864@1, k=8 → Emb:"She"@1 (de=24.62) +7 more |
| 7 | `get_upstream_features` | L0:F12519@1, k=8 → Emb:"She"@1 (de=21.88) +7 more |
| 8 | `inspect_feature` ×7 | L4:7864, L0:12519, L16:12752, L18:6105, L17:14680, L14:9449, L19:1589 |
| 9 | `get_upstream_features` | L16:F12752@13, k=5 → Emb:" nutrition"@13 (de=9.19) +4 more |
| 10 | `get_upstream_features` | L18:F6105@13, k=5 → Emb:" nutrition"@13 (de=31.50) +4 more |
| 11 | `get_upstream_features` | L17:F14680@13, k=5 → Emb:" nutrition"@13 (de=29.50) +4 more |
| 12 | `get_upstream_features` | L14:F9449@13, k=5 → Emb:" nutrition"@13 (de=8.94) +4 more |
| 13 | `get_upstream_features` | L0:F15382@1, k=5 → Emb:"She"@1 (de=16.88) +4 more |
| 14 | `get_upstream_features` | L17:F2771@13, k=5 → Emb:" nutrition"@13 (de=4.28) +4 more |
| 15 | `get_upstream_features` | L18:F186@13, k=5 → Emb:" nutrition"@13 (de=5.34) +4 more |
| 16 | `get_upstream_features` | L15:F2510@17, k=5 → Emb:" cook"@17 (de=28.88) +4 more |
| 17 | `inspect_feature` | L0, F15382 → "mentions of a female person." |

### Build

`build_circuit` → 20 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 50,030 | 6,272 | 206,585 | 0 | $0.0349 | — | — |
| **Total** | | **50,030** | **6,272** | **206,585** | **0** | **$0.0349** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 18s