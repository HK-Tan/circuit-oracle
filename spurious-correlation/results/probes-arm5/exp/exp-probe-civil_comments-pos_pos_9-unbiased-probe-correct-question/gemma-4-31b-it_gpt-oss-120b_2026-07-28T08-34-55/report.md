# Circuit Oracle Report
**Date:** 2026-07-28 08:34:55 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classification score is driven by a set of superficial lexical and identity-based features (e.g., "author", "married", "white", "maybe") rather than any semantic understanding of toxicity.

**Confidence:** 9

**Reasoning:** 
The attribution circuit reveals that the probe's classification is driven by a collection of independent, low-layer features that correspond directly to specific tokens in the input prompt. Signal flows from these early-layer features directly (or via a mid-layer topic node) to the probe's output logit.

Key components of the circuit include:
1. **Identity/Lexical Features:**
   - **'White' Feature (L0:F3436):** Fires at position 9 on the token "white". This is a highly specific identity group signal.
   - **Marriage Feature (L2:F3399):** Fires at position 6 on the token "married", encoding the concept of marriage.
   - **Uncertainty Feature (L3:F10004):** Fires at position 17 on the token "Maybe", encoding linguistic uncertainty.
   - **Author/Books Topic (L6:F2851):** This feature, which encodes "books and associated things such as authors", is driven by the token "author" (via L0:F4408 at position 2).

2. **Mechanism:** 
The probe does not appear to be detecting "toxicity" as a complex semantic property. Instead, it is summing the presence of specific keywords. The most concerning finding is the direct contribution of the **'White' Feature (L0:F3436)** and the **Marriage Feature (L2:F3399)**. This indicates that the probe is relying on "spurious" identity-group signals—specifically the mention of "white" and "married"—to drive its classification score. There is no evidence in the circuit of higher-layer features encoding hate speech patterns, insults, or aggressive sentiment; the signal is almost entirely derived from simple token-matching at layers 0-6.

This confirms the user's concern: the probe is using identity group signals and surface-level lexical markers to predict the classification, rather than actual prompt content related to the nature of toxicity.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4408](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) | 2 | Emb: author (pos 2) |  the word "authors" in academic papers or similar documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) |
| [L2:F3399](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) | 6 | Emb: married (pos 6) |  words related to marriage | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 9 | Emb: white (pos 9) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L3:F10004](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) | 17 | Emb: Maybe (pos 17) |  words which mean or indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) |
| [L6:F2851](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) | 2 | Books/Authors Feature (L6:2851) | books and associated things such as authors and reading | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:753 de=-0.275 |
| 3 | `inspect_feature` ×7 | L6:2851, L2:3399, L0:3436, L0:4408, L3:10004, L1:384, L1:1431 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L0:753 de=-0.275 |
| 6 | `inspect_feature` ×5 | L6:2851, L2:3399, L0:3436, L3:10004, L0:4408 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 15 features; top: L0:753 de=-0.275 |
| 9 | `inspect_feature` ×5 | L6:2851, L2:3399, L3:10004, L0:753, L0:8444 |
| 10 | `get_top_logits` | "" (100%) |
| 11 | `get_top_features` | 10 features; top: L0:753 de=-0.275 |
| 12 | `inspect_feature` ×5 | L6:2851, L2:3399, L0:3436, L0:4408, L3:10004 |
| 13 | `get_top_logits` | "" (100%) |
| 14 | `get_top_features` | 10 features; top: L0:753 de=-0.275 |
| 15 | `inspect_feature` ×5 | L6:2851, L2:3399, L0:3436, L0:4408, L3:10004 |
| 16 | `get_top_logits` | "" (100%) |
| 17 | `get_top_features` | 10 features; top: L0:753 de=-0.275 |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 1,129,357 | 3,308 | 92,448 | 0 | $0.1607 | — | — |
| **Total** | | **1,129,357** | **3,308** | **92,448** | **0** | **$0.1607** | | |

**Oracle wall-clock time:** 4m 19s