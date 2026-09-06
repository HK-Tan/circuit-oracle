# Elicitation Report

**Prompt:** Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

## One-shot analysis

The top features driving the probe are dominated by surface-level conversational and discourse markers ('well', 'yeah', 'the', 'okay', 'anyway', conjunctions) and low-level lexical features (letters, the word 'double', 'tournament', 'year', 'season'). There is almost no semantic content about the actual claim (NCAA tournament, Sweet 16, watching games). Notably, L0:F4365 ('neither' and negative terms) and L0:F6236 ('t' after 'isn''/'doesn'') are negation-related artifacts, though the input text does contain 'haven't' and 'I haven't missed'. The most content-relevant feature is L0:F12862 ('tournament'), but overall the circuit is driven by stylistic/discourse markers and spurious lexical cues rather than the actual semantic content about the sporting event claim.

**Verdict:** spurious

**Spurious features:** L4:F12126, L0:F6236, L0:F4365, L0:F8352, L3:F14620, L2:F15282, L0:F15682, L0:F3820, L6:F11557, L4:F4847
**Causal features:** L0:F12862, L1:F13255, L0:F8083, L1:F177

