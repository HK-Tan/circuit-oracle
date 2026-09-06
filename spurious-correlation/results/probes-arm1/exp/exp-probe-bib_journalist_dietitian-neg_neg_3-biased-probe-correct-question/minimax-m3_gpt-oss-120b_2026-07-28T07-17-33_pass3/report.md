# Circuit Oracle Report
**Date:** 2026-07-28 07:17:33 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession-classification score is driven by a tangle of low-level token-level detectors, but the user-suspected gender-marker pathway is genuinely present: male-pronoun features for "He" (pos 1), "him" (pos 46), and "his" (pos 52) carry substantial positive direct effects on the probe (e.g. L7:F14893 at pos 1 contributes +0.163, pos 46 +0.196, pos 52 directly through L0:F2994 +0.179) alongside genuine profession-indicating features for "researches" (L0:F4564, L0:F10036), "stories" (L0:F61, F5333, F14812), "represents" (L1:F7449), and "journalistic" (L4:F13253, promoted tokens: "Journalism", "journalists"). The pronoun contribution is roughly comparable in magnitude to the profession-keyword contribution.

**Confidence:** 6

**Reasoning:** Tracing the circuit from the probe output backwards reveals three convergent inputs. (1) **Gender-marker pathway** — confirmed and substantive. `Emb: He` (pos 1) feeds the male-pronoun aggregator L6:F12990 ("male pronouns and titles", suppresses "herself", promotes "himself") → L4:F14796 ("he/him") → L7:F14893 (pos 1, +0.163). `Emb: him` (pos 46) → L0:F16297 ("him", frac=0.033) → L2:F6929 → L3:F2434 → L4:F11391 → L7:F14893 (pos 46, +0.196). `Emb: his` (pos 52) → L0:F2994 ("his/he", frac=0.073) → L4:F4315 (pos 52) → L7:F14893 (pos 52, +0.179). All three male-pronoun tokens converge on the same L7 pronoun aggregator, which directly drives the probe. (2) **Genuine profession pathway** — `Emb: researches` → L0:F4564 ("research", suppressed "research") + L0:F10036 ("scientists", frac=0.013) (+0.212, +0.167). `Emb: stories` → L0:F61, F5333, F14812 ("stories/stories being told") (+0.202, +0.205, +0.217). `Emb: represents` → L1:F7449 ("representation") + L1:F5267 (+0.217, +0.179). `Emb: journalistic` → L4:F13253 ("journalism and the media", promotes "Journalism", "journalists", frac=0.006) (+0.154). These features directly encode the journalist profession and provide independent positive signal. (3) **Generic function-word noise** — L0:F3255 ("and"), F10187 ("time"), F6051 (periods), F7696 ("on"), F9026 (technical notation, frac=0.41 — fires generically), F14520 (verbs of reduction/change) carry mostly negative direct effects (-0.203, -0.202, -0.256, -0.243), suggesting the probe direction subtracts generic low-content signal.

The user's concern is **partially validated**: the circuit does use male-pronoun markers as a strong secondary signal — the L7:F14893 pathway alone contributes three positive direct effects of ~+0.18 each from different positions, comparable in magnitude to any single profession keyword. However, the profession-pathway features (`researches`, `stories`, `represents`, `journalistic`) are also clearly present and directly drive the probe with positive direct effects. The probe appears to use a mix of legitimate profession indicators AND a strong male-pronoun short-cut, meaning it would likely misfire on passages describing female journalists that contain the same profession keywords but lack the male pronouns.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Mid-layer pronoun aggregators (L4, L7) — male pronoun detectors that fire on he/him/his |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 46 | Mid-layer pronoun aggregators (L4, L7) — male pronoun detectors that fire on he/him/his |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 52 | Mid-layer pronoun aggregators (L4, L7) — male pronoun detectors that fire on he/him/his |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L4:F11391](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11391) | 46 | Mid-layer pronoun aggregators (L4, L7) — male pronoun detectors that fire on he/him/his |  pronouns referring to people and words related to negative experiences | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11391) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 52 | Mid-layer pronoun aggregators (L4, L7) — male pronoun detectors that fire on he/him/his |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 1 | Mid-layer pronoun aggregators (L4, L7) — male pronoun detectors that fire on he/him/his | the pronoun "he" or "him" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 1 | Mid-layer pronoun aggregators (L4, L7) — male pronoun detectors that fire on he/him/his | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 52 | Low-layer pronoun detectors (L0, L2, L3, L4, L6) — fire on he/him/his and male-associated tokens | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 46 | Low-layer pronoun detectors (L0, L2, L3, L4, L6) — fire on he/him/his and male-associated tokens | the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L2:F6929](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6929) | 46 | Low-layer pronoun detectors (L0, L2, L3, L4, L6) — fire on he/him/his and male-associated tokens |  the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6929) |
| [L3:F2434](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2434) | 46 | Low-layer pronoun detectors (L0, L2, L3, L4, L6) — fire on he/him/his and male-associated tokens |  the word "him", and possibly other pronouns referring to males | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2434) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Low-layer pronoun detectors (L0, L2, L3, L4, L6) — fire on he/him/his and male-associated tokens |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | Low-layer pronoun detectors (L0, L2, L3, L4, L6) — fire on he/him/his and male-associated tokens |  all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Low-layer pronoun detectors (L0, L2, L3, L4, L6) — fire on he/him/his and male-associated tokens | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 4 | Function-word / generic-token detectors (L0) — fire on and, time, on, period, representation; low-content features that pull the probe both ways |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F10187](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10187) | 8 | Function-word / generic-token detectors (L0) — fire on and, time, on, period, representation; low-content features that pull the probe both ways | the word "time" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10187) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | Function-word / generic-token detectors (L0) — fire on and, time, on, period, representation; low-content features that pull the probe both ways | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F7696](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7696) | 18 | Function-word / generic-token detectors (L0) — fire on and, time, on, period, representation; low-content features that pull the probe both ways | the word "on" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7696) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 9 | Function-word / generic-token detectors (L0) — fire on and, time, on, period, representation; low-content features that pull the probe both ways | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F14520](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14520) | 9 | Function-word / generic-token detectors (L0) — fire on and, time, on, period, representation; low-content features that pull the probe both ways | verbs that describe actions affecting a noun, especially in the context of protection, reduction, or change | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14520) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Profession-related word detectors (L0, L1, L4) — research, stories, journalists/media | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F10036](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10036) | 2 | Profession-related word detectors (L0, L1, L4) — research, stories, journalists/media |  words about scientific research and scientists | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10036) |
| [L0:F61](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) | 3 | Profession-related word detectors (L0, L1, L4) — research, stories, journalists/media | the word "stories" sometimes along with apostrophes and common names. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | Profession-related word detectors (L0, L1, L4) — research, stories, journalists/media | mentions of stories that are being told | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | Profession-related word detectors (L0, L1, L4) — research, stories, journalists/media |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F7449](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) | 9 | Profession-related word detectors (L0, L1, L4) — research, stories, journalists/media | instances of the word "representation" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) |
| [L0:F5267](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5267) | 9 | Profession-related word detectors (L0, L1, L4) — research, stories, journalists/media | mentions of representation or things standing for other things. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5267) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | Profession-related word detectors (L0, L1, L4) — research, stories, journalists/media |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L0:F9121](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9121) | 3 | Profession-related word detectors (L0, L1, L4) — research, stories, journalists/media |  the word "nice" and words with positive sentiment, sometimes related to the weather or seasons | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9121) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:6051 de=-0.256 |
| 3 | `inspect_feature` ×8 | L1:7449, L1:14812, L0:4564, L0:5333, L0:61, L7:14893, L0:2994, L0:10036 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@46` | ✅ reported | 3 | 4 | Trace this pronoun feature upstream. What does L7:F14893 (pronouns/possessives) … |
| SA-2 | `L1:F7449@9` | ❌ error | — | — | Trace this "representation" word feature upstream. Where does the signal come fr… |
| SA-3 | `L0:F2994@52` | ❌ error | — | — | Trace this "his/he" pronoun feature upstream to identify the exact token positio… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@46, k=10 | Emb:" him"@46 (de=12.56) +9 more |
| 3 | `inspect_feature` | L0, F16297 | " the pronoun "him"" |
| 4 | `get_upstream_features` | L0:F16297@46, k=10 | Emb:" him"@46 (de=43.25) +9 more |
| 5 | `inspect_feature` | L4, F11391 | " pronouns referring to people and words related to negative experience" |
| 6 | `get_upstream_features` | L4:F11391@46, k=10 | Emb:" him"@46 (de=21.12) +9 more |

**Findings:** The pronoun feature L7:F14893 at position 46 is driven primarily by the raw token embedding for "him" (direct_effect 12.56) and by a low‑level detector L0:F16297 that also responds to the token "him" (direct_effect 3.02). Tracing one hop further shows that L0:F16297 receives its strongest signal directly from the same token embedding "him" (direct_effect 43.25). Thus the pronoun circuit originates…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F7449@9, k=10 → Emb:" represents"@9 (de=20.50) +9 more |
| 2 | `get_upstream_features` | L0:F2994@52, k=8 → Emb:" his"@52 (de=45.00) +7 more |
| 3 | `get_upstream_features` | L0:F16297@46, k=8 → Emb:" him"@46 (de=43.25) +7 more |
| 4 | `inspect_feature` ×3 | L0:5267, L0:14520, L4:11391 |
| 5 | `get_upstream_features` | L7:F14893@1, k=8 → Emb:"He"@1 (de=14.75) +7 more |
| 6 | `inspect_feature` ×3 | L6:12990, L4:9757, L4:14796 |
| 7 | `get_upstream_features` | L4:F11391@46, k=6 → Emb:" him"@46 (de=21.12) +5 more |
| 8 | `get_upstream_features` | L7:F14893@1, k=6 → Emb:"He"@1 (de=14.75) +5 more |
| 9 | `inspect_feature` ×5 | L2:6929, L3:2434, L4:15567, L2:9301, L3:373 |
| 10 | `get_upstream_features` | L1:F14812@3, k=8 → Emb:" stories"@3 (de=18.62) +7 more |
| 11 | `get_upstream_features` | L0:F4564@2, k=8 → Emb:" researches"@2 (de=13.25) +7 more |
| 12 | `get_upstream_features` | L0:F5333@3, k=8 → Emb:" stories"@3 (de=16.38) +7 more |
| 13 | `get_upstream_features` | L0:F61@3, k=8 → Emb:" stories"@3 (de=17.38) +7 more |
| 14 | `get_upstream_features` | L0:F9026@9, k=6 → Emb:" stories"@3 (de=-2.06) +5 more |
| 15 | `get_upstream_features` | L0:F3255@4, k=6 → Emb:" and"@4 (de=36.00) +5 more |
| 16 | `get_upstream_features` | L0:F10187@8, k=6 → Emb:" time"@8 (de=34.75) +5 more |
| 17 | `get_upstream_features` | L0:F6051@15, k=6 → Emb:"."@15 (de=47.00) +5 more |
| 18 | `get_upstream_features` | L0:F7696@18, k=6 → Emb:" on"@18 (de=39.00) +5 more |
| 19 | `get_upstream_features` | L0:F9121@3, k=6 → Emb:" stories"@3 (de=11.38) +5 more |
| 20 | `get_upstream_features` | L4:F13253@13, k=6 → Emb:" journalistic"@13 (de=25.62) +5 more |
| 21 | `inspect_feature` ×7 | L0:3255, L0:10187, L0:6051, L0:7696, L0:9121, L4:13253, L0:9026 |
| 22 | `get_source_influence` | {'depth': 2, 'source_positions': [46, 52, 1]} → {'depth': 2, 'source_positions': [1, 46, 52], 'S_pct_of_total': 4.912, 'R_pct_of |
| 23 | `get_source_influence` | {'depth': 2, 'source_positions': [2, 3, 9, 13, 14, 15]} → {'depth': 2, 'source_positions': [2, 3, 9, 13, 14, 15], 'S_pct_of_total': 4.827, |
| 24 | `get_upstream_features` | L7:F14893@46, k=4 → Emb:" him"@46 (de=12.56) +3 more |
| 25 | `get_upstream_features` | L7:F14893@52, k=3 → Emb:" his"@52 (de=23.62) +2 more |
| 26 | `get_upstream_features` | L7:F14893@9, k=3 → ❌ Feature (layer=7, feature_idx=14893) not found at pos=9. Thi |
| 27 | `inspect_feature` | L4, F4315 → " mentions of "his" and other associated pronouns like he, him, or hers" |
| 28 | `get_upstream_features` | L7:F14893@23, k=3 → Emb:" he"@23 (de=16.12) +2 more |
| 29 | `get_upstream_features` | L0:F16297@46, k=3 → Emb:" him"@46 (de=43.25) +2 more |

### Build

`build_circuit` → 17 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 63,535 | 6,270 | 572,992 | 0 | $0.0610 | — | — |
| SA-1 | openai/gpt-oss-120b | 53,357 | 3,200 | 0 | 0 | $0.0099 | ✅ 3F/4E | Trace this pronoun feature upstream. What does L7:F14893 (pr… |
| **Total** | | **116,892** | **9,470** | **572,992** | **0** | **$0.0709** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 14s