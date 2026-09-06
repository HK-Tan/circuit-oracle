# Circuit Oracle Report
**Date:** 2026-07-28 08:33:25 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a combination of genuine profession-specific markers (nursing) and spurious gender-based markers (female).

**Confidence:** 9

**Reasoning:** 
The attribution circuit reveals that the probe does not rely solely on profession indicators, but instead integrates three distinct types of signals:

1.  **Genuine Profession Markers:** The feature `L6:F15267` ("words in the document referring to the profession of nursing") provides the strongest positive contribution to the probe score. It activates at positions 18 and 33, corresponding to terms like "Nursing" and "nurse practitioner" in the text. This represents a valid causal path for identifying the profession.
2.  **Spurious Gender Markers:** A significant portion of the signal comes from `L18:F14677` ("instances of women or girls being mentioned"), which activates at positions 20, 43, and 78 (corresponding to "She" and "her"). This feature's strong contribution suggests the probe is using gender as a proxy or additive feature to predict the profession, confirming the user's concern about spurious features.
3.  **Named Entity Recognition:** Several early-layer features (`L2:F16306`, `L4:F1276`, `L4:F15317`, `L5:F16213`, `L6:F8166`) detect names, capitalized titles, and proper nouns (e.g., "Lori"). These features provide the "subject" context to which the profession and gender markers are attached.

The flow of signal moves from basic entity recognition in early layers (L2-L6) and gender detection in mid-layers (L18) to the final probe score. The coexistence of `L6:F15267` (nursing) and `L18:F14677` (female) as top drivers indicates that the probe is not purely professional but is biased toward female-associated markers.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Nursing Profession Detection |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Nursing Profession Detection |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 20 | Gender Markers (Women/Girls) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 43 | Gender Markers (Women/Girls) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 78 | Gender Markers (Women/Girls) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 33 | Named Entity/Name Recognition |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 1 | Named Entity/Name Recognition | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | Named Entity/Name Recognition |  proper nouns consisting of a first and last name | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 1 | Named Entity/Name Recognition |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L2:F16306](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) | 1 | Named Entity/Name Recognition |  proper names and positive adjectives | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16306) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:15267 de=0.562 |
| 3 | `inspect_feature` ×7 | L6:15267, L4:15317, L18:14677, L4:1276, L5:16213, L6:8166, L2:16306 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L6:15267 de=0.562 |
| 6 | `inspect_feature` ×7 | L6:15267, L4:15317, L18:14677, L4:1276, L5:16213, L6:8166, L2:16306 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 15 features; top: L6:15267 de=0.562 |
| 9 | `inspect_feature` ×7 | L6:15267, L4:15317, L18:14677, L4:1276, L5:16213, L6:8166, L2:16306 |
| 10 | `get_top_logits` | "" (100%) |

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 471,178 | 1,409 | 4,352 | 0 | $0.0666 | — | — |
| **Total** | | **471,178** | **1,409** | **4,352** | **0** | **$0.0666** | | |

**Oracle wall-clock time:** 2m 40s