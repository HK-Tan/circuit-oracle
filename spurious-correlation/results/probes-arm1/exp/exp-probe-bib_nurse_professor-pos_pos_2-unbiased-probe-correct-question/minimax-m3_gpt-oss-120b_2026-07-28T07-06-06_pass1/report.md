# Circuit Oracle Report
**Date:** 2026-07-28 07:06:06 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "nursing profession" is driven overwhelmingly by genuine profession indicators — chiefly the token "Nursing"/"nursing" and its surrounding hospital/medical context — not by gender markers.

**Confidence:** 9

**Reasoning:** Tracing the full circuit shows the probe's positive score is built almost entirely from a tight cascade of *profession-specific* features keyed to the token " Nursing" at pos 10 (and " nursing" at pos 22). The strongest individual feature is L18:F13596 (nurse-manager text, activation 46.5, frac_nonzero 0.0049), whose single largest direct input is the " Nursing" embedding itself (DE = 42.75), with the L6 nursing-profession detector L6:F15267 (DE = 9.44) and the L14 medical/management feature L14:F3985 (DE = 6.31) feeding in below it. The same " Nursing" embedding directly excites L15:F15159 (medicine/healthcare, DE = 10.56), L15:F8289 (clinical medicine, DE = 6.25), L14:F3985 (DE = 12.12), L8:F16339 (hospital context, DE = 7.66), and L7:F210 (Asante/healthcare system, DE = 8.19) — all features with autointerp labels that mention nursing, hospital, medical, clinical, or patient care. Auxiliary positive contributions come from "graduated" (L0:F5038, L0:F11959, L2:F14478, the famous bio-template phrase) and from " University" (L0:F6270, DE = 22.13 on the "University" embedding), " Of" (L0:F16075), and " Carolina" (L0:F11988) — these are institution-of-degree cues that complement the profession signal. The "She" pronoun at pos 1 contributes only a tiny DE of 0.37 to L0:F5038 (vs 22.25 from the " graduated" embedding) and does not appear as a top-20 driver of the probe; no "she/her/her" pronoun feature shows up anywhere in the top positive contributors. Negative contributors (L7:F3979, L3:F15901) are themselves nursing-related features, suggesting the probe's net output is the residual of competing nursing-context signals. In short, the user's concern is not supported by this circuit: the classification is driven by the word "Nursing" and its associated medical/hospital/institution context, not by the female pronoun "She."

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 10 | L18: Nurse manager / nursing-leadership text |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 10 | L14: Medical/management/leadership terms | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 10 | L15: Medicine/healthcare & clinical terms |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L15:F8289](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) | 10 | L15: Medicine/healthcare & clinical terms |  words and phrases related to clinical medicine, including the terms clinicians use and related scientific fields | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 10 | L7 / L3: Nursing/healthcare terms (suppress probe — negative DE) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 10 | L7 / L3: Nursing/healthcare terms (suppress probe — negative DE) |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 22 | L7 / L3: Nursing/healthcare terms (suppress probe — negative DE) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 22 | L7 / L3: Nursing/healthcare terms (suppress probe — negative DE) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | L6: Nursing-profession terms (RN, nurse, DNP) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 10 | L8 / L6 / L7: Hospital / medical-proper-noun / health-system features |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 10 | L8 / L6 / L7: Hospital / medical-proper-noun / health-system features |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 10 | L8 / L6 / L7: Hospital / medical-proper-noun / health-system features |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 2 | L0/L2: 'graduated' / 'graduate' word features | the word "graduated" or variations of it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L0:F11959](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) | 2 | L0/L2: 'graduated' / 'graduate' word features |  the word "graduated" and the word "more." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) |
| [L2:F14478](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14478) | 2 | L0/L2: 'graduated' / 'graduate' word features |  the word graduate | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14478) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 14 | L0: 'University', 'Of' (institution phrase), North Carolina | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L0:F16075](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) | 15 | L0: 'University', 'Of' (institution phrase), North Carolina | the word "of" and court names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) |
| [L0:F11988](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11988) | 17 | L0: 'University', 'Of' (institution phrase), North Carolina |  mentions of North Carolina, sometimes in conjunction with "University" or "study" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11988) |
| [L6:F11057](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11057) | 15 | L0: 'University', 'Of' (institution phrase), North Carolina |  capitalized words, especially in titles and headings, and ordinal words like "first" | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11057) |
| [L7:F4654](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4654) | 10 | L0: 'University', 'Of' (institution phrase), North Carolina |  words related to medical supplies and care | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4654) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.188 |
| 3 | `inspect_feature` ×18 | L14:3985, L6:15267, L0:5038, L0:6270, L7:3979, L3:15901, L0:11959, L0:11988, L0:16075, L2:14478, L15:15159, L6:4490, L8:16339, L7:210, L18:13596, L7:4654, L15:8289, L6:11057 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@10` | ✅ reported | 5 | 8 | Trace from L14:F3985 (medical/management/nursing terms feature) at pos 10. The c… |
| SA-2 | `L6:F15267@10` | ✅ reported | 10 | 10 | Trace from L6:F15267 (nursing profession references feature) at pos 10. This fea… |
| SA-3 | `L0:F5038@2` | ❌ error | — | — | Trace from L0:F5038 (the word "graduated" feature) at pos 2. Pos 2 in the input … |
| SA-4 | `L18:F13596@10` | ✅ reported | 3 | 3 | Trace from L18:F13596 (nurse managers text feature) at pos 10. This fires very s… |
| SA-5 | `L0:F11959@2` | ✅ reported | 3 | 0 | Check the early-layer features that fired at pos 2 (the "She" / beginning-of-bio… |
| SA-6 | `L15:F15159@10` | ✅ reported | 7 | 11 | Trace from L15:F15159 (medicine/healthcare feature) at pos 10 and L15:F8289 (cli… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@10, k=15 | Emb:" Nursing"@10 (de=12.12) +14 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 5 | `get_upstream_features` | L8:F16339@10, k=15 | Emb:" Nursing"@10 (de=7.66) +14 more |
| 6 | `get_upstream_features` | L7:F210@10, k=10 | Emb:" Nursing"@10 (de=8.19) +9 more |
| 7 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 8 | `inspect_feature` | L8, F9619 | " words and phrases related to medical treatment" |
| 9 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |

**Findings:** The L14 medical/management feature is driven primarily by the token embedding for "Nursing" at position 10. This token excites a chain of lower‑layer features: a nursing‑profession detector (L6:F15267), a hospital‑context detector (L8:F16339), and a health‑system name detector (L7:F210). These lower‑layer features in turn positively influence the target L14 feature, with additional modest contribu…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@10, k=10 | Emb:" Nursing"@10 (de=17.38) +9 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `get_upstream_features` | L4:F11037@10, k=10 | Emb:" Nursing"@10 (de=10.62) +9 more |
| 5 | `get_upstream_features` | L6:F15267@22, k=10 | Emb:" nursing"@22 (de=21.00) +9 more |
| 6 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `get_upstream_features` | L2:F10852@10, k=10 | Emb:" Nursing"@10 (de=11.44) +9 more |

**Findings:** The nursing‑profession feature (L6:F15267) is driven primarily by the raw token embeddings for the words 'Nursing'/'nursing' at the positions where they appear (direct_effect >17). Mid‑layer features (L4:11037, L5:1275, L2:10852) provide contextual reinforcement by detecting related healthcare professional terminology and degree titles. All traced paths reach the lower‑third of the model (layers ≤…

</details>

<details>
<summary><b>SA-4</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 2 | `get_upstream_features` | L18:F13596@10, k=10 | Emb:" Nursing"@10 (de=42.75) +9 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 5 | `get_upstream_features` | L6:F15267@10, k=10 | Emb:" Nursing"@10 (de=17.38) +9 more |

**Findings:** The target feature L18:F13596 (nurse manager role) at token position 10 receives its strongest drive from the raw input token " Nursing" (embedding direct effect 42.75). Mid‑level upstream features include L6:F15267, a generic nursing‑term detector, and L14:F3985, a leadership/management‑in‑medical context detector. Both feed positively into the nurse‑manager feature, providing the semantic ground…

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F11959 | " the word "graduated" and the word "more."" |
| 2 | `get_upstream_features` | L0:F11959@2, k=10 | Emb:" graduated"@2 (de=20.75) +9 more |
| 3 | `inspect_feature` | L7, F3979 | " words related to nursing and healthcare" |
| 4 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 5 | `get_upstream_features` | L7:F3979@2, k=10 | ❌ Feature (layer=7, feature_idx=3979) not found at pos=2. This |
| 6 | `get_upstream_features` | L7:F3979@10, k=10 | L6:F15267 (de=8.75) +9 more |
| 7 | `get_upstream_features` | L3:F15901@10, k=10 | Emb:" Nursing"@10 (de=15.12) +9 more |
| 8 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 9 | `get_upstream_features` | L6:F15267@10, k=10 | Emb:" Nursing"@10 (de=17.38) +9 more |
| 10 | `inspect_feature` | L0, F5038 | "the word "graduated" or variations of it" |

**Findings:** Tracing from the early‑layer feature L0:F11959 (position 2) shows that its activation is almost entirely explained by the raw input embedding for the token "graduated" (direct effect ≈20.75). The only other positive upstream token is "She" with a negligible effect (≈0.24). No upstream feature in layers ≤8 carries a gender‑related signal. The negative‑contribution features L7:F3979 and L3:F15901 ar…

</details>

<details>
<summary><b>SA-6</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F15159 | " words related to medicine and healthcare" |
| 2 | `get_upstream_features` | L15:F15159@10, k=10 | Emb:" Nursing"@10 (de=10.56) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `get_upstream_features` | L8:F16339@10, k=10 | Emb:" Nursing"@10 (de=7.66) +9 more |
| 5 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 6 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 7 | `get_upstream_features` | L6:F15267@10, k=10 | Emb:" Nursing"@10 (de=17.38) +9 more |
| 8 | `inspect_feature` | L15, F8289 | " words and phrases related to clinical medicine, including the terms c" |
| 9 | `get_upstream_features` | L15:F8289@10, k=10 | Emb:" Nursing"@10 (de=6.25) +9 more |
| 10 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 11 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 12 | `get_upstream_features` | L6:F4490@10, k=10 | Emb:" Nursing"@10 (de=11.62) +9 more |
| 13 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 14 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 15 | `get_upstream_features` | L4:F11037@10, k=10 | Emb:" Nursing"@10 (de=10.62) +9 more |
| 16 | `get_upstream_features` | L14:F3985@10, k=10 | Emb:" Nursing"@10 (de=12.12) +9 more |

**Findings:** Both target features (L15:F15159 and L15:F8289) are primarily driven by the input token "Nursing" at position 10. The signal passes through a short cascade of lower‑layer medical‑entity detectors (L6:F4490, L6:F15267, L8:F16339) before reaching the late‑layer medicine/clinical features. This satisfies the required conditions: we reached layers ≤8 and identified positive embedding connections. The …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F3979@10, k=5 → L6:F15267 (de=8.75) +4 more |
| 2 | `get_upstream_features` | L0:F6270@14, k=5 → Emb:" University"@14 (de=22.12) +4 more |
| 3 | `get_upstream_features` | L0:F16075@15, k=5 → Emb:" Of"@15 (de=26.50) +4 more |
| 4 | `get_upstream_features` | L14:F3985@10, k=5 → Emb:" Nursing"@10 (de=12.12) +4 more |
| 5 | `get_upstream_features` | L18:F13596@10, k=8 → Emb:" Nursing"@10 (de=42.75) +7 more |
| 6 | `get_upstream_features` | L15:F15159@10, k=5 → Emb:" Nursing"@10 (de=10.56) +4 more |
| 7 | `get_upstream_features` | L15:F8289@10, k=5 → Emb:" Nursing"@10 (de=6.25) +4 more |
| 8 | `get_upstream_features` | L0:F5038@2, k=5 → Emb:" graduated"@2 (de=22.25) +4 more |
| 9 | `get_upstream_features` | L6:F15267@10, k=8 → Emb:" Nursing"@10 (de=17.38) +7 more |

### Build

`build_circuit` → 16 nodes, 28 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 93,927 | 5,609 | 201,043 | 0 | $0.0470 | — | — |
| SA-4 | openai/gpt-oss-120b | 36,586 | 2,847 | 5,056 | 0 | $0.0073 | ✅ 3F/3E | Trace from L18:F13596 (nurse managers text feature) at pos 1… |
| SA-2 | openai/gpt-oss-120b | 65,187 | 5,012 | 7,648 | 0 | $0.0129 | ✅ 10F/10E | Trace from L6:F15267 (nursing profession references feature)… |
| SA-1 | openai/gpt-oss-120b | 110,311 | 6,962 | 8,640 | 0 | $0.0209 | ✅ 5F/8E | Trace from L14:F3985 (medical/management/nursing terms featu… |
| SA-5 | openai/gpt-oss-120b | 121,377 | 5,973 | 0 | 0 | $0.0218 | ✅ 3F/0E | Check the early-layer features that fired at pos 2 (the "She… |
| SA-6 | openai/gpt-oss-120b | 217,005 | 10,336 | 21,952 | 0 | $0.0391 | ✅ 7F/11E | Trace from L15:F15159 (medicine/healthcare feature) at pos 1… |
| **Total** | | **644,393** | **36,739** | **244,339** | **0** | **$0.1489** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 14s