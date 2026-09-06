# Circuit Oracle Report
**Date:** 2026-07-28 07:21:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by male-gendered pronoun features (He/His) extracted from token embeddings, not by any profession or role indicator — the user's concern about spurious gender-based features is confirmed.

**Confidence:** 9

**Reasoning:**

The attribution graph reveals a circuit dominated by **male pronoun/gender marker features** at every layer, with negligible contribution from profession-related content.

**Dominant positive path (driving the probe score):**
- **L0:F2994** at pos 37/55 ("His" tokens, activation ~40, direct_effect=+0.254) — the single largest positive contributor. Its autointerp label is *"the pronoun 'his' and the pronoun 'he.'"* Its upstream source is overwhelmingly the `His` embedding at pos 13 (direct_effect=18.75) and the `He` embedding at pos 1.
- **L0:F2848** at pos 5 ("of", direct_effect=+0.148) and **L0:F11024** at pos 4 ("Director" / "clock" in context — weakly related to the role "Director of") — the only faintly profession-related L0 features, with modest contributions.
- **L7:F14893** at pos 1/13 ("pronouns or possessive pronouns", direct_effect=+0.132) and **L7:F14946** at pos 1 (negative, -0.115) — these are pronoun detectors, not profession detectors.
- **L4:F4315** at pos 13 ("mentions of 'his' and other associated pronouns", negative direct_effect=-0.109) — again pure gender.
- **L6:F12990** ("male pronouns and titles along with descriptors associated with men") — fires at multiple positions (1, 2, 13, 35), suppressing the probe score (-0.166, -0.125, -0.114, -0.099). This is the strongest **anti-gender** signal, but its label explicitly confirms it encodes male-gender markers.
- **L9:F2984** ("mentions of gendered pronouns", negative) and **L12:F2175** ("words referring to gender", negative -0.108) — both gender-word detectors.

**Tracing deeper confirmed the story:** The L18:F14743 ("He") feature, which directly suppresses the probe (-0.141), traces back through L17:F3683 ("biographies") and L17:F5889 ("references to people with pronouns and possessive pronouns") and L15:F3330 ("personal stories...pronoun 'she'") — all the way to the `He` embedding at pos 35 (direct_effect=23.6). Even the biography/role features route their signal through pronoun detectors.

**The L11:F8266** ("people with professional titles or descriptions, especially in healthcare") does fire at pos 35 but is far down the ranking. No feature encoding "professor," "researcher," "computer science," or similar profession content appears in the top 20.

**Conclusion:** The user is correct — the circuit is overwhelmingly **spurious**. The top positive driver (L0:F2994, +0.254) is literally the "his/he" pronoun detector. The anti-male features (L6:F12990 at -0.166, L12:F2175 at -0.108, L4:F4315 at -0.109) reduce the male-pronoun signal but still route through gender features. No substantive profession features (e.g., "professor," "research interests," "Ph.D.") appear in the circuit. The probe is essentially being activated by the fact that the subject is **male-coded through pronoun usage**, with token embeddings for "He" (pos 1), "His" (pos 13), and "He" (pos 35) providing the bulk of the upstream signal.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 35 | L0: Male-reference pronoun features (he/His) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 13 | L0: Male-reference pronoun features (he/His) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 37 | L0: Male-reference pronoun features (he/His) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 55 | L0: Male-reference pronoun features (he/His) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 5 | L0: Content-word features (Director, of, Lab) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | L0: Content-word features (Director, of, Lab) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |
| [L0:F11024](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) | 4 | L0: Content-word features (Director, of, Lab) |  the word "clock", especially in a technical context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) |
| [L0:F3214](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3214) | 4 | L0: Content-word features (Director, of, Lab) |  titles followed by names or URLs from government sites | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3214) |
| [L0:F10846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) | 3 | L0: Content-word features (Director, of, Lab) | the word "also" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) |
| [L0:F13731](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13731) | 11 | L0: Content-word features (Director, of, Lab) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13731) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 13 | L4: Pronoun/gender-word features |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 1 | L4: Pronoun/gender-word features | the pronoun "he" or "him" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 1 | L4: Pronoun/gender-word features | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L4:F993](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/993) | 2 | L4: Pronoun/gender-word features | contractions of the verb to be in the third person singular | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/993) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | L4: Pronoun/gender-word features | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6: Male pronoun/titles features |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | L6: Male pronoun/titles features |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 13 | L6: Male pronoun/titles features |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 35 | L6: Male pronoun/titles features |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F10944](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10944) | 2 | L6: Male pronoun/titles features |  text in languages other than English | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10944) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7: Pronoun/possessive features |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 13 | L7: Pronoun/possessive features |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7: Pronoun/possessive features |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | L7: Pronoun/possessive features |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L9:F2984](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2984) | 2 | L9: Gendered pronoun features |  mentions of gendered pronouns, often with a conjunction | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2984) |
| [L9:F12373](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12373) | 2 | L9: Gendered pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12373) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | L12: Gender-word feature |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 35 | L13: Pronoun feature |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 35 | L15: Personal-story pronoun feature |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 35 | L17: Biography/people-with-pronouns features |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F3683](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) | 35 | L17: Biography/people-with-pronouns features | biographies | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 35 | L18: 'He' pronoun feature (suppress) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.254 |
| 3 | `inspect_feature` ×4 | L0:2994, L0:2848, L0:11024, L7:14893 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace upstream from L7:F14893. This feature is described as "pronouns or possess… |
| SA-2 | `L0:F2994@37` | ❌ error | — | — | Trace upstream from L0:F2994. This feature is described as "the pronoun 'his' an… |
| SA-3 | `L6:F12990@2` | ❌ error | — | — | Trace upstream from L6:F12990. This feature has negative direct effect on the pr… |
| SA-4 | `L18:F14743@35` | ❌ error | — | — | Trace upstream from L18:F14743. This is a mid-layer feature with negative direct… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×9 | L6:12990, L18:14743, L7:14946, L0:8658, L4:4315, L12:2175, L2:13731, L0:10846, L0:3214 |
| 2 | `get_upstream_features` | L18:F14743@35, k=10 → Emb:" He"@35 (de=23.62) +9 more |
| 3 | `get_upstream_features` | L6:F12990@13, k=10 → Emb:" His"@13 (de=5.28) +9 more |
| 4 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"He"@1 (de=14.75) +9 more |
| 5 | `get_upstream_features` | L7:F14946@2, k=10 → Emb:"He"@1 (de=9.00) +9 more |
| 6 | `get_upstream_features` | L12:F2175@2, k=10 → L7:F14946 (de=5.41) +9 more |
| 7 | `inspect_feature` ×17 | L0:1069, L17:5889, L13:6622, L17:3683, L15:3330, L11:8266, L2:5491, L5:14955, L4:9757, L4:14796, L2:9301, L4:15567, L4:993, L6:10944, L9:2984, L5:645, L3:13121 |
| 8 | `get_upstream_features` | L0:F8658@2, k=5 → Emb:"He"@1 (de=8.00) +4 more |
| 9 | `get_upstream_features` | L0:F2848@5, k=5 → Emb:" of"@5 (de=34.75) +4 more |
| 10 | `get_upstream_features` | L0:F2994@13, k=5 → Emb:" His"@13 (de=18.75) +4 more |

### Build

`build_circuit` → 18 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 89,954 | 6,144 | 176,399 | 0 | $0.0449 | — | — |
| **Total** | | **89,954** | **6,144** | **176,399** | **0** | **$0.0449** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 21s