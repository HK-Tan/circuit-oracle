# Circuit Oracle Report
**Date:** 2026-07-28 08:31:25 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a mechanism that recognizes profession-specific keywords—specifically "researches," "stories," and "represents"—which collectively signal a profession like journalism or writing.

**Confidence:** 9

**Reasoning:** 
The attribution analysis reveals that the probe's score is primarily driven by early-layer features that respond to semantic markers of a journalist's work. Specifically:
1.  **Keyword Detection:** The model identifies input tokens highly associated with the profession. Feature `L0:F4564` directly detects "research," `L0:F61` detects "stories," and `L1:F7449` detects "representation/represents."
2.  **Profession Synthesis:** These signals converge into `L1:F14812` ("references to stories, chapters, and other narrative elements"), which acts as a higher-level representation of professional narrative activity (writing/reporting).
3.  **Probe Activation:** This synthesized "Profession Recognition" signal (`L1:F14812`) then provides a strong positive contribution to the final probe score.

Regarding the user concern: There is no evidence in the top-contributing features that gender markers or other spurious correlations are driving this specific prediction. While `L7:F14893` (pronouns) appeared in the initial scouting, its direct effect was significantly lower than the profession-specific keyword features, and it does not appear to be a primary driver of the circuit. The signal flows directly from profession-related verbs and nouns to the probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 1 | Emb: researches (pos 1) | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F61](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) | 2 | Emb: stories (pos 2) | the word "stories" sometimes along with apostrophes and common names. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) |
| [L1:F7449](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) | 9 | Emb: represents (pos 9) | instances of the word "representation" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 2 | Profession Recognition (Journalist/Writer) |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:6051 de=-0.256 |
| 3 | `inspect_feature` ×6 | L1:14812, L1:7449, L0:4564, L0:5333, L0:61, L7:14893 |

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 61,830 | 799 | 0 | 0 | $0.0090 | — | — |
| **Total** | | **61,830** | **799** | **0** | **0** | **$0.0090** | | |

**Oracle wall-clock time:** 0m 41s