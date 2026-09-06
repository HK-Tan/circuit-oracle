# Elicitation Report

**Prompt:** Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L0:F0 | 1 | Emb: His (pos 1) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 2 | Emb: research (pos 2) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 8 | Emb: science (pos 8) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F2994 | 1 | L0: F2994 'the pronoun his and the pronoun he' (pos 1) | the pronoun "his" and the pronoun "he." | 7.33e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| L0:F4564 | 2 | L0: F4564 'the word research' (pos 2) | the word "research." | 6.94e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| L0:F2827 | 8 | L0: F2827 'the word science' (pos 8) |  the word "science" | 9.90e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2827) |
| L0:F6051 | 13 | L0: F6051 'periods, spaces, and the number 1' (pos 13) | periods, spaces, and the number 1 | 5.69e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| L2:F9740 | 3 | L2: F9740 'the word interest and related words' (pos 3) | the word "interest" and related words. | 5.63e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) |
| L2:F5491 | 1 | L2: F5491 'references to God in the third person' (pos 1) | references to God in the third person. | 8.24e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| L4:F4315 | 1 | L4: F4315 'mentions of his and other associated pronouns' (pos 1) |  mentions of "his" and other associated pronouns like he, him, or hers. | 2.62e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| L6:F12990 | 1 | L6: F12990 'male pronouns and titles with male-associated descriptors' (pos 1) |  male pronouns and titles along with descriptors associated with men | 6.77e-02 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| L7:F14893 | 1 | L7: F14893 'pronouns or possessive pronouns' (pos 1) |  pronouns or possessive pronouns | 8.85e-03 | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| L7:F14946 | 1 | L7: F14946 'the possessive pronoun his (or similar pronouns like he and him)' (pos 1) | the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | 1.67e-02 | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| L18:F14743 | 14 | L18: F14743 'He' (pos 14) | He | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| L18:F7400 | 1 | L18: F7400 'coding/UI words; promoted tokens: himself/his' (pos 1) |  words related to coding and software/UI interfaces, with some bias toward non-English words | 1.58e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| L19:F8814 | 1 | L19: F8814 'various pronouns and names referring to people; promotes she/her' (pos 1) | various pronouns and names referring to people | 8.66e-02 | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_his | L0_his_late |
| emb_his | L4_his_surface |
| emb_his | L6_male_pronoun |
| emb_his | L7_his_core |
| emb_his | L19_gender_gate |
| emb_research | L0_research |
| emb_science | L0_science |
| L0_his_late | L7_possessive |
| L2_interest | logit |
| L2_god_his | logit |
| L4_his_surface | L6_male_pronoun |
| L4_his_surface | L7_possessive |
| L4_his_surface | L7_his_core |
| L4_his_surface | L19_gender_gate |
| L6_male_pronoun | L7_possessive |
| L6_male_pronoun | L7_his_core |
| L6_male_pronoun | L18_male_he |
| L6_male_pronoun | L19_gender_gate |
| L7_possessive | logit |
| L7_his_core | L19_gender_gate |
| L18_he_subject | logit |
| L18_male_he | L19_gender_gate |
| L19_gender_gate | logit |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's classification score is driven almost entirely by a cascade of male-gender/possessive-pronoun features originating from the token "His" at position 1, with negligible contribution from genuine profession indicators like "research", "science", or "visualization".

**Confidence:** 9

**Reasoning:**

The attribution circuit reveals a textbook case of a **spurious gender-marker circuit** rather than a profession-indicator circuit. Tracing the top 20 features driving the probe direction confirms this:

**The dominant positive pathway (pos 1, "His"):**
- **L7:F14893** (direct_effect = +0.43, frac_nonzero = 0.009) — labeled "pronouns or possessive pronouns," promotes tokens like `▁herself`, `▁she`, `▁elle`. This is the single strongest positive driver.
- **L19:F8814** (direct_effect = +0.24, frac_nonzero = 0.087) — labeled "various pronouns and names referring to people," strongly promotes feminine pronouns `▁herself`, `▁she`, `▁her`. Despite the feminine-promotion, this feature aggregates the entire gender-pronoun signal and is fed by a chain of male-pronoun detectors.
- **L0:F2994** (direct_effect = +0.23) — literally labeled "the pronoun 'his' and the pronoun 'he.'"

These all trace back to the **embedding node for "His" at position 1** (`Emb: His`), which contributes direct_effect = +9.3 directly to L19:F8814 and +23.5 to L4:F4315. The multi-hop path is: `Emb: His → L4:F4315 (his surface) → L6:F12990 (male pronouns) → L7:F14946 (his core) / L7:F14893 (possessive) → L19:F8814 (gender gate) → logit`. The L7:L19:gender gate supernode's promoted tokens (`herself`, `she`, `her`) indicate it is encoding a gender axis that happens to correlate with the male "His" input on this prompt.

**Negative pathway (also gender):**
- **L6:F12990** at pos 1 (direct_effect = −0.29) is labeled "male pronouns and titles along with descriptors associated with men." It acts as an inhibitory male-pronoun gate.
- **L18:F14743** at pos 14 and pos 37 (direct_effect ≈ −0.25, −0.21) is labeled simply "He" — this fires on the subject pronoun "He" later in the text and suppresses the probe score. The "He" at pos 14 (in "He received a BS...") is also a male-gender marker.
- **L18:F7400** (direct_effect = −0.16) has coding/UI top examples but its promoted tokens are `▁himself`, `▁his`, `▁seine` — again a male-pronoun signal.

**Genuine profession indicators are absent or weak:**
- L0:F2827 ("the word science"), L0:F4564 ("the word research"), and L2:F9740 ("the word interest") — all features whose top-activating examples clearly point to *computer science / research* content — appear in the circuit with **small direct effects** (≤+0.16). Crucially, none of them feed into a profession-classification supernode; they only weakly push the probe.
- L0:F14201 (direct_effect = −0.11), labeled "words related to trade (business, finance, and health)," is generic and unrelated to CS/academia.
- No features fire on "visualization," "computer graphics," "PhD," "university," or "laboratory" in the top-20 list.

**Conclusion:** The user's concern is validated. The probe direction is driven primarily by a chain of **gender-pronoun features** anchored at the word "His" (pos 1) and "He" (pos 14, 37). The positive contribution from the L7:L19:possessive/gender-pronoun features (L7:F14893 +0.43, L19:F8814 +0.24, L0:F2994 +0.23 ≈ +0.90 total) is partially cancelled by the negative male-pronoun gates (L6:F12990 −0.29, L18:F14743 ≈ −0.25, L18:F7400 −0.16 ≈ −0.70), but the net signal is still gender-driven. Genuine profession content features (research, science, interest) are present but contribute only weakly (≤+0.16) and do not form any profession-classification pathway. The circuit thus exhibits exactly the kind of **spurious correlation with male gender markers** that the user suspected — the probe is using pronoun-based gender cues as a shortcut rather than profession-specific semantic content.
