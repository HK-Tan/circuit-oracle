# Circuit Oracle Report
**Date:** 2026-07-28 07:22:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

Based on the extensive tracing, the circuit reaches token-embedding nodes via early-layer features (L0:5038 "graduated", L0:11959 "graduated", L2:10852 "academic titles/degrees", L2:9995 "occupations/fields of study", etc.), and the embedding nodes for the literal "Nursing" (pos 18), "practitioner" (pos 33), and "nurse" (pos 32) tokens are the dominant drivers of the late-layer features. I have already included these as `tok_nursing_practitioner` and `tok_graduated` nodes. The circuit is complete.

**Analysis:** The probe's classification of "nurse" is driven by genuine profession-indicating features (nursing lexicon, healthcare terminology, academic degrees) flowing from the literal token embeddings of "Nursing," "nurse," and "practitioner," not by gender markers.

**Confidence:** 8

**Reasoning:** The terminal node is the probe direction (nurse profession), and it is fed primarily by L18:13596 ("nurse managers / nursing leadership", frac_nonzero=0.00495) and L20:4927 ("titles and acronyms following names, especially within the healthcare field", frac_nonzero=0.01744). These late-layer profession-specific features sit on top of a deep, well-formed chain of healthcare/nursing-concept features: L14:3985 ("management, leadership, medicine, studies, research"), L15:15159 ("medicine and healthcare"), L8:9619/L7:15132/L8:12680 (clinical/medical-treatment), L4:9036/L4:4665 (healthcare words and abbreviations), L6:15267 ("words referring to the profession of nursing", frac_nonzero=0.01594), L3:15901 ("nurses, nursing, and nurse management"), L7:3979 ("nursing and healthcare"), L5:1275 ("healthcare professionals and medical fields"), L4:11037 ("counseling, therapy, social work, academic degree programs"), L2:10852 ("academic titles and degrees"), L2:9995 ("occupations and fields of study"). The two earliest driving features are L0:5038/L0:11959 ("graduated"), which signal professional biography framing.

Crucially, every one of these features was inspected against its top-activating examples and none of them selectively fires on female pronouns, gendered names, or "She/Her" — the L18:13596 top examples are about nurse-manager leadership literature, L6:15267 fires on "RN", "registered nurse", L4:9036 on "practitioner/practitioners", L0:5038 on "graduated". The embedding nodes that anchor the circuit are the literal "Nursing" (pos 18), "nurse" (pos 32), and "practitioner" (pos 33) tokens, plus "graduated" (pos 2) and "Lori" (pos 1). Signal flow: `tok_nursing_practitioner` → `mid_profession_nursing` (L6:15267, L3:15901, L7:3979) → `mid_healthcare_practice` (L7-L8) → `mid_management_medicine` (L14:3985) → `late_nurse_manager` (L18:13596) → output. Parallel support flows from `tok_graduated` → `early_graduated` (L0:5038/11959) → academic-degree/healthcare-professional features, reinforcing the professional-biography context.

The user's concern that the circuit relies on spurious gender markers is **not supported**. There is no "She" or "Her" token represented in the embedding layer of the traced paths, no female-name-specific feature with positive direct_effect on the probe, and no pronoun-detection feature active in the top-20 list. The "Lori" embedding (pos 1) does appear as a small contributor to L20:4927 and L18:13596 (direct_effect ≈ 2.4-2.9), but this is the name itself functioning as a proper-noun signal, not a gender signal — and its magnitude is dwarfed by the "Nursing" (direct_effect 21.5-30.5) and "nurse"/"practitioner" embeddings (direct_effect 5.7-14.4). The probe's classification is therefore driven by genuine, content-bearing profession indicators (the nursing/healthcare lexicon and professional biography framing) rather than by gendered correlates.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 18 | Nurse managers / nursing leadership (L18:13596) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 33 | Nurse managers / nursing leadership (L18:13596) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F14457](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) | 27 | Nurse managers / nursing leadership (L18:13596) |  words or phrases related to healthcare implementation, patient care and technology | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 27 | Healthcare titles/acronyms after names (L20:4927) |  titles and acronyms following names, especially within the healthcare field | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 18 | Management / medicine / research terms (L14:3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 33 | Management / medicine / research terms (L14:3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 18 | Medicine / healthcare words (L15:15159) |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L15:F8289](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) | 18 | Medicine / healthcare words (L15:15159) |  words and phrases related to clinical medicine, including the terms clinicians use and related scientific fields | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) |
| [L8:F9619](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) | 33 | Healthcare practice / clinical setting (L8:9619, L7:15132, L8:12680) |  words and phrases related to medical treatment | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) |
| [L8:F9619](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) | 18 | Healthcare practice / clinical setting (L8:9619, L7:15132, L8:12680) |  words and phrases related to medical treatment | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) |
| [L7:F15132](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) | 33 | Healthcare practice / clinical setting (L8:9619, L7:15132, L8:12680) |  references to medical practices | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) |
| [L8:F12680](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12680) | 33 | Healthcare practice / clinical setting (L8:9619, L7:15132, L8:12680) |  words and phrases that would be used in a clinical setting, especially in primary care | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12680) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 18 | Healthcare practice / clinical setting (L8:9619, L7:15132, L8:12680) |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | Healthcare words / abbreviations (L4:9036, L4:4665) |  words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 52 | Healthcare words / abbreviations (L4:9036, L4:4665) |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Nursing profession / professional bio (L6:15267, L3:15901, L7:3979, L8:440, L7:5829, L7:8194) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Nursing profession / professional bio (L6:15267, L3:15901, L7:3979, L8:440, L7:5829, L7:8194) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 18 | Nursing profession / professional bio (L6:15267, L3:15901, L7:3979, L8:440, L7:5829, L7:8194) |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 33 | Nursing profession / professional bio (L6:15267, L3:15901, L7:3979, L8:440, L7:5829, L7:8194) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L8:F440](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/440) | 18 | Nursing profession / professional bio (L6:15267, L3:15901, L7:3979, L8:440, L7:5829, L7:8194) |  text from professional biographies | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/440) |
| [L7:F5829](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5829) | 18 | Nursing profession / professional bio (L6:15267, L3:15901, L7:3979, L8:440, L7:5829, L7:8194) | mentions of nursing or higher education degrees. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5829) |
| [L7:F8194](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) | 18 | Nursing profession / professional bio (L6:15267, L3:15901, L7:3979, L8:440, L7:5829, L7:8194) | mentions of the word "nurse" or the initials or last names of people | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 18 | Proper nouns / medical roles / hospital codes (L6:4490, L7:210) |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 18 | Proper nouns / medical roles / hospital codes (L6:4490, L7:210) |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | Healthcare professionals / academic study (L5:1275, L5:10392, L4:11037, L1:1494, L1:15395) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 18 | Healthcare professionals / academic study (L5:1275, L5:10392, L4:11037, L1:1494, L1:15395) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 18 | Healthcare professionals / academic study (L5:1275, L5:10392, L4:11037, L1:1494, L1:15395) |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 18 | Healthcare professionals / academic study (L5:1275, L5:10392, L4:11037, L1:1494, L1:15395) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 33 | Healthcare professionals / academic study (L5:1275, L5:10392, L4:11037, L1:1494, L1:15395) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 33 | Healthcare professionals / academic study (L5:1275, L5:10392, L4:11037, L1:1494, L1:15395) |  words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L1:F15395](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) | 33 | Healthcare professionals / academic study (L5:1275, L5:10392, L4:11037, L1:1494, L1:15395) |  words and abbreviations related to medical studies and procedures | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 18 | Academic degrees (L2:10852, L7:14129) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 33 | Academic degrees (L2:10852, L7:14129) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 2 | Word 'graduated' (L0:5038, L0:11959) | the word "graduated" or variations of it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L0:F11959](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) | 2 | Word 'graduated' (L0:5038, L0:11959) |  the word "graduated" and the word "more." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) |
| [L2:F9995](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) | 18 | Profession / occupation / medical specialty words (L2:9995, L2:2589) |  terms related to occupations and fields of study | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 33 | Profession / occupation / medical specialty words (L2:9995, L2:2589) |  words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: 'Nursing' (pos 18), 'practitioner' (pos 33), 'nurse' (pos 32) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 33 | Emb: 'Nursing' (pos 18), 'practitioner' (pos 33), 'nurse' (pos 32) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 32 | Emb: 'Nursing' (pos 18), 'practitioner' (pos 33), 'nurse' (pos 32) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: 'graduated' (pos 2), 'Lori' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'graduated' (pos 2), 'Lori' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.157 |
| 3 | `inspect_feature` ×16 | L14:3985, L6:15267, L4:9036, L8:9619, L20:4927, L18:13596, L15:15159, L0:5038, L4:4665, L0:6270, L7:3979, L3:15901, L7:15132, L6:4490, L0:11959, L5:10478 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@18` | ❌ error | — | — | Trace this feature upstream to find which tokens and earlier features drive "man… |
| SA-2 | `L6:F15267@33` | ❌ error | — | — | Trace this "nursing profession" feature upstream to find which input tokens driv… |
| SA-3 | `L18:F13596@18` | ❌ error | — | — | Trace this "nurse managers/leadership" feature upstream to find which input toke… |
| SA-4 | `L20:F4927@27` | ❌ error | — | — | Trace this "healthcare titles/acronyms after names" feature upstream. Position 2… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@18, k=15 → Emb:" Nursing"@18 (de=11.56) +14 more |
| 2 | `get_upstream_features` | L6:F15267@33, k=15 → Emb:" nurse"@32 (de=5.66) +14 more |
| 3 | `get_upstream_features` | L20:F4927@27, k=15 → L18:F13596 (de=29.62) +14 more |
| 4 | `get_upstream_features` | L18:F13596@18, k=15 → Emb:" Nursing"@18 (de=43.00) +14 more |
| 5 | `get_upstream_features` | L18:F13596@33, k=10 → Emb:" nurse"@32 (de=14.44) +9 more |
| 6 | `get_upstream_features` | L14:F3985@33, k=10 → L4:F9036 (de=6.41) +9 more |
| 7 | `get_upstream_features` | L6:F15267@18, k=10 → Emb:" Nursing"@18 (de=17.38) +9 more |
| 8 | `get_upstream_features` | L8:F16339@18, k=10 → Emb:" Nursing"@18 (de=7.28) +9 more |
| 9 | `get_upstream_features` | L5:F1275@33, k=10 → L4:F9036 (de=1.70) +9 more |
| 10 | `get_upstream_features` | L5:F1275@18, k=10 → L4:F11037 (de=2.05) +9 more |
| 11 | `inspect_feature` ×10 | L8:16339, L5:1275, L4:11037, L8:440, L7:210, L15:15159, L6:170, L7:5829, L7:8194, L7:14129 |
| 12 | `get_upstream_features` | L8:F9619@33, k=10 → L6:F15267 (de=5.53) +9 more |
| 13 | `get_upstream_features` | L7:F15132@33, k=10 → Emb:" practitioner"@33 (de=11.12) +9 more |
| 14 | `get_upstream_features` | L7:F14129@33, k=8 → Emb:" practitioner"@33 (de=4.97) +7 more |
| 15 | `get_upstream_features` | L4:F11037@33, k=8 → Emb:" practitioner"@33 (de=6.47) +7 more |
| 16 | `inspect_feature` ×10 | L5:11028, L1:1494, L6:13357, L8:4607, L15:8289, L1:15395, L18:14457, L17:3936, L7:1547, L8:12680 |
| 17 | `get_upstream_features` | L14:F3985@2, k=5 → ❌ Feature (layer=14, feature_idx=3985) not found at pos=2. Thi |
| 18 | `get_upstream_features` | L6:F15267@2, k=5 → ❌ Feature (layer=6, feature_idx=15267) not found at pos=2. Thi |
| 19 | `get_upstream_features` | L20:F4927@18, k=8 → Emb:" Nursing"@18 (de=30.50) +7 more |
| 20 | `inspect_feature` ×11 | L16:1007, L2:2589, L5:10392, L3:13034, L3:5611, L3:3105, L3:6246, L4:8751, L4:15317, L2:10852, L2:9995 |

### Build

`build_circuit` → 15 nodes, 28 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 85,499 | 7,755 | 465,431 | 0 | $0.0629 | — | — |
| **Total** | | **85,499** | **7,755** | **465,431** | **0** | **$0.0629** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 39s