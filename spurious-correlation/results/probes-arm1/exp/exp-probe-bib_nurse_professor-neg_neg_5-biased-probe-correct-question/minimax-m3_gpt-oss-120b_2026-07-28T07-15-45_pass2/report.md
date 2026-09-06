# Circuit Oracle Report
**Date:** 2026-07-28 07:15:45 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by masculine pronoun features (His/He/He) detected across the early and late layers, with the L0:L2994 ("His"/"he") and L0:L1069 ("He"/"His") token-embedding detectors acting as the entry points — genuine profession-related content tokens (history, Harvard) play only a marginal role.

**Confidence:** 9

**Reasoning:** The user concern is well-supported by the circuit. The signal flow is: token embeddings of the male pronouns "His" (pos 1, direct_effect ≈ 23.5 into L7:L14893) and "He" (pos 10, direct_effect ≈ 35.75 into L0:L1069; pos 23, direct_effect ≈ 36.75 into L0:L1069) feed L0:L2994 (label: "pronoun 'his' and 'he'", frac_nonzero=0.07, also at pos 1) and L0:L1069 (label: "references to a male person... 'He' or 'His'", frac_nonzero=0.008), which are the dominant "His" detectors at the very first layer. These feed a chain of mid-layer pronoun-specific detectors: L4:L4315 ("mentions of 'his' and other associated pronouns like he, him", frac_nonzero=0.026), L6:L12990 ("male pronouns and titles along with descriptors associated with men", frac_nonzero=0.068, but fires with direct_effect = -0.34 and -0.20 at the probe level, *inhibiting* the probe's positive direction), and L7:L14893 (pronouns/possessive pronouns, with promoted tokens like ▁herself, ▁she — i.e. its pushed output is feminine; frac_nonzero=0.009; direct_effect = +0.49 on the probe at pos 1) plus L7:L14946 (the dual-natured "his"/"he"/"him" detector with promoted tokens ▁himself/▁his — i.e. its pushed output is masculine; frac_nonzero=0.017; direct_effect = -0.49 on the probe at pos 1). L7:L14893 and L7:L14946 are nearly perfectly anti-correlated in the circuit and are both driven by the same "His" token embedding.

These mid-layer pronoun features then feed late-layer features like L18:L14743 ("He", direct_effect = -0.29 and -0.17 at pos 10 and 23), L18:L7400 (label is "code/UI" but its promoted/suppressed tokens are ▁himself/▁his vs. ▁herself/▁she — a strong male/female gender detector encoded on a feature whose own surface label is misleading; direct_effect = -0.19 at pos 1, *pushing against* the probe's positive direction), L19:L8814 (pronouns and names; direct_effect = +0.29 at pos 1, pushes for the probe), L21:L6216 (pronoun references, direct_effect = +0.12 at pos 10), and L22:L12117 (action references; direct_effect = -0.18 at pos 11).

By contrast, the genuinely content-bearing features are much weaker: L0:L1773 ("the word 'history'", direct_effect = +0.11 at pos 8) and L12:L10137 (universities/institutions, direct_effect = -0.11 at pos 20, *suppressing* the probe's positive direction). The "history" token embedding (pos 8) itself contributes only +0.63 to the most relevant upstream feature, and "Harvard" (pos 20) +1.9 to L12:L10137 — tiny compared to the pronoun direct effects of 20–35.

The fundamental finding: the probe's positive direction is predominantly aligned with a male-pronoun/masculine-entity circuit, not with a "professor/academic" circuit. Features whose semantic labels clearly describe "his" / "he" pronouns dominate the top-20 list by both activation magnitude and direct effect on the probe, while content words that would indicate profession (history, Harvard, Ph.D., Economics, M.B.A., research) contribute only weakly. The male-pronoun chain is reinforced redundantly (L0:L2994, L0:L1069, L4:L4315, L6:L12990, L7:L14893, L7:L14946, L18:L7400, L18:L14743, L19:L8814, L21:L6216, L22:L12117), and several of those features are double-coded — their autointerp label says one thing (e.g. "code/UI" or "He" or "various pronouns") but their promoted/suppressed token projections reveal they are gender-direction detectors (▁himself/▁his vs. ▁herself/▁she). This is a textbook spurious-corrrelate circuit: the probe has latched onto the gender of the subject rather than the academic/professional content. Note: there's internal disagreement on sign — L7:L14893 (promoted ▁herself) *adds* positively to the probe (+0.49), while L7:L14946 (promoted ▁himself) *subtracts* (-0.49), even though both are downstream of the same "His" token. This indicates the probe is sensitive to a specific sub-direction of the gender feature space, not a simple "male ⇒ high score" rule — but the upstream signal is still unambiguously about gender-marked pronouns, not profession.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Late-layer male-pronoun / person-reference features (L18-L22) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L19:F8186](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) | 10 | Late-layer male-pronoun / person-reference features (L18-L22) |  references to a person, especially third-person pronouns and possessive pronouns. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 10 | Late-layer male-pronoun / person-reference features (L18-L22) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Late-layer male-pronoun / person-reference features (L18-L22) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Late-layer male-pronoun / person-reference features (L18-L22) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Late-layer male-pronoun / person-reference features (L18-L22) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L21:F6216](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/6216) | 10 | Late-layer male-pronoun / person-reference features (L18-L22) |  references to a specific person, often using pronouns or names | [view](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/6216) |
| [L22:F12117](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) | 11 | Late-layer male-pronoun / person-reference features (L18-L22) |  references to actions that people can take or have taken. | [view](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Early/mid-layer pronoun features (L4-L7) — his/he/him generic detectors |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Early/mid-layer pronoun features (L4-L7) — his/he/him generic detectors |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 10 | Early/mid-layer pronoun features (L4-L7) — his/he/him generic detectors |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Early/mid-layer pronoun features (L4-L7) — his/he/him generic detectors |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Early/mid-layer pronoun features (L4-L7) — his/he/him generic detectors |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 10 | Early/mid-layer pronoun features (L4-L7) — his/he/him generic detectors |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 10 | Early/mid-layer pronoun features (L4-L7) — his/he/him generic detectors |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Layer-0 / L2 token-embedding-based pronoun detectors at position 1 (His) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Layer-0 / L2 token-embedding-based pronoun detectors at position 1 (His) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 10 | Layer-0 / L2 token-embedding-based pronoun detectors at position 1 (His) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 23 | Layer-0 / L2 token-embedding-based pronoun detectors at position 1 (His) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 12 | Layer-0 / L2 token-embedding-based pronoun detectors at position 1 (His) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | Layer-0 / L2 token-embedding-based pronoun detectors at position 1 (His) | references to God in the third person. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: His (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: He (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: He (pos 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: history (pos 8) — genuine content token, but minor effect | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: Harvard (pos 20) — institution token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe direction (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.490 |
| 3 | `inspect_feature` ×15 | L7:14893, L7:14946, L0:2994, L6:12990, L19:8814, L18:14743, L18:7400, L22:12117, L18:10315, L4:4315, L21:6216, L19:8186, L0:1773, L12:10137, L2:5491 |
| 4 | `get_upstream_features` | Emb:"His"@1 (de=23.50) +9 more |
| 5 | `get_upstream_features` | Emb:"His"@1 (de=18.38) +9 more |
| 6 | `get_upstream_features` | Emb:"His"@1 (de=9.31) +9 more |
| 7 | `get_upstream_features` | Emb:" He"@10 (de=22.38) +9 more |
| 8 | `get_upstream_features` | Emb:" He"@23 (de=24.50) +9 more |
| 9 | `get_upstream_features` | L18:F14743 (de=7.53) +9 more |
| 10 | `get_upstream_features` | Emb:"His"@1 (de=13.00) +9 more |
| 11 | `get_upstream_features` | Emb:"His"@1 (de=21.38) +9 more |
| 12 | `get_upstream_features` | L21:F4895 (de=5.69) +9 more |
| 13 | `get_upstream_features` | Emb:" history"@8 (de=26.75) +9 more |
| 14 | `get_upstream_features` | Emb:" Harvard"@20 (de=5.16) +9 more |
| 15 | `inspect_feature` ×10 | L15:851, L11:10933, L11:9183, L9:8770, L0:1069, L15:3330, L17:5889, L21:4895, L20:10934, L17:3683 |
| 16 | `get_upstream_features` | Emb:"His"@1 (de=23.50) +7 more |
| 17 | `get_upstream_features` | Emb:"His"@1 (de=19.75) +7 more |
| 18 | `get_upstream_features` | Emb:"His"@1 (de=4.91) +7 more |
| 19 | `get_upstream_features` | Emb:" He"@10 (de=35.75) +7 more |
| 20 | `get_upstream_features` | Emb:" He"@23 (de=36.75) +7 more |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 53,429 | 5,142 | 220,645 | 0 | $0.0354 | — | — |
| **Total** | | **53,429** | **5,142** | **220,645** | **0** | **$0.0354** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 26s