# Elicitation Report

**Prompt:** Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L4:F12126 | 2 | Acknowledgement/conversational opener |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | 1.23e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| L4:F4847 | 2 | Acknowledgement/conversational opener |  words or short phrases often used in conversation, and especially questions and answers | 1.16e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| L2:F1759 | 2 | Acknowledgement/conversational opener | — | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) |
| L0:F8083 | 6 | NCAA phrase / 'double A' and sports-stat form | the word "double" and surrounding words when numbers are also present | 1.55e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| L3:F9770 | 7 | NCAA phrase / 'double A' and sports-stat form |  technical and scientific writing about neuroscience and chemistry, possibly about calcium | 1.09e-02 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| L4:F5709 | 14 | Temporal 'now' cue | astronomy terms | 1.42e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| L0:F6236 | 20 | Token-level contracted negation detector | the letter "t" when it follows the word "isn'" or "doesn'" | 2.58e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| L0:F16366 | 25 | Lexical because detector |  the word "because" | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_well | well_discourse |
| emb_yeah | well_discourse |
| emb_double | sports_number |
| emb_now | now_cue |
| emb_havent | negation |
| emb_apostrophe | negation |
| emb_t | negation |
| emb_because | causal |
| well_discourse | probe |
| sports_number | probe |
| now_cue | probe |
| negation | probe |
| causal | probe |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The contradiction-probe score is driven primarily by shallow lexical/discourse features—especially the opening “yeah well,” contracted negation in “haven’t,” and local “double A”/“now” cues—rather than by a compositional representation that resolves the incompatibility between *“haven’t watched … a single game”* and *“haven’t missed a single game.”*

**Confidence:** 8/10

**Reasoning:** The saved circuit shows a predominantly surface-form mechanism feeding the linear probe direction.

* **Discourse-opener path:** `Emb: yeah (pos 1)` and `Emb: well (pos 2)` strongly excite the acknowledgement/conversational-opener supernode. Its major components are:
  * L4:F12126 at pos 2, labelled acknowledgement/agreement expressions such as “well” and “yeah” (`frac_nonzero=0.01233`), which has the largest listed probe effect, **−0.6484**.
  * L4:F4847 at pos 2, a conversational-question/answer feature (`frac_nonzero=0.01156`), with **+0.3887** probe effect.
  * The upstream attribution is direct and lexical: “ well” contributes +14.625 into F12126 and +8.0625 into F4847; “yeah” contributes +4.625 into F12126. This is compelling evidence of a discourse-style cue, not contradiction reasoning. The two related features even push the probe in opposite directions, consistent with an incidental probe alignment to a style subspace.

* **Negation path:** `Emb: haven (pos 18)`, the apostrophe at pos 19, and `t` at pos 20 feed L0:F6236. This feature is explicitly a contracted-negation-token detector—“t” after *isn’*/*doesn’*—with very low firing frequency (`frac_nonzero=0.00258`) and top promoted tokens **“not,” “Not,” “NOT”**. It has a substantial **negative** direct effect on the probe (**−0.4570**). Its immediate upstream evidence is exact tokenization: `t` +17.875, `haven` +16.625, apostrophe +12.125. Thus, the probe is plainly sensitive to negation morphology, but this feature alone neither represents nor compares the two propositions.

* **“Double A” / sports-form path:** `Emb: double (pos 6)` directly activates L0:F8083, which detects “double” in numerical contexts (`frac_nonzero=0.01553`; **−0.3320** to the probe), with direct input attribution +19.625 from “double.” It also feeds the L3:F9770 path (**−0.3145**), whose nominal autogenerated label is neuroscience/chemistry but whose strongest examples include sports statistics, scores, rebounds, and “figures”; in this prompt it is driven primarily by `Emb: double (pos 6)` (+18.0), not by an abstract NCAA-tournament representation. This looks like a local lexical/format cue associated with the phrase “NC double A,” rather than semantic recognition of the sporting claim.

* **Temporal and causal lexical paths:** L4:F5709 at “now” (pos 14) has **−0.2773** probe effect, despite its noisy “astronomy terms” label. The actual attribution identifies `Emb: now (pos 14)` as overwhelmingly dominant (+40.75), so its operative role here is a token-specific *now* cue. Similarly, L0:F16366 detects “because” (`frac_nonzero=0.01813`) and has **+0.2930** effect; it receives +40.75 directly from `Emb: because (pos 25)`. This is lexical detection of a causal connective, not a representation of the causal proposition.

The circuit contains some task-relevant ingredients: it detects the negation in “haven’t,” and it notices discourse/cause markers around the two claims. But no traced high-impact feature is an entity-specific or proposition-level feature for **Louisville**, **watching games**, **missing games**, or a cross-sentence incompatibility relation. In particular, the strongest paths reach embeddings directly at the exact cue words, rather than showing a multi-layer merge of the first statement’s *not watched any* content with the second statement’s *not missed any* content.

Therefore, the user concern is substantially supported: this probe’s classification score is dominated by spurious or weakly correlated lexical/style signatures—especially contracted negation—rather than robust semantic contradiction detection. The fact that “because,” “yeah well,” “double,” and “now” independently have large effects is further evidence that the linear probe direction is entangled with training-distribution artifacts.
