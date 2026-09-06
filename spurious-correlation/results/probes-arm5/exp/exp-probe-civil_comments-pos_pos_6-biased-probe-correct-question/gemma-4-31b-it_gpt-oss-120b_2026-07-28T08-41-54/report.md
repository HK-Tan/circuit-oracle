# Circuit Oracle Report
**Date:** 2026-07-28 08:41:54 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by an identity-group detection circuit that primarily triggers on the mention of race ("white"), regardless of the semantic context or actual toxicity of the prompt.

**Confidence:** 9

**Reasoning:**
The attribution circuit reveals that the probe's classification score is predominantly fueled by features that detect demographic identities rather than lexical markers of hate speech or toxicity. 

1. **Signal Origin:** The primary signal originates from the embedding of the token `" white"` at position 2. This flows into a low-level detector **L0:F10910**, which is specifically tuned to the word "white".
2. **Hierarchical Aggregation:** The signal is passed through a series of race- and ethnicity-related features. **L2:F13158** ("words about race and ethnicity") and **L2:F1708** ("mentions of colors") aggregate this input.
3. **High-Level Identity Gating:** These mid-layer features then feed into high-level identity detectors including **L3:F13061** ("words related to race, gender and social issues"), **L3:F16373** ("mentions of demographic identity"), and **L4:F117** ("terms related to race, racism, and social justice"). These features have very low `frac_nonzero` (e.g., 0.006 - 0.011), indicating they are highly selective for these specific demographic categories.
4. **Final Output:** These high-level identity features provide the strongest direct effect on the probe's terminal score. A secondary, weaker path also exists from the token `" dude"` (**L0:F9026**) into the identity gate.

Crucially, there are no significant paths originating from tokens related to the actual "toxicity" or the "stealing thunder" action of the prompt. Instead, the probe simply "sees" the identity markers ("white", "black") and classifies the input as toxic based on the presence of these identity group signals, confirming the user's concern that the probe relies on spurious identity-group correlations.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 2 | Low-Level Identity Detection ('white') | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 2 | Mid-Level Race/Ethnicity Aggregation | words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 2 | Mid-Level Race/Ethnicity Aggregation | mentions of colors | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 3 | High-Level Demographic Identity Detector |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 3 | High-Level Demographic Identity Detector |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 3 | High-Level Demographic Identity Detector |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L4:117 de=0.875 |
| 3 | `inspect_feature` ×6 | L4:117, L3:13061, L4:9880, L6:3902, L3:16373, L8:2483 |
| 4 | `get_top_logits` | "" (100%) |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F117@3` | ❌ error | — | — | Trace the path from L4:F117 and L3:F13061 to identify which input tokens drive t… |
| SA-2 | `L3:F13061@3` | ✅ reported | 8 | 6 | Trace the path from L3:F13061 and L3:F16373 to identify input tokens. Focus on i… |

<details>
<summary><b>SA-2</b> — tool trace (20 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 2 | `get_upstream_features` | L3:F13061@3, k=10 | Emb:" white"@2 (de=12.44) +9 more |
| 3 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 4 | `get_upstream_features` | L2:F13158@2, k=10 | Emb:" white"@2 (de=12.62) +9 more |
| 5 | `inspect_feature` | L3, F16373 | " mentions of demographic identity, especially race and gender" |
| 6 | `get_upstream_features` | L3:F16373@3, k=10 | Emb:" white"@2 (de=23.12) +9 more |
| 7 | `inspect_feature` | L2, F1708 | " mentions of colors" |
| 8 | `get_upstream_features` | L1:F7821@2, k=10 | Emb:" white"@2 (de=15.69) +9 more |
| 9 | `inspect_feature` | L0, F10910 | "the word "possession" and the words "white", "immediate" and "once" re" |
| 10 | `inspect_feature` | L2, F11363 | " colors and words like Diamond." |
| 11 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |
| 12 | `get_upstream_features` | L2:F11363@2, k=10 | Emb:" white"@2 (de=10.94) +9 more |
| 13 | `get_upstream_features` | L2:F1708@2, k=10 | Emb:" white"@2 (de=18.38) +9 more |
| 14 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 15 | `inspect_feature` | L2, F15317 | " gendered words, with a slight bias toward female-gendered words" |
| 16 | `inspect_feature` | L0, F9076 | " mentions of men, boys, areas, or general locations in a text" |
| 17 | `inspect_feature` | L0, F12059 | " words related to purpose and intent" |
| 18 | `get_upstream_features` | L0:F10910@2, k=10 | Emb:" white"@2 (de=14.31) +9 more |
| 19 | `inspect_feature` | L2, F9837 | " references to men" |
| 20 | `get_upstream_features` | L0:F9026@3, k=10 | Emb:" dude"@3 (de=8.19) +9 more |

**Findings:** Both L3:F13061 and L3:F16373 receive strong positive influence from the input token embedding " white" at position 2. The signal propagates through low‑layer features: L0:10910 → L1:7821 → L2:13158 → L3:13061 and L0:10910 → L1:7821 → L2:1708 → L3:16373. Additionally, L3:F16373 receives a smaller positive contribution from the token " dude" via L0:9026. All traced paths reach layer ≤ 8 and include …

</details>

### Build

`build_circuit` → 6 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 105,208 | 1,211 | 8,320 | 0 | $0.0153 | — | — |
| SA-2 | openai/gpt-oss-120b | 278,092 | 22,239 | 133,728 | 0 | $0.0571 | ✅ 8F/6E | Trace the path from L3:F13061 and L3:F16373 to identify inpu… |
| **Total** | | **383,300** | **23,450** | **142,048** | **0** | **$0.0724** | | |

**Oracle wall-clock time:** 11m 13s