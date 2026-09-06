# Circuit Oracle Report
**Date:** 2026-07-28 07:23:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is a mix. Strong causal, task-relevant features include L1:F14812 (stories/narrative), L0:F5333 (stories being told), L3:F3341 (the word 'story'), L14:F4420 (journalism/newspapers), L4:F13253 (journalism/media), L1:F2344 and L0:F15423 (the word 'country'), L0:F4564 (the word 'research'), L0:F2711 ('foreign'), and L0:F11261 ('migration' adjacent) — these point to a journalist/researcher context. However, the top feature L0:F14906 ('binding') is off-topic, and critically L0:F1069 directly encodes the male pronoun 'He'/'His', which is a gender/spurious cue the user flagged. This feature has a strong negative direct effect on the probe score, meaning the probe's classification is partly calibrated against male-gendered input rather than purely from profession semantics. The presence of both genuine profession/journalism features and an explicit gender-pronoun feature constitutes a mixed circuit.

**Verdict:** mixed

**Spurious features:** L0:F1069
**Causal features:** L1:F14812, L0:F5333, L3:F3341, L14:F4420, L4:F13253, L0:F4564, L0:F2711, L1:F2344, L0:F15423


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:14906 de=-0.222 |
| 3 | `inspect_feature` ×25 | L0:14906, L1:14812, L0:11603, L0:1069, L0:11261, L0:8061, L14:4420, L1:16233, L0:2711, L0:5333, L0:6962, L0:6051, L4:13253, L1:9201, L0:15423, L0:1301, L1:1154, L0:4564, L1:2344, L6:12712, L0:12009, L0:8350, L3:3341, L0:10255, L0:1003 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,457 | 317 | 114 | 0 | — | — | — |
| **Total** | | **1,457** | **317** | **114** | **0** | **—** | | |
