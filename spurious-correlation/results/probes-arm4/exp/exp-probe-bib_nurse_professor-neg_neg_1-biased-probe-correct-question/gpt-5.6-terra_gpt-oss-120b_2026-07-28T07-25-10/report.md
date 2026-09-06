# Circuit Oracle Report
**Date:** 2026-07-28 07:25:10 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven predominantly by a male-reference/pronoun circuit centered on *“His”* and *“He,”* with only weak direct evidence of genuine research/professional content.

**Confidence:** 9/10

**Reasoning:** The saved circuit indicates a substantial spurious gender pathway into the profession-classification direction.

- The most important positive direct driver is **L7:14893 at pos 1** (+0.4297). It is a selective pronoun feature (frac_nonzero **0.00885**) labeled “pronouns or possessive pronouns”; its strongest English examples activate on *his*, and its promoted tokens include *she/herself* while suppressing *his/himself*. Its strongest upstream source is directly **Emb: His (pos 1)** (+23.5), not a profession term.
- The near-equal countervailing feature, **L7:14946 at pos 1** (−0.4258; frac_nonzero **0.01669**), is explicitly a *his/he/him* detector. It too receives its dominant positive input from **Emb: His (pos 1)** (+18.375). Thus the probe contains a strong learned **gender/pronoun contrast**, rather than merely a generic biography feature.
- Earlier components reinforce that interpretation: **L0:2994**, **L4:4315**, and **L6:12990** are all male-pronoun detectors. In particular, L6:12990 is labeled male pronouns/titles/descriptors, has frac_nonzero **0.06766**, promotes *himself*, and suppresses feminine forms. These form the circuit’s **Early male-pronoun detectors** supernode feeding the L7 contrast.
- A second major negative contribution is **L18:14743** at both pos 14 (−0.2520) and pos 37 (−0.2051). This is a highly selective *He* feature (frac_nonzero **0.01809**), and at pos 14 its overwhelmingly largest upstream input is **Emb: He (pos 14)** (+22.375). Its activity is therefore again explained by masculine coreference, not “visualization,” “graphics,” or another occupation-specific concept.
- The late **person/pronoun representation** also enters the score: **L19:8814 at pos 1** contributes positively (+0.2402), is a broad person/pronoun feature (frac_nonzero **0.08655**), and receives input from *His*, L7:14946, and **L18:10315**, another possessive-pronoun detector (frac_nonzero **0.03892**). This preserves the gender/reference signal into late layers before it projects to the probe.
- There is some authentic topical signal available: **L0:4564 at pos 2** is a sparse lexical detector for *“research”* (frac_nonzero **0.00694**), sourced by the input’s “research.” But its direct effect on the probe is only **+0.1572**, far smaller than the combined magnitude of the pronoun-related features. The inspected late “software/coding” feature **L18:7400** also appeared in the pathway, but its direct probe effect is negative (−0.1592) and it is not an unambiguous profession detector in this particular input.

In short, the circuit supports the user’s concern. The classification direction is not cleanly reading the explicit profession evidence—*research interests, scientific visualization, computer graphics, computer science degrees, technical staff, Advanced Computing Laboratory*. Instead, its largest causal components are highly specific features tracking **male pronouns and male person-reference structure**. The net score reflects a mixture of genuine research/technical-biography evidence and a much more prominent gender-correlated shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Early male-pronoun detectors | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Early male-pronoun detectors |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Early male-pronoun detectors |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7 pronoun / gender contrast |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7 pronoun / gender contrast |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Research lexical detector | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 14 | Late He / male-reference detector | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 37 | Late He / male-reference detector | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Late person/pronoun representation |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Late person/pronoun representation |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L7:14893 de=0.430 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace this strongest positive probe-driving feature upstream to embeddings. Dete… |
| SA-2 | `L7:F14946@1` | ❌ error | — | — | Trace this strongest negative probe-driving feature upstream to embeddings. Iden… |
| SA-3 | `L18:F14743@14` | ❌ error | — | — | Trace this high-activation negative feature at pos14 upstream to embeddings. Det… |
| SA-4 | `L19:F8814@1` | ❌ error | — | — | Trace the positive late feature upstream to embeddings and assess whether it car… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L7:14893, L7:14946, L18:14743, L19:8814, L0:2994 |
| 2 | `get_upstream_features` | L7:F14893@1, k=12 → Emb:"His"@1 (de=23.50) +11 more |
| 3 | `get_upstream_features` | L7:F14946@1, k=12 → Emb:"His"@1 (de=18.38) +11 more |
| 4 | `get_upstream_features` | L18:F14743@14, k=12 → Emb:" He"@14 (de=22.38) +11 more |
| 5 | `get_upstream_features` | L19:F8814@1, k=12 → Emb:"His"@1 (de=9.31) +11 more |
| 6 | `inspect_feature` ×5 | L4:4315, L6:12990, L18:7400, L18:10315, L0:4564 |

### Build

`build_circuit` → 9 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 24,987 | 3,533 | 73,620 | 0 | $0.1339 | — | — |
| **Total** | | **24,987** | **3,533** | **73,620** | **0** | **$0.1339** | | |

**Oracle wall-clock time:** 0m 54s