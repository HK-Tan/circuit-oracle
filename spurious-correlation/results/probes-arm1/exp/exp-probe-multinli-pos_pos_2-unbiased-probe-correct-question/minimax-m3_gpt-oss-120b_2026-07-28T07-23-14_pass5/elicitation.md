# Elicitation Report

**Prompt:** Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L0:F0 | 2 | Emb: ' well' (pos 2) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 1 | Emb: 'yeah' (pos 1) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 20 | Emb: 't' (pos 20, end of 'haven't') | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 18 | Emb: ' haven' (pos 18) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 19 | Emb: \"'\" (pos 19) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 25 | Emb: ' because' (pos 25) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 8 | Emb: ' tournament' (pos 8) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 6 | Emb: ' double' (pos 6) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F6236 | 20 | Layer-0 lexical/word-identity features (discourse markers & content words) | the letter "t" when it follows the word "isn'" or "doesn'" | 2.58e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| L0:F16366 | 25 | Layer-0 lexical/word-identity features (discourse markers & content words) |  the word "because" | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| L0:F8659 | 8 | Layer-0 lexical/word-identity features (discourse markers & content words) | the word "foundation" in different contexts, including religious, legal, and abstract senses. | 2.92e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) |
| L0:F8083 | 6 | Layer-0 lexical/word-identity features (discourse markers & content words) | the word "double" and surrounding words when numbers are also present | 1.55e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| L0:F12862 | 8 | Layer-0 lexical/word-identity features (discourse markers & content words) |  the word "tournament" and related words such as "winning", but not always | 1.53e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) |
| L0:F177 | 6 | Layer-0 lexical/word-identity features (discourse markers & content words) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/177) |
| L0:F3820 | 3 | Layer-0 lexical/word-identity features (discourse markers & content words) | the word "the" | 2.99e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| L0:F5112 | 1 | Layer-0 lexical/word-identity features (discourse markers & content words) |  the word "resolution", sometimes in the context of displaying images or patterns | 1.46e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) |
| L0:F8352 | 2 | Layer-0 lexical/word-identity features (discourse markers & content words) |  the word "well" | 3.50e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| L1:F177 | 6 | Layer 1-3 mid-level features (discourse/composition) |  the word "double" and words that begin with "multi" or "doubly" | 1.41e-02 | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| L1:F6696 | 2 | Layer 1-3 mid-level features (discourse/composition) | the word "pool" in different contexts, but it also shows some activation for words associated with water-related activities and computing processes. | 8.11e-03 | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6696) |
| L2:F1759 | 2 | Layer 1-3 mid-level features (discourse/composition) | occurrences of the word "know" with emphasis words or interjections nearby | 7.23e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) |
| L2:F7222 | 2 | Layer 1-3 mid-level features (discourse/composition) | the word "well" | 1.07e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7222) |
| L3:F4735 | 2 | Layer 1-3 mid-level features (discourse/composition) |  references to multi-well plates and software used in scientific experiments | 8.79e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4735) |
| L3:F9770 | 7 | Layer 1-3 mid-level features (discourse/composition) |  technical and scientific writing about neuroscience and chemistry, possibly about calcium | 1.09e-02 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| L3:F12849 | 7 | Layer 1-3 mid-level features (discourse/composition) |  words or phrases that include the word "double", or contain a hyphen | 6.88e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) |
| L3:F13677 | 2 | Layer 1-3 mid-level features (discourse/composition) | — | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13677) |
| L3:F15027 | 2 | Layer 1-3 mid-level features (discourse/composition) | — | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15027) |
| L3:F2663 | 2 | Layer 1-3 mid-level features (discourse/composition) | — | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2663) |
| L3:F14561 | 2 | Layer 1-3 mid-level features (discourse/composition) | — | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14561) |
| L3:F14620 | 2 | Layer 1-3 mid-level features (discourse/composition) |  the word "well" and conjunctions like "and" | 7.70e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) |
| L3:F9271 | 2 | Layer 1-3 mid-level features (discourse/composition) | — | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9271) |
| L3:F8423 | 2 | Layer 1-3 mid-level features (discourse/composition) | — | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8423) |
| L3:F5309 | 2 | Layer 1-3 mid-level features (discourse/composition) | — | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5309) |
| L4:F12126 | 2 | Layer 4 discourse/conversational features (key probe drivers) |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | 1.23e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| L4:F4847 | 2 | Layer 4 discourse/conversational features (key probe drivers) |  words or short phrases often used in conversation, and especially questions and answers | 1.16e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| L4:F5709 | 14 | Layer 4 discourse/conversational features (key probe drivers) | astronomy terms | 1.42e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| L4:F3730 | 7 | Layer 4 discourse/conversational features (key probe drivers) |  text relating to lithium-ion batteries | 3.63e-03 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) |
| L26:F0 | 0 | Probe classification direction (output) | — | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_t_pos20 | l0_lexical_conversation |
| emb_haven_pos18 | l0_lexical_conversation |
| emb_apostrophe_pos19 | l0_lexical_conversation |
| emb_because_pos25 | l0_lexical_conversation |
| emb_tournament_pos8 | l0_lexical_conversation |
| emb_double_pos6 | l0_lexical_conversation |
| emb_well_pos2 | l0_lexical_conversation |
| emb_yeah_pos1 | l0_lexical_conversation |
| l0_lexical_conversation | l1_l3_midfeatures |
| l1_l3_midfeatures | l4_discourse_features |
| l4_discourse_features | probe_output |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's "contradiction" classification is driven primarily by surface-level lexical/discourse signals — specifically discourse markers ("well", "yeah"), the contraction fragment "'t" (end of "haven't"), and the conjunction "because" — rather than by semantic content about the NCAA tournament, Louisville, or the Sweet 16.

**Confidence:** 7

**Reasoning:**

The attribution graph reveals that the probe's classification direction is dominated by shallow features:

1. **Strongest negative driver: L4:F12126 (pos 2, de=-0.65)** — labeled "expressions of agreement or acknowledgement, particularly 'well' and 'yeah'". This feature's top upstream inputs are the embeddings of " well" (de=14.6) and "yeah" (de=4.6), plus L0:F8352 ("the word 'well'") and L3:F4735 (multi-well plates — a false lexical match on the "well" token, not relevant). The circuit routes the *filler-word* "well" into the probe.

2. **Second strongest negative: L0:F6236 (pos 20, de=-0.46)** — labeled "the letter 't' when it follows the word 'isn'' or 'doesn''" (a contraction-ending detector). Its top inputs are embeddings for "t" (pos 20, de=17.9), " haven" (pos 18, de=16.6), and "'" (pos 19, de=12.1) — i.e., the "haven't" contraction, which the user explicitly flagged as a candidate spurious "negation word" signal. Promoted tokens confirm it pushes "not"/"Not"/"NOT".

3. **Strongest positive driver: L0:F16366 (pos 25, de=+0.29)** — labeled "the word 'because'", driven almost entirely by the "because" embedding (de=40.75). This is a conjunction/justification marker.

4. **L0:F8659 (pos 8, de=+0.29)** — labeled "the word 'foundation'" but firing on the "tournament" embedding (de=15.25); a generic word-identity feature.

5. **L4:F4847 (pos 2, de=+0.39)** — labeled "words/phrases often used in conversation, especially questions and answers" — another discourse-marker feature driven by " well" (de=8.06).

**Key finding confirming the user's concern:** The most negative-driving features (L4:F12126, L0:F6236) are **discourse/register markers** ("well", "yeah", "haven't") and a **contraction-ending 't'** that the LLM has learned to associate with negation. The "haven't" fragment is precisely the "negation word" signal the user flagged. The probe is not reading the semantic contradiction (Louisville being out, "I haven't missed a single game" — which is actually a *consistent* statement, not a contradiction). Instead, it keys on the **colloquial discourse register** (filler "well"/"yeah", contraction "haven't", casual "because") to fire its contradiction classification. The "tournament"/"double A" content words contribute only weakly (L0:F12862, F8083, F177 — "tournament"/"double" detectors) and are outvoted.

This validates the user's hypothesis: the probe relies on spurious lexical/discourse-marker features rather than understanding the actual semantic content of the prompt.
