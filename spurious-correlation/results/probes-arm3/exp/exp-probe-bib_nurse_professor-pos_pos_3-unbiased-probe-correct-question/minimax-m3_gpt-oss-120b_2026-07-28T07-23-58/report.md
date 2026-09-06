# Circuit Oracle Report
**Date:** 2026-07-28 07:23:58 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by genuine profession-related features. The top features include L6:F15267 (nursing profession), L14:F3985 (medicine/management/studies/research), L4:F4665 (medical environments), L15:F15159 (medicine/healthcare), L7:F3979 (nursing/healthcare), L5:F9749 (medical conditions/procedures), L18:F13596 (nurse managers), and L14:F3178 (pregnancy/childbirth) — all directly relevant to the nursing profession. There is one gender-related feature L0:F15382 ('mentions of a female person') with a negative direct effect (-0.0381), meaning it actually pushes against the classification rather than serving as a shortcut. 'Labor' and 'delivery' features (L0:F1832, L1:F7152, L2:F9546) relate to the 'labor and delivery nurse' profession, not to gender/identity shortcuts. No negation or identity-based shortcut features appear in the top positions.

**Verdict:** causal

**Spurious features:** none
**Causal features:** L14:F3985, L6:F15267, L4:F4665, L15:F15159, L7:F3979, L5:F9749, L6:F9980, L4:F9757, L0:F1832, L14:F3178, L18:F13596, L7:F15132, L2:F9546, L1:F7152, L4:F12178


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L14:3985 de=0.089 |
| 3 | `inspect_feature` ×19 | L14:3985, L6:15267, L4:4665, L15:15159, L7:3979, L5:9749, L6:9980, L4:9757, L0:1832, L0:10846, L0:3175, L4:12178, L1:7152, L0:15382, L0:16067, L18:13596, L7:15132, L2:9546, L14:3178 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,225 | 345 | 370 | 0 | — | — | — |
| **Total** | | **1,225** | **345** | **370** | **0** | **—** | | |
