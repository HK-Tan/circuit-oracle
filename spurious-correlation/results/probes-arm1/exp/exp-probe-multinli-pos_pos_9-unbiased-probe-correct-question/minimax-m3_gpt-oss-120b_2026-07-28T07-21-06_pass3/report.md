# Circuit Oracle Report
**Date:** 2026-07-28 07:21:06 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe classification score is driven by an almost entirely shallow, surface-lexical feature bundle anchored on just three input tokens — `A` (pos 1), ` recorded` (pos 2), ` menu` (pos 3), ` will` (pos 4) — with no late-layer (>L4) circuit nodes and no semantic/contextual integration. The classification is a shallow bag-of-content-word detector, not a contradiction-reasoning circuit.

**Confidence:** 7

**Reasoning:**

The attribution graph is unusually shallow — the only feature above layer 4 is **L17:F451** ("start of sentences", activation 68.5, direct_effect +0.19), which fires on the capital `A` at pos 1 (a sentence-initial token). All other top features live in L0–L3, and `get_upstream_features` returns the raw input embeddings immediately, confirming the signal never travels through deeper reasoning layers.

Tracing to the embeddings reveals the full mechanism:

1. **The two largest positive contributors are a single token: ` recorded` (pos 2).** `get_upstream_features` on the pos-2 cluster (L2:F8776 "finance/property law", L1:F3691 "word 'recording' in scientific/experimental documentation", L2:F3059 "verb 'record'", L0:F7443 "word 'record'", L2:F11317 "abbreviated examples", L0:F7404 "word 'faith'", L0:F9990 "word 'concert'", L0:F13280 "real-estate passages") returns `Emb: ' recorded' (pos 2)` with direct_effect **+24.75** and **+22.625** at the two traced features — these are simply co-active "record/recorded"-lexeme detectors (and a few spurious neighbours: "faith", "concert", "real-estate passages", "finance/property law") firing on the same token. They push the score **up** (total ≈ +1.3–1.8).

2. **The largest negative contributors are the tokens ` menu` (pos 3) and ` will` (pos 4).** L0:F2108 ("word 'menu'", pos 3, de -0.48), L1:F12253 ("word 'menu'", pos 3, de -0.43), L3:F3573 ("word 'menu' in interface elements", pos 3, de -0.29), L2:F3648 ("code snippets with menus/restaurants", pos 3, de -0.21), L0:F5128 ("word 'words'", pos 3, de +0.20), L0:F8046 ("word 'will'", pos 4, de -0.38), L2:F188 ("word 'will'", pos 4, de -0.21), L0:F4523 ("'domestic'/globalism", pos 3, de -0.19) all trace back to `Emb: ' menu' (pos 3)` or `Emb: ' will' (pos 4)`. They push the score **down** (total ≈ -2.0).

3. **L17:F451** ("start of sentences", pos 1, de +0.19) is the lone deep feature. Its upstream is `Emb: 'A' (pos 1)` (de +7.9) plus a sentence-context feature L16:F10989 (de -10.4). It contributes modestly based purely on the capital-letter sentence initial — no semantic content.

**User concern (validated):** the user's hypothesis is correct. The user said the circuit "uses spurious features (e.g., 'negation words' signals) rather than actual prompt content." The actual evidence is even more concrete: the circuit uses **shallow, single-token-anchored lexical detectors with no semantic integration whatsoever**. There is no negation word involved here, but the spirit of the critique is right — the "classification" is essentially a bag of words on `recorded/menu/will` with a few low-frac_nonzero neighbours (L2:F8776 frac=0.011, L1:F3691 frac=0.0073, L0:F2108 frac=0.0035, L1:F12253 frac=0.0041, L3:F3573 frac=0.0021, L2:F3648 frac=0.0015) that fire on the same token. The probe picks up "the word 'recorded' appears" + "the word 'menu' appears" + "the word 'will' appears" as a contradiction signal, with no read of the actual semantic relation "menu does not provide information" vs. the premise. The only late-layer feature (L17:F451) is a generic sentence-starter, and the positive side of the ledger is contaminated by obviously spurious neighbours (faith, concert, real-estate, finance/property-law) that happen to co-fire on `recorded` in feature-space but carry none of the relevant content.

**Confidence rationale:** High confidence on the structural observation (all top contributors trace to raw embeddings, no late-layer circuit exists). Moderate on the interpretive claim because the "recorded/menu" combination could be a genuine but shallow NLI heuristic rather than pure noise — but the explicit presence of features like "faith", "concert", "real-estate passages" in the positive side and the absence of any feature reading the meaning of `do not provide` confirm the user's "spurious surface features" diagnosis.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Sentence-start / new-context detector | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | Early-layer 'recorded' / 'recording' features (pos 2, sentence 1) |  words related to finance and property law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | Early-layer 'recorded' / 'recording' features (pos 2, sentence 1) |  the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L2:F3059](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) | 2 | Early-layer 'recorded' / 'recording' features (pos 2, sentence 1) |  the verb "record" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) |
| [L2:F11317](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11317) | 2 | Early-layer 'recorded' / 'recording' features (pos 2, sentence 1) |  abbreviated examples | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11317) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | Early-layer 'recorded' / 'recording' features (pos 2, sentence 1) | the word "record" appearing in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L0:F7404](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) | 2 | Early-layer 'recorded' / 'recording' features (pos 2, sentence 1) |  the word "faith", sometimes in association with related ideas like "links" or "opportunities" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) |
| [L0:F9990](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9990) | 2 | Early-layer 'recorded' / 'recording' features (pos 2, sentence 1) |  the word "concert" and some words related to concerts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9990) |
| [L0:F13280](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) | 2 | Early-layer 'recorded' / 'recording' features (pos 2, sentence 1) |  passages discussing real estate | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | 'menu' features (pos 3) — push score DOWN | the word "menu" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |
| [L1:F12253](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) | 3 | 'menu' features (pos 3) — push score DOWN |  the word 'menu' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) |
| [L3:F3573](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) | 3 | 'menu' features (pos 3) — push score DOWN | the word "menu" often in conjunction with interface elements | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) |
| [L2:F3648](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) | 3 | 'menu' features (pos 3) — push score DOWN | code snippets related to menus and restaurants | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) |
| [L0:F5128](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) | 3 | 'menu' features (pos 3) — push score DOWN |  the word "words" or words that are similar in meaning (word, Word, phrases, matrix) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 4 | 'will' and other generic features (pos 4) — push score DOWN |  the word "will." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L2:F188](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) | 4 | 'will' and other generic features (pos 4) — push score DOWN | the word "will" in various contexts, sometimes alongside words related to consequences or legal matters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) |
| [L0:F4523](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) | 3 | 'will' and other generic features (pos 4) — push score DOWN | the word "domestic" and words associated with globalism | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) |
| [L0:F6649](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) | 3 | Misc early-layer positive contributors |  the word "Title" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) |
| [L4:F7643](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7643) | 5 | Misc early-layer positive contributors |  words related to providing assistance or describing results | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7643) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'contradiction' is not one of the top-k next-token can |
| 3 | `get_top_features` | 10 features; top: L2:8776 de=0.523 |
| 4 | `inspect_feature` ×10 | L2:8776, L0:2108, L1:12253, L0:8046, L1:3691, L0:7443, L3:3573, L0:6649, L0:7404, L4:7998 |
| 5 | `get_top_features` | 20 features; top: L2:8776 de=0.523 |
| 6 | `inspect_feature` ×10 | L2:3648, L2:188, L2:3059, L0:5128, L0:4523, L17:451, L2:11317, L4:7643, L0:9990, L0:13280 |
| 7 | `get_upstream_features` | L16:F10989 (de=-10.38) +4 more |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F8776@2` | ❌ error | — | — | Trace upstream from L2:F8776 (finance/property law words) to identify the input … |
| SA-2 | `L1:F3691@2` | ❌ error | — | — | Trace upstream from L1:F3691 (word "recording" in scientific context) to identif… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F3691@2, k=5 → Emb:" recorded"@2 (de=24.75) +4 more |
| 2 | `get_upstream_features` | L2:F8776@2, k=5 → Emb:" recorded"@2 (de=19.50) +4 more |
| 3 | `get_upstream_features` | L0:F7443@2, k=5 → Emb:" recorded"@2 (de=22.62) +4 more |
| 4 | `get_upstream_features` | L0:F6649@3, k=5 → Emb:" menu"@3 (de=14.38) +4 more |

### Build

`build_circuit` → 10 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 57,641 | 4,328 | 182,082 | 0 | $0.0334 | — | — |
| **Total** | | **57,641** | **4,328** | **182,082** | **0** | **$0.0334** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 12s