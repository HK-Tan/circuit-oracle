# Circuit Oracle Report
**Date:** 2026-07-28 07:23:57 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features overwhelmingly relate to genuine profession/content indicators: nursing terminology (L6:F15267, L4:F4665, L8:F16339), nurse management/leadership (L14:F3985, L18:F13596, L18:F14457), healthcare titles/acronyms (L20:F4927), and medical environments (L7:F3979, L4:F4665). These features directly encode the profession (nursing/perioperative) and role-related content. Only two features relate to gender/women (L18:F14677 and L6:F11646), and they have relatively small negative direct effects (-0.0645, -0.0608). Their negative direction means they actually push against the probe's classification rather than driving it. The circuit is clearly driven by causal profession/role content, not by gender shortcuts.

**Verdict:** causal

**Spurious features:** none
**Causal features:** L14:F3985, L6:F15267, L4:F4665, L18:F13596, L20:F4927, L7:F3979, L18:F14457, L8:F16339, L8:F4607


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L14:3985 de=0.163 |
| 3 | `inspect_feature` ×17 | L14:3985, L6:15267, L3:15901, L7:3979, L8:16339, L4:4665, L18:13596, L7:210, L4:8736, L20:4927, L4:9757, L2:15437, L9:16275, L18:14677, L18:14457, L6:11646, L8:4607 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,248 | 264 | 370 | 0 | — | — | — |
| **Total** | | **1,248** | **264** | **370** | **0** | **—** | | |
