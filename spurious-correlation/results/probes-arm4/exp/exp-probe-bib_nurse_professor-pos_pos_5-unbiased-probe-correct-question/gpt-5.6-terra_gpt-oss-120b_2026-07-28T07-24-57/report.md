# Circuit Oracle Report
**Date:** 2026-07-28 07:24:57 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s positive profession-classification score is driven primarily by explicit nursing and obstetric employment evidence—especially “Labor and Delivery nurse”—which is composed into a medical/nursing concept circuit, rather than by the gendered name *Melissa*.

**Confidence:** 9/10

**Reasoning:**  
The synthetic probe target has probability 1, as expected for an injected linear-probe direction rather than a vocabulary prediction. Its largest positive direct effects include late feature **L14:F3985** at positions 11, 12, and 19 (effects **+0.1064**, **+0.0962**, and **+0.0608**), plus medical/nursing features such as **L6:F9980** (+0.0728), **L7:F210** (+0.0654), **L6:F15267** (+0.0635), **L4:F4665** (+0.0630), and **L6:F4490** (+0.0615).

The saved circuit is:

`Emb: Labor / Delivery / nurse → Early medical/procedure representation → Medical-care/hospital context + Nursing detector → Healthcare-profile context → Late clinical/nursing concept → Probe classification score.`

The decisive path is grounded in profession tokens:

- **Emb: “nurse” (pos 12)** directly and strongly excites the late clinical feature **L14:F3985(pos 12)** (**+10.75**) and the healthcare-context feature **L7:F210(pos 12)** (**+9.19**). This is unusually direct evidence that the probe accesses the literal occupation word, not merely a correlated demographic cue.
- **Emb: “Delivery” (pos 11)** and **Emb: “Labor” (pos 9)** feed **L3:F10198(pos 11)** with strong positive effects (**+7.59** and **+4.94**). This feature is labeled *anesthetics and medical procedures* (frequency **0.00748**), so it represents the obstetric/clinical phrase structure rather than a name or gender.
- Those same *Labor* and *Delivery* embeddings feed **L4:F4665(pos 11)**, a medical-care/facility feature, directly (**+2.89** from *Labor*) and through the early procedure feature (**+3.44** from L3:F10198). **L4:F4665** is a reasonably selective medical-environment detector (frac_nonzero **0.01235**) whose examples concern patients, hospital rooms, clinical departments, and care, and whose promoted tokens include *hospital(s)*.
- **L6:F4490(pos 11)** further integrates this evidence. Its strongest positive parent is L4:F4665 (**+3.92**), with further positive direct input from *Delivery* (**+1.33**) and *Labor* (**+1.27**). Its label is broad—medical roles/organizations and proper nouns (frac_nonzero **0.04189**)—but its promoted tokens are strongly hospital/patient-oriented.
- The dedicated nursing detector, **L6:F15267(pos 12)** (frac_nonzero **0.01594**), is explicitly labeled *words in the document referring to the profession of nursing*; its activating examples include “RN,” “registered nurse,” and “nurse.” It positively feeds the healthcare-profile feature **L7:F210(pos 12)** by **+2.88**. The low-level **L0:F8854(pos 12)** is also explicitly a *“nurse”* detector (frac_nonzero **0.00465**) and positively feeds the same L7 feature (**+1.45**).
- **L7:F210** is labeled healthcare-system/profile context (frac_nonzero **0.01297**), promotes *medical* and *hospital*, and receives strong positive direct input from *nurse* and *Delivery*. Its interpretation is not nurse-specific on its own, but it is a natural intermediate that packages the local occupation phrase into a healthcare-profile representation.
- The principal late feature, **L14:F3985**, is a selective clinical/professional concept feature (frac_nonzero **0.06604**) labeled management/leadership/medicine/studies/research. Its strongest examples repeatedly activate on *nurse* or *nurses*, and it promotes **patients, medical, clinical, clinicians**. It receives positive upstream evidence from:
  - *nurse* directly at pos 12 (**+10.75**),
  - **L7:F210(pos 12)** (**+4.03**),
  - **L6:F9980(pos 11)** (**+2.55**),
  - **L4:F4665(pos 11)** (**+2.67**),
  - **L6:F4490(pos 11)** (**+3.00**), and
  - *Delivery* directly (**+2.63** at pos 11).
  
Thus, L14:F3985 appears to combine explicit nursing terminology with medical/obstetric context before projecting positively into the probe direction.

There is **no positive gender-marker path** in the important circuit. In fact, the one inspected healthcare-profile feature **L7:F210(pos 12)** receives a **negative** direct input from **Emb: “Melissa” (pos 5), −1.22**. Likewise, L4:F4665 gets a small negative contribution from *Melissa* (**−0.64**). The name therefore does not support the positive classification through these paths; if anything, it mildly suppresses part of the relevant healthcare-context circuit.

One caveat: some circuit features are broad medical-domain detectors rather than a narrowly entity-specific representation of “labor-and-delivery nurse.” For example, L7:F210 is healthcare-profile context, L4:F4665 is medical environment, and L14:F3985 is broad clinical/professional content. But their causal activation here is anchored in the literal occupation phrase *Labor and Delivery nurse*, with an independently identified nursing-specific L6 feature. Therefore the concern that the classifier is primarily exploiting gender markers is **not supported by this attribution graph**; the dominant mechanism is genuine profession and clinical-context evidence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L3:F10198](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) | 11 | Early medical/procedure representation |  words related to anesthetics and medical procedures | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10198) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 11 | Medical-care / hospital context |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 12 | Medical-care / hospital context |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 11 | Medical-care / hospital context |  proper nouns corresponding to locations, organizations, medical roles, and coding terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | Nursing-profession detector |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L0:F8854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) | 12 | Nursing-profession detector |  the word "nurse" as well as some pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 11 | Healthcare organization/profile context |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 12 | Healthcare organization/profile context |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | Late clinical/nursing concept | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 12 | Late clinical/nursing concept | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 19 | Late clinical/nursing concept | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.106 |
| 3 | `inspect_feature` ×4 | L14:3985, L0:9911, L6:9980, L7:210 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@11` | ❌ error | — | — | Trace this major positive probe-driving feature upstream to embeddings. Determin… |
| SA-2 | `L14:F3985@12` | ❌ error | — | — | Trace this major positive probe-driving feature upstream to embeddings. Determin… |
| SA-3 | `L6:F9980@11` | ❌ error | — | — | Trace this independent positive probe-driving feature upstream to embeddings. Ch… |
| SA-4 | `L7:F210@12` | ❌ error | — | — | Trace this positive probe-driving feature upstream to embeddings. Determine sign… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@11, k=20 → L6:F4490 (de=3.00) +19 more |
| 2 | `get_upstream_features` | L14:F3985@12, k=20 → Emb:" nurse"@12 (de=10.75) +19 more |
| 3 | `get_upstream_features` | L6:F9980@11, k=15 → L4:F4665 (de=2.80) +14 more |
| 4 | `get_upstream_features` | L7:F210@12, k=15 → Emb:" nurse"@12 (de=9.19) +14 more |
| 5 | `get_upstream_features` | L4:F4665@11, k=15 → L3:F10198 (de=3.44) +14 more |
| 6 | `inspect_feature` ×6 | L4:4665, L6:4490, L6:15267, L8:16339, L3:10198, L0:8854 |
| 7 | `get_upstream_features` | L3:F10198@11, k=20 → Emb:" Delivery"@11 (de=7.59) +19 more |
| 8 | `get_upstream_features` | L6:F4490@11, k=20 → L4:F4665 (de=3.92) +19 more |

### Build

`build_circuit` → 9 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 25,504 | 2,854 | 58,796 | 0 | $0.1213 | — | — |
| **Total** | | **25,504** | **2,854** | **58,796** | **0** | **$0.1213** | | |

**Oracle wall-clock time:** 0m 35s