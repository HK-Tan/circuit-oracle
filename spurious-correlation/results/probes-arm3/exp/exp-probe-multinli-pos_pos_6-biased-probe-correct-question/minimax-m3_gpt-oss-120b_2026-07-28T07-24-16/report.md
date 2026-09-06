# Circuit Oracle Report
**Date:** 2026-07-28 07:24:16 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features driving the probe's classification include a strong cluster of negation-related features: L16:F12358 ('not' followed by 'to be'), L4:F4492 ('negations in various languages'), L0:F4958 ('the word not'), L3:F1101 (negation in software contexts), and L4:F2422 (negations in other languages). These are all at the critical position 21, which corresponds to the phrase 'were not allowed to deforest.' This strongly suggests the probe is using negation words as a shortcut to detect contradiction, rather than understanding the semantic content. Some causal features exist (L1:F361 on agriculture/ecology at pos 9, L2:F4819 on 'fire' at pos 12, L0:F3498 on 'they' pronouns, L15:F2080 on 'set' phrases), but they are outweighed by the negation-cluster features that fire on the contradictory clause.

**Verdict:** spurious

**Spurious features:** L16:F12358, L4:F4492, L0:F4958, L3:F1101, L4:F2422
**Causal features:** L1:F361, L2:F4819, L0:F3498, L15:F2080, L0:F3820


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:3498 de=-0.785 |
| 3 | `inspect_feature` ×23 | L0:3498, L0:2238, L3:8011, L3:1101, L16:12358, L2:2952, L4:4492, L2:4819, L0:3820, L0:8444, L4:2422, L15:2080, L1:8332, L3:8733, L3:6227, L0:4958, L3:13138, L3:3797, L1:361, L0:12492, L8:8406, L4:7140, L0:9161 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,210 | 287 | 370 | 0 | — | — | — |
| **Total** | | **1,210** | **287** | **370** | **0** | **—** | | |
