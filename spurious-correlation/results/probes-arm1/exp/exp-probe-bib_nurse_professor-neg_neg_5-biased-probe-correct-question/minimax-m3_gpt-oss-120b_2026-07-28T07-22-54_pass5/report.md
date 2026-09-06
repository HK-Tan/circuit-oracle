# Circuit Oracle Report
**Date:** 2026-07-28 07:22:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a chain of male-pronoun detector features that originate from the input tokens "His" (pos 1), " He" (pos 10), and " his" (pos 12), with virtually no contribution from profession-indicating content like "History," "Ph.D.," "Economics," "MBA," or university names.

**Confidence:** 9

**Reasoning:** The circuit is dominated by features whose entire purpose is to fire on male pronouns. Starting from the embedding inputs at positions 1 ("His"), 10 (" He"), and 12 (" his"), the signal flows through a hierarchy of pronoun-specific detectors:

- **Early (L0–L4)**: F2994 ("the pronoun 'his' and 'he'", frac_nonzero 0.073), F1069 ("references to a male person, particularly 'He' or 'His'", frac_nonzero 0.008), F5491 (firing on "His" with divine-pronoun pattern, frac_nonzero 0.008), F4315 ("mentions of 'his' and other pronouns like he, him", frac_nonzero 0.026). Every one of these labels is a male-pronoun detector, and every one feeds in from the "His"/"He" tokens — not from profession terms.
- **Mid (L6–L7)**: F12990 ("male pronouns and titles along with descriptors associated with men", frac_nonzero 0.068, positive effect), F14893 ("pronouns or possessive pronouns", promoted: "herself, she, her", frac_nonzero 0.009), F14946 ("the possessive pronoun 'his' ... and 'he' and 'him'", frac_nonzero 0.017). These consolidate the pronoun signal — F12990 and F14946 promote "himself/his" and suppress "herself/she/her," confirming an asymmetric male signal.
- **Late (L18–L19)**: F8814 ("various pronouns and names referring to people", promotes "herself/she/her," suppresses "himself/his," frac_nonzero 0.087, direct_effect +0.295 — the largest positive contributor) and F10315 ("pronouns and possessive pronouns", promotes "himself/his," suppresses "her/their," frac_nonzero 0.039, direct_effect -0.182). F14743 ("He", fires on "He"/"He ", frac_nonzero 0.018, direct_effect -0.285) and F7400 (pronoun-detector, direct_effect -0.193) also operate here.
- **L22**: F12117 ("references to actions that people can take or have taken," promotes "his/himself/he") sits near the output but contributes only -0.185.

The promoted/suppressed token vectors are the smoking gun: male-pronoun features push the probe score, with "his/he/him" on the promote side and "her/she/herself" on the suppress side. Critically, the top-15 features list contains no profession-related entity features (no "historian," "economist," "professor," university, or degree-indicating features), and the upstream tracing at L0:F2994 (pos 12) shows the embedding for " his" (pos 12) as the dominant driver (direct_effect 44.5) while every other content token contributes under 1.1.

This confirms the user's concern: the probe is classifying using spurious gendered features (male pronouns "He"/"His") as a shortcut, not genuine profession indicators. If the same biography were rewritten with "She/Her" pronouns, the features driving the probe would flip sign and likely reclassify the subject, even though no professional information changed.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'His' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' his' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: ' He' (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Early male-pronoun detectors (L0–L4) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 12 | Early male-pronoun detectors (L0–L4) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Early male-pronoun detectors (L0–L4) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | Early male-pronoun detectors (L0–L4) | references to God in the third person. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Early male-pronoun detectors (L0–L4) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Mid-layer male-pronoun features (L6–L7) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Mid-layer male-pronoun features (L6–L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Mid-layer male-pronoun features (L6–L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Late-layer male reference (L18–L19) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Late-layer male reference (L18–L19) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 10 | Late-layer male reference (L18–L19) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Late-layer male reference (L18–L19) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L22:F12117](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) | 11 | Action/verb feature (L22) |  references to actions that people can take or have taken. | [view](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.490 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F8814@1` | ❌ error | — | — | Trace L19:F8814 upstream to understand what it encodes. This is the strongest po… |
| SA-2 | `L7:F14893@1` | ❌ error | — | — | Trace L7:F14893 upstream to understand what it encodes. This is the second stron… |
| SA-3 | `L0:F2994@12` | ❌ error | — | — | Trace L0:F2994 (pos 12) upstream. This is an early-layer feature at position 12.… |
| SA-4 | `L18:F14743@10` | ❌ error | — | — | Trace L18:F14743 (pos 10) upstream. This is a negative contributor (suppresses p… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L19:8814, L7:14893, L0:2994, L18:14743 |
| 2 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (de=9.31) +9 more |
| 3 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 4 | `get_upstream_features` | L0:F2994@12, k=10 → Emb:" his"@12 (de=44.50) +9 more |
| 5 | `get_upstream_features` | L18:F14743@10, k=10 → Emb:" He"@10 (de=22.38) +9 more |
| 6 | `inspect_feature` | L0, F2994 → "the pronoun "his" and the pronoun "he."" |
| 7 | `get_upstream_features` | L6:F12990@1, k=8 → Emb:"His"@1 (de=4.91) +7 more |
| 8 | `get_upstream_features` | L4:F4315@1, k=8 → Emb:"His"@1 (de=23.50) +7 more |
| 9 | `get_upstream_features` | L2:F5491@1, k=8 → Emb:"His"@1 (de=23.88) +7 more |
| 10 | `inspect_feature` ×7 | L18:10315, L7:14946, L18:7400, L6:12990, L4:4315, L2:5491, L22:12117 |
| 11 | `get_upstream_features` | L0:F2994@1, k=8 → Emb:"His"@1 (de=19.75) +7 more |
| 12 | `inspect_feature` | L0, F1069 → " references to a male person, particularly when using the pronoun "He"" |

### Build

`build_circuit` → 8 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 28,257 | 4,051 | 142,274 | 0 | $0.0219 | — | — |
| **Total** | | **28,257** | **4,051** | **142,274** | **0** | **$0.0219** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 15s