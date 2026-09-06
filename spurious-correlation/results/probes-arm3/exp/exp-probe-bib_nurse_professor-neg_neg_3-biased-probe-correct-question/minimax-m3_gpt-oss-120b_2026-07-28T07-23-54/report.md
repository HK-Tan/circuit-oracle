# Circuit Oracle Report
**Date:** 2026-07-28 07:23:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top 25 features are dominated by pronoun/gender markers. L0:F2994, L6:F12990, L7:F14946, L7:F14893, L12:F2175, L18:F14743, L0:F1069, L18:F10315, and L4:F14796 all detect 'he/his/him' or male pronouns and titles. These account for the vast majority of the direct effect on the probe. Only a handful of features relate to genuine profession/task content: L6:F170 (academic fields), L0:F6127 (degree/academia), L0:F12351 (receiving), and L8:F12026 (advanced degrees and affiliations). The pronoun/gender features have substantially larger direct effects than the few content features, indicating the probe's decision is primarily driven by the male pronoun 'He' as a shortcut rather than by genuine profession indicators like academic field or degree type.

**Verdict:** spurious

**Spurious features:** L0:F2994, L6:F12990, L7:F14946, L7:F14893, L12:F2175, L18:F14743, L0:F1069, L18:F10315, L4:F14796
**Causal features:** L6:F170, L0:F6127, L8:F12026, L0:F12351


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:2994 de=0.297 |
| 3 | `inspect_feature` ×15 | L0:2994, L6:12990, L7:14946, L7:14893, L12:2175, L0:6270, L18:14743, L6:170, L0:6127, L0:1069, L18:10315, L0:15320, L0:12351, L4:14796, L8:12026 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,276 | 307 | 370 | 0 | — | — | — |
| **Total** | | **1,276** | **307** | **370** | **0** | **—** | | |
