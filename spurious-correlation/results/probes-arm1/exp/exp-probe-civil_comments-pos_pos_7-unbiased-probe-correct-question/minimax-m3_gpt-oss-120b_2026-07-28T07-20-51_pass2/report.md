# Circuit Oracle Report
**Date:** 2026-07-28 07:20:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven almost entirely by spurious **identity-token features** (dedicated detectors for the literal words "Black," "White," "Pride," "proud," and an HIV/gay identity-association feature), not by any feature that actually reads the prompt's content (the claim "White Pride = NAZI!" or the closing moralizing sentence).

**Confidence:** 8

**Reasoning:** Tracing the circuit from the probe's output direction back to the token embeddings confirms the user's concern. The top features driving the probe's score are overwhelmingly lexical-identity detectors:

- **L0:1015** ("black", activation 13.4 at pos 1, 20.8 at pos 5), **L0:3436** ("white", activation 15 at pos 17) and **L1:13069** ("black", activation 16.8 at pos 5) are dedicated identity-name detectors with `frac_nonzero` < 0.01 — they fire only on the race-label tokens themselves. Their direct effects on the probe are large and negative (L0:1015 +0.08, L1:13069 −0.12) simply because the words "black/Black" happen to appear in the prompt.
- **L3:15701** ("proud") and **L0:12717** ("pride") fire on the literal Pride/proud tokens. **L3:13061** at pos 2 is a "Black Pride" bigram-style capitalized feature whose strongest upstream is literally `Emb: 'Black' (pos 1)` (direct_effect 12.06) — i.e., it just notes that a capitalized identity word sits next to "Pride."
- **L6:15295** is the most damning: its Neuronpedia label is "HIV/AIDS and viral infections," but its **promoted tokens** are `▁gays, ▁gay, ▁homosexuality, ▁homosexual, ▁lesbian`. Its single largest upstream is `Emb: ' Pride' (pos 2)` with direct_effect 10.75 — meaning the model associates the word "Pride" with gay/LGBTQ+ identity. It then adds direct_effect 0.08 to the toxicity probe. This is a textbook spurious correlation: the feature was trained on medical text mentioning HIV in LGBT contexts, so "Pride" routes through it, and the probe reads that as a toxicity signal.
- **L5:615** ("named holidays or days of the year") fires on "Pride" because Pride is a holiday.
- Other contributors (L0:9222 "=", L4:192 "=letters", L3:11279 "p-value symbols") are pure punctuation/format detectors — they fire because the prompt uses the format "X = Y," not because they encode meaning.
- The **final moral sentence "Hypocrisy is worse than racism"** is barely represented; no feature specifically about hypocrisy, racism-as-concept, or moral judgment appears in the top contributors. Instead, the **"White Pride = NAZI!"** line is being read as toxic mainly because "White" (L0:3436, direct_effect +0.067 to the probe) is a known identity token.

The user's diagnosis is correct: the probe classifies this prompt as toxic by matching identity tokens (Black, White, Pride, gay) to its training-time correlation between identity mentions and toxic content. The actual semantic content of the prompt (the explicit NAZI equation, the hypocrisy claim) is **not** represented in the circuit — only the surface identity vocabulary is. If the same probe were applied to a non-toxic sentence that happened to contain the words "Black," "Pride," and "Gay," it would likely score as toxic for the same reason.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'Black' (pos 1) — capitalized Black identity token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' Pride' (pos 2) — first Pride token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' =' (pos 3) — equals sign token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: ' being' (pos 4) — generic 'being' word | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' black' (pos 5) — lowercase 'black' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: 'White' (pos 17) — capitalized White identity token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F12717](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) | 2 | L0 Generic Lexical Detectors (low-level, mixed effects) |  the word "pride" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) |
| [L0:F9222](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) | 3 | L0 Generic Lexical Detectors (low-level, mixed effects) |  the equals sign | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) |
| [L0:F45](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) | 4 | L0 Generic Lexical Detectors (low-level, mixed effects) | the word "being" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) |
| [L0:F2177](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2177) | 2 | L0 Generic Lexical Detectors (low-level, mixed effects) |  capitalized words or phrases | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2177) |
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 1 | L0 Race/Identity Token Detectors (spurious identity-name features) |  the word "black" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 5 | L0 Race/Identity Token Detectors (spurious identity-name features) |  the word "black" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 17 | L0 Race/Identity Token Detectors (spurious identity-name features) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L1:F13069](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) | 1 | L1 'black' word detector (spurious identity-name feature) | the word 'black' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) |
| [L1:F13069](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) | 5 | L1 'black' word detector (spurious identity-name feature) | the word 'black' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 5 | L1 'warm/heat' feature (incidental) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L2:F5266](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) | 4 | L2 'being' phrase detector | phrases that include the word "being" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) |
| [L3:F15701](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) | 2 | L3 'proud' word detector (spurious pride/proud identity-association feature) | instances of the word "proud" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) |
| [L3:F11279](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11279) | 3 | L3 scientific-symbol / p-value feature (off-target) |  symbols common in scientific research papers, such as p-values and replicates | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11279) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 2 | L3 capitalized-word / Black-Pride bigram feature (spurious identity pairing) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L4:F192](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/192) | 3 | L4 '= with letters/numbers' (math formula) feature | equal signs adjacent to numbers, letters and symbols, which may be mathematical formulas | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/192) |
| [L5:F615](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/615) | 2 | L5 named-holiday/day-of-year feature (spurious — fires on 'Pride') |  named holidays or days of the year | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/615) |
| [L6:F15295](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) | 2 | L6 HIV/gay/homosexuality lexicon (spurious identity-feature — promoted tokens include 'gays', 'gay', 'homosexuality', 'lesbian') |  words and abbreviations related to HIV/AIDS and viral infections. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:12717 de=-0.133 |
| 3 | `inspect_feature` ×19 | L0:12717, L3:15701, L3:11279, L1:13069, L0:9222, L0:45, L0:9113, L3:12034, L0:1088, L0:2177, L2:5266, L0:12054, L0:10164, L6:15295, L0:1015, L5:615, L0:10074, L0:7894, L4:192 |
| 4 | `get_top_features` | 30 features; top: L0:12717 de=-0.133 |
| 5 | `inspect_feature` ×9 | L2:1311, L2:6014, L0:3436, L3:12020, L0:5463, L3:7084, L0:10321, L0:44, L3:13601 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F15295@2` | ❌ error | — | — | Trace the upstream path from L6:F15295 at pos 2. This feature promotes tokens li… |
| SA-2 | `L0:F1015@5` | ❌ error | — | — | Trace the upstream path from L0:F1015 at pos 5 (this is "black" detector at posi… |
| SA-3 | `L0:F3436@17` | ❌ error | — | — | Trace the upstream path from L0:F3436 at pos 17 (this is "white" detector — pos … |
| SA-4 | `L3:F11279@3` | ❌ error | — | — | Trace the upstream path from L3:F11279 at pos 3 (this is a "scientific symbols/p… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F15295@2, k=15 → Emb:" Pride"@2 (de=10.75) +14 more |
| 2 | `get_upstream_features` | L0:F1015@5, k=15 → Emb:" black"@5 (de=23.62) +14 more |
| 3 | `get_upstream_features` | L0:F3436@17, k=15 → Emb:"White"@17 (de=16.75) +14 more |
| 4 | `get_upstream_features` | L3:F11279@3, k=15 → Emb:" ="@3 (de=11.31) +14 more |
| 5 | `get_upstream_features` | L3:F13061@2, k=8 → Emb:"Black"@1 (de=12.06) +7 more |
| 6 | `get_upstream_features` | L0:F12717@2, k=10 → Emb:" Pride"@2 (de=11.69) +9 more |
| 7 | `get_upstream_features` | L3:F15701@2, k=10 → Emb:" Pride"@2 (de=18.62) +9 more |
| 8 | `get_upstream_features` | L5:F615@2, k=10 → Emb:" Pride"@2 (de=12.69) +9 more |
| 9 | `get_upstream_features` | L2:F5266@4, k=10 → Emb:" being"@4 (de=31.00) +9 more |
| 10 | `get_upstream_features` | L1:F13069@5, k=10 → Emb:" black"@5 (de=22.25) +9 more |
| 11 | `get_upstream_features` | L0:F12717@1, k=8 → ❌ Feature (layer=0, feature_idx=12717) not found at pos=1. Thi |
| 12 | `get_upstream_features` | L0:F1015@1, k=8 → Emb:"Black"@1 (de=16.88) +7 more |
| 13 | `get_upstream_features` | L0:F45@4, k=8 → Emb:" being"@4 (de=32.75) +7 more |
| 14 | `get_upstream_features` | L0:F9222@3, k=8 → Emb:" ="@3 (de=11.19) +7 more |
| 15 | `get_upstream_features` | L6:F15295@2, k=8 → Emb:" Pride"@2 (de=10.75) +7 more |
| 16 | `get_upstream_features` | L1:F13069@1, k=8 → Emb:"Black"@1 (de=19.38) +7 more |

### Build

`build_circuit` → 18 nodes, 27 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 118,563 | 7,157 | 303,929 | 0 | $0.0624 | — | — |
| **Total** | | **118,563** | **7,157** | **303,929** | **0** | **$0.0624** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 47s