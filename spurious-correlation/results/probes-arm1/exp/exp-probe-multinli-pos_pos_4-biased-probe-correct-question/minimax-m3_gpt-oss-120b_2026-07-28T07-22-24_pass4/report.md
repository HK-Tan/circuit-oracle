# Circuit Oracle Report
**Date:** 2026-07-28 07:22:24 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven primarily by a deep "No" / negation feature chain at the "No one" position (pos 16-17), confirmed by surface-level "no" / "one" / "no one" lexical detectors; supporting positive signals come from content words like "map", "pick up", and "tours", while "about" and "here" push the score down.

**Confidence:** 7

**Reasoning:** The attribution graph shows that the dominant signal toward the contradiction probe direction flows through a tight compound of negation detectors anchored at positions 16-17 ("No one is usually..."). At the bottom: Emb:"No" (pos 16, direct_effect=33 into L14:F336) and Emb:"one" (pos 17, direct_effect=15 into L1:F15800) directly drive two early-layer lexical detectors — L0:F1143 ("no" detector, frac_nonzero=0.014, promoted "no/nobody/none/nothing"), L2:F2771 ("no" + conceptual negation), L2:F8837 ("no one" / "nobody" compound), and L0:F4438 ("one" detector, frac_nonzero=0.0011) — which then feed upward into a deep negation chain at the "No" position: L12:F8719 ("phrases that start with no."), L13:F10768 ("negative sentiments and words like 'no'"), L14:F336 ("the word 'no' and related negative words", frac_nonzero=0.0044, the strongest single late feature with direct_effect=+0.183 at the top), L15:F13061 ("uses of 'no' or similar negative statements"), and L16:F11298 (pos 16, direct_effect=+0.175). This is exactly the kind of "negation word → contradiction" shortcut the user is concerned about: the probe is reading the literal surface form "No" at the start of the second sentence as evidence of contradiction, even though semantically "No one is usually at the tourist office" is just an explanation of a normal state of affairs — not a negation of the first sentence. The contradiction here is a real NLI property of the two sentences, but the *mechanism* is largely surface-level: it tracks the presence of the word "No" plus content-word vocabulary from the first sentence ("map", "tourist", "tours", "pick up", "office") rather than computing any deep semantic inconsistency. Pushing AGAINST the contradiction score are L2:F3116 ("pick up" phrasal verb, direct_effect=−0.609 — the single largest magnitude effect, driven by Emb:"Pick" pos 1 with direct_effect=50 and Emb:"up" pos 2 with 20.75), L2:F14413 + L2:F1016 ("tour"/"tours" detectors at pos 14, direct_effect=−0.281 and +0.217), L0:F2238 ("about" at pos 12, direct_effect=−0.215), L4:F10722 ("here" at pos 9, direct_effect=−0.213), and L0:F8566 ("pick" at pos 1, direct_effect=−0.208). Pushing TOWARD contradiction are L0:F10562 ("up", +0.295 — but as an isolated word, not in the "pick up" phrase), L0:F10904 ("adequate", +0.287 — likely co-occurring with the bulk of the sentence), L1:F15800 ("one", +0.248), L2:F1016 ("tour" positive at pos 14, +0.217), L0:F7727 ("map"/"mapping", +0.194), L8:F1872 (diagrams/presentations, +0.178), L16:F11298 (pos 16, +0.175), and L0:F13354 (pos 11, +0.168). The user concern is validated: the circuit is heavily dominated by spurious negation-word features (L0:F1143, L2:F2771, L2:F8837, L12:F8719, L13:F10768, L14:F336, L15:F13061, L16:F11298 — eight separate "no" detectors stacked vertically) and a generic "one" detector, rather than features that encode the semantic relationship between the two sentences. The probe is essentially pattern-matching on "the second sentence starts with 'No' AND mentions content words from the first sentence" — a classic contradiction artifact, not a genuine entailment-contradiction computation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 16 | Deep-layer "no" / negation compound (L12-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 16 | Deep-layer "no" / negation compound (L12-L16) |  uses of the word "no" or similar negative statements and words associated with "one" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 16 | Deep-layer "no" / negation compound (L12-L16) | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L13:F10768](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) | 16 | Deep-layer "no" / negation compound (L12-L16) |  negative sentiments and words like "no" in the context of a discussion or argument. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) |
| [L12:F8719](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) | 16 | Deep-layer "no" / negation compound (L12-L16) |  phrases that start with "no." | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) |
| [L1:F15800](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) | 17 | L1 "one" detector at "one" position 17 |  the word "one" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 17 | L0 "one" detector at pos 17 | the word "one". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L0:F1143](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) | 16 | L0 "no" / negation word detectors at pos 16 |  the word "no" and related words like "nobody" and "trust" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) |
| [L2:F2771](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) | 16 | L0 "no" / negation word detectors at pos 16 |  the word "no" as well as words and phrases that are conceptually related to negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 17 | L0 "no" / negation word detectors at pos 16 |  the word "one" or "body" when preceded by the words "no" or "every." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | "tour/tours" features at pos 14 (suppress contradiction) | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L2:F1016](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) | 14 | "tour/tours" features at pos 14 (suppress contradiction) |  forms of the verb "tour" and the noun "tour." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) |
| [L1:F6872](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6872) | 14 | "tour/tours" features at pos 14 (suppress contradiction) |  the word "interpretation" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6872) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | "pick up" phrasal verb at pos 2 (suppress contradiction) |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 1 | "pick up" phrasal verb at pos 2 (suppress contradiction) |  the word "pick" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F10562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) | 2 | "pick up" phrasal verb at pos 2 (suppress contradiction) | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) |
| [L0:F13092](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13092) | 2 | "pick up" phrasal verb at pos 2 (suppress contradiction) |  the words "down" and "up", often in combination | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13092) |
| [L0:F10904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) | 1 | "pick up" phrasal verb at pos 2 (suppress contradiction) | the word "adequate" (and words that appear near it) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 12 | "about" at pos 12 (suppress contradiction) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L4:F10722](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10722) | 9 | "here" / locative features at pos 9 | uses of the word "here" alongside demonstrative pronouns and temporal words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10722) |
| [L0:F7204](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) | 9 | "here" / locative features at pos 9 | the word "here" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) |
| [L2:F13998](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13998) | 9 | "here" / locative features at pos 9 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13998) |
| [L0:F7727](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7727) | 4 | "map"/mapping feature at pos 4 (positive toward probe) |  code or documentation mentioning the word "mapping." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7727) |
| [L4:F11969](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11969) | 4 | "map"/mapping feature at pos 4 (positive toward probe) |  mentions of printed advertising materials | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11969) |
| [L8:F1872](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/1872) | 4 | "map"/mapping feature at pos 4 (positive toward probe) |  words and phrases related to diagrams and presentations | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/1872) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | "map"/mapping feature at pos 4 (positive toward probe) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F13354](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13354) | 11 | "map"/mapping feature at pos 4 (positive toward probe) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13354) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:3116 de=-0.609 |
| 3 | `inspect_feature` ×8 | L2:3116, L0:10562, L0:10904, L2:14413, L1:15800, L2:1016, L0:2238, L4:10722 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F3116@2` | ❌ error | — | — | Trace L2:F3116 ("pick up" phrasal verb) upstream to find what input token positi… |
| SA-2 | `L2:F14413@14` | ❌ error | — | — | Trace L2:F14413 ("tour/tours" at pos 14) upstream. Find what drives this feature… |
| SA-3 | `L1:F15800@17` | ❌ error | — | — | Trace L1:F15800 ("one" at pos 17) upstream. Find what drives this feature and re… |
| SA-4 | `L0:F2238@12` | ❌ error | — | — | Trace L0:F2238 ("about" at pos 12) upstream. Find what drives this feature and r… |
| SA-5 | `L4:F10722@9` | ❌ error | — | — | Trace L4:F10722 ("here" at pos 9) upstream. Find what drives this feature and re… |
| SA-6 | `L16:F11298@16` | ❌ error | — | — | Trace L16:F11298 (pos 16) upstream. This is a deeper-layer feature (layer 16) th… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F3116@2, k=12 → Emb:"Pick"@1 (de=50.00) +11 more |
| 2 | `get_upstream_features` | L2:F14413@14, k=12 → Emb:" tours"@14 (de=28.38) +11 more |
| 3 | `get_upstream_features` | L1:F15800@17, k=12 → Emb:" one"@17 (de=15.25) +11 more |
| 4 | `get_upstream_features` | L0:F2238@12, k=12 → Emb:" about"@12 (de=35.00) +11 more |
| 5 | `get_upstream_features` | L4:F10722@9, k=12 → Emb:" here"@9 (de=24.12) +11 more |
| 6 | `get_upstream_features` | L16:F11298@16, k=12 → Emb:" No"@16 (de=12.44) +11 more |
| 7 | `get_upstream_features` | L14:F336@16, k=12 → Emb:" No"@16 (de=33.00) +11 more |
| 8 | `get_upstream_features` | L2:F1016@14, k=12 → Emb:" tours"@14 (de=27.75) +11 more |
| 9 | `inspect_feature` ×8 | L15:13061, L12:8719, L13:10768, L0:1143, L0:4438, L2:2771, L0:6051, L0:7204 |
| 10 | `get_upstream_features` | L15:F13061@16, k=10 → Emb:" No"@16 (de=12.50) +9 more |
| 11 | `get_upstream_features` | L2:F13998@9, k=8 → Emb:" here"@9 (de=33.25) +7 more |
| 12 | `inspect_feature` ×4 | L0:7727, L1:6872, L4:11969, L8:1872 |
| 13 | `get_upstream_features` | L14:F336@16, k=10 → Emb:" No"@16 (de=33.00) +9 more |
| 14 | `inspect_feature` | L14, F336 → "the word "no" and related negative words" |
| 15 | `get_upstream_features` | L1:F13179@1, k=8 → Emb:"Pick"@1 (de=21.62) +7 more |
| 16 | `inspect_feature` ×4 | L2:8837, L2:11769, L0:13092, L0:8566 |

### Build

`build_circuit` → 17 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 50,320 | 6,285 | 204,282 | 0 | $0.0349 | — | — |
| **Total** | | **50,320** | **6,285** | **204,282** | **0** | **$0.0349** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 23s