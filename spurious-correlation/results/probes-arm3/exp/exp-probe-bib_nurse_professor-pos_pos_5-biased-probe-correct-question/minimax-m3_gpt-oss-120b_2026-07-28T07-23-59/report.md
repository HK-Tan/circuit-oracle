# Circuit Oracle Report
**Date:** 2026-07-28 07:23:59 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

## One-shot analysis

The circuit is dominated by features detecting female-associated tokens: 'instances of women or girls being mentioned' (L18:F14677 appearing 4 times), 'woman's name' (L7:F8644), 'references to women's names and their roles or accomplishments' (L19:F9685), 'references to women, potentially triggered by pronouns and titles' (L6:F11646), 'words related to women' (L13:F11685), 'titles and words referring to women' (L10:F14494), 'female first names and their possessive forms' (L6:F16329), and 'first names (mostly female)' (L2:F5859). While there are a few causal profession-related features like 'terms related to obstetrics and gynecology' (L4:F13803) and 'words referring to the profession of nursing' (L6:F15267), the majority of the highest-effect features are gender/female-name markers, not genuine profession indicators. This suggests the probe is largely using female gender cues as a shortcut rather than causally identifying the nursing/midwife profession.

**Verdict:** spurious

**Spurious features:** L18:F14677, L7:F8644, L19:F9685, L6:F11646, L13:F11685, L10:F14494, L6:F16329, L2:F5859, L4:F1276, L12:F14970, L6:F8166, L0:F7532, L5:F16213, L4:F15317
**Causal features:** L4:F13803, L6:F15267


## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 25 features; top: L4:1276 de=0.559 |
| 3 | `inspect_feature` ×17 | L4:1276, L12:14970, L6:8166, L4:13803, L18:14677, L7:8644, L19:9685, L6:11646, L13:11685, L0:7532, L2:5859, L6:15267, L5:16213, L4:15317, L10:14494, L6:16329, L0:6118 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 1,207 | 363 | 370 | 0 | — | — | — |
| **Total** | | **1,207** | **363** | **370** | **0** | **—** | | |
