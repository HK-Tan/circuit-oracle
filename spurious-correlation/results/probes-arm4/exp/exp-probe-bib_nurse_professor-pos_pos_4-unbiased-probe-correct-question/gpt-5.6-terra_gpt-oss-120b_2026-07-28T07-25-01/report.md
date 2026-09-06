# Circuit Oracle Report
**Date:** 2026-07-28 07:25:01 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven primarily by an explicit, multi-layer nursing-profession circuit—especially “Nursing,” “nurse,” and “practitioner”—rather than by Lori’s name or gendered pronouns, with a smaller nonspecific education-biography contribution from “graduated.”

**Confidence:** 9/10

**Reasoning:** The built circuit shows several direct input-to-concept paths feeding the **Probe classification score** rather than an ordinary vocabulary logit.

- The strongest profession-specific evidence begins at **Emb: Nursing (pos 18)**. It directly excites the late integrated-medical feature **L14:F3985 (pos 18)** by +11.56 and the high-level nurse-role feature **L18:F13596 (pos 18)** by +43.0. This is unusually direct and decisive evidence that the classification is tied to the literal profession-bearing degree word, not a demographic proxy.
  - **L6:F15267** is explicitly a *nursing profession* detector (fraction nonzero **0.01594**); its examples activate on “RN,” “nurse,” and “nurses.” It contributes positively to the probe at pos 33 (+0.1187) and pos 18 (+0.1016), and feeds L14:F3985.
  - **L7:F3979**, another selective nursing/healthcare feature (fraction nonzero **0.00826**), also recognizes “Nursing,” “nurse,” and “nursing.” Its direct effect on this particular probe direction is negative (about −0.10 at pos 33 and −0.07 at pos 18), so it is a countervailing nursing representation rather than the source of the positive score. Its presence confirms that the model is representing the nursing concept, while the probe weight happens to oppose this particular subfeature.

- A second explicit path begins with **Emb: nurse (pos 32)** and **Emb: practitioner (pos 33)** in the phrase “acute care nurse practitioner.”
  - **L4:F9036 (pos 33)** is a healthcare/practitioner feature (fraction nonzero **0.01468**) whose examples center on “practitioner” and “care.” It receives especially large direct support from “practitioner” (+14.0), plus “nurse” (+4.91) and “acute” (+2.09), then feeds L14:F3985 strongly (+6.41).
  - **L5:F1275 (pos 33)** detects healthcare professionals and medical fields (fraction nonzero **0.01326**), with examples specifically including “nurse care manager” and “practitioner.” It is driven by the nurse/practitioner tokens and supports the nursing feature L6:F15267 (+5.53).
  - **L8:F9619 (pos 33)** adds a broader medical-treatment representation (fraction nonzero **0.01388**) which also participates in the integrated medical-profession node.
  - These converge in **L14:F3985**, a medical/professional concept feature (fraction nonzero **0.06604**) that promotes tokens such as *patients*, *Medical*, *medical*, *clinical*, and *clinicians*. It is the top positive probe driver: +0.1572 at the “Nursing” position and +0.1309 at the “practitioner” position. Its activating examples are repeatedly nurse-manager/nursing text, so despite its broad label it clearly carries healthcare-and-nursing evidence in this input.

- The high-level endpoint, **L18:F13596 (pos 18)**, is highly selective (fraction nonzero **0.00495**) and specifically labels *nurse manager roles, skills, and leadership*. Its promoted tokens are overwhelmingly “Nurse,” “nurse,” “Nursing,” and “nursing.” It contributes +0.0535 directly to the probe. It receives strong direct support from the “Nursing” embedding (+43.0) and from L6:F15267 (+10.13), establishing a coherent deep profession-specific pathway:
  **“Nursing” → nursing detector → medical/nurse-role representation → probe score.**

- There is one smaller generic-biographical signal: **Emb: graduated (pos 2) → L0:F5038 → probe**, where **L0:F5038** detects “graduated” (fraction nonzero **0.01596**) and contributes +0.0767 directly to the probe. This is plausibly a dataset/style correlate—professional biographies often mention degrees—but it is not gendered and does not by itself identify nursing. It should be regarded as a secondary, somewhat nonspecific cue.

Regarding the user concern: the traced positive circuit does **not** support the claim that gender markers are the main mechanism. The name embedding **“Lori” (pos 1)** appears only as a very weak input to L0:F5038 (+0.45) and as a small support to L4:F9036 (+0.30), while the direct causal evidence from profession tokens is orders of magnitude larger: “Nursing” → L18:F13596 is +43, “practitioner” → L4:F9036 is +14, “Nursing” → L14:F3985 is +11.56, and “nurse” → L6:F15267 is +5.66. No gender-pronoun or female-name feature was among the important direct score drivers.

Thus, the probe does include a modest generic **education/biography** correlate, but its dominant mechanism is genuine textual recognition of nursing credentials and the nurse-practitioner role, not a spurious gender shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F5038](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) | 2 | Education wording detector | the word "graduated" or variations of it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5038) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | Healthcare / practitioner context |  words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | Healthcare / practitioner context | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 33 | Healthcare / practitioner context |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Nursing-specific detectors |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Nursing-specific detectors |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 18 | Nursing-specific detectors |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 33 | Nursing-specific detectors |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 18 | Integrated medical-profession concept | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 33 | Integrated medical-profession concept | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L8:F9619](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) | 33 | Integrated medical-profession concept |  words and phrases related to medical treatment | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 18 | High-level nurse-role representation |  text about the role, skills and leadership of nurse managers | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.157 |
| 3 | `inspect_feature` ×4 | L14:3985, L6:15267, L0:5038, L4:9036 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@18` | ❌ error | — | — | Trace this major positive path upstream to token embeddings. Determine whether i… |
| SA-2 | `L14:F3985@33` | ❌ error | — | — | Trace this major positive path upstream to token embeddings. Determine what text… |
| SA-3 | `L6:F15267@33` | ❌ error | — | — | Trace this large positive mid-layer path to embedding nodes; identify input evid… |
| SA-4 | `L0:F5038@2` | ❌ error | — | — | Inspect/trace this early positive feature. Identify the exact input token at pos… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@18, k=20 → Emb:" Nursing"@18 (de=11.56) +19 more |
| 2 | `get_upstream_features` | L14:F3985@33, k=20 → L4:F9036 (de=6.41) +19 more |
| 3 | `get_upstream_features` | L6:F15267@33, k=20 → Emb:" nurse"@32 (de=5.66) +19 more |
| 4 | `get_upstream_features` | L0:F5038@2, k=20 → Emb:" graduated"@2 (de=22.25) +19 more |
| 5 | `inspect_feature` ×5 | L7:3979, L18:13596, L5:1275, L4:11037, L8:9619 |
| 6 | `get_upstream_features` | L18:F13596@18, k=15 → Emb:" Nursing"@18 (de=43.00) +14 more |
| 7 | `get_upstream_features` | L4:F9036@33, k=15 → Emb:" practitioner"@33 (de=14.00) +14 more |
| 8 | `get_upstream_features` | L5:F1275@33, k=15 → L4:F9036 (de=1.70) +14 more |

### Build

`build_circuit` → 11 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 30,022 | 2,836 | 53,264 | 0 | $0.1309 | — | — |
| **Total** | | **30,022** | **2,836** | **53,264** | **0** | **$0.1309** | | |

**Oracle wall-clock time:** 0m 36s