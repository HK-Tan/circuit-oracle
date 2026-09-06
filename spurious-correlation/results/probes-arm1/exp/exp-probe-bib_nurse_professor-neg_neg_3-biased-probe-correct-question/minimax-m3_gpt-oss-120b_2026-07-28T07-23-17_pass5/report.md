# Circuit Oracle Report
**Date:** 2026-07-28 07:23:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a chain of male-pronoun features, with the profession-relevant content (academic fields, degree) being a minor secondary contributor.

**Confidence:** 8

**Reasoning:** Tracing the attribution graph from output to embeddings reveals that the dominant signal flow is a gender-marker pathway, not a profession-indicator pathway:

1. **Male-pronoun signal chain (the dominant pathway).** At the very top of the circuit is **L18:F14743** (label "He", frac_nonzero=0.018, max_token "▁He"), which receives large direct_effects from " He" embeddings at positions 21 and 42 (direct_effect ~24), and from L0:F1069 (the "He/His" male-person feature, direct_effect ~7.7-8.4). F1069 itself is fed directly by the "He"/" He" embeddings. F14743's top activating examples and suppressed tokens ("▁she", "▁her") confirm it specifically represents subject "He". Below F14743, the chain goes F1069 → F5889 (L17, "He") → F6622 (L13) → F2587 (L9, third-person pronoun) → F1069 (L0). So a deep, dedicated circuit converts the literal tokens "He" and " His" into a robust late-layer "male subject" feature. Note that F14743 has direct_effect = **-0.1475** on the probe target (it's a suppressor), so the male-pronoun pathway is actually PUSHING DOWN on the probe classification score — but a competing path, F14893 (L7, generic pronoun, direct_effect +0.167) and the embeddings for "He"/"His" at L0 (F2994, F1069, F14893) push the probe POSITIVELY.

2. **The "anti-suppressor" effect (the actual driver).** Looking at the top-feature list, the most positively-contributing features are F2994 (L0, "his/he pronoun", direct_effect +0.30 and +0.16), F14893 (L7, generic pronoun, +0.17), F1069 (L0, He/His, +0.15), and L6:F170 ("academic fields especially humanities", +0.12). F2994 fires at positions 3, 23, 44 — the three " his" embeddings — and the upstream confirms it is directly driven by the " his" token embedding (direct_effect 42-45 at each). Critically, F2994's promoted tokens are "▁" and ".", and its **suppressed tokens include "his"**, meaning its decoder direction moves AWAY from the pronoun semantically but its firing on " his" embeddings still gives it positive direct_effect on the probe.

3. **Profession/academic field pathway (secondary).** The genuine profession content shows up in **L5:F10392** ("fields of academic study", activated on "Mathematics", "science", "Management"), which feeds **L6:F170** ("references to academic fields, especially humanities", fires on "science"/"literature"). F170 receives direct input from the " Mathematics" embedding (pos 10) and from L0:F6127 (the "degree" feature, direct_effect = 16.9 on its own embedding). However, F10392 has only direct_effect contribution through F170, and F170's direct_effect on the probe is only +0.12. The "degree" feature F6127 is the only profession-leakage feature with strong direct effect, but it sits at L0 and its label ("degree and words associated with academia, especially higher education") is academic-vocabulary, not specifically "professor"/"computer science".

4. **Conclusion regarding the user's concern.** The user's hypothesis is CONFIRMED. The circuit is dominated by male-gender/masculine-pronoun features (F1069, F2994, F12990, F14743, F2175, F5889, F14893, F2587) and a generic academic-vocabulary feature (F6127 = "degree"). There is no late-layer feature that specifically encodes "professor" or "computer science" or any specific profession. The only profession-relevant feature is F170/L6 ("academic field names" — a generic category, not a profession), and its contribution (+0.12) is dwarfed by the cumulative male-pronoun feature contributions (F2994 +0.30 + 0.16 + 0.14, F14893 +0.17 + 0.12 + 0.12, F1069 +0.15, etc., all pushed by "He"/"his" embeddings at multiple positions). The model has learned to use "He/His" as a spurious shortcut correlated with the biography's author gender, rather than identifying the actual profession "Computer Science professor" from the text.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Male pronoun detector (his/he) — L0:F2994 | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 23 | Male pronoun detector (his/he) — L0:F2994 | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 44 | Male pronoun detector (his/he) — L0:F2994 | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male-person reference (He/His) — L0:F1069 |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 21 | Male-person reference (He/His) — L0:F1069 |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 42 | Male-person reference (He/His) — L0:F1069 |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F6127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) | 8 | 'degree' / academic words — L0:F6127 |  instances of the word "degree" and words associated with academia, especially higher education | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 13 | 'whom' / function-word — L0:F6270 | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Male pronouns/titles — L6:F12990 |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | Male pronouns/titles — L6:F12990 |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 21 | Male pronouns/titles — L6:F12990 |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 42 | Male pronouns/titles — L6:F12990 |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | Academic field names — L6:F170 |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Possessive 'his' (with ©/he) — L7:F14946 |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | Possessive 'his' (with ©/he) — L7:F14946 |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 3 | Possessive 'his' (with ©/he) — L7:F14946 |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Generic pronoun — L7:F14893 |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 2 | Generic pronoun — L7:F14893 |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 3 | Generic pronoun — L7:F14893 |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L9:F2587](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2587) | 2 | Third-person pronoun — L9:F2587 |  references to personal pronouns in the third person, and possibly first person | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2587) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | Gender-words — L12:F2175 |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 21 | 'He' biography mid-feature — L13:F6622 | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 21 | Personal-story pronoun (he/she) — L15:F3330 |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 42 | Personal-story pronoun (he/she) — L15:F3330 |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F7191](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/7191) | 21 | People/places/dates (biographical) — L15:F7191 |  words associated with people, places, organizations, and dates, possibly from biographical data | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/7191) |
| [L15:F7191](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/7191) | 42 | People/places/dates (biographical) — L15:F7191 |  words associated with people, places, organizations, and dates, possibly from biographical data | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/7191) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 21 | Subject 'He' — L17:F5889 | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 21 | 'He' late feature (pushes probe) — L18:F14743 | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 42 | 'He' late feature (pushes probe) — L18:F14743 | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | Fields of academic study — L5:F10392 |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.297 |
| 3 | `inspect_feature` ×10 | L0:2994, L0:6270, L6:12990, L7:14946, L7:14893, L18:14743, L12:2175, L0:1069, L0:6127, L6:170 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ❌ error | — | — | Trace upstream from L0:F2994 (his/he pronoun feature at pos 3) to find which inp… |
| SA-2 | `L6:F12990@21` | ❌ error | — | — | Trace upstream from L6:F12990 (male pronouns/titles feature) to find which input… |
| SA-3 | `L18:F14743@21` | ❌ error | — | — | Trace upstream from L18:F14743 ("He" feature at pos 21) to find its upstream cir… |
| SA-4 | `L12:F2175@2` | ❌ error | — | — | Trace upstream from L12:F2175 (gender words feature at pos 2) to find which feat… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2994@3, k=10 → Emb:" his"@3 (de=42.50) +9 more |
| 2 | `get_upstream_features` | L0:F2994@44, k=10 → Emb:" his"@44 (de=45.50) +9 more |
| 3 | `get_upstream_features` | L0:F2994@23, k=10 → Emb:" his"@23 (de=45.25) +9 more |
| 4 | `get_upstream_features` | L18:F14743@21, k=10 → Emb:" He"@21 (de=23.38) +9 more |
| 5 | `get_upstream_features` | L18:F14743@42, k=10 → Emb:" He"@42 (de=24.62) +9 more |
| 6 | `get_upstream_features` | L12:F2175@2, k=10 → L7:F14946 (de=4.50) +9 more |
| 7 | `get_upstream_features` | L6:F12990@21, k=10 → Emb:" He"@21 (de=4.59) +9 more |
| 8 | `get_upstream_features` | L17:F5889@21, k=8 → Emb:" He"@21 (de=22.50) +7 more |
| 9 | `get_upstream_features` | L13:F6622@21, k=8 → Emb:" He"@21 (de=13.38) +7 more |
| 10 | `inspect_feature` ×4 | L15:3330, L15:7191, L6:2267, L9:2587 |
| 11 | `get_upstream_features` | L9:F2587@2, k=8 → Emb:"He"@1 (de=6.91) +7 more |
| 12 | `inspect_feature` | L0, F6127 → " instances of the word "degree" and words associated with academia, es" |
| 13 | `get_upstream_features` | L0:F6127@8, k=8 → Emb:" degree"@8 (de=16.88) +7 more |
| 14 | `get_upstream_features` | L6:F170@10, k=8 → L5:F10392 (de=11.38) +7 more |
| 15 | `get_upstream_features` | L5:F10392@10, k=5 → L3:F4113 (de=3.34) +4 more |
| 16 | `inspect_feature` | L5, F10392 → " fields of academic study" |

### Build

`build_circuit` → 25 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 36,991 | 6,530 | 223,777 | 0 | $0.0324 | — | — |
| **Total** | | **36,991** | **6,530** | **223,777** | **0** | **$0.0324** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 43s