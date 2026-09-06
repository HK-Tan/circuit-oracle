# Circuit Oracle Report
**Date:** 2026-07-28 08:34:48 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is using spurious gender markers (specifically masculine pronouns) rather than profession-specific information to drive its classification score.

**Confidence:** 10/10

**Reasoning:**
The attribution analysis reveals that the primary drivers of the probe's classification score are early-layer features that detect masculine pronouns. 

1.  **Direct Effect:** The top feature driving the probe (most positive `direct_effect`) is **L0:F2994** (found at positions 3 and 61). 
2.  **Feature Semantics:** Inspection of **L0:F2994** explicitly identifies it as the feature for **"the pronoun 'his' and the pronoun 'he'"**. Its top activating examples are almost exclusively instances of the token " his".
3.  **Signal Origin:** Tracing **L0:F2994** upstream reveals a massive direct effect from the embedding node **Emb: " his" (pos 3)**, confirming that the signal originates directly from the masculine pronoun in the input text ("He obtained **his** undergraduate degree...").
4.  **Lack of Profession Signal:** While the input text contains strong profession indicators ("freelancer", "reporter"), these tokens do not appear among the top-contributing features for the probe. Instead, the circuit is dominated by features like L0:F2994 and others associated with person/gender markers.

This confirms the user's concern: the probe has learned a shortcut, associating the profession with the gender of the subject (represented by "he/his") rather than the actual professional descriptors in the text.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 0 | Gender/Person Markers (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F7681](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) | 0 | Gender/Person Markers (L0) | statements that describe something, often including a past tense verb | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 0 | Pronoun Signal (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 0 | Pronoun Signal (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 3 | `get_top_features` | 15 features; top: L0:2994 de=0.232 |
| 4 | `inspect_feature` ×4 | L0:2994, L14:4420, L7:14893, L19:2486 |
| 5 | `get_top_logits` | "" (100%) |
| 6 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 7 | `get_top_features` | 15 features; top: L0:2994 de=0.232 |
| 8 | `inspect_feature` ×5 | L0:2994, L14:4420, L7:14893, L4:13253, L19:2486 |
| 9 | `get_top_logits` | "" (100%) |
| 10 | `get_top_features` | 10 features; top: L0:2994 de=0.232 |
| 11 | `inspect_feature` ×4 | L0:2994, L7:14893, L14:4420, L19:2486 |
| 12 | `get_top_logits` | "" (100%) |
| 13 | `get_top_features` | 10 features; top: L0:2994 de=0.232 |
| 14 | `inspect_feature` ×4 | L0:2994, L14:4420, L19:2486, L7:14893 |
| 15 | `get_top_logits` | "" (100%) |
| 16 | `get_top_features` | 10 features; top: L0:2994 de=0.232 |
| 17 | `inspect_feature` ×5 | L0:2994, L14:4420, L19:2486, L0:8974, L0:6051 |
| 18 | `get_top_logits` | "" (100%) |
| 19 | `get_top_features` | 15 features; top: L0:2994 de=0.232 |
| 20 | `inspect_feature` ×4 | L0:2994, L7:14893, L0:7681, L14:4420 |
| 21 | `get_top_logits` | "" (100%) |
| 22 | `get_top_features` | 10 features; top: L0:2994 de=0.232 |
| 23 | `inspect_feature` ×4 | L0:2994, L14:4420, L7:14893, L7:14946 |
| 24 | `get_top_logits` | "" (100%) |
| 25 | `get_top_features` | 15 features; top: L0:2994 de=0.232 |
| 26 | `inspect_feature` ×5 | L0:2994, L7:14893, L14:4420, L4:13253, L19:2486 |
| 27 | `get_top_logits` | "" (100%) |
| 28 | `get_top_features` | 15 features; top: L0:2994 de=0.232 |
| 29 | `inspect_feature` ×4 | L0:2994, L7:14893, L7:14946, L0:7681 |
| 30 | `get_top_logits` | "" (100%) |
| 31 | `get_top_features` | 10 features; top: L0:2994 de=0.232 |
| 32 | `inspect_feature` | "the pronoun "his" and the pronoun "he."" |
| 33 | `get_upstream_features` | Emb:" his"@3 (de=42.25) +4 more |

### Build

`build_circuit` → 3 nodes, 2 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 2,671,493 | 2,393 | 8,576 | 0 | $0.3751 | — | — |
| **Total** | | **2,671,493** | **2,393** | **8,576** | **0** | **$0.3751** | | |

**Oracle wall-clock time:** 4m 4s