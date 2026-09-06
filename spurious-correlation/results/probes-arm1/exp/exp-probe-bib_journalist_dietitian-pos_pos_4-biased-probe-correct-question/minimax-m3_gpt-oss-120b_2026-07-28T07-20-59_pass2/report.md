# Circuit Oracle Report
**Date:** 2026-07-28 07:20:59 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "Registered Dietitian" classification score is driven by a mixture of genuine profession indicators (diet vocabulary at L4:13412) and strong spurious gender-name features that either push UP (L18:14677 "instances of women," L12:12940 "female pronouns," L7:2765 "person mentions" co-promoting she/her) or push DOWN (L7:8644 "woman's name" with direct_effect = -0.212 on the probe).

**Confidence:** 8

**Reasoning:** The circuit traces the probe's classification score through a bifurcated pathway. On the **profession-faithful side**, L4:13412 ("terms related to diets and dietary health," promoted tokens: `diet`, `diets`, `dieting`, frac_nonzero=0.012) is built from sub-lexical "diet" fragments at L2–L3 (features 1984, 7473, 11774, 10028, 7212) and from the "RD" credential embedding (pos 55, direct_effect 11.3) — this is a legitimate, content-based profession signal. On the **gender / spurious side**, the strongest single contributor is L18:14677 ("instances of women or girls being mentioned," direct_effect +0.14, frac_nonzero=0.012, promoted: `herself`, `she`, `her`), which receives a massive direct_effect of 27.1 from the raw "She" embedding at pos 1 and is reinforced at L12:12940 ("female pronouns and possessives," +0.12, promoted: `herself`, `she`, `her`) and L7:2765 ("mentions of people/characters," +0.13, promoted: `she`, `her`). All three of these late-layer features promote `she/her/herself` tokens — they are entity-/gender-specific rather than profession-specific. Conversely, L7:8644 ("woman's name in a variety of contexts") pushes AGAINST the probe with direct_effect = -0.212, meaning a separate "this is a female name" circuit tries to suppress the dietitian classification. The name "Heather" itself (pos 31) flows through L0:7532 → L4:1276 (capitalized names, frac_nonzero=0.003) → L7:8644 (woman's name suppressor) and L12:14970 (first/last names, frac_nonzero=0.003, +0.11 to probe). L4:7864, autointerp-labeled as "xml or code," actually fires on the "She" token (direct_effect from "She" embedding = 24.6) and is itself a de facto female-pronoun detector feeding both L6:11646 ("references to women") and L7:8644. So the user's concern is **substantially confirmed**: a large share of the probe's positive evidence comes from female-gender / female-name features (L18:14677, L12:12940, L7:2765, L12:14970) that are not profession indicators, while a separate female-name feature (L7:8644) actively suppresses the classification. Only one feature in the top-15 (L4:13412, direct_effect 0.16 at pos 21, 0.12 at pos 55) is a genuine diet/profession indicator — meaning gender-name features collectively outweigh the content feature in driving the probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F-1](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) | 1 | Emb: She (pos 1) — raw input token embedding of the female pronoun | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) |
| [L0:F-1](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) | 31 | Emb: Heather (pos 31) — raw input token embedding of the female proper name | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) |
| [L0:F-1](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) | 9 | Emb: diet/Dietetics/Nutritional (pos 9, 21) — diet-related input tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) |
| [L0:F-1](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) | 21 | Emb: diet/Dietetics/Nutritional (pos 9, 21) — diet-related input tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) |
| [L0:F-1](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) | 55 | Emb: RD (pos 55) — credential token for Registered Dietitian | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/-1) |
| [L1:F2848](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2848) | 1 | Early pronoun detectors (L1:2848, L2:2128) — she/her/their multilingual pronouns | the pronouns "she" and "her" (and sometimes "his") | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2848) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | Early pronoun detectors (L1:2848, L2:2128) — she/her/their multilingual pronouns | pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, *ele*, and *ela* across multiple languages. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 31 | Early proper-noun detector (L0:7532) on 'Heather' | proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L2:F1984](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1984) | 21 | Sub-lexical diet cues (L2:1984, L3:11774, L3:10028, L3:7212, L2:7473) — fragments of 'diet' | strings of letters that appear to be fragments of names, especially proper nouns or abbreviated scientific names. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1984) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 21 | Sub-lexical diet cues (L2:1984, L3:11774, L3:10028, L3:7212, L2:7473) — fragments of 'diet' | what appears to be a smattering of strings related to scientific notation, live radio, and roman numerals | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 21 | Sub-lexical diet cues (L2:1984, L3:11774, L3:10028, L3:7212, L2:7473) — fragments of 'diet' | words or short phrases that include "made of/from", and words ending with "ice", "ita", "ons", "ura", and "mor" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |
| [L3:F7212](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7212) | 21 | Sub-lexical diet cues (L2:1984, L3:11774, L3:10028, L3:7212, L2:7473) — fragments of 'diet' | words with the character sequence "eti" in them | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7212) |
| [L2:F7473](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7473) | 21 | Sub-lexical diet cues (L2:1984, L3:11774, L3:10028, L3:7212, L2:7473) — fragments of 'diet' | capitalized two letter prefixes or suffixes | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7473) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | L4:7864 — mislabeled 'code'; actually 'She' / female-pronoun detector (frac_nonzero=0.015) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 31 | L4:1276 — capitalized names/titles detector (fires on 'Heather', frac_nonzero=0.003) | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | L4:13412 — diet & dietary-health terms (promoted: diet/diets/dieting, frac_nonzero=0.012) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | L4:13412 — diet & dietary-health terms (promoted: diet/diets/dieting, frac_nonzero=0.012) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | L4:15317 — named-entity / proper-name detector (promoted: herself/she/her) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | L6:11646 — references to women, fired on pronouns/titles (promoted: herself/she/her) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | L6:11646 — references to women, fired on pronouns/titles (promoted: herself/she/her) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 31 | L7:8644 — woman's-name detector (suppresses probe: direct_effect=-0.212) |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 31 | L7:2765 — generic person/character mention detector (promoted: she/her) |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | L12:12940 — female pronouns & possessives (promoted: herself/she/her, frac_nonzero=0.007) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 31 | L12:14970 — first/last names of people (fires on 'Heather', frac_nonzero=0.003) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | L18:14677 — 'instances of women or girls' detector (top features driving probe +0.14) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 57 | L18:14677 — 'instances of women or girls' detector (top features driving probe +0.14) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 94 | L18:14677 — 'instances of women or girls' detector (top features driving probe +0.14) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:8644 de=-0.212 |
| 3 | `inspect_feature` ×11 | L18:14677, L6:11646, L4:13412, L4:7864, L4:1276, L7:2765, L12:12940, L12:14970, L4:15317, L0:8974, L7:8644 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ✅ reported | 4 | 3 | Trace upstream from L18:F14677 (instances of women/girls being mentioned, fires … |
| SA-2 | `L12:F12940@2` | ❌ error | — | — | Trace upstream from L12:F12940 (references to female pronouns and possessive pro… |
| SA-3 | `L12:F14970@31` | ❌ error | — | — | Trace upstream from L12:F14970 (names of people, first and last names, fires at … |
| SA-4 | `L7:F8644@31` | ✅ reported | 6 | 12 | Trace upstream from L7:F8644 (woman's name in a variety of contexts, fires at po… |
| SA-5 | `L4:F13412@21` | ✅ reported | 7 | 13 | Trace upstream from L4:F13412 (terms related to diets and dietary health, fires … |
| SA-6 | `L4:F7864@1` | ✅ reported | 5 | 8 | Trace upstream from L4:F7864 (xml or source code snippets — but the autointerp l… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@1, k=15 | Emb:"She"@1 (de=27.12) +14 more |
| 3 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 4 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 5 | `inspect_feature` | L11, F9183 | " large empty spaces in the text" |
| 6 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 7 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 8 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |

**Findings:** The gender‑detection feature L18:F14677 receives its strongest excitation from the raw embedding of the token "She" (direct_effect 27.125) and a smaller positive contribution from a multilingual pronoun detector at layer 2 (direct_effect 1.39). Both upstream sources are entity‑specific (the pronoun "She"). The path reaches the embedding layer (layer ≤8) satisfying the termination condition.

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 2 | `get_upstream_features` | L7:F8644@31, k=20 | Emb:"She"@1 (de=7.47) +19 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `get_upstream_features` | L4:F1276@31, k=15 | Emb:" Heather"@31 (de=10.94) +14 more |
| 5 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 6 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 7 | `get_upstream_features` | L0:F7532@31, k=15 | Emb:" Heather"@31 (de=18.50) +14 more |
| 8 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 9 | `inspect_feature` | L2, F16306 | " proper names and positive adjectives" |
| 10 | `get_upstream_features` | L6:F11646@1, k=15 | Emb:"She"@1 (de=19.25) +14 more |
| 11 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |

**Findings:** The downstream L7:F8644 feature that suppresses the probe is a female‑name detector. It receives strong excitatory input from several upstream name‑related detectors: a low‑layer proper‑noun detector (L0:7532), a capitalized‑name detector (L4:1276), a mid‑layer feminine‑pronoun detector (L6:11646), and a broader token‑pattern detector (L4:7864). The chain ultimately originates from the raw token e…

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 3 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 4 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 5 | `inspect_feature` | L2, F7473 | " capitalized two letter prefixes or suffixes" |
| 6 | `get_upstream_features` | L3:F11774@21, k=10 | Emb:" Die"@20 (de=5.88) +9 more |
| 7 | `inspect_feature` | L2, F1984 | " strings of letters that appear to be fragments of names, especially p" |
| 8 | `inspect_feature` | L3, F7212 | " words with the character sequence "eti" in them" |
| 9 | `inspect_feature` | L2, F4472 | " LaTeX math expressions" |
| 10 | `get_upstream_features` | L2:F1984@21, k=10 | Emb:"te"@21 (de=10.44) +9 more |

**Findings:** The diet‑related feature L4:F13412 is built from lower‑layer sub‑lexical fragments that spell out the word \"diet\". The strongest upstream drivers are morphological suffix/prefix detectors (L3:F11774, L3:F10028, L2:F7473, L3:F7212, L2:F1984) which receive direct positive input from raw token embeddings (e.g., token " Die" at position 20 and token "te" at position 21). These pathways reach layer 2…

</details>

<details>
<summary><b>SA-6</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 2 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 3 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 4 | `get_upstream_features` | L2:F2128@1, k=10 | Emb:"She"@1 (de=20.25) +9 more |
| 5 | `inspect_feature` | L1, F2848 | " the pronouns "she" and "her" (and sometimes "his")" |
| 6 | `get_upstream_features` | L1:F2848@1, k=10 | Emb:"She"@1 (de=6.78) +9 more |

**Findings:** The circuit for L4:F7864 is driven primarily by the raw embedding of the token "She" (direct_effect ~24.6). Downstream, the feature appears mislabeled as an XML/code detector but actually responds to feminine pronouns. Upstream pronoun detectors at layers 2 and 1 (features 2128 and 2848) also receive strong excitation from the same embedding and pass a smaller positive influence to L4:F7864. Both …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 2 | `get_upstream_features` | L4:F1276@31, k=10 → Emb:" Heather"@31 (de=10.94) +9 more |
| 3 | `get_upstream_features` | L4:F13412@55, k=10 → Emb:" RD"@55 (de=11.31) +9 more |

### Build

`build_circuit` → 18 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 54,198 | 5,556 | 75,359 | 0 | $0.0274 | — | — |
| SA-6 | openai/gpt-oss-120b | 55,417 | 3,951 | 64 | 0 | $0.0107 | ✅ 5F/8E | Trace upstream from L4:F7864 (xml or source code snippets — … |
| SA-1 | openai/gpt-oss-120b | 98,053 | 3,482 | 2,528 | 0 | $0.0168 | ✅ 4F/3E | Trace upstream from L18:F14677 (instances of women/girls bei… |
| SA-5 | openai/gpt-oss-120b | 145,099 | 9,280 | 2,528 | 0 | $0.0274 | ✅ 7F/13E | Trace upstream from L4:F13412 (terms related to diets and di… |
| SA-4 | openai/gpt-oss-120b | 135,296 | 9,278 | 11,424 | 0 | $0.0260 | ✅ 6F/12E | Trace upstream from L7:F8644 (woman's name in a variety of c… |
| **Total** | | **488,063** | **31,547** | **91,903** | **0** | **$0.1084** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 41s