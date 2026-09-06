# Circuit Oracle Report
**Date:** 2026-07-28 07:23:46 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features by direct effect are overwhelmingly gender/pronoun markers: L7:F14893 (pronouns), L7:F14946 ('his'), L6:F12990 (male pronouns/titles), L0:F2994 ('his'/'he'), L19:F8814 (pronouns/names), L18:F14743 ('He'), L4:F4315 ('his' and associated pronouns), L18:F10315 (pronouns), L2:F9301 (men/women in gendered contexts), L0:F2208 ('Him'/'His'). These are shortcut cues detecting male gender, not profession. The few task-relevant features exist but are lower-ranked: L14:F4420 (journalism/newspapers), L19:F2486 (news outlets), and possibly L1:F5893 (world/countries). The circuit is dominated by spurious gender signals.

**Verdict:** spurious

**Spurious features:** L7:F14893, L7:F14946, L6:F12990, L0:F2994, L19:F8814, L18:F14743, L4:F4315, L18:F10315, L2:F9301, L0:F2208
**Causal features:** L14:F4420, L19:F2486, L1:F5893


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L7:14893 de=0.488 |
| 3 | `inspect_feature` ×24 | L7:14893, L7:14946, L6:12990, L0:2994, L19:8814, L18:14743, L4:4315, L18:10315, L18:7400, L14:4420, L0:2011, L2:9301, L4:11898, L19:2486, L0:8444, L0:7927, L0:2208, L0:11767, L2:5491, L1:5893, L7:16284, L0:13381, L21:5451, L0:2987 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,437 | 296 | 114 | 0 | — | — | — |
| **Total** | | **1,437** | **296** | **114** | **0** | **—** | | |
