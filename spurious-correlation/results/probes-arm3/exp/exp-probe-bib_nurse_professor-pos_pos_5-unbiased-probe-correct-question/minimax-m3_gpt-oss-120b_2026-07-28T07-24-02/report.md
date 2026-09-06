# Circuit Oracle Report
**Date:** 2026-07-28 07:24:02 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by features directly tied to the profession of nursing and midwifery: L3:F15901 (nurses/nursing), L6:F15267 (nursing profession), L4:F4665 (medical environments/personnel), L7:F3979 (nursing/healthcare), L18:F13596 (nurse managers), L0:F1832 ('labor'), and L7:F2861 (pregnancy/labor). These are genuine profession/specialty indicators. There are no gender-marker or pronoun-identity features in the top 25 (L0:F11132 mentions 'his' but is a minor mix-feature with negative effect, not a clear gender shortcut). The few non-profession features (L0:F9911 'that', L0:F8444 'to', L0:F10771 'linked', L0:F6515/L0:F11333 years) are generic function-word/temporal features unlikely to constitute a gender-based shortcut. The probe appears to be driven by causal profession content.

**Verdict:** causal

**Spurious features:** none
**Causal features:** L3:F15901, L6:F15267, L4:F4665, L7:F3979, L18:F13596, L0:F1832, L7:F2861, L14:F3985


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L14:3985 de=0.106 |
| 3 | `inspect_feature` ×20 | L14:3985, L0:9911, L3:15901, L0:10771, L6:9980, L0:8444, L7:210, L6:15267, L4:4665, L6:4490, L0:7532, L0:6515, L7:3979, L2:15437, L8:16339, L18:13596, L0:11333, L0:1832, L0:11132, L7:2861 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,220 | 289 | 370 | 0 | — | — | — |
| **Total** | | **1,220** | **289** | **370** | **0** | **—** | | |
