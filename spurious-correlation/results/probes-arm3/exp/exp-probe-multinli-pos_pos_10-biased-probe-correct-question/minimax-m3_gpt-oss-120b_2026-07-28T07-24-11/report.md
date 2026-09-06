# Circuit Oracle Report
**Date:** 2026-07-28 07:24:11 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features by direct effect are overwhelmingly negation-related: L4:F2422 (negations in other languages), L4:F4492 (negations in various languages), L3:F1101 (absence/negation in software), L0:F4958 ('not'), L3:F12079 (negations), L16:F12358 ('not' + 'to be'), L1:F14233 (negative sentiment markers), L4:F7500 (negation words), L2:F12021 ('not'/negative terms), and L9:F14687 ('not' phrases). These directly correspond to the 'There is not' construction in the second sentence, which is the cue marking contradiction. A few features like L1:F15749 ('strange'), L0:F630 ('going'), L0:F13522 ('speed'), and L1:F2580 ('reverse') relate to actual prompt content (role reversal, strangest), but their effects are smaller and secondary. The probe is primarily driven by the presence of the negation word 'not', which is a surface-level shortcut for detecting contradiction rather than a deeper semantic understanding of the entailment relationship.

**Verdict:** spurious

**Spurious features:** L4:F2422, L4:F4492, L3:F1101, L0:F4958, L3:F12079, L16:F12358, L1:F14233, L4:F7500, L2:F12021, L9:F14687, L1:F14233
**Causal features:** L1:F15749, L0:F630, L1:F2580, L3:F10225, L0:F11375, L4:F430


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L4:2422 de=-1.273 |
| 3 | `inspect_feature` ×25 | L4:2422, L4:4492, L3:1101, L0:4958, L3:8011, L3:12079, L16:12358, L3:2232, L3:9803, L2:16097, L3:3669, L0:11375, L1:14233, L1:15749, L9:14687, L2:6993, L0:13522, L4:5709, L4:430, L4:7500, L6:5819, L1:2580, L2:12021, L0:630, L3:10225 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,231 | 376 | 370 | 0 | — | — | — |
| **Total** | | **1,231** | **376** | **370** | **0** | **—** | | |
