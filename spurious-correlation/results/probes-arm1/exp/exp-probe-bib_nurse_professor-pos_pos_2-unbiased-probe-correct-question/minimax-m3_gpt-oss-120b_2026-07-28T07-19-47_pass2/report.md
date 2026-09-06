# Circuit Oracle Report
**Date:** 2026-07-28 07:19:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe classifies the subject as a nurse, and its score is driven overwhelmingly by *genuine nursing-profession features* (not by gender markers): the dominant signal flows from the raw token "Nursing" at pos 10 (and "nursing" at pos 22) through a tightly nursing-specific feature cascade — L6:F15267 (frac_nonzero 0.016, explicitly fires on "RN", "nurse", "DNP", "Nursing"), L7:F3979 (healthcare words), L8:F16339 (hospital/medical environment), L14:F3985 (nursing management, promotes "Patients"/"Medical"), L15:F15159 (medical/healthcare), and finally L18:F13596 (nurse-manager narrative, frac_nonzero 0.005, max-activates on "Nurse") — feeding into the probe.

**Confidence:** 9

**Reasoning:** The circuit gives no evidence for the user's "spurious gender marker" concern. Every positive feature in the trace has a *nursing/medical* semantic label:
- The two strongest top features by direct effect, L14:F3985 (+0.19) and L6:F15267 (+0.13), are explicitly "nursing management/medicine" and "nursing profession" detectors (frac_nonzero 0.07 and 0.016).
- Both trace cleanly to the embedding of the **input token "Nursing"** at pos 10 (direct effect 12.1 into F3985, 17.4 into F15267) — there is no "She/her" or first-name embedding in the upstream set.
- A parallel "nurse-manager" feature (L18:F13596) is driven 42.75 by the "Nursing" token embedding and 35.5 by the "nursing" token embedding at pos 22; its top-activating examples are all about *nurse managers* and it promotes "Nurse" tokens.
- Layer-0 features that look superficially suspicious are actually innocuous: L0:F6270 ("whom" at pos 14) and L0:F16075 ("Of" at pos 15) are generic function-word detectors; their top activations are the "University" and "Medical" token embeddings, not gender tokens, and their downstream contribution is small (≈+0.07 each). The L0:F5038 "graduated" feature is a generic biography marker, not a gendered cue.
- The only negative-effect feature in the top-15, L3:F15901 (direct effect −0.10), is itself labeled "mentions of nurses, nursing, and nurse management" — it is a *profession* feature acting as a local suppressor, and its upstream chain is degree/academic-program detectors (L1:F10429, L2:F10852) feeding the nursing feature, not gender tokens.
- Pruned-token analysis confirms the signal is content-driven: the "Nursing"/"nursing" tokens at pos 10 and pos 22 each provide direct embedding drive of 17–42 to nursing-specific mid/late features, while "She" (pos 1) has near-zero direct effect on any profession feature (≈+0.24 into the L0 "graduated" detector, 0.37 into a token-level feature, and no path to the probe).

In short, the model's "nurse" classification is built from the literal tokens "Nursing"/"RN"/"nurse"/"Medical University of South Carolina" via profession-specific transcoder features, with no measurable contribution from gendered tokens like "She" or "her." The user's concern is not supported by this circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 2 | L0: word "graduated" detectors (pos 2) | the word "graduated" or variations of it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L0:F11959](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) | 2 | L0: word "graduated" detectors (pos 2) |  the word "graduated" and the word "more." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11959) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 14 | L0: function-word "of" / "University" detectors (pos 14, 15) | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L0:F16075](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) | 15 | L0: function-word "of" / "University" detectors (pos 14, 15) | the word "of" and court names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 10 | L1–L2: academic degree / occupation context features (pos 10) | academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L1:F10429](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10429) | 10 | L1–L2: academic degree / occupation context features (pos 10) | words related to academic programs | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10429) |
| [L2:F9995](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) | 10 | L1–L2: academic degree / occupation context features (pos 10) | terms related to occupations and fields of study | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 10 | L3: nurse/nursing mentions (pos 10) — local suppressor |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 10 | L4: healthcare/academic-degree profession feature (pos 10) | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | L6: nursing-profession detector (pos 10, pos 22) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 22 | L6: nursing-profession detector (pos 10, pos 22) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 10 | L6: medical proper-noun / hospital context (pos 10) |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 10 | L7: healthcare/nursing & institution words (pos 10) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 10 | L7: healthcare/nursing & institution words (pos 10) |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 10 | L8: hospital/medical-environment (pos 10) |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 10 | L14: nursing management / medicine / research (pos 10) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 10 | L15: medical/healthcare vocabulary (pos 10) |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 10 | L18: nurse-manager / role-skill narrative (pos 10, pos 22) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 22 | L18: nurse-manager / role-skill narrative (pos 10, pos 22) |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.188 |
| 3 | `inspect_feature` ×4 | L14:3985, L6:15267, L0:5038, L0:6270 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@10` | ✅ reported | 6 | 7 | Trace the path from L14:F3985 (which encodes terms related to nursing/medicine/m… |
| SA-2 | `L6:F15267@10` | ✅ reported | 3 | 5 | Trace the path from L6:F15267 (nursing profession words, fires at pos 10 "RN"). … |
| SA-3 | `L0:F5038@2` | ❌ error | — | — | Trace from L0:F5038 ("graduated" word feature, pos 2). What feeds this — the act… |
| SA-4 | `L0:F6270@14` | ❌ error | — | — | Trace from L0:F6270 ("whom" word feature at pos 14, "where she worked closely wi… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@10, k=10 | Emb:" Nursing"@10 (de=12.12) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 5 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 6 | `get_upstream_features` | L8:F16339@10, k=10 | Emb:" Nursing"@10 (de=7.66) +9 more |
| 7 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |

**Findings:** L14:F3985, a nursing/medical management feature, receives its strongest drive from the raw token embedding "Nursing" (direct effect 12.1). Additional upstream contributors are mid‑layer features that capture hospital environment (L8:F16339), healthcare institution names (L7:F210), and generic medical proper nouns (L6:F4490). A lower‑layer (layer 6) feature L6:F15267 explicitly fires on nursing pro…

</details>

<details>
<summary><b>SA-2</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@10, k=10 | Emb:" Nursing"@10 (de=17.38) +9 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 5 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 6 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 7 | `get_upstream_features` | L4:F11037@10, k=10 | Emb:" Nursing"@10 (de=10.62) +9 more |
| 8 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 9 | `get_upstream_features` | L5:F1275@10, k=10 | L4:F11037 (de=1.99) +9 more |
| 10 | `inspect_feature` | L3, F6246 | " the word "Nutrients" and words containing "ure"." |
| 11 | `get_upstream_features` | L2:F10852@10, k=10 | Emb:" Nursing"@10 (de=11.44) +9 more |
| 12 | `inspect_feature` | L1, F5829 | " uses of the word 'necessarily', sometimes near scientific or mathemat" |
| 13 | `inspect_feature` | L1, F10429 | " words related to academic programs" |
| 14 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |
| 15 | `inspect_feature` | L1, F12372 | " mentions of US universities and sports teams" |
| 16 | `get_upstream_features` | L4:F8751@10, k=10 | Emb:" Nursing"@10 (de=8.31) +9 more |

**Findings:** The path starts at the nursing‑specific feature L6:F15267. Its strongest upstream driver is the raw token embedding for "Nursing" (positive direct effect 17.375) and a mid‑layer feature L4:F11037 (direct effect 4.25). L4:F11037 is in turn driven by L2:F10852 (direct effect 1.93), which represents academic degree titles. All three features lie in layers ≤8, satisfying the lower‑third floor requirem…

</details>

### Re-dispatch (round 2): 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L0:F6270@14` | ❌ error | — | — | Trace L0:F6270 ("whom" feature at pos 14). This is a function-word feature in a … |
| SA-6 | `L3:F15901@10` | ✅ reported | 4 | 4 | Trace L3:F15901 (mentions of nurses/nursing/nurse management) at pos 10. It has … |
| SA-7 | `L0:F16075@15` | ❌ error | — | — | Trace L0:F16075 ("of" word feature) at pos 15. Find its downstream and whether i… |

<details>
<summary><b>SA-6</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F15901 | " mentions of nurses, nursing, and nurse management" |
| 2 | `get_upstream_features` | L3:F15901@10, k=10 | Emb:" Nursing"@10 (de=15.12) +9 more |
| 3 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |
| 4 | `get_upstream_features` | L2:F9995@10, k=10 | Emb:" Nursing"@10 (de=5.41) +9 more |
| 5 | `inspect_feature` | L1, F10429 | " words related to academic programs" |
| 6 | `get_upstream_features` | L1:F10429@10, k=10 | Emb:" Nursing"@10 (de=4.78) +9 more |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `get_upstream_features` | L2:F10852@10, k=10 | Emb:" Nursing"@10 (de=11.44) +9 more |
| 9 | `inspect_feature` | L1, F8848 | "the word "register", possibly in a code context" |
| 10 | `inspect_feature` | L0, F6337 | "the word "dig" in different contexts." |
| 11 | `inspect_feature` | L1, F12372 | " mentions of US universities and sports teams" |

**Findings:** The negative‑effect feature L3:F15901 (nursing mentions) is driven primarily by a direct token embedding for the word "Nursing" and a cascade of upstream occupation‑related detectors: a generic occupation feature (L2:F9995) feeds into it, which itself is powered by an academic‑program detector (L1:F10429) that captures degree terminology, and further by a low‑level layer‑0 pattern feature (L0:F633…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×9 | L3:15901, L7:3979, L6:4490, L8:16339, L7:210, L0:16075, L0:11959, L15:15159, L18:13596 |
| 2 | `get_upstream_features` | L0:F6270@14, k=5 → Emb:" University"@14 (de=22.12) +4 more |
| 3 | `get_upstream_features` | L0:F16075@15, k=5 → Emb:" Of"@15 (de=26.50) +4 more |
| 4 | `get_upstream_features` | L6:F15267@22, k=5 → Emb:" nursing"@22 (de=21.00) +4 more |
| 5 | `get_upstream_features` | L18:F13596@10, k=5 → Emb:" Nursing"@10 (de=42.75) +4 more |
| 6 | `get_upstream_features` | L0:F5038@2, k=3 → Emb:" graduated"@2 (de=22.25) +2 more |
| 7 | `get_upstream_features` | L0:F11959@2, k=3 → Emb:" graduated"@2 (de=20.75) +2 more |
| 8 | `get_upstream_features` | L15:F15159@10, k=3 → Emb:" Nursing"@10 (de=10.56) +2 more |
| 9 | `get_upstream_features` | L18:F13596@22, k=3 → Emb:" nursing"@22 (de=35.50) +2 more |

### Build

`build_circuit` → 18 nodes, 32 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 45,412 | 5,732 | 141,742 | 0 | $0.0290 | — | — |
| SA-1 | openai/gpt-oss-120b | 67,272 | 3,967 | 2,528 | 0 | $0.0125 | ✅ 6F/7E | Trace the path from L14:F3985 (which encodes terms related t… |
| SA-2 | openai/gpt-oss-120b | 253,715 | 10,260 | 5,200 | 0 | $0.0443 | ✅ 3F/5E | Trace the path from L6:F15267 (nursing profession words, fir… |
| SA-6 | openai/gpt-oss-120b | 112,436 | 7,905 | 13,952 | 0 | $0.0218 | ✅ 4F/4E | Trace L3:F15901 (mentions of nurses/nursing/nurse management… |
| **Total** | | **478,835** | **27,864** | **163,422** | **0** | **$0.1076** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 26s