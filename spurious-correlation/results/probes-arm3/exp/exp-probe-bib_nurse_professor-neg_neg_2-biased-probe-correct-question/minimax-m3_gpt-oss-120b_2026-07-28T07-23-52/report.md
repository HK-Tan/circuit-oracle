# Circuit Oracle Report
**Date:** 2026-07-28 07:23:52 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features driving the probe are overwhelmingly gender/pronoun-related: L0:F2994 (his/he), L7:F14893 (pronouns), L7:F14946 (his), L12:F2175 (gender), L6:F12990 (male pronouns), L18:F14743 (He), L0:F1069 (male person), and L18:F10315 (pronouns) occupy 9 of the top 25 slots and dominate the highest direct effects. While there are a few profession-relevant features (L6:F170 humanities, L5:F10392 academic fields, L2:F13900 'master'/'slave' in technical context), they have lower direct effects and are outnumbered by pronoun/gender features. The probe appears to rely primarily on gender markers (he/his) rather than genuine profession indicators to classify this text.

**Verdict:** spurious

**Spurious features:** L0:F2994, L7:F14893, L7:F14946, L12:F2175, L6:F12990, L18:F14743, L0:F1069, L18:F10315
**Causal features:** L6:F170, L5:F10392, L2:F13900


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:2994 de=0.395 |
| 3 | `inspect_feature` ×19 | L0:2994, L7:14893, L7:14946, L12:2175, L6:12990, L6:170, L18:14743, L5:10392, L0:1326, L0:7532, L0:12351, L0:13526, L0:15320, L0:13553, L18:10315, L0:1069, L3:6656, L0:4185, L2:13900 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,199 | 276 | 370 | 0 | — | — | — |
| **Total** | | **1,199** | **276** | **370** | **0** | **—** | | |
