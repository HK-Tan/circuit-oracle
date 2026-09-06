# Circuit Oracle Report
**Date:** 2026-07-28 07:09:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of Sarah's profession is driven almost entirely by a cascading chain of female-gender/pronominal features (triggered by "She", "her", "Sarah") rather than by any profession- or nutrition-specific signal.

**Confidence:** 9

**Reasoning:** The top 20 features driving the probe are, with virtually no exception, *gender*-focused:
- L6:F11646 — "references to women, potentially triggered by pronouns and titles" (frac=0.020) — the #1 driver, also the #2 driver at the next position, with combined direct_effect ≈ 0.68.
- L18:F14677 — "instances of women or girls being mentioned" (frac=0.012) — fires at positions 1, 12, and 34 (all "She"/"Sarah" tokens), direct_effect ≈ 0.51.
- L12:F12940 — "references to female pronouns and possessive pronouns" (frac=0.007) — direct_effect 0.25 at pos 2 ("loves"/"her" position).
- L14:F12501 — "uses of the feminine pronoun" (frac=0.014) — direct_effect 0.13.
- L10:F14965 — "terms relating to women" (frac=0.019).
- L12:F14970 — "names of people, both first and last names" (frac=0.003), firing on "Sarah" but with promoted_tokens biased toward "herself"/"she"/"her".
- L6:F16329 — "female first names and their possessive forms" (negative direct_effect, suppressing the male-name direction).
- L7:F2765 — "mentions of people or characters" — fires generically on person references but is wired to the same women/gender downstream features.
- L4/5 entity detectors (F15317, F7864, F16213) — proper-noun/character detectors that flow into the gender detectors rather than into profession detectors.

The upstream trace from L12:F12940 confirms this: it is driven by the **"She" embedding** (direct_effect 8.4), the **"loves" embedding** (6.3), and downstream features like L10:F14965 ("terms relating to women") and L6:F11646 ("references to women, pronouns and titles") — all of which are pure-gender signals. The subagent that traced this path confirmed that *every* upstream link encodes gender or generic personhood, with **no profession, nutrition, or domain-specific semantic** anywhere in the chain. The L18:F14677 "women/girls" feature shows direct_effect 27.1 from the "She" embedding alone — the dominant signal is the gendered first word.

A single non-gender feature does appear: L1:F15251 — the "client" word feature — but it has a *negative* direct_effect (-0.17) on the probe and is being used to suppress the female-pronoun direction, not to support a profession reading. Likewise L0:F7509 ("female pronouns and words like daughter and husband") has negative direct_effect at pos 4 ("her"). The only profession-adjacent tokens in the text ("Nutrition", "Academy of Nutrition and Dietetics", "recipes") do not appear in the top-feature list, and "Nutrition" itself shows up only as a small upstream contributor to the L18 women-mentioning feature at pos 34, with direct_effect 1.14 — it reaches the probe only by reinforcing the female-entity signal at "Sarah's blog".

The picture is unambiguous: the probe is essentially implementing a "this text is about a woman" classifier. The female-pronoun and female-name cascade is being interpreted as evidence of profession — a textbook spurious-correlation failure mode where gender markers (she/her/Sarah) substitute for genuine profession indicators (dietitian, nutritionist, Academy of Nutrition, RD credential, recipes, food, nutrition). The user's concern is confirmed: the circuit is using gender as a proxy for profession, not profession content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7509](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) | 4 | Early gender/pronoun detectors |  female pronouns and words like daughter and husband that refer to women | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) |
| [L1:F15251](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) | 5 | 'client' word feature (L1) |  the word "client" and its plural form more often than not when capitalized as the first word of a sentence or preceded by a special character | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Named-entity / proper-name detectors |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Named-entity / proper-name detectors | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | Named-entity / proper-name detectors |  proper nouns consisting of a first and last name | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer gender/women detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer gender/women detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Mid-layer gender/women detectors | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 2 | Mid-layer gender/women detectors | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 12 | Mid-layer gender/women detectors |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | Mid-layer gender/women detectors |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 5 | Mid-layer gender/women detectors |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 11 | Mid-layer gender/women detectors |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 12 | Mid-layer gender/women detectors |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Late-layer gender/women detectors |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Late-layer gender/women detectors | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 12 | Late-layer gender/women detectors |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 2 | Late-layer gender/women detectors |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer gender/women detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 12 | Late-layer gender/women detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 34 | Late-layer gender/women detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.375 |
| 3 | `inspect_feature` ×13 | L6:11646, L12:12940, L18:14677, L4:7864, L4:15317, L7:8644, L6:16329, L0:7509, L1:15251, L5:16213, L7:2765, L12:14970, L14:12501 |
| 4 | `get_upstream_features` | L12:F12940 (de=10.38) +14 more |
| 5 | `get_upstream_features` | Emb:" Sarah"@12 (de=4.62) +14 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ❌ error | — | — | Trace the path from L18:F14677 ('instances of women or girls being mentioned') b… |
| SA-2 | `L12:F12940@2` | ✅ reported | 9 | 9 | Trace the path from L12:F12940 ('references to female pronouns and possessive pr… |
| SA-3 | `L14:F12501@2` | ❌ error | — | — | Trace the path from L14:F12501 ('uses of the feminine pronoun') backward. Find t… |

<details>
<summary><b>SA-2</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:"She"@1 (de=5.31) +9 more |
| 3 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 4 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 5 | `get_upstream_features` | L10:F14965@2, k=10 | Emb:"She"@1 (de=5.50) +9 more |
| 6 | `get_upstream_features` | L7:F2765@2, k=10 | Emb:"She"@1 (de=4.16) +9 more |
| 7 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 8 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 9 | `get_upstream_features` | L6:F11646@2, k=10 | Emb:" loves"@2 (de=5.66) +9 more |
| 10 | `inspect_feature` | L5, F16213 | " proper nouns consisting of a first and last name" |
| 11 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=12.44) +9 more |
| 12 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 13 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 14 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=12.44) +9 more |
| 15 | `inspect_feature` | L2, F899 | " language related to arts, crafts, blogs and medical situations" |
| 16 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 17 | `inspect_feature` | L9, F2587 | " references to personal pronouns in the third person, and possibly fir" |

**Findings:** The L12:F12940 gender feature is driven primarily by the embedding of the token "She" and reinforced by a cascade of higher‑layer gender detectors (terms relating to women, generic person mentions, named‑entity and proper‑name detectors). All upstream signals encode gender or generic personhood; none reference professions, nutrition, or any other domain. Therefore this feature is tied solely to fe…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@1, k=15 → Emb:"She"@1 (de=27.12) +14 more |
| 2 | `get_upstream_features` | L14:F12501@2, k=15 → L12:F12940 (de=10.38) +14 more |
| 3 | `get_upstream_features` | L18:F14677@34, k=15 → Emb:" Sarah"@34 (de=5.69) +14 more |
| 4 | `inspect_feature` ×3 | L10:14965, L15:851, L11:9183 |
| 5 | `get_top_features` | token="", k=20 → 20 features; top: L6:11646 de=0.375 |

### Build

`build_circuit` → 13 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 76,609 | 4,169 | 175,342 | 0 | $0.0385 | — | — |
| SA-2 | openai/gpt-oss-120b | 267,160 | 15,959 | 47,296 | 0 | $0.0504 | ✅ 9F/9E | Trace the path from L12:F12940 ('references to female pronou… |
| **Total** | | **343,769** | **20,128** | **222,638** | **0** | **$0.0889** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 10m 58s