# Elicitation Report

**Prompt:** Dataset: civil_comments-pos_pos_3 | Probe: biased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L0:F9026 | 6 | L0-F9026: 'jew' letter fragment (pos 6) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| L0:F9369 | 7 | L0-F9369: subtraction symbol ' -' (pos 7) |  subtraction symbols | 6.04e-02 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9369) |
| L0:F8736 | 3 | L0-F8736: 'hat' token (pos 3) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8736) |
| L2:F13158 | 6 | L2-F13158: 'race/ethnicity words' (pos 6, +0.29) |  words about race and ethnicity | 9.86e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| L2:F3983 | 3 | L2-F3983: 'hat' substring detector (pos 3, -0.20) | the word "hat" | 5.61e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3983) |
| L1:F1774 | 3 | L1-F1774: LaTeX text (pos 3, -0.20) |  text in a Latex document | 6.50e-03 | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1774) |
| L3:F12151 | 6 | L3-F12151: 'JE/JEW' letter pattern (pos 6) |  capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH", "WE", "SE" | 3.22e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) |
| L3:F13819 | 3 | L3-F13819: 'interconnectedness/together' (pos 3, +0.17) |  words and phrases about interconnectedness, self-similarity, and things holding together. | 1.52e-02 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13819) |
| L4:F2405 | 6 | L4-F2405: religious identity words (pos 6, +0.24) |  words related to religious identity/affiliation or spirituality including related holidays | 7.05e-03 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| L4:F14733 | 6 | L4-F14733: Israel-Palestine conflict (pos 6) |  content related to the Israel-Palestine conflict and possibly some related topics like NBA trades. | 9.58e-03 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) |
| L4:F8407 | 4 | L4-F8407: antagonists/fighting (pos 4, +0.16) |  words related to antagonists and fighting | 8.74e-03 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| L6:F648 | 6 | L6-F648: discrimination vs religious/ethnic groups (pos 6, +0.74) |  words related to discrimination against particular religious or ethnic groups | 1.61e-02 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) |
| L5:F7488 | 10 | L5-F7488: legal language / 'stain/stains' (pos 10) |  legal language, specifically terms related to evidence and accusations | 1.06e-02 | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7488) |
| L6:F1561 | 10 | L6-F1561: respect/status/pride words (pos 10) |  words related to respect, status, and pride, both positive and negative | 8.47e-03 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) |
| L8:F13875 | 10 | L8-F13875: negative sentiment, reputation/betrayal (pos 10, +0.23) | negative sentiment related to reputation and betrayal of trust. | 1.02e-02 | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) |
| L8:F13197 | 6 | L8-F13197: religion/faith words (pos 6, +0.14) |  words related to religion and faith | 1.35e-02 | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) |
| L8:F2483 | 3 | L8-F2483: slavery/prejudice/disability (pos 3, +0.17) |  discussions of slavery, prejudice, and disabilities | 2.26e-02 | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_jew | early_jew_letter |
| emb_jew | jewe_suffix_l3 |
| emb_jew | race_ethnicity_l2 |
| emb_liberal | race_ethnicity_l2 |
| emb_liberal | jewe_suffix_l3 |
| emb_liberal | religious_l4 |
| emb_hat | early_hat_token |
| emb_hat | hat_substring_l2 |
| emb_stain | legal_stain_l5 |
| emb_dash | early_subtraction |
| early_jew_letter | jewe_suffix_l3 |
| early_jew_letter | religious_l4 |
| early_jew_letter | race_ethnicity_l2 |
| jewe_suffix_l3 | discrim_l6 |
| jewe_suffix_l3 | religious_l4 |
| race_ethnicity_l2 | religious_l4 |
| race_ethnicity_l2 | discrim_l6 |
| religious_l4 | discrim_l6 |
| israel_palestine_l4 | discrim_l6 |
| discrim_l6 | output |
| religion_l8 | output |
| legal_stain_l5 | respect_status_l6 |
| respect_status_l6 | betrayal_l8 |
| betrayal_l8 | output |
| together_l3 | slavery_prej_l8 |
| slavery_prej_l8 | output |
| antagonist_l4 | output |
| latex_l1 | output |
| hat_substring_l2 | output |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's toxicity classification is driven almost entirely by the token `Jew` (pos 6) activating a stack of identity-group features — race/ethnicity (L2:F13158, +0.29), religious identity (L4:F2405, +0.24), Israel/Palestine context (L4:F14733), and culminating in the top driver L6:F648 "discrimination vs religious/ethnic groups" (+0.74) — with secondary contributions from `stain` (pos 9) feeding a "reputation/betrayal" path (L8:F13875, +0.23), while off-token subword artifacts (`hat`, ` -`, LaTeX patterns) and the suppression-leaning L3:Latex feature dilute rather than construct the score.

**Confidence:** 8

**Reasoning:** The circuit traces cleanly to embedding nodes. The dominant supernode `discrim_l6` (L6:F648, direct_effect=+0.74, frac_nonzero=0.016) is essentially a single-token detector for `Jew` — its #1 upstream node is the ` Jew` embedding at pos 6 with direct_effect=19.4, and the next strongest inputs are the identity-cluster letter/suffix feature L3:F12151 (also "JE/JEW" pattern, frac_nonzero=0.003) and L4:F14733 ("Israel-Palestine conflict", promoted_tokens include Palestinian/Palestine). L2:F13158 ("race/ethnicity words", +0.29) and L4:F2405 ("religious identity/affiliation", +0.24) at the same position reinforce the same `Jew` signal. The user is correct: the probe treats the *presence* of an identity-group token (`Jew`, `liberal`) as a near-sufficient signal of toxicity, rather than reading the pejorative verb "stain" or the negative framing "Self-hating … a stain on his brethren and his country." Notably, the "stain" path does exist (Emb ` stain` → L5:F7488 "legal language/stains" → L6:F1561 "respect/status/pride" → L8:F13875 "reputation/betrayal", total ~+0.23) but it is dwarfed by the identity-token path (~+1.3 in direct effects on the top feature alone). Off-target subword noise (L1:F1774 "LaTeX text", L2:F3983 "hat" substring) actually pushes the probe score *negatively* (-0.20, -0.20) because the token `hat` inside "hating" looks like the common English word "hat" / a LaTeX command `\hat` to low-level features. The mechanism is: **identity-token → identity-feature stack → probe**, with the actual insulting semantics ("stain", "Self-hating", "brethren") playing a secondary role. This confirms the user's concern that the probe latches on to *group-mention* features rather than toxic content.
