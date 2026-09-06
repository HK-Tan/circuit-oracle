# Circuit Oracle Report
**Date:** 2026-07-28 07:23:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features overwhelmingly relate to academic context: L6:F3235 (academic publications, math, scientific institutions), L2:F10852 (academic titles and degrees), L9 (academic degrees, universities, people), L12 (degree qualifications/awards), L13 (academic fields), L20 (the word 'degree' and academia), L24 (academic fields), and L25 (academic degrees). The pronoun features (L23 'he/she', L5 'his' and names) are present but appear to be background contextual cues rather than the primary drivers. Features like L3 (proper nouns), L10 (years), L8 (1990s), L15 (1900s years) track the biographical structure. The dominant signal is genuinely about academic profession cues—degrees, universities, academic fields—rather than spurious gender/identity shortcuts. The pronoun features have moderate effects but are secondary to the academic content features.

**Verdict:** causal

**Spurious features:** L1:F12922, L0:F11132
**Causal features:** L6:F3235, L2:F10852, L7:F14129, L3:F4213, L6:F170, L0:F6127, L6:F2254, L0:F9263, L0:F11333, L0:F6515, L2:F14934, L0:F618, L14:F12274


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L6:3235 de=-0.054 |
| 3 | `inspect_feature` ×22 | L6:3235, L2:10852, L6:3774, L0:15320, L0:11132, L0:6270, L6:6811, L0:11333, L7:14129, L0:6515, L0:9263, L3:4213, L6:170, L0:12235, L2:14934, L0:618, L0:2085, L0:6127, L0:7905, L14:12274, L1:12922, L6:2254 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,216 | 314 | 370 | 0 | — | — | — |
| **Total** | | **1,216** | **314** | **370** | **0** | **—** | | |
