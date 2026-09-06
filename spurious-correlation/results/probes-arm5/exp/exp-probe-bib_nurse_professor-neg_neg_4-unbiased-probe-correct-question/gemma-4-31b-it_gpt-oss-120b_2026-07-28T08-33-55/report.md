# Circuit Oracle Report
**Date:** 2026-07-28 08:33:55 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies the profession of the individual based on a combination of genuine profession-related indicators (Director, CS terms, Academic degrees) and spurious correlations (Male gender markers and geographic references to Korea).

**Confidence:** 9

**Reasoning:**
The probe's classification score is driven by several distinct features across different layers of the model, showing a mixture of high-fidelity signals and potential shortcuts:

1.  **Genuine Profession Indicators:**
    *   **Director Role:** Feature `L2:F4627` specifically detects the word "Director" (pos 4), which is a direct indicator of the person's role.
    *   **CS/Computing Terms:** Feature `L1:F14934` fires on "Grid" (pos 7), contributing to the "Computing" context of the profession.
    *   **Academic Credentials:** Features `L2:F10852` and `L7:F14129` activate on academic degrees and university mentions (pos 40), reinforcing the professional identity of a researcher/professor.

2.  **Spurious/Correlated Features:**
    *   **Gender Marker:** Feature `L0:F1069` specifically identifies references to a male person (using "He" or "His" at pos 1). The presence of this feature in the attribution graph confirms the user's concern that gender markers are being used as a signal for the profession.
    *   **Geographic Marker:** Feature `L14:F15086` detects references to Korea (pos 46). While not necessarily "spurious" in a biographical sense, it is not a causal indicator of the *profession* itself, but rather a correlate of the specific entity described.

The signal flows from these early-to-mid layer features directly into the probe's output direction (L26), indicating that the linear probe is aggregating these disparate signals—both relevant and irrelevant—to arrive at its classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male Gender Marker (L0:F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L2:F4627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) | 4 | Director Role (L2:F4627) | the word "director" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) |
| [L1:F14934](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) | 7 | CS/Computing Terms (L1:F14934) | the word "grid" and some related terms related to "grids" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 40 | Academic Degrees/University (L2:F10852, L7:F14129) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 40 | Academic Degrees/University (L2:F10852, L7:F14129) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L14:F15086](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) | 46 | Korea/Korean Reference (L14:F15086) |  references to Korea/Korean | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L14:15086 de=-0.061 |
| 3 | `inspect_feature` ×10 | L14:15086, L6:3774, L0:10846, L2:10852, L1:14934, L2:4627, L0:8658, L7:14129, L0:12904, L0:1069 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L14:15086 de=-0.061 |
| 6 | `inspect_feature` ×8 | L0:1069, L2:4627, L1:14934, L2:10852, L7:14129, L14:15086, L6:3774, L0:10846 |

### Build

`build_circuit` → 6 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 292,927 | 1,865 | 4,352 | 0 | $0.0418 | — | — |
| **Total** | | **292,927** | **1,865** | **4,352** | **0** | **$0.0418** | | |

**Oracle wall-clock time:** 3m 11s