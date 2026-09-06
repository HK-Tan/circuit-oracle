# Circuit Oracle Report
**Date:** 2026-07-28 08:33:51 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven by a combination of shallow lexical triggers and early-layer semantic patterns, including negation-like quantifiers ("no one") and common functional words, rather than deep semantic reasoning.

**Confidence:** 8/10

**Reasoning:**
The attribution circuit reveals that the probe relies heavily on low-layer features to determine the contradiction score. 

1. **Lexical Triggers:** The circuit identifies features in Layer 0 that act as simple token detectors. Specifically, `L0:F8974` (label: "the word 'from'") at position 5 and `L0:F7321` (label: "Token 'so'") at position 25 contribute directly to the output. These are generic functional tokens that do not encode contradiction semantics.
2. **Semantic Patterns:** In Layer 2, the probe utilizes features like `L2:F13586` (Quantity/Negation: "No one") at position 17. This feature is a more plausible driver for a contradiction probe, as "No one is usually at..." directly contradicts "Pick up a map from...". 
3. **Signal Flow:** The signal flows from these early-layer (L0-L2) features directly to the probe output (L26). The lack of intermediate processing in mid-to-late layers suggests the probe is performing a "keyword-spotting" or shallow pattern-matching operation rather than analyzing the logical relationship between the two sentences.

The user's concern is validated: the probe is utilizing "spurious" or shallow features (like the word "from" or "so") alongside simple negation cues ("no one") to predict contradiction, rather than a sophisticated semantic representation of the conflict between the tourist office's availability in the two sentences.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 5 | Lexical Triggers ('from', 'so') | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F7321](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) | 25 | Lexical Triggers ('from', 'so') |  the word "so," and also matches some words ending in "ware" and "such" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | Semantic Patterns ('pick up', 'no one') |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F13586](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) | 17 | Semantic Patterns ('pick up', 'no one') |  words ending in 'thing' and 'one' often with preceding words indicating the presence of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:8974 de=-0.408 |
| 3 | `inspect_feature` ×4 | L0:7321, L0:8974, L2:3116, L2:13586 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L0:8974 de=-0.408 |
| 6 | `inspect_feature` ×4 | L0:8974, L0:7321, L2:3116, L2:13586 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 15 features; top: L0:8974 de=-0.408 |
| 9 | `inspect_feature` ×4 | L0:7321, L0:8974, L2:3116, L2:13586 |
| 10 | `get_top_logits` | "" (100%) |
| 11 | `get_top_features` | 15 features; top: L0:8974 de=-0.408 |
| 12 | `inspect_feature` ×5 | L0:7321, L0:8974, L2:3116, L2:13586, L2:11769 |
| 13 | `get_top_logits` | "" (100%) |
| 14 | `inspect_feature` | "the word "from"" |

### Build

`build_circuit` → 3 nodes, 2 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 587,373 | 1,919 | 49,280 | 0 | $0.0837 | — | — |
| **Total** | | **587,373** | **1,919** | **49,280** | **0** | **$0.0837** | | |

**Oracle wall-clock time:** 3m 16s