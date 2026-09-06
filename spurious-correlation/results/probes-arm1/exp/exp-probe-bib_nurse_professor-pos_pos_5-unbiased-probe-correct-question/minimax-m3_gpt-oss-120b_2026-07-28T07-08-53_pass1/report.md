# Circuit Oracle Report
**Date:** 2026-07-28 07:08:53 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe scores a passage about Melissa (a nurse who became a midwife) and the attribution circuit shows the score is driven by a combination of genuine nursing/medical-specialty features and several layout-only or incidental features (date markers, function words), but the strongest positive contributions come from medically-relevant tokens — `Labor`/`Delivery` (medical-environment + OB/GYN + birth) and `nurse`/`Nursing` (nursing-profession features) — so the prediction is *primarily* grounded in the subject's own profession words, with one notable confounder: a pediatric-gastroenterology feature that fires off the word "Labor" and pushes the score up spuriously.

**Confidence:** 7

**Reasoning:**

**Positive (push toward midwife classification):**
- The dominant L14 feature **F3985** ("management/leadership/medicine/studies/research", activation ~16-17) fires on the same positions as the input and is the largest single contributor to the probe (direct_effect 0.106, 0.096, 0.061 at pos 11/12/19). It is *not* a gender feature — its promoted tokens are "patients/Patients/Medical/clinical" and its top activating examples are about "nurse manager", "nursing leadership", etc. (frac_nonzero 0.066).
- F3985 receives strong excitation from a **stack of medical/OB-GYN features** that ultimately trace to two input tokens:
  - **`Labor` (pos 9)** → F9008 (L3 "childbirth/birth") + F10198 (L3 "anesthetics/medical procedures") → F4665 (L4 "medical environments/treatments") + F13803 (L4 "obstetrics/gynecology") + F15022 (L5 "obstetricians/gynecologists") → F9980 (L6 "pediatric gastroenterology") and F4490 (L6 proper-noun medical entities) → F3985 (L14).
  - **`Delivery` (pos 11)** takes the same path with high direct_effect on F9008 (11.2), F10198 (7.6), F13803 (12.2).
  - **`nurse` (pos 12)** → F10920/F8854/F15074 (L0 "nurse") → F15267 (L6 "nursing profession", direct_effect 20.5 from embedding) → F3985 (L14) and F210 (L7 "Asante healthcare/hospital system").
- The user's concern about **gender markers is NOT supported**: I see no She/her/She-became-a-mom path. The pronoun positions do not appear in the top contributors. Instead, the negative-effect feature at L3:F15901 ("mentions of nurses/nursing") actually *suppresses* the probe (direct_effect −0.077 at pos 12), and L6:F15267 at pos 19 also has negative direct_effect — so the explicit "nurse/nursing" profession labels are *anti-predictive* of the midwife class, which is the opposite of a gender artifact. F3979 at pos 19 ("nursing/healthcare") also fires negatively.

**Negative (push away from midwife classification):**
- L3:F15901 "nurse" mentions (direct_effect −0.077 at pos 12) — driven by the "nurse" embedding (15.8) and "register" (L1:F8848).
- L0:F6515 "199X year" (direct_effect −0.060 at pos 27) — fires on "1999", unrelated to profession.
- L0:F10771 "linked" (direct_effect −0.076 at pos 6) — fires on "worked", spurious function-word effect.
- L7:F3979 "nursing/healthcare" (direct_effect −0.058 at pos 19) — driven by "Nursing" (pos 19) embedding.

**Spurious/incidental positives:**
- L6:F9980 "pediatric gastroenterology" (direct_effect 0.073 at pos 11) is unexpected for a midwife bio; it fires because `Labor` is a child-birth/medical-procedure context word and F9980's gating is loose enough to respond. Its presence adds a noisy ~7% nudge unrelated to the actual profession.

**Mechanism summary:** The probe's positive score is built mostly by a **professionally relevant cascade** — medical-environment/OB-GYN/birth features driven by `Labor` and `Delivery` (positions 9 and 11), plus the L14 medical-management feature, plus the Asante-healthcare/hospital-system feature. The `nurse` token (pos 12) *paradoxically suppresses* via the explicit nursing-profession detectors (F15901, F15267 at pos 19, F3979), so the model distinguishes "nurse" (previous career) from the probe's "midwife" target via a *negation* — exactly the right discriminative signal. There is no evidence of spurious gender features; the only spurious effects are (a) F9980's pediatric-GI false-positive, (b) the 1999 year-detector (L0:F6515) and (c) the "linked" feature (L0:F10771) on "worked" — all of which are tangential. The user's hypothesis that the circuit uses gender markers rather than profession indicators is **not supported** — the circuit is dominated by medical/OB-GYN/profession features, with explicit "nurse" mentions being *anti-predictive* of the midwife label.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | L14: Medical/management/leadership (F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 12 | L14: Medical/management/leadership (F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 19 | L14: Medical/management/leadership (F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | L6: Nursing profession detector (F15267) at pos 12 |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 19 | L6: Nursing profession detector (F15267) at pos 19 (NEGATIVE) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 11 | L6: Proper-noun medical entity detector (F4490) |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 11 | L6: Pediatric gastroenterology (F9980) — unexpected activation |  words and abbreviations associated with pediatric gastroenterology and inflammatory bowel disease. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 12 | L7: Asante Healthcare (F210) — generic hospital system |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 19 | L7: Nursing/healthcare word detector (F3979) at pos 19 (NEGATIVE) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 11 | L4: Medical environment vocabulary (F4665) |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 12 | L4: Medical environment vocabulary (F4665) |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | L4: Obstetrics/gynecology terminology (F13803) |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 12 | L4: Counseling/social-work/degree (F11037) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 19 | L4: Counseling/social-work/degree (F11037) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F8751](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8751) | 12 | L4: Glial cells/scientific terms (F8751) — fires on 'staff' |  cell types in the brain, especially glial cells and neurons, and related scientific terminology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8751) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 12 | L3: Nurse/nursing mentions (F15901) (NEGATIVE) |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 19 | L3: Nurse/nursing mentions (F15901) (NEGATIVE) |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 11 | L3: Childbirth/birth (F9008) |  words related to childbirth or birth in general, including in animals. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L3:F10198](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) | 11 | L3: Anesthetics/medical procedures (F10198) |  words related to anesthetics and medical procedures | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) |
| [L5:F15022](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15022) | 11 | L5: Obstetrician/gynecologist mentions (F15022) |  mentions of obstetricians and gynecologists | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15022) |
| [L5:F12279](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12279) | 12 | L5: Jobs/education (F12279) |  terms relating to jobs and education | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12279) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 19 | L5: Healthcare professionals/fields (F1275) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L3:F10868](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) | 8 | L3: 'I'm a / I am a' (F10868) at pos 8 | the phrase "I'm a" or "I am a" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 19 | L2: Academic titles/degrees (F10852) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10070](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10070) | 12 | L2: Verb-centric pattern (F10070) | the verb "went" and other verbs related to movement but sometimes finds legal arguments | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10070) |
| [L1:F8848](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8848) | 12 | L1: 'register' code context (F8848) | the word "register", possibly in a code context | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8848) |
| [L1:F10791](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10791) | 11 | L1: 'delivery' word (F10791) | the word "delivery" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10791) |
| [L1:F12372](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12372) | 19 | L1: US universities/teams (F12372) |  mentions of US universities and sports teams | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12372) |
| [L0:F10920](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) | 12 | L0: 'nurse' / 'nurse+pronouns' (F10920, F8854) |  the word "nurse" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) |
| [L0:F8854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) | 12 | L0: 'nurse' / 'nurse+pronouns' (F10920, F8854) |  the word "nurse" as well as some pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) |
| [L0:F15074](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15074) | 12 | L0: 'nurse' / 'nurse+pronouns' (F10920, F8854) |  words and phrases related to nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15074) |
| [L0:F9911](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9911) | 3 | L0: 'that' word (F9911) |  the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9911) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 2 | L0: 'to' word (F8444) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 5 | L0: Proper nouns (F7532) — fires on 'Melissa' |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F10771](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10771) | 6 | L0: 'linked' word (F10771) — fires on 'worked' (NEGATIVE) | the word "linked" and related words, in technical and scientific contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10771) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 27 | L0: 199X/200X year (F6515) — fires on '1999' (NEGATIVE) |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.106 |
| 3 | `inspect_feature` ×13 | L14:3985, L0:9911, L6:9980, L4:4665, L0:10771, L3:15901, L0:8444, L7:210, L6:15267, L6:4490, L0:7532, L0:6515, L7:3979 |

### Dispatch: 11 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@11` | ✅ reported | 6 | 7 | Trace this feature upstream to see what tokens drive it. This is the L14 'medica… |
| SA-2 | `L6:F15267@12` | ✅ reported | 7 | 11 | Trace upstream from the L6 'nursing profession' feature firing at pos 12. Find w… |
| SA-3 | `L6:F9980@11` | ✅ reported | 5 | 4 | Trace upstream from the L6 'pediatric gastroenterology' feature at pos 11. This … |
| SA-4 | `L7:F210@12` | ✅ reported | 7 | 9 | Trace upstream from the L7 'Asante healthcare' feature at pos 12. Find what toke… |
| SA-5 | `L3:F15901@12` | ✅ reported | 4 | 3 | Trace upstream from L3:15901 (mentions of nurses, nursing) at pos 12. This featu… |
| SA-6 | `L0:F9911@3` | ❌ error | — | — | Trace upstream from L0:9911 'the word that' at pos 3. Find what input tokens dri… |
| SA-7 | `L0:F7532@5` | ❌ error | — | — | Trace upstream from L0:7532 'proper nouns' at pos 5. This fires on the name 'Mel… |
| SA-8 | `L0:F8444@2` | ❌ error | — | — | Trace upstream from L0:8444 'the word to' at pos 2. Find what tokens drive it. |
| SA-9 | `L0:F10771@6` | ❌ error | — | — | Trace upstream from L0:10771 'the word linked' at pos 6. This has NEGATIVE direc… |
| SA-10 | `L0:F6515@27` | ❌ error | — | — | Trace upstream from L0:6515 'the year 199X or 200X' at pos 27. This has NEGATIVE… |
| SA-11 | `L7:F3979@19` | ✅ reported | 8 | 6 | Trace upstream from L7:3979 'nursing and healthcare' at pos 19. NEGATIVE direct_… |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@11, k=10 | L6:F4490 (de=3.00) +9 more |
| 3 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 4 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 5 | `get_upstream_features` | L6:F4490@11, k=10 | L4:F4665 (de=3.92) +9 more |
| 6 | `inspect_feature` | L6, F9980 | " words and abbreviations associated with pediatric gastroenterology an" |
| 7 | `get_upstream_features` | L6:F9980@11, k=10 | L4:F4665 (de=2.80) +9 more |
| 8 | `get_upstream_features` | L4:F4665@11, k=10 | L3:F10198 (de=3.44) +9 more |
| 9 | `inspect_feature` | L3, F10198 | " words related to anesthetics and medical procedures" |
| 10 | `get_upstream_features` | L3:F10198@11, k=10 | Emb:" Delivery"@11 (de=7.59) +9 more |
| 11 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 12 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 13 | `inspect_feature` | L6, F5948 | " words related to scientific publications" |
| 14 | `inspect_feature` | L5, F15022 | " mentions of obstetricians and gynecologists" |

**Findings:** The L14 feature (F3985) that fires on the token 'Delivery' in the phrase 'Labor and Delivery' is driven primarily by a cascade of lower‑layer medical‑environment detectors. The strongest upstream driver is a layer‑6 proper‑noun detector (F4490), which itself receives strong excitation from a layer‑4 medical‑environment feature (F4665). That layer‑4 feature is in turn driven by a layer‑3 procedural…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@12, k=10 | Emb:" nurse"@12 (de=20.50) +9 more |
| 3 | `inspect_feature` | L5, F12279 | " terms relating to jobs and education" |
| 4 | `get_upstream_features` | L5:F12279@12, k=10 | Emb:" nurse"@12 (de=-2.19) +9 more |
| 5 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 6 | `inspect_feature` | L0, F15074 | " words and phrases related to nurses, nursing, and nurse management" |
| 7 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 8 | `get_upstream_features` | L4:F8751@12, k=10 | Emb:" nurse"@12 (de=8.94) +9 more |
| 9 | `inspect_feature` | L3, F10868 | " the phrase "I'm a" or "I am a"" |
| 10 | `get_upstream_features` | L0:F15074@12, k=5 | Emb:" nurse"@12 (de=14.12) +4 more |
| 11 | `inspect_feature` | L2, F5224 | " words related to retail and customer service jobs" |
| 12 | `inspect_feature` | L2, F10070 | " the verb "went" and other verbs related to movement but sometimes fin" |

**Findings:** The L6 nursing‑profession feature (F15267) is overwhelmingly driven by the raw token embedding for " nurse" at position 12 (direct_effect 20.5). Secondary upstream contributors include a mid‑level occupational‑context feature (L5:F12279) and a low‑level lexical nurse detector (L0:F15074). The occupational feature itself receives its strongest positive boost from the embedding " worked" (pos 6) and…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F9980 | " words and abbreviations associated with pediatric gastroenterology an" |
| 2 | `get_upstream_features` | L6:F9980@11, k=10 | L4:F4665 (de=2.80) +9 more |
| 3 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 4 | `get_upstream_features` | L4:F4665@11, k=10 | L3:F10198 (de=3.44) +9 more |
| 5 | `inspect_feature` | L5, F15022 | " mentions of obstetricians and gynecologists" |
| 6 | `inspect_feature` | L4, F13803 | " terms related to obstetrics and gynecology" |
| 7 | `get_upstream_features` | L5:F15022@11, k=10 | L4:F4665 (de=2.56) +9 more |
| 8 | `inspect_feature` | L3, F10198 | " words related to anesthetics and medical procedures" |
| 9 | `get_upstream_features` | L3:F10198@11, k=10 | Emb:" Delivery"@11 (de=7.59) +9 more |
| 10 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |

**Findings:** The surprising activation of the pediatric gastroenterology feature (L6:9980) is driven primarily by the token embedding for "Labor" (a delivery‑related word) and by a cascade of medical‑context features in layers 4‑5 that detect generic hospital terminology and obstetrics/gynecology mentions. These upstream signals reside in the lower third of the model (layers ≤8) and provide the positive direct…

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 2 | `get_upstream_features` | L7:F210@12, k=15 | Emb:" nurse"@12 (de=9.19) +14 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `get_upstream_features` | L6:F15267@12, k=15 | Emb:" nurse"@12 (de=20.50) +14 more |
| 5 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 6 | `inspect_feature` | L5, F12279 | " terms relating to jobs and education" |
| 7 | `get_upstream_features` | L4:F4665@12, k=15 | Emb:" nurse"@12 (de=8.50) +14 more |
| 8 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 9 | `get_upstream_features` | L5:F12279@12, k=15 | Emb:" nurse"@12 (de=-2.19) +14 more |
| 10 | `inspect_feature` | L0, F6337 | "the word "dig" in different contexts." |
| 11 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |

**Findings:** The circuit starts at the L7 Asante‑healthcare feature (F210). Its strongest positive upstream driver is the raw token embedding for "nurse" (direct_effect ~9.2) and the layer‑6 nursing‑profession detector (F15267), which itself is driven overwhelmingly by the same "nurse" embedding (direct_effect ~20.5). The nursing feature also feeds a generic job/education detector (L5 F12279) and a medical‑env…

</details>

<details>
<summary><b>SA-5</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 2 | `get_upstream_features` | L3:F15901@12, k=10 | Emb:" nurse"@12 (de=15.81) +9 more |
| 3 | `inspect_feature` | L1, F8848 | "the word "register", possibly in a code context" |
| 4 | `get_upstream_features` | L1:F8848@12, k=10 | Emb:" nurse"@12 (de=13.25) +9 more |
| 5 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 6 | `get_upstream_features` | L0:F8854@12, k=10 | Emb:" nurse"@12 (de=24.38) +9 more |
| 7 | `inspect_feature` | L2, F5224 | " words related to retail and customer service jobs" |
| 8 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 9 | `inspect_feature` | L0, F10920 | " the word "nurse"" |

**Findings:** The negative influence on the probe originates from the high‑layer feature L3:15901, which encodes mentions of nurses. The dominant upstream driver is the raw token embedding for " nurse" at position 12, providing a large positive direct effect to L3:15901 (and also to a lower‑layer L1 feature). Consequently, when the prompt contains the word "nurse" at this position, L3:15901 becomes strongly act…

</details>

<details>
<summary><b>SA-11</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F3979 | " words related to nursing and healthcare" |
| 2 | `get_upstream_features` | L7:F3979@19, k=10 | L6:F15267 (de=8.75) +9 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `get_upstream_features` | L6:F15267@19, k=10 | Emb:" Nursing"@19 (de=17.62) +9 more |
| 5 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 6 | `inspect_feature` | L6, F3475 | " words related to military titles, professional sports, or the medical" |
| 7 | `get_upstream_features` | L4:F11037@19, k=10 | Emb:" Nursing"@19 (de=10.44) +9 more |
| 8 | `inspect_feature` | L5, F14386 | " words related to professional qualifications or roles in aviation, th" |
| 9 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 10 | `get_upstream_features` | L2:F10852@19, k=5 | Emb:" Nursing"@19 (de=10.81) +4 more |
| 11 | `inspect_feature` | L5, F10392 | " fields of academic study" |

**Findings:** The negative influence on the target token originates from the raw token embedding for "Nursing" (pos 19) which positively excites a mid‑layer nursing‑profession detector (L6:F15267). This detector strongly drives L7:F3979 (nursing/healthcare). Additional positive pathways flow through degree‑title detectors (L2:F10852) and broader health‑service detectors (L4:F11037, L5:F14386, L5:F10392). All pa…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F9911@3, k=5 → Emb:" that"@3 (de=15.62) +4 more |
| 2 | `get_upstream_features` | L0:F7532@5, k=5 → Emb:" Melissa"@5 (de=21.25) +4 more |
| 3 | `get_upstream_features` | L0:F8444@2, k=5 → Emb:" to"@2 (de=39.50) +4 more |
| 4 | `get_upstream_features` | L0:F10771@6, k=5 → Emb:" worked"@6 (de=17.00) +4 more |
| 5 | `get_upstream_features` | L0:F6515@27, k=5 → Emb:"1"@26 (de=29.00) +4 more |
| 6 | `get_upstream_features` | L6:F4490@11, k=5 → L4:F4665 (de=3.92) +4 more |
| 7 | `get_upstream_features` | L4:F4665@11, k=5 → L3:F10198 (de=3.44) +4 more |
| 8 | `inspect_feature` ×12 | L3:10198, L3:9008, L0:15074, L0:8854, L0:10920, L5:12279, L4:8751, L4:11037, L5:15022, L4:13803, L2:10852, L1:12372 |
| 9 | `get_upstream_features` | L7:F3979@19, k=5 → L6:F15267 (de=8.75) +4 more |
| 10 | `get_upstream_features` | L6:F15267@19, k=5 → Emb:" Nursing"@19 (de=17.62) +4 more |
| 11 | `inspect_feature` ×3 | L5:9749, L4:13857, L1:10791 |
| 12 | `get_upstream_features` | L0:F10920@12, k=3 → Emb:" nurse"@12 (de=26.50) +2 more |
| 13 | `get_upstream_features` | L3:F10868@8, k=3 → Emb:" a"@8 (de=18.88) +2 more |
| 14 | `get_upstream_features` | L2:F10852@19, k=3 → Emb:" Nursing"@19 (de=10.81) +2 more |
| 15 | `get_upstream_features` | L1:F8848@12, k=3 → Emb:" nurse"@12 (de=13.25) +2 more |
| 16 | `get_upstream_features` | L1:F12372@19, k=3 → Emb:" Nursing"@19 (de=5.53) +2 more |
| 17 | `get_upstream_features` | L6:F9980@11, k=5 → L4:F4665 (de=2.80) +4 more |
| 18 | `get_upstream_features` | L4:F11037@19, k=3 → Emb:" Nursing"@19 (de=10.44) +2 more |
| 19 | `get_upstream_features` | L2:F10070@12, k=3 → Emb:" nurse"@12 (de=19.75) +2 more |
| 20 | `get_upstream_features` | L3:F15901@12, k=5 → Emb:" nurse"@12 (de=15.81) +4 more |
| 21 | `get_upstream_features` | L4:F8751@12, k=3 → Emb:" nurse"@12 (de=8.94) +2 more |
| 22 | `get_upstream_features` | L5:F12279@12, k=5 → Emb:" nurse"@12 (de=-2.19) +4 more |
| 23 | `inspect_feature` ×2 | L2:15437, L2:5224 |
| 24 | `get_upstream_features` | L3:F10198@11, k=3 → Emb:" Delivery"@11 (de=7.59) +2 more |
| 25 | `get_upstream_features` | L3:F9008@11, k=3 → Emb:" Delivery"@11 (de=11.19) +2 more |
| 26 | `get_upstream_features` | L0:F10219@8, k=3 → Emb:" a"@8 (de=41.00) +2 more |
| 27 | `get_upstream_features` | L4:F4665@12, k=3 → Emb:" nurse"@12 (de=8.50) +2 more |
| 28 | `get_upstream_features` | L5:F15022@11, k=3 → L4:F4665 (de=2.56) +2 more |
| 29 | `get_upstream_features` | L4:F13803@11, k=3 → Emb:" Delivery"@11 (de=12.19) +2 more |
| 30 | `inspect_feature` ×4 | L2:2363, L1:1538, L6:3475, L5:1275 |

### Build

`build_circuit` → 42 nodes, 60 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 86,273 | 11,189 | 613,697 | 0 | $0.0761 | — | — |
| SA-2 | openai/gpt-oss-120b | 144,463 | 9,237 | 7,808 | 0 | $0.0273 | ✅ 7F/11E | Trace upstream from the L6 'nursing profession' feature firi… |
| SA-1 | openai/gpt-oss-120b | 178,208 | 11,203 | 39,744 | 0 | $0.0340 | ✅ 6F/7E | Trace this feature upstream to see what tokens drive it. Thi… |
| SA-3 | openai/gpt-oss-120b | 96,894 | 5,460 | 14,336 | 0 | $0.0180 | ✅ 5F/4E | Trace upstream from the L6 'pediatric gastroenterology' feat… |
| SA-4 | openai/gpt-oss-120b | 132,727 | 10,151 | 20,224 | 0 | $0.0263 | ✅ 7F/9E | Trace upstream from the L7 'Asante healthcare' feature at po… |
| SA-5 | openai/gpt-oss-120b | 97,850 | 7,703 | 13,056 | 0 | $0.0195 | ✅ 4F/3E | Trace upstream from L3:15901 (mentions of nurses, nursing) a… |
| SA-11 | openai/gpt-oss-120b | 122,658 | 10,893 | 24,224 | 0 | $0.0253 | ✅ 8F/6E | Trace upstream from L7:3979 'nursing and healthcare' at pos … |
| **Total** | | **859,073** | **65,836** | **733,089** | **0** | **$0.2266** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 27s