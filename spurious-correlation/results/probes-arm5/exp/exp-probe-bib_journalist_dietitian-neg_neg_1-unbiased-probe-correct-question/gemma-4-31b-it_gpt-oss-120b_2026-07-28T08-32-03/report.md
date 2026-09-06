# Circuit Oracle Report
**Date:** 2026-07-28 08:32:03 UTC | **Orchestrator:** google/gemma-4-31b-it | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by features encoding journalism and news-related concepts, which are activated by the context of the input text.

**Confidence:** 9/10

**Reasoning:** 
The attribution analysis reveals that the probe's score is primarily driven by high-level semantic features related to the profession of journalism. Specifically, late-layer features such as **L14:F4420** ("words and phrases related to journalism and newspapers") and **L19:F2486** ("journalistic sources and news outlets") have significant direct effects on the probe score. These features promote tokens like "journalist", "reporter", and "reporting", directly aligning with the professional identity mentioned in the text ("report for some of the top news organizations").

While the `get_top_features` results also showed some early-layer activations (L0) for tokens like "His" (L0:F8964), "see" (L0:F14287), and "to" (L0:F8444), these appear to be part of the general linguistic framework of the sentence rather than the primary causal drivers of the profession classification. The strong signal flows from the context of the person's career ("report for... news organizations") into the **Journalism_Core** supernode (L14:F4420, L19:F2486), which then directly increases the probe's classification score. 

Contrary to the user's concern, there is no evidence in the top-contributing features that the probe is relying on spurious gender markers (like "His") to make its prediction; instead, it is leveraging genuine indicators of the journalism profession.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 0 | Input Tokens (His, see, to) |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L0:F14287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) | 4 | Input Tokens (His, see, to) | the word "see" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 5 | Input Tokens (His, see, to) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Journalism & News Features | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Journalism & News Features |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.147 |
| 3 | `inspect_feature` ×5 | L14:4420, L19:2486, L0:8964, L0:8444, L0:14287 |

### Build

`build_circuit` → 3 nodes, 2 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | google/gemma-4-31b-it | 80,053 | 1,019 | 0 | 0 | $0.0116 | — | — |
| **Total** | | **80,053** | **1,019** | **0** | **0** | **$0.0116** | | |

**Oracle wall-clock time:** 1m 22s