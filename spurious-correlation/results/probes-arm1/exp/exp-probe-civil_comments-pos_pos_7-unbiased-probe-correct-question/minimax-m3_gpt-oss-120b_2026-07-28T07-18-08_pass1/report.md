# Circuit Oracle Report
**Date:** 2026-07-28 07:18:08 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a small set of low-level, token-specific lexical features (mostly L0–L3) that fire on the identity word "black" (pos 5) and a couple of generic "scientific-symbol"/figure/meal detectors, not by any higher-layer semantic or toxicity concept.

**Confidence:** 7

**Reasoning:** The top features driving the probe direction are almost all single-word or token-shape detectors in the lowest transcoder layers, with no late-layer or abstract features present:
- **"black" identity-word features (pos 5):** L1:F13069 "the word 'black'" (direct_effect −0.121, frac_nonzero 0.0037), L1:F9113 "discussions about race and slavery" (direct_effect +0.090, frac_nonzero 0.019), and L0:F1015 "the word 'black'" (positive 0.357) — these trace back via get_upstream_features to the raw ` black` token embedding (pos 5, direct_effect 17.5–22.25) and to a small extent to the capitalized `Black` embedding at pos 1. The probe literally fires on the identity token itself, plus a thin "race/slavery" wrapper on top.
- **"pride"/"proud" features (pos 2):** L0:F12717 "the word 'pride'" (−0.133) and L3:F15701 "instances of the word 'proud'" (−0.124), both driven by the ` Pride` (pos 2) embedding and a pair of generic layer-0 features (F12292, F7019).
- **"being" features (pos 4):** L0:F45 "the word 'being'" (−0.099, frac_nonzero 0.014) and L2:F5266 "phrases that include the word 'being'" (−0.086, frac_nonzero 0.0066) — both fed directly by the ` being` (pos 4) embedding (direct_effect 31).
- **"=" features (pos 3):** L3:F11279 "scientific p-value symbols" (−0.124, frac_nonzero 0.026) and L0:F9222 "the equals sign" (−0.116, frac_nonzero 0.008) — driven by the ` =` (pos 3) embedding (direct_effect 11.3); the F11279 autointerp "scientific research paper symbols" is a textbook spurious correlation.
- **Spurious generic features:** L0:F1088 "meal / fondness for something" (+0.087, frac_nonzero 0.019) and L3:F12034 "technical terms describing graphs/figures — dots/bars/circles" (+0.087, frac_nonzero 0.082) fire on pos 2/3 but have nothing to do with toxicity or identity.

Notably, the top-10 list contains no layer-4+ semantic features at all — the deepest features (L3:F15701 "proud", L3:F11279 "p-values", L3:F12034 "figure elements") are themselves just lexical detectors. The user's concern is corroborated: the probe classification is being driven by **shallow identity-token features ("black", with a thin "race/slavery" wrapper) plus a grab-bag of spurious generic word/symbol detectors ("pride", "being", "=", "meal", figure-graphics terms)**, rather than by any prompt-level semantic, syntactic, or toxicity-related representation. The race/slavery feature is a *narrow* "Black identity word" detector, not a deep identity-group concept. The mechanism is essentially: "the input contains the word *black* (an identity word), plus a few common neutral tokens" → high probe score.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'Black' (pos 1, capitalized identity word) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' black' (pos 5, lowercase identity word) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' Pride' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: ' being' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' =' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 5 | L0: 'black' lexical detector (F1015) — fires on the word 'black' (pos 5) |  the word "black" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L1:F13069](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) | 5 | L0: 'black'/'Black' lexical detector (F13069) — the word 'black' | the word 'black' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13069) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 5 | L1: 'discussions about race and slavery' (F9113) at pos 5 |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L0:F12717](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) | 2 | L0: 'the word pride in different contexts' (F12717) at pos 2 |  the word "pride" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12717) |
| [L3:F15701](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) | 2 | L3: 'instances of the word proud' (F15701) at pos 2 | instances of the word "proud" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15701) |
| [L0:F45](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) | 4 | L0: 'the word being in different contexts' (F45) at pos 4 | the word "being" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/45) |
| [L2:F5266](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) | 4 | L2: 'phrases that include the word being' (F5266) at pos 4 | phrases that include the word "being" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5266) |
| [L3:F11279](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11279) | 3 | L3: '= in scientific notation' (F11279) at pos 3 |  symbols common in scientific research papers, such as p-values and replicates | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11279) |
| [L0:F9222](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) | 3 | L0: 'the equals sign' (F9222) at pos 3 |  the equals sign | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9222) |
| [L3:F12034](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12034) | 2 | L3: 'technical terms describing graphs/figures' (F12034) at pos 2 — spurious generic figure-element detector | technical terms, especially those used to describe graphs and figures | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12034) |
| [L0:F1088](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1088) | 2 | L0: 'meal / fondness-for-something' (F1088) at pos 2 — spurious generic feature | mentions of "meal" and, to a lesser extent, words indicating a fondness for something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1088) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'probe_target' is not one of the top-k next-token cand |
| 3 | `get_top_features` | 10 features; top: L0:12717 de=-0.133 |
| 4 | `inspect_feature` ×10 | L0:12717, L3:11279, L3:15701, L1:13069, L0:9222, L0:45, L1:9113, L3:12034, L0:1088, L2:5266 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F13069@5` | ❌ error | — | — | Trace the path from L1:F13069 (the word "black" at pos 5 — i.e., the "Black" in … |
| SA-2 | `L3:F15701@2` | ✅ reported | 3 | 6 | Trace the path from L3:F15701 (the word "proud" at pos 2 — "Black Pride = being … |
| SA-3 | `L0:F12717@2` | ❌ error | — | — | Trace the path from L0:F12717 (the word "pride" at pos 2). Find what feeds this,… |
| SA-4 | `L1:F9113@5` | ❌ error | — | — | Trace the path from L1:F9113 ("discussions about race and slavery" at pos 5). Fi… |

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F15701 | "instances of the word "proud"" |
| 2 | `get_upstream_features` | L3:F15701@2, k=10 | Emb:" Pride"@2 (de=18.62) +9 more |
| 3 | `get_upstream_features` | L0:F12292@2, k=10 | Emb:"Black"@1 (de=12.31) +9 more |
| 4 | `inspect_feature` | L0, F7019 | " terms that indicate the quality, importance, or origin of things" |
| 5 | `get_upstream_features` | L0:F7019@2, k=10 | Emb:"Black"@1 (de=9.12) +9 more |
| 6 | `inspect_feature` | L0, F12292 | " words or phrases related to specifications or cost" |

**Findings:** The target L3 feature (F15701) representing the word "proud" receives a strong positive push from the input embedding of the token " Pride" (pos 2). Two early‑layer (layer 0) features—F12292 and F7019—also feed into it with modest positive effects. Both layer‑0 features are driven primarily by the embedding of the token "Black" (pos 1), establishing a low‑level route that brings the identity token…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F13069@5, k=10 → Emb:" black"@5 (de=22.25) +9 more |
| 2 | `get_upstream_features` | L0:F12717@2, k=10 → Emb:" Pride"@2 (de=11.69) +9 more |
| 3 | `get_upstream_features` | L1:F9113@5, k=10 → Emb:" black"@5 (de=17.50) +9 more |
| 4 | `get_upstream_features` | L3:F11279@3, k=10 → Emb:" ="@3 (de=11.31) +9 more |
| 5 | `get_upstream_features` | L2:F5266@4, k=10 → Emb:" being"@4 (de=31.00) +9 more |
| 6 | `inspect_feature` ×4 | L0:1444, L0:1015, L0:12292, L0:7019 |

### Build

`build_circuit` → 17 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 34,122 | 4,637 | 110,902 | 0 | $0.0225 | — | — |
| SA-2 | openai/gpt-oss-120b | 57,974 | 5,680 | 5,056 | 0 | $0.0122 | ✅ 3F/6E | Trace the path from L3:F15701 (the word "proud" at pos 2 — "… |
| **Total** | | **92,096** | **10,317** | **115,958** | **0** | **$0.0346** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 56s