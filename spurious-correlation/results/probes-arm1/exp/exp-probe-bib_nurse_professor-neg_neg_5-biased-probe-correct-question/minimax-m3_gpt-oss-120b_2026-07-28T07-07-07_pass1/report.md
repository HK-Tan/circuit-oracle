# Circuit Oracle Report
**Date:** 2026-07-28 07:07:07 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession classification is driven primarily by gender/pronoun features tracking the male subject ("His", "He") rather than by genuine profession indicators in the biography.

**Confidence:** 8

**Reasoning:** The attribution circuit is dominated by male-pronoun features, not by features encoding academic profession signals.

- **Top drivers of the probe score** are pronoun/gender features with the largest signed effects coming from L7:F14893 (+0.49) and L0:F2994 (+0.38, +0.26), and L19:F8814 (+0.29). L7:F14946 (-0.49) and L6:F12990 (-0.34) push in the opposite direction (suppressors).
- **The "His" cascade (pos 1)**: The token embedding "His" at pos 1 directly excites L0:F2994 ("the pronoun his and he", frac_nonzero=0.073). This token signal propagates through L4:F4315 ("his and other pronouns like he, him, hers"), L6:F12990 ("male pronouns and titles along with descriptors associated with men"), and L7:F14946 ("possessive pronoun his ... he ... him"). At L18, F7400 promotes masculine tokens (▁himself, ▁his) and suppresses feminine ones (▁herself, ▁she). At L19, F8814 is a generic pronoun aggregator whose promoted tokens are feminine (▁herself, ▁she, ▁her) — i.e., it carries a "person reference" signal. The chain is explicitly traced to embedding nodes Emb: His (pos 1) and Emb: He (pos 10) via L0:F1069.
- **The "He" cascade (pos 10)**: L18:F14743 (pos 10) is a "He" detector with promoted tokens ▁himself/▁Himself. It is fed by L0:F1069 ("references to a male person, particularly when using the pronoun He or His", frac_nonzero=0.0078) — a sharp, selective male-pronoun feature — and the same feature recurs at pos 23 ("He also holds...").
- **Education features are weakly present and gender-biased**: L22:F12117 (pos 11, "received") nominally encodes "actions people take" but its promoted tokens are ▁his/himself/▁he, meaning the action-verb detector is itself a male-pronoun route. L19:F11110 detects "people's education history" with promoted tokens ▁Masters/Master. L8:F7587 detects education/qualification terms. However, these features are downstream of, and partly driven by, the pronoun signal at the same position (L18:F14743 pos 10 contributes +2.62 to F12117 at pos 11). Genuine semantic profession features (e.g., "transnational business history", "Ph.D.", "Economics", "M.B.A.", "Stanford/Harvard/Chicago") are largely absent from the top of the attribution list — only the generic "received" and "Economics"-position L0:F1773 appear, with no entity-recognizing feature in mid-layers.
- **Mechanism**: The probe's positive direction is activated by a stack of low-frac_nonzero, gender-selective pronoun detectors (F2994 0.073, F1069 0.0078, F12990 0.068, F14946 0.017, F7400 0.016, F14743 0.018) whose strongest input is the *emb* of the masculine pronoun tokens "His" and "He". The male-pronoun features both promote masculine tokens and the L19:F8814 aggregator, which then feeds the probe. The competing negative-direction features (L7:F14946, L6:F12990, L4:F4315) at pos 1 are also male-pronoun detectors — they suppress the score, but the positive net at pos 1 is driven by the same pronoun signal.
- **Spuriousness confirmed**: The user concern is correct. The circuit is essentially "male pronoun → probe" rather than "academic credentials in business/economics/history → probe". Identity-relevant profession content (Ph.D., MBA, business history, Economics, university names) is barely represented in the top features; the dominant signal is the gendered subject reference. The probe appears to have learned an association between male subjects and the target profession class, so a male pronoun alone (without the profession-indicating text) would likely yield a similar score. This is a textbook spurious-correlation artifact: the probe relies on a demographic cue (gender of the subject) instead of discriminative content (the field of study, degree type, or institutional prestige).

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Late pronoun features (pos 1, "His") — promote feminine, suppress masculine tokens |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Late pronoun features (pos 1, "His") — promote feminine, suppress masculine tokens |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Late pronoun features (pos 1, "His") — promote feminine, suppress masculine tokens | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Late pronoun features (pos 1, "His") — promote feminine, suppress masculine tokens |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Late pronoun features (pos 1, "His") — promote feminine, suppress masculine tokens |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Male pronoun / titles detectors (pos 1 and pos 10) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Male pronoun / titles detectors (pos 1 and pos 10) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 10 | Male pronoun / titles detectors (pos 1 and pos 10) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 10 | Male pronoun / titles detectors (pos 1 and pos 10) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Male pronoun / titles detectors (pos 1 and pos 10) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L22:F12117](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) | 11 | Education/qualification features (pos 11, "received") — promote masculine tokens |  references to actions that people can take or have taken. | [view](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) |
| [L19:F11110](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/11110) | 11 | Education/qualification features (pos 11, "received") — promote masculine tokens | text describing people's education history | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/11110) |
| [L8:F7587](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7587) | 11 | Education/qualification features (pos 11, "received") — promote masculine tokens | words related to education and professional qualifications | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7587) |
| [L21:F6216](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/6216) | 10 | Education/qualification features (pos 11, "received") — promote masculine tokens | — | [view](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/6216) |
| [L20:F10934](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/10934) | 11 | Education/qualification features (pos 11, "received") — promote masculine tokens | action verbs with past tense forms | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/10934) |
| [L12:F10137](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10137) | 20 | Education/qualification features (pos 11, "received") — promote masculine tokens | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10137) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Base L0 pronoun feature (pos 1 and 12) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 12 | Base L0 pronoun feature (pos 1 and 12) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1773](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1773) | 8 | Base L0 pronoun feature (pos 1 and 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1773) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | Base L0 pronoun feature (pos 1 and 12) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L4:F11633](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11633) | 11 | Base L0 pronoun feature (pos 1 and 12) | words related to education and employment history | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11633) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.490 |
| 3 | `inspect_feature` ×4 | L7:14893, L0:2994, L19:8814, L6:12990 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F8814@1` | ✅ reported | 5 | 7 | Trace upstream from L19:F8814 (various pronouns/names referring to people). What… |
| SA-2 | `L7:F14893@1` | ✅ reported | 3 | 5 | Trace upstream from L7:F14893 (pronouns/possessive pronouns). This feature has h… |
| SA-3 | `L18:F14743@10` | ✅ reported | 6 | 9 | Trace upstream from L18:F14743 (pos 10, negative effect). Pos 10 corresponds to … |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F8814 | " various pronouns and names referring to people" |
| 2 | `get_upstream_features` | L19:F8814@1, k=10 | Emb:"His"@1 (de=9.31) +9 more |
| 3 | `inspect_feature` | L18, F7400 | " words related to coding and software/UI interfaces, with some bias to" |
| 4 | `get_upstream_features` | L18:F7400@1, k=10 | Emb:"His"@1 (de=13.00) +9 more |
| 5 | `inspect_feature` | L7, F14946 | " the possessive pronoun "his" (or similar pronouns like "he" and "him"" |
| 6 | `get_upstream_features` | L7:F14946@1, k=10 | Emb:"His"@1 (de=18.38) +9 more |
| 7 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 8 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 9 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 10 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 11 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 12 | `inspect_feature` | L0, F2994 | "the pronoun "his" and the pronoun "he."" |

**Findings:** The circuit for L19:F8814 is driven primarily by the input token "His" at position 1. The token feeds directly into the layer‑19 feature with a positive effect (9.31). Upstream, the same token strongly excites a cascade of male‑pronoun detectors: layer‑18 feature 7400, layer‑7 feature 14946, and an early layer‑4 feature 4315, each with increasing direct effects. These lower‑layer features (especia…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `get_upstream_features` | L6:F12990@1, k=10 | Emb:"His"@1 (de=4.91) +9 more |
| 5 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 6 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 7 | `get_upstream_features` | L4:F4315@1, k=10 | Emb:"His"@1 (de=23.50) +9 more |
| 8 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 9 | `inspect_feature` | L2, F9301 | " all mentions of men and women in the context of relationships, dating" |
| 10 | `get_upstream_features` | L4:F15567@1, k=10 | Emb:"His"@1 (de=19.25) +9 more |

**Findings:** L7:F14893 is a pronoun/possessive‑pronoun detector strongly excited by the token embedding 'His'. Upstream excitatory inputs come from a male‑pronoun detector (L6:F12990) and a generic pronoun‑mention detector (L4:F4315), both of which also receive direct excitation from the same token embedding. All involved layers are within the lower third (≤8) and we have identified a positive embedding connec…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@10, k=10 | Emb:" He"@10 (de=22.38) +9 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `get_upstream_features` | L0:F1069@10, k=10 | Emb:" He"@10 (de=35.75) +9 more |
| 5 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 6 | `inspect_feature` | L18, F14743 | "He" |
| 7 | `get_upstream_features` | L17:F5889@10, k=10 | Emb:" He"@10 (de=21.75) +9 more |
| 8 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 9 | `get_upstream_features` | L6:F2267@10, k=10 | Emb:"<bos>"@0 (de=-7.34) +9 more |
| 10 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 11 | `inspect_feature` | L13, F6622 | " pronouns." |

**Findings:** The target L18:F14743 (position 10) is a masculine pronoun detector ('He'). Its strongest upstream driver is the layer‑0 feature 1069, an early pronoun detector, which itself is directly driven by the 'He' token embedding. Additional upstream contributors include a higher‑layer pronoun cluster (L17:5889) and several gender‑narrative features (L15:3330, L13:6622). Tracing one hop further from the m…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L22:F12117@11` | ✅ reported | 6 | 49 | Trace upstream from L22:F12117 (pos 11, references to actions people can take, p… |

<details>
<summary><b>SA-4</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L22, F12117 | " references to actions that people can take or have taken." |
| 2 | `get_upstream_features` | L22:F12117@11, k=10 | L21:F4895 (de=5.69) +9 more |
| 3 | `inspect_feature` | L21, F4895 | "prepositions and related words" |
| 4 | `inspect_feature` | L20, F10934 | " action verbs with past tense forms" |
| 5 | `get_upstream_features` | L21:F4895@11, k=10 | L19:F11110 (de=11.00) +9 more |
| 6 | `inspect_feature` | L19, F11110 | " text describing people's education history" |
| 7 | `inspect_feature` | L20, F14093 | " academic author lists and acknowledgements." |
| 8 | `get_upstream_features` | L19:F11110@11, k=10 | L18:F7334 (de=16.88) +9 more |
| 9 | `inspect_feature` | L8, F7587 | " words related to education and professional qualifications" |
| 10 | `get_upstream_features` | L8:F7587@11, k=10 | Emb:" received"@11 (de=7.38) +9 more |
| 11 | `inspect_feature` | L4, F11633 | " words related to education and employment history" |
| 12 | `get_upstream_features` | L4:F11633@11, k=10 | Emb:" received"@11 (de=7.88) +9 more |

**Findings:** The upstream trace from the target feature (L22:F12117) reaches a lower‑third layer (L8) and includes direct embedding contributions (token "received"). The pathway shows a gender‑driven signal that originates from low‑level education/qualification detectors and propagates up to the pronoun‑promotion feature, confirming that the token "received" is fed by both generic education cues and a gender‑b…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L18:7400, L7:14946, L0:1069, L22:12117, L4:4315, L6:12990 |
| 2 | `get_upstream_features` | L0:F2994@1, k=5 → Emb:"His"@1 (de=19.75) +4 more |

### Build

`build_circuit` → 11 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 31,670 | 3,915 | 92,294 | 0 | $0.0197 | — | — |
| SA-1 | openai/gpt-oss-120b | 97,494 | 7,333 | 53,600 | 0 | $0.0198 | ✅ 5F/7E | Trace upstream from L19:F8814 (various pronouns/names referr… |
| SA-3 | openai/gpt-oss-120b | 126,149 | 8,436 | 13,504 | 0 | $0.0242 | ✅ 6F/9E | Trace upstream from L18:F14743 (pos 10, negative effect). Po… |
| SA-2 | openai/gpt-oss-120b | 132,288 | 8,924 | 5,184 | 0 | $0.0253 | ✅ 3F/5E | Trace upstream from L7:F14893 (pronouns/possessive pronouns)… |
| SA-4 | openai/gpt-oss-120b | 206,842 | 17,536 | 13,312 | 0 | $0.0417 | ✅ 6F/49E | Trace upstream from L22:F12117 (pos 11, references to action… |
| **Total** | | **594,443** | **46,144** | **177,894** | **0** | **$0.1308** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 15s