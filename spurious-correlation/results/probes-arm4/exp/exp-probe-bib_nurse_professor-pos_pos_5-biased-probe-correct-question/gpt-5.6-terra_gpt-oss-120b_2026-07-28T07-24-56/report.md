# Circuit Oracle Report
**Date:** 2026-07-28 07:24:56 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s positive profession-classification score is driven by a mixture of genuine nursing/obstetrics evidence and a substantial, direct female-gender/biographical cue pathway.

**Confidence:** 9/10

**Reasoning:** The saved circuit shows two distinct mechanisms feeding the output probe score.

1. **Genuine profession evidence is present.**
   - The strongest direct profession-relevant feature is **L4:F13803 at “Delivery” (pos 11)**, which detects *obstetrics and gynecology* language (frac_nonzero **0.0138**) and promotes tokens including *pregnancy*, *postpartum*, *fertility*, and *motherhood*. Its main positive upstream inputs are exactly **“Labor” (pos 9, +8.81)** and **“Delivery” (pos 11, +12.19)**. Thus the `Emb: Labor` → `Labor-and-delivery / obstetrics cue` → probe branch is semantically grounded.
   - **L6:F15267 at “nurse” (pos 12)** is explicitly a *nursing-profession detector* (frac_nonzero **0.01594**), with examples firing on “RN,” “nurse,” and “nurses.” It directly pushes the probe score positively (+0.281). This is the clearest occupation-specific contribution.
   - The late female feature **L18:F14677** also receives a positive direct input from the first **“nurse” (pos 12, +2.53)**, so profession language is partly being incorporated into its broader representation.

2. **But the circuit prominently uses spurious gender signals.**
   - **L18:F14677** is one of the largest positive probe drivers: it fires at positions 54, 31, and 68, contributing **+0.447, +0.434, and +0.412** respectively. Its interpretation is unambiguously *mentions of women or girls* (frac_nonzero **0.01225**); it promotes **“she,” “her,” “herself”** and suppresses **“his,” “him,” “himself.”**
   - At its occurrence on **“She” (pos 54)**, its dominant upstream cause is the raw **`Emb: She (pos 54)` embedding (+14.56)**. This makes the gender contribution causal rather than merely correlational in the feature label: the female pronoun is directly propagated into a feature that positively drives the profession probe.
   - **L19:F9685 at “Melissa” (pos 31)** is another major positive driver (+0.441). It detects *women’s names and their roles/accomplishments* (frac_nonzero **0.01351**) and likewise promotes feminine pronouns. Its upstream inputs include **“Melissa” (pos 31, +2.19)**, **“Melissa” (pos 5, +1.35)**, **“her” (pos 15, +0.95)**, and **“nurse” (pos 12, +2.33)**. This is a blended “woman in a biographical role” pattern, not a clean occupation representation.
   - The name path begins with **L4:F1276**, a generic capitalized-name detector (frac_nonzero **0.00341**), and **L6:F8166**, detecting longer proper names ending in *a/i/e* (frac_nonzero **0.00559**). Those feed **L12:F14970**, a broad person-name feature at **“Melissa” (pos 5)**, which is itself the single largest listed direct positive contribution to the probe (**+0.559**). These are not nursing-specific features. The *Melissa* name additionally supports the female-biography representation.

Therefore, the concern is **supported**: this is not a profession classification based solely, or even primarily at every stage, on explicit occupational terms. There is legitimate evidence from *Labor and Delivery* and *nurse*, but the probe direction is also strongly aligned with features encoding **female names, female pronouns, and “a woman’s biography/accomplishments.”** In particular, the direct `She (pos 54)` → L18:F14677 → probe route is a clear spurious gender-marker pathway. The circuit suggests the trained probe has learned a conflated direction: **nursing/midwifery/obstetrics language plus female-coded identity cues**, rather than a gender-invariant occupation concept.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 5 | Early name / proper-name cues | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 31 | Early name / proper-name cues | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 5 | Early name / proper-name cues |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 31 | Early name / proper-name cues |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | Labor-and-delivery / obstetrics cue |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | Nursing-profession detector |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 5 | Person-name representation |  names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 54 | Female-reference / female biography representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 31 | Female-reference / female biography representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 68 | Female-reference / female biography representation |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 31 | Female-reference / female biography representation |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 54 | Female-reference / female biography representation |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L12:14970 de=0.559 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@54` | ❌ error | — | — | Trace why this repeated late feature drives the probe; determine whether it repr… |
| SA-2 | `L19:F9685@31` | ❌ error | — | — | Trace this late probe-driving feature upstream. Determine its semantic role and … |
| SA-3 | `L12:F14970@5` | ❌ error | — | — | Trace the strong early/mid feature at the Melissa token upstream to determine wh… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L18:14677, L19:9685, L12:14970, L4:1276, L4:13803 |
| 2 | `get_upstream_features` | L18:F14677@54, k=15 → Emb:" She"@54 (de=14.56) +14 more |
| 3 | `get_upstream_features` | L19:F9685@31, k=15 → Emb:" nurse"@12 (de=2.33) +14 more |
| 4 | `get_upstream_features` | L4:F13803@11, k=15 → Emb:" Delivery"@11 (de=12.19) +14 more |
| 5 | `get_upstream_features` | L12:F14970@5, k=15 → L4:F1276 (de=3.36) +14 more |
| 6 | `inspect_feature` ×3 | L6:8166, L6:11646, L6:15267 |

### Build

`build_circuit` → 11 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 16,180 | 2,500 | 46,526 | 0 | $0.0896 | — | — |
| **Total** | | **16,180** | **2,500** | **46,526** | **0** | **$0.0896** | | |

**Oracle wall-clock time:** 0m 32s