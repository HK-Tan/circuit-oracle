# Circuit Oracle Report
**Date:** 2026-07-28 07:23:43 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features are overwhelmingly gender/pronoun-related: L7:F14893 (pronouns), L7:F14946 ('his'/'he'/'him'), L6:F12990 (male pronouns and titles), L0:F2994 ('his'/'he'), L19:F8814 (pronouns and names), L18:F14743 ('He'), L4:F4315 ('his' and other pronouns), L18:F10315 (pronouns), L2:F9301 (mentions of men/women in gendered contexts), L0:F2208 ('Him'/'His'). The dominant causal features driving the probe are male pronoun features, not profession indicators. The few profession-related features (L14:F4420 'journalism and newspapers', L19:F2486 'journalistic sources and news outlets') appear much lower in the ranking with smaller direct effects. The probe is classifying based on the gendered subject cue rather than the journalistic content.

**Verdict:** spurious

**Spurious features:** L7:F14893, L7:F14946, L6:F12990, L0:F2994, L19:F8814, L18:F14743, L4:F4315, L18:F10315, L2:F9301, L0:F2208
**Causal features:** L14:F4420, L19:F2486


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L7:14893 de=0.471 |
| 3 | `inspect_feature` ×24 | L7:14893, L7:14946, L6:12990, L0:2994, L19:8814, L18:14743, L4:4315, L18:10315, L14:4420, L18:7400, L0:2011, L2:9301, L0:8444, L0:7927, L4:11898, L0:2208, L0:11767, L19:2486, L0:13381, L1:5893, L7:16284, L2:5491, L0:2987, L0:15981 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,451 | 303 | 114 | 0 | — | — | — |
| **Total** | | **1,451** | **303** | **114** | **0** | **—** | | |
