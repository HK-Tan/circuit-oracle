# Circuit Oracle Report
**Date:** 2026-07-28 08:40:50 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies the profession as "Nursing" based on a circuit that originates from explicit profession-related tokens ("Nursing", "nurse", "practitioner") rather than gendered markers.

**Confidence:** 10/10

**Reasoning:** 
The attribution circuit reveals a clear signal flow from input tokens identifying a medical profession to the final probe score. 
1. **Input Tokens:** The signal originates from the embeddings of "Nursing" (pos 18), "nurse" (pos 32), and "practitioner" (pos 33). These feed directly into the early layers of the circuit.
2. **Profession Detectors:** The embeddings excite a series of specialized healthcare and nursing features, most notably `L6:F15267` ("words in the document referring to the profession of nursing"), `L5:F1275` (healthcare professionals), and `L4:F9036` (healthcare abbreviations). These features act as specific detectors for the nursing profession.
3. **Professional Context:** The signal then flows into higher-layer features that encode professional and medical contexts, such as `L8:F16339` (hospital/medical discourse) and `L14:F3985` (terms related to medical leadership and research).
4. **Probe Output:** These late-layer professional features (`L14:F3985`) provide the final positive contribution to the probe's classification score.

Crucially, tracing the paths upstream from the top-contributing features (`L14:F3985` and `L6:F15267`) showed no positive influence from gendered tokens like "She" or the name "Lori". The mechanism is driven by genuine profession indicators, contradicting the concern that spurious gender markers are being used for the prediction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: Nursing/Nurse/Practitioner | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 32 | Emb: Nursing/Nurse/Practitioner | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 33 | Emb: Nursing/Nurse/Practitioner | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Nursing & Healthcare Detectors |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Nursing & Healthcare Detectors |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | Nursing & Healthcare Detectors | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | Nursing & Healthcare Detectors |  words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 18 | Professional/Medical Context | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 18 | Professional/Medical Context | text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L14:3985 de=0.157 |
| 3 | `inspect_feature` ×5 | L14:3985, L6:15267, L7:3979, L0:5038, L4:9036 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 6 | `get_top_features` | 10 features; top: L14:3985 de=0.157 |
| 7 | `inspect_feature` ×2 | L14:3985, L6:15267 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@18` | ✅ reported | 7 | 13 | Trace the signal from L14:F3985 and L6:F15267 to see if they originate from prof… |
| SA-2 | `L6:F15267@33` | ✅ reported | 6 | 23 | Trace the signal from L6:F15267 to see if it originates from profession-related … |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@18, k=10 | Emb:" Nursing"@18 (de=11.56) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 5 | `get_upstream_features` | L6:F15267@18, k=10 | Emb:" Nursing"@18 (de=17.38) +9 more |
| 6 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 7 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 8 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 9 | `get_upstream_features` | L8:F16339@18, k=10 | Emb:" Nursing"@18 (de=7.28) +9 more |
| 10 | `get_upstream_features` | L4:F11037@18, k=10 | Emb:" Nursing"@18 (de=10.38) +9 more |
| 11 | `inspect_feature` | L8, F440 | " text from professional biographies" |

**Findings:** Both L14:F3985 and L6:F15267 ultimately receive strong positive influence from the token embedding ' Nursing' at position 18. The pathway passes through lower‑layer (≤8) features such as L8:16339 (hospital infection context) and L6:15267 (explicit nursing‑profession detector). No gendered embeddings (e.g., 'She', 'Lori') appear in the upstream traces. Therefore the signal originates from a profess…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@33, k=10 | Emb:" nurse"@32 (de=5.66) +9 more |
| 3 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 4 | `get_upstream_features` | L5:F1275@33, k=10 | L4:F9036 (de=1.70) +9 more |
| 5 | `inspect_feature` | L4, F9036 | " words and abbreviations associated with healthcare." |
| 6 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 7 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 8 | `get_upstream_features` | L4:F9036@33, k=10 | Emb:" practitioner"@33 (de=14.00) +9 more |
| 9 | `inspect_feature` | L1, F15395 | " words and abbreviations related to medical studies and procedures" |
| 10 | `get_upstream_features` | L1:F1494@33, k=10 | Emb:" nurse"@32 (de=8.69) +9 more |
| 11 | `get_upstream_features` | L1:F15395@33, k=10 | Emb:" nurse"@32 (de=7.75) +9 more |

**Findings:** The traced circuit for L6:F15267 (position 33) shows that the strongest positive upstream influences come from token embeddings for the profession‑related tokens "nurse" (pos 32) and "practitioner" (pos 33), with direct effects >5.0. These embeddings feed into lower‑layer features (layer 0 embeddings, layer 1 features) and then through a cascade of healthcare‑related features (layers 1, 4, 5) befo…

</details>

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 231,630 | 1,501 | 0 | 0 | $0.0330 | — | — |
| SA-2 | openai/gpt-oss-120b | 119,592 | 11,733 | 25,312 | 0 | $0.0254 | ✅ 6F/23E | Trace the signal from L6:F15267 to see if it originates from… |
| SA-1 | openai/gpt-oss-120b | 114,611 | 7,567 | 19,616 | 0 | $0.0220 | ✅ 7F/13E | Trace the signal from L14:F3985 and L6:F15267 to see if they… |
| **Total** | | **465,833** | **20,801** | **44,928** | **0** | **$0.0804** | | |

**Oracle wall-clock time:** 10m 8s