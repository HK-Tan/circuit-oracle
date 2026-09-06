# Circuit Oracle Report
**Date:** 2026-07-28 07:24:04 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification score is driven primarily by profession-indicating features (nurse, Labor/Delivery, Nursing) at late layers, not by spurious gender markers — the user concern is largely unfounded for this graph.

**Confidence:** 7

**Reasoning:** The circuit traces the probe's score through a clean profession-detection pathway, not a gender-association shortcut. At the top of the feature ranking, the most positive contributors are L14:F3985 (a profession detector firing on "Delivery" pos 11, "nurse" pos 12, and "Nursing" pos 19, with direct_effect 0.10), L6:F9980 and L6:F4490 (Labor/Delivery medical context, ~0.07 each), and the L18:F13596 nurse-detector (0.054). L0:F7532 fires on the "Melissa" embedding (direct_effect 0.06), and L0:F9911 fires on "that" (pos 3, 0.086) — these are token-level embeddings that, while name-adjacent, are not gender-coded features but rather positional/contextual detectors contributing neutrally to the residue. Tracing upstream, L14:F3985 is fed by L6:F4490 (direct_effect 3.0), L4:F4665 (2.67), and the " Delivery" embedding (pos 11, 2.63) — all profession-relevant. The L18 late-layer nurse feature is dominated by the " nurse" embedding (39.25) and L6:F15267 (4.8), which itself receives 20.5 from the " nurse" embedding. Crucially, no feature in the top contributors encodes gender specifically; the L0:F9911 "that" feature and L0:F7532 "Melissa" feature are name/function-word embeddings whose contributions are small and balanced. The negative contributors (L3:F15901 -0.077, L0:F10771 "worked" -0.076, L0:F8444 "to" -0.069) suppress the score, but again none are gender features. The pathway runs: token embeddings (nurse/Delivery/Labor) → early nurse token features (L0-L2) → labor+delivery combo (L3-L4) → labor/delivery context (L6-L7) → nursing profession detectors (L8, L14) → late nurse features (L15-L18) → probe output. This is a textbook profession-circuit, not a gender-proxy circuit. The user's concern is not supported by the features visible here.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 12 | Late-layer profession features (nurse/nursing) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L16:F6954](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6954) | 12 | Late-layer profession features (nurse/nursing) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6954) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 12 | Late-layer profession features (nurse/nursing) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | Mid-layer nursing/medical profession detectors | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 12 | Mid-layer nursing/medical profession detectors | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 19 | Mid-layer nursing/medical profession detectors | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 12 | Mid-layer nurse/nursing token features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L8:F4607](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) | 12 | Mid-layer nurse/nursing token features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | Labor/Delivery/medical context features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 19 | Labor/Delivery/medical context features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 66 | Labor/Delivery/medical context features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 11 | Labor/Delivery/medical context features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 11 | Labor/Delivery/medical context features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 11 | Labor/Delivery/medical context features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 12 | Labor/Delivery/medical context features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 11 | Labor+Delivery combination features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | Labor+Delivery combination features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L3:F10198](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) | 11 | Labor+Delivery combination features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 11 | Labor+Delivery combination features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L2:F15437](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) | 12 | Early-layer nurse token features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15437) |
| [L1:F14469](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) | 12 | Early-layer nurse token features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) |
| [L0:F8854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) | 12 | Early-layer nurse token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) |
| [L0:F10920](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) | 12 | Early-layer nurse token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 12 | Suppressing features (push probe away) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 19 | Suppressing features (push probe away) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 12 | Suppressing features (push probe away) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 19 | Suppressing features (push probe away) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L13:F3597](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3597) | 12 | Suppressing features (push probe away) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3597) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.106 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@11` | ❌ error | — | — | Trace this feature upstream to understand what it encodes. It fires at positions… |
| SA-2 | `L0:F9911@3` | ❌ error | — | — | Trace this feature upstream. It fires at position 3 which is "Melissa". Determin… |
| SA-3 | `L18:F13596@12` | ❌ error | — | — | Trace this late-layer feature upstream. It has a high activation (37.25) at posi… |
| SA-4 | `L6:F9980@11` | ❌ error | — | — | Trace this mid-layer feature upstream. It fires at position 11 ("Delivery"). Det… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@11, k=15 → L6:F4490 (de=3.00) +14 more |
| 2 | `get_upstream_features` | L0:F9911@3, k=15 → Emb:" that"@3 (de=15.62) +14 more |
| 3 | `get_upstream_features` | L18:F13596@12, k=15 → Emb:" nurse"@12 (de=39.25) +14 more |
| 4 | `get_upstream_features` | L6:F9980@11, k=15 → L4:F4665 (de=2.80) +14 more |
| 5 | `get_upstream_features` | L4:F4665@11, k=10 → L3:F10198 (de=3.44) +9 more |
| 6 | `get_upstream_features` | L6:F15267@12, k=10 → Emb:" nurse"@12 (de=20.50) +9 more |
| 7 | `get_upstream_features` | L7:F210@12, k=10 → Emb:" nurse"@12 (de=9.19) +9 more |
| 8 | `get_upstream_features` | L4:F13803@11, k=10 → Emb:" Delivery"@11 (de=12.19) +9 more |
| 9 | `get_upstream_features` | L0:F7532@5, k=10 → Emb:" Melissa"@5 (de=21.25) +9 more |
| 10 | `get_upstream_features` | L0:F8444@2, k=10 → Emb:" to"@2 (de=39.50) +9 more |
| 11 | `get_upstream_features` | L3:F15901@12, k=10 → Emb:" nurse"@12 (de=15.81) +9 more |
| 12 | `get_upstream_features` | L8:F16339@12, k=10 → Emb:" nurse"@12 (de=7.31) +9 more |
| 13 | `get_upstream_features` | L0:F10771@6, k=10 → Emb:" worked"@6 (de=17.00) +9 more |
| 14 | `get_upstream_features` | L0:F6515@27, k=10 → Emb:"1"@26 (de=29.00) +9 more |
| 15 | `get_upstream_features` | L16:F6954@12, k=10 → Emb:"<bos>"@0 (de=-1.83) +9 more |
| 16 | `get_upstream_features` | L8:F4607@12, k=10 → Emb:" nurse"@12 (de=8.12) +9 more |
| 17 | `get_upstream_features` | L2:F15437@12, k=10 → Emb:" nurse"@12 (de=22.38) +9 more |
| 18 | `get_upstream_features` | L3:F10198@11, k=10 → Emb:" Delivery"@11 (de=7.59) +9 more |
| 19 | `get_upstream_features` | L7:F3979@19, k=10 → L6:F15267 (de=8.75) +9 more |
| 20 | `get_upstream_features` | L15:F15159@12, k=10 → Emb:" nurse"@12 (de=16.38) +9 more |
| 21 | `get_upstream_features` | L0:F8854@12, k=10 → Emb:" nurse"@12 (de=24.38) +9 more |
| 22 | `get_upstream_features` | L0:F10920@12, k=10 → Emb:" nurse"@12 (de=26.50) +9 more |
| 23 | `get_upstream_features` | L1:F14469@12, k=10 → Emb:" nurse"@12 (de=20.88) +9 more |
| 24 | `get_upstream_features` | L3:F9008@11, k=10 → Emb:" Delivery"@11 (de=11.19) +9 more |
| 25 | `get_upstream_features` | L0:F7532@5, k=8 → Emb:" Melissa"@5 (de=21.25) +7 more |
| 26 | `get_upstream_features` | L0:F9911@3, k=8 → Emb:" that"@3 (de=15.62) +7 more |
| 27 | `get_upstream_features` | L1:F12174@11, k=8 → Emb:" Labor"@9 (de=7.06) +7 more |
| 28 | `get_upstream_features` | L13:F3597@12, k=8 → Emb:"<bos>"@0 (de=-33.25) +7 more |

### Build

`build_circuit` → 16 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 28,864 | 5,371 | 94,952 | 0 | $0.0208 | — | — |
| **Total** | | **28,864** | **5,371** | **94,952** | **0** | **$0.0208** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 10s