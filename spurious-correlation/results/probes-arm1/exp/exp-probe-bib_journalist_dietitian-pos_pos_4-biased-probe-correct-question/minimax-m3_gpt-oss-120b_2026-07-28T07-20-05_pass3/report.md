# Circuit Oracle Report
**Date:** 2026-07-28 07:20:05 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "Dietitian" is driven overwhelmingly by gender/female-reference features (female pronouns "She"/"she"/"her" at positions 1 and 57, the proper name "Heather", and a multi-layer cascade of women/pronoun detectors culminating in L18:F14677 "instances of women/girls being mentioned" and L19:F9685 "women's names with roles/accomplishments"), with only a small contribution from genuine diet/nutrition-topic features (L4:F13412, L6:F11327) — the user's concern about spurious gender-based features is validated.

**Confidence:** 8

**Reasoning:** The attribution graph is dominated by a parallel "female-reference" cascade: the **"She"** token at pos 1 (Emb direct_effect ~+6 to L12:F12940, ~+8.9 to L6:F11646, ~+27 to L18:F14677, ~+13.6 to L4:F15317) feeds L0:F9519 ("she/her pronoun"), L2:F7672 ("mentions of women by name"), L4:F15317 ("named entities like people"), L6:F11646 ("references to women"), L6:F16329 ("female first names", but acts as a suppressor of female pronouns here), L7:F8644 ("woman's name", driven by the **"Heather"** embedding at pos 31 via L4:F1276 capitalized-name detector), L10:F14965 ("terms relating to women"), L12:F12940 ("female pronouns"), L12:F14970 ("person names"), L15:F3330 ("personal stories… often indicated by the pronoun 'she'"), L17:F5889 ("people with pronouns"), and finally L18:F14677 ("instances of women/girls") and L19:F9685 ("women's names and roles"). A second **" she"** token at pos 57 contributes a strong direct_effect of +22.6 to L18:F14677 and +14.4 to L6:F16329. These late-layer gender detectors (L18:F14677, L19:F9685) have the largest direct effects on the probe (e.g., L18:F14677 at pos 57: +0.14, pos 94: +0.12, pos 1: +0.12; L19:F9685 at pos 57: +0.09, pos 94: +0.08). By contrast, the genuine profession indicators are weak and few: **L4:F13412** ("diets and dietary health", driven by the " Die"/"te" sub-token embeddings of "Dietetics" at pos 20-21) has direct_effects of +0.16 at pos 21, +0.12 at pos 55, and is the single largest direct contributor; **L6:F11327** ("food or nutrition") adds +0.08; there is NO feature that specifically encodes "Dietitian" or "Public Health" or "RD" as a profession token. The probe direction is therefore effectively the model's "is-this-text-about-a-woman" representation projected onto a profession-direction space, not a representation of nutritional/dietetics expertise. The diet-topic features (L4:F13412, L6:F11327) are present but are eclipsed in number, layer depth, and accumulated direct_effect by the female-gender cascade — confirming the user's concern that the circuit is using spurious gender markers (female pronouns, the female name "Heather") rather than genuine profession-indicative content to predict the profession.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'She' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 57 | Emb: ' she' (pos 57) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 31 | Emb: 'Heather' (pos 31) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: ' Die' (pos 20) / 'te' (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: ' Die' (pos 20) / 'te' (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 31 | L0:F7532 — proper nouns |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | L0:F9519 — 'she' / 'her' pronoun detector |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 57 | L0:F12519 — 'she' pronoun (pos 57) |  the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | L2:F7672 — mentions of women by name and relationship |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | L4:F13412 — diet / dietary terms |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | L4:F13412 — diet / dietary terms |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | L4:F13412 — diet / dietary terms |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 37 | L4:F13412 — diet / dietary terms |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 31 | L4:F1276 — capitalized names (e.g. 'Heather') | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | L4:F15317 — named entities (people) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | L4:F7864 — code/XML snippets (promotes 'she') | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L5:F5996](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) | 1 | L5:F5996 — words associated with females |  words associated with females, femininity or womanhood | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5996) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | L6:F11646 — references to women (pronouns, titles) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | L6:F11646 — references to women (pronouns, titles) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 21 | L6:F11327 — food / nutrition terms |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | L6:F16329 — female first names / possessive (inhibitory) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 57 | L6:F16329 — female first names / possessive (inhibitory) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 31 | L7:F8644 — woman's name detector |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 31 | L7:F2765 — mentions of people & personal details |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | L10:F14965 — terms relating to women |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | L12:F12940 — female pronouns ('She'/'her'/'herself') | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 31 | L12:F14970 — person names (first & last) |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L14:F13478](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) | 94 | L14:F13478 — people's names (often with titles) |  occurrences of people's names, often with titles | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 57 | L15:F3330 — personal stories of individuals (often women) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 57 | L17:F5889 — people with pronouns/possessives |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 94 | L17:F5889 — people with pronouns/possessives |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 57 | L18:F14677 — instances of women/girls mentioned |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 94 | L18:F14677 — instances of women/girls mentioned |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | L18:F14677 — instances of women/girls mentioned |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 57 | L19:F9685 — women's names with roles/accomplishments |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 94 | L19:F9685 — women's names with roles/accomplishments |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe logit (classification score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:8644 de=-0.212 |
| 3 | `inspect_feature` ×11 | L7:8644, L6:11646, L4:13412, L18:14677, L4:7864, L7:2765, L4:1276, L12:12940, L0:8974, L12:14970, L4:15317 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ✅ reported | 5 | 4 | Trace this feature (L18:F14677, "instances of women or girls being mentioned") u… |
| SA-2 | `L12:F12940@2` | ✅ reported | 6 | 10 | Trace this feature (L12:F12940, "references to female pronouns and possessive pr… |
| SA-3 | `L4:F13412@21` | ✅ reported | 6 | 18 | Trace this feature (L4:F13412, "terms related to diets and dietary health") upst… |
| SA-4 | `L7:F8644@31` | ✅ reported | 4 | 7 | Trace this feature (L7:F8644, "woman's name in a variety of contexts") upstream.… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@1, k=10 | Emb:"She"@1 (de=27.12) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 5 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 6 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 7 | `get_upstream_features` | L15:F851@1, k=10 | L12:F12493 (de=22.38) +9 more |

**Findings:** Tracing from L18:F14677 (layer 18) reveals that the dominant driver is the raw embedding of the token 'She' (direct_effect 27.1). Additional positive contributions come from three intermediate features in layers 4, 6, and 15, each modestly amplifying the signal. The upstream path reaches a lower‑third layer (layer 4) and includes a concrete embedding node, satisfying the termination condition. The…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:"She"@1 (de=6.03) +9 more |
| 3 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 4 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 5 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=13.56) +9 more |
| 6 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 7 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 8 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 9 | `get_upstream_features` | L2:F7672@1, k=10 | Emb:"She"@1 (de=13.88) +9 more |

**Findings:** The target feature L12:12940 that flags references to female pronouns is primarily driven by the input token "She" (positive direct_effect at the embedding level). Upstream, a cascade of gender‑related features in layers 4, 6, 10, and 2 amplify this signal, each detecting named entities, women‑related terms, or mentions of women. All paths converge on the same token embedding, confirming that the …

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 2 | `get_upstream_features` | L4:F13412@21, k=10 | L3:F11774 (de=4.81) +9 more |
| 3 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 4 | `get_upstream_features` | L3:F11774@21, k=10 | Emb:" Die"@20 (de=5.88) +9 more |
| 5 | `inspect_feature` | L3, F10028 | "words or short phrases that include "made of/from", and words ending w" |
| 6 | `get_upstream_features` | L3:F10028@21, k=10 | Emb:" Die"@20 (de=6.94) +9 more |
| 7 | `inspect_feature` | L2, F7473 | " capitalized two letter prefixes or suffixes" |
| 8 | `inspect_feature` | L2, F1984 | " strings of letters that appear to be fragments of names, especially p" |
| 9 | `get_upstream_features` | L2:F7473@21, k=10 | Emb:" Die"@20 (de=19.00) +9 more |
| 10 | `inspect_feature` | L2, F4472 | " LaTeX math expressions" |

**Findings:** The diet‑topic feature (L4:F13412) is principally driven by the sub‑word embeddings of the word "Diet" – the token " Die" at position 20 and its continuation "te" at position 21. Upstream feature detectors in layers 3 and 2 contribute by recognizing short alphanumeric fragments (L3:11774), suffix patterns (L3:10028), capitalised prefixes (L2:7473), and name‑like fragments (L2:1984). No evidence sh…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F8644 | " woman's name in a variety of contexts" |
| 2 | `get_upstream_features` | L7:F8644@31, k=10 | Emb:"She"@1 (de=7.47) +9 more |
| 3 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `get_upstream_features` | L4:F1276@31, k=10 | Emb:" Heather"@31 (de=10.94) +9 more |
| 6 | `inspect_feature` | L0, F7532 | " proper nouns" |

**Findings:** Tracing from L7:F8644 (women's name detector) shows its activation is driven primarily by a capitalized‑name detector at L4:F1276, which itself receives a strong positive push from the input token "Heather" (embedding) and from a low‑level proper‑noun feature L0:F7532. Additional upstream influence comes from gender‑pronoun feature L6:F11646 and the pronoun embedding "She". Thus the circuit encode…

</details>

### Re-dispatch (round 2): 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-5 | `L19:F9685@57` | ❌ error | — | — | Trace this feature (L19:F9685, "references to women's names and their roles or a… |
| SA-6 | `L6:F11327@21` | ❌ error | — | — | Trace this feature (L6:F11327, "words or phrases related to food or nutrition") … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_features` | token="", k=30 → 30 features; top: L7:8644 de=-0.212 |
| 2 | `inspect_feature` ×8 | L6:16329, L19:9685, L0:6051, L0:9519, L8:15861, L13:11685, L0:6429, L6:11327 |
| 3 | `get_upstream_features` | L18:F14677@57, k=5 → Emb:" she"@57 (de=22.62) +4 more |
| 4 | `get_upstream_features` | L19:F9685@94, k=5 → Emb:" She"@94 (de=5.88) +4 more |
| 5 | `inspect_feature` ×8 | L17:5889, L15:3330, L14:13478, L0:12519, L15:851, L10:14965, L2:7672, L0:7532 |
| 6 | `get_upstream_features` | L12:F14970@31, k=3 → Emb:"<bos>"@0 (de=-3.48) +2 more |
| 7 | `get_upstream_features` | L7:F2765@31, k=3 → Emb:"She"@1 (de=3.34) +2 more |
| 8 | `get_upstream_features` | L6:F16329@1, k=3 → Emb:"She"@1 (de=8.94) +2 more |
| 9 | `get_upstream_features` | L6:F16329@57, k=3 → Emb:" she"@57 (de=14.44) +2 more |
| 10 | `inspect_feature` ×2 | L5:5996, L2:899 |

### Build

`build_circuit` → 27 nodes, 45 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 71,496 | 7,623 | 353,460 | 0 | $0.0518 | — | — |
| SA-1 | openai/gpt-oss-120b | 76,670 | 4,302 | 0 | 0 | $0.0141 | ✅ 5F/4E | Trace this feature (L18:F14677, "instances of women or girls… |
| SA-2 | openai/gpt-oss-120b | 108,834 | 6,003 | 0 | 0 | $0.0199 | ✅ 6F/10E | Trace this feature (L12:F12940, "references to female pronou… |
| SA-4 | openai/gpt-oss-120b | 58,099 | 2,861 | 0 | 0 | $0.0104 | ✅ 4F/7E | Trace this feature (L7:F8644, "woman's name in a variety of … |
| SA-3 | openai/gpt-oss-120b | 121,102 | 11,156 | 18,176 | 0 | $0.0251 | ✅ 6F/18E | Trace this feature (L4:F13412, "terms related to diets and d… |
| **Total** | | **436,201** | **31,945** | **371,636** | **0** | **$0.1214** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 50s