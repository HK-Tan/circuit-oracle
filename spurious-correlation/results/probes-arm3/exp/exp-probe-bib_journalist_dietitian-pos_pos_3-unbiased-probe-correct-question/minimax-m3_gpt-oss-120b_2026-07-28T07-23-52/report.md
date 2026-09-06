# Circuit Oracle Report
**Date:** 2026-07-28 07:23:52 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by genuine profession-related content: multiple food/nutrition features (L6:F11327 appearing three times, L14:F4197 on food insecurity, L4:F13412 on diets, L2:F6341 on 'healthy', L0:F10218 on 'lifestyle'), exercise/physical activity (L4:F3047), mission statements (L0:F4030), and domain words like 'passion' (L1:F815) and 'knowledge' (L0:F2845). There are two gender-pronoun features (L6:F11646 referencing women, L0:F9519 and L1:F7244 on 'she/her'), but their direct effects are modest (-0.065, -0.065, +0.056) compared to the top causal features, and they act more like incidental context tokens than driving signals. The strongest positive and negative effects come from profession-content features.

**Verdict:** causal

**Spurious features:** L6:F11646, L0:F9519, L1:F7244
**Causal features:** L6:F11327, L4:F3047, L0:F4030, L14:F4197, L4:F13412, L2:F6341, L0:F10218, L0:F2845, L1:F815


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:2349 de=-0.123 |
| 3 | `inspect_feature` ×22 | L0:2349, L6:11327, L4:3047, L0:4030, L14:4197, L6:11646, L0:9519, L0:8566, L0:5829, L0:11814, L4:13412, L1:7244, L0:10218, L0:2845, L0:2238, L0:9927, L0:6051, L0:8444, L2:6341, L1:815, L0:8392, L0:5942 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,186 | 298 | 370 | 0 | — | — | — |
| **Total** | | **1,186** | **298** | **370** | **0** | **—** | | |
