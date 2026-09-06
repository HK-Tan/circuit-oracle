# Circuit Oracle Report
**Date:** 2026-07-28 08:33:03 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by a circuit that detects race-related terminology, specifically triggered by the word "race" in the input, rather than analyzing the semantic toxicity of the sentence.

**Confidence:** 10/10

**Reasoning:**
The attribution circuit reveals a direct causal path from the input token "race" to the probe's high classification score. 
1. **Input Source:** The signal originates at the embedding for the token `" race"` (pos 5), which has a strong positive direct effect on downstream race-detection features.
2. **Mid-Layer Processing:** The signal is amplified by a supernode of "Race/Justice Terminology Detectors" in Layer 4. Specifically, `L4:F5584` (words related to race, ethnicity, nationality) and `L4:F117` (terms related to race, racism, and social justice) detect the lexical presence of race-related language.
3. **Late-Layer Driving:** These feed into `L6:F3902` ("terms referring to race and ethnicity"), which acts as the primary driver for the probe's output score. `L6:F3902` has a high `direct_effect` (0.5859) and a low `frac_nonzero` (0.01786), indicating it is a selective feature for race-related concepts.
4. **Mechanism:** The probe is not identifying "toxicity" in the sense of harmful intent or hate speech, but is instead acting as a "race-mention detector." Because the signal flows directly from the embedding of the word "race" through generic identity-group detectors to the output, this confirms the user's concern: the probe relies on spurious identity-group signals (the mere mention of race) rather than the actual lexical or semantic content that would constitute toxicity.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: race (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L4:F5584](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) | 6 | Race/Justice Terminology Detectors | words related to race, ethnicity, nationality or population groups | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Race/Justice Terminology Detectors |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 6 | Race/Ethnicity Feature (Probe Driver) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:3902 de=0.586 |
| 3 | `inspect_feature` ×4 | L6:3902, L4:117, L3:13061, L2:10509 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 10 features; top: L6:3902 de=0.586 |
| 6 | `inspect_feature` ×4 | L6:3902, L2:10509, L4:117, L3:13061 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_upstream_features` | Emb:" race"@5 (de=19.00) +4 more |
| 9 | `get_top_features` | 10 features; top: L6:3902 de=0.586 |
| 10 | `inspect_feature` | " terms referring to race and ethnicity" |

### Dispatch: 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@6` | ✅ reported | 4 | 4 | Trace the signal from L6:F3902 (race/ethnicity feature) back to the input tokens… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |
| 2 | `get_upstream_features` | L6:F3902@6, k=15 | Emb:" race"@5 (de=11.00) +14 more |
| 3 | `inspect_feature` | L4, F5584 | " words related to race, ethnicity, nationality or population groups" |
| 4 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 5 | `inspect_feature` | L5, F12135 | " terms related to discrimination based on identity" |
| 6 | `get_upstream_features` | L4:F5584@6, k=10 | Emb:" race"@5 (de=16.62) +9 more |
| 7 | `get_upstream_features` | L4:F117@6, k=10 | Emb:" race"@5 (de=19.00) +9 more |

**Findings:** The L6:F3902 race/ethnicity probe receives its strongest excitation from the raw input token " race" at position 5 (direct_effect 11.0). Upstream, two lower‑layer (≤8) features—L4:5584 and L4:117—contribute sizable positive effects (≈5 each) by detecting generic race terminology and race‑justice discourse respectively. A higher‑layer (L5:12135) discrimination detector adds a modest boost. The path…

</details>

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 317,205 | 1,337 | 4,224 | 0 | $0.0450 | — | — |
| SA-1 | openai/gpt-oss-120b | 70,877 | 3,807 | 0 | 0 | $0.0129 | ✅ 4F/4E | Trace the signal from L6:F3902 (race/ethnicity feature) back… |
| **Total** | | **388,082** | **5,144** | **4,224** | **0** | **$0.0579** | | |

**Oracle wall-clock time:** 2m 25s