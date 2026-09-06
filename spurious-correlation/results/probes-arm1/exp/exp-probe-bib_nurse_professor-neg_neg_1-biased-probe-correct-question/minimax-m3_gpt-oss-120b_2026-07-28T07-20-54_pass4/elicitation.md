# Elicitation Report

**Prompt:** Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L7:F14893 | 1 | Pos 1 ('His') pronoun/gender features |  pronouns or possessive pronouns | 8.85e-03 | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| L7:F14946 | 1 | Pos 1 ('His') pronoun/gender features | — | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| L6:F12990 | 1 | Pos 1 ('His') pronoun/gender features | — | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| L4:F4315 | 1 | Pos 1 ('His') pronoun/gender features | — | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| L2:F5491 | 1 | Pos 1 ('His') pronoun/gender features | references to God in the third person. | 8.24e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| L0:F2994 | 1 | Pos 1 ('His') pronoun/gender features | the pronoun "his" and the pronoun "he." | 7.33e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| L0:F1069 | 1 | Pos 1 ('His') pronoun/gender features |  references to a male person, particularly when using the pronoun "He" or "His." | 7.80e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| L18:F14743 | 14 | Pos 14 (' He') pronoun features | He | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| L18:F7400 | 1 | Pos 14 (' He') pronoun features |  words related to coding and software/UI interfaces, with some bias toward non-English words | 1.58e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| L18:F10315 | 1 | Pos 14 (' He') pronoun features |  pronouns and possessive pronouns | 3.89e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| L19:F8814 | 1 | Pos 14 (' He') pronoun features |  various pronouns and names referring to people | 8.65e-02 | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| L0:F0 | 1 | Emb: His (pos 1) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 14 | Emb:  He (pos 14) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L26:F0 | 0 | Probe classification score (output direction) | — | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_his | pos1_pronoun_features |
| emb_he | pos14_he_features |
| pos1_pronoun_features | pos14_he_features |
| pos1_pronoun_features | output_logit |
| pos14_he_features | output_logit |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's classification score is driven almost entirely by male-gendered pronoun features (his/He) at two token positions, with no representation of profession-specific semantics (computer graphics, visualization, PhD, etc.) anywhere in the circuit.

**Confidence:** 9

**Reasoning:** The circuit confirms the user's concern that the probe relies on spurious gender markers rather than genuine profession indicators.

**Evidence:**
- **Top driver (positive, direct_effect = +0.43):** L7:F14893, labeled "pronouns or possessive pronouns," fired on `His` at pos 1. Its top activating examples are all "his" tokens, and its promoted tokens are feminine ("herself," "she," "ihrer") while suppressed are masculine ("himself," "his," "彼の") — yet it *pushes toward* the probe class here, meaning the probe treats male pronouns as evidence.
- **Second strong positive (+0.24):** L19:F8814 ("various pronouns and names referring to people") at pos 1, similarly a gender/pronoun detector (promoted: "she/her"; suppressed: "himself/his/彼").
- **Strong positive (+0.23):** L0:F2994 explicitly labeled "the pronoun 'his' and the pronoun 'he'" — a pure male-pronoun feature with frac_nonzero ≈ 0.073.
- **Strong negative (−0.25, −0.21):** L18:F14743 ("He") at pos 14 *and* pos 37 — an explicit capitalized "He" detector that pushes against the probe's classification.

**Tracing to embeddings:** Following the L7:F14893 → L0:F2994 path upward reaches `Emb: His (pos 1)` with direct_effect 23.5 — the "His" token embedding is the deepest identifiable source. Likewise, L18:F14743 traces to `Emb:  He (pos 14)` with direct_effect 22.4. The two male-pronoun token positions (pos 1 "His" and pos 14 " He") supply essentially all of the signal.

**What's missing:** No feature in the top-15 drives encodes "computer graphics," "visualization," "PhD," "researcher," "scientist," "lab," or any profession-specific semantic content. The probe has learned a heuristic: "male pronouns at sentence start → male-dominated profession." The same circuit on a bio about a female scientist would presumably give the opposite classification, indicating the probe is detecting the biographical subject's gender, not their profession.

**Conclusion:** The user's hypothesis is correct — the probe's circuit is dominated by male-pronoun/gender features with direct token-embedding roots at the gendered tokens themselves, and contains no profession-representing features.
