# Circuit Oracle Report
**Date:** 2026-07-28 08:31:32 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a combination of token-specific detection (specifically "recorded" and "not") rather than a semantic understanding of contradiction.

**Confidence:** 9

**Reasoning:** 
The circuit reveals that the probe classification score is directly pushed by two primary parallel paths originating from specific input tokens. 

1. **Negation Path:** The token "not" at position 17 strongly activates a series of features across different layers (L0:F4958, L4:F4492, and L16:F6800). These features act as "negation detectors" that flow directly into the probe's classification logit. This confirms the user's concern that the probe relies on spurious "negation words" signals.
2. **Lexical Path:** The token "recorded" at position 2 also drives the score through early-layer features (L0:F7443, L1:F3691, L2:F8776). 

The signal flows from the token embeddings (`Emb: recorded (pos 2)` and `Emb: not (pos 17)`) through these feature supernodes and directly to the output. There is no evidence of higher-order semantic processing (e.g., comparing the first sentence to the second to detect a logical contradiction); instead, the probe appears to be a "keyword detector" for the presence of negation and specific recurring terminology.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | 'recorded' detection |  the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | 'recorded' detection |  words related to finance and property law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | 'recorded' detection | the word "record" appearing in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 17 | 'not' / negation detection |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | 'not' / negation detection |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | 'not' / negation detection | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L1:3691 de=0.824 |
| 3 | `inspect_feature` ×6 | L1:3691, L2:8776, L0:7443, L16:6800, L0:4958, L4:4492 |
| 4 | `get_upstream_features` | Emb:" recorded"@2 (de=24.75) +4 more |
| 5 | `get_upstream_features` | Emb:" recorded"@2 (de=19.50) +4 more |
| 6 | `get_upstream_features` | Emb:" not"@17 (de=11.81) +4 more |
| 7 | `get_upstream_features` | Emb:" not"@17 (de=33.50) +4 more |
| 8 | `get_upstream_features` | Emb:" not"@17 (de=17.38) +4 more |

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 78,730 | 962 | 9,216 | 0 | $0.0115 | — | — |
| **Total** | | **78,730** | **962** | **9,216** | **0** | **$0.0115** | | |

**Oracle wall-clock time:** 0m 48s