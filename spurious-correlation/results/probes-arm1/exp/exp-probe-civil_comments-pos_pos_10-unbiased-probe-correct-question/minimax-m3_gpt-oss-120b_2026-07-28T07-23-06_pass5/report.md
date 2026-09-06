# Circuit Oracle Report
**Date:** 2026-07-28 07:23:06 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a constellation of lexical/structural features anchored on a handful of content tokens — the trigger is the *co-occurrence* of the identity word "race" and discourse verbs like "mention" / "question" inside a negation frame, not any "identity group" detector per se.

**Confidence:** 7

**Reasoning:** The output direction is fed by features across layers 0–4, all of which trace back through `get_upstream_features` to specific token embeddings:

- **Identity-token signal (the user's concern):** "race" at pos 5 lights up *three* stacked features — L0:10682 (the word "race", frac_nonzero=0.010, *suppresses* the probe by −0.227 once you combine with the matching L0:14813 "mentions of race, racial issues, racism" suppressor at −0.106) plus the *promoter* L2:10509 ("the word race", +0.146) and L3:5475 ("occurrences of the word race", +0.101). These are not entity-specific detectors — their top activating examples are overwhelmingly **cycling/sporting races** ("tough race over the Wicklow Mountains", "Loughman one of the main organisers"). The racial-context reading comes mainly from L0:14813's autointerp, whose top examples are all "race or gender", "race-based admissions", "race-of-defendant effect" — i.e. it *is* a genuine race-issues feature, but it acts as a **suppressor** of the probe, not a driver.

- **Discourse / metalinguistic signal (the actual driver):** the dominant positive contributions are L4:15173 "statements about mentioning or discussing something" (+0.135), L3:6517 "words related to mentioning" (+0.105), L2:11639 "the word 'mention'" (+0.112), L2:6539 "'mention' and opinion/matter" (+0.100), L2:12770 "'question' and related" + L2:12030 "issue in legal context" feeding L3:672 "the word 'question'" (+0.105), all of which root at Emb:"mentioning" (pos 3, direct_effect up to 27.25 into L2:11639), Emb:"question" (pos 10, direct_effect 38.75 into L3:672 and 30.375 into L2:12770), and Emb:"in"/"not".

- **Negation and uncertainty scaffolding:** L0:4958 "the word 'not'" (+0.227, the largest single effect — but *suppressive* at −0.227) and L2:14569 "uncertainty / lack of clarity phrases" (promoted token "unclear") at +0.099, with L0:2317 "words or phrases expressing uncertainty or doubt" (max_token "far"/"clear"/"too") providing more negation-modality content.

- **Off-target / generic noise:** L0:1903 "sentence-initial The" (frac_nonzero=0.011) and L0:573 "code boolean operators !" (frac_nonzero=0.024, here firing on "By not" — a syntactic false-positive) are generic lexical detectors with no semantic connection to toxicity; they contribute via input bias only.

**Mechanism and answer to the user concern:** The probe is *not* primarily reading off an "identity group" signal. The single largest positive driver is the *discourse* feature L4:15173 ("statements about mentioning or discussing") whose input is the word "mentioning" at pos 3, and its companion L2:11639/6539 cluster. The "race" tokens contribute, but (a) the L0 racial-issues feature is *suppressive*, and (b) the L2/L3 race features have top activating examples dominated by **non-racial** race uses (cycling races). What the probe is actually picking up is the *linguistic pattern* "By not [mentioning/discussing] the [race/question] of [a group]" — a metalinguistic complaint about omission, dressed in the lexical form `negation + discourse verb + identity attribute + in + question`. The circuit is a **lexical-combinatorial** pattern detector, not an identity detector. The genuine toxicity-relevant content (the substantive critique that the text is making a racially-loaded accusation) is largely *not* the signal flowing into the probe; the signal is the *metapragmatic frame* ("this is a complaint about what was not said"). That is a different — and arguably more easily gamed — feature than "identity group content" alone, but it is also not a simple identity-keyword shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F15173](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) | 3 | L4: discourse about mentioning/discussing |  statements about mentioning or discussing something | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) |
| [L4:F2668](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) | 3 | L4: realizations/acknowledgement |  instances of realizations coupled with acknowledgement or acknowledgment of something. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) |
| [L3:F6517](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) | 3 | L3: words related to 'mention' |  words related to mentioning something | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) |
| [L3:F12410](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) | 1 | L3: 'By' at sentence start | the word "By" at the start of a phrase or sentence | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) |
| [L3:F11688](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11688) | 1 | L3: 'By' at sentence start |  instances of the word "By", possibly followed by "the" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11688) |
| [L3:F672](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) | 10 | L3: the word 'question' |  the word "question" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) |
| [L3:F5475](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) | 5 | L3: occurrences of 'race' |  occurrences of the word "race" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) |
| [L2:F11639](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) | 3 | L2: 'mention' / opinion / matter | the word "mention" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) |
| [L2:F6539](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) | 3 | L2: 'mention' / opinion / matter | the word "mention" and words or phrases related to opinions or significance, as well as the word "matter." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) |
| [L2:F10509](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) | 5 | L2: the word 'race' |  the word "race." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) |
| [L2:F14569](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14569) | 3 | L2: uncertainty/lack of clarity phrases |  phrases indicating uncertainty or lack of clarity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14569) |
| [L2:F12770](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12770) | 10 | L2: 'question' and related words | the word "question" and related words | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12770) |
| [L2:F12030](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12030) | 10 | L2: 'question' and related words |  the word "issue" or related terms within a legal context | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12030) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 2 | L0: word 'not' |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F10682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) | 5 | L0: lexical 'race' / racial issues |  the word "race" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) |
| [L0:F14813](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14813) | 5 | L0: lexical 'race' / racial issues |  mentions of race, racial issues, or racism | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14813) |
| [L0:F819](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/819) | 10 | L0: word 'question' (often legal context) |  the word "question" specifically in the context of legal documents or investigations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/819) |
| [L0:F4368](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4368) | 10 | L0: word 'question' (often legal context) |  mentions of questions, references, generalities, or doubts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4368) |
| [L0:F2317](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2317) | 3 | L0: words expressing uncertainty/doubt |  words or phrases expressing uncertainty or doubt | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2317) |
| [L0:F1903](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) | 1 | L0: sentence-initial 'The' | instances of sentences starting with "The" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) |
| [L0:F573](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/573) | 2 | L0: code boolean operators (off-target suppressor) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/573) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:4958 de=-0.227 |
| 3 | `inspect_feature` ×15 | L0:10682, L4:15173, L3:12410, L2:11639, L3:672, L2:6539, L4:2668, L0:4958, L2:10509, L0:1903, L0:14813, L3:5475, L4:573, L0:2317, L0:819 |
| 4 | `get_upstream_features` | Emb:" mentioning"@3 (de=17.50) +9 more |
| 5 | `get_upstream_features` | Emb:"By"@1 (de=48.75) +9 more |
| 6 | `get_upstream_features` | Emb:" mentioning"@3 (de=27.25) +9 more |
| 7 | `get_upstream_features` | Emb:" question"@10 (de=38.75) +9 more |
| 8 | `get_upstream_features` | Emb:" mentioning"@3 (de=7.91) +9 more |
| 9 | `get_upstream_features` | Emb:" not"@2 (de=9.50) +9 more |
| 10 | `get_upstream_features` | Emb:" race"@5 (de=17.00) +9 more |
| 11 | `get_upstream_features` | Emb:" race"@5 (de=30.12) +9 more |
| 12 | `get_upstream_features` | Emb:" race"@5 (de=27.62) +9 more |
| 13 | `get_upstream_features` | Emb:" race"@5 (de=22.62) +9 more |
| 14 | `get_upstream_features` | Emb:" not"@2 (de=30.12) +9 more |
| 15 | `get_upstream_features` | Emb:" in"@9 (de=14.56) +9 more |
| 16 | `get_upstream_features` | Emb:" mentioning"@3 (de=23.12) +7 more |
| 17 | `get_upstream_features` | Emb:" not"@2 (de=12.94) +7 more |
| 18 | `get_upstream_features` | Emb:" question"@10 (de=30.38) +7 more |
| 19 | `inspect_feature` ×4 | L2:12030, L2:12770, L3:6517, L2:14569 |
| 20 | `get_upstream_features` | Emb:" race"@5 (de=27.62) +7 more |
| 21 | `get_upstream_features` | Emb:" in"@9 (de=39.50) +7 more |
| 22 | `get_upstream_features` | Emb:"By"@1 (de=47.50) +7 more |
| 23 | `get_upstream_features` | Emb:" in"@9 (de=16.12) +7 more |
| 24 | `inspect_feature` ×4 | L3:11688, L0:4368, L0:8061, L0:2317 |
| 25 | `get_upstream_features` | Emb:" question"@10 (de=17.25) +7 more |

### Build

`build_circuit` → 24 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 48,158 | 6,268 | 242,174 | 0 | $0.0365 | — | — |
| **Total** | | **48,158** | **6,268** | **242,174** | **0** | **$0.0365** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 18s