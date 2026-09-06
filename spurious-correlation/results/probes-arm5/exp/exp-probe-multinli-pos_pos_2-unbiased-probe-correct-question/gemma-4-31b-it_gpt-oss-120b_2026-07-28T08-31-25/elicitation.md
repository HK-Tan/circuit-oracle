# Elicitation Report

**Prompt:** Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L4:F12126 | 2 | Conversational Fillers ('yeah', 'well') |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | 1.23e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| L4:F4847 | 2 | Conversational Fillers ('yeah', 'well') |  words or short phrases often used in conversation, and especially questions and answers | 1.16e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| L0:F6236 | 20 | Negation/Contraction Signal ('n't') | the letter "t" when it follows the word "isn'" or "doesn'" | 2.58e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| L0:F16366 | 25 | Causal Marker ('because') |  the word "because" | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| L0:F8083 | 6 | Numeric/Double Context ('double') | the word "double" and surrounding words when numbers are also present | 1.55e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| filler_words | probe_logit |
| negation_signals | probe_logit |
| causal_marker | probe_logit |
| numeric_context | probe_logit |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's classification is driven by superficial linguistic markers—specifically conversational fillers, negation signals, and causal conjunctions—rather than a semantic understanding of the prompt's content.

**Confidence:** 9

**Reasoning:** 
The attribution analysis reveals that the probe's classification score is determined by several low-level, non-semantic features. 

1. **Conversational Fillers:** Features **L4:F12126** and **L4:F4847** (grouped in `filler_words`) respond to "yeah" and "well" at the start of the prompt. These features have a strong effect on the logit, but they encode conversational style rather than contradiction or any specific factual claim.
2. **Negation/Contraction Signals:** Feature **L0:F6236** (`negation_signals`) specifically detects the letter "t" following contractions like "isn't" or "doesn't" (detected at position 20, corresponding to "haven't"). This is a classic "spurious feature" where the probe relies on the presence of negation markers to predict a "contradiction" label without analyzing the actual meaning of the negated statement.
3. **Causal Markers:** Feature **L0:F16366** (`causal_marker`) detects the word "because". While "because" often introduces an explanation that could be contradictory, the feature itself is a simple lexical detector.
4. **Generic Context:** Feature **L0:F8083** (`numeric_context`) detects the word "double" in a numeric context (e.g., "NC double A"), which is entirely irrelevant to the semantic task of contradiction detection.

The signal flows directly from these early-layer (L0-L4) lexical detectors to the probe output. There is no evidence of higher-layer semantic integration or entity-specific reasoning. This confirms the user's concern: the probe is utilizing spurious "shortcut" features (negation words and filler phrases) to make its prediction.
