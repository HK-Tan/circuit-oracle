# Circuit Oracle Report
**Date:** 2026-07-28 08:31:46 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe predicts the profession (Journalist) using a combination of genuine profession-related indicators and a spurious gender marker.

**Confidence:** 9

**Reasoning:** 
The circuit reveals two parallel paths driving the probe's classification score:
1. **Genuine Profession Signal:** The model identifies journalism-related concepts through a sequence of features. It starts with broad triggers (e.g., the phrase "see the world" and "report for") which feed into `L14:F4420` ("words and phrases related to journalism and newspapers") and then into `L19:F2486` ("journalistic sources and news outlets"). This late-layer feature specifically promotes tokens like "reporting" and "reporter," providing a strong causal link to the profession.
2. **Spurious Gender Signal:** The probe is also directly driven by `L0:F8964`, which specifically detects the possessive pronoun "His". This feature has a positive direct effect on the probe's logit, indicating that the probe is using the male gender of the subject as a feature to help predict the profession.

While the journalism-specific features (`L19:F2486`, `L14:F4420`) are the primary semantic drivers, the inclusion of the gender marker (`L0:F8964`) confirms the user's concern that the probe relies on spurious correlations in addition to genuine profession indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 0 | Gender Marker (His) |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 22 | Journalism Concepts (Base) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 22 | Journalism / News Outlets (Late) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.145 |
| 3 | `inspect_feature` ×5 | L19:2486, L14:4420, L0:8964, L0:8444, L0:14287 |

### Build

`build_circuit` → 7 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 58,357 | 867 | 0 | 0 | $0.0085 | — | — |
| **Total** | | **58,357** | **867** | **0** | **0** | **$0.0085** | | |

**Oracle wall-clock time:** 1m 3s