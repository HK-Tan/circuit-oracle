# Circuit Oracle Report
**Date:** 2026-07-28 07:22:49 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "nurse" is driven by a clean profession-anchored circuit rooted in the literal tokens "nurse", "Labor", "Delivery", and "Nursing" — not by spurious gender markers.

**Confidence:** 8/10

**Reasoning:** Signal flows from the genuine profession tokens at positions 9/11/12/19/66 (Emb: " Labor", " Delivery", " nurse", " Nursing", " midwife") upward through a clean hierarchy of profession-specific features. The late-layer drivers are L14:F3985 ("medicine/leadership/management/patients" — promoted tokens: patients, Medical, clinical; frac=0.066) and L18:F13596 ("nurse managers' role, skills and leadership" — promoted: Nurse, Nursing; frac=0.005), with L20:F4927 ("titles and acronyms following names, especially healthcare" — promoted: nursing, Nursing, nurse, RN; frac=0.017) feeding the probe output. L7:F3979 ("nursing and healthcare") and L6:F15267 ("words referring to the profession of nursing") act as mid-layer profession aggregators.

Crucially, the user's concern about gender is **not supported** by this circuit. I searched the top-15 features and the entire upstream chain at positions 12 and 15, and found **no she/her/female/Melissa-as-female** features with positive direct_effect on the probe. "Melissa" (pos 5) and "her" (pos 15) only appear as low-magnitude embeddings; "her" actually has a **negative** direct_effect (-4.2) on L20:F4927, meaning the pronoun mildly *suppresses* the nurse classification rather than driving it. The name "Melissa" is not routed to a profession signal — it sits in a generic function-word/name supernode (L0:F9911 "that", L0:F8444 "to", L0:F7532 "proper nouns") with direct_effect=+0.06 on the output, but it doesn't propagate through the nursing circuit. The single feature (L0:F7532 "proper nouns") that fires on "Melissa" is a generic name detector, not a gendered-noun feature, and its path to the output is weak.

The strongest profession-evidence path is: "nurse" (pos 12) emb → L0:F8854 (the word "nurse", frac=0.005) → L3:F15901 (nurse/nursing/nurse management, frac=0.005) → L6:F15267 (nursing profession, frac=0.016) → L14:F3985 (medicine+leadership, frac=0.066) → L18:F13596 (nurse manager role, frac=0.005) → L20:F4927 (healthcare titles after names, frac=0.017) → output. A parallel path runs through "Nursing" (pos 19) and "Midwife" (pos 66) to the same L6/L18/L20 features — all semantically nursing/medical/obstetric.

The "Labor and Delivery" specialty is captured by L2:F10127 ("the word 'delivery' or 'deliver'", frac=0.002), L3:F10198 (anesthetics/medical procedures), L4:F13803 (obstetrics and gynecology — promoted: pregnancy, postpartum, gravid, fertility; frac=0.014), L7:F2861 (pregnancy and labor, frac=0.005), and L6:F9980 (medical specialties promoted: hospital, medical). These are specialty/clinical context features, not gendered ones.

Conclusion: the probe reads genuine profession tokens (nurse, Labor, Delivery, Nursing, midwife) through a tight profession-feature chain (L0 word→L3 nurse-mgmt→L6 nursing profession→L14 medicine-leadership→L18 nurse manager role→L20 healthcare titles). There is no evidence of the circuit using "Melissa", "she", or "her" as profession predictors. The user's suspicion is reasonable to check, but the data here contradicts it.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) | 12 | Layer 0: 'nurse' word features |  the word "nurse" as well as some pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) |
| [L0:F10920](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) | 12 | Layer 0: 'nurse' word features |  the word "nurse" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) |
| [L0:F15074](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15074) | 12 | Layer 0: 'nurse' word features |  words and phrases related to nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15074) |
| [L0:F1832](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) | 9 | Layer 0: 'labor' word feature | the word "labor" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) |
| [L1:F7152](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7152) | 11 | Layer 0/1: 'delivery' word feature | the word "delivery" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7152) |
| [L0:F9911](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9911) | 3 | Layer 0: function words & name |  the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9911) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 2 | Layer 0: function words & name | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 5 | Layer 0: function words & name |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 27 | Layer 0: function words & name |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 28 | Layer 0: function words & name |  the 1990's | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 28 | Layer 0: function words & name |  a mix of possessive pronouns like "his", names associated with historical records, and years. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L1:F14469](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) | 12 | Layer 1: 'nurse' mentions |  mentions of 'nurse' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) |
| [L2:F10127](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10127) | 11 | Layer 2: 'delivery/deliver' | the word "delivery" or "deliver" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10127) |
| [L2:F15437](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) | 12 | Layer 2: 'delivery/deliver' |  words related to nurses and sound | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 12 | Layer 3: nursing/medical specialties |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L3:F9123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9123) | 11 | Layer 3: nursing/medical specialties |  terms related to business, science, and finance | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9123) |
| [L3:F10198](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) | 11 | Layer 3: nursing/medical specialties |  words related to anesthetics and medical procedures | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) |
| [L3:F14128](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14128) | 13 | Layer 3: nursing/medical specialties | the word "following" and occasionally the word "after" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14128) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 11 | Layer 4: medical env + OB/GYN + degrees |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | Layer 4: medical env + OB/GYN + degrees |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F13857](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13857) | 11 | Layer 4: medical env + OB/GYN + degrees | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13857) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 19 | Layer 4: medical env + OB/GYN + degrees |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 66 | Layer 4: medical env + OB/GYN + degrees |  words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 11 | Layer 5: medical conditions, jobs/education |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 19 | Layer 5: medical conditions, jobs/education | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L5:F12279](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12279) | 12 | Layer 5: medical conditions, jobs/education |  terms relating to jobs and education | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12279) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 19 | Layer 5: medical conditions, jobs/education |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | Layer 6: 'nursing profession' features |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 11 | Layer 6: 'nursing profession' features |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 11 | Layer 6: 'nursing profession' features |  words and abbreviations associated with pediatric gastroenterology and inflammatory bowel disease. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 19 | Layer 6: 'nursing profession' features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 19 | Layer 7: nursing/healthcare + pregnancy/labor |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 12 | Layer 7: nursing/healthcare + pregnancy/labor |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F2861](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2861) | 66 | Layer 7: nursing/healthcare + pregnancy/labor |  words and phrases relating to pregnancy and labor | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2861) |
| [L8:F8185](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8185) | 11 | Layer 8: hospitals/medical specialties |  words related to hospitals, medical specialities, and medical staff | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8185) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 12 | Layer 8: hospitals/medical specialties |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L8:F4607](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) | 12 | Layer 8: hospitals/medical specialties | phrases in job advertisements related to pay | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | Layer 14: medicine/leadership/management | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 12 | Layer 14: medicine/leadership/management | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 19 | Layer 14: medicine/leadership/management | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L16:F6954](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6954) | 12 | Layer 16: 'Professional' | Professional | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6954) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 12 | Layer 18: nurse manager role + healthcare impl |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F14457](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) | 15 | Layer 18: nurse manager role + healthcare impl |  words or phrases related to healthcare implementation, patient care and technology | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) |
| [L19:F11110](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/11110) | 15 | Layer 19: education history + medical jargon |  text describing people's education history | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/11110) |
| [L19:F7484](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/7484) | 15 | Layer 19: education history + medical jargon |  words and jargon used to describe military, medical, and government personnel | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/7484) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 15 | Layer 20: healthcare titles/acronyms after names |  titles and acronyms following names, especially within the healthcare field | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: probe direction (nurse profession) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.106 |
| 3 | `inspect_feature` ×13 | L14:3985, L0:9911, L3:15901, L0:10771, L6:9980, L0:8444, L7:210, L6:15267, L4:4665, L6:4490, L0:7532, L0:6515, L7:3979 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@11` | ❌ error | — | — | Trace the upstream path from L14:F3985 at position 11 ("Labor and Delivery nurse… |
| SA-2 | `L7:F3979@19` | ❌ error | — | — | Trace upstream from L7:F3979 at position 19 (around 'labor and delivery nurse').… |
| SA-3 | `L3:F15901@12` | ❌ error | — | — | Trace upstream from L3:F15901 (nurse/nursing/nurse-management) at position 12. D… |
| SA-4 | `L6:F15267@12` | ❌ error | — | — | Trace upstream from L6:F15267 (nursing profession) at position 12. What input to… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@11, k=15 → L6:F4490 (de=3.00) +14 more |
| 2 | `get_upstream_features` | L6:F15267@12, k=15 → Emb:" nurse"@12 (de=20.50) +14 more |
| 3 | `get_upstream_features` | L7:F3979@19, k=15 → L6:F15267 (de=8.75) +14 more |
| 4 | `get_upstream_features` | L3:F15901@12, k=15 → Emb:" nurse"@12 (de=15.81) +14 more |
| 5 | `get_upstream_features` | L6:F9980@11, k=15 → L4:F4665 (de=2.80) +14 more |
| 6 | `get_upstream_features` | L4:F4665@11, k=12 → L3:F10198 (de=3.44) +11 more |
| 7 | `get_upstream_features` | L6:F4490@11, k=12 → L4:F4665 (de=3.92) +11 more |
| 8 | `get_upstream_features` | L7:F210@12, k=12 → Emb:" nurse"@12 (de=9.19) +11 more |
| 9 | `inspect_feature` ×10 | L3:10198, L4:13803, L3:9123, L5:9749, L2:10127, L2:15437, L6:3475, L8:8185, L1:14469, L4:11037 |
| 10 | `get_top_features` | token="", k=30 → 30 features; top: L14:3985 de=0.106 |
| 11 | `inspect_feature` ×9 | L8:16339, L18:13596, L0:11333, L0:1832, L0:11132, L7:2861, L1:7152, L3:14128, L20:4927 |
| 12 | `get_upstream_features` | L18:F13596@12, k=12 → Emb:" nurse"@12 (de=39.25) +11 more |
| 13 | `get_upstream_features` | L20:F4927@15, k=12 → Emb:" nurse"@12 (de=25.25) +11 more |
| 14 | `inspect_feature` ×5 | L16:6954, L8:4607, L19:11110, L18:14457, L19:7484 |
| 15 | `get_upstream_features` | L7:F3979@12, k=12 → Emb:" nurse"@12 (de=8.88) +11 more |
| 16 | `get_upstream_features` | L6:F15267@19, k=12 → Emb:" Nursing"@19 (de=17.62) +11 more |
| 17 | `inspect_feature` ×15 | L4:8751, L5:10392, L5:12279, L5:1275, L4:7746, L3:8037, L3:6246, L0:8854, L0:15074, L1:8848, L0:11835, L0:5398, L0:5415, L2:12997, L1:5829 |
| 18 | `get_upstream_features` | L14:F3985@19, k=12 → Emb:" Nursing"@19 (de=12.75) +11 more |
| 19 | `get_upstream_features` | L4:F4665@12, k=10 → Emb:" nurse"@12 (de=8.50) +9 more |
| 20 | `get_upstream_features` | L6:F15267@66, k=10 → Emb:" midwife"@66 (de=11.62) +9 more |
| 21 | `get_upstream_features` | L6:F9980@66, k=10 → Emb:" midwife"@66 (de=-5.00) +9 more |
| 22 | `inspect_feature` ×7 | L0:9026, L0:6337, L0:10920, L2:2363, L4:9036, L0:9911, L0:8444 |

### Build

`build_circuit` → 26 nodes, 68 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 114,788 | 10,051 | 916,149 | 0 | $0.1015 | — | — |
| **Total** | | **114,788** | **10,051** | **916,149** | **0** | **$0.1015** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 13s