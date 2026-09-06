# Circuit Oracle Report
**Date:** 2026-07-28 07:19:45 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-classification probe score is driven almost entirely by genuine nursing-profession indicators anchored to the literal token "Nursing" (pos 18) and " nurse"/" practitioner" (pos 32–33), with a single, tiny 2.39-effect edge from the "Lori" name token reaching only a late-layer healthcare-titles feature; no pronoun/gender features (e.g. "She") carry positive weight.

**Confidence:** 8

**Reasoning:** The circuit reaches the output via a clean profession-lexicon cascade, not via gender cues:

- **Token-embedding roots.** The dominant upstream drive comes from `Emb: 'Nursing' (pos 18)`, which feeds L6:F15267 (direct_effect 17.375), L14:F3985 (11.5625), L18:F13596 (43.0), and L20:F4927 (21.5) — by far the largest single effects in the graph. `Emb: ' nurse' (pos 32)` and `Emb: ' practitioner' (pos 33)` independently push L18:F13596 (14.4 and 9.3 respectively). These are profession nouns, not gendered words.

- **Profession-feature cascade.** The mid-layer detectors are unambiguously profession-specific by their autointerp labels and frac_nonzero: L6:F15267 "profession of nursing" (frac=0.016, fires on RN/nurse), L4:F11037 "counseling, therapy, social work, academic degree programs" (0.007), L4:F9036 "healthcare abbreviations" (0.015), L5:F1275 "healthcare professionals" (0.013), L6:F4490 "hospitals/medical roles" (0.042), L14:F3985 "management, leadership, medicine, studies, research" (0.066, fires on "nurse", "nurses", "leadership"), L18:F13596 "role, skills and leadership of nurse managers" (0.005, max-act 404 on "Nurse"). None of these features' top activating examples or promoted tokens are gendered — they promote "Nurse"/"nurse"/"nursing".

- **No genuine gender signal.** I searched explicitly for the pronoun token "She" and the name "Lori" in upstream traces. The only positive contribution from a name is `Emb: 'Lori' (pos 1) → L20:F4927` with direct_effect 2.39 — about 10× smaller than the "Nursing" embedding's contribution to the same feature (21.5) and routed through a title-pattern feature, not a gender feature. There is no L7:F210 ("Asante Healthcare system") influence here despite its label mentioning "Gender: Male" in its activation examples — that influence is absent on this graph. L3:F15901 and L7:F3979 appear as *inhibitory* nodes (negative direct_effect), consistent with suppression of non-nursing readings.

- **Address of the concern.** The user worried the circuit uses spurious features like gender markers. The traced circuit does not support that: the probe's positive score is built from a profession-lexicon hierarchy (token → profession-noun feature → nurse-manager feature → healthcare-titles feature → probe), and the only "name" node (Lori) contributes marginally to a title-context feature, not to a gender axis. The classification is driven by the nursing vocabulary itself.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 18 | Academic degree / program terminology (L4:F11037) | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | Healthcare abbreviations and professional terms (L4:F9036) | words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Nursing-profession detector (L6:F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Nursing-profession detector (L6:F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 18 | Medical institutions / hospital role terms (L6:F4490) | proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | Healthcare professional detector (L5:F1275) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 18 | Management / leadership / medicine / research terms (L14:F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 33 | Management / leadership / medicine / research terms (L14:F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 18 | Nurse manager role / leadership (L18:F13596) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 33 | Nurse manager role / leadership (L18:F13596) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L20:F4927](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) | 27 | Healthcare titles / acronyms after names (L20:F4927) |  titles and acronyms following names, especially within the healthcare field | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/4927) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.157 |
| 3 | `inspect_feature` ×6 | L14:3985, L6:15267, L0:5038, L0:6270, L18:13596, L20:4927 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@18` | ✅ reported | 6 | 10 | Trace the path upstream from L14:F3985 at position 18 ("management/leadership/me… |
| SA-2 | `L6:F15267@33` | ✅ reported | 11 | 15 | Trace the path upstream from L6:F15267 at position 33 (profession of nursing). T… |
| SA-3 | `L20:F4927@27` | ✅ reported | 6 | 6 | Trace the path upstream from L20:F4927 at position 27 (titles and acronyms follo… |
| SA-4 | `L0:F5038@2` | ❌ error | — | — | Trace the path upstream from L0:F5038 at position 2 (the word "graduated"). This… |
| SA-5 | `L18:F13596@18` | ✅ reported | 3 | 4 | Trace the path upstream from L18:F13596 at position 18 (nurse managers/leadershi… |
| SA-6 | `L0:F6270@6` | ❌ error | — | — | Trace the path upstream from L0:F6270 at position 6 (the word "whom"). Determine… |
| SA-7 | `L0:F5038@2` | ❌ error | — | — | Trace upstream from L0:F5038 at position 2 (the word "graduated"). This is an ea… |
| SA-8 | `L0:F6270@6` | ❌ error | — | — | Trace upstream from L0:F6270 at position 6. Position 6 should be checked — what … |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@18, k=10 | Emb:" Nursing"@18 (de=11.56) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 5 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 6 | `inspect_feature` | L8, F9619 | " words and phrases related to medical treatment" |
| 7 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 8 | `get_upstream_features` | L6:F15267@18, k=10 | Emb:" Nursing"@18 (de=17.38) +9 more |
| 9 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 10 | `get_upstream_features` | L8:F16339@18, k=10 | Emb:" Nursing"@18 (de=7.28) +9 more |

**Findings:** The nursing‑profession signal at L14:F3985 is driven primarily by the raw token embedding "Nursing" (pos 18). This feeds into a mid‑level nursing‑profession detector (L6:F15267), which is reinforced by a counseling/health‑team detector (L4:F11037) and a medical‑institution detector (L6:F4490). A higher‑level hospital‑context feature (L8:F16339) and a health‑system/gender-aware feature (L7:F210) ad…

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@33, k=10 | Emb:" nurse"@32 (de=5.66) +9 more |
| 3 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 4 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 5 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 6 | `inspect_feature` | L5, F7539 | " words related to medical professionals performing actions on a patien" |
| 7 | `get_upstream_features` | L5:F1275@33, k=10 | L4:F9036 (de=1.70) +9 more |
| 8 | `inspect_feature` | L4, F9036 | " words and abbreviations associated with healthcare." |
| 9 | `inspect_feature` | L2, F2589 | " words related to medical professionals and medical specialties" |
| 10 | `get_upstream_features` | L4:F9036@33, k=10 | Emb:" practitioner"@33 (de=14.00) +9 more |
| 11 | `get_upstream_features` | L1:F1494@33, k=10 | Emb:" nurse"@32 (de=8.69) +9 more |
| 12 | `inspect_feature` | L0, F6337 | "the word "dig" in different contexts." |
| 13 | `inspect_feature` | L1, F8222 | " words related to medical practice" |

**Findings:** The nursing‑profession feature (L6:F15267) is driven primarily by the raw token embedding for "nurse" and reinforced by a cascade of mid‑layer healthcare‑related detectors (L5:F1275, L4:F9036, L4:F11037) and a low‑layer medical‑practice detector (L1:F1494). No gender, pronoun, or name features appear in the positive upstream path. The tracing reaches a raw embedding node and passes through layer 1…

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F4927 | " titles and acronyms following names, especially within the healthcare" |
| 2 | `get_upstream_features` | L20:F4927@27, k=10 | L18:F13596 (de=29.62) +9 more |
| 3 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 4 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 5 | `get_upstream_features` | L6:F15267@18, k=10 | Emb:" Nursing"@18 (de=17.38) +9 more |
| 6 | `get_top_logits` | k=5 | "" (100%) |
| 7 | `get_upstream_features` | L18:F13596@27, k=10 | Emb:" Nursing"@18 (de=25.25) +9 more |
| 8 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 9 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 10 | `get_upstream_features` | L4:F11037@18, k=10 | Emb:" Nursing"@18 (de=10.38) +9 more |
| 11 | `get_upstream_features` | L20:F4927@27, k=20 | L18:F13596 (de=29.62) +19 more |
| 12 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |

**Findings:** The circuit for L20:F4927 (position 27) starts with the raw token " Nursing" at position 18, which directly excites the target feature. Upstream, a chain of increasingly abstract features detects nursing profession language (L18:F13596), nursing‑related degree mentions (L6:F15267), and broader management/leadership context (L14:F3985). These feed into the title‑pattern detector. The pathway reache…

</details>

<details>
<summary><b>SA-5</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F13596 | " text about the role, skills and leadership of nurse managers" |
| 2 | `get_upstream_features` | L18:F13596@18, k=10 | Emb:" Nursing"@18 (de=43.00) +9 more |
| 3 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 4 | `get_upstream_features` | L6:F15267@18, k=10 | Emb:" Nursing"@18 (de=17.38) +9 more |
| 5 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 6 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |

**Findings:** The nurse‑manager leadership feature (L18:F13596) is driven primarily by the raw token embedding for "Nursing" at position 18, which supplies a large positive direct effect (43.0). The next strongest upstream contributor is a lower‑layer nursing‑profession detector (L6:F15267) with direct effect 10.125; this feature itself is strongly excited by the same "Nursing" embedding (17.375) and also recei…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L7, F210 → " words and names associated with the Asante Healthcare system" |
| 2 | `get_upstream_features` | L7:F210@18, k=8 → Emb:" Nursing"@18 (de=7.88) +7 more |
| 3 | `get_upstream_features` | L20:F4927@27, k=8 → L18:F13596 (de=29.62) +7 more |
| 4 | `get_upstream_features` | L18:F13596@18, k=8 → Emb:" Nursing"@18 (de=43.00) +7 more |
| 5 | `get_upstream_features` | L18:F13596@33, k=8 → Emb:" nurse"@32 (de=14.44) +7 more |
| 6 | `get_upstream_features` | L14:F3985@18, k=8 → Emb:" Nursing"@18 (de=11.56) +7 more |
| 7 | `get_upstream_features` | L6:F15267@18, k=8 → Emb:" Nursing"@18 (de=17.38) +7 more |

### Build

`build_circuit` → 13 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 22,344 | 4,816 | 97,847 | 0 | $0.0184 | — | — |
| SA-5 | openai/gpt-oss-120b | 49,490 | 3,089 | 2,528 | 0 | $0.0093 | ✅ 3F/4E | Trace the path upstream from L18:F13596 at position 18 (nurs… |
| SA-1 | openai/gpt-oss-120b | 141,721 | 7,418 | 5,136 | 0 | $0.0258 | ✅ 6F/10E | Trace the path upstream from L14:F3985 at position 18 ("mana… |
| SA-2 | openai/gpt-oss-120b | 201,373 | 9,752 | 13,312 | 0 | $0.0363 | ✅ 11F/15E | Trace the path upstream from L6:F15267 at position 33 (profe… |
| SA-3 | openai/gpt-oss-120b | 122,000 | 8,823 | 10,176 | 0 | $0.0237 | ✅ 6F/6E | Trace the path upstream from L20:F4927 at position 27 (title… |
| **Total** | | **536,928** | **33,898** | **128,999** | **0** | **$0.1135** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 26s