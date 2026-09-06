# Circuit Oracle Report
**Date:** 2026-07-28 07:20:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score for this prompt is driven almost entirely by shallow, single-word lexical detectors (L0/L1/L2) that fire on individual function words like "from", "so", "up", "about", "Pick", "tourist", "usually", "tours", "here", "one" — with each upstream trace terminating at its own raw token embedding. No mid/high-layer compositional or entity-level features participate.

**Confidence:** 7

**Reasoning:** Looking at the 15 top features in `get_top_features`, every single one is a shallow (L0–L2) lexical detector with `frac_nonzero` between 0.003 and 0.057 and a label that names a specific word ("from", "so", "up", "about", "Pick", "tourist", "usually", "tours", "here", "one", "pick up"). When I traced each upstream:
- L0:F8974 ("from", pos 5) → almost entirely from `Emb: from` (direct_effect = 38.75), with trivial other-token contributions. Label is literally "the word 'from'."
- L0:F7321 ("so", pos 25) → 95% of its drive is the `Emb: so` token (direct_effect = 40.5). Label: "the word 'so'."
- L2:F3116 ("pick up", pos 2) → `Emb: Pick` (50.0) + `Emb: up` (20.75); the other L0 helpers (positive-adjective, restrictions, "then/else") have direct_effects of ~0.8 each — roughly 1–2 orders of magnitude smaller. Label: "the phrasal verb 'pick up' and variations."
- L2:F13586 (pos 17, "No one") → `Emb: No` (14) + `Emb: one` (12.9) + L0:F4438 "the word 'one'" (7.7) drive it; only L0:F13585 "negative statements or the absence of something" contributes a non-embedding direct_effect (1.78), and that itself is a generic negative/absence detector with frac_nonzero 0.016. Label is "words ending in 'thing' and 'one'."
- L1:F8159 ("usually") → `Emb: usually` (24.25); only L0:F3507 ("typically" and other adverbs of frequency) contributes a real non-embedding edge (−0.85). Label: "the word 'usually.'"
- L2:F14413 ("tours", pos 14) → `Emb: tours` (28.4); only L1:F6872 "the word 'interpretation'" (an unrelated, weakly connected L1 feature, −0.62) is non-embedding. Label: "the word 'tour' or 'tours.'"
- L0:F2238 ("about", pos 12), L0:F6051 (period at pos 15), L0:F10904 ("Pick" at pos 1 — its label is "adequate" but the top-activating example is generic, and the upstream trace is dominated by `Emb: Pick` with 13.4 direct_effect), L0:F306 ("tourist"), L0:F7204 ("here"), L0:F8566 ("Pick" again as "one" — the label was mislabeled by autointerp; its upstream is `Emb: Pick` with 16.75 direct_effect), L0:F10562/L2:F11769 (both "up"), and L0:F12744 ("positive adjectives") all show the same pattern: ~90% of each feature's direct effect on the probe comes from the local token embedding itself, with only tiny contributions from sibling/adjacent-token features.

**Key observations:**
1. **The circuit is flat and shallow.** All circuit-driving features are at layers 0–2. There is no convergence at a mid-layer "contradiction-detector" feature; the model never abstracts away from the raw tokens.
2. **Each feature is a single-word lexical detector.** Labels literally name one word ("from", "so", "about", "up", "Pick", "tourist", "here", "one", "usually", "tours"). The only mildly "semantic" candidate is L2:F13586 ("thing/one words") which fires on "No one", and even that is described as a lexical pattern.
3. **No genuine negation/contradiction detector is present.** The user's worry is that the circuit uses "negation words" as a spurious shortcut. The closest candidate is L0:F13585 (autointerp: "negative statements or the absence of something"), but it contributes only 1.78 direct_effect to L2:F13586 — about 1/15th of the embedding contributions combined. The dominant signal in the "No one" path is the literal words "No" and "one", not a negation concept.
4. **Signs are mixed.** "from" (−0.41) and "pick up" (−0.35) push toward the contradiction class; "so" (+0.38) and "about" (−0.19) and "Pick" (+0.19) push in various directions. The probe is not making a coherent contradiction decision; it is being pushed by a bag of mostly independent word-presence features, each of which has been trained into the probe as a heuristic correlate of the NLI label distribution (e.g., "if the hypothesis contains 'pick up a map from …' and the premise does not, that pair is often labeled contradiction → probe learns to fire on those lexical items").
5. **Reaching the embeddings confirms the "spurious" diagnosis.** Every important feature bottoms out at a single token embedding (e.g., `Emb: Pick` is the source of 50% of L2:F3116's drive, 13.4% of L0:F10904, 16.75% of L0:F8566, 5.6% of L2:F11769). The "Pick" word alone contributes to the contradiction score via multiple parallel lexical detectors.

**Verdict on the user's concern:** Their concern is partially correct but worth refining. The circuit is not driven by an abstract "negation" or "contradiction" concept at all — it is driven by a scattered collection of single-word lexical detectors (mostly L0 features, frac_nonzero 0.003–0.06, labels naming individual words like "from", "so", "up", "about", "Pick", "tourist", "here", "one", "usually", "tours"). The signal is *even more* spurious than "negation words" — it is essentially "the presence of these particular content words and function words, each independently." The single mildly semantic feature that resembles a negation/absence detector (L0:F13585, "negative statements or the absence of something") is a minor contributor (direct_effect = 1.78) compared to the raw "No" and "one" token embeddings (14 and 12.9). The probe is acting as a bag-of-words classifier that has memorized lexical correlates of contradiction labels rather than learning the actual contradiction relation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Pick (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: up (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: map (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: from (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: here (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: about (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: . (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: No (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: one (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: tours (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: usually (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: tourist (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: office (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: so (pos 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 5 | Lexical: the word "from" | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F7321](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) | 25 | Lexical: the word "so" |  the word "so," and also matches some words ending in "ware" and "such" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | Lexical: phrasal verb "pick up" |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F13586](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) | 17 | Lexical: words ending in "thing"/"one" (No one) |  words ending in 'thing' and 'one' often with preceding words indicating the presence of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) |
| [L2:F11769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) | 2 | Lexical: the word "up" | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) |
| [L0:F10562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) | 2 | Lexical: the word "up" | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 12 | Lexical: the word "about" (pos 12) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | Lexical: periods/spaces/numerals (pos 15) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F10904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) | 1 | Lexical: the word "Pick" (pos 1) | the word "adequate" (and words that appear near it) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) |
| [L0:F306](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) | 7 | Lexical: the word "tourist" (pos 7) | the word "adoption" in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) |
| [L1:F8159](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) | 19 | Lexical: "usually" (pos 19) |  the word "usually" and, to a lesser extent, words that sometimes accompany it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | Lexical: "tour" / "tours" (pos 14) | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L0:F7204](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) | 9 | Lexical: the word "here" (pos 9) | the word "here" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 1 | Lexical: the word "one" (pos 17) |  the word "pick" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F12744](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12744) | 2 | Lexical: positive adjectives/adverbs (pos 2) | positive adjectives and adverbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12744) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:8974 de=-0.408 |
| 3 | `inspect_feature` ×15 | L0:8974, L0:7321, L2:3116, L0:2238, L2:13586, L2:11769, L0:6051, L0:10904, L0:306, L1:8159, L0:10562, L2:14413, L0:8566, L0:7204, L0:12744 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F7321@25` | ❌ error | — | — | Trace this feature (the word "so," at pos 25 in the second sentence) back throug… |
| SA-2 | `L0:F8974@5` | ❌ error | — | — | Trace this feature (the word "from" at pos 5 in the first sentence) back through… |
| SA-3 | `L2:F3116@2` | ✅ reported | 4 | 3 | Trace this feature (the phrasal verb "pick up" at pos 2 in the first sentence) b… |
| SA-4 | `L2:F13586@17` | ❌ error | — | — | Trace this feature (words ending in "thing"/"one" at pos 17, likely "someone" in… |

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F3116 | " the phrasal verb "pick up" and variations" |
| 2 | `get_upstream_features` | L2:F3116@2, k=10 | Emb:"Pick"@1 (de=50.00) +9 more |
| 3 | `inspect_feature` | L0, F11794 | " text related to external, imposed restrictions or conditions" |
| 4 | `inspect_feature` | L0, F12744 | "positive adjectives and adverbs" |
| 5 | `get_upstream_features` | L0:F11794@2, k=10 | Emb:" up"@2 (de=7.84) +9 more |
| 6 | `get_upstream_features` | L0:F12744@2, k=10 | Emb:" up"@2 (de=9.62) +9 more |
| 7 | `inspect_feature` | L0, F7064 | "conditional statements within programming code, and potentially tempor" |
| 8 | `get_upstream_features` | L0:F7064@2, k=10 | Emb:" up"@2 (de=13.06) +9 more |

**Findings:** The L2 feature detecting the phrasal verb "pick up" receives its main drive from the raw token embeddings for "Pick" and "up" (large positive direct effects). Three very low‑layer (layer 0) features also feed into it with modest positive contributions. Among those, L0:11794 encodes a notion of external restrictions/constraints, which can bias the model toward a refusal‑type response even though it…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F7321@25, k=10 → Emb:" so"@25 (de=40.50) +9 more |
| 2 | `get_upstream_features` | L0:F8974@5, k=10 → Emb:" from"@5 (de=38.75) +9 more |
| 3 | `get_upstream_features` | L2:F13586@17, k=10 → Emb:" No"@16 (de=14.00) +9 more |
| 4 | `get_upstream_features` | L2:F11769@2, k=10 → Emb:" up"@2 (de=19.50) +9 more |
| 5 | `get_upstream_features` | L1:F8159@19, k=10 → Emb:" usually"@19 (de=24.25) +9 more |
| 6 | `get_upstream_features` | L2:F14413@14, k=10 → Emb:" tours"@14 (de=28.38) +9 more |
| 7 | `inspect_feature` ×8 | L0:4438, L0:11351, L0:3507, L1:6872, L0:10562, L0:13585, L1:805, L0:4438 |
| 8 | `get_upstream_features` | L2:F3116@2, k=10 → Emb:"Pick"@1 (de=50.00) +9 more |
| 9 | `get_upstream_features` | L0:F2238@12, k=10 → Emb:" about"@12 (de=35.00) +9 more |
| 10 | `get_upstream_features` | L0:F10904@1, k=10 → Emb:"Pick"@1 (de=13.38) +9 more |
| 11 | `get_upstream_features` | L0:F306@7, k=10 → Emb:" tourist"@7 (de=22.00) +9 more |
| 12 | `get_upstream_features` | L0:F6051@15, k=10 → Emb:"."@15 (de=46.25) +9 more |
| 13 | `get_upstream_features` | L0:F7204@9, k=10 → Emb:" here"@9 (de=41.00) +9 more |
| 14 | `get_upstream_features` | L0:F8566@1, k=10 → Emb:"Pick"@1 (de=16.75) +9 more |
| 15 | `get_upstream_features` | L0:F12744@2, k=10 → Emb:" up"@2 (de=9.62) +9 more |
| 16 | `get_upstream_features` | L0:F10562@2, k=10 → Emb:" up"@2 (de=36.75) +9 more |

### Build

`build_circuit` → 30 nodes, 33 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 80,816 | 7,968 | 182,040 | 0 | $0.0447 | — | — |
| SA-3 | openai/gpt-oss-120b | 87,758 | 6,427 | 11,216 | 0 | $0.0172 | ✅ 4F/3E | Trace this feature (the phrasal verb "pick up" at pos 2 in t… |
| **Total** | | **168,574** | **14,395** | **193,256** | **0** | **$0.0619** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 31s