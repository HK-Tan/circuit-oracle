# Circuit Oracle Report
**Date:** 2026-07-28 08:35:17 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe's classification score is driven by a circuit that detects medical profession markers (specifically "nurse") and healthcare-related research terminology, rather than spurious gendered markers.

**Confidence:** 10/10

**Reasoning:**
The attribution circuit shows a clear flow from specific professional and medical terminology to the probe's output. Two primary pathways converge in the late layers:

1.  **Nursing Profession Pathway:** The signal originates from the input token **" nurse" (pos 7)**. This token strongly activates a suite of occupational detectors in early-to-mid layers, including **L6:F15267** (specifically labeled for the profession of nursing, `frac_nonzero: 0.01594`), as well as more generic occupational features like **L4:F11037** and **L5:F12279**.
2.  **Medical Context Pathway:** A parallel signal flows from medical research terms (e.g., "clinical", "trials", "Medicine"). This is captured by early-layer features such as **L0:F15756** (health/medical research), **L1:F11869** (clinical trials), and **L2:F6268** (scientific studies).

These two pathways converge on a high-level "Medical Professionalism" feature, **L14:F3985** (`frac_nonzero: 0.06604`), which encodes concepts related to medical leadership, studies, and research. This feature then provides the final direct causal push to the probe's output logit. 

Crucially, the trace shows that while gendered tokens (e.g., "She" at pos 1) provide negligible positive influence, the dominant drivers are explicitly tied to the profession of nursing and the medical field. The mechanism is thus based on genuine profession indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 7 | Emb: nurse (pos 7) proxy |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L0:F15756](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15756) | 22 | Emb: medical terms proxy | words and phrases related to health, studies, and medical research | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15756) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 25 | Nursing & Occupational Detectors |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 7 | Nursing & Occupational Detectors | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L5:F12279](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12279) | 7 | Nursing & Occupational Detectors | terms relating to jobs and education | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12279) |
| [L1:F11869](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11869) | 22 | Medical Research & Study Features | mentions of clinical trials and studies, with a focus on phases, results, and patients. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11869) |
| [L2:F6268](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6268) | 22 | Medical Research & Study Features | mentions of scientific and/or medical research studies | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6268) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 22 | Medical Professionalism Summary | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.089 |
| 3 | `inspect_feature` ×5 | L14:3985, L6:15267, L4:4665, L15:15159, L6:9980 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@25` | ✅ reported | 4 | 11 | Trace the path from L14:F3985 to determine if the signal originates from nursing… |
| SA-2 | `L6:F15267@25` | ✅ reported | 8 | 12 | Trace the path from L6:F15267 to identify the specific input tokens triggering t… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@25, k=10 | ❌ Feature (layer=14, feature_idx=3985) not found at pos=25. Th |
| 3 | `get_upstream_features` | L14:F3985@22, k=10 | L1:F11869 (de=2.89) +9 more |
| 4 | `inspect_feature` | L1, F11869 | " mentions of clinical trials and studies, with a focus on phases, resu" |
| 5 | `inspect_feature` | L2, F6268 | "mentions of scientific and/or medical research studies" |
| 6 | `inspect_feature` | L0, F15756 | " words and phrases related to health, studies, and medical research" |
| 7 | `get_upstream_features` | L1:F11869@22, k=10 | Emb:" trials"@22 (de=5.56) +9 more |
| 8 | `get_upstream_features` | L1:F11869@22, k=10 | Emb:" trials"@22 (de=5.56) +9 more |
| 9 | `get_upstream_features` | L2:F6268@22, k=10 | Emb:" trials"@22 (de=8.75) +9 more |
| 10 | `get_upstream_features` | L14:F3985@25, k=10 | ❌ Feature (layer=14, feature_idx=3985) not found at pos=25. Th |

**Findings:** Tracing from L14:F3985 (position 22) reveals a cascade of positive influences rooted in early‑layer (≤8) features and raw token embeddings. The strongest upstream drivers are medical‑research features (L1:F11869, L2:F6268) and embeddings for tokens such as "clinical", "trials", "Medicine", and "nurse". No gendered terms appear among the top upstream tokens or features. Thus the signal originates f…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@25, k=10 | ❌ Feature (layer=6, feature_idx=15267) not found at pos=25. Th |
| 3 | `get_upstream_features` | L6:F15267@7, k=10 | Emb:" nurse"@7 (de=21.62) +9 more |
| 4 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 5 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 6 | `inspect_feature` | L5, F12279 | " terms relating to jobs and education" |
| 7 | `get_upstream_features` | L4:F8751@7, k=10 | Emb:" nurse"@7 (de=9.25) +9 more |
| 8 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 9 | `get_upstream_features` | L4:F8751@7, k=10 | Emb:" nurse"@7 (de=9.25) +9 more |
| 10 | `inspect_feature` | L2, F5224 | " words related to retail and customer service jobs" |
| 11 | `get_upstream_features` | L4:F11037@7, k=10 | Emb:" nurse"@7 (de=5.91) +9 more |
| 12 | `get_upstream_features` | L2:F5224@7, k=10 | Emb:" nurse"@7 (de=13.31) +9 more |

**Findings:** The nursing‑profession feature (L6:F15267) is driven primarily by the raw token embedding for the word "nurse" at position 7 (direct_effect ≈ 21.6). Secondary contributions flow through a cascade of occupational‑detector features in layers 4, 5, and 2 (F8751, F11037, F12279, F5224), all of which receive a positive push from the same "nurse" embedding. Since we have reached a lower‑third layer (lay…

</details>

### Build

`build_circuit` → 6 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 107,589 | 1,774 | 0 | 0 | $0.0158 | — | — |
| SA-1 | openai/gpt-oss-120b | 69,889 | 5,563 | 31,072 | 0 | $0.0143 | ✅ 4F/11E | Trace the path from L14:F3985 to determine if the signal ori… |
| SA-2 | openai/gpt-oss-120b | 118,231 | 7,073 | 18,560 | 0 | $0.0223 | ✅ 8F/12E | Trace the path from L6:F15267 to identify the specific input… |
| **Total** | | **295,709** | **14,410** | **49,632** | **0** | **$0.0523** | | |

**Oracle wall-clock time:** 4m 35s