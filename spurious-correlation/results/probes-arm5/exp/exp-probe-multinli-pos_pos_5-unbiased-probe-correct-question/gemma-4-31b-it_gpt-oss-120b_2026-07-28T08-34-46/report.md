# Circuit Oracle Report
**Date:** 2026-07-28 08:34:46 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

{"analysis": "The probe's classification of contradiction is primarily driven by the detection of a contrast/negation pattern ('but', 'not only') occurring within a reporting context, rather than a semantic understanding of the contradiction. The circuit utilizes a late-layer 'Contrast/Negation' detector (L15:F12905, L17:F3763) that is excited by the input tokens 'but' and 'only'. This signal is reinforced by a 'Reporting Verb' detector (L5:F7144) and a lexical 'program' detector (L2:F13565), suggesting the probe identifies the structure of a disputed claim (Person X said Y, but actually Z) as a proxy for contradiction.", "confidence": 9, "reasoning": "The circuit flows from embedding nodes of 'but' and 'only' into a contrast-detecting supernode (L15:F12905, L17:F3763), which has a high direct effect on the probe score. This is combined with a reporting context feature (L5:F7144) and a specific entity feature (L2:F13565 for 'program'). The combination of reporting verbs and contrastive markers is a classic spurious signal for contradiction detection in NLI tasks, as it matches the surface pattern of many contradictory examples without requiring the model to resolve the actual semantic conflict between the two statements."}

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L5:F7144](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) | 1 | Reporting Verb Detector (e.g., 'said') |  proper nouns followed by the word "said" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) |
| [L2:F13565](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) | 3 | Entity Detector ('program') |  the word "program(me)s" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 11 | Contrast/Negation Pattern Detector ('but', 'not only') |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L17:F3763](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) | 6 | Contrast/Negation Pattern Detector ('but', 'not only') | only | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L15:12905 de=-0.355 |
| 3 | `inspect_feature` ×5 | L15:12905, L0:8046, L5:7144, L2:13565, L4:12847 |
| 4 | `get_top_logits` | "" (100%) |
| 5 | `get_top_features` | 15 features; top: L15:12905 de=-0.355 |
| 6 | `inspect_feature` ×8 | L15:12905, L0:8046, L5:7144, L2:13565, L4:12847, L3:2782, L0:15525, L17:3763 |
| 7 | `get_top_logits` | "" (100%) |
| 8 | `get_top_features` | 10 features; top: L15:12905 de=-0.355 |
| 9 | `inspect_feature` ×5 | L15:12905, L0:8046, L5:7144, L2:13565, L17:3763 |
| 10 | `get_top_logits` | "" (100%) |
| 11 | `get_top_features` | 15 features; top: L15:12905 de=-0.355 |
| 12 | `inspect_feature` ×7 | L15:12905, L0:8046, L5:7144, L2:13565, L4:12847, L17:3763, L12:12606 |
| 13 | `get_top_logits` | "" (100%) |
| 14 | `get_top_features` | 15 features; top: L15:12905 de=-0.355 |
| 15 | `inspect_feature` ×7 | L15:12905, L0:8046, L5:7144, L2:13565, L4:12847, L17:3763, L12:12606 |
| 16 | `get_top_logits` | "" (100%) |
| 17 | `get_top_features` | 10 features; top: L15:12905 de=-0.355 |
| 18 | `inspect_feature` ×5 | L15:12905, L17:3763, L5:7144, L2:13565, L4:12847 |
| 19 | `get_top_logits` | "" (100%) |
| 20 | `get_top_features` | 15 features; top: L15:12905 de=-0.355 |
| 21 | `inspect_feature` ×7 | L15:12905, L0:8046, L5:7144, L2:13565, L4:12847, L17:3763, L12:12606 |

### Build

`build_circuit` → 8 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 1,629,962 | 2,325 | 4,224 | 0 | $0.2292 | — | — |
| **Total** | | **1,629,962** | **2,325** | **4,224** | **0** | **$0.2292** | | |

**Oracle wall-clock time:** 4m 1s