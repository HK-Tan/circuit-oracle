# Circuit Oracle Report
**Date:** 2026-07-28 07:24:47 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven primarily by genuine journalism/profession evidence at the explicit word “reporter,” but it also contains substantial direct sensitivity to masculine pronouns, so the user’s spurious-gender concern is supported.

**Confidence:** 8/10

**Reasoning:** The saved circuit has two distinct, partially independent routes into the **Output: probe classification score**.

1. **Genuine profession route — strong and semantically specific.**  
   The embedding for **“reporter” (pos 66)** directly excites the late profession features:
   - **Journalism/reporter concept** — L14:F4420 at pos 66, direct effect on the probe **−0.2051**. Its label is “words and phrases related to journalism and newspapers,” with low firing frequency **0.0165** and promoted tokens including *journalists, journalist, journalism, reporter,* and *editorial*. Its strongest upstream source is the exact **“reporter”** embedding (effect **+18.75**), with smaller support from **“freelancer” (pos 21, +2.31)** and education wording.
   - **News-source/reporting concept** — L19:F2486 at pos 66, direct effect **−0.1196**. It is similarly profession-specific (frequency **0.02926**) and promotes *reporting, reporter, coverage,* and *reporters*. It receives very strong direct input from **“reporter”** (**+28.25**) and from L14:F4420 (**+18.25**).

   Thus the circuit explicitly constructs a journalism/reporter representation from the occupation word itself:  
   **Emb: reporter → L14 journalism concept → L19 reporting concept → probe**, with direct reporter-to-L19 support as well. The negative signs merely mean that journalism evidence moves the probe toward whichever of its two class directions is encoded negatively; they do not make the signal non-professional.

2. **Spurious male-gender / pronoun route — also direct and nontrivial.**  
   The largest positive feature-level contributor overall is:
   - **L0:F2994**, “the pronoun ‘his’ and the pronoun ‘he’,” at pos 3: **+0.2324**, and again at pos 61: **+0.1270**. It has frequency **0.07326** and is unequivocally a masculine-pronoun detector. Its dominant upstream input is exactly **Emb: “his” (pos 3)**, with attribution **+42.25**.

   There are also later gender/reference features:
   - **L18:F14743** at pos 25 (**−0.1064**) and pos 86 (**−0.0928**), labeled **“He”**, frequency **0.01809**, and strongly driven by **Emb: “He” (pos 25, +24)**. Its promoted outputs include *himself* and its suppressed outputs include *she* and *her*, supporting a masculine-reference interpretation.
   - **L7:F14893** at pos 1 contributes **+0.1377**. Its label is broader (“pronouns or possessive pronouns,” frequency **0.00885**), but the direct source is **Emb: “He” (pos 1, +14.75)**. It should be treated as pronoun/coreference context rather than profession evidence.

   The corresponding path is:  
   **Emb: his / He → male-pronoun and masculine-reference features → probe**.

The concern is therefore **partly validated**. The probe is not solely exploiting gender: the explicit term **“reporter”** generates two selective, high-level journalism features with exact occupation-relevant semantics. However, the probe direction also gives large direct weight to lexical and contextual evidence of male gender. Most notably, the single L0 male-pronoun feature at “his” has the largest listed signed effect (**+0.2324**), comparable to or larger in magnitude than either individual journalism feature. This means a counterfactual edit replacing *He/his* with *She/her* could materially change the probe score even if the reporter evidence were held fixed—clear evidence that the learned classifier is not profession-pure.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Male-pronoun lexical detectors | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 61 | Male-pronoun lexical detectors | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Pronoun-context feature |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 25 | He / masculine-reference feature | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 86 | He / masculine-reference feature | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | Journalism/reporter concept | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | News-source/reporting concept |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.232 |
| 3 | `inspect_feature` ×5 | L0:2994, L14:4420, L19:2486, L18:14743, L7:14893 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@66` | ❌ error | — | — | Trace the major negative driver of the profession probe score at pos 66 to embed… |
| SA-2 | `L19:F2486@66` | ❌ error | — | — | Trace this major late negative feature to its input sources; assess profession v… |
| SA-3 | `L18:F14743@25` | ❌ error | — | — | Trace feature at graduate-degree context upstream to embeddings, identify semant… |
| SA-4 | `L7:F14893@1` | ❌ error | — | — | Trace this positive feature from early sentence context to embeddings; test if g… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@66, k=15 → Emb:" reporter"@66 (de=18.75) +14 more |
| 2 | `get_upstream_features` | L19:F2486@66, k=15 → Emb:" reporter"@66 (de=28.25) +14 more |
| 3 | `get_upstream_features` | L18:F14743@25, k=15 → Emb:" He"@25 (de=24.00) +14 more |
| 4 | `get_upstream_features` | L7:F14893@1, k=15 → Emb:"He"@1 (de=14.75) +14 more |
| 5 | `get_upstream_features` | L0:F2994@3, k=10 → Emb:" his"@3 (de=42.25) +9 more |

### Build

`build_circuit` → 11 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 12,208 | 2,258 | 42,867 | 0 | $0.0751 | — | — |
| **Total** | | **12,208** | **2,258** | **42,867** | **0** | **$0.0751** | | |

**Oracle wall-clock time:** 0m 34s