# Circuit Oracle Report
**Date:** 2026-07-28 07:25:12 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s contradiction score is driven primarily by shallow, token-local lexical features for **“recorded,” “menu,” and “will,”** rather than a composed representation of the two sentences’ semantic incompatibility; notably, it is not chiefly driven by a generic negation-word detector.

**Confidence:** 8/10

**Reasoning:** The saved circuit shows three direct embedding-to-lexical-feature routes into the synthetic contradiction-probe score:

- **Emb: ` recorded` (pos 2) → Recorded/record lexical detectors → probe.**  
  This is the strongest positive branch. The high-impact positive feature **L2:F8776 at pos 2** contributes **+0.5234** to the probe direction. Although its autointerp label is “finance and property law” (firing rate **0.01099**), its upstream attribution is overwhelmingly the literal token embedding ` recorded` (**+19.5**), so that label is not a credible explanation of this input’s classification. The same branch includes:
  - **L0:F7443**, a generic *record* detector (**frac_nonzero 0.01531**), directly fed by ` recorded` (**+22.625**);
  - **L1:F3691**, a *recording* detector (**frac_nonzero 0.00733**), fed by ` recorded` (**+24.75**);
  - **L2:F3059**, a verb-*record* detector (**frac_nonzero 0.00430**).  
  These are word/form detectors, not features representing that a recorded menu *will provide* information or that a later statement denies this.

- **Emb: ` menu` (pos 3) → Menu lexical detectors → probe.**  
  The strongest negative contributors are explicitly menu features:
  - **L0:F2108** (“the word ‘menu’,” **frac_nonzero 0.00353**) contributes **−0.4805**;
  - **L1:F12253** (“the word ‘menu’,” **frac_nonzero 0.00409**) contributes **−0.4277**;
  - **L2:F3648**, menu/restaurant/code contexts (**frac_nonzero 0.00151**), contributes **−0.2129**;
  - **L3:F3573**, menu/interface contexts (**frac_nonzero 0.00205**), contributes **−0.2891**.  
  The input is unambiguously lexical: ` menu` directly excites L0:F2108 by **+25.75**, and directly excites L1:F12253 by **+20.625**; L0:F2108 itself supplies **+2.1562** upstream influence to L1:F12253. These features suppress the particular probe direction here, but their role is still a learned association with the word **menu**, not semantic contradiction resolution.

- **Emb: ` will` (pos 4) → Will/future-form lexical detector → probe.**  
  **L0:F8046** is a literal *will* detector (**frac_nonzero 0.02665**) and makes a substantial negative contribution (**−0.3809**); it is driven almost entirely by ` will` (**+36**). Its downstream counterpart **L2:F188** is another *will* feature (**frac_nonzero 0.0176**) and contributes **−0.2100**. Thus even the apparent propositional/future construction is represented through local lexical detection, not through a relation between the two assertions.

The graph does contain a positive feature for telecommunications/telephones, **L4:F7998** (**−0.2334** to the probe direction; **frac_nonzero 0.01076**), which is plausibly related to “recorded menu” as a phone-service phrase. But it is negative and much weaker than the shallow direct lexical effects. It therefore does not establish that the probe has computed the contradiction.

Most importantly for the user concern: **no high-impact feature inspected is a detector for “not,” denial, negation, or an entailment/contradiction relation.** The literal `not` tokens are later in the passage, whereas the prominent circuit terminates at the early tokens `recorded menu will` (positions 2–4). The classification is consequently best characterized as **spurious lexical/template association**—largely the opening phrase “A recorded menu will…” and the repeated word “menu”—rather than either (a) a negation-only heuristic or (b) a genuine comparison of “will provide information” against “do not provide any information at this time.”

The attempted delegated deep traces were unavailable due to a tool-side key-limit error, but direct upstream tracing did reach the relevant token embeddings, making the central lexical-source conclusion well supported.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | Recorded/record lexical detectors | the word "record" appearing in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L0:F7404](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) | 2 | Recorded/record lexical detectors |  the word "faith", sometimes in association with related ideas like "links" or "opportunities" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) |
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | Recorded/record lexical detectors |  the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L2:F3059](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) | 2 | Recorded/record lexical detectors |  the verb "record" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | Recorded/record lexical detectors |  words related to finance and property law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | Menu lexical detectors | the word "menu" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |
| [L1:F12253](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) | 3 | Menu lexical detectors |  the word 'menu' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) |
| [L2:F3648](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) | 3 | Menu lexical detectors | code snippets related to menus and restaurants | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) |
| [L3:F3573](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) | 3 | Menu lexical detectors | the word "menu" often in conjunction with interface elements | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 4 | Will/future-form lexical detector |  the word "will." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L2:F188](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) | 4 | Will/future-form lexical detector | the word "will" in various contexts, sometimes alongside words related to consequences or legal matters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L2:8776 de=0.523 |
| 3 | `inspect_feature` ×6 | L2:8776, L0:2108, L1:12253, L0:8046, L1:3691, L0:7443 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F8776@2` | ❌ error | — | — | Trace the strongest positive driver of the synthetic contradiction-probe score u… |
| SA-2 | `L1:F12253@3` | ❌ error | — | — | Trace this strong negative driver of the probe score to embeddings and identify … |
| SA-3 | `L1:F3691@2` | ❌ error | — | — | Trace this positive probe-driving feature upstream to token embeddings. Identify… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F8776@2, k=20 → Emb:" recorded"@2 (de=19.50) +19 more |
| 2 | `get_upstream_features` | L1:F12253@3, k=20 → Emb:" menu"@3 (de=20.62) +19 more |
| 3 | `get_upstream_features` | L1:F3691@2, k=20 → Emb:" recorded"@2 (de=24.75) +19 more |
| 4 | `get_upstream_features` | L0:F2108@3, k=20 → Emb:" menu"@3 (de=25.75) +19 more |
| 5 | `get_upstream_features` | L0:F8046@4, k=20 → Emb:" will"@4 (de=36.00) +19 more |
| 6 | `get_upstream_features` | L0:F7443@2, k=20 → Emb:" recorded"@2 (de=22.62) +19 more |
| 7 | `inspect_feature` ×8 | L3:3573, L4:7998, L2:3648, L2:188, L2:3059, L0:7404, L0:6649, L0:5128 |
| 8 | `get_upstream_features` | L0:F7404@2, k=8 → Emb:" recorded"@2 (de=14.25) +7 more |
| 9 | `get_upstream_features` | L0:F6649@3, k=8 → Emb:" menu"@3 (de=14.38) +7 more |

### Build

`build_circuit` → 7 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 27,238 | 2,674 | 83,853 | 0 | $0.1292 | — | — |
| **Total** | | **27,238** | **2,674** | **83,853** | **0** | **$0.1292** | | |

**Oracle wall-clock time:** 0m 38s