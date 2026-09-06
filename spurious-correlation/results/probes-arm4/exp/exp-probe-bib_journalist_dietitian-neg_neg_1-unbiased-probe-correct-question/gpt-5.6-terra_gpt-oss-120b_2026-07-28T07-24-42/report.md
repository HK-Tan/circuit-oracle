# Circuit Oracle Report
**Date:** 2026-07-28 07:24:42 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The synthetic profession-probe score is driven chiefly by a genuine journalism/reporter circuit anchored on “report,” with a smaller but direct positive contribution from the male pronoun “His.”

**Confidence:** 8/10

**Reasoning:** The dominant semantic path is:

`Emb: report (pos 21)` → **Reporter/news-reporting detector** (L8:8855) → **Journalism/newspaper concept** (L14:4420) → **Journalistic-source/news-outlet concept** (L19:2486) → **synthetic profession-probe score**.

This is strong evidence for a real profession-related mechanism rather than a purely demographic shortcut:

- L8:8855 is a selective reporter/news-reporting feature (frac_nonzero **0.00847**), with promoted tokens including *reporter, journalist, reporting,* and *journalism*. It receives its largest upstream signal directly from the embedding of **“report”** at position 21 (direct effect **+12.06**).
- L14:4420 is a journalism/newspaper feature (frac_nonzero **0.0165**), promoting *journalist, journalism, reporter,* and *editorial*. It is positively supplied by both the “report” embedding (**+5.22**) and L8:8855 (**+5.03**).
- L19:2486 represents journalistic sources/news outlets (frac_nonzero **0.02926**) and promotes *reporting, reporter, coverage,* and *reporters*. It is strongly downstream of L14:4420 (**+14.31**) and additionally receives L8:8855 (**+4.03**) and “report” embedding (**+3.36**) signals.

Importantly, L14:4420 and L19:2486 have **negative direct effects on the probe score** (respectively **−0.1475** and **−0.0972** at position 21). Thus, they are not merely activating: their journalism semantics are being read by the probe as evidence *against the probe’s positive direction* (or equivalently for the probe’s negative profession class). The exact class polarity is not recoverable from the synthetic blank label, but the causal content is clear: the score tracks the reporting/journalism profession cue.

There is also a confirmed spurious gender path:

`Emb: His (pos 1)` → **Male possessive marker** (L0:8964) → **synthetic profession-probe score**.

L0:8964 is highly specific to the token **“His”** (frac_nonzero **0.01755**) and receives a large direct embedding contribution from that exact token (**+13.69**). It has a positive direct effect on the probe score (**+0.0879**), so the probe is indeed using masculine marking as independent evidence. This substantiates the user’s concern, but it is not the only—or apparently principal semantic—mechanism in this example.

In short: the classifier mixes a valid profession signal centered on “report” and a journalism representation with a direct gender-correlated feature. The latter is a bias vulnerability, while the main multi-layer semantic circuit is a genuine reporter/journalist detector.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | Male possessive marker: L0 F8964 |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Reporter/news-reporting detector: L8 F8855 |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Journalism/newspaper concept: L14 F4420 | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Journalistic-source/news-outlet concept: L19 F2486 |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.147 |
| 3 | `inspect_feature` ×7 | L14:4420, L19:2486, L0:8964, L0:8444, L0:14287, L1:14511, L8:8855 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ❌ error | — | — | Trace this negative late/mid-layer contribution to the synthetic profession-prob… |
| SA-2 | `L19:F2486@21` | ❌ error | — | — | Trace this repeated negative high-layer feature upstream to embeddings. Determin… |
| SA-3 | `L8:F8855@21` | ❌ error | — | — | Trace the position-21 negative feature upstream to embeddings, looking for sourc… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@21, k=15 → Emb:" report"@21 (de=5.22) +14 more |
| 2 | `get_upstream_features` | L19:F2486@21, k=15 → L14:F4420 (de=14.31) +14 more |
| 3 | `get_upstream_features` | L8:F8855@21, k=15 → Emb:" report"@21 (de=12.06) +14 more |
| 4 | `get_upstream_features` | L1:F14511@21, k=15 → Emb:" report"@21 (de=20.62) +14 more |
| 5 | `get_upstream_features` | L0:F8964@1, k=15 → Emb:"His"@1 (de=13.69) +14 more |

### Build

`build_circuit` → 7 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 15,013 | 2,052 | 48,879 | 0 | $0.0805 | — | — |
| **Total** | | **15,013** | **2,052** | **48,879** | **0** | **$0.0805** | | |

**Oracle wall-clock time:** 0m 32s