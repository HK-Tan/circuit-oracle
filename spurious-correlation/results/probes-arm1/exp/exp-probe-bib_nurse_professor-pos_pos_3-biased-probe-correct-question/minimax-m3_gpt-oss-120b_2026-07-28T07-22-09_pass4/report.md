# Circuit Oracle Report
**Date:** 2026-07-28 07:22:09 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mixture of two pathways: (1) a dominant **gender/women-mentioned pathway** triggered by the pronoun "She" and the female-gendered word "Linda" at the very start of the text, and (2) a secondary **profession/medical-specialty pathway** activated by "nurse practitioner" and "labor and delivery" tokens. The gender pathway carries the highest direct-effect features, indicating the probe relies heavily on female-marker cues rather than profession-specific terminology alone.

**Confidence:** 7

**Reasoning:** The top direct-effect features are gender-notional, not profession-notional:
- **L18:F14677** (activation ~30, direct_effect 0.32; "instances of women or girls being mentioned") and **L19:F9685** (direct_effect 0.24; "women's names and their roles or accomplishments") are late-layer abstractions that fire on the "She" pronoun and "Linda" name. Their upstream is dominated by the embedding of "She" (pos 1, direct_effect 27.1) feeding into mid-layer features like **L6:F11646** ("references to women, potentially triggered by pronouns and titles"), **L10:F14965** ("terms relating to women"), **L7:F2765** ("mentions of people or characters…personal details"), and **L12:F12940** ("female pronouns and possessive pronouns").
- These converge on the probe direction via two more supernodes: a "naming" pathway (L2:F5859 "first names (mostly female)", L12:F14970 "names of people", L16:F6025 "capitalized first names") fed by the "Linda" embedding at pos 24 (direct_effect 3.45 into L19:F9685), and a generic "she" pronoun chain (L4:F7864, L4:F15317 — both with promoted_tokens "herself/she/her" and suppressed_tokens "himself/his").
- The **profession pathway** is genuine but smaller: L6:F15267 ("words…referring to the profession of nursing", direct_effect 0.39, max activation on "nurse"/"RN") at pos 8, fed by the "nurse" embedding (pos 7, direct_effect 7.06) and L5:F1275 ("healthcare professionals and medical fields"), L1:F1494 ("words related to medical practices"). L4:F13803 ("terms related to obstetrics and gynecology", promoted "pregnancy/postpartum") and L3:F9008 ("words related to childbirth or birth") fire on "labor"/"delivery" embeddings (pos 44/46, direct_effect 10.2/13.8) and connect to the probe direction.
- **The user's concern is partially supported**: the probe's top features and the single largest embedding contribution come from "She" (pos 1, direct_effect 27.1 into L18:F14677) and "Linda" (pos 24, direct_effect 3.45 into L19:F9685) — female-name/marker features. The L12:L18:L19 chain from "She" → L12:F12940 → L18:F14677 → probe is causally large and is the dominant signal in the graph. However, genuine profession features (L6:F15267, L4:F13803, L3:F9008) also contribute directly to the output, so this is **not purely a gender-spurious circuit** — it is a **mixed circuit** in which female-gender markers (pronoun + female first name) supply most of the upward signal while nursing/obstetrics vocabulary supplies a smaller profession-specific contribution. Because the gender features have the highest direct effects and frac_nonzero values (~0.01–0.02, low/specific), they are doing targeted, entity-level work rather than firing generically; they would likely also fire on a male nurse text but with different sign, so the probe is using a combination of *gender co-occurrence with profession* rather than a pure gender shortcut, but the gender leg is the stronger of the two.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output Logit (probe classification) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 24 | Late-layer "women mentioned" features |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer "women mentioned" features |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 55 | Late-layer "women mentioned" features |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Late-layer "women mentioned" features | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer female pronoun/women features |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer female pronoun/women features |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Mid-layer female pronoun/women features |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | Mid-layer female pronoun/women features |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 24 | Proper-name and person features |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L16:F6025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6025) | 24 | Proper-name and person features |  capitalized first names, sometimes followed by last names | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6025) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 24 | Proper-name and person features |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 24 | Proper-name and person features |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 24 | Proper-name and person features |  first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 24 | Proper-name and person features |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Profession "nurse" features |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 8 | Profession "nurse" features | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 8 | Profession "nurse" features |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 8 | Profession "nurse" features |  words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 46 | Obstetrics/gynecology/childbirth features |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 46 | Obstetrics/gynecology/childbirth features |  words related to childbirth or birth in general, including in animals. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 24 | Emb: Linda (pos 24) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: nurse (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 44 | Emb: labor (pos 44) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: delivery (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.494 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ❌ error | — | — | Trace this feature (L18:F14677) upstream to understand what it encodes. This fir… |
| SA-2 | `L6:F15267@8` | ❌ error | — | — | Trace this feature (L6:F15267) upstream — it has very high activation (23.4) and… |
| SA-3 | `L4:F13803@46` | ❌ error | — | — | Trace L4:F13803 at pos 46 upstream. This has high activation (21.75) and direct_… |
| SA-4 | `L12:F12940@2` | ❌ error | — | — | Trace L12:F12940 at pos 2 upstream. This has activation 15.5 and direct_effect 0… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×12 | L18:14677, L6:15267, L4:13803, L6:11646, L4:7864, L4:15317, L12:14970, L12:12940, L7:2765, L7:8644, L6:8166, L19:9685 |
| 2 | `get_upstream_features` | L18:F14677@1, k=10 → Emb:"She"@1 (de=27.12) +9 more |
| 3 | `get_upstream_features` | L6:F15267@8, k=10 → Emb:" nurse"@7 (de=7.06) +9 more |
| 4 | `get_upstream_features` | L4:F13803@46, k=10 → Emb:" delivery"@46 (de=13.81) +9 more |
| 5 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:"She"@1 (de=6.03) +9 more |
| 6 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 7 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"She"@1 (de=24.62) +9 more |
| 8 | `get_upstream_features` | L4:F15317@2, k=10 → Emb:"She"@1 (de=13.56) +9 more |
| 9 | `get_upstream_features` | L12:F14970@24, k=10 → Emb:"<bos>"@0 (de=-3.17) +9 more |
| 10 | `get_upstream_features` | L19:F9685@24, k=10 → Emb:" Linda"@24 (de=3.45) +9 more |
| 11 | `get_upstream_features` | L7:F2765@24, k=10 → Emb:"She"@1 (de=3.12) +9 more |
| 12 | `get_upstream_features` | L6:F8166@24, k=10 → L5:F6637 (de=-3.17) +9 more |
| 13 | `inspect_feature` ×9 | L15:851, L11:9183, L10:12232, L5:1275, L4:11037, L1:1494, L3:9008, L10:14965, L8:7245 |
| 14 | `get_upstream_features` | L19:F9685@1, k=8 → ❌ Feature (layer=19, feature_idx=9685) not found at pos=1. Thi |
| 15 | `get_upstream_features` | L15:F851@1, k=8 → L12:F12493 (de=22.38) +7 more |
| 16 | `inspect_feature` ×7 | L9:8770, L12:12493, L4:1276, L2:5859, L0:7532, L13:8128, L16:6025 |

### Build

`build_circuit` → 11 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 55,036 | 5,249 | 247,533 | 0 | $0.0377 | — | — |
| **Total** | | **55,036** | **5,249** | **247,533** | **0** | **$0.0377** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 38s