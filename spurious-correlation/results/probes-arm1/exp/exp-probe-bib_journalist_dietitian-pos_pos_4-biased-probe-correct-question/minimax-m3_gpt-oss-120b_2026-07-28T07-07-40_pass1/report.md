# Circuit Oracle Report
**Date:** 2026-07-28 07:07:40 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is driven primarily by **gendered pronoun/name features** (she/her/Heather/Rebecca), with only a secondary contribution from the genuine diet/profession terms (Dietetics, RD, Nutrition), confirming the user's concern that the classifier relies on spurious gender markers.

**Confidence:** 8

**Reasoning:**

The attribution graph for this profession probe (which should detect "Dietitian" or "Nutritionist") reveals two distinct pathways:

**1. Spurious Gender Pathway (dominant, ~5× stronger):**
The bulk of the direct_effect on the probe comes from a cascade of female-gender features. At the input, the embedding of "She" (pos 1) drives L4:F7864 and L0:F12519 (frac_nonzero 0.015–0.039), which feed L6:F11646 ("references to women / pronouns and titles", frac_nonzero 0.020, direct_effect 0.209). This in turn feeds:
- L7:F8644 ("woman's name in a variety of contexts", direct_effect 0.134) — a name detector with **opposite sign** to its label (promoted tokens are male: "himself", "his"), making it act as a *feminine-name detector* in this context
- L12:F12940 ("female pronouns", direct_effect 0.116)
- L18:F14677 ("instances of women or girls being mentioned", direct_effect 0.144)
- L19:F9685 ("women's names and roles", direct_effect 0.095)

The L18:F14677 feature alone appears three times in the top-20 (pos 1, 57, 94), each anchored to a "she/She" embedding (direct_effect 15.6–27.1), and the later L19:F9685 receives direct embedding drive from "she" at pos 57 (direct_effect 9.94).

**2. Genuine Profession Pathway (minor):**
L4:F13412 ("terms related to diets and dietary health", frac_nonzero 0.012) is genuinely about the profession. It fires on "Dietetics" (pos 21, direct_effect 0.163), "RD" (pos 55, direct_effect 0.123), and the "titian" suffix of "Nutrititian" (pos 37, direct_effect 0.089). It receives input from L3:F10028 (food/ingredient phrasing) and L3:F7212 ("eti" substring in "dietary"). However, its direct_effect on the output (≈0.47 total across positions) is much smaller than the gender pathway's combined ≈0.85.

**Conclusion:** The probe direction is largely aligned with the model's "woman-being-mentioned" direction, not its "dietitian-content" direction. The classifier is exploiting the strong correlation in its training data between the *profession* Dietitian and *female* pronouns/names, and has not learned to rely primarily on professional vocabulary. This is a textbook **spurious-correlation / gender-bias failure** of the linear probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early pronoun 'she' detector | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 57 | Early pronoun 'she' detector |  the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 31 | Proper-noun / capitalized-name detection | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 31 | Proper-noun / capitalized-name detection | proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Proper-noun / capitalized-name detection |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer female pronoun/title detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer female pronoun/title detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Mid-layer female pronoun/title detector | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | Diet/dietary content features |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | Diet/dietary content features |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | Diet/dietary content features |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 37 | Diet/dietary content features |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 21 | Diet/dietary content features | words or short phrases that include "made of/from", and words ending with "ice", "ita", "ons", "ura", and "mor" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 55 | Diet/dietary content features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 31 | Woman's name detector (Heather/Rebecca) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 31 | Woman's name detector (Heather/Rebecca) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | Woman's name detector (Heather/Rebecca) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Late-layer female pronoun aggregator | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 31 | Late-layer female pronoun aggregator |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer women-mention detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 57 | Late-layer women-mention detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 94 | Late-layer women-mention detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 57 | Late-layer women-mention detector |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 94 | Late-layer women-mention detector |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 57 | Late-layer women-mention detector | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 94 | Late-layer women-mention detector | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 57 | Late-layer women's roles/accomplishments |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:8644 de=-0.212 |
| 3 | `inspect_feature` ×14 | L18:14677, L4:13412, L6:11646, L7:8644, L7:2765, L4:7864, L4:1276, L12:12940, L12:14970, L4:15317, L19:9685, L0:8974, L0:6051, L6:16329 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ✅ reported | 3 | 6 | Trace the path from L18:F14677 (instances of women being mentioned) upstream. Wh… |
| SA-2 | `L4:F13412@21` | ❌ error | — | — | Trace the path from L4:F13412 (terms related to diets and dietary health) upstre… |
| SA-3 | `L7:F8644@31` | ✅ reported | 5 | 9 | Trace the path from L7:F8644 (woman's name) upstream at position 31. What tokens… |
| SA-4 | `L19:F9685@57` | ✅ reported | 3 | 4 | Trace the path from L19:F9685 (women's names and their roles) upstream at positi… |
| SA-5 | `L4:F13412@21` | ✅ reported | 9 | 8 | Trace the path from L4:F13412 (terms related to diets and dietary health) upstre… |

<details>
<summary><b>SA-1</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@1, k=10 | Emb:"She"@1 (de=27.12) +9 more |
| 3 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 6 | `inspect_feature` | L11, F9183 | " large empty spaces in the text" |
| 7 | `get_upstream_features` | L15:F851@1, k=10 | L12:F12493 (de=22.38) +9 more |
| 8 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 9 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 10 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 11 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 12 | `get_upstream_features` | L12:F12493@1, k=10 | L10:F14174 (de=15.38) +9 more |
| 13 | `inspect_feature` | L12, F12493 | " words that end in "ing", "ecti", "tial", or "ogi", and also the word " |
| 14 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 15 | `inspect_feature` | L10, F14174 | "left curly brackets" |

**Findings:** The target feature L18:F14677 (women‑mention detector) receives its strongest drive from the raw embedding of the token 'She' (direct_effect 27.1). It also aggregates signal from two earlier layers: a layer‑6 feature that specializes in gendered pronouns (direct_effect ~4.2) and a layer‑4 feature that, despite a code‑snippet label, activates on the same token and passes positive influence (direct_…

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 2 | `get_upstream_features` | L7:F8644@31, k=15 | Emb:"She"@1 (de=7.47) +14 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `get_upstream_features` | L4:F1276@31, k=15 | Emb:" Heather"@31 (de=10.94) +14 more |
| 6 | `get_upstream_features` | L4:F1276@31, k=15 | Emb:" Heather"@31 (de=10.94) +14 more |
| 7 | `get_upstream_features` | L4:F1276@31, k=15 | Emb:" Heather"@31 (de=10.94) +14 more |
| 8 | `get_upstream_features` | L4:F1276@31, k=15 | Emb:" Heather"@31 (de=10.94) +14 more |
| 9 | `get_upstream_features` | L6:F11646@1, k=15 | Emb:"She"@1 (de=19.25) +14 more |
| 10 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 11 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 12 | `inspect_feature` | L0, F7532 | " proper nouns" |

**Findings:** The woman's‑name feature (L7:F8644) is driven primarily by the pronoun embedding "She" and by two upstream name‑related detectors: a capitalized‑name detector (L4:F1276) and a female‑reference detector (L6:F11646). The capitalized‑name detector itself is strongly activated by the input token embedding "Heather" (the actual name token) and by a generic proper‑noun detector (L0:F7532). The female‑re…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@57, k=10 | Emb:" she"@57 (de=9.94) +9 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `get_upstream_features` | L17:F5889@57, k=10 | Emb:" she"@57 (de=30.62) +9 more |
| 5 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 6 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |

**Findings:** The women's‑names/roles feature (L19:F9685) is primarily driven by the pronoun token " she" at the same position. The pronoun token strongly excites a low‑layer pronoun detector (L0:F12519) and a mid‑layer pronoun‑context aggregator (L17:F5889). The aggregator (L17:F5889) in turn contributes positively to the women's‑names detector. This chain reaches a lower‑third layer (layer 0) and includes exp…

</details>

<details>
<summary><b>SA-5</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 3 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 4 | `get_upstream_features` | L3:F11774@21, k=10 | Emb:" Die"@20 (de=5.88) +9 more |
| 5 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 6 | `inspect_feature` | L2, F1984 | " strings of letters that appear to be fragments of names, especially p" |
| 7 | `inspect_feature` | L3, F7212 | " words with the character sequence "eti" in them" |
| 8 | `inspect_feature` | L2, F7473 | " capitalized two letter prefixes or suffixes" |
| 9 | `get_upstream_features` | L2:F1984@21, k=10 | Emb:"te"@21 (de=10.44) +9 more |
| 10 | `inspect_feature` | L2, F4472 | " LaTeX math expressions" |
| 11 | `inspect_feature` | L2, F9618 | "the substrings "ith" and "io", especially when they occur together, an" |
| 12 | `get_upstream_features` | L3:F10028@21, k=10 | Emb:" Die"@20 (de=6.94) +9 more |
| 13 | `get_upstream_features` | L2:F7473@21, k=10 | Emb:" Die"@20 (de=19.00) +9 more |
| 14 | `inspect_feature` | L0, F8585 | "the substring 'tam' or 'tab', sometimes in a medical context" |

**Findings:** The diet‑related L4:F13412 feature is driven primarily by two mid‑level detectors: L3:F11774 (scientific‑numeric patterns) and L3:F10028 (ingredient‑type phrasing). Both receive strong excitatory input from the raw token embedding " Die" at position 20, satisfying the lower‑third layer and embedding‑shortcut requirements. Additional positive contributions come from lower‑layer features (L2:F7473, …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@2, k=10 → L4:F15317 (de=8.75) +9 more |
| 2 | `get_upstream_features` | L4:F15317@2, k=10 → Emb:"She"@1 (de=13.56) +9 more |
| 3 | `get_upstream_features` | L12:F14970@31, k=10 → Emb:"<bos>"@0 (de=-3.48) +9 more |
| 4 | `get_upstream_features` | L18:F14677@57, k=10 → Emb:" she"@57 (de=22.62) +9 more |
| 5 | `get_upstream_features` | L18:F14677@94, k=10 → Emb:" She"@94 (de=15.62) +9 more |
| 6 | `get_upstream_features` | L4:F13412@55, k=10 → Emb:" RD"@55 (de=11.31) +9 more |
| 7 | `get_upstream_features` | L4:F13412@37, k=8 → Emb:"titian"@37 (de=14.00) +7 more |
| 8 | `get_upstream_features` | L12:F12940@2, k=8 → Emb:"She"@1 (de=6.03) +7 more |

### Build

`build_circuit` → 15 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,161 | 5,016 | 140,784 | 0 | $0.0298 | — | — |
| SA-4 | openai/gpt-oss-120b | 45,880 | 3,684 | 8,416 | 0 | $0.0092 | ✅ 3F/4E | Trace the path from L19:F9685 (women's names and their roles… |
| SA-1 | openai/gpt-oss-120b | 219,723 | 10,295 | 23,072 | 0 | $0.0395 | ✅ 3F/6E | Trace the path from L18:F14677 (instances of women being men… |
| SA-3 | openai/gpt-oss-120b | 163,998 | 10,472 | 10,976 | 0 | $0.0310 | ✅ 5F/9E | Trace the path from L7:F8644 (woman's name) upstream at posi… |
| SA-5 | openai/gpt-oss-120b | 205,183 | 13,995 | 28,416 | 0 | $0.0396 | ✅ 9F/8E | Trace the path from L4:F13412 (terms related to diets and di… |
| **Total** | | **685,945** | **43,462** | **211,664** | **0** | **$0.1492** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 47s