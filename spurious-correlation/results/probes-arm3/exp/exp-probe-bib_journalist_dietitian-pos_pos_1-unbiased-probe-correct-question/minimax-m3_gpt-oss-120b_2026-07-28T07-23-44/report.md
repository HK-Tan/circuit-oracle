# Circuit Oracle Report
**Date:** 2026-07-28 07:23:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The vast majority of high-impact features in this circuit are genuinely related to nutrition, diet, and food (L4:F13412 diet/health, L6:F11327 food/nutrition, L19:F1589 nutritional studies, L15:F8177 eating, L0:F2175 'eat', L1:F5530 meals/food, L6:F8984 health, L4:F12213 health research). These are causal profession indicators for a dietitian. L6:F6115 about commercial activity/customers is also relevant to client-facing work. Only L6:F11646 (references to women, triggered by pronouns/titles) appears as a potentially spurious gender feature, but it has a relatively small negative effect (-0.0586) and is triggered by the pronoun 'her' — a legitimate contextual signal rather than a stereotyped shortcut. L0:F6051 (periods/spaces) is a formatting artifact with negative effect. The dominant signal is clearly content-based nutrition/diet terms.

**Verdict:** causal

**Spurious features:** L6:F11646
**Causal features:** L6:F6115, L4:F13412, L14:F4197, L6:F11327, L19:F1589, L4:F12213, L0:F9888, L6:F8984, L15:F8177, L0:F2175, L1:F5530


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L6:6115 de=0.128 |
| 3 | `inspect_feature` ×18 | L6:6115, L4:13412, L14:4197, L6:11327, L19:1589, L0:6051, L4:12213, L1:15251, L0:9888, L5:3400, L0:5697, L0:8444, L6:8984, L15:8177, L0:2175, L6:11646, L4:15160, L1:5530 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,191 | 312 | 370 | 0 | — | — | — |
| **Total** | | **1,191** | **312** | **370** | **0** | **—** | | |
