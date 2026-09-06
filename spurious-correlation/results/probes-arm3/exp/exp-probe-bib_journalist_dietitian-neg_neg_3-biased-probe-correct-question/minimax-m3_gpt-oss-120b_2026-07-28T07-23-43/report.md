# Circuit Oracle Report
**Date:** 2026-07-28 07:23:43 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The probe's classification appears driven by a mix of causal profession-related features and spurious demographic features. Causal indicators include L1:F14812 (stories/narrative), L1:F7449 (representation), L0:F4564 (research), L0:F5333 (stories being told), L0:F61 (stories), L0:F10036 (scientific research), L4:F13253 (journalism/media), L14:F4420 (journalism/newspapers), and L4:F4411 (verbs) — these reflect the actual profession described (journalist/researcher). However, several spurious features appear: L7:F14893 (pronouns), L0:F2994 ('his'/'he'), L7:F14946 ('his'/'he'/'him'), L18:F14743 ('He'), L2:F9301 (mentions of men/women in gendered contexts), and L6:F12990 (male pronouns/titles with male descriptors) — these track gender rather than profession. The presence of multiple gender-marker features in the top 25 alongside genuine profession features suggests the probe uses both, but the gender features are prominent and likely act as shortcuts.

**Verdict:** mixed

**Spurious features:** L7:F14893, L0:F2994, L7:F14946, L18:F14743, L2:F9301, L6:F12990
**Causal features:** L1:F14812, L1:F7449, L0:F4564, L0:F5333, L0:F61, L0:F10036, L4:F13253, L14:F4420, L4:F4411


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:6051 de=-0.256 |
| 3 | `inspect_feature` ×24 | L0:6051, L0:7696, L1:14812, L1:7449, L0:4564, L0:5333, L0:3255, L0:10187, L0:61, L7:14893, L0:2994, L0:10036, L4:13253, L0:9121, L7:14946, L0:1301, L18:14743, L0:14216, L14:4420, L0:8061, L2:9301, L4:4411, L6:12990, L0:1506 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,442 | 369 | 114 | 0 | — | — | — |
| **Total** | | **1,442** | **369** | **114** | **0** | **—** | | |
