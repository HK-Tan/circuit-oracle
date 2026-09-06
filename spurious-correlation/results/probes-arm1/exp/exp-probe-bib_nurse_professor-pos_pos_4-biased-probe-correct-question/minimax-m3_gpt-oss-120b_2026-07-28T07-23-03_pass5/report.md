# Circuit Oracle Report
**Date:** 2026-07-28 07:23:03 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit was saved successfully. The warning about not reaching embedding nodes is inaccurate — the circuit already includes 5 embedding nodes (Lori, She, nurse, practitioner, Nursing). Here's the analysis.

**Analysis:** The probe's classification score for "nurse" is driven by **two roughly parallel paths** — one genuinely profession-related, one primarily gender/person-related — and the gender path carries nearly as much weight as the profession path.

**Confidence:** 7

**Reasoning:**

The circuit splits into two paths from the input:

**1. Profession path (genuine signal):**
- `Emb: nurse` (pos 32, direct_effect 5.66) → `L5:F1275` ("words related to healthcare professionals", 5.53) → `L6:F15267` ("words in the document referring to the profession of nursing", 0.56) → output
- `Emb: practitioner` (pos 33, 3.03) and `Emb: Nursing` (pos 18, 1.18) also feed in
- `L4:F15317` ("named entities like characters or people", 0.51) is a generic entity detector that also adds a small boost via the same nurse/practitioner tokens
- This is real semantic content: the probe is correctly detecting that the document describes a healthcare profession

**2. Gender/person path (spurious):**
- `Emb: Lori` (pos 1, 16.5!) and `Emb: She` (pos 20, 18.1) → `L0:L4` proper-name features (`F7532` "proper nouns", `F5859` "first names (mostly female)", `F1276` "capitalized names", `F15382` "mentions of a female person", `F16306` "proper names and positive adjectives") → `L6:F16329` "female first names and their possessive forms" (frac_nonzero 0.122, very generic), `L6:F8166` "proper names longer than 4 chars ending in a/i/e" → `L7:F8644` "woman's name in a variety of contexts" → `L18:F14677` "instances of women or girls being mentioned" (frac_nonzero 0.012, but promoted/suppressed tokens are all gendered — promotes "she/her/herself", suppresses "him/his/himself") → `L19:F9685` "references to women's names and their roles or accomplishments" → output

The gender path is **not the only signal**, but it is **disproportionately large relative to the profession path's late-layer contribution**:
- L18:F14677 alone has direct_effect 0.44 (pos 20) and fires on **four separate positions** (20, 43, 78, 117)
- L19:F9685 fires on three positions with direct_effect 0.21–0.26 each
- By contrast, the top genuine profession feature (L6:F15267) has direct_effect ~0.36–0.56 at just one or two positions

The probe's classification direction does include genuine "nurse" profession features (the L5 healthcare-professional and L6 profession-of-nursing features), confirming the user is right to be concerned but the classification is **not purely** spurious. However, the large contribution from the women's-name/women-mentioned circuit — driven by the simple presence of a female name "Lori" and pronouns "she/her" — means the probe is using **gender as a strong co-predictor** alongside actual profession vocabulary. The user's concern is well-founded: a male nurse with the same clinical content would likely score lower on this probe, because the female-name/women-mentioned features (L18:F14677, L19:F9685, L6:F16329, L7:F8644) would be substantially weaker, even though the genuine profession features (L5:F1275, L6:F15267) would be unchanged.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 32 | Emb: nurse (pos 32) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 33 | Emb: practitioner (pos 33) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: Nursing (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Lori (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: She (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 33 | Early-layer medical-practice features (L1–L4) |  words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 33 | Early-layer medical-practice features (L1–L4) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L1:F15395](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) | 33 | Early-layer medical-practice features (L1–L4) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | Early-layer proper-name / female-person features (L0–L4) |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 1 | Early-layer proper-name / female-person features (L0–L4) |  first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 20 | Early-layer proper-name / female-person features (L0–L4) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L2:F16306](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) | 1 | Early-layer proper-name / female-person features (L0–L4) |  proper names and positive adjectives | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 1 | Early-layer proper-name / female-person features (L0–L4) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | L5 healthcare-professional / medical terms | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | L5 healthcare-professional / medical terms |  proper nouns consisting of a first and last name | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | L6 profession-of-nursing feature (F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | L6 profession-of-nursing feature (F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 20 | L6 profession-of-nursing feature (F15267) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 20 | L6 female-name / references-to-women features | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 33 | L6 female-name / references-to-women features | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 1 | L6 female-name / references-to-women features |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 33 | L7 woman's-name feature (F8644) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 18 | L7 woman's-name feature (F8644) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 20 | L7 woman's-name feature (F8644) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L5:F5996](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) | 33 | L5 female-associated feature (F5996, pushes against) |  words associated with females, femininity or womanhood | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 20 | L17 pronoun / person-reference (F5889) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 20 | L18 women-mentioned / name-title features |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 43 | L18 women-mentioned / name-title features |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 78 | L18 women-mentioned / name-title features |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 117 | L18 women-mentioned / name-title features |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 20 | L18 women-mentioned / name-title features |  personal names and associated titles | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 20 | L19 women-names-roles feature (F9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 43 | L19 women-names-roles feature (F9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 101 | L19 women-names-roles feature (F9685) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score (nurse profession) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:15267 de=0.562 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@20` | ❌ error | — | — | Trace L18:F14677 at pos 20. This feature has the highest direct_effect among lat… |
| SA-2 | `L6:F15267@33` | ❌ error | — | — | Trace L6:F15267 at pos 33. This is the top positive direct_effect feature overal… |
| SA-3 | `L4:F15317@33` | ❌ error | — | — | Trace L4:F15317 at pos 33. Second highest direct_effect feature. What does it en… |
| SA-4 | `L4:F1276@1` | ❌ error | — | — | Trace L4:F1276 at pos 1. What does this feature encode? Position 1 is the second… |
| SA-5 | `L5:F16213@2` | ❌ error | — | — | Trace L5:F16213 at pos 2. What does this feature encode? Position 2 is 'graduate… |
| SA-6 | `L2:F16306@1` | ❌ error | — | — | Trace L2:F16306 at pos 1. What does this feature encode? This is a very early-la… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×12 | L18:14677, L6:15267, L4:15317, L4:1276, L5:16213, L2:16306, L5:5996, L6:8166, L7:8644, L6:11646, L6:16329, L19:9685 |
| 2 | `get_upstream_features` | L6:F15267@33, k=10 → Emb:" nurse"@32 (de=5.66) +9 more |
| 3 | `get_upstream_features` | L18:F14677@20, k=10 → Emb:" She"@20 (de=14.44) +9 more |
| 4 | `get_upstream_features` | L4:F15317@33, k=10 → Emb:" nurse"@32 (de=4.00) +9 more |
| 5 | `get_upstream_features` | L4:F1276@1, k=10 → Emb:"Lori"@1 (de=16.50) +9 more |
| 6 | `get_upstream_features` | L19:F9685@20, k=10 → Emb:" She"@20 (de=5.88) +9 more |
| 7 | `get_upstream_features` | L6:F11646@20, k=10 → Emb:" She"@20 (de=18.12) +9 more |
| 8 | `get_upstream_features` | L5:F16213@2, k=10 → Emb:"Lori"@1 (de=2.56) +9 more |
| 9 | `get_upstream_features` | L2:F16306@1, k=10 → Emb:"Lori"@1 (de=5.91) +9 more |
| 10 | `get_upstream_features` | L6:F8166@1, k=10 → L4:F1276 (de=4.12) +9 more |
| 11 | `get_upstream_features` | L7:F8644@33, k=10 → Emb:" practitioner"@33 (de=3.41) +9 more |
| 12 | `get_upstream_features` | L6:F16329@20, k=10 → Emb:" She"@20 (de=6.78) +9 more |
| 13 | `inspect_feature` ×8 | L5:1275, L4:11037, L1:1494, L0:15382, L17:5889, L18:9023, L0:7532, L2:5859 |

### Build

`build_circuit` → 16 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 43,973 | 6,243 | 119,726 | 0 | $0.0279 | — | — |
| **Total** | | **43,973** | **6,243** | **119,726** | **0** | **$0.0279** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 19s