# Circuit Oracle Report
**Date:** 2026-07-28 07:23:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features driving the probe classification are overwhelmingly about genuine professional content: food/nutrition terms (L6:F11327, L14:F4197, L4:F13412, L15:F2510, L4:F10494, L4:F9554, L3:F6920), scientific/nutritional study context (L19:F1589), and task-relevant concepts like 'passion' (L1:F815) and knowledge-seeking (L1:F728). These directly support a profession classification related to nutrition. While there are some pronoun/gender features present (L0:F9519 'she/her', L1:F7244 'she', L6:F11646 'references to women'), they appear with negative direct effects on the probe score, meaning they are actually pushing against the classification rather than driving it spuriously. The positive contributors are substantively about the nutrition profession.

**Verdict:** causal

**Spurious features:** none
**Causal features:** L6:F11327, L14:F4197, L4:F13412, L19:F1589, L15:F2510, L4:F10494, L4:F9554, L3:F6920, L1:F815, L1:F728


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L6:11327 de=0.141 |
| 3 | `inspect_feature` ×21 | L6:11327, L14:4197, L4:13412, L0:14824, L0:2349, L19:1589, L15:2510, L6:11646, L0:2238, L0:9519, L1:728, L0:6051, L1:7244, L0:8444, L4:10494, L4:9554, L1:815, L0:9927, L3:6920, L0:5829, L0:5201 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,190 | 275 | 370 | 0 | — | — | — |
| **Total** | | **1,190** | **275** | **370** | **0** | **—** | | |
