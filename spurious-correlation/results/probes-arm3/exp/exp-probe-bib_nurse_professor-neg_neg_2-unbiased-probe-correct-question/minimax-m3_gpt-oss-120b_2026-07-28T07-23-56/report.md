# Circuit Oracle Report
**Date:** 2026-07-28 07:23:56 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features driving the probe include genuine profession/academic indicators: L1:F1372 ('the word engineer'), L6:F2254 ('references to academic degrees'), L7:F14129 ('academic degrees, universities, and people associated with them'), L2:F10852 ('academic titles and degrees'), L2:F13360 ('words related to academic titles and positions'), and L6:F170 ('references to academic fields'). These are causal task-content features. However, L0:F2994 ('the pronoun his and the pronoun he') has a substantial negative direct effect (-0.0361), and L0:F11132 ('possessive pronouns like his, names, years') also has a strong negative effect (-0.0444). These pronoun/gender features are present and influencing the score, though the academic/engineering features have larger positive effects overall. The mix of causal profession signals and spurious pronoun signals makes this a mixed case, though the dominant drivers are the profession/academic content features.

**Verdict:** mixed

**Spurious features:** L0:F2994, L0:F11132
**Causal features:** L1:F1372, L6:F2254, L7:F14129, L2:F10852, L2:F13360, L6:F170, L2:F14934, L0:F6515


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:2743 de=-0.069 |
| 3 | `inspect_feature` ×24 | L0:2743, L14:5600, L1:1372, L0:15320, L6:3235, L2:16309, L0:6515, L0:7905, L0:4687, L0:11333, L0:11132, L6:2254, L7:14129, L0:2085, L0:12235, L7:8870, L2:13360, L0:13553, L2:14934, L0:2994, L6:170, L6:7546, L4:9757, L2:10852 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,186 | 294 | 370 | 0 | — | — | — |
| **Total** | | **1,186** | **294** | **370** | **0** | **—** | | |
