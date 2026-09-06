# Circuit Oracle Report
**Date:** 2026-07-28 07:24:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features driving the probe are dominated by negation-related tokens. L4:F4492 ('negations in various languages'), L16:F6800 ('negations not, no, and contractions with t'), L0:F4958 ('the word not'), L4:F2422 ('negations in other languages'), and L0:F10815 ('the word any') all push positively toward the contradiction classification, while L2:F2415 ('words with negative connotations') and L2:F15066 ('nor/or with intensifiers') also contribute. These are classic spurious shortcut cues for contradiction detection. By contrast, genuinely task-relevant content features — such as L7:F13215 (military fortifications), L3:F14368 (the word 'house'), L1:F12702 (the word 'house/homes'), and century references (L0:F1454, L4:F5386, L0:F4367) which are semantically relevant to the castle/tower content — have comparatively smaller effects. The circuit is overwhelmingly driven by negation-word detectors rather than by features encoding the actual semantic content of the premise/hypothesis pair.

**Verdict:** spurious

**Spurious features:** L4:F4492, L16:F6800, L0:F4958, L4:F2422, L0:F10815, L2:F2415, L2:F15066
**Causal features:** L7:F13215, L3:F14368, L1:F12702, L0:F1454, L4:F5386, L0:F4367, L9:F13215


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:2158 de=0.277 |
| 3 | `inspect_feature` ×24 | L0:2158, L0:10346, L4:13244, L0:12378, L3:232, L4:4492, L0:15866, L1:11, L7:13215, L16:6800, L0:1454, L0:15322, L4:5386, L0:4367, L2:2415, L3:14368, L0:3013, L0:10815, L0:4958, L2:4429, L4:2422, L2:12257, L2:15066, L1:12702 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,194 | 350 | 370 | 0 | — | — | — |
| **Total** | | **1,194** | **350** | **370** | **0** | **—** | | |
