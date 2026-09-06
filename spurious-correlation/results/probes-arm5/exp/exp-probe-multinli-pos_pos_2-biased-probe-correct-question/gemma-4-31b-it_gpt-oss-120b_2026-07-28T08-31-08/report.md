# Circuit Oracle Report
**Date:** 2026-07-28 08:31:08 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by superficial linguistic markers—specifically filler words and common keywords—rather than the semantic content of the prompt.

**Confidence:** 9

**Reasoning:** 
The attribution circuit reveals that the probe's score is primarily determined by a collection of "spurious" features. The most significant contributions come from:
1. **Filler Words/Agreement:** Features such as `L4:F9602` (interjections and filler words) and `L4:F12126` (agreement expressions like "well" and "yeah") contribute significantly. These features fire on the conversational markers "yeah well" and "uh" at the start of the prompt.
2. **Generic Keywords:** The probe is positively driven by the presence of common tokens, specifically the word "because" (`L0:F16366`) and the word "the" (`L0:F3820`).
3. **Negation/Contradiction Markers:** Interestingly, `L0:F6236` (which detects the "t" in "isn't" or "doesn't") has a strong positive effect, suggesting the probe may be associating negative contractions with the target class.

There is no evidence of features encoding the actual subject matter (NCAA tournament, Louisville, Sweet 16) or the logical contradiction present in the text (not watching the tournament vs. not missing a single game). Instead, the signal flows directly from these low-level lexical and stylistic markers to the probe's output, confirming the user's concern that the probe relies on spurious correlations.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F9602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) | 4 | Filler Words/Agreement (well, uh, yeah) |  interjections and filler words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) |
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Filler Words/Agreement (well, uh, yeah) |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Keyword: "because" |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Keyword: "the" | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:9602 de=-0.629 |
| 3 | `inspect_feature` ×6 | L0:6236, L0:3820, L0:16366, L4:9602, L0:8352, L4:12126 |
| 4 | `get_top_logits` | "" (100%) |

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 85,971 | 779 | 4,224 | 0 | $0.0124 | — | — |
| **Total** | | **85,971** | **779** | **4,224** | **0** | **$0.0124** | | |

**Oracle wall-clock time:** 0m 29s