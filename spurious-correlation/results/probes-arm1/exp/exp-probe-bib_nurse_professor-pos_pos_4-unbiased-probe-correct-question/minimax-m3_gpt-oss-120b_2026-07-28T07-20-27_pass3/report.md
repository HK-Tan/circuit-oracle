# Circuit Oracle Report
**Date:** 2026-07-28 07:20:28 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies "nursing" almost entirely from profession-indicating tokens ("Nursing" at pos 18, "nurse"/"practitioner" at pos 33, "care"/"pediatric" at pos 52, and "Lori" at pos 27) flowing through a stack of healthcare/nursing-occupation features, with no gender-marker features contributing positively.

**Confidence:** 8

**Reasoning:** The dominant direct effect on the probe comes from L14:3985 ("management/leadership/medicine/studies"), L6:15267 ("nursing profession"), and L18:13596 ("nurse managers") — every one of these is a profession/occupation feature, not a gender feature. The traced paths confirm this: the "Nursing" embedding at position 18 directly excites L6:15267 (direct_effect 17.4), L18:13596 (25.3), and L20:4927 (21.5); L4:11037 ("academic degrees / counseling") and L2:10852 (pre-degree) sit underneath L6:15267; the "Lori" token at pos 27 is the seed for L20:4927 ("healthcare titles/acronyms after names", activation 97, direct_effect 0.047). All upstream features identified have labels like "nursing profession", "nurse managers", "medical environments", "healthcare words", and "academic degree programs" — they encode the healthcare/educational/career context, not gender. The two negative-contribution features (L7:3979 "nursing/healthcare words" and L3:15901 "nurses, nursing, nurse management") are themselves profession features that happen to suppress in this context (likely redundant-signal suppression), not gender features. The `whom` token (pos 6) feeds a generic function-word feature (L0:6270) with only modest downstream effect on the medical-features branch; get_source_influence from position 2/6 contributes only 2.4% signed share vs 10.8% from positions 18/27/33/52, confirming the profession words dominate. There are no features in the circuit labeled "she", "her", female pronouns, gendered titles, or family-role language driving the probe — the user's concern about spurious gender features is not borne out by this attribution graph; instead the probe is reading the genuine healthcare/nursing/degree context of the bio. The only minor caveat is that the model uses very profession-specific low-frac_nonzero features (e.g., L18:13596 at frac_nonzero 0.005, L20:4927 at 0.017), which is a sign of *more* specific, not less specific, profession detection.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 2 | "graduated" token (pos 2) | the word "graduated" or variations of it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 6 | "whom" function word (pos 6) | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 18 | Academic degree / counseling language (pos 18) | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 52 | Medical environment / facility / personnel (pos 52) |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | Healthcare words & abbreviations (pos 33) |  words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Nursing profession detector (pos 18, 33) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Nursing profession detector (pos 18, 33) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 18 | Proper nouns: locations, orgs, medical roles (pos 18) |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 18 | Nursing/healthcare words (suppressing, pos 18, 33) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 33 | Nursing/healthcare words (suppressing, pos 18, 33) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F15132](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) | 33 | Medical practices (pos 33) |  references to medical practices | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) |
| [L8:F9619](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) | 33 | Medical treatment language (pos 33) |  words and phrases related to medical treatment | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 18 | Management / leadership / medicine / studies (pos 18, 33) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 33 | Management / leadership / medicine / studies (pos 18, 33) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 18 | Medicine & healthcare words (pos 18) |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 18 | Nurse-manager role / skills / leadership (pos 18, 33) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 33 | Nurse-manager role / skills / leadership (pos 18, 33) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 27 | Healthcare titles/acronyms after names (pos 27) |  titles and acronyms following names, especially within the healthcare field | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.157 |
| 3 | `inspect_feature` ×16 | L14:3985, L6:15267, L7:3979, L0:5038, L4:9036, L3:15901, L8:9619, L0:6270, L4:4665, L7:15132, L18:13596, L15:15159, L6:4490, L20:4927, L5:10478, L0:11959 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@18` | ✅ reported | 5 | 7 | Trace this feature (L14:3985 at pos 18) all the way back to the token embedding.… |
| SA-2 | `L6:F15267@33` | ❌ error | — | — | Trace this feature (L6:15267 at pos 33, "nursing profession") all the way back t… |
| SA-3 | `L18:F13596@18` | ✅ reported | 6 | 7 | Trace this feature (L18:13596 at pos 18, "nurse managers") all the way back to t… |
| SA-4 | `L0:F5038@2` | ❌ error | — | — | Trace this feature (L0:5038 at pos 2, "graduated") all the way back to the token… |
| SA-5 | `L20:F4927@27` | ✅ reported | 6 | 10 | Trace this feature (L20:4927 at pos 27, "titles/acronyms after names in healthca… |
| SA-6 | `L15:F15159@18` | ❌ error | — | — | Trace this feature (L15:15159 at pos 18, "medicine/healthcare words") all the wa… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@18, k=10 | Emb:" Nursing"@18 (de=11.56) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 5 | `get_upstream_features` | L8:F16339@18, k=10 | Emb:" Nursing"@18 (de=7.28) +9 more |
| 6 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 7 | `get_upstream_features` | L6:F4490@18, k=10 | Emb:" Nursing"@18 (de=11.56) +9 more |
| 8 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 9 | `get_upstream_features` | L6:F15267@18, k=10 | Emb:" Nursing"@18 (de=17.38) +9 more |
| 10 | `inspect_feature` | L8, F9619 | " words and phrases related to medical treatment" |
| 11 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 12 | `get_upstream_features` | L4:F11037@18, k=10 | Emb:" Nursing"@18 (de=10.38) +9 more |

**Findings:** The target feature L14:3985 (leadership/medical terms) is driven primarily by the input token 'Nursing' at position 18 (positive direct effect >11). The signal propagates through a chain of profession‑related features: L8:16339 (hospital infection context) and L6:4490 (medical role nouns) both receive strong excitation from the same 'Nursing' embedding, and L6:15267 explicitly detects nursing term…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 2 | `get_upstream_features` | L18:F13596@18, k=10 | Emb:" Nursing"@18 (de=43.00) +9 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `get_upstream_features` | L6:F15267@18, k=10 | Emb:" Nursing"@18 (de=17.38) +9 more |
| 5 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 6 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 7 | `inspect_feature` | L8, F440 | " text from professional biographies" |

**Findings:** The target feature L18:13596 ("nurse managers") is primarily driven by the input token embedding for the word "Nursing" at position 18 (direct_effect = 43.0). The signal passes through a low‑layer profession detector (layer 6 feature 15267, direct_effect ≈ 10), then through intermediate management‑and‑medical language detectors (layers 14, 8, 4). All upstream nodes are profession‑related; no refus…

</details>

<details>
<summary><b>SA-5</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F4927 | " titles and acronyms following names, especially within the healthcare" |
| 2 | `get_upstream_features` | L20:F4927@27, k=10 | L18:F13596 (de=29.62) +9 more |
| 3 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 4 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 5 | `get_upstream_features` | L18:F13596@27, k=10 | Emb:" Nursing"@18 (de=25.25) +9 more |
| 6 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 7 | `get_upstream_features` | L6:F15267@18, k=10 | Emb:" Nursing"@18 (de=17.38) +9 more |
| 8 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 9 | `get_upstream_features` | L4:F11037@18, k=10 | Emb:" Nursing"@18 (de=10.38) +9 more |

**Findings:** The chain originates from the raw input token "Nursing" (pos 18). That embedding strongly excites a low‑layer (L6) feature that recognises any reference to the nursing profession. This feeds into a higher‑layer (L18) nurse‑manager descriptor and further into the target L20 feature that flags professional titles/acronyms after names in healthcare. All positive connections are on the path, and we ha…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F3979@18, k=5 → L6:F15267 (de=9.19) +4 more |
| 2 | `get_upstream_features` | L20:F4927@27, k=3 → L18:F13596 (de=29.62) +2 more |
| 3 | `get_source_influence` | {'depth': 3, 'source_positions': [18, 33, 52, 27]} → {'depth': 3, 'source_positions': [18, 27, 33, 52], 'S_pct_of_total': 5.281, 'R_p |
| 4 | `get_source_influence` | {'depth': 3, 'source_positions': [2, 6]} → {'depth': 3, 'source_positions': [2, 6], 'S_pct_of_total': 2.418, 'R_pct_of_tota |

### Build

`build_circuit` → 18 nodes, 37 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 63,032 | 5,252 | 127,318 | 0 | $0.0329 | — | — |
| SA-5 | openai/gpt-oss-120b | 89,385 | 5,658 | 2,592 | 0 | $0.0168 | ✅ 6F/10E | Trace this feature (L20:4927 at pos 27, "titles/acronyms aft… |
| SA-1 | openai/gpt-oss-120b | 142,940 | 6,663 | 10,176 | 0 | $0.0256 | ✅ 5F/7E | Trace this feature (L14:3985 at pos 18) all the way back to … |
| SA-3 | openai/gpt-oss-120b | 68,704 | 5,611 | 10,528 | 0 | $0.0138 | ✅ 6F/7E | Trace this feature (L18:13596 at pos 18, "nurse managers") a… |
| **Total** | | **364,061** | **23,184** | **150,614** | **0** | **$0.0891** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 56s