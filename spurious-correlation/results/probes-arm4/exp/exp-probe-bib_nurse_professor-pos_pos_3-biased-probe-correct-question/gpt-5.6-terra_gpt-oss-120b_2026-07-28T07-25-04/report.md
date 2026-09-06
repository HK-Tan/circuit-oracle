# Circuit Oracle Report
**Date:** 2026-07-28 07:25:04 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s positive classification score is driven by both genuine nursing/clinical-profession evidence and a substantial, independent female-reference / female-biography signal, so the user’s concern about spurious gender reliance is supported.

**Confidence:** 9/10

**Reasoning:** The saved circuit has three positive routes into **Output: classification-probe score**:

1. **Direct profession route — genuine evidence.**  
   The input embeddings **Emb: nurse (pos 7)** and **Emb: practitioner (pos 8)** feed **Nursing / clinical-profession evidence**. In particular:
   - **L5:F1275 at pos 8** is a selective medical-profession feature (`frac_nonzero=0.01326`), whose activating examples include “nurse care manager,” “practitioner,” “DNP,” and “Respiratory Therapist.”
   - **L6:F15267 at pos 8** is explicitly a nursing detector (`frac_nonzero=0.01594`), with top examples triggered by “RN” and “nurse.” Its direct effect on the probe is strongly positive (**+0.3926**).
   
   This is an appropriate semantic mechanism: the phrase “nurse practitioner” directly contributes to the predicted profession class.

2. **Female-reference route — clearly spurious with respect to profession.**  
   **Emb: She (pos 1)** strongly excites **Female-reference detector**, especially:
   - **L6:F11646 at pos 1**, direct effect **+0.4941**, and again at pos 2, **+0.3965**. This feature is highly selective (`frac_nonzero=0.01976`) and its examples overwhelmingly activate on “she” and “her”; it promotes `she`, `her`, and `herself`.
   - The same signal feeds **L12:F12940 at pos 2** (`frac_nonzero=0.00652`), another female pronoun/possessive detector.
   - These then support **L18:F14677 at pos 1 and pos 55**, a later female-subject feature (`frac_nonzero=0.01225`) with direct effects **+0.3203** and **+0.3164**. Its activating examples are overwhelmingly “She/she,” and it promotes `she`, `her`, and `herself` while suppressing male-pronoun tokens.
   
   Most importantly, the direct upstream attribution to L18:F14677 is **Emb: She (pos 1), +27.125**, far larger than any individual intermediate contribution. Thus the circuit is not merely using grammatical gender as an incidental contextual cue: the raw female pronoun is a dominant causal input to a positive probe-driving representation.

3. **Female named-biography/accomplishment route — another correlated, non-profession-specific route.**  
   **Emb: Linda (pos 24)**, along with “She” and the earlier female-reference representation, feeds **Named female biography / accomplishments**:
   - **L12:F14970 at pos 24** is a rare named-person feature (`frac_nonzero=0.00269`) with positive direct effect **+0.3242**. Its examples are personal names, and its promoted tokens include `herself`.
   - **L19:F9685 at pos 24** has direct effect **+0.2383**, is labeled female names plus roles/accomplishments (`frac_nonzero=0.01351`), and is directly supported by **Linda** (**+3.4531**), **She** (**+2.9844**), and even **nurse** (**+1.8047**).
   
   This looks like a “woman described in a biographical profile” representation rather than a nurse-specific one. It probably captures the document genre and the named female subject, which can correlate with the target class but does not identify the profession independently.

The probe is therefore **not driven exclusively by the explicit profession phrase**. It does contain a valid nursing detector, but the strongest reported positive driver is **L6:F11646**, a gender-marker feature (+0.4941), and later woman-reference features remain major contributors. The circuit supports a mixed mechanism: **profession evidence plus gender-correlated biography cues**, with the latter sufficiently strong to constitute a meaningful spurious feature pathway.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female-reference detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Female-reference detector |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Female-reference detector | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 8 | Nursing / clinical-profession evidence | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Nursing / clinical-profession evidence |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Female-subject representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 55 | Female-subject representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 24 | Named female biography / accomplishments |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 24 | Named female biography / accomplishments |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.494 |
| 3 | `inspect_feature` ×6 | L6:11646, L6:15267, L18:14677, L12:14970, L12:12940, L19:9685 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ❌ error | — | — | Trace this major positive driver of the probe score upstream to embeddings; dete… |
| SA-2 | `L12:F14970@24` | ❌ error | — | — | Trace this positive probe-driving feature upstream to embeddings, identifying th… |
| SA-3 | `L6:F11646@1` | ❌ error | — | — | Trace this strongest positive early feature from 'She' context to embeddings and… |
| SA-4 | `L19:F9685@24` | ❌ error | — | — | Trace this late positive probe driver upstream to embeddings and characterize th… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@1, k=15 → Emb:"She"@1 (de=27.12) +14 more |
| 2 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"She"@1 (de=19.25) +14 more |
| 3 | `get_upstream_features` | L6:F15267@8, k=15 → Emb:" nurse"@7 (de=7.06) +14 more |
| 4 | `get_upstream_features` | L19:F9685@24, k=15 → Emb:" Linda"@24 (de=3.45) +14 more |
| 5 | `get_upstream_features` | L12:F12940@2, k=15 → Emb:"She"@1 (de=6.03) +14 more |
| 6 | `get_upstream_features` | L12:F14970@24, k=15 → Emb:"<bos>"@0 (de=-3.17) +14 more |
| 7 | `inspect_feature` ×4 | L4:7864, L5:1275, L4:15317, L7:2765 |

### Build

`build_circuit` → 9 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 20,316 | 2,626 | 69,382 | 0 | $0.1075 | — | — |
| **Total** | | **20,316** | **2,626** | **69,382** | **0** | **$0.1075** | | |

**Oracle wall-clock time:** 0m 38s