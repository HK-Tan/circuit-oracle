# Circuit Oracle Report
**Date:** 2026-07-28 07:23:40 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by features that genuinely encode journalism-related content: L14:F4420 (journalism/newspapers), L19:F2486 (journalistic sources/news outlets, appearing 7 times across positions 21-30), L8:F8855 (news reporters/reporting), L20:F8433 (news broadcasting), L15:F2579 (people providing information officially), and L1:F14511/L0:F1579 (the word 'report'). These are causal profession indicators. However, two features are clearly spurious shortcuts: L0:F8964 ('His' possessive pronoun) and L0:F1069 (male pronoun 'He'/'His'), both firing on the gendered subject. These gender markers contribute positively to the probe score without representing the profession itself. The mix of journalism features (clearly causal) and pronoun features (spurious) makes this a mixed case, though the journalism features dominate in count and direct effect magnitude.

**Verdict:** mixed

**Spurious features:** L0:F8964, L0:F1069
**Causal features:** L14:F4420, L19:F2486, L8:F8855, L20:F8433, L15:F2579, L1:F14511, L0:F1579, L0:F14287, L5:F771


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L14:4420 de=-0.147 |
| 3 | `inspect_feature` ×17 | L14:4420, L19:2486, L0:8964, L0:8444, L0:14287, L0:2203, L0:2011, L0:13948, L1:14511, L8:8855, L0:15693, L20:8433, L5:771, L0:1069, L4:11898, L0:1579, L15:2579 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,392 | 291 | 114 | 0 | — | — | — |
| **Total** | | **1,392** | **291** | **114** | **0** | **—** | | |
