# Elicitation Report

**Prompt:** Dataset: civil_comments-pos_pos_3 | Probe: biased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L6:F648 | 6 | Probe driver: identity-token detector (L6:F648) | — | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) |
| L4:F14733 | 6 | Probe driver: identity-token detector (L6:F648) | — | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) |
| L4:F117 | 6 | Probe driver: identity-token detector (L6:F648) | — | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| L3:F12151 | 6 | Probe driver: identity-token detector (L6:F648) | — | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) |
| L2:F13158 | 6 | Probe driver: identity-token detector (L6:F648) | — | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| L4:F2405 | 6 | Probe driver: identity-token detector (L6:F648) | — | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| L8:F13875 | 10 | Slur/identity phrase detector (L8:F13875 at pos 10, "stain on his brethren/country") | — | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) |
| L6:F1561 | 10 | Slur/identity phrase detector (L8:F13875 at pos 10, "stain on his brethren/country") | — | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) |
| L5:F7488 | 10 | Slur/identity phrase detector (L8:F13875 at pos 10, "stain on his brethren/country") | — | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7488) |
| L0:F9026 | 6 | Early identity-token features (L0-L1) firing on "Jew" | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| L1:F15359 | 6 | Early identity-token features (L0-L1) firing on "Jew" | — | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15359) |
| L2:F8236 | 6 | Early identity-token features (L0-L1) firing on "Jew" | — | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8236) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_jew | early_jew_feat |
| emb_liberal | early_jew_feat |
| early_jew_feat | probe_driver |
| emb_jew | probe_driver |
| emb_liberal | probe_driver |
| probe_driver | output |
| emb_stain | slur_path |
| emb_on | slur_path |
| slur_path | output |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's toxicity classification is driven almost entirely by features that fire on the identity tokens "Jew" (pos 6) and "liberal" (pos 5) — and on the slur-adjacent phrase "stain on his" (pos 9-10) — rather than by features that encode the actual hate-speech *structure* (e.g., the verb "self-hating", the predicate "a stain on", the second-person framing).

**Confidence:** 8

**Reasoning:**

The circuit has two converging supernodes that feed the probe's output logit (L26 terminal):

1. **Probe driver supernode (L2–L6, pos 6)** — anchored by L6:F648 (direct_effect=0.74, activation=28.5), the single largest contributor to the probe score. Tracing upstream, L6:F648 is fed primarily by the raw embedding of "Jew" (direct_effect=19.4) and "liberal" (1.63), then by L3:F12151 (5.9) and L4:F2405 (2.95). Both mid-layer features trace back to the same identity-token embeddings: L3:F12151 has "Jew" at 11.0 and "liberal" at 3.38; L4:F2405 has "liberal" at 6.75 and "Jew" at 3.78. Further upstream, L0:F9026 at pos 6 receives a massive 31.4 direct_effect from the "Jew" embedding alone — this is essentially an "identity group label" detector.

2. **Slur-path supernode (L5–L8, pos 10)** — L8:F13875 (direct_effect=0.23) traces back to L6:F1561 (3.42), which in turn is fed by L5:F7488 (6.19) and the "stain" embedding (5.47). The phrase "stain on his" is the second cluster driving the probe.

Critically, the **predicate and syntactic structure** of the sentence — "Self-hating", "a stain on", "his brethren and his country" — do not appear as upstream drivers of the probe. None of the top features activate on "Self", "hating", or "his". The probe is therefore picking up on:
- The mere presence of a **minority identity noun** ("Jew") and a **political identity adjective** ("liberal"), and
- A **negatively-charged noun** ("stain") adjacent to "on his".

This confirms the user's concern: the probe relies on **identity-group token presence** (a "Jewish person mentioned" signal) and an isolated slur-adjacent word ("stain") rather than on compositional features that would encode the actual toxic structure (the compound noun "Self-hating [identity] Jew", the predicate "is a stain on his group and country", etc.). The model has not learned a structural notion of "slur against an identity group"; it has learned a bag-of-identity-words-and-negative-lexeme detector. The embedding "Jew" (pos 6) is the single largest causal contributor (31.4 → F9026, 19.4 → F648, 15.2 → F15359, 11.0 → F12151, 6.8 → F13158), making the probe classification highly sensitive to the mere occurrence of the identity token itself — a classic spurious-correlation / identity-mention shortcut.
