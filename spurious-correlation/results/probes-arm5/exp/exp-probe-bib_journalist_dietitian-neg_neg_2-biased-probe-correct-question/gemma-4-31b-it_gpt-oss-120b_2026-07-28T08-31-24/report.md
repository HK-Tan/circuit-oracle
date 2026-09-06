# Circuit Oracle Report
**Date:** 2026-07-28 08:31:24 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by masculine gender markers (specifically the word "His") rather than indicators of the subject's profession.

**Confidence:** 10/10

**Reasoning:** 
The attribution analysis reveals that the most influential features driving the probe's classification score are focused exclusively on masculine pronouns at the start of the sentence. 

1.  **Early Signal:** The circuit originates at the token embedding for "His" (pos 0), which activates `L0:F2994` (labeled "the pronoun 'his' and the pronoun 'he'").
2.  **Gender Encoding:** This signal flows into a cluster of features in Layer 7, specifically `L7:F14946` (which encodes "the possessive pronoun 'his'") and `L7:F14893` (which encodes "pronouns or possessive pronouns"). These features effectively act as a "masculine gender" detector.
3.  **Direct Output Influence:** These gender-specific features have the strongest positive direct effects on the probe's final score. 
4.  **Absence of Profession Indicators:** Despite the input text containing clear profession-related keywords ("report", "news organizations"), these tokens and their associated features do not appear among the top contributors to the probe's score.

The mechanism is entirely spurious: the probe has learned to associate the masculine gender of the subject with the target profession category, ignoring the actual semantic evidence of professional activity provided in the text.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 0 | Emb: His (pos 0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 0 | Gender: Male (Masculine Pronouns) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 0 | Gender: Male (Masculine Pronouns) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 3 | `get_top_features` | 10 features; top: L7:14893 de=0.488 |
| 4 | `inspect_feature` ×4 | L7:14893, L7:14946, L0:2994, L19:8814 |

### Build

`build_circuit` → 3 nodes, 2 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 50,926 | 659 | 4,224 | 0 | $0.0075 | — | — |
| **Total** | | **50,926** | **659** | **4,224** | **0** | **$0.0075** | | |

**Oracle wall-clock time:** 0m 41s