# Circuit Oracle Report
**Date:** 2026-07-28 07:11:56 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This is a contradiction-detection probe whose score is driven primarily by a single dedicated "negation-word" feature pathway (the token **" not"** at position 17, via a stack of L0→L3→L4→L5→L14→L15→L16 negation features) rather than by representations of the actual content words "recorded"/"menu".

**Confidence:** 8

**Reasoning:** Tracing the top features shows a clear split between content and negation pathways:

- **Negation pathway (primary signal).** L16:F6800 (label: *"negations 'not', 'no', and contractions with 't'"*, direct_effect +0.44) feeds the output. Its subagent trace shows it is fed by L15:F11794 (disagreement/negation phrases, de=6.03) → L14:F6648 (speculative/negating language, de=3.77) → L5:F3553, L4:F4492 (multi-lingual negation, de≈1.1–1.3) → L3:F3534 ("n't" contraction, de=2.6) → L0:F4958 (the word "not", activation 27.9, de=2.56). Critically, L0:F4958 is directly driven by the `Emb: ' not' (pos 17)` node with direct_effect 33.5 — a single lexical token, not any semantic content.

- **Content pathway (secondary/balanced).** L1:F3691 ("recording in scientific documentation", +0.82) is driven by `Emb: ' recorded' (pos 2)` (de 24.75) and is opposed by L1:F12253 ("the word 'menu'", de −0.47) which is driven by `Emb: ' menu' (pos 3)` (de 25.75). L2:F8776 is also driven by `Emb: ' recorded'` (de 19.5). These features are essentially lexical detectors for "recorded" and "menu" with opposing signs — they barely constitute semantic understanding; they're a shallow lexical match.

The user's concern is validated. The probe's classification is **not** driven by an integrated semantic representation of the sentence's content. Instead, the dominant late-layer signal is a pure **negation-word detector** triggered by the single token " not" in "do not provide". The opposing +/- signals on "recorded" vs "menu" at L1-L2 are similarly shallow lexical token-detectors, not comprehension. Both classes of features (negation tokens and individual content-word detectors) are the kind of "spurious shortcut" features the user described — the probe latches onto surface markers (negation words and a few content words) rather than reasoning about the contradiction between the two sentences. The `recorded`↔`menu` opposition is structurally present but weak (fractions of the direct_effect budget of the negation pipeline) and operates at a layer where no composition has happened.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: ' not' (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' recorded' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' menu' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Lexical content detectors (L0) | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | Lexical content detectors (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | Lexical content detectors (L0) | the word "menu" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | Lexical content detectors (L1-L2) | the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L1:F12253](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) | 3 | Lexical content detectors (L1-L2) |  the word 'menu' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | Lexical content detectors (L1-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 17 | Negation/abstraction pipeline (L3-L5) | the character sequence "n't" or "nut" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Negation/abstraction pipeline (L3-L5) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L5:F3553](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3553) | 17 | Negation/abstraction pipeline (L3-L5) | words suggesting that the world is working out as it should | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3553) |
| [L14:F6648](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) | 17 | Mid-layer negation/speculation features (L14-L15) | words and phrases that indicate speculation, possibility, or negation regarding facts, rules, or causality. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 17 | Mid-layer negation/speculation features (L14-L15) | phrases that express disagreement or negation | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 17 | High-level negation gate (L16) |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L1:3691 de=0.824 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F3691@2` | ✅ reported | 3 | 4 | Trace this feature upstream. It has the largest positive direct effect (0.82) on… |
| SA-2 | `L2:F8776@2` | ❌ error | — | — | Trace this feature upstream. It has a large positive direct effect (0.64) on the… |
| SA-3 | `L16:F6800@17` | ✅ reported | 6 | 7 | Trace this feature upstream. It's a late-layer (L16) feature with positive direc… |
| SA-4 | `L0:F2108@3` | ❌ error | — | — | Trace this feature upstream. It has the largest negative direct effect (-0.63) o… |
| SA-5 | `L0:F4958@17` | ❌ error | — | — | Trace this feature upstream. It's a positive (0.43) feature at position 17 ("tim… |

<details>
<summary><b>SA-1</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F3691 | " the word "recording" in scientific or experimental documentation" |
| 2 | `get_upstream_features` | L1:F3691@2, k=10 | Emb:" recorded"@2 (de=24.75) +9 more |
| 3 | `inspect_feature` | L0, F7404 | " the word "faith", sometimes in association with related ideas like "l" |
| 4 | `inspect_feature` | L0, F13938 | "the word "wild"" |

**Findings:** The primary upstream driver of L1:F3691 is the embedding for the token "recorded" (direct_effect 24.75), confirming that this feature is a straightforward content detector for the word "recording"/"recorded". Additional weaker upstream contributions come from the BOS token and two layer‑0 lexical detectors ("faith" and "wild"), none of which encode negation, contradiction, or refusal. Consequently…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F6800 | " negations "not", "no", and contractions with "t". " |
| 2 | `get_upstream_features` | L16:F6800@17, k=10 | Emb:" not"@17 (de=11.81) +9 more |
| 3 | `inspect_feature` | L15, F11794 | " phrases that express disagreement or negation" |
| 4 | `inspect_feature` | L3, F3534 | "the character sequence "n't" or "nut"" |
| 5 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 6 | `get_upstream_features` | L3:F3534@17, k=10 | Emb:" not"@17 (de=16.12) +9 more |
| 7 | `get_upstream_features` | L15:F11794@17, k=10 | L14:F6648 (de=3.77) +9 more |
| 8 | `inspect_feature` | L14, F6648 | " words and phrases that indicate speculation, possibility, or negation" |
| 9 | `get_upstream_features` | L14:F6648@17, k=10 | Emb:" not"@17 (de=6.88) +9 more |
| 10 | `inspect_feature` | L5, F3553 | "words suggesting that the world is working out as it should" |

**Findings:** The target L16:F6800 is a high‑level negation detector. Its strongest excitatory input comes directly from the raw " not" token embedding (pos 17) and from lower‑layer negation‑related features. The main causal chain traced is: embedding " not" (layer 0) → L0:4958 (word "not") → L15:11794 (phrase‑level disagreement/negation) → L16:6800 (final negation gate). Intermediate contributors include L14:6…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F8776@2, k=10 → Emb:" recorded"@2 (de=19.50) +9 more |
| 2 | `get_upstream_features` | L0:F2108@3, k=10 → Emb:" menu"@3 (de=25.75) +9 more |
| 3 | `get_upstream_features` | L0:F4958@17, k=10 → Emb:" not"@17 (de=33.50) +9 more |
| 4 | `get_upstream_features` | L0:F7443@2, k=10 → Emb:" recorded"@2 (de=22.62) +9 more |
| 5 | `inspect_feature` ×3 | L1:12253, L0:2108, L4:4492 |

### Build

`build_circuit` → 9 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 12,552 | 3,161 | 49,638 | 0 | $0.0105 | — | — |
| SA-1 | openai/gpt-oss-120b | 22,433 | 2,317 | 10,112 | 0 | $0.0049 | ✅ 3F/4E | Trace this feature upstream. It has the largest positive dir… |
| SA-3 | openai/gpt-oss-120b | 121,998 | 10,432 | 15,584 | 0 | $0.0248 | ✅ 6F/7E | Trace this feature upstream. It's a late-layer (L16) feature… |
| **Total** | | **156,983** | **15,910** | **75,334** | **0** | **$0.0402** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 10s