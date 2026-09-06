# Circuit Oracle Report
**Date:** 2026-07-28 07:24:56 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession probe is driven primarily by explicit nursing and clinical-workplace evidence—especially “nurse practitioner,” “nurse,” “Internal Medicine,” and “labor”—rather than by the gendered wording “She” or the name “Linda.”

**Confidence:** 8/10

**Reasoning:** The saved circuit shows several convergent profession-relevant routes into the **Output: profession-classification probe score**.

- The strongest direct positive probe drivers are the explicit nursing detector **L6:F15267** at positions 7–8 (direct effects **+0.056 to +0.087**). Its interpretation is specifically “words in the document referring to the profession of nursing,” with a low firing rate (**frac_nonzero 0.01594**) and top activating examples centered on *RN*, *registered nurse*, and *nurse*. This is highly diagnostic profession evidence, not a demographic proxy.
  - Upstream, it is driven most strongly by **Emb: nurse (pos 7)** (**+7.06**) and **Emb: practitioner (pos 8)** (**+3.48**), with an additional positive feature at L5. Thus the literal occupation phrase *“nurse practitioner”* is directly represented and read out by the probe.

- A late medical/patient integration feature, **L14:F3985** at positions 7, 8, and 11, is also a major positive driver (**+0.041 to +0.089**). Its examples and promoted tokens—*patients*, *medical*, *clinical*, *clinicians*—identify it as a medical/professional-context feature (**frac_nonzero 0.06604**).
  - It receives strong positive input from **Emb: practitioner (pos 8)** (**+6.19**) and from the nursing detector **L6:F15267** (**+2.02**), as well as direct input from **Emb: nurse (pos 7)**. This constitutes a coherent composition: occupation title → nursing representation → medical/patient context.

- The circuit separately captures later biographical clinical context through **L4:F4665 at pos 46** (direct effect **+0.0527**). This is a medical-environment feature (**frac_nonzero 0.01235**) that promotes *hospital* and activates on care, departments, units, and facilities.
  - Its strongest input is **Emb: labor (pos 44)** (**+3.45**), with further positive input from **Emb: Medicine (pos 11)** (**+1.67**) and **Emb: nurse (pos 7)** (**+2.22**). Although the low-level **L0:F1832** is a generic *labor* word detector (**frac_nonzero 0.00632**) and can occur in non-medical contexts, it is disambiguated here by the surrounding medical/nursing pathway and the explicit phrase *“labor and delivery nurse.”*

- **L15:F15159 at pos 7** adds a highly selective healthcare feature (**frac_nonzero 0.00612**), promoted toward *healthcare*, *patients*, and *medical*. It is dominated upstream by **Emb: nurse (pos 7)** (**+17.5**) and also gets positive input from the L14 medical-summary feature. This is another occupation/healthcare route rather than a gender route.

Regarding the concern about spurious gender features: **“She” (pos 1)** does appear as a small positive upstream contribution to L15:F15159 (**+1.09**), but it is tiny relative to the explicit **nurse** contribution (**+17.5**) and is not itself among the top direct positive features driving the probe. No inspected top feature is a pronoun-, female-name-, or gender-marker detector. The prominent evidence instead tracks the occupation phrase and corroborating clinical vocabulary.

The probe therefore appears to classify this example using **genuine profession indicators**, with some broad healthcare-context dependence. A remaining limitation is that the mechanism is strongest for explicit lexical cues—particularly *nurse* and *practitioner*—so it may be more a detector of overt nursing/clinical language than an abstract, context-independent representation of the profession.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 7 | Explicit nursing/profession detector |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Explicit nursing/profession detector |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 46 | Clinical workplace and labor/delivery context |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L0:F1832](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) | 44 | Clinical workplace and labor/delivery context | the word "labor" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 7 | Medical/patient concept integration | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 8 | Medical/patient concept integration | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | Medical/patient concept integration | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 7 | Healthcare semantic detector |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.089 |
| 3 | `inspect_feature` ×4 | L14:3985, L15:15159, L4:4665, L6:15267 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@8` | ❌ error | — | — | Trace this major positive driver of the synthetic profession-probe score upstrea… |
| SA-2 | `L15:F15159@7` | ❌ error | — | — | Trace this late positive probe-score feature upstream to embeddings. Determine i… |
| SA-3 | `L4:F4665@46` | ❌ error | — | — | Trace this positive feature at the nursing/clinical-text position to embeddings.… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@8, k=15 → Emb:" practitioner"@8 (de=6.19) +14 more |
| 2 | `get_upstream_features` | L6:F15267@8, k=15 → Emb:" nurse"@7 (de=7.06) +14 more |
| 3 | `get_upstream_features` | L15:F15159@7, k=15 → Emb:" nurse"@7 (de=17.50) +14 more |
| 4 | `get_upstream_features` | L4:F4665@46, k=15 → Emb:" labor"@44 (de=3.45) +14 more |
| 5 | `inspect_feature` ×3 | L0:1832, L4:9757, L4:12178 |

### Build

`build_circuit` → 9 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 14,772 | 2,208 | 42,799 | 0 | $0.0807 | — | — |
| **Total** | | **14,772** | **2,208** | **42,799** | **0** | **$0.0807** | | |

**Oracle wall-clock time:** 0m 34s