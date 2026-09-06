# Circuit Oracle Report
**Date:** 2026-07-28 08:37:07 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by the detection of specific identity group keywords ("Muslim", "gay") and social justice terminology, rather than the actual harmful intent or syntactic structure of the prompt.

**Confidence:** 10/10

**Reasoning:**
The attribution circuit reveals that the probe's classification score is primarily the sum of three independent paths, each corresponding to a specific keyword or phrase in the input text:

1.  **LGBTQ+ Identity Path:** The most significant contribution comes from the token `" gay"` (pos 17). This embedding drives early-layer LGBTQ+ identity features (L4:F15899, L4:F8645), which in turn excite high-level detectors for homosexuality and same-sex marriage (L6:F6085, L8:F15771). These late-layer features feed directly into the probe logit.
2.  **Muslim Identity Path:** The token `"Muslim"` (pos 12) drives a sequence of religious identity features, starting from a Middle-East name detector (L0:F13885) and a general religion feature (L2:F31), converging on a high-level Muslim detector (L6:F7282) that pushes the probe score higher.
3.  **Social Justice Path:** The tokens `" social"` (pos 5) and `" justice"` (pos 6) trigger a cluster of lexical features related to social programs and services (L0:F3591, L1:F13646, L3:F5157). These flow into an abstract "social justice" feature (L4:F117), which also contributes positively to the probe.

Notably, the circuit contains no evidence of the probe detecting the word "warrior" or the aggressive/imperative structure of the sentence ("go to... and order..."). The probe is essentially acting as a "keyword detector" for protected groups and politically charged terms, confirming the user's concern that it relies on spurious identity signals rather than actual toxic semantics.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: social justice (pos 5,6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: social justice (pos 5,6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F3591](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) | 6 | Social Justice Lexical Features | terms related to government social programs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 6 | Social Justice Lexical Features | text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L3:F5157](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5157) | 6 | Social Justice Lexical Features | references to social services and social work | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5157) |
| [L0:F11685](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11685) | 6 | Social Justice Lexical Features | words related to social justice | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11685) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Social Justice Abstract Feature (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: Muslim (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F13885](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) | 12 | Muslim/Religious Identity Features |  names of people and places, specifically those related to the middle east | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) |
| [L2:F31](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/31) | 12 | Muslim/Religious Identity Features |  terms related to paganism, neopaganism, and related cultural celebrations and historical terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/31) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 12 | Muslim/Religious Identity Features |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 12 | Muslim High-Level Detector (L6:F7282) |  mentions of Islam or Middle Eastern places and people, as well as mentions of a specific district. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: gay (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 17 | LGBTQ+ Identity Features | language associated with the LGBTQ community and discussions of gender and identity. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L4:F8645](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) | 17 | LGBTQ+ Identity Features | passages discussing same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 17 | LGBTQ+ High-Level Features (L6:F6085, L8:F15771) |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 17 | LGBTQ+ High-Level Features (L6:F6085, L8:F15771) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L6:6085 de=0.326 |
| 3 | `inspect_feature` ×5 | L6:6085, L8:15771, L4:117, L6:7282, L4:2405 |
| 4 | `get_top_logits` | "" (100%) |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F6085@17` | ✅ reported | 7 | 12 | Trace the path from L6:F6085 and L8:F15771 to see if they originate from LGBTQ+ … |
| SA-2 | `L6:F7282@12` | ✅ reported | 4 | 7 | Trace the path from L6:F7282 and L4:F2405 to see if they originate from Muslim/r… |
| SA-3 | `L4:F117@6` | ✅ reported | 7 | 15 | Trace the path from L4:F117 to see if it originates from 'social justice warrior… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F6085 | " text related to homosexuality and same-sex marriage" |
| 2 | `get_upstream_features` | L6:F6085@17, k=10 | Emb:" gay"@17 (de=37.00) +9 more |
| 3 | `inspect_feature` | L4, F8645 | " passages discussing same-sex marriage" |
| 4 | `inspect_feature` | L8, F15771 | "discussion of LGBTQ+ issues, especially same-sex marriage, adoption, a" |
| 5 | `get_upstream_features` | L8:F15771@17, k=10 | Emb:" gay"@17 (de=17.00) +9 more |
| 6 | `get_upstream_features` | L4:F8645@17, k=10 | Emb:" gay"@17 (de=22.88) +9 more |
| 7 | `inspect_feature` | L4, F15899 | " language associated with the LGBTQ community and discussions of gende" |
| 8 | `inspect_feature` | L7, F16171 | " texts about homosexuality, gay marriage, and religious views on these" |

**Findings:** Both L6:F6085 and L8:F15771 are primarily driven by the token embedding for the word 'gay' at position 17 (large positive direct effects). Upstream analysis shows that the strongest upstream drivers are lower‑layer features (layers 4 and 6) that themselves detect LGBTQ‑related language such as same‑sex marriage and gender identity. These lower‑layer features satisfy the requirement to reach the lo…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F7282 | " mentions of Islam or Middle Eastern places and people, as well as men" |
| 2 | `get_upstream_features` | L6:F7282@12, k=10 | Emb:" Muslim"@12 (de=22.62) +9 more |
| 3 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 4 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 5 | `get_upstream_features` | L4:F2405@12, k=10 | Emb:" Muslim"@12 (de=15.75) +9 more |
| 6 | `inspect_feature` | L2, F31 | " terms related to paganism, neopaganism, and related cultural celebrat" |
| 7 | `get_upstream_features` | L0:F13885@12, k=10 | Emb:" Muslim"@12 (de=10.38) +9 more |
| 8 | `get_upstream_features` | L2:F31@12, k=10 | Emb:" Muslim"@12 (de=12.88) +9 more |

**Findings:** Both L6:F7282 and L4:F2405 receive strong positive direct effects from the input embedding of the token "Muslim" at position 12 (22.6 and 15.8 respectively). The path from the low‑layer Middle‑East name detector (L0:F13885) and the generic religious‑term detector (L2:F31) also converge on the same token embedding, confirming that these higher‑level features are grounded in the Muslim/religious ide…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 2 | `get_upstream_features` | L4:F117@6, k=10 | Emb:" justice"@6 (de=5.12) +9 more |
| 3 | `inspect_feature` | L0, F3591 | " terms related to government social programs" |
| 4 | `get_upstream_features` | L0:F3591@6, k=10 | Emb:" social"@5 (de=21.00) +9 more |
| 5 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |
| 6 | `get_upstream_features` | L1:F13646@6, k=10 | Emb:" justice"@6 (de=4.22) +9 more |
| 7 | `inspect_feature` | L3, F5157 | " references to social services and social work" |
| 8 | `get_upstream_features` | L3:F5157@6, k=10 | Emb:" social"@5 (de=24.12) +9 more |
| 9 | `inspect_feature` | L2, F1537 | " words and phrases related to political and social issues and movement" |
| 10 | `inspect_feature` | L1, F15781 | " the phrase "ends of justice" and words implying a shift in law or leg" |
| 11 | `inspect_feature` | L0, F11685 | " words related to social justice" |

**Findings:** The L4:F117 node that fires on race‑related social‑justice language is driven almost entirely by the token embeddings for the words 'social' (pos5) and 'justice' (pos6). These embeddings feed directly into L4:F117 and also cascade through a set of low‑layer lexical features (L0:F3591, L1:F13646, L3:F5157, L0:F11685) that are each specialized for social‑program, social‑justice, and social‑service t…

</details>

### Build

`build_circuit` → 10 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 108,478 | 1,658 | 4,224 | 0 | $0.0159 | — | — |
| SA-2 | openai/gpt-oss-120b | 85,801 | 5,768 | 10,912 | 0 | $0.0165 | ✅ 4F/7E | Trace the path from L6:F7282 and L4:F2405 to see if they ori… |
| SA-1 | openai/gpt-oss-120b | 82,968 | 7,603 | 15,168 | 0 | $0.0172 | ✅ 7F/12E | Trace the path from L6:F6085 and L8:F15771 to see if they or… |
| SA-3 | openai/gpt-oss-120b | 112,178 | 9,588 | 15,168 | 0 | $0.0228 | ✅ 7F/15E | Trace the path from L4:F117 to see if it originates from 'so… |
| **Total** | | **389,425** | **24,617** | **45,472** | **0** | **$0.0724** | | |

**Oracle wall-clock time:** 6m 28s