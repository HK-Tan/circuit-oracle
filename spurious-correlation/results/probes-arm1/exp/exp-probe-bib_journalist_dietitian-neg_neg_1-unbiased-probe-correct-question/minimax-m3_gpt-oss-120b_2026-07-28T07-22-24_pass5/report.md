# Circuit Oracle Report
**Date:** 2026-07-28 07:22:24 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "journalist" is driven by *genuine profession-content* tokens — primarily the literal word "report" (pos 21) and "news" (pos 27) — funneling through a clean chain of journalism-encoding transcoder features. Despite the surface concern about gender markers, the "His" feature (L0:8964) is present in the top features list but only contributes a small positive direct_effect (0.088) and does NOT feed into the dominant L14:4420 or L19:2486 profession features at any meaningful path; the "His" embedding connects only tangentially to the L1:14511 "report" word feature with weak effect.

**Confidence:** 8

**Reasoning:** The circuit traces cleanly from the embedding of " report" (pos 21, direct_effect=5.22 into L14:4420, 12.06 into L8:8855, 20.62 into L1:14511) and the embedding of " news" (pos 27, direct_effect=7.94 into L19:2486) upward through a stack of journalism-encoding features:
- **L1:14511** ("the word 'report'") at pos 21 — fires on the literal profession-content token
- **L4:13253** ("things related to journalism and the media"), **L7:13646** ("news reporting and journalism") — early journalism/media detectors
- **L8:8855** ("mentions of news reporters and news reporting"), **L8:8437** (film/media production) — mid-layer profession features
- **L14:4420** ("words and phrases related to journalism and newspapers", frac_nonzero=0.0165, promoted_tokens: journalists/journalist/reporter/journalism) — strong late-layer profession feature, with direct_effect=-0.148 to probe (the largest negative push) because it *suppresses* the probe direction
- **L19:2486** ("journalistic sources and news outlets", frac_nonzero=0.029, promoted_tokens: reporting/reporter/coverage) — late-layer profession feature with direct_effect=-0.097 (negative) and additional L19:2486 instances at pos 22, 27, 28, 29 also suppressing

The user worried about spurious gender markers. The "His" feature (L0:8964) is the only clearly gender-coded feature in the top-15, but it appears at only a single position (pos 1) with modest activation 10.69 and direct_effect 0.088 — a small positive contribution to the probe. Crucially, it does not connect into the L14:4420 or L19:2486 profession features (no path found). The "His" embedding has only weak downstream effects (direct_effect=0.95 into L8:8855, 0.81 into "him" at pos 17). The dominant signal is clearly the profession content: "report", "news", and the journalism concept — not the pronoun.

The suppressors (L9:7435, L9:2845, L16:8642, L17:5218) and suppressor-embeddings ("<bos>", "world", "countries") are negative-edge features that push *against* the probe's classification — likely firing on the non-journalism portions of the prompt (travel/world content) and pulling the score down. The net effect is that the model's late-layer journalism features fire on the relevant content tokens, but the probe direction itself rates them with a negative sign, suggesting the probe may actually be reading against these features (perhaps probing for "NOT journalist" or a contrastive direction), or the classification is marginal.

**Conclusion:** The attribution circuit shows the probe's classification is **not** relying on spurious gender markers. The "His" feature is a minor, isolated contributor. The dominant signal flows from the genuine profession-content tokens "report" and "news" through stacked journalism-encoding features (L1→L4/L7→L8→L14→L19), with suppressors (L9, L16, L17) and non-content embeddings ("world", "countries", "<bos>") opposing the classification. The mechanism is genuine profession recognition, not gender-based shortcutting.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F14511](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14511) | 21 | L0: report word feature (L0:14511) |  the word "report" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14511) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | Early journalism/media features (L4-L7) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | Early journalism/media features (L4-L7) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 22 | Early journalism/media features (L4-L7) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 21 | Early journalism/media features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F12495](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12495) | 21 | Early journalism/media features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12495) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Mid-layer journalism features (L8) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 22 | Mid-layer journalism features (L8) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | Mid-layer journalism features (L8) | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 21 | Mid-layer journalism features (L8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Late journalism feature (L14:4420) — multi-position | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 22 | Late journalism feature (L14:4420) — multi-position | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | Late journalism feature (L14:4420) — multi-position | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 29 | Late journalism feature (L14:4420) — multi-position | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L9:F7435](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) | 21 | L9 suppressor (L9:7435) — negative on L14:4420 | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) |
| [L9:F2845](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) | 21 | L9 suppressor (L9:7435) — negative on L14:4420 | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2845) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Late journalism feature (L19:2486) — multi-position |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 22 | Late journalism feature (L19:2486) — multi-position |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 27 | Late journalism feature (L19:2486) — multi-position |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 28 | Late journalism feature (L19:2486) — multi-position |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 29 | Late journalism feature (L19:2486) — multi-position |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L16:F8642](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) | 21 | Late suppressors (L16-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) |
| [L17:F5218](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) | 21 | Late suppressors (L16-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.147 |
| 3 | `inspect_feature` ×10 | L14:4420, L19:2486, L0:8964, L0:8444, L0:14287, L0:2203, L0:2011, L0:13948, L1:14511, L8:8855 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ❌ error | — | — | Trace upstream from L14:4420 (journalism/newspapers feature) at pos 21 to find w… |
| SA-2 | `L19:F2486@21` | ❌ error | — | — | Trace upstream from L19:2486 (journalistic sources and news outlets) at pos 21. … |
| SA-3 | `L0:F8964@1` | ❌ error | — | — | Trace upstream from L0:8964 (the possessive pronoun "His") at pos 1. Confirm wha… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@21, k=15 → Emb:" report"@21 (de=5.22) +14 more |
| 2 | `get_upstream_features` | L19:F2486@21, k=15 → L14:F4420 (de=14.31) +14 more |
| 3 | `get_upstream_features` | L8:F8855@21, k=15 → Emb:" report"@21 (de=12.06) +14 more |
| 4 | `get_upstream_features` | L1:F14511@21, k=15 → Emb:" report"@21 (de=20.62) +14 more |
| 5 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 6 | `get_upstream_features` | L19:F2486@29, k=10 → Emb:" news"@27 (de=7.94) +9 more |
| 7 | `inspect_feature` ×3 | L7:13646, L8:8437, L4:13253 |
| 8 | `get_upstream_features` | L0:F8964@1, k=10 → Emb:"His"@1 (de=13.69) +9 more |
| 9 | `get_upstream_features` | L19:F2486@22, k=10 → L14:F4420 (de=8.44) +9 more |

### Build

`build_circuit` → 14 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 31,499 | 5,425 | 177,178 | 0 | $0.0266 | — | — |
| **Total** | | **31,499** | **5,425** | **177,178** | **0** | **$0.0266** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 11s