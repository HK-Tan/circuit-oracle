# Elicitation Report

**Prompt:** Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L0:F0 | 18 | Emb: ' haven ' (pos 18) + ' (pos 19) + t (pos 20) — NEGATION token 'haven't' | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 25 | Emb: ' because ' (pos 25) — causal connector | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 8 | Emb: ' tournament ' (pos 8) — sports event noun | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 6 | Emb: ' double ' (pos 6) + ' A ' (pos 7) — NCAA compound tokens | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 14 | Emb: ' now ' (pos 14) + ' right ' (pos 13) — temporal adverb | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 24 | Emb: ' year ' (pos 24) + ' this ' (pos 23) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 2 | Emb: ' well ' (pos 2) + 'yeah' (pos 1) — discourse markers | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F6236 | 20 | Negation token feature: apostrophe-t apostrophe (haven't spelling) (L0:F6236, pos 20) | the letter "t" when it follows the word "isn'" or "doesn'" | 2.58e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| L0:F16366 | 25 | Lexical 'because' feature (L0:F16366, pos 25) |  the word "because" | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| L0:F12862 | 8 | Lexical 'tournament' feature (L0:F12862, pos 8) |  the word "tournament" and related words such as "winning", but not always | 1.53e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) |
| L0:F8083 | 6 | Lexical 'double' feature (L0:F8083, pos 6) | the word "double" and surrounding words when numbers are also present | 1.55e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| L0:F5912 | 24 | Lexical 'year' feature (L0:F5912, pos 24) | "year" but also sometimes finds related words that include "day", "living", or "sold" | 2.71e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) |
| L0:F8352 | 2 | Lexical 'well' + 'yeah' discourse markers (L0:F8352, pos 2) |  the word "well" | 3.50e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| L1:F177 | 6 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') |  the word "double" and words that begin with "multi" or "doubly" | 1.41e-02 | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| L3:F12849 | 7 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') |  words or phrases that include the word "double", or contain a hyphen | 6.88e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) |
| L3:F9770 | 7 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') |  technical and scientific writing about neuroscience and chemistry, possibly about calcium | 1.09e-02 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| L4:F5709 | 14 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') | astronomy terms | 1.42e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| L4:F3730 | 7 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') |  text relating to lithium-ion batteries | 3.63e-03 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) |
| L6:F11557 | 4 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') |  frequently used words such as conjunctions, pronouns, or discourse markers | 3.10e-02 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) |
| L0:F8659 | 8 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') | the word "foundation" in different contexts, including religious, legal, and abstract senses. | 2.92e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) |
| L4:F12126 | 2 | Late-layer discourse / contrast features (L4:F12126 'well/yeah agreement', L4:F4847 'conversational Q/A', L3:F14620 'well/and') |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | 1.23e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| L4:F4847 | 2 | Late-layer discourse / contrast features (L4:F12126 'well/yeah agreement', L4:F4847 'conversational Q/A', L3:F14620 'well/and') |  words or short phrases often used in conversation, and especially questions and answers | 1.16e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| L3:F14620 | 2 | Late-layer discourse / contrast features (L4:F12126 'well/yeah agreement', L4:F4847 'conversational Q/A', L3:F14620 'well/and') |  the word "well" and conjunctions like "and" | 7.70e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_t_haven | negation_contr_feature |
| emb_because | because_feature |
| emb_tournament | tournament_feature |
| emb_double_A | double_feature |
| emb_year_this | year_feature |
| emb_well_yeah | well_yeah_feature |
| emb_now_right | mid_negation_supernode |
| negation_contr_feature | mid_negation_supernode |
| because_feature | mid_negation_supernode |
| tournament_feature | mid_negation_supernode |
| double_feature | mid_negation_supernode |
| year_feature | mid_negation_supernode |
| well_yeah_feature | late_disagreement_supernode |
| mid_negation_supernode | late_disagreement_supernode |
| mid_negation_supernode | output |
| late_disagreement_supernode | output |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's classification score is driven primarily by low-layer (L0–L1) lexical features that fire on the **literal tokens** of the input — "haven't" (negation, via L0:F6236 with promoted tokens "not/Not/NOT"), "because" (L0:F16366), "well/yeah" discourse markers (L0:F8352, L4:F12126, L4:F4847), "tournament" (L0:F12862), and "double" / "A" / "now" / "year" — most of which are content-bearing sports-event and discourse words from the prompt. The strongest single direct effect on the probe is the **negation-token feature L0:F6236 at pos 20** (the apostrophe-t closing the word "haven't"), whose label and promoted tokens ("not/Not/NOT") confirm it is a dedicated detector of the English contraction negation construction. Supporting "because", "tournament", "well" and "year" features also fire at L0 and feed signal upward. The mid-layer cluster (L1:L3:L4) re-uses several of these same lexical detectors (L1:F177 "double", L3:F12849 "double/-hyphen", L3:F9770 science, L4:F5709 astronomy/'now', L4:F3730 batteries, L6:F11557 discourse markers, L0:F8659 "foundation"), and the late layer (L3:L4) consolidates them into a "conversational well/yeah agreement" detector (L4:F12126, L4:F4847, L3:F14620). The user's hypothesis is **partially correct but overstated**: the circuit IS heavy on the negation construction "haven't" (L0:F6236, the largest negative direct effect on the probe) — this is a *token-level spelling pattern* (apostrophe-t), not a semantic entity-recognizer, and it functions essentially as a heuristic "negation cue". However, the circuit is *not* purely a generic negation-detector: it also activates on the content nouns "tournament", "double", "A", "year", and the discourse markers "well" / "yeah" / "and", plus causal "because". So the mechanism is a mix of (a) a spurious surface-form "haven't" negation feature (which is exactly the "spurious feature" the user flagged) and (b) genuine lexical content tokens from the NCAA tournament sentence. The probe direction is therefore not driven by a clean semantic entity-recognizer (no "Louisville", "Sweet 16", or "NCAA" entity features appear) but by a bundle of low-level lexical detectors with a heavy weight on the negation construction — a classic spurious-correlation signature.

**Confidence:** 6

**Reasoning:** The circuit confirms the user's concern is well-founded on one specific feature: **L0:F6236** (the apostrophe-t of "haven't" at pos 20) is the single largest direct effect feeding the probe (-0.648) and is, by autointerp label and promoted tokens, a pure "isn't/doesn't contraction" detector that promotes "not/NOT/Not". This is precisely the kind of surface-form shortcut the user is worried about — a model classifying the sentence as "contradiction" partly because it sees the substring `n't`, not because it understands the meaning of "I haven't watched it this year because Louisville's out of it". The other large negative contributions come from lexical "well/yeah" discourse features (L4:F12126 -0.648, L1:F177 "double" -0.268, L0:F12862 "tournament" -0.236, L3:F9770 off-target "neuroscience" -0.315, L4:F5709 off-target "astronomy/now" -0.277, L4:F3730 off-target "batteries" -0.218) — and importantly several of these mid-layer features (9770 neuroscience, 5709 astronomy, 3730 batteries, 8659 "foundation") are **off-topic domain detectors** that happen to fire spuriously on these tokens. Embedding traces confirm the direct lineage: " well"→L4:F12126 (de=14.6), " yeah"→L4:F12126 (de=4.6), " haven'+'t"→L0:F6236 (de=17.9+16.6+12.1), " because"→L0:F16366 (de=40.8), " tournament"→L0:F12862 (de=20.6), " double"→L0:F8083 (de=19.6) and L1:F177 (de=24), " now"→L4:F5709 (de=40.8), " year"→L0:F5912 (de=18.6). Positively-pushing features (L3:F14620 "well/and" +0.231, L0:F3820 "the" +0.215, L0:F16366 "because" +0.293, L6:F11557 discourse markers +0.201, L0:F15682 "okay" +0.193) are generic function-word features, not entity features. The probe therefore relies on: (1) a real negation surface feature (L0:F6236 on "haven't" — this is the spurious cue the user identified), (2) a small set of sports-lexical features ("tournament", "double", "A", "year", "because"), and (3) several off-target domain features (neuroscience, astronomy, batteries, "foundation") that fired accidentally. There is no evidence of a "Louisville / Sweet 16 / NCAA" entity circuit — the model never recognizes the *entities* in the prompt. This is exactly the failure mode the user suspected: the probe uses a negation-construction cue (and a few other shallow lexical shortcuts) rather than the actual semantic content (sports-team identity, tournament identity, the claim "I haven't missed a single game" being contradicted by "I haven't watched it this year"). The user's intuition is correct: the contradiction classification is being driven by `haven't` (and to a lesser extent "tournament/double/well") rather than by understanding that the speaker contradicted themselves.
