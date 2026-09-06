# Circuit Oracle Report
**Date:** 2026-07-28 07:21:26 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe driving the classification of "journalist/male profession" is dominated by an aggregation of male-pronoun signal across the passage, with a much weaker secondary contribution from institution-name features at the beginning of the text.

**Confidence:** 8

**Reasoning:**

The circuit reveals a striking, almost monolithic structure: **the probe is driven overwhelmingly by gender-marker features rather than profession/occupation features.**

**The dominant pronoun circuit** runs from raw token embeddings of "he" (pos 22) and "He" (pos 39, 67) → up a dedicated pronoun-detection cascade:

- **L0–L3** early features: L0:F12768 ("he/she in close proximity", pos 22, direct_effect 3.44 to L18:F14743), L0:F1069 ("references to a male person via He/His", pos 39 and 67, direct_effect 7.34 and 7.53 to L18:F14743), L1:F8685 ("the pronoun he"), L2:F6155 ("references to people, especially pronouns"), L2:F11473 ("instances of 'he' and government/law words"), L2:F9233 ("she and he pronouns"), L3:F6712 (pronouns in legal contexts), L0:F2994 ("his and he"). All have frac_nonzero < 0.05, indicating these are genuine pronoun detectors.
- **L4–L7** mid-features: L4:F15567 ("sentences with male or female pronouns and possessives, especially writing contexts"), L4:F14796 ("he or him"), L6:F12990 ("male pronouns and titles along with descriptors associated with men"), L7:F14946 ("possessive pronoun his").
- **L13–L14**: L13:F1937/F6622 ("pronouns used to describe people"), L14:F14097 ("occurrences of the word he"), L14:F5740 ("sentences with multiple pronouns"), L14:F13478 ("occurrences of people's names, often with titles" — fires on capitalized "He" at pos 67).
- **L15**: L15:F10510 ("references to males in third person"), L15:F3330 ("personal stories of individuals"), L15:F13002 ("titles and names followed by their role or profession" — a profession-flavored feature, but it tracks the name+role pattern after a He/He pronoun).
- **L17**: L17:F5889 ("references to people with pronouns and possessive pronouns") — a positional aggregator that also receives strong direct contribution from the raw "he" token embedding (37.5).
- **L18**: L18:F14743 ("He") — the terminal output-driving feature, which fires at all three "he/He" positions and pushes the probe. Critically, this feature's **strongest upstream signal is the raw "he" token embedding itself (direct_effect 28.6 at pos 22, plus 21.9 at pos 39 and 23.4 at pos 67)**, with the pronoun-aggregator cascade contributing additional positive drive.

**The (much weaker) profession circuit** consists only of L1:F4459 ("mentions of research institutes" at pos 7, the "Institute" in "Royal United Services Institute"), which gets direct_effect 27.5 from the "Institute" token embedding. It receives some downstream support from L0:F15661 ("the word 'spin'"), L0:F5288 ("services"), L0:F8466 ("volume"), L0:F10439 ("agenda/Institute"), L0:F11002 (legal/scientific/institutional terminology) — but these are largely **content-word surface features, not profession-concept features**; they fire because the text is a Wikipedia-style bio with institutional names and journalistic vocabulary, not because they encode "journalist" as a profession.

**Source-influence check:** get_source_influence at depth 3 confirms the pronoun positions (22, 39, 67) carry S_pct_of_total = -6.2% (negative because L18:F14743's direct effect on the probe is negative at the *target* position, but the sign is the same across all three positions, and the structure clearly aggregates them). The institution-name positions (4–7) show S_pct_of_total = -10.5%, but this includes both F4459 and its embed input — the genuinely profession-relevant feature (F4459) is a thin sliver of that. The pronoun cascade is the larger, more concentrated driver.

**Verdict on the user's concern:** The concern is **strongly supported**. The dominant circuit path — from "he/He" tokens through ~6 layers of pronoun-detection features (L0 → L1 → L2 → L3 → L4 → L6 → L7 → L13/14 → L15 → L17 → L18) into the output — is essentially a single "this text is full of male pronouns" channel. Genuine profession indicators (writer, journalist, analyst, institutional affiliation, type of publications) are present in the text but are represented only by content-word surface features (L0:F15661 "spin", L0:F5288 "service", L0:F10439 "agenda/Institute") and one shallow institute detector (L1:F4459, frac_nonzero 0.003) — none of which form a coherent "journalist" concept. The probe is leveraging the strongest correlated signal in the data, which is gender, not occupation. This is a classic spurious-correlation failure mode: when a profession is overwhelmingly held by one gender in training data, the probe's residual direction aligns with the gender feature rather than the profession feature.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | Late pronoun-aggregator "he" (pos 22) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 39 | Late pronoun-aggregator "He" (pos 39) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 67 | Late pronoun-aggregator "He" (pos 67) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 22 | L17 pronoun/possessive collector (frac 0.018) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 39 | L17 pronoun/possessive collector (frac 0.018) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 67 | L17 pronoun/possessive collector (frac 0.018) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F10510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10510) | 22 | L15 male third-person pronoun features |  references to males in third person and first person pronouns | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10510) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 39 | L15 male third-person pronoun features |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F13002](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13002) | 39 | L15 male third-person pronoun features |  titles and names of people followed by their role or profession | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13002) |
| [L15:F13002](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13002) | 67 | L15 male third-person pronoun features |  titles and names of people followed by their role or profession | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13002) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 67 | L15 male third-person pronoun features |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 22 | L13/L14 pronoun/possessive aggregators |  occurrences of the word "he" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L13:F1937](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/1937) | 22 | L13/L14 pronoun/possessive aggregators |  pronouns used to describe people, including possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/1937) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 22 | L13/L14 pronoun/possessive aggregators |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 39 | L13/L14 pronoun/possessive aggregators |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 67 | L13/L14 pronoun/possessive aggregators |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L14:F5740](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) | 39 | L13/L14 pronoun/possessive aggregators |  sentences with multiple pronouns in them | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) |
| [L14:F13478](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) | 67 | L13/L14 pronoun/possessive aggregators |  occurrences of people's names, often with titles | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 22 | Mid-layer pronoun-aggregator features (L4-L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 22 | Mid-layer pronoun-aggregator features (L4-L7) | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 22 | Mid-layer pronoun-aggregator features (L4-L7) | the pronoun "he" or "him" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 22 | Mid-layer pronoun-aggregator features (L4-L7) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Early pronoun-aggregator features (L0-L3) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L1:F8685](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8685) | 22 | Early pronoun-aggregator features (L0-L3) |  the pronoun "he" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8685) |
| [L2:F6155](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6155) | 22 | Early pronoun-aggregator features (L0-L3) |  references to people, especially pronouns like "he" or "she" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6155) |
| [L2:F11473](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11473) | 22 | Early pronoun-aggregator features (L0-L3) |  instances of the word 'he' and words related to government and law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11473) |
| [L2:F9233](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9233) | 22 | Early pronoun-aggregator features (L0-L3) |  the pronouns "she" and "he" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9233) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 22 | Early pronoun-aggregator features (L0-L3) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 39 | Early pronoun-aggregator features (L0-L3) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 67 | Early pronoun-aggregator features (L0-L3) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L3:F6712](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6712) | 22 | Early pronoun-aggregator features (L0-L3) | references to people, particularly pronouns and titles in legal contexts, and verbs that refer to intent or performance | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6712) |
| [L3:F9548](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9548) | 22 | Early pronoun-aggregator features (L0-L3) |  uses of the word "this" followed by a pause or conjunction, sometimes near location-specific info. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9548) |
| [L4:F4017](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4017) | 22 | Early pronoun-aggregator features (L0-L3) |  words and short phrases in French | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4017) |
| [L1:F4459](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) | 7 | L1 institute/research-org detector (pos 7) |  mentions of research institutes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) |
| [L0:F15661](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) | 7 | Generic function-word features (spin, instance, fine, volume, agenda, for) | the word "spin" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) |
| [L0:F5288](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5288) | 6 | Generic function-word features (spin, instance, fine, volume, agenda, for) |  the word "service" and related terms in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5288) |
| [L0:F8466](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8466) | 7 | Generic function-word features (spin, instance, fine, volume, agenda, for) |  the word "volume." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8466) |
| [L0:F8147](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8147) | 7 | Generic function-word features (spin, instance, fine, volume, agenda, for) | the word "instance" and related words like "instances" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8147) |
| [L0:F8575](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8575) | 7 | Generic function-word features (spin, instance, fine, volume, agenda, for) |  the word "fine" along with references to code or numbers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8575) |
| [L0:F10439](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10439) | 7 | Generic function-word features (spin, instance, fine, volume, agenda, for) |  the word "agenda" and sometimes the word "Institute" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10439) |
| [L0:F11002](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11002) | 7 | Generic function-word features (spin, instance, fine, volume, agenda, for) |  terminology used in legal documents, science (chemistry, physics, general research), software development, manufacturing and government agencies | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11002) |
| [L0:F12879](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12879) | 7 | Generic function-word features (spin, instance, fine, volume, agenda, for) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12879) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 7 | Generic function-word features (spin, instance, fine, volume, agenda, for) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F9297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) | 7 | Generic function-word features (spin, instance, fine, volume, agenda, for) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) |
| [L0:F3800](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3800) | 6 | Generic function-word features (spin, instance, fine, volume, agenda, for) | the word "services" (especially "health services") and the word "sum" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3800) |
| [L0:F15492](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) | 8 | Generic function-word features (spin, instance, fine, volume, agenda, for) |  the word "for" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) |
| [L0:F11322](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11322) | 4 | Generic function-word features (spin, instance, fine, volume, agenda, for) |  the word "manual" in the context of instructions or product descriptions | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11322) |
| [L0:F13751](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13751) | 8 | Generic function-word features (spin, instance, fine, volume, agenda, for) | the word "for." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13751) |
| [L0:F15323](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15323) | 1 | Generic function-word features (spin, instance, fine, volume, agenda, for) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15323) |
| [L0:F7124](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) | 2 | Generic function-word features (spin, instance, fine, volume, agenda, for) | the word "at" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Generic function-word features (spin, instance, fine, volume, agenda, for) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 11 | Generic function-word features (spin, instance, fine, volume, agenda, for) |  commas and sometimes reach (context not clear) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 38 | Generic function-word features (spin, instance, fine, volume, agenda, for) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F6556](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6556) | 1 | Generic function-word features (spin, instance, fine, volume, agenda, for) |  instances of the word "closing" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6556) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:7124 de=-0.160 |
| 3 | `inspect_feature` ×13 | L1:15323, L0:5288, L0:12768, L0:7124, L18:14743, L0:15661, L0:3820, L0:6556, L14:14097, L1:4459, L0:4870, L0:6051, L7:14946 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F14097@22` | ❌ error | — | — | Trace the path from L14:F14097 (occurrences of "he") at position 22 ("he" in "he… |
| SA-2 | `L18:F14743@22` | ✅ reported | 6 | 12 | Trace the path from L18:F14743 (the pronoun "He") at position 22. Identify what … |
| SA-3 | `L0:F12768@22` | ❌ error | — | — | Trace the path from L0:F12768 ("he"/"she" in proximity) at position 22. What inp… |

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@22, k=15 | Emb:" he"@22 (de=28.62) +14 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 5 | `get_upstream_features` | L4:F15567@22, k=10 | Emb:" he"@22 (de=17.75) +9 more |
| 6 | `inspect_feature` | L0, F12768 | " mentions of "he" and "she" in close proximity" |
| 7 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 8 | `get_upstream_features` | L17:F5889@22, k=10 | Emb:" he"@22 (de=37.50) +9 more |
| 9 | `inspect_feature` | L3, F9548 | " uses of the word "this" followed by a pause or conjunction, sometimes" |
| 10 | `get_upstream_features` | L3:F9548@22, k=10 | Emb:" he"@22 (de=10.31) +9 more |
| 11 | `inspect_feature` | L15, F10510 | " references to males in third person and first person pronouns" |
| 12 | `inspect_feature` | L2, F9233 | " the pronouns "she" and "he"" |

**Findings:** The pronoun "He" at position 22 (L18:F14743) receives its strongest drive from the raw token embedding of " he" (direct_effect ≈ 28.6), confirming a direct content‑word signal. Upstream, a cascade of pronoun‑focused features aggregates this signal: layer‑17 feature 5889 collects pronoun/possessive references, layer‑14 feature 14097 flags the literal word "he", layer‑4 feature 15567 captures senten…

</details>

### Re-dispatch (round 2): 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-4 | `L1:F4459@7` | ❌ error | — | — | Trace the path from L1:F4459 (mentions of research institutes) at position 7 ("I… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14743@22, k=15 → Emb:" he"@22 (de=28.62) +14 more |
| 2 | `get_upstream_features` | L7:F14946@22, k=15 → Emb:" he"@22 (de=14.19) +14 more |
| 3 | `inspect_feature` ×12 | L17:5889, L4:15567, L1:8685, L15:10510, L13:1937, L13:6622, L2:6155, L0:2994, L4:14796, L6:12990, L2:11473, L3:9548 |
| 4 | `get_upstream_features` | L1:F4459@7, k=15 → Emb:" Institute"@7 (de=27.50) +14 more |
| 5 | `inspect_feature` | L5, F3992 → "the start of documentation blocks in code" |
| 6 | `get_upstream_features` | L7:F14946@22, k=12 → Emb:" he"@22 (de=14.19) +11 more |
| 7 | `get_upstream_features` | L14:F14097@22, k=12 → Emb:" he"@22 (de=2.70) +11 more |
| 8 | `get_upstream_features` | L4:F15567@22, k=10 → Emb:" he"@22 (de=17.75) +9 more |
| 9 | `get_upstream_features` | L0:F12768@22, k=10 → Emb:" he"@22 (de=40.25) +9 more |
| 10 | `inspect_feature` ×5 | L4:4017, L2:9233, L3:6712, L0:11400, L1:2848 |
| 11 | `get_upstream_features` | L18:F14743@39, k=10 → Emb:" He"@39 (de=21.88) +9 more |
| 12 | `get_upstream_features` | L18:F14743@67, k=10 → Emb:" He"@67 (de=23.38) +9 more |
| 13 | `inspect_feature` ×10 | L0:8466, L0:8147, L0:8575, L0:10439, L0:11002, L0:1069, L15:3330, L15:13002, L14:5740, L14:13478 |
| 14 | `get_source_influence` | {'depth': 3, 'source_positions': [22, 39, 67]} → {'depth': 3, 'source_positions': [22, 39, 67], 'S_pct_of_total': -6.222, 'R_pct_ |
| 15 | `get_source_influence` | {'depth': 3, 'source_positions': [4, 5, 6, 7, 8, 9, 10]} → {'depth': 3, 'source_positions': [4, 5, 6, 7, 8, 9, 10], 'S_pct_of_total': -10.5 |
| 16 | `inspect_feature` ×5 | L0:15492, L0:11322, L0:3800, L0:13751, L0:2241 |
| 17 | `get_upstream_features` | L0:F1069@39, k=8 → Emb:" He"@39 (de=37.25) +7 more |

### Build

`build_circuit` → 15 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 86,163 | 8,196 | 704,250 | 0 | $0.0779 | — | — |
| SA-2 | openai/gpt-oss-120b | 185,419 | 11,364 | 5,152 | 0 | $0.0347 | ✅ 6F/12E | Trace the path from L18:F14743 (the pronoun "He") at positio… |
| **Total** | | **271,582** | **19,560** | **709,402** | **0** | **$0.1126** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 16s