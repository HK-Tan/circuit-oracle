# Circuit Oracle Report
**Date:** 2026-07-28 07:22:38 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit was saved successfully (the embedding nodes are already included). Let me now provide the analysis.

**Analysis:** The probe's classification of "nurse" is driven primarily by **profession-specific lexical-semantic features** (nurse word detectors, nursing profession, obstetrics/gynecology, labor-and-delivery vocabulary) — NOT by spurious gender markers.

**Confidence:** 8

**Reasoning:** The circuit traces from the output probe through two convergent late-layer features into the embedding tokens of this text:

**Path 1 — The dominant positive pathway** flows from the input tokens **` nurse` (pos 7)**, **` practitioner` (pos 8)**, and **` delivery` (pos 46)** through a hierarchy of medical-semantic features. At L0, the dedicated word detector **F8854** (label: "the word 'nurse'…", max token "▁nurse") activates directly on ` nurse`. This feeds L6:F15267 ("words in the document referring to the profession of nursing", frac_nonzero=0.016, max_token "▁RN"/"▁nurse") at pos 7, which in turn drives L14:F3985 (frac_nonzero=0.066, promoted tokens "▁patients", "Medical", "▁clinicians", "▁clinical") at pos 7/8/11/46 — the largest late-layer contributor to the probe (direct_effect 0.0889 at pos 8). L15:F15159 ("medicine and healthcare", promoted "▁healthcare", "▁patients", "▁medical") is the second-strongest late-layer feature. Crucially, the upstream L4 features **F13803** ("terms related to obstetrics and gynecology", max_token "▁stet"/"▁uri", promoted "▁pregnancy", "▁postpartum") and **F4665** ("medical environments, treatments, personnel, facilities", promoted "▁hospital") are activated directly by the **` labor` (pos 44)** and **` delivery` (pos 46)** embeddings via L3:F9008 ("childbirth/birth", max_token "▁thing"/"▁world", promoted "▁birth") and L1:F7152 ("the word 'delivery'"). These are genuine domain indicators for the nursing sub-specialty of labor-and-delivery — exactly the profession being classified.

**Path 2 — The negative/suppressing pathway** is what addresses the user's concern. The female-gender feature **L0:F15382** ("mentions of a female person", max_token "▁Her", promoted "▁her", "▁she", frac_nonzero=0.009) fires on **`She` (pos 1)** and is *included* in the graph (direct_effect −0.0381 at pos 1), but importantly it has **negative direct_effect** and **no positive edges into the L14:L15 output features** — its only downstream effects are mildly negative (slightly inhibiting `late_medical_leadership`). The L7 nursing/healthcare suppressor (F3979, also negative direct_effect) plays a similar dampening role. Gender is therefore not a positive driver of the probe; if anything it slightly reduces the score. The probe's positive signal flows almost entirely through the *lexical content* (nurse/practitioner/labor/delivery) and the *medical-semantic composition* those words build.

**Conclusion:** The user's concern is **not supported by this circuit**. The probe is not relying on the female pronoun "She" as a spurious shortcut. It is genuinely reading the profession markers "nurse practitioner", "labor", and "delivery" and the implied obstetrics/medical-infrastructure vocabulary. The female-gender feature is present in the top-20 list but functions as a weak *suppressor* (negative direct_effect) rather than a positive driver of the classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' nurse' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: ' practitioner' (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 44 | Emb: ' labor' (pos 44) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: ' delivery' (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: ' Medicine' (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'She' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F8854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) | 7 | L0: 'nurse' word detector (F8854) |  the word "nurse" as well as some pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) |
| [L0:F1832](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) | 44 | L0: 'labor' word detector (F1832) | the word "labor" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | L0: female-person mention detector (F15382) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L1:F7152](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7152) | 46 | L1: 'delivery' word detector (F7152) | the word "delivery" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7152) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 8 | L1: medical practice/studies (F1494) |  words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 46 | L3: childbirth/birth (F9008) |  words related to childbirth or birth in general, including in animals. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L3:F10198](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) | 46 | L3: anesthetics/medical procedures (F10198) |  words related to anesthetics and medical procedures | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 46 | L4: obstetrics & gynecology (F13803) |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 46 | L4: medical environments/personnel (F4665) |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 8 | L4: healthcare/practitioner (F9036) |  words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 8 | L4: counseling/social work (F11037) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F12178](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12178) | 30 | L4: career/years-time phrases (F12178) |  phrases that include words expressing a length of time | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12178) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 8 | L5: healthcare professionals (F1275) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 8 | L5: medical conditions/procedures (F9749) [POS] |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 46 | L5: medical conditions/procedures (F9749) [POS] |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 46 | L6: pediatric gastro / IBD (F9980) |  words and abbreviations associated with pediatric gastroenterology and inflammatory bowel disease. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 7 | L6: nursing profession words (F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | L6: nursing profession words (F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L7:F15132](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) | 8 | L7: references to medical practices (F15132) |  references to medical practices | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 8 | L7: nursing & healthcare (F3979) [NEG] |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 7 | L14: management/leadership/medicine/research (F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 8 | L14: management/leadership/medicine/research (F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | L14: management/leadership/medicine/research (F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 46 | L14: management/leadership/medicine/research (F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 7 | L15: medicine and healthcare (F15159) |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: probe classification score | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.089 |
| 3 | `inspect_feature` ×8 | L14:3985, L6:15267, L4:4665, L15:15159, L7:3979, L5:9749, L6:9980, L4:9757 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@8` | ❌ error | — | — | Trace the path from L14:F3985 at pos 8 ("nurse") upstream to find which input to… |
| SA-2 | `L6:F15267@8` | ❌ error | — | — | Trace the path from L6:F15267 at pos 8 upstream. This feature is "words in docum… |
| SA-3 | `L4:F4665@46` | ❌ error | — | — | Trace the path from L4:F4665 at pos 46 upstream. This feature detects "words rel… |
| SA-4 | `L15:F15159@7` | ❌ error | — | — | Trace the path from L15:F15159 at pos 7 upstream. This is "medicine and healthca… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@8, k=15 → Emb:" practitioner"@8 (de=6.19) +14 more |
| 2 | `get_upstream_features` | L6:F15267@8, k=15 → Emb:" nurse"@7 (de=7.06) +14 more |
| 3 | `get_upstream_features` | L4:F4665@46, k=15 → Emb:" labor"@44 (de=3.45) +14 more |
| 4 | `get_upstream_features` | L4:F4665@46, k=10 → Emb:" labor"@44 (de=3.45) +9 more |
| 5 | `get_upstream_features` | L5:F9749@8, k=15 → Emb:" nurse"@7 (de=5.88) +14 more |
| 6 | `get_upstream_features` | L4:F9757@1, k=15 → Emb:"<bos>"@0 (de=15.94) +14 more |
| 7 | `inspect_feature` ×10 | L4:9036, L5:1275, L3:9008, L3:10198, L1:1494, L0:1832, L4:12178, L0:3175, L0:15382, L0:8854 |
| 8 | `get_upstream_features` | L5:F1275@8, k=15 → Emb:" nurse"@7 (de=2.30) +14 more |
| 9 | `get_upstream_features` | L4:F9036@8, k=10 → Emb:" practitioner"@8 (de=14.69) +9 more |
| 10 | `get_upstream_features` | L3:F9008@46, k=10 → Emb:" delivery"@46 (de=14.25) +9 more |
| 11 | `get_upstream_features` | L15:F15159@7, k=15 → Emb:" nurse"@7 (de=17.50) +14 more |
| 12 | `get_upstream_features` | L6:F9980@46, k=15 → L4:F4665 (de=2.77) +14 more |
| 13 | `get_upstream_features` | L15:F15159@7, k=10 → Emb:" nurse"@7 (de=17.50) +9 more |
| 14 | `get_upstream_features` | L6:F9980@46, k=10 → L4:F4665 (de=2.77) +9 more |
| 15 | `get_upstream_features` | L4:F4665@46, k=10 → Emb:" labor"@44 (de=3.45) +9 more |
| 16 | `get_upstream_features` | L5:F9749@46, k=10 → L4:F4665 (de=2.92) +9 more |
| 17 | `inspect_feature` ×9 | L4:13803, L4:11037, L1:7152, L1:12174, L3:9123, L8:16339, L7:15132, L6:4490, L7:210 |
| 18 | `get_upstream_features` | L5:F9749@8, k=10 → Emb:" nurse"@7 (de=5.88) +9 more |
| 19 | `get_upstream_features` | L6:F9980@46, k=10 → L4:F4665 (de=2.77) +9 more |
| 20 | `get_upstream_features` | L4:F12178@30, k=10 → Emb:" spent"@26 (de=10.12) +9 more |
| 21 | `get_upstream_features` | L1:F7152@46, k=10 → Emb:" delivery"@46 (de=17.00) +9 more |
| 22 | `get_upstream_features` | L4:F13803@46, k=10 → Emb:" delivery"@46 (de=13.81) +9 more |

### Build

`build_circuit` → 27 nodes, 40 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 79,364 | 12,475 | 353,912 | 0 | $0.0600 | — | — |
| **Total** | | **79,364** | **12,475** | **353,912** | **0** | **$0.0600** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 5s