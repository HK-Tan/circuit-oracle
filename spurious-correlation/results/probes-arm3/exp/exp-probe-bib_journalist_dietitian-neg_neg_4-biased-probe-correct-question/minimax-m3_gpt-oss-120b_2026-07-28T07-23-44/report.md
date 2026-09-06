# Circuit Oracle Report
**Date:** 2026-07-28 07:23:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit shows a strong mix of spurious and causal features. Spurious gender markers dominate the top of the ranking: L18:F14743 (appearing 3 times, labeled 'He'), L14:F14097 ('he'), L7:F14946 ('his'/'he'/'him'), L15-related L0:F12768 ('he' and 'she' in proximity), and L6:F12990 ('male pronouns and titles along with descriptors associated with men'). These male-pronoun features carry large direct effects and are clearly functioning as gender shortcuts rather than profession indicators. Causal features pointing to genuine profession content include L1:F4459 ('mentions of research institutes'), L14:F4420 ('journalism and newspapers'), L1:F15416 ('writers' or 'writer'), L1:F15323 ('starting' in academic papers), L0:F5288 ('service' terms), and L0:F13754 ('official or functional bodies'). However, the pronoun/gender features are among the highest-magnitude direct effects, which is consistent with the user's concern that the probe may be using gender as a shortcut.

**Verdict:** spurious

**Spurious features:** L18:F14743, L14:F14097, L7:F14946, L0:F12768, L6:F12990
**Causal features:** L1:F4459, L14:F4420, L1:F15416, L1:F15323, L0:F5288, L0:F13754


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:7124 de=-0.160 |
| 3 | `inspect_feature` ×23 | L0:7124, L18:14743, L1:15323, L0:15661, L0:3820, L14:14097, L0:6556, L1:4459, L0:4870, L0:5288, L0:6051, L7:14946, L0:12768, L2:9293, L1:15063, L6:12990, L14:4420, L1:15416, L0:9630, L0:13754, L0:5710, L4:11134, L0:8067 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,423 | 331 | 114 | 0 | — | — | — |
| **Total** | | **1,423** | **331** | **114** | **0** | **—** | | |
