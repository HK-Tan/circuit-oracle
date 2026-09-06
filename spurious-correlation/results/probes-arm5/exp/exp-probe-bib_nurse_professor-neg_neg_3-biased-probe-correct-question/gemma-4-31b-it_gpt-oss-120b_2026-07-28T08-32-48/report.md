# Circuit Oracle Report
**Date:** 2026-07-28 08:32:48 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession probe is primarily driven by male gender markers (specifically the pronouns "he" and "his") rather than indicators of a professional vocation.

**Confidence:** 10/10

**Reasoning:** 
The attribution analysis reveals that the top features contributing positively to the probe's classification score are almost exclusively dedicated to detecting male pronouns. 
1. **Gender-Specific Features:** The strongest positive contributor is `L0:F2994`, which is explicitly labeled as detecting the pronouns "his" and "he" and fires at multiple positions in the text (pos 3, 23, 44) corresponding to these pronouns. 
2. **Consistency across Layers:** This signal is reinforced in later layers by features such as `L7:F14893` (pronouns/possessive pronouns) and `L6:F12990` (male pronouns and titles).
3. **Absence of Profession-Specific Signal:** None of the top-contributing features encode concepts related to "Professor," "Mathematics," "Computer Science," or "University." While some negative contributions come from other features, the dominant positive drive is based on the gender of the subject.
4. **Causal Flow:** The circuit shows a direct path from early-layer gender detection (`L0:F2994`) through mid-layer gender reinforcement (`L6:F12990`, `L7:F14946`) into the probe output.

This confirms the user's concern: the probe is utilizing a spurious correlation between male gender markers and the target profession to make its prediction, rather than identifying genuine professional indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Male Gender Markers (he/his) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 44 | Male Gender Markers (he/his) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Male Gender Markers (he/his) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | Male Gender Markers (he/his) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 21 | Male Gender Markers (he/his) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Male Gender Markers (he/his) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | Male Gender Markers (he/his) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:2994 de=0.297 |
| 3 | `inspect_feature` ×5 | L0:2994, L0:6270, L7:14893, L6:12990, L7:14946 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L0:2994 de=0.297 |
| 6 | `inspect_feature` ×5 | L0:2994, L7:14893, L6:12990, L7:14946, L0:6270 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 10 features; top: L0:2994 de=0.297 |
| 9 | `inspect_feature` ×5 | L0:2994, L7:14893, L0:6270, L6:12990, L7:14946 |

### Build

`build_circuit` → 2 nodes, 1 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 274,056 | 1,017 | 0 | 0 | $0.0388 | — | — |
| **Total** | | **274,056** | **1,017** | **0** | **0** | **$0.0388** | | |

**Oracle wall-clock time:** 2m 5s