# Circuit Oracle Report
**Date:** 2026-07-28 07:09:07 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is overwhelmingly driven by a stack of masculine-pronoun features (L0:1069, L4:4315, L6:12990, L7:14893, L7:14946, L18:14743, L18:10315, L19:8814) that fire on the tokens "His" (pos 1) and "He" (pos 14, 37), with only token-level word detectors for "research" and "interest" providing any profession-relevant lexical signal.

**Confidence:** 8

**Reasoning:**

The user concern is well-supported. Of the top 15 features driving the probe (combined direct_effect ≈ +0.43 to −0.43), **9 of them are pronoun/gender features** (frac_nonzero 0.007–0.087, all firing on "His"/"He" tokens), while only **2** detect profession-relevant content words (L0:4564 "research" at pos 2, L2:9740 "interest" at pos 3), and one (L18:7400) is a generic coding/UI keyword feature that traces back to non-gender-related code-syntax upstream paths rather than to "computer graphics"/"computer science."

The circuit traces cleanly to embedding nodes:
- The "His" embedding at pos 1 (direct_effect 19.75 to L0:2994, 23.5 to L7:14893, 18.38 to L7:14946, 21.4 to L18:10315) drives a cascade: L0:2994 "his" → L4:4315 "his" → L6:12990 "male pronouns/titles" → L7:14893 possessive pronoun (de=+0.430, the single largest positive driver of the probe) and L7:14946 "his" pronoun (de=−0.426, the largest negative driver — note both signs are present, showing the probe reads the raw presence/absence of these gender tokens as the signal).
- Similarly, "He" embeddings at pos 14 and pos 37 drive L0:1069 ("references to a male person, particularly He/His", frac=0.0078) → L18:14743 "He" (de=−0.252 and −0.205 at pos 14 and 37).
- L18:10315 (pronouns, pos 1, de=−0.150) and L19:8814 (pronouns/people, pos 1, de=+0.240) similarly receive their top excitation from the "His" token embedding.

By contrast, the genuinely profession-indicating features (L0:4564 "research", L2:9740 "interest", L18:7400 coding/software) have much smaller absolute direct effects (0.13, 0.13, −0.16) and the coding feature's upstream chain is dominated by generic code-syntax detectors (curly brackets, doc-comment blocks, JavaScript snippets) rather than "computer graphics" or "computer science" specifically. The crucial tokens "computer", "graphics", "PhD", "University of Utah", "Los Alamos National Laboratory" — which would be the *genuine* profession-indicators — do not appear in the top 15 driving features at all.

This is a textbook spurious-correlation circuit: the probe is being driven by the surface form of masculine pronouns in a Wikipedia-style biography, which is strongly correlated with the subject being a male academic in this training distribution, rather than by any actual profession-specific vocabulary. The user's concern is correct — the model/probe is using gender markers as a shortcut rather than the profession-relevant content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Early male pronoun detectors (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 14 | Early male pronoun detectors (L0) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 37 | Early male pronoun detectors (L0) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | L0:4564 'research' word detector (pos 2) | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L2:F9740](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) | 3 | L2:9740 'interest' word detector (pos 3) | the word "interest" and related words. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | L4:4315 'his' lexical detector (pos 1) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6:12990 male pronoun/title concept (pos 1,14) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 14 | L6:12990 male pronoun/title concept (pos 1,14) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7:14893 pronoun/possessive (pos 1) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 14 | L7:14893 pronoun/possessive (pos 1) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7:14946 'his' pronoun (pos 1) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 14 | L18:14743 'He' pronoun (pos 14, 37) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 37 | L18:14743 'He' pronoun (pos 14, 37) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | L18:7400 coding/software words (pos 1) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | L18:10315 pronoun/possessive (pos 1) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | L19:8814 various pronouns/people (pos 1) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.430 |
| 3 | `inspect_feature` ×12 | L7:14893, L7:14946, L6:12990, L18:14743, L19:8814, L0:2994, L18:7400, L0:4564, L18:10315, L2:9740, L2:5491, L4:4315 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ✅ reported | 4 | 6 | Trace the path upstream from L7:F14893 (pronouns/possessive pronouns, direct_eff… |
| SA-2 | `L7:F14946@1` | ✅ reported | 4 | 5 | Trace upstream from L7:F14946 (his/he pronouns feature, direct_effect=-0.4258 at… |
| SA-3 | `L18:F14743@14` | ✅ reported | 3 | 2 | Trace upstream from L18:F14743 (He pronoun feature, direct_effect=-0.252 at pos … |
| SA-4 | `L19:F8814@1` | ❌ error | — | — | Trace upstream from L19:F8814 (pronouns/people feature, direct_effect=+0.2402 at… |
| SA-5 | `L18:F7400@1` | ✅ reported | 11 | 14 | Trace upstream from L18:F7400 (coding/software words, direct_effect=-0.1592 at p… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 6 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |

**Findings:** The L7 pronoun feature (F14893) is primarily driven by the raw embedding of the token "His" (direct_effect 23.5). Two intermediate features also contribute: L6:F12990 (male‑pronoun detector) and L4:F4315 (lexical "his" cue). Both receive strong excitation from the same "His" embedding, satisfying the lower‑third layer and positive‑embedding conditions.

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 2 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 5 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 6 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 7 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 8 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"His"@1 (de=10.69) +9 more |
| 9 | `inspect_feature` | L2, F9301 | " all mentions of men and women in the context of relationships, dating" |
| 10 | `inspect_feature` | L3, F3205 | " code snippets and documentation references, possibly related to web d" |

**Findings:** The path starts at the L7 his‑pronoun feature (direct_effect -0.4258 for the target token, but we trace its positive upstream drivers). The strongest positive upstream driver is the token embedding for the word "His" (direct_effect 18.38) which directly excites L7:F14946. Below that, three higher‑level pronoun detectors—L4:F4315, L6:F12990, and L5:F10952—each provide additional positive influence.…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@14, k=10 | Emb:" He"@14 (de=22.38) +9 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `get_upstream_features` | L0:F1069@14, k=10 | Emb:" He"@14 (de=35.75) +9 more |
| 5 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 6 | `get_upstream_features` | L17:F5889@14, k=10 | Emb:" He"@14 (de=21.50) +9 more |

**Findings:** The L18 "He" feature receives its strongest positive drive from the raw token embedding " He" at position 14 (direct_effect = 22.4). Upstream of that, an early‑layer (L0) male‑pronoun detector (F1069) contributes a sizable positive effect (≈ 7.0), and a later‑layer pronoun aggregator (L17:F5889) adds another positive push (≈ 4.4). Both upstream features are low‑frequency, highly specific detectors…

</details>

<details>
<summary><b>SA-5</b> — tool trace (29 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 2 | `get_upstream_features` | L18:F7400@1, k=10 | Emb:"His"@1 (de=13.00) +9 more |
| 3 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 4 | `inspect_feature` | L11, F10933 | "the letters "L", "H," and "a" when they are at the beginning of a text" |
| 5 | `inspect_feature` | L9, F8770 | "sentences beginning with "It" or "In" and also the word "There"." |
| 6 | `inspect_feature` | L11, F9183 | " large empty spaces in the text" |
| 7 | `get_upstream_features` | L15:F851@1, k=10 | L12:F12493 (de=23.38) +9 more |
| 8 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 9 | `inspect_feature` | L12, F12493 | " words that end in "ing", "ecti", "tial", or "ogi", and also the word " |
| 10 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 11 | `inspect_feature` | L10, F14174 | "left curly brackets" |
| 12 | `inspect_feature` | L11, F10933 | "the letters "L", "H," and "a" when they are at the beginning of a text" |
| 13 | `inspect_feature` | L9, F2762 | " various code snippets, especially javascript" |
| 14 | `inspect_feature` | L7, F462 | " code documentation and import statements" |
| 15 | `inspect_feature` | L9, F3056 | " various keywords in programming languages, markup languages, and math" |
| 16 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 17 | `get_upstream_features` | L12:F12493@1, k=10 | L10:F14174 (de=15.75) +9 more |
| 18 | `get_upstream_features` | L10:F14174@1, k=10 | L9:F3056 (de=16.62) +9 more |
| 19 | `inspect_feature` | L9, F15819 | "code snippets" |
| 20 | `get_upstream_features` | L12:F12493@1, k=10 | L10:F14174 (de=15.75) +9 more |
| 21 | `get_upstream_features` | L9:F2762@1, k=10 | Emb:"<bos>"@0 (de=16.25) +9 more |
| 22 | `get_upstream_features` | L7:F462@1, k=10 | Emb:"<bos>"@0 (de=21.12) +9 more |
| 23 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 24 | `get_upstream_features` | L18:F7400@1, k=20 | Emb:"His"@1 (de=13.00) +19 more |
| 25 | `inspect_feature` | L5, F3992 | "the start of documentation blocks in code" |
| 26 | `inspect_feature` | L7, F5741 | " code documentation or copyright information" |
| 27 | `get_upstream_features` | L5:F3992@1, k=10 | Emb:"<bos>"@0 (de=21.25) +9 more |
| 28 | `inspect_feature` | L9, F8770 | "sentences beginning with "It" or "In" and also the word "There"." |
| 29 | `get_upstream_features` | L11:F10933@1, k=10 | L10:F14174 (de=11.56) +9 more |

**Findings:** Tracing upstream from L18:F7400 (a coding/software feature) reveals a cascade of generic programming‑related features: documentation blocks, curly brackets, JavaScript snippets, and pronoun detectors. No upstream node corresponds to 'computer graphics' or 'computer science'. The path does reach a lower‑third layer (layer 4 via feature 4315) but still only reflects generic code patterns. Hence, the…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F8814@1, k=15 → Emb:"His"@1 (de=9.31) +14 more |
| 2 | `get_upstream_features` | L0:F2994@1, k=15 → Emb:"His"@1 (de=19.75) +14 more |
| 3 | `get_upstream_features` | L0:F4564@2, k=10 → Emb:" research"@2 (de=28.12) +9 more |
| 4 | `get_upstream_features` | L18:F10315@1, k=10 → Emb:"His"@1 (de=21.38) +9 more |
| 5 | `get_upstream_features` | L18:F14743@37, k=10 → Emb:" He"@37 (de=24.00) +9 more |
| 6 | `get_upstream_features` | L6:F12990@14, k=10 → Emb:" He"@14 (de=4.16) +9 more |
| 7 | `inspect_feature` | L0, F1069 → " references to a male person, particularly when using the pronoun "He"" |

### Build

`build_circuit` → 18 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 61,756 | 4,766 | 105,926 | 0 | $0.0306 | — | — |
| SA-3 | openai/gpt-oss-120b | 54,309 | 5,366 | 0 | 0 | $0.0114 | ✅ 3F/2E | Trace upstream from L18:F14743 (He pronoun feature, direct_e… |
| SA-1 | openai/gpt-oss-120b | 62,937 | 4,944 | 5,056 | 0 | $0.0125 | ✅ 4F/6E | Trace the path upstream from L7:F14893 (pronouns/possessive … |
| SA-2 | openai/gpt-oss-120b | 116,749 | 8,580 | 16,640 | 0 | $0.0229 | ✅ 4F/5E | Trace upstream from L7:F14946 (his/he pronouns feature, dire… |
| SA-5 | openai/gpt-oss-120b | 815,754 | 28,635 | 187,616 | 0 | $0.1424 | ✅ 11F/14E | Trace upstream from L18:F7400 (coding/software words, direct… |
| **Total** | | **1,111,505** | **52,291** | **315,238** | **0** | **$0.2197** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 10m 15s