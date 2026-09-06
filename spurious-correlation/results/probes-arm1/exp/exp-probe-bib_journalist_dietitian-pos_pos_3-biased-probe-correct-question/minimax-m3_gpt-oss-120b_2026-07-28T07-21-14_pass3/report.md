# Circuit Oracle Report
**Date:** 2026-07-28 07:21:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by features that detect the *gender* of the subject (female pronouns, women's names, women in general) rather than by any genuine nutrition-/health-coach-domain indicator — the entire attribution graph is a gender-marker circuit that rides on the repeated "She/her" tokens.

**Confidence:** 9

**Reasoning:** The top features feeding the probe direction are uniformly gender-detectors. The two strongest direct contributors are L6:F11646 ("references to women, triggered by pronouns and titles," frac_nonzero 0.02, promoted tokens = herself/她/ihr/she/her) with direct_effect 0.34, and L18:F14677 ("instances of women or girls being mentioned," frac_nonzero 0.012, promoted tokens = herself/she/her/herself/她) with direct_effect 0.24. Subagent tracing shows L6:F11646 is driven by the raw "She" embedding (direct_effect 19.25 from Emb:She pos 1) through a pronoun cascade: L2:F2128 → L4:F7864 / L5:F10952 → L6:F11646. L18:F14677 receives its top input from the "She" token at pos 29 (direct_effect 14.4) plus L17:F5889 and L0:F15382 — both "pronouns/people" detectors. L19:F9685 ("references to women's names and their roles or accomplishments," promoted tokens herself/she/her) is the other top contributor (direct_effect 0.15) and is also driven primarily by Emb:She pos 29 (direct_effect 5.6) and Emb:She pos 1 (direct_effect 3.7), with a "personal names and titles" feature L18:F9023 as an auxiliary. L12:F12940 ("references to female pronouns and possessive pronouns," promoted tokens herself) is yet another pure pronoun detector. No feature in the circuit encodes nutrition, diet, food philosophy, coaching, exercise, self-care, or any other domain content — the only content-bearing nodes are generic "the word 'others'" (L0:F2349, fired by Emb:others) and the embedding for "empowering," both of which feed *into* the gender circuit rather than representing profession-level expertise. The user concern is confirmed: the probe is essentially asking the model "does this text talk about a woman?", and the model's answer is built from She/her tokens at positions 1, 2, 29, 40, 66 and their associated pronoun/women-reference features. This is a textbook spurious-correlation circuit — a profession classifier that will fire on any text mentioning a woman, regardless of whether the subject is actually a nutritionist.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 29 | Late-layer gender/women-in-context detectors |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 29 | Late-layer gender/women-in-context detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer gender/women-in-context detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 66 | Late-layer gender/women-in-context detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 40 | Late-layer gender/women-in-context detectors |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 29 | Late-layer gender/women-in-context detectors |  personal names and associated titles | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 29 | Late-layer gender/women-in-context detectors |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L16:F2918](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) | 29 | Late-layer gender/women-in-context detectors | Pronouns | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 29 | Late-layer gender/women-in-context detectors |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L14:F13478](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) | 29 | Late-layer gender/women-in-context detectors |  occurrences of people's names, often with titles | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-layer female pronoun and gendered-entity features | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Mid-layer female pronoun and gendered-entity features | terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L8:F7245](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7245) | 2 | Mid-layer female pronoun and gendered-entity features | content in languages other than English, particularly French and possibly Sanskrit. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7245) |
| [L13:F11685](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) | 29 | Mid-layer female pronoun and gendered-entity features |  words related to women | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Early/mid gender-reference and pronoun detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Early/mid gender-reference and pronoun detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 29 | Early/mid gender-reference and pronoun detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Early/mid gender-reference and pronoun detectors | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 29 | Early/mid gender-reference and pronoun detectors | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 29 | Early/mid gender-reference and pronoun detectors |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Early/mid gender-reference and pronoun detectors | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early/mid gender-reference and pronoun detectors | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early/mid gender-reference and pronoun detectors |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 6 | Layer-0 word detector ("others") |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 29 | Layer-0 word detector ("others") | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Layer-0 word detector ("others") |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | Layer-0 word detector ("others") | pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, *ele*, and *ela* across multiple languages. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.340 |
| 3 | `inspect_feature` ×10 | L6:11646, L18:14677, L4:7864, L6:16329, L12:12940, L19:9685, L4:15317, L7:8644, L0:2349, L2:7672 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 4 | 8 | Trace upstream from L6:F11646 (references to women, triggered by pronouns/titles… |
| SA-2 | `L18:F14677@29` | ❌ error | — | — | Trace upstream from L18:F14677 (instances of women or girls being mentioned, pos… |
| SA-3 | `L19:F9685@29` | ❌ error | — | — | Trace upstream from L19:F9685 (references to women's names and their roles/accom… |
| SA-4 | `L12:F12940@2` | ✅ reported | 5 | 5 | Trace upstream from L12:F12940 (references to female pronouns and possessive pro… |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 5 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 6 | `get_upstream_features` | L2:F2128@1, k=10 | Emb:"She"@1 (de=20.25) +9 more |
| 7 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 8 | `get_upstream_features` | L0:F12519@1, k=10 | Emb:"She"@1 (de=21.88) +9 more |
| 9 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |

**Findings:** The primary driver of the women‑reference feature (L6:F11646) is the raw token embedding for the pronoun "She" (direct_effect ~19). This signal propagates through a cascade of pronoun‑sensitive features: a low‑level multilingual pronoun detector (L2:F2128), which feeds both a mid‑level aggregator (L4:F7864) and a higher‑level contextual pronoun feature (L5:F10952). Both mid‑ and high‑level feature…

</details>

<details>
<summary><b>SA-4</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:"She"@1 (de=6.56) +9 more |
| 3 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 4 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=13.12) +9 more |
| 5 | `get_upstream_features` | L10:F14965@2, k=10 | L6:F11646 (de=5.34) +9 more |
| 6 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 7 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 8 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 9 | `get_upstream_features` | L6:F11646@2, k=10 | L4:F15317 (de=7.69) +9 more |
| 10 | `inspect_feature` | L5, F645 | " verbs in past tense" |
| 11 | `get_upstream_features` | L7:F2765@2, k=10 | Emb:"She"@1 (de=2.84) +9 more |
| 12 | `inspect_feature` | L5, F16213 | " proper nouns consisting of a first and last name" |

**Findings:** Tracing upstream from the mid‑layer driver L12:F12940 (female pronoun detector) reveals a short chain of gender‑related features. The strongest upstream influence is the named‑entity detector L4:F15317, which itself is driven by the input token embedding for "She" (pos 1) and a lower‑layer feature L2:7672. Further downstream contributors include L10:F14965 (terms relating to women) and L6:F11646 (…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@29, k=8 → Emb:" She"@29 (de=14.38) +7 more |
| 2 | `get_upstream_features` | L19:F9685@29, k=8 → Emb:" She"@29 (de=5.62) +7 more |
| 3 | `inspect_feature` ×7 | L17:5889, L15:3330, L0:15382, L13:11685, L16:2918, L18:9023, L14:13478 |
| 4 | `get_upstream_features` | L6:F16329@1, k=8 → Emb:"She"@1 (de=8.94) +7 more |
| 5 | `get_upstream_features` | L7:F8644@29, k=8 → Emb:"She"@1 (de=8.31) +7 more |
| 6 | `get_upstream_features` | L0:F2349@6, k=8 → Emb:" others"@6 (de=41.00) +7 more |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 53,671 | 3,976 | 140,745 | 0 | $0.0293 | — | — |
| SA-1 | openai/gpt-oss-120b | 96,371 | 5,832 | 0 | 0 | $0.0180 | ✅ 4F/8E | Trace upstream from L6:F11646 (references to women, triggere… |
| SA-4 | openai/gpt-oss-120b | 141,922 | 9,119 | 11,104 | 0 | $0.0269 | ✅ 5F/5E | Trace upstream from L12:F12940 (references to female pronoun… |
| **Total** | | **291,964** | **18,927** | **151,849** | **0** | **$0.0742** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 2s