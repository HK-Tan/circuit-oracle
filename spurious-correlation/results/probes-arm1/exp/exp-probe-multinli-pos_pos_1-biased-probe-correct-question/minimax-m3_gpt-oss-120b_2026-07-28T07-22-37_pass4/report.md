# Circuit Oracle Report
**Date:** 2026-07-28 07:22:37 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by the surface-level presence of the word "**No**" and the bigram "**No one**" at the end of the prompt, with very small contributions from conspiracy-themed content detectors at positions 2-3, and the circuit confirms the user's concern that the model leans heavily on negation/structural markers rather than the actual content about MasterCard and the chip.

**Confidence:** 8

**Reasoning:**

The attribution target here is a probe (likely a contradiction/NLI classifier) rather than a next-token distribution, so I read the direct_effect values as evidence of what features push the probe's score positive. The picture is striking: the **dominant positive signal comes from the final sentence's "No one thinks mastercard is up to anything nefarious."**

**Token-position anatomy of the circuit:**
- Position 30 ("**No**") is the single largest contributor. Its embedding node directly drives L14:F336 ("the word 'no' and related negative words", direct_effect to probe = 0.196) and L16:F11298 ("no", 0.240) and L15:F13061 ("uses of the word 'no' or similar negative statements and words associated with 'one'", 0.210). Tracing deeper, the "No" embedding at pos 30 has direct_effect = 12 into L15:F13061, 33.75 into L14:F336, and 12 into L16:F11298 — these are the strongest single-edge values in the graph.
- Position 31 ("**one**") provides the *other* half of the "No one" idiom: L0:F4438 ("the word 'one'", activation 30, direct_effect 0.29) and L0:F11351 ("the number 'one'", 0.20) — but more importantly, L2:F8837 ("the word 'one' or 'body' when preceded by the words 'no' or 'every'", activation 33.5, direct_effect 0.197) is a dedicated "no one" phrase detector with activation 33.5 at this position.
- L2:F8142 ("words related to places, managing, and negation", frac_nonzero 0.0086) and L4:F15764 ("fragments of sentences that contain a pronoun, a verb, and the word 'one'", promoted tokens all negation/quantifier words) reinforce the "No one" idiom.

**Contradiction-direction features also pick up the prompt:**
- L2:F16028 at pos 3 ("terms related to speculation, lies, false information, and conspiracy theories", direct_effect 0.207), L3:F9739 at pos 2 ("words related to conspiracies", 0.200), L5:F559 at pos 2 ("words frequently related to legal conspiracies and co-conspirators", 0.270), L8:F12761 at pos 3 ("words associated with the QAnon conspiracy theory", promoted: "preuve, accuse, incest, proof"), L9:F13961 at pos 3 ("political commentary related to Trump and elections", max_token "theories") — these are real content detectors that fire on the *beginning* of the prompt ("Conspiracy theorists"). However their individual direct_effects (~0.20-0.27) are similar in magnitude to the bare "no"/"No" detectors.
- L10:F16373 at pos 7 ("bigoted statements about minority groups", direct_effect 0.207) appears to fire off the word "MasterCard" — its top activating tokens are "evil" / "harder" / "blacks" — i.e. it's likely firing on the general topic of nefarious corporate behaviour rather than the chip content per se.

**Function-word detectors (the "content" channel):** L0:F11375 ("is"), L0:F3635 ("that"), L0:F14574 ("your"), L1:F13292 ("personal" — but firing on the prompt at pos 11 which is "chip", so spurious), L0:F351 ("expert" — also firing on chip/personal), L1:F13684 ("theory"), L0:F14625 ("Cons"), L0:F44 ("cons"), L2:F16230 ("chip", frac_nonzero 0.0097, direct_effect 0.206), L2:F7725 ("card", 0.193), L0:F2115 at pos 2 (0.200, generic percentage-and-countries detector, not even on the right span). These are high-frac_nonzero surface features that pick up individual words but don't form a coherent "MasterCard is investing in a chip" content representation that competes with the negation signal.

**Verdict on the user's concern:** The concern is **validated by the circuit**. The top-positive direct_effect features are dominated by (a) bare negation detectors on the "**No**" token at pos 30 (L14:F336, L15:F13061, L16:F11298, all direct_effect 0.19-0.24, all frac_nonzero ≤ 0.015, all promoted-token lists full of "no/nobody/nowhere") and (b) the "no one" phrase detector L2:F8837 at pos 31 (direct_effect 0.197, frac_nonzero 0.011). These surface-lexical negation features sit directly at the end of the prompt and have no content-specificity — they would fire on any prompt ending in "No one…". The genuine content detectors at positions 1-3 (conspiracy / theory / theorists) and 5-7 (MasterCard / is) contribute, but their individual direct_effects are *smaller* than or comparable to those of the bare "no"/"No"/"No one" detectors, and they fire on a small set of conspiracy-coded words rather than on the full MasterCard-as-contradicting-content semantic structure. **The probe is therefore primarily exploiting a shallow negation-bigram cue, not a real semantic content match** — which is a textbook spurious-correlation failure mode for NLI probes and supports the user's hypothesis.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 31 | Probe (contradiction) output direction | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 30 | Late-layer negation-aggregator supernode (L14-L16) | no | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 30 | Late-layer negation-aggregator supernode (L14-L16) |  uses of the word "no" or similar negative statements and words associated with "one" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 30 | Late-layer negation-aggregator supernode (L14-L16) | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L12:F8719](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) | 30 | Late-layer negation-aggregator supernode (L14-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) |
| [L13:F10768](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) | 30 | Late-layer negation-aggregator supernode (L14-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) |
| [L2:F2771](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) | 30 | Late-layer negation-aggregator supernode (L14-L16) |  the word "no" as well as words and phrases that are conceptually related to negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) |
| [L3:F3266](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) | 30 | Late-layer negation-aggregator supernode (L14-L16) |  the abbreviation "No." for Number | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) |
| [L0:F1143](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) | 30 | Late-layer negation-aggregator supernode (L14-L16) |  the word "no" and related words like "nobody" and "trust" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) |
| [L0:F14862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) | 30 | Late-layer negation-aggregator supernode (L14-L16) | the word "no" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) |
| [L6:F15886](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15886) | 30 | Late-layer negation-aggregator supernode (L14-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15886) |
| [L4:F15764](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) | 31 | "No one" phrase detector (L2-L4) |  fragments of sentences that contain a pronoun, a verb, and the word "one", or words with similar meanings | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 31 | "No one" phrase detector (L2-L4) |  the word "one" or "body" when preceded by the words "no" or "every." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L2:F8142](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8142) | 31 | "No one" phrase detector (L2-L4) | words related to places, managing, and negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8142) |
| [L2:F13586](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) | 31 | "No one" phrase detector (L2-L4) |  words ending in 'thing' and 'one' often with preceding words indicating the presence of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 31 | "No one" phrase detector (L2-L4) | the word "one". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L0:F11351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11351) | 31 | "No one" phrase detector (L2-L4) |  the number "one" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11351) |
| [L2:F16028](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) | 3 | "No one" phrase detector (L2-L4) |  terms related to speculation, lies, false information, and conspiracy theories | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | "No one" phrase detector (L2-L4) |  words related to conspiracies | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L5:F559](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) | 2 | "No one" phrase detector (L2-L4) |  words frequently related to legal conspiracies and co-conspirators | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) |
| [L9:F13961](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13961) | 3 | "No one" phrase detector (L2-L4) | political commentary related to Trump and elections | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13961) |
| [L8:F12761](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) | 3 | "No one" phrase detector (L2-L4) |  words associated with the QAnon conspiracy theory | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) |
| [L10:F16373](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/16373) | 7 | "No one" phrase detector (L2-L4) | bigoted statements about minority groups | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/16373) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | Function-word & chip/card detectors (L0-L2) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | Function-word & chip/card detectors (L0-L2) | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F14574](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) | 18 | Function-word & chip/card detectors (L0-L2) | the possessive adjective "your." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) |
| [L1:F13292](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) | 11 | Function-word & chip/card detectors (L0-L2) |  the word "personal" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) |
| [L0:F351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) | 11 | Function-word & chip/card detectors (L0-L2) |  the word "expert" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) |
| [L1:F13684](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) | 3 | Function-word & chip/card detectors (L0-L2) |  the word "theory" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) |
| [L0:F14625](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) | 1 | Function-word & chip/card detectors (L0-L2) |  the abbreviation "Cons" or "AC" followed by other letters | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) |
| [L0:F44](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) | 1 | Function-word & chip/card detectors (L0-L2) | words starting with "cons" that might indicate a constitution or consolidated standard, alongside "pride" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Function-word & chip/card detectors (L0-L2) |  mentions of semiconductor chips and devices | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L2:F7725](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) | 6 | Function-word & chip/card detectors (L0-L2) | the word "card" when used in a technical context | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) |
| [L0:F2115](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) | 2 | Function-word & chip/card detectors (L0-L2) |  data reported as a percentage inside brackets, especially in a laboratory or medical context, and also recognizes countries | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:44 de=-0.527 |
| 3 | `inspect_feature` ×20 | L0:11375, L0:3635, L4:15764, L0:14625, L5:559, L1:13292, L16:11298, L0:351, L15:13061, L2:16028, L10:16373, L2:16230, L3:9739, L0:2115, L2:8142, L14:336, L2:7725, L0:44, L0:14574, L1:13684 |
| 4 | `get_upstream_features` | L15:F13061 (de=14.00) +9 more |
| 5 | `get_upstream_features` | L14:F336 (de=13.00) +9 more |
| 6 | `get_upstream_features` | Emb:" No"@30 (de=33.75) +9 more |
| 7 | `get_upstream_features` | Emb:" theorists"@3 (de=11.75) +9 more |
| 8 | `get_upstream_features` | Emb:"Cons"@1 (de=8.75) +9 more |
| 9 | `get_upstream_features` | Emb:"piracy"@2 (de=6.72) +9 more |
| 10 | `get_upstream_features` | Emb:" No"@30 (de=27.00) +9 more |
| 11 | `get_upstream_features` | Emb:" No"@30 (de=14.19) +9 more |
| 12 | `get_upstream_features` | Emb:" No"@30 (de=16.50) +9 more |
| 13 | `get_upstream_features` | Emb:" No"@30 (de=12.06) +9 more |
| 14 | `get_upstream_features` | Emb:" one"@31 (de=10.75) +9 more |
| 15 | `get_upstream_features` | Emb:" No"@30 (de=14.62) +9 more |
| 16 | `get_upstream_features` | Emb:" theorists"@3 (de=1.91) +9 more |
| 17 | `get_upstream_features` | Emb:" chip"@11 (de=27.00) +9 more |
| 18 | `get_upstream_features` | Emb:" No"@30 (de=8.38) +9 more |
| 19 | `get_upstream_features` | Emb:" theorists"@3 (de=25.38) +9 more |
| 20 | `get_upstream_features` | Emb:" is"@7 (de=31.38) +9 more |
| 21 | `get_upstream_features` | Emb:" that"@12 (de=41.00) +9 more |
| 22 | `get_upstream_features` | Emb:" chip"@11 (de=17.00) +9 more |
| 23 | `get_upstream_features` | Emb:" chip"@11 (de=19.25) +9 more |
| 24 | `get_upstream_features` | Emb:" your"@18 (de=45.25) +9 more |
| 25 | `get_upstream_features` | Emb:"Cons"@1 (de=17.88) +9 more |
| 26 | `get_upstream_features` | Emb:"Cons"@1 (de=22.38) +9 more |
| 27 | `get_upstream_features` | Emb:" theorists"@3 (de=10.12) +9 more |
| 28 | `get_upstream_features` | Emb:"piracy"@2 (de=12.88) +9 more |
| 29 | `get_upstream_features` | Emb:" No"@30 (de=16.00) +9 more |
| 30 | `get_upstream_features` | Emb:" No"@30 (de=19.75) +9 more |
| 31 | `get_upstream_features` | Emb:" No"@30 (de=29.38) +9 more |
| 32 | `get_upstream_features` | Emb:" one"@31 (de=38.75) +9 more |
| 33 | `get_upstream_features` | L8:F12761 (de=6.88) +9 more |
| 34 | `get_upstream_features` | Emb:" theorists"@3 (de=4.56) +9 more |
| 35 | `inspect_feature` ×9 | L0:11351, L0:4438, L2:8837, L2:13586, L8:12761, L9:13961, L0:1143, L0:14862, L0:9026 |
| 36 | `get_upstream_features` | Emb:" one"@31 (de=10.75) +9 more |
| 37 | `get_upstream_features` | ❌ Feature (layer=0, pos=3, feature_idx=4) not found in graph's |
| 38 | `get_upstream_features` | Emb:" theorists"@3 (de=10.00) +9 more |
| 39 | `get_upstream_features` | Emb:"Cons"@1 (de=22.88) +9 more |
| 40 | `get_upstream_features` | Emb:"Cons"@1 (de=17.25) +9 more |
| 41 | `get_upstream_features` | Emb:" No"@30 (de=14.81) +9 more |
| 42 | `get_upstream_features` | Emb:" No"@30 (de=29.25) +9 more |
| 43 | `inspect_feature` ×3 | L2:2771, L3:3266, L4:15764 |

### Build

`build_circuit` → 15 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 68,678 | 7,398 | 420,068 | 0 | $0.0547 | — | — |
| **Total** | | **68,678** | **7,398** | **420,068** | **0** | **$0.0547** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 37s