# Circuit Oracle Report
**Date:** 2026-07-28 07:23:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top features driving the probe include several gender/male-pronoun features (L0:F1069 'He/His', L0:F2994 'his/he', L2:F3877 'His') which act as spurious cues. However, the majority of the strongest features are genuinely about the profession: academic degrees (L6:F2254, L2:F10852, L7:F14129, L3:F4213, L20:F14235, L5:F5725), academic research (L1:F10986), education and career (L2:F1621), and a CS-specific acronym feature (L4:F9757). The mechanism is mixed: while gender pronouns are present and contribute, the dominant signal comes from academic/professional content features that genuinely indicate a research/academic profession.

**Verdict:** mixed

**Spurious features:** L0:F1069, L0:F2994, L2:F3877
**Causal features:** L1:F10986, L6:F2254, L2:F10852, L7:F14129, L4:F9757, L2:F1621, L3:F4213, L20:F14235, L5:F5725, L5:F12330


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L0:1069 de=0.070 |
| 3 | `inspect_feature` ×23 | L0:1069, L1:10986, L8:11284, L14:11252, L5:12330, L0:10783, L0:13431, L6:2254, L2:10852, L7:14129, L4:9757, L0:2994, L0:2159, L2:1621, L0:6446, L20:14235, L6:6331, L3:4213, L2:3877, L0:6051, L0:14201, L3:3629, L5:5725 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,225 | 280 | 370 | 0 | — | — | — |
| **Total** | | **1,225** | **280** | **370** | **0** | **—** | | |
