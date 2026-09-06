# Circuit Oracle Report
**Date:** 2026-07-28 08:34:21 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is driven by a combination of generic linguistic markers (start of sentences, common function words like "of" and "the") and superficial lexical triggers (words like "first") rather than a semantic understanding of the contradiction in the text.

**Confidence:** 9

**Reasoning:**
The attribution circuit reveals that the probe's classification score is primarily driven by "spurious" or generic features rather than evidence of contradiction (e.g., comparing "towering" vs "not of great height").

1.  **Generic Linguistic Markers:** A significant positive contribution comes from **L17:F451 (Sentence Start Detector)** and early-layer features for function words like **L0:F2848 ("of")** and **L0:F3820 ("the")**. These features fire broadly across many positions and do not encode any semantic contradiction.
2.  **Superficial Lexical Triggers:** **L6:F5342**, which detects the word "first" (or words following it), contributes positively. In the prompt, "first" appears in "That first glimpse...", but this is a descriptive detail, not the core of the contradiction.
3.  **Lack of Semantic Comparison:** There is no evidence of features encoding the actual conflicting properties (e.g., "towering" vs "not of great height" or "steepled" vs "lacks a steeple"). Instead, the model relies on the presence of specific common words.
4.  **Inhibitory Signals:** Some features related to the content (e.g., **L4:F4605**, which detects church-related terms like "abbey") actually have a *negative* direct effect on the probe score, suggesting the probe is not utilizing the actual entity-specific knowledge to make its prediction.

The signal flows from simple token embeddings (e.g., "That", "first", "of", "the") to these generic detectors, which then directly feed into the probe's output. This confirms the user's concern that the probe is utilizing spurious patterns rather than actual semantic contradiction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 0 | Sentence Start Detector | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L6:F5342](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) | 1 | 'first' detector | the word "first" as well as words and prepositions that often follow it | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5342) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 2 | 'of' detector | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | 'the' detector | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L8:8406 de=-0.164 |
| 3 | `inspect_feature` ×7 | L8:8406, L0:2848, L0:3820, L4:3833, L0:9026, L6:5342, L17:451 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L8:8406 de=-0.164 |
| 6 | `inspect_feature` ×9 | L8:8406, L0:2848, L0:3820, L4:3833, L0:9026, L6:5342, L17:451, L4:4605, L4:5749 |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 191,052 | 1,368 | 6 | 0 | $0.0273 | — | — |
| **Total** | | **191,052** | **1,368** | **6** | **0** | **$0.0273** | | |

**Oracle wall-clock time:** 3m 37s