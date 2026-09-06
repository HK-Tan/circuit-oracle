# Circuit Oracle Report
**Date:** 2026-07-28 07:23:59 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by features signaling genuine profession/occupation content: academic degrees (L2:F10852, L9:F988, L14:F3956), universities and credentials (L7:F14129, L20:F14235, L8:F11284), academic research (L1:F10986), academic publications (L6:F3235, L6:F13001), and humanities fields (L6:F170). These are the causal task-content features driving the probe. A few features encode spurious gender cues: L0:F1069 ('He/His' male pronoun), L0:F2994 ('his'/'he'), and L6:F2161 (identity). These are present but the academic-credential features are clearly the dominant direct-effect contributors (negative effects from credential features like L20:F14235, L2:F10852, L14:F3956 outweigh the gender feature effects). The probe is primarily driven by academic content, with some incidental gender-feature contribution.

**Verdict:** mixed

**Spurious features:** L0:F1069, L0:F2994, L6:F2161
**Causal features:** L2:F10852, L7:F14129, L8:F11284, L20:F14235, L1:F10986, L14:F3956, L9:F988, L6:F3235, L6:F13001, L6:F170


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L8:2383 de=-0.090 |
| 3 | `inspect_feature` ×20 | L8:2383, L0:6051, L6:14747, L2:10852, L1:10986, L7:14129, L8:11284, L20:14235, L0:1069, L6:2161, L6:3235, L14:3956, L9:988, L6:13001, L1:1505, L4:16301, L0:2994, L4:9757, L6:170, L9:228 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,156 | 313 | 370 | 0 | — | — | — |
| **Total** | | **1,156** | **313** | **370** | **0** | **—** | | |
