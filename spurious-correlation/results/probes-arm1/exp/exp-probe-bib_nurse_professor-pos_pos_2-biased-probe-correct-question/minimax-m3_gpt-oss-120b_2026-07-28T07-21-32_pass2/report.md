# Circuit Oracle Report
**Date:** 2026-07-28 07:21:32 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is classified positively by a circuit dominated by a cascade of female-pronoun / "woman-being-mentioned" features (She/She/her across positions 1, 19, 50) that propagates from raw token embeddings through low-level pronoun detectors, while a genuine but weaker nursing-profession feature (RN, nurse at pos 10) sits in parallel and contributes only a modest direct effect.

**Confidence:** 7

**Reasoning:** The top direct-effect drivers of the probe are L18:F14677 ("instances of women or girls being mentioned", direct_effect 0.377 at pos 19, 0.291 at pos 1, 0.229 at pos 50, frac_nonzero 0.012) and L6:F11646 ("references to women, potentially triggered by pronouns and titles", direct_effect 0.498 at pos 1, frac_nonzero 0.020) and L19:F9685 ("women's names and their roles or accomplishments", direct_effect 0.260 at pos 140). Tracing L18:F14677 upstream at pos 19 shows the strongest single driver is the **Emb:" She"** token (direct_effect 15.3), followed by **Emb:"She"** (pos 1, 4.28), and L17:F5889 / L15:F3330 (which themselves are pronoun / personal-story detectors). At pos 1 the top driver is again **Emb:"She"** (27.1) feeding L15:F851 (5.6) and L6:F11646 (4.2), which traces back to L2:F2128 (multilingual pronoun detector, 0.98) and L4:F7864. The L6:F11646 subagent confirmed a clean pronoun-cascade from the "She" embedding through L2:F2128 → L4:F7864 / L5:F10952 → L6:F11646, with the "She" token contributing direct_effect 19.25 directly.

By contrast, the genuine profession pathway (L6:F15267, "words in the document referring to the profession of nursing", direct_effect 0.473 at pos 10, frac_nonzero 0.016) is rooted at **Emb:" Nursing"** (direct_effect 17.4) and flows through L4:F11037 (professional-services, 4.25) and L5:F1275 (healthcare professionals, 2.0). The subagent explicitly verified that this path has no upstream gender-feature with positive direct_effect. However, this nursing feature sits only at layer 6 and is not further amplified into a late-layer "nurse-as-profession" supernode the way the female-pronoun signal is — the late-layer (L18, L19) features that feed the probe are almost entirely the gendered ones.

The user's concern is **substantively confirmed**: the probe's classification is driven primarily by repeated female pronouns ("She" at positions 1, 19, 50) cascading through a long, well-developed gender-reference feature chain (L0:F15382 → L6:F11646 → L12:F12940 / L18:F14677 / L19:F9685), rather than by a comparably developed profession-indicator chain. A genuine nursing signal exists and reaches the output (L6:F15267 has a +0.473 direct effect on the probe from a single token), but it is not the dominant late-layer story — the probe has learned to lean on the much more strongly represented "this is about a woman" signal that the model developed from the "She"-prefixed biography structure.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: She (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 50 | Emb: She (pos 50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: Nursing (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 19 | L0: Female-person detectors (pronoun/cue features) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 50 | L0: Female-person detectors (pronoun/cue features) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F16075](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) | 15 | L0: Female-person detectors (pronoun/cue features) | the word "of" and court names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | L2-L5: Low-level pronoun detectors (multilingual pronouns, 'She'/'her') | pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, *ele*, and *ela* across multiple languages. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | L2-L5: Low-level pronoun detectors (multilingual pronouns, 'She'/'her') | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | L2-L5: Low-level pronoun detectors (multilingual pronouns, 'She'/'her') | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | L6: Female pronoun/title detectors (She/her, female names) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | L6: Female pronoun/title detectors (She/her, female names) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 19 | L6: Female pronoun/title detectors (She/her, female names) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 50 | L6: Female pronoun/title detectors (She/her, female names) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | L6: Female pronoun/title detectors (She/her, female names) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 81 | L6: Female pronoun/title detectors (She/her, female names) |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | L6: Nursing profession detector (RN, nurse) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 10 | L4: Professional-services and named-entity context (RN, degree terms) | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | L4: Professional-services and named-entity context (RN, degree terms) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 140 | L4: Professional-services and named-entity context (RN, degree terms) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F1302](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1302) | 140 | L4: Professional-services and named-entity context (RN, degree terms) |  parts of names or titles, sometimes followed by numbers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1302) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 10 | L5: Healthcare professional terminology | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 10 | L7: Woman's name / female kinship roles |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 19 | L7: Woman's name / female kinship roles |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 50 | L7: Woman's name / female kinship roles |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 140 | L7: Woman's name / female kinship roles |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 19 | L7: Woman's name / female kinship roles | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 50 | L7: Woman's name / female kinship roles | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | L12: Female pronoun/possessive (her, she) detector | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L13:F11685](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) | 140 | L12: Female pronoun/possessive (her, she) detector |  words related to women | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 19 | L15-L17: Personal-story / pronoun & possessive features |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | L15-L17: Personal-story / pronoun & possessive features |  code documentation blocks in various programming languages | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L15:F4094](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4094) | 140 | L15-L17: Personal-story / pronoun & possessive features | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4094) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 19 | L15-L17: Personal-story / pronoun & possessive features |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F15936](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/15936) | 140 | L15-L17: Personal-story / pronoun & possessive features | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/15936) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | L18: Women/girls being mentioned (She/She/her, very high activation) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 19 | L18: Women/girls being mentioned (She/She/her, very high activation) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 50 | L18: Women/girls being mentioned (She/She/her, very high activation) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F3679](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) | 140 | L18: Other late features | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 140 | L19: Women's names and roles/accomplishments |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.498 |
| 3 | `inspect_feature` ×11 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940, L7:8644, L19:9685, L6:8166, L6:16329, L0:16075 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@19` | ❌ error | — | — | Trace the upstream circuit for the late-layer feature L18:F14677, which detects … |
| SA-2 | `L6:F15267@10` | ✅ reported | 8 | 10 | Trace the upstream circuit for the feature L6:F15267 which detects "words in the… |
| SA-3 | `L6:F11646@1` | ✅ reported | 4 | 4 | Trace the upstream circuit for L6:F11646 — "references to women, potentially tri… |

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@10, k=10 | Emb:" Nursing"@10 (de=17.38) +9 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 5 | `get_upstream_features` | L4:F11037@10, k=10 | Emb:" Nursing"@10 (de=10.62) +9 more |
| 6 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 7 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 8 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 9 | `inspect_feature` | L1, F5829 | " uses of the word 'necessarily', sometimes near scientific or mathemat" |
| 10 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |

**Findings:** The nursing‑profession detector (L6:F15267) receives its strongest excitation directly from the raw token embedding " Nursing" (pos 10) with a direct effect of 17.375, confirming that the genuine nursing signal reaches the feature without needing any gender‑related mediation. The next‑largest upstream driver is a layer‑4 professional‑services detector (L4:F11037) which also gets a strong push from…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 6 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |
| 7 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 8 | `get_upstream_features` | L2:F2128@1, k=10 | Emb:"She"@1 (de=20.25) +9 more |

**Findings:** The target feature L6:F11646 (gendered‑reference detector) receives its strongest positive drive from the input token "She" (direct_effect 19.25). The signal propagates through a hierarchy of pronoun‑detecting features in lower layers: L4:7864 and L5:10952 (both ≤ layer 8) and an even earlier multilingual pronoun detector L2:2128. Each of these lower‑layer features also has a direct positive influ…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@19, k=12 → Emb:" She"@19 (de=15.31) +11 more |
| 2 | `get_upstream_features` | L18:F14677@1, k=12 → Emb:"She"@1 (de=27.12) +11 more |
| 3 | `inspect_feature` ×5 | L15:851, L11:9183, L17:5889, L15:3330, L0:15382 |
| 4 | `get_upstream_features` | L19:F9685@140, k=10 → L4:F1276 (de=1.45) +9 more |
| 5 | `get_upstream_features` | L18:F14677@50, k=10 → Emb:" She"@50 (de=15.69) +9 more |
| 6 | `get_upstream_features` | L18:F3679@140, k=10 → Emb:"<bos>"@0 (de=-2.89) +9 more |
| 7 | `inspect_feature` ×2 | L13:11685, L4:1302 |
| 8 | `get_upstream_features` | L6:F16329@1, k=8 → Emb:"She"@1 (de=8.94) +7 more |
| 9 | `inspect_feature` | L4, F1276 → "capitalized names and titles, and names with lowercase letters in the " |

### Build

`build_circuit` → 18 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 70,821 | 6,348 | 229,256 | 0 | $0.0426 | — | — |
| SA-3 | openai/gpt-oss-120b | 99,568 | 5,750 | 96 | 0 | $0.0184 | ✅ 4F/4E | Trace the upstream circuit for L6:F11646 — "references to wo… |
| SA-2 | openai/gpt-oss-120b | 134,698 | 8,860 | 5,152 | 0 | $0.0256 | ✅ 8F/10E | Trace the upstream circuit for the feature L6:F15267 which d… |
| **Total** | | **305,087** | **20,958** | **234,504** | **0** | **$0.0866** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 13s