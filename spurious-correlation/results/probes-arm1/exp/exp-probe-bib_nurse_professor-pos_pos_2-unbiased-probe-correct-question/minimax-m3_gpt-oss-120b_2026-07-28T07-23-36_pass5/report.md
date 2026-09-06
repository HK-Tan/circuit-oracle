# Circuit Oracle Report
**Date:** 2026-07-28 07:23:36 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for the nursing profession is driven almost entirely by the literal token "Nursing" at position 10 ("Bachelors of Science in Nursing from the Medical University Of South Carolina"), with no detectable contribution from gendered pronouns like "She"/"her".

**Confidence:** 9

**Reasoning:** The attribution graph is dominated by a single, well-localized feature cluster converging on the **" Nursing"** token embedding at pos 10 (Bachelors of **Science in Nursing** from the Medical University Of South Carolina). Walking upstream from the top output-driving features reveals a textbook profession-detection circuit:

- **L18:F13596** ("text about the role, skills and leadership of nurse managers", pos 10, direct_effect=0.052) — its top upstream is the **" Nursing"** embedding (direct_effect=42.75), plus L6:F15267 (nursing profession words) and L14:F3985 (management/leadership/medicine/studies).
- **L14:F3985** (pos 10, direct_effect=0.1875 — the largest single positive contributor) — receives direct_effect=12.125 from the **" Nursing"** embedding, plus positive input from L8:F16339 (hospital/medical), L7:F210 (Hospital/healthcare), L6:F4490 (medical proper nouns/hospitals), and inhibitory input from L7:F3979 and L3:F15901 (other "nurse/nursing/healthcare" detectors that partially overlap and cancel).
- **L6:F15267** at both pos 10 (direct_effect=0.1348) and pos 22 (0.05) — explicitly labeled "words in the document referring to the profession of nursing". Each instance receives the bulk of its direct_effect (~17–21) directly from the **" Nursing"** / **" nursing"** token embeddings.
- **L15:F15159** (medicine & healthcare, 0.068) and **L15:F8289** (clinical medicine, 0.047) — also primarily fed by the **" Nursing"** embedding.
- **L6:F11057** at pos 15 (capitalised/Of, 0.046) and **L4:F16096** (Of, direct_effect=10.4) — the chain "Medical University **Of** South Carolina" is the named-institution detector; these features fire on **" Of"** and **" University"** embeddings (not on gendered content).
- **L0:F5038/F11959/F14478** at pos 2 (graduated, 0.088) and **L0:F6270** at pos 14 (University, 0.072) — fire on the literal **" graduated"** and **" University"** embeddings and contribute to the academic-credential side of the profession signal.

Crucially, **the gendered pronouns "She" (pos 1), "her" (pos 4) do not appear in the upstream of any top-20 output-driving feature**. The only "She"-related upstream edges anywhere in the circuit are tiny noise-level contributions (e.g., L0:F5038 direct_effect=0.373 from "She"; L8:F16339 direct_effect=0.82 from "She") that are dwarfed by the corresponding " Nursing"/" graduated" edges by 1–2 orders of magnitude. No L0/L1/L2 feature activated by "She" or "her" makes it into the top features returned by get_top_features, and the embeddings themselves never feed into the dominant profession features.

The probe is therefore doing the right thing: it classifies the profession from genuine profession indicators — chiefly the explicit "Nursing" token and supporting medical/healthcare/clinical/hospital/institution lexicon — not from gendered markers. The user's concern that the circuit uses spurious gender features is **not supported**: the circuit is anchored to profession/medical vocabulary and to the academic-credential phrase "graduated … University Of …".

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 10 | L18: Nurse manager role & leadership (F13596, pos 10) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 10 | L14: management/leadership/medicine/studies (F3985, pos 10) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 10 | L15: medicine & healthcare (F15159, pos 10) |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L15:F8289](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) | 10 | L15: clinical medicine terms (F8289, pos 10) |  words and phrases related to clinical medicine, including the terms clinicians use and related scientific fields | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 10 | L8: hospital infections/bacteria (F16339, pos 10) |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 10 | L7: Asante healthcare/Hospital terms (F210, pos 10) |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 10 | L6: proper nouns/medical roles/hospitals (F4490, pos 10) |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L7:F4654](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4654) | 10 | L7: medical supplies/care (F4654, pos 10) |  words related to medical supplies and care | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4654) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | L6: nursing profession words (F15267, pos 10) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 22 | L6: nursing profession words at pos 22 (F15267, pos 22) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L8:F9619](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) | 10 | L8: medical treatment (F9619, pos 10) |  words and phrases related to medical treatment | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) |
| [L8:F440](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/440) | 10 | L8: professional biography text (F440, pos 10) |  text from professional biographies | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/440) |
| [L8:F4607](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) | 10 | L8: shift/pay in job ads (F4607, pos 10) | phrases in job advertisements related to pay | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 10 | L7: nursing & healthcare (F3979, pos 10) — INHIBITORY |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 10 | L3: nurse/nursing/management mentions (F15901, pos 10) — INHIBITORY |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L10:F1461](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/1461) | 10 | L10: medical research/healthcare (F1461, pos 10) — INHIBITORY (broad) |  words and phrases related to medicine, medical research, and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/1461) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 10 | L4: counseling/social work/degree (F11037, pos 10) |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | L5: fields of academic study (F10392, pos 10) |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L1:F14469](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) | 10 | L1: 'nurse' mentions (F14469, pos 10) |  mentions of 'nurse' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) |
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 2 | L0: 'graduated' (F5038, pos 2) | the word "graduated" or variations of it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L2:F14478](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14478) | 2 | L2: 'graduate/graduated' (F14478, pos 2) |  the word graduate | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14478) |
| [L0:F11959](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) | 2 | L0: 'graduated' & 'More' (F11959, pos 2) |  the word "graduated" and the word "more." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 14 | L0: 'University' (F6270, pos 14) | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L0:F16075](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) | 15 | L0: 'of' (F16075, pos 15) | the word "of" and court names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) |
| [L6:F11057](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11057) | 15 | L6: capitalised/Of/heading words (F11057, pos 15) |  capitalized words, especially in titles and headings, and ordinal words like "first" | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11057) |
| [L4:F16096](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/16096) | 15 | L4: 'Of' in titles (F16096, pos 15) | instances of the word "of" preceded by particular words and abbreviations | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/16096) |
| [L0:F11988](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11988) | 17 | L0: 'North/South Carolina' (F11988, pos 17) |  mentions of North Carolina, sometimes in conjunction with "University" or "study" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11988) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.188 |
| 3 | `inspect_feature` ×18 | L14:3985, L6:15267, L7:3979, L3:15901, L0:5038, L0:6270, L15:15159, L6:4490, L8:16339, L7:210, L0:11959, L0:16075, L18:13596, L7:4654, L15:8289, L6:11057, L2:14478, L0:11988 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@10` | ❌ error | — | — | Trace L14:F3985 (terms related to management, leadership, medicine, studies, and… |
| SA-2 | `L6:F15267@10` | ❌ error | — | — | Trace L6:F15267 (words referring to nursing profession, pos 10, direct_effect=0.… |
| SA-3 | `L18:F13596@10` | ❌ error | — | — | Trace L18:F13596 (text about the role, skills, and leadership of nurse managers,… |
| SA-4 | `L7:F3979@10` | ❌ error | — | — | Trace L7:F3979 (words related to nursing and healthcare, pos 10, direct_effect=-… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@10, k=15 → Emb:" Nursing"@10 (de=12.12) +14 more |
| 2 | `get_upstream_features` | L6:F15267@10, k=15 → Emb:" Nursing"@10 (de=17.38) +14 more |
| 3 | `get_upstream_features` | L18:F13596@10, k=15 → Emb:" Nursing"@10 (de=42.75) +14 more |
| 4 | `get_upstream_features` | L7:F3979@10, k=15 → L6:F15267 (de=8.75) +14 more |
| 5 | `get_upstream_features` | L7:F3979@22, k=15 → L6:F15267 (de=8.81) +14 more |
| 6 | `get_upstream_features` | L6:F15267@22, k=15 → Emb:" nursing"@22 (de=21.00) +14 more |
| 7 | `get_upstream_features` | L0:F5038@2, k=10 → Emb:" graduated"@2 (de=22.25) +9 more |
| 8 | `get_upstream_features` | L0:F6270@14, k=10 → Emb:" University"@14 (de=22.12) +9 more |
| 9 | `get_upstream_features` | L0:F16075@15, k=10 → Emb:" Of"@15 (de=26.50) +9 more |
| 10 | `get_upstream_features` | L0:F11988@17, k=10 → Emb:" Carolina"@17 (de=12.94) +9 more |
| 11 | `get_upstream_features` | L6:F4490@10, k=10 → Emb:" Nursing"@10 (de=11.62) +9 more |
| 12 | `get_upstream_features` | L8:F16339@10, k=10 → Emb:" Nursing"@10 (de=7.66) +9 more |
| 13 | `get_upstream_features` | L7:F210@10, k=10 → Emb:" Nursing"@10 (de=8.19) +9 more |
| 14 | `get_upstream_features` | L7:F4654@10, k=10 → Emb:" Nursing"@10 (de=7.22) +9 more |
| 15 | `get_upstream_features` | L4:F11037@10, k=10 → Emb:" Nursing"@10 (de=10.62) +9 more |
| 16 | `get_upstream_features` | L15:F15159@10, k=10 → Emb:" Nursing"@10 (de=10.56) +9 more |
| 17 | `get_upstream_features` | L15:F8289@10, k=10 → Emb:" Nursing"@10 (de=6.25) +9 more |
| 18 | `get_upstream_features` | L2:F14478@2, k=10 → Emb:" graduated"@2 (de=19.75) +9 more |
| 19 | `get_upstream_features` | L0:F11959@2, k=10 → Emb:" graduated"@2 (de=20.75) +9 more |
| 20 | `get_upstream_features` | L6:F11057@15, k=10 → L4:F16096 (de=10.38) +9 more |
| 21 | `get_upstream_features` | L3:F15901@10, k=10 → Emb:" Nursing"@10 (de=15.12) +9 more |
| 22 | `get_upstream_features` | L8:F9619@10, k=10 → Emb:" Nursing"@10 (de=5.84) +9 more |
| 23 | `get_upstream_features` | L8:F440@10, k=10 → Emb:" Nursing"@10 (de=9.44) +9 more |
| 24 | `get_upstream_features` | L8:F7457@10, k=10 → Emb:" Nursing"@10 (de=3.23) +9 more |
| 25 | `get_upstream_features` | L8:F4607@10, k=10 → Emb:" Nursing"@10 (de=7.78) +9 more |
| 26 | `inspect_feature` ×8 | L10:1461, L4:11037, L8:9619, L8:440, L8:4607, L1:14469, L5:10392, L4:16096 |
| 27 | `get_upstream_features` | L0:F10@1, k=10 → ❌ Feature (layer=0, pos=1, feature_idx=10) not found in graph' |
| 28 | `get_upstream_features` | L0:F10@4, k=10 → ❌ Feature (layer=0, pos=4, feature_idx=10) not found in graph' |
| 29 | `get_upstream_features` | L6:F11057@15, k=10 → L4:F16096 (de=10.38) +9 more |

### Build

`build_circuit` → 41 nodes, 46 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 70,948 | 9,140 | 349,035 | 0 | $0.0532 | — | — |
| **Total** | | **70,948** | **9,140** | **349,035** | **0** | **$0.0532** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 55s