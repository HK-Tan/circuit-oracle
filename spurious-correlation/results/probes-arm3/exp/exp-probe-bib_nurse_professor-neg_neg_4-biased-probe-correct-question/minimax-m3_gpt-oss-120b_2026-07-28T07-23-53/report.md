# Circuit Oracle Report
**Date:** 2026-07-28 07:23:53 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features are overwhelmingly gender/pronoun related: L0:F2994 (he/his), L6:F12990 (male pronouns and titles), L7:F14893 (pronouns), L7:F14946 (his/he/him), L4:F4315 (his/he/him/hers), L12:F2175 (gender words), and L18:F14743 (He). These features fire on 'He', 'his', 'He is also', etc. While there are a few content-relevant features like L2:F13731 (lab/laboratory) and L3:F9871 (Vice President) and L0:F11024 (clock/technical), the dominant signal driving the probe is male gender pronouns rather than profession-specific content.

**Verdict:** spurious

**Spurious features:** L0:F2994, L6:F12990, L7:F14893, L7:F14946, L4:F4315, L12:F2175, L18:F14743, L0:F8658, L0:F10846, L0:F2848
**Causal features:** L2:F13731, L3:F9871, L0:F11024, L0:F3214


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:2994 de=0.254 |
| 3 | `inspect_feature` ×16 | L0:2994, L6:12990, L0:2848, L0:11024, L18:14743, L7:14893, L7:14946, L0:8658, L4:4315, L12:2175, L2:13731, L0:3214, L0:10846, L0:6051, L3:9871, L0:3255 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,214 | 278 | 370 | 0 | — | — | — |
| **Total** | | **1,214** | **278** | **370** | **0** | **—** | | |
