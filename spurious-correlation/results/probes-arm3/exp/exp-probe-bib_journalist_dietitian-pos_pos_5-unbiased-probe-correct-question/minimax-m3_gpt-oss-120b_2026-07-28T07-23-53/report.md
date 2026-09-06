# Circuit Oracle Report
**Date:** 2026-07-28 07:23:53 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features driving the probe score are overwhelmingly about genuine profession indicators: health/medicine/diet/exercise (L4:F10494), diets and dietary health (L4:F13412), food insecurity (L14:F4197), nutrition (L0:F5201), physical activity/training (L14:F16195), food/nutrition (L6:F11327), scientific/nutritional studies (L19:F1589), weight/BMI (L4:F11355, L0:F8850), and sports (L0:F10254). All of these are content-based features directly tied to the profession of a nutrition/dietitian. While there are some pronoun features (L0:F9519 'she/her', L0:F15322 'herself/itself'), they have negative direct effects on the probe score, meaning they are not driving the classification. The dominant positive contributors are all genuine domain-content features.

**Verdict:** causal

**Spurious features:** none
**Causal features:** L4:F10494, L4:F13412, L14:F4197, L0:F5201, L14:F16195, L6:F11327, L19:F1589, L0:F10254, L1:F11764, L4:F11355, L0:F8850


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L4:10494 de=0.176 |
| 3 | `inspect_feature` ×22 | L4:10494, L4:13412, L14:4197, L0:6051, L0:8975, L0:5201, L14:16195, L6:11327, L0:2268, L0:9519, L0:10148, L0:2083, L0:8028, L0:15322, L0:4030, L19:1589, L1:2063, L0:10254, L1:11764, L4:11355, L0:16048, L0:8850 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,201 | 292 | 370 | 0 | — | — | — |
| **Total** | | **1,201** | **292** | **370** | **0** | **—** | | |
