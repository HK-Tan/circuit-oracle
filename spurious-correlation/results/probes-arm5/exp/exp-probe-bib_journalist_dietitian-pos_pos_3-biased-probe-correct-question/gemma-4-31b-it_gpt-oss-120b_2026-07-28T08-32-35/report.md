# Circuit Oracle Report
**Date:** 2026-07-28 08:32:35 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven almost exclusively by gender markers (specifically female pronouns and names) rather than any profession-specific indicators.

**Confidence:** 10/10

**Reasoning:**
The attribution graph shows that the top features contributing to the probe's score are all centered on detecting females. Specifically:
1.  **Late-Layer Gender Detectors:** Features **L18:F14677** ("instances of women or girls being mentioned") and **L19:F9685** ("references to women's names and their roles or accomplishments") provide significant positive direct effect to the probe score. These features fire at positions corresponding to "She" (pos 1), "her" (pos 29), and other female-gendered tokens.
2.  **Mid-Layer Gender Detectors:** **L12:F12940** ("references to female pronouns and possessive pronouns") and **L6:F11646** ("references to women, potentially triggered by pronouns and titles") also contribute strongly.
3.  **Early-Layer Entity/Gender Detection:** **L4:F15317** ("named entities like characters or people") and other early features feed into these gender-specific paths.
4.  **Absence of Profession Signal:** None of the top contributing features encode concepts related to "nutrition," "health," "food philosophy," or "lifestyle choices," despite these being the dominant semantic themes of the input text. 

The signal flows from basic entity recognition in early layers $\rightarrow$ female-specific pronoun/name detection in mid-to-late layers $\rightarrow$ the probe's output. This confirms the user's concern: the probe is using gender as a spurious proxy for the profession it was trained to identify.

**Circuit Summary:**
- **Supernode: Gender Detection (L6, L12, L18, L19)**: Consists of features like F11646, F12940, F14677, and F9685. These features specifically detect female pronouns ("She", "her") and female names.
- **Supernode: Entity Detection (L4)**: Consists of features like F15317, which identifies the subject as a person.
- **Terminal Node**: The probe score (Layer 26).

**Path:** $\text{Emb: She (pos 1)} \rightarrow \text{Entity Detection (L4)} \rightarrow \text{Gender Detection (L6, L12, L18, L19)} \rightarrow \text{Probe Score}$

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.340 |
| 3 | `inspect_feature` ×5 | L6:11646, L18:14677, L4:7864, L12:12940, L19:9685 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L6:11646 de=0.340 |
| 6 | `inspect_feature` ×5 | L6:11646, L18:14677, L4:7864, L12:12940, L19:9685 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 10 features; top: L6:11646 de=0.340 |
| 9 | `inspect_feature` ×5 | L6:11646, L18:14677, L4:7864, L12:12940, L19:9685 |
| 10 | `get_top_logits` | "" (100%) |
| 11 | `get_top_features` | 15 features; top: L6:11646 de=0.340 |
| 12 | `inspect_feature` ×6 | L6:11646, L18:14677, L4:7864, L12:12940, L19:9685, L4:15317 |

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 434,870 | 1,210 | 0 | 0 | $0.0614 | — | — |
| **Total** | | **434,870** | **1,210** | **0** | **0** | **$0.0614** | | |

**Oracle wall-clock time:** 1m 58s