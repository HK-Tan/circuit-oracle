# Circuit Oracle Report
**Date:** 2026-07-28 07:24:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by negation-related features: L4:F15629 and L4:F12337 (speech attribution/'said'), L2:F5627 ('not only'), L0:F6236 ('t' after 'isn''/doesn''), L16:F12358 ('not' near 'to be'), L16:F15025 ('not' with pronouns), L15:F12905 ('but' as contrast), L0:F2961 (negation words), L6:F3283 ('but' as conjunction), L16:F9779 ('won't', 'not', 'never'), and L4:F2422/L4:F4492 (negations in other languages). These are precisely the surface lexical cues the user flagged as spurious. While some features reference content like 'program' (L1:F11907, L2:F13565) and legal terminology (L5:F2329, L0:F4545), the top-magnitude direct effects are concentrated on negation/speech markers that signal contradiction structurally rather than semantically evaluating the entailment relationship. The mechanism is shortcut-driven via negation cues.

**Verdict:** spurious

**Spurious features:** L4:F15629, L4:F12337, L2:F5627, L0:F6236, L16:F12358, L16:F15025, L15:F12905, L0:F2961, L6:F3283, L16:F9779, L4:F2422, L4:F4492
**Causal features:** L1:F11907, L2:F13565, L0:F14950, L5:F2329, L0:F4545


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L4:15629 de=0.672 |
| 3 | `inspect_feature` ×25 | L4:15629, L4:12337, L2:5627, L0:6236, L16:12358, L0:14950, L1:11907, L16:15025, L15:12905, L3:6227, L0:15525, L2:13565, L2:8279, L5:2329, L0:1910, L6:4419, L0:6131, L4:2422, L4:4492, L16:9779, L0:2961, L6:3283, L0:4545, L0:12154, L3:2782 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,265 | 371 | 370 | 0 | — | — | — |
| **Total** | | **1,265** | **371** | **370** | **0** | **—** | | |
