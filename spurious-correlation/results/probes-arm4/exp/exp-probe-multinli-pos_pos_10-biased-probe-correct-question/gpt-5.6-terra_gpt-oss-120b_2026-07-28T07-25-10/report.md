# Circuit Oracle Report
**Date:** 2026-07-28 07:25:10 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven primarily by the second sentence’s surface form—especially the token **“not”** in *“There is not role reversal…”* and its local *“not + is”* construction—rather than by a circuit that compares the two propositions’ meanings.

**Confidence:** 9/10

**Reasoning:** The saved circuit has a clear lexical-negation pathway from **Emb: ` not` (pos 17)**, with a smaller local syntactic contribution from **Emb: ` is` (pos 16)**, into the probe direction.

- The most direct early feature is **L0:4958 at pos 17**, labelled *“the word ‘not’”* (`frac_nonzero=0.0184`). It is a highly selective lexical detector, not an entity- or proposition-specific feature. It directly supports the probe score (+0.6797) and strongly excites the late feature **L16:12358** (+8.125 upstream effect).
- At layer 3, the circuit contains a cluster of generic negation/absence features:
  - **L3:8011** (`frac_nonzero=0.00299`), labelled a multilingual/code-fragment mixture but with promoted tokens overwhelmingly *not / NOT / nicht / geen*; it contributes positively to the probe (+0.6641) and to **L4:4492** (+3.2969).
  - **L3:12079** (`frac_nonzero=0.00976`), labelled *“negations and Chinese names,”* with activating examples including English *not/no*; it contributes +0.6602 and feeds **L4:4492** (+2.8906).
  - **L3:1101** (`frac_nonzero=0.00901`), an absence/negation feature from software-error contexts. Its probe effect is negative (-1.2109), and it negatively feeds both layer-4 negation features. This indicates the probe direction is not a clean semantic “contradiction” axis: different variants of the same broad negation family receive opposing weights.
- The two largest direct effects on the probe are both layer-4 multilingual-negation features at the exact **` not`** position:
  - **L4:4492**, *“negations in various languages”* (`frac_nonzero=0.03828`), supports the probe (+1.2188). Its largest upstream input is directly **Emb: ` not`** (+18), with additional support from the layer-3 negation features.
  - **L4:2422**, *“negations in other languages…”* (`frac_nonzero=0.01567`), opposes it (-1.2734) but is likewise driven most strongly by exactly the same **Emb: ` not`** (+16.5). Thus, the score reflects a signed mixture of local negation detectors, rather than a stable semantic relation representation.
- The highest-layer meaningful feature, **L16:12358** (`frac_nonzero=0.02769`), is explicitly labelled *“the word ‘not’ followed within a few tokens by a form of the verb ‘to be’.”* It contributes positively (+0.6562). Its upstream attribution is dominated by **` not`** (+23.125), then **L0:4958** (+8.125), and the local copula **` is`** (+4.375). This is direct evidence of a local grammatical-template detector: **“is not”**, not a cross-sentence contradiction computation.

The circuit therefore does **not** show evidence that the probe compares the first claim (*“role reversal is going on …”*) against the second claim’s denial, aligns the shared predicate *role reversal going on*, or composes the relevant semantic negation. There is a small upstream input from **` reversal` (pos 4)** into L16:12358 (+1.7578), but it is far weaker than the `not` pathway and is not evidence of a proposition-level comparison.

Most importantly, the decisive source tokens and features are concentrated at position 17 on **“not”**, with a nearby dependency on **“is.”** The user’s concern is supported: this probe’s classification is substantially driven by spurious lexical/syntactic negation cues. The opposing signs among several negation features also suggest the linear probe is exploiting an idiosyncratic residual-space mixture correlated with contradiction labels, rather than representing contradiction robustly or semantically.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Direct lexical negation detector |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | Early negation / absence pattern features |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | Early negation / absence pattern features | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | Early negation / absence pattern features |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Mid-layer multilingual-negation feature (positive signed probe path) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Mid-layer multilingual-negation feature (negative signed probe path) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 17 | Late `not` + nearby copula feature |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:2422 de=-1.273 |
| 3 | `inspect_feature` ×4 | L4:2422, L4:4492, L3:1101, L16:12358 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F4492@17` | ❌ error | — | — | Trace the strongest positive probe-driving feature. Determine its semantic conte… |
| SA-2 | `L4:F2422@17` | ❌ error | — | — | Trace the strongest negative probe-driving feature; determine what opposing-clas… |
| SA-3 | `L3:F1101@17` | ❌ error | — | — | Trace this strong negative feature upstream to characterize its cue and token or… |
| SA-4 | `L16:F12358@17` | ❌ error | — | — | Trace the highest-layer positive feature upstream to discover whether it supplie… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F4492@17, k=15 → Emb:" not"@17 (de=18.00) +14 more |
| 2 | `get_upstream_features` | L4:F2422@17, k=15 → Emb:" not"@17 (de=16.50) +14 more |
| 3 | `get_upstream_features` | L3:F1101@17, k=15 → Emb:" not"@17 (de=13.19) +14 more |
| 4 | `get_upstream_features` | L16:F12358@17, k=15 → Emb:" not"@17 (de=23.12) +14 more |
| 5 | `inspect_feature` ×3 | L0:4958, L3:8011, L3:12079 |

### Build

`build_circuit` → 8 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 19,474 | 2,424 | 39,879 | 0 | $0.0950 | — | — |
| **Total** | | **19,474** | **2,424** | **39,879** | **0** | **$0.0950** | | |

**Oracle wall-clock time:** 0m 38s