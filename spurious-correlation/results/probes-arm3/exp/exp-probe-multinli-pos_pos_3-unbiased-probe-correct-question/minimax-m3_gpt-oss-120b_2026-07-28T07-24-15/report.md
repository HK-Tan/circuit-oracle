# Circuit Oracle Report
**Date:** 2026-07-28 07:24:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The probe's classification is driven by a mix of causal content features and a clear spurious signal. Causal features include lexical/semantic content from the premise: L1:F1027 ('tower'), L0:F5494 ('early'), L0:F7513 ('together'), L0:F4367 (centuries), L4:F5749 (ancient settlements/fortifications), L2:F4429 (beginning of period), and L1:F11220 (restore). These reflect genuine entailment-relevant content. However, a strongly negative spurious feature is L0:F10815 ('any'), a negation-word cue that appears in the hypothesis ('does not contain any') and directly drives the contradiction classification. This is a classic shortcut: the probe latches onto the negation 'any' rather than the semantic contradiction.

**Verdict:** mixed

**Spurious features:** L0:F10815
**Causal features:** L1:F1027, L0:F5494, L0:F7513, L0:F4367, L4:F5749, L2:F4429, L1:F11220, L0:F8974, L0:F8082, L0:F2158


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L4:13244 de=0.287 |
| 3 | `inspect_feature` ×24 | L4:13244, L2:1430, L0:2158, L0:7360, L1:1027, L0:5494, L1:11220, L0:14108, L2:4429, L0:7513, L6:486, L0:8974, L4:5749, L3:10598, L0:4367, L0:10815, L0:8082, L0:4079, L8:8406, L1:593, L2:6867, L2:3491, L1:8005, L0:5565 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,163 | 263 | 370 | 0 | — | — | — |
| **Total** | | **1,163** | **263** | **370** | **0** | **—** | | |
