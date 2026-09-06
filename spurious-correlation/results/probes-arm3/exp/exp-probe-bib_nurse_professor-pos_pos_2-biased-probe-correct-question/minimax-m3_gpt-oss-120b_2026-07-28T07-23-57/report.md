# Circuit Oracle Report
**Date:** 2026-07-28 07:23:57 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit shows a strong mix of features. The top features by direct effect include L6:F11646 and L18:F14677 (references to women / female pronouns), L7:F8644 (woman's name), L6:F16329 (female first names), L5:F5996 (femininity), L19:F9685 (women's names and roles), L6:F8166 (female-ending proper names), and L12:F12940 (female pronouns) — these are predominantly gender/identity cues. Only a handful of features genuinely reference the nursing profession: L6:F15267 (nursing profession) at pos 10 and pos 136, and L14:F3985 (management/medicine/research) and L20 (academic fields). The dominant positive direct effect comes from gender/identity features, suggesting the probe's decision is largely shortcut-driven by gender markers rather than by the substantive nursing-related content.

**Verdict:** spurious

**Spurious features:** L6:F11646, L18:F14677, L12:F12940, L7:F8644, L6:F16329, L5:F5996, L19:F9685, L6:F8166, L2:F7672, L4:F15317
**Causal features:** L6:F15267, L14:F3985, L6:F170


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L6:11646 de=0.498 |
| 3 | `inspect_feature` ×15 | L6:11646, L6:15267, L18:14677, L4:15317, L4:7864, L12:12940, L7:8644, L19:9685, L6:8166, L6:16329, L0:16075, L6:170, L5:5996, L14:3985, L2:7672 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,229 | 303 | 370 | 0 | — | — | — |
| **Total** | | **1,229** | **303** | **370** | **0** | **—** | | |
