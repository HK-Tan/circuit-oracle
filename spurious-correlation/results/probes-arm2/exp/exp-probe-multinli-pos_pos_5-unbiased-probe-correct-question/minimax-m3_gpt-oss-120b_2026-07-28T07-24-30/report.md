# Circuit Oracle Report
**Date:** 2026-07-28 07:24:30 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven almost entirely by a shallow lexical circuit that detects the presence of contradiction-marker words ("not", "but", "only") in the prompt, rather than building a semantic representation of the two sentences and comparing their meaning.

**Confidence:** 9

**Reasoning:** The circuit confirms the user's concern that the probe is using a spurious "negation word" shortcut rather than actual semantic content comparison.

The dominant inputs are raw token embeddings for "but" (pos 13, direct_effect 42.5 into L0:F11101, and 4.0 into L15:F12905), " not" (pos 6, direct_effect 3.1 into the late summarizer), and " only" (pos 7, direct_effect 6.0 into L1:F1500 and 21.3 into L2:F5627). These three function-word embeddings flow into early-layer features that fire on negation/conjunction tokens regardless of what they are negating — L0:F11101 is essentially a "but"-detector (activation 36, driven 42.5 by the "but" token itself), L2:F5627 is a "not/only" co-occurrence detector (activation 46.25 at pos 7), and L3:F3755 and L2:F4481 are higher-level contrast-word detectors.

These features feed into mid-layer contrast composers (L4:L2884, L6:L3283, L6:L3655) that compose the negation words with the surrounding context words, and then into late summarizers (L12:F10235, L13:F2557, L14:F11020, L15:F12905 at activation 49.5) that simply count how many contradiction-marker tokens appear. The top output-driving feature L15:F12905 (direct_effect -0.36 to the probe) receives its signal predominantly from the embeddings of " only" (5.97), " but" (4.0), and " not" (3.09) — i.e., it is measuring token-level negation density, not the semantic relationship between the hypothesis and premise.

Crucially, the content words "program", "improve", "lawyers", "public", "image", "needy" — which would be needed for an actual entailment comparison — barely appear. Features like L2:F13565 (direct_effect 0.20) and L3:F2782 (direct_effect -0.19) on "program" are weak and largely cancel out. The strong positive features (L5:F7144, L2:F13565, L4:F12847) fire on a quote-attribution pattern ("Wagonheim said") rather than on the proposition being attributed. This means swapping the content words for any other content words (e.g., "The program isn't going to harm lawyers' private image") would leave the contradiction score essentially unchanged, because the circuit is reading the negation/conjunction scaffolding, not the meaning.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Negation/Correction Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Negation/Correction Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Negation/Correction Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Other Input Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Other Input Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Other Input Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Other Input Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Other Input Token Embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F11101](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11101) | 13 | Early-Layer Negation/Conjunction Detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11101) |
| [L0:F12483](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12483) | 7 | Early-Layer Negation/Conjunction Detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12483) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | Early-Layer Negation/Conjunction Detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L0:F15525](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) | 3 | Early-Layer Negation/Conjunction Detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15525) |
| [L2:F13565](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) | 5 | Early-Layer Negation/Conjunction Detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) |
| [L3:F16191](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16191) | 3 | Early-Layer Negation/Conjunction Detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16191) |
| [L3:F41](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/41) | 3 | Early-Layer Negation/Conjunction Detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/41) |
| [L3:F881](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/881) | 13 | Early-Layer Negation/Conjunction Detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/881) |
| [L3:F3755](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3755) | 13 | Early-Layer Negation/Conjunction Detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3755) |
| [L3:F2782](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2782) | 5 | Early-Layer Negation/Conjunction Detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2782) |
| [L4:F2884](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) | 13 | Mid-Layer Contrast Composers (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) |
| [L4:F12847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) | 3 | Mid-Layer Contrast Composers (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) |
| [L5:F7144](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) | 3 | Mid-Layer Contrast Composers (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) |
| [L6:F3655](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) | 7 | Mid-Layer Contrast Composers (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3655) |
| [L6:F3283](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3283) | 13 | Mid-Layer Contrast Composers (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3283) |
| [L6:F6720](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6720) | 13 | Mid-Layer Contrast Composers (L4-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6720) |
| [L7:F4284](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4284) | 13 | Mid-Layer Negation Aggregators (L7-L10) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4284) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 7 | Mid-Layer Negation Aggregators (L7-L10) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L10:F6078](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) | 13 | Mid-Layer Negation Aggregators (L7-L10) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6078) |
| [L10:F12520](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12520) | 13 | Mid-Layer Negation Aggregators (L7-L10) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12520) |
| [L12:F10235](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10235) | 13 | Late-Layer Summarizers (L12-L15) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10235) |
| [L13:F2557](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/2557) | 13 | Late-Layer Summarizers (L12-L15) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/2557) |
| [L14:F11020](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) | 13 | Late-Layer Summarizers (L12-L15) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) |
| [L15:F1990](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) | 7 | Late-Layer Summarizers (L12-L15) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | Late-Layer Summarizers (L12-L15) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L14:F10765](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10765) | 7 | Late-Layer Summarizers (L12-L15) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10765) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe Output Direction | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'contradiction' is not one of the top-k next-token can |
| 3 | `get_top_features` | 10 features; top: L15:12905 de=-0.355 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L15:F12905@13` | ❌ error | — | — | Trace the path from L15:F12905 at pos 13. This is the strongest feature driving … |
| SA-2 | `L0:F8046@8` | ❌ error | — | — | Trace the path from L0:F8046 at pos 8. This is a strong early-layer feature. Pos… |
| SA-3 | `L5:F7144@3` | ❌ error | — | — | Trace the path from L5:F7144 at pos 3. This is a mid-layer feature with positive… |
| SA-4 | `L2:F13565@5` | ❌ error | — | — | Trace the path from L2:F13565 at pos 5. This is a low-layer feature with positiv… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L15:F12905@13, k=15 → Emb:" only"@7 (de=5.97) +14 more |
| 2 | `get_upstream_features` | L0:F8046@8, k=15 → Emb:" will"@8 (de=37.75) +14 more |
| 3 | `get_upstream_features` | L5:F7144@3, k=15 → L3:F16191 (de=2.97) +14 more |
| 4 | `get_upstream_features` | L2:F13565@5, k=15 → Emb:" program"@5 (de=16.75) +14 more |
| 5 | `get_upstream_features` | L4:F12847@3, k=15 → Emb:" said"@3 (de=4.41) +14 more |
| 6 | `get_upstream_features` | L3:F2782@5, k=15 → Emb:" program"@5 (de=27.00) +14 more |
| 7 | `get_upstream_features` | L0:F15525@3, k=15 → Emb:" said"@3 (de=20.25) +14 more |
| 8 | `get_upstream_features` | L17:F3763@7, k=15 → L15:F1990 (de=10.38) +14 more |
| 9 | `get_upstream_features` | L1:F1500@7, k=15 → Emb:" only"@7 (de=6.31) +14 more |
| 10 | `get_upstream_features` | L0:F6131@3, k=15 → Emb:" said"@3 (de=7.47) +14 more |
| 11 | `get_upstream_features` | L2:F5627@7, k=12 → Emb:" only"@7 (de=21.25) +11 more |
| 12 | `get_upstream_features` | L9:F12274@7, k=12 → L6:F3655 (de=9.19) +11 more |
| 13 | `get_upstream_features` | L15:F1990@7, k=12 → Emb:" not"@6 (de=9.69) +11 more |
| 14 | `get_upstream_features` | L4:F2884@13, k=12 → Emb:" but"@13 (de=17.75) +11 more |
| 15 | `get_upstream_features` | L14:F11020@13, k=10 → L13:F2557 (de=9.75) +9 more |
| 16 | `get_upstream_features` | L6:F3655@7, k=10 → Emb:" only"@7 (de=8.94) +9 more |
| 17 | `get_upstream_features` | L6:F3283@13, k=10 → Emb:" only"@7 (de=6.03) +9 more |
| 18 | `get_upstream_features` | L7:F4284@13, k=10 → Emb:" but"@13 (de=7.19) +9 more |
| 19 | `get_upstream_features` | L13:F2557@13, k=10 → L12:F10235 (de=6.09) +9 more |
| 20 | `get_upstream_features` | L12:F10235@13, k=10 → Emb:" but"@13 (de=4.69) +9 more |
| 21 | `get_upstream_features` | L10:F6078@13, k=10 → Emb:" but"@13 (de=5.69) +9 more |
| 22 | `get_upstream_features` | L3:F881@13, k=10 → Emb:" only"@7 (de=10.69) +9 more |
| 23 | `get_upstream_features` | L0:F11101@13, k=10 → Emb:" but"@13 (de=42.50) +9 more |
| 24 | `get_upstream_features` | L10:F12520@13, k=8 → Emb:" but"@13 (de=5.69) +7 more |
| 25 | `get_upstream_features` | L3:F3755@13, k=8 → Emb:" but"@13 (de=9.81) +7 more |

### Build

`build_circuit` → 7 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 19,105 | 4,751 | 104,088 | 0 | $0.0177 | — | — |
| **Total** | | **19,105** | **4,751** | **104,088** | **0** | **$0.0177** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 5s