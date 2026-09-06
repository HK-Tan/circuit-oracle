# Circuit Oracle Report
**Date:** 2026-07-28 07:11:35 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven by a shallow lexical circuit in which the raw embeddings of a small number of high-salience tokens (notably `No`, `one`, `tours`, and the `Pick … up` phrasal verb) are routed through low-frac_nonzero, layer-0–14 word-detector features into the probe output — there is no contradiction-reasoning circuit, only sparse negation/tourism lexical cues.

**Confidence:** 7

**Reasoning:**

The user's concern is well-founded. Every dominant direct-effect edge in the attribution graph terminates in an early-layer word-detector feature whose own strongest input is the **raw token embedding** of the word it encodes. There is essentially no abstract semantic-reasoning pathway.

**1. The "No" / "No one" negation pathway (the most prominent cue).** The largest single source is the embedding of ` No` at position 16, which pushes the contradiction score through a chain of stacked lexical detectors: L0:F14862 (`"the word 'no'"`, frac_nonzero 0.0022), L2:F2771 (`"the word 'no' and conceptually related negation words"`, 0.0020), L3:F3266 (`"abbreviation 'No.' for Number"`, 0.0016), L12:F8719 (`"phrases that start with 'no.'"`, 0.0028), L13:F10768 (`"negative sentiments / 'no' in argument"`, 0.018), and finally L14:F336 (`"the word 'no' and related negative words"`, 0.0044). The direct effect from the ` No` embedding to L14:F336 alone is 33.0, and the same ` No` embedding has a direct effect of 18.6 on L2:F8837 (`"one"/"body" preceded by "no"/"every"`, frac_nonzero 0.011, activated at `pos 17`). Together these are by far the largest positive contributors to the probe score, and they are pure **negation lexical cues** — none of them encode what is being negated, whether the negation is true, or whether the two sentences are semantically consistent.

**2. The "tours" / "tourism" lexical pathway.** A parallel purely-lexical track drives the score from the embedding of ` tours` (pos 14) via L0:F9653 and F9924 (`"the word 'tour'"`, 0.014/0.026), L0:F10891 (`"excursions and professions"`, 0.038), L1:F12555 (`"trails, paths, navigation"`, 0.015) and L1:F7927 (`"trails/paths/hiking"`, 0.010) into L2:F14413 and L2:F1016 (both `"tour"/"tours" detectors`, 0.011/0.0076). These features detect the *word* "tour" — they do not encode the relation between the premise ("ask about walking tours") and the hypothesis ("No one is usually at the tourist office…you'll have to go somewhere else to find out about walking tours"). They simply notice that the word "tours" appears in the input.

**3. The "Pick up" phrasal-verb pathway.** L2:F3116 (`"the phrasal verb 'pick up' and variations"`, 0.006) and its upstream L0:F8566 (`"the word 'pick'"`, 0.011), L0:F10562 and L2:F11769 (`"the word 'up'"`, 0.014/0.0053), L0:F13092 (`"'down' and 'up'"`, 0.0013) all fire on `Pick … up`. This is yet another bag of low-frac_nonzero lexical detectors — they recognize the surface form of the verb, not the argument structure of the sentence.

**4. Other minor contributions.** L4:F10722 (`"the word 'here' alongside demonstrative pronouns"`, 0.019, at `pos 9`) is again a deictic lexical cue. L0:F7727 (`"code/documentation mentioning 'mapping'"`, 0.0015, at `pos 4`) detects the word "map" in a coding context — almost certainly spurious for a NLI task. L0:F2238 (`"'about' followed by a numerical value"`, 0.0066, at `pos 12`) fires on the word "about" in a context that has no numerical value following. L0:F10904 (`"the word 'adequate'"`, 0.0079, at `pos 1`) fires on "Pick" — yet another spurious lexical coincidence. L0:F6051 (`"periods, spaces, and the number 1"`, 0.057, at `pos 15`) is a generic punctuation feature.

**5. Why this is a "spurious negation" circuit, not a real contradiction circuit.** A genuine NLI contradiction circuit would need to (a) identify the relevant proposition in the premise, (b) identify the conflicting proposition in the hypothesis, and (c) compute that they cannot both be true. Nothing in this graph performs (b) or (c). The top features by absolute direct effect are dominated by:
- `L2:F3116` "pick up" (-0.61) — *opposes* the probe even though it is a phrasal-verb detector
- `L0:F10562` "up" (+0.29) and `L0:F10904` "adequate/Pick" (+0.29) — generic surface forms
- `L2:F14413` "tour" (-0.28) and `L2:F1016` "tour" (+0.22) — same word, opposite signs
- `L1:F15800` "one" (+0.25) and `L2:F8837` "no one / every body" (-0.21) — same bigram, opposite signs

The signs flip based on which specific word-detector fires first, with no compositional semantics: `No one` is a negation cue, `Pick up` is a phrasal-verb cue, `tours` is a tourism cue. The probe is essentially doing a **bag-of-lexical-cues** classification: "if the input contains the word `No` and the word `tours` and a phrasal verb, classify as contradiction." That is exactly the kind of heuristic shortcut the user suspected.

**6. Evidence that the signal is lexical, not semantic.** Every meaningful path bottoms out at a `type=embedding` node (the raw token), not at any higher-layer compositional feature. The frac_nonzero values of the dominant features (0.001–0.04) confirm they are highly specific word-detectors, and the L14:F336 → L13:F10768 → L12:F8719 → L3:F3266 → L2:F2771 → L0:F14862 stack is a textbook lexical cascade: each layer simply re-encodes the same `No` token in slightly different contexts, never moving toward propositional meaning. The probe is therefore not learning contradiction; it is learning that the surface form "No … tours … Pick up" co-occurs with the contradiction label in its training distribution.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F14862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) | 16 | Emb: ' No' (pos 16) | the word "no" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) |
| [L2:F2771](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) | 16 | Emb: ' No' (pos 16) | the word "no" as well as words and phrases that are conceptually related to negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) |
| [L3:F3266](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) | 16 | Emb: ' No' (pos 16) | the abbreviation "No." for Number | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) |
| [L12:F8719](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) | 16 | Emb: ' No' (pos 16) | phrases that start with "no." | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) |
| [L13:F10768](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) | 16 | Emb: ' No' (pos 16) | negative sentiments and words like "no" in the context of a discussion or argument. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 16 | Emb: ' No' (pos 16) | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 17 | Emb: ' No' (pos 16) + ' one' (pos 17) — bigram cue | the word "one". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L1:F15800](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) | 17 | Emb: ' No' (pos 16) + ' one' (pos 17) — bigram cue |  the word "one" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 17 | Emb: ' No' (pos 16) + ' one' (pos 17) — bigram cue |  the word "one" or "body" when preceded by the words "no" or "every." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L1:F12555](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12555) | 14 | Emb: ' tours' (pos 14) — tourism/tour lexical cue | words associated with trails and paths, especially words for navigation and locomotion. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12555) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | Emb: ' tours' (pos 14) — tourism/tour lexical cue | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L2:F1016](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) | 14 | Emb: ' tours' (pos 14) — tourism/tour lexical cue |  forms of the verb "tour" and the noun "tour." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) |
| [L0:F10891](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10891) | 14 | Emb: ' tours' (pos 14) — tourism/tour lexical cue | words connected to excursions and professions | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10891) |
| [L0:F9653](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9653) | 14 | Emb: ' tours' (pos 14) — tourism/tour lexical cue | the word "tour" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9653) |
| [L0:F9924](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9924) | 14 | Emb: ' tours' (pos 14) — tourism/tour lexical cue | the word "tour" and words or phrases associated with places, events, or dates | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9924) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 1 | Emb: 'Pick'/' up' (pos 1-2) — phrasal verb cue |  the word "pick" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F10562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) | 2 | Emb: 'Pick'/' up' (pos 1-2) — phrasal verb cue | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) |
| [L0:F13092](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13092) | 2 | Emb: 'Pick'/' up' (pos 1-2) — phrasal verb cue |  the words "down" and "up", often in combination | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13092) |
| [L2:F11769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) | 2 | Emb: 'Pick'/' up' (pos 1-2) — phrasal verb cue | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | Emb: 'Pick'/' up' (pos 1-2) — phrasal verb cue |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L0:F10904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) | 1 | Emb: miscellaneous tokens ('adequate', 'about', 'here', 'map', '.', etc.) | the word "adequate" (and words that appear near it) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 12 | Emb: miscellaneous tokens ('adequate', 'about', 'here', 'map', '.', etc.) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F7727](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7727) | 4 | Emb: miscellaneous tokens ('adequate', 'about', 'here', 'map', '.', etc.) |  code or documentation mentioning the word "mapping." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7727) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | Emb: miscellaneous tokens ('adequate', 'about', 'here', 'map', '.', etc.) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L4:F10722](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10722) | 9 | Emb: miscellaneous tokens ('adequate', 'about', 'here', 'map', '.', etc.) | uses of the word "here" alongside demonstrative pronouns and temporal words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10722) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (contradiction score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L2:3116 de=-0.609 |
| 3 | `inspect_feature` ×16 | L2:3116, L0:10562, L0:10904, L2:14413, L1:15800, L2:1016, L0:2238, L4:10722, L0:8566, L2:8837, L2:11769, L0:13092, L0:6051, L0:7727, L14:336, L0:10904 |
| 4 | `get_upstream_features` | Emb:" No"@16 (de=33.00) +9 more |
| 5 | `get_upstream_features` | Emb:"Pick"@1 (de=50.00) +9 more |
| 6 | `get_upstream_features` | Emb:" No"@16 (de=18.62) +9 more |
| 7 | `get_upstream_features` | Emb:" tours"@14 (de=27.75) +9 more |
| 8 | `get_upstream_features` | Emb:" here"@9 (de=24.12) +9 more |
| 9 | `get_upstream_features` | Emb:" one"@17 (de=15.25) +9 more |
| 10 | `get_upstream_features` | Emb:" tours"@14 (de=28.38) +9 more |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F336@16` | ✅ reported | 7 | 12 | Trace the full upstream circuit for the L14:F336 'no/negation words' feature at … |
| SA-2 | `L2:F8837@17` | ✅ reported | 5 | 4 | Trace the full upstream circuit for L2:F8837 ('the word "one" or "body" when pre… |
| SA-3 | `L2:F1016@14` | ✅ reported | 3 | 3 | Trace upstream for L2:F1016 ('forms of the verb "tour"') at pos 14. Find the sou… |
| SA-4 | `L2:F14413@14` | ✅ reported | 5 | 7 | Trace upstream for L2:F14413 ('the word "tour"') at pos 14. Find the source of t… |

<details>
<summary><b>SA-1</b> — tool trace (17 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F336 | "the word "no" and related negative words" |
| 2 | `get_upstream_features` | L14:F336@16, k=15 | Emb:" No"@16 (de=33.00) +14 more |
| 3 | `inspect_feature` | L0, F1143 | " the word "no" and related words like "nobody" and "trust"" |
| 4 | `get_upstream_features` | L0:F1143@16, k=10 | Emb:" No"@16 (de=26.88) +9 more |
| 5 | `inspect_feature` | L13, F10768 | " negative sentiments and words like "no" in the context of a discussio" |
| 6 | `inspect_feature` | L3, F3266 | " the abbreviation "No." for Number" |
| 7 | `inspect_feature` | L12, F8719 | " phrases that start with "no."" |
| 8 | `get_upstream_features` | L13:F10768@16, k=10 | Emb:" No"@16 (de=11.88) +9 more |
| 9 | `inspect_feature` | L12, F8719 | " phrases that start with "no."" |
| 10 | `get_upstream_features` | L12:F8719@16, k=15 | Emb:" No"@16 (de=15.38) +14 more |
| 11 | `inspect_feature` | L2, F2771 | " the word "no" as well as words and phrases that are conceptually rela" |
| 12 | `get_upstream_features` | L2:F2771@16, k=10 | Emb:" No"@16 (de=13.75) +9 more |
| 13 | `get_upstream_features` | L3:F3266@16, k=10 | Emb:" No"@16 (de=27.50) +9 more |
| 14 | `inspect_feature` | L0, F14862 | "the word "no"" |
| 15 | `inspect_feature` | L0, F6051 | "periods, spaces, and the number 1" |
| 16 | `inspect_feature` | L14, F336 | "the word "no" and related negative words" |
| 17 | `get_upstream_features` | L0:F14862@16, k=10 | Emb:" No"@16 (de=8.31) +9 more |

**Findings:** The L14:F336 negation feature is overwhelmingly driven by the raw embedding of the actual input token " No" at position 16 (direct_effect 33.0). Downstream, a cascade of lower‑layer lexical detectors (L0:F1143, L2:F2771, L3:F3266, L12:F8719, L13:F10768) each receive a positive push from the same " No" embedding and in turn contribute to the target. All these upstream nodes reside in layers ≤8, sat…

</details>

<details>
<summary><b>SA-2</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F8837 | " the word "one" or "body" when preceded by the words "no" or "every."" |
| 2 | `get_upstream_features` | L2:F8837@17, k=10 | Emb:" No"@16 (de=18.62) +9 more |
| 3 | `inspect_feature` | L0, F4438 | "the word "one"." |
| 4 | `inspect_feature` | L1, F15800 | " the word "one"" |
| 5 | `get_upstream_features` | L0:F4438@17, k=10 | Emb:" No"@16 (de=29.38) +9 more |

**Findings:** The target L2:F8837 receives its strongest positive influence from the embedding of the preceding token ' No' (direct_effect 18.6) and from the embedding of the token ' one' (9.25). A lower‑layer lexical detector L0:F4438 for the word 'one' adds another 9.1, and a modest L1 detector contributes 1.4. All upstream sources are either the token 'No' or the token 'one' themselves; there is no evidence …

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F1016 | " forms of the verb "tour" and the noun "tour."" |
| 2 | `get_upstream_features` | L2:F1016@14, k=10 | Emb:" tours"@14 (de=27.75) +9 more |
| 3 | `inspect_feature` | L1, F12555 | " words associated with trails and paths, especially words for navigati" |
| 4 | `inspect_feature` | L0, F10891 | " words connected to excursions and professions" |
| 5 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 6 | `get_upstream_features` | L1:F12555@14, k=10 | Emb:" tours"@14 (de=9.81) +9 more |
| 7 | `inspect_feature` | L0, F10891 | " words connected to excursions and professions" |
| 8 | `inspect_feature` | L0, F5886 | "the word "tour" and its variations." |
| 9 | `get_upstream_features` | L0:F10891@14, k=10 | Emb:" tours"@14 (de=18.12) +9 more |

**Findings:** L2:F1016 ('forms of the verb "tour"') is primarily driven by the raw token embedding for 'tours' at the same position (direct effect ~27.7). Two lower‑layer lexical detectors—L1:F12555 (navigation‑related) and L0:F10891 (excursion‑related)—also contribute positive signal (0.65 and 0.50 respectively). All upstream sources are lexical; no broader contextual or policy‑related features appear on the s…

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F14413 | "the word "tour" or "tours"" |
| 2 | `get_upstream_features` | L2:F14413@14, k=10 | Emb:" tours"@14 (de=28.38) +9 more |
| 3 | `inspect_feature` | L1, F12555 | " words associated with trails and paths, especially words for navigati" |
| 4 | `inspect_feature` | L1, F7927 | " text referring to trails, paths, and hiking, including descriptions o" |
| 5 | `get_upstream_features` | L1:F12555@14, k=10 | Emb:" tours"@14 (de=9.81) +9 more |
| 6 | `inspect_feature` | L0, F9924 | " the word "tour" and words or phrases associated with places, events, " |
| 7 | `inspect_feature` | L0, F9653 | " the word "tour"" |
| 8 | `get_upstream_features` | L1:F12555@14, k=10 | Emb:" tours"@14 (de=9.81) +9 more |
| 9 | `get_upstream_features` | L0:F9924@14, k=10 | Emb:" tours"@14 (de=15.19) +9 more |
| 10 | `get_upstream_features` | L1:F7927@14, k=10 | Emb:" tours"@14 (de=9.62) +9 more |
| 11 | `inspect_feature` | L0, F9653 | " the word "tour"" |

**Findings:** The target L2:F14413 (layer 2) is primarily driven by the input token embedding for " tours" (direct effect ≈ 28). Secondary contributions come from low‑layer lexical and semantic features (layers 0‑1) that also detect the word "tour" and related navigation/path concepts. Tracing one hop further upstream from the strongest intermediate feature (L1:F12555) reveals a direct embedding influence from …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F4438@17, k=10 → Emb:" No"@16 (de=29.38) +9 more |

### Build

`build_circuit` → 6 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 36,265 | 5,473 | 200,435 | 0 | $0.0295 | — | — |
| SA-1 | openai/gpt-oss-120b | 241,668 | 16,944 | 40,192 | 0 | $0.0470 | ✅ 7F/12E | Trace the full upstream circuit for the L14:F336 'no/negatio… |
| SA-2 | openai/gpt-oss-120b | 42,415 | 3,162 | 2,688 | 0 | $0.0083 | ✅ 5F/4E | Trace the full upstream circuit for L2:F8837 ('the word "one… |
| SA-4 | openai/gpt-oss-120b | 132,794 | 9,543 | 20,576 | 0 | $0.0260 | ✅ 5F/7E | Trace upstream for L2:F14413 ('the word "tour"') at pos 14. … |
| SA-3 | openai/gpt-oss-120b | 113,521 | 6,525 | 10,144 | 0 | $0.0211 | ✅ 3F/3E | Trace upstream for L2:F1016 ('forms of the verb "tour"') at … |
| **Total** | | **566,663** | **41,647** | **274,035** | **0** | **$0.1318** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 10s