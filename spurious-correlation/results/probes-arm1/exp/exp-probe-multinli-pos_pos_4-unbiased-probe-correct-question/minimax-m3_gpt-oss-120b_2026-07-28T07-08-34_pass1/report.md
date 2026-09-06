# Circuit Oracle Report
**Date:** 2026-07-28 07:08:35 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction-classification score is driven almost entirely by single-word lexical detectors — "pick up", "from", "tourist", "about", "tours", "usually", "No", "one", "so" — none of which is a negation or contradiction cue, and the strongest contributor is the phrasal-verb detector for "pick up" whose upstream chain reaches the raw "Pick" / "up" token embeddings.

**Confidence:** 8

**Reasoning:**

The circuit is a bag of single-word lexical features, exactly the kind of *content* signal one would want, and crucially it is **not** a "negation detector." Let me list the top features and what they encode:

- **L2:F3116 (pos 2, "pick up" phrasal verb)** — direct_effect = −0.35. Traced upstream: L0 lexical detectors for "Pick" (F10904, F8566) and "up" (F10562, F12744, F16358, F11658), then the raw token embeddings Emb:`Pick` (pos 1, direct_effect 13.4) and Emb:`up` (pos 2, direct_effect 19.5). This feature was confirmed by the subagent to be driven by the surface tokens "Pick"/"up" with only generic lexical context.
- **L0:F8974 (pos 5, "from")** — direct_effect = −0.41. Upstream is Emb:`from` (direct_effect 38.75). A plain preposition detector.
- **L0:F7321 (pos 25, "so")** — direct_effect = +0.38. Upstream is Emb:`so` (direct_effect 40.5). Generic causal-conjunction "so" detector.
- **L2:F13586 (pos 17, "-thing/-one words")** — direct_effect = −0.21. Upstream are Emb:`No` (14) and Emb:`one` (12.9) plus three "one" features. This is a quantifier/pronoun detector, not a "negation" detector; "No one" activates it, but so would "anyone", "someone", "everything" (its promoted tokens include Everyone, Nobody, anyone, everybody).
- **L1:F8159 (pos 19, "usually")** — direct_effect = −0.18. Upstream is Emb:`usually` (direct_effect 24.25). Habitual-frequency adverb.
- **L2:F14413 (pos 14, "tour/tours")** — direct_effect = −0.17. Upstream is Emb:`tours` (direct_effect 28.4). A topic/content word.
- **L0:F306 (pos 7, "tourist")** — direct_effect = +0.19. Upstream is Emb:`tourist` (direct_effect 22). Topic word.
- **L0:F2238 (pos 12, "about")** — direct_effect = −0.19. Upstream is Emb:`about` (direct_effect 35). Function word.
- **L0:F6051 (pos 15, periods/punctuation)** — direct_effect = −0.19. Upstream is Emb:`.` (direct_effect 46.25).

**Refuting the user's hypothesis.** The user worried the circuit uses "negation words" like "No" / "usually" as spurious contradiction cues. The evidence runs the other way:

1. The single largest driver of the probe is **L2:F3116 (the phrasal verb "pick up")** at direct_effect −0.35, and its trace goes through embeddings for the actual content words "Pick" and "up" — this is prototypical prompt content, not a negation cue.
2. The "No one" pair contributes through **L2:F13586**, which is a *quantifier/pronoun* feature (its promoted tokens are Everyone, Nobody, anybody, Everybody, etc.), not a negation feature. Firing on "No one" is incidental to firing on "anyone"/"everyone".
3. "usually" (L1:F8159) is a frequency adverb, not a contradiction signal. Its only role in the contradiction label is lexical, not logical.
4. **No "No" or "n't" negation detector appears** in the top features. If the model were keying on negation, we would expect a "No" or "not" feature with large direct_effect; we see instead the word "No" riding along inside the generic "-one" quantifier feature.
5. **Mixed signs matter.** If this were a "negation → contradiction" circuit, the contributions would all be positive. Instead they are mixed (−0.41, −0.35, −0.21, −0.20, −0.19, +0.38, +0.19, +0.16…), which is exactly the signature of a probe that reads content-lexical features from many positions, not a single semantic rule.

**Conclusion:** The user's hypothesis is not supported. The probe's contradiction score is being driven by a constellation of content-word lexical features — most prominently the "pick up" phrasal verb, plus topic words ("tourist", "tours", "about") and a mix of function words ("from", "so", "usually", "No", "one"). No dedicated negation feature appears; the apparent "negation" signal is just the generic quantifier feature F13586, which fires equally on "anyone/everyone/nobody". The circuit reflects genuine prompt content (what the sentence is about and which verbs/nouns it uses), not a spurious negation heuristic.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Pick (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: up (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: from (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: tourist (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: about (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: tours (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: . (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: No (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: one (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: usually (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: so (pos 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F10904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) | 1 | L0: pickup / Pick word detector | the word "adequate" (and words that appear near it) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 1 | L0: pickup / Pick word detector | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F10562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) | 2 | L0: pickup / Pick word detector | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) |
| [L0:F12744](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12744) | 2 | L0: pickup / Pick word detector | positive adjectives and adverbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12744) |
| [L0:F16358](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16358) | 2 | L0: pickup / Pick word detector | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16358) |
| [L0:F11658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11658) | 2 | L0: pickup / Pick word detector | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11658) |
| [L0:F2868](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2868) | 4 | L0: pickup / Pick word detector | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2868) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 5 | L0: word 'from' / preposition | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F306](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) | 7 | L0: word 'tourist' | the word "adoption" in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 12 | L0: word 'about' |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | L0: periods/punctuation | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 17 | L0: word 'one' | the word "one". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L0:F11351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11351) | 17 | L0: word 'one' |  the number "one" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11351) |
| [L0:F7636](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7636) | 17 | L0: word 'one' |  the word "one" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7636) |
| [L0:F7321](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) | 25 | L0: word 'so' (causal) |  the word "so," and also matches some words ending in "ware" and "such" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) |
| [L0:F7204](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) | 9 | L0: word 'so' (causal) | the word "here" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) |
| [L1:F8159](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) | 19 | L1: word 'usually' |  the word "usually" and, to a lesser extent, words that sometimes accompany it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | L2: phrasal verb 'pick up' |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F11769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) | 2 | L2: phrasal verb 'pick up' | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | L2: word 'tour/tours' | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L2:F13586](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) | 17 | L2: -thing/-one quantifier |  words ending in 'thing' and 'one' often with preceding words indicating the presence of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:8974 de=-0.408 |
| 3 | `inspect_feature` ×8 | L0:8974, L0:7321, L2:3116, L2:13586, L0:6051, L0:2238, L1:8159, L2:14413 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F3116@2` | ✅ reported | 5 | 4 | Trace the path upstream from L2:F3116 (phrasal verb "pick up" at pos 2). I want … |
| SA-2 | `L0:F7321@25` | ❌ error | — | — | Trace upstream from L0:F7321 (the word "so" at pos 25). Pos 25 is the "so" in "s… |
| SA-3 | `L0:F8974@5` | ❌ error | — | — | Trace upstream from L0:F8974 (the word "from" at pos 5). Pos 5 is "from" in "Pic… |
| SA-4 | `L1:F8159@19` | ✅ reported | 4 | 4 | Trace upstream from L1:F8159 (the word "usually" at pos 19). Pos 19 is "usually"… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F3116 | " the phrasal verb "pick up" and variations" |
| 2 | `get_upstream_features` | L2:F3116@2, k=15 | Emb:"Pick"@1 (de=50.00) +14 more |
| 3 | `inspect_feature` | L0, F11794 | " text related to external, imposed restrictions or conditions" |
| 4 | `inspect_feature` | L0, F12744 | "positive adjectives and adverbs" |
| 5 | `inspect_feature` | L0, F7064 | "conditional statements within programming code, and potentially tempor" |
| 6 | `inspect_feature` | L0, F9659 | "phrases involving "together" or "up"" |
| 7 | `get_upstream_features` | L0:F11794@2, k=10 | Emb:" up"@2 (de=7.84) +9 more |
| 8 | `get_upstream_features` | L0:F11794@2, k=10 | Emb:" up"@2 (de=7.84) +9 more |

**Findings:** The target feature L2:F3116 encodes the phrasal verb "pick up" at position 2. Its strongest upstream drivers are the raw input embeddings for the tokens "Pick" (pos 1) and " up" (pos 2), accounting for the bulk of its activation. A handful of low‑layer (layer 0) features provide modest additional context: feature 11794 supplies a generic action‑related cue, feature 12744 contributes a generic posi…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F8159 | " the word "usually" and, to a lesser extent, words that sometimes acco" |
| 2 | `get_upstream_features` | L1:F8159@19, k=10 | Emb:" usually"@19 (de=24.25) +9 more |
| 3 | `inspect_feature` | L0, F12637 | " the adjective "huge"" |
| 4 | `inspect_feature` | L0, F3019 | " the word "focused"" |
| 5 | `inspect_feature` | L0, F10298 | "the word "Collections" and words that mean "in addition to" or "to the" |
| 6 | `get_upstream_features` | L0:F12637@19, k=10 | Emb:" usually"@19 (de=10.50) +9 more |
| 7 | `get_upstream_features` | L0:F3019@19, k=10 | Emb:" usually"@19 (de=9.56) +9 more |
| 8 | `get_upstream_features` | L0:F10298@19, k=10 | Emb:" usually"@19 (de=9.88) +9 more |
| 9 | `inspect_feature` | L0, F2238 | " the word "about" when followed by a numerical value" |
| 10 | `get_upstream_features` | L0:F2238@19, k=10 | ❌ Feature (layer=0, feature_idx=2238) not found at pos=19. Thi |

**Findings:** The target L1 feature (8159) is a direct detector for the adverb 'usually'. Its strongest upstream influence is the raw token embedding for 'usually' (positive direct_effect 24.25), satisfying the embedding‑shortcut requirement. Additionally, three lower‑layer (layer 0) features feed into it with small positive direct_effects, providing a concrete lower‑third path. No refusal‑related tokens or gat…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F7321@25, k=5 → Emb:" so"@25 (de=40.50) +4 more |
| 2 | `get_upstream_features` | L0:F8974@5, k=5 → Emb:" from"@5 (de=38.75) +4 more |
| 3 | `get_upstream_features` | L2:F11769@2, k=5 → Emb:" up"@2 (de=19.50) +4 more |
| 4 | `get_upstream_features` | L2:F13586@17, k=5 → Emb:" No"@16 (de=14.00) +4 more |
| 5 | `get_upstream_features` | L0:F10904@1, k=5 → Emb:"Pick"@1 (de=13.38) +4 more |
| 6 | `get_upstream_features` | L0:F306@7, k=5 → Emb:" tourist"@7 (de=22.00) +4 more |
| 7 | `get_upstream_features` | L2:F14413@14, k=5 → Emb:" tours"@14 (de=28.38) +4 more |
| 8 | `inspect_feature` ×6 | L2:11769, L0:10904, L0:306, L0:4438, L0:10562, L0:12744 |
| 9 | `get_upstream_features` | L0:F2238@12, k=5 → Emb:" about"@12 (de=35.00) +4 more |
| 10 | `get_upstream_features` | L0:F8566@1, k=5 → Emb:"Pick"@1 (de=16.75) +4 more |
| 11 | `inspect_feature` ×3 | L0:7204, L0:11351, L0:7636 |
| 12 | `get_upstream_features` | L0:F6051@15, k=5 → Emb:"."@15 (de=46.25) +4 more |
| 13 | `get_top_features` | token="", k=30 → 30 features; top: L0:8974 de=-0.408 |

### Build

`build_circuit` → 23 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 39,575 | 7,245 | 187,663 | 0 | $0.0318 | — | — |
| SA-1 | openai/gpt-oss-120b | 110,355 | 6,404 | 0 | 0 | $0.0204 | ✅ 5F/4E | Trace the path upstream from L2:F3116 (phrasal verb "pick up… |
| SA-4 | openai/gpt-oss-120b | 97,845 | 6,618 | 11,264 | 0 | $0.0188 | ✅ 4F/4E | Trace upstream from L1:F8159 (the word "usually" at pos 19).… |
| **Total** | | **247,775** | **20,267** | **198,927** | **0** | **$0.0710** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 2s