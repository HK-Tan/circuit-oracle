# Circuit Oracle Report
**Date:** 2026-07-28 07:21:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies the profession primarily through a cascade of profession-grounded features anchored on the tokens "nurses" (pos 15) and "Perioperative" (perative pos 14 / Perio pos 13), NOT through gender/pronominal cues; a female-pronoun feature (L18:F14677 on "she") is present but acts as a small net suppressor, not a driver.

**Confidence:** 7

**Reasoning:** The top-20 features driving the probe score overwhelmingly encode *nursing/healthcare content* rather than gender:
- **Late-layer drivers** (L14:L18:L20) are all profession features: L20:F4927 (positions 14 and 15, direct_effect ≈ 0.07 each, activation 56–60), L19:F5028 ("healthcare industry"), L18:F13596 ("nurse managers' role, skills and leadership", direct_effect 0.098 at pos 15, activation 46), L18:F14457 ("healthcare implementation, patient care and technology", direct_effect 0.06). L14:F3985 ("management, leadership, medicine, studies, research", direct_effect 0.16 at pos 15) is the single largest positive driver.
- **Mid-layer profession features** (L4–L8) all cleanly identify the profession: L6:F15267 ("the profession of nursing", frac_nonzero 0.016), L7:F3979 ("nursing and healthcare", frac_nonzero 0.008), L7:F210 ("Asante Healthcare system"), L7:F8194 ("word 'nurse' or initials"), L8:F16339 ("hospital infections/bacteria"), L4:F4665 ("medical environments, treatments, personnel, facilities", promoted tokens: hospital/hospitals/medical/clinical). L4:L5 features about counseling, neuro-biology and broader healthcare professionals feed these.
- **Token-embedding path** is profession-rooted: the " nurses" embedding at pos 15 has direct_effect 16.1 → L6:F15267 and direct_effect 42 → L18:F13596; "perative" (pos 14, the tail of "Perioperative") has direct_effect 4.4 → L6:F15267; "Perio" (pos 13) has direct_effect 3.8 → L20:F4927.
- **Gender markers are present but suppressive**: L18:F14677 ("instances of women or girls being mentioned", fires on "she", pos 7, direct_effect −0.065) and L6:F11646 ("references to women … triggered by pronouns and titles", direct_effect 5.6) and L12:F12940 ("female pronouns and possessive pronouns") all appear. Critically, L18:F14677 has a **negative** direct_effect on the probe and L3:F15901 ("mentions of nurses, nursing, and nurse management") is also **suppressive** (direct_effect −0.13). The "she" embedding actually flows through a *generic* pronoun feature path; the `get_source_influence` query from pos 7 returns S_pct_of_total = −0.7% vs R_pct_of_total = 2.4% (S_over_R = −0.29), meaning pos 7 ("she") is a net *negligible-to-slightly-negative* contributor compared to the strongest non-source position. The probe is **not** copying the pronoun signal.
- **Conclusion**: The user's concern is *not* confirmed by this graph. The mechanism driving the profession classification is a clean, textually grounded medical/nursing vocabulary cascade: tokens "nurses" + "Perioperative"/"Perio" → L6 nursing-profession + L4 medical-environment features → L14 leadership/medicine feature → L18 nurse-manager and healthcare-implementation concepts → L19/L20 healthcare-industry and role representations. The "she" pronoun participates only through a suppressive path, and source-influence propagation shows the pronoun position contributes essentially zero net signal to the probe score.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 7 | Fem-pronoun context (slight suppressor) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 14 | Late-layer nurse-manager leadership concept | — | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 15 | Late-layer nurse-manager leadership concept | — | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |
| [L19:F5028](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/5028) | 14 | Late-layer nurse-manager leadership concept |  words related to the healthcare industry | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/5028) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 15 | Late-layer nurse-manager leadership concept |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 14 | Late-layer nurse-manager leadership concept |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F14457](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) | 14 | Late-layer nurse-manager leadership concept |  words or phrases related to healthcare implementation, patient care and technology | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 15 | Mid-layer medical/nursing context | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 14 | Mid-layer medical/nursing context | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 15 | Mid-layer medical/nursing context | text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 15 | Mid-layer medical/nursing context | words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 15 | Mid-layer medical/nursing context |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F8194](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) | 15 | Mid-layer medical/nursing context |  mentions of the word "nurse" or the initials or last names of people | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Mid-layer medical/nursing context | words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | Mid-layer medical/nursing context | words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 14 | Mid-layer medical/nursing context |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 45 | Mid-layer medical/nursing context |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 15 | Early lexical/acronym scaffolding | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F8751](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8751) | 15 | Early lexical/acronym scaffolding | cell types in the brain, especially glial cells and neurons, and related scientific terminology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8751) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 15 | Early lexical/acronym scaffolding | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L1:F1889](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1889) | 14 | Early lexical/acronym scaffolding | words related to medical studies, procedures, and patient outcomes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1889) |
| [L0:F437](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/437) | 1 | Early lexical/acronym scaffolding | words that are names or titles of things, or otherwise capitalized non-nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/437) |
| [L0:F7344](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7344) | 1 | Early lexical/acronym scaffolding | content markers like figures and section headers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7344) |
| [L3:F373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) | 1 | Early lexical/acronym scaffolding | word beginnings with the letters "a," "h," "i," "r," and "p" (perhaps prefixes and/or related to medical or scientific terms) | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Early lexical/acronym scaffolding | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 15 | Suppressive (born/raised phrase, women-mention) |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L2:F15437](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) | 15 | Suppressive (born/raised phrase, women-mention) |  words related to nurses and sound | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) |
| [L4:F8736](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8736) | 2 | Suppressive (born/raised phrase, women-mention) |  the phrase "born and raised" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8736) |
| [L9:F16275](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/16275) | 15 | Suppressive (born/raised phrase, women-mention) |  terms related to the workplace environment, including job titles, business descriptions or complaints about work | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/16275) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.163 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@15` | ✅ reported | 4 | 7 | Trace from L14:F3985 (pos 15, direct_effect 0.1631). What does this feature enco… |
| SA-2 | `L6:F15267@15` | ✅ reported | 6 | 5 | Trace from L6:F15267 (pos 15, direct_effect 0.1582). What does this feature enco… |
| SA-3 | `L18:F13596@15` | ✅ reported | 3 | 5 | Trace from L18:F13596 (pos 15, direct_effect 0.0981). What does this feature enc… |
| SA-4 | `L4:F4665@14` | ✅ reported | 4 | 3 | Trace from L4:F4665 (pos 14, direct_effect 0.105). What does this feature encode… |
| SA-5 | `L4:F9757@1` | ✅ reported | 4 | 3 | Trace from L4:F9757 (pos 1, direct_effect 0.0752). What does this feature encode… |
| SA-6 | `L8:F16339@15` | ✅ reported | 6 | 7 | Trace from L8:F16339 (pos 15, direct_effect 0.1055). What does this feature enco… |
| SA-7 | `L20:F4927@14` | ❌ error | — | — | Trace from L20:F4927 (pos 14, direct_effect 0.0752). What does this feature enco… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@15, k=10 | Emb:" nurses"@15 (de=10.62) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 5 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 6 | `get_upstream_features` | L8:F16339@15, k=10 | Emb:" nurses"@15 (de=4.72) +9 more |
| 7 | `get_upstream_features` | L14:F3985@15, k=10 | Emb:" nurses"@15 (de=10.62) +9 more |

**Findings:** The target L14:F3985 is a higher‑level healthcare‑context feature that aggregates signals about nursing leadership and medical management. Its strongest upstream drivers are the raw token embedding for "nurses" (pos 15) and mid‑level features that detect hospital infection language (L8:F16339), specific hospital system mentions (L7:F210), and nursing‑profession terminology (L6:F15267). All three u…

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 5 | `get_upstream_features` | L4:F11037@15, k=10 | Emb:" nurses"@15 (de=5.16) +9 more |
| 6 | `get_upstream_features` | L4:F8751@15, k=10 | Emb:" nurses"@15 (de=9.81) +9 more |
| 7 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |

**Findings:** L6:F15267 is a mid‑layer (layer 6) feature that strongly activates on the token "nurses" and related nursing terminology. Its top upstream drivers are the raw embedding for the word "nurses" (direct_effect ~16), a partial embedding for "perative", and a set of mid‑to‑high‑layer medical‑context features (layers 4‑5) that detect counseling, neuro‑biology, and broader healthcare professional language…

</details>

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 2 | `get_upstream_features` | L18:F13596@15, k=10 | Emb:" nurses"@15 (de=42.00) +9 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |
| 5 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |

**Findings:** The target L18:F13596 (pos 15) is a high‑level nurse‑manager concept. Its strongest upstream driver is the raw token embedding for the word " nurses" (direct_effect 42), which directly excites the feature. The next‑most important upstream node is a lower‑layer feature L6:F15267 that detects nursing‑profession terminology; it itself is strongly driven by the same " nurses" embedding (direct_effect …

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 2 | `get_upstream_features` | L4:F4665@14, k=10 | Emb:"perative"@14 (de=15.44) +9 more |
| 3 | `inspect_feature` | L1, F1889 | " words related to medical studies, procedures, and patient outcomes" |
| 4 | `inspect_feature` | L3, F14131 | " the word "all"" |
| 5 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 6 | `get_upstream_features` | L1:F1889@14, k=10 | Emb:"perative"@14 (de=5.38) +9 more |

**Findings:** The target feature L4:F4665 is a medical‑environment detector (hospital, department, etc.). Its strongest positive upstream driver is a low‑level embedding token "perative" (pos 14) with a huge direct effect, indicating the word 'imperative' in the prompt is feeding strongly into the medical context. The main mid‑level upstream contributors are L1:F1889 (medical procedure terminology) and L3:F1413…

</details>

<details>
<summary><b>SA-5</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F9757 | "various acronyms, IDs, and symbols, possibly related to scientific dat" |
| 2 | `get_upstream_features` | L4:F9757@1, k=10 | Emb:"<bos>"@0 (de=14.00) +9 more |
| 3 | `inspect_feature` | L0, F7344 | " content markers like figures and section headers" |
| 4 | `get_upstream_features` | L0:F7344@1, k=10 | Emb:"<bos>"@0 (de=11.50) +9 more |
| 5 | `inspect_feature` | L0, F437 | " words that are names or titles of things, or otherwise capitalized no" |
| 6 | `inspect_feature` | L3, F373 | " word beginnings with the letters "a," "h,""i," "r," and "p" (perhaps " |

**Findings:** L4:F9757 (pos 1) is a mid‑layer detector for acronyms, IDs and scientific symbols. Its strongest positive drivers are lower‑layer features: L0:F7344 (figures/section headers), L0:F437 (capitalised proper nouns/titles) and L3:F373 (common scientific prefixes). Both of these lower‑layer nodes lie in layers ≤8, satisfying the lower‑third floor, and the circuit also receives direct excitatory input fr…

</details>

<details>
<summary><b>SA-6</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 2 | `get_upstream_features` | L8:F16339@15, k=10 | Emb:" nurses"@15 (de=4.72) +9 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |
| 5 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 6 | `inspect_feature` | L7, F8194 | "mentions of the word "nurse" or the initials or last names of people" |
| 7 | `get_upstream_features` | L7:F210@15, k=10 | Emb:" nurses"@15 (de=11.38) +9 more |

**Findings:** L8:F16339 is a medical‑safety feature that fires on discussion of hospital‑acquired infections and bacterial threats. Its strongest upstream drivers are the raw token embedding for 'nurses' and a downstream nursing‑profession feature (L6:15267), both of which are clearly medical‑staff signals. Additional upstream contributions come from a hospital‑system name feature (L7:210) and a generic 'nurse'…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L3:15901, L7:3979, L2:15437, L18:14677, L9:16275, L4:8736, L18:14457 |
| 2 | `get_upstream_features` | L18:F14677@7, k=15 → Emb:" she"@7 (de=28.38) +14 more |
| 3 | `inspect_feature` | L4, F4665 → " words and phrases related to medical environments, treatments, person" |
| 4 | `get_upstream_features` | L20:F4927@14, k=10 → L18:F13596 (de=14.31) +9 more |
| 5 | `inspect_feature` ×5 | L6:11646, L12:12940, L19:5028, L4:7864, L18:14457 |
| 6 | `get_source_influence` | {'depth': 5, 'source_positions': [7]} → {'depth': 5, 'source_positions': [7], 'S_pct_of_total': -0.699, 'R_pct_of_total' |

### Build

`build_circuit` → 12 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 39,896 | 4,733 | 134,737 | 0 | $0.0257 | — | — |
| SA-3 | openai/gpt-oss-120b | 34,262 | 2,986 | 5,088 | 0 | $0.0070 | ✅ 3F/5E | Trace from L18:F13596 (pos 15, direct_effect 0.0981). What d… |
| SA-2 | openai/gpt-oss-120b | 57,549 | 3,872 | 5,088 | 0 | $0.0110 | ✅ 6F/5E | Trace from L6:F15267 (pos 15, direct_effect 0.1582). What do… |
| SA-6 | openai/gpt-oss-120b | 60,349 | 4,066 | 2,592 | 0 | $0.0115 | ✅ 6F/7E | Trace from L8:F16339 (pos 15, direct_effect 0.1055). What do… |
| SA-5 | openai/gpt-oss-120b | 49,380 | 3,679 | 7,616 | 0 | $0.0097 | ✅ 4F/3E | Trace from L4:F9757 (pos 1, direct_effect 0.0752). What does… |
| SA-4 | openai/gpt-oss-120b | 51,333 | 3,849 | 5,056 | 0 | $0.0101 | ✅ 4F/3E | Trace from L4:F4665 (pos 14, direct_effect 0.105). What does… |
| SA-1 | openai/gpt-oss-120b | 61,163 | 3,835 | 5,184 | 0 | $0.0116 | ✅ 4F/7E | Trace from L14:F3985 (pos 15, direct_effect 0.1631). What do… |
| **Total** | | **353,932** | **27,020** | **165,361** | **0** | **$0.0867** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 1s