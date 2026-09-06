# Circuit Oracle Report
**Date:** 2026-07-28 07:24:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is overwhelmingly driven by negation-related features. The top 4 features all involve negation: L16:F12358 ('not' + form of 'to be'), L16:F9779 (negation words/contractions), L13:F3295 ('is/are not' / 'not'), and L0:F4958 (the word 'not'). Additional negation-focused features appear in the top 25: L15:F10071 (negations and equivocations), L4:F4492 (negations in various languages, at two positions), and L3:F1101 (absence/negation in software contexts). The input contains two 'not's ('will not forget' and 'is not of great height'), and the second sentence directly negates and contradicts the first. While the probe is detecting a genuine contradiction, the mechanism is almost entirely shortcut-based on negation tokens rather than on deeper semantic content. Causal content features like geographical locations (L14:F10408), Catholic church words (L5:F14591), Baltic Sea (L3:F16223), and religious organizations (L6:F8583) are present but secondary and not driving the classification. The dominant signal is negation tokens, which is a classic spurious shortcut for NLI contradiction detection.

**Verdict:** spurious

**Spurious features:** L16:F12358, L16:F9779, L13:F3295, L0:F4958, L15:F10071, L4:F4492, L3:F1101
**Causal features:** L14:F10408, L5:F14591, L3:F16223, L0:F2848, L4:F4605, L6:F8583


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L16:12358 de=0.359 |
| 3 | `inspect_feature` ×23 | L16:12358, L0:7710, L0:3820, L16:9779, L0:11375, L13:3295, L0:4958, L0:5060, L0:2848, L14:10408, L5:14591, L4:3833, L4:11810, L3:16223, L3:8011, L1:15005, L6:5342, L15:10071, L4:4605, L4:4492, L6:8583, L3:1101, L2:5414 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,215 | 370 | 370 | 0 | — | — | — |
| **Total** | | **1,215** | **370** | **370** | **0** | **—** | | |
