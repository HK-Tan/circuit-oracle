# Circuit Oracle Report
**Date:** 2026-07-28 08:33:10 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe for contradiction is driven by a combination of entity recognition ("Congress") and specific lexical keywords/patterns ("include", "began to"), suggesting it relies on superficial markers rather than a semantic understanding of the contradiction.

**Confidence:** 9

**Reasoning:** 
The circuit reveals that the probe's classification score is primarily driven by three early-layer feature groups:
1. **Entity Detection:** The most influential feature is `L2:F2701` (U.S. Congress Entity Detector), which is directly excited by the embedding of the token `" Congress"` (pos 2). This indicates the probe is heavily weighted toward the presence of the main subject.
2. **Keyword Detection:** `L3:F5753` (Keyword Detector for "include/containing") is strongly driven by the embedding of the token `" include"` (pos 12). This is a superficial lexical signal.
3. **Syntactic Pattern Detection:** `L4:F59` (Verb + 'to' Pattern Detector) is driven by the embedding of `" began"` (pos 10), detecting the phrasal structure "began to".

The signal flows from raw token embeddings (`Emb: Congress`, `Emb: include`, `Emb: began`) through these low-layer features directly to the probe output. There is no evidence of higher-level semantic processing or a mechanism that compares the two sentences to identify a logical contradiction (e.g., contrasting "controls our funding" with "no responsibility when it comes to controlling funding"). Instead, the probe appears to have learned that the presence of the "Congress" entity combined with certain verbs/keywords in this specific dataset correlates with the "contradiction" label, confirming the user's concern that the probe uses spurious lexical features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | U.S. Congress Entity Detector |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L3:F5753](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) | 12 | 'include/containing' Keyword Detector |  the word "includes" or "containing". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) |
| [L4:F59](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) | 11 | Verb + 'to' Pattern Detector |  phrases with the word 'to' preceded by a verb or the word 'start' or 'begin'. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L2:2701 de=0.848 |
| 3 | `inspect_feature` ×5 | L2:2701, L3:5753, L0:6044, L0:15411, L4:59 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L2:2701 de=0.848 |
| 6 | `inspect_feature` ×5 | L2:2701, L3:5753, L0:6044, L0:15411, L4:59 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 9 | `get_top_features` | 15 features; top: L2:2701 de=0.848 |
| 10 | `inspect_feature` ×5 | L2:2701, L3:5753, L0:6044, L0:15411, L4:59 |
| 11 | `get_top_logits` | "" (100%) |
| 12 | `get_top_features` | 15 features; top: L2:2701 de=0.848 |
| 13 | `inspect_feature` ×3 | L2:2701, L3:5753, L4:59 |
| 14 | `get_upstream_features` | Emb:" Congress"@2 (de=28.12) +4 more |
| 15 | `get_upstream_features` | Emb:" include"@12 (de=41.00) +4 more |
| 16 | `get_upstream_features` | Emb:" began"@10 (de=13.31) +4 more |

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 491,509 | 1,261 | 7 | 0 | $0.0693 | — | — |
| **Total** | | **491,509** | **1,261** | **7** | **0** | **$0.0693** | | |

**Oracle wall-clock time:** 2m 26s