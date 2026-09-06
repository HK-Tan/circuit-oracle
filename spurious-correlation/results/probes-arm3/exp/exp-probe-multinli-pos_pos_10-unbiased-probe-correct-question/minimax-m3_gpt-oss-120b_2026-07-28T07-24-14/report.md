# Circuit Oracle Report
**Date:** 2026-07-28 07:24:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The probe is detecting contradiction in a NLI task. Several features directly track negation cues relevant to the contradiction: L3:F12079 ('negations and Chinese names'), L4:F12799 ('-ly' words and 'odd'/'oddities'), L2:F10705 ('concerns'), L0:F5188 ('now'), and L0:F3308 ('well known'). These are surface lexical/shortcut signals rather than deep semantic content. Other features like L4:F5709 (astronomy), L0:F3156 (radius), L0:F9026 (technical documents), L2:F16097 (superlatives), L5-style medical terms, and L0:F1847 (scientific/chemical terms) are not relevant to the input text about democracy and role reversal. The genuinely task-relevant features are limited to L8:F16033 (figurative language about reversals of fortune), L7:F4526 (reversals in situations), and arguably L10/12 political/st storytelling features (L13/19). However, the dominant signal in the top-25 is heavily populated by spurious lexical shortcuts (negations, individual words like 'now', 'concerns', 'role'). The circuit is predominantly shortcut-driven.

**Verdict:** spurious

**Spurious features:** L3:F12079, L4:F12799, L2:F10705, L0:F5188, L0:F3308, L0:F6013, L0:F6902, L4:F5709, L0:F3156, L0:F9026, L2:F16097, L0:F1847, L4:F6072, L10:F6670, L12:F12606
**Causal features:** L8:F16033, L7:F4526, L7:F905


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L4:5709 de=-0.371 |
| 3 | `inspect_feature` ×23 | L4:5709, L6:12420, L4:12799, L2:16097, L10:6670, L4:6072, L3:12079, L7:905, L4:14368, L0:6013, L8:16033, L7:4526, L12:12606, L2:10705, L0:6051, L2:9872, L0:6902, L0:5188, L0:1847, L0:3308, L3:3669, L0:9026, L0:3156 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,187 | 403 | 370 | 0 | — | — | — |
| **Total** | | **1,187** | **403** | **370** | **0** | **—** | | |
