# Circuit Oracle Report
**Date:** 2026-07-28 07:23:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction-classification probe on this NLI-style prompt is driven by a mixture of genuine lexical/topic signals (tourism vocabulary like "tourist office", "pick up", "tours") and a small set of spurious surface features (negation tokens "No one" and the adverb "usually") that, while not irrelevant to the premise/hypothesis mismatch, fire on relatively shallow lexical patterns.

**Confidence:** 6

**Reasoning:** The output node is a linear probe for the contradiction class. Going downstream-to-upstream, late-layer (L3-L4) features are mostly semantically rich and on-topic: **L4:F12961** ("tourist attraction", "points of interest") at pos 8, **L3:F9405** ("tourism/tour" at pos 8), **L3:F8202** ("office" at pos 8) and **L4:F11236** (imperative "ask" at pos 11) — these encode the travel/tourist-office topic and the *action* aspect of the prompt. The strongest single contributor, **L2:F3116** (frac_nonzero=0.006, "pick up" phrasal verb) at pos 2, is also on-topic and gets the bulk of its activation from the **Emb: "Pick" (pos 1)** and **Emb: " up" (pos 2)** nodes (direct_effect 50 and 20.75 from embeddings), with one L0 "up"-word feature (F10562, -7.78) suppressing it slightly. **L2:F14413** ("tour" at pos 14) and **L1:F8587** ("travel agencies" at pos 8) round out the genuine content path.

The concerning findings for the user's worry are the negation-/quantifier-driven features: **L2:F8837** ("the word 'one' or 'body' when preceded by 'no' or 'every'", frac_nonzero=0.011) at pos 17 fires on the "No one" construction — its upstream is dominated by **Emb: " No" (pos 16, de=18.6)** and **Emb: " one" (pos 17, de=9.25)** with **L0:F4438** ("the word 'one'", frac_nonzero=0.001, very specific; promoted: "nobody/Everyone/Nobody") — a classic negation detector, not a contradiction-reasoning feature. **L3:F10901** and **L1:F8159** (both labeled "usually") at pos 19 fire on the adverb "usually" via the **Emb: " usually"** node and have direct_effects of -0.14 / -0.18 against the probe (they push the score toward contradiction). **L0:F7321** ("the word 'so,'") at pos 25 and **L2:F8837** also produce the *No…usually* surface pattern the NLI dataset uses as a contradiction cue. **L4:F4739** ("so followed by a pronoun") at pos 25 is a lexical-syntax detector on the connector.

In short: the circuit does not pivot on a single "negation word" artifact — most of the late-layer mass is tourism/lexical topic features, and a contradiction probe plausibly uses topic + negation together. However, **two of the largest-magnitude contributors (L2:F3116 = -0.35 and L2:F8837 = -0.13) are content-bearing but not contradiction-reasoning per se**: F3116 is a "pick up" phrasal-verb detector, and F8837 is a "no one"/nobody negation pattern. Together with the "usually" adverb features and the "so" connector features, they do amount to a bag of surface cues — negation word, frequency adverb, conjunction — that the probe has learned correlate with contradiction in this kind of prompt, rather than features that compute the *semantic* entailment relationship. So the user's concern is **partially warranted**: the probe leans on the "No one…usually" negation/adverb cue, not just on a deep understanding that the premise and hypothesis actually contradict.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 1 | L0 lexical: 'pick', 'up' at pos 2, 'a', 'from' |  the word "pick" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F10562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) | 2 | L0 lexical: 'pick', 'up' at pos 2, 'a', 'from' | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) |
| [L0:F16358](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16358) | 2 | L0 lexical: 'pick', 'up' at pos 2, 'a', 'from' | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16358) |
| [L0:F10904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) | 1 | L0 lexical: 'pick', 'up' at pos 2, 'a', 'from' | the word "adequate" (and words that appear near it) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 5 | L0 lexical: 'pick', 'up' at pos 2, 'a', 'from' | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F10219](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) | 3 | L0 lexical: 'pick', 'up' at pos 2, 'a', 'from' |  the indefinite article "a" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) |
| [L0:F11658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11658) | 2 | L0 lexical: 'pick', 'up' at pos 2, 'a', 'from' |  occurrences of the substring "up" and phrases that end in the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11658) |
| [L0:F12744](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12744) | 2 | L0 lexical: 'pick', 'up' at pos 2, 'a', 'from' | positive adjectives and adverbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12744) |
| [L0:F7204](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) | 9 | L0 lexical: 'here' (pos 9), 'adoption' (pos 7), 'mapping' (pos 4), 'period' (pos 15), 'about' (pos 12) | the word "here" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) |
| [L0:F306](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) | 7 | L0 lexical: 'here' (pos 9), 'adoption' (pos 7), 'mapping' (pos 4), 'period' (pos 15), 'about' (pos 12) | the word "adoption" in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) |
| [L0:F2868](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2868) | 4 | L0 lexical: 'here' (pos 9), 'adoption' (pos 7), 'mapping' (pos 4), 'period' (pos 15), 'about' (pos 12) |  the word "mapping" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2868) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | L0 lexical: 'here' (pos 9), 'adoption' (pos 7), 'mapping' (pos 4), 'period' (pos 15), 'about' (pos 12) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 12 | L0 lexical: 'here' (pos 9), 'adoption' (pos 7), 'mapping' (pos 4), 'period' (pos 15), 'about' (pos 12) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 17 | L0 lexical: 'one' at pos 17, 'so' at pos 25, 'thing' at pos 9, 'to' at pos 30 | the word "one". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L0:F7321](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) | 25 | L0 lexical: 'one' at pos 17, 'so' at pos 25, 'thing' at pos 9, 'to' at pos 30 |  the word "so," and also matches some words ending in "ware" and "such" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) |
| [L0:F7036](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7036) | 9 | L0 lexical: 'one' at pos 17, 'so' at pos 25, 'thing' at pos 9, 'to' at pos 30 | the word "thing" and words associated with an idea or concept | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7036) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 30 | L0 lexical: 'one' at pos 17, 'so' at pos 25, 'thing' at pos 9, 'to' at pos 30 | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F11351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11351) | 17 | L0 lexical: 'one' at pos 17, 'so' at pos 25, 'thing' at pos 9, 'to' at pos 30 |  the number "one" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11351) |
| [L1:F8159](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) | 19 | L1: 'usually' (8159) and travel/office related words (8587, 7976) |  the word "usually" and, to a lesser extent, words that sometimes accompany it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) |
| [L1:F8587](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8587) | 8 | L1: 'usually' (8159) and travel/office related words (8587, 7976) |  words related to travel, planning trips, and travel agencies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8587) |
| [L1:F7976](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7976) | 11 | L1: 'usually' (8159) and travel/office related words (8587, 7976) | the word "load" in technical documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7976) |
| [L1:F474](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/474) | 4 | L1: 'usually' (8159) and travel/office related words (8587, 7976) | the word "crop" when used to refer to farmed plants | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/474) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | L2: 'pick up' phrasal verb at pos 2 (3116) |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F11769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) | 2 | L2: 'pick up' phrasal verb at pos 2 (3116) | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) |
| [L2:F13586](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) | 17 | L2: 'pick up' phrasal verb at pos 2 (3116) |  words ending in 'thing' and 'one' often with preceding words indicating the presence of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) |
| [L2:F8478](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8478) | 5 | L2: 'pick up' phrasal verb at pos 2 (3116) | SQL queries | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8478) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 17 | L2: 'no one'/'nobody' pattern (8837) at pos 17 |  the word "one" or "body" when preceded by the words "no" or "every." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | L2: 'no one'/'nobody' pattern (8837) at pos 17 | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L2:F5495](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5495) | 19 | L2: 'no one'/'nobody' pattern (8837) at pos 17 |  adverbs of frequency | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5495) |
| [L3:F8202](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8202) | 8 | L3: 'office' context (8202), 'usually' (10901), tourism/operator (9405) |  mentions of legal or governmental offices | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8202) |
| [L3:F10901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10901) | 19 | L3: 'office' context (8202), 'usually' (10901), tourism/operator (9405) | the word "usually" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10901) |
| [L3:F9405](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9405) | 8 | L3: 'office' context (8202), 'usually' (10901), tourism/operator (9405) |  words related to tourism, travel, and organized events | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9405) |
| [L4:F12961](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) | 8 | L4: 'tourism/attractions' (12961 pos 8), 'imperatives' (11236 pos 11), 'so + pronoun' (4739 pos 25) |  words pertaining to tourism | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12961) |
| [L4:F11236](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11236) | 11 | L4: 'tourism/attractions' (12961 pos 8), 'imperatives' (11236 pos 11), 'so + pronoun' (4739 pos 25) |  calls to action and imperative verbs. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11236) |
| [L4:F4739](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4739) | 25 | L4: 'tourism/attractions' (12961 pos 8), 'imperatives' (11236 pos 11), 'so + pronoun' (4739 pos 25) |  the word "so" followed by personal pronouns or words associated with personal experience | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4739) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:8974 de=-0.408 |
| 3 | `inspect_feature` ×15 | L0:8974, L0:7321, L2:3116, L2:13586, L2:11769, L0:6051, L0:10904, L0:2238, L0:306, L1:8159, L0:10562, L2:14413, L0:8566, L0:7204, L0:12744 |
| 4 | `get_top_features` | 30 features; top: L0:8974 de=-0.408 |
| 5 | `inspect_feature` ×15 | L0:8444, L1:474, L2:8478, L3:10901, L0:2868, L0:7036, L0:16358, L4:12961, L1:7976, L4:11236, L3:8202, L4:4739, L2:8837, L0:10219, L0:11658 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F3116@2` | ❌ error | — | — | Trace this feature back to embedding nodes. Feature is the 'pick up' phrasal ver… |
| SA-2 | `L3:F10901@19` | ❌ error | — | — | Trace this 'usually' feature upstream to embedding nodes. Position 19 is 'usuall… |
| SA-3 | `L4:F12961@8` | ❌ error | — | — | Trace this 'tourism words' feature back to embeddings. Pos 8 is 'tourist' in the… |
| SA-4 | `L2:F8837@17` | ❌ error | — | — | Trace this 'no one' feature (L2:F8837) upstream to embeddings. Pos 17 is 'No' in… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F3116@2, k=15 → Emb:"Pick"@1 (de=50.00) +14 more |
| 2 | `get_upstream_features` | L3:F10901@19, k=15 → Emb:" usually"@19 (de=23.50) +14 more |
| 3 | `get_upstream_features` | L4:F12961@8, k=15 → Emb:" tourist"@7 (de=19.12) +14 more |
| 4 | `get_upstream_features` | L2:F8837@17, k=15 → Emb:" No"@16 (de=18.62) +14 more |
| 5 | `inspect_feature` ×10 | L2:5495, L3:9405, L0:4438, L0:11351, L3:8202, L2:15544, L1:8587, L2:14199, L4:4739, L4:11236 |
| 6 | `get_upstream_features` | L4:F4739@25, k=15 → Emb:" so"@25 (de=29.75) +14 more |
| 7 | `get_upstream_features` | L4:F11236@11, k=15 → Emb:" ask"@11 (de=7.72) +14 more |
| 8 | `get_upstream_features` | L3:F8202@8, k=15 → Emb:" office"@8 (de=23.62) +14 more |
| 9 | `get_upstream_features` | L2:F3116@2, k=10 → Emb:"Pick"@1 (de=50.00) +9 more |
| 10 | `get_upstream_features` | L2:F11769@2, k=10 → Emb:" up"@2 (de=19.50) +9 more |
| 11 | `get_upstream_features` | L1:F8159@19, k=10 → Emb:" usually"@19 (de=24.25) +9 more |
| 12 | `get_upstream_features` | L2:F14413@14, k=10 → Emb:" tours"@14 (de=28.38) +9 more |
| 13 | `get_upstream_features` | L3:F9405@8, k=10 → Emb:" tourist"@7 (de=12.38) +9 more |
| 14 | `get_upstream_features` | L4:F4739@25, k=10 → Emb:" so"@25 (de=29.75) +9 more |

### Build

`build_circuit` → 17 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 103,372 | 7,022 | 534,064 | 0 | $0.0715 | — | — |
| **Total** | | **103,372** | **7,022** | **534,064** | **0** | **$0.0715** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 15s