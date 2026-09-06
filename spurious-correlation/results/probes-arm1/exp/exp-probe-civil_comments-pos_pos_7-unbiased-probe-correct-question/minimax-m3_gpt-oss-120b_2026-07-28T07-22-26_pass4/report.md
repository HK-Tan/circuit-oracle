# Circuit Oracle Report
**Date:** 2026-07-28 07:22:26 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

I have good coverage of the circuit. Let me now produce my analysis.

**Analysis:** The probe's toxicity classification is driven by an "identity-group-as-toxic" circuit: lexical detectors for race/color words ("black") and identity-movement words ("Pride") at the embedding and L0–L1 layers feed into mid-layer "demographic identity" features (race/gender/sexual-orientation associations) at L2–L3, which in turn activate a late-layer L6 feature (L6:F15295) that semantically encodes HIV/AIDS and LGBT vocabulary — this last feature feeds the probe direction.

**Confidence:** 7

**Reasoning:**

**Bottom of the circuit (embeddings + lexical features, L0–L1):** The signal starts from the input token embeddings themselves, with massive direct effects on key upstream features: " Pride" (pos 2, DE=18.6 → mid_pride_l2 and DE=10.75 → out_l6), " black" (pos 5, DE=22.25 → L1:F13069), and "Black" (pos 1, DE=7.25 → L3:F12034 and DE=−1.36 → out_l6). These embeddings feed lexical features that are pure word detectors with low frac_nonzero and high specificity: L0:F1015 ("the word 'black'", frac=0.007), L0:F12717 ("the word 'pride'", frac=0.011), L0:F45 ("the word 'being'"), L0:F12054 ("the word 'being'"), L0:F9222 ("the equals sign", frac=0.008), L0:F2177 ("capitalized words", frac=0.015), and L1:F13069 ("the word 'black'", frac=0.004) and L1:F9113 ("discussions about race and slavery", frac=0.019, suppressed tokens include "Black"/"white"/"black"). Critically, these are NOT toxicity-relevant features — they are simple word-shape and word-identity detectors.

**Mid layers (L2–L3):** The lexical features are routed into mid-layer concepts:
- L2:F1644 ("different forms of the word 'pride'") and L2:F5266 ("phrases that include the word 'being'") — generic phrase detectors, not toxic.
- L2:F9528 ("the color black", frac=0.0024) and L2:F11363 ("colors and words like Diamond") — color features that nevertheless get recruited.
- L3:F15701 ("instances of the word 'proud'"), L3:F11279 ("scientific notation symbols"), L3:F12034 ("technical terms, graphs and figures") — word/symbol detectors.
- L3:F13061 ("words related to race, gender and social issues", frac=0.009) and L3:F16373 ("mentions of demographic identity, especially race and gender", frac=0.006) — these are the first features that actually approach content beyond simple word identity, but they fire on any mention of race/gender/social-issues terminology regardless of stance or valence.

**Late layer (L6):** L6:F15295 ("words and abbreviations related to HIV/AIDS and viral infections", frac=0.039) is the deepest feature that directly drives the probe. Its promoted tokens include "▁gays", "▁gay", "▁homosexuality", "▁homosexual", "▁lesbian" — so although its headline description is medical/HIV, the feature has a clear LGBT-identity sub-component. It also receives direct embedding signal from " Pride" (pos 2, DE=10.75), so it is partly activated by Pride as a token, not by a toxicity pattern.

**Mechanism and whether the circuit is spurious:** The user is right that the circuit leans on identity-group signals rather than the actual prompt content (the "NAZI" / "worse than racism" / "Hypocrisy" content). The direct path to the probe flows: identity-word embeddings ("Pride", "Black", "black") → lexical word detectors (L0:F1015/F12717) → race/gender identity features (L3:F13061/F16373) → L6:F15295 (HIV/AIDS-LGBT-tinged) → probe. Crucially, none of the upstream features encode toxicity, slur, or negative-stance content. The L2 race/slavery context feature (L1:F9113) and the late HIV/LGBT feature (L6:F15295) are the closest the circuit gets to "social-issue" encoding, and they activate on identity vocabulary itself. The actual toxic content tokens ("NAZI", "worse than racism", "Hypocrisy") do not appear anywhere in the upstream chain — features like L3:F11279 (scientific symbols) and L3:F12034 (technical terms, graphs/figures) are off-target noise from co-firing positions, not meaningful semantic contributions. In short, the probe's classification is being driven by a "this text mentions an identity group (Black + Pride)" shortcut rather than the actual hateful or hypocritical content of the passage, which validates the user's concern about spurious features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' black' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'Black' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' Pride' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: ' being' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' =' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: '<bos>' (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 5 | Lexical: word 'black' (L0) |  the word "black" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L0:F1088](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1088) | 2 | Lexical: word 'black' (L0) | mentions of "meal" and, to a lesser extent, words indicating a fondness for something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1088) |
| [L1:F13069](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) | 5 | Lexical: word 'black' / race-and-slavery context (L1) | the word 'black' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 5 | Lexical: word 'black' / race-and-slavery context (L1) |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L0:F12717](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) | 2 | Lexical: word 'pride' (L0) |  the word "pride" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) |
| [L0:F12054](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12054) | 4 | Lexical: word 'proud' (L0) | the word "being" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12054) |
| [L0:F45](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) | 4 | Lexical: word 'being' (L0) | the word "being" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) |
| [L0:F10164](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10164) | 2 | Lexical: word 'being' (L0) |  relative pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10164) |
| [L0:F9222](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) | 3 | Lexical: '=' sign (L0) |  the equals sign | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) |
| [L0:F2177](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2177) | 2 | Lexical: capitalized words (L0) |  capitalized words or phrases | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2177) |
| [L2:F5266](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) | 4 | Mid: 'being' as in 'being X' phrase (L2) | phrases that include the word "being" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) |
| [L2:F1644](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) | 2 | Mid: forms of 'pride' (L2) |  different forms of the word "pride" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) |
| [L2:F3014](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3014) | 3 | Mid: 'being' in 'being X' phrase (L2) |  snippets of mathematical notation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3014) |
| [L2:F14025](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14025) | 3 | Mid: 'being' in 'being X' phrase (L2) | hyphens and tildes adjacent to words or numbers | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14025) |
| [L3:F15701](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) | 2 | Mid: 'pride'/'proud' forms + race/gender (L3) | instances of the word "proud" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) |
| [L3:F11279](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11279) | 3 | Mid: 'pride'/'proud' forms + race/gender (L3) |  symbols common in scientific research papers, such as p-values and replicates | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11279) |
| [L3:F12034](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12034) | 2 | Mid: 'pride'/'proud' forms + race/gender (L3) | technical terms, especially those used to describe graphs and figures | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12034) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 1 | Mid: 'color black' / 'colors and Diamond' (L2) |  the color black | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L2:F11363](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) | 1 | Mid: 'color black' / 'colors and Diamond' (L2) |  colors and words like Diamond. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 2 | Mid: race/gender/demographic identity (L3) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 2 | Mid: race/gender/demographic identity (L3) |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L4:F5217](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5217) | 2 | Mid: URL/website words, holidays (L4-5) |  words and abbreviations that often appear in URLs or website names | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5217) |
| [L5:F615](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/615) | 2 | Mid: URL/website words, holidays (L4-5) |  named holidays or days of the year | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/615) |
| [L6:F15295](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) | 2 | Late: HIV/AIDS / LGBT-tinged identity words (L6) |  words and abbreviations related to HIV/AIDS and viral infections. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: probe (toxicity) direction | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:12717 de=-0.133 |
| 3 | `inspect_feature` ×15 | L0:12717, L3:11279, L3:15701, L1:13069, L0:45, L0:1088, L0:12054, L0:10164, L0:9222, L1:9113, L3:12034, L0:2177, L2:5266, L0:1015, L6:15295 |
| 4 | `get_upstream_features` | Emb:" black"@5 (de=22.25) +9 more |
| 5 | `get_upstream_features` | Emb:" black"@5 (de=17.50) +9 more |
| 6 | `inspect_feature` ×5 | L0:16013, L0:13380, L0:1444, L0:2489, L0:13168 |
| 7 | `get_upstream_features` | Emb:" ="@3 (de=11.31) +9 more |
| 8 | `get_upstream_features` | Emb:" Pride"@2 (de=18.62) +9 more |
| 9 | `get_upstream_features` | Emb:"Black"@1 (de=7.25) +9 more |
| 10 | `get_upstream_features` | Emb:" Pride"@2 (de=10.75) +9 more |
| 11 | `inspect_feature` ×9 | L3:13061, L4:5217, L3:16373, L5:615, L2:11363, L2:9528, L2:1644, L2:14025, L2:3014 |

### Build

`build_circuit` → 22 nodes, 28 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 54,473 | 6,012 | 219,404 | 0 | $0.0367 | — | — |
| **Total** | | **54,473** | **6,012** | **219,404** | **0** | **$0.0367** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 29s