# Circuit Oracle Report
**Date:** 2026-07-28 08:32:55 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies the profession by relying on a mixture of genuine academic markers (research interests, degrees, universities) and a spurious gender marker (male pronouns).

**Confidence:** 9

**Reasoning:** 
The attribution circuit shows that the probe's classification score is driven by three primary signals. First, it utilizes genuine academic indicators: features L1:F10986 (Academic Research Context) and L7:F14129 (Academic Degrees/Universities) contribute positively to the score. These features capture the semantic essence of the text (e.g., "research interests," "Ph.D. in History," "Stanford University"). 

However, the circuit also reveals a significant contribution from L0:F1069, which is explicitly labeled as a "Male Gender Marker" (detecting "He" or "His"). This feature's presence in the causal path to the probe score indicates that the probe is partially using the subject's gender as a heuristic to predict their profession, confirming the user's concern about spurious features. The signal flows from these early-layer markers (L0, L1, L7) directly into the probe's classification direction (L26), suggesting the probe is sensitive to both the professional context and the demographic marker of the individual.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male Gender Marker (He/His) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Academic Research Context |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 15 | Academic Degrees/Universities |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 3 | `get_top_features` | 15 features; top: L8:2383 de=-0.090 |
| 4 | `inspect_feature` ×6 | L0:6051, L1:10986, L7:14129, L0:1069, L8:2383, L6:14747 |
| 5 | `get_top_logits` | "" (100%) |
| 6 | `get_top_features` | 15 features; top: L8:2383 de=-0.090 |
| 7 | `inspect_feature` ×5 | L0:6051, L1:10986, L0:1069, L7:14129, L8:2383 |
| 8 | `get_top_logits` | "" (100%) |
| 9 | `get_top_features` | 10 features; top: L8:2383 de=-0.090 |
| 10 | `inspect_feature` ×6 | L0:6051, L1:10986, L7:14129, L0:1069, L8:2383, L6:14747 |
| 11 | `get_top_logits` | "" (100%) |
| 12 | `get_top_features` | 15 features; top: L8:2383 de=-0.090 |
| 13 | `inspect_feature` | " references to a male person, particularly when using the pronoun "He"" |

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 516,976 | 1,062 | 4,352 | 0 | $0.0729 | — | — |
| **Total** | | **516,976** | **1,062** | **4,352** | **0** | **$0.0729** | | |

**Oracle wall-clock time:** 2m 12s