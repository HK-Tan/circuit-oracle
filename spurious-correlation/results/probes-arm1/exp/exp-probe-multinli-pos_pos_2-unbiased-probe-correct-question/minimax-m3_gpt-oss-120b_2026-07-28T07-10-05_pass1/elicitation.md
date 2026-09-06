# Elicitation Report

**Prompt:** Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L4:F12126 | 2 | Mid-layer discourse/filler features |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | 1.23e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| L4:F4847 | 2 | Mid-layer discourse/filler features |  words or short phrases often used in conversation, and especially questions and answers | 1.16e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| L3:F14620 | 2 | Mid-layer discourse/filler features |  the word "well" and conjunctions like "and" | 7.70e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) |
| L6:F11557 | 4 | Mid-layer discourse/filler features |  frequently used words such as conjunctions, pronouns, or discourse markers | 3.10e-02 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) |
| L3:F9770 | 7 | Mid-layer discourse/filler features |  technical and scientific writing about neuroscience and chemistry, possibly about calcium | 1.09e-02 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| L3:F12849 | 7 | Mid-layer discourse/filler features |  words or phrases that include the word "double", or contain a hyphen | 6.88e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) |
| L4:F3730 | 7 | Mid-layer discourse/filler features |  text relating to lithium-ion batteries | 3.63e-03 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) |
| L0:F15682 | 1 | Mid-layer discourse/filler features |  the word "okay" plus a few related expressions. | 1.31e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15682) |
| L0:F6236 | 20 | Negation: 't' after "haven'"/"isn'" (promotes 'not') | the letter "t" when it follows the word "isn'" or "doesn'" | 2.58e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| L0:F16366 | 25 | Word 'because' |  the word "because" | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| L0:F5912 | 24 | Word 'year' | "year" but also sometimes finds related words that include "day", "living", or "sold" | 2.71e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) |
| L4:F5709 | 14 | Word 'now' | astronomy terms | 1.42e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| L0:F8083 | 6 | Word 'double' (NCAA double-A) | the word "double" and surrounding words when numbers are also present | 1.55e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| L1:F177 | 6 | Word 'double' (NCAA double-A) |  the word "double" and words that begin with "multi" or "doubly" | 1.41e-02 | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| L0:F12862 | 8 | Word 'tournament' |  the word "tournament" and related words such as "winning", but not always | 1.53e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) |
| L0:F8659 | 8 | Word 'tournament' | the word "foundation" in different contexts, including religious, legal, and abstract senses. | 2.92e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) |
| L0:F8352 | 2 | Word 'well' (L0:F8352) |  the word "well" | 3.50e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| L0:F5112 | 1 | Spoken-style/negation features on 'yeah' |  the word "resolution", sometimes in the context of displaying images or patterns | 1.46e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) |
| L0:F4365 | 1 | Spoken-style/negation features on 'yeah' | the word "neither" and related negative terms. | 9.13e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4365) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_t_haven | l0_negation_haven_t |
| emb_because | l0_because |
| emb_year | l0_year |
| emb_now | l4_now |
| emb_double | l0_double_a |
| emb_tournament | l0_tournament |
| emb_well | l0_well_8352 |
| emb_well | l4_well_yeah_conv |
| emb_yeah | l0_yeah_5112 |
| l0_negation_haven_t | mid_negation_circuit |
| l0_because | mid_negation_circuit |
| l0_year | mid_negation_circuit |
| l4_now | mid_negation_circuit |
| l0_double_a | mid_negation_circuit |
| l0_tournament | mid_negation_circuit |
| l0_well_8352 | mid_negation_circuit |
| l0_yeah_5112 | mid_negation_circuit |
| l4_well_yeah_conv | mid_negation_circuit |
| mid_negation_circuit | probe_out |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's classification score is driven not by lexical/semantic content of the prompt but almost entirely by a cluster of low-layer "spoken-style / negation / discourse-filler" features that fire on common colloquial tokens (well, yeah, uh, the 't' in "haven't", because, year, now, double, tournament). The strongest positive contributors are "well" / "yeah" / filler features and discourse markers; the strongest negative contributors are also surface-level token detectors ("the", "okay", "t after haven'", "double"). The circuit is essentially a bag-of-discourse-markers circuit — not a content-aware contradiction detector.

**Confidence:** 7

**Reasoning:** The attribution graph on this probe direction is dominated by ~20 L0-L4 features that are all surface-form / discourse-marker detectors rather than semantic features that would distinguish factual contradiction from agreement. The top features and their semantics:

- **L0:F6236 at pos 20 ("t" of "haven't"), de = -0.648** — explicitly the contraction 't following "isn'"/"doesn'"/"haven'" with **promoted_tokens = "▁not, ▁Not, ▁NOT, not, Not, ▁bukan, ▁nicht, ▁tidak, ▁niet, ▁ikke"** (multi-lingual "not"). This is a textbook negation surface feature.
- **L0:F5112 at pos 1 ("yeah"), de = -0.206** — labeled "the word 'resolution'" but fires on "yeah" here.
- **L0:F15682 at pos 1 ("yeah"), de = 0.193** — the word "okay" plus related expressions; generic spoken-affirmation detector.
- **L0:F4365 at pos 1 ("yeah"), de = 0.198** — "the word 'neither' and related negative terms" — but fires on "yeah" pos, so it is acting as a generic short/negative-text feature.
- **L0:F8083 at pos 6 ("double"), de = -0.332** — "the word 'double' and surrounding words when numbers are also present"; pure lexical.
- **L1:F177 at pos 6 ("double"), de = -0.268** — "the word 'double' and words that begin with 'multi' or 'doubly'"; pure lexical.
- **L0:F12862 at pos 8 ("tournament"), de = -0.236** — "the word 'tournament' and related words such as 'winning'"; pure lexical.
- **L0:F8659 at pos 8 ("tournament"), de = 0.285** — labeled "foundation" but fires on "tournament" (multi-word co-occurrence feature).
- **L0:F16366 at pos 25 ("because"), de = 0.293** — "the word 'because'"; pure lexical.
- **L0:F5912 at pos 24 ("year"), de = -0.197** — "the word 'year'"; pure lexical.
- **L3:F9770 at pos 7 ("A"), de = -0.315** — generic scientific/neurochemistry text feature (spurious context match).
- **L3:F12849 at pos 7 ("A"), de = -0.230** — "words that include 'double', or contain a hyphen".
- **L3:F14620 at pos 2 ("well"), de = 0.230** — "the word 'well' and conjunctions like 'and'".
- **L4:F5709 at pos 14 ("now"), de = -0.277** — "astronomy terms" but fires on "now" (suppressed token is "now").
- **L4:F12126 at pos 2 ("well"), de = -0.648** — "expressions of agreement or acknowledgement, particularly 'well' and 'yeah'" (the biggest single driver in absolute terms).
- **L4:F4847 at pos 2 ("well"), de = 0.389** — "words or short phrases often used in conversation, and especially questions and answers".
- **L6:F11557 at pos 4 ("uh"), de = 0.201** — "frequently used words such as conjunctions, pronouns, or discourse markers".
- **L0:F3820 at pos 3 ("the"), de = 0.215** — "the word 'the'"; pure function word.

I traced these upstream and confirmed each bottoms out at a single token-embedding node: Emb "well" (pos 2) → L0:F8352/L4:F4847/L4:F12126; Emb "yeah" (pos 1) → L0:F5112/F15682/F4365; Emb "t" (pos 20) → L0:F6236; Emb "because" (pos 25) → L0:F16366; Emb "year" (pos 24) → L0:F5912; Emb "now" (pos 14) → L4:F5709; Emb "double" (pos 6) → L0:F8083/L1:F177; Emb "tournament" (pos 8) → L0:F12862/F8659. The user-concern hypothesis is supported:

1. **The strongest single contributor (L4:F12126, |de|=0.648) is literally the "well / yeah" acknowledgment detector** — a filler/pragmatic feature, not a semantic feature.
2. **L0:F6236 is an explicit negation surface feature** ("t" after "haven'", promoted tokens are "not", "Not", "NOT" in many languages). It fires on the 't in "haven't" and contributes -0.648 — the biggest push *against* the probe direction. The prompt's two "haven't" / "isn't" constructions are being read as a generic "negation signal".
3. **The bulk of remaining features are word-identity detectors** ("because", "year", "now", "double", "tournament", "well", "yeah", "uh", "the", "okay") — none of them encode whether the content contradicts a premise. They encode which content-words are present, with no role for the contrastive structure (e.g. "I haven't watched … because Louisville's out").
4. **The "because" feature (L0:F16366, de = +0.293) promotes no semantic content** — its decoder projects onto punctuation/letters because it is a single-word identity feature. It is the connective marker the model "latches onto" not because it understands the causal structure but because "because" is a high-information discourse token in this dataset.
5. **Source-influence analysis** (source_positions = the "because" and "year" / "t" tokens) returned S_pct_of_total = -3.06% and S_over_R = -0.54, indicating these key content tokens are NOT strong drivers of the probe direction; the signal is diffuse and dominated by filler positions.

The circuit therefore matches the user's concern: the probe is reading the input through a **surface-form / discourse-marker lens** — counting "well", "yeah", "uh", "haven't", "because", "the", and topic words (tournament, double, year) — rather than through a semantic contradiction circuit. There is no entity-recognition or event-comparison feature anywhere in the graph; the most semantically loaded features in the attribution (L0:F6236 negation, L4:F12126 well/yeah acknowledgment) are pragmatic/syntactic markers, not world-knowledge or compositional features. The "contradiction" classification appears to be driven by the **density of spoken-style discourse markers and the presence of a negation surface form**, exactly the kind of spurious pattern the user worried about.
