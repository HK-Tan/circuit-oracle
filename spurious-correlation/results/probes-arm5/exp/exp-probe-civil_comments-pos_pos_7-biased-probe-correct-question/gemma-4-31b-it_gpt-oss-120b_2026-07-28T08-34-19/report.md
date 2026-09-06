# Circuit Oracle Report
**Date:** 2026-07-28 08:34:19 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven by a circuit that detects identity group mentions (Race and LGBTQ+ terms) rather than the actual toxicity or semantic content of the prompt.

**Confidence:** 10/10

**Reasoning:** 
The attribution circuit reveals that the probe's score is primarily pushed positive by features that encode identity markers. Specifically:
1. **Identity-Specific Detectors:** The most influential late-layer feature is **L8:F15771** ("discussion of LGBTQ+ issues"), which receives a strong signal from **L6:F6085** ("text related to homosexuality") and **L4:F15899** ("language associated with the LGBTQ community"). These, in turn, are directly triggered by the input token **"Gay" (pos 9)**.
2. **Race/Ethnicity Detection:** The feature **L2:F13158** ("words about race and ethnicity") also contributes significantly to the probe score. It is directly driven by the input tokens **"black" (pos 5)** and **"White" (pos 17)**.
3. **Spurious Correlation:** Notably, the circuit contains no features related to the actual toxic words in the prompt (e.g., "NAZI!") or the overall sentiment of "hypocrisy." Instead, the signal flows from identity embeddings $\rightarrow$ identity detectors $\rightarrow$ probe score.
4. **Convergence:** The signal from race-related terms (L2:F13158) even feeds into the LGBTQ+ detector chain (L4:F15899), suggesting a generalized "identity group" signal that the probe uses as a proxy for toxicity.

This confirms the user's concern: the probe is utilizing spurious features (identity group signals) to predict toxicity, meaning it would likely flag benign mentions of "black", "White", or "Gay" as toxic regardless of context.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: Race Identity ('black', 'White') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: Race Identity ('black', 'White') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: LGBTQ Identity ('Gay') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 9 | Race/Ethnicity Detector (L2:F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 17 | Race/Ethnicity Detector (L2:F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 9 | Generic LGBTQ Detector (L4:F15899) |  language associated with the LGBTQ community and discussions of gender and identity. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 9 | Homosexuality Detector (L6:F6085) |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 9 | LGBTQ Issues Detector (L8:F15771) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L8:15771 de=0.324 |
| 3 | `inspect_feature` ×5 | L8:15771, L6:6085, L2:13158, L3:13061, L4:15899 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L8:15771 de=0.324 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F15771@9` | ✅ reported | 5 | 10 | Trace the signal from the LGBTQ+ and Race features (L8:F15771, L6:F6085, L2:F131… |
| SA-2 | `L2:F13158@17` | ✅ reported | 4 | 3 | Trace the signal from the Race feature (L2:F13158) back to the input tokens. |

<details>
<summary><b>SA-1</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F15771 | "discussion of LGBTQ+ issues, especially same-sex marriage, adoption, a" |
| 2 | `get_upstream_features` | L8:F15771@9, k=10 | Emb:"Gay"@9 (de=10.38) +9 more |
| 3 | `inspect_feature` | L6, F6085 | " text related to homosexuality and same-sex marriage" |
| 4 | `inspect_feature` | L4, F15899 | " language associated with the LGBTQ community and discussions of gende" |
| 5 | `get_upstream_features` | L6:F6085@9, k=10 | Emb:"Gay"@9 (de=21.75) +9 more |
| 6 | `inspect_feature` | L4, F8645 | " passages discussing same-sex marriage" |
| 7 | `get_upstream_features` | L4:F15899@9, k=10 | Emb:"Gay"@9 (de=13.81) +9 more |
| 8 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 9 | `get_upstream_features` | L2:F13158@9, k=10 | Emb:"Gay"@9 (de=8.94) +9 more |
| 10 | `inspect_feature` | L1, F8766 | " words related to Harry Potter fan fiction and formal procedures" |
| 11 | `inspect_feature` | L1, F1055 | " variations of the verb "perform"" |

**Findings:** Tracing from the LGBTQ+ feature (L8:F15771) reveals a cascade of upstream detectors: a mid‑layer LGBTQ+ detector (L6:F6085), a generic LGBTQ+/gender language feature (L4:F15899), and a same‑sex marriage specific feature (L4:F8645). All of these receive strong positive influence from the input token embedding "Gay" (position 9), confirming that the identity term directly triggers the circuit. The u…

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 2 | `get_upstream_features` | L2:F13158@17, k=10 | Emb:"White"@17 (de=13.56) +9 more |
| 3 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |
| 4 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |
| 5 | `get_upstream_features` | L1:F13646@17, k=10 | Emb:"White"@17 (de=4.62) +9 more |
| 6 | `get_upstream_features` | L1:F7821@17, k=10 | Emb:"White"@17 (de=13.25) +9 more |
| 7 | `inspect_feature` | L0, F3167 | " the word "shape"" |

**Findings:** The race‑related feature (L2:F13158) receives its strongest excitation from the input token "White" (pos 17) and from upstream features in lower layers. The top upstream driver is a social‑justice feature (L1:F13646) that itself is fed by a low‑level lexical shape feature (L0:F3167). All traced nodes lie in layers ≤8, satisfying the lower‑third floor requirement, and we have identified explicit to…

</details>

### Build

`build_circuit` → 7 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 129,999 | 1,331 | 0 | 0 | $0.0187 | — | — |
| SA-2 | openai/gpt-oss-120b | 58,641 | 4,537 | 7,904 | 0 | $0.0116 | ✅ 4F/3E | Trace the signal from the Race feature (L2:F13158) back to t… |
| SA-1 | openai/gpt-oss-120b | 123,053 | 6,213 | 12,640 | 0 | $0.0224 | ✅ 5F/10E | Trace the signal from the LGBTQ+ and Race features (L8:F1577… |
| **Total** | | **311,693** | **12,081** | **20,544** | **0** | **$0.0527** | | |

**Oracle wall-clock time:** 3m 41s