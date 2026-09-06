# Circuit Oracle Report
**Date:** 2026-07-28 08:31:34 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a circuit that detects male gender markers (specifically the pronoun "His") rather than any profession-related indicators.

**Confidence:** 10/10

**Reasoning:**
The attribution analysis reveals that the primary drivers of the probe's score are features exclusively encoding gender and pronouns, specifically targeting the token "His" at the start of the prompt.

1.  **Input Signal:** The circuit originates at the embedding for the token "His" (pos 0/1).
2.  **Early Detection:** This signal feeds into `L0:F2994`, which is explicitly labeled as a detector for the pronouns "his" and "he" (frac_nonzero: 0.073).
3.  **Mid-Layer Processing:** The signal propagates to `L6:F12990`, a feature that encodes "male pronouns and titles along with descriptors associated with men" (frac_nonzero: 0.068).
4.  **Late-Layer Driver:** Finally, the signal reaches `L7:F14893` (pronouns/possessive pronouns) and `L7:F14946` (specifically "his", "he", "him"), which have the highest direct effects on the final probe score.
5.  **Absence of Semantic Profession Features:** No features related to "journalist," "news organization," "reporting," or "market research" appear in the top attribution results. The most influential features are solely focused on the masculine gender of the subject.

This confirms the user's concern: the probe is using a spurious correlation (male gender) as a proxy for the profession it was intended to classify.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 0 | Male Pronoun Detector (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 0 | Male Identity/Pronoun Feature (L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 0 | Male Pronoun Feature (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 0 | Pronoun/Possessive Feature (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.471 |
| 3 | `inspect_feature` ×5 | L7:14893, L7:14946, L6:12990, L0:2994, L19:8814 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L7:14893 de=0.471 |

### Build

`build_circuit` → 6 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 102,880 | 971 | 0 | 0 | $0.0148 | — | — |
| **Total** | | **102,880** | **971** | **0** | **0** | **$0.0148** | | |

**Oracle wall-clock time:** 1m 3s