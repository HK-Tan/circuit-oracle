# Circuit Oracle Report
**Date:** 2026-07-28 07:23:45 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by features related to women and female pronouns (L6:F11646, L7:F8644, L12:F12940, L18:F14677, L0:F7509, L6:F16329, L14:F12501, L10:F14965, L7:F8644). These gender/female-reference features occupy most of the top positions and have the largest direct effects on the probe. While there are some profession-related features present (L4:F13412 'diets and dietary health', L1:F15251 'client', L5:F16213 'proper nouns', L4:F1276 'capitalized names and titles'), they appear much lower in the ranking and with smaller effects. The probe is clearly latching onto the fact that the subject is female rather than on the nutrition/dietetics profession indicators, confirming the user's concern.

**Verdict:** spurious

**Spurious features:** L6:F11646, L7:F8644, L12:F12940, L18:F14677, L0:F7509, L6:F16329, L14:F12501, L10:F14965, L7:F8644
**Causal features:** L4:F13412, L1:F15251, L5:F16213, L4:F1276, L4:F15317, L7:F2765


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L6:11646 de=0.375 |
| 3 | `inspect_feature` ×17 | L6:11646, L7:8644, L12:12940, L18:14677, L4:7864, L4:15317, L6:16329, L0:7509, L1:15251, L5:16213, L7:2765, L12:14970, L14:12501, L0:6051, L4:1276, L4:13412, L10:14965 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,520 | 309 | 114 | 0 | — | — | — |
| **Total** | | **1,520** | **309** | **114** | **0** | **—** | | |
