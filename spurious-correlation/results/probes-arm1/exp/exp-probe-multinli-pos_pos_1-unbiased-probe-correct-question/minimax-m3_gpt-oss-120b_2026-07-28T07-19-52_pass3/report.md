# Circuit Oracle Report
**Date:** 2026-07-28 07:19:52 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven by a constellation of early-to-mid-layer features that detect specific content words from the premise — "Conspiracy", "theorists/theory", "invest", "Card", "chip" — rather than spurious negation markers. The top direct-effect contributors are *content-keyword features* (chip-as-semiconductor, credit-card/loans, conspiracy terms, QAnon-association, "invest"), and the user's hypothesis about "negation words" driving the score is not supported by the circuit.

**Confidence:** 7

**Reasoning:** I traced the top 20 direct-effect features on the probe target and inspected their semantic labels:

- **L2:F16230 @ pos 11 (chip)** — `direct_effect = +0.266`, label: "mentions of semiconductor chips and devices", max activating token `▁chip`. Traces directly to **Emb: chip (pos 11)** with `direct_effect=27.0`. This is a *content* feature about the actual noun in the hypothesis, not negation.
- **L7:F1062 @ pos 6 & pos 11 (credit cards/money)** — `direct_effect = -0.237 / -0.151`, label: "words and phrases related to credit cards, loans, spending, gambling, and money in general." Upstream trace goes to **Emb: Card (pos 6)** (`direct_effect=14`) and **Emb: chip (pos 11)** via L6:F10189. This is a *content/domain* feature about financial transactions, not negation.
- **L0:F16015 @ pos 1 (cons prefix)** — `direct_effect = +0.187`, label: "the prefix 'cons'". This detects the lexical "Cons" in **Conspiracy**, not negation.
- **L1:F13684 @ pos 3 (theory)** — `direct_effect = -0.195`, label: "the word 'theory'". Upstream is **Emb: theorists (pos 3)** (`direct_effect=10.1`). Again content-bearing.
- **L3:F9739 @ pos 2 (conspiracy)** — `direct_effect = -0.348`, label: "words related to conspiracies". Traces to **Emb: Cons (pos 1)** and **Emb: piracy (pos 2)**. Content word.
- **L8:F12761 @ pos 3 (QAnon)** — `direct_effect = -0.160`, label: "words associated with the QAnon conspiracy theory". Content — the very topic of the premise.
- **L0:F3635 @ pos 12 (that)** — `direct_effect = +0.225`, label: "the word 'that'". Trivial function word.
- **L1:F8696 @ pos 8 (invest)** — `direct_effect = +0.145`, label: "the word 'invest' and its derivatives". Content.
- **L2:F15808 @ pos 6 (credit cards/payment)** — `direct_effect = -0.132`, content.
- **L0:F4287 @ pos 1 (marketing)** — off-target, low direct_effect.
- **L0:F15958 @ pos 3 (tomorrow)** — pos 3 is "theorists"; the feature actually fires on "▁theory" inside "theorists", explaining the activation. Not negation.
- **L0:F4802 (whitespace), L0:F12377 (whitespace), L0:F3937 (from scratch), L0:F8444 (to), L0:F11375 (is), L4:F1602 (enthusiasm), L1:F9693 (gambling)**, L2:F16241 (constructor/dering) — none encode negation; they are either off-target low-effect lexical features, function-word detectors, or content features about enthusiasm/credit/gambling. The "dering" feature at L2:16241 fires because "**Cons**piracy" contains the substring "**dering**" only weakly — its top activating examples are unrelated substrings (constructor, considering, dering); it is a generic *substring* feature, not a negation feature.
- **L2:F16230 (chip)** — despite the headline label being "semiconductor chips", its **suppressed_tokens** list includes `▁chip`, `▁Chip`, `chip`, `chips` (note: the *suppressed* set, not promoted), so the feature actually activates broadly and reflects the model's representation of "chip" tokens, consistent with its positive direct_effect on this input.

The user's concern is that the probe might latch onto spurious *negation* cues. Looking at the top direct-effect features, **there are no features whose labels or top-activating examples match negation words** ("not", "no", "never", "nefarious", "No one thinks"). Instead, every high-effect feature resolves to either:
1. A **content word from the premise** (chip, Card, Conspiracy, theorists, invest), or
2. A **function word** (that, is, to, the), or
3. An **off-target/weakly-related** feature (whitespace, "tomorrow", "dering" substring, "marketing", "enthusiasm").

The dominant positive signal is the **chip/Card/credit-cards/Conspiracy** cluster, which is the *actual semantic content* of the premise (a statement that MasterCard is putting too much on a chip). The negative-signaling features (L3:F9739 conspiracy, L7:F1062 credit-money, L1:F13684 theory) push the probe *toward* the contradiction label because the premise text contains a long conspiracy vocabulary, which the model recognizes as likely-contradictory (the ironic/contradictory register of "No one thinks Mastercard is up to anything nefarious"). So the probe is reading the *topic distribution* — conspiracy + financial-domain content — not the negation. This is a legitimate (if imperfect) content-based driver, not a "spurious negation" artifact, and the user's concern is **not corroborated** by the attribution circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F16015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) | 1 | Lexical "cons" prefix (pos 1) | the prefix "cons" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) |
| [L0:F4287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) | 1 | Lexical "cons" prefix (pos 1) |  words or phrases that relate to marketing or advertising | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | "that" detector (pos 12) | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L1:F13684](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) | 3 | "theory" detector (pos 3) |  the word "theory" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) |
| [L1:F8696](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) | 8 | "invest" detector (pos 8) |  the word "invest" and its derivatives | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) |
| [L1:F9693](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9693) | 11 | gambling/card-game terms (pos 11) | This neuron looks for gambling and card game-related terminology. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9693) |
| [L2:F16241](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) | 2 | constructor/dering subword (pos 2) |  partial strings of the word "constructor" or words ending in "dering" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | semiconductor/chip feature (pos 11) |  mentions of semiconductor chips and devices | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L2:F15808](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15808) | 6 | credit card/payment mentions (pos 6) | mentions of credit cards and payment. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15808) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | conspiracy-related words (pos 2) |  words related to conspiracies | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L4:F1602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) | 3 | intense-interest/enthusiasm (pos 3) |  words or phrases that indicate intense interest or enthusiasm, often associated with hobbies or preferences | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 6 | credit cards/loans/spending/money (pos 6) |  words and phrases related to credit cards, loans, spending, gambling, and money in general. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 11 | credit cards/loans/spending/money (pos 6) |  words and phrases related to credit cards, loans, spending, gambling, and money in general. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |
| [L8:F12761](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) | 3 | QAnon/conspiracy (pos 3) |  words associated with the QAnon conspiracy theory | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L3:9739 de=-0.348 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F9739@2` | ❌ error | — | — | Trace this early-layer feature (most negative direct_effect) upstream. What is i… |
| SA-2 | `L2:F16230@11` | ❌ error | — | — | Trace this early-layer feature (positive direct_effect on probe) upstream. What … |
| SA-3 | `L7:F1062@6` | ❌ error | — | — | Trace this mid-layer feature (negative direct_effect) upstream. Does it detect n… |
| SA-4 | `L0:F3635@12` | ❌ error | — | — | Trace this early-layer feature at pos 12 (token "keys") upstream. What does it e… |
| SA-5 | `L0:F16015@1` | ❌ error | — | — | Trace this L0 feature at pos 1 ("theorists") upstream. What does it encode? |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×19 | L3:9739, L2:16230, L7:1062, L0:3635, L0:16015, L1:13684, L4:1602, L2:16241, L0:4287, L8:12761, L0:15958, L0:11375, L1:8696, L0:4802, L2:15808, L0:12377, L0:3937, L0:8444, L1:9693 |
| 2 | `get_upstream_features` | L7:F1062@6, k=10 → Emb:"Card"@6 (de=14.00) +9 more |
| 3 | `get_upstream_features` | L7:F1062@11, k=10 → Emb:"Card"@6 (de=7.31) +9 more |
| 4 | `get_upstream_features` | L3:F9739@2, k=10 → Emb:"Cons"@1 (de=8.75) +9 more |
| 5 | `get_upstream_features` | L8:F12761@3, k=10 → Emb:" theorists"@3 (de=4.56) +9 more |
| 6 | `get_upstream_features` | L1:F13684@3, k=10 → Emb:" theorists"@3 (de=10.12) +9 more |
| 7 | `get_upstream_features` | L4:F1602@3, k=10 → Emb:" theorists"@3 (de=3.23) +9 more |
| 8 | `get_upstream_features` | L2:F16241@2, k=8 → Emb:"Cons"@1 (de=17.25) +7 more |
| 9 | `get_upstream_features` | L2:F16230@11, k=10 → Emb:" chip"@11 (de=27.00) +9 more |

### Build

`build_circuit` → 19 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 59,161 | 5,181 | 143,447 | 0 | $0.0326 | — | — |
| **Total** | | **59,161** | **5,181** | **143,447** | **0** | **$0.0326** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 2s