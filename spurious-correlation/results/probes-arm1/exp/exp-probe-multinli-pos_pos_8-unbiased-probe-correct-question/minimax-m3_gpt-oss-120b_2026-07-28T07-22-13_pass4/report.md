# Circuit Oracle Report
**Date:** 2026-07-28 07:22:13 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven primarily by entity recognition of "Congress" at pos 2 and content-word features around "began to include many members" (pos 10-12), with the signal flowing from token embeddings through early-layer entity detectors and mid-layer semantic features to the probe direction.

**Confidence:** 7

**Reasoning:** The circuit traces from the probe output through two main paths. The dominant path runs through L2:F2701 ("words related to the U.S. Congress", frac_nonzero=0.011, direct_effect=0.85) and L3:F123 ("mentions of the United States Congress", frac_nonzero=0.007, direct_effect=0.25), which trace directly back to the "Congress" embedding at pos 2. L0:F15411 ("terms relating to political bodies, figures, and processes", frac_nonzero=0.008) also strongly activates on the same "Congress" token (direct_effect=0.49). The second path flows through L3:F5753 ("the word 'includes' or 'containing'", frac_nonzero=0.002, direct_effect=0.53) which traces to the "include" embedding at pos 12, and L4:F59 (direct_effect=0.41) tracing to the "began" embedding at pos 10. L0:F195 ("the word 'who'", frac_nonzero=0.002) and L0:F13437 activate on the "who"/"members" tokens at pos 14-15.

The user's concern about "negation words" is partially validated but the picture is more nuanced: L0:F9557 ("the word 'clean' and words/phrases associated with people") and L0:F10401 ("mentions of genes and proteins") appear to be generic lexical features that happen to co-activate on the "Congress" token (pos 2) but contribute *negatively* (direct_effect -0.31 and -0.37). L0:F6044 ("the word 'yield'") similarly activates generically. The "no responsibility" / negation content of the second sentence does NOT appear in the top features driving the probe — the circuit is dominated by entity recognition (Congress) and content-word features (include, began, who, members) from the *first* sentence, not negation signals from the second. The features are entity-specific (Congress, political bodies) and content-word-specific (include, began) rather than contradiction-specific negation patterns, so the probe appears to be using semantic content about Congress and the action of "beginning to include" rather than relying primarily on negation cues. The warning about not reaching embedding nodes is resolvable — the traces already show strong positive direct_effects from embeddings (e.g., "Congress" → L2:F2701 = 28.1, "include" → L3:F5753 = 41.0, "began" → L4:F59 = 13.3, "who" → L0:F195 = 16.25), confirming the input-token grounding.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: Congress (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: include (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: began (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: to (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: who (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: members (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: , (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F15411](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) | 2 | Early-layer Congress/political entity (L0) |  terms relating to political bodies, figures, and processes | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) |
| [L0:F10401](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10401) | 2 | Early-layer Congress/political entity (L0) |  mentions of genes and proteins | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10401) |
| [L0:F10198](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) | 2 | Early-layer Congress/political entity (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) |
| [L0:F195](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/195) | 15 | Early-layer 'who' (L0) | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/195) |
| [L0:F13437](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) | 15 | Early-layer 'who' (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) |
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | Early-layer generic/negative (L0) | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F9557](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) | 2 | Early-layer generic/negative (L0) | the word "clean" and words/phrases associated with people | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) |
| [L0:F10783](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) | 12 | Early-layer generic/negative (L0) |  the word "include" (and variations of the word) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) |
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | Mid-layer Congress features (L2-3) |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | Mid-layer Congress features (L2-3) |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L2:F6735](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) | 2 | Mid-layer Congress features (L2-3) |  political parties and politicians | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) |
| [L3:F5753](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) | 12 | Mid-layer 'include(s)/began to' features (L2-4) |  the word "includes" or "containing". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) |
| [L3:F8351](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8351) | 12 | Mid-layer 'include(s)/began to' features (L2-4) |  words related to including and code language symbols | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8351) |
| [L4:F59](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) | 11 | Mid-layer 'include(s)/began to' features (L2-4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) |
| [L4:F7775](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7775) | 9 | Mid-layer 'include(s)/began to' features (L2-4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7775) |
| [L2:F11469](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11469) | 11 | Mid-layer 'include(s)/began to' features (L2-4) |  the word "to" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11469) |
| [L3:F12596](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) | 11 | Mid-layer 'include(s)/began to' features (L2-4) |  actions or methods, sometimes preceeded by the preposition 'a' or 'to'. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe direction (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:2701 de=0.848 |
| 3 | `inspect_feature` ×4 | L2:2701, L3:5753, L0:6044, L0:15411 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F2701@2` | ❌ error | — | — | Trace upstream from L2:F2701 (Congress-related words) to identify embedding node… |
| SA-2 | `L3:F5753@12` | ❌ error | — | — | Trace upstream from L3:F5753 ("includes" word detector at pos 12, "began to incl… |
| SA-3 | `L4:F59@11` | ❌ error | — | — | Trace upstream from L4:F59 at pos 11. Identify what this feature encodes and wha… |
| SA-4 | `L4:F7775@9` | ❌ error | — | — | Trace upstream from L4:F7775 at pos 9. Identify what this feature encodes and wh… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F2701@2, k=15 → Emb:" Congress"@2 (de=28.12) +14 more |
| 2 | `get_upstream_features` | L3:F5753@12, k=15 → Emb:" include"@12 (de=41.00) +14 more |
| 3 | `get_upstream_features` | L4:F59@11, k=15 → Emb:" began"@10 (de=13.31) +14 more |
| 4 | `get_upstream_features` | L4:F7775@9, k=15 → Emb:","@9 (de=4.94) +14 more |
| 5 | `get_upstream_features` | L3:F123@2, k=10 → Emb:" Congress"@2 (de=20.62) +9 more |
| 6 | `inspect_feature` ×5 | L3:123, L3:12596, L2:11469, L2:11734, L0:4870 |
| 7 | `get_top_features` | token="", k=30 → 30 features; top: L2:2701 de=0.848 |
| 8 | `inspect_feature` ×6 | L3:8351, L0:10401, L2:6735, L0:9557, L0:10783, L0:195 |
| 9 | `get_upstream_features` | L3:F8351@12, k=10 → Emb:" include"@12 (de=28.38) +9 more |
| 10 | `get_upstream_features` | L0:F10401@2, k=10 → Emb:" Congress"@2 (de=13.25) +9 more |
| 11 | `get_upstream_features` | L2:F6735@2, k=10 → Emb:" Congress"@2 (de=9.12) +9 more |
| 12 | `get_upstream_features` | L0:F195@15, k=10 → Emb:" who"@15 (de=16.25) +9 more |

### Build

`build_circuit` → 13 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 44,292 | 4,241 | 169,654 | 0 | $0.0286 | — | — |
| **Total** | | **44,292** | **4,241** | **169,654** | **0** | **$0.0286** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 4s