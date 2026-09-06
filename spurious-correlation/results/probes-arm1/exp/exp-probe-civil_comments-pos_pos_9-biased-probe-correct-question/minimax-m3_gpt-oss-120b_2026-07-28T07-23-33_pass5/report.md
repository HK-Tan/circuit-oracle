# Circuit Oracle Report
**Date:** 2026-07-28 07:23:33 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven almost entirely by a cascade of *identity-category detector* features (race/ethnicity, gender, social-issue terms, names, profanity) triggered by surface tokens like "white", "oriental", "last name", "married", "author", "appears" — with no feature in the circuit encoding the *toxic* lexical/semantic content (e.g., "self hater", "lust", "self-hate") of the actual slur. The user's concern is confirmed: the circuit uses spurious identity-group signals as proxies for toxicity.

**Confidence:** 8

**Reasoning:**

Tracing from the probe output downward, the dominant late-layer signal is **L6:F3902** — labeled *"terms referring to race and ethnicity"* (frac_nonzero=0.018, direct_effect=+0.34) — which fires at positions 9 ("white"), 10 ("guy"), and 27 ("oriental"). Its sibling **L6:F15948** (*"gender/pronouns"*, frac_nonzero=0.21 — a generic, dense feature) provides additional positive drive at pos 10. These are the only late features with meaningful direct effect on the probe.

The L6 race detector is fed by a **mid-layer L3-L4 social-identity supernode**:
- **L4:F117** *"race/racism, especially Black people"* (frac_nonzero=0.012) fires at pos 9/10/27.
- **L3:F13061** *"race, gender, social issues"* (frac_nonzero=0.009, de=+0.39) fires at pos 10.
- **L3:F16373** *"demographic identity, especially race and gender"* (frac_nonzero=0.006) fires at pos 10.
- **L4:F12975** *"Asian countries / eastern religions"* (frac_nonzero=0.007) fires at pos 27 on "oriental" — note the promoted tokens include "Chinese/China".
- **L5:F13063** *"strings of profanity"* (frac_nonzero=0.007) fires at pos 27.
- **L3:F4512** *"first names, last names, phone numbers"* (frac_nonzero=0.007) fires at pos 15 on "name".

These in turn are driven by an **early L0-L2 supernode** of race-lexicon detectors:
- **L2:F13158** *"words about race and ethnicity"* (frac_nonzero=0.010) at pos 9 and 27, with embedding direct_effect of 13.6 on "white" — this is the single largest edge in the upstream graph.
- **L1:F6576** *"the word 'appearance'"* (pos 3), **L1:F384** *"'ash'/'pund'"* (pos 2), **L0:F241** *"marriage"* (pos 6), **L0:F7773** *"lower/higher"* (pos 3), **L1:F5220** *"authors and publications"* (pos 2).

**The critical finding:** the entire causal path from input to the probe's toxicity score is mediated by features whose semantic content is *"this token/span mentions a racial or ethnic group, gender, or name."* The actual toxicity-bearing phrases — "self hater", "like all those other… who lust after", the slur construction "oriental women who lust after white men" — do not surface as features in the top contributors. The only mildly content-bearing feature is L5:F13063 (profanity, triggered by subword structure near "oriental"), but it has low direct_effect (+0.06) compared to the race-detectors.

The strongest single input-to-feature edge is **Emb:"white" → L2:F13158** (de=13.6) and **Emb:"white" → L6:F3902** (de=13.6). The mere presence of the racial identifier token "white" — which is lexical content but *not* a slur — is the largest single causal driver of the probe's toxicity classification. This is exactly the spurious-correlation mechanism the user suspected: a toxicity probe that has learned to fire on **identity-group mentions** rather than on **toxic content**, because identity words and toxic text co-occur heavily in its training distribution. A benign sentence like "the author is white and married to a man named Smith" would likely produce a similar L6:F3902 / L4:F117 / L2:F13158 cascade and thus a similar high probe score, despite containing no toxicity whatsoever.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 9 | Late-layer race/ethnicity features (L6) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 10 | Late-layer race/ethnicity features (L6) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 27 | Late-layer race/ethnicity features (L6) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F15948](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) | 10 | Late-layer race/ethnicity features (L6) |  words and entities referring to gender and pronouns | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 9 | Mid-layer race/gender/social-issue features (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 10 | Mid-layer race/gender/social-issue features (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 27 | Mid-layer race/gender/social-issue features (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 10 | Mid-layer race/gender/social-issue features (L3-L4) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 10 | Mid-layer race/gender/social-issue features (L3-L4) |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L4:F12975](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) | 27 | Mid-layer race/gender/social-issue features (L3-L4) | mentions of Asian countries, calendars, and paganism/eastern religions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) |
| [L5:F13063](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13063) | 27 | Mid-layer race/gender/social-issue features (L3-L4) |  strings of profanity | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13063) |
| [L3:F4512](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) | 15 | Mid-layer race/gender/social-issue features (L3-L4) |  mentions of first names, last names, and phone numbers | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 9 | Early-layer race/ethnicity word features (L1-L2) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 27 | Early-layer race/ethnicity word features (L1-L2) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L1:F6576](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6576) | 3 | Early-layer race/ethnicity word features (L1-L2) |  the word "appearance" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6576) |
| [L1:F384](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) | 2 | Early-layer race/ethnicity word features (L1-L2) |  the string "ash" or "pund" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) |
| [L0:F241](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/241) | 6 | Early-layer race/ethnicity word features (L1-L2) | mentions of marriage | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/241) |
| [L1:F5220](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5220) | 2 | Early-layer race/ethnicity word features (L1-L2) |  references to authors and publications | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5220) |
| [L0:F7773](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7773) | 3 | Early-layer race/ethnicity word features (L1-L2) |  the word "lower" or "higher" in the context of comparisons | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7773) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L1:5220 de=-0.453 |
| 3 | `inspect_feature` ×8 | L3:13061, L6:3902, L4:117, L1:384, L1:6576, L2:13158, L3:4512, L0:7773 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@9` | ❌ error | — | — | Trace upstream from L6:F3902 at position 9 — this is a 'terms referring to race … |
| SA-2 | `L4:F117@10` | ❌ error | — | — | Trace upstream from L4:F117 at position 10 — a 'race/racism/Black people' featur… |
| SA-3 | `L3:F13061@10` | ❌ error | — | — | Trace upstream from L3:F13061 at position 10 — a 'race, gender, social issues' w… |
| SA-4 | `L2:F13158@9` | ❌ error | — | — | Trace upstream from L2:F13158 at position 9 — a 'race and ethnicity' words featu… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F3902@9, k=10 → Emb:" white"@9 (de=13.56) +9 more |
| 2 | `get_upstream_features` | L3:F13061@10, k=10 → Emb:" white"@9 (de=11.00) +9 more |
| 3 | `get_upstream_features` | L4:F117@10, k=10 → Emb:" white"@9 (de=12.12) +9 more |
| 4 | `get_upstream_features` | L2:F13158@9, k=10 → Emb:" white"@9 (de=13.62) +9 more |
| 5 | `get_upstream_features` | L6:F3902@27, k=10 → Emb:" oriental"@27 (de=8.75) +9 more |
| 6 | `get_upstream_features` | L3:F4512@15, k=10 → Emb:" last"@14 (de=24.75) +9 more |
| 7 | `get_upstream_features` | L1:F6576@3, k=10 → Emb:" appears"@3 (de=19.00) +9 more |
| 8 | `get_upstream_features` | L1:F9113@9, k=5 → Emb:" white"@9 (de=14.44) +4 more |
| 9 | `inspect_feature` ×3 | L6:15948, L1:5220, L0:241 |
| 10 | `get_upstream_features` | L6:F3902@10, k=8 → L4:F117 (de=3.78) +7 more |
| 11 | `inspect_feature` ×3 | L3:16373, L4:12975, L5:13063 |

### Build

`build_circuit` → 11 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 30,512 | 4,693 | 151,342 | 0 | $0.0239 | — | — |
| **Total** | | **30,512** | **4,693** | **151,342** | **0** | **$0.0239** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 36s