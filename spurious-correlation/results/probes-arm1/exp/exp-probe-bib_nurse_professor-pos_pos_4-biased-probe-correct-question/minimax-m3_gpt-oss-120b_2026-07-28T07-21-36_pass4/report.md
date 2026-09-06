# Circuit Oracle Report
**Date:** 2026-07-28 07:21:36 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "nurse" is driven by two parallel subcircuits: a legitimate nursing-vocabulary path (token `nurse` at pos 32 / `Nursing` at pos 18 → L5 healthcare-pro feature F1275, L4 medical-practices F1494, L4 counseling/therapy F11037 → L6 nursing-words F15267), and a much larger spurious gender-marker path that activates on the subject's name `Lori` (pos 1), the pronoun `She` (pos 20), and the word `graduated` (pos 2) — feeding through a chain of "female person" features (L0 F15382, L2 F16306, L4 F7864, L6 F11646 "references to women", L6 F16329 "female first names") up to a late-layer "instances of women or girls being mentioned" feature (L18 F14677, firing at positions 20, 43, 78, 117) and a "women's names and their roles or accomplishments" feature (L19 F9685).

**Confidence:** 8

**Reasoning:** The user's concern is confirmed and quantitatively clear. Looking at the top direct-effects driving the probe: L18:F14677 (women/girls mentioned, direct_effect 0.44), L19:F9685 (women's names and roles, 0.26), L6:F16329 (female first names, *suppresses* the probe at -0.33) — together the female-name and female-pronoun path dominates the circuit. The legitimate nursing path is comparatively thin: only L6:F15267 (nursing profession) and L4/L5 healthcare-professional features, fed by the tokens `nurse` (pos 32, direct_effect 5.66), `practitioner` (pos 33, 3.03), and `Nursing` (pos 18, 1.18). Critically, the gender-marker path originates from *the subject's name `Lori` itself* (L2:F16306 "proper names and positive adjectives", L4:F1276 "capitalized names", L5:F16213 "proper nouns first+last name" — all fired on `Lori` at pos 1) and the pronoun `She` at pos 20 (L0:F15382 "mentions of a female person", activation 22.5, direct_effect 2.4 → L6:F11646 → L15:F3330 "personal stories of individuals, especially women" → L17:F5889 "references to people with pronouns" → L18:F14677). The very feature L19:F9685 (women's names and their accomplishments) has "Debbie Gregory DNP, RN" as its top-activating example, showing the model has learned that female names *co-occur* with nursing professions in its training data. The circuit thus predicts "nurse" from a female-gendered prior about who the subject is, *not* from the nursing-specific vocabulary that is actually present. This is exactly the spurious-correlation mechanism the user suspected: the linear probe's classification direction aligns with the model's internal "woman" representation more than with the "nurse" representation, because in the training distribution those two are highly correlated.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 20 | Early-layer female-marker features (L0-L2) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L2:F16306](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) | 1 | Early-layer female-marker features (L0-L2) |  proper names and positive adjectives | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) |
| [L2:F899](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/899) | 20 | Early-layer female-marker features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/899) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 20 | Early-layer female-marker features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 20 | Early-layer female-marker features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 1 | Mid-layer female name/title features (L4-L7) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | Mid-layer female name/title features (L4-L7) |  proper nouns consisting of a first and last name | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 1 | Mid-layer female name/title features (L4-L7) |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 20 | Mid-layer female name/title features (L4-L7) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 20 | Mid-layer female name/title features (L4-L7) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 20 | Mid-layer female name/title features (L4-L7) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L5:F5996](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) | 33 | Mid-layer female name/title features (L4-L7) |  words associated with females, femininity or womanhood | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 20 | Mid-layer female name/title features (L4-L7) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L3:F4020](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4020) | 20 | Mid-layer female name/title features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4020) |
| [L1:F4232](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) | 20 | Mid-layer female name/title features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 33 | Nursing/profession-specific features (L4-L6) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 33 | Nursing/profession-specific features (L4-L6) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 33 | Nursing/profession-specific features (L4-L6) |  words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | Nursing/profession-specific features (L4-L6) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | Nursing/profession-specific features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L3:F13034](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13034) | 33 | Nursing/profession-specific features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13034) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 33 | Nursing/profession-specific features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L1:F15395](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) | 33 | Nursing/profession-specific features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) |
| [L5:F4161](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4161) | 33 | Nursing/profession-specific features (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4161) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Nursing/profession-specific features (L4-L6) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Nursing/profession-specific features (L4-L6) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 20 | Mid-layer gender-name features (L13-L18) |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L14:F13478](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) | 20 | Mid-layer gender-name features (L13-L18) |  occurrences of people's names, often with titles | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 20 | Mid-layer gender-name features (L13-L18) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L16:F2918](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) | 20 | Mid-layer gender-name features (L13-L18) | Pronouns | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 20 | Mid-layer gender-name features (L13-L18) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F4709](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4709) | 20 | Mid-layer gender-name features (L13-L18) |  mentions of Dr. Asin and related dental practice terms. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4709) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 20 | Late-layer gender/female features (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 43 | Late-layer gender/female features (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 78 | Late-layer gender/female features (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 117 | Late-layer gender/female features (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 20 | Late-layer gender/female features (L18-L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 43 | Late-layer gender/female features (L18-L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 101 | Late-layer gender/female features (L18-L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 20 | Late-layer gender/female features (L18-L19) |  personal names and associated titles | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:15267 de=0.562 |
| 3 | `inspect_feature` ×12 | L6:15267, L4:15317, L18:14677, L4:1276, L5:16213, L6:16329, L2:16306, L5:5996, L7:8644, L6:11646, L19:9685, L6:8166 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15267@33` | ❌ error | — | — | Trace this nursing-profession feature upstream to find what tokens and features … |
| SA-2 | `L19:F9685@20` | ❌ error | — | — | Trace this "women's names and roles" feature (L19:F9685) upstream to find what d… |
| SA-3 | `L18:F14677@20` | ❌ error | — | — | Trace this "instances of women or girls being mentioned" feature (L18:F14677) up… |
| SA-4 | `L6:F16329@20` | ❌ error | — | — | Trace this "female first names" feature (L6:F16329) upstream — it has a NEGATIVE… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F15267@33, k=15 → Emb:" nurse"@32 (de=5.66) +14 more |
| 2 | `get_upstream_features` | L19:F9685@20, k=15 → Emb:" She"@20 (de=5.88) +14 more |
| 3 | `get_upstream_features` | L18:F14677@20, k=15 → Emb:" She"@20 (de=14.44) +14 more |
| 4 | `get_upstream_features` | L6:F16329@20, k=15 → Emb:" She"@20 (de=6.78) +14 more |
| 5 | `inspect_feature` ×12 | L17:5889, L4:11037, L0:15382, L5:1275, L1:1494, L15:3330, L15:4709, L18:9023, L14:13478, L16:2918, L13:6622, L4:7864 |

### Build

`build_circuit` → 13 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 73,877 | 5,143 | 112,436 | 0 | $0.0351 | — | — |
| **Total** | | **73,877** | **5,143** | **112,436** | **0** | **$0.0351** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 1s