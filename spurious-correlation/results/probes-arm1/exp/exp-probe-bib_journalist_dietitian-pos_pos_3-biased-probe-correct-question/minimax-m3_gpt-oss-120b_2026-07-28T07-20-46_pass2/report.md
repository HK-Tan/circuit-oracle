# Circuit Oracle Report
**Date:** 2026-07-28 07:20:46 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven overwhelmingly by **gender/pronoun features rather than by profession-relevant content** — the dominant causal path flows from the "She" token embedding through layers of female-pronoun detectors (L6:11646, L17:5889, L18:14677) into the probe output, while the actual nutrition/food profession content (L6:11327 "food or nutrition") contributes a single weak positive effect.

**Confidence:** 9

**Reasoning:**

The circuit is dominated by a single **female-gender signal** that originates at the input token "She" (pos 1 and pos 29, both with leading-space variants) and is propagated through a clear hierarchy of gender-pronoun detectors:

1. **Token-embedding entry (L0:15382, L0:9519, both at pos 29; promoted_token "She"/"Her")** — direct_effect up to **14.375** into L18:F14677. The " She" embedding is by far the single largest input to the late-layer gender feature.
2. **Early/mid pronoun layer (L6:11646 "references to women via pronouns and titles", L6:16329 "female first names and possessive forms", L4:7864 mislabelled as "xml" but actually fires on "She", L4:15317, L2:7672 "women by name", L5:10952, L2:2128)** — these all detect the *gender marker* itself, with no profession vocabulary in any of their promoted-token lists. Direct effects of 0.18–0.34 at the probe.
3. **Pronoun aggregation (L13:6622 "pronouns", L15:3330 "personal stories… often indicated by 'she'", L16:2918 "Pronouns", L17:5889 "references to people with pronouns and possessive pronouns")** — generic pronoun aggregators whose top-activating examples are "He"/"She"/"his"/"her" only.
4. **Late-layer women-mentioned features (L12:12940 "female pronouns and possessive pronouns", L14:12501 "uses of the feminine pronoun", L14:13478 "people's names… titles", L18:9023 "personal names and associated titles", L18:14677 "instances of women or girls being mentioned", L19:9685 "women's names and their roles or accomplishments")** — these provide the largest direct effects on the probe (+0.13 to +0.34). L18:14743 ("He") provides a *negative* direct effect of -0.115, confirming the probe is *opposing* the male counterpart and tracking the female-gender axis specifically.

The autointerp labels of L18:14677 and L19:9685 sound as if they should encode profession ("roles or accomplishments"), but the traced upstream shows their entire mass comes from the pronoun "She" (L0:15382 contributes 14.375 directly to L18:14677; " She" embedding contributes 5.625 to L19:9685) and the pronoun-tracking chain above. None of the upstream features have profession-related content in their promoted tokens; the entire signal is gender-marker aggregation.

**The profession-related content is marginal:** the only genuine topic signal is L6:11327 ("food or nutrition", pos 15, direct_effect +0.1035) driven directly by the "food" token embedding (direct_effect +34). There is no dedicated "dietitian"/"nutritionist"/"health-coach" profession feature, no role-noun detector, and no path connecting nutrition vocabulary to a late-layer "this person is a nutritionist" abstraction. The probe appears to be latching onto "female + food/health content" co-occurrence, with the female-gender half carrying most of the weight.

**Conclusion regarding the user concern:** The concern is **confirmed**. The probe's classification is primarily driven by spurious gender markers (she/her pronouns) rather than by genuine profession indicators. The dominant late-layer features (L18:14677, L19:9685) are downstream of pure pronoun detectors, and the only content-bearing feature (L6:11327 food/nutrition) is small and never composed with the gender signal into a profession abstraction — instead, the female-gender features themselves are the output.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 29 | Women mentioned (gender signal) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 29 | Women mentioned (gender signal) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 29 | Women mentioned (gender signal) |  personal names and associated titles | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |
| [L14:F13478](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) | 29 | Women mentioned (gender signal) |  occurrences of people's names, often with titles | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Women mentioned (gender signal) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 3 | Women mentioned (gender signal) |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 29 | Pronoun aggregation (he/she/they tracking) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L16:F2918](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) | 29 | Pronoun aggregation (he/she/they tracking) | Pronouns | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 29 | Pronoun aggregation (he/she/they tracking) |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 29 | Pronoun aggregation (he/she/they tracking) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Gender pronoun/title detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Gender pronoun/title detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 29 | Gender pronoun/title detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 29 | Gender pronoun/title detector | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Gender pronoun/title detector | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Gender pronoun/title detector |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Gender pronoun/title detector |  mentions of women by name and relationship | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Gender pronoun/title detector | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | Gender pronoun/title detector |  pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, *ele*, and *ela* across multiple languages. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 29 | Gender pronoun/title detector |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 19 | Gender pronoun/title detector |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 29 | Male pronoun (suppressor) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 29 | Token embedding: "She" | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 29 | Token embedding: "She" |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | Food/nutrition vocabulary (profession-related content) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 15 | Food/nutrition vocabulary (profession-related content) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 6 | Token embedding: "others" |  the word "others" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.340 |
| 3 | `inspect_feature` ×13 | L6:11646, L18:14677, L4:7864, L6:16329, L12:12940, L19:9685, L6:11327, L14:12501, L18:14743, L7:8644, L4:15317, L0:2349, L2:7672 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@29` | ✅ reported | 6 | 10 | Trace this feature upstream. This is a "women or girls being mentioned" feature.… |
| SA-2 | `L19:F9685@29` | ❌ error | — | — | Trace this feature upstream. This is "references to women's names and their role… |
| SA-3 | `L6:F11646@1` | ✅ reported | 4 | 6 | Trace this feature upstream. This is a "references to women, triggered by pronou… |
| SA-4 | `L12:F12940@2` | ❌ error | — | — | Trace this feature upstream. This is "female pronouns and possessive pronouns". … |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@29, k=10 | Emb:" She"@29 (de=14.38) +9 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 6 | `get_upstream_features` | L17:F5889@29, k=10 | Emb:" She"@29 (de=19.38) +9 more |
| 7 | `get_upstream_features` | L0:F15382@29, k=10 | Emb:" She"@29 (de=23.38) +9 more |
| 8 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 9 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 10 | `get_upstream_features` | L0:F15382@29, k=10 | Emb:" She"@29 (de=23.38) +9 more |
| 11 | `get_upstream_features` | L15:F3330@29, k=10 | Emb:" She"@29 (de=15.00) +9 more |
| 12 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |
| 13 | `get_upstream_features` | L6:F11646@29, k=10 | Emb:" She"@29 (de=17.62) +9 more |

**Findings:** The gender‑mention feature (L18:F14677) is driven primarily by low‑level token embeddings of the word "She" (layer‑0 embeddings) and early transformer features that detect female pronouns. Upstream analysis shows the strongest contributors are L17:F5889 (pronoun aggregation), L15:F3330 (female‑story narrative), and L6:F11646 (female pronoun/title detector). All of these are activated by the pronou…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 5 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 6 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |
| 7 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |

**Findings:** Tracing from the L6:11646 gender‑reference feature shows it is driven primarily by the input token embedding for "She" (positive direct effect 19.25). Upstream internal features at layers 4, 5, and 2 are also pronoun detectors, though some have misleading autointerp labels (e.g., XML snippet detector). No profession‑specific tokens appear in the promoted token lists of these upstream features; the…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F9685@29, k=10 → Emb:" She"@29 (de=5.62) +9 more |
| 2 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:"She"@1 (de=6.56) +9 more |
| 3 | `get_upstream_features` | L18:F14677@29, k=5 → Emb:" She"@29 (de=14.38) +4 more |
| 4 | `get_upstream_features` | L18:F14743@29, k=8 → Emb:" She"@29 (de=16.88) +7 more |
| 5 | `get_upstream_features` | L6:F11327@15, k=8 → Emb:" food"@15 (de=34.00) +7 more |
| 6 | `get_upstream_features` | L14:F12501@3, k=8 → L13:F11685 (de=-7.72) +7 more |
| 7 | `inspect_feature` ×11 | L18:9023, L14:13478, L13:6622, L16:2918, L0:15382, L0:9519, L17:5889, L15:3330, L4:13412, L5:10952, L2:2128 |
| 8 | `get_upstream_features` | L6:F11327@15, k=3 → Emb:" food"@15 (de=34.00) +2 more |
| 9 | `get_upstream_features` | L19:F9685@29, k=5 → Emb:" She"@29 (de=5.62) +4 more |

### Build

`build_circuit` → 9 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 62,016 | 4,812 | 196,063 | 0 | $0.0361 | — | — |
| SA-3 | openai/gpt-oss-120b | 64,879 | 4,535 | 2,528 | 0 | $0.0125 | ✅ 4F/6E | Trace this feature upstream. This is a "references to women,… |
| SA-1 | openai/gpt-oss-120b | 192,559 | 10,828 | 0 | 0 | $0.0354 | ✅ 6F/10E | Trace this feature upstream. This is a "women or girls being… |
| **Total** | | **319,454** | **20,175** | **198,591** | **0** | **$0.0840** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 29s