# Circuit Oracle Report
**Date:** 2026-07-28 07:26:00 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction-probe score is driven primarily by a lexical/syntactic **negation** circuit—especially the two occurrences of *not* and the final *is not* construction—rather than by a circuit that compares the abbey’s asserted *steeple/height* properties across sentences.

**Confidence:** 9/10

**Reasoning:** The saved circuit identifies a dominant path from the embeddings for **“not”** at pos 29 (the final *“is not …”*) and pos 23 (*“will not forget”*) through lexical negation detectors into late features that directly raise the synthetic probe score.

- The strongest positive output-driving feature is **L16:F12358 at pos 29** (direct effect **+0.3594**). It is highly specifically a local negation/copula pattern detector: *“not followed within a few tokens by a form of ‘to be’”* (frac_nonzero **0.02769**). Its principal upstream input is directly the final **Emb: “not” (pos 29)**, with a very large positive contribution (**+19.5**), followed by **Emb: “is” (pos 28)** (**+4.41**) and the earlier negation feature **L13:F3295** (**+3.13**). This is compelling evidence that the probe reads the surface form of the final *“is not”*, not a resolved conflict between the two descriptions.

- **L13:F3295 at pos 29** is likewise a generic negation feature, labelled *“negations in the form of ‘is/are not’ as well as other uses of ‘not’”* (frac_nonzero **0.01255**) and contributes **+0.1855** to the probe. Its primary upstream source is again **Emb: “not” (pos 29)** (**+17.75**), with a smaller copular contribution from **Emb: “is” (pos 28)** (**+3.33**). The lower-level component, **L0:F4958**, is simply *“the word ‘not’”* (frac_nonzero **0.0184**) at both relevant positions.

- A second late positive feature, **L16:F9779 at pos 23** (direct effect **+0.2393**), detects *“negation words or contractions like ‘won’t’, ‘not’, ‘never’”* (frac_nonzero **0.01701**). Its upstream attribution points directly to **Emb: “not” (pos 23)** (**+6.81**) and **Emb: “will” (pos 22)** (**+7.31**): the entirely non-contradictory phrase *“you will not forget.”* This is particularly strong evidence for the user’s concern: a negation in the **first** sentence is supporting a contradiction classification despite not expressing the semantic mismatch.

- The only clearly topical/content feature among the major positives is **L14:F10408 at pos 14** (direct effect **+0.1758**), a water/geographic-location feature with promoted tokens including *sea, seawater, seaweed, coastal,* and *ocean* (frac_nonzero **0.01482**). It is overwhelmingly sourced by **Emb: “sea” (pos 14)** (**+22.88**). This contributes to the score, but it encodes the scenic setting, not the critical relation that the same abbey is first described as *steepled* and later as *lacking a steeple*.

The circuit therefore flows as:

1. **Embeddings:** *not* (positions 23 and 29), *will* (22), and *is* (28)  
2. **L0 lexical detector:** **F4958**, a literal *not* feature  
3. **L13 composition:** **F3295**, *is/are not*  
4. **L16 output-facing detectors:** **F12358** (not + copula) and **F9779** (generic negation)  
5. **Probe output:** synthetic contradiction-probe score.

A weakly relevant parallel input is **Emb: sea (pos 14) → L14:F10408 → probe**, but this is content/topic association, not contradiction detection.

Thus, this instance supports the concern: the classification mechanism is substantially **spurious lexical cueing on negation**, with no traced major causal path from *steepled*, *lacks a steeple*, *great height*, or their cross-sentence comparison into the strongest probe-driving features. The probe may correlate with contradictions in its training distribution because contradictions often contain explicit negation, but this graph does not show that it has grounded the contradiction in the prompt’s property-level semantics.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 29 | Lexical negation detectors ('not') |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 23 | Lexical negation detectors ('not') |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 29 | Negation/copula composition | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 29 | Late negation pattern detectors |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L16:F9779](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) | 23 | Late negation pattern detectors | negation words or contractions like "won't", "not", "never" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) |
| [L14:F10408](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) | 14 | Sea/location content feature |  geographical locations, especially related to bodies of water | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L16:12358 de=0.359 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@29` | ❌ error | — | — | Trace why this strongest positive driver of the synthetic contradiction-probe sc… |
| SA-2 | `L16:F9779@23` | ❌ error | — | — | Trace this positive late driver of the synthetic probe score. Identify whether i… |
| SA-3 | `L13:F3295@29` | ❌ error | — | — | Trace this positive final-token driver upstream, looking specifically for signal… |
| SA-4 | `L14:F10408@14` | ❌ error | — | — | Trace this mid/late positive feature upstream and determine its semantic role an… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L0:7710, L0:3820, L0:11375, L0:4958, L16:12358, L16:9779, L13:3295, L14:10408 |
| 2 | `get_upstream_features` | L16:F12358@29, k=12 → Emb:" not"@29 (de=19.50) +11 more |
| 3 | `get_upstream_features` | L16:F9779@23, k=12 → Emb:" will"@22 (de=7.31) +11 more |
| 4 | `get_upstream_features` | L13:F3295@29, k=12 → Emb:" not"@29 (de=17.75) +11 more |
| 5 | `get_upstream_features` | L14:F10408@14, k=12 → Emb:" sea"@14 (de=22.88) +11 more |
| 6 | `inspect_feature` ×2 | L0:2848, L0:5060 |

### Build

`build_circuit` → 10 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 23,858 | 2,366 | 44,902 | 0 | $0.1064 | — | — |
| **Total** | | **23,858** | **2,366** | **44,902** | **0** | **$0.1064** | | |

**Oracle wall-clock time:** 1m 28s