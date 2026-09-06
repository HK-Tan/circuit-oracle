# Circuit Oracle Report
**Date:** 2026-07-28 08:32:47 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is primarily driven by a "negation word" detector that triggers on the token "No" (within "No one"), rather than any semantic understanding of the contradiction between the two sentences.

**Confidence:** 9

**Reasoning:** 
The attribution analysis reveals that the probe's high classification score is caused by a set of features that act as simple lexical detectors. Specifically, late-layer features like **L16:F11298** (and L15:F13061) have a strong positive direct effect on the probe's score. Inspection of **L16:F11298** shows it is a highly specific feature for the token "no" (frac_nonzero = 0.01043), firing strongly on "No one" in the second sentence. 

The circuit flows from the embedding of the token "No" (pos 21) through these negation-detecting features directly into the probe score. While there is some minor influence from the word "Conspiracy" at the start of the prompt (L0:F44), the dominant positive drivers are tied to the presence of negation markers. This confirms the user's concern: the probe is utilizing a spurious "negation words" signal to predict contradiction, rather than analyzing the semantic conflict between the claim that MasterCard is investing in a chip and the claim that no one thinks they are up to anything nefarious.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F44](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) | 1 | Emb: Conspiracy (pos 1) | words starting with "cons" that might indicate a constitution or consolidated standard, alongside "pride" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 21 | Emb: No one (pos 21) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 21 | Negation/No-one Detector |  uses of the word "no" or similar negative statements and words associated with "one" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 21 | Negation/No-one Detector | no | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:44 de=-0.527 |
| 3 | `inspect_feature` ×6 | L4:15764, L16:11298, L15:13061, L0:11375, L0:44, L0:14574 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L0:44 de=-0.527 |
| 6 | `inspect_feature` ×5 | L4:15764, L16:11298, L15:13061, L0:44, L0:11375 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 10 features; top: L0:44 de=-0.527 |
| 9 | `inspect_feature` | "no" |

### Build

`build_circuit` → 4 nodes, 2 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 333,539 | 1,282 | 0 | 0 | $0.0472 | — | — |
| **Total** | | **333,539** | **1,282** | **0** | **0** | **$0.0472** | | |

**Oracle wall-clock time:** 2m 5s