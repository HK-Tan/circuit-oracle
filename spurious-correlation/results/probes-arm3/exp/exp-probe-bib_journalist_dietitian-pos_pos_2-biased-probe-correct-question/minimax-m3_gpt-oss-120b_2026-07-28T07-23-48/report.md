# Circuit Oracle Report
**Date:** 2026-07-28 07:23:48 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top-25 features are overwhelmingly dominated by gender/female-marker features: L6:F11646 (women references), L12:F12940 (female pronouns), L18:F14677 (women/girls mentioned), L4:F15317 (named entities), L8:F16329 (female first names), L10:F14965 (terms relating to women), L14:F12501 (feminine pronoun), L19:F9685 (women's names and roles), L2:F7672 (women by name), L7:F8644 (woman's name), L7:F8952 (references to women), L13:F11685 (words related to women), L5:F5996 (females/femininity). These are classic spurious shortcuts. The genuinely task-relevant features (nutrition/food: L6:F11327, L4:F13412; food insecurity: L14:F4197) are present but appear much lower in the ranking and with smaller direct effects. The probe is primarily driven by gender/identity cues rather than the professional content (nutritionist/cooking expertise).

**Verdict:** spurious

**Spurious features:** L6:F11646, L12:F12940, L18:F14677, L6:F16329, L10:F14965, L14:F12501, L19:F9685, L2:F7672, L7:F8644, L7:F8952, L13:F11685, L5:F5996, L18:F14743, L12:F12940
**Causal features:** L6:F11327, L4:F13412, L14:F4197


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L6:11646 de=0.357 |
| 3 | `inspect_feature` ×19 | L6:11646, L12:12940, L18:14677, L4:15317, L4:7864, L6:16329, L10:14965, L6:11327, L14:12501, L19:9685, L2:7672, L7:8644, L4:13412, L18:14743, L7:8952, L13:11685, L14:4197, L5:5996, L7:2765 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,180 | 368 | 370 | 0 | — | — | — |
| **Total** | | **1,180** | **368** | **370** | **0** | **—** | | |
