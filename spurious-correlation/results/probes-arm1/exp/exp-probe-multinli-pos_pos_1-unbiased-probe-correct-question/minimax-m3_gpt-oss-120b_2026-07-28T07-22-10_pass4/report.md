# Circuit Oracle Report
**Date:** 2026-07-28 07:22:10 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" score is driven by a mix of entity/lexical content features and a few light function-word features, with NO dedicated "negation" circuit — the user concern about spurious negation signals is not supported.

**Confidence:** 8

**Reasoning:** The attribution graph is dominated by content-bearing features that track actual prompt content, not by abstract negation detectors:

1. **Conspiracy-entity supernode (L0–L3, direct_effect ±0.22–0.35):** L3:F9739 ("words related to conspiracies", frac_nonzero=0.0076, max_token "pir") and L2:F16230 ("semiconductor chips", frac_nonzero=0.0097) trace cleanly back to the input token embeddings for `piracy` (direct_effect 8.75, 7.625, 27), `Cons` (8.75), `chip` (27), `investing` (21.875), and `that` (41). These are token-anchored content features, not negation detectors. Their promoted tokens (`collaboration`, `cooperation`) and suppressed tokens (`chip`, `comment`, `experiment`) confirm they are entity-recognition features, not polarity features.

2. **MasterCard/finance supernode (L2–L7):** L7:F1062 ("credit cards/loans/spending", frac_nonzero=0.0031) and L6:F10189 ("payment/credit cards/data security") trace back to the `Card` embedding (direct_effect 14, 7.3125). This is entity recognition, not negation.

3. **QAnon supernode (L8, L2):** L8:F12761 ("QAnon conspiracy theory", frac_nonzero=0.0319) traces to the `theorists` embedding (direct_effect 4.56). Again, entity-level content.

4. **The "negation function words" supernode contains NO actual negation features.** Inspection reveals: L4:F1602 = "intense interest/enthusiasm" (anth, ophile, buffs); L2:F16241 = "constructor/dering substring" (CONSIDER, Consider); L1:F13684 = "the word 'theory'"; L0:F11375 = "the word 'is'"; L0:F15958 = "the word 'tomorrow'"; L0:F4802 = "blocks of whitespace and numbers". The word `No` (pos 4) and the negation words `isn't`/`nothing` (pos 13, 14) do not appear as upstream features anywhere in the top direct-effect paths. The only word "No" would have hit is not detected — these are generic lexical detectors firing on tokens the model happened to encode with those detectors.

The two features with the largest individual direct_effects to the probe — L3:F9739 (–0.35, "conspiracy") and L2:F16230 (+0.27, "chip") — are both entity-anchored. The "contradiction" direction is driven by **content mismatch (conspiracy framing vs. corporate financial entity) plus the explicit "Conspiracy theorists" framing**, exactly the linguistic structure the NLI premise/hypothesis probe is designed to detect. The circuit does contain some noise from generic function-word features (low frac_nonzero 0.007–0.043 firing on incidental tokens like `is` and `that`), but these are NOT negation detectors and their direct_effect magnitudes (0.13–0.20) are smaller than the content features. The user's concern about "spurious negation signals" is not borne out by this circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe (Contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | Conspiracy/entity features (L0–L3) — 'conspiracy theorists', 'MasterCard is investing in a chip', 'No one thinks' |  words related to conspiracies | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Conspiracy/entity features (L0–L3) — 'conspiracy theorists', 'MasterCard is investing in a chip', 'No one thinks' |  mentions of semiconductor chips and devices | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L1:F8696](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) | 8 | Conspiracy/entity features (L0–L3) — 'conspiracy theorists', 'MasterCard is investing in a chip', 'No one thinks' |  the word "invest" and its derivatives | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8696) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | Conspiracy/entity features (L0–L3) — 'conspiracy theorists', 'MasterCard is investing in a chip', 'No one thinks' | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F16015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) | 1 | Conspiracy/entity features (L0–L3) — 'conspiracy theorists', 'MasterCard is investing in a chip', 'No one thinks' | the prefix "cons" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16015) |
| [L0:F4287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) | 1 | Conspiracy/entity features (L0–L3) — 'conspiracy theorists', 'MasterCard is investing in a chip', 'No one thinks' |  words or phrases that relate to marketing or advertising | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4287) |
| [L2:F13361](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13361) | 2 | Conspiracy/entity features (L0–L3) — 'conspiracy theorists', 'MasterCard is investing in a chip', 'No one thinks' | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13361) |
| [L7:F1062](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) | 6 | MasterCard/credit-card/money features (L4, L6, L7) — credit cards, banking, payment, financial info |  words and phrases related to credit cards, loans, spending, gambling, and money in general. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1062) |
| [L6:F10189](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10189) | 6 | MasterCard/credit-card/money features (L4, L6, L7) — credit cards, banking, payment, financial info |  phrases related to payment and financial information (especially credit cards) as well as data security | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10189) |
| [L4:F4153](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4153) | 6 | MasterCard/credit-card/money features (L4, L6, L7) — credit cards, banking, payment, financial info |  words or phrases related to currency and banking transactions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4153) |
| [L2:F7725](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) | 6 | MasterCard/credit-card/money features (L4, L6, L7) — credit cards, banking, payment, financial info | the word "card" when used in a technical context | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) |
| [L8:F12761](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) | 3 | Late-layer conspiracy/QAnon features (L8) |  words associated with the QAnon conspiracy theory | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) |
| [L2:F16028](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) | 3 | Late-layer conspiracy/QAnon features (L8) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) |
| [L4:F1602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) | 3 | Function-word/light-lexical features (L0–L4) — 'that', 'is', whitespace, 'Conspiracy' prefix, 'theory' |  words or phrases that indicate intense interest or enthusiasm, often associated with hobbies or preferences | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1602) |
| [L2:F16241](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) | 2 | Function-word/light-lexical features (L0–L4) — 'that', 'is', whitespace, 'Conspiracy' prefix, 'theory' |  partial strings of the word "constructor" or words ending in "dering" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) |
| [L1:F13684](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) | 3 | Function-word/light-lexical features (L0–L4) — 'that', 'is', whitespace, 'Conspiracy' prefix, 'theory' |  the word "theory" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | Function-word/light-lexical features (L0–L4) — 'that', 'is', whitespace, 'Conspiracy' prefix, 'theory' |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F15958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15958) | 3 | Function-word/light-lexical features (L0–L4) — 'that', 'is', whitespace, 'Conspiracy' prefix, 'theory' |  the word "tomorrow" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15958) |
| [L0:F4802](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4802) | 4 | Function-word/light-lexical features (L0–L4) — 'that', 'is', whitespace, 'Conspiracy' prefix, 'theory' |  large blocks of whitespace and numbers | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4802) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Cons (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: piracy (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: theorists (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: MasterCard (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: Card (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: investing (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: chip (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: that (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L3:9739 de=-0.348 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F9739@2` | ❌ error | — | — | Trace the path upstream from L3:F9739 at position 2. This is the most influentia… |
| SA-2 | `L2:F16230@11` | ❌ error | — | — | Trace the path upstream from L2:F16230 at position 11. This feature has a strong… |
| SA-3 | `L7:F1062@6` | ❌ error | — | — | Trace upstream from L7:F1062 at position 6. Strong negative direct_effect (-0.23… |
| SA-4 | `L0:F3635@12` | ❌ error | — | — | Trace upstream from L0:F3635 at position 12. Strong positive direct_effect (0.22… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L3:9739, L2:16230, L7:1062, L0:3635 |
| 2 | `get_upstream_features` | L3:F9739@2, k=12 → Emb:"Cons"@1 (de=8.75) +11 more |
| 3 | `get_upstream_features` | L2:F16230@11, k=12 → Emb:" chip"@11 (de=27.00) +11 more |
| 4 | `get_upstream_features` | L7:F1062@6, k=12 → Emb:"Card"@6 (de=14.00) +11 more |
| 5 | `get_upstream_features` | L0:F3635@12, k=8 → Emb:" that"@12 (de=41.00) +7 more |
| 6 | `inspect_feature` ×10 | L0:16015, L0:4287, L1:13684, L4:1602, L2:16241, L0:15958, L0:11375, L8:12761, L0:4802, L1:8696 |
| 7 | `get_upstream_features` | L7:F1062@11, k=8 → Emb:"Card"@6 (de=7.31) +7 more |
| 8 | `inspect_feature` ×2 | L6:10189, L4:4153 |
| 9 | `get_upstream_features` | L2:F13361@2, k=5 → Emb:"Cons"@1 (de=17.38) +4 more |
| 10 | `get_upstream_features` | L0:F2115@2, k=5 → Emb:"piracy"@2 (de=12.88) +4 more |
| 11 | `inspect_feature` | L0, F2115 → " data reported as a percentage inside brackets, especially in a labora" |
| 12 | `get_upstream_features` | L0:F800@2, k=5 → Emb:"piracy"@2 (de=12.00) +4 more |
| 13 | `get_upstream_features` | L0:F9026@2, k=5 → Emb:"piracy"@2 (de=24.38) +4 more |
| 14 | `get_upstream_features` | L1:F8696@8, k=5 → Emb:" investing"@8 (de=21.88) +4 more |
| 15 | `get_upstream_features` | L8:F12761@3, k=5 → Emb:" theorists"@3 (de=4.56) +4 more |
| 16 | `inspect_feature` | L2, F7725 → "the word "card" when used in a technical context" |

### Build

`build_circuit` → 13 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 49,165 | 5,048 | 181,705 | 0 | $0.0317 | — | — |
| **Total** | | **49,165** | **5,048** | **181,705** | **0** | **$0.0317** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 10s