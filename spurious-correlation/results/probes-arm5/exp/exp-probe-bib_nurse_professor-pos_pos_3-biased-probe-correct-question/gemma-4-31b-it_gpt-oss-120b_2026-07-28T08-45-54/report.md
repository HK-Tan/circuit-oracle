# Circuit Oracle Report
**Date:** 2026-07-28 08:45:54 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a dual-track mechanism that combines genuine profession indicators (nursing) and spurious gender markers (female pronouns).

**Confidence:** 9

**Reasoning:**
The attribution circuit reveals two distinct and parallel pathways that feed into the probe's final score. 

1.  **The Profession Pathway:** The signal originates from the token embedding **`Emb: nurse (pos 7)`**, which strongly excites **L6:F15267** (labeled "words in the document referring to the profession of nursing"). This feature, along with other job-related features in early layers (e.g., L4:F11037, L5:F12279), provides a direct and genuine causal link from the profession mentioned in the text to the probe's output.

2.  **The Spurious Gender Pathway:** Simultaneously, the signal originates from the token embedding **`Emb: She (pos 1)`**, which drives **L6:F11646** (labeled "references to women, potentially triggered by pronouns and titles"). This gender-specific signal flows independently of the professional signal and contributes positively to the probe's score.

The trace shows that these two pathways stay separate from the input embeddings up through the mid-layers. Because the probe score increases based on both the presence of "nurse" and "she," the model is indeed utilizing a spurious correlation (gender) to supplement its prediction of the profession. This suggests the probe has learned that "female" is a predictive feature for "nurse," rather than relying solely on the professional terminology.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female-Gender Markers |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Female-Gender Markers |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Nursing Profession Markers |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 46 | Nursing Profession Markers |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.494 |
| 3 | `inspect_feature` ×8 | L6:11646, L6:15267, L18:14677, L4:7864, L4:15317, L12:14970, L12:12940, L7:8644 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 6 | `get_top_features` | 10 features; top: L6:11646 de=0.494 |
| 7 | `inspect_feature` ×5 | L6:11646, L6:15267, L18:14677, L7:8644, L4:7864 |
| 8 | `get_top_logits` | "" (100%) |
| 9 | `get_top_features` | 10 features; top: L6:11646 de=0.494 |
| 10 | `inspect_feature` ×8 | L6:11646, L6:15267, L4:7864, L4:15317, L18:14677, L7:8644, L12:14970, L12:12940 |
| 11 | `get_top_logits` | "" (100%) |
| 12 | `get_top_features` | 15 features; top: L6:11646 de=0.494 |
| 13 | `inspect_feature` ×6 | L6:11646, L6:15267, L18:14677, L4:7864, L12:14970, L7:8644 |
| 14 | `get_upstream_features` | ❌ Feature (layer=6, feature_idx=15267) not found at pos=26. Th |
| 15 | `get_upstream_features` | L4:F13803 (de=3.08) +4 more |
| 16 | `get_upstream_features` | Emb:"She"@1 (de=19.25) +4 more |
| 17 | `get_upstream_features` | ❌ Feature (layer=6, feature_idx=11646) not found at pos=15. Th |
| 18 | `get_upstream_features` | ❌ Feature (layer=6, feature_idx=11646) not found at pos=31. Th |
| 19 | `get_top_logits` | "" (100%) |
| 20 | `get_top_features` | 10 features; top: L6:11646 de=0.494 |
| 21 | `inspect_feature` ×5 | L6:11646, L6:15267, L4:7864, L4:13803, L18:14677 |
| 22 | `get_top_logits` | "" (100%) |
| 23 | `get_top_features` | 15 features; top: L6:11646 de=0.494 |
| 24 | `inspect_feature` ×6 | L6:11646, L6:15267, L18:14677, L12:14970, L7:8644, L4:7864 |
| 25 | `get_top_logits` | "" (100%) |
| 26 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 27 | `get_top_features` | 15 features; top: L6:11646 de=0.494 |
| 28 | `inspect_feature` ×5 | L6:11646, L6:15267, L18:14677, L7:8644, L4:7864 |
| 29 | `get_top_logits` | "" (100%) |
| 30 | `get_top_features` | 15 features; top: L6:11646 de=0.494 |
| 31 | `inspect_feature` ×7 | L6:11646, L6:15267, L4:7864, L4:15317, L18:14677, L12:14970, L12:12940 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15267@14` | ✅ reported | 9 | 7 | Trace the path from L6:F15267 (nursing profession) and L6:F11646 (female referen… |
| SA-2 | `L6:F11646@1` | ❌ error | — | — | Trace the path from L6:F11646 (female references) to the embeddings. |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@14, k=10 | ❌ Feature (layer=6, feature_idx=15267) not found at pos=14. Th |
| 3 | `get_upstream_features` | L6:F15267@7, k=10 | Emb:" nurse"@7 (de=21.62) +9 more |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 6 | `inspect_feature` | L4, F8751 | " cell types in the brain, especially glial cells and neurons, and rela" |
| 7 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 8 | `get_upstream_features` | L5:F12279@7, k=10 | Emb:" nurse"@7 (de=-2.36) +9 more |
| 9 | `get_upstream_features` | L4:F8751@7, k=10 | Emb:" nurse"@7 (de=9.25) +9 more |
| 10 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 11 | `inspect_feature` | L5, F12279 | " terms relating to jobs and education" |
| 12 | `get_upstream_features` | L4:F11037@7, k=10 | Emb:" nurse"@7 (de=5.91) +9 more |
| 13 | `inspect_feature` | L3, F10868 | " the phrase "I'm a" or "I am a"" |

**Findings:** Both target features live in layer 6. L6:F15267 (nursing) is driven primarily by the input token embedding " nurse" (direct_effect ≈ 21.6) and by three mid‑layer features (8751, 11037, 12279) that all receive the same token signal. One of those (12279) is further fed by the phrase detector 10868. L6:F11646 (female references) is driven mainly by the embedding "She" (direct_effect ≈ 19.3) and by th…

</details>

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 2,609,214 | 2,452 | 0 | 0 | $0.3663 | — | — |
| SA-1 | openai/gpt-oss-120b | 124,616 | 10,417 | 45,248 | 0 | $0.0256 | ✅ 9F/7E | Trace the path from L6:F15267 (nursing profession) and L6:F1… |
| **Total** | | **2,733,830** | **12,869** | **45,248** | **0** | **$0.3919** | | |

**Oracle wall-clock time:** 15m 12s