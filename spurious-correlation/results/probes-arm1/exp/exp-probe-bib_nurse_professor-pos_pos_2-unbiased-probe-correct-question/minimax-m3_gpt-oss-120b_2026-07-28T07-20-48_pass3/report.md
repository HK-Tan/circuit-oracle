# Circuit Oracle Report
**Date:** 2026-07-28 07:20:48 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's nurse classification is driven primarily by genuine profession-specific tokens ("Nursing", "nursing", "graduated", "Bachelors", "Medical") and a hierarchy of features that explicitly detect nursing/medical language, not by gender markers. The dominant signal is the token "Nursing" at positions 10 and 22, which directly excites the L6:F15267 / L7:F3979 nursing-profession detector and the L18:F13596 nurse-manager feature with the largest direct effects in the graph.

**Confidence:** 9/10

**Reasoning:**

- **L18:F13596** ("text about the role, skills and leadership of nurse managers", frac_nonzero 0.005) is the single most positively driving late-layer feature, and its top upstream driver is the **"Nursing" embedding at pos 10** (direct_effect +42.75) followed by the L6 nursing-profession feature (+9.44) and L14 management/medicine feature (+6.31). Its promoted tokens are "Nurse/Nursing/nursing" — pure profession vocabulary.
- **L14:F3985** (management/medicine/research, frac_nonzero 0.066) is also driven mostly by the "Nursing" embedding (+12.1) and the L6/L7 nursing features; its top activating examples are about nurse managers, not gender.
- **L6:F15267** (words referring to the profession of nursing, frac_nonzero 0.016) receives direct_effect +17.4 from the "Nursing" token at pos 10 and +21.0 from the "nursing" token at pos 22. Its top activating examples are all "RN", "nurse", "nurse manager" — profession-specific.
- **L7:F3979** (nursing and healthcare, frac_nonzero 0.008) is parallel to L6:F15267 and also driven by the nursing tokens (DE +7.78 on "Nursing" at pos 10).
- **L0/L2 token detectors** — L0:F5038 (the word "graduated"), L2:F14478 ("graduate"), L0:F6270 ("whom"), L0:F16075 ("of") — were inspected. **None of them are gender features.** L0:F6270 fires on the function word "whom" (top examples: "of whom", "to whom", "all of whom") with no female/male bias; its direct_effect on the probe comes from upstream function-word positions (University, Of, Medical, etc.) and is small. The early-layer features with the highest direct effect on the probe are L0:F16075 (DE +0.07, the word "of" / court names — clearly driven by the "Of" token at pos 15 in "University Of South Carolina") and L0:F11988 (DE +0.04, "Carolina"). These are local proper-noun / function-word detectors, not pronoun/gender features.
- **Negative direction feature** L3:F15901 ("nurses, nursing, and nurse management", frac_nonzero 0.005) actively *suppresses* the probe (DE −0.098 on the probe; also inhibits L18:F13596 with DE −5.28). It is itself strongly excited by the "Nursing" embedding (DE +15.13). Its suppressed tokens are "nurse/nursing/Nurse" — so it is an anti-nursing feature in this context, not a gender feature.
- **No gendered features** (e.g. "she", "her", female-pronoun features) appear anywhere in the top 20 features or in the upstream traces. The "She"/"her" tokens at positions 1, 4 etc. do not produce any feature with notable direct_effect on the probe; the only pos-1 upstream entries for the pos-2 "graduated" feature have direct_effect 0.
- Signal flow: Emb("Nursing", pos 10/22) and Emb("graduated"/"Bachelors"/"Science"/"Medical", pos 2/6/8/13) → core_nursing_token (L6:F15267, L7:F3979, L3:F15901, L2:F10852) → mid_nursing_healthcare (L4:L8 features that combine "nurse + degree + medical" context) → late_nurse_manager (L14:L18 nurse-manager/clinical-medicine/medical-healthcare features) → probe_logit.

The circuit confirms the probe is using **genuine profession indicators** (the word "Nursing", degree tokens "Bachelors"/"Science"/"graduated", medical-context features) as the causal evidence. The function-word features (L0:F16075 "of", L0:F6270 "whom", L0:F11988 "Carolina") contribute only minor amounts to the score and are present because proper-noun phrases and prepositions are how a degree is named — they are not gendered, and the user's hypothesized gender-marker confound is not supported by this attribution graph.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 10 | Nurse-manager role/leadership description |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 10 | Nurse-manager role/leadership description |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L15:F8289](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) | 10 | Nurse-manager role/leadership description |  words and phrases related to clinical medicine, including the terms clinicians use and related scientific fields | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 10 | Nurse-manager role/leadership description | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 10 | Mid-layer nursing & healthcare terminology |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 10 | Mid-layer nursing & healthcare terminology |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F4654](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4654) | 10 | Mid-layer nursing & healthcare terminology |  words related to medical supplies and care | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4654) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 10 | Mid-layer nursing & healthcare terminology |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L6:F11057](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11057) | 15 | Mid-layer nursing & healthcare terminology |  capitalized words, especially in titles and headings, and ordinal words like "first" | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11057) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 10 | Mid-layer nursing & healthcare terminology | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 10 | Mid-layer nursing & healthcare terminology | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | Nursing-specific profession detector (L6:F15267 / L7:F3979) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 22 | Nursing-specific profession detector (L6:F15267 / L7:F3979) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 10 | Nursing-specific profession detector (L6:F15267 / L7:F3979) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 22 | Nursing-specific profession detector (L6:F15267 / L7:F3979) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 10 | Nursing-specific profession detector (L6:F15267 / L7:F3979) |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 10 | Nursing-specific profession detector (L6:F15267 / L7:F3979) | academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F14478](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14478) | 2 | Academic-degree / "graduated" tokens |  the word graduate | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14478) |
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 2 | Academic-degree / "graduated" tokens | the word "graduated" or variations of it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L0:F11959](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) | 2 | Academic-degree / "graduated" tokens |  the word "graduated" and the word "more." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) |
| [L4:F16096](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/16096) | 15 | Function-word / "of" detectors (NOT gender-related) | instances of the word "of" preceded by particular words and abbreviations | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/16096) |
| [L0:F16075](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) | 15 | Function-word / "of" detectors (NOT gender-related) | the word "of" and court names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 14 | Function-word / "of" detectors (NOT gender-related) | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L0:F11988](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11988) | 17 | Function-word / "of" detectors (NOT gender-related) |  mentions of North Carolina, sometimes in conjunction with "University" or "study" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11988) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.188 |
| 3 | `inspect_feature` ×18 | L14:3985, L6:15267, L15:15159, L8:16339, L0:5038, L0:6270, L7:3979, L3:15901, L0:16075, L18:13596, L6:4490, L7:210, L2:14478, L6:11057, L0:11959, L0:11988, L7:4654, L15:8289 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@10` | ✅ reported | 5 | 14 | Trace upstream from L14:F3985 (terms related to management/leadership/medicine/s… |
| SA-2 | `L6:F15267@10` | ✅ reported | 4 | 20 | Trace upstream from L6:F15267 (nursing profession terms) at position 10. Identif… |
| SA-3 | `L0:F5038@2` | ❌ error | — | — | Trace upstream from L0:F5038 (the word "graduated") at position 2. Confirm if th… |
| SA-4 | `L0:F6270@14` | ❌ error | — | — | Trace upstream from L0:F6270 (the word "whom") at position 14. Identify what inp… |
| SA-5 | `L0:F16075@15` | ❌ error | — | — | Trace upstream from L0:F16075 (the word "of") at position 15. Identify what inpu… |
| SA-6 | `L18:F13596@10` | ✅ reported | 10 | 13 | Trace upstream from L18:F13596 (text about role, skills, leadership of nurse man… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@10, k=10 | Emb:" Nursing"@10 (de=12.12) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 5 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 6 | `get_upstream_features` | L8:F16339@10, k=10 | Emb:" Nursing"@10 (de=7.66) +9 more |
| 7 | `get_upstream_features` | L7:F210@10, k=10 | Emb:" Nursing"@10 (de=8.19) +9 more |
| 8 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 9 | `get_upstream_features` | L6:F15267@10, k=10 | Emb:" Nursing"@10 (de=17.38) +9 more |
| 10 | `inspect_feature` | L8, F9619 | " words and phrases related to medical treatment" |

**Findings:** The target feature L14:F3985 (management/leadership/medicine) is primarily driven by the input token "Nursing" (direct_effect >12) and by a cascade of nursing-specific and generic medical features. The strongest nursing-specific upstream node is L6:F15267, which explicitly detects nursing-related words and also receives a huge direct effect from the "Nursing" token. This feeds into mid-level medic…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@10, k=15 | Emb:" Nursing"@10 (de=17.38) +14 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 5 | `get_upstream_features` | L4:F11037@10, k=15 | Emb:" Nursing"@10 (de=10.62) +14 more |
| 6 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 7 | `get_upstream_features` | L5:F1275@10, k=15 | L4:F11037 (de=1.99) +14 more |
| 8 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 9 | `get_upstream_features` | L2:F10852@10, k=10 | Emb:" Nursing"@10 (de=11.44) +9 more |

**Findings:** The L6:F15267 nursing‑term detector is primarily driven by the raw input token "Nursing" (direct_effect ≈ 17). It also receives substantial upstream support from a mid‑layer health‑education feature (L4:F11037) and a broader healthcare‑professional feature (L5:F1275). Those mid‑layer features, in turn, are themselves strongly activated by the same "Nursing" token and by degree‑related substrings (…

</details>

<details>
<summary><b>SA-6</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 2 | `get_upstream_features` | L18:F13596@10, k=10 | Emb:" Nursing"@10 (de=42.75) +9 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `get_upstream_features` | L6:F15267@10, k=10 | Emb:" Nursing"@10 (de=17.38) +9 more |
| 5 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 6 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 7 | `get_upstream_features` | L5:F1275@10, k=10 | L4:F11037 (de=1.99) +9 more |
| 8 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 9 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |

**Findings:** The trace starts at the late‑layer feature L18:F13596 that encodes the description of nurse‑manager roles. Its strongest upstream driver is the raw token embedding for "Nursing" (direct effect 42.75) and a lower‑layer feature L6:F15267 (layer 6, within the lower third) that detects nursing‑related words (direct effect 9.44). L6:F15267 itself is driven primarily by the same "Nursing" embedding (dir…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F5038@2, k=10 → Emb:" graduated"@2 (de=22.25) +9 more |
| 2 | `get_upstream_features` | L0:F6270@14, k=10 → Emb:" University"@14 (de=22.12) +9 more |
| 3 | `get_upstream_features` | L0:F16075@15, k=10 → Emb:" Of"@15 (de=26.50) +9 more |
| 4 | `get_upstream_features` | L2:F14478@2, k=10 → Emb:" graduated"@2 (de=19.75) +9 more |
| 5 | `get_upstream_features` | L0:F11959@2, k=10 → Emb:" graduated"@2 (de=20.75) +9 more |
| 6 | `get_upstream_features` | L0:F11988@17, k=10 → Emb:" Carolina"@17 (de=12.94) +9 more |
| 7 | `get_upstream_features` | L6:F11057@15, k=10 → L4:F16096 (de=10.38) +9 more |
| 8 | `inspect_feature` | L4, F16096 → "instances of the word "of" preceded by particular words and abbreviati" |
| 9 | `get_upstream_features` | L6:F11057@14, k=5 → ❌ Feature (layer=6, feature_idx=11057) not found at pos=14. Th |
| 10 | `inspect_feature` | L3, F7251 → " mentions of bicycle racing, specifically "de", "la", "del", or "prix"" |
| 11 | `get_upstream_features` | L18:F13596@10, k=5 → Emb:" Nursing"@10 (de=42.75) +4 more |
| 12 | `inspect_feature` | L3, F15901 → " mentions of nurses, nursing, and nurse management" |
| 13 | `get_upstream_features` | L7:F3979@10, k=8 → L6:F15267 (de=8.75) +7 more |
| 14 | `inspect_feature` | L3, F15901 → " mentions of nurses, nursing, and nurse management" |
| 15 | `get_upstream_features` | L6:F15267@22, k=8 → Emb:" nursing"@22 (de=21.00) +7 more |
| 16 | `get_upstream_features` | L3:F15901@10, k=8 → Emb:" Nursing"@10 (de=15.12) +7 more |
| 17 | `get_upstream_features` | L7:F3979@22, k=5 → L6:F15267 (de=8.81) +4 more |
| 18 | `get_upstream_features` | L6:F11057@15, k=5 → L4:F16096 (de=10.38) +4 more |

### Build

`build_circuit` → 16 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 82,505 | 6,050 | 265,154 | 0 | $0.0479 | — | — |
| SA-1 | openai/gpt-oss-120b | 126,439 | 7,200 | 8,480 | 0 | $0.0234 | ✅ 5F/14E | Trace upstream from L14:F3985 (terms related to management/l… |
| SA-2 | openai/gpt-oss-120b | 107,993 | 9,532 | 5,056 | 0 | $0.0220 | ✅ 4F/20E | Trace upstream from L6:F15267 (nursing profession terms) at … |
| SA-6 | openai/gpt-oss-120b | 109,800 | 9,348 | 896 | 0 | $0.0221 | ✅ 10F/13E | Trace upstream from L18:F13596 (text about role, skills, lea… |
| **Total** | | **426,737** | **32,130** | **279,586** | **0** | **$0.1154** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 33s