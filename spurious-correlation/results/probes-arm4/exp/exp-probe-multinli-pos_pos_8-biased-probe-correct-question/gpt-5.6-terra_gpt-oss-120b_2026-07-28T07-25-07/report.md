# Circuit Oracle Report
**Date:** 2026-07-28 07:25:07 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s contradiction score is driven primarily by lexical/entity features for *Congress*, *controls*, and *many*, rather than by a circuit that explicitly compares the two statements’ conflicting claims about Congressional responsibility for funding.

**Confidence:** 8/10

**Reasoning:** The synthetic probe target has probability 1, so the traced direction is the probe’s classification score rather than a language-model token logit. Its largest direct drivers are notably shallow: L0:6044 at position 2 (+0.789), L6:6096 at position 2 (+0.451), L1:2116 at position 7 (+0.379), L2:2701 at position 2 (+0.379), L3:13271 at position 5 (+0.359), L3:123 at position 2 (+0.356), and L3:8382 at position 13 (+0.328). This shallow, token-local profile already argues against a clean high-level relational contradiction computation.

The saved circuit has three principal positive paths:

1. **Congress/political-content path:**  
   `Emb: Congress (pos 2) → Congress/political entity detectors → Political-affiliation representation → contradiction probe`.
   * L2:2701 is explicitly a U.S.-Congress feature (frac_nonzero **0.01068**), and L3:123 is likewise a “mentions of the United States Congress” feature (frac_nonzero **0.00652**). L2:6735 detects political parties/politicians (frac_nonzero **0.00871**; promoted tokens include *party*, *Democrat*, *Republican*).  
   * These converge on L6:6096, a sparse political-party/affiliation feature (frac_nonzero **0.00587**, promoted token includes *Democrats*) that positively drives the probe by **+0.451**.  
   * Crucially, upstream attribution for L6:6096 is dominated by the raw `Congress` embedding at position 2 (**+13.81**), with the political detector L2:6735 supplying a further **+5.375**. L3:123 similarly receives its overwhelmingly largest positive input directly from `Congress` (**+20.625**). This is genuine entity/topic recognition—Congress/politics—but not a representation of the proposition “Congress controls funding” being contradicted later.

2. **Control-word path:**  
   `Emb: controls (pos 5) → Lexical control detector → contradiction probe`.
   * L3:13271 is a sparse detector for the literal word **“control”** (frac_nonzero **0.0036**) and contributes **+0.359** directly to the probe direction.
   * Its immediate upstream signal is dominated by the raw `controls` embedding (**+18.5**). Thus this branch is highly lexical. It signals occurrence of the predicate used in the first sentence, not whether the second sentence negates that predicate’s relation to Congress/funding.

3. **“Many” lexical path:**  
   `Emb: many (pos 13) → Lexical quantity detector → contradiction probe`.
   * L3:8382 detects **“many”** / nearby *times* or *people* (frac_nonzero **0.00376**) and adds **+0.328** to the probe. Its largest upstream contribution is the literal `many` embedding (**+23.5**).
   * This is plainly not necessary to the semantic contradiction. It is a superficial lexical correlate of this specific source sentence/template.

There is some content-relevant representation: the model detects *Congress* robustly, and the `controls` detector is relevant to the first statement’s subject–predicate content. But the circuit evidence does **not** show a feature binding the first claim (“Congress controls funding levels”) to the later denial (“Congress has no responsibility … controlling funding levels”), nor a specific negation/denial feature among the strongest positive contributors. Instead, the score is a mixture of sparse token/topic features—especially political/Congress content—and local lexical features for *controls* and *many*.

The negative contributors reinforce that this probe direction is not simply “semantic contradiction”: e.g., L0:13437 for **“who”** contributes **−0.582**, L2:6735 political content contributes **−0.402** directly despite also feeding the later political feature positively, and L2:156’s generic *levels/amount* representation contributes **−0.371**. Such mixed shallow coefficients are consistent with a linear probe exploiting correlated residual directions rather than a dedicated contradiction circuit.

Therefore, the user concern is substantially supported: this classification appears to rely materially on spurious or at least non-diagnostic lexical/topic cues. It uses actual prompt content in the narrow sense of recognizing *Congress* and *controls*, but the available causal paths do not establish that it computes the cross-sentence contradiction; in particular, *many* is an especially clear irrelevant positive cue.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | Congress/political entity detectors |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L2:F6735](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) | 2 | Congress/political entity detectors |  political parties and politicians | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | Congress/political entity detectors |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L6:F6096](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) | 2 | Political-affiliation representation |  political parties and affiliations | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) |
| [L3:F13271](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) | 5 | Lexical control detector |  the word "control." | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) |
| [L3:F8382](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) | 13 | Lexical quantity detector |  the word "many", and sometimes "times" or "people" when near it | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:6044 de=0.789 |
| 3 | `inspect_feature` ×7 | L0:6044, L6:6096, L1:2116, L2:2701, L3:13271, L3:123, L3:8382 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F6096@2` | ❌ error | — | — | Trace this strongest higher-layer positive driver of the synthetic contradiction… |
| SA-2 | `L3:F13271@5` | ❌ error | — | — | Trace this positive probe-driving path upstream to embeddings. Identify the text… |
| SA-3 | `L3:F8382@13` | ❌ error | — | — | Trace this positive probe-driving path upstream to embeddings and assess whether… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L0:13437, L2:6735, L1:6948, L2:156 |
| 2 | `get_upstream_features` | L6:F6096@2, k=20 → Emb:" Congress"@2 (de=13.81) +19 more |
| 3 | `get_upstream_features` | L3:F13271@5, k=15 → Emb:" controls"@5 (de=18.50) +14 more |
| 4 | `get_upstream_features` | L3:F8382@13, k=15 → Emb:" many"@13 (de=23.50) +14 more |
| 5 | `get_upstream_features` | L3:F123@2, k=15 → Emb:" Congress"@2 (de=20.62) +14 more |

### Build

`build_circuit` → 8 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 36,174 | 2,397 | 38,616 | 0 | $0.1360 | — | — |
| **Total** | | **36,174** | **2,397** | **38,616** | **0** | **$0.1360** | | |

**Oracle wall-clock time:** 0m 34s