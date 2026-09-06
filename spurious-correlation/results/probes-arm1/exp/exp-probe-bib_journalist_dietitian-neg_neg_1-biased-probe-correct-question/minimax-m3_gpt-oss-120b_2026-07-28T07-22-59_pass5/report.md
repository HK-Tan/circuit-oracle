# Circuit Oracle Report
**Date:** 2026-07-28 07:22:59 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "reporter/journalist" profession is driven overwhelmingly by gender-pronoun markers ("His", "him", "he", "his") rather than by the actual profession-related word "report" at position 21, which in fact contributes *negatively* to the score. The circuit is largely a pronoun-detector circuit, with journalism features present but being suppressed.

**Confidence:** 7

**Reasoning:**

The strongest single contributors to the probe's score are gender/possessive pronoun features:
- **L7:F14893 (pos 1, direct_effect = +0.47)** — labeled "pronouns or possessive pronouns," promotes "herself/she." This is a generic pronoun feature whose top activations include `▁his`. Its main upstream driver is the **Emb: "His" (pos 1)** with direct_effect = 23.5.
- **L7:F14946 (pos 1, direct_effect = -0.47)** — labeled "the possessive pronoun 'his' and pronouns like 'he' and 'him'," promotes "himself/his." This is the mirror pronoun feature, also driven by **Emb: "His" (pos 1)** (direct_effect = 18.375) and **Emb: "<bos>" (pos 0)** (direct_effect = 3.84).
- **L19:F8814 (pos 1, +0.23)** — labeled "various pronouns and names referring to people."
- **L6:F12990 (pos 1, -0.30)** — labeled "male pronouns and titles along with descriptors associated with men." Top activation: `▁man`, `▁his`.

These pronoun features are sourced overwhelmingly from the **Emb: "His" (pos 1)** token (the very first content word of the prompt). The L0 "His" detector (F2994) and L0 "him" detector (F16297, at pos 9) propagate through multiple layers and contribute through several pronoun supernodes.

The profession-related signal is much weaker and counter-productive:
- **L14:F4420 (pos 21, direct_effect = -0.16)** — labeled "words and phrases related to journalism and newspapers," promotes "journalists/journalistic." Top activation: `▁reporter`. This fires on the **Emb: "report" (pos 21)** token — the actual profession word.
- **L8:F8855 (pos 21)** — "mentions of news reporters and news reporting," promotes "reporter." Sourced directly from **Emb: "report" (pos 21)** (direct_effect = 12.06).
- **L19:F2486 (pos 21, -0.09)** — "journalistic sources and news outlets," also negative.

Notably, all the journalism features that *do* fire on "report" push the probe *downward* (negative direct_effect). The only positive profession-related contribution is indirect (via L0 features F2011 "dream"/"desire", F7927 "past-participles/taken") and is small.

The user's concern is **substantiated by the circuit**. The model classifies "reporter" essentially by reading the gender pronoun "His" at the start of the sentence, not by recognizing the profession word "report." The strongest "his/him/he" pronoun features are balanced roughly symmetrically (L7:F14893 +0.47 vs L7:F14946 -0.47), suggesting the probe is sensitive to the presence of male-gendered subject pronouns. Meanwhile, the genuine profession indicator (the word "report") is recognized by the model but contributes *negatively* to the probe score — meaning the probe is in fact using a *spurious correlation* (male subject pronoun) rather than the profession marker. If the same sentence began with "Her" or "Their," the pronoun-driven signal would either vanish or flip sign, while the profession signal at "report" would be unchanged.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | "him"/"he" pronoun detectors at pos 9 (negative contribution) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | General pronoun features at pos 9 (positive contribution) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | General pronoun features at pos 9 (positive contribution) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | General pronoun features at pos 9 (positive contribution) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | His/possessive pronoun detector (negative) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | His/possessive pronoun detector (negative) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L0:F2208](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2208) | 1 | His/possessive pronoun detector (negative) |  the pronoun "Him" and the possessive pronoun "His" when used in a religious context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2208) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Generic pronoun detector (positive) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Generic pronoun detector (positive) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | His pronoun detectors at pos 1 (mixed signs) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 9 | His pronoun detectors at pos 1 (mixed signs) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 9 | His pronoun detectors at pos 1 (mixed signs) |  the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L16:F14120](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/14120) | 9 | His pronoun detectors at pos 1 (mixed signs) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/14120) |
| [L14:F10344](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10344) | 9 | His pronoun detectors at pos 1 (mixed signs) |  pronouns related to feelings or actions | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10344) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Journalism/reporting features at pos 21 (negative contribution) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Journalism/reporting features at pos 21 (negative contribution) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | News/report detection at mid layers (pos 21) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | News/report detection at mid layers (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | News/report detection at mid layers (pos 21) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L4:F11898](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) | 6 | World/location context (positive contribution) |  mentions of "World" followed by a sport or war-related word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) |
| [L0:F11767](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11767) | 6 | World/location context (positive contribution) | the word "world" with a lower activation for "net" and "market" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11767) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | Action/verb context features (positive) |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F7927](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) | 8 | Action/verb context features (positive) |  past-participle verbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) |
| [L0:F13381](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13381) | 2 | Action/verb context features (positive) |  occurrences of the words 'android', 'ios', 'mouth', or 'face' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13381) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.471 |
| 3 | `inspect_feature` ×10 | L7:14893, L7:14946, L0:2994, L19:8814, L6:12990, L18:14743, L4:4315, L18:10315, L14:4420, L18:7400 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ❌ error | — | — | Trace the L14:4420 (journalism/newspaper feature) at pos 21. It has NEGATIVE dir… |
| SA-2 | `L7:F14893@1` | ❌ error | — | — | Trace L7:14893 (pronouns/possessive pronouns feature, positive direct_effect +0.… |
| SA-3 | `L7:F14946@1` | ❌ error | — | — | Trace L7:14946 ("his" pronoun feature, NEGATIVE direct_effect -0.47) at pos 1. T… |
| SA-4 | `L19:F8814@1` | ❌ error | — | — | Trace L19:8814 (pronouns and names referring to people, positive +0.23) at pos 1… |
| SA-5 | `L14:F4420@21` | ❌ error | — | — | Trace the L14:4420 (journalism/newspaper feature) at pos 21. It has NEGATIVE dir… |
| SA-6 | `L7:F14893@1` | ❌ error | — | — | Trace L7:14893 (pronouns feature, positive +0.47) at pos 1 - strongest positive … |
| SA-7 | `L7:F14946@1` | ❌ error | — | — | Trace L7:14946 ("his" pronoun feature, negative -0.47) at pos 1 - strongest nega… |
| SA-8 | `L19:F8814@1` | ❌ error | — | — | Trace L19:8814 (pronouns/names, positive +0.23) at pos 1. Late-layer feature. Tr… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 2 | `get_upstream_features` | L7:F14946@1, k=10 → Emb:"His"@1 (de=18.38) +9 more |
| 3 | `get_upstream_features` | L0:F2994@1, k=10 → Emb:"His"@1 (de=19.75) +9 more |
| 4 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 5 | `get_upstream_features` | L8:F8855@21, k=10 → Emb:" report"@21 (de=12.06) +9 more |
| 6 | `get_upstream_features` | L7:F13646@21, k=10 → Emb:" report"@21 (de=7.22) +9 more |
| 7 | `get_upstream_features` | L6:F12990@1, k=10 → Emb:"His"@1 (de=4.91) +9 more |
| 8 | `get_upstream_features` | L18:F14743@9, k=10 → Emb:" him"@9 (de=18.38) +9 more |
| 9 | `get_upstream_features` | L0:F16297@9, k=10 → Emb:" him"@9 (de=42.25) +9 more |
| 10 | `get_upstream_features` | L8:F8437@21, k=8 → Emb:" report"@21 (de=5.75) +7 more |
| 11 | `get_upstream_features` | L16:F14120@9, k=8 → Emb:" him"@9 (de=10.00) +7 more |
| 12 | `inspect_feature` ×4 | L0:16297, L8:8855, L7:13646, L14:10344 |
| 13 | `get_upstream_features` | L0:F2011@2, k=8 → Emb:" desire"@2 (de=12.94) +7 more |
| 14 | `get_upstream_features` | L0:F7927@8, k=8 → Emb:" has"@7 (de=16.00) +7 more |
| 15 | `get_upstream_features` | L0:F11767@6, k=8 → Emb:" world"@6 (de=16.38) +7 more |
| 16 | `get_upstream_features` | L4:F11898@6, k=8 → Emb:" world"@6 (de=35.25) +7 more |
| 17 | `inspect_feature` ×8 | L0:2011, L0:7927, L0:11767, L4:11898, L0:8444, L0:2208, L19:2486, L0:13381 |

### Build

`build_circuit` → 17 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 55,767 | 6,116 | 308,734 | 0 | $0.0426 | — | — |
| **Total** | | **55,767** | **6,116** | **308,734** | **0** | **$0.0426** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 47s