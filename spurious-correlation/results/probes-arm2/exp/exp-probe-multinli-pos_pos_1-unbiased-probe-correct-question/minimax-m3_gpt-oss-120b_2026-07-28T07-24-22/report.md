# Circuit Oracle Report
**Date:** 2026-07-28 07:24:22 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's CONTRADICTION score is driven primarily by entity- and content-specific features (Conspiracy/MasterCard/chip/investing) plus the rhetorical "No one thinks" framing, not by generic negation cues.

**Confidence:** 6

**Reasoning:** The circuit's top features all attach to **specific content words** of the prompt rather than abstract negation markers. The strongest positive driver is **L2:F16230 (pos 11, +0.27)** — traced back to the embedding of the literal token **" chip"** (direct_effect 27), with cascading L0 features (F2115, F3937, F351, F1506) all keyed to pos 11. Likewise **L0:F16015 (+0.19)** and **L0:F4287 (+0.17)** at pos 1 trace to the embedding of **"Cons"** (direct_effects 21 and 11), and **L0:F11375 (+0.15)** traces to **" is"** (pos 7, de=31), while **L0:F8444 (+0.13)** traces to **" to"** (pos 24, de=42) and **L1:F8696 (+0.14)** traces to **" investing"** (pos 8, de=22). **L0:F3635 (+0.22)** at pos 12 is the literal **" that"** of the relative clause — a syntactic pivot, not a negation word. On the negative side, the largest suppressor **L3:F9739 (-0.35)** at pos 2 ("piracy") and **L1:F13684 (-0.20)** at pos 3 (" theorists") fire on the conspiracy-noun tokens themselves; **L7:F1062 (-0.24)** at pos 6 (and pos 11) fires on **"Card"** / " chip" embeddings (de=14) — i.e. MasterCard/chip entity features push *against* the contradiction score. Crucially, the prompt's actual negation cues ("No", "n't") never appear in the top-20 features, and the word "nefarious" (which the user might expect to carry the contradiction signal) is **not represented at all** in the top features. So the user's hypothesis is only partially supported: the circuit does over-weight the "No one thinks" framing surface form (" that", " is", " to") and the conspiracy/chip token identity, rather than the semantic contradiction between the two sentences. But the mechanism is not literally a "negation-word detector" — it is a mixture of (a) entity-identity features on the named tokens (Conspiracy, MasterCard, chip) and (b) function-word/positional features on the framing (" that", " is investing in a chip that...", " to anything") that happen to co-locate with the rhetorical/sarcastic construction "No one thinks X is up to anything Y." The contradiction is therefore detected via a *bag of conspiratorial-entity tokens + sarcastic-framing surface tokens*, which is more lexical/syntactic than semantic and partially justifies the concern.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F16015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) | 1 | Conspiracy-theorists prefix (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) |
| [L0:F4287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) | 1 | Conspiracy-theorists prefix (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Conspiracy-theorists prefix (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L0:F2115](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) | 11 | Conspiracy-theorists prefix (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) |
| [L0:F3937](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3937) | 11 | Conspiracy-theorists prefix (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3937) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | chip / is / investing content tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F12377](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12377) | 4 | chip / is / investing content tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12377) |
| [L0:F4802](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4802) | 4 | chip / is / investing content tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4802) |
| [L1:F8696](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) | 8 | chip / is / investing content tokens | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 24 | chip / is / investing content tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F15958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15958) | 3 | 'theorists' / generic person-noun signal | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15958) |
| [L1:F13684](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) | 3 | 'theorists' / generic person-noun signal | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | 'theorists' / generic person-noun signal | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L4:F1602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) | 3 | 'theorists' / generic person-noun signal | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) |
| [L8:F12761](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) | 3 | 'theorists' / generic person-noun signal | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) |
| [L2:F16241](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) | 2 | 'theorists' / generic person-noun signal | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 6 | MasterCard entity features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 11 | MasterCard entity features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |
| [L2:F15808](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15808) | 6 | MasterCard entity features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15808) |
| [L1:F9693](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9693) | 11 | MasterCard entity features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9693) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | relative clause 'that can store...' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Input token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Input token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Input token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Input token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Input token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Input token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Input token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Input token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Input token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 24 | Input token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'CONTRADICTION' is not one of the top-k next-token can |
| 3 | `rank_segment_features` | ❌ This tool requires ctx.sibling_graphs to be set (at least on |
| 4 | `get_top_features` | 20 features; top: L3:9739 de=-0.348 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F16230@11` | ❌ error | — | — | Trace L2:F16230 (pos 11, direct_effect=+0.266). This is the strongest positive d… |
| SA-2 | `L0:F3635@12` | ❌ error | — | — | Trace L0:F3635 (pos 12, direct_effect=+0.225). Pos 12 is likely "No" — test if t… |
| SA-3 | `L0:F16015@1` | ❌ error | — | — | Trace L0:F16015 (pos 1, direct_effect=+0.186). Pos 1 is "Conspiracy". Determine … |
| SA-4 | `L3:F9739@2` | ❌ error | — | — | Trace L3:F9739 (pos 2, direct_effect=-0.348). This is the strongest negative dri… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F16230@11, k=15 → Emb:" chip"@11 (de=27.00) +14 more |
| 2 | `get_upstream_features` | L0:F3635@12, k=15 → Emb:" that"@12 (de=41.00) +14 more |
| 3 | `get_upstream_features` | L0:F16015@1, k=15 → Emb:"Cons"@1 (de=21.12) +14 more |
| 4 | `get_upstream_features` | L3:F9739@2, k=15 → Emb:"Cons"@1 (de=8.75) +14 more |
| 5 | `get_upstream_features` | L0:F2115@11, k=10 → Emb:" chip"@11 (de=8.75) +9 more |
| 6 | `get_upstream_features` | L2:F16241@2, k=10 → Emb:"Cons"@1 (de=17.25) +9 more |
| 7 | `get_upstream_features` | L0:F11375@7, k=10 → Emb:" is"@7 (de=31.38) +9 more |
| 8 | `get_upstream_features` | L0:F8444@24, k=10 → Emb:" to"@24 (de=42.00) +9 more |
| 9 | `get_upstream_features` | L7:F1062@6, k=10 → Emb:"Card"@6 (de=14.00) +9 more |
| 10 | `get_upstream_features` | L0:F4802@4, k=10 → Emb:"  "@4 (de=15.00) +9 more |
| 11 | `get_upstream_features` | L4:F1602@3, k=10 → Emb:" theorists"@3 (de=3.23) +9 more |
| 12 | `get_upstream_features` | L1:F13684@3, k=10 → Emb:" theorists"@3 (de=10.12) +9 more |
| 13 | `get_upstream_features` | L2:F15808@6, k=10 → Emb:"Card"@6 (de=6.09) +9 more |
| 14 | `get_upstream_features` | L0:F12377@4, k=10 → Emb:"  "@4 (de=10.12) +9 more |
| 15 | `get_upstream_features` | L1:F8696@8, k=10 → Emb:" investing"@8 (de=21.88) +9 more |
| 16 | `get_upstream_features` | L0:F3937@11, k=10 → Emb:" chip"@11 (de=12.75) +9 more |
| 17 | `get_upstream_features` | L1:F9693@11, k=10 → Emb:" chip"@11 (de=14.88) +9 more |
| 18 | `get_upstream_features` | L8:F12761@3, k=10 → Emb:" theorists"@3 (de=4.56) +9 more |
| 19 | `get_upstream_features` | L0:F15958@3, k=10 → Emb:" theorists"@3 (de=12.06) +9 more |
| 20 | `get_upstream_features` | L0:F4287@1, k=10 → Emb:"Cons"@1 (de=10.62) +9 more |

### Build

`build_circuit` → 7 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 25,797 | 4,609 | 68,476 | 0 | $0.0174 | — | — |
| **Total** | | **25,797** | **4,609** | **68,476** | **0** | **$0.0174** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 7s