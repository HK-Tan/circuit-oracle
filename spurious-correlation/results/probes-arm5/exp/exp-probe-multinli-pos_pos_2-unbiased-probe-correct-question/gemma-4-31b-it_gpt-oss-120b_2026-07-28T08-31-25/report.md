# Circuit Oracle Report
**Date:** 2026-07-28 08:31:25 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by superficial linguistic markers—specifically conversational fillers, negation signals, and causal conjunctions—rather than a semantic understanding of the prompt's content.

**Confidence:** 9

**Reasoning:** 
The attribution analysis reveals that the probe's classification score is determined by several low-level, non-semantic features. 

1. **Conversational Fillers:** Features **L4:F12126** and **L4:F4847** (grouped in `filler_words`) respond to "yeah" and "well" at the start of the prompt. These features have a strong effect on the logit, but they encode conversational style rather than contradiction or any specific factual claim.
2. **Negation/Contraction Signals:** Feature **L0:F6236** (`negation_signals`) specifically detects the letter "t" following contractions like "isn't" or "doesn't" (detected at position 20, corresponding to "haven't"). This is a classic "spurious feature" where the probe relies on the presence of negation markers to predict a "contradiction" label without analyzing the actual meaning of the negated statement.
3. **Causal Markers:** Feature **L0:F16366** (`causal_marker`) detects the word "because". While "because" often introduces an explanation that could be contradictory, the feature itself is a simple lexical detector.
4. **Generic Context:** Feature **L0:F8083** (`numeric_context`) detects the word "double" in a numeric context (e.g., "NC double A"), which is entirely irrelevant to the semantic task of contradiction detection.

The signal flows directly from these early-layer (L0-L4) lexical detectors to the probe output. There is no evidence of higher-layer semantic integration or entity-specific reasoning. This confirms the user's concern: the probe is utilizing spurious "shortcut" features (negation words and filler phrases) to make its prediction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Conversational Fillers ('yeah', 'well') |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Conversational Fillers ('yeah', 'well') |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 20 | Negation/Contraction Signal ('n't') | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Causal Marker ('because') |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L0:F8083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) | 6 | Numeric/Double Context ('double') | the word "double" and surrounding words when numbers are also present | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L4:12126 de=-0.648 |
| 3 | `inspect_feature` ×6 | L4:12126, L0:6236, L4:4847, L0:8083, L3:9770, L0:16366 |
| 4 | `get_top_logits` | "" (100%) |

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 87,423 | 937 | 0 | 0 | $0.0126 | — | — |
| **Total** | | **87,423** | **937** | **0** | **0** | **$0.0126** | | |

**Oracle wall-clock time:** 0m 43s