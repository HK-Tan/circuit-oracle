# Elicitation Report

**Prompt:** Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L4:F12126 | 2 | Mid-layer discourse/conversation detectors (pos 2) |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | 1.23e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| L4:F4847 | 2 | Mid-layer discourse/conversation detectors (pos 2) |  words or short phrases often used in conversation, and especially questions and answers | 1.16e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| L3:F14620 | 2 | Mid-layer discourse/conversation detectors (pos 2) |  the word "well" and conjunctions like "and" | 7.70e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) |
| L2:F1759 | 2 | Mid-layer discourse/conversation detectors (pos 2) | occurrences of the word "know" with emphasis words or interjections nearby | 7.23e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) |
| L2:F7222 | 2 | Mid-layer discourse/conversation detectors (pos 2) | the word "well" | 1.07e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7222) |
| L0:F8352 | 2 | Mid-layer discourse/conversation detectors (pos 2) |  the word "well" | 3.50e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| L0:F15972 | 1 | Mid-layer discourse/conversation detectors (pos 2) | the word "yeah" | 1.25e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) |
| L0:F6236 | 20 | Negation 't' detector (isn't/haven't) at pos 20 | the letter "t" when it follows the word "isn'" or "doesn'" | 2.58e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| L0:F16366 | 25 | Causal connector 'because' (pos 25) |  the word "because" | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| L0:F8083 | 6 | 'double' / number token detectors (pos 6) | the word "double" and surrounding words when numbers are also present | 1.55e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| L1:F177 | 6 | 'double' / number token detectors (pos 6) |  the word "double" and words that begin with "multi" or "doubly" | 1.41e-02 | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| L3:F12849 | 7 | 'double' / number token detectors (pos 6) |  words or phrases that include the word "double", or contain a hyphen | 6.88e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) |
| L3:F9770 | 7 | 'double' / number token detectors (pos 6) |  technical and scientific writing about neuroscience and chemistry, possibly about calcium | 1.09e-02 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| L2:F15133 | 7 | 'double' / number token detectors (pos 6) |  capital letters, especially those that are used as labels on figures, tables, experimental conditions, or chemical compounds | 1.64e-02 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15133) |
| L0:F12862 | 8 | 'tournament' / 'foundation' / 'resolution' lexical detectors (pos 8) |  the word "tournament" and related words such as "winning", but not always | 1.53e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) |
| L0:F8659 | 8 | 'tournament' / 'foundation' / 'resolution' lexical detectors (pos 8) | the word "foundation" in different contexts, including religious, legal, and abstract senses. | 2.92e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) |
| L0:F5112 | 1 | 'tournament' / 'foundation' / 'resolution' lexical detectors (pos 8) |  the word "resolution", sometimes in the context of displaying images or patterns | 1.46e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) |
| L6:F11557 | 4 | Filler 'uh' / discourse-marker at pos 4 |  frequently used words such as conjunctions, pronouns, or discourse markers | 3.10e-02 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) |
| L0:F15682 | 1 | Filler 'uh' / discourse-marker at pos 4 |  the word "okay" plus a few related expressions. | 1.31e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15682) |
| L0:F3820 | 3 | Filler 'uh' / discourse-marker at pos 4 | the word "the" | 2.99e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| L0:F4365 | 1 | Filler 'uh' / discourse-marker at pos 4 | the word "neither" and related negative terms. | 9.13e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4365) |
| L0:F5912 | 24 | Filler 'uh' / discourse-marker at pos 4 | "year" but also sometimes finds related words that include "day", "living", or "sold" | 2.71e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_well | mid_discourse |
| emb_yeah | mid_discourse |
| emb_double | double_feat |
| emb_tournament | tournament_feat |
| emb_t | negation_isnt |
| emb_haven | negation_isnt |
| emb_because | because_feat |
| emb_uh | uh_feat |
| emb_year | uh_feat |
| emb_the | uh_feat |
| mid_discourse | logit |
| negation_isnt | logit |
| because_feat | logit |
| double_feat | logit |
| tournament_feat | logit |
| uh_feat | logit |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's contradiction classification is driven almost entirely by surface-level lexical/orthographic features (discourse fillers, single-letter negation tokens, the word "because," the token "double," the noun "tournament") rather than by any deep semantic understanding of the claim being contradicted.

**Confidence:** 8

**Reasoning:**

The top-feature call returned a set of transcoder features whose direct effects on the probe are dominated by **shallow lexical detectors** that fire on individual tokens or subword fragments, not on meaning:

- **Negation-by-orthography (the user's main concern, confirmed):** L0:F6236 (frac_nonzero 0.0026, *very* specific) detects the letter "t" when it follows "isn'" or "doesn'". Its upstream driver is literally the **token embedding of "t" at pos 20 (direct_effect 17.9)** plus the embedding of " haven" at pos 18 (16.6) and the apostrophe "'" at pos 19 (12.1). This is a *purely orthographic* detector for the apostrophe-t contraction ending — the model is treating the surface form "haven't" as a contradiction cue, not interpreting what the speaker is actually negating. The "neither" feature L0:F4365 (pos 1, activation 11.9) and the "okay" feature L0:F15682 (pos 1) similarly add light contribution. This directly validates the user's concern: the probe treats *negation words* themselves as evidence of contradiction, irrespective of whether the content is semantically contradicting anything.

- **Discourse-marker / filler words being read as a contradiction signature:** The biggest single driver is L4:F12126 (direct_effect −0.65), labeled "expressions of agreement or acknowledgement, particularly 'well' and 'yeah'", traced back through the subagent to the embeddings of " well" (pos 2, direct_effect 14.6) and "yeah" (pos 1, direct_effect 4.6). Its partner L4:F4847 (+0.39, "words or short phrases often used in conversation, especially questions and answers") and L3:F14620 ("the word 'well' and conjunctions like 'and'") are also pure filler/conversation detectors. So conversational openers — "yeah well the uh" — are themselves being weighted as evidence of contradiction. The "uh" at pos 4 feeds L6:F11557 (conjunctions / discourse markers), again a generic surface pattern.

- **Topic-name lexical hits, not semantic content:** L0:F12862 ("the word 'tournament' and related words such as 'winning'", pos 8, +0.29), L0:F8659 ("the word 'foundation'", pos 8, +0.29), L0:F16366 ("the word 'because'", pos 25, +0.29), and L0:F8083 / L1:F177 ("the word 'double'", pos 6, −0.33) are all single-word lexical detectors. The "double" branch is particularly notable — it actually pushes *against* the contradiction direction (negative direct effects at L0:8083, L1:177, L3:12849), which is consistent with "NC double A tournament" being a benign proper-noun phrase that the model has no contradiction handle for.

- **Causal connector as contradiction signal:** L0:F16366 fires on the literal token "because" (embedding direct_effect 40.75 to the feature). The model is reading the *presence of a causal connective* in the second sentence ("because Louisville's out of it this year") as another contradiction cue, rather than the actual content of the cause.

In short, every late-layer feature driving the contradiction score decomposes into either (a) single-token lexical detectors (tournament, because, double, year, the, okay, neither) or (b) discourse/filler detectors (yeah, well, uh) or (c) an orthographic contraction-ending detector (apostrophe-t). The only feature that could plausibly encode *meaning* of the contradiction itself — the idea that "I haven't watched it because Louisville's out of it" negates the prior "I haven't missed a single game" — would need to integrate the semantic relation between clauses, but no such feature is in the top-20. The circuit is dominated by surface-form artifacts (negation orthography + filler words + topic nouns), which is exactly the spurious-feature failure mode the user flagged.
