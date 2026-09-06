# Circuit Oracle Report
**Date:** 2026-07-28 08:41:20 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven primarily by a "spurious" negation detection mechanism that triggers on the word "not" rather than a semantic understanding of the contradictory content.

**Confidence:** 9

**Reasoning:** 
The attribution circuit reveals that the probe's score is heavily influenced by two main signal paths: one tracking military fortification concepts and another tracking negation. 

1.  **Negation Path (Dominant Spurious Signal):** The most critical drivers of the probe's score are late-layer negation features, specifically **L16:F6800** ("negations 'not', 'no', and contractions with 't'") and **L4:F4492** ("negations in various languages"). Deep tracing using a subagent confirms that L16:F6800 is the terminal node of a hierarchical negation circuit. The signal originates from the raw token embedding of "not" (pos 36), which activates **L0:F4958** (exact match for "not"), propagating through **L3:F3534** (character sequence "n't"), **L13:F102** (phrases containing "not"), and **L15:F11794** (disagreement/negation phrases), finally hitting L16:F6800. This confirms the probe is effectively acting as a "not-detector."

2.  **Lexical Path (Content Signal):** There is a parallel signal from **L7:F13215**, which encodes "terms used to describe military fortifications" (likely triggered by "castle" and "tower house"). This indicates the probe recognizes the domain of the text, but the a-priori classification of "contradiction" is pushed over the threshold by the presence of negation words.

Because the signal flows directly from the literal token "not" through a series of generic negation detectors to the probe, the model is relying on a surface-level heuristic (the presence of "not") rather than performing a semantic comparison between the two sentences to identify a contradiction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L7:F13215](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) | 1 | Military Fortification Concept |  terms used to describe military fortifications. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 26 | Negation Detection | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 26 | Negation Detection |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 3 | `get_top_features` | 10 features; top: L0:2158 de=0.277 |
| 4 | `inspect_feature` ×5 | L0:2158, L4:13244, L4:4492, L16:6800, L7:13215 |
| 5 | `get_top_logits` | "" (100%) |
| 6 | `get_top_features` | 10 features; top: L0:2158 de=0.277 |
| 7 | `inspect_feature` ×5 | L4:4492, L16:6800, L7:13215, L0:2158, L4:13244 |
| 8 | `get_top_logits` | "" (100%) |
| 9 | `get_top_features` | 10 features; top: L0:2158 de=0.277 |
| 10 | `inspect_feature` ×5 | L0:2158, L4:13244, L4:4492, L16:6800, L0:12378 |
| 11 | `get_top_logits` | "" (100%) |
| 12 | `get_top_features` | ❌ Token '""' is not one of the top-k next-token candidates cap |
| 13 | `get_top_features` | 15 features; top: L0:2158 de=0.277 |
| 14 | `inspect_feature` ×5 | L0:2158, L4:13244, L4:4492, L16:6800, L7:13215 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F6800@32` | ✅ reported | 5 | 22 | Trace the path from the probe-driving features (L16:F6800 and others) to determi… |
| SA-2 | `L7:F13215@1` | ❌ error | — | — | Trace the path from the probe-driving features to see if it connects to 'castle'… |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F6800 | " negations "not", "no", and contractions with "t". " |
| 2 | `get_upstream_features` | L16:F6800@32, k=10 | ❌ Feature (layer=16, feature_idx=6800) not found at pos=32. Th |
| 3 | `get_upstream_features` | L16:F6800@36, k=15 | Emb:" not"@36 (de=12.50) +14 more |
| 4 | `inspect_feature` | L15, F11794 | " phrases that express disagreement or negation" |
| 5 | `get_upstream_features` | L15:F11794@36, k=10 | Emb:" does"@35 (de=7.19) +9 more |
| 6 | `inspect_feature` | L3, F3534 | "the character sequence "n't" or "nut"" |
| 7 | `get_upstream_features` | L3:F3534@36, k=10 | Emb:" not"@36 (de=16.12) +9 more |
| 8 | `inspect_feature` | L13, F102 | " phrases containing "not" or negative connotations" |
| 9 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 10 | `get_upstream_features` | L13:F102@36, k=10 | Emb:" not"@36 (de=9.50) +9 more |
| 11 | `get_upstream_features` | L0:F4958@36, k=10 | Emb:" not"@36 (de=34.00) +9 more |
| 12 | `inspect_feature` | L14, F6648 | " words and phrases that indicate speculation, possibility, or negation" |
| 13 | `inspect_feature` | L12, F9489 | "negations combined with verbs, modal verbs, and words relating to yout" |
| 14 | `inspect_feature` | L2, F15695 | " the letter "t"" |

**Findings:** The trace shows that L16:F6800’s activation is driven mainly by the literal token "not" in the prompt. The signal propagates through a hierarchy of low‑level negation detectors (embedding "not" → L0:4958 → L3:3534 → L13:102 → L15:11794 → L16:6800). A lower‑third feature (L3:3534) is reached, satisfying the layer‑floor requirement, and a positive‑effect embedding connection is present, satisfying t…

</details>

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 598,702 | 1,559 | 6 | 0 | $0.0844 | — | — |
| SA-1 | openai/gpt-oss-120b | 156,104 | 12,359 | 47,168 | 0 | $0.0315 | ✅ 5F/22E | Trace the path from the probe-driving features (L16:F6800 an… |
| **Total** | | **754,806** | **13,918** | **47,174** | **0** | **$0.1160** | | |

**Oracle wall-clock time:** 10m 36s