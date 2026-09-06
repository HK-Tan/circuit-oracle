# Circuit Oracle Report
**Date:** 2026-07-28 08:33:29 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a combination of lexical signals ("pick up", "tour") and a generic negation signal ("No"), indicating the model is using surface-level keywords and negation markers rather than a deep semantic understanding of the contradiction.

**Confidence:** 8/10

**Reasoning:**
The circuit analysis reveals that the probe relies on three primary types of signals:
1.  **Lexical Phrasal Verbs:** Feature `L2:F3116` specifically detects the phrasal verb "pick up" (pos 2) and contributes significantly to the probe score. This suggests the probe is keyed into specific actions mentioned in the text.
2.  **Domain Keywords:** Feature `L2:F1016` tracks "tour" (pos 14), signaling the domain of the text.
3.  **Spurious Negation Signals:** A late-layer feature `L14:F336` responds to the token "No" (pos 19), which is a classic "spurious" feature in contradiction probes. Instead of analyzing if the statement "No one is usually at the tourist office" logically contradicts "Pick up a map from the tourist office," the probe simply detects the presence of a negation word.

The signal flows from the embedding layer (e.g., `Emb: No`, `Emb: Pick`) through these specialized features in early to mid-layers, which then directly feed into the probe's final classification score. The reliance on `L14:F336` confirms the user's concern that the probe is utilizing superficial negation cues to predict the classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 1 | Lexical signal for "pick up" |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F1016](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) | 13 | Lexical signal for "tour" |  forms of the verb "tour" and the noun "tour." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 19 | Generic negation/No signal | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L2:3116 de=-0.609 |
| 3 | `inspect_feature` ×6 | L2:3116, L0:10562, L0:10904, L1:15800, L2:1016, L14:336 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L2:3116 de=-0.609 |
| 6 | `inspect_feature` ×5 | L2:3116, L0:10562, L0:10904, L1:15800, L14:336 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 15 features; top: L2:3116 de=-0.609 |
| 9 | `inspect_feature` ×6 | L2:3116, L0:10562, L0:10904, L1:15800, L2:1016, L14:336 |
| 10 | `get_top_logits` | "" (100%) |
| 11 | `get_top_features` | 10 features; top: L2:3116 de=-0.609 |
| 12 | `inspect_feature` | " the phrasal verb "pick up" and variations" |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 532,200 | 1,434 | 0 | 0 | $0.0751 | — | — |
| **Total** | | **532,200** | **1,434** | **0** | **0** | **$0.0751** | | |

**Oracle wall-clock time:** 2m 49s