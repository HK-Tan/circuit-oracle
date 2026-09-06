# Circuit Oracle Report
**Date:** 2026-07-28 07:24:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features fire on content words from the prompt itself: 'menu' (L0:F2108, L1:F12253, L3:F3573, L2:F3648), 'will' (L0:F8046, L2:F188), 'record'/'recording' (L1:F3691, L0:F7443, L2:F3059, L5:F14641), 'provide' (L2:F7863), and domain features (telephony L4:F7998, finance/property L2:F8776). These are lexical/semantic representations of the actual premise and hypothesis content, not shortcut cues like negation ('not') or identity terms. There is no 'not/never/no' feature driving the decision; instead the circuit integrates the proposition-level content (what 'recorded menus' do and don't provide). The directionality is mixed (some pos some neg) reflecting how different content features push the contradiction judgment, which is consistent with a genuine entailment/contradiction computation rather than a single spurious cue.

**Verdict:** causal

**Spurious features:** none
**Causal features:** L0:F2108, L1:F12253, L3:F3573, L2:F3648, L0:F8046, L2:F188, L1:F3691, L0:F7443, L2:F3059, L5:F14641, L2:F7863, L4:F7998, L2:F8776, L4:F7643


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L2:8776 de=0.523 |
| 3 | `inspect_feature` ×24 | L2:8776, L0:2108, L1:12253, L0:8046, L1:3691, L0:7443, L3:3573, L0:6649, L0:7404, L4:7998, L2:3648, L2:188, L2:3059, L0:5128, L0:4523, L17:451, L2:11317, L4:7643, L0:13280, L0:9990, L0:15480, L5:14641, L2:7863, L6:11757 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,156 | 339 | 370 | 0 | — | — | — |
| **Total** | | **1,156** | **339** | **370** | **0** | **—** | | |
