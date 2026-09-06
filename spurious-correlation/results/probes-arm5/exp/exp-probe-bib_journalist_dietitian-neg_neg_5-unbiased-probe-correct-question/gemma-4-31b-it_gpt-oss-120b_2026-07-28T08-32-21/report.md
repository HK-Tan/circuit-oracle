# Circuit Oracle Report
**Date:** 2026-07-28 08:32:21 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a circuit that detects the professional keyword "reporter" and propagates this signal through layers of journalism-specific semantic features.

**Confidence:** 9

**Reasoning:** 
The attribution circuit demonstrates that the probe relies on genuine professional indicators rather than spurious markers. The signal originates at the token embedding for "reporter" (pos 61), which activates an early-layer feature (L4:F13253) associated with "things related to journalism and the media." This signal then flows through mid-layer features specifically encoding journalism and newspaper concepts (L14:F4420), and finally into a late-layer feature (L19:F2486) that encodes "journalistic sources and news outlets." 

This chain of evidence—from the specific token "reporter" to increasingly abstract journalism-related semantic features—shows a clear, causal path from professional identity in the text to the probe's classification score. No gender markers or other unrelated demographic features were found to be significant drivers in the top attribution paths.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 61 | Emb: reporter (pos 61) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 61 | Journalism Entity Detection (L4) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 61 | Journalism Concept (L14) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 61 | Journalism Classification (L19) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L14:4420 de=-0.196 |
| 3 | `inspect_feature` ×6 | L14:4420, L19:2486, L4:13253, L0:4874, L0:6051, L0:8642 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L14:4420 de=-0.196 |
| 6 | `inspect_feature` ×5 | L14:4420, L19:2486, L4:13253, L0:4874, L0:8642 |

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 161,333 | 1,166 | 32,640 | 0 | $0.0235 | — | — |
| **Total** | | **161,333** | **1,166** | **32,640** | **0** | **$0.0235** | | |

**Oracle wall-clock time:** 1m 36s