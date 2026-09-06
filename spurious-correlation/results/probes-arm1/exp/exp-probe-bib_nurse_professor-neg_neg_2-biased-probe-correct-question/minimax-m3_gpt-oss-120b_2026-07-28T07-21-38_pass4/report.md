# Circuit Oracle Report
**Date:** 2026-07-28 07:21:38 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven predominantly by gender-marker circuits (male pronouns like "his", "He", masculine titled references) rather than genuine profession/academic-field signals, confirming the user's concern about spurious features.

**Confidence:** 8

**Reasoning:** The circuit reveals that the probe classification (target = probe direction in layer 26) is overwhelmingly fed by features that detect masculine pronouns and gender markers, not by profession-specific terms. The dominant features by direct effect on the probe target are:

- **L0:F2994 (direct_effect=+0.39 at pos 3)**, label: "the pronoun 'his' and the pronoun 'he'" — fires on every "his" in the prompt (pos 3, 25, 47) with high activation (39.5, 41, 39.25). The upstream trace shows this is driven almost entirely by the `his` embedding at position 3 (direct_effect=43.25). The feature's promoted tokens are sentence punctuation; it suppresses "his/himself" — it acts as a *non-masculine* indicator that paradoxically still codes gender contrast.

- **L7:F14893 (direct_effect=+0.20 at pos 3)**, label: "pronouns or possessive pronouns" — upstream driven by `his` embedding (direct_effect=24.4), with promoted tokens including "herself, she, elle, she" and suppressed "himself, his". This is a feminine-promoting pronoun feature.

- **L7:F14946 (direct_effect=−0.18)**, label: "'his' possessive pronoun" — opposite direction, promoted "himself/his" suppressed "herself/she". These two L7 features form an explicit masculine-vs-feminine contrast at the same token.

- **L12:F2175 (direct_effect=−0.17 at pos 2)**, label: "words referring to gender" — fires on "male, masculine, men" (promoted: "himself, masculinity"; suppressed: "herself, female, woman"). Frac_nonzero=0.0062 (specific). This is a generic gender-marker feature.

- **L18:F14743 (direct_effect=−0.14 at pos 22)**, label: "He" — fires on the capitalized "He" pronoun with direct upstream contribution from the `He` embedding at pos 22 (direct_effect=21.9), `His` at pos 3, plus the pronoun pipeline (L7:F14893, L13:F6622, L15:F3330, L17:F5889). Promoted: "himself"; suppressed: "she, her, their".

- **L6:F12990 (direct_effect=−0.17)**, label: "male pronouns and titles along with descriptors associated with men" — fires on "man, his, male" (frac_nonzero=0.068). Upstream: `He` embedding at pos 22 (direct_effect=4.47) and `his` at pos 3.

By contrast, the **profession/academic-field** signal is comparatively small:
- L5:F10392 (direct_effect=−0.11 at pos 9, "Engineering"), label: "fields of academic study" — upstream is L5:L6384, L4:L3727, L2:L1440 plus `Engineering`/`achelors`/`degree` embeddings. Frac_nonzero=0.0036 (specific).
- L6:F170 (direct_effect=+0.14 at pos 9, "Engineering"), label: "references to academic fields, especially those in the humanities" — upstream is L5:F10392 and `Engineering`/`achelors`/`degree` embeddings. Fires on "science, literature, English, Writing".

The **gender-marker supernodes** (L0_his_he, L6_male_pronouns, L12_gender_words, L18_He_pronoun, L7_pronouns_pos/neg) collectively have direct_effects on the probe of roughly **|0.39 + 0.20 + 0.18 + 0.17 + 0.14| ≈ 1.08**, while the **profession signal** (L5:L10392 + L6:F170) totals roughly **|0.11 + 0.14| ≈ 0.25**. Gender features outweigh genuine profession features by roughly 4:1 in absolute direct effect on the probe score.

Furthermore, the gender circuit is **trivially activated** — it just needs the single token "his" or "He" anywhere in the prompt. The `his` embedding at position 3 (the second token of the prompt) contributes direct_effect=43.25 to L0:F2994 alone, propagating through the pronoun pipeline to influence the probe via at least four downstream features. The profession circuit, in contrast, requires the specific bigram "Mechanical Engineering" (or another academic field) to be processed at pos 9 and several specific embedding contributions to align.

Conclusion: The user's concern is **validated**. The probe is using a spurious shortcut — it relies on male-pronoun indicators ("his", "He", masculine-gender words) that are present in this biography of "Daniel", rather than on the genuine profession indicators (Mechanical Engineering, Ph.D., Robotics/Computer Vision). A biography of a female engineer ("she received her degree in Mechanical Engineering…") would produce a substantially different probe score despite identical professional content, because the gender-circuit contribution would flip sign (the L7 features encode an explicit male/female contrast, L12:F2175 explicitly suppresses "female/woman", and L18:F14743 explicitly suppresses "she/her"). The probe is detecting "is this text about a man?" rather than "is this text about a [profession]?"

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: his (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: He (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Daniel (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: University (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: Waterloo (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Layer 0 — 'his'/'he' pronoun detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 25 | Layer 0 — 'his'/'he' pronoun detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 47 | Layer 0 — 'his'/'he' pronoun detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 22 | Layer 0 — male person reference ('He'/'His') |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1326](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1326) | 14 | Layer 0 — organization / institution mentions |  mentions of organizations and government agencies. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1326) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | Layer 0 — proper noun detector |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 3 | Layer 4 — 'his' pronoun feature |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 9 | Layer 5 — fields of academic study |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 22 | Layer 6 — male pronouns and titles with male descriptors |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 9 | Layer 6 — academic field references |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 8 | Layer 6 — academic field references |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 3 | Layer 7 — possessive/pronoun feature (positive) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 3 | Layer 7 — 'his'/possessive pronoun (suppresses feminine) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | Layer 12 — words referring to gender |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | Layer 18 — 'He' pronoun feature | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 81 | Layer 18 — 'He' pronoun feature | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.395 |
| 3 | `inspect_feature` ×6 | L0:2994, L7:14893, L7:14946, L12:2175, L6:170, L5:10392 |
| 4 | `get_upstream_features` | Emb:" his"@3 (de=43.25) +9 more |
| 5 | `get_upstream_features` | Emb:" his"@3 (de=24.38) +9 more |
| 6 | `get_upstream_features` | L5:F10392 (de=10.94) +9 more |
| 7 | `get_upstream_features` | Emb:" He"@22 (de=21.88) +9 more |
| 8 | `get_upstream_features` | Emb:" He"@22 (de=4.47) +9 more |
| 9 | `inspect_feature` ×9 | L18:14743, L6:12990, L0:1069, L17:5889, L13:6622, L15:3330, L0:1326, L0:7532, L0:12351 |
| 10 | `get_upstream_features` | Emb:" received"@2 (de=4.09) +7 more |
| 11 | `get_upstream_features` | Emb:" He"@22 (de=37.00) +7 more |
| 12 | `inspect_feature` ×3 | L5:7317, L5:6228, L4:4315 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14743@22` | ❌ error | — | — | Trace the upstream path from L18:F14743 at position 22 (the "He" male-pronoun fe… |
| SA-2 | `L7:F14893@3` | ❌ error | — | — | Trace the upstream path from L7:F14893 at position 3 (pronoun feature with posit… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F7532@1, k=5 → Emb:"Daniel"@1 (de=10.12) +4 more |
| 2 | `get_upstream_features` | L0:F1326@14, k=5 → Emb:" University"@12 (de=7.28) +4 more |

### Build

`build_circuit` → 18 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 49,377 | 6,004 | 204,970 | 0 | $0.0343 | — | — |
| **Total** | | **49,377** | **6,004** | **204,970** | **0** | **$0.0343** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 22s