# Circuit Oracle Report
**Date:** 2026-07-28 08:39:48 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

> **Circuit Summary:**
> `Emb: not (pos 21)` $\rightarrow$ `Negation_Lexical (L0:F4958)` $\rightarrow$ `Negation_Patterns (L16:F12358, etc.)` $\rightarrow$ `Probe_Output`

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 21 | Lexical Negation Detection (not) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 21 | Syntactic Negation Patterns (not...be) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 21 | Syntactic Negation Patterns (not...be) | "not" or negative terms, with some bonus for sports-related terms and "purpose". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 21 | Syntactic Negation Patterns (not...be) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 21 | Syntactic Negation Patterns (not...be) | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 21 | Syntactic Negation Patterns (not...be) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L0:3498 de=-0.785 |
| 3 | `inspect_feature` ×4 | L16:12358, L4:4492, L3:8011, L3:1101 |

### Dispatch: 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@21` | ✅ reported | 8 | 10 | Trace the path from L16:F12358. This feature detects "not" followed by "to be", … |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F12358 | " the word "not" followed within a few tokens by a form of the verb "to" |
| 2 | `get_upstream_features` | L16:F12358@21, k=10 | Emb:" not"@21 (de=19.00) +9 more |
| 3 | `inspect_feature` | L0, F4958 | " the word "not"" |
| 4 | `get_upstream_features` | L0:F4958@21, k=5 | Emb:" not"@21 (de=33.75) +4 more |
| 5 | `inspect_feature` | L0, F9646 | " words that indicate the degree, scale, or validity of something" |
| 6 | `inspect_feature` | L2, F12021 | ""not" or negative terms, with some bonus for sports-related terms and " |
| 7 | `get_upstream_features` | L2:F12021@21, k=10 | Emb:" not"@21 (de=23.12) +9 more |
| 8 | `get_upstream_features` | L0:F9646@21, k=5 | Emb:" were"@20 (de=14.00) +4 more |
| 9 | `inspect_feature` | L15, F10071 | "negations and equivocations" |
| 10 | `get_upstream_features` | L15:F10071@21, k=10 | Emb:" not"@21 (de=9.81) +9 more |
| 11 | `inspect_feature` | L3, F8011 | " a mix of words and code fragments from different languages" |
| 12 | `inspect_feature` | L13, F3295 | "negations in the form of "is/are not" as well as other uses of "not"" |
| 13 | `inspect_feature` | L4, F4492 | "negations in various languages" |

**Findings:** The target L16:F12358 (negation pattern detector) receives its strongest excitatory drive directly from the embedding of the token "not" (direct_effect 19.0) and from a low‑layer lexical detector L0:F4958 which simply flags the presence of "not" (direct_effect 6.4). Both are positive, confirming that the feature is indeed driven by the token "not" at position 21. Additional upstream contributors i…

</details>

### Build

`build_circuit` → 4 nodes, 3 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 54,737 | 1,030 | 24,448 | 0 | $0.0084 | — | — |
| SA-1 | openai/gpt-oss-120b | 169,970 | 12,371 | 25,344 | 0 | $0.0333 | ✅ 8F/10E | Trace the path from L16:F12358. This feature detects "not" f… |
| **Total** | | **224,707** | **13,401** | **49,792** | **0** | **$0.0417** | | |

**Oracle wall-clock time:** 9m 6s