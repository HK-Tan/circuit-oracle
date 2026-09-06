# Circuit Oracle Report
**Date:** 2026-07-28 07:03:26 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "nurse" is driven by a coherent, profession-specific circuit rooted in the token " nurses" and the medical phrase "Perioperative" — NOT by gender markers.

**Confidence:** 9

**Reasoning:** The circuit shows that the probe is driven entirely by profession-indicating features, not spurious ones. The signal originates at the token-embedding nodes for " nurses" (pos 15, direct_effect 42 to L18:F13596) and "Perio"/"perative" (pos 13/14, direct_effects 6.25 + 9.69 to L18 and 15.4 to L4:F4665). The " she" embedding (pos 7) contributes only marginally to one L7 feature (L7:F8194, direct_effect 1.87) which is a *combined* nurse/personal-name detector — its activation here is driven primarily by the nursing keyword (L7:F8194 receives direct_effect 5.66 from the nursing profession feature L6:F15267, and 3.83 from the " nurses" embedding, vs. only 1.87 from " she"). The probe score receives the bulk of its positive direct_effect from L18:F13596 (nurse-manager leadership, frac_nonzero=0.005 — highly specific), L18:F14457 (healthcare implementation/patient care, frac=0.026), L19:F5028 (healthcare industry), L20:F4927 (healthcare titles/acronyms, with promoted tokens including "nursing"/"nurse"/"Nursing"), and L14:F3985 (management/leadership in medicine, promoted tokens include "patients"/"Medical"/"clinical"). Every major feature's promoted-token list or top-activating examples explicitly centers on nursing or healthcare — there is no gender-only or pronoun-only feature carrying the prediction. The user's concern about gender markers is not supported: the only "she" contribution is a small secondary input to a name/pronoun detector that is itself dominated by the nursing signal. The mechanism is genuine profession recognition, propagating from the profession-keyword embedding through a layered hierarchy: L2:L4:L6 nursing detectors → L7:L8 healthcare-institution detectors → L14 management/medicine → L18 nurse-manager leadership → L20 healthcare titles → output probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: nurses (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: perative (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: Perio (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: she (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F15437](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) | 15 | L2: Nurse keyword (L2:F15437) |  words related to nurses and sound | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 15 | L3: Nurse mention (L3:F15901) |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 14 | L4: Medical environments/Perioperative (L4:F4665) |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 15 | L4: Health professional/counseling (L4:F11037) | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F8751](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8751) | 15 | L4: Biomedical terminology (L4:F8751) | cell types in the brain, especially glial cells and neurons, and related scientific terminology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8751) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 15 | L5: Healthcare professional (L5:F1275) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | L6: Nursing profession (L6:F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | L6: Nursing profession (L6:F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 15 | L7: Healthcare institution (L7:F210) |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F8194](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) | 15 | L7: Nurse / personal name mention (L7:F8194) | mentions of the word "nurse" or the initials or last names of people | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 15 | L7: Nursing/healthcare (L7:F3979) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 15 | L8: Hospital/medical environment (L8:F16339) |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 15 | L14: Management/leadership in medicine (L14:F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 14 | L14: Management/leadership in medicine (L14:F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L16:F10491](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10491) | 15 | L16: Professions (L16:F10491) | Professions | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10491) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 15 | L18: Nurse manager role/leadership (L18:F13596) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 14 | L18: Nurse manager role/leadership (L18:F13596) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F14457](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) | 15 | L18: Healthcare implementation/patient care (L18:F14457) |  words or phrases related to healthcare implementation, patient care and technology | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) |
| [L18:F14457](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) | 14 | L18: Healthcare implementation/patient care (L18:F14457) |  words or phrases related to healthcare implementation, patient care and technology | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14457) |
| [L19:F5028](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/5028) | 15 | L19: Healthcare industry (L19:F5028) |  words related to the healthcare industry | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/5028) |
| [L19:F5028](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/5028) | 14 | L19: Healthcare industry (L19:F5028) |  words related to the healthcare industry | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/5028) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 14 | L20: Healthcare titles/acronyms (L20:F4927) |  titles and acronyms following names, especially within the healthcare field | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 15 | L20: Healthcare titles/acronyms (L20:F4927) |  titles and acronyms following names, especially within the healthcare field | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.163 |
| 3 | `inspect_feature` ×12 | L14:3985, L6:15267, L4:4665, L18:13596, L3:15901, L7:3979, L8:16339, L7:210, L20:4927, L4:9757, L2:15437, L4:8736 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F13596@15` | ❌ error | — | — | Trace L18:F13596 (nurse manager role/leadership feature) upstream to input token… |
| SA-2 | `L14:F3985@15` | ✅ reported | 4 | 6 | Trace L14:F3985 (management/leadership/medicine terms feature) upstream to input… |
| SA-3 | `L6:F15267@15` | ✅ reported | 6 | 9 | Trace L6:F15267 (nursing profession feature) upstream to embedding/input tokens.… |
| SA-4 | `L18:F13596@15` | ✅ reported | 8 | 13 | Trace L18:F13596 (nurse manager role/leadership feature) upstream to input token… |

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@15, k=10 | Emb:" nurses"@15 (de=10.62) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 5 | `get_upstream_features` | L8:F16339@15, k=10 | Emb:" nurses"@15 (de=4.72) +9 more |
| 6 | `get_upstream_features` | L7:F210@15, k=10 | Emb:" nurses"@15 (de=11.38) +9 more |
| 7 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 8 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |

**Findings:** The target feature L14:F3985 (management/leadership/medicine terms) is primarily driven by the input token "nurses" at position 15. The token excites a nursing‑specific feature in layer 6 (F15267), which in turn strongly activates a healthcare‑institution feature in layer 7 (F210) and a hospital‑environment feature in layer 8 (F16339). These mid‑layer features cascade up to L14:F3985. Because the …

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `get_upstream_features` | L4:F11037@15, k=10 | Emb:" nurses"@15 (de=5.16) +9 more |
| 5 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 6 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 7 | `get_upstream_features` | L4:F8751@15, k=5 | Emb:" nurses"@15 (de=9.81) +4 more |
| 8 | `inspect_feature` | L2, F15437 | " words related to nurses and sound" |
| 9 | `get_upstream_features` | L5:F1275@15, k=10 | Emb:" nurses"@15 (de=1.62) +9 more |
| 10 | `get_upstream_features` | L2:F15437@15, k=10 | Emb:" nurses"@15 (de=19.25) +9 more |
| 11 | `inspect_feature` | L2, F5224 | " words related to retail and customer service jobs" |

**Findings:** The nursing‑profession feature (L6:F15267) is driven primarily by the input token " nurses" at position 15, which supplies a very large positive direct effect (16.1) in the upstream list. Additional token "perative" contributes modestly. Higher‑level health‑care detectors (L4:F11037, L4:F8751, L5:F1275) amplify the signal, each also receiving strong positive influence from the same " nurses" embed…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 2 | `get_upstream_features` | L18:F13596@15, k=10 | Emb:" nurses"@15 (de=42.00) +9 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |
| 5 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 6 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 7 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 8 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 9 | `get_upstream_features` | L4:F11037@15, k=10 | Emb:" nurses"@15 (de=5.16) +9 more |
| 10 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |

**Findings:** The target feature L18:F13596 (nurse‑manager role/leadership) is driven primarily by the input token " nurses" (direct_effect 42) and by a low‑frequency, profession‑specific nursing detector (L6:F15267) which itself is strongly activated by the same token and by other nursing‑related words. Additional upstream signals provide medical, leadership, and hospital‑context cues (layers 14, 8, 7) but the…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F8736@2, k=10 → Emb:" from"@2 (de=6.09) +9 more |
| 2 | `get_upstream_features` | L4:F9757@1, k=10 → Emb:"<bos>"@0 (de=14.00) +9 more |
| 3 | `inspect_feature` | L3, F5273 → "words related to being accepted or correct" |
| 4 | `get_upstream_features` | L14:F3985@15, k=10 → Emb:" nurses"@15 (de=10.62) +9 more |
| 5 | `get_upstream_features` | L20:F4927@14, k=10 → L18:F13596 (de=14.31) +9 more |
| 6 | `get_upstream_features` | L18:F13596@15, k=10 → Emb:" nurses"@15 (de=42.00) +9 more |
| 7 | `get_upstream_features` | L20:F4927@15, k=10 → Emb:" nurses"@15 (de=27.50) +9 more |
| 8 | `inspect_feature` ×4 | L18:14457, L19:5028, L16:10491, L7:8194 |
| 9 | `get_upstream_features` | L4:F4665@14, k=10 → Emb:"perative"@14 (de=15.44) +9 more |
| 10 | `get_upstream_features` | L7:F8194@15, k=10 → Emb:"<bos>"@0 (de=-6.12) +9 more |

### Build

`build_circuit` → 22 nodes, 41 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,107 | 5,913 | 225,010 | 0 | $0.0359 | — | — |
| SA-2 | openai/gpt-oss-120b | 71,143 | 4,456 | 5,088 | 0 | $0.0134 | ✅ 4F/6E | Trace L14:F3985 (management/leadership/medicine terms featur… |
| SA-3 | openai/gpt-oss-120b | 113,975 | 10,527 | 25,536 | 0 | $0.0238 | ✅ 6F/9E | Trace L6:F15267 (nursing profession feature) upstream to emb… |
| SA-4 | openai/gpt-oss-120b | 123,594 | 10,715 | 8,448 | 0 | $0.0251 | ✅ 8F/13E | Trace L18:F13596 (nurse manager role/leadership feature) ups… |
| **Total** | | **359,819** | **31,611** | **264,082** | **0** | **$0.0982** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 34s