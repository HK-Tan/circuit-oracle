# Elicitation Report

**Prompt:** Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L0:F0 | 2 | Emb: well (pos 2) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 1 | Emb: yeah (pos 1) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 18 | Emb: haven't (pos 18-20) - negation | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 19 | Emb: haven't (pos 18-20) - negation | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 20 | Emb: haven't (pos 18-20) - negation | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 5 | Emb: NC double (pos 5-6) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 6 | Emb: NC double (pos 5-6) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 23 | Emb: this year (pos 23-24) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 24 | Emb: this year (pos 23-24) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 25 | Emb: because (pos 25) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F6236 | 20 | Negation-form features (haven't / t after isn't/doesn't) | the letter "t" when it follows the word "isn'" or "doesn'" | 2.58e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| L0:F8352 | 2 | Negation-form features (haven't / t after isn't/doesn't) |  the word "well" | 3.50e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| L0:F5112 | 1 | Discourse markers: yeah/well/uh |  the word "resolution", sometimes in the context of displaying images or patterns | 1.46e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) |
| L0:F15612 | 1 | Discourse markers: yeah/well/uh | mentions of dollar amounts | 1.04e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15612) |
| L0:F3820 | 3 | Discourse markers: yeah/well/uh | the word "the" | 2.99e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| L0:F15682 | 1 | Discourse markers: yeah/well/uh |  the word "okay" plus a few related expressions. | 1.31e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15682) |
| L0:F8083 | 6 | Content words: double/tournament/because/year/foundation | the word "double" and surrounding words when numbers are also present | 1.55e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| L0:F16366 | 25 | Content words: double/tournament/because/year/foundation |  the word "because" | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| L0:F12862 | 8 | Content words: double/tournament/because/year/foundation |  the word "tournament" and related words such as "winning", but not always | 1.53e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) |
| L0:F5912 | 24 | Content words: double/tournament/because/year/foundation | "year" but also sometimes finds related words that include "day", "living", or "sold" | 2.71e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) |
| L0:F8659 | 8 | Content words: double/tournament/because/year/foundation | the word "foundation" in different contexts, including religious, legal, and abstract senses. | 2.92e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) |
| L0:F4365 | 1 | Content words: double/tournament/because/year/foundation | the word "neither" and related negative terms. | 9.13e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4365) |
| L1:F177 | 6 | Double / hyphen features (L1-L3) |  the word "double" and words that begin with "multi" or "doubly" | 1.41e-02 | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| L1:F13255 | 8 | Double / hyphen features (L1-L3) |  the word "season" and words associated with it | 5.28e-03 | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13255) |
| L1:F7762 | 8 | Double / hyphen features (L1-L3) |  the word "inspection" | 1.03e-02 | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7762) |
| L2:F5201 | 8 | Double / hyphen features (L1-L3) | awards and accomplishments in the context of sports | 9.93e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) |
| L2:F2629 | 1 | Double / hyphen features (L1-L3) |  the word "doubt" | 4.97e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2629) |
| L2:F15282 | 1 | Double / hyphen features (L1-L3) | the words "anyway" and "yeah" | 2.40e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15282) |
| L3:F9770 | 7 | Double / hyphen mid-layer features (L3-L4) |  technical and scientific writing about neuroscience and chemistry, possibly about calcium | 1.09e-02 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| L3:F12849 | 7 | Double / hyphen mid-layer features (L3-L4) |  words or phrases that include the word "double", or contain a hyphen | 6.88e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) |
| L3:F14620 | 2 | Double / hyphen mid-layer features (L3-L4) |  the word "well" and conjunctions like "and" | 7.70e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) |
| L3:F9247 | 7 | Double / hyphen mid-layer features (L3-L4) |  hyphenated words related to building and tools | 1.05e-02 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9247) |
| L4:F12126 | 2 | Discourse/well features (L4) |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | 1.23e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| L4:F4847 | 2 | Discourse/well features (L4) |  words or short phrases often used in conversation, and especially questions and answers | 1.16e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| L4:F5709 | 14 | Discourse/well features (L4) | astronomy terms | 1.42e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| L4:F3730 | 7 | Discourse/well features (L4) |  text relating to lithium-ion batteries | 3.63e-03 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) |
| L4:F6072 | 14 | Discourse/well features (L4) |  the word "now" followed by a verb | 6.05e-03 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) |
| L6:F11557 | 4 | Late-layer function-word aggregators (L6) |  frequently used words such as conjunctions, pronouns, or discourse markers | 3.10e-02 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) |
| L6:F12415 | 4 | Late-layer function-word aggregators (L6) |  expressions of mild emotion or acknowledgement, particularly "umm" and similar sounds, and also words implying difficulty or problems | 2.24e-02 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12415) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_havent | negation_tokens |
| emb_well | negation_tokens |
| emb_yeah | discourse_markers |
| emb_double | content_words |
| emb_year | content_words |
| emb_because | content_words |
| negation_tokens | discourse_high |
| discourse_markers | discourse_high |
| content_words | double_features |
| double_features | mid_double_features |
| mid_double_features | discourse_high |
| discourse_high | late_features |
| late_features | output |
| discourse_high | output |
| content_words | output |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's classification is driven by a sparse, early-layer circuit dominated by negation-form tokens (haven't, isn't), discourse markers (yeah, well, uh), and incidental surface tokens (NC, double, year) — not by any deep semantic representation of the prompt's actual content about NCAA basketball / Louisville.

**Confidence:** 6

**Reasoning:** The circuit is heavily concentrated in layers 0–4 with a few L6 aggregators, and the strongest direct-effect features are functional/surface rather than semantic. The top driver is **L4:F12126** at pos 2 (the "well" discourse marker, frac_nonzero 0.012, effect −0.65) and **L0:F6236** at pos 20 (the literal "t" completing "haven't" in "haven't missed a single game", frac_nonzero 0.003, effect −0.46) — both classic negation/discourse surface features. Their upstream traces confirm this: L0:F6236 is driven by the embeddings of `t` (pos 20), `haven` (pos 18), `'` (pos 19) — i.e. the bare surface form of the contraction. The strongly positive feature **L4:F4847** (pos 2, +0.39) and **L3:F14620** (pos 2, +0.23) both fire on "well"/discourse-acknowledgement context, and their upstream feeds are the "well" and "yeah" embeddings. Even the content-word features (**L0:F8083** "double" with effect −0.33; **L0:F12862** "tournament"; **L0:F5912** "year"; **L0:F16366** "because") are pure lexical lookups for the literal token strings "double", "tournament", "year", "because" — they do not aggregate to a sports/NCAATournament semantic concept, but instead propagate into the **L1–L3 "double" / hyphen feature cluster** (F177 "double/multi", F12849 "double/hyphen", F9770 hyphen-related, F9247 hyphenated) which then feeds the L4 discourse features and ultimately the output. The late-layer features are all generic function-word / connective aggregators (L6:F11557 "frequently used words such as conjunctions, pronouns, or discourse markers", L6:F12415 "umm / words implying difficulty"). 

This is exactly the failure mode the user flagged: the strongest single contributor (L0:F6236, the "t"-of-"haven't" feature) is a textbook **negation-surface feature**, and its negative direct_effect on the probe direction means the presence of "haven't" pushes the probe toward contradiction. The discourse markers (well, yeah, uh) and the literal "NC double" tokens contribute the bulk of the remaining signal. None of the traced features encode a genuine contradiction semantics — they encode **lexical surface features** for negation/contracted-"not", discourse markers, and content nouns — which is why this probe would be fooled by paraphrases that preserve the surface negation while flipping the meaning, or by negated statements that are not contradictions. The user's concern is well-supported by the circuit.
