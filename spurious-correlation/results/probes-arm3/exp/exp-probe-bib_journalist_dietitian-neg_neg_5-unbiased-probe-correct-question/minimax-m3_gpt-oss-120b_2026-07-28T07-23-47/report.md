# Circuit Oracle Report
**Date:** 2026-07-28 07:23:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features by absolute direct effect show a strong mix. The most prominent negative contributors are journalism/news-related features (L14:F4420, L19:F2486, L4:F13253, L11:L8:F8855, L7:F13646), which are genuinely task-relevant. There are also several causal academic/employment features: L0:F6127 (degree/academia), L2:F11349 (academic degrees), L0:F5099 (obtain), L0:F112 (since, temporal/career context), L4:F110 (employment/contractor language), L6:F12712 (editor/publisher titles), and L0:F9397 (technical jargon). However, L0:F1069 explicitly fires on male pronouns ('He'/'His'), and L0:F1069 is the 7th most influential feature with a substantial negative direct effect. Other low-layer features like L0:F8061 ('in'), L0:F14824 ('has'), L0:F8974 ('from'), L0:F13864 ('ever'), and L0:F6051 (punctuation/numbers) are generic surface cues rather than profession indicators. The presence of a dedicated male-pronoun feature with strong effect suggests gender is being used as a signal, which is a spurious shortcut — though journalism features also dominate, indicating the probe is not purely gender-driven.

**Verdict:** mixed

**Spurious features:** L0:F1069, L0:F8061, L0:F14824, L0:F8974, L0:F13864, L0:F6051, L0:F8642
**Causal features:** L14:F4420, L19:F2486, L4:F13253, L8:F8855, L6:F12712, L0:F6127, L2:F11349, L0:F5099, L0:F112, L4:F110, L7:F13646


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L14:4420 de=-0.196 |
| 3 | `inspect_feature` ×22 | L14:4420, L19:2486, L4:13253, L0:4874, L0:6051, L0:8642, L0:1069, L0:8061, L0:14824, L0:8974, L8:8855, L6:12712, L0:13864, L0:9397, L0:926, L0:5099, L0:6786, L0:6127, L7:13646, L2:11349, L0:112, L4:110 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,446 | 430 | 114 | 0 | — | — | — |
| **Total** | | **1,446** | **430** | **114** | **0** | **—** | | |
