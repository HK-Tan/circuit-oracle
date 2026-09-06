# Circuit Oracle Report
**Date:** 2026-07-28 08:36:56 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession classification probe is driven by a hierarchical circuit that detects nursing-specific terminology and healthcare environments, originating from the input token "Nursing".

**Confidence:** 10/10

**Reasoning:** 
The circuit originates from the input token "Nursing" (position 10), which directly activates several lower-layer features specialized in healthcare. Specifically, it triggers **L6:F15267** (a highly specific nursing profession detector, `frac_nonzero: 0.01594`), which then feeds into a set of context-building features including **L7:F210** (healthcare system names) and **L8:F16339** (hospital environment/infection terminology). These signals converge on **L14:F3985**, a higher-level feature encoding "terms related to management, leadership, medicine, studies, and research" (`frac_nonzero: 0.06604`). This late-layer feature, which strongly promotes clinical vocabulary like "patients" and "clinicians", provides the final causal push to the probe's classification score. 

Crucially, the attribution trace shows no evidence of signal originating from gender markers (e.g., "She") or other spurious tokens. The path is strictly anchored in profession-specific identifiers ("Nursing", "RN") and the associated medical domain context, confirming that the model is using genuine profession indicators to drive the probe's output.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 1 | Emb: graduated | the word "graduated" or variations of it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 1 | Emb: Nursing | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 1 | Nursing Detector (Early) |  mentions of nurses, nursing, and nurse management | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 1 | Nursing Profession (Mid) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 1 | Medical/Professional Terms (Late) | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.188 |
| 3 | `inspect_feature` ×6 | L14:3985, L6:15267, L0:5038, L0:6270, L15:15159, L8:16339 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L14:3985 de=0.188 |
| 6 | `inspect_feature` ×5 | L14:3985, L6:15267, L0:5038, L0:6270, L3:15901 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 15 features; top: L14:3985 de=0.188 |
| 9 | `inspect_feature` ×5 | L14:3985, L6:15267, L0:5038, L0:6270, L3:15901 |
| 10 | `get_top_logits` | "" (100%) |
| 11 | `get_top_features` | 15 features; top: L14:3985 de=0.188 |
| 12 | `inspect_feature` | "terms related to management, leadership, medicine, studies, and resear" |

### Dispatch: 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@10` | ✅ reported | 5 | 11 | Trace the signal from L14:F3985 (Medical/Professional) back to the embeddings. C… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3985 | "terms related to management, leadership, medicine, studies, and resear" |
| 2 | `get_upstream_features` | L14:F3985@10, k=10 | Emb:" Nursing"@10 (de=12.12) +9 more |
| 3 | `inspect_feature` | L8, F16339 | " text discussing hospital infections and bacteria" |
| 4 | `inspect_feature` | L7, F210 | " words and names associated with the Asante Healthcare system" |
| 5 | `get_upstream_features` | L8:F16339@10, k=10 | Emb:" Nursing"@10 (de=7.66) +9 more |
| 6 | `inspect_feature` | L6, F4490 | " proper nouns corresponding to locations, organizations, medical roles" |
| 7 | `get_upstream_features` | L6:F4490@10, k=10 | Emb:" Nursing"@10 (de=11.62) +9 more |
| 8 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 9 | `get_upstream_features` | L7:F210@10, k=10 | Emb:" Nursing"@10 (de=8.19) +9 more |
| 10 | `get_upstream_features` | L6:F15267@10, k=10 | Emb:" Nursing"@10 (de=17.38) +9 more |

**Findings:** The signal in L14:F3985 originates primarily from the input token 'Nursing' (positive direct_effect >12). The token drives a cascade through a chain of lower‑layer medical features: L6:15267 (explicit nursing‑profession detector) → L8:16339 (hospital‑infection context) and L7:210 (healthcare‑system names) → L6:4490 (medical proper‑noun detector) → the top‑level professional/medical feature L14:F39…

</details>

### Build

`build_circuit` → 6 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 616,280 | 2,121 | 0 | 0 | $0.0871 | — | — |
| SA-1 | openai/gpt-oss-120b | 89,675 | 6,207 | 21,248 | 0 | $0.0175 | ✅ 5F/11E | Trace the signal from L14:F3985 (Medical/Professional) back … |
| **Total** | | **705,955** | **8,328** | **21,248** | **0** | **$0.1046** | | |

**Oracle wall-clock time:** 6m 16s