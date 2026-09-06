# Circuit Oracle Report
**Date:** 2026-07-28 07:21:12 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a stack of female-pronoun / female-person features, with the dominant top-5 features all being gender markers ("She", "her", "Sarah" as a name, "herself") and *no* profession-specific content (no "dietitian", "nutrition", "RD", "Academy" features appear in the top direct effects).

**Confidence:** 8

**Reasoning:**

Tracing the circuit from the output logit backward:

- **L18:F14677** ("instances of women or girls being mentioned", frac_nonzero=0.012, pos 1 direct_effect=+0.247, pos 34 +0.138, pos 12 +0.128) is the single largest contributor to the probe. Its promoted tokens are "herself, she, her, 她, 但她" and its top activating examples all fire on female pronouns. It traces back through **L15:F851** (pronoun context), **L12:F12493** (inhibitory male marker, −4.81), **L11:F9183** (female subject), and directly to the **"She"** embedding (direct_effect 27.1) — i.e., the "She" token itself is the dominant driver.

- **L6:F11646** ("references to women, triggered by pronouns and titles", frac_nonzero=0.020, pos 1 +0.375, pos 2 +0.305) is the second-largest contributor. Its top activating examples trigger on "her", "she", "her" — purely pronouns. Promoted tokens "herself, she, her". It also traces back to the **"She"** embedding (direct_effect 19.25) with no profession content.

- **L7:F8644** ("woman's name in a variety of contexts", frac_nonzero=0.009) is *inhibitory* (pos 12 direct_effect −0.270, pos 34 −0.108). Interestingly, this is the one feature that fires on "Sarah" (a name), and it is *suppressing* the probe — it fires on female first names in general (Belmont, Johnston, Knight, etc.), not on profession-specific content.

- **L12:F12940** ("female pronouns and possessive pronouns", pos 2 +0.252) reinforces the pronoun signal. Upstream is "She" embedding (5.31) and "loves" (4.25) — again, the pronoun, not the profession.

- **L14:F12501** ("uses of the feminine pronoun", pos 2 +0.130) is the third late-layer pronoun feature. Promoted tokens are "Obrigada, feminist, herself, feminists".

The mid-layer features **L7:F2765** ("mentions of people…personal details", frac_nonzero=0.045, the highest frac_nonzero in the circuit), **L4:F7864** (a code/XML feature that has been repurposed to also encode "herself/she/her" — note its promoted tokens include "herself, she's, she" and suppressed "himself"), **L0:F7509** ("female pronouns and words like daughter and husband", frac_nonzero=0.047), and **L1:F15251** (the "client" feature, pos 5, −0.170 — this is one of the few features that *does* touch profession content, but its direct effect is *inhibitory* on the probe).

The signal flow is: **"She"/"her"/"Sarah" embeddings → early gender/pronoun features (L0-L4) → mid-layer female-reference features (L6-L7) → late-layer female-person features (L12, L14, L18) → output**. Crucially, the only potentially profession-relevant features (L1:F15251 on "client", L7:F8644 on a female name) have *negative* direct effects on the probe, while every *positive* contributor is a generic female-gender marker. The actual nutrition/dietitian vocabulary ("nutrition", "diet", "Academy of Nutrition", "healthy", "blog") does not appear anywhere in the top direct-effect features. The user is correct: this probe is being driven by spurious gender features rather than genuine profession indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer female-person / pronoun features (L18, L14) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 34 | Late-layer female-person / pronoun features (L18, L14) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 12 | Late-layer female-person / pronoun features (L18, L14) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 2 | Late-layer female-person / pronoun features (L18, L14) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Late-layer female-person / pronoun features (L18, L14) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 12 | Female-name / proper-noun features (L7, L12, L6) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 12 | Female-name / proper-noun features (L7, L12, L6) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 34 | Female-name / proper-noun features (L7, L12, L6) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | Female-name / proper-noun features (L7, L12, L6) |  proper nouns consisting of a first and last name | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Female-name / proper-noun features (L7, L12, L6) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Female-name / proper-noun features (L7, L12, L6) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer female-reference features (L6, L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer female-reference features (L6, L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | Mid-layer female-reference features (L6, L7) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 5 | Mid-layer female-reference features (L6, L7) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 12 | Mid-layer female-reference features (L6, L7) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 11 | Mid-layer female-reference features (L6, L7) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early-layer gender/pronoun features (L0, L1, L4) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 12 | Early-layer gender/pronoun features (L0, L1, L4) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L0:F7509](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) | 4 | Early-layer gender/pronoun features (L0, L1, L4) |  female pronouns and words like daughter and husband that refer to women | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) |
| [L1:F15251](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) | 5 | Early-layer gender/pronoun features (L0, L1, L4) |  the word "client" and its plural form more often than not when capitalized as the first word of a sentence or preceded by a special character | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.375 |
| 3 | `inspect_feature` ×4 | L6:11646, L18:14677, L12:12940, L7:8644 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ❌ error | — | — | Trace upstream from L18:F14677 at pos 1 ("She"). This is a "women/girls mentione… |
| SA-2 | `L6:F11646@1` | ❌ error | — | — | Trace upstream from L6:F11646 at pos 1 ("She"). This is a "references to women, … |
| SA-3 | `L12:F12940@2` | ❌ error | — | — | Trace upstream from L12:F12940 at pos 2 ("loves"). This is a "female pronouns an… |
| SA-4 | `L7:F8644@12` | ❌ error | — | — | Trace upstream from L7:F8644 at pos 12. This is a "woman's name in a variety of … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@1, k=10 → Emb:"She"@1 (de=27.12) +9 more |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 3 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:"She"@1 (de=5.31) +9 more |
| 4 | `get_upstream_features` | L7:F8644@12, k=10 → Emb:"She"@1 (de=8.25) +9 more |
| 5 | `inspect_feature` ×10 | L4:7864, L7:2765, L4:15317, L5:16213, L0:7509, L1:15251, L6:16329, L4:1276, L12:14970, L14:12501 |
| 6 | `get_upstream_features` | L18:F14677@34, k=8 → Emb:" Sarah"@34 (de=5.69) +7 more |
| 7 | `get_upstream_features` | L12:F12940@12, k=8 → ❌ Feature (layer=12, feature_idx=12940) not found at pos=12. T |
| 8 | `get_upstream_features` | L14:F12501@2, k=8 → L12:F12940 (de=10.38) +7 more |
| 9 | `get_upstream_features` | L12:F14970@12, k=8 → Emb:" Sarah"@12 (de=4.62) +7 more |
| 10 | `get_upstream_features` | L7:F8644@34, k=8 → Emb:"She"@1 (de=4.00) +7 more |

### Build

`build_circuit` → 10 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 41,913 | 4,537 | 133,751 | 0 | $0.0260 | — | — |
| **Total** | | **41,913** | **4,537** | **133,751** | **0** | **$0.0260** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 5s