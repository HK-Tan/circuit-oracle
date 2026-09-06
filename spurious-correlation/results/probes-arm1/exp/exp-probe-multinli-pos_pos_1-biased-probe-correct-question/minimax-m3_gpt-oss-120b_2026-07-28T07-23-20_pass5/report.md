# Circuit Oracle Report
**Date:** 2026-07-28 07:23:20 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's CONTRADICTION score is driven primarily by a chain of features that all fire on the single token "No" at position 30 (the start of "No one thinks Mastercard is up to anything nefarious") — a negation word appears to be the dominant signal the probe learned to associate with contradiction.

**Confidence:** 8

**Reasoning:** The circuit reveals a striking pattern. The strongest late-layer features driving the probe — L16:F11298 (direct_effect=0.24, label "no"), L15:F13061 (0.21, "uses of the word 'no' or similar negative statements"), and L14:F336 (0.196, "the word 'no' and related negative words") — are all position-30 features dedicated to detecting the literal word "No" (and in L15's case, also "one"). Tracing upstream through get_upstream_features confirms this is a single-token circuit: the embedding for " No" (pos 30) directly feeds L0:F1143 + L0:F14862 (both labeled "the word 'no'") with direct_effect=27, then L2:F2771 ("the word 'no' as well as words and phrases that are conceptually related to negation", frac_nonzero=0.002), L3:F3266 ("the abbreviation 'No.' for Number" — also fires on 'No'), L12:F8719, L13:F10768, and onward up to the L16 "no" feature. L4:F15764 (label: "fragments of sentences that contain a pronoun, a verb, and the word 'one', or words with similar meanings", promoted_tokens include "nobody/Nobody/nobody") also receives direct input from the "No" embedding (via L0) and pushes the probe score at pos 31. The user's concern is confirmed: these are spurious lexical negation features, not semantic contradiction detectors. The other top features (L0:F44/F14625 detecting "Cons" from "Conspiracy" at pos 1; L0:F14574 "your"; L0:F3635 "that"; L0:F11375 "is"; L5:F559 about "conspiracy/co-conspirators"; L10:F16373 about "bigoted statements about minority groups") are generic lexical detectors and a conspiracy-related feature (L5:F559 at pos 2 "piracy"), but none of them encodes a real model of the premise–hypothesis contradiction; they fire on common words. The probe has effectively learned the shortcut "if the hypothesis contains the word 'No', classify as contradiction" rather than modeling the actual semantic relationship. The frac_nonzero values of the negation features (0.002–0.014) confirm they are highly specific, but that specificity is to a single word, not to the contradiction phenomenon.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 30 | Emb: No (pos 30) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: BOS (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1143](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) | 30 | L0: 'No' / negation tokens |  the word "no" and related words like "nobody" and "trust" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) |
| [L0:F14862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) | 30 | L0: 'No' / negation tokens | the word "no" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) |
| [L2:F2771](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) | 30 | L2: 'no' / conceptually related negation |  the word "no" as well as words and phrases that are conceptually related to negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) |
| [L3:F3266](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) | 30 | L3: 'No.' abbreviation / negation |  the abbreviation "No." for Number | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) |
| [L12:F8719](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) | 30 | L12: negation feature (pos 30) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) |
| [L13:F10768](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) | 30 | L13: negation feature (pos 30) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 30 | L14: 'no' and related negative words | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 30 | L15: 'no' / negative statements |  uses of the word "no" or similar negative statements and words associated with "one" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 30 | L16: 'no' | no | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |
| [L5:F559](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) | 2 | L5: legal conspiracies / co-conspirators words (pos 2) |  words frequently related to legal conspiracies and co-conspirators | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) |
| [L10:F16373](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/16373) | 7 | L10: bigoted / 'evil' statements (pos 7) | bigoted statements about minority groups | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/16373) |
| [L4:F15764](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) | 31 | L4: pronoun+verb+'one' / nobody etc. (pos 31) |  fragments of sentences that contain a pronoun, a verb, and the word "one", or words with similar meanings | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) |
| [L0:F44](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) | 1 | L0: 'Cons'/'cons' words (pos 1) | words starting with "cons" that might indicate a constitution or consolidated standard, alongside "pride" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) |
| [L0:F14625](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) | 1 | L0: 'Cons'/'cons' words (pos 1) |  the abbreviation "Cons" or "AC" followed by other letters | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) |
| [L0:F14574](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) | 18 | L0: 'your' / possessive (pos 18) | the possessive adjective "your." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | L0: 'that' word (pos 12) | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | L0: 'is' word (pos 7) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'CONTRADICTION' is not one of the top-k next-token can |
| 3 | `get_top_features` | 20 features; top: L0:44 de=-0.527 |
| 4 | `inspect_feature` ×6 | L0:11375, L0:3635, L0:14574, L0:44, L0:14625, L4:15764 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F11298@30` | ❌ error | — | — | Trace from L16:F11298 at pos 30 — what does this feature encode and where does t… |
| SA-2 | `L15:F13061@30` | ❌ error | — | — | Trace from L15:F13061 at pos 30 — what does this feature encode and where does t… |
| SA-3 | `L14:F336@30` | ❌ error | — | — | Trace from L14:F336 at pos 30 — what does this feature encode and where does the… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×3 | L16:11298, L15:13061, L14:336 |
| 2 | `get_upstream_features` | L16:F11298@30, k=10 → L15:F13061 (de=14.00) +9 more |
| 3 | `get_upstream_features` | L15:F13061@30, k=10 → L14:F336 (de=13.00) +9 more |
| 4 | `get_upstream_features` | L14:F336@30, k=10 → Emb:" No"@30 (de=33.75) +9 more |
| 5 | `inspect_feature` ×2 | L10:16373, L5:559 |
| 6 | `get_upstream_features` | L12:F8719@30, k=10 → Emb:" No"@30 (de=16.50) +9 more |
| 7 | `get_upstream_features` | L13:F10768@30, k=10 → Emb:" No"@30 (de=12.06) +9 more |
| 8 | `get_upstream_features` | L0:F1143@30, k=10 → Emb:" No"@30 (de=27.00) +9 more |
| 9 | `inspect_feature` ×5 | L16:11298, L2:2771, L0:1143, L0:14862, L3:3266 |
| 10 | `get_upstream_features` | L10:F16373@7, k=10 → Emb:" theorists"@3 (de=1.91) +9 more |
| 11 | `get_upstream_features` | L5:F559@2, k=10 → Emb:"piracy"@2 (de=6.72) +9 more |

### Build

`build_circuit` → 18 nodes, 28 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 34,709 | 4,843 | 153,244 | 0 | $0.0254 | — | — |
| **Total** | | **34,709** | **4,843** | **153,244** | **0** | **$0.0254** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 19s