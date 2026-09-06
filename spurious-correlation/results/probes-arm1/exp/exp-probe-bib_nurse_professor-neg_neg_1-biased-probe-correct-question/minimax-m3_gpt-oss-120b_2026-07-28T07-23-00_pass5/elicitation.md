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
| L0:F0 | 3 | Emb: interests (pos 3) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 8 | Emb: scientific (pos 8) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 14 | Emb: He (pos 14) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 37 | Emb: He (pos 37) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 13 | Emb: . (pos 13) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F4564 | 2 | Lexical: research (L0:F4564) | the word "research." | 6.94e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| L0:F2827 | 8 | Lexical: science (L0:F2827) |  the word "science" | 9.90e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2827) |
| L2:F9740 | 3 | Lexical: interest/interest(s) (L2:F9740) | the word "interest" and related words. | 5.63e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9740) |
| L0:F6051 | 13 | Lexical: period/spacing (L0:F6051) | periods, spaces, and the number 1 | 5.69e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| L0:F2994 | 1 | Low-level male-pronoun features (L0:L2) | the pronoun "his" and the pronoun "he." | 7.33e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| L2:F5491 | 1 | Low-level male-pronoun features (L0:L2) | references to God in the third person. | 8.24e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| L0:F1069 | 1 | Low-level male-pronoun features (L0:L2) |  references to a male person, particularly when using the pronoun "He" or "His." | 7.80e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| L0:F1069 | 14 | Low-level male-pronoun features (L0:L2) |  references to a male person, particularly when using the pronoun "He" or "His." | 7.80e-03 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| L4:F4315 | 1 | Mid-layer pronoun/man features (L4:L6) |  mentions of "his" and other associated pronouns like he, him, or hers. | 2.62e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| L6:F12990 | 1 | Mid-layer pronoun/man features (L4:L6) |  male pronouns and titles along with descriptors associated with men | 6.77e-02 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| L7:F14893 | 1 | Late pronoun features pushing AGAINST probe (L7) |  pronouns or possessive pronouns | 8.85e-03 | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| L7:F14946 | 1 | Late pronoun features pushing AGAINST probe (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | 1.67e-02 | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| L14:F14097 | 14 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  occurrences of the word "he" | 1.97e-02 | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| L18:F14743 | 14 | Late biography/pronoun features (L14:L19) pushing AGAINST probe | He | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| L18:F14743 | 37 | Late biography/pronoun features (L14:L19) pushing AGAINST probe | He | 1.81e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| L18:F7400 | 1 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  words related to coding and software/UI interfaces, with some bias toward non-English words | 1.58e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| L18:F10315 | 1 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  pronouns and possessive pronouns | 3.89e-02 | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| L19:F8814 | 1 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  various pronouns and names referring to people | 8.65e-02 | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| L19:F8186 | 14 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  references to a person, especially third-person pronouns and possessive pronouns. | 2.62e-02 | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) |
| L22:F12117 | 15 | Late biography/pronoun features (L14:L19) pushing AGAINST probe |  references to actions that people can take or have taken. | 3.43e-02 | [view](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) |
| L26:F0 | 0 | Probe direction (output) | — | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_His | gender_features_low |
| emb_research | L0_lex_research |
| emb_scientific | L0_lex_science |
| emb_interests | L0_lex_interest |
| emb_period | L0_lex_period |
| emb_He_pos14 | gender_features_low |
| emb_He_pos37 | gender_features_low |
| gender_features_low | mid_gender_mid |
| mid_gender_mid | late_pronoun_neg |
| late_pronoun_neg | late_pronoun_neg_bio |
| L0_lex_research | logit |
| L0_lex_interest | logit |
| L0_lex_science | logit |
| L0_lex_period | logit |
| late_pronoun_neg | logit |
| late_pronoun_neg_bio | logit |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's classification score is driven almost entirely by male-gendered pronoun/male-biographical features, with weak positive contributions from the lexical "research" and "science" tokens; the user's concern is well-founded — gender markers dominate the circuit while genuine profession/field indicators are a minor side-channel.

**Confidence:** 8

**Reasoning:**

Looking at the top direct effects on the probe direction, the most influential features are all gendered language detectors:

- **L7:F14893** (label: "pronouns or possessive pronouns", frac_nonzero=0.009) has direct_effect = +0.430 — fires on "his/his/her" with promoted tokens = `▁herself, ▁elle, ▁she` (feminine-promoting). Upstream: the **Emb: "His" (pos 1)** is its biggest driver (direct_effect=23.5), confirming this is a male-possessive circuit originating from the very first content token.
- **L7:F14946** (label: "the possessive pronoun 'his'", frac_nonzero=0.017) direct_effect = −0.426 — anti-his detection, again tracing back to **Emb: "His"** (de=18.4) and Emb:"\<bos\>" (de=3.8).
- **L6:F12990** (label: "male pronouns and titles along with descriptors associated with men", frac_nonzero=0.068) direct_effect = −0.295 — fires on "his, man, husband, himself" with suppressed_tokens = `▁herself, ▁she, ▁ihrem`. Its biggest upstream is again **Emb: "His"** (de=4.9).
- **L18:F14743** (label: "He", frac_nonzero=0.018) fires at TWO positions (pos 14 and pos 37) with direct_effects of −0.252 and −0.205. Upstream it is fed by the **Emb: " He"** at pos 14 (de=22.4) and pos 37 (de=24.0), plus L17:F5889 ("references to people with pronouns and possessive pronouns") and L13:F6622 ("pronouns"). This is a textbook generic-pronoun stack, not a profession circuit.
- **L18:F7400** and **L18:F10315** (both labeled "pronouns and possessive pronouns", frac_nonzero ≈ 0.016/0.039) and **L19:F8814** ("various pronouns and names referring to people", frac_nonzero=0.087) and **L19:F8186** ("references to a person, especially third-person pronouns", frac_nonzero=0.026) and **L22:F12117** ("references to actions that people can take or have taken", frac_nonzero=0.034) all chain back to **Emb: "His"** (de=9.3 for F8814) and **Emb: "He"** at pos 14/37. Even the L17:F3683 "biographies" feature (which does fire on biographical text like "Jianlin Cheng…") sits in the pronoun-gendered circuit; its biggest upstream is also **Emb: " He"** (de=14.5) and L18:F14743.
- **L0:F1069** ("references to a male person, particularly when using the pronoun 'He' or 'His'", frac_nonzero=0.008) is the lowest-layer male-pronoun detector, feeding forward into all the above features.

The only features driving the probe that are NOT pure pronoun/male markers are the lexical topic words:

- **L0:F4564** ("the word 'research'", frac_nonzero=0.007) direct_effect = +0.157, driven by **Emb: " research"** (pos 2, de=28.1) — a genuine content signal.
- **L0:F2827** ("the word 'science'", frac_nonzero=0.010) direct_effect = −0.122, driven by **Emb: " scientific"** (pos 8, de=22.1).
- **L2:F9740** ("the word 'interest' and related words", frac_nonzero=0.006) direct_effect = +0.133, driven by **Emb: " interests"** (pos 3, de=27.0).
- **L0:F6051** ("periods, spaces, and the number 1", frac_nonzero=0.057) direct_effect = −0.125, driven by **Emb: "."** (pos 13, de=46.3) — a syntactic-formatting feature that is anti-correlated with biographies.

The sum of absolute direct effects on the probe direction is overwhelmingly carried by gendered features. The top-2 contributions alone (L7:F14893 +0.43 and L7:F14946 −0.43) are pure pronoun features; the top-10 contains only one topic-word feature (L0:F4564 "research"). Crucially, the "He" detector (L18:F14743) at both pos 14 and pos 37 pushes AGAINST the probe direction (negative direct_effect), meaning the pronoun circuit is partially cancelling itself rather than providing an unambiguous profession signal.

The two biography-related features that appear (L17:F3683 "biographies" and L18:F9023 "personal names and associated titles") are themselves downstream of male-pronoun features (L18:F14743, L0:F1069) and are tied to the "He" tokens, not to any profession-specific vocabulary. There is no feature in the top-25 whose label is "professor", "academic", "scientist", or any field/occupation indicator; the only "title/role" feature (L18:F9023) fires on bare personal names rather than on "Dr./PhD/Professor" tokens, and even so it sits downstream of the pronoun stack.

**Bottom line on the user's concern:** The concern is strongly supported by the circuit. The dominant signal flow is Emb("His"/"He") → L0:L2 male-pronoun features → L4:L6 mid-pronoun/man features → L7 pronoun features (largest individual contributors, ±0.43) → L14:L22 biography/pronoun features. The genuine profession/field signal (L0:F4564 "research", L0:F2827 "science", L2:F9740 "interest") is present but constitutes a much smaller portion of the total direct effect and is partially cancelled by an anti-pronoun push in the same direction. The probe is largely classifying along a male-gendered biographical-text axis rather than along a computer-science/researcher axis.
