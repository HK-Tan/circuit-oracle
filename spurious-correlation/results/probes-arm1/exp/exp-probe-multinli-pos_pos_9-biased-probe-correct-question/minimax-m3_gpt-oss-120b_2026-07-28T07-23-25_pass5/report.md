# Circuit Oracle Report
**Date:** 2026-07-28 07:23:25 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven almost entirely by a shallow, token-level negation detection circuit that activates on the literal word "not" at position 17 and a separate lexical circuit that activates on "recorded" — neither path involves any semantic comparison between the two sentences.

**Confidence:** 9

**Reasoning:**

The user is right: this circuit is a textbook spurious-feature detector. The dominant signal to the output is **L16:F6800** (direct_effect=+0.4355, activation=22.6), explicitly labeled "negations 'not', 'no', and contractions with 't'" with frac_nonzero=0.031 and max_token="t" on training examples. Tracing upstream at position 17 ("not") reveals a monotone chain of negation detectors, all on the same token:

- **Emb: "not" (pos 17)** → L0:F4958 (lexical "not" detector, direct_effect=33.5) → L3:F3534 ("do not" bigram detector, fed by both "not" and "do" embeddings) → L4:F4492 (multilingual negations: "tak/pas/je") + L5:F3553 → L13:F102 → L14:F6648 → L15:F11794 → L16:F6800 → output.

The chain is exclusively lexical/syntactic — it detects the surface form "not" and propagates it up as a single feature vector. Crucially, **L16:F6800 receives its biggest direct feed from the raw "not" embedding itself (direct_effect=11.8) and from the early L0 "not" detector (direct_effect=2.6)**, bypassing all intermediate semantic processing. There is no path from content words like "provide," "information," "lists," or "menus" into this feature; the "menus" embedding at pos 15 actually *suppresses* it (-1.05). This is a negation-presence detector, not a contradiction-semantics detector.

A second, weaker path is **Emb: "recorded" (pos 2) → L0:F7443 ("record" detector) + L0:F2108 ("menu" detector at pos 3) → L1:F3691 ("recording" feature) → output** (direct_effect=+0.82+0.58+0.64 = ~2.0 net). This path is purely topic-lexical — it fires because the *hypothesis* sentence contains the word "recorded," not because it has been compared to the premise. Note that **L0:F2108 ("menu") and L0:F12253 ("menu") both have negative direct_effects** at pos 3 (-0.625, -0.474), meaning "menu" in the hypothesis *suppresses* the contradiction score — a bizarre signal for genuine entailment reasoning (the premise says menus "will provide information"; the hypothesis says they "do not provide any information" — "menu" content is exactly what should drive contradiction, and here it works against it).

The full prompt encodes a clean NLI contradiction: premise "will provide…information" vs. hypothesis "do not provide any information." A correct circuit would route through (a) premise/hypothesis alignment on "provide information," (b) polarity-flip detection, and (c) the content words "menu/list." Instead, the circuit reads **"not" + "recorded"** and fires. This is the negation-words-are-contradiction heuristic the user flagged: the probe is essentially `contradiction ≈ 1[has "not"] + small_topic_boost[has "recorded"]`, with no actual entailment reasoning.

Confidence is high (9/10) because: (1) the dominant path is fully traced to embeddings and contains zero content-word or alignment features; (2) the single content-word feature present ("menu" at pos 3) suppresses rather than promotes the score; (3) the label of the top feature (L16:F6800) explicitly confirms it is a generic negation detector with 3.1% base rate — the textbook signature of a spurious feature.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 17 | Late-layer 'not/no/'nt' detector (broad negation) |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 17 | Mid-layer 'do not' / 'recorded menus do not' pattern | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L14:F6648](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) | 17 | Sentence-level negation context | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) |
| [L13:F102](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) | 17 | Mid-layer negation feature | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) |
| [L5:F3553](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3553) | 17 | Early-mid 'not' pattern detector | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3553) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Multilingual negations (tak/pas/je/no) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 17 | 'do not' bigram detector | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L1:F3311](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3311) | 17 | Early negation context feature | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3311) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Lexical 'not' detector (position 17) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F9203](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9203) | 17 | Lexical 'do'/'aux' detector (position 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9203) |
| [L0:F8136](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8136) | 17 | Lexical 'do'/'aux' detector (position 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8136) |
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | 'recording' lexical feature (pos 2) |  the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | 'record'/'menu' lexical features (pos 2-3) | the word "record" appearing in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | 'record'/'menu' lexical features (pos 2-3) | the word "menu" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'contradiction' is not one of the top-k next-token can |
| 3 | `get_top_features` | 20 features; top: L1:3691 de=0.824 |
| 4 | `inspect_feature` ×10 | L1:3691, L2:8776, L0:2108, L0:7443, L1:12253, L16:6800, L0:4958, L4:4492, L0:13938, L4:2422 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F6800@17` | ❌ error | — | — | Trace this L16 negation feature ('not', 'no', contractions with 't') upstream to… |
| SA-2 | `L4:F4492@17` | ❌ error | — | — | Trace this L4 multilingual-negation feature upstream. Position 17 is "not" in th… |
| SA-3 | `L1:F3691@2` | ❌ error | — | — | Trace this L1 "recording" feature upstream. Position 2 is "A" in the prompt - wa… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F6800@17, k=15 → Emb:" not"@17 (de=11.81) +14 more |
| 2 | `get_upstream_features` | L0:F4958@17, k=10 → Emb:" not"@17 (de=33.50) +9 more |
| 3 | `get_upstream_features` | L15:F11794@17, k=10 → L14:F6648 (de=3.77) +9 more |
| 4 | `get_upstream_features` | L3:F3534@17, k=10 → Emb:" not"@17 (de=16.12) +9 more |
| 5 | `get_upstream_features` | L13:F102@17, k=10 → Emb:" not"@17 (de=8.31) +9 more |
| 6 | `get_upstream_features` | L1:F3311@17, k=10 → Emb:" do"@16 (de=8.38) +9 more |
| 7 | `get_upstream_features` | L2:F13554@17, k=10 → Emb:" do"@16 (de=7.22) +9 more |
| 8 | `get_upstream_features` | L1:F3691@2, k=10 → Emb:" recorded"@2 (de=24.75) +9 more |
| 9 | `get_upstream_features` | L14:F6648@17, k=10 → Emb:" not"@17 (de=6.88) +9 more |
| 10 | `get_upstream_features` | L5:F3553@17, k=10 → Emb:" not"@17 (de=3.48) +9 more |
| 11 | `get_upstream_features` | L0:F9203@17, k=10 → Emb:" do"@16 (de=14.88) +9 more |
| 12 | `get_upstream_features` | L0:F8136@17, k=10 → Emb:" not"@17 (de=17.62) +9 more |

### Build

`build_circuit` → 17 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 27,808 | 4,692 | 129,614 | 0 | $0.0217 | — | — |
| **Total** | | **27,808** | **4,692** | **129,614** | **0** | **$0.0217** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 5s