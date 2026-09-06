# Circuit Oracle Report
**Date:** 2026-07-28 07:19:02 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "toxic / identity-group" classification is driven almost entirely by shallow lexical features that fire on the four identity/slang tokens "white", "black", "dude", and "Another" — not by any semantic understanding of the sentence as an insult. The circuit is a bag of word-presence detectors, not a coherent meaning circuit.

**Confidence:** 8

**Reasoning:** Every top-10 direct-effect feature in the attribution graph is a low-layer (L0–L6) keyword detector anchored directly to a specific input token embedding:

- **L0:F3436 (direct_effect +0.289, frac_nonzero 0.061)** — a "white" word detector, top-activating on tokens like "white" in race-relations text. Receives +17.9 from the **" white" embedding at pos 2** (`get_upstream_features`). Sibling **L0:F10910** (frac 0.015) also keys on "white" and feeds the deeper **L4:F15204** ("art galleries, museums, White House"), which is the "white"-as-cultural-institution reading, not a toxicity signal.
- **L4:F7136 (−0.190)** — a "color white" detector, fed by the **" white" embedding (+46.3 direct_effect)** and the generic **L2:F1708** color-mention detector (promotes "Black", "Blue", "Red", "White"). This is a literal color feature with no toxicity content.
- **L6:F4008 (+0.143)** — a "profanity / strong opinions / expletives" detector, but its only direct upstream is the **" dude" embedding (+10.6)** plus the generic **L2:F9909** "guys/dudes/people" feature. The insulting verbs ("stealing", "thunder") and the slur-free noun phrases are not in its upstream chain at all.
- **L0:F1015 (+0.116, on "black" at pos 6)** — a "black" word detector (frac 0.007), driven by the **" black" embedding (+23.9)**. Feeds the **L3:F13061** "race / gender / social-issues words" feature (+0.122), whose top activating examples are about Black-vs-white wage gaps and Trump-era coverage — i.e., it is a topic detector for race/identity discussion, not a toxicity detector. The suppressors for F13061 are noise (programming tokens), and its promoted tokens are equally generic.
- **L0:F4090 (−0.273) / L2:F2850 (−0.121)** — "another" word detectors (frac ~0.01–0.02), driven by the **"Another" embedding (+32.8)**. They push against the probe — "another" is a benign connective, so this is roughly neutral noise.

The signal flow is therefore: identity/slang token embeddings → single-word lexical features (L0–L2) → mid-layer category features (L3–L6) that label the topic as "race discourse" or "informal profanity" → probe output. The actual hateful content of the sentence ("stealing the … man's thunder") is not represented anywhere in the top 10 — there is no feature for "stealing", "thunder", "appreciation", or "credit-taking". The probe fires because the input *mentions racial groups in an informal register*; it would fire just as strongly on "Another white scientist publishing groundbreaking work on black history".

This is exactly the "spurious identity-group signal" pattern the user suspected: the circuit is **lexical and topic-level, not semantic**. The L0 features have very low frac_nonzero (0.007–0.061), so they are highly specific to particular words, but the *words* they detect are identity terms, and the downstream features (L3:F13061 "race/social-issues", L6:F4008 "profanity/slang") aggregate those tokens into a coarse "identity-discussed + casual register" topic representation that the probe reads as toxic. No feature in the circuit encodes intent, comparison structure, or the verb of theft — the mechanism is a bag of identity-token detectors, confirming the user's hypothesis.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 2 | L0: lexical "white" detector (F3436, F10910) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 2 | L0: lexical "white" detector (F3436, F10910) | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L0:F4090](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) | 1 | L0: lexical "another" detector (F4090, F2850) | the word "another" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) |
| [L2:F2850](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2850) | 1 | L0: lexical "another" detector (F4090, F2850) | the word "another" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2850) |
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 6 | L0: lexical "black" detector (F1015) |  the word "black" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 2 | L2: color mention detector (F1708) | mentions of colors | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 7 | L3: race/gender/social-issues words (F13061) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 2 | L4: "white" cultural-institution detector (F15204) |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L4:F7136](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) | 2 | L4: "color white" detector (F7136) | the color white | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) |
| [L5:F10172](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10172) | 3 | L5: ethnic-slur / Southern American vocabulary (F10172) | ethnic slurs and terms related to the American South | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10172) |
| [L5:F14851](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14851) | 3 | L5: ethnic-slur / Southern American vocabulary (F10172) | slang terms and phrases used in rap music | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14851) |
| [L2:F9909](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9909) | 3 | L2: informal group descriptors (F9909) | terms used to describe groups of people or places | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9909) |
| [L6:F4008](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4008) | 3 | L6: profanity / strong-opinion / slang detector (F4008) | expletives, strong opinions and negative words | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4008) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '1' is not one of the top-k next-token candidates capt |
| 3 | `get_top_features` | 10 features; top: L0:3436 de=0.289 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F3436@2` | ❌ error | — | — | Trace this L0 feature. What does it detect? Look at top activating examples and … |
| SA-2 | `L0:F4090@1` | ❌ error | — | — | Trace this L0 feature (negative direct_effect). What does it detect? |
| SA-3 | `L4:F15204@2` | ✅ reported | 3 | 3 | Trace this L4 feature. What does it detect? Look at top activating examples. |
| SA-4 | `L4:F7136@2` | ✅ reported | 3 | 3 | Trace this L4 feature (negative direct_effect). What does it detect? |
| SA-5 | `L6:F4008@3` | ✅ reported | 6 | 9 | Trace this L6 feature. What does it detect? |

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15204 | " art galleries, museums and the White House" |
| 2 | `get_upstream_features` | L4:F15204@2, k=10 | Emb:" white"@2 (de=43.50) +9 more |
| 3 | `get_upstream_features` | L0:F10910@2, k=10 | Emb:" white"@2 (de=14.31) +9 more |
| 4 | `inspect_feature` | L0, F10910 | "the word "possession" and the words "white", "immediate" and "once" re" |
| 5 | `inspect_feature` | L0, F3436 | " mentions of the word "white"" |
| 6 | `get_upstream_features` | L0:F3436@2, k=5 | Emb:" white"@2 (de=17.88) +4 more |
| 7 | `inspect_feature` | L0, F3241 | " contexts related to "agreement", especially in a collaborative or pol" |
| 8 | `get_upstream_features` | L0:F10910@2, k=10 | Emb:" white"@2 (de=14.31) +9 more |

**Findings:** The target L4 feature (F15204) is primarily driven by the literal token 'white' at position 2, as shown by a strong positive embedding edge (direct_effect 43.5). Upstream, a layer‑0 lexical detector (F10910) that specializes in the word 'white' (and related keywords) also contributes positively, and a generic agreement‑context detector (F3241) adds a minor bias. All upstream paths satisfy the term…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F7136 | " the color white" |
| 2 | `get_upstream_features` | L4:F7136@2, k=10 | Emb:" white"@2 (de=46.25) +9 more |
| 3 | `inspect_feature` | L2, F1708 | " mentions of colors" |
| 4 | `get_upstream_features` | L2:F1708@2, k=10 | Emb:" white"@2 (de=18.38) +9 more |
| 5 | `inspect_feature` | L2, F11363 | " colors and words like Diamond." |
| 6 | `get_top_logits` | k=5 | "" (100%) |

**Findings:** The L4:F7136 feature is a color‑specific detector for the word 'white'. It receives its strongest excitation directly from the embedding of the token 'white' (positive direct_effect >46) and also through an intermediate L2 feature that signals any color mention (positive direct_effect ~2.4). Both upstream nodes are in low layers (≤8), satisfying the lower‑third floor condition, and the path includ…

</details>

<details>
<summary><b>SA-5</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F4008 | " expletives, strong opinions and negative words" |
| 2 | `get_upstream_features` | L6:F4008@3, k=10 | Emb:" dude"@3 (de=10.56) +9 more |
| 3 | `inspect_feature` | L2, F9909 | " terms used to describe groups of people or places" |
| 4 | `get_upstream_features` | L2:F9909@3, k=10 | Emb:" dude"@3 (de=12.56) +9 more |
| 5 | `inspect_feature` | L5, F10172 | " ethnic slurs and terms related to the American South" |
| 6 | `get_upstream_features` | L5:F10172@3, k=10 | Emb:" white"@2 (de=3.12) +9 more |
| 7 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 8 | `inspect_feature` | L5, F14851 | "slang terms and phrases used in rap music" |
| 9 | `inspect_feature` | L1, F9058 | " various slang and strong language." |
| 10 | `get_upstream_features` | L1:F9058@3, k=10 | Emb:" dude"@3 (de=8.31) +9 more |

**Findings:** The L6:F4008 feature is a high‑level profanity and strong‑opinion detector. Its strongest upstream driver is the token embedding for "dude" (a slang term), and deeper upstream it receives input from lower‑layer features that detect informal group descriptors (L2:9909), ethnic slurs and Southern terminology (L5:10172), race/gender/social‑issue language (L3:13061), rap‑style slang (L5:14851), and a …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L0:3436, L0:4090, L0:13663, L3:13061, L2:2850, L0:1015 |
| 2 | `get_upstream_features` | L0:F3436@2, k=5 → Emb:" white"@2 (de=17.88) +4 more |
| 3 | `get_upstream_features` | L0:F4090@1, k=5 → Emb:"Another"@1 (de=32.75) +4 more |
| 4 | `get_upstream_features` | L6:F4008@3, k=5 → Emb:" dude"@3 (de=10.56) +4 more |
| 5 | `get_upstream_features` | L3:F13061@7, k=5 → Emb:" black"@6 (de=15.69) +4 more |
| 6 | `get_upstream_features` | L0:F1015@6, k=5 → Emb:" black"@6 (de=23.88) +4 more |
| 7 | `inspect_feature` | L0, F10910 → "the word "possession" and the words "white", "immediate" and "once" re" |

### Build

`build_circuit` → 15 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 22,990 | 4,150 | 60,652 | 0 | $0.0155 | — | — |
| SA-4 | openai/gpt-oss-120b | 46,909 | 3,195 | 7,680 | 0 | $0.0091 | ✅ 3F/3E | Trace this L4 feature (negative direct_effect). What does it… |
| SA-3 | openai/gpt-oss-120b | 65,641 | 5,141 | 10,176 | 0 | $0.0131 | ✅ 3F/3E | Trace this L4 feature. What does it detect? Look at top acti… |
| SA-5 | openai/gpt-oss-120b | 128,571 | 9,404 | 7,584 | 0 | $0.0250 | ✅ 6F/9E | Trace this L6 feature. What does it detect? |
| **Total** | | **264,111** | **21,890** | **86,092** | **0** | **$0.0627** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 45s