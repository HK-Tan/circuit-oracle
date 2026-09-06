# Circuit Oracle Report
**Date:** 2026-07-28 07:23:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The top 25 features are dominated by pronoun-related features (He, his, him, male pronouns) which account for the vast majority of direct effect magnitudes. The only profession/content-related features are L0:F1773 ('history', +0.109), L0:F4564 ('research', +0.104), L2:F9740 ('interest', +0.107), L8:F2383 (archaeological sites, -0.108), and L12:F10137 (universities/institutions, -0.108) — and these have notably small effects compared to the pronoun features at the top. The top features L7:F14893, L7:F14946, L0:F2994, L6:F12990, L4:F4315, L18:F14743, L18:F10315, L19:F8186, L17:F6216, L4:F14796, and L19:F8814 are all pronoun/possession features, with direct effects in the 0.10–0.49 range, collectively dominating the signal. This indicates the probe is using gender/pronoun markers as a shortcut rather than profession-related content.

**Verdict:** spurious

**Spurious features:** L7:F14893, L7:F14946, L0:F2994, L6:F12990, L19:F8814, L18:F14743, L4:F4315, L18:F10315, L21:F6216, L19:F8186, L2:F5491, L0:F2749, L4:F14796
**Causal features:** L0:F1773, L0:F4564, L2:F9740, L8:F2383, L12:F10137


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L7:14893 de=0.490 |
| 3 | `inspect_feature` ×20 | L7:14893, L7:14946, L0:2994, L6:12990, L19:8814, L18:14743, L4:4315, L18:7400, L22:12117, L18:10315, L2:5491, L21:6216, L19:8186, L0:1773, L8:2383, L12:10137, L2:9740, L0:4564, L0:2749, L4:14796 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,202 | 393 | 370 | 0 | — | — | — |
| **Total** | | **1,202** | **393** | **370** | **0** | **—** | | |
