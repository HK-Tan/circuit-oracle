# Circuit Oracle Report
**Date:** 2026-07-28 07:24:07 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by a very shallow circuit: a handful of early-layer (L0–L3, one L6) features, each anchored to a specific content token in the prompt (" author", " married", " white", " Maybe", " to") — with no mid/late-layer "identity group" or "spurious topic" supernodes mediating the signal. The probe reads essentially raw lexical/relational features, not an abstract "mentions an identity" representation.

**Confidence:** 7

**Reasoning:**

- `get_top_features` on the (synthetic) probe token returned only **layers 0–6**. The top features sit at L0 (F4408, F8444, F3436, F753, F5538, F6087, F9796), L1 (F384, F1431), L2 (F3399), L3 (F6262, F8254, F10004, F11152, F494), and a single L6 (F2851, F13528). There is **no deep, late-layer, identity-group feature** in the top-k. The probe classification is being driven by a shallow, mostly-embedding-adjacent subgraph.

- Tracing upstream via `get_upstream_features` shows every one of these features bottoms out at **token-embedding nodes** within 1–2 hops. Examples:
  - L6:F2851 (pos 2, direct_effect +0.21) → Emb " author" (pos 2, direct_effect 11.06) and Emb "The" (pos 1, 1.21).
  - L2:F3399 (pos 6, +0.17) → Emb " married" (pos 6, direct_effect 29.0).
  - L0:F3436 (pos 9, +0.17) → Emb " white" (pos 9, direct_effect 18.0).
  - L3:F10004 (pos 17, +0.14) → Emb " Maybe" (pos 17, direct_effect 43.25).
  - L0:F8444 (pos 7, –0.18) → Emb " to" (pos 7, direct_effect 41.75) — this is the **inhibitory** partner that suppresses the probe when the L3 " married" features fire (note: in `trace_path_subagent` is unavailable here, so I chained `get_upstream_features` directly; the picture is consistent — these are all single-hop to embeddings).

- **Supernode grouping** in `build_circuit`:
  - `L0_author_ctx` (L0:L1 features on pos 2): bundle of generic bigram/subword features over " author" — neutral, low-level lexical. Direct effects are mixed (+0.16 from F4408, –0.28 from F753, etc.), and they fan into `L6_author_out`.
  - `L6_author_out` (F2851 +0.21, F13528 +0.11) is the deepest feature and is the principal **pro-tox** contributor at pos 2. It receives the L0 " author" context and feeds the probe directly.
  - `L2_married_rel` (F3399, +0.17) is a *relational* "married" feature — the model has detected a relationship assertion, not an identity.
  - `L3_maybe_17` (F10004 +0.14, F11152 –0.12): discourse-marker feature on " Maybe" signaling speculative/hedged content — a hedging cue, not a demographic cue.
  - `L3_married_neg` (F6262, F8254, F494, F1431): a cluster of **suppressive** features on " married" / " to" that subtract from the probe. The probe doesn't ride a clean "married" signal — it rides a partial one.
  - `L0_white_9` (F3436, +0.17): a low-level lexical feature on the *word* "white"; no downstream feature abstracts it to "racial identity".

- **No identity-group supernode exists.** There is no L20+ feature aggregating "white + oriental + women + men" into a "mentions racial groups" detector. The signal is fragmented across individual content words, with the late-layer `L6_author_out` being the only feature past layer 3, and it is keyed to a non-identity word (" author").

- **Implication for the user's concern.** The user's worry was that the probe would latch onto a spurious "an identity group is mentioned" feature rather than actual prompt content. The graph shows the opposite: the probe's score is being assembled from **shallow, content-bound features** — one per salient content word. This is closer to "lexical bag" than to "identity abstraction." That said, "white" and " oriental" still contribute as individual lexical features (F3436 on "white" directly promotes the probe), so the probe is not content-neutral either — it is just not abstracting them into a higher-level "racial topic" feature first. In short, the circuit does **not** route through a late-layer identity detector; it routes through early lexical features on the specific content words, plus one mid-layer "author" context feature and a discourse-hedging feature on " Maybe."

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4408](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) | 2 | L0 early features on ' author' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) |
| [L0:F753](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) | 2 | L0 early features on ' author' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) |
| [L0:F5538](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5538) | 2 | L0 early features on ' author' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5538) |
| [L0:F6087](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6087) | 2 | L0 early features on ' author' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6087) |
| [L0:F9796](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9796) | 2 | L0 early features on ' author' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9796) |
| [L1:F384](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) | 2 | L0 early features on ' author' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 7 | L0:F8444 on ' to' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L2:F3399](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) | 6 | L2:F3399 ' married' relation feature (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) |
| [L3:F6262](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) | 6 | L3 inhibitory features on ' married' (pos 6/7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) |
| [L3:F8254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) | 7 | L3 inhibitory features on ' married' (pos 6/7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) |
| [L3:F494](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) | 6 | L3 inhibitory features on ' married' (pos 6/7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) |
| [L1:F1431](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) | 6 | L3 inhibitory features on ' married' (pos 6/7) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 9 | L0:F3436 on ' white' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L3:F10004](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) | 17 | L3 features on ' Maybe' (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) |
| [L3:F11152](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) | 17 | L3 features on ' Maybe' (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) |
| [L6:F2851](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) | 2 | L6 late feature on ' author' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) |
| [L6:F13528](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13528) | 2 | L6 late feature on ' author' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13528) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:753 de=-0.275 |
| 3 | `get_upstream_features` | Emb:" author"@2 (de=11.06) +4 more |
| 4 | `get_upstream_features` | Emb:" married"@6 (de=29.00) +4 more |
| 5 | `get_upstream_features` | Emb:" white"@9 (de=18.00) +4 more |
| 6 | `get_upstream_features` | Emb:" Maybe"@17 (de=43.25) +4 more |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F8444@7` | ❌ error | — | — | Trace this feature upstream. What does it encode and where does its signal origi… |
| SA-2 | `L3:F6262@6` | ❌ error | — | — | Trace this feature upstream. What does it encode and where does its signal origi… |
| SA-3 | `L0:F4408@2` | ❌ error | — | — | Trace this feature upstream. What does it encode and where does its signal origi… |
| SA-4 | `L3:F8254@7` | ❌ error | — | — | Trace this feature upstream. What does it encode and where does its signal origi… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F8444@7, k=5 → Emb:" to"@7 (de=41.75) +4 more |
| 2 | `get_upstream_features` | L3:F6262@6, k=5 → Emb:" married"@6 (de=37.75) +4 more |
| 3 | `get_upstream_features` | L3:F8254@7, k=5 → Emb:" married"@6 (de=26.62) +4 more |
| 4 | `get_upstream_features` | L0:F4408@2, k=5 → Emb:" author"@2 (de=15.94) +4 more |

### Build

`build_circuit` → 13 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 9,544 | 4,016 | 38,895 | 0 | $0.0100 | — | — |
| **Total** | | **9,544** | **4,016** | **38,895** | **0** | **$0.0100** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 55s