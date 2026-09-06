# Circuit Oracle Report
**Date:** 2026-07-28 07:23:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by late-layer features that encode "instances of women/girls being mentioned" (L18:14677, L19:9685) and mid-layer "references to women via pronouns and titles" (L6:11646, L7:2765), with profession-related diet/nutrition tokens (L4:13412) feeding into the same mid-layer women-features, indicating the profession signal is conflated with gender rather than used independently.

**Confidence:** 8

**Reasoning:** The circuit reveals two parallel pathways converging on the probe:

1. **Gender pathway (dominant):** The token "She" at pos 1 drives the embedding → L0:8974 ("from" at pos 11, -0.11 direct effect, but acts as a confound through later L4 features) and most importantly → L4:7864 (She-token feature, direct_effect 0.13) → L6:11646 ("references to women", +0.21 at pos 1, +0.14 at pos 2) → L18:14677 ("instances of women or girls being mentioned", +0.14 at pos 1, +0.12 at pos 57, frac_nonzero 0.012) → output. The She token at pos 57 contributes direct_effect=22.6 to L18:14677 and 9.94 to L19:9685 ("references to women's names and their roles"). These gender features have near-binary labels (promoted tokens are "herself/she/her", suppressed are "himself/his/his").

2. **Profession pathway (confounded):** L4:13412 ("terms related to diets and dietary health") fires at pos 21, 22, 37, 55 — the tokens "Die(tetics)", "titian", "RD" — with direct_effect +0.16, +0.10, +0.09, +0.12. Tracing upstream: this feature receives signal from embedding "Die" (pos 20, +4.06) and "RD" (pos 55, +11.3) and "titian" (pos 37, +14.0) — genuine profession tokens. However, L4:13412 also feeds INTO the mid-layer women-features (L6:11646, L7:2765), which then feed L18:14677. This means the diet/nutrition profession signal is being routed through a "woman-mention" feature before reaching the probe.

3. **Counter-signal:** L7:8644 ("woman's name in a variety of contexts", activated by "Heather" at pos 31 and "she" at pos 57) has direct_effect -0.21 on the probe — a strong *suppressive* gender signal. This feature's suppressed tokens are "herself/she/her/her" while promoted are "himself". This is a competing mechanism pulling the probe score down.

The user's concern is **substantiated**: the probe is being driven by gender-identity features (L6:11646 "references to women", L18:14677 "instances of women or girls", L19:9685 "women's names and their roles") that have nothing inherently to do with the dietitian profession. While L4:13412 does encode legitimate diet/nutrition content, its signal is *combined with* rather than *separated from* the gender signal by the time it reaches the probe direction. The probe direction vector is aligned with late-layer representations that integrate both profession-content and female-gender-marking into a single "female in a caring profession" feature direction — a classic spurious correlation. The presence of the negative L7:8644 feature further suggests the model internally distinguishes "woman's name as proper noun" from "woman as gender identity," and the probe is reading out the latter mixed with the former rather than the dietetics profession in isolation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) — subject pronoun | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 57 | Emb: she (pos 57) — pronoun, later position | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 31 | Emb: Heather (pos 31) — female proper name | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: Nutritional/Dietetics/RD (pos 9, 20, 55) — profession tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: Nutritional/Dietetics/RD (pos 9, 20, 55) — profession tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 55 | Emb: Nutritional/Dietetics/RD (pos 9, 20, 55) — profession tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: from (pos 11) — generic preposition | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 11 | Early-layer gender/person features (L0-L4) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early-layer gender/person features (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 31 | Early-layer gender/person features (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early-layer gender/person features (L0-L4) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | Diet/nutrition profession features (L4:13412 across pos 21,22,37,55) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | Diet/nutrition profession features (L4:13412 across pos 21,22,37,55) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 37 | Diet/nutrition profession features (L4:13412 across pos 21,22,37,55) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | Diet/nutrition profession features (L4:13412 across pos 21,22,37,55) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer 'women/gender pronoun' features (L6-L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer 'women/gender pronoun' features (L6-L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 31 | Mid-layer 'women/gender pronoun' features (L6-L7) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 57 | Mid-layer 'women/gender pronoun' features (L6-L7) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-layer 'women/gender pronoun' features (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 31 | Mid-layer 'women/gender pronoun' features (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 31 | Negative female-name feature (L7:8644) — suppresses probe score |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 57 | Negative female-name feature (L7:8644) — suppresses probe score |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Negative female-name feature (L7:8644) — suppresses probe score | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer 'women/girls' identity features (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 57 | Late-layer 'women/girls' identity features (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 57 | Late-layer 'women/girls' identity features (L18-L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:8644 de=-0.212 |
| 3 | `inspect_feature` ×4 | L6:11646, L18:14677, L4:13412, L7:2765 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ❌ error | — | — | Trace the L18:14677 "women/girls" feature upstream. What specific input tokens d… |
| SA-2 | `L6:F11646@1` | ❌ error | — | — | Trace L6:11646 "references to women" upstream. What tokens does this gender feat… |
| SA-3 | `L4:F13412@21` | ❌ error | — | — | Trace L4:13412 "diets and dietary health" upstream. What specific tokens does th… |
| SA-4 | `L7:F8644@31` | ❌ error | — | — | Trace L7:8644 upstream. This feature has a large negative direct_effect on the p… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@1, k=15 → Emb:"She"@1 (de=27.12) +14 more |
| 2 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"She"@1 (de=19.25) +14 more |
| 3 | `get_upstream_features` | L4:F13412@21, k=15 → L3:F11774 (de=4.81) +14 more |
| 4 | `get_upstream_features` | L7:F8644@31, k=15 → Emb:"She"@1 (de=7.47) +14 more |
| 5 | `inspect_feature` | L7, F8644 → " woman's name in a variety of contexts" |
| 6 | `get_upstream_features` | L18:F14677@57, k=15 → Emb:" she"@57 (de=22.62) +14 more |
| 7 | `get_upstream_features` | L6:F11646@2, k=10 → L4:F15317 (de=8.75) +9 more |
| 8 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"She"@1 (de=24.62) +9 more |
| 9 | `get_upstream_features` | L4:F1276@31, k=10 → Emb:" Heather"@31 (de=10.94) +9 more |
| 10 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:"She"@1 (de=6.03) +9 more |
| 11 | `get_upstream_features` | L12:F14970@31, k=10 → Emb:"<bos>"@0 (de=-3.48) +9 more |
| 12 | `get_upstream_features` | L19:F9685@57, k=10 → Emb:" she"@57 (de=9.94) +9 more |
| 13 | `inspect_feature` ×3 | L19:9685, L17:5889, L4:15317 |
| 14 | `get_upstream_features` | L4:F13412@55, k=10 → Emb:" RD"@55 (de=11.31) +9 more |
| 15 | `get_upstream_features` | L4:F13412@37, k=10 → Emb:"titian"@37 (de=14.00) +9 more |
| 16 | `get_upstream_features` | L4:F13412@22, k=10 → L3:F11774 (de=3.98) +9 more |
| 17 | `get_upstream_features` | L6:F16329@1, k=10 → Emb:"She"@1 (de=8.94) +9 more |
| 18 | `get_upstream_features` | L0:F8974@11, k=10 → Emb:" from"@11 (de=40.00) +9 more |
| 19 | `inspect_feature` ×2 | L6:16329, L0:8974 |
| 20 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"She"@1 (de=24.62) +9 more |

### Build

`build_circuit` → 11 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 22,430 | 5,069 | 178,217 | 0 | $0.0235 | — | — |
| **Total** | | **22,430** | **5,069** | **178,217** | **0** | **$0.0235** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 29s