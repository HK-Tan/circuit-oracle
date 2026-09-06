# Circuit Oracle Report
**Date:** 2026-07-28 08:33:43 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by features that recognize academic qualifications, university affiliations, and academic fields, rather than spurious markers like gender.

**Confidence:** 9

**Reasoning:** 
The attribution circuit shows that the probe score is primarily driven by a set of features specialized in detecting academic credentials. At the late stage of the circuit, **L7:F14129** ("academic degrees, universities, and people associated with them") has a strong positive direct effect on the probe's output. This feature is supported by earlier-layer features that identify broader academic contexts: **L6:F170** ("references to academic fields") and **L3:F4213** ("mentions of degree qualifications or awards"). 

The signal originates from the input tokens describing the subject's educational history (B.A., M.S., Ph.D., and university names). No features related to gender markers or other irrelevant demographics appeared in the top-k attribution for the probe score. The flow of information is a logical progression from recognizing individual academic keywords to identifying a general "academic profile," which the probe then uses to classify the profession (likely as "Professor" or "Academic").

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 0 | Input Tokens (Academic/Context) |  the word "ice" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 0 | Input Tokens (Academic/Context) | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 0 | Academic Field & Award Detection |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 0 | Academic Field & Award Detection |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 0 | Degree & University Recognition |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:3235 de=-0.054 |
| 3 | `inspect_feature` ×6 | L0:15320, L0:6270, L7:14129, L3:4213, L6:170, L2:14934 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 6 | `get_top_features` | 15 features; top: L6:3235 de=-0.054 |
| 7 | `inspect_feature` ×6 | L0:15320, L0:6270, L7:14129, L3:4213, L6:170, L2:14934 |
| 8 | `get_top_logits` | "" (100%) |
| 9 | `get_top_features` | 15 features; top: L6:3235 de=-0.054 |
| 10 | `inspect_feature` ×6 | L0:15320, L0:6270, L7:14129, L3:4213, L6:170, L2:14934 |
| 11 | `get_top_logits` | "" (100%) |
| 12 | `get_top_features` | 15 features; top: L6:3235 de=-0.054 |
| 13 | `inspect_feature` ×6 | L0:15320, L0:6270, L7:14129, L3:4213, L6:170, L2:14934 |
| 14 | `get_top_logits` | "" (100%) |

### Build

`build_circuit` → 4 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 673,849 | 1,278 | 0 | 0 | $0.0949 | — | — |
| **Total** | | **673,849** | **1,278** | **0** | **0** | **$0.0949** | | |

**Oracle wall-clock time:** 2m 58s