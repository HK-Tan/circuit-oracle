# Circuit Oracle Report
**Date:** 2026-07-28 07:20:43 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifying this text as "nurse" is driven primarily by a *genuine* profession signal: the token `nurse` (pos 12) and `Nursing` (pos 19) feed token-level detectors and mid-layer "nursing profession" features that then excite a late medical-role concept. Only secondarily do proper-noun detectors (firing on "Melissa") and a date detector (firing on "1999") push the probe with smaller, indirect effects — these are generic L0 features, not specifically gendered.

**Confidence:** 7

**Reasoning:** The dominant positive driver is L14:F3985 (medical/management/nurse terminology, frac_nonzero=0.066) with direct_effect ≈ 0.10 at positions 11/12/19. Its top upstream drivers are mid-layer *medical-environment* features (L6:F4490 "hospital/patient", L4:F4665 "medical environments", L6:F9980 "ology"-suffix medical terms, all with frac_nonzero ≤ 0.04 — selective) and these are excited by the embeddings for `Delivery` (pos 11) and `Labor` (pos 9), routing through L3:F10198 (medical procedures, frac_nonzero=0.0075). The `Nursing` token at pos 19 contributes via L6:F15267 (nursing profession, direct_effect=20.5 from the `nurse` embedding) → L7:F3979 → L14:F3985.

The user's concern about *spurious gender markers* is **not supported by this circuit**: the only "Melissa"-related path is the very early L0 proper-noun detector F7532 (frac_nonzero=0.06, generic), which contributes to the probe with a moderate direct_effect (0.0605) *not through a gender-specific feature*. Its top activating examples are diverse proper nouns (Raquel, Doreen, Corinne, etc.) — the suppressed_tokens list (`Manuela, Karla, Kayla, Hayley, Mónica, Valeria, Rhonda, Davide, Maureen, Marlene`) looks gendered, but this is a *generic proper-noun* feature, not a gendered-name feature. The model has no obvious "feminine name → nurse" shortcut in this graph.

The L0 function-word detectors (F9911 "that", F10771 "linked", F8444 "to", F6515 "199X year") pushing negatively on the probe are token-identity features, not gender markers either. The L3:F15901 nursing-context feature pushes *negatively* (direct_effect=-0.077) toward the probe despite its label — this is the feature that suppresses "nurse" tokens, consistent with its suppressed_tokens list. So negative contributions come from generic "nurse token" features that the probe has learned to discount.

The core profession signal (positive contributions) flows: `nurse`/`Nursing`/`Delivery`/`Labor` token embeddings → early token detectors (L0-L1) → mid-layer medical/profession features (L3-L7) → L14 medical-role concept → probe. There is no detectable "Melissa is a female name → nurse" path; the apparent name-signal is just generic proper-noun detection, and the profession signal is carried by the profession words themselves.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 5 | Emb: Melissa (pos 5) |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 31 | Emb: Melissa (pos 31) |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 2 | Emb: Labor (pos 9) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F8854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) | 12 | Emb: nurse (pos 12) |  the word "nurse" as well as some pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) |
| [L1:F14469](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) | 12 | Emb: nurse (pos 12) |  mentions of 'nurse' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 27 | Emb: 1999 date tokens (pos 26-27) |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F9911](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9911) | 3 | Emb: function words (to/that/worked, pos 2/3/6) |  the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9911) |
| [L0:F10771](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10771) | 6 | Emb: function words (to/that/worked, pos 2/3/6) | the word "linked" and related words, in technical and scientific contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10771) |
| [L1:F8848](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8848) | 12 | Token-level 'nurse' detectors (L0-L1) | the word "register", possibly in a code context | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8848) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 12 | Nursing-context detector (L3:F15901) |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 19 | Nursing-context detector (L3:F15901) |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L3:F10198](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) | 11 | Medical procedure tokens (L3:F10198) | words related to anesthetics and medical procedures | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 11 | Medical environment/hospital vocabulary (L4-L6) |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 19 | Medical environment/hospital vocabulary (L4-L6) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 11 | Medical environment/hospital vocabulary (L4-L6) |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 19 | Medical environment/hospital vocabulary (L4-L6) |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 11 | Medical environment/hospital vocabulary (L4-L6) |  words and abbreviations associated with pediatric gastroenterology and inflammatory bowel disease. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | Nursing profession detectors (L6-L7) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 19 | Nursing profession detectors (L6-L7) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 12 | Nursing profession detectors (L6-L7) |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 19 | Nursing profession detectors (L6-L7) |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 19 | Nursing profession detectors (L6-L7) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 19 | Nursing profession detectors (L6-L7) |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | Late medical/professional role concept (L14:F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 12 | Late medical/professional role concept (L14:F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 19 | Late medical/professional role concept (L14:F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |

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
| SA-1 | `L14:F3985@11` | ✅ reported | 5 | 10 | Trace the path upstream from L14:F3985 (medical/management/nurse terms feature) … |
| SA-2 | `L6:F15267@12` | ❌ error | — | — | Trace L6:F15267 (nursing profession feature) at position 12. What input tokens a… |
| SA-3 | `L7:F3979@19` | ✅ reported | 3 | 4 | Trace L7:F3979 (nursing/healthcare, negative direct_effect) at position 19. What… |
| SA-4 | `L0:F7532@5` | ❌ error | — | — | Trace L0:F7532 (proper nouns feature) at position 5. The label suggests proper n… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@11, k=10 | L6:F4490 (de=3.00) +9 more |
| 3 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 4 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 5 | `get_upstream_features` | L6:F4490@11, k=10 | L4:F4665 (de=3.92) +9 more |
| 6 | `inspect_feature` | L6, F9980 | " words and abbreviations associated with pediatric gastroenterology an" |
| 7 | `get_upstream_features` | L4:F4665@11, k=10 | L3:F10198 (de=3.44) +9 more |
| 8 | `inspect_feature` | L3, F10198 | " words related to anesthetics and medical procedures" |
| 9 | `get_upstream_features` | L3:F10198@11, k=10 | Emb:" Delivery"@11 (de=7.59) +9 more |
| 10 | `inspect_feature` | L4, F13857 | " words describing jobs, roles or professional activity" |

**Findings:** The target feature L14:F3985 (medical/management/nurse terms) is driven primarily by lower‑layer medical‑entity detectors (L6:F4490, L4:F4665) and a disease‑specific detector (L6:F9980). These mid‑level features themselves receive strong excitatory input from a very early procedural token detector (L3:F10198) and directly from the input token embeddings "Delivery" (pos 11) and "Labor" (pos 9). All…

</details>

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F3979 | " words related to nursing and healthcare" |
| 2 | `get_upstream_features` | L7:F3979@19, k=10 | L6:F15267 (de=8.75) +9 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `get_upstream_features` | L6:F15267@19, k=10 | Emb:" Nursing"@19 (de=17.62) +9 more |
| 5 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |

**Findings:** Tracing from L7:F3979 (nursing/healthcare detection) shows its strongest positive upstream driver is L6:F15267, a feature that fires on the profession of nursing. The direct effect from L6:F15267 (8.75) dwarfs other contributors. L6:F15267 itself is primarily excited by the raw input embedding for the token " Nursing" (direct_effect 17.63) and to a lesser extent by the embedding for " nurse". A se…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L7:F210@12` | ❌ error | — | — | Trace L7:F210 (Asante Healthcare/hospital system feature) at position 12. Is thi… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F15267@12, k=10 → Emb:" nurse"@12 (de=20.50) +9 more |
| 2 | `get_upstream_features` | L0:F8444@2, k=10 → Emb:" to"@2 (de=39.50) +9 more |
| 3 | `get_upstream_features` | L0:F7532@5, k=10 → Emb:" Melissa"@5 (de=21.25) +9 more |
| 4 | `get_upstream_features` | L0:F6515@27, k=10 → Emb:"1"@26 (de=29.00) +9 more |
| 5 | `get_upstream_features` | L0:F9911@3, k=10 → Emb:" that"@3 (de=15.62) +9 more |
| 6 | `get_upstream_features` | L0:F10771@6, k=10 → Emb:" worked"@6 (de=17.00) +9 more |
| 7 | `inspect_feature` | L4, F11037 → " words related to counseling, therapy, social work, and academic degre" |
| 8 | `get_upstream_features` | L0:F7532@6, k=10 → ❌ Feature (layer=0, feature_idx=7532) not found at pos=6. This |
| 9 | `get_upstream_features` | L14:F3985@19, k=10 → Emb:" Nursing"@19 (de=12.75) +9 more |
| 10 | `inspect_feature` ×2 | L0:7532, L8:16339 |
| 11 | `get_upstream_features` | L0:F7532@31, k=10 → Emb:" Melissa"@31 (de=22.25) +9 more |
| 12 | `get_upstream_features` | L7:F210@12, k=10 → Emb:" nurse"@12 (de=9.19) +9 more |
| 13 | `get_upstream_features` | L3:F15901@12, k=10 → Emb:" nurse"@12 (de=15.81) +9 more |
| 14 | `inspect_feature` ×4 | L0:8854, L1:14469, L0:11835, L1:8848 |

### Build

`build_circuit` → 17 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 90,980 | 5,809 | 200,482 | 0 | $0.0463 | — | — |
| SA-3 | openai/gpt-oss-120b | 36,835 | 2,517 | 2,528 | 0 | $0.0071 | ✅ 3F/4E | Trace L7:F3979 (nursing/healthcare, negative direct_effect) … |
| SA-1 | openai/gpt-oss-120b | 110,471 | 6,787 | 5,184 | 0 | $0.0207 | ✅ 5F/10E | Trace the path upstream from L14:F3985 (medical/management/n… |
| **Total** | | **238,286** | **15,113** | **208,194** | **0** | **$0.0741** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 23s