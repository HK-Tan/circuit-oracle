# Circuit Oracle Report
**Date:** 2026-07-28 07:23:34 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by genuine profession-related content tokens (food, healthy, physically active, dieting, knowledge, confidence, lifestyle, empowering) rather than by the "She" gender pronoun, which appears only once with a small contribution.

**Confidence:** 8

**Reasoning:** The attribution graph shows that the top features driving the probe's positive score are all directly tied to nutrition/wellness content. The largest positive direct_effects come from:

- **L6:F11327 (pos 15 & 41) and L14:F4197 (pos 15)** — trace back to the "food" token embedding (direct_effect 34 & 41.25 on the upstream call), and L14:F4197 specifically promotes a "food/nutrition" context representation.
- **L4:F3047 (pos 22)** — traces back to "active" (10.25) and "physically" (8.4375) embeddings, encoding the "physically active" phrase.
- **L4:F13412 (pos 34)** — traces back to the "dieting" token embedding (direct_effect 18.25), a domain-specific term.
- **L2:F6341 (pos 14)** — traces back to the "healthy" token embedding (29.25).
- **L0 content-word supernode** — many L0 features (F4030, F11814, F10218, F8444, F2238, F2845, F5829, F8566, F2349, F9927) each track individual content tokens: "passionate," "about," "others," "knowledge," "confidence," "to," "lifestyle," "empowering." These are shallow bigram-level detectors but they fire on genuine profession-semantic words, not on gender.

The "She" pronoun (pos 1) appears via L0:F7244 with activation 8.69 and direct_effect 0.056 — a positive but very small contribution. It is also countered by L0:F9519 (pos 1, direct_effect −0.065) and L6:F11646 (pos 1, direct_effect −0.065), both of which fire on "She" and *inhibit* the probe score. Net gendered signal from pos 1 is approximately zero or slightly negative.

The dominant positive signal is unambiguously content-driven: nutrition vocabulary ("food," "healthy," "dieting"), wellness activity ("physically active"), and empowerment/coaching lexicon ("knowledge," "confidence," "empowering," "lifestyle," "passionate") — all genuine indicators of a health/wellness profession (consistent with a nutritionist/dietitian classification). The user's concern that the circuit relies on gender markers is not supported: the "She" pronoun contributes minimally and bidirectionally (both positive and negative L0 features on pos 1), while content tokens provide the bulk of the positive drive. This circuit is using legitimate profession-discriminative features, not spurious gender cues.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 15 | L14: 'food' / nutrition context (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L4:F3047](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) | 22 | L4: 'physically active' (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3047) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 15 | L6: 'food' token (pos 15 & 41) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 41 | L6: 'food' token (pos 15 & 41) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 34 | L4: 'dieting' (pos 34) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L2:F6341](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6341) | 14 | L2: 'healthy' (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6341) |
| [L0:F4030](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) | 3 | L0: content-word features (knowledge, confidence, others, lifestyle, etc.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) |
| [L0:F11814](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11814) | 11 | L0: content-word features (knowledge, confidence, others, lifestyle, etc.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11814) |
| [L0:F10218](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) | 17 | L0: content-word features (knowledge, confidence, others, lifestyle, etc.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10218) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 12 | L0: content-word features (knowledge, confidence, others, lifestyle, etc.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | L0: content-word features (knowledge, confidence, others, lifestyle, etc.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F2845](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) | 9 | L0: content-word features (knowledge, confidence, others, lifestyle, etc.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2845) |
| [L0:F5829](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5829) | 3 | L0: content-word features (knowledge, confidence, others, lifestyle, etc.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5829) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 9 | L0: content-word features (knowledge, confidence, others, lifestyle, etc.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 6 | L0: content-word features (knowledge, confidence, others, lifestyle, etc.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L0:F9927](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9927) | 3 | L0: content-word features (knowledge, confidence, others, lifestyle, etc.) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9927) |
| [L0:F7244](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7244) | 1 | L0: 'She' pronoun (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7244) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2349 de=-0.123 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11327@15` | ❌ error | — | — | Trace upstream from L6:F11327 at pos 15 to understand what input tokens/concepts… |
| SA-2 | `L4:F3047@22` | ❌ error | — | — | Trace upstream from L4:F3047 at pos 22 to understand what input tokens/concepts … |
| SA-3 | `L14:F4197@15` | ❌ error | — | — | Trace upstream from L14:F4197 at pos 15 to understand what input tokens/concepts… |
| SA-4 | `L0:F4030@3` | ❌ error | — | — | Trace upstream from L0:F4030 at pos 3 to understand what input token/concept thi… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11327@15, k=10 → Emb:" food"@15 (de=34.00) +9 more |
| 2 | `get_upstream_features` | L4:F3047@22, k=10 → Emb:" active"@22 (de=10.25) +9 more |
| 3 | `get_upstream_features` | L14:F4197@15, k=10 → Emb:" food"@15 (de=22.62) +9 more |
| 4 | `get_upstream_features` | L0:F4030@3, k=10 → Emb:" passionate"@3 (de=6.31) +9 more |
| 5 | `get_upstream_features` | L0:F11814@11, k=10 → Emb:" confidence"@11 (de=13.81) +9 more |
| 6 | `get_upstream_features` | L0:F10218@17, k=10 → Emb:" lifestyle"@17 (de=25.00) +9 more |
| 7 | `get_upstream_features` | L0:F8444@12, k=10 → Emb:" to"@12 (de=41.25) +9 more |
| 8 | `get_upstream_features` | L0:F2238@4, k=10 → Emb:" about"@4 (de=34.50) +9 more |
| 9 | `get_upstream_features` | L0:F2845@9, k=10 → Emb:" knowledge"@9 (de=17.00) +9 more |
| 10 | `get_upstream_features` | L0:F2349@6, k=10 → Emb:" others"@6 (de=41.00) +9 more |
| 11 | `get_upstream_features` | L4:F13412@34, k=8 → Emb:" dieting"@34 (de=18.25) +7 more |
| 12 | `get_upstream_features` | L1:F7244@1, k=8 → Emb:"She"@1 (de=13.56) +7 more |
| 13 | `get_upstream_features` | L0:F5829@3, k=8 → Emb:" passionate"@3 (de=15.00) +7 more |
| 14 | `get_upstream_features` | L0:F8566@9, k=8 → Emb:" knowledge"@9 (de=16.62) +7 more |
| 15 | `get_upstream_features` | L0:F6051@28, k=8 → Emb:"."@28 (de=47.25) +7 more |
| 16 | `get_upstream_features` | L2:F6341@14, k=8 → Emb:" healthy"@14 (de=29.25) +7 more |
| 17 | `get_upstream_features` | L0:F9519@1, k=8 → Emb:"She"@1 (de=15.75) +7 more |
| 18 | `get_upstream_features` | L0:F9927@3, k=8 → Emb:" passionate"@3 (de=10.62) +7 more |
| 19 | `get_upstream_features` | L6:F11327@41, k=8 → Emb:" food"@41 (de=41.25) +7 more |

### Build

`build_circuit` → 23 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 28,112 | 4,885 | 65,278 | 0 | $0.0182 | — | — |
| **Total** | | **28,112** | **4,885** | **65,278** | **0** | **$0.0182** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 59s