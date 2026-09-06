# Circuit Oracle Report
**Date:** 2026-07-28 07:23:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top 25 features are dominated by gender/women-related markers. The single most influential feature (L6:F11646, 'references to women, potentially triggered by pronouns and titles') and numerous others (L7:F8644 woman's name, L6:F16329 female first names, L19:F9685 women's names and roles, L5:F5996 words associated with females, L20:F12501 feminine pronoun, L0:F9519 'she'/'her', L2:F9301 men and women in gendered contexts, L2:F7672 mentions of women by name and relationship) all encode gender/femininity signals. Genuine profession indicators are nearly absent—L4:F13412 (diets/dietary health) is a weak professional cue, and L25:F8089 ('areas') is superficial. The circuit clearly latches onto gender markers (pronouns, female names, femininity language) rather than domain-specific professional content like 'sports nutrition', 'Academy of Nutrition and Dietetics', or 'consultant'.

**Verdict:** spurious

**Spurious features:** L6:F11646, L7:F8644, L6:F16329, L19:F9685, L5:F5996, L14:F12501, L0:F9519, L2:F9301, L2:F7672, L18:F14677, L12:F14970, L4:F1276, L6:F8166, L7:F2765, L0:F5686, L0:F6051, L0:F10148, L2:F8089, L4:F7864
**Causal features:** L4:F13412


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L6:11646 de=0.283 |
| 3 | `inspect_feature` ×20 | L6:11646, L7:8644, L18:14677, L12:14970, L6:16329, L4:13412, L19:9685, L4:1276, L0:6051, L0:10148, L4:7864, L7:2765, L0:5686, L5:5996, L14:12501, L2:9301, L6:8166, L0:9519, L2:7672, L2:8089 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,250 | 376 | 370 | 0 | — | — | — |
| **Total** | | **1,250** | **376** | **370** | **0** | **—** | | |
