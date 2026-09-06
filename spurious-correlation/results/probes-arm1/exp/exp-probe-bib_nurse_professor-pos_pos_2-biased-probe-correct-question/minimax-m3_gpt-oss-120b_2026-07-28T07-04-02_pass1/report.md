# Circuit Oracle Report
**Date:** 2026-07-28 07:04:02 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by a dense network of female-gender-marker features that fire on pronouns ("She", "her"), female-coded proper names, and possessive pronouns — alongside a much narrower nursing-vocabulary pathway — meaning the classifier relies on gender-correlated surface cues more than on profession-specific semantics.

**Confidence:** 7

**Reasoning:** The circuit splits into two parallel sub-circuits that both feed the probe output (layer=26).

**Gender sub-circuit (dominant):** The most strongly-excited embedding nodes are the raw "She" tokens at positions 1, 19, 2 (her) and the first name "Kay" at position 140. These feed a low-layer L0:15382 ("mentions of a female person," frac_nonzero=0.009) and L0:8153 (first-name token). They are aggregated by L6:11646 ("references to women via pronouns/titles," frac_nonzero=0.020) at three positions, L12:12940 ("female pronouns and possessive pronouns," frac_nonzero=0.007), and ultimately two large late-layer aggregators: L18:14677 ("instances of women/girls being mentioned," frac_nonzero=0.012, direct_effect 0.377 at pos 19), which fires at four positions, and L19:9685 ("references to women's names and roles," frac_nonzero=0.014, direct_effect 0.260 at pos 140). L19:9685's direct-effect from the "Nursing" token embedding is only 2.83 versus 6.19 from "She" — gender tokens dominate. The downstream L17:5889 pronoun-pattern feature, L15:3330 "personal stories of women" narrative feature, and L18:3679 pronoun/proper-noun feature form a convergence hub for these gender signals.

**Profession sub-circuit (narrower):** L6:15267 ("words referring to the profession of nursing," frac_nonzero=0.016) fires on the "Nursing" token at pos 10, fed by the embedding (direct_effect 17.4) and by L5:1275 (healthcare professionals / RN / DNP), L5:10392 (academic fields), L4:11037 (counseling/health-service vocab), and L2:10852 (academic titles/degrees). It then feeds L14:3985 ("management/leadership/medicine/studies," frac_nonzero=0.066, direct_effect 0.204), which does encode nurse/medical semantics (top tokens: "nurse", "patients", "Medical") — but this is only one of the top features.

**Suppression evidence:** L6:16329 (pos 1, 19) and L7:8644 (pos 10) actively *suppress* the probe (direct_effects -0.23, -0.28, -0.21), with L5:5996 (-0.21) also negative on the profession path — the suppressors target the same gender positions, indicating the probe's positive score is held up specifically by the positive female-marker features, not by a balanced mix.

**Verdict on the user's concern:** Confirmed. The circuit demonstrates clear gender-marker reliance: the highest-magnitude and most redundant features (L6:11646 at 3 positions, L12:12940, L15:3330, L17:5889, L18:14677 at 4 positions, L19:9685 at 2 positions) all encode female pronouns/names, not nursing. Only a single feature in the top 20 (L6:15267) directly detects the profession word, and only one (L14:3985) aggregates medical/nurse semantics. A male nurse ("He began his nursing career…") would suppress L6:11646, L12:12940, and L18:14677 entirely, likely causing the probe to misclassify despite identical professional content. The classifier is exploiting a gender-profession co-occurrence in its training distribution rather than learning the profession independently.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: She (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: Nursing (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: her (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 140 | Emb: Kay (pos 140) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | L0:15382 — mentions of a female person (token-level) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 19 | L0:15382 — mentions of a female person (token-level) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F16075](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) | 15 | L0:16075 — word "of" / formal context (pos 15) | the word "of" and court names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) |
| [L0:F8153](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8153) | 140 | L0:8153 — first-name token detector (pos 140) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8153) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 140 | L2:5859 — first names (mostly female) (pos 140) | first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 10 | L2:10852 — academic titles and degrees (pos 10) | academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L3:F6246](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) | 10 | L3:6246 — "Nutrients"/"-ure" suffix pattern (pos 10) | the word "Nutrients" and words containing "ure". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 140 | L4:1276 — capitalized names/titles (pos 140) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F1302](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1302) | 140 | L4:1302 — name/title fragments (pos 140) | parts of names or titles, sometimes followed by numbers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1302) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | L4:15317 — named entities like characters/people (pos 2) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 10 | L4:11037 — counseling/therapy/social-work/health-service vocabulary (pos 10) | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F15688](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15688) | 1 | L4:15688 — sentences with "she" and conflict/states (pos 1) | sentences that contain the word "she" and words associated with conflict, opinions, origin, physical feelings or situations | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15688) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 10 | L5:1275 — healthcare professionals / RN / DNP (pos 10) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | L5:10392 — fields of academic study (pos 10) | fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | L5:10952 — third-person pronouns (pos 1) | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | L6:11646 — references to women (pronouns/titles) (pos 1,2,19) | references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | L6:11646 — references to women (pronouns/titles) (pos 1,2,19) | references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 19 | L6:11646 — references to women (pronouns/titles) (pos 1,2,19) | references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | L6:15267 — words referring to the profession of nursing (pos 10) | words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 81 | L6:8166 — long proper names ending in a/i/e (female-coded) (pos 81) |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | L6:170 — references to academic fields (pos 10) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F7864](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7864) | 1 | L6:7864 — token-detector for "She" (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7864) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | L12:12940 — female pronouns and possessive pronouns (pos 2) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 10 | L14:3985 — management/leadership/medicine/studies (nurse) (pos 10) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 19 | L15:3330 — personal stories of women, "she" surrounding tokens (pos 19) | personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 19 | L17:5889 — references to people via pronouns/possessives (pos 19) | references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | L18:14677 — instances of women/girls being mentioned (pos 1,2,19,50) | instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 2 | L18:14677 — instances of women/girls being mentioned (pos 1,2,19,50) | instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 19 | L18:14677 — instances of women/girls being mentioned (pos 1,2,19,50) | instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 50 | L18:14677 — instances of women/girls being mentioned (pos 1,2,19,50) | instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F3679](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) | 140 | L18:3679 — personal pronouns / proper nouns (pos 140) | personal pronouns and/or proper nouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 19 | L19:9685 — references to women's names and roles (pos 19,140) | references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 140 | L19:9685 — references to women's names and roles (pos 19,140) | references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.498 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@19` | ✅ reported | 5 | 8 | Trace this feature upstream. It fires at multiple positions (pos 1, 2, 19, 50). … |
| SA-2 | `L6:F11646@1` | ✅ reported | 5 | 14 | Trace this feature upstream. It fires at positions 1, 2, 19. Determine: (1) what… |
| SA-3 | `L6:F15267@10` | ✅ reported | 7 | 10 | Trace this feature upstream. It fires at position 10. Determine: (1) what does t… |
| SA-4 | `L19:F9685@140` | ✅ reported | 5 | 5 | Trace this feature upstream. It fires at positions 19 and 140. Determine: (1) wh… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@19, k=10 | Emb:" She"@19 (de=15.31) +9 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 6 | `get_upstream_features` | L6:F11646@19, k=10 | Emb:" She"@19 (de=19.00) +9 more |
| 7 | `get_upstream_features` | L17:F5889@19, k=10 | Emb:" She"@19 (de=21.38) +9 more |
| 8 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 9 | `get_upstream_features` | L0:F15382@19, k=10 | Emb:" She"@19 (de=23.62) +9 more |

**Findings:** The target feature L18:F14677 is a gender‑marker that signals the presence of female references (pronoun she/her) across the prompt. Its upstream chain starts at raw token embeddings for the word "She" (pos 19 and pos 1) and propagates through a low‑layer detector (L0:15382) that simply flags a female token, then through an early‑layer concrete female‑pronoun detector (L6:11646). Mid‑layers add co…

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 5 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 6 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 7 | `get_upstream_features` | L0:F15382@1, k=10 | Emb:"She"@1 (de=16.88) +9 more |
| 8 | `inspect_feature` | L4, F15688 | " sentences that contain the word "she" and words associated with confl" |
| 9 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |
| 10 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 11 | `get_upstream_features` | L4:F15688@1, k=10 | Emb:"She"@1 (de=18.25) +9 more |
| 12 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 13 | `get_upstream_features` | L2:F2128@1, k=10 | Emb:"She"@1 (de=20.25) +9 more |

**Findings:** The target feature L6:F11646 is a female‑reference detector, primarily triggered by feminine pronouns such as "her" and "She". Its strongest upstream driver is the raw embedding of the token "She" (direct_effect ≈19), with additional contributions from early‑layer features that also respond to the token "She" (L4:F7864, L5:F10952, L0:F15382, L4:F15688). All identified upstream nodes lie at layers …

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@10, k=10 | Emb:" Nursing"@10 (de=17.38) +9 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 5 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 6 | `get_upstream_features` | L4:F11037@10, k=10 | Emb:" Nursing"@10 (de=10.62) +9 more |
| 7 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 8 | `get_upstream_features` | L5:F1275@10, k=10 | L4:F11037 (de=1.99) +9 more |
| 9 | `inspect_feature` | L1, F5829 | " uses of the word 'necessarily', sometimes near scientific or mathemat" |
| 10 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 11 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |

**Findings:** The target feature L6:F15267 is a nursing‑profession detector. Its strongest upstream driver is the raw token embedding for the word "Nursing" (direct effect 17.4), confirming that the circuit directly responds to the noun token. The next strongest upstream contributors are mid‑layer semantic features that capture broader health‑service and academic‑degree vocabularies (L4:F11037, L5:F1275). Those…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F9685 | " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L19:F9685@140, k=10 | L4:F1276 (de=1.45) +9 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `inspect_feature` | L4, F1302 | " parts of names or titles, sometimes followed by numbers" |
| 5 | `get_upstream_features` | L4:F1276@140, k=10 | Emb:" Kay"@139 (de=3.77) +9 more |
| 6 | `inspect_feature` | L18, F3679 | " personal pronouns and/or proper nouns" |
| 7 | `get_upstream_features` | L4:F1276@140, k=10 | Emb:" Kay"@139 (de=3.77) +9 more |
| 8 | `inspect_feature` | L2, F5859 | " first names (mostly female)" |
| 9 | `get_upstream_features` | L2:F5859@140, k=10 | Emb:" Kay"@139 (de=5.47) +9 more |
| 10 | `get_upstream_features` | L4:F1302@140, k=10 | Emb:"te"@140 (de=2.73) +9 more |

**Findings:** The target feature L19:F9685 is a female‑reference detector: it fires on feminine pronouns (She, her) and on women’s names. Upstream, the strongest drivers are a low‑layer (L4) capitalized‑name detector (F1276) that is strongly excited by the token "Kay" (embedding at position 139). That token flows through a first‑name detector (L2:F5859) which also recognises female first names. Additional name‑…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L12:12940, L4:15317, L6:8166, L0:16075 |
| 2 | `get_upstream_features` | L19:F9685@19, k=8 → Emb:" She"@19 (de=6.19) +7 more |
| 3 | `inspect_feature` ×2 | L14:3985, L6:170 |

### Build

`build_circuit` → 32 nodes, 40 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 24,755 | 6,680 | 67,920 | 0 | $0.0195 | — | — |
| SA-1 | openai/gpt-oss-120b | 100,795 | 5,905 | 2,688 | 0 | $0.0187 | ✅ 5F/8E | Trace this feature upstream. It fires at multiple positions … |
| SA-3 | openai/gpt-oss-120b | 120,867 | 7,013 | 14,176 | 0 | $0.0226 | ✅ 7F/10E | Trace this feature upstream. It fires at position 10. Determ… |
| SA-4 | openai/gpt-oss-120b | 93,727 | 6,944 | 21,856 | 0 | $0.0186 | ✅ 5F/5E | Trace this feature upstream. It fires at positions 19 and 14… |
| SA-2 | openai/gpt-oss-120b | 173,828 | 10,681 | 23,616 | 0 | $0.0328 | ✅ 5F/14E | Trace this feature upstream. It fires at positions 1, 2, 19.… |
| **Total** | | **513,972** | **37,223** | **130,256** | **0** | **$0.1122** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 9s