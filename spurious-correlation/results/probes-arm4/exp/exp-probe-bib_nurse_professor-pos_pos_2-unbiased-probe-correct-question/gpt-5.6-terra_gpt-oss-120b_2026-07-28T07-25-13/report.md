# Circuit Oracle Report
**Date:** 2026-07-28 07:25:13 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s profession score is driven primarily by explicit, token-local nursing evidence—especially the word **“Nursing”**—which is transformed into increasingly specific nurse/clinical concepts, not by the gender marker “She.”

**Confidence:** 9/10

**Reasoning:** The saved circuit shows a strong causal route from **Emb: “Nursing” (pos 10)** through explicit nursing detectors to the probe score:

- The largest positive probe feature is **L14:F3985 (pos 10)**, direct effect **+0.1875**. Its label is medical/clinical/professional terminology; its activating examples repeatedly fire on *nurse/nurses*, and it promotes **“patients,” “Medical,” “clinical,”** and **“clinicians.”** It is moderately selective (**frac_nonzero 0.06604**). Its strongest upstream input is directly the **“Nursing” embedding** (**+12.125**), with further positive support from nursing-relevant intermediate features, including **L6:F15267** (**+2.2344**).

- **L6:F15267 (pos 10)** is an especially clear profession feature: *“words in the document referring to the profession of nursing”*, with low firing frequency (**frac_nonzero 0.01594**) and examples triggered by **“RN”** and **“nurse.”** It directly raises the probe score by **+0.1348**, its second-largest positive contribution. Crucially, this feature is itself driven overwhelmingly by **Emb: “Nursing” (pos 10)** with direct effect **+17.375**, rather than by a pronoun, name, or generic biographical formatting.

- The late, highly selective semantic representation **L18:F13596 (pos 10)** contributes **+0.0520** directly to the probe. It is labeled as text about nurse-manager roles, skills, and leadership, fires only **0.00495** of the time, and promotes **“Nurse,” “nurse,” “Nursing,”** and **“nursing.”** Its most important upstream cause is again **Emb: “Nursing” (pos 10)** (**+42.75**), followed by the nursing feature **L6:F15267** (**+9.4375**) and clinical aggregation **L14:F3985** (**+6.3125**). This is strong evidence of a semantic nursing concept being encoded and aligned with the probe direction.

Thus the main forward mechanism in the circuit is:

**Emb: “Nursing” → Explicit nursing-token detectors (L6:F15267; associated L6/L7/L8 features) → Clinical/nursing semantic aggregation (L14:F3985) → nurse-specific concept (L18:F13596) → profession probe score.**

There is a small separate biography/education-context route: **Emb: “graduated” (pos 2) → L0:F5038 → probe**. **L0:F5038** is a “graduated” detector and has a positive direct effect of **+0.0884**. Its upstream attribution is overwhelmingly the literal **“graduated”** embedding (**+22.25**), with only a very small contribution from **Emb: “She” (pos 1)** (**+0.373**). This is generic resume/education evidence, not an identity or gender representation.

The pronoun **“She”** does not appear as a meaningful upstream driver of the core nursing features. Its only observed positive connection is weak and indirect through the generic graduation detector; it is orders of magnitude smaller than the direct “Nursing” signal. Likewise, other top layer-0 features in the raw ranking are not evidence of gender: **L0:F6270** is principally a *“whom”/function-word* detector, and **L0:F16075** is an *“of”/court-name* detector.

There are also countervailing nursing/healthcare features, notably **L7:F3979**, which is semantically nursing-related (**frac_nonzero 0.00826**) but has a **negative** direct probe effect (**−0.1099** at pos 10). This indicates the linear probe does not simply reward every healthcare feature; it weights particular nursing representations positively and others negatively. That complicates the probe direction somewhat, but does not change the main conclusion about the evidence source.

**Conclusion on the concern:** in this attribution graph, the classification is **not chiefly using a spurious gender shortcut**. It is predominantly grounded in explicit profession text—“Nursing,” reinforced by the surrounding nursing-career content—and represented by selective nursing/nurse features. The generic “graduated” signal provides an additional, weaker resume-like cue; “She” has negligible causal support in the traced circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 2 | Education-context detector: graduated | the word "graduated" or variations of it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | Explicit nursing-token detectors |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 10 | Explicit nursing-token detectors | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 10 | Explicit nursing-token detectors | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 10 | Explicit nursing-token detectors | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 10 | Clinical/nursing semantic aggregation | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 10 | Highly specific nurse/nurse-manager concept |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.188 |
| 3 | `inspect_feature` ×4 | L14:3985, L6:15267, L18:13596, L0:5038 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@10` | ❌ error | — | — | Trace this strongest positive driver of the profession probe to embeddings. Dete… |
| SA-2 | `L6:F15267@10` | ❌ error | — | — | Trace this major positive driver to embeddings. Identify the exact input evidenc… |
| SA-3 | `L18:F13596@10` | ❌ error | — | — | Trace this later positive feature to embeddings and assess its semantic evidence… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@10, k=20 → Emb:" Nursing"@10 (de=12.12) +19 more |
| 2 | `get_upstream_features` | L6:F15267@10, k=20 → Emb:" Nursing"@10 (de=17.38) +19 more |
| 3 | `get_upstream_features` | L18:F13596@10, k=20 → Emb:" Nursing"@10 (de=42.75) +19 more |
| 4 | `get_upstream_features` | L0:F5038@2, k=20 → Emb:" graduated"@2 (de=22.25) +19 more |
| 5 | `inspect_feature` ×3 | L0:6270, L0:16075, L7:3979 |

### Build

`build_circuit` → 8 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 14,902 | 2,224 | 43,669 | 0 | $0.0815 | — | — |
| **Total** | | **14,902** | **2,224** | **43,669** | **0** | **$0.0815** | | |

**Oracle wall-clock time:** 0m 47s