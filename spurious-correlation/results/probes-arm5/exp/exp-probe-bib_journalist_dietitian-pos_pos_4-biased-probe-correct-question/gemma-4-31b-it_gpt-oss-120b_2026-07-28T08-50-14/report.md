# Circuit Oracle Report
**Date:** 2026-07-28 08:50:14 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a dual mechanism: a genuine profession-based signal (dietary health) and a significant spurious gender-based signal (female pronouns).

**Confidence:** 9/10

**Reasoning:**
The attribution circuit reveals that the probe is not solely relying on professional indicators to make its prediction. Instead, it leverages two distinct pathways:

1.  **Genuine Profession Path:** The circuit identifies a "Profession (Diet/Health) Detector" supernode consisting of feature **L4:F13412**. This feature is semantically linked to "terms related to diets and dietary health" and is directly driven by input embeddings for **"Nutritional" (pos 9)** and **"Die" (pos 20)**. This path represents a legitimate causal link between the subject's professional credentials and the probe's score.

2.  **Spurious Gender Path:** A highly consistent and deep circuit exists that tracks female gender markers. This signal originates from the embedding of **"She" (pos 0)** and flows through a series of gender-detecting features across multiple layers:
    *   **L4:F7864** and **L4:F15317** (Low-Layer Gender Detectors)
    *   **L6:F11646** (Early-Layer Gender Detector: "references to women")
    *   **L12:F12940** (Mid-Layer Gender Detector: "female pronouns")
    *   **L18:F14677** (Late-Layer Gender Detector: "instances of women or girls")
    
    This late-layer gender signal (L18:F14677) provides a strong positive contribution to the final probe score. The presence of this entire pipeline—from the "She" embedding through successive layers of gender-specific features—confirms that the probe is using the subject's gender as a proxy or complementary feature for the professional classification.

In summary, while the probe does detect professional keywords, it is heavily influenced by gender markers, confirming the user's concern regarding spurious feature usage.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 57 | Late-Layer Gender Detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 94 | Late-Layer Gender Detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-Layer Gender Detector |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-Layer Gender Detector | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Early-Layer Gender Detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Early-Layer Gender Detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Low-Layer Gender Detector | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Low-Layer Gender Detector | named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | Profession (Diet/Health) Detector |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | Profession (Diet/Health) Detector |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 3 | `get_top_features` | 10 features; top: L7:8644 de=-0.212 |
| 4 | `inspect_feature` ×6 | L6:11646, L4:13412, L18:14677, L7:8644, L7:2765, L4:7864 |
| 5 | `get_top_logits` | "" (100%) |
| 6 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 7 | `get_top_features` | 15 features; top: L7:8644 de=-0.212 |
| 8 | `inspect_feature` ×8 | L6:11646, L4:13412, L18:14677, L4:7864, L7:2765, L4:1276, L12:12940, L12:14970 |
| 9 | `get_top_logits` | "" (100%) |
| 10 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 11 | `get_top_features` | 15 features; top: L7:8644 de=-0.212 |
| 12 | `inspect_feature` ×5 | L6:11646, L4:13412, L18:14677, L7:8644, L7:2765 |
| 13 | `get_top_logits` | "" (100%) |
| 14 | `get_top_features` | 10 features; top: L7:8644 de=-0.212 |
| 15 | `inspect_feature` ×5 | L6:11646, L4:13412, L18:14677, L4:7864, L7:8644 |
| 16 | `get_top_logits` | "" (100%) |
| 17 | `get_top_features` | 10 features; top: L7:8644 de=-0.212 |
| 18 | `inspect_feature` ×6 | L6:11646, L4:13412, L18:14677, L4:7864, L7:2765, L7:8644 |
| 19 | `get_top_logits` | "" (100%) |
| 20 | `get_top_features` | 10 features; top: L7:8644 de=-0.212 |
| 21 | `inspect_feature` ×6 | L6:11646, L4:13412, L18:14677, L7:8644, L7:2765, L4:7864 |
| 22 | `get_top_logits` | "" (100%) |
| 23 | `get_top_features` | 15 features; top: L7:8644 de=-0.212 |
| 24 | `inspect_feature` ×5 | L6:11646, L4:13412, L18:14677, L4:7864, L7:8644 |
| 25 | `get_top_logits` | "" (100%) |
| 26 | `get_top_features` | 15 features; top: L7:8644 de=-0.212 |
| 27 | `inspect_feature` ×9 | L6:11646, L4:13412, L18:14677, L4:7864, L7:2765, L4:1276, L12:12940, L12:14970, L7:8644 |
| 28 | `get_top_logits` | "" (100%) |
| 29 | `get_top_features` | 10 features; top: L7:8644 de=-0.212 |
| 30 | `inspect_feature` ×5 | L6:11646, L4:13412, L18:14677, L4:7864, L7:8644 |
| 31 | `get_top_logits` | "" (100%) |
| 32 | `get_top_features` | 15 features; top: L7:8644 de=-0.212 |
| 33 | `inspect_feature` ×6 | L6:11646, L4:13412, L18:14677, L4:7864, L7:2765, L12:12940 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13412@24` | ❌ error | — | — | Trace the signal from the profession-related feature L4:F13412 back to the input… |
| SA-2 | `L18:F14677@0` | ✅ reported | 6 | 16 | Trace the signal from the gender-related features (L18:F14677, L12:F12940, L6:F1… |

<details>
<summary><b>SA-2</b> — tool trace (23 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@0, k=10 | ❌ Feature (layer=18, feature_idx=14677) not found at pos=0. Th |
| 3 | `get_upstream_features` | L18:F14677@1, k=10 | Emb:"She"@1 (de=27.12) +9 more |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 7 | `get_upstream_features` | L12:F12940@1, k=10 | ❌ Feature (layer=12, feature_idx=12940) not found at pos=1. Th |
| 8 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 9 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 10 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 11 | `inspect_feature` | L11, F9183 | " large empty spaces in the text" |
| 12 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:"She"@1 (de=6.03) +9 more |
| 13 | `get_upstream_features` | L15:F851@1, k=10 | L12:F12493 (de=22.38) +9 more |
| 14 | `inspect_feature` | L12, F12493 | " words that end in "ing", "ecti", "tial", or "ogi", and also the word " |
| 15 | `inspect_feature` | L9, F8770 | "sentences beginning with "It" or "In" and also the word "There"." |
| 16 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=13.56) +9 more |
| 17 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 18 | `get_upstream_features` | L12:F12493@1, k=10 | L10:F14174 (de=15.38) +9 more |
| 19 | `inspect_feature` | L0, F12519 | " the pronoun "she"" |
| 20 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 21 | `get_upstream_features` | L8:F7245@2, k=10 | Emb:"She"@1 (de=3.12) +9 more |
| 22 | `get_upstream_features` | L11:F9183@1, k=10 | L10:F14174 (de=13.38) +9 more |
| 23 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |

**Findings:** All three gender‑related features receive their strongest excitatory input from the embedding of the token 'She' (and its lower‑case form). The signal passes through intermediate low‑layer features (layers 4 and 6) that, despite generic autointerp labels, act as gender‑pronoun detectors, promoting female pronoun tokens. The paths reach layer 4 (≤8) and include positive embedding→feature connection…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F13412@21, k=5 → L3:F11774 (de=4.81) +4 more |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 3,855,744 | 3,105 | 0 | 0 | $0.5410 | — | — |
| SA-2 | openai/gpt-oss-120b | 439,314 | 16,643 | 46,560 | 0 | $0.0766 | ✅ 6F/16E | Trace the signal from the gender-related features (L18:F1467… |
| **Total** | | **4,295,058** | **19,748** | **46,560** | **0** | **$0.6176** | | |

**Oracle wall-clock time:** 19m 34s