# Circuit Oracle Report
**Date:** 2026-07-28 07:24:18 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by features related to U.S. Congress mentions (L2:F2701, L3:F123, L1:F3276, L0:F7021), political parties/affiliations (L6:F6096, L2:F6735), and legal services/representation (L1:F2116). These reflect genuine content features about the topic of the premise and hypothesis. There are no strong negation-word features (e.g., 'no', 'not') in the top 25, nor identity/gender markers. The word 'who' features (L0:F13437, L0:F195) are syntactic. Some features are weak or off-topic (military, registration, 'lift'), but they have small effects. Overall, the probe appears driven by causal content features about Congress/legal services rather than spurious shortcuts.

**Verdict:** causal

**Spurious features:** none
**Causal features:** L2:F2701, L3:F123, L1:F3276, L0:F7021, L6:F6096, L2:F6735, L1:F2116, L0:F13929, L0:F11606, L3:F13271


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:6044 de=0.789 |
| 3 | `inspect_feature` ×25 | L0:6044, L0:13437, L6:6096, L2:6735, L1:6948, L2:2701, L1:2116, L2:156, L0:9557, L3:13271, L0:11606, L3:123, L0:9529, L0:6948, L3:8382, L1:3276, L6:13778, L0:7021, L1:8982, L1:12456, L0:13929, L3:12596, L0:195, L1:4224, L0:2470 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,170 | 265 | 370 | 0 | — | — | — |
| **Total** | | **1,170** | **265** | **370** | **0** | **—** | | |
