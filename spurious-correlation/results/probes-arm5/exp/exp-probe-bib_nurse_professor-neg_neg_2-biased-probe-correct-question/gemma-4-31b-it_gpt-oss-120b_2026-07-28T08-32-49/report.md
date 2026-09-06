# Circuit Oracle Report
**Date:** 2026-07-28 08:32:49 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a combination of academic field indicators (Mechanical Engineering) and spurious gender markers (his, he), suggesting the model is using demographic shortcuts alongside genuine professional data.

**Confidence:** 9/10

**Reasoning:**
The circuit reveals two parallel pathways contributing to the probe's classification score:

1.  **Genuine Profession Path:** The embeddings for "degree" (pos 6), "Mechanical" (pos 7), and "Engineering" (pos 8) feed into a supernode of `Academic_Features` (e.g., L6:F170). This path captures the explicit professional qualifications mentioned in the text.
2.  **Spurious Gender Path:** A significant portion of the signal originates from gendered pronouns "his" (pos 2, 12) and "He" (pos 11). These embeddings drive a sequence of `Gender_Features` across multiple layers (L0:F2994 $\rightarrow$ L6:F12990 $\rightarrow$ L7:F14893 $\rightarrow$ L12:F2175). This indicates that the probe is partially relying on the subject's gender as a proxy for the profession.

The convergence of both the `Academic_Features` and `Gender_Features` supernodes into the final `Probe_Logit` (L26) confirms that the classification is not based solely on the professional credentials, validating the user's concern regarding the use of spurious gender markers.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 2 | Gender/Male Markers | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | Gender/Male Markers |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 2 | Gender/Male Markers |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | Gender/Male Markers |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 8 | Academic/Field Markers |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:2994 de=0.395 |
| 3 | `inspect_feature` ×7 | L0:2994, L7:14893, L7:14946, L12:2175, L6:12990, L6:170, L18:14743 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L0:2994 de=0.395 |
| 6 | `inspect_feature` ×5 | L0:2994, L7:14893, L6:170, L6:12990, L12:2175 |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 222,037 | 1,503 | 0 | 0 | $0.0317 | — | — |
| **Total** | | **222,037** | **1,503** | **0** | **0** | **$0.0317** | | |

**Oracle wall-clock time:** 2m 8s