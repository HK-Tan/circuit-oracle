# Elicitation Report

**Prompt:** Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L19:F8814 | 1 | Late pronoun aggregators @ pos 1 (His) |  various pronouns and names referring to people | 8.65e-02 | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| L18:F10315 | 1 | Late pronoun aggregators @ pos 1 (His) |  pronouns and possessive pronouns | 3.89e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| L18:F7400 | 1 | Late pronoun aggregators @ pos 1 (His) |  words related to coding and software/UI interfaces, with some bias toward non-English words | 1.58e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| L7:F14893 | 1 | Mid-layer pronoun/possessive features @ pos 1 (promote, +) |  pronouns or possessive pronouns | 8.85e-03 | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| L7:F14946 | 1 | Mid-layer pronoun/possessive features @ pos 1 (promote, +) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | 1.67e-02 | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| L6:F12990 | 1 | Mid-layer male-pronoun feature @ pos 1 (suppress, −) |  male pronouns and titles along with descriptors associated with men | 6.77e-02 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| L4:F4315 | 1 | Mid-layer male-pronoun feature @ pos 1 (suppress, −) |  mentions of "his" and other associated pronouns like he, him, or hers. | 2.62e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| L18:F14743 | 14 | Late 'He' pronoun feature @ pos 14 (suppress, −) | He | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| L18:F14743 | 37 | Late 'He' pronoun feature @ pos 14 (suppress, −) | He | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| L14:F14097 | 14 | Late 'He' pronoun feature @ pos 14 (suppress, −) |  occurrences of the word "he" | 1.97e-02 | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| L22:F12117 | 15 | Late 'He' pronoun feature @ pos 14 (suppress, −) |  references to actions that people can take or have taken. | 3.43e-02 | [view](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) |
| L19:F8186 | 14 | Late 'He' pronoun feature @ pos 14 (suppress, −) |  references to a person, especially third-person pronouns and possessive pronouns. | 2.62e-02 | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) |
| L0:F2994 | 1 | Early pronoun / person-reference features @ pos 1 | the pronoun "his" and the pronoun "he." | 7.33e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| L0:F2749 | 1 | Early pronoun / person-reference features @ pos 1 |  references to ownership or association with a person or group of people | 1.54e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2749) |
| L0:F1069 | 14 | Early pronoun / person-reference features @ pos 1 |  references to a male person, particularly when using the pronoun "He" or "His." | 7.80e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| L2:F5491 | 1 | Early pronoun / person-reference features @ pos 1 | references to God in the third person. | 8.24e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| L0:F1065 | 3 | Lexical periphery @ pos 1 (minor contributors) |  the word "interest", sometimes near the word "practicing" or "pattern" | 1.59e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1065) |
| L0:F6568 | 3 | Lexical periphery @ pos 1 (minor contributors) | the word "anyway" | 1.22e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6568) |
| L7:F16284 | 14 | Lexical periphery @ pos 1 (minor contributors) |  mentions of people's names and relationships | 9.56e-02 | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16284) |
| L0:F4564 | 2 | Profession-adjacent content words (research / interest / science) | the word "research." | 6.94e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| L2:F9740 | 3 | Profession-adjacent content words (research / interest / science) | the word "interest" and related words. | 5.63e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) |
| L0:F2827 | 8 | Profession-adjacent content words (research / interest / science) |  the word "science" | 9.90e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2827) |
| L0:F14201 | 3 | Profession-adjacent content words (research / interest / science) | words related to trade (business, finance, and health) | 1.86e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14201) |
| L0:F6051 | 13 | Profession-adjacent content words (research / interest / science) | periods, spaces, and the number 1 | 5.69e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_his | pos1_early_pronoun |
| emb_his | pos1_mid_pronoun_pos |
| emb_his | pos1_mid_pronoun_neg |
| emb_his | pos1_late |
| emb_he | pos14_he_feature |
| emb_research | profession_words |
| emb_science | profession_words |
| emb_interest | profession_words |
| pos1_early_pronoun | pos1_mid_pronoun_pos |
| pos1_early_pronoun | pos1_mid_pronoun_neg |
| pos1_mid_pronoun_pos | pos1_mid_pronoun_neg |
| pos1_mid_pronoun_pos | pos1_late |
| pos1_mid_pronoun_neg | pos1_mid_pronoun_pos |
| pos1_mid_pronoun_neg | pos1_late |
| pos1_late | logit |
| pos14_he_feature | logit |
| profession_words | logit |
| pos1_lexical_minor | logit |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's profession-classification score is driven almost entirely by masculine-gendered pronoun features ("His" at pos 1, "He" at pos 14/37) and not by genuine profession-indicating content words like "research," "science," or "interest," confirming the user's concern about spurious gender-marker features.

**Confidence:** 9

**Reasoning:**

The top direct-effect features on the probe direction are overwhelmingly pronoun/gender features. The largest single contributor is **L7:F14893** (pos 1, direct_effect +0.430, label "pronouns or possessive pronouns") followed by its sibling **L7:F14946** (pos 1, −0.426, "the possessive pronoun 'his'") and **L6:F12990** (pos 1, −0.295, "male pronouns and titles"). All three are traceable to the raw embedding of the token " His" (pos 1) — subagent 1 confirmed direct_effects of 23.5 (→F14893), 18.4 (→F14946), 4.9 (→F12990) from the "His" embedding, with a cascade of supporting pronoun detectors at L0:F2994, L4:F4315, L2:F5491, and L0:F2749 all firing on the same token. The same pattern repeats at position 14/37 where the " He" embedding (direct_effect 22.4) drives **L18:F14743** ("He" feature, activation ~30) at three positions and **L14:F14097** ("he" detector). These late-layer features all suppress the probe score (negative direct_effects of −0.252, −0.205, −0.094, etc.) — so the probe is being pushed by the *presence of masculine pronouns* rather than by profession semantics.

The early-layer profession-adjacent content features exist but contribute much less and are partially neutralized. **L0:F4564** ("the word 'research'", pos 2, frac_nonzero 0.007) is directly driven by the " research" embedding (28.1) and pushes the probe positively (+0.157). Similarly **L2:F9740** ("interest", pos 3, +0.133), **L0:F2827** ("science", pos 8, −0.122), and **L0:F1065** ("interest" at pos 3, +0.088). However, their magnitudes are small relative to the pronoun features, and the L18:L7400 code/UI feature (pos 1, −0.159) and other pronoun features at the same position swamp them. There is no "computer scientist" or "professor" or "researcher" entity-feature visible in the top 30 — the closest things to profession content are generic lexical features for "research"/"science"/"interest", which are just noun vocabulary, not profession identity.

In short, the circuit shows the probe classification of this text is being driven by the explicit "He" / "His" pronoun tokens cascading through a chain of gendered-pronoun detectors (pos 1: L0→L4/L6→L7→L18/L19; pos 14: L0:1069→L13:6622→L17:5889→L18:14743), with the profession-indicating content words "research" and "interest" contributing only a small positive push that is dominated by the pronoun features. The user's concern is validated: this is a textbook spurious-feature prediction, where the probe has learned a gender-marker shortcut (male pronouns ⇔ "computer scientist" profession) rather than a profession-concept representation.
