# Circuit Oracle Report
**Date:** 2026-07-28 07:21:01 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven primarily by *genuine* profession-related signals — the token " report" at position 21 and " top" at position 26 — which activate a cascade of journalism-specific features (reporter, news outlets, news broadcasting) at layers 7–20, not by gender markers like "His".

**Confidence:** 7

**Reasoning:** The user's concern that the circuit uses spurious gender features is **not supported** by this graph. The dominant late-layer drivers of the probe are all profession-related:

- **L14:F4420** (direct_effect −0.1455, frac_nonzero 0.0165) — explicitly labeled "words and phrases related to journalism and newspapers" with promoted tokens "journalists", "journalist", "journalism", "reporter", "editorial". Its top upstream input is the embedding of " report" (pos 21) with direct_effect 5.22.
- **L19:F2486** (direct_effect −0.1128, frac_nonzero 0.029) — "journalistic sources and news outlets" with promoted tokens "reporting", "reporter", "coverage", "reporters". Its top upstream input is L14:F4420 (direct_effect 14.31) and the " report" embedding (direct_effect 3.36).
- **L20:F8433** (direct_effect −0.0623) — "words related to news broadcasting" with promoted tokens "news", "journalists", "newspaper", "reporters". Its top upstream input is the " top" embedding (pos 26, direct_effect 5.69) and L14:F4420 (direct_effect 5.06), which together light up on the phrase "top news organizations".
- **L8:F8855** (direct_effect −0.0513) — "mentions of news reporters and news reporting" (frac_nonzero 0.0085, very specific). Traces back to the " report" embedding (direct_effect 12.06).
- **L15:F2579** — "people providing information in some sort of official capacity" with " report" embedding as dominant input (direct_effect 38.25).

The token-level path is: **Emb:" report" (pos 21)** → L4:F661 (report token, direct_effect 14.4) → L7:F13646 (journalism association) → L8:F8855 (reporter, direct_effect 4.19) → L14:F4420 (journalism main) → L19:F2486 (news outlets) → L20:F8433 (news broadcasting at " top" pos 26) → probe.

The "**His**" feature (L0:F8964, direct_effect 0.079) does appear at the input, but it is a **token-embedding feature** at pos 1 with no downstream feature carrying its signal into the profession-detecting circuit. It contributes only its raw direct_effect of 0.079 — roughly half the strength of one of several journalism features, and it does not feed any profession-relevant mid/late-layer feature. The masculine pronoun is present in the input but is not functionally wired into the probe's classification pathway.

The actual mechanism is the model recognizing the word " report" → activating reporter/journalism semantic features → combining with " top" → activating news-organization features, which then project onto the probe direction. The profession signal is content-driven, not gender-driven.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: "His" (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: " report" (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: " top" (pos 26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | L0: "His" possessive pronoun detector |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | L0: "to" word detector | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F14287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) | 4 | L0: "see" word detector | the word "see" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) |
| [L4:F661](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) | 21 | L4: "report" token feature | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | L7: journalism-associated features at "report" | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 21 | L7: journalism-associated features at "report" | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F12495](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12495) | 21 | L7: journalism-associated features at "report" | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12495) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | L8: news/reporter features at "report" |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | L8: news/reporter features at "report" | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | L14: journalism/newspapers feature (pos 21) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L15:F2579](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) | 21 | L15: people reporting/informing officially | instances of people providing information in some sort of official capacity. Like reporting incidents, communicating facts or informing others of something. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | L19: journalistic sources/news outlets (pos 21) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 26 | L20: news broadcasting words (pos 26) | words related to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:4420 de=-0.145 |
| 3 | `inspect_feature` ×10 | L0:8964, L0:8444, L0:14287, L14:4420, L19:2486, L20:8433, L8:8855, L4:11898, L15:2579, L7:3085 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F2486@21` | ❌ error | — | — | Trace the path upstream from L19:F2486 (journalistic sources/news outlets) at po… |
| SA-2 | `L14:F4420@21` | ❌ error | — | — | Trace the path upstream from L14:F4420 (journalism/newspapers) at pos 21. What i… |
| SA-3 | `L0:F8964@1` | ❌ error | — | — | Trace upstream from L0:F8964 (possessive "His") at pos 1. Verify it connects to … |
| SA-4 | `L20:F8433@26` | ❌ error | — | — | Trace upstream from L20:F8433 (news broadcasting words) at pos 26. What input to… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F2486@21, k=15 → L14:F4420 (de=14.31) +14 more |
| 2 | `get_upstream_features` | L14:F4420@21, k=15 → Emb:" report"@21 (de=5.22) +14 more |
| 3 | `get_upstream_features` | L20:F8433@26, k=15 → Emb:" top"@26 (de=5.69) +14 more |
| 4 | `get_upstream_features` | L15:F2579@21, k=15 → Emb:" report"@21 (de=38.25) +14 more |
| 5 | `get_upstream_features` | L0:F8964@1, k=10 → Emb:"His"@1 (de=13.69) +9 more |
| 6 | `get_upstream_features` | L8:F8855@21, k=15 → Emb:" report"@21 (de=12.06) +14 more |
| 7 | `get_upstream_features` | L7:F13646@21, k=10 → Emb:" report"@21 (de=7.22) +9 more |
| 8 | `get_upstream_features` | L8:F8437@21, k=10 → Emb:" report"@21 (de=5.75) +9 more |
| 9 | `get_upstream_features` | L4:F661@21, k=10 → Emb:" report"@21 (de=14.38) +9 more |

### Build

`build_circuit` → 14 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 27,058 | 4,429 | 146,543 | 0 | $0.0222 | — | — |
| **Total** | | **27,058** | **4,429** | **146,543** | **0** | **$0.0222** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 6s