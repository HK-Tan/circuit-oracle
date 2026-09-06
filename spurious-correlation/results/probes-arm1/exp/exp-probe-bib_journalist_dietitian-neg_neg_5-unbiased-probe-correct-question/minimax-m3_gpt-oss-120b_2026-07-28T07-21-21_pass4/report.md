# Circuit Oracle Report
**Date:** 2026-07-28 07:21:21 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies the profession as "reporter/journalist" through a textbook clean circuit: a journalism concept feature at L19:F2486 (frac_nonzero=0.029, promoted tokens: reporting, reporter, coverage, reporters, Reporter) directly drives the output, fed from an earlier "journalism/newspapers" feature at L14:F4420 (frac_nonzero=0.017, promoted: journalists, journalistic, journalist, journalism, Journalist, reporter) and ultimately grounded in the input token " reporter" at position 66 (direct_effect=28.25 into L19, 18.75 into L14, 26.625 into L4:F13253).

**Confidence:** 8

**Reasoning:** The signal flow traces a profession-relevant (not gender) pathway from input to probe. All the top features driving the classification (L19:F2486, L14:F4420, L4:F13253, L8:F8855, L6:F12712, L7:F13646, L7:F9092) have autointerp labels explicitly about journalism/reporter/media — none encode gender. Their `promoted_tokens` project to journalist/reporter/journalism vocabulary, and the top-activating examples are newsroom text. The strongest upstream causal anchor is the literal " reporter" token embedding (pos 66), with a secondary semantic contribution from " freelancer" (pos 21, direct_effect 2.3-3.6 into mid-layer journalism features) and "." (pos 24, direct_effect 47.25 into L0:F6051, a period/space feature used as a generic structural context). The mid-layer supernode (L7-L9) contains 6 distinct journalism-concept features, all converging into the late-layer L14:L19 journalism concept, which finally feeds the probe. 

Regarding the user concern: the "He" pronoun at position 1 is NOT a primary driver — the L0:F1069 feature (label: "references to a male person, particularly when using the pronoun 'He'") has direct_effect=0.0000 at pos 1 (its contribution to the probe is zero, as confirmed by the upstream trace of F4874 which listed F1069 with direct_effect=0). The pronoun only enters the circuit weakly through a generic writing/editing baseline feature at L1 (F1024, direct_effect 1.3) and never reaches the late-layer output-driving features. The profession is identified via the actual occupation term "reporter" and supporting journalism vocabulary, not via gender markers. The circuit is therefore **not** relying on spurious gender features — it uses genuine profession indicators (the word "reporter" itself plus multi-layer journalism-concept abstractions).

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | Journalism/Media Concept (L14-L19) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | Journalism/Media Concept (L14-L19) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L17:F5218](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) | 66 | Journalism/Media Concept (L14-L19) |  text about journalism, media, and related topics | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) |
| [L9:F7435](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) | 66 | Journalism Concept (L7-L9) |  words and phrases related to news production and media | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 66 | Journalism Concept (L7-L9) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F15435](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15435) | 66 | Journalism Concept (L7-L9) |  words relating to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15435) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 66 | Journalism Concept (L7-L9) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 66 | Journalism Concept (L7-L9) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F72](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/72) | 66 | Journalism Concept (L7-L9) |  words related to writing professionally | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/72) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 66 | Journalism Concept (L4-L6) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | Journalism Concept (L4-L6) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F661](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) | 66 | Journalism Concept (L4-L6) |  words and phrases used when referring to reports, documentaries, and television coverage of news | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) |
| [L1:F1024](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1024) | 66 | Writing/Editing Baseline (L1-L2) |  words and phrases frequently used when discussing writing, publishing, and editing books and other written works. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1024) |
| [L1:F5357](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5357) | 66 | Writing/Editing Baseline (L1-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5357) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.196 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@66` | ❌ error | — | — | Trace the path from L14:F4420 at position 66. This is the strongest feature driv… |
| SA-2 | `L19:F2486@66` | ❌ error | — | — | Trace the path from L19:F2486 at position 66. This is the second strongest featu… |
| SA-3 | `L4:F13253@66` | ❌ error | — | — | Trace the path from L4:F13253 at position 66. This is the third strongest featur… |
| SA-4 | `L0:F4874@2` | ❌ error | — | — | Trace the path from L0:F4874 at position 2. This is the fourth strongest feature… |
| SA-5 | `L0:F6051@24` | ❌ error | — | — | Trace the path from L0:F6051 at position 24. This is the fifth strongest feature… |
| SA-6 | `L0:F1069@1` | ❌ error | — | — | Trace the path from L0:F1069 at position 1. This is a key feature driving the pr… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×14 | L14:4420, L19:2486, L4:13253, L0:4874, L0:6051, L0:1069, L0:8642, L0:8974, L0:14824, L0:8061, L0:13864, L0:9397, L8:8855, L6:12712 |
| 2 | `get_upstream_features` | L14:F4420@66, k=10 → Emb:" reporter"@66 (de=18.75) +9 more |
| 3 | `get_upstream_features` | L19:F2486@66, k=10 → Emb:" reporter"@66 (de=28.25) +9 more |
| 4 | `get_upstream_features` | L4:F13253@66, k=10 → Emb:" reporter"@66 (de=26.62) +9 more |
| 5 | `get_upstream_features` | L8:F8855@66, k=10 → Emb:" reporter"@66 (de=16.88) +9 more |
| 6 | `get_upstream_features` | L6:F12712@66, k=10 → Emb:" reporter"@66 (de=11.56) +9 more |
| 7 | `get_upstream_features` | L7:F13646@66, k=10 → Emb:" reporter"@66 (de=15.12) +9 more |
| 8 | `get_upstream_features` | L7:F9092@66, k=10 → L4:F13253 (de=6.81) +9 more |
| 9 | `get_upstream_features` | L0:F4874@2, k=10 → Emb:" obtained"@2 (de=11.69) +9 more |
| 10 | `get_upstream_features` | L0:F6051@24, k=10 → Emb:"."@24 (de=47.25) +9 more |
| 11 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"He"@1 (de=22.62) +9 more |
| 12 | `get_upstream_features` | L17:F5218@66, k=10 → L14:F4420 (de=6.47) +9 more |
| 13 | `get_upstream_features` | L9:F7435@66, k=10 → Emb:" reporter"@66 (de=5.47) +9 more |
| 14 | `inspect_feature` ×10 | L17:5218, L9:7435, L7:13646, L7:9092, L7:9521, L4:661, L1:1024, L8:15435, L15:12472, L7:72 |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,779 | 4,272 | 192,561 | 0 | $0.0310 | — | — |
| **Total** | | **47,779** | **4,272** | **192,561** | **0** | **$0.0310** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 18s