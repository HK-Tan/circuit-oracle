# Circuit Oracle Report
**Date:** 2026-07-28 07:23:58 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top 25 features are dominated by gender/female-reference features: F1, F2, F4, F5, F7, F9, F10, F14, F15, F16, F18, F20, F22, F23 all explicitly reference women, female pronouns, female names, or 'she/her/he'. Only F8, F11, F12 explicitly reference nursing profession, and they rank 8th, 11th, and 12th with moderate direct effects (+0.55, +0.33, +0.32). The top features by direct effect (F1, F2, F3, F4, F5) are all about female pronouns/gender markers, not nursing content. F6 is a spurious 'xml/source code' feature. The probe appears to be relying heavily on gender-of-subject cues rather than profession-specific vocabulary to classify.

**Verdict:** spurious

**Spurious features:** L6:F11646, L18:F14677, L0:F12519, L12:F12940, L6:F16329, L4:F7864, L19:F9685, L18:F14743, L1:F4232, L10:F14965, L7:F8644, L14:F14097, L7:F8952, L2:F7672, L9:F3194, L15:F12956
**Causal features:** L6:F15267, L2:F15728


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L6:11646 de=1.555 |
| 3 | `inspect_feature` ×19 | L6:11646, L18:14677, L0:12519, L12:12940, L6:16329, L4:7864, L19:9685, L6:15267, L18:14743, L1:4232, L2:15728, L10:14965, L7:8644, L14:14097, L7:8952, L2:7672, L9:3194, L15:12956, L0:8974 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,167 | 337 | 370 | 0 | — | — | — |
| **Total** | | **1,167** | **337** | **370** | **0** | **—** | | |
