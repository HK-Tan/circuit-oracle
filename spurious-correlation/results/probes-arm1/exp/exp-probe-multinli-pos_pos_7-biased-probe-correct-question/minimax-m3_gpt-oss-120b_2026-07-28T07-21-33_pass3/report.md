# Circuit Oracle Report
**Date:** 2026-07-28 07:21:33 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is driven primarily by late-layer negation/contradiction features (e.g., L16:F12358 "not"+form-of-"to be" at pos 29, L16:F9779 "won't/not" at pos 23, and L13:F3295 "is/are not") that read out generic negation lexical items, with smaller contributions from a generic "bodies of water" feature (L14:F10408) on the "sea" token, while entity-recognition features (church, abbey, specific landmark) contribute little to no net effect.

**Confidence:** 7

**Reasoning:** The user's suspicion is well-founded by the circuit. The strongest positive contributions to the probe direction come from late-layer transcoder features whose semantic content is essentially "this token is a negation" rather than any actual understanding of the premise–hypothesis relationship:

- **L16:F12358 @29** (direct_effect 0.3594): labeled "the word 'not' followed within a few tokens by a form of the verb 'to be'". This fires on the final "not" in "...abbey is not of great height" and is fed by the token embeddings of "not" and "is" (direct_effects 19.5 and 4.4) plus L13:F3295 (a dedicated "is/are not" detector).
- **L16:F9779 @23** (direct_effect 0.2393): labeled "negation words or contractions like 'won't', 'not', 'never'", fires on the first "not" in "...you will not forget" and is fed by the embeddings of "will" (7.3) and "not" (6.8).
- **L13:F3295 @29** (direct_effect 0.1855): a mid-layer "is/are not" feature, with the "not" token embedding (17.75) as its dominant input.

The upstream chains for these are pure lexical: the "not" token embedding at position 29 (or 23) drives L0:F4958 ("the word 'not'") and then the dedicated negation features in layers 13 and 16. There is no entity-specific feature (e.g., a "Mont Saint-Michel" detector) carrying the premise subject; the only top-level features touching the *content* of the premise are L14:F10408 (a generic "geographical locations / bodies of water" detector) on "sea", L5:F14591 (a generic "Catholic church" detector on "abbey", with a small *negative* direct_effect −0.174), and L3:F16223 (a generic "Baltic Sea" detector on "sea", also *negative* −0.158). These are not landmark-specific — the church feature fires on generic church vocabulary, and the "Baltic Sea" feature is irrelevant noise.

Several L0 features (L0:F3820 "the", L0:F2848 "of", L0:F7710 "you", L0:F5060 "dinner/breakfast", L0:F11375 "is") and the L4 features (L4:F3833 "plot summary/courtroom", L4:F11810 "That/paragraph") all show positive direct_effects to the probe but are essentially generic-function-word detectors that happen to fire on common boilerplate ("That first glimpse…", "of", "the"). They are not evidence of semantic understanding.

The most content-relevant features in the top-15 list (L14:F10408 "geographical/bodies of water" at 0.1758, L5:F14591 "Catholic church" at −0.1738, L3:F16223 "Baltic Sea" at −0.1582) are all generic categories rather than landmark-specific entities, and the church/sea-specific ones are *inhibiting* the probe direction. Meanwhile, the probe is *boosted* by features that fire on any sufficiently long sentence containing a "not"-type contraction, regardless of whether the negation is actually contradicting the premise.

In sum, the circuit is consistent with the user's concern: the contradiction probe rides almost entirely on **lexical negation detectors** (the literal "not" token, "is/are not" patterns, and contraction forms) plus a small amount of **generic function-word / boilerplate** signal, while actual prompt content (the specific landmark, the semantic incompatibility between "steepled" and "lacks a steeple") is barely represented — and where it appears (church, sea features), it pushes *against* the probe direction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 29 | Late negation: 'not' + form-of-'to be' pattern (L16:F12358 @29) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L16:F9779](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) | 23 | Negation contraction / 'won't','not' feature (L16:F9779 @23) | negation words or contractions like "won't", "not", "never" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 29 | Mid-layer 'is/are not' / other 'not' feature (L13:F3295 @29) | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L14:F10408](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) | 14 | Geographic / 'bodies of water' feature (L14:F10408 @14) |  geographical locations, especially related to bodies of water | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) |
| [L5:F14591](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14591) | 10 | Catholic-church vocabulary feature (L5:F14591 @10) — negative direct_effect |  words related to the Catholic church | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14591) |
| [L3:F16223](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16223) | 14 | Generic 'Baltic Sea' / marine feature (L3:F16223 @14) — negative direct_effect |  mentions of the Baltic Sea | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16223) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 29 | Layer-0 literal 'not' word feature (L0:F4958) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 23 | Layer-0 literal 'not' word feature (L0:F4958) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 18 | Layer-0 literal 'is' word feature (L0:F11375) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 21 | Layer-0 literal 'you' word feature (L0:F7710) | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | Layer-0 literal 'the' word feature (L0:F3820) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | Layer-0 literal 'of' word feature (L0:F2848) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F5060](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5060) | 1 | Layer-0 'dinner/breakfast' feature (L0:F5060) — top boosting, low-semantic relevance | mentions of dinner or breakfast | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5060) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 3 | Layer-4 'plot summary / courtroom' word feature (L4:F3833) |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F3833](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) | 4 | Layer-4 'plot summary / courtroom' word feature (L4:F3833) |  words used when summarizing plot points or providing courtroom insights | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3833) |
| [L4:F11810](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11810) | 1 | Layer-4 'That' / paragraph context feature (L4:F11810) |  the words "that", "way", "refer", "affirmative", "ished", located near a long sentence or paragraph | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11810) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L16:12358 de=0.359 |
| 3 | `inspect_feature` ×14 | L16:12358, L16:9779, L0:3820, L0:11375, L13:3295, L0:4958, L0:7710, L0:5060, L0:2848, L14:10408, L5:14591, L4:3833, L4:11810, L3:16223 |
| 4 | `get_upstream_features` | Emb:" not"@29 (de=19.50) +9 more |
| 5 | `get_upstream_features` | Emb:" will"@22 (de=7.31) +9 more |
| 6 | `get_upstream_features` | Emb:" not"@29 (de=17.75) +9 more |
| 7 | `get_upstream_features` | Emb:" sea"@14 (de=22.88) +9 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@29` | ❌ error | — | — | Trace the path from L16:F12358 (negation "not"+"to be" pattern) at pos 29. What … |
| SA-2 | `L16:F9779@23` | ❌ error | — | — | Trace the path from L16:F9779 (negation "not"/"won't" feature) at pos 23. Identi… |
| SA-3 | `L14:F10408@14` | ❌ error | — | — | Trace the path from L14:F10408 (geographical locations / bodies of water) at pos… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×9 | L3:8011, L0:9646, L2:12021, L15:10071, L15:3521, L4:4173, L6:3848, L4:4492, L2:12694 |
| 2 | `get_upstream_features` | L3:F8011@29, k=8 → Emb:" not"@29 (de=21.62) +7 more |
| 3 | `get_upstream_features` | L15:F10071@29, k=8 → Emb:" not"@29 (de=9.75) +7 more |
| 4 | `get_upstream_features` | L4:F4173@14, k=8 → Emb:" sea"@14 (de=21.62) +7 more |
| 5 | `get_upstream_features` | L5:F14591@10, k=8 → Emb:" abbey"@10 (de=10.00) +7 more |
| 6 | `get_upstream_features` | L4:F3833@3, k=8 → Emb:" glimpse"@3 (de=13.56) +7 more |
| 7 | `get_upstream_features` | L4:F11810@1, k=8 → Emb:"That"@1 (de=14.31) +7 more |
| 8 | `get_upstream_features` | L3:F16223@14, k=8 → Emb:" sea"@14 (de=19.88) +7 more |
| 9 | `get_upstream_features` | L14:F10408@14, k=15 → Emb:" sea"@14 (de=22.88) +14 more |
| 10 | `inspect_feature` ×8 | L4:4605, L4:1104, L4:4872, L8:3174, L7:5770, L7:9840, L5:5540, L13:15057 |
| 11 | `get_upstream_features` | L5:F14591@10, k=8 → Emb:" abbey"@10 (de=10.00) +7 more |
| 12 | `get_upstream_features` | L0:F5060@1, k=8 → Emb:"That"@1 (de=11.88) +7 more |
| 13 | `get_upstream_features` | L0:F3820@5, k=8 → Emb:" the"@5 (de=34.25) +7 more |
| 14 | `get_upstream_features` | L0:F7710@21, k=8 → Emb:" you"@21 (de=42.25) +7 more |
| 15 | `get_upstream_features` | L0:F11375@18, k=8 → Emb:" is"@18 (de=32.50) +7 more |
| 16 | `get_upstream_features` | L0:F2848@4, k=8 → Emb:" of"@4 (de=35.25) +7 more |
| 17 | `get_upstream_features` | L13:F3295@29, k=15 → Emb:" not"@29 (de=17.75) +14 more |
| 18 | `get_upstream_features` | L16:F9779@23, k=15 → Emb:" will"@22 (de=7.31) +14 more |
| 19 | `get_upstream_features` | L16:F12358@29, k=15 → Emb:" not"@29 (de=19.50) +14 more |

### Build

`build_circuit` → 20 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 73,706 | 6,426 | 422,635 | 0 | $0.0552 | — | — |
| **Total** | | **73,706** | **6,426** | **422,635** | **0** | **$0.0552** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 43s