# Circuit Oracle Report
**Date:** 2026-07-28 08:35:22 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by a spurious mechanism that triggers on the identity of the group mentioned (specifically the suffix "-ian" in "Indians") rather than the toxic semantic content of the prompt.

**Confidence:** 9/10

**Reasoning:** 
The attribution circuit reveals that the probe's score is primarily influenced by features identifying a specific ethnic/national group. The signal originates from the input token "Indians" (pos 1), which activates a morphological detector in layer 2 (L2:F2123) that specifically targets words ending in "-ian" (a common suffix for nationalities/ethnicities, e.g., Canadian, Bosnian, Russian). 

This morphological signal then feeds into L3:F13473, which appears to function as a broader "ethnic group detector" (triggered by "Indians" and "are" at pos 1 and 2). Crucially, this early-layer identity signal flows directly into the probe's classification score. There is no evidence in the top features that lexical markers of toxicity (e.g., "abusers", "destroy", "backlash") are the primary drivers of the probe's output in this instance. Instead, the probe is using the presence of an identity group—detected via a simple morphological pattern—as a proxy for toxicity, confirming the user's concern about spurious identity-based signals.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Indians (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F2123](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) | 1 | Suffix '-ian' detector (L2:F2123) |  words ending in "ian", "jani", "iti", "ino", or "olan" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | Ethnic group detector (L3:F13473) |  mentions of racial and ethnic groups, especially in the United States | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:11375 de=0.221 |
| 3 | `inspect_feature` ×5 | L0:11375, L0:11668, L3:14281, L0:11154, L6:10545 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 6 | `get_top_features` | 15 features; top: L0:11375 de=0.221 |
| 7 | `inspect_feature` ×7 | L0:11375, L0:11668, L0:11154, L0:8381, L6:10545, L3:13473, L2:1680 |
| 8 | `get_top_logits` | "" (100%) |
| 9 | `get_top_features` | 15 features; top: L0:11375 de=0.221 |
| 10 | `inspect_feature` ×9 | L0:11375, L0:11668, L3:14281, L0:11154, L6:10545, L3:13473, L5:3229, L2:1680, L0:8381 |
| 11 | `get_top_logits` | "" (100%) |
| 12 | `get_top_features` | 15 features; top: L0:11375 de=0.221 |
| 13 | `inspect_feature` ×5 | L0:11375, L0:11668, L6:10545, L3:13473, L5:3229 |
| 14 | `get_top_logits` | "" (100%) |
| 15 | `get_top_features` | 10 features; top: L0:11375 de=0.221 |
| 16 | `inspect_feature` ×5 | L0:11375, L0:11668, L3:14281, L0:11154, L6:10545 |
| 17 | `get_top_logits` | "" (100%) |
| 18 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 19 | `get_top_features` | 15 features; top: L0:11375 de=0.221 |
| 20 | `inspect_feature` ×6 | L0:11375, L0:11668, L0:11154, L0:8381, L6:10545, L3:13473 |
| 21 | `get_top_logits` | "" (100%) |
| 22 | `get_top_features` | ❌ Token '''' is not one of the top-k next-token candidates cap |
| 23 | `get_top_features` | 15 features; top: L0:11375 de=0.221 |
| 24 | `inspect_feature` ×6 | L0:11375, L0:11668, L0:11154, L6:10545, L3:13473, L0:8381 |
| 25 | `get_top_logits` | "" (100%) |
| 26 | `get_top_features` | 15 features; top: L0:11375 de=0.221 |
| 27 | `inspect_feature` ×3 | L0:11668, L3:13473, L0:11375 |
| 28 | `get_upstream_features` | Emb:"Indians"@1 (de=10.25) +4 more |
| 29 | `inspect_feature` | " words ending in "ian", "jani", "iti", "ino", or "olan"" |

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 3,196,131 | 2,409 | 0 | 0 | $0.4484 | — | — |
| **Total** | | **3,196,131** | **2,409** | **0** | **0** | **$0.4484** | | |

**Oracle wall-clock time:** 4m 37s