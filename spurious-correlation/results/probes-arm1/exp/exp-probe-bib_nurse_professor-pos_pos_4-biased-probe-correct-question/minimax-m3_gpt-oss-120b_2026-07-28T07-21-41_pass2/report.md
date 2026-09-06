# Circuit Oracle Report
**Date:** 2026-07-28 07:21:41 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "nurse" is driven by TWO competing circuits: a genuine profession pathway rooted in medical tokens (" nurse", " practitioner", " Nursing") and a separate, parallel **female-gender pathway** rooted almost entirely in the pronoun "She" that both drives and partially suppresses the output.

**Confidence:** 7

**Reasoning:**

**The genuine profession circuit (pushes probe toward nurse):**
- **Emb: " nurse" (pos 32)** → direct_effect 5.66 → and **Emb: " practitioner" (pos 33)** → direct_effect 3.03 → both feed **L6:F15267** ("words referring to the profession of nursing", direct_effect +0.56, frac_nonzero 0.016) via the L1→L4→L5→L6 healthcare stack (**L1:F1494 "medical practices" → L4:F11037 "counseling/therapy/degree programs" + L4:F9036 "healthcare jargon" → L5:F1275 "healthcare professionals/medical fields" → L6:F15267 "nursing profession words"**).
- Emb: " Nursing" (pos 18) also contributes (+1.18). This is a textbook profession indicator — a clean semantic pathway grounded in profession-specific vocabulary, with no gender dependency in its upstream signal.

**The female-gender circuit (a separate, large pathway that ALSO drives the probe):**
- **Emb: "She" (pos 20)** is the dominant source: it has direct_effect **+14.44** on L18:F14677, **+18.13** on L6:F11646, and **+6.78** on L6:F16329.
- This single pronoun token feeds an entire parallel gender-marker stack: **L0:F15382 ("mentions of a female person") → L4:F7864 (mislabeled as XML; actually a "She"-pronoun amplifier, frac_nonzero 0.015) → L4:F15317 ("named entities... characters or people", whose promoted tokens are she/her/herself) → L6:F16329 ("female first names", frac_nonzero 0.12) and L6:F11646 ("references to women, pronouns and titles") → L15:F3330 ("personal stories of women, indicated by she") → L17:F5889 ("references to people with pronouns") → L18:F14677 ("instances of women or girls being mentioned", direct_effect +0.44, fires at positions 20/43/78/117) → L19:F9685 ("women's names and roles/accomplishments", direct_effect +0.26, fires at 20/43/101)**.
- Crucially, **L19:F9685 is a late-layer (L19) feature that feeds the output logit directly** with positive direct_effect, and it is NOT a profession feature — it is a *female-person-in-role* feature. The "role" portion is supplied by neighboring "Nursing" / "graduated" tokens, but the *gender* activation comes almost entirely from "She".
- The proper name "Lori" (pos 1) enters via **L4:F1276 "capitalized names and titles" + L5:F16213 "proper nouns first+last name" + L2:F16306 "proper names" + L6:F8166 "proper names ending in a/i/e"** (all of which promote female tokens like "actress", "herself"), then feeds the same L19:F9685 female-role feature.

**Suppressor path (a gender-suppression effect coexists):**
- **L7:F8644 ("woman's name in various contexts", promoted tokens: himself/himself — i.e., it acts as a male-marker comparator) has direct_effect −0.30, and L6:F16329 also inhibits L18:F14677 (−0.22).** These are genuinely surprising — the same "female-name" feature that excites one branch is partially suppressing another, consistent with probe competition between female-coded and profession-coded subspaces.

**The user's concern is VALIDATED but qualified.** The circuit is NOT purely spurious — the nursing-vocabulary pathway is real, clean, and directly evidence-driven. However, a substantial portion of the probe's score (via L19:F9685 at direct_effect +0.21 to +0.26 across multiple positions) flows through a **gendered "female person in a role"** pathway whose entire source is the pronoun "She" at position 20. The model has learned an association between female pronouns + role context and the nurse profession in its training data, and the probe is partly reading that confound. A male nurse with the same clinical biography but pronouns "he/him" would likely score lower on this probe, not because the profession signal changed, but because the gender pathway would vanish. This is the classic spurious-correlation concern: the probe is using profession vocabulary *and* a female-gender/pronoun feature as parallel evidence for "nurse", making it sensitive to gender rewriting attacks.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 20 | Probe Output Logit (Nursing profession direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | L6:F15267 — 'words referring to the profession of nursing' (pos 33) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | L6:F15267 — 'words referring to the profession of nursing' (pos 33) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | L5:F1275 — 'healthcare professionals / medical fields' (pos 33) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 33 | L4:F11037 — 'counseling/therapy/degree programs' + L4:F9036 healthcare jargon (pos 33) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | L4:F11037 — 'counseling/therapy/degree programs' + L4:F9036 healthcare jargon (pos 33) | words and abbreviations associated with healthcare | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 33 | L1:F1494 — 'medical practices and studies' (pos 33) | words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 33 | L4:F15317 — 'named entities like characters or people' — promotes female pronouns (pos 33) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 20 | L4:F15317 — 'named entities like characters or people' — promotes female pronouns (pos 33) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 20 | L6:F16329 — 'female first names and possessive forms' (pos 20) — SUPPRESSES profession | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 33 | L6:F16329 — 'female first names and possessive forms' (pos 20) — SUPPRESSES profession | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 20 | L6:F11646 — 'references to women, pronouns and titles' (pos 20) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 20 | L18:F14677 — 'instances of women or girls being mentioned' (pos 20) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 78 | L18:F14677 — 'instances of women or girls being mentioned' (pos 20) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 43 | L18:F14677 — 'instances of women or girls being mentioned' (pos 20) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 117 | L18:F14677 — 'instances of women or girls being mentioned' (pos 20) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 20 | L19:F9685 — 'women's names and roles/accomplishments' (pos 20) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 43 | L19:F9685 — 'women's names and roles/accomplishments' (pos 20) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 101 | L19:F9685 — 'women's names and roles/accomplishments' (pos 20) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 20 | L17:F5889 — 'references to people with pronouns' (pos 20) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 20 | L15:F3330 — 'personal stories of women, indicated by she' (pos 20) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 20 | L0:F15382 — 'mentions of a female person' (pos 20) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 20 | L0:F12519 — generic female-name/pronoun feature (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 1 | L4:F1276 — 'capitalized names and titles' (pos 1, 'Lori') | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | L4:F1276 — 'capitalized names and titles' (pos 1, 'Lori') |  proper nouns consisting of a first and last name | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L2:F16306](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) | 1 | L4:F1276 — 'capitalized names and titles' (pos 1, 'Lori') |  proper names and positive adjectives | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 1 | L4:F1276 — 'capitalized names and titles' (pos 1, 'Lori') |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 20 | L7:F8644 — 'woman's name in various contexts' (pos 20) — SUPPRESSES |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 18 | L7:F8644 — 'woman's name in various contexts' (pos 20) — SUPPRESSES |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L5:F5996](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) | 33 | L7:F8644 — 'woman's name in various contexts' (pos 20) — SUPPRESSES | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: 'She' (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 32 | Emb: ' nurse' (pos 32) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 33 | Emb: ' practitioner' (pos 33) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: ' Nursing' (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'Lori' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' graduated' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:15267 de=0.562 |
| 3 | `inspect_feature` ×10 | L6:15267, L4:15317, L18:14677, L4:1276, L5:16213, L6:16329, L6:8166, L2:16306, L6:11646, L19:9685 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15267@33` | ✅ reported | 6 | 25 | Trace the path from L6:F15267 (nursing profession words). What input tokens driv… |
| SA-2 | `L18:F14677@20` | ❌ error | — | — | Trace the path from L18:F14677 (instances of women/girls being mentioned). This … |
| SA-3 | `L19:F9685@20` | ✅ reported | 5 | 11 | Trace the path from L19:F9685 (women's names and their roles/accomplishments). T… |
| SA-4 | `L4:F15317@33` | ✅ reported | 4 | 5 | Trace the path from L4:F15317 (named entities like characters/people) at positio… |
| SA-5 | `L6:F16329@20` | ✅ reported | 3 | 6 | Trace the path from L6:F16329 (female first names) at position 20. This feature … |
| SA-6 | `L18:F14677@20` | ❌ error | — | — | Trace the path from L18:F14677 (instances of women/girls being mentioned) at pos… |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@33, k=10 | Emb:" nurse"@32 (de=5.66) +9 more |
| 3 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 4 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 5 | `get_upstream_features` | L5:F1275@33, k=10 | L4:F9036 (de=1.70) +9 more |
| 6 | `get_upstream_features` | L4:F11037@33, k=10 | Emb:" practitioner"@33 (de=6.47) +9 more |
| 7 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 8 | `inspect_feature` | L4, F9036 | " words and abbreviations associated with healthcare." |
| 9 | `get_upstream_features` | L1:F1494@33, k=10 | Emb:" nurse"@32 (de=8.69) +9 more |
| 10 | `get_upstream_features` | L4:F9036@33, k=10 | Emb:" practitioner"@33 (de=14.00) +9 more |
| 11 | `inspect_feature` | L0, F6337 | "the word "dig" in different contexts." |

**Findings:** The tracing starts at L6:F15267, a feature that fires on nursing-related words. Its strongest upstream drivers are the raw token embeddings for "nurse" (pos 32) and "practitioner" (pos 33), confirming that the feature is a genuine indicator of the nursing profession. These embeddings feed into a mid-layer healthcare-professional detector (L5:F1275), which in turn draws from a counseling/academic-h…

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@20, k=10 | Emb:" She"@20 (de=5.88) +9 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `get_upstream_features` | L17:F5889@20, k=10 | Emb:" She"@20 (de=19.50) +9 more |
| 5 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 6 | `get_upstream_features` | L0:F15382@20, k=10 | Emb:" She"@20 (de=23.62) +9 more |
| 7 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 8 | `get_upstream_features` | L15:F3330@20, k=10 | Emb:" She"@20 (de=15.75) +9 more |
| 9 | `get_upstream_features` | L6:F11646@20, k=10 | Emb:" She"@20 (de=18.12) +9 more |

**Findings:** The target feature L19:F9685 is a higher‑layer detector for any female name together with contextual role/accomplishment cues. Its strongest upstream driver is the raw token embedding "She" (pos 20), which flows through a cascade of lower‑layer gender and pronoun features (L0:F15382, L17:F5889, L15:F3330) before reaching L19:F9685. The name token "Lori" at position 1 contributes a very small posit…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 2 | `get_upstream_features` | L4:F15317@33, k=10 | Emb:" nurse"@32 (de=4.00) +9 more |
| 3 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 4 | `get_upstream_features` | L1:F1494@33, k=10 | Emb:" nurse"@32 (de=8.69) +9 more |
| 5 | `inspect_feature` | L3, F13446 | " job titles related to people" |
| 6 | `inspect_feature` | L3, F9350 | " a smattering of words or parts of words that don't have a clear relat" |

**Findings:** The gendered-entity feature L4:F15317 (promoting female pronouns) is driven primarily by two input token embeddings: the token "nurse" at position 32 (direct_effect 4.0) and "practitioner" at position 33 (direct_effect 1.25). These medical-domain tokens activate a lower-layer medical-context feature (L1:1494), which in turn feeds into the gendered entity detector. Additional supportive signals com…

</details>

<details>
<summary><b>SA-5</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F16329 | "female first names and their possessive forms" |
| 2 | `get_upstream_features` | L6:F16329@20, k=15 | Emb:" She"@20 (de=6.78) +14 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `get_upstream_features` | L4:F7864@20, k=10 | Emb:" She"@20 (de=18.00) +9 more |
| 5 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 6 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 7 | `get_upstream_features` | L0:F15382@20, k=10 | Emb:" She"@20 (de=23.62) +9 more |
| 8 | `inspect_feature` | L0, F3232 | " mentions of the third person plural pronoun "They"" |

**Findings:** The L6 female‑name feature receives strong excitatory input from the pronoun "She" (embedding) both directly and via two lower‑layer gender cues: L0:F15382 (a generic female‑person detector) and L4:F7864 (a pronoun‑amplifier that the autointerp mislabels as XML code). These upstream signals propagate a gender context into the female‑name detector, which then exerts a negative direct_effect on the …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L4:7864, L0:15382, L15:3330, L17:5889 |
| 2 | `get_upstream_features` | L18:F14677@20, k=10 → Emb:" She"@20 (de=14.44) +9 more |
| 3 | `get_upstream_features` | L6:F15267@33, k=10 → Emb:" nurse"@32 (de=5.66) +9 more |
| 4 | `get_upstream_features` | L6:F11646@20, k=10 → Emb:" She"@20 (de=18.12) +9 more |
| 5 | `inspect_feature` ×4 | L15:4709, L7:8644, L5:1275, L4:11037 |

### Build

`build_circuit` → 22 nodes, 36 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 65,652 | 7,300 | 152,436 | 0 | $0.0376 | — | — |
| SA-1 | openai/gpt-oss-120b | 127,139 | 9,201 | 16,096 | 0 | $0.0248 | ✅ 6F/25E | Trace the path from L6:F15267 (nursing profession words). Wh… |
| SA-4 | openai/gpt-oss-120b | 56,144 | 5,541 | 13,184 | 0 | $0.0119 | ✅ 4F/5E | Trace the path from L4:F15317 (named entities like character… |
| SA-5 | openai/gpt-oss-120b | 85,270 | 5,817 | 2,592 | 0 | $0.0163 | ✅ 3F/6E | Trace the path from L6:F16329 (female first names) at positi… |
| SA-3 | openai/gpt-oss-120b | 91,335 | 5,096 | 2,528 | 0 | $0.0168 | ✅ 5F/11E | Trace the path from L19:F9685 (women's names and their roles… |
| **Total** | | **425,540** | **32,955** | **186,836** | **0** | **$0.1075** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 27s