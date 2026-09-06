# Circuit Oracle Report
**Date:** 2026-07-28 07:24:45 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession probe score is driven predominantly by the input’s male possessive **“His”** and a propagated male/pronoun representation, rather than by the text’s genuine journalism/reporting evidence.

**Confidence:** 9/10

**Reasoning:** The saved circuit is a pronoun-to-probe pathway centered on **Emb: His (pos 1)**, not on tokens such as *“report,” “news organizations,”* or *“Reagents Global Market.”*

- The raw embedding for **“His”** directly excites several downstream features: strongly **L7:14893** (+23.5 upstream attribution), **L19:8814** (+9.31), **L6:12990** (+4.91), and the L0 detector **L0:2994** (+19.75). This reaches the embedding floor, so the relevant source token is directly established.
- **L0:2994** is an explicit detector for **“his” / “he”** (`frac_nonzero=0.07326`). Despite being a basic lexical feature, it has a sizeable **positive direct effect on the probe of +0.2852**. Thus the probe direction itself aligns positively with a male-pronoun component.
- **L4:4315** is another possessive-pronoun representation—*his/he/him/hers*—with `frac_nonzero=0.02624`. It receives positive input from the “His” embedding and feeds the later pronoun pathway, including L6, L7, and L19.
- **L6:12990**, labeled **male pronouns and titles / male-associated descriptors** (`frac_nonzero=0.06766`), is driven by “His” and L4:4315. Its effect on the probe is **negative (-0.2969)**, so the model has an internal countervailing male cue as well. This does not rescue the probe: it shows the score contains multiple gender-coded directions with different signs.
- The dominant positive scoring feature, **L7:14893**, is a sparse pronoun/possessive feature (`frac_nonzero=0.00885`) and has the **largest positive direct effect, +0.4707**. Its top examples include *“his”*, while its promoted tokens are feminine pronouns such as *she*, *herself*, and *elle* and its suppressed tokens include *his/himself*. Mechanistically, it appears to encode a pronoun/gender contrast rather than an occupation. It is directly supplied by the “His” embedding and by L6:12990/L4:4315.
- **L19:8814** (`frac_nonzero=0.08655`) is a broad person/pronoun feature whose examples repeatedly activate on *he/his* and person references. It contributes **+0.2324** to the probe and receives positive support from “His,” L4:4315, and L6:12990. Although later in the network, its semantic content remains person/gender reference—not reporting or journalism.
- There is also a large negative competing feature, **L7:14946** (**-0.4668**), explicitly associated with *his/he/him* (`frac_nonzero=0.01669`), and other negative pronoun-related features. This indicates that the probe does not simply read “male = positive”; rather, its score is a signed mixture of gender/pronoun directions. But critically, the **largest positive evidence and the traced causal source are still pronoun/gender features**, while no top probe-driving feature inspected here encodes journalism, reporting, media organizations, travel, or the named employer.

Therefore the user concern is supported: this graph provides strong evidence that the linear profession probe is substantially using **spurious gender-marker information**, specifically the opening word **“His,”** instead of grounding its classification primarily in the explicit profession-relevant phrase *“opportunity to report for ... top news organizations.”*

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | L0 male-pronoun detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | L4 possessive-pronoun representation |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6 male-pronoun/title representation |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7 pronoun/gender coding |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | L19 person/pronoun representation |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 10 features; top: L7:14893 de=0.471 |
| 3 | `inspect_feature` ×5 | L7:14893, L0:2994, L19:8814, L7:14946, L6:12990 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace this strongest positive probe-driving feature upstream to embedding nodes.… |
| SA-2 | `L19:F8814@1` | ❌ error | — | — | Trace this positive late feature upstream to embeddings. Determine whether its p… |
| SA-3 | `L7:F14946@1` | ❌ error | — | — | Trace this strongest negative/countervailing feature upstream to embeddings. Ide… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@1, k=15 → Emb:"His"@1 (de=23.50) +14 more |
| 2 | `get_upstream_features` | L19:F8814@1, k=15 → Emb:"His"@1 (de=9.31) +14 more |
| 3 | `get_upstream_features` | L7:F14946@1, k=15 → Emb:"His"@1 (de=18.38) +14 more |
| 4 | `get_upstream_features` | L0:F2994@1, k=15 → Emb:"His"@1 (de=19.75) +14 more |
| 5 | `get_upstream_features` | L6:F12990@1, k=15 → Emb:"His"@1 (de=4.91) +14 more |
| 6 | `inspect_feature` | L4, F4315 → " mentions of "his" and other associated pronouns like he, him, or hers" |

### Build

`build_circuit` → 7 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 17,283 | 2,459 | 54,998 | 0 | $0.0938 | — | — |
| **Total** | | **17,283** | **2,459** | **54,998** | **0** | **$0.0938** | | |

**Oracle wall-clock time:** 0m 37s