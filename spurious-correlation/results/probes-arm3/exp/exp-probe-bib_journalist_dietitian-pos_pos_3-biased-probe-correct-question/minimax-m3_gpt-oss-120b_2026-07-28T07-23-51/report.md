# Circuit Oracle Report
**Date:** 2026-07-28 07:23:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is overwhelmingly dominated by features related to gender/female references. Of the top 25 features, at least 14 are explicitly about women, female pronouns, or women's names (L6:F11646 x3, L18:F14677 x3, L12:F12940, L19:F9685, L6:F16329 x2, L7:F8644 x2, L14:F12501 x2, L10:F14965, L2:F7672, L7:F8952). The only profession-relevant feature is L6:F11327 about food/nutrition, which ranks #19 with a relatively modest effect (+0.1035). The strongest effects come from gender markers (female pronouns like 'She', 'her') rather than from content indicating a nutrition profession. This indicates the probe is relying on the subject's gender as a shortcut rather than on genuine task content like 'food philosophy', 'healthy food', 'dieting', or 'wholefoods'.

**Verdict:** spurious

**Spurious features:** L6:F11646, L18:F14677, L12:F12940, L19:F9685, L6:F16329, L7:F8644, L14:F12501, L10:F14965, L2:F7672, L7:F8952, L18:F14743, L4:F15317, L0:F2349, L7:F2765
**Causal features:** L6:F11327


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L6:11646 de=0.340 |
| 3 | `inspect_feature` ×16 | L6:11646, L18:14677, L4:7864, L6:16329, L12:12940, L19:9685, L4:15317, L7:8644, L0:2349, L2:7672, L14:12501, L18:14743, L6:11327, L7:8952, L10:14965, L7:2765 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,208 | 333 | 370 | 0 | — | — | — |
| **Total** | | **1,208** | **333** | **370** | **0** | **—** | | |
