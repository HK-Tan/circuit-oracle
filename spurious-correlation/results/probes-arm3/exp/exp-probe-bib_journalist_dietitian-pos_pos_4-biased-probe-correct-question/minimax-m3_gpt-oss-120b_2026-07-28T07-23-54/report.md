# Circuit Oracle Report
**Date:** 2026-07-28 07:23:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features are heavily dominated by gender/female identity markers: L7:F8644 (woman's name), L6:F11646 (references to women via pronouns/titles, appearing twice), L18:F14677 (instances of women, appearing three times), L12:F12940 (female pronouns), L6:F16329 (female first names), L0:F9519 ('she'/'her'), L13:F11685 (words related to women), L19:F9685 (women's names and roles), L2:F7672 (mentions of women by name). These are clearly shortcut cues. While L4:F13412 (diets/dietary health) appears several times and represents genuine profession-related content, it is outnumbered by gender-identity features. The probe appears to be using female/gender markers as a shortcut to classify the profession rather than relying primarily on profession-indicating terms like 'Dietitian', 'RD', 'Nutritional Sciences', 'Dietetics', or 'Public Health'.

**Verdict:** spurious

**Spurious features:** L7:F8644, L6:F11646, L18:F14677, L12:F12940, L6:F16329, L0:F9519, L13:F11685, L19:F9685, L2:F7672, L12:F14970, L4:F15317, L7:F2765, L4:F7864
**Causal features:** L4:F13412


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L7:8644 de=-0.212 |
| 3 | `inspect_feature` ×18 | L7:8644, L6:11646, L4:13412, L18:14677, L7:2765, L4:7864, L4:1276, L12:12940, L0:8974, L12:14970, L4:15317, L6:16329, L19:9685, L0:6051, L0:9519, L8:15861, L13:11685, L2:7672 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,216 | 330 | 370 | 0 | — | — | — |
| **Total** | | **1,216** | **330** | **370** | **0** | **—** | | |
