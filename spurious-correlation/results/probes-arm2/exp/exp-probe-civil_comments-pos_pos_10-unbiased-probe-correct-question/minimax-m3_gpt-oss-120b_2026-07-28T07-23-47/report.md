# Circuit Oracle Report
**Date:** 2026-07-28 07:23:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by a sparse, surface-level circuit that fires almost entirely on individual content-word tokens (especially "race", "By", "question", "mentioning", "not") rather than on any integrated representation of the sentence's meaning or its social/racial context.

**Confidence:** 4

**Reasoning:** Of the 20 top features feeding the probe direction, the largest direct effects are shallow L0–L2 embedding-gated features whose upstream traces terminate at raw token embeddings: L0:F10682 at pos 5 traces directly to **Emb: "race"** (de=+0.145), L0:F3820 at pos 4 to **Emb: "the"** next to "mentioning" (de=+0.083), L0:F4958 and L2:F2713 at pos 2 to **Emb: "not"** (de=+0.146 combined), and L3:F12410 at pos 1 to **Emb: "By"** (de=+0.129). A second cluster of L2–L4 features (F11639, F6539, F11194, F15173, F2668) at pos 2–3 builds a "not mentioning" bigram detector with combined direct effects of roughly +0.45. L3:F672 at pos 10 fires on **Emb: "question"** (de=+0.105). 

Critically, the tokens that actually carry the *content* of the prompt — "black", "cops", "white", "helpless", "force" — do **not** appear anywhere in the circuit. The features that *do* appear (the function words "By"/"not"/"the"/"question", and the single identity-adjacent content word "race") are exactly the kind of shallow lexical cues a linear probe would latch onto when its classification boundary is being driven by surface features rather than semantic content. 

The user's concern is partially but not fully supported: the circuit is dominated by generic function-word embeddings and the literal token "race" (pos 5), which is a legitimate identity-group signal. However, "race" is the only identity-bearing token; the rest are syntactically general ("By", "not", "the", "question", "mentioning"). So the mechanism is better described as **shallow lexical/bag-of-words** rather than a coherent "identity-group" circuit — the probe appears to be using mostly irrelevant surface tokens as its cue. The lack of any deep integration (no L5+ features, no convergent entity-recognition supernode, no semantic composition) reinforces this: the toxicity score is being read off individual word embeddings that happen to be activated by this prompt, not off a genuine understanding of the content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F10682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) | 5 | Emb: race (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 4 | Emb: mentioning (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 2 | Emb: not (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L2:F2713](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2713) | 2 | Emb: not (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2713) |
| [L3:F12410](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) | 1 | Emb: By (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) |
| [L3:F672](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) | 10 | Emb: question (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) |
| [L2:F11639](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) | 3 | L2-L3 features on 'mentioning/not' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) |
| [L2:F6539](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) | 3 | L2-L3 features on 'mentioning/not' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) |
| [L3:F11194](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11194) | 3 | L2-L3 features on 'mentioning/not' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11194) |
| [L4:F15173](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) | 3 | L2-L3 features on 'mentioning/not' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) |
| [L4:F2668](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) | 3 | L2-L3 features on 'mentioning/not' (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:4958 de=-0.227 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F12410@1` | ❌ error | — | — | Trace upstream from L3:F12410 (pos 1, direct_effect=+0.1289) — what tokens and e… |
| SA-2 | `L4:F15173@3` | ❌ error | — | — | Trace upstream from L4:F15173 (pos 3, direct_effect=+0.1348) — what does this fe… |
| SA-3 | `L2:F11639@3` | ❌ error | — | — | Trace upstream from L2:F11639 (pos 3, direct_effect=+0.1118) — what tokens/featu… |
| SA-4 | `L3:F672@10` | ❌ error | — | — | Trace upstream from L3:F672 (pos 10, direct_effect=+0.105) — what does this feat… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L3:F12410@1, k=10 → Emb:"By"@1 (de=48.75) +9 more |
| 2 | `get_upstream_features` | L4:F15173@3, k=10 → Emb:" mentioning"@3 (de=17.50) +9 more |
| 3 | `get_upstream_features` | L2:F11639@3, k=10 → Emb:" mentioning"@3 (de=27.25) +9 more |
| 4 | `get_upstream_features` | L3:F672@10, k=10 → Emb:" question"@10 (de=38.75) +9 more |
| 5 | `get_upstream_features` | L0:F10682@5, k=5 → Emb:" race"@5 (de=22.62) +4 more |
| 6 | `get_upstream_features` | L0:F3820@4, k=5 → Emb:" the"@4 (de=33.00) +4 more |
| 7 | `get_upstream_features` | L2:F2713@2, k=5 → Emb:" not"@2 (de=20.25) +4 more |
| 8 | `get_upstream_features` | L4:F2668@3, k=5 → Emb:" not"@2 (de=9.50) +4 more |
| 9 | `get_upstream_features` | L2:F6539@3, k=5 → Emb:" mentioning"@3 (de=7.91) +4 more |
| 10 | `get_upstream_features` | L3:F11194@3, k=5 → Emb:" mentioning"@3 (de=16.12) +4 more |
| 11 | `get_upstream_features` | L0:F4958@2, k=5 → Emb:" not"@2 (de=30.12) +4 more |

### Build

`build_circuit` → 7 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 9,610 | 3,061 | 52,602 | 0 | $0.0097 | — | — |
| **Total** | | **9,610** | **3,061** | **52,602** | **0** | **$0.0097** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 51s