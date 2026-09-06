# Circuit Oracle Report
**Date:** 2026-07-28 07:08:34 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for the "nurse" profession is driven overwhelmingly by genuine, profession-specific lexical and semantic evidence (the tokens *nurse* and *practitioner* propagating through dedicated nursing/healthcare features at layers 4–15), with the suppressed context feature (L5:F9749) and the L7 nursing-suppressor simply being generic medical-context filters rather than gender markers.

**Confidence:** 7

**Reasoning:**

The user's concern is that the circuit might rely on spurious gender cues (She/her/Linda) rather than real profession indicators. The circuit does **not** support that concern. The dominant positive drivers at the probe logit are:

1. **L14:F3985 (direct_effect ≈ +0.21 across pos 7/8/11)** — labeled "management, leadership, medicine, studies, research" with top activating tokens *nurse*, *nurses*, *nurse manager*. It receives strong excitation from the `nurse` and `practitioner` embeddings (via L4:F9036 "healthcare abbreviations" direct_effect ≈ +6.1) and from the dedicated **L6:F15267 "nursing profession" detector** (direct_effect ≈ +2.0, frac_nonzero 0.016, a low/specific feature whose top examples are RN, nurse, nurse manager). This is genuine profession signal.
2. **L15:F15159 "medicine & healthcare words" (direct_effect ≈ +0.05)** — directly excited by the `nurse` token embedding (direct_effect 17.5, the single largest one-hop effect in the graph) and by the L0:F8854 feature literally labeled "the word 'nurse' as well as some pronouns" (frac_nonzero 0.005 — extremely selective). Again genuine profession signal.

Gender tokens play only a **negligible** role. The `She` embedding (pos 1) contributes direct_effects of only 2.16 to L4:F9757 (an "acronyms/symbols" feature, not a profession feature), 0.95 to L6:F4490 (proper-noun/medical-roles, which is *also* driven by the `nurse` token at 13.06), 0.49 to L5:F1275 (healthcare professionals, where `nurse` contributes 2.30 and `practitioner` 1.75), and 0.71 to L6:F9980 (a pediatric-GI feature driven by `labor` at 2.47). In every case the profession tokens dominate the gender token by 3–20×.

The inhibitory features L5:F9749 (medical-conditions, direct_effect −0.088) and L7:F3979 (nursing/healthcare, direct_effect −0.049) are **content-suppressors, not gender-suppressors**: L5:F9749 is excited by the `delivery`/`labor` token cascade (L1:F7152 → L3:F9008 "childbirth/birth" → L4:F13803 "obstetrics & gynecology"), and L7:F3979 is a near-duplicate of the nursing detector (same top-activating tokens, including the very `Debbie Gregory DNP, RN` example). These push *against* the nurse classification, likely because the *specificity* of the text (mentioning a real named individual with subspecialty detail) is off-distribution for a generic nurse profile. They are profession/context suppressors, not gender proxies.

The signal flow is: **`nurse`/`practitioner` embeddings → L0:F8854 + L1:F1494 nurse-detectors → L4:F9036 healthcare-abbrev + L6:F15267 nursing-detector → L14:F3985 leadership-medicine + L15:F15159 medicine-healthcare → probe logit**. All major positive edges originate from the profession tokens; gender and proper-name tokens contribute only minor secondary effects. The user's concern about gender-based spurious correlation is not borne out by this circuit — the probe appears to be using legitimate nursing-profession lexical evidence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' nurse' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: ' practitioner' (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 44 | Emb: ' labor' (pos 44) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: ' delivery' (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'She' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F8854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) | 7 | Early-layer 'nurse' detector (L0:F8854) + L1:F1494 medical-practice |  the word "nurse" as well as some pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 8 | Early-layer 'nurse' detector (L0:F8854) + L1:F1494 medical-practice | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L1:F7152](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7152) | 46 | 'delivery' word detector (L1:F7152) | the word "delivery" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7152) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 46 | Childbirth / birth feature (L3:F9008) |  words related to childbirth or birth in general, including in animals. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L0:F1832](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) | 44 | 'labor' token feature (L0:F1832) | the word "labor" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 46 | Obstetrics/gynecology feature (L4:F13803) |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 46 | Medical environments/personnel/facilities (L4:F4665) |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 8 | Medical environments/personnel/facilities (L4:F4665) |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 8 | Healthcare abbreviations/practitioners (L4:F9036) | words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 46 | Pediatric GI/IBD (L6:F9980) — context-specific medical |  words and abbreviations associated with pediatric gastroenterology and inflammatory bowel disease. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 46 | Medical conditions/procedures (L5:F9749) — SUPPRESSOR |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 8 | Medical conditions/procedures (L5:F9749) — SUPPRESSOR |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 8 | Healthcare professionals/fields (L5:F1275) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Nursing profession detector (L6:F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 7 | Nursing profession detector (L6:F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 7 | Proper nouns / medical roles (L6:F4490) |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 8 | Nursing & healthcare feature (L7:F3979) — SUPPRESSOR |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F15132](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) | 8 | Medical practices (L7:F15132) | references to medical practices | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 7 | Asante Healthcare system (L7:F210) |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L8:F9619](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) | 8 | Medical treatment (L8:F9619) | words and phrases related to medical treatment | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 7 | Management/leadership/medicine/research (L14:F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 8 | Management/leadership/medicine/research (L14:F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | Management/leadership/medicine/research (L14:F3985) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 7 | Medicine & healthcare words (L15:F15159) |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.089 |
| 3 | `inspect_feature` ×4 | L14:3985, L6:15267, L4:4665, L15:15159 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@8` | ✅ reported | 6 | 7 | Trace upstream from L14:F3985 (terms related to management, leadership, medicine… |
| SA-2 | `L6:F15267@8` | ✅ reported | 4 | 12 | Trace upstream from L6:F15267 (words in document referring to nursing profession… |
| SA-3 | `L15:F15159@7` | ✅ reported | 4 | 7 | Trace upstream from L15:F15159 (medical/healthcare words). Find what input token… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@8, k=10 | Emb:" practitioner"@8 (de=6.19) +9 more |
| 3 | `inspect_feature` | L4, F9036 | " words and abbreviations associated with healthcare." |
| 4 | `inspect_feature` | L7, F15132 | " references to medical practices" |
| 5 | `inspect_feature` | L8, F9619 | " words and phrases related to medical treatment" |
| 6 | `get_upstream_features` | L4:F9036@8, k=10 | Emb:" practitioner"@8 (de=14.69) +9 more |
| 7 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 8 | `get_upstream_features` | L1:F1494@8, k=10 | Emb:" nurse"@7 (de=10.75) +9 more |

**Findings:** The upstream circuit for L14:F3985 originates from low‑level input tokens that denote professions, especially "practitioner" and "nurse". These embeddings excite an early‑layer feature (L1:F1494) that passes the signal to a healthcare‑term detector (L4:F9036). L4:F9036 aggregates broader medical vocabulary and forwards a strong excitatory signal to the target. Additional contributions come from a …

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@8, k=10 | Emb:" nurse"@7 (de=7.06) +9 more |
| 3 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 4 | `get_upstream_features` | L5:F1275@8, k=10 | Emb:" nurse"@7 (de=2.30) +9 more |
| 5 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 6 | `get_upstream_features` | L4:F11037@8, k=10 | Emb:" practitioner"@8 (de=7.03) +9 more |
| 7 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 8 | `get_upstream_features` | L1:F1494@8, k=10 | Emb:" nurse"@7 (de=10.75) +9 more |

**Findings:** Tracing upstream from L6:F15267 reveals that its strongest excitatory drivers are the input token embeddings "nurse" (pos 7) and "practitioner" (pos 8). The path also passes through higher‑level medical‑profession detectors (L5:F1275, L4:F11037, L1:F1494). A gendered token "She" does appear upstream of F1275 but contributes only a minor positive effect (0.49) and is not a primary driver. All requi…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F15159 | " words related to medicine and healthcare" |
| 2 | `get_upstream_features` | L15:F15159@7, k=10 | Emb:" nurse"@7 (de=17.50) +9 more |
| 3 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 4 | `get_upstream_features` | L6:F4490@7, k=10 | Emb:" nurse"@7 (de=13.06) +9 more |
| 5 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 6 | `inspect_feature` | L0, F8854 | " the word "nurse" as well as some pronouns" |
| 7 | `get_upstream_features` | L0:F8854@7, k=5 | Emb:" nurse"@7 (de=24.38) +4 more |

**Findings:** The medical/healthcare feature (L15:F15159) is driven primarily by the input token 'nurse' (positive direct_effect 17.5). This signal propagates through a low‑layer detector for the word nurse (L0:F8854) and a proper‑noun detector that also picks up medical role tokens (L6:F4490). A gender pronoun token 'She' provides a small additional excitation to L6:F4490, indicating a modest gender‑marker inf…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L5:F9749@46` | ❌ error | — | — | Trace upstream from L5:F9749 (medical conditions/procedures/practitioners featur… |

### Re-dispatch (round 3): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L5:F9749@46` | ✅ reported | 11 | 12 | Trace upstream from L5:F9749 (medical conditions/procedures feature, pos 46). Th… |

<details>
<summary><b>SA-5</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F9749 | " words related to various medical conditions, procedures, and practiti" |
| 2 | `get_upstream_features` | L5:F9749@46, k=15 | L4:F4665 (de=2.92) +14 more |
| 3 | `inspect_feature` | L4, F4665 | " words and phrases related to medical environments, treatments, person" |
| 4 | `get_upstream_features` | L4:F4665@46, k=10 | Emb:" labor"@44 (de=3.45) +9 more |
| 5 | `inspect_feature` | L4, F13803 | " terms related to obstetrics and gynecology" |
| 6 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |
| 7 | `get_upstream_features` | L4:F13803@46, k=10 | Emb:" delivery"@46 (de=13.81) +9 more |
| 8 | `get_upstream_features` | L4:F4665@46, k=15 | Emb:" labor"@44 (de=3.45) +14 more |
| 9 | `get_upstream_features` | L3:F9008@46, k=10 | Emb:" delivery"@46 (de=14.25) +9 more |
| 10 | `inspect_feature` | L3, F10198 | " words related to anesthetics and medical procedures" |
| 11 | `get_upstream_features` | L3:F9008@46, k=10 | Emb:" delivery"@46 (de=14.25) +9 more |
| 12 | `inspect_feature` | L1, F7152 | "the word "delivery"" |

**Findings:** Tracing from the medical‑conditions feature (L5:F9749) reveals a cascade of upstream nodes that originate in lower layers. The strongest positive drivers are embeddings for the tokens "delivery" (pos 46) and "labor" (pos 44), which directly excite a low‑layer delivery detector (L1:F7152). This detector feeds into a childbirth feature (L3:F9008), which in turn excites both a generic medical‑environ…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L0:1832, L4:9757, L0:10846, L4:12178, L6:9980, L5:9749, L7:3979 |
| 2 | `get_upstream_features` | L6:F9980@46, k=10 → L4:F4665 (de=2.77) +9 more |
| 3 | `get_upstream_features` | L0:F1832@44, k=10 → Emb:" labor"@44 (de=25.00) +9 more |
| 4 | `get_upstream_features` | L4:F12178@30, k=10 → Emb:" spent"@26 (de=10.12) +9 more |
| 5 | `get_upstream_features` | L4:F9757@1, k=10 → Emb:"<bos>"@0 (de=15.94) +9 more |
| 6 | `get_upstream_features` | L0:F10846@3, k=10 → Emb:" also"@3 (de=33.50) +9 more |
| 7 | `inspect_feature` ×7 | L0:8854, L6:4490, L5:1275, L4:13803, L3:9008, L1:7152, L7:210 |

### Build

`build_circuit` → 24 nodes, 32 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 76,528 | 6,152 | 128,677 | 0 | $0.0381 | — | — |
| SA-1 | openai/gpt-oss-120b | 94,923 | 7,229 | 5,056 | 0 | $0.0187 | ✅ 6F/7E | Trace upstream from L14:F3985 (terms related to management, … |
| SA-2 | openai/gpt-oss-120b | 71,649 | 5,467 | 2,528 | 0 | $0.0141 | ✅ 4F/12E | Trace upstream from L6:F15267 (words in document referring t… |
| SA-3 | openai/gpt-oss-120b | 60,977 | 4,657 | 5,152 | 0 | $0.0120 | ✅ 4F/7E | Trace upstream from L15:F15159 (medical/healthcare words). F… |
| SA-5 | openai/gpt-oss-120b | 154,010 | 13,512 | 7,936 | 0 | $0.0313 | ✅ 11F/12E | Trace upstream from L5:F9749 (medical conditions/procedures … |
| **Total** | | **458,087** | **37,017** | **149,349** | **0** | **$0.1141** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 9m 41s