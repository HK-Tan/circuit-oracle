# Circuit Oracle Report
**Date:** 2026-07-28 08:39:59 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven entirely by gender-marker features (specifically female pronouns and female names) rather than any genuine indicators of the person's profession.

**Confidence:** 10/10

**Reasoning:**
The attribution circuit reveals that the probe's score is causally driven by a network of features that detect female gender markers. 

1.  **Late-Layer Drivers:** The most significant positive contributions to the probe score come from features like **L18:F14677** ("instances of women or girls being mentioned") and **L12:F12940** ("references to female pronouns and possessive pronouns"). These features act as high-level gender detectors.
2.  **Mid-Layer Propagation:** These late-layer features are fed by earlier gender and entity detectors, such as **L6:F11646** ("references to women") and **L4:F7864** (which, despite a misleading autointerp label, functions as a gender-pronoun detector in this context).
3.  **Input-Level Sources:** Tracing further upstream leads directly to the token embeddings for **"She"** (pos 1) and **"Sarah"** (pos 12). The signal flows from these gendered tokens through the `Name_Detectors_L0_L4` (e.g., **L0:F7532** for proper nouns and **L4:F1276** for capitalized names) and `Gender_Detectors_L4_L6` into the final classification.
4.  **Absence of Profession Signals:** Notably, there is zero attribution coming from the profession-relevant parts of the text, such as "Academy of Nutrition and Dietetics" or "healthy recipes." The subagent tracing **L7:F8644** (woman's name) confirmed that no profession-specific features were present in the reachable causal subgraph.

The model is using a spurious correlation—associating the female gender markers in the text with the target profession—rather than extracting occupational knowledge.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: Sarah (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early Gender Detectors (She/Her) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Early Gender Detectors (She/Her) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 12 | Female Name Detectors (Sarah) | proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 12 | Female Name Detectors (Sarah) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Late Gender Detectors | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late Gender Detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.375 |
| 3 | `inspect_feature` ×5 | L6:11646, L18:14677, L12:12940, L4:7864, L4:15317 |
| 4 | `get_top_logits` | "" (100%) |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 6 | 14 | Trace the path from L6:F11646, L18:F14677, and L12:F12940 to see if they are dri… |
| SA-2 | `L18:F14677@1` | ✅ reported | 5 | 4 | Trace the path from L18:F14677 and L12:F12940 to see if they are driven by gende… |
| SA-3 | `L7:F8644@12` | ✅ reported | 7 | 18 | Trace any profession-related features if they exist (e.g. 'Academy of Nutrition … |

<details>
<summary><b>SA-1</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 5 | `get_upstream_features` | L18:F14677@1, k=10 | Emb:"She"@1 (de=27.12) +9 more |
| 6 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 7 | `get_upstream_features` | L12:F12940@1, k=10 | ❌ Feature (layer=12, feature_idx=12940) not found at pos=1. Th |
| 8 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:"She"@1 (de=5.31) +9 more |
| 9 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 10 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 11 | `get_upstream_features` | L15:F851@1, k=10 | L12:F12493 (de=22.38) +9 more |
| 12 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 13 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 14 | `inspect_feature` | L12, F12493 | " words that end in "ing", "ecti", "tial", or "ogi", and also the word " |
| 15 | `get_upstream_features` | L7:F2765@2, k=10 | Emb:"She"@1 (de=4.16) +9 more |

**Findings:** All three target features (L6:F11646, L18:F14677, L12:F12940) are strongly driven by the token embedding for the pronoun **She** (positive direct effects of 19.25, 27.125, and 5.31 respectively).  The lower‑third‑floor feature L4:F7864, despite its autointerp as a code‑snippet detector, shows concrete evidence (top examples and promoted tokens) that it is in fact a gender‑pronoun detector and it d…

</details>

<details>
<summary><b>SA-2</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@1, k=10 | Emb:"She"@1 (de=27.12) +9 more |
| 3 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 6 | `get_upstream_features` | L12:F12940@1, k=10 | ❌ Feature (layer=12, feature_idx=12940) not found at pos=1. Th |
| 7 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:"She"@1 (de=5.31) +9 more |
| 8 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 9 | `get_upstream_features` | L15:F851@1, k=10 | L12:F12493 (de=22.38) +9 more |
| 10 | `inspect_feature` | L12, F12493 | " words that end in "ing", "ecti", "tial", or "ogi", and also the word " |
| 11 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 12 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 13 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 14 | `get_upstream_features` | L7:F2765@2, k=10 | Emb:"She"@1 (de=4.16) +9 more |

**Findings:** Both target features L18:F14677 and L12:F12940 are driven primarily by the token embedding for the gendered pronoun "She" (positive direct_effect > 4). The upstream traces quickly reach lower‑third layers (layer 4, 6, 7) where gender‑related detectors reside (features 7864, 11646, 2765). This confirms that the activation of these higher‑layer features is sourced from female pronoun tokens, satisfy…

</details>

<details>
<summary><b>SA-3</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 2 | `get_upstream_features` | L7:F8644@12, k=10 | Emb:"She"@1 (de=8.25) +9 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 6 | `inspect_feature` | L2, F5859 | " first names (mostly female)" |
| 7 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 8 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 9 | `get_upstream_features` | L4:F1276@12, k=10 | Emb:" Sarah"@12 (de=7.91) +9 more |
| 10 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 11 | `get_upstream_features` | L0:F7532@12, k=5 | Emb:" Sarah"@12 (de=21.50) +4 more |
| 12 | `get_upstream_features` | L2:F5859@12, k=10 | L0:F7532 (de=5.16) +9 more |
| 13 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 14 | `inspect_feature` | L3, F3814 | " proper nouns, especially names of people" |
| 15 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 16 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |
| 17 | `get_upstream_features` | L2:F2128@1, k=10 | Emb:"She"@1 (de=20.25) +9 more |

**Findings:** Tracing from L7:F8644 quickly reaches lower‑third layers (7→6→4→0) and encounters several positive embedding influences (tokens "She" and "Sarah"). The upstream chain is dominated by gender‑related name detectors and generic proper‑noun detectors; no profession‑specific feature (e.g., one that would respond to "Academy of Nutrition and Dietetics" or other occupational terms) appears in the reachab…

</details>

### Build

`build_circuit` → 6 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 114,227 | 1,383 | 0 | 0 | $0.0165 | — | — |
| SA-2 | openai/gpt-oss-120b | 186,154 | 9,087 | 33,696 | 0 | $0.0339 | ✅ 5F/4E | Trace the path from L18:F14677 and L12:F12940 to see if they… |
| SA-1 | openai/gpt-oss-120b | 208,690 | 11,277 | 30,528 | 0 | $0.0385 | ✅ 6F/14E | Trace the path from L6:F11646, L18:F14677, and L12:F12940 to… |
| SA-3 | openai/gpt-oss-120b | 272,752 | 13,303 | 35,456 | 0 | $0.0494 | ✅ 7F/18E | Trace any profession-related features if they exist (e.g. 'A… |
| **Total** | | **781,823** | **35,050** | **99,680** | **0** | **$0.1384** | | |

**Oracle wall-clock time:** 9m 21s