# Circuit Oracle Report
**Date:** 2026-07-28 07:19:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven by a cluster of low/mid-layer features that fire on identity-group terms (race, gender, family relations) — predominantly triggered by the literal tokens "white", "guy", "oriental", "married", "last name", and "self" — rather than by features encoding the actual hateful or threatening content of the statement.

**Confidence:** 6

**Reasoning:** The top of the circuit is a stack of near-redundant "identity-term" detectors. L6:F3902 ("terms referring to race and ethnicity", direct_effect +0.34 / +0.21 / +0.19 across pos 9/10/27) is the strongest driver and is fed by the raw embeddings of the words "white" (pos 9, direct_effect 13.56) and "oriental" (pos 27, direct_effect 8.75), and amplifies through L4:F117 ("race/racism/social-justice terms", +0.31) and L3:F13061 ("race, gender and social issues", +0.39) — both of which trace their dominant positive input straight back to the "white" and "guy" token embeddings (direct_effects 11–13). L6:F5671 (gender/family-relation) and L6:F15948 (gendered words) fire on "guy" (pos 10) and feed directly into the output. The "white" token alone supplies direct_effect ≥11 to four separate race/ethnicity features (L2:F13158, L3:F13061, L4:F117, L6:F3902), and the "oriental" embedding alone triggers L6:F3902 with direct_effect 8.75.

Crucially, the features that actually track the hateful content — slurs like "self hater", "oriental", "lust", the imperative "appears to be" framing — are *not* the dominant contributors. L4:F10004 ("self-" hyphenated words, direct_effect +0.155) is the only feature that even approaches capturing the pejorative "self hater", and it is fed by the "self" token embedding (direct_effect 46.75) — meaning the feature is really just a "self-" prefix detector, not a hostility detector. L0:F241 (marriage, +0.16) is a pure lexical marriage-detector fired by the "married" embedding. L3:F4512 (first/last names, +0.22) is fired by "name" (pos 15, direct_effect 11.6). None of the top features encode the insulting, dehumanizing, or threatening content (the in-group/out-group framing, "lust after", "self hater", "hater like all those other") as a coherent semantic unit; instead they fire on each individual identity-attribute word as if it were a tally mark.

The user's concern is borne out: the probe is reading off a "bag of identity tokens" representation. The signal is dominated by race-words ("white", "oriental"), gender-words ("guy", "women"), and the relational frame ("married", "last name"), while features that would encode actual toxicity semantics (hostility, dehumanization, slur-usage-as-attack) are either absent or comparatively weak. This is consistent with a probe that has learned a shortcut — identity mentions correlate with toxicity in training data — rather than the semantic toxicity of the utterance. Notably, the same "white" token would produce the same L6:F3902 / L4:F117 / L3:F13061 activation in a perfectly neutral sentence like "my white neighbor", and "oriental" alone would still drive L6:F3902. The circuit is not mechanism-specific to toxicity.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 9 | L6 Race/Ethnicity terms (L6:F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 10 | L6 Race/Ethnicity terms (L6:F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 27 | L6 Race/Ethnicity terms (L6:F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 10 | L3 Race/gender social-issues terms (L3:F13061) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 10 | L3 Race/gender social-issues terms (L3:F13061) |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 9 | L3 Race/gender social-issues terms (L3:F13061) |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 9 | L2 Race/Ethnicity words (L2:F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 27 | L2 Race/Ethnicity words (L2:F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 9 | L4 Race/racism terms (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 10 | L4 Race/racism terms (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 27 | L4 Race/racism terms (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L6:F5671](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) | 10 | L6 Gender / family-relation terms (L6:F5671, L6:F15948) |  references to people, with an emphasis on gender and family relations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) |
| [L6:F15948](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) | 10 | L6 Gender / family-relation terms (L6:F5671, L6:F15948) |  words and entities referring to gender and pronouns | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15948) |
| [L3:F4512](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) | 15 | L3 First/last-name mentions (L3:F4512) |  mentions of first names, last names, and phone numbers | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) |
| [L4:F10004](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) | 22 | L4 'self-' hyphenated words (L4:F10004) |  hyphenated words beginning with "self" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) |
| [L0:F241](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/241) | 6 | L0 'marriage' lexical feature (L0:F241) | mentions of marriage | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/241) |
| [L1:F6576](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6576) | 3 | L1 'appearance' (L1:F6576) and L0 'lower/higher' (L0:F7773) and L1 'author' (L1:F5220) |  the word "appearance" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6576) |
| [L0:F7773](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7773) | 3 | L1 'appearance' (L1:F6576) and L0 'lower/higher' (L0:F7773) and L1 'author' (L1:F5220) |  the word "lower" or "higher" in the context of comparisons | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7773) |
| [L1:F5220](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5220) | 2 | L1 'appearance' (L1:F6576) and L0 'lower/higher' (L0:F7773) and L1 'author' (L1:F5220) |  references to authors and publications | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5220) |
| [L0:F753](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) | 2 | L1 'appearance' (L1:F6576) and L0 'lower/higher' (L0:F7773) and L1 'author' (L1:F5220) | the word "author" and words related to selling and prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: white (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: guy (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: oriental (pos 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: married (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: last (pos 14) / name (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: last (pos 14) / name (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: self (pos 21) / hater (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: self (pos 21) / hater (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: author (pos 2) / appears (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: author (pos 2) / appears (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L1:5220 de=-0.453 |
| 3 | `inspect_feature` ×17 | L3:13061, L6:3902, L4:117, L1:384, L1:5220, L1:6576, L2:13158, L3:4512, L1:9113, L0:7773, L0:241, L0:753, L3:10286, L4:10004, L2:15558, L6:5671, L6:15948 |
| 4 | `get_upstream_features` | Emb:" white"@9 (de=13.56) +7 more |
| 5 | `get_upstream_features` | Emb:" white"@9 (de=11.00) +7 more |
| 6 | `get_upstream_features` | Emb:" white"@9 (de=12.12) +7 more |
| 7 | `get_upstream_features` | Emb:" white"@9 (de=13.62) +7 more |
| 8 | `inspect_feature` ×11 | L2:15317, L0:9076, L2:14965, L2:1708, L3:16373, L3:13919, L0:3024, L0:2242, L1:7821, L1:1480, L0:16013 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@9` | ❌ error | — | — | Trace the L6 race/ethnicity feature at position 9 ("white") all the way to embed… |
| SA-2 | `L3:F13061@10` | ❌ error | — | — | Trace the L3 race/gender social issues feature at position 10 ("guy") all the wa… |
| SA-3 | `L2:F13158@9` | ❌ error | — | — | Trace the L2 race/ethnicity feature at pos 9 ("white") all the way to embedding … |
| SA-4 | `L4:F117@10` | ❌ error | — | — | Trace the L4 race/racism feature at pos 10 ("guy") all the way to embedding node… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F5671@10, k=6 → Emb:" guy"@10 (de=5.03) +5 more |
| 2 | `get_upstream_features` | L4:F10004@22, k=6 → Emb:" self"@21 (de=46.75) +5 more |
| 3 | `get_upstream_features` | L3:F4512@15, k=6 → Emb:" last"@14 (de=24.75) +5 more |
| 4 | `get_upstream_features` | L0:F241@6, k=6 → Emb:" married"@6 (de=12.81) +5 more |
| 5 | `get_upstream_features` | L6:F3902@27, k=5 → Emb:" oriental"@27 (de=8.75) +4 more |
| 6 | `get_upstream_features` | L3:F4512@9, k=5 → ❌ Feature (layer=3, feature_idx=4512) not found at pos=9. This |
| 7 | `get_upstream_features` | L0:F7773@3, k=5 → Emb:" appears"@3 (de=14.81) +4 more |
| 8 | `get_upstream_features` | L0:F753@2, k=5 → Emb:" author"@2 (de=18.38) +4 more |

### Build

`build_circuit` → 17 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 62,741 | 6,090 | 291,085 | 0 | $0.0436 | — | — |
| **Total** | | **62,741** | **6,090** | **291,085** | **0** | **$0.0436** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 14s