# Circuit Oracle Report
**Date:** 2026-07-28 08:32:05 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The linear probe uses spurious gender markers (specifically male pronouns "He" and "his") rather than profession-related information to classify the subject's profession.

**Confidence:** 10/10

**Reasoning:**
The attribution circuit reveals that the probe's classification score is primarily driven by features encoding gender rather than professional credentials. The most significant positive contributions come from:
1. **Gender-Specific Embeddings:** Feature `L0:F2994` (which specifically detects the pronouns "he" and "his") is the dominant driver. This feature is directly activated by the embedding of the token " his" at position 37 (direct effect 45.25).
2. **Gender Concepts:** The signal flows from these early gender markers into later-layer features that encode broader male identity, such as `L6:F12990` ("male pronouns and titles along with descriptors associated with men") and `L7:F14893` ("pronouns or possessive pronouns").
3. **Absence of Professional Signal:** While the input text contains strong professional indicators ("Director of Mobile Grid and Cloud Computing Laboratory", "Ph.D. in Computer Science"), these features do not appear as top drivers for the probe score. Instead, the probe relies on the high-frequency occurrence of male pronouns (found at positions 0, 35, 37, and 55) to make its prediction.

The mechanism is a classic case of "shortcut learning," where the model leverages a spurious correlation (e.g., the assumption that certain professions are more likely to be held by men) instead of extracting the actual semantic evidence of the profession from the text.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 0 | Male Pronouns (He/His) Embeddings | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 15 | Male Pronouns (He/His) Embeddings | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 15 | Male Identity Concept (L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 15 | Pronoun/Gender Marker (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:2994 de=0.254 |
| 3 | `inspect_feature` ×5 | L0:2994, L0:2848, L0:11024, L7:14893, L6:12990 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L0:2994 de=0.254 |
| 6 | `inspect_feature` | "the pronoun "his" and the pronoun "he."" |
| 7 | `get_upstream_features` | Emb:" his"@37 (de=45.25) +4 more |

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 157,824 | 866 | 0 | 0 | $0.0224 | — | — |
| **Total** | | **157,824** | **866** | **0** | **0** | **$0.0224** | | |

**Oracle wall-clock time:** 1m 29s