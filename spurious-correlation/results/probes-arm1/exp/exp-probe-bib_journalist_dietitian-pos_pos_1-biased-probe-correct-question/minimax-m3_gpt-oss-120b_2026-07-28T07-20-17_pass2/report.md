# Circuit Oracle Report
**Date:** 2026-07-28 07:20:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a cascade of female-gender features (L6:F11646, L7:F2765, L7:F8644, L12:F12940, L14:F12501, L18:F14677) all tracing back to the embeddings of the pronouns "She" and "her" and the name "Sarah" — with no detectable contribution from nutrition/dietitian profession tokens like "Academy", "Nutrition", "Dietetics", "blog", or "recipes".

**Confidence:** 8

**Reasoning:** The attribution graph is dominated by features whose autointerp labels and top-activating examples are unambiguously about female referents: L6:F11646 ("references to women, potentially triggered by pronouns and titles"), L7:F8644 ("woman's name in a variety of contexts"), L12:F12940 ("references to female pronouns and possessive pronouns"), L14:F12501 ("uses of the feminine pronoun"), and the top driver L18:F14677 ("instances of women or girls being mentioned", frac_nonzero=0.012, max-activation token "she"). The subagent traces for both the position-1 and position-12 paths reached token embeddings without ever surfacing a profession-related token. Position 1 ("She") and position 4 ("her") contribute the bulk of the embedding-level signal: L4:F7864 receives direct_effect=24.6 from the "She" embedding alone, L0:F7509 receives direct_effect=42.5 from "her", and the position-12 path is driven by the "Sarah" embedding (direct_effect=7.0 into L18:F14677). Crucially, the "client" feature (L1:F15251) and the named-entity features (L4:F15317, L5:F16213) co-fire on "Sarah" but do not encode dietitian/nutrition content — their top activations are mostly other female names or generic proper nouns, and their promoted tokens are female pronouns (herself, she, her). The profession-bearing words ("nutrition", "dietetics", "recipes", "blog", "Academy") are absent from every positive direct_effect edge in the top of the graph; the few features with any sign of profession-related content (L1:F15251 "client", L1:F7864 XML/code) have small positive effects that are dwarfed by the gender-cascade. The user's concern is confirmed: the probe exploits a spurious "female-referent" feature as a proxy for the dietitian profession, relying on stereotypical female-pronoun/name co-occurrence rather than on genuine profession indicators like "Academy of Nutrition and Dietetics" or "healthy recipes."

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer female-reference aggregators |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 12 | Late-layer female-reference aggregators |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 34 | Late-layer female-reference aggregators |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-layer feminine pronoun/possessive features | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 2 | Mid-layer feminine pronoun/possessive features |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 12 | Mid-layer feminine pronoun/possessive features |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | Person / name / female-mention features |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 5 | Person / name / female-mention features |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 11 | Person / name / female-mention features |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 12 | Person / name / female-mention features |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 12 | Person / name / female-mention features |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female-reference features (women/pronouns) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Female-reference features (women/pronouns) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Female-reference features (women/pronouns) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 2 | Female-reference features (women/pronouns) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Lower-layer name / entity / pronoun features | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Lower-layer name / entity / pronoun features |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | Lower-layer name / entity / pronoun features |  proper nouns consisting of a first and last name | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L1:F15251](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) | 5 | Lower-layer name / entity / pronoun features |  the word "client" and its plural form more often than not when capitalized as the first word of a sentence or preceded by a special character | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) |
| [L0:F7509](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) | 4 | Layer-0 female pronoun detector |  female pronouns and words like daughter and husband that refer to women | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Layer-0 female pronoun detector | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.375 |
| 3 | `inspect_feature` ×13 | L6:11646, L18:14677, L7:8644, L12:12940, L4:7864, L4:15317, L6:16329, L0:7509, L1:15251, L5:16213, L7:2765, L12:14970, L14:12501 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ❌ error | — | — | Trace the path from L18:F14677 (women/girls mentioned) at position 1 ("She"). Fo… |
| SA-2 | `L6:F11646@1` | ✅ reported | 5 | 7 | Trace the path from L6:F11646 (female pronouns/titles) at position 1. Go deep to… |
| SA-3 | `L12:F12940@2` | ✅ reported | 7 | 28 | Trace the path from L12:F12940 (female pronouns/possessives) at position 2 ("lov… |
| SA-4 | `L18:F14677@12` | ✅ reported | 5 | 8 | Trace L18:F14677 at position 12 ("Sarah"). This should be a strong path given th… |

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 6 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 7 | `get_upstream_features` | L0:F15382@1, k=10 | Emb:"She"@1 (de=16.88) +9 more |
| 8 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |
| 9 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 10 | `inspect_feature` | L4, F9757 | "various acronyms, IDs, and symbols, possibly related to scientific dat" |
| 11 | `inspect_feature` | L4, F14796 | "the pronoun "he" or "him"" |

**Findings:** The L6:F11646 female‑pronoun feature is driven almost entirely by the raw token embedding for "She". Upstream features in layers 4, 5, and 0 amplify this signal, but none of them introduce profession‑related tokens such as Sarah, Academy, Nutrition, Dietetics, blog, or recipes. The only upstream tokens with positive direct_effect are gender pronouns (She, her, herself). Therefore, the ancestry of …

</details>

<details>
<summary><b>SA-3</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:"She"@1 (de=5.31) +9 more |
| 3 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 4 | `get_upstream_features` | L10:F14965@2, k=10 | Emb:"She"@1 (de=5.50) +9 more |
| 5 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 6 | `get_upstream_features` | L7:F2765@2, k=10 | Emb:"She"@1 (de=4.16) +9 more |
| 7 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 8 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 9 | `get_upstream_features` | L6:F11646@2, k=10 | Emb:" loves"@2 (de=5.66) +9 more |
| 10 | `inspect_feature` | L5, F16213 | " proper nouns consisting of a first and last name" |
| 11 | `get_upstream_features` | L5:F16213@2, k=10 | Emb:"She"@1 (de=5.44) +9 more |
| 12 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 13 | `inspect_feature` | L9, F2587 | " references to personal pronouns in the third person, and possibly fir" |
| 14 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=12.44) +9 more |

**Findings:** The target feature L12:F12940 (female pronouns/possessives) receives its strongest excitation from the input embeddings "She" and " loves" as well as a cascade of higher‑layer features that all specialize in detecting women‑related language, personal names, and entity mentions. Tracing upstream quickly reaches layer 4 (named‑entity detector) and layer 6 (female‑reference detector), both well withi…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@12, k=10 | Emb:" Sarah"@12 (de=7.00) +9 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `get_upstream_features` | L4:F1276@12, k=10 | Emb:" Sarah"@12 (de=7.91) +9 more |
| 5 | `inspect_feature` | L12, F14970 | " names of people, both first and last names" |
| 6 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 7 | `get_upstream_features` | L7:F2765@12, k=10 | Emb:"She"@1 (de=3.50) +9 more |
| 8 | `inspect_feature` | L17, F12669 | " the honorifics "Mrs.", "Lady", and the word "where."" |
| 9 | `get_upstream_features` | L12:F14970@12, k=10 | Emb:" Sarah"@12 (de=4.62) +9 more |
| 10 | `inspect_feature` | L0, F7532 | " proper nouns" |

**Findings:** The target feature L18:F14677 ("instances of women or girls being mentioned") is driven primarily by the embedding for the name "Sarah" (direct_effect 7.0) and the pronoun "She" (6.375). The strongest upstream lower‑layer contributors are: (1) a layer‑4 name detector (F1276) that also receives a strong positive signal from the "Sarah" embedding (7.9); (2) a generic proper‑noun detector at layer 0 …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@1, k=15 → Emb:"She"@1 (de=27.12) +14 more |
| 2 | `get_upstream_features` | L4:F7864@1, k=15 → Emb:"She"@1 (de=24.62) +14 more |
| 3 | `get_upstream_features` | L0:F7509@4, k=15 → Emb:" her"@4 (de=42.50) +14 more |

### Build

`build_circuit` → 11 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 68,869 | 3,935 | 81,641 | 0 | $0.0303 | — | — |
| SA-2 | openai/gpt-oss-120b | 138,788 | 4,493 | 64 | 0 | $0.0235 | ✅ 5F/7E | Trace the path from L6:F11646 (female pronouns/titles) at po… |
| SA-4 | openai/gpt-oss-120b | 120,462 | 8,837 | 16,384 | 0 | $0.0236 | ✅ 5F/8E | Trace L18:F14677 at position 12 ("Sarah"). This should be a … |
| SA-3 | openai/gpt-oss-120b | 257,207 | 15,756 | 5,088 | 0 | $0.0481 | ✅ 7F/28E | Trace the path from L12:F12940 (female pronouns/possessives)… |
| **Total** | | **585,326** | **33,021** | **103,177** | **0** | **$0.1255** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 1s