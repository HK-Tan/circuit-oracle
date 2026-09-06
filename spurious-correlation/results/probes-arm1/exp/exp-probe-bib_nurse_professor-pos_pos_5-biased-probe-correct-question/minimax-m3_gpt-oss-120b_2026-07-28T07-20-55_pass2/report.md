# Circuit Oracle Report
**Date:** 2026-07-28 07:20:55 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for "midwife" is driven by two parallel, largely independent pathways: a dominant *feminine-name/pronoun* pathway originating from the proper noun "Melissa" and the pronouns "She"/"her", and a weaker *obstetric-semantic* pathway anchored on the tokens "Labor"/"Delivery"/"nurse"/"midwife". The user's concern is well-founded: the feminine-gender path contributes a larger and more direct share of the probe's score than the actual profession tokens.

**Confidence:** 8

**Reasoning:** The top features by direct effect on the probe are concentrated in feminine-reference detectors rather than profession-specific ones. The two most-positive single-edge contributions come from embedding nodes for "She" (pos 54, de ≈ 14.1) and " Melissa" (pos 5, de ≈ 9.6) feeding into L4:F1276 (capitalized names/titles) and L0:F7532 (proper nouns, frac=0.06), and from "Melissa" embeddings driving L2:F5859 ("first names (mostly female)", frac=0.0045) and L6:F8166 ("proper names ending in a/i/e", promoted "herself/motherhood", suppressed "himself", frac=0.006). These feed the mid-layer "person-name / pronoun aggregators" supernode (L13:L18), which includes L14:F12501 ("uses of the feminine pronoun", promoted "feminist/feminism"), L13:F4753 (proper nouns, esp. people), L17:F5889 (pronoun+possessive patterns), and L15:F3330 (personal stories of women). The late-layer supernode (L18:F14677 "instances of women or girls being mentioned" + L19:F9685 "women's names and their roles or accomplishments") sits at the top with the highest direct effects (0.41–0.45), and its upstream trace terminates at the embedding of " She" (de ≈ 14–20) and the "Melissa" tokens, with no obstetric-semantic content required to activate it. By contrast, the genuine profession pathway — L1:L12174 → L3:F9008 ("words related to childbirth or birth") → L4:F13803 ("terms related to obstetrics and gynecology", promoted "pregnancy/postpartum") — is anchored by "Delivery" (de ≈ 11.2), "Labor" (de ≈ 4.75), and "midwife" (de ≈ 22.4 at pos 66), but its downstream effect on the probe is smaller and more diffuse. In other words, the probe can already achieve a high score merely by detecting that the subject is a named woman (Melissa + She/her pronouns); the actual midwifery/obstetric vocabulary is a secondary, corroborating signal. This matches the user's hypothesis: the circuit uses a spurious gender marker pathway as the primary driver, with the profession-indicator pathway playing a smaller, supporting role.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 31 | Late-layer gender-reference gates |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 54 | Late-layer gender-reference gates |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 86 | Late-layer gender-reference gates |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 31 | Late-layer gender-reference gates |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 54 | Late-layer gender-reference gates |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 68 | Late-layer gender-reference gates |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F3679](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) | 31 | Mid-layer pronoun / person-name aggregators |  personal pronouns and/or proper nouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) |
| [L18:F3679](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) | 86 | Mid-layer pronoun / person-name aggregators |  personal pronouns and/or proper nouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 31 | Mid-layer pronoun / person-name aggregators |  personal names and associated titles | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 54 | Mid-layer pronoun / person-name aggregators | references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 68 | Mid-layer pronoun / person-name aggregators | references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 54 | Mid-layer pronoun / person-name aggregators |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 68 | Mid-layer pronoun / person-name aggregators |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 31 | Mid-layer pronoun / person-name aggregators |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L14:F4385](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4385) | 31 | Mid-layer pronoun / person-name aggregators | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4385) |
| [L13:F4753](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4753) | 31 | Mid-layer pronoun / person-name aggregators |  proper nouns, especially names of people | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4753) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 54 | Mid-layer pronoun / person-name aggregators | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L16:F2918](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) | 54 | Mid-layer pronoun / person-name aggregators | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 5 | Early-layer feminine-name / pronoun detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 54 | Early-layer feminine-name / pronoun detectors |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 5 | Early-layer feminine-name / pronoun detectors |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 31 | Early-layer feminine-name / pronoun detectors |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 5 | Early-layer feminine-name / pronoun detectors | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 31 | Early-layer feminine-name / pronoun detectors | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 5 | Early-layer feminine-name / pronoun detectors |  first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 5 | Early-layer feminine-name / pronoun detectors |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 54 | Early-layer feminine-name / pronoun detectors | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 68 | Early-layer feminine-name / pronoun detectors | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 54 | Early-layer feminine-name / pronoun detectors | the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 5 | Early-layer feminine-name / pronoun detectors |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | Obstetrics / birth semantic features |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 66 | Obstetrics / birth semantic features |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 11 | Obstetrics / birth semantic features | words related to childbirth or birth in general, including in animals. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L1:F12174](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12174) | 11 | Obstetrics / birth semantic features | words relating to ways things are conventionally done, potential problems, or political/economic issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12174) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:1276 de=0.559 |
| 3 | `inspect_feature` ×8 | L4:1276, L12:14970, L6:8166, L4:13803, L18:14677, L19:9685, L0:7532, L2:5859 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@54` | ✅ reported | 6 | 11 | Trace upstream from L18:F14677 at pos 54. This feature fires on "instances of wo… |
| SA-2 | `L19:F9685@31` | ❌ error | — | — | Trace upstream from L19:F9685 at pos 31. This feature fires on "references to wo… |
| SA-3 | `L4:F13803@11` | ✅ reported | 3 | 4 | Trace upstream from L4:F13803 at pos 11. This feature fires on obstetrics/gyneco… |
| SA-4 | `L4:F1276@5` | ❌ error | — | — | Trace upstream from L4:F1276 at pos 5. This feature fires on capitalized names a… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@54, k=10 | Emb:" She"@54 (de=14.56) +9 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `get_upstream_features` | L15:F3330@54, k=10 | Emb:" She"@54 (de=16.12) +9 more |
| 5 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 6 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 7 | `get_upstream_features` | L17:F5889@54, k=10 | Emb:" She"@54 (de=19.88) +9 more |
| 8 | `get_upstream_features` | L6:F11646@54, k=10 | Emb:" She"@54 (de=19.25) +9 more |
| 9 | `inspect_feature` | L0, F15382 | "mentions of a female person." |
| 10 | `inspect_feature` | L0, F9519 | " the pronoun "she" and the possessive pronoun "her"" |

**Findings:** Feature L18:F14677 is the final female‑reference gate that promotes tokens such as she/her/herself. The strongest upstream driver is the raw token embedding for " She" at position 54 (direct effect ~14‑20), indicating the input token itself carries the gender cue. Mid‑layer contributors (layers 17, 15, 6) are pronoun‑aggregation detectors that recognize feminine pronoun patterns and amplify the si…

</details>

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13803 | " terms related to obstetrics and gynecology" |
| 2 | `get_upstream_features` | L4:F13803@11, k=10 | Emb:" Delivery"@11 (de=12.19) +9 more |
| 3 | `inspect_feature` | L3, F9008 | " words related to childbirth or birth in general, including in animals" |
| 4 | `get_upstream_features` | L3:F9008@11, k=10 | Emb:" Delivery"@11 (de=11.19) +9 more |
| 5 | `inspect_feature` | L1, F12174 | " words relating to ways things are conventionally done, potential prob" |

**Findings:** The obstetrics/gynecology feature L4:F13803 (pos 11) is driven primarily by the input token "Delivery" (direct_effect 12.19) and also by "Labor" (8.81). Upstream, a birth‑semantic feature L3:F9008 (pos 11) adds a further positive boost (4.16), and this in turn is amplified by a contextual procedural feature L1:F12174 (pos 11) with a smaller positive effect (1.65). The path reaches a lower‑third la…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F9685@31, k=10 → Emb:" nurse"@12 (de=2.33) +9 more |
| 2 | `get_upstream_features` | L4:F1276@5, k=10 → Emb:" Melissa"@5 (de=9.62) +9 more |
| 3 | `get_upstream_features` | L12:F14970@5, k=10 → L4:F1276 (de=3.36) +9 more |
| 4 | `get_upstream_features` | L2:F5859@5, k=10 → L0:F7532 (de=5.28) +9 more |
| 5 | `inspect_feature` ×8 | L18:3679, L18:9023, L13:4753, L14:12501, L4:13803, L18:14677, L15:3330, L6:11646 |
| 6 | `get_upstream_features` | L4:F13803@66, k=10 → Emb:" midwife"@66 (de=22.38) +9 more |
| 7 | `get_upstream_features` | L6:F8166@5, k=10 → L4:F1276 (de=5.19) +9 more |
| 8 | `get_upstream_features` | L3:F9008@11, k=8 → Emb:" Delivery"@11 (de=11.19) +7 more |
| 9 | `get_upstream_features` | L19:F9685@54, k=8 → Emb:" She"@54 (de=5.56) +7 more |
| 10 | `get_upstream_features` | L19:F9685@86, k=8 → Emb:" midwife"@66 (de=3.95) +7 more |
| 11 | `get_upstream_features` | L18:F14677@31, k=8 → L14:F4385 (de=2.17) +7 more |
| 12 | `get_upstream_features` | L18:F14677@68, k=8 → Emb:" She"@68 (de=14.06) +7 more |

### Build

`build_circuit` → 16 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 52,098 | 5,326 | 203,449 | 0 | $0.0342 | — | — |
| SA-3 | openai/gpt-oss-120b | 37,803 | 2,863 | 2,528 | 0 | $0.0074 | ✅ 3F/4E | Trace upstream from L4:F13803 at pos 11. This feature fires … |
| SA-1 | openai/gpt-oss-120b | 133,775 | 8,693 | 2,752 | 0 | $0.0253 | ✅ 6F/11E | Trace upstream from L18:F14677 at pos 54. This feature fires… |
| **Total** | | **223,676** | **16,882** | **208,729** | **0** | **$0.0670** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 41s