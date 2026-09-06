# Circuit Oracle Report
**Date:** 2026-07-28 07:24:52 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven chiefly by genuine journalism-related lexical/concept features triggered by “journalistic,” with smaller direct contributions from generic narrative language and a male-pronoun feature.

**Confidence:** 8/10

**Reasoning:** The saved circuit shows a clear profession-relevant route:

- **Emb: journalistic (pos 13)** strongly excites the **Journalism/media concept detector** (L4:F13253, pos 13; upstream direct effect **+25.625**) and even more directly the **Journalism profession detector** (L14:F4420, pos 13; **+24.375**).
  - L4:F13253 is selective (`frac_nonzero=0.00648`) and its promoted tokens include *“Journalism,” “journalists,” “journalism,” “media,”* and *“reporters.”*
  - L14:F4420 is also selective (`frac_nonzero=0.0165`) and has a highly specific journalism label, with top activations on *reporter*, *newspaper*, and *reporting*. Its promoted tokens are *“journalists,” “journalistic,” “journalist,” “journalism,” “reporter,”* and *“editorial.”*
  - This L4 → L14 pathway therefore represents a real semantic profession signal, rather than an accidental stylistic association.

Importantly, L14:F4420 is a **negative** direct driver of the particular synthetic probe direction (**−0.1279**): it pushes the score toward the probe’s negative side. That sign does not make it spurious—it means that, for this probe’s chosen orientation/class convention, journalism evidence lowers the reported score. The circuit establishes that the model is nevertheless reading the appropriate profession-bearing content.

There are two lesser, less profession-specific routes:

- **Emb: stories (pos 3)** strongly drives L1:F14812 (**+18.625**). This feature detects stories/narrative material (`frac_nonzero=0.00947`), and contributes positively to the probe (**+0.1895**). It is generic contextual evidence: “He researches stories” plausibly correlates with journalistic/writing work, but it is not a reliable profession indicator on its own.
- **Emb: He (pos 1)** triggers L0:F1069, a male-pronoun detector (`frac_nonzero=0.0078`; top examples are overwhelmingly “He” and “His”). This feature directly contributes **−0.1621** to the probe. Thus, the user’s concern is partly valid: the probe direction does include a meaningful gender-correlated component. However, the traced circuit does **not** show gender feeding the journalism detector; it is a separate, direct shortcut into the linear probe score.

Other large early direct effects are largely lexical/nonspecific—for example L0:F11603 (“too,” **−0.1631**) and L0:F14906 (“binding,” **−0.2217**)—rather than coherent professional reasoning. They reinforce that a linear residual-stream probe can use incidental token-level correlates.

Overall, this is **not primarily a gender-marker classifier**. The strongest interpretable semantic mechanism is the direct and hierarchical journalism pathway, **journalistic → media/journalism features → probe**. But the probe is not cleanly profession-only: direct male-pronoun and incidental lexical features have comparable individual signed effects, so gender-swapped and profession-word-ablated counterfactual tests would be necessary before treating its classification as robustly profession-based.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | Narrative/story lexical detector |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | Journalism/media concept detector |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | Journalism profession detector | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male-pronoun/gender detector |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:14906 de=-0.222 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@13` | ❌ error | — | — | Trace this strong late negative driver of the probe score to embeddings; determi… |
| SA-2 | `L4:F13253@13` | ❌ error | — | — | Trace this negative mid-layer probe driver upstream to identify input-token orig… |
| SA-3 | `L1:F14812@3` | ❌ error | — | — | Trace this positive early driver to embeddings; assess whether it is driven by t… |
| SA-4 | `L1:F16233@3` | ❌ error | — | — | Trace this positive early driver to embeddings; assess semantic mechanism and sp… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L14:4420, L4:13253, L1:14812, L1:16233, L0:14906, L0:11261, L0:11603, L0:1069 |
| 2 | `get_upstream_features` | L14:F4420@13, k=20 → Emb:" journalistic"@13 (de=24.38) +19 more |
| 3 | `get_upstream_features` | L4:F13253@13, k=20 → Emb:" journalistic"@13 (de=25.62) +19 more |
| 4 | `get_upstream_features` | L1:F14812@3, k=20 → Emb:" stories"@3 (de=18.62) +19 more |
| 5 | `get_upstream_features` | L1:F16233@3, k=20 → Emb:" stories"@3 (de=13.62) +19 more |
| 6 | `get_upstream_features` | L0:F1069@1, k=20 → Emb:"He"@1 (de=22.62) +19 more |

### Build

`build_circuit` → 8 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 21,213 | 2,382 | 54,522 | 0 | $0.1024 | — | — |
| **Total** | | **21,213** | **2,382** | **54,522** | **0** | **$0.1024** | | |

**Oracle wall-clock time:** 0m 37s