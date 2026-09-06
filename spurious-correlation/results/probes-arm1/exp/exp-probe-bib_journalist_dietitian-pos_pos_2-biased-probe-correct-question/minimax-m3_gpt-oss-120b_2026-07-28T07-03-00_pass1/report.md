# Circuit Oracle Report
**Date:** 2026-07-28 07:03:00 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by **gender/pronoun features**, not by profession content features — the user's concern about spurious gender-marker reliance is strongly confirmed.

**Confidence:** 9

**Reasoning:**

**Two parallel paths converge on the probe output:**

1. **Gender path (dominant, ~2× the signal):** Three pronoun tokens — `She` (pos 1), `her` (pos 2), `She` (pos 23) — feed the embedding into a cascade of female-reference features:
   - L0 `F15382` (early token-level, frac=0.009) → L2 `F7672` "mentions of women by name and relationship" → L4 `F15317` "named entities/people" + L4 `F7864` → L6 `F11646` "references to women, triggered by pronouns and titles" (frac=0.020) → L10 `F14965` "terms relating to women" (frac=0.019) → L12 `F12940` "female pronouns and possessive pronouns" (frac=0.007) → L14 `F12501` "uses of the feminine pronoun" (frac=0.014) → L18 `F14677` "instances of women or girls being mentioned" (frac=0.012, direct_effect=+0.24) → output probe.
   - Top features by direct_effect to the probe are gender features: `L6:F11646@1` (+0.36), `L12:F12940@2` (+0.29), `L18:F14677@23` (+0.24).
   - Crucially, the male-pronoun suppressor `L18:F14743` "He" (frac=0.018, promoted = himself/his) fires with **negative direct_effect** (-0.11), confirming the probe direction explicitly contrasts female vs. male pronouns.

2. **Nutrition/content path (minor):** The `nutrition` embedding at pos 13 drives `L3:F6246` (nutrient root, frac=0.004) → `L4:F13412` (diets/dietary health, frac=0.012) + `L4:F9554` (food/rations, frac=0.013) → `L6:F11327` "food or nutrition" (frac=0.012, direct_effect=+0.15). This is a legitimate profession-content signal but contributes only one top-15 feature.

**Why the user is correct:** The probe direction is aligned with a *gender contrast* dimension (feminine-promoted, masculine-suppressed) more than with a profession dimension. The dominant late-layer features driving the probe score are explicitly pronoun/feminine-reference features whose promoted tokens are `herself/she/her` and suppressed tokens are `himself/his/His` — classic spurious gender markers, not nutritionist/cooking/owner indicators. The single nutrition feature (`L6:F11327`) is overshadowed by ~4–5× more pronoun-driven features at the top of the ranking. If the subject's biography had used "He" or "his", the probe score would drop substantially via `L18:F14743`'s inhibition even though the profession content (nutrition, recipes, cooking) would be identical — confirming the classification relies on gender-correlated surface features rather than genuine profession indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) — primary female-pronoun signal | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: She (pos 23) — secondary female-pronoun signal | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: her (pos 2) — possessive female-pronoun signal | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: nutrition (pos 13) — profession/content token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 23 | Early-layer female-token detectors (L0) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L3:F6246](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) | 13 | Early nutrient-root detector (L3) | the word "Nutrients" and words containing "ure". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Mid-layer female-reference / person-entity detectors (L4-L6) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Mid-layer female-reference / person-entity detectors (L4-L6) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer female-reference / person-entity detectors (L4-L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer female-reference / person-entity detectors (L4-L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 23 | Mid-layer female-reference / person-entity detectors (L4-L6) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Mid-layer female-reference / person-entity detectors (L4-L6) |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Mid-layer diet/food detectors (L4) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Mid-layer diet/food detectors (L4) | words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Mid-layer female-pronoun & feminine-pronoun features (L10-L12) |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-layer female-pronoun & feminine-pronoun features (L10-L12) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 3 | Mid-layer female-pronoun & feminine-pronoun features (L10-L12) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 2 | Mid-layer female-pronoun & feminine-pronoun features (L10-L12) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Mid-layer food/nutrition feature (L6) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer female-reference features (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 2 | Late-layer female-reference features (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 23 | Late-layer female-reference features (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 23 | Late-layer female-reference features (L18-L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 23 | Late-layer female-reference features (L18-L19) | personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 23 | Late-layer female-reference features (L18-L19) | references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Late-layer male-pronoun suppressor (L18) — fires on 'He' to suppress probe | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 23 | Late-layer male-pronoun suppressor (L18) — fires on 'He' to suppress probe |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 23 | Probe output direction | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.357 |
| 3 | `inspect_feature` ×12 | L6:11646, L12:12940, L18:14677, L4:15317, L4:7864, L2:7672, L10:14965, L6:11327, L14:12501, L19:9685, L4:13412, L6:16329 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@23` | ✅ reported | 4 | 8 | Trace this gender/female-reference feature upstream to its input token source. I… |
| SA-2 | `L12:F12940@2` | ✅ reported | 7 | 9 | Trace this female-pronoun feature upstream to find which input tokens drive it. |
| SA-3 | `L6:F11327@13` | ✅ reported | 4 | 7 | Trace the food/nutrition feature upstream to its input token source. Identify wh… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@23, k=10 | Emb:" She"@23 (de=14.31) +9 more |
| 3 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 4 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 5 | `get_upstream_features` | L0:F15382@23, k=10 | Emb:" She"@23 (de=23.62) +9 more |
| 6 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 7 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 8 | `get_upstream_features` | L6:F11646@23, k=10 | Emb:" She"@23 (de=18.75) +9 more |
| 9 | `get_upstream_features` | L17:F5889@23, k=10 | Emb:" She"@23 (de=19.12) +9 more |
| 10 | `inspect_feature` | L13, F6622 | " pronouns." |
| 11 | `get_upstream_features` | L13:F6622@23, k=10 | Emb:" She"@23 (de=12.50) +9 more |

**Findings:** The female‑gender signal at L18:F14677 (position 23) originates from the raw input token " She" at position 23. The embedding of that token provides a strong positive direct effect to the target feature and also drives a sparse layer‑0 detector (L0:F15382). This low‑layer feature propagates to mid‑layer pronoun‑reference features (L17:F5889 and L15:F3330), which together activate the final gender …

</details>

<details>
<summary><b>SA-2</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:"She"@1 (de=6.03) +9 more |
| 3 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 4 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 5 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 6 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=13.56) +9 more |
| 7 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 8 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 9 | `get_upstream_features` | L6:F11646@2, k=10 | L4:F15317 (de=8.75) +9 more |
| 10 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 11 | `get_upstream_features` | L10:F14965@2, k=10 | L4:F15317 (de=5.56) +9 more |
| 12 | `get_upstream_features` | L2:F7672@1, k=10 | Emb:"She"@1 (de=13.88) +9 more |
| 13 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 14 | `get_upstream_features` | L8:F7245@2, k=10 | Emb:"She"@1 (de=3.12) +9 more |
| 15 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |

**Findings:** Starting from the female‑pronoun feature L12:F12940 (pos 2), the strongest upstream driver is the embedding of the token "She" (pos 1) with a direct positive effect of 6.03. The next major contributors are mid‑layer person‑entity detectors: L4:F15317 (named‑entity detector) and L6:F11646 (female‑reference detector). These themselves are driven largely by the same "She" token and by each other (L4:…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@13, k=10 | Emb:" nutrition"@13 (de=21.00) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |
| 5 | `get_upstream_features` | L4:F13412@13, k=10 | Emb:" nutrition"@13 (de=14.06) +9 more |
| 6 | `get_upstream_features` | L4:F9554@13, k=10 | Emb:" nutrition"@13 (de=15.88) +9 more |
| 7 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |

**Findings:** The food/nutrition detector (L6:F11327) receives its strongest excitatory drive directly from the input token embedding ' nutrition' at the same position (pos 13) with a large positive direct effect (21.0). Intermediate diet‑related features in layers 4 (F13412, F9554) also feed into the target, each themselves driven largely by the same ' nutrition' embedding. A lower‑layer (L3:F6246) feature tha…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 2 | `get_upstream_features` | L4:F15317@1, k=10 → ❌ Feature (layer=4, feature_idx=15317) not found at pos=1. Thi |
| 3 | `inspect_feature` ×2 | L18:14743, L7:8644 |

### Build

`build_circuit` → 13 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 60,527 | 4,146 | 73,457 | 0 | $0.0275 | — | — |
| SA-3 | openai/gpt-oss-120b | 58,575 | 4,029 | 10,208 | 0 | $0.0114 | ✅ 4F/7E | Trace the food/nutrition feature upstream to its input token… |
| SA-1 | openai/gpt-oss-120b | 149,179 | 7,915 | 8,480 | 0 | $0.0273 | ✅ 4F/8E | Trace this gender/female-reference feature upstream to its i… |
| SA-2 | openai/gpt-oss-120b | 241,138 | 11,680 | 23,744 | 0 | $0.0435 | ✅ 7F/9E | Trace this female-pronoun feature upstream to find which inp… |
| **Total** | | **509,419** | **27,770** | **115,889** | **0** | **$0.1097** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 7s