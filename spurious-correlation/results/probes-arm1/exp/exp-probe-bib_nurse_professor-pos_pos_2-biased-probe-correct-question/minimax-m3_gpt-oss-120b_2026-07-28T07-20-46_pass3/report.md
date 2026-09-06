# Circuit Oracle Report
**Date:** 2026-07-28 07:20:46 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by a cascade of female-gender/female-pronoun features that fire on tokens like "She", "her", and "herself", with only a marginal contribution from genuine nursing/medical profession features.

**Confidence:** 9

**Reasoning:** The user's concern is clearly confirmed by the attribution graph. The circuit traces from late-layer women-reference aggregators backward through a pronoun/gender cascade:

- **Late-layer aggregators (L18–L19):** L18:F14677 ("instances of women or girls being mentioned", frac_nonzero=0.012) fires at positions 1, 19, and 50 — exactly the locations of "She" tokens — with direct_effect up to 0.377. L19:F9685 ("references to women's names and their roles", frac_nonzero=0.014) is a sibling aggregator firing on "She" at pos 19 and at pos 140. Both features' **promoted tokens are exclusively feminine pronouns (she/her/herself)** and they **suppress masculine pronouns (him/his/himself)**. Their top-activating examples are all "She...she...she" passages about female subjects, with NO nursing content.

- **Mid-layer female-reference features (L6–L7):** L6:F11646 ("references to women... pronouns and titles", frac_nonzero=0.020) is the single largest direct contributor (direct_effect 0.498 on pos 1) and fires on every "She" instance in the prompt. Its upstream chain traces through L0:F9519 ("the pronoun 'she' and possessive 'her'") and L1:F2848 (dedicated "she/her" detector) all the way back to the **Emb: She (pos 1)** token embedding, with direct_effect 19.25 from the embedding alone. L6:F16329 ("female first names and their possessive forms") and L5:F5996 ("words associated with females, femininity or womanhood") are gender-specific suppressors (note the **negative direct_effect of -0.207 and -0.206** — these features actively *push against* the "feminine" classification, suggesting the probe is trying to *predict female-as-positive*).

- **The nursing/medical signal is weak and conflicted:** L6:F15267 at pos 10 is the lone profession-relevant feature with direct_effect 0.473. Its autointerp label IS "words in the document referring to the profession of nursing" and its top-activating examples show "RN", "nurse", "nurse managers" — genuinely a nursing detector. However, the SAME position (10) is also where L7:F8644 ("a woman's name in a variety of contexts", promotes himself/suppresses herself) fires with **negative** direct_effect -0.285, and where L6:F170 ("academic fields... humanities") fires. The "Nursing" token embedding is shared by *both* the genuine nursing feature and the gender cascade — meaning the "Nursing" word itself carries female connotations in this model's representation.

- **L14:F3985** is the only mid-layer feature with a clear medical/management label ("terms related to management, leadership, medicine, studies, and research", promoted tokens: patients/Medical/clinical), but its direct_effect on the probe is only 0.204 — an order of magnitude smaller than the gender-driven contributions.

- **Causal path summary:** Emb:"She"(pos1) → L0:F9519 + L1:F2848 + L2:F7672 → L4:F7864 + L4:F15317 → L6:F11646 (0.498 direct_effect) → L12:F12940 + L18:F14677 (0.377) → output. Concurrently, Emb:"Nursing"(pos10) → L6:F15267 (0.473) → L14:F3985 (0.204) → output, but this profession path is overshadowed by the gender path which fires at *multiple* "She" positions (1, 2, 19, 50) simultaneously.

**The user is correct:** the probe is predominantly using gender/pronoun features as its signal. A male nurse with the same biography rephrased with "He" would likely score differently on this probe, confirming the spurious-correlation concern. The nursing profession signal is present but secondary.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: ' She' (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: ' Nursing' (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' graduated' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 81 | Emb: ' her' (pos 81) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 19 | Low-layer pronoun/gender detectors (L0–L5) | the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 19 | Low-layer pronoun/gender detectors (L0–L5) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F16075](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) | 15 | Low-layer pronoun/gender detectors (L0–L5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) |
| [L1:F2848](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2848) | 1 | Low-layer pronoun/gender detectors (L0–L5) | the pronouns "she" and "her" (and sometimes "his") | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2848) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | Low-layer pronoun/gender detectors (L0–L5) | pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, *ele*, and *ela* across multiple languages. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Low-layer pronoun/gender detectors (L0–L5) | mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Low-layer pronoun/gender detectors (L0–L5) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Low-layer pronoun/gender detectors (L0–L5) | named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 140 | Low-layer pronoun/gender detectors (L0–L5) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Low-layer pronoun/gender detectors (L0–L5) | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L5:F5996](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) | 81 | Low-layer pronoun/gender detectors (L0–L5) |  words associated with females, femininity or womanhood | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer female-reference features (L6–L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer female-reference features (L6–L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 19 | Mid-layer female-reference features (L6–L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 81 | Mid-layer female-reference features (L6–L7) |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Mid-layer female-reference features (L6–L7) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 19 | Mid-layer female-reference features (L6–L7) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | Mid-layer female-reference features (L6–L7) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 10 | Mid-layer female-reference features (L6–L7) |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | Mid-layer female-reference features (L6–L7) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 10 | Mid-layer female-reference features (L6–L7) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 10 | Mid-layer female-reference features (L6–L7) | words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 10 | Mid-layer female-reference features (L6–L7) | text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-layer female-reference features (L6–L7) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 19 | Mid-layer female-reference features (L6–L7) | personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | Mid-layer female-reference features (L6–L7) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 19 | Mid-layer female-reference features (L6–L7) | references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F3679](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) | 140 | Mid-layer female-reference features (L6–L7) | unknown (auto‑interp not provided) | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer women/pronoun aggregators (L18–L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 19 | Late-layer women/pronoun aggregators (L18–L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 50 | Late-layer women/pronoun aggregators (L18–L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 19 | Late-layer women/pronoun aggregators (L18–L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 140 | Late-layer women/pronoun aggregators (L18–L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 10 | Minor medical/management signal (L14) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.498 |

### Dispatch: 9 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 3 | 3 | Trace L6:F11646 at position 1 (fires on 'She') - does this encode a gender marke… |
| SA-2 | `L6:F15267@10` | ❌ error | — | — | Trace L6:F15267 at position 10 (likely 'She' or beginning of a sentence about nu… |
| SA-3 | `L18:F14677@19` | ✅ reported | 6 | 6 | Trace L18:F14677 at position 19 - what does this late-layer feature encode? Does… |
| SA-4 | `L4:F15317@2` | ✅ reported | 4 | 7 | Trace L4:F15317 at position 2. Does this encode a pronoun/gender signal or somet… |
| SA-5 | `L4:F7864@1` | ✅ reported | 4 | 4 | Trace L4:F7864 at position 1 (likely 'She'). What does this feature encode? |
| SA-6 | `L12:F12940@2` | ✅ reported | 3 | 4 | Trace L12:F12940 at position 2. Does this encode profession (nurse) or gender? |
| SA-7 | `L19:F9685@140` | ✅ reported | 4 | 5 | Trace L19:F9685 at position 140. What does this late-layer feature encode? |
| SA-8 | `L0:F16075@15` | ❌ error | — | — | Trace L0:F16075 at position 15. This is at the embedding layer. What token does … |
| SA-9 | `L14:F3985@10` | ✅ reported | 6 | 10 | Trace L14:F3985 at position 10. Does this encode a medical/nursing concept or ge… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 5 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 6 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |

**Findings:** The target feature L6:F11646 fires on the token 'She'. Its autointerp label points to references to women, and its promoted tokens are explicitly female pronouns. Upstream, the strongest positive driver is the raw embedding of the token 'She' (direct_effect 19.25). The next strongest upstream driver is a lower‑layer (layer 4) feature F7864 (direct_effect 4.41), which despite a label about code sni…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@19, k=10 | Emb:" She"@19 (de=15.31) +9 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 7 | `get_upstream_features` | L6:F11646@19, k=10 | Emb:" She"@19 (de=19.00) +9 more |
| 8 | `get_upstream_features` | L17:F5889@19, k=10 | Emb:" She"@19 (de=21.38) +9 more |
| 9 | `get_upstream_features` | L15:F3330@19, k=10 | Emb:" She"@19 (de=18.00) +9 more |
| 10 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 11 | `get_upstream_features` | L0:F15382@19, k=5 | Emb:" She"@19 (de=23.62) +4 more |

**Findings:** The traced circuit shows that L18:F14677 is a high‑level gender‑related feature. Its strongest upstream drivers are the token embedding for the word "She" and a cascade of lower‑layer pronoun detectors (L17:F5889, L6:F11646, L0:F15382, L0:F9519). These upstream nodes are all explicitly about female pronouns or mentions, with no evidence of nursing/medical terminology. Consequently, L18:F14677 enco…

</details>

<details>
<summary><b>SA-4</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 2 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=10.94) +9 more |
| 3 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 4 | `inspect_feature` | L0, F4230 | " words related to positions in academic, professional, or sports hiera" |
| 5 | `get_upstream_features` | L2:F7672@1, k=10 | Emb:"She"@1 (de=13.88) +9 more |
| 6 | `inspect_feature` | L0, F11959 | " the word "graduated" and the word "more."" |
| 7 | `get_upstream_features` | L0:F4230@2, k=10 | Emb:" graduated"@2 (de=16.38) +9 more |

**Findings:** L4:F15317 (layer 4, feature 15317) appears to be a gender‑aware entity detector. Its autointerp label mentions generic named entities, but its promoted tokens heavily favor female pronouns (she, her, herself) and it suppresses male pronouns. The strongest upstream driver is the input token embedding for "She", confirming a direct pronoun signal. Additional upstream contributors include a lower‑lay…

</details>

<details>
<summary><b>SA-5</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 2 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 3 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 4 | `get_upstream_features` | L4:F7864@1, k=20 | Emb:"She"@1 (de=24.62) +19 more |
| 5 | `inspect_feature` | L0, F3232 | " mentions of the third person plural pronoun "They"" |
| 6 | `get_upstream_features` | L2:F2128@1, k=10 | Emb:"She"@1 (de=20.25) +9 more |
| 7 | `inspect_feature` | L1, F2848 | " the pronouns "she" and "her" (and sometimes "his")" |

**Findings:** Tracing from L4:F7864 (pos 1) reveals that its strongest upstream driver is the raw token embedding for "She" (direct effect ≈ 24.6). The feature inherits a gendered pronoun signal via a cascade: a generic pronoun detector in layer 2 (F2128) receives a positive boost from a dedicated feminine‑pronoun detector in layer 1 (F2848). A minor contribution also arrives from a layer‑0 plural‑pronoun detec…

</details>

<details>
<summary><b>SA-6</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:" graduated"@2 (de=4.81) +9 more |
| 3 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=10.94) +9 more |
| 6 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 7 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 8 | `get_upstream_features` | L6:F11646@2, k=10 | L4:F15317 (de=5.94) +9 more |

**Findings:** The traced circuit shows L12:F12940 is driven primarily by female pronoun signals. Upstream, a gender‑specific embedding ("She") feeds a named‑entity detector (L4:F15317), which in turn strongly activates the target. Additional positive upstream contributions come from a women‑reference feature at layer 6 and the input token "graduated". No upstream feature indicating a profession such as "nurse" …

</details>

<details>
<summary><b>SA-7</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@140, k=10 | L4:F1276 (de=1.45) +9 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `inspect_feature` | L5, F5996 | " words associated with females, femininity or womanhood" |
| 5 | `inspect_feature` | L4, F1302 | " parts of names or titles, sometimes followed by numbers" |

**Findings:** L19:F9685 is a gender‑specific feature that lights up when female names or roles are referenced. Its strongest upstream drivers are low‑layer name‑detector features (L4:F1276 and L4:F1302) that recognise capitalised name tokens and name fragments, as well as direct input embeddings for the pronoun "She" and the profession token " Nursing". The pathway therefore routes from raw gendered tokens and …

</details>

<details>
<summary><b>SA-9</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@10, k=10 | Emb:" Nursing"@10 (de=12.12) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 5 | `get_upstream_features` | L8:F16339@10, k=10 | Emb:" Nursing"@10 (de=7.66) +9 more |
| 6 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 7 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 8 | `get_upstream_features` | L7:F210@10, k=10 | Emb:" Nursing"@10 (de=8.19) +9 more |

**Findings:** The traced circuit shows a strong nursing/medical signal. The raw embedding "Nursing" is the top upstream driver (direct_effect >12) feeding into L14:F3985. Upstream features in layers 8,7,6 all relate to hospital, healthcare system, and explicitly to the nursing profession. No gender‑related tokens or features appear. Therefore L14:F3985 encodes a medical/nursing concept, not a gender concept.

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×9 | L6:15267, L7:8644, L18:14677, L6:11646, L6:4490, L6:8166, L6:16329, L6:170, L5:5996 |
| 2 | `get_upstream_features` | L19:F9685@19, k=5 → Emb:" She"@19 (de=6.19) +4 more |
| 3 | `get_upstream_features` | L6:F15267@10, k=5 → Emb:" Nursing"@10 (de=17.38) +4 more |
| 4 | `get_upstream_features` | L6:F11646@19, k=5 → Emb:" She"@19 (de=19.00) +4 more |
| 5 | `get_upstream_features` | L6:F15267@1, k=5 → ❌ Feature (layer=6, feature_idx=15267) not found at pos=1. Thi |
| 6 | `get_upstream_features` | L12:F12940@2, k=5 → Emb:" graduated"@2 (de=4.81) +4 more |
| 7 | `get_upstream_features` | L18:F14677@1, k=5 → Emb:"She"@1 (de=27.12) +4 more |
| 8 | `inspect_feature` ×3 | L4:8751, L4:11037, L19:9685 |

### Build

`build_circuit` → 11 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 33,439 | 5,463 | 190,769 | 0 | $0.0280 | — | — |
| SA-1 | openai/gpt-oss-120b | 48,429 | 3,022 | 5,632 | 0 | $0.0092 | ✅ 3F/3E | Trace L6:F11646 at position 1 (fires on 'She') - does this e… |
| SA-4 | openai/gpt-oss-120b | 64,919 | 4,661 | 5,152 | 0 | $0.0126 | ✅ 4F/7E | Trace L4:F15317 at position 2. Does this encode a pronoun/ge… |
| SA-5 | openai/gpt-oss-120b | 64,608 | 3,730 | 5,056 | 0 | $0.0120 | ✅ 4F/4E | Trace L4:F7864 at position 1 (likely 'She'). What does this … |
| SA-7 | openai/gpt-oss-120b | 40,577 | 2,723 | 5,056 | 0 | $0.0078 | ✅ 4F/5E | Trace L19:F9685 at position 140. What does this late-layer f… |
| SA-6 | openai/gpt-oss-120b | 81,687 | 4,031 | 5,056 | 0 | $0.0147 | ✅ 3F/4E | Trace L12:F12940 at position 2. Does this encode profession … |
| SA-9 | openai/gpt-oss-120b | 64,965 | 5,423 | 16,096 | 0 | $0.0132 | ✅ 6F/10E | Trace L14:F3985 at position 10. Does this encode a medical/n… |
| SA-3 | openai/gpt-oss-120b | 130,986 | 5,590 | 12,768 | 0 | $0.0232 | ✅ 6F/6E | Trace L18:F14677 at position 19 - what does this late-layer … |
| **Total** | | **529,610** | **34,643** | **245,585** | **0** | **$0.1208** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 25s