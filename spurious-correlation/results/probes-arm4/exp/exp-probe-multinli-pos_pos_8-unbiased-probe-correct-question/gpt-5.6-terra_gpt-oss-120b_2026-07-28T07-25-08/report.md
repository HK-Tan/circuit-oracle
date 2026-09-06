# Circuit Oracle Report
**Date:** 2026-07-28 07:25:08 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s contradiction score is driven chiefly by lexical/entity recognition of **“Congress”**, with additional shallow syntactic cues for **“began to”** and **“include,”** rather than by a circuit that explicitly represents the final negated claim (“no responsibility”).

**Confidence:** 8/10

**Reasoning:** The output is a synthetic probe target (the only returned “token” was the empty probe label), so feature direct effects measure contributions to the **classification direction**, not next-token generation.

The strongest positive contributor is **L2:F2701 at pos 2** (activation 22.25; direct effect **+0.8477**), an unusually selective U.S.-Congress detector (`frac_nonzero=0.01068`). Its activating examples are directly triggered by *Congress*, and its upstream attribution is overwhelmingly the raw **Emb: “ Congress” (pos 2)** with positive effect **+28.125**. This is an entity-specific lexical path, not a contradiction computation. It feeds the probe directly.

A parallel later Congress feature, **L3:F123 at pos 2** (direct effect **+0.25**), is likewise labeled “mentions of the United States Congress” (`frac_nonzero=0.00652`) and obtains **+20.625** directly from **Emb: “ Congress” (pos 2)**. The circuit therefore contains robust recognition of the shared subject/entity, but the inspected paths do not show a comparator joining the first sentence’s *controls funding* proposition to the second sentence’s *no responsibility controlling funding* denial.

The early political detector **L0:F15411 at pos 2** (direct effect **+0.4902**, `frac_nonzero=0.0079`) is also fed by **Congress** (**+17.0**) and detects political bodies/processes. It provides a weaker supporting lexical signal. In contrast, the other L0 feature grouped beside it, **L0:F6044**, has a misleading local activation at this position: Neuronpedia labels it a *yield* detector (`frac_nonzero=0.02939`), but it too is directly sourced mainly from the **Congress** embedding (**+17.0**). Thus its positive probe effect (+0.4922) should not be interpreted as semantic evidence for contradiction; it is likely an accidental/basis-level feature aligned with the probe direction at this token.

The remaining high-positive paths are primarily surface-form/syntactic:

- **L3:F5753 at pos 12** contributes **+0.5273** and detects *include/includes/containing* (`frac_nonzero=0.00202`). It is driven almost entirely by **Emb: “ include” (pos 12)**, with **+41.0** direct upstream effect. Its contribution appears to be a lexical/template association, not negation or logical incompatibility.
- **L4:F59 at pos 11** contributes **+0.4141** and detects verb/start/begin + *to* constructions (`frac_nonzero=0.02046`). It receives **+13.3125** from **Emb: “ began” (pos 10)** and **+2.0625** from **Emb: “ to” (pos 11)**. This captures the first sentence’s “began to include” construction, again without representing the contradiction relation.

The saved circuit reflects these paths: **Emb: Congress → political/Congress entity detectors → probe**, plus **Emb: include → inclusion-construction detector → probe** and **Emb: began → began-to template → probe**.

Critically, none of the dominant positive features inspected is a detector for **“no,” “not,” “no responsibility,”** denial, responsibility, or a cross-sentence reversal of the *controls funding* relation. There are negative contributors (for example L3:F8351, an include-related feature, −0.3477), but they do not establish a negation-based positive mechanism either. Therefore, the user’s specific concern is only partly supported: the circuit is **not primarily using a “negation word” feature** in the traced top paths. However, it is indeed relying substantially on **spurious shallow lexical and syntactic correlations**—Congress/political vocabulary and “include/began-to” form—rather than a compositional semantic contradiction circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F15411](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) | 2 | Congress/political lexical detectors |  terms relating to political bodies, figures, and processes | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) |
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | Congress/political lexical detectors | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | U.S. Congress entity features |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | U.S. Congress entity features |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L3:F5753](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) | 12 | Inclusion-construction detector |  the word "includes" or "containing". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) |
| [L4:F59](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) | 11 | Began/start-to syntactic template |  phrases with the word 'to' preceded by a verb or the word 'start' or 'begin'. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L2:2701 de=0.848 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F2701@2` | ❌ error | — | — | Trace the strongest positive probe-driving feature upstream to embeddings. Deter… |
| SA-2 | `L3:F5753@12` | ❌ error | — | — | Trace this positive probe-driving feature upstream to embeddings. Determine what… |
| SA-3 | `L4:F59@11` | ❌ error | — | — | Trace this positive probe-driving feature upstream to embeddings. Determine sema… |
| SA-4 | `L0:F6044@2` | ❌ error | — | — | Inspect and trace this direct positive input-level probe feature, including embe… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L2:2701, L3:5753, L4:59, L0:6044, L0:15411, L3:123, L0:10401, L3:8351 |
| 2 | `get_upstream_features` | L2:F2701@2, k=20 → Emb:" Congress"@2 (de=28.12) +19 more |
| 3 | `get_upstream_features` | L3:F5753@12, k=20 → Emb:" include"@12 (de=41.00) +19 more |
| 4 | `get_upstream_features` | L4:F59@11, k=20 → Emb:" began"@10 (de=13.31) +19 more |
| 5 | `get_upstream_features` | L3:F123@2, k=20 → Emb:" Congress"@2 (de=20.62) +19 more |
| 6 | `get_upstream_features` | L0:F6044@2, k=20 → Emb:" Congress"@2 (de=17.00) +19 more |
| 7 | `get_upstream_features` | L0:F15411@2, k=20 → Emb:" Congress"@2 (de=17.00) +19 more |

### Build

`build_circuit` → 8 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 17,836 | 2,249 | 57,956 | 0 | $0.0928 | — | — |
| **Total** | | **17,836** | **2,249** | **57,956** | **0** | **$0.0928** | | |

**Oracle wall-clock time:** 0m 34s