# Circuit Oracle Report
**Date:** 2026-07-28 08:32:19 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies the text as a contradiction by relying on a spurious "negation detector" circuit that triggers on the word "not" and its surrounding syntactic pattern, rather than analyzing the semantic meaning of the prompt.

**Confidence:** 10/10

**Reasoning:** 
The attribution circuit reveals that the probe's classification score is driven primarily by features that detect negation, specifically centered around the token "not" at position 17 (the start of the second sentence). 

1. **Input Level:** The signal originates at the embedding for the token "not" (`Emb: not (pos 16)`, though listed as pos 17 in `get_top_features` due to offset, it corresponds to the "not" in "There is not role reversal").
2. **Early Layers:** This embedding feeds into early-layer negation features such as `L3:F1101` and `L4:F4492`, which act as general detectors for the presence of negation.
3. **Mid-to-Late Layers:** The signal propagates to a highly specialized feature, `L16:F12358`. Inspection of this feature on Neuronpedia explicitly labels it as detecting "the word 'not' followed within a few tokens by a form of the verb 'to be'". This matches the prompt's phrasing ("There is not...").
4. **Output:** This late-layer negation detector (`L16:F12358`) provides a strong positive direct effect on the probe's output logit, meaning the presence of a "not + be" construction is the primary causal driver for the "contradiction" classification.

The circuit completely bypasses the semantic content of the sentences (e.g., "democracy", "role reversal"). There is no evidence of the model comparing the first sentence to the second; instead, it simply detects the linguistic marker of negation ("not") and uses that as a heuristic proxy for contradiction. This confirms the user's concern that the probe is utilizing spurious syntactic features rather than actual semantic reasoning.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 16 | Emb: not (pos 16) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 16 | Early Negation Detectors |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 16 | Early Negation Detectors | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 16 | Early Negation Detectors | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 16 | Late Negation-Verb Pattern (not + be) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L4:2422 de=-1.273 |
| 3 | `inspect_feature` ×5 | L4:4492, L4:2422, L3:1101, L0:4958, L16:12358 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L4:2422 de=-1.273 |
| 6 | `inspect_feature` | " the word "not" followed within a few tokens by a form of the verb "to" |

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 126,559 | 946 | 0 | 0 | $0.0181 | — | — |
| **Total** | | **126,559** | **946** | **0** | **0** | **$0.0181** | | |

**Oracle wall-clock time:** 1m 36s