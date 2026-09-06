# Circuit Oracle Report
**Date:** 2026-07-28 07:23:43 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by features that detect genuine profession-relevant content: journalism/newspapers (L14:F4420), editors/publishers (L6:F12712), research institutes (L1:F4459), military/weapons terminology (L1:F1445), Middle East geopolitical context (L2:F12901, L0:F15880, L0:F3007), TV/radio broadcasting (L6:F10984), and institutional references (L4:F5060, L0:F8690). These all point toward a defense journalist profession. However, L0:F12768 explicitly detects gendered pronouns ('he'/'she'), which is a potential spurious cue. The negative direct effect of L0:F12768 (-0.0942) actually works against the probe's classification, suggesting gender is not driving the decision in this case. The dominant positive drivers are content-based (Middle East, journalism, institutes, broadcasting).

**Verdict:** causal

**Spurious features:** L0:F12768
**Causal features:** L14:F4420, L6:F12712, L1:F4459, L2:F12901, L0:F15880, L0:F3007, L6:F10984, L1:F1445, L4:F5060, L0:F8690, L0:F10881, L3:F10489


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:7124 de=-0.157 |
| 3 | `inspect_feature` ×25 | L0:7124, L0:15661, L0:12768, L0:6484, L14:4420, L0:3007, L0:2348, L6:12712, L1:4459, L0:10881, L0:1229, L0:9297, L3:10489, L2:12901, L1:1445, L6:10984, L0:13096, L0:9728, L0:6051, L0:12713, L4:5060, L0:8690, L1:15323, L0:15880, L2:12068 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,418 | 305 | 114 | 0 | — | — | — |
| **Total** | | **1,418** | **305** | **114** | **0** | **—** | | |
