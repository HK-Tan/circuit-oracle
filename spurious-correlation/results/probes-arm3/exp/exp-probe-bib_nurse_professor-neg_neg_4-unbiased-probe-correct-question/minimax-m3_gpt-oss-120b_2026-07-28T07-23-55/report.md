# Circuit Oracle Report
**Date:** 2026-07-28 07:23:55 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit contains a mix of features. Genuine profession-related causal features include: L2:F10852 (academic titles/degrees), L2:F4627 ('director'), L7:F14129 (academic degrees/universities), L3:F4213 (degree qualifications/awards), L4:F15748 (organizational titles/processes), L2:F12316 ('mobile' in technical context), L0:F4621 (administrative positions), and L14:F15086 (Korea/Korean references) — all pointing to genuine professional/academic content. However, L0:F1069 is explicitly a male-gender pronoun feature ('He'/'His') and is among the top features by direct effect, representing a spurious cue. Other features like L0:F10846 ('also'), L0:F8658 ('is'), L0:F3255 ('and') are generic syntax tokens. The presence of the explicit gender marker feature alongside genuine profession features makes this a mixed case.

**Verdict:** mixed

**Spurious features:** L0:F1069
**Causal features:** L2:F10852, L2:F4627, L7:F14129, L3:F4213, L4:F15748, L2:F12316, L0:F4621, L14:F15086, L1:F14934


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L14:15086 de=-0.061 |
| 3 | `inspect_feature` ×24 | L14:15086, L6:3774, L0:10846, L2:10852, L1:14934, L2:4627, L0:8658, L7:14129, L0:12904, L0:1069, L0:1242, L0:15160, L0:3255, L0:5743, L4:12934, L0:5718, L8:11284, L0:4621, L0:12208, L0:10457, L2:12316, L3:4213, L4:15748, L0:6051 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,181 | 292 | 370 | 0 | — | — | — |
| **Total** | | **1,181** | **292** | **370** | **0** | **—** | | |
