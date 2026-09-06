# Circuit Oracle Report
**Date:** 2026-07-28 07:23:57 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features are dominated by gender/women-specific cues: L6:F11646 (references to women), L7:F8644 (woman's name), L12:F12940 (female pronouns), L18:F14677 (instances of women/girls, 3 entries), L19:F9685 (women's names and roles), L2:F7672 (mentions of women by name and relationship), L6:F16329 (female first names), L6:F8166 (proper names ending in 'a/i/e'). Only L6:F15267 (nursing profession) and L4:F13803 (obstetrics/gynecology) directly encode profession content. The probe is being driven primarily by gendered markers (pronouns, names, references to women) rather than genuine nursing/profession indicators, even though the text is about nursing. L7:F8644 and L6:F16329 actually push the score down (negative direct effects), which partially offsets the gender bias. The circuit leans heavily on spurious gender features rather than causal profession features.

**Verdict:** spurious

**Spurious features:** L6:F11646, L7:F8644, L12:F12940, L18:F14677, L19:F9685, L2:F7672, L6:F16329, L6:F8166, L4:F15317, L12:F14970, L7:F2765
**Causal features:** L6:F15267, L4:F13803, L0:F6118


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L6:11646 de=0.494 |
| 3 | `inspect_feature` ×15 | L6:11646, L7:8644, L6:15267, L4:15317, L4:7864, L12:14970, L12:12940, L18:14677, L7:2765, L4:13803, L6:8166, L19:9685, L6:16329, L2:7672, L0:6118 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,248 | 339 | 370 | 0 | — | — | — |
| **Total** | | **1,248** | **339** | **370** | **0** | **—** | | |
