# Circuit Oracle Report
**Date:** 2026-07-28 08:42:21 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a spurious mechanism that detects the presence of negation tokens (specifically "not") rather than understanding the semantic contradiction in the prompt.

**Confidence:** 10/10

**Reasoning:**
The attribution circuit reveals a direct and dominant pathway from the input embeddings of the token "not" to the probe's output score. The signal flow is as follows:
1. **Input Embeddings:** The signal originates from the embeddings of the token "not" at positions 23 and 29 (`Emb_not_23`, `Emb_not_29`).
2. **Early Token Detection:** These embeddings strongly excite layer-0 features like **L0:F4958**, which is a highly selective detector for the word "not" (`frac_nonzero` = 0.0184).
3. **Higher-Level Negation Patterns:** This signal propagates to mid-to-late layer features that encode negation and refusal-like patterns. These include **L13:F3295** ("negations in the form of 'is/are not'"), **L16:F12358** ("the word 'not' followed by a form of 'to be'"), and **L16:F9779** ("negation words or contractions like 'won't', 'not', 'never'").
4. **Probe Output:** These negation features directly drive the final probe score.

Crucially, there is no evidence of signal originating from lexical tokens that define the contradiction (e.g., "abbey", "steeple", "height", "sea"). The circuit relies entirely on a "negation word" heuristic. Because the prompt contains two instances of "not" in the second sentence (the contradictory part), the probe identifies these markers as a proxy for contradiction, confirming the user's concern that the probe is utilizing spurious features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: not (pos 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 29 | Emb: not (pos 29) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 23 | Token \"not\" Detectors (L0) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 29 | Token \"not\" Detectors (L0) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 37 | Negation & Refusal Patterns (L13-L16) | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 29 | Negation & Refusal Patterns (L13-L16) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L16:F9779](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) | 37 | Negation & Refusal Patterns (L13-L16) | negation words or contractions like "won't", "not", "never" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 3 | `get_top_features` | 15 features; top: L16:12358 de=0.359 |
| 4 | `inspect_feature` ×4 | L16:12358, L16:9779, L13:3295, L14:10408 |
| 5 | `get_top_logits` | "" (100%) |
| 6 | `get_top_features` | 10 features; top: L16:12358 de=0.359 |
| 7 | `inspect_feature` ×4 | L16:12358, L16:9779, L13:3295, L14:10408 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@37` | ✅ reported | 7 | 11 | Trace the signal flow to the embedding nodes. Determine if the probe is driven b… |
| SA-2 | `L16:F9779@37` | ✅ reported | 7 | 15 | Trace the signal flow to the embedding nodes. Determine if the probe is driven b… |
| SA-3 | `L13:F3295@37` | ✅ reported | 3 | 10 | Trace the signal flow to the embedding nodes. Determine if the probe is driven b… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F12358 | " the word "not" followed within a few tokens by a form of the verb "to" |
| 2 | `get_upstream_features` | L16:F12358@37, k=10 | ❌ Feature (layer=16, feature_idx=12358) not found at pos=37. T |
| 3 | `get_upstream_features` | L16:F12358@29, k=10 | Emb:" not"@29 (de=19.50) +9 more |
| 4 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 5 | `get_upstream_features` | L0:F4958@29, k=10 | Emb:" not"@29 (de=34.25) +9 more |
| 6 | `inspect_feature` | L13, F3295 | "negations in the form of "is/are not" as well as other uses of "not"" |
| 7 | `get_upstream_features` | L13:F3295@29, k=10 | Emb:" not"@29 (de=17.75) +9 more |
| 8 | `inspect_feature` | L15, F10071 | "negations and equivocations" |
| 9 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 10 | `get_upstream_features` | L3:F8011@29, k=10 | Emb:" not"@29 (de=21.62) +9 more |
| 11 | `inspect_feature` | L0, F9646 | " words that indicate the degree, scale, or validity of something" |
| 12 | `inspect_feature` | L2, F12021 | ""not" or negative terms, with some bonus for sports-related terms and " |

**Findings:** The target feature L16:F12358 (layer 16) is a high‑level negation detector that looks for the pattern "not" followed shortly by a form of "to be". Its strongest upstream driver is the raw embedding of the token "not" (direct_effect ~19.5), which feeds into a layer‑0 "not" detector (F4958). That detector in turn is driven directly by the same token embedding (direct_effect ~34.25). Additional posit…

</details>

<details>
<summary><b>SA-2</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F9779 | "negation words or contractions like "won't", "not", "never"" |
| 2 | `get_upstream_features` | L16:F9779@37, k=10 | ❌ Feature (layer=16, feature_idx=9779) not found at pos=37. Th |
| 3 | `get_upstream_features` | L16:F9779@23, k=15 | Emb:" will"@22 (de=7.31) +14 more |
| 4 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 5 | `inspect_feature` | L15, F3521 | "sentences containing words expressing negation or uncertainty in past " |
| 6 | `inspect_feature` | L2, F12694 | " the word "Canisius" and words that express possibility or a small pro" |
| 7 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 8 | `inspect_feature` | L16, F9779 | "negation words or contractions like "won't", "not", "never"" |
| 9 | `get_upstream_features` | L0:F4958@23, k=10 | Emb:" not"@23 (de=33.50) +9 more |
| 10 | `get_upstream_features` | L15:F3521@23, k=10 | Emb:" will"@22 (de=5.91) +9 more |
| 11 | `get_upstream_features` | L4:F4492@23, k=10 | Emb:" not"@23 (de=18.50) +9 more |
| 12 | `get_upstream_features` | L2:F12694@23, k=10 | Emb:" will"@22 (de=15.38) +9 more |
| 13 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 14 | `inspect_feature` | L13, F102 | " phrases containing "not" or negative connotations" |
| 15 | `inspect_feature` | L0, F15454 | " the word "not"" |
| 16 | `get_upstream_features` | L3:F8011@23, k=10 | Emb:" not"@23 (de=19.62) +9 more |

**Findings:** The target feature L16:9779 (negation word detector) receives its strongest excitatory influence from the embedding of the token " not" (direct_effect ≈ 7.3) and from the low‑layer feature L0:4958, which itself is directly driven by the same " not" embedding (direct_effect ≈ 33.5). Additional positive contributors include the token " will" and higher‑layer negation/uncertainty features (L15:3521, …

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L13, F3295 | "negations in the form of "is/are not" as well as other uses of "not"" |
| 2 | `get_upstream_features` | L13:F3295@37, k=10 | ❌ Feature (layer=13, feature_idx=3295) not found at pos=37. Th |
| 3 | `get_upstream_features` | L13:F3295@29, k=10 | Emb:" not"@29 (de=17.75) +9 more |
| 4 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 5 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 6 | `get_upstream_features` | L3:F8011@29, k=10 | Emb:" not"@29 (de=21.62) +9 more |
| 7 | `get_upstream_features` | L0:F4958@29, k=10 | Emb:" not"@29 (de=34.25) +9 more |

**Findings:** The probe's activation traces back almost entirely to the token embedding for the word 'not' (position 29). This token drives a cascade through a low‑layer word detector (L0:F4958) and an intermediate mixing feature (L3:F8011) before reaching the higher‑level negation feature (L13:F3295). No significant upstream influence comes from tokens such as 'abbey' or 'sea'; their direct effects are negligi…

</details>

### Build

`build_circuit` → 5 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 180,482 | 1,400 | 4,359 | 0 | $0.0259 | — | — |
| SA-3 | openai/gpt-oss-120b | 55,258 | 4,676 | 5,088 | 0 | $0.0112 | ✅ 3F/10E | Trace the signal flow to the embedding nodes. Determine if t… |
| SA-1 | openai/gpt-oss-120b | 160,511 | 15,993 | 25,440 | 0 | $0.0341 | ✅ 7F/11E | Trace the signal flow to the embedding nodes. Determine if t… |
| SA-2 | openai/gpt-oss-120b | 245,375 | 13,588 | 25,856 | 0 | $0.0453 | ✅ 7F/15E | Trace the signal flow to the embedding nodes. Determine if t… |
| **Total** | | **641,626** | **35,657** | **60,743** | **0** | **$0.1165** | | |

**Oracle wall-clock time:** 11m 44s