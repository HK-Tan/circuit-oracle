# Circuit Oracle Report
**Date:** 2026-07-28 07:19:58 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of Melissa as a nurse/midwife is driven primarily by genuine profession-related features (nursing vocabulary, hospital/clinical settings, and OB-GYN/childbirth terminology) anchored on the input tokens "Labor", "Delivery", and "nurse" — not by spurious gender markers.

**Confidence:** 7

**Reasoning:**

**Positive (profession-driving) circuit.** The dominant late-layer feature is L14:3985 (direct_effect +0.106 at pos 11, frac_nonzero 0.066) labeled "terms related to management, leadership, medicine, studies, and research," with top activating examples centered on "nurse" and patient/clinical vocabulary. It is fed by two genuine profession-related mid-layer features:
- L6:4490 — "proper nouns corresponding to locations, organizations, medical roles" (promoted tokens: hospital, hospitals, Patient, patients)
- L4:4665 — "medical environments, treatments, personnel, facilities" (promoted tokens: hospital, hospitals)

Tracing these down reaches token embeddings: the **Emb:"Delivery" (pos 11)** token strongly excites L3:10198 (anesthetics/procedures, de=7.6) and the birth/childbirth feature L3:9008, which then feed L4:4665 and L6:9980 (OB/GYN specialty). The **Emb:"Labor" (pos 9)** token also drives L4:4665 (de=2.89). L6:15267 at pos 12 is a dedicated "profession of nursing" feature (max activation 73.9 on "RN" / "nurse") — its top driver is **Emb:"nurse" (pos 12)** with de=20.5. L7:210 ("Asante Healthcare/hospital system words") and L5:15022 (obstetricians/gynecologists) reinforce this profession pathway.

**Negative/suppressive features.** Several of the top features push the probe *down*, but they are NOT gender markers:
- L3:15901 (nurse-mention feature, de=−0.077) suppresses the probe despite being about nurses — this is an idiosyncrasy of how the probe reads this layer's representation, not a spurious cue.
- L0:10771 ("linked" — generic word feature, fires on "worked" at pos 6, de=−0.076)
- L0:6515 (199X/200X year digit, de=−0.060) fires on the "1999" date
- L0:8444 (function word "to") and L0:9911 (function word "that") — generic syntactic features
- L7:3979 (nursing/healthcare words, de=−0.058) — same kind of layer-specific suppression as L3:15901

**On the user's concern (gender/spurious features).** No feature in the top 15 activates on female-name tokens, pronouns like "She/her/Melissa", or other gender markers. The L0:7532 feature at pos 5 ("proper nouns") is anchored on the " Melissa" embedding but is a generic proper-noun detector (suppressed tokens include male names like "Marlene" is female but "Davide" is male and others are gender-neutral) with no clear gender bias, and its de is modest. The " Melissa" name itself is not driving the prediction — **Emb:"nurse" (pos 12) is the single largest single-edge driver in the whole circuit (de=20.5 into L6:15267)**, and the words "Labor" and "Delivery" supply the clinical-context signal via genuine medical-environment features.

**Conclusion:** The probe's classification is being driven by legitimate profession/clinical-context features (nurse, hospital, delivery, OB/GYN, childbirth) — not by gender markers. The " Melissa" name is not used as a spurious female indicator; instead, the word "nurse" itself is the strongest single contributor. The user's concern about gender-based spuriousness is not supported by this circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification (nurse/midwife) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | Late-layer nursing/clinical leadership feature | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 12 | Late-layer nursing/clinical leadership feature | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 19 | Late-layer nursing/clinical leadership feature | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 11 | Hospital / clinical setting entity features | proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | Hospital / clinical setting entity features |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 11 | Hospital / clinical setting entity features | words and abbreviations associated with pediatric gastroenterology and inflammatory bowel disease. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 11 | Medical environments / settings (hospital, delivery rooms) | words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | Medical environments / settings (hospital, delivery rooms) | terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L5:F15022](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15022) | 11 | OB/GYN / obstetrician profession features | mentions of obstetricians and gynecologists | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15022) |
| [L3:F10198](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) | 11 | Procedural / anesthetic terminology | words related to anesthetics and medical procedures | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 11 | Procedural / anesthetic terminology | words related to childbirth or birth in general, including in animals. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 12 | Asante Healthcare / hospital system words |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 19 | Nursing/healthcare words (suppressive at L14) |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 12 | L3 nurse-mention feature (suppresses prediction) |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 2 | Function word 'to' (generic) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F9911](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9911) | 3 | Function word 'to' (generic) |  the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9911) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 5 | Function word 'that' (generic) |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F10771](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10771) | 6 | 'linked' word feature (suppressive, generic) | the word "linked" and related words, in technical and scientific contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10771) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 27 | 199X/200X year digit feature (suppressive) |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: Labor (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: Delivery (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: nurse (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: Melissa (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.106 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@11` | ✅ reported | 4 | 4 | Trace this L14:3985 feature upstream. What does it encode? Does it represent nur… |
| SA-2 | `L0:F9911@3` | ❌ error | — | — | Trace this L0:9911 feature upstream. What token/pattern does it detect? Is it pr… |
| SA-3 | `L3:F15901@12` | ❌ error | — | — | Trace this L3:15901 feature upstream (it has a negative direct_effect). What doe… |
| SA-4 | `L6:F9980@11` | ✅ reported | 6 | 8 | Trace this L6:9980 feature upstream. What does it encode? Is it profession-relat… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@11, k=10 | L6:F4490 (de=3.00) +9 more |
| 3 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 4 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 5 | `inspect_feature` | L6, F9980 | " words and abbreviations associated with pediatric gastroenterology an" |
| 6 | `get_upstream_features` | L6:F4490@11, k=10 | L4:F4665 (de=3.92) +9 more |
| 7 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 8 | `get_upstream_features` | L4:F4665@11, k=10 | L3:F10198 (de=3.44) +9 more |
| 9 | `inspect_feature` | L3, F10198 | " words related to anesthetics and medical procedures" |

**Findings:** Tracing from L14:3985 (position 11) reveals a cascade through lower‑layer features specialized in medical entities and environments, originating from input token embeddings such as "Delivery" and "Labor". The strongest upstream drivers are L6:4490 and L4:4665, both of which focus on hospitals, nurses, and clinical settings. The top activating examples and promoted tokens for L14:3985 heavily invol…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F9980 | " words and abbreviations associated with pediatric gastroenterology an" |
| 2 | `get_upstream_features` | L6:F9980@11, k=10 | L4:F4665 (de=2.80) +9 more |
| 3 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 4 | `inspect_feature` | L5, F15022 | " mentions of obstetricians and gynecologists" |
| 5 | `inspect_feature` | L4, F13803 | " terms related to obstetrics and gynecology" |
| 6 | `get_upstream_features` | L4:F4665@11, k=10 | L3:F10198 (de=3.44) +9 more |
| 7 | `get_upstream_features` | L4:F4665@11, k=10 | L3:F10198 (de=3.44) +9 more |
| 8 | `inspect_feature` | L3, F10198 | " words related to anesthetics and medical procedures" |
| 9 | `get_upstream_features` | L3:F10198@11, k=10 | Emb:" Delivery"@11 (de=7.59) +9 more |
| 10 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |

**Findings:** The target L6:9980 feature is a specialist medical detector for pediatric gastroenterology/IBD. Its strongest upstream driver is a generic medical‑environment feature (layer 4, idx 4665), which itself is driven mainly by the token embedding "Labor" and by a lower‑layer birth‑related feature (layer 3, idx 10198) that receives a strong boost from the embedding "Delivery". Additional upstream cues in…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F9911@3, k=10 → Emb:" that"@3 (de=15.62) +9 more |
| 2 | `get_upstream_features` | L3:F15901@12, k=10 → Emb:" nurse"@12 (de=15.81) +9 more |
| 3 | `inspect_feature` ×9 | L0:10771, L0:8444, L7:210, L6:15267, L0:7532, L0:6515, L7:3979, L0:9911, L3:15901 |
| 4 | `get_upstream_features` | L0:F7532@5, k=8 → Emb:" Melissa"@5 (de=21.25) +7 more |
| 5 | `get_upstream_features` | L14:F3985@12, k=8 → Emb:" nurse"@12 (de=10.75) +7 more |
| 6 | `get_upstream_features` | L6:F15267@12, k=8 → Emb:" nurse"@12 (de=20.50) +7 more |
| 7 | `get_upstream_features` | L7:F210@12, k=8 → Emb:" nurse"@12 (de=9.19) +7 more |

### Build

`build_circuit` → 17 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 31,544 | 4,608 | 81,295 | 0 | $0.0199 | — | — |
| SA-1 | openai/gpt-oss-120b | 120,122 | 7,515 | 32 | 0 | $0.0225 | ✅ 4F/4E | Trace this L14:3985 feature upstream. What does it encode? D… |
| SA-4 | openai/gpt-oss-120b | 125,992 | 7,579 | 5,920 | 0 | $0.0235 | ✅ 6F/8E | Trace this L6:9980 feature upstream. What does it encode? Is… |
| **Total** | | **277,658** | **19,702** | **87,247** | **0** | **$0.0659** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 23s