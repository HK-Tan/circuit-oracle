# Circuit Oracle Report
**Date:** 2026-07-28 07:24:12 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features driving the probe are highly relevant to the actual content of the prompt. L3:F9739 captures conspiracy-related language, L2:F16230 detects mentions of semiconductor chips, L7:F1062 fires on credit cards/money terminology, L1:F8696 activates on 'invest' derivatives, L2:F15808 covers credit card mentions, and L10:F12761 picks up QAnon-associated vocabulary. These are genuine semantic/lexical features tied to the prompt's content. While L17:F4804 (negations) appears, it's a minor contributor (-0.1123) and ranks near the bottom. Other features like function words ('that', 'is', 'to', 'personal') are generic lexical cues, not spurious shortcuts. The dominant positive and negative direct effects all track the conspiracy/credit-card/financial-investment semantics of the input.

**Verdict:** causal

**Spurious features:** L17:F4804
**Causal features:** L3:F9739, L2:F16230, L7:F1062, L1:F8696, L2:F15808, L8:F12761, L0:F16015


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L3:9739 de=-0.348 |
| 3 | `inspect_feature` ×24 | L3:9739, L2:16230, L7:1062, L0:3635, L1:13684, L4:1602, L0:16015, L2:16241, L0:4287, L8:12761, L0:15958, L0:11375, L1:8696, L0:4802, L2:15808, L0:12377, L0:3937, L0:8444, L1:13292, L1:9693, L16:2624, L3:15642, L0:800, L17:4804 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,173 | 257 | 370 | 0 | — | — | — |
| **Total** | | **1,173** | **257** | **370** | **0** | **—** | | |
