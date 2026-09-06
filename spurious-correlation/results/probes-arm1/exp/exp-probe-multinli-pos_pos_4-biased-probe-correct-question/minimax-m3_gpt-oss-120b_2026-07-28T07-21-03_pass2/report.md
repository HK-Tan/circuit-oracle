# Circuit Oracle Report
**Date:** 2026-07-28 07:21:03 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies the input as contradiction primarily because of a lexical "No" → negation cascade anchored at the "No one is usually at the tourist office" token (pos 16), with semantic content words ("pick up", "tours", "map") weakly pushing the opposite direction — the circuit is largely driven by the negation token, not by prompt content.

**Confidence:** 8

**Reasoning:** 

The probe direction receives a strong positive push from a **lexical negation cascade** rooted almost entirely at position 16 ("No" in "No one is usually at the tourist office"). Embedding → L0 (F1143 "the word 'no'", F14862) → L2-L6 negation detectors (F2771 "no and conceptually related negation", F434 "disagreement/negation", F15886 "no/not/never") → L12-L13 phrase-level features (F8719 "phrases that start with 'no'", F10768 "negative sentiments…in a discussion") → L14-L15 mid gates (F336 "the word 'no' and related negative words", F13061 "uses of 'no'…'one'") → L16 late gate (F11298 "no"). Every layer is a "no"-flavored detector — `frac_nonzero` values are 0.002–0.04, all semantically confirming lexical negation. Tracing back, **the L16 gate is driven directly by the " No" token embedding (direct_effect ≈ 12.4) and L14 F336 by the " No" embedding (direct_effect ≈ 33)**. `get_source_influence` confirms position 16 carries S_pct=10.2% with S_over_R=1.41 — the strongest source in the graph.

A second contribution comes from the "No one / nobody" bigram at positions 16-17: L0:F4438 ("the word 'one'") and L2:F8837 ("no/every…one/body") fire jointly. Their top activating examples are dominated by "No one is usually / has ever / ever mentions", confirming the unit encodes the *collocation* "No one" — again, negation, not entity content.

**Counter-evidence is content-driven but weak:** the actual prompt content ("Pick up a map from the tourist office here and ask about walking tours") is carried by L2:F3116 ("Pick up" phrasal verb, direct_effect −0.61 to the probe — i.e. *suppresses* the contradiction classification), L0:F10562 ("up"), L0:F8566 ("pick"), L2:F14413/F1016 ("tour"/"tours", direct_effects −0.28/+0.22), L0:F2238 ("about"), L1:F6872 ("interpretation", incidentally), L8:F1872 (diagrams/charts — off-target), L0:F13354 ("ask"). Their `direct_effect` magnitudes are all smaller than the negation cascade, and `get_source_influence` at positions 2, 14, 1 returns S_over_R of 0.71, 0.14, 0.29 — well below 1, i.e. the "no"-positions dominate.

**Verdict on the user's concern:** The user is correct. The probe's contradiction score is not driven by deep semantic analysis of premise vs. hypothesis alignment — there is no entity-recognition, no overlap feature, no entailment-relation circuit. It is driven by a chain of detectors that fire on the literal token "No" (and "No one") in the second sentence. A contradictory premise with no negation cue (e.g., a negated hypothesis, an antonym swap without "no") would presumably yield a different score from this circuit. This is a textbook spurious correlation: a classifier probe that latched onto "negation word present" rather than to genuine contradiction reasoning.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 16 | Late negation gate (L16: 'no') | no | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 16 | Mid negation gate (L14: 'no' / negative words) | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 16 | Mid negation gate (L14: 'no' / negative words) |  uses of the word "no" or similar negative statements and words associated with "one" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L12:F8719](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) | 16 | Phrase-level 'No' (L12-L13) |  phrases that start with "no." | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) |
| [L13:F10768](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) | 16 | Phrase-level 'No' (L12-L13) |  negative sentiments and words like "no" in the context of a discussion or argument. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) |
| [L6:F15886](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15886) | 16 | Lower negation cascade (L2-L6) |  the word "no" and related negative words like "not" or "never," often near other important keywords. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15886) |
| [L4:F434](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/434) | 16 | Lower negation cascade (L2-L6) |  words and phrases expressing disagreement or negation | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/434) |
| [L3:F3266](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) | 16 | Lower negation cascade (L2-L6) | the abbreviation "No." for Number | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) |
| [L2:F2771](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) | 16 | Lower negation cascade (L2-L6) | the word "no" as well as words and phrases that are conceptually related to negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) |
| [L0:F1143](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) | 16 | Lexical 'no' detectors (L0-L1) |  the word "no" and related words like "nobody" and "trust" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) |
| [L0:F14862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) | 16 | Lexical 'no' detectors (L0-L1) | the word "no" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 17 | 'No one' / 'nobody' unit (L1-L2) |  the word "one" or "body" when preceded by the words "no" or "every." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L1:F15800](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) | 17 | 'No one' / 'nobody' unit (L1-L2) |  the word "one" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 17 | 'No one' / 'nobody' unit (L1-L2) | the word "one". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | 'Pick up' / 'up' / map (pushes AGAINST contradiction) |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L0:F10562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) | 2 | 'Pick up' / 'up' / map (pushes AGAINST contradiction) | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 1 | 'Pick up' / 'up' / map (pushes AGAINST contradiction) |  the word "pick" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L2:F11769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) | 2 | 'Pick up' / 'up' / map (pushes AGAINST contradiction) | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) |
| [L0:F13092](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13092) | 2 | 'Pick up' / 'up' / map (pushes AGAINST contradiction) |  the words "down" and "up", often in combination | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13092) |
| [L0:F7727](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7727) | 4 | 'Pick up' / 'up' / map (pushes AGAINST contradiction) |  code or documentation mentioning the word "mapping." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7727) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | 'Tour'/'tours' (pushes AGAINST contradiction) | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L2:F1016](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) | 14 | 'Tour'/'tours' (pushes AGAINST contradiction) |  forms of the verb "tour" and the noun "tour." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) |
| [L1:F6872](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6872) | 14 | 'Tour'/'tours' (pushes AGAINST contradiction) |  the word "interpretation" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6872) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 12 | 'Tour'/'tours' (pushes AGAINST contradiction) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L4:F11969](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11969) | 4 | 'Tour'/'tours' (pushes AGAINST contradiction) |  mentions of printed advertising materials | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11969) |
| [L8:F1872](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/1872) | 4 | 'Tour'/'tours' (pushes AGAINST contradiction) |  words and phrases related to diagrams and presentations | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/1872) |
| [L0:F13354](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13354) | 11 | 'Tour'/'tours' (pushes AGAINST contradiction) | the word "ask" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13354) |
| [L4:F10722](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10722) | 9 | Deictic / structure (L4) | uses of the word "here" alongside demonstrative pronouns and temporal words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10722) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | Punctuation / period feature (pushes AGAINST) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:3116 de=-0.609 |
| 3 | `inspect_feature` ×20 | L2:3116, L0:10562, L0:10904, L2:14413, L1:15800, L2:1016, L0:2238, L4:10722, L0:8566, L2:8837, L2:11769, L0:13092, L0:6051, L0:7727, L14:336, L1:6872, L4:11969, L8:1872, L16:11298, L0:13354 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F11298@16` | ✅ reported | 7 | 24 | Trace this L16 'no/negation' feature upstream to identify what input tokens and … |
| SA-2 | `L14:F336@16` | ✅ reported | 7 | 6 | Trace this L14 'no/negation' feature upstream to identify what drives it. Is it … |
| SA-3 | `L2:F3116@2` | ✅ reported | 4 | 5 | Trace this L2 'pick up' phrasal verb feature upstream. The input is "Pick up a m… |
| SA-4 | `L2:F8837@17` | ❌ error | — | — | Trace this L2 'no one / nobody' feature upstream. Input is "...so you'll have to… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F11298 | "no" |
| 2 | `get_upstream_features` | L16:F11298@16, k=10 | Emb:" No"@16 (de=12.44) +9 more |
| 3 | `inspect_feature` | L15, F13061 | " uses of the word "no" or similar negative statements and words associ" |
| 4 | `get_upstream_features` | L15:F13061@16, k=10 | Emb:" No"@16 (de=12.50) +9 more |
| 5 | `inspect_feature` | L6, F15886 | " the word "no" and related negative words like "not" or "never," often" |
| 6 | `get_upstream_features` | L6:F15886@16, k=10 | Emb:" No"@16 (de=14.44) +9 more |
| 7 | `inspect_feature` | L4, F434 | " words and phrases expressing disagreement or negation" |
| 8 | `inspect_feature` | L14, F336 | "the word "no" and related negative words" |

**Findings:** The L16 'no' feature (F11298) is driven primarily by the raw input embedding for the token "No" at position 16 (direct_effect ~12.4), confirming a lexical source. Upstream, a cascade of specialized negation detectors (layers 15, 14, 12, 13, 6, 4) amplify the signal. Notably, layer‑4 feature 434 is an early‑layer (≤8) detector of disagreement/negation, and its activation flows through layer‑6 featu…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F336 | "the word "no" and related negative words" |
| 2 | `get_upstream_features` | L14:F336@16, k=10 | Emb:" No"@16 (de=33.00) +9 more |
| 3 | `inspect_feature` | L0, F1143 | " the word "no" and related words like "nobody" and "trust"" |
| 4 | `inspect_feature` | L13, F10768 | " negative sentiments and words like "no" in the context of a discussio" |
| 5 | `get_upstream_features` | L0:F1143@16, k=10 | Emb:" No"@16 (de=26.88) +9 more |
| 6 | `inspect_feature` | L3, F3266 | " the abbreviation "No." for Number" |
| 7 | `inspect_feature` | L2, F2771 | " the word "no" as well as words and phrases that are conceptually rela" |
| 8 | `inspect_feature` | L12, F8719 | " phrases that start with "no."" |
| 9 | `get_upstream_features` | L3:F3266@16, k=10 | Emb:" No"@16 (de=27.50) +9 more |
| 10 | `get_upstream_features` | L13:F10768@16, k=10 | Emb:" No"@16 (de=11.88) +9 more |
| 11 | `get_upstream_features` | L2:F2771@16, k=10 | Emb:" No"@16 (de=13.75) +9 more |
| 12 | `get_upstream_features` | L12:F8719@16, k=10 | Emb:" No"@16 (de=15.38) +9 more |

**Findings:** The L14 negation feature (F336) is driven primarily by the raw token embedding for "No" (positive direct effect ~33 at this layer). The embedding activates low‑level lexical detectors in layer‑0 (features 1143 and 14862) that are highly specific to the token "No". Their activation propagates upward through a cascade of higher‑layer features that broaden the representation: layer‑2 feature 2771 gro…

</details>

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F3116 | " the phrasal verb "pick up" and variations" |
| 2 | `get_upstream_features` | L2:F3116@2, k=10 | Emb:"Pick"@1 (de=50.00) +9 more |
| 3 | `inspect_feature` | L0, F11794 | " text related to external, imposed restrictions or conditions" |
| 4 | `inspect_feature` | L0, F12744 | "positive adjectives and adverbs" |
| 5 | `inspect_feature` | L0, F7064 | "conditional statements within programming code, and potentially tempor" |

**Findings:** The L2 feature 3116 is strongly driven by the embeddings of the exact tokens 'Pick' and ' up' (direct effects 50.0 and 20.75), indicating it encodes the specific phrasal verb token pair. Minor upstream contributions from generic low‑frequency features (restrictions, positivity, conditionals) exist but are negligible. The tracing reached layer 0 (lower‑third floor) and identified embedding nodes, s…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F8837@17, k=8 → Emb:" No"@16 (de=18.62) +7 more |
| 2 | `get_upstream_features` | L2:F1016@14, k=8 → Emb:" tours"@14 (de=27.75) +7 more |
| 3 | `get_upstream_features` | L1:F15800@17, k=6 → Emb:" one"@17 (de=15.25) +5 more |
| 4 | `get_source_influence` | {'depth': 3, 'source_positions': [16]} → {'depth': 3, 'source_positions': [16], 'S_pct_of_total': 10.221, 'R_pct_of_total |
| 5 | `get_source_influence` | {'depth': 3, 'source_positions': [17]} → {'depth': 3, 'source_positions': [17], 'S_pct_of_total': 3.537, 'R_pct_of_total' |
| 6 | `inspect_feature` ×9 | L0:4438, L0:11351, L15:13061, L6:15886, L4:434, L13:10768, L12:8719, L0:1143, L0:14862 |
| 7 | `get_source_influence` | {'depth': 3, 'source_positions': [2]} → {'depth': 3, 'source_positions': [2], 'S_pct_of_total': 7.265, 'R_pct_of_total': |
| 8 | `get_source_influence` | {'depth': 3, 'source_positions': [14]} → {'depth': 3, 'source_positions': [14], 'S_pct_of_total': 1.439, 'R_pct_of_total' |
| 9 | `get_source_influence` | {'depth': 3, 'source_positions': [1]} → {'depth': 3, 'source_positions': [1], 'S_pct_of_total': 2.953, 'R_pct_of_total': |

### Build

`build_circuit` → 17 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 105,786 | 6,113 | 222,838 | 0 | $0.0524 | — | — |
| SA-3 | openai/gpt-oss-120b | 45,601 | 2,763 | 0 | 0 | $0.0085 | ✅ 4F/5E | Trace this L2 'pick up' phrasal verb feature upstream. The i… |
| SA-2 | openai/gpt-oss-120b | 175,967 | 9,893 | 2,560 | 0 | $0.0324 | ✅ 7F/6E | Trace this L14 'no/negation' feature upstream to identify wh… |
| SA-1 | openai/gpt-oss-120b | 97,607 | 9,340 | 2,560 | 0 | $0.0203 | ✅ 7F/24E | Trace this L16 'no/negation' feature upstream to identify wh… |
| **Total** | | **424,961** | **28,109** | **227,958** | **0** | **$0.1136** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 53s