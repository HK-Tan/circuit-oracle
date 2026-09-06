# Circuit Oracle Report
**Date:** 2026-07-28 07:24:51 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven primarily by an explicit **“reporter” → journalism/news-reporting** circuit, rather than by the input’s male pronouns or other gender markers.

**Confidence:** 9/10

**Reasoning:** The saved circuit shows a direct lexical-semantic path from **Emb: “reporter” (pos 66)** through progressively more abstract journalism features into the **probe classification score**.

- The strongest causal features all occur at the final token, *“reporter”*, and have **negative direct effects** on the injected probe direction: L14:4420 (−0.1963), L19:2486 (−0.1260), L4:13253 (−0.1162), and L8:8855 (−0.0815). The sign identifies which pole of the binary/probe direction they support; regardless of that label orientation, these are the dominant profession-semantic drivers.

- **Early journalism/media concept** is L4:13253. It has a rare firing rate (**frac_nonzero = 0.00648**) and is labeled *“things related to journalism and the media”*. Its promoted tokens include **“Journalism,” “journalists,” “journalism,” “media,” “reporters.”** Its upstream attribution is dominated by the literal reporter embedding: **Emb “reporter” → L4:13253 = +26.625**. This is strong evidence for direct profession-word recognition.

- The representation is elaborated in the **Reporter/news-reporting representations** supernode:
  - L7:13646, *“news reporting and journalism”* (**frac_nonzero = 0.00757**), promotes **“journalist,” “reporter,” “correspondent.”**
  - L8:8855, *“mentions of news reporters and news reporting”* (**frac_nonzero = 0.00847**), promotes **“reporter,” “reporters,” “journalist,” “reporting,” “journalism.”**
  
  Both receive substantial positive input from **Emb “reporter”** (respectively +15.125 and +16.875), with L8:8855 also receiving +4.219 from L7:13646 and +2.406 from L4:13253. This establishes a coherent concept-building pathway rather than an unrelated surface correlation.

- The late **Journalism/newspaper and source representation** supernode consolidates this evidence:
  - L14:4420 is *“words and phrases related to journalism and newspapers”* (**frac_nonzero = 0.0165**) and promotes **“journalists,” “journalistic,” “journalist,” “journalism,” “reporter,” “editorial.”**
  - L19:2486 is *“journalistic sources and news outlets”* (**frac_nonzero = 0.02926**) and promotes **“reporting,” “reporter,” “coverage,” “reporters.”**
  
  The causal links are sizable: L4:13253 → L14:4420 is +6.75; L8:8855 → L14:4420 is +5.625; L14:4420 → L19:2486 is +18.25. Directly, **Emb “reporter” → L14:4420 is +18.75** and **Emb “reporter” → L19:2486 is +28.25**. These late features then feed the probe output.

- **“freelancer” (pos 21)** contributes modestly as supporting occupational-context evidence: it feeds L19:2486 by +3.578, L14:4420 by +2.313, L8:8855 by +1.586, and L7:13646 by +0.664. This is plausibly profession-adjacent but is far smaller than the direct “reporter” signal.

Regarding the stated concern, there **is** a male-reference feature among the top direct probe contributors: L0:1069 at position 1, labeled *“references to a male person, particularly … ‘He’ or ‘His’”*, with direct effect −0.0889. Thus gender information is present in the probe’s linear readout. However, it is not part of the traced dominant positive upstream circuit at the *reporter* position, whereas the main pathway is a densely corroborated cascade of highly selective journalism features grounded directly in the word **“reporter.”** The other high-ranked layer-0 features inspected are largely generic lexical/syntactic detectors (“from,” “in,” “has,” punctuation), not gender or profession concepts.

Therefore, on this example the classification is best characterized as **genuine profession-indicator driven, with a detectable but secondary gender-associated feature in the direct probe readout**.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | Early journalism/media concept |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 66 | Reporter/news-reporting representations |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 66 | Reporter/news-reporting representations |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | Journalism/newspaper and source representation | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | Journalism/newspaper and source representation |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L14:4420 de=-0.196 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F2486@66` | ❌ error | — | — | Trace this strong late negative driver of the probe score upstream to embeddings… |
| SA-2 | `L14:F4420@66` | ❌ error | — | — | Trace this strongest negative probe driver upstream to embeddings; identify sema… |
| SA-3 | `L4:F13253@66` | ❌ error | — | — | Trace this early-to-mid negative driver upstream through the graph to token embe… |
| SA-4 | `L8:F8855@66` | ❌ error | — | — | Trace this negative probe-driving path to embeddings and assess whether it repre… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L19:2486, L14:4420, L4:13253, L0:4874, L0:6051, L0:8642 |
| 2 | `get_upstream_features` | L19:F2486@66, k=12 → Emb:" reporter"@66 (de=28.25) +11 more |
| 3 | `get_upstream_features` | L14:F4420@66, k=12 → Emb:" reporter"@66 (de=18.75) +11 more |
| 4 | `get_upstream_features` | L4:F13253@66, k=12 → Emb:" reporter"@66 (de=26.62) +11 more |
| 5 | `inspect_feature` ×6 | L8:8855, L7:13646, L0:1069, L0:8974, L0:8061, L0:14824 |
| 6 | `get_upstream_features` | L8:F8855@66, k=12 → Emb:" reporter"@66 (de=16.88) +11 more |
| 7 | `get_upstream_features` | L7:F13646@66, k=12 → Emb:" reporter"@66 (de=15.12) +11 more |

### Build

`build_circuit` → 6 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 27,175 | 2,672 | 55,550 | 0 | $0.1219 | — | — |
| **Total** | | **27,175** | **2,672** | **55,550** | **0** | **$0.1219** | | |

**Oracle wall-clock time:** 0m 38s