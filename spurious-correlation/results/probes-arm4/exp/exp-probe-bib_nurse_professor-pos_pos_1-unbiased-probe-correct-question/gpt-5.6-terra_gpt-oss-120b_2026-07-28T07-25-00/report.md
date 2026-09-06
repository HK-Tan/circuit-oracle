# Circuit Oracle Report
**Date:** 2026-07-28 07:25:00 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s positive profession score is driven primarily by explicit *perioperative nursing* evidence—especially the token “nurses” and the adjacent “Perio/perative” tokens—rather than by the female pronoun “she.”

**Confidence:** 9/10

**Reasoning:** The saved circuit shows a coherent profession-semantic pathway from **Emb: nurses (pos 15)** and **Emb: Perio/perative (pos 13–14)** through medical-context and nursing detectors into the profession-probe output.

* The strongest direct positive feature is **L14:F3985 at pos 15** (+0.1631 to the probe). It detects management/leadership/medical language, fires relatively selectively (**frac_nonzero 0.06604**), and its top examples are specifically nurse-manager and professional-skills text. It promotes clinical vocabulary such as *patients*, *medical*, and *clinicians*. Its strongest upstream source is the raw **“ nurses” embedding** (+10.625), with further positive support from the medical-context features and **L6:F15267**.

* The most diagnostic lexical detector is **L6:F15267 at pos 15** (+0.1582; also +0.084 at pos 14), whose label is explicitly “words in the document referring to the profession of nursing.” It is highly selective (**frac_nonzero 0.01594**) and its activating examples include *RN*, *nurse*, and *nurses*. It receives by far its largest positive input from **Emb: nurses (pos 15)** (+16.125), followed by **“perative”** (+4.375) and **“Perio”** (+1.25). This is direct evidence that the score is responding to the occupation-bearing phrase *Perioperative nurses*, not merely generic healthcare prose.

* The later specialized nurse-leadership feature **L18:F13596 at pos 15** (+0.0981; +0.0815 at pos 14) is even more selective (**frac_nonzero 0.00495**). Its examples specifically describe *nurse managers*, nursing leadership, and nursing skills; its promoted tokens are *Nurse*, *nurse*, *Nursing*, and *nurses*. It is driven overwhelmingly by **Emb: nurses** (+42), with secondary support from L6:F15267 (+7.125), “perative” (+6.25), L14:F3985 (+3.7969), and healthcare-context features. Thus the representation is not just “female healthcare worker”: it is a fairly specific nursing/clinical-leadership concept.

* The supporting **Medical/perioperative context detector** supernode contains:
  * **L4:F4665 at pos 14** (+0.105), a medical-environment/facility feature (**frac_nonzero 0.01235**) promoting *hospital*;
  * **L8:F16339 at pos 15** (+0.1055), a hospital/medical-context feature (**frac_nonzero 0.02303**) promoting *hospital*, *medical*, and *physician*; and
  * **L7:F210 at pos 15** (+0.0938), a healthcare-system/context feature (**frac_nonzero 0.01297**) promoting *medical* and *hospital*.
  
  These features are positively sourced by “Perio/perative” and “nurses,” then feed the nurse-management integration features. They provide context consistent with perioperative clinical work, but the explicit nursing feature is more profession-specific.

Regarding the concern about gender: **Emb: she (pos 7)** has a small positive edge into L6:F15267 (+1.039) and into L4:F4665 (+1.281), but these are far smaller than the corresponding occupation-token inputs—e.g. “nurses” contributes +16.125 to L6:F15267 and +42 to L18:F13596. Moreover, no inspected top output-driving feature is labeled as a female/gender detector. Therefore, this graph provides **some minor evidence of pronoun-associated contribution**, but the causal mechanism is predominantly genuine, text-grounded profession evidence: *Perioperative nurses*, medical settings, certification, and nursing-management semantics.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 14 | Medical/perioperative context detector |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 15 | Medical/perioperative context detector |  text discussing hospital infections and bacteria | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 15 | Medical/perioperative context detector |  words and names associated with the Asante Healthcare system | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Explicit nursing-profession detector |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 15 | Nurse-management / clinical-leadership integration | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 15 | Nurse-management / clinical-leadership integration |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L14:3985 de=0.163 |
| 3 | `inspect_feature` ×5 | L14:3985, L6:15267, L18:13596, L8:16339, L4:4665 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@15` | ❌ error | — | — | Trace this major positive driver of the profession probe score upstream to embed… |
| SA-2 | `L6:F15267@15` | ❌ error | — | — | Trace this major positive driver upstream to embedding nodes. Determine what inp… |
| SA-3 | `L18:F13596@15` | ❌ error | — | — | Trace this late positive feature upstream, including embedding sources, to deter… |
| SA-4 | `L8:F16339@15` | ❌ error | — | — | Trace the positive L8 feature to embeddings and identify whether its source sign… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@15, k=15 → Emb:" nurses"@15 (de=10.62) +14 more |
| 2 | `get_upstream_features` | L6:F15267@15, k=15 → Emb:" nurses"@15 (de=16.12) +14 more |
| 3 | `get_upstream_features` | L18:F13596@15, k=15 → Emb:" nurses"@15 (de=42.00) +14 more |
| 4 | `get_upstream_features` | L8:F16339@15, k=15 → Emb:" nurses"@15 (de=4.72) +14 more |
| 5 | `get_upstream_features` | L4:F4665@14, k=15 → Emb:"perative"@14 (de=15.44) +14 more |
| 6 | `inspect_feature` | L7, F210 → " words and names associated with the Asante Healthcare system" |

### Build

`build_circuit` → 7 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 12,672 | 2,125 | 57,075 | 0 | $0.0778 | — | — |
| **Total** | | **12,672** | **2,125** | **57,075** | **0** | **$0.0778** | | |

**Oracle wall-clock time:** 0m 32s