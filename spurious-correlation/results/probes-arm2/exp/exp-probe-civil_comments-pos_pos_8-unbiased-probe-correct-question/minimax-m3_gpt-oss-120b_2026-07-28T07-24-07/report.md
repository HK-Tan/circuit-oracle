# Circuit Oracle Report
**Date:** 2026-07-28 07:24:07 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_8 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven primarily by shallow, content-agnostic syntactic features — most notably L0:F11375 (a copula "is" detector firing at positions 5 and 14), L0:F3635 ("that" complementizer at pos 6), L0:F880 (pronoun "it" at pos 7), and L0:F7253/L2:F8909 ("The problem" NP detector) — rather than by features that encode the meaning of the toxic content (e.g. "false religion", "Allah is Lucifer"). The genuinely content-bearing nodes (Islam-features at L6-L8, the late-layer L12:F7779 on "false religion") carry comparatively small direct effects (≤0.10), while the function-word detectors carry the largest direct effects in the graph (0.226, 0.118, 0.094, 0.084).

**Confidence:** 5

**Reasoning:** Tracing the top-20 direct-effect features back to their embedding inputs reveals that 5 of the 7 strongest drivers (L0:F11375@5 [0.226], L0:F3635@6 [0.118], L0:F7253@2 [0.094], L0:F880@7 [0.084], L0:F11375@14 [0.083]) are *generic* L0 token detectors. F11375 fires on "is" at two positions (5 and 14) with direct_effect +0.226 and +0.083; its sole upstream signal is the embedding of " is" (direct_effect 31.9) — it is a pure copula detector, not a content feature. F3635 (direct_effect +0.118) is fed almost entirely by the "that" embedding (direct_effect 40.5). F880 (direct_effect +0.084) is fed by the "it" embedding (44.0). F7253 (direct_effect +0.094) and F8909 (direct_effect +0.069) both fire on "The problem" and are driven by the "The" and "problem" embeddings. The "with" path (F2158, F16106, F8595, F9503) is *inhibitory* (direct_effects -0.097, -0.071, -0.076, -0.095) — it actively *suppresses* the probe. By contrast, the features that *do* target the actual toxic content — F7282, F16294, F5783, F11758 on "Islam" (pos 4) and F7779 on "false religion" (pos 11) — have direct_effects of only ~0.07–0.10, roughly half the magnitude of the top function-word feature. L8:F5783 on "Islam" is even negative (direct_effect +0.087 upstream from F7282 but driven by embedding "with" at -1.45). This pattern is consistent with the user's concern: the probe appears to be classifying toxicity from shallow, identity-/religion-adjacent structural cues ("is"/"that"/"it" framing a copular clause, the noun phrase "The problem") rather than from semantically meaningful features tied to the hateful content. However, the L0 detectors are still "content-agnostic syntactic" rather than "identity-group" features per se — the indirect path through them is amplified by the copular "X is Y" template, which the model associates with identity assertions. A caveat: this is a *probe* attribution graph (a linear classifier on residual stream), not the model's own output distribution, so the circuit may be partly an artifact of the probe's training data. With no `inspect_feature` available to confirm frac_nonzero and semantic labels, and given the top-20 view is partial, the confidence is moderate rather than high.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 5 | L0 copula 'is' detector (fires on pos 5 and 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 14 | L0 copula 'is' detector (fires on pos 5 and 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 6 | L0 'that' complementizer detector (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 7 | L0 pronoun 'it' detector (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |
| [L0:F7253](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7253) | 2 | L0 'The problem' NP-start detector (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7253) |
| [L2:F8909](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8909) | 2 | L0 'The problem' NP-start detector (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8909) |
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 3 | L0 preposition 'with' detector (pos 3, inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L4:F16106](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/16106) | 3 | L0 preposition 'with' detector (pos 3, inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/16106) |
| [L3:F8595](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8595) | 3 | L0 preposition 'with' detector (pos 3, inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8595) |
| [L7:F9503](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9503) | 3 | L0 preposition 'with' detector (pos 3, inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9503) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 4 | Mid-layer features on 'Islam' (pos 4) — mixed/weak signs | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L8:F16294](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16294) | 4 | Mid-layer features on 'Islam' (pos 4) — mixed/weak signs | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16294) |
| [L8:F5783](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/5783) | 4 | Mid-layer features on 'Islam' (pos 4) — mixed/weak signs | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/5783) |
| [L7:F11758](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11758) | 4 | Mid-layer features on 'Islam' (pos 4) — mixed/weak signs | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11758) |
| [L0:F13885](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) | 4 | Mid-layer features on 'Islam' (pos 4) — mixed/weak signs | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) |
| [L12:F7779](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/7779) | 11 | Late-layer feature on 'false religion' (pos 11) — weak driver | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/7779) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:11375 de=0.226 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F11375@5` | ❌ error | — | — | Trace the path from L0:F11375 at pos 5 (activation 34.25, direct_effect 0.226 — … |
| SA-2 | `L0:F3635@6` | ❌ error | — | — | Trace L0:F3635 at pos 6 (direct_effect +0.118, the 4th strongest driver). What d… |
| SA-3 | `L0:F7253@2` | ❌ error | — | — | Trace L0:F7253 at pos 2 (direct_effect +0.094). What does this feature encode? F… |
| SA-4 | `L0:F880@7` | ❌ error | — | — | Trace L0:F880 at pos 7 (direct_effect +0.084). What does this feature encode? Fo… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F11375@5, k=8 → Emb:" is"@5 (de=31.88) +7 more |
| 2 | `get_upstream_features` | L0:F3635@6, k=8 → Emb:" that"@6 (de=40.50) +7 more |
| 3 | `get_upstream_features` | L0:F7253@2, k=8 → Emb:"The"@1 (de=6.94) +7 more |
| 4 | `get_upstream_features` | L0:F880@7, k=8 → Emb:" it"@7 (de=44.00) +7 more |
| 5 | `get_upstream_features` | L0:F2158@3, k=8 → Emb:" with"@3 (de=32.50) +7 more |
| 6 | `get_upstream_features` | L0:F11375@14, k=8 → Emb:" is"@14 (de=33.25) +7 more |
| 7 | `get_upstream_features` | L7:F9503@3, k=6 → Emb:" problem"@2 (de=7.84) +5 more |
| 8 | `get_upstream_features` | L8:F16294@4, k=6 → Emb:" Islam"@4 (de=3.53) +5 more |
| 9 | `get_upstream_features` | L2:F8909@2, k=5 → Emb:" problem"@2 (de=24.88) +4 more |
| 10 | `get_upstream_features` | L8:F5783@4, k=5 → L6:F7282 (de=3.48) +4 more |
| 11 | `get_upstream_features` | L7:F11758@4, k=5 → L6:F7282 (de=4.28) +4 more |
| 12 | `get_upstream_features` | L12:F7779@11, k=5 → Emb:" false"@10 (de=6.72) +4 more |
| 13 | `get_upstream_features` | L6:F7282@4, k=5 → Emb:" Islam"@4 (de=18.50) +4 more |
| 14 | `get_upstream_features` | L4:F7647@5, k=5 → Emb:" with"@3 (de=2.78) +4 more |

### Build

`build_circuit` → 18 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 17,267 | 4,871 | 46,771 | 0 | $0.0138 | — | — |
| **Total** | | **17,267** | **4,871** | **46,771** | **0** | **$0.0138** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 55s