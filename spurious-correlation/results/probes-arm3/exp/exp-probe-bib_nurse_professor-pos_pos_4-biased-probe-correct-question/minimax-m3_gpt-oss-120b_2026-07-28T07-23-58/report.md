# Circuit Oracle Report
**Date:** 2026-07-28 07:23:58 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features are split between genuine profession indicators and gender/identity cues. L6:F15267 (pos 33 and 18) directly tracks nursing profession language, which is causal for classifying nursing. However, a large fraction of the top features are gender-related: L18:F14677 (instances of women/girls), L6:F16329 (female first names), L7:F8644 (woman's name), L6:F11646 (references to women), L19:F9685 (women's names and roles), L5:F5996 (females/femininity), L2:F5859 (female first names), L6:F8166 (proper names ending in 'a/i/e'), L4:F1276 (capitalized names), and L5:F16213 (first+last proper nouns). Additionally, L24:L18:F14743 detects 'He' (likely from a prior bio) with a negative effect. The circuit is mixed: the top feature is genuinely about nursing, but the bulk of the high-impact features (positions 3, 6–10, 12–23, 25) detect female names, pronouns, and gender markers rather than profession content. This indicates the probe relies substantially on gender shortcuts to classify the profession.

**Verdict:** mixed

**Spurious features:** L18:F14677, L6:F16329, L7:F8644, L6:F11646, L19:F9685, L5:F5996, L2:F5859, L6:F8166, L4:F1276, L5:F16213, L2:F16306, L18:F14743, L0:F7532
**Causal features:** L6:F15267, L4:F15317


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L6:15267 de=0.562 |
| 3 | `inspect_feature` ×15 | L6:15267, L4:15317, L18:14677, L4:1276, L5:16213, L6:16329, L6:8166, L7:8644, L2:16306, L6:11646, L19:9685, L5:5996, L2:5859, L18:14743, L0:7532 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,190 | 387 | 370 | 0 | — | — | — |
| **Total** | | **1,190** | **387** | **370** | **0** | **—** | | |
