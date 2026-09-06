# Circuit Oracle Report
**Date:** 2026-07-28 07:00:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "nurse" is driven by a hybrid circuit: a legitimate profession path (anchored on the tokens "nurse", "practitioner", and "Nursing") is supplemented — and partly overshadowed — by an extensive gender-marker path that detects female subjects ("She", feminine pronouns, female-name features) and a name-identity path anchored on the first-name "Lori".

**Confidence:** 8

**Reasoning:**

The circuit has three converging supernodes feeding the probe direction at layer 26:

1. **`prof_path` (genuine profession signal, mid-layers, pos 32-33/18):** The strongest single contributor is L6:F15267 ("words in the document referring to the profession of nursing", frac_nonzero=0.016, max_token=`▁RN`/`▁nurse`), with direct_effect +0.56 at pos 33 and +0.36 at pos 18. It traces back to L5:F1275 and L4:F11037/F9036 (which promote `▁practitioner` and `▁nurse`, direct_effects 14.0 and 6.5 from the `practitioner` token embedding), L1:F1494 ("words related to medical practices and studies", max_token=`▁practice`), and L2:F2589 ("words related to medical professionals", max_token=`▁physicians`/`▁practitioners`). The bottom of this path is the token embeddings `▁nurse` (pos 32), `▁practitioner` (pos 33), and `▁Nursing` (pos 18). This is the legitimate semantic evidence.

2. **`gender_path` (spurious gender signal, late layers, pos 20, 43, 78, 101, 117):** This is the most striking finding and **directly confirms the user's concern**. The largest late-layer feature is L18:F14677 ("instances of women or girls being mentioned", frac_nonzero=0.012, max_token=`▁she`/`▁She`, with female-pronoun `▁herself`/`▁she`/`▁her` dominating its promoted tokens). It fires on five different "She" positions (20, 43, 78, 117) with direct_effects 0.21–0.44 each. L19:F9685 ("references to women's names and their roles or accomplishments") fires on pos 20/43/101 with direct_effects 0.21–0.26. These late-layer gender detectors are fed by a long chain of intermediate features: L17:F5889 (pronouns, She, +3.77), L15:F3330 (pronouns, +3.0), L13:F6622 (pronouns, +1.96), L16:F2918 (pronouns, +0.99), L6:F11646 ("references to women, pronouns and titles", direct_effect 2.23), L6:F16329 ("female first names", direct_effect −2.16 — *suppresses* here because the subject is "She" not a name), and L7:F8644 ("woman's name", direct_effect −2.22). The root of the path is the `▁She` token embedding at pos 20 (direct_effect up to 25.75 in upstream L0 features like F15382, F12519, F9519). Note also L6:F16329 at pos 33 has direct_effect −0.33 — the *female-name* feature actively *suppresses* the probe when the token is "practitioner" (a profession word, not a name), which is incidental noise.

3. **`name_path` (identity signal, layers 2-6, pos 1):** L5:F16213 ("proper nouns consisting of a first and last name", max_token=`▁Lori`-like) and L4:F1276 ("capitalized names and titles", max_token=`▁Lori`) fire on "Lori" with combined direct_effect ~0.75, backed by L2:F16306 ("proper names and positive adjectives", max_token `▁Lori`) and L0:F7532 (max_token `▁Lori`, direct_effect 14.3). L6:F8166 ("proper names ending in 'a', 'i', or 'e'") also fires on "Lori" (+0.31). This path uses the female first-name as a quasi-gender proxy.

**Why this confirms the user's concern:** The legitimate profession pathway through L6:F15267 has a single feature with direct_effect ~0.56, plus the upstream `practitioner`/`nurse` features at layer 4-5 (direct_effects up to 14 on F9036, 6.5 on F11037). However, the *late-layer* features that sit closest to the probe direction are dominated by L18:F14677 and L19:F9685 — both explicitly "women/female" detectors — which fire on **five different positions** (20, 43, 78, 101, 117) and on `▁She` and `▁her` pronouns throughout the text, **not on the nursing tokens**. The profession features at L4-L6 are mid-layer; the gender features at L17-L19 are late-layer and therefore have a more direct line to whatever direction the probe reads. The name path adds another non-profession signal via "Lori". A probe that learns to use these features would likely misclassify male nurses (whose bios would lack the "She" pronouns) and over-fire on female non-nurses. The circuit is **partially legitimate** (the profession words do contribute) but **substantially contaminated by gender markers and first-name features** — exactly the spurious-correlation pattern the user suspected.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Profession-indicating path (nurse/practitioner at pos 32-33) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Profession-indicating path (nurse/practitioner at pos 32-33) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 33 | Profession-indicating path (nurse/practitioner at pos 32-33) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | Profession-indicating path (nurse/practitioner at pos 32-33) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | Profession-indicating path (nurse/practitioner at pos 32-33) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 33 | Profession-indicating path (nurse/practitioner at pos 32-33) |  words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 33 | Profession-indicating path (nurse/practitioner at pos 32-33) |  words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 20 | Gender/female-subject path (She at pos 20) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 43 | Gender/female-subject path (She at pos 20) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 78 | Gender/female-subject path (She at pos 20) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 117 | Gender/female-subject path (She at pos 20) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 20 | Gender/female-subject path (She at pos 20) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 43 | Gender/female-subject path (She at pos 20) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 101 | Gender/female-subject path (She at pos 20) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 20 | Gender/female-subject path (She at pos 20) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 20 | Gender/female-subject path (She at pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F4709](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4709) | 20 | Gender/female-subject path (She at pos 20) |  mentions of Dr. Asin and related dental practice terms. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4709) |
| [L14:F13478](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) | 20 | Gender/female-subject path (She at pos 20) |  occurrences of people's names, often with titles | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 20 | Gender/female-subject path (She at pos 20) |  personal names and associated titles | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |
| [L16:F2918](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) | 20 | Gender/female-subject path (She at pos 20) | Pronouns | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 20 | Gender/female-subject path (She at pos 20) |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 20 | Gender/female-subject path (She at pos 20) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 20 | Gender/female-subject path (She at pos 20) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 20 | Gender/female-subject path (She at pos 20) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 33 | Gender/female-subject path (She at pos 20) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 18 | Gender/female-subject path (She at pos 20) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L5:F5996](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) | 33 | Gender/female-subject path (She at pos 20) |  words associated with females, femininity or womanhood | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 20 | Gender/female-subject path (She at pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 20 | Gender/female-subject path (She at pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 20 | Gender/female-subject path (She at pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F3232](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3232) | 20 | Gender/female-subject path (She at pos 20) |  mentions of the third person plural pronoun "They" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3232) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | Name/identity path (Lori at pos 1) |  proper nouns consisting of a first and last name | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 1 | Name/identity path (Lori at pos 1) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 1 | Name/identity path (Lori at pos 1) |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L2:F16306](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) | 1 | Name/identity path (Lori at pos 1) |  proper names and positive adjectives | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 1 | Name/identity path (Lori at pos 1) |  first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L3:F6656](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6656) | 2 | Name/identity path (Lori at pos 1) | verbs or phrases indicating action, saying, or feeling | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6656) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | Name/identity path (Lori at pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:15267 de=0.562 |
| 3 | `inspect_feature` ×12 | L6:15267, L4:15317, L18:14677, L4:1276, L5:16213, L6:16329, L6:8166, L7:8644, L2:16306, L6:11646, L19:9685, L5:5996 |
| 4 | `get_upstream_features` | Emb:" nurse"@32 (de=5.66) +14 more |
| 5 | `get_upstream_features` | Emb:" nurse"@32 (de=4.00) +14 more |
| 6 | `get_upstream_features` | Emb:" She"@20 (de=14.44) +14 more |
| 7 | `get_upstream_features` | Emb:"Lori"@1 (de=2.56) +14 more |
| 8 | `get_upstream_features` | L4:F9036 (de=1.70) +9 more |
| 9 | `get_upstream_features` | Emb:" She"@20 (de=5.88) +14 more |
| 10 | `get_upstream_features` | Emb:"Lori"@1 (de=16.50) +9 more |
| 11 | `get_upstream_features` | Emb:"Lori"@1 (de=5.91) +9 more |
| 12 | `get_upstream_features` | Emb:" practitioner"@33 (de=6.47) +9 more |
| 13 | `get_upstream_features` | Emb:" practitioner"@33 (de=14.00) +9 more |
| 14 | `get_upstream_features` | Emb:" She"@20 (de=6.78) +9 more |
| 15 | `get_upstream_features` | Emb:" She"@20 (de=23.62) +4 more |
| 16 | `get_upstream_features` | Emb:" She"@20 (de=19.00) +4 more |
| 17 | `get_upstream_features` | Emb:" She"@20 (de=25.75) +4 more |
| 18 | `get_upstream_features` | Emb:"Lori"@1 (de=14.31) +4 more |
| 19 | `get_upstream_features` | L6:F16329 (de=-5.81) +9 more |
| 20 | `get_upstream_features` | Emb:" She"@20 (de=19.50) +9 more |
| 21 | `get_upstream_features` | Emb:" She"@20 (de=15.75) +9 more |
| 22 | `get_upstream_features` | Emb:" She"@20 (de=18.12) +9 more |
| 23 | `get_upstream_features` | L13:F15487 (de=3.89) +4 more |
| 24 | `inspect_feature` ×4 | L0:3232, L0:14257, L1:1494, L2:2589 |
| 25 | `get_upstream_features` | Emb:" graduated"@2 (de=4.84) +4 more |
| 26 | `get_upstream_features` | Emb:"Lori"@1 (de=3.38) +4 more |
| 27 | `inspect_feature` ×10 | L3:6656, L2:5859, L4:7864, L15:4709, L14:13478, L18:9023, L16:2918, L13:6622, L17:5889, L0:9026 |
| 28 | `get_upstream_features` | Emb:" Nursing"@18 (de=17.38) +4 more |
| 29 | `inspect_feature` | " named entities like characters or people" |

### Build

`build_circuit` → 10 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 71,197 | 6,503 | 381,037 | 0 | $0.0520 | — | — |
| **Total** | | **71,197** | **6,503** | **381,037** | **0** | **$0.0520** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 49s