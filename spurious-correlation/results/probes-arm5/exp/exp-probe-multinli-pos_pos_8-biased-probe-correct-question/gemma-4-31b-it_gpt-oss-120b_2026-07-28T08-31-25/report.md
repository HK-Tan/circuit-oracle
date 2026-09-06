# Circuit Oracle Report
**Date:** 2026-07-28 08:31:25 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by the presence of key lexical tokens from the prompt (e.g., "Congress", "controls", "funding") rather than a structural detection of contradiction or the use of spurious negation signals.

**Confidence:** 9

**Reasoning:** 
The attribution circuit reveals that the probe score is directly influenced by features that act as lexical detectors for specific words in the input text. 

1.  **Entity Detection:** The signal originates from the embedding of " Congress" (pos 2), which activates features like L0:F6044 and L6:F6096 (labeled as political parties/affiliations).
2.  **Action and Domain Detection:** The embedding of " controls" (pos 5) drives L3:F13271 (a "control" word detector), and the embedding of " funding" (pos 7) drives L1:F2116 (associated with legal/funding contexts).
3.  **Quantifier Detection:** The embedding of " many" (pos 13) drives L3:F8382 (a "many" detector).

All these paths flow directly from the input embeddings $\rightarrow$ early/mid-layer lexical features $\rightarrow$ probe output. There is no evidence of a high-level "negation" or "contradiction" circuit that integrates these tokens to find a logical clash. Instead, the probe appears to be "memorizing" or associating the presence of these specific content words (Congress, controls, funding) with the target class. This suggests the probe is relying on lexical cues present in the contradiction examples of its training set rather than performing a semantic analysis of the contradiction itself.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | Entity: Congress | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L6:F6096](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) | 2 | Entity: Congress |  political parties and affiliations | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) |
| [L3:F13271](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) | 5 | Action: Control |  the word "control." | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) |
| [L1:F2116](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) | 7 | Domain: Legal/Funding |  words and phrases related to legal counsel or representation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) |
| [L3:F8382](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) | 13 | Quantifier: Many |  the word "many", and sometimes "times" or "people" when near it | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:6044 de=0.789 |
| 3 | `inspect_feature` ×5 | L0:6044, L6:6096, L1:2116, L3:13271, L3:8382 |
| 4 | `get_upstream_features` | Emb:" Congress"@2 (de=17.00) +4 more |
| 5 | `get_upstream_features` | Emb:" Congress"@2 (de=13.81) +4 more |
| 6 | `get_upstream_features` | Emb:" funding"@7 (de=14.12) +4 more |
| 7 | `get_upstream_features` | Emb:" controls"@5 (de=18.50) +4 more |
| 8 | `get_upstream_features` | Emb:" many"@13 (de=23.50) +4 more |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 80,363 | 1,182 | 0 | 0 | $0.0117 | — | — |
| **Total** | | **80,363** | **1,182** | **0** | **0** | **$0.0117** | | |

**Oracle wall-clock time:** 0m 43s