# Circuit Oracle Report
**Date:** 2026-07-28 07:19:29 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven primarily by a late-layer negation feature (L16:F6800, "not"/"no"/contractions, direct_effect=+0.44) sitting on the " not" token at pos 17, with secondary support from lexical "recorded/recording/record" detectors at pos 2 — together these purely surface-level, lexical signals constitute the entire positive drive toward the contradiction classification.

**Confidence:** 8

**Reasoning:** The circuit is short and shallow, terminating at the probe-output node (layer=26). The two supernodes feeding it are:

1. **late_negation_L16 supernode** — anchored by L16:F6800 ("negations 'not', 'no', and contractions with 't'", frac_nonzero=0.031, activation=22.6, direct_effect=+0.44 on the probe). It is fed by L15:F11794 (direct_effect=+6.03 from " not" embedding), L13:F102, L3:F3534, and L4:F4492 ("negations in various languages", frac_nonzero=0.038). Upstream tracing shows the dominant source is the **" not" embedding at pos 17** (direct_effect=+11.8 into L16:F6800; direct_effect=+33.5 into L0:F4958), with smaller contributions from " do" (pos 16, +5.4) and " menus" (pos 15, -1.0). L0:F4958 ("the word 'not'", frac_nonzero=0.018) is a direct early "not" detector that also pulls in " obtain" (pos 10).

2. **recorded_lexical_L0_L1_L2 supernode** — a cluster of surface-form detectors on " recorded" at pos 2: L0:F7443 ("the word 'record'…", frac_nonzero=0.015, direct_effect=+0.58), L1:F3691 ("the word 'recording'…", frac_nonzero=0.007, direct_effect=+0.82), L2:F8776 (finance/property, frac_nonzero=0.011, direct_effect=+0.64), L1:F12253 ("menu", -0.47), L0:F2108 ("menu", -0.63), and L0:F13938 ("wild", -0.37). Upstream tracing on L1:F3691 and L2:F8776 confirms they are almost entirely driven by the **" recorded" embedding at pos 2** (direct_effects of +24.75 and +19.5 respectively), with a minor boost from `<bos>` and a small inhibition from the "A" embedding (pos 1, ~-1.3 to -1.6).

**Mechanism.** Both branches of the circuit are pure lexical, not semantic. The probe is activated by (a) the literal word "not" — specifically the surface form in the phrase "do not provide" at the end of the second sentence — and (b) a cluster of surface-form detectors on the literal word "recorded" in the first sentence. There is no feature in the circuit that encodes the actual semantic content of the passage (e.g., the contradiction between "will provide information" in sentence 1 and "do not provide any information" in sentence 2, the topic of accessibility, the concept of negation-of-promise, or any entity/relation beyond the raw word). The semantic contradiction is being inferred from a few bag-of-words triggers: the presence of the negative-polarity word "not" plus the word "record"/"menu". This is exactly the kind of **spurious, surface-feature-driven shortcut** the user suspected: a negation-word detector in late layers (L13–L16) carries the bulk of the positive signal into the probe, with the "recorded" lexical features acting as secondary positive evidence and the unrelated "wild" feature (L0:F13938) being the main negative contributor. The probe's classification therefore appears to rely on negation/keyword presence rather than on a real entailment-contradiction computation over the prompt's meaning.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 17 | Late-layer negation feature: "not"/"no"/contractions on " not" at pos 17 |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 17 | Late-layer negation feature: "not"/"no"/contractions on " not" at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L13:F102](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) | 17 | Late-layer negation feature: "not"/"no"/contractions on " not" at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 17 | Late-layer negation feature: "not"/"no"/contractions on " not" at pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Late-layer negation feature: "not"/"no"/contractions on " not" at pos 17 | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Early "not" detector at pos 17 |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | Lexical "recorded/recording/record" detectors at pos 2 |  words related to finance and property law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | Lexical "recorded/recording/record" detectors at pos 2 |  the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | Lexical "recorded/recording/record" detectors at pos 2 | the word "record" appearing in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | Lexical "recorded/recording/record" detectors at pos 2 | the word "menu" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |
| [L1:F12253](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) | 3 | Lexical "recorded/recording/record" detectors at pos 2 |  the word 'menu' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) |
| [L0:F13938](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13938) | 2 | Lexical "recorded/recording/record" detectors at pos 2 | the word "wild" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13938) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'contradiction' is not one of the top-k next-token can |
| 3 | `get_top_features` | 10 features; top: L1:3691 de=0.824 |
| 4 | `inspect_feature` ×10 | L1:3691, L2:8776, L0:2108, L0:7443, L16:6800, L0:4958, L4:4492, L0:13938, L1:12253, L4:2422 |
| 5 | `get_upstream_features` | Emb:" not"@17 (de=11.81) +11 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F6800@17` | ❌ error | — | — | Trace the path from L16:F6800 (a negation-feature "not"/"no"/contractions). This… |
| SA-2 | `L1:F3691@2` | ❌ error | — | — | Trace the path from L1:F3691 (a feature about "recording" / "record" word). This… |
| SA-3 | `L2:F8776@2` | ❌ error | — | — | Trace the path from L2:F8776 (finance/property-law related feature). This drives… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F3691@2, k=12 → Emb:" recorded"@2 (de=24.75) +11 more |
| 2 | `get_upstream_features` | L2:F8776@2, k=12 → Emb:" recorded"@2 (de=19.50) +11 more |
| 3 | `get_upstream_features` | L0:F4958@17, k=10 → Emb:" not"@17 (de=33.50) +9 more |

### Build

`build_circuit` → 11 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 43,752 | 3,842 | 94,877 | 0 | $0.0234 | — | — |
| **Total** | | **43,752** | **3,842** | **94,877** | **0** | **$0.0234** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 19s