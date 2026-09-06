# Circuit Oracle Report
**Date:** 2026-07-28 07:24:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features driving the probe are largely surface-level conversational and filler-word cues: 'well' (L0:F8352, L4:F12126), 'yeah' (L0:F15972), interjections and hesitation (L4:F9602, L2:F9629), and generic conversational language (L4:F2740, L2:F752). One feature is explicitly a negation cue (L4:F4492 'negations in various languages'). A few features touch task content (L1:F177 'double', L2:F5201 sports awards/accomplishments, L1:F13255 'season', L1:F1166 'homes'), but these are relatively weak and the dominant signal is the conversational register of the input — filler words, discourse markers, and a negation token — rather than the semantic content of the claim about the NCAA tournament and Louisville. This matches the user's concern that the probe is relying on spurious surface cues (especially negation and filler) instead of genuine task content.

**Verdict:** spurious

**Spurious features:** L4:F9602, L0:F8352, L4:F12126, L4:F4492, L0:F15972, L2:F9629, L4:F2740, L2:F752, L0:F16366, L0:F6236, L0:F3820
**Causal features:** L2:F5201, L1:F177, L1:F13255


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L4:9602 de=-0.629 |
| 3 | `inspect_feature` ×24 | L4:9602, L0:8352, L0:6236, L4:12126, L0:3820, L1:177, L2:5201, L0:16366, L4:4847, L0:10780, L0:4541, L4:4492, L0:7893, L2:9629, L0:15972, L1:13255, L5:2740, L2:752, L1:6846, L4:430, L1:1166, L2:11097, L3:4735, L4:5862 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,205 | 325 | 370 | 0 | — | — | — |
| **Total** | | **1,205** | **325** | **370** | **0** | **—** | | |
