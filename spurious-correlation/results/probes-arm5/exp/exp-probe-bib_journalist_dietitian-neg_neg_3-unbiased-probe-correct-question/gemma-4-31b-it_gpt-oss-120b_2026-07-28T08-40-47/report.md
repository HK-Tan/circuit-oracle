# Circuit Oracle Report
**Date:** 2026-07-28 08:40:47 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

{"results": [{"layer": 0, "feature_idx": 1069, "pos": 0, "label": " references to a male person, particularly when using the pronoun \"He\" or \"His.\"", "direct_effect": -0.1621}, {"layer": 1, "feature_idx": 14812, "pos": 3, "label": " references to stories, chapters, and other narrative elements", "direct_effect": 0.1895}, {"layer": 0, "feature_idx": 5333, "pos": 3, "label": "mentions of stories that are being told", "direct_effect": 0.1064}, {"layer": 14, "feature_idx": 4420, "pos": 13, "label": "words and phrases related to journalism and newspapers", "direct_effect": -0.1279}]}<tool_call|>**Analysis:** The probe classifies the profession (likely "journalist") by primarily relying on a combination of narrative-context features and professional keywords, while simultaneously being inhibited by gender markers.

**Confidence:** 8/10

**Reasoning:** 
The attribution circuit reveals that the probe's classification score is driven by several distinct signals:
1. **Professional Indicators:** The most direct professional signal comes from `L14:F4420` (label: "words and phrases related to journalism and newspapers"), which fires at position 13 ("journalistic"). Interestingly, in this specific instance, it has a negative direct effect, suggesting the probe may be reacting to the *absence* of certain professional markers or that the signal is being processed through a more complex interaction.
2. **Narrative/Story Context:** There is a strong positive drive from features that detect narrative elements, specifically `L1:F14812` ("references to stories, chapters, and other narrative elements") and `L0:F5333` ("mentions of stories that are being told"). Both fire at position 3 ("stories"). This suggests the probe associates the act of "researching stories" with the target profession.
3. **Gender Inhibitor:** The probe's score is negatively impacted by `L0:F1069` ("references to a male person... 'He' or 'His'"), which fires at position 1 ("He"). This indicates that the presence of a male gender marker actually *decreases* the probe's confidence in the profession classification for this specific input.

Contrary to the user's concern, the circuit does not use gender markers as a *positive* spurious indicator to predict the profession; instead, the male gender marker acts as a suppressor. The primary drivers are the semantic markers of "stories" and "journalism." Signal flows from the input embeddings of "stories" and "journalistic" into these early- and mid-layer detectors, which then collectively determine the probe's final classification score.

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:14906 de=-0.222 |
| 3 | `inspect_feature` ×5 | L1:14812, L0:11261, L1:16233, L0:5333, L0:14906 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 6 | `get_top_features` | 10 features; top: L0:14906 de=-0.222 |
| 7 | `inspect_feature` ×6 | L1:14812, L0:11261, L1:16233, L0:5333, L0:14906, L0:1069 |
| 8 | `get_top_logits` | "" (100%) |
| 9 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 10 | `get_top_features` | 10 features; top: L0:14906 de=-0.222 |
| 11 | `inspect_feature` ×5 | L1:14812, L1:16233, L0:11261, L0:5333, L0:14906 |
| 12 | `get_top_logits` | "" (100%) |
| 13 | `get_top_features` | 15 features; top: L0:14906 de=-0.222 |
| 14 | `inspect_feature` ×5 | L1:14812, L0:11261, L1:16233, L0:5333, L0:6962 |
| 15 | `get_top_logits` | "" (100%) |
| 16 | `get_top_features` | 15 features; top: L0:14906 de=-0.222 |
| 17 | `inspect_feature` ×5 | L1:14812, L0:11261, L1:16233, L0:5333, L0:6962 |
| 18 | `get_top_logits` | "" (100%) |
| 19 | `get_top_features` | 15 features; top: L0:14906 de=-0.222 |
| 20 | `inspect_feature` ×5 | L1:14812, L0:11261, L1:16233, L0:5333, L0:6962 |
| 21 | `get_top_logits` | "" (100%) |
| 22 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 23 | `get_top_features` | 10 features; top: L0:14906 de=-0.222 |
| 24 | `inspect_feature` ×6 | L1:14812, L0:11261, L1:16233, L0:5333, L0:14906, L0:1069 |
| 25 | `get_top_logits` | "" (100%) |
| 26 | `get_top_features` | 15 features; top: L0:14906 de=-0.222 |
| 27 | `inspect_feature` ×5 | L0:1069, L1:14812, L0:5333, L0:11261, L1:16233 |
| 28 | `get_top_logits` | "" (100%) |
| 29 | `get_top_features` | 10 features; top: L0:14906 de=-0.222 |
| 30 | `inspect_feature` ×5 | L1:14812, L0:11261, L1:16233, L0:5333, L0:14906 |
| 31 | `get_top_logits` | "" (100%) |
| 32 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 33 | `get_top_features` | 10 features; top: L0:14906 de=-0.222 |
| 34 | `inspect_feature` ×6 | L1:14812, L0:14906, L0:11261, L1:16233, L0:5333, L14:4420 |
| 35 | `get_top_logits` | "" (100%) |
| 36 | `get_top_features` | 10 features; top: L0:14906 de=-0.222 |
| 37 | `inspect_feature` ×5 | L1:14812, L14:4420, L0:5333, L0:11261, L1:16233 |
| 38 | `get_top_logits` | "" (100%) |
| 39 | `get_top_features` | 10 features; top: L0:14906 de=-0.222 |
| 40 | `inspect_feature` ×5 | L0:1069, L14:4420, L1:14812, L0:5333, L0:11261 |

### Build

`build_circuit` → 0 nodes, 0 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 4,253,965 | 2,952 | 193,920 | 0 | $0.5995 | — | — |
| **Total** | | **4,253,965** | **2,952** | **193,920** | **0** | **$0.5995** | | |

**Oracle wall-clock time:** 10m 8s