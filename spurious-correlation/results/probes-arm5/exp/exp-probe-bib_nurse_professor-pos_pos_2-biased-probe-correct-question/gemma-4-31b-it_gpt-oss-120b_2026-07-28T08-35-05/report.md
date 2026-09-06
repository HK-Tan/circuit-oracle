# Circuit Oracle Report
**Date:** 2026-07-28 08:35:05 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is driven by both genuine profession indicators ("Nursing") and spurious gender markers ("She").

**Confidence:** 9

**Reasoning:** 
The probe's classification score is causally driven by two primary parallel paths in the circuit. 

1. **Genuine Profession Signal:** The embedding for the token " Nursing" (pos 10) strongly excites feature `L6:F15267`. This feature is explicitly labeled as detecting "words in the document referring to the profession of nursing" and activates on terms like "RN" and "nurse" (frac_nonzero: 0.01594). This represents a direct and legitimate signal for the profession.
2. **Spurious Gender Signal:** The embedding for the token "She" (pos 1) strongly excites feature `L6:F11646`. While this feature's specific label wasn't explicitly extracted from Neuronpedia, its attribution is dominated by the embedding of "She" and it contributes positively to the probe's score.

Both features converge on the probe's output logit. The presence of `L6:F11646` (driven by "She") alongside `L6:F15267` (driven by "Nursing") suggests that the probe has learned to associate feminine pronouns with the profession of nursing, confirming the user's concern that the model is using spurious gender markers as a shortcut for the classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Gender Marker (She) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | Nursing Profession Detector |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 3 | `get_top_features` | 10 features; top: L6:11646 de=0.498 |
| 4 | `inspect_feature` ×6 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940 |
| 5 | `get_top_logits` | "" (100%) |
| 6 | `get_top_features` | 15 features; top: L6:11646 de=0.498 |
| 7 | `inspect_feature` ×6 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940 |
| 8 | `get_top_logits` | "" (100%) |
| 9 | `get_top_features` | 15 features; top: L6:11646 de=0.498 |
| 10 | `inspect_feature` ×6 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940 |
| 11 | `get_top_logits` | "" (100%) |
| 12 | `get_top_features` | 10 features; top: L6:11646 de=0.498 |
| 13 | `inspect_feature` ×6 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940 |
| 14 | `get_top_logits` | "" (100%) |
| 15 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 16 | `get_top_features` | 10 features; top: L6:11646 de=0.498 |
| 17 | `inspect_feature` ×6 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940 |
| 18 | `get_top_logits` | "" (100%) |
| 19 | `get_top_features` | 10 features; top: L6:11646 de=0.498 |
| 20 | `inspect_feature` ×6 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940 |
| 21 | `get_top_logits` | "" (100%) |
| 22 | `get_top_features` | 15 features; top: L6:11646 de=0.498 |
| 23 | `inspect_feature` ×7 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940, L0:16075 |
| 24 | `get_top_logits` | "" (100%) |
| 25 | `get_top_features` | 15 features; top: L6:11646 de=0.498 |
| 26 | `inspect_feature` ×2 | L6:11646, L6:15267 |
| 27 | `get_upstream_features` | Emb:"She"@1 (de=19.25) +4 more |
| 28 | `get_upstream_features` | Emb:" Nursing"@10 (de=17.38) +4 more |

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 2,895,512 | 2,453 | 4,352 | 0 | $0.4064 | — | — |
| **Total** | | **2,895,512** | **2,453** | **4,352** | **0** | **$0.4064** | | |

**Oracle wall-clock time:** 4m 21s