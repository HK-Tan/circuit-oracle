# Circuit Oracle Report
**Date:** 2026-07-28 07:22:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of this text as "reporter" is driven by a hybrid circuit in which genuine profession-related features (the word "reporter", journalism vocabulary) and a strong, parallel set of male-pronoun features (he/his) both feed the probe — confirming the user's concern that gender markers are part of the driving signal, not just a side effect.

**Confidence:** 7

**Reasoning:**

The single most positive direct-effect feature on the probe is the L0 pronoun detector L0:F2994 (direct_effect = +0.23), which autointerp says fires on "his" / "he" and whose only large upstream signal is the embedding of the token " his" (pos 3, direct_effect = 42.25) and " his" (pos 61, direct_effect = 45.5). A second L0 pronoun feature, L0:F1069 ("references to a male person, particularly 'He' or 'His'"), fires at pos 25 on the token " He" (direct_effect = 37) and is fed upward into L7 pronoun features (F14893, F14946), into L14:5740 ("sentences with multiple pronouns") and L14:14097 ("occurrences of 'he'"), and ultimately into L17:F5889 and L18:F14743, both of which autointerp as "He" / "references to people with pronouns". L18:F14743 has direct_effect = −0.106 at pos 25 and −0.093 at pos 86 ("he"), so by L18 the male-pronoun pathway is large and *negative* on the probe. Crucially the *sign* of the pronoun feature's contribution flips between layers (strongly positive at L0, strongly negative at L18) — the model is using the count/presence of male pronouns, not the semantic content of "reporter", as a calibrated cue.

Running alongside it is a genuine profession pathway. The " reporter" embedding at pos 66 is the dominant upstream driver of L4:F13253 (journalism/media), L7:F13646 and L7:F9092 (broadcast-journalism vocabulary), and L14:F4420 (promoted tokens literally include "reporters", "journalist", "journalism"). L14:F4420 then feeds L19:F2486 ("journalistic sources and news outlets") and L17:F5218 ("text about journalism, media, and related topics"). L19:F2486 has the second-largest negative direct_effect on the probe (−0.120), and L17:F5218 / L18:F14663 (a "report" word-form feature) are also in the top of the ranking — these are the legitimate profession-indicating signals.

The source-influence check is telling: positions {1,3,25,51,61,86} (the pronoun sites) carry S_pct = −8.9% of the total signed influence, while position 66 (the word "reporter") carries only S_pct ≈ +0.6% — i.e. the *signed multi-hop* influence of the pronoun positions is an order of magnitude larger than that of the profession word, even though "reporter" is the explicit semantic anchor. In other words, the male-pronoun chain is doing more *net signed work* on the classification score than the literal profession word.

**Verdict on the user's concern:** the concern is supported but qualified. The circuit is *not* purely spurious — there is a real "reporter / journalism" pathway (L4:13253 → L7:13646/9092 → L14:4420 → L17:5218/L19:2486) that is genuinely profession-related. But the *strongest single feature* in the entire attribution graph is a male-possessive-pronoun detector (L0:F2994), and a parallel male-pronoun chain (L0:F1069 → L7:F14893/F14946 → L13:F6622 → L14:F5740/F14097 → L17:F5889 → L18:F14743) is also active, with sign-flipping contributions at L0 (positive) and L18 (negative). The net signed influence of the pronoun positions substantially exceeds that of the "reporter" position, indicating the probe is partially keying off male-gender markers. The profession signal is real, but it is *entangled with* and *amplified by* a gender-marker pathway — a classic pattern of a probe that has learned a partially spurious shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Pronoun "his"/"he" detector (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 61 | Pronoun "his"/"he" detector (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 25 | Pronoun "his"/"he" detector (L0) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 9 | Other early-layer content tokens (L0) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 24 | Other early-layer content tokens (L0) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F886](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) | 2 | Other early-layer content tokens (L0) |  text related to discounts, offers, or prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 6 | Other early-layer content tokens (L0) |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F7681](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) | 2 | Other early-layer content tokens (L0) | statements that describe something, often including a past tense verb | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 16 | Other early-layer content tokens (L0) | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 86 | Other early-layer content tokens (L0) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | Journalism / media concept (L4) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Male pronoun / possessive features (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Male pronoun / possessive features (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 66 | Male pronoun / possessive features (L7) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 66 | Male pronoun / possessive features (L7) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 25 | Pronouns / subject reference (L13) |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | "Reporter / journalist" feature (L14) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F5740](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) | 25 | "He" + sentence-pronoun context (L14) |  sentences with multiple pronouns in them | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 25 | "He" + sentence-pronoun context (L14) |  occurrences of the word "he" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 25 | Personal-story-of-individual feature (L15) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 86 | Personal-story-of-individual feature (L15) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 25 | Subject pronoun reference / journalism (L17) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 86 | Subject pronoun reference / journalism (L17) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F5218](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) | 66 | Subject pronoun reference / journalism (L17) |  text about journalism, media, and related topics | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 25 | "He" / male-pronoun feature (L18) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 86 | "He" / male-pronoun feature (L18) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14663](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) | 66 | "He" / male-pronoun feature (L18) | variations of the word "report." | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | Journalistic sources / outlets (L19) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.232 |
| 3 | `inspect_feature` ×13 | L0:2994, L14:4420, L7:14893, L19:2486, L0:8974, L0:6051, L4:13253, L7:14946, L18:14743, L0:886, L0:8061, L0:7681, L0:14824 |
| 4 | `get_upstream_features` | Emb:" reporter"@66 (de=18.75) +14 more |
| 5 | `get_upstream_features` | Emb:" He"@25 (de=24.00) +14 more |
| 6 | `get_upstream_features` | Emb:" reporter"@66 (de=28.25) +14 more |
| 7 | `inspect_feature` | "the pronoun "his" and the pronoun "he."" |
| 8 | `get_upstream_features` | Emb:" his"@3 (de=42.25) +9 more |
| 9 | `get_upstream_features` | Emb:" his"@61 (de=45.50) +9 more |
| 10 | `get_upstream_features` | Emb:" reporter"@66 (de=26.62) +9 more |
| 11 | `get_upstream_features` | Emb:"He"@1 (de=14.75) +9 more |
| 12 | `get_upstream_features` | Emb:"He"@1 (de=11.50) +9 more |
| 13 | `get_upstream_features` | Emb:" he"@86 (de=23.88) +9 more |
| 14 | `inspect_feature` ×8 | L8:8855, L7:13646, L0:12768, L17:5889, L15:3330, L0:1069, L7:9092, L13:6622 |
| 15 | `get_source_influence` | {'depth': 3, 'source_positions': [1, 3, 25, 51, 61, 86], 'S_pct_of_total': -8.94 |
| 16 | `get_source_influence` | {'depth': 3, 'source_positions': [66], 'S_pct_of_total': 0.563, 'R_pct_of_total' |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@66` | ❌ error | — | — | Trace upstream from L14:F4420 at pos 66 ("reporter") to find which input tokens … |
| SA-2 | `L0:F2994@3` | ❌ error | — | — | Trace upstream from L0:F2994 at pos 3 (the "his/he" pronoun feature). This featu… |
| SA-3 | `L19:F2486@66` | ❌ error | — | — | Trace upstream from L19:F2486 at pos 66 ("journalistic sources and news outlets"… |
| SA-4 | `L18:F14743@25` | ❌ error | — | — | Trace upstream from L18:F14743 at pos 25 (the "He" feature). This feature fires … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@25, k=10 → Emb:" He"@25 (de=37.00) +9 more |
| 2 | `get_upstream_features` | L14:F5740@25, k=10 → Emb:" He"@25 (de=16.88) +9 more |
| 3 | `get_upstream_features` | L14:F14097@25, k=10 → Emb:" He"@25 (de=2.83) +9 more |
| 4 | `inspect_feature` ×5 | L14:5740, L14:14097, L2:6155, L18:14663, L17:5218 |

### Build

`build_circuit` → 19 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 62,972 | 6,972 | 315,923 | 0 | $0.0462 | — | — |
| **Total** | | **62,972** | **6,972** | **315,923** | **0** | **$0.0462** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 36s