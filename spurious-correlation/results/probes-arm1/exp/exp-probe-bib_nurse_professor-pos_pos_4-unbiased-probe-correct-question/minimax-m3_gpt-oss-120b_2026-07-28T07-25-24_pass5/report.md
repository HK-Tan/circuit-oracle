# Circuit Oracle Report
**Date:** 2026-07-28 07:25:24 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies this text as "nurse profession" via a circuit rooted in genuine profession-indicating tokens ("Nursing" in "Bachelor of Science in Nursing", "nurse practitioner", "operating room") — not in gender markers like "Lori" or "She/her".

**Confidence:** 8

**Reasoning:** The user's concern (gender-marker bias) is not supported by the circuit. The terminal-node supernode `profession_summary_L14_18` contains the top direct-effect features for the probe: **L14:F3985** ("management, leadership, medicine, studies, research", DE=0.157 at pos 18), **L6:F15267** ("nursing profession words", DE=0.119 at pos 33), **L18:F13596** ("role, skills and leadership of nurse managers", DE=0.054 at pos 18) and **L15:F15159** ("medicine and healthcare", DE=0.053 at pos 18). All of these are semantically *nursing-profession* detectors, and each is firmly anchored to explicit profession tokens, not to pronouns or the subject's name. 

Tracing upstream, L18:F13596 receives its dominant excitation (DE=43) directly from the **Emb: " Nursing" (pos 18)** token, plus positive contributions from L6:F15267 (DE=10.1) and L14:F3985 (DE=6.2) and only weak/mixed contributions from the BOS token. L6:F15267 itself is anchored to Emb " Nursing" (DE=17.4) and L5:F11037 (counseling/social-work/degree-program feature, DE=4.4), and its downstream equivalents fire also on Emb " nurse" (pos 32) and Emb " practitioner" (pos 33). L4:F9036 ("healthcare abbreviations", DE=0.073) traces to Emb " practitioner" (DE=14) and Emb " nurse" (DE=4.9). L4:F4665 (medical-environments) traces to Emb " room" (pos 52) and Emb " operating" (pos 51) — i.e. "operating room". 

The token-anchor features at L0–L2 — **L0:F5038 "graduated"**, **L0:F6270 "University"** at pos 6, and L2:F9995 ("occupations and fields of study") at pos 18 — provide a *profession-biography* frame, but the **Emb: "Lori" (pos 1)** token contributes only a small L0:F2285 ("name followed by a number", DE=5.0) and otherwise is essentially absent from the L6+ circuit; no "she/her"-type feature appears anywhere in the top upstream paths. Negative contributions from L7:F3979 (nursing/healthcare, DE=-0.10) and L3:F15901 (mentions of nurses, DE=-0.07) are *also* nursing-related — they inhibit profession-generalized features rather than reflecting a gender confound. The L8–L10 medical-context supernode (F9619 medical-treatment, F16339 hospital infections, F440 professional biographies, F4607 job-ads) reinforces the same medical/clinical register, all sourced from the same profession-token embeddings.

In short, every strongly-contributing path in the circuit lands on an explicit nursing/medical token ("Nursing", "nurse", "practitioner", "operating", "room", "graduated", "University"); the only path touching the subject's first name is a generic "name" feature that is not in any direct-effect path to the probe's output. The user's hypothesis of gender-marker bias is therefore *not* what the circuit shows.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: Nursing (pos 18) - in "Bachelor of Science in Nursing" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 32 | Emb: nurse (pos 32) - in "nurse practitioner" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 33 | Emb: practitioner (pos 33) - in "nurse practitioner" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 51 | Emb: operating (pos 51) - in "operating room" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 52 | Emb: room (pos 52) - in "operating room" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: graduated (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: University (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Lori (pos 1) - subject name (female-coded) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 2 | Token-level anchors (L0-L2): "graduated", "University", "Lori", "occupation/field" | the word "graduated" or variations of it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 6 | Token-level anchors (L0-L2): "graduated", "University", "Lori", "occupation/field" | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L0:F2285](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2285) | 1 | Token-level anchors (L0-L2): "graduated", "University", "Lori", "occupation/field" |  name followed by a number | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2285) |
| [L2:F9995](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) | 18 | Token-level anchors (L0-L2): "graduated", "University", "Lori", "occupation/field" |  terms related to occupations and fields of study | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) |
| [L0:F10920](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) | 18 | Direct "nurse" word features (L0-L2): explicit nurse/nurse-practitioner detectors |  the word "nurse" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) |
| [L0:F8854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) | 18 | Direct "nurse" word features (L0-L2): explicit nurse/nurse-practitioner detectors |  the word "nurse" as well as some pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) |
| [L1:F14469](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) | 18 | Direct "nurse" word features (L0-L2): explicit nurse/nurse-practitioner detectors |  mentions of 'nurse' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 33 | Direct "nurse" word features (L0-L2): explicit nurse/nurse-practitioner detectors |  words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L1:F15395](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) | 33 | Direct "nurse" word features (L0-L2): explicit nurse/nurse-practitioner detectors |  words and abbreviations related to medical studies and procedures | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) |
| [L2:F15437](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) | 32 | Direct "nurse" word features (L0-L2): explicit nurse/nurse-practitioner detectors |  words related to nurses and sound | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 18 | Medical-context / degree-program features (L4-L7): healthcare+academic-degree context, "operating room" |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 33 | Medical-context / degree-program features (L4-L7): healthcare+academic-degree context, "operating room" |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | Medical-context / degree-program features (L4-L7): healthcare+academic-degree context, "operating room" |  words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 52 | Medical-context / degree-program features (L4-L7): healthcare+academic-degree context, "operating room" |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L3:F11871](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11871) | 52 | Medical-context / degree-program features (L4-L7): healthcare+academic-degree context, "operating room" | words ending in "er" followed by words with the suffix "able". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11871) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | Medical-context / degree-program features (L4-L7): healthcare+academic-degree context, "operating room" | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 18 | Medical-context / degree-program features (L4-L7): healthcare+academic-degree context, "operating room" | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 18 | Medical-context / degree-program features (L4-L7): healthcare+academic-degree context, "operating room" |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 18 | Medical-context / degree-program features (L4-L7): healthcare+academic-degree context, "operating room" |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L0:F5424](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5424) | 51 | Medical-context / degree-program features (L4-L7): healthcare+academic-degree context, "operating room" | the word "operating" and verbs ending in 'ed' or 'ing' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5424) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Core "nursing profession" supernode (L6-L7) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Core "nursing profession" supernode (L6-L7) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 18 | Core "nursing profession" supernode (L6-L7) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 33 | Core "nursing profession" supernode (L6-L7) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 18 | Core "nursing profession" supernode (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F8194](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) | 18 | Core "nursing profession" supernode (L6-L7) | mentions of the word "nurse" or the initials or last names of people | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) |
| [L7:F5829](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5829) | 18 | Core "nursing profession" supernode (L6-L7) | mentions of nursing or higher education degrees. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5829) |
| [L7:F15132](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) | 33 | Core "nursing profession" supernode (L6-L7) |  references to medical practices | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) |
| [L7:F4208](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4208) | 18 | Core "nursing profession" supernode (L6-L7) |  words related to medical or dental procedures, especially in a professional setting | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4208) |
| [L7:F4654](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4654) | 18 | Core "nursing profession" supernode (L6-L7) |  words related to medical supplies and care | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4654) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 18 | Medical-context composition (L8-L10) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L8:F9619](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) | 18 | Medical-context composition (L8-L10) |  words and phrases related to medical treatment | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) |
| [L8:F9619](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) | 33 | Medical-context composition (L8-L10) |  words and phrases related to medical treatment | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) |
| [L8:F440](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/440) | 18 | Medical-context composition (L8-L10) |  text from professional biographies | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/440) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 18 | Medical-context composition (L8-L10) |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L8:F4607](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) | 18 | Medical-context composition (L8-L10) | phrases in job advertisements related to pay | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) |
| [L8:F7457](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7457) | 18 | Medical-context composition (L8-L10) |  words relating to healthcare, medicine, and studies | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7457) |
| [L9:F11754](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/11754) | 18 | Medical-context composition (L8-L10) |  words related to nurses, managers, and/or employees | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/11754) |
| [L10:F1461](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/1461) | 18 | Medical-context composition (L8-L10) |  words and phrases related to medicine, medical research, and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/1461) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 18 | Late-layer profession summary features (L14-L18) - drive the probe | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 33 | Late-layer profession summary features (L14-L18) - drive the probe | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 18 | Late-layer profession summary features (L14-L18) - drive the probe |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L15:F8289](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) | 18 | Late-layer profession summary features (L14-L18) - drive the probe | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 18 | Late-layer profession summary features (L14-L18) - drive the probe |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: Probe classification logit (nurse profession) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.157 |
| 3 | `inspect_feature` ×12 | L14:3985, L6:15267, L7:3979, L0:5038, L4:9036, L3:15901, L8:9619, L0:6270, L4:4665, L7:15132, L18:13596, L15:15159 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@18` | ❌ error | — | — | Trace upstream from L14:F3985 at pos 18 (nurse/medicine-related feature) to unde… |
| SA-2 | `L18:F13596@18` | ❌ error | — | — | Trace upstream from L18:F13596 (nurse manager leadership feature) to understand … |
| SA-3 | `L6:F15267@18` | ❌ error | — | — | Trace upstream from L6:F15267 (nursing profession words feature) to identify the… |
| SA-4 | `L7:F3979@18` | ❌ error | — | — | Trace upstream from L7:F3979 at pos 18 (nursing/healthcare feature with NEGATIVE… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@18, k=12 → Emb:" Nursing"@18 (de=11.56) +11 more |
| 2 | `get_upstream_features` | L6:F15267@18, k=12 → Emb:" Nursing"@18 (de=17.38) +11 more |
| 3 | `get_upstream_features` | L18:F13596@18, k=12 → Emb:" Nursing"@18 (de=43.00) +11 more |
| 4 | `get_upstream_features` | L3:F15901@18, k=10 → Emb:" Nursing"@18 (de=15.19) +9 more |
| 5 | `get_upstream_features` | L0:F5038@2, k=8 → Emb:" graduated"@2 (de=22.25) +7 more |
| 6 | `get_upstream_features` | L0:F6270@6, k=8 → Emb:" University"@6 (de=22.38) +7 more |
| 7 | `get_upstream_features` | L4:F4665@52, k=8 → Emb:" room"@52 (de=10.75) +7 more |
| 8 | `get_upstream_features` | L6:F15267@33, k=8 → Emb:" nurse"@32 (de=5.66) +7 more |
| 9 | `get_upstream_features` | L6:F4490@18, k=8 → Emb:" Nursing"@18 (de=11.56) +7 more |
| 10 | `get_upstream_features` | L7:F210@18, k=6 → Emb:" Nursing"@18 (de=7.88) +5 more |
| 11 | `get_upstream_features` | L8:F16339@18, k=6 → Emb:" Nursing"@18 (de=7.28) +5 more |
| 12 | `get_upstream_features` | L15:F8289@18, k=6 → Emb:" Nursing"@18 (de=6.38) +5 more |
| 13 | `get_upstream_features` | L8:F440@18, k=6 → Emb:" Nursing"@18 (de=9.19) +5 more |
| 14 | `get_upstream_features` | L8:F9619@18, k=6 → L6:F15267 (de=5.78) +5 more |
| 15 | `get_upstream_features` | L4:F9036@33, k=6 → Emb:" practitioner"@33 (de=14.00) +5 more |
| 16 | `get_upstream_features` | L8:F9619@33, k=6 → L6:F15267 (de=5.53) +5 more |
| 17 | `get_upstream_features` | L7:F15132@33, k=6 → Emb:" practitioner"@33 (de=11.12) +5 more |
| 18 | `get_upstream_features` | L3:F11871@52, k=6 → Emb:" operating"@51 (de=24.25) +5 more |
| 19 | `get_upstream_features` | L15:F15159@18, k=6 → Emb:" Nursing"@18 (de=10.81) +5 more |
| 20 | `get_upstream_features` | L0:F2285@1, k=6 → Emb:"Lori"@1 (de=5.03) +5 more |
| 21 | `get_upstream_features` | L1:F14469@18, k=6 → Emb:" Nursing"@18 (de=17.62) +5 more |
| 22 | `inspect_feature` ×10 | L0:2285, L1:14469, L2:9995, L5:10392, L4:11037, L5:1275, L8:4607, L1:1494, L1:1889, L7:4208 |
| 23 | `get_upstream_features` | L7:F3979@33, k=6 → L6:F15267 (de=8.12) +5 more |
| 24 | `get_upstream_features` | L14:F3985@33, k=6 → L4:F9036 (de=6.41) +5 more |
| 25 | `get_upstream_features` | L8:F4607@18, k=6 → Emb:" Nursing"@18 (de=7.47) +5 more |
| 26 | `get_upstream_features` | L15:F8289@18, k=6 → Emb:" Nursing"@18 (de=6.38) +5 more |
| 27 | `inspect_feature` ×6 | L7:4654, L7:8194, L7:5829, L1:15395, L0:10920, L0:8854 |
| 28 | `get_upstream_features` | L7:F3979@18, k=6 → L6:F15267 (de=9.19) +5 more |
| 29 | `get_upstream_features` | L7:F3979@33, k=6 → L6:F15267 (de=8.12) +5 more |
| 30 | `get_upstream_features` | L3:F15901@33, k=6 → ❌ Feature (layer=3, feature_idx=15901) not found at pos=33. Th |
| 31 | `get_upstream_features` | L3:F15901@32, k=6 → Emb:" nurse"@32 (de=16.38) +5 more |
| 32 | `get_upstream_features` | L6:F170@18, k=6 → L5:F10392 (de=10.19) +5 more |
| 33 | `inspect_feature` | L6, F170 → " references to academic fields, especially those in the humanities" |
| 34 | `get_upstream_features` | L0:F2285@1, k=4 → Emb:"Lori"@1 (de=5.03) +3 more |
| 35 | `inspect_feature` ×6 | L0:5424, L4:8751, L10:1461, L9:11754, L8:7457, L2:15437 |
| 36 | `get_upstream_features` | L8:F9619@33, k=6 → L6:F15267 (de=5.53) +5 more |
| 37 | `inspect_feature` ×4 | L8:440, L8:16339, L3:11871, L7:15132 |
| 38 | `get_upstream_features` | L3:F15901@18, k=4 → Emb:" Nursing"@18 (de=15.19) +3 more |
| 39 | `get_upstream_features` | L4:F4665@52, k=4 → Emb:" room"@52 (de=10.75) +3 more |
| 40 | `get_upstream_features` | L1:F15395@33, k=4 → Emb:" nurse"@32 (de=7.75) +3 more |

### Build

`build_circuit` → 15 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 93,151 | 15,411 | 928,114 | 0 | $0.1021 | — | — |
| **Total** | | **93,151** | **15,411** | **928,114** | **0** | **$0.1021** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 39s