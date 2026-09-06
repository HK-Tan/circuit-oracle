# Circuit Oracle Report
**Date:** 2026-07-28 07:20:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction-classification score is driven primarily by a stack of shallow, lexical/negation-encoding features at late layers — most importantly L14:F336 ("the word 'no' and related negative words", pos 30, direct_effect=0.196), L15:F13061 ("no/negative + one", pos 30, 0.21), and L16:F11298 ("no", pos 30, 0.24) — which in turn are caused almost entirely by the literal token embedding of " No" at position 30 (direct_effect=33.75 into L14:F336, 12–12.7 into the other two), with secondary support from the literal " one" at pos 31, " your" at pos 18, and a generic "conspiracy/speculation/piracy" lexical cluster (L2:F16028, L3:F9739, L5:F559) anchored to the surface tokens "piracy" and "theorists".

**Confidence:** 9

**Reasoning:** The circuit cleanly exhibits the user's hypothesized "spurious negation-feature" pathology. The terminal probe direction is fed by a "negation_chain" supernode whose three dominant members (L14:F336, L15:F13061, L16:F11298) are all shallow "no"-word detectors firing at pos 30 (the literal "No one thinks..."). Their direct_effects on the probe (≈0.20–0.24 each, the three largest in the graph) and on each other (L14→L15 = 13, L15→L16 = 14) show a near-feedforward chain that bottoms out at the **Emb: No (pos 30)** node with direct_effects of 33.75 → 12.7 → 12.0 through the chain. The complementary " one" at pos 31 and " your" at pos 18 also flow into this same chain (L4:F15764 — "pronoun + verb + one" — direct_effect 0.291, fed directly by Emb: " one" with direct_effect 10.75, and Emb: " your" with direct_effect 45.25 into L0:F14574). Critically, **none of these late-layer features encode the actual semantic content** of the passage (MasterCard, chip, cash, medical history, keys). Content-word features like L0:F11375 ("is"), L0:F3635 ("that"), L0:F14574 ("your"), L2:F16230 ("chip"), and L2:F7725 ("card") do exist in the graph but with smaller direct_effects (0.20–0.48) and are not the late-layer drivers. The "conspiracy_lexical" supernode (L2:F16028 "speculation/conspiracy theories", L3:F9739 "conspiracy", L5:F559 "legal conspiracies") fires on the surface trigram "Conspiracy theorists" but contributes through generic word-level co-occurrence rather than via a contradiction-reasoning circuit — its peak direct_effect (≈0.27) is again smaller than the "no" chain. In short, the contradiction probe is largely a **bag-of-cue-word detector**: it lights up because the prompt contains the negation "No" plus the conspiracy-frame keywords, not because the model has identified the semantic contradiction between the premise (MasterCard investing in a chip storing medical/keys data) and the claim (no one thinks it's nefarious). The user's concern is well-founded — the classification is grounded in negation-lexical features rather than a true NLI-style semantic-comparison circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 31 | Probe classification score (contradiction direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 30 | "No" / "one" / "your" — negation & possessive lexical features at pos 30/31/18 (L14–L16) | no | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 30 | "No" / "one" / "your" — negation & possessive lexical features at pos 30/31/18 (L14–L16) |  uses of the word "no" or similar negative statements and words associated with "one" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 30 | "No" / "one" / "your" — negation & possessive lexical features at pos 30/31/18 (L14–L16) | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L10:F16373](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/16373) | 7 | "No" / "one" / "your" — negation & possessive lexical features at pos 30/31/18 (L14–L16) | bigoted statements about minority groups | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/16373) |
| [L4:F15764](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) | 31 | "No" / "one" / "your" — negation & possessive lexical features at pos 30/31/18 (L14–L16) |  fragments of sentences that contain a pronoun, a verb, and the word "one", or words with similar meanings | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) |
| [L5:F559](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) | 2 | Conspiracy/speculation/piracy lexical features (L2–L5) |  words frequently related to legal conspiracies and co-conspirators | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | Conspiracy/speculation/piracy lexical features (L2–L5) |  words related to conspiracies | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L2:F16028](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) | 3 | Conspiracy/speculation/piracy lexical features (L2–L5) |  terms related to speculation, lies, false information, and conspiracy theories | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) |
| [L2:F8142](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8142) | 31 | Conspiracy/speculation/piracy lexical features (L2–L5) | words related to places, managing, and negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8142) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Content-word lexical features — "is", "that", "your", "chip", "card" (L0–L2) |  mentions of semiconductor chips and devices | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L2:F7725](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) | 6 | Content-word lexical features — "is", "that", "your", "chip", "card" (L0–L2) | the word "card" when used in a technical context | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) |
| [L1:F13292](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) | 11 | Content-word lexical features — "is", "that", "your", "chip", "card" (L0–L2) |  the word "personal" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) |
| [L1:F13684](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) | 3 | Content-word lexical features — "is", "that", "your", "chip", "card" (L0–L2) |  the word "theory" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | Content-word lexical features — "is", "that", "your", "chip", "card" (L0–L2) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | Content-word lexical features — "is", "that", "your", "chip", "card" (L0–L2) | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F14574](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) | 18 | Content-word lexical features — "is", "that", "your", "chip", "card" (L0–L2) | the possessive adjective "your." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) |
| [L0:F14625](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) | 1 | Content-word lexical features — "is", "that", "your", "chip", "card" (L0–L2) |  the abbreviation "Cons" or "AC" followed by other letters | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) |
| [L0:F44](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) | 1 | Content-word lexical features — "is", "that", "your", "chip", "card" (L0–L2) | words starting with "cons" that might indicate a constitution or consolidated standard, alongside "pride" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) |
| [L0:F351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) | 11 | Content-word lexical features — "is", "that", "your", "chip", "card" (L0–L2) |  the word "expert" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 30 | Emb: No (pos 30) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 31 | Emb: one (pos 31) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: your (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: chip (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: piracy (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: theorists (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Cons (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: is (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: that (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: Card (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:44 de=-0.527 |
| 3 | `inspect_feature` ×20 | L0:11375, L0:3635, L4:15764, L16:11298, L15:13061, L0:44, L0:14574, L5:559, L1:13292, L0:14625, L10:16373, L2:16028, L2:16230, L3:9739, L2:8142, L14:336, L2:7725, L0:351, L0:2115, L1:13684 |
| 4 | `get_upstream_features` | L15:F13061 (de=14.00) +9 more |
| 5 | `get_upstream_features` | L14:F336 (de=13.00) +9 more |
| 6 | `get_upstream_features` | Emb:" No"@30 (de=33.75) +9 more |
| 7 | `get_upstream_features` | Emb:" theorists"@3 (de=1.91) +9 more |
| 8 | `get_upstream_features` | Emb:" one"@31 (de=10.75) +9 more |
| 9 | `get_upstream_features` | ❌ Feature (layer=0, pos=30, feature_idx=5) not found in graph' |
| 10 | `get_upstream_features` | Emb:"piracy"@2 (de=6.72) +7 more |
| 11 | `get_upstream_features` | Emb:" theorists"@3 (de=11.75) +7 more |
| 12 | `get_upstream_features` | Emb:" is"@7 (de=31.38) +7 more |
| 13 | `get_upstream_features` | Emb:"Cons"@1 (de=22.38) +7 more |
| 14 | `get_upstream_features` | Emb:" your"@18 (de=45.25) +7 more |
| 15 | `get_upstream_features` | Emb:" one"@31 (de=10.75) +7 more |
| 16 | `get_upstream_features` | Emb:"piracy"@2 (de=6.72) +7 more |
| 17 | `get_upstream_features` | Emb:" theorists"@3 (de=11.75) +7 more |
| 18 | `get_upstream_features` | Emb:"Cons"@1 (de=17.88) +7 more |
| 19 | `get_upstream_features` | Emb:" that"@12 (de=41.00) +7 more |
| 20 | `get_upstream_features` | L15:F13061 (de=14.00) +7 more |
| 21 | `get_upstream_features` | L14:F336 (de=13.00) +7 more |
| 22 | `get_upstream_features` | Emb:" No"@30 (de=33.75) +9 more |
| 23 | `get_upstream_features` | Emb:" No"@30 (de=14.62) +7 more |
| 24 | `get_upstream_features` | Emb:" chip"@11 (de=27.00) +7 more |
| 25 | `get_upstream_features` | Emb:" chip"@11 (de=19.25) +7 more |
| 26 | `get_upstream_features` | Emb:"piracy"@2 (de=12.88) +7 more |
| 27 | `get_upstream_features` | Emb:" chip"@11 (de=17.00) +7 more |
| 28 | `get_upstream_features` | Emb:"Cons"@1 (de=8.75) +7 more |

### Build

`build_circuit` → 14 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 59,872 | 5,536 | 216,868 | 0 | $0.0376 | — | — |
| **Total** | | **59,872** | **5,536** | **216,868** | **0** | **$0.0376** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 25s