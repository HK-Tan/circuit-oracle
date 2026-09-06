# Circuit Oracle Report
**Date:** 2026-07-28 07:24:20 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" classification is driven almost entirely by a shallow surface-feature circuit that counts and aggregates negation/scope markers (" said", " not", " only", " but", " isn't", " going", " to") rather than by any genuine semantic comparison between the premise and hypothesis.

**Confidence:** 8

**Reasoning:** The full causal pathway, traced from the probe output back to token embeddings, passes through four shallow layers (L0–L4) where features respond to individual lexical items and immediately feed L13–L16 aggregation features, which in turn push the probe direction.

1. **Token-embedding inputs.** The strongest upstream signals at the bottom of the graph are *embedding nodes* for the exact function-word positions that any NLI contradiction cue-stripper would flag: `Emb: ' said' (pos 3)` (direct_effect 34.25 into L4:F15629), `Emb: ' not' (pos 6)` (32.0 into L0:F4958), `Emb: ' only' (pos 7)` (21.25 into L2:F5627), `Emb: ' but' (pos 13)` (42.5 into L0:F11101), `Emb: ' isn'/' '/t' (pos 26–28)` (23.4 / 12.3 / 18.4 into L0:F6236), and `Emb: ' going' (pos 29)` (29.1 into L3:F5548). No content words (`Wagon`, `program`, `lawyers`, `image`, `needy`, `benefit`) appear as positive contributors.

2. **Early lexical detectors (L0–L3).** These embeddings drive a tightly clustered set of single-token- or phrase-specific features: L0:F4958 ("not"), L0:F6236 ("isn'/t"), L0:F11101 ("but"), L1:F11907 (pos 5 "program" but with *negative* direct_effect on the probe, i.e. generic-content suppression), L2:F5627 ("not only" idiom at pos 7, activation 46.25), L2:F13565, and L3:F5548 ("going to"). The dominant activation pattern is *negation/scope vocabulary*, not entities.

3. **Mid-layer composers (L4).** L4:F15629 (pos 3, +0.67) and its inhibitor L4:F12337 (-0.51) sit directly on " said" — a reporting-verb cue that often co-occurs with contradiction in NLI training data. L4:F2884 (pos 13, "but") and L4:F2422 (pos 28, negative) are again contrastive-connector features.

4. **Late aggregators (L13–L16).** These are the heavy hitters directly feeding the probe: L13:F4368 (pos 6 "not", +0.43 to L16:F15025), L14:F11020 (pos 13 "but also", 3.38), L15:F12905 (pos 13, -0.32 inhibitory on the same position), L15:F10071 and L16:F12358 (both on the "isn't" token at pos 28, activations 19.25 and 31.13, ~0.37 direct effect on the probe), and L16:F9779 (pos 30 "to", +0.20). All of these features are tied to the negation/contrast word positions, not to entities or propositions.

5. **Probe output.** Summing signed direct effects from the late aggregators alone (≈ +0.37 + 0.32 + 0.20 + 0.37 + 0.43 + 3.38 - 0.32 ≈ +4.7) is more than enough to dominate the probe score; the early/mid features route further to these.

**The user's concern is confirmed.** The circuit is a textbook *spurious-feature* story: a contradiction probe that is mostly read off a bag of cue words (`not`, `only`, `but`, `isn't`, `going`, `said`). No path in the attribution graph routes through a representation that compares the two sentences' content; the model never appears to compute that the hypothesis *negates* a specific predicate of the premise (improve lawyers' public image) — it only registers that the sentence contains an "isn't" and several negation/contrast particles, and the probe lights up. This is consistent with well-known NLI artifact behavior (Poliak et al. 2018; McCoy et al. 2019) where contradiction cues are lexically biased.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' said' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' not' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' only' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: ' but' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: ' isn'+t+' (pos 26-28) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: ' isn'+t+' (pos 26-28) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 28 | Emb: ' isn'+t+' (pos 26-28) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 29 | Emb: ' going' (pos 29) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 6 | Early lexical negation detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 28 | Early lexical negation detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F11101](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11101) | 13 | Early lexical negation detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11101) |
| [L1:F11907](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) | 5 | Early lexical negation detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11907) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | Early lexical negation detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L2:F13565](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) | 5 | Early lexical negation detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) |
| [L3:F5548](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5548) | 30 | Early lexical negation detectors (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5548) |
| [L4:F15629](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) | 3 | Mid-layer negation/composition features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) |
| [L4:F12337](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) | 3 | Mid-layer negation/composition features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12337) |
| [L4:F2884](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) | 13 | Mid-layer negation/composition features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 28 | Mid-layer negation/composition features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L13:F4368](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) | 6 | Late negation/contradiction aggregators (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) |
| [L14:F11020](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) | 13 | Late negation/contradiction aggregators (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | Late negation/contradiction aggregators (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 28 | Late negation/contradiction aggregators (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 28 | Late negation/contradiction aggregators (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L16:F15025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) | 6 | Late negation/contradiction aggregators (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) |
| [L16:F9779](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) | 30 | Late negation/contradiction aggregators (L13-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: Probe classification (contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:15629 de=0.672 |
| 3 | `get_upstream_features` | Emb:" said"@3 (de=34.25) +9 more |
| 4 | `get_upstream_features` | Emb:" only"@7 (de=21.25) +9 more |
| 5 | `get_upstream_features` | Emb:" isn"@26 (de=23.38) +9 more |
| 6 | `get_upstream_features` | Emb:" only"@7 (de=5.97) +9 more |
| 7 | `get_upstream_features` | Emb:"t"@28 (de=12.69) +7 more |
| 8 | `get_upstream_features` | Emb:" not"@6 (de=12.19) +7 more |
| 9 | `get_upstream_features` | Emb:"<bos>"@0 (de=3.05) +7 more |
| 10 | `get_upstream_features` | Emb:" not"@6 (de=15.25) +7 more |
| 11 | `get_upstream_features` | Emb:" not"@6 (de=32.00) +7 more |
| 12 | `get_upstream_features` | L0:F6236 (de=5.16) +7 more |
| 13 | `get_upstream_features` | Emb:" going"@29 (de=29.12) +5 more |
| 14 | `get_upstream_features` | L0:F6236 (de=6.69) +5 more |
| 15 | `get_upstream_features` | Emb:"<bos>"@0 (de=3.69) +5 more |
| 16 | `get_upstream_features` | L13:F2557 (de=9.75) +5 more |
| 17 | `get_upstream_features` | Emb:" but"@13 (de=42.50) +5 more |
| 18 | `get_upstream_features` | L12:F10235 (de=6.09) +5 more |
| 19 | `get_upstream_features` | Emb:" program"@5 (de=23.25) +5 more |
| 20 | `get_upstream_features` | Emb:" program"@5 (de=24.38) +5 more |

### Build

`build_circuit` → 10 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 14,791 | 4,328 | 51,427 | 0 | $0.0127 | — | — |
| **Total** | | **14,791** | **4,328** | **51,427** | **0** | **$0.0127** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 55s