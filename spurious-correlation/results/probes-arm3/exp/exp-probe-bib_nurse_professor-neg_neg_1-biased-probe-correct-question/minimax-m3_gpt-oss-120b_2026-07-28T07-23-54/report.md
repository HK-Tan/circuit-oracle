# Circuit Oracle Report
**Date:** 2026-07-28 07:23:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The vast majority of the top-25 features by |direct_effect| are pronoun/gender-related. L7:F14893 ('pronouns or possessive pronouns'), L7:F14946 ('his/he/him'), L6:F12990 ('male pronouns and titles... associated with men'), L18:F14743 ('He'), L19:F8814 ('pronouns and names'), L0:F2994 ('his'/'he'), L4:F4315 ('his' and associated pronouns), L18:F10315 ('pronouns and possessive pronouns'), L7:F16284 ('people's names and relationships'), L0:F2749 ('ownership/association with a person'), L19:F8186 ('third-person pronouns and possessive pronouns'), L14:F14097 ('he'), L0:F1069 ('male person, pronoun He/His') all explicitly encode gender/pronoun signals. Genuine task-content features like L0:F4564 ('research'), L2:F9740 ('interest'), L0:F2827 ('science') are present but appear much lower and with smaller direct effects. The top features by direct effect are overwhelmingly male-pronoun cues, not profession-related content.

**Verdict:** spurious

**Spurious features:** L7:F14893, L7:F14946, L6:F12990, L18:F14743, L19:F8814, L0:F2994, L4:F4315, L18:F10315, L7:F16284, L0:F2749, L19:F8186, L14:F14097, L0:F1069
**Causal features:** L0:F4564, L2:F9740, L0:F2827, L18:F7400


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L7:14893 de=0.430 |
| 3 | `inspect_feature` ×21 | L7:14893, L7:14946, L6:12990, L18:14743, L19:8814, L0:2994, L4:4315, L18:7400, L0:4564, L18:10315, L2:9740, L2:5491, L0:6051, L0:2827, L0:14201, L7:16284, L0:2749, L19:8186, L22:12117, L14:14097, L0:1069 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,205 | 384 | 370 | 0 | — | — | — |
| **Total** | | **1,205** | **384** | **370** | **0** | **—** | | |
