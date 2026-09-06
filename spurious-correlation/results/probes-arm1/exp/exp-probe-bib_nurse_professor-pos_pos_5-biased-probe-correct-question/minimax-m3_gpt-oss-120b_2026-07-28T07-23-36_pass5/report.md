# Circuit Oracle Report
**Date:** 2026-07-28 07:23:36 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "midwife/nurse" is driven by a circuit that conflates the profession with the subject's gender — the top features encode "instances of women or girls being mentioned" and "feminine pronouns" rather than the medical/obstetric profession keywords themselves.

**Confidence:** 8

**Reasoning:** The user concern is **strongly confirmed by the circuit**. The most influential features feeding the output are gender- and identity-marker features, not profession features:

- **Top feature (L19:F9685, direct_effect ~0.44–0.28)**: "references to women's names and their roles or accomplishments" — explicitly feminine, fires on `She`, `Melissa`, `Kathryn`, `Andrea`, `Daphne`, etc.
- **L18:F14677 (direct_effect ~0.45–0.41)**: "instances of women or girls being mentioned" — promoted tokens `▁herself`, `▁she`, `▁her`; suppressed `▁himself`, `▁his`.
- **L13:F11685 (direct_effect −0.37 at pos 66)**: "words related to women" — promotes `▁himself`/`▁his` (i.e., it actively *suppresses* the profession classification when the surrounding context is female-coded; the negative sign here actually means it pushed toward the opposite direction from the gender-marker features at the same position).

Crucially, the **upstream chain** that drives these late-layer gender features traces back to:
- `She` (pos 54, direct_effect 14.6) and `She` (pos 68, direct_effect 14.1) embeddings
- `Melissa` embeddings (pos 5, 31, 86) flowing through L0:F7532 ("proper nouns") and L0:F15382 ("mentions of a female person")
- L0:F9519 ("she/her") and L0:F12519 ("she") features at pos 54
- L6:F11646 ("references to women, potentially triggered by pronouns and titles") at pos 5

**Mid-layer profession features do exist** (L4:F13803 "obstetrics/gynecology" at pos 11 `Delivery` with direct_effect 0.45; L8:F10019 "childbirth and labor" at pos 66 `midwife`; L7:F2861 "pregnancy and labor" at pos 66) — and they ARE in the circuit. But their contribution is secondary: `midwife` (pos 66) flows mainly into the L18:L19 *gender-entity* features (L18:F3679 receives 1.5 from `Melissa` pos 86 and the `midwife` token, L19:F9685 receives 2.33 from `nurse` pos 12 and 2.19 from `Melissa` pos 31), so even the profession-token signal is being routed through personhood/femininity detectors.

The single most-cited upstream edge for the top L19 feature F9685 is the embedding of `nurse` (pos 12, direct_effect 2.33) — but F9685's label is "references to women's names and their roles or accomplishments," meaning the model has bound the token "nurse" to a female-personal-roles detector, not to a medical-profession detector.

**Topology summary:** Token embeddings (`Melissa`, `She`, `her`, `nurse`, `midwife`, `Labor`, `Delivery`) → L0–L8 features encoding proper-nounhood and the noun "nurse"/obstetric terms → L13–L17 features encoding female-person + feminine-pronoun context → L18–L19 features explicitly encoding "women" and "feminine roles" → output. The profession signal is present but is mediated by, and largely subsumed under, a female-gender/personhood pathway.

This is exactly the spurious-correlation pattern the user suspected: the probe classifies the profession primarily because the subject is signaled as female, via the female first name `Melissa`, feminine pronouns `She`/`her`, and the model's learned association between nursing/midwifery and feminine identity — rather than from features that recognize the professional content (`Labor and Delivery`, `Bachelors of Nursing`, `midwife`, `obstetrics`) in a profession-neutral way.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 31 | Late-layer: women & feminine identities |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 54 | Late-layer: women & feminine identities |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 86 | Late-layer: women & feminine identities |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 54 | Late-layer: women & feminine identities |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 31 | Late-layer: women & feminine identities |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 68 | Late-layer: women & feminine identities |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F3679](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) | 31 | Late-layer: women & feminine identities |  personal pronouns and/or proper nouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) |
| [L18:F3679](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) | 86 | Late-layer: women & feminine identities |  personal pronouns and/or proper nouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 31 | Late-layer: women & feminine identities |  personal names and associated titles | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 86 | Late-layer: women & feminine identities |  personal names and associated titles | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |
| [L17:F3558](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3558) | 31 | Mid-layer: female persons, feminine pronouns, name tokens |  mentions of people's names or pronouns referring to people | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3558) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 54 | Mid-layer: female persons, feminine pronouns, name tokens |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 68 | Mid-layer: female persons, feminine pronouns, name tokens |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L16:F2918](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) | 54 | Mid-layer: female persons, feminine pronouns, name tokens | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 54 | Mid-layer: female persons, feminine pronouns, name tokens |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 68 | Mid-layer: female persons, feminine pronouns, name tokens |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F9209](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/9209) | 31 | Mid-layer: female persons, feminine pronouns, name tokens |  names of people | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/9209) |
| [L14:F4385](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4385) | 31 | Mid-layer: female persons, feminine pronouns, name tokens | proper nouns, pronouns, and some verbs. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4385) |
| [L14:F8671](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8671) | 31 | Mid-layer: female persons, feminine pronouns, name tokens |  capitalized names of people | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8671) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 31 | Mid-layer: female persons, feminine pronouns, name tokens |  uses of the feminine pronoun. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L13:F4753](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4753) | 31 | Mid-layer: female persons, feminine pronouns, name tokens |  proper nouns, especially names of people | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4753) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 54 | Mid-layer: female persons, feminine pronouns, name tokens | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L13:F15487](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/15487) | 31 | Mid-layer: female persons, feminine pronouns, name tokens |  the names and professions of people and companies and certain article words | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/15487) |
| [L13:F15487](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/15487) | 86 | Mid-layer: female persons, feminine pronouns, name tokens |  the names and professions of people and companies and certain article words | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/15487) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 5 | Mid-layer: female persons, feminine pronouns, name tokens |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L12:F15193](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/15193) | 31 | Mid-layer: female persons, feminine pronouns, name tokens | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/15193) |
| [L12:F4810](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/4810) | 31 | Mid-layer: female persons, feminine pronouns, name tokens | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/4810) |
| [L8:F10019](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/10019) | 66 | Mid-layer: medical/obstetric professional content |  words and phrases associated with childbirth and labor | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/10019) |
| [L7:F2861](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2861) | 66 | Mid-layer: medical/obstetric professional content |  words and phrases relating to pregnancy and labor | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2861) |
| [L7:F7389](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7389) | 66 | Mid-layer: medical/obstetric professional content | text related to pregnancy and childbirth | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7389) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 12 | Mid-layer: medical/obstetric professional content |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L6:F11360](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11360) | 66 | Mid-layer: medical/obstetric professional content | words and phrases related to pregnancy and childbirth | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11360) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | Mid-layer: medical/obstetric professional content |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F5548](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5548) | 66 | Mid-layer: medical/obstetric professional content | a wide array of words associated with medical fields, women, sewing, or history. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5548) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | Mid-layer: medical/obstetric professional content |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 66 | Mid-layer: medical/obstetric professional content |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L2:F8648](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8648) | 66 | Mid-layer: medical/obstetric professional content |  words and phrases related to medicine, anatomy, and medical sciences | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8648) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 5 | Mid-layer: medical/obstetric professional content |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 31 | Mid-layer: medical/obstetric professional content |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 5 | Mid-layer: medical/obstetric professional content |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 12 | Mid-layer: medical/obstetric professional content | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 54 | Mid-layer: medical/obstetric professional content | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 5 | Mid-layer: medical/obstetric professional content |  first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L2:F1056](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1056) | 86 | Mid-layer: medical/obstetric professional content | names of people | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1056) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 5 | Layer 0: proper nouns & pronoun features |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 31 | Layer 0: proper nouns & pronoun features |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 86 | Layer 0: proper nouns & pronoun features |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F1276](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1276) | 5 | Layer 0: proper nouns & pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1276) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 66 | Layer 0: proper nouns & pronoun features | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 5 | Layer 0: proper nouns & pronoun features | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F9022](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9022) | 66 | Layer 0: proper nouns & pronoun features |  technical words used in computing, science, or engineering | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9022) |
| [L0:F3604](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3604) | 66 | Layer 0: proper nouns & pronoun features |  commands and filenames in code | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3604) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 54 | Layer 0: proper nouns & pronoun features | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 68 | Layer 0: proper nouns & pronoun features | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 54 | Layer 0: proper nouns & pronoun features |  the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 54 | Layer 0: proper nouns & pronoun features |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F14257](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14257) | 54 | Layer 0: proper nouns & pronoun features | the word 'newly' and adjectives ending in 'able' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14257) |
| [L0:F3232](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3232) | 54 | Layer 0: proper nouns & pronoun features |  mentions of the third person plural pronoun "They" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3232) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: Melissa (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: nurse (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: Labor (pos 9) / Delivery (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: Labor (pos 9) / Delivery (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: her (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 31 | Emb: Melissa (pos 31) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 54 | Emb: She (pos 54) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 66 | Emb: midwife (pos 66) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 68 | Emb: She (pos 68) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 86 | Emb: Melissa (pos 86) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:1276 de=0.559 |
| 3 | `inspect_feature` ×10 | L4:1276, L12:14970, L6:8166, L4:13803, L18:14677, L7:8644, L19:9685, L6:11646, L0:7532, L13:11685 |
| 4 | `get_upstream_features` | Emb:" nurse"@12 (de=2.33) +9 more |
| 5 | `get_upstream_features` | Emb:" She"@54 (de=14.56) +9 more |
| 6 | `get_upstream_features` | Emb:" Delivery"@11 (de=12.19) +9 more |
| 7 | `get_upstream_features` | Emb:" midwife"@66 (de=22.38) +9 more |
| 8 | `get_upstream_features` | Emb:" nurse"@12 (de=5.62) +9 more |
| 9 | `get_upstream_features` | Emb:" nurse"@12 (de=20.50) +9 more |
| 10 | `get_upstream_features` | Emb:" Melissa"@5 (de=6.94) +9 more |
| 11 | `get_upstream_features` | L4:F1276 (de=5.19) +9 more |
| 12 | `get_upstream_features` | L14:F4385 (de=2.17) +7 more |
| 13 | `get_upstream_features` | Emb:" She"@68 (de=14.06) +7 more |
| 14 | `get_upstream_features` | L17:F3558 (de=3.61) +7 more |
| 15 | `get_upstream_features` | Emb:" She"@54 (de=5.56) +7 more |
| 16 | `get_upstream_features` | Emb:" midwife"@66 (de=3.95) +7 more |
| 17 | `get_upstream_features` | Emb:" Melissa"@5 (de=9.62) +7 more |
| 18 | `get_upstream_features` | Emb:" midwife"@66 (de=22.38) +7 more |
| 19 | `get_upstream_features` | Emb:"<bos>"@0 (de=-2.64) +7 more |
| 20 | `get_upstream_features` | Emb:"<bos>"@0 (de=4.00) +7 more |
| 21 | `get_upstream_features` | Emb:" Melissa"@31 (de=3.73) +7 more |
| 22 | `get_upstream_features` | L13:F4753 (de=2.50) +7 more |
| 23 | `get_upstream_features` | Emb:" She"@54 (de=19.88) +7 more |
| 24 | `get_upstream_features` | Emb:" She"@54 (de=16.12) +7 more |
| 25 | `get_upstream_features` | Emb:" midwife"@66 (de=7.97) +7 more |
| 26 | `inspect_feature` ×18 | L18:3679, L18:9023, L13:4753, L14:12501, L14:4385, L17:5889, L15:3330, L6:15267, L0:15382, L0:12519, L6:16329, L0:9026, L2:5859, L17:3558, L0:9022, L0:3604, L0:9519, L13:15487 |
| 27 | `get_upstream_features` | Emb:"<bos>"@0 (de=-4.44) +5 more |
| 28 | `get_upstream_features` | Emb:"<bos>"@0 (de=2.28) +5 more |
| 29 | `get_upstream_features` | Emb:" She"@54 (de=13.38) +5 more |
| 30 | `get_upstream_features` | Emb:" She"@54 (de=14.69) +5 more |
| 31 | `get_upstream_features` | Emb:" midwife"@66 (de=7.97) +5 more |
| 32 | `get_upstream_features` | ❌ Feature (layer=18, feature_idx=3679) not found at pos=54. Th |
| 33 | `get_upstream_features` | Emb:"<bos>"@0 (de=-7.59) +5 more |
| 34 | `get_upstream_features` | Emb:"<bos>"@0 (de=-2.64) +5 more |
| 35 | `inspect_feature` ×10 | L17:7837, L15:9209, L14:8671, L6:2267, L8:10019, L6:5548, L2:8648, L2:1056, L0:14257, L0:3232 |
| 36 | `get_upstream_features` | Emb:"."@85 (de=-1.74) +7 more |
| 37 | `get_upstream_features` | Emb:" midwife"@66 (de=7.97) +5 more |
| 38 | `get_upstream_features` | L7:F2861 (de=11.31) +5 more |
| 39 | `inspect_feature` ×3 | L7:2861, L7:7389, L6:11360 |
| 40 | `get_upstream_features` | Emb:" midwife"@66 (de=17.25) +5 more |

### Build

`build_circuit` → 14 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 82,771 | 8,476 | 517,886 | 0 | $0.0661 | — | — |
| **Total** | | **82,771** | **8,476** | **517,886** | **0** | **$0.0661** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 51s