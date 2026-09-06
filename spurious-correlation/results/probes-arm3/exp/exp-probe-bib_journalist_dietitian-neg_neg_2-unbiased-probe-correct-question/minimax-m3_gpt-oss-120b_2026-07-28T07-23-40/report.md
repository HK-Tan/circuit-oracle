# Circuit Oracle Report
**Date:** 2026-07-28 07:23:40 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by journalism-related features: L14:F4420 ('words and phrases related to journalism and newspapers'), L19:F2486 ('journalistic sources and news outlets'), L20:F8433 ('words related to news broadcasting'), L8:F8855 ('mentions of news reporters and news reporting'), L15:F2579 ('people providing information in an official capacity'), L21:F4401 ('government, news, and reporting'), and L6:F4923 ('someone wanting to work in a specific profession'). These are genuinely causal profession indicators for journalism. One potential spurious cue is L0:F8964 ('His'), the gender-marked pronoun, which has a positive direct effect on the probe. However, its effect (0.0791) is smaller than the top journalism features and is outweighed by multiple strong causal profession features. The pronoun likely contributes to a male-presenting profession default but is not the primary driver.

**Verdict:** mixed

**Spurious features:** L0:F8964
**Causal features:** L14:F4420, L19:F2486, L20:F8433, L8:F8855, L15:F2579, L21:F4401, L6:F4923


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L14:4420 de=-0.145 |
| 3 | `inspect_feature` ×18 | L14:4420, L19:2486, L0:8964, L0:8444, L0:14287, L20:8433, L0:2203, L4:11898, L5:771, L0:2011, L0:13948, L8:8855, L7:3085, L15:2579, L0:15693, L6:4923, L0:15185, L21:4401 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,421 | 269 | 114 | 0 | — | — | — |
| **Total** | | **1,421** | **269** | **114** | **0** | **—** | | |
