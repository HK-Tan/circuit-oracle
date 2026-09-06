# Circuit Oracle Report
**Date:** 2026-07-28 07:24:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by features tied to the content words of the prompt: 'recording' (L1:F3691), 'menu' (L0:F2108, L1:F12253), 'record' (L0:F7443), and several audio/recording/telecommunications features (L5:F14641, L4:F7998, L0:F10952, L6:F11757). These encode the actual prompt content about recorded menus. However, negation features (L16:F6800, L0:F4958, L4:F4492, L4:F2422, L3:F1101) also contribute substantially — the sentence contains 'do not', and the probe likely classifies this as contradiction (the menu does not provide info). Both content and negation cues drive the score, so the mechanism is mixed rather than purely spurious.

**Verdict:** mixed

**Spurious features:** L16:F6800, L0:F4958, L4:F4492, L4:F2422, L3:F1101
**Causal features:** L1:F3691, L0:F2108, L0:F7443, L1:F12253, L4:F7998, L5:F14641


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L1:3691 de=0.824 |
| 3 | `inspect_feature` ×24 | L1:3691, L2:8776, L0:2108, L0:7443, L1:12253, L16:6800, L0:4958, L4:4492, L0:13938, L4:2422, L4:7998, L0:6649, L3:1101, L1:763, L5:14641, L2:12257, L2:15894, L0:3007, L0:4523, L0:10952, L0:5128, L2:12098, L6:11757, L0:1485 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,162 | 277 | 370 | 0 | — | — | — |
| **Total** | | **1,162** | **277** | **370** | **0** | **—** | | |
