# Circuit Oracle Report
**Date:** 2026-07-28 07:23:03 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven primarily by mid-layer features that literally read the "Conspiracy" / "Conspiracy theorists" prefix (positions 1-2), together with credit-card ("MasterCard"), and a "chip" feature — not by generic negation signals.

**Confidence:** 7

**Reasoning:** Contrary to the user's hypothesis, the circuit does NOT rely on spurious negation or generic "no/not" features. The top direct-effect features are content-specific:

1. **Conspiracy recognition is the dominant signal.** L8:F12761 ("words associated with the QAnon conspiracy theory," pos 3, direct_effect = -0.1602) and L3:F9739 ("words related to conspiracies," pos 2, direct_effect = -0.3477 — the LARGEST in absolute terms) both fire on the actual "Conspiracy theorists" tokens. Their upstream traces hit the literal "Cons" / "piracy" embeddings (e.g., L2:F16241 gets direct_effect 17.25 from the "Cons" embedding at pos 1). These features are the strongest single contributors to the probe score.

2. **MasterCard / payment / "invest" features** (L7:F1062 "credit cards/loans/spending" at pos 6, L2:F15808 "credit cards and payment" at pos 6, L1:F8696 "invest" at pos 8) all trace cleanly to the "Card" / "Master" / "investing" embeddings, not to negation.

3. **"Chip" feature** (L2:F16230 "semiconductor chips and devices," pos 11) traces to the literal " chip" embedding (direct_effect 27) and L1:F9693 ("gambling/card game terminology") — i.e., it activates on the physical-chip word, not on negation.

4. The user's "negation words" hypothesis is weakly supported: only L4:F1602 ("intense interest/enthusiasm/hobby" at pos 3) and a couple of L0 function-word detectors (L0:F11375 "is," L0:F3635 "that," L0:F8444 "to") are generic, and they have small direct effects (< 0.15). No feature in the top 20 has a "negation" autointerp label; the closest is the L3:F9739 conspiracy feature which actually has NEGATIVE direct_effect, so it pushes the probe TOWARD a particular class using the conspiracy content, not toward contradiction via negation.

The "No one thinks" sentence in the prompt is the natural candidate for a negation-only artifact, but the attribution path does not go through any negation detector — the circuit reads the topic (conspiracy/MasterCard/chip) and routes the score from there. The user's concern is not supported by this attribution graph.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F16015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) | 1 | Emb: Conspiracy (pos 1-2) | the prefix "cons" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) |
| [L0:F2115](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) | 2 | Emb: Conspiracy (pos 1-2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) |
| [L2:F16241](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) | 2 | Conspiracy / "Conspiracy theorists" recognition (L0-L3) |  partial strings of the word "constructor" or words ending in "dering" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) |
| [L2:F1741](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1741) | 2 | Conspiracy / "Conspiracy theorists" recognition (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1741) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | Conspiracy / "Conspiracy theorists" recognition (L0-L3) |  words related to conspiracies | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L2:F16028](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) | 3 | Conspiracy / "Conspiracy theorists" recognition (L0-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) |
| [L8:F12761](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) | 3 | Conspiracy / "Conspiracy theorists" recognition (L0-L3) |  words associated with the QAnon conspiracy theory | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) |
| [L2:F15808](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15808) | 6 | MasterCard / credit-card / payment features (L1-L7) | mentions of credit cards and payment. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15808) |
| [L4:F4153](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4153) | 6 | MasterCard / credit-card / payment features (L1-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4153) |
| [L6:F10189](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10189) | 6 | MasterCard / credit-card / payment features (L1-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10189) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 6 | MasterCard / credit-card / payment features (L1-L7) |  words and phrases related to credit cards, loans, spending, gambling, and money in general. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |
| [L1:F8696](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) | 8 | MasterCard / credit-card / payment features (L1-L7) |  the word "invest" and its derivatives | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) |
| [L1:F9693](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9693) | 11 | Chip / "invest" / "electronic cash" features (L1-L4) | This neuron looks for gambling and card game-related terminology. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9693) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Chip / "invest" / "electronic cash" features (L1-L4) |  mentions of semiconductor chips and devices | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L0:F3937](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3937) | 11 | Chip / "invest" / "electronic cash" features (L1-L4) |  the phrase "from scratch", sometimes activating on words nearby | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3937) |
| [L4:F1602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) | 3 | Chip / "invest" / "electronic cash" features (L1-L4) |  words or phrases that indicate intense interest or enthusiasm, often associated with hobbies or preferences | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | Chip / "invest" / "electronic cash" features (L1-L4) | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | Chip / "invest" / "electronic cash" features (L1-L4) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 24 | Chip / "invest" / "electronic cash" features (L1-L4) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F15958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15958) | 3 | Generic / whitespace / mixed function-word features |  the word "tomorrow" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15958) |
| [L0:F4287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) | 1 | Generic / whitespace / mixed function-word features |  words or phrases that relate to marketing or advertising | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) |
| [L0:F12377](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12377) | 4 | Generic / whitespace / mixed function-word features |  large gaps of whitespace | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12377) |
| [L0:F4802](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4802) | 4 | Generic / whitespace / mixed function-word features |  large blocks of whitespace and numbers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4802) |
| [L1:F13684](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) | 3 | Generic / whitespace / mixed function-word features |  the word "theory" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L3:9739 de=-0.348 |
| 3 | `inspect_feature` ×19 | L3:9739, L2:16230, L7:1062, L0:3635, L1:13684, L4:1602, L0:16015, L2:16241, L0:4287, L8:12761, L0:15958, L0:11375, L1:8696, L0:4802, L2:15808, L0:12377, L0:3937, L0:8444, L1:9693 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F12761@3` | ❌ error | — | — | Trace the conspiracy/QAnon feature (L8:F12761 at pos 3) upstream. This is the to… |
| SA-2 | `L3:F9739@2` | ❌ error | — | — | Trace the conspiracy words feature (L3:F9739 at pos 2) upstream. What does it se… |
| SA-3 | `L7:F1062@6` | ❌ error | — | — | Trace the credit card/money feature (L7:F1062 at pos 6) upstream. Does it actual… |
| SA-4 | `L2:F16230@11` | ❌ error | — | — | Trace the chip/semiconductor feature (L2:F16230 at pos 11) upstream. It fires on… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L8:F12761@3, k=15 → Emb:" theorists"@3 (de=4.56) +14 more |
| 2 | `get_upstream_features` | L3:F9739@2, k=15 → Emb:"Cons"@1 (de=8.75) +14 more |
| 3 | `get_upstream_features` | L7:F1062@6, k=15 → Emb:"Card"@6 (de=14.00) +14 more |
| 4 | `get_upstream_features` | L2:F16230@11, k=15 → Emb:" chip"@11 (de=27.00) +14 more |
| 5 | `get_upstream_features` | L2:F16028@3, k=10 → Emb:" theorists"@3 (de=11.75) +9 more |
| 6 | `get_upstream_features` | L7:F13859@3, k=10 → Emb:"piracy"@2 (de=5.22) +9 more |
| 7 | `get_upstream_features` | L2:F16241@2, k=10 → Emb:"Cons"@1 (de=17.25) +9 more |
| 8 | `get_upstream_features` | L4:F1602@3, k=10 → Emb:" theorists"@3 (de=3.23) +9 more |
| 9 | `get_upstream_features` | L1:F8696@8, k=10 → Emb:" investing"@8 (de=21.88) +9 more |
| 10 | `get_upstream_features` | L0:F1847@3, k=10 → Emb:" theorists"@3 (de=10.00) +9 more |

### Build

`build_circuit` → 6 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 50,387 | 4,671 | 177,765 | 0 | $0.0314 | — | — |
| **Total** | | **50,387** | **4,671** | **177,765** | **0** | **$0.0314** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 1s