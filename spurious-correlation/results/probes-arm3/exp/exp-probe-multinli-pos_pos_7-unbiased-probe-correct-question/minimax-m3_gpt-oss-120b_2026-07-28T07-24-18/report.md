# Circuit Oracle Report
**Date:** 2026-07-28 07:24:18 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is driven by a mix of features. On the causal side, L4:F4605 (churches/chapels) and L4:F5749 (ancient settlements/fortifications) both push toward the target with negative effects, and L4:F2581 ('first' mentions) and L0:F12189 (the word 'moment') appear to track key content tokens like 'abbey' and 'moment' from the input. However, the top feature L8:F8406 is labeled as 'I' and 'Exactly' and pushes in the opposite direction — a clearly spurious shortcut. Function words like 'of' (L0:F2848) and 'the' (L0:F3820) also contribute substantially, which are generic lexical features rather than semantic content. The presence of negation-related or generic pronouns as the top driver, alongside content words, suggests the probe is partly relying on surface cues.

**Verdict:** mixed

**Spurious features:** L8:F8406, L0:F2848, L0:F3820, L0:F7710, L17:F451
**Causal features:** L4:F4605, L4:F5749, L4:F2581, L0:F12189, L6:F5342


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L8:8406 de=-0.164 |
| 3 | `inspect_feature` ×20 | L8:8406, L0:2848, L0:3820, L4:3833, L0:9026, L6:5342, L17:451, L4:4605, L4:5749, L0:7710, L4:13244, L4:2581, L0:11835, L2:8046, L0:9854, L5:7444, L4:9757, L2:8185, L6:1610, L0:12189 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,222 | 280 | 370 | 0 | — | — | — |
| **Total** | | **1,222** | **280** | **370** | **0** | **—** | | |
