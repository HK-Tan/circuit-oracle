# Circuit Oracle Report
**Date:** 2026-07-28 07:23:59 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by features explicitly tied to the nursing profession (L6:F15267 appearing 4 times, L7:F3979 twice, L3:F15901, L13/L15 features on medical/healthcare, L7:F4208 on medical procedures, L18:F13596 on nurse managers). These are genuine profession indicators. One feature, L0:F11988, references 'North Carolina' (close to 'South Carolina' in the text), which is a geographic shortcut rather than a profession cue, but its effect is modest (+0.043). No gender-pronoun features appear in the top 25. The dominance of nursing/medical features and the absence of gendered or other spurious shortcuts indicates the probe is driven primarily by causal profession content.

**Verdict:** causal

**Spurious features:** none
**Causal features:** L6:F15267, L7:F3979, L3:F15901, L14:F3985, L15:F15159, L6:F4490, L18:F13596, L7:F4654, L15:F8289, L7:F4208, L0:F5038, L2:F14478


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L14:3985 de=0.188 |
| 3 | `inspect_feature` ×20 | L14:3985, L6:15267, L7:3979, L3:15901, L0:5038, L0:6270, L15:15159, L6:4490, L8:16339, L7:210, L0:11959, L0:16075, L18:13596, L7:4654, L15:8289, L6:11057, L2:14478, L0:11988, L7:4208, L8:4607 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,263 | 264 | 370 | 0 | — | — | — |
| **Total** | | **1,263** | **264** | **370** | **0** | **—** | | |
