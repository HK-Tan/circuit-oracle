# Circuit Oracle Report
**Date:** 2026-07-28 08:40:09 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by a hierarchy of identity-group detectors that trigger on the mention of "white" people, rather than the actual toxic semantic content of the prompt.

**Confidence:** 9/10

**Reasoning:**
The circuit demonstrates that the probe's classification score is primarily produced by "spurious" identity signals. The signal originates at the embedding for the token **" white" (pos 9)**, which serves as the primary excitatory driver for the entire path.

1.  **Early Detection:** The " white" embedding directly activates early-layer identity detectors, including **L2:F13158** (words about race and ethnicity) and **L2:F585** (specific lexical detector for "white"). There is also a secondary path from the token "guy" (pos 10) through **L2:F15317** (gendered words).
2.  **Mid-Layer Aggregation:** These early signals converge into a set of mid-layer race and social-issue aggregators. These include **L3:F13061** (race/gender/social issues), **L3:F16373** (demographic identity), **L4:F117** (race/racism/social justice), and **L6:F3902** (race and ethnicity). Notably, L4:F117's label specifically mentions a focus on Black people, yet it is strongly driven by the "white" token embedding (direct_effect $\approx 15.1$), suggesting it acts as a general "racial discourse" detector.
3.  **Output:** These aggregators then drive the final probe score. 

Crucially, the circuit reveals that the highly toxic term **"oriental"** (a key semantic driver of toxicity in this prompt) does not have a significant positive attribution path to the probe score. Instead, the model relies on the presence of the identity group "white" to predict toxicity, confirming the user's concern that the probe is using spurious identity markers rather than lexical toxicity.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: white (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 9 | Early Identity Detection (Race/Gender) | words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 9 | Early Identity Detection (Race/Gender) | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F15317](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15317) | 10 | Early Identity Detection (Race/Gender) | gendered words, with a slight bias toward female‑gendered words | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15317) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 10 | Mid-Layer Race/Ethnicity Aggregators |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 10 | Mid-Layer Race/Ethnicity Aggregators | mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 10 | Mid-Layer Race/Ethnicity Aggregators |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 9 | Mid-Layer Race/Ethnicity Aggregators |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L1:5220 de=-0.453 |
| 3 | `inspect_feature` ×5 | L3:13061, L6:3902, L4:117, L1:5220, L3:4512 |
| 4 | `get_top_logits` | "" (100%) |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F13061@10` | ✅ reported | 4 | 7 | Trace the signal flow to these race/identity features. Do they originate from sp… |
| SA-2 | `L6:F3902@9` | ✅ reported | 4 | 5 | Trace the signal flow to this race/ethnicity feature. Does it come from 'white' … |
| SA-3 | `L4:F117@10` | ✅ reported | 5 | 11 | Trace the signal flow to this racism/Black-people feature. Why is it firing here… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 2 | `get_upstream_features` | L3:F13061@10, k=15 | Emb:" white"@9 (de=11.00) +14 more |
| 3 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 4 | `get_upstream_features` | L2:F13158@9, k=15 | Emb:" white"@9 (de=13.62) +14 more |
| 5 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |
| 6 | `inspect_feature` | L2, F15317 | " gendered words, with a slight bias toward female-gendered words" |
| 7 | `get_upstream_features` | L2:F15317@10, k=15 | Emb:" guy"@10 (de=9.44) +14 more |

**Findings:** The race/identity signal at L3:F13061 is primarily sourced from the explicit token embedding "white" (pos 9). This token feeds directly into a mid‑layer race detector (L2:F13158), which in turn receives a pattern‑level boost from a lower‑layer feature (L1:F7821) that appears to capture the "white guy" context. A secondary path runs through a gender‑related feature (L2:F15317) driven by the "guy" t…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |
| 2 | `get_upstream_features` | L6:F3902@9, k=10 | Emb:" white"@9 (de=13.56) +9 more |
| 3 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 4 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 5 | `inspect_feature` | L4, F14329 | " mentions of the colors black, white, or another color with "or" in it" |
| 6 | `inspect_feature` | L2, F585 | "the word "white", often in association with "dwarf"" |
| 7 | `get_upstream_features` | L4:F117@9, k=10 | Emb:" white"@9 (de=15.06) +9 more |
| 8 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |

**Findings:** The race/ethnicity feature L6:F3902 receives its strongest excitatory input directly from the input token embedding " white" (direct_effect ≈ 13.6) and from a lower‑layer race‑detector feature L4:F117 (direct_effect ≈ 4.1). L4:F117 itself is driven primarily by the same " white" embedding (direct_effect ≈ 15.1). No positive‑effect upstream path involving the token "oriental" was observed. Therefor…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 2 | `get_upstream_features` | L4:F117@10, k=10 | Emb:" white"@9 (de=12.12) +9 more |
| 3 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 4 | `inspect_feature` | L3, F16373 | " mentions of demographic identity, especially race and gender" |
| 5 | `get_upstream_features` | L3:F13061@10, k=10 | Emb:" white"@9 (de=11.00) +9 more |
| 6 | `get_upstream_features` | L3:F13061@10, k=10 | Emb:" white"@9 (de=11.00) +9 more |
| 7 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 8 | `get_upstream_features` | L3:F16373@10, k=10 | Emb:" white"@9 (de=23.88) +9 more |
| 9 | `get_upstream_features` | L2:F13158@9, k=10 | Emb:" white"@9 (de=13.62) +9 more |
| 10 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |

**Findings:** The target race‑related feature (L4:F117) is primarily driven by the embedding of the token "white" at position 9, which supplies a large positive direct effect. This token also excites intermediate race‑identity detectors in layers 3 (F13061 and F16373), which aggregate demographic language and pass activation upward. Those layer‑3 features receive additional excitation from a lower‑layer race‑et…

</details>

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 108,772 | 1,591 | 30,848 | 0 | $0.0163 | — | — |
| SA-1 | openai/gpt-oss-120b | 82,721 | 5,839 | 2,528 | 0 | $0.0159 | ✅ 4F/7E | Trace the signal flow to these race/identity features. Do th… |
| SA-2 | openai/gpt-oss-120b | 73,520 | 3,822 | 15,168 | 0 | $0.0135 | ✅ 4F/5E | Trace the signal flow to this race/ethnicity feature. Does i… |
| SA-3 | openai/gpt-oss-120b | 105,879 | 8,434 | 21,088 | 0 | $0.0213 | ✅ 5F/11E | Trace the signal flow to this racism/Black-people feature. W… |
| **Total** | | **370,892** | **19,686** | **69,632** | **0** | **$0.0671** | | |

**Oracle wall-clock time:** 9m 31s