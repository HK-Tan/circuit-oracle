# Circuit Oracle Report
**Date:** 2026-07-28 07:23:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven primarily by L0–L3 features whose direct upstream drivers are the "Indians" identity-mention embedding and assorted function-word embeddings ("is", "are", "stated", "by", "abusers", "how/know/to"), not by features encoding the actual toxic predicates ("abusers", "destroy", "backlash", "abusing").

**Confidence:** 7

**Reasoning:** Tracing the top features to their roots reveals that nearly every positive contributor flows from the "Indians" token-embedding at pos 1 (e.g., L0:F11668 has direct_effect 12.4 from `Emb: Indians`; L2:F1680 has 8.56; L3:F13473 has 10.25; L0:F6035 indirectly via pos 7). These features fire on identity-group tokens (and surrounding copula/auxiliary words) rather than encoding the toxicity-bearing verbs/nouns ("abusers", "destroy", "backlash", "abusing"). The single negative feature (L3:F14281) traces to generic function words "how/know/to" (pos 16–18) and merely suppresses the score. The "abusers" embedding at pos 3 contributes only modestly (e.g., 12.75 to L3:F9646 and 1.89 to L6:F10545) and is overshadowed by the much larger identity-entity pathway. This pattern — the probe picking up a "this sentence mentions an identity group" signal rather than the actual toxic content — is exactly the spurious-correlation concern the user flagged: a model that classifies the text as toxic primarily because a demographic term is present, not because the predicates are slurs or calls for harm. Early-layer (L0–L3) identity and copula features dominate the signed influence, with downstream L4–L6 features providing only minor modulation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F11668](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11668) | 1 | Identity-entity features (L0-L3) — fire on "Indians"/identity mentions | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11668) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 8 | Identity-entity features (L0-L3) — fire on "Indians"/identity mentions | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F8381](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8381) | 23 | Identity-entity features (L0-L3) — fire on "Indians"/identity mentions | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8381) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 7 | Identity-entity features (L0-L3) — fire on "Indians"/identity mentions | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L2:F1680](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) | 1 | Identity-entity features (L0-L3) — fire on "Indians"/identity mentions | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | Identity-entity features (L0-L3) — fire on "Indians"/identity mentions | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L3:F9646](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9646) | 2 | Identity-entity features (L0-L3) — fire on "Indians"/identity mentions | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9646) |
| [L3:F4327](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4327) | 3 | Identity-entity features (L0-L3) — fire on "Indians"/identity mentions | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4327) |
| [L3:F2705](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2705) | 3 | Identity-entity features (L0-L3) — fire on "Indians"/identity mentions | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2705) |
| [L0:F6035](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6035) | 7 | Identity-entity features (L0-L3) — fire on "Indians"/identity mentions | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6035) |
| [L0:F15956](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15956) | 25 | Identity-entity features (L0-L3) — fire on "Indians"/identity mentions | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15956) |
| [L0:F11154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) | 2 | Generic copula/function-word features (L0-L4) — suppress probe | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) |
| [L3:F14281](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14281) | 18 | Generic copula/function-word features (L0-L4) — suppress probe | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14281) |
| [L6:F10545](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) | 3 | Generic copula/function-word features (L0-L4) — suppress probe | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) |
| [L5:F3229](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3229) | 3 | Generic copula/function-word features (L0-L4) — suppress probe | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3229) |
| [L6:F1600](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1600) | 12 | Generic copula/function-word features (L0-L4) — suppress probe | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1600) |
| [L3:F5853](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5853) | 7 | Generic copula/function-word features (L0-L4) — suppress probe | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5853) |
| [L1:F13535](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13535) | 1 | Generic copula/function-word features (L0-L4) — suppress probe | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13535) |
| [L4:F4021](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) | 4 | Generic copula/function-word features (L0-L4) — suppress probe | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 5 | Generic copula/function-word features (L0-L4) — suppress probe | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:11375 de=0.221 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F11375@8` | ❌ error | — | — | Trace L0:F11375 at pos 8. What token/pattern does this feature detect? This is t… |
| SA-2 | `L0:F11668@1` | ❌ error | — | — | Trace L0:F11668 at pos 1. This is the 2nd top positive contributor. What does it… |
| SA-3 | `L3:F14281@18` | ❌ error | — | — | Trace L3:F14281 at pos 18. This is the top negative contributor. What does it de… |
| SA-4 | `L0:F11154@2` | ❌ error | — | — | Trace L0:F11154 at pos 2. This is the 2nd top negative contributor. What does it… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F11375@8, k=10 → Emb:" is"@8 (de=32.50) +9 more |
| 2 | `get_upstream_features` | L0:F11668@1, k=10 → Emb:"Indians"@1 (de=12.38) +9 more |
| 3 | `get_upstream_features` | L0:F11154@2, k=10 → Emb:" are"@2 (de=36.00) +9 more |
| 4 | `get_upstream_features` | L0:F8381@23, k=10 → Emb:" by"@23 (de=36.25) +9 more |
| 5 | `get_upstream_features` | L3:F14281@18, k=10 → Emb:" how"@17 (de=31.38) +9 more |
| 6 | `get_upstream_features` | L3:F13473@2, k=10 → Emb:"Indians"@1 (de=10.25) +9 more |
| 7 | `get_upstream_features` | L6:F10545@3, k=10 → Emb:" abusers"@3 (de=1.90) +9 more |
| 8 | `get_upstream_features` | L0:F3436@7, k=10 → Emb:" stated"@7 (de=10.75) +9 more |
| 9 | `get_upstream_features` | L0:F11375@3, k=5 → ❌ Feature (layer=0, feature_idx=11375) not found at pos=3. Thi |
| 10 | `get_upstream_features` | L2:F1680@1, k=10 → Emb:"Indians"@1 (de=8.56) +9 more |
| 11 | `get_upstream_features` | L3:F9646@2, k=10 → Emb:"Indians"@1 (de=3.97) +9 more |
| 12 | `get_upstream_features` | L3:F4327@3, k=10 → Emb:" abusers"@3 (de=12.75) +9 more |

### Build

`build_circuit` → 11 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 23,169 | 3,548 | 33,707 | 0 | $0.0132 | — | — |
| **Total** | | **23,169** | **3,548** | **33,707** | **0** | **$0.0132** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 40s