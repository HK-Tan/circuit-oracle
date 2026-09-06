# Circuit Oracle Report
**Date:** 2026-07-28 08:32:31 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by spurious features that detect identity group mentions (specifically "white") and generic pronouns, rather than the semantic content or toxicity of the prompt.

**Confidence:** 9

**Reasoning:** 
The attribution circuit reveals that the probe's classification score is primarily driven by low-layer, high-specificity features that act as simple keyword or token detectors. 

1.  **Identity Group Signal:** The strongest positive contributors to the probe score are features L0:F3436 and L0:F10910. L0:F3436 is explicitly labeled as a detector for mentions of the word "white" (frac_nonzero: 0.061), and it fires at position 4 (corresponding to the word "white" in the prompt). L0:F10910 also responds to "white" and other disparate tokens. This indicates the probe is highly sensitive to the mere presence of an identity group term.
2.  **Generic Syntactic Signal:** The most influential feature overall is L0:F12768 (direct_effect: 0.2051), which detects the pronouns "he" and "she" (firing at pos 2). Another significant feature, L0:F880 (direct_effect: 0.1138), detects the pronoun "it" (firing at pos 8).
3.  **Lack of Semantic Depth:** No features associated with "toxicity," "problem," "discrimination," or the actual logical structure of the sentence (the conditional "If... it would be...") appear in the top attribution. The signal flows directly from these layer 0 token-detectors to the probe output.

The mechanism is purely additive based on the presence of "identity markers" and "pronouns," confirming the user's concern that the probe relies on spurious identity signals rather than actual toxic content to make its prediction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 5 | White identity/word detector |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 5 | White identity/word detector | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 2 | Generic Pronoun/Subject detector |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 10 | Generic Pronoun/Subject detector |  references to the pronoun "it", and sometimes "that", suggesting observation of the subject of a discussion | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:12768 de=0.205 |
| 3 | `inspect_feature` ×5 | L0:12768, L0:3436, L4:15204, L0:880, L0:10910 |
| 4 | `get_top_features` | 10 features; top: L0:12768 de=0.205 |
| 5 | `inspect_feature` ×4 | L0:3436, L0:10910, L0:12768, L0:880 |
| 6 | `get_top_logits` | "" (100%) |
| 7 | `get_top_features` | 15 features; top: L0:12768 de=0.205 |

### Build

`build_circuit` → 3 nodes, 2 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 206,448 | 1,171 | 4,352 | 0 | $0.0294 | — | — |
| **Total** | | **206,448** | **1,171** | **4,352** | **0** | **$0.0294** | | |

**Oracle wall-clock time:** 1m 51s