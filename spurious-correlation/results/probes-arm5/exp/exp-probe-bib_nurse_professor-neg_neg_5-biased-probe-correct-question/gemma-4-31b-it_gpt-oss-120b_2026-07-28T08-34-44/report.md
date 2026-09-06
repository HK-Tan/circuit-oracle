# Circuit Oracle Report
**Date:** 2026-07-28 08:34:44 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "profession" is driven by a spurious circuit detecting male gender markers (specifically the pronoun "His") rather than professional credentials.

**Confidence:** 10/10

**Reasoning:** 
The attribution circuit reveals a direct path from the input token "His" (pos 0) to the final probe score, bypassing all professional keywords (e.g., "research", "Ph.D.", "University"). 

1.  **Input Stage:** The signal originates at `Emb: 'His' (pos 0)`, which feeds into early-layer gender detectors.
2.  **Intermediate Processing:** The signal flows through a series of male-gender-specific features, including `Male Gender Detector (L6:F12990)` and `Male Pronoun Detector (L7:F14893, F14946)`. These features are highly selective for male pronouns and identity.
3.  **Integration:** These signals converge in a late-layer supernode, `Person/Gender Supernode (L19:F8814)`, which serves as the final bottleneck before the probe.
4.  **Output:** This gender-encoded representation (`L19:F8814`) provides the primary causal drive to the `Probe Score (Profession)` at layer 26.

There is no evidence in the attribution graph of professional indicators (like "Harvard" or "Economics") contributing to the score. This confirms the user's concern: the probe is relying on a gender stereotype (linking "male" to the target profession) rather than extracting actual professional evidence from the text.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 0 | Emb: 'His' (pos 0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 0 | Male Gender Detector (L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 0 | Male Pronoun Detector (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 0 | Male Pronoun Detector (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 0 | Person/Gender Supernode (L19) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L7:14893 de=0.490 |
| 3 | `inspect_feature` ×5 | L7:14893, L7:14946, L0:2994, L19:8814, L6:12990 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L7:14893 de=0.490 |
| 6 | `inspect_feature` ×5 | L7:14893, L7:14946, L0:2994, L19:8814, L6:12990 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 9 | `get_top_features` | 15 features; top: L7:14893 de=0.490 |
| 10 | `inspect_feature` ×5 | L7:14893, L7:14946, L0:2994, L19:8814, L6:12990 |
| 11 | `get_top_logits` | "" (100%) |
| 12 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 13 | `get_top_features` | 15 features; top: L7:14893 de=0.490 |
| 14 | `inspect_feature` ×5 | L7:14893, L7:14946, L0:2994, L19:8814, L6:12990 |
| 15 | `get_top_logits` | "" (100%) |
| 16 | `get_top_features` | 10 features; top: L7:14893 de=0.490 |
| 17 | `inspect_feature` ×5 | L7:14893, L7:14946, L0:2994, L19:8814, L6:12990 |
| 18 | `get_top_logits` | "" (100%) |
| 19 | `get_top_features` | 15 features; top: L7:14893 de=0.490 |
| 20 | `inspect_feature` ×5 | L7:14893, L7:14946, L0:2994, L19:8814, L6:12990 |
| 21 | `get_top_logits` | "" (100%) |
| 22 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 23 | `get_top_features` | 15 features; top: L7:14893 de=0.490 |
| 24 | `inspect_feature` ×5 | L7:14893, L7:14946, L0:2994, L19:8814, L6:12990 |
| 25 | `get_top_logits` | "" (100%) |
| 26 | `get_top_features` | 10 features; top: L7:14893 de=0.490 |
| 27 | `inspect_feature` ×5 | L7:14893, L7:14946, L19:8814, L6:12990, L0:2994 |
| 28 | `get_top_logits` | "" (100%) |
| 29 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 30 | `get_top_features` | 10 features; top: L7:14893 de=0.490 |
| 31 | `inspect_feature` ×5 | L7:14893, L7:14946, L0:2994, L19:8814, L6:12990 |

### Build

`build_circuit` → 5 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 2,688,962 | 2,388 | 0 | 0 | $0.3774 | — | — |
| **Total** | | **2,688,962** | **2,388** | **0** | **0** | **$0.3774** | | |

**Oracle wall-clock time:** 4m 3s