# Circuit Oracle Report
**Date:** 2026-07-28 07:23:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The probe's classification appears to be driven by a mix of causal profession-indicating features and spurious gender-marker features. Causal features: L14:F4420, L4:F13253, and L19:F2486 all relate to journalism/newspapers/reporting, which is the actual profession being discussed. Spurious gender features are also prominently represented: L0:F2994, L7:F14946, L18:F14743, and L6:F12990 detect male pronouns ('he', 'his') and male descriptors. These pronoun features have large direct effects (e.g., L0:F2994 at +0.2324, L7:F14946 at -0.1201, L18:F14743 at -0.1064, L6:F12990 at -0.0928), suggesting the probe partly relies on gender as a shortcut rather than purely on profession content.

**Verdict:** mixed

**Spurious features:** L0:F2994, L7:F14893, L7:F14946, L18:F14743, L6:F12990
**Causal features:** L14:F4420, L4:F13253, L19:F2486


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:2994 de=0.232 |
| 3 | `inspect_feature` ×18 | L0:2994, L14:4420, L0:8974, L0:6051, L4:13253, L7:14893, L7:14946, L19:2486, L18:14743, L0:886, L0:8061, L0:7681, L0:14824, L6:12990, L0:4677, L0:3255, L0:12660, L0:8642 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,466 | 265 | 114 | 0 | — | — | — |
| **Total** | | **1,466** | **265** | **114** | **0** | **—** | | |
