# Elicitation Report

**Prompt:** Dataset: civil_comments-pos_pos_3 | Probe: biased | Method: correct

**Baseline (no intervention):**

> 

**Total interventions tried:** 0

## Pinned Features

Features pinned by the Oracle in BUILD, with their autointerp labels and the Oracle's proposed role (supernode label). Click the Neuronpedia link to inspect each feature.

| Feature | Pos | Supernode role | Autointerp label | frac_nonzero | Neuronpedia |
|---------|-----|----------------|------------------|--------------|-------------|
| L0:F0 | 6 | Emb: Jew (pos 6) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 5 | Emb: liberal (pos 5) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 3 | Emb: hat (pos 3) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 1 | Emb: Self (pos 1) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 9 | Emb: stain (pos 9) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F0 | 7 | Emb: - (pos 7) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| L0:F9026 | 6 | L0:F9026 (Jew-token amplifier, pos 6) | — | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| L1:F14516 | 3 | L1:F14516 (hat-token, pos 3) | — | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14516) |
| L2:F13158 | 6 | L2:F13158 (race/ethnicity words, pos 6) |  words about race and ethnicity | 9.86e-03 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| L2:F3588 | 5 | L2:F3588 (political terms, pos 5) |  terms related to politics and political parties | 1.39e-02 | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3588) |
| L3:F592 | 3 | L3:F592 (love/hate words, pos 3,4) | words related to love, affection, and hate, including foreign language | 4.40e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| L3:F592 | 4 | L3:F592 (love/hate words, pos 3,4) | words related to love, affection, and hate, including foreign language | 4.40e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| L3:F12151 | 6 | L3:F12151 (capitalized ISH/EM/WE patterns incl. Jew, pos 6) |  capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH", "WE", "SE" | 3.22e-03 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) |
| L3:F13819 | 3 | L3:F13819 (interconnectedness/brethren, pos 3) |  words and phrases about interconnectedness, self-similarity, and things holding together. | 1.52e-02 | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13819) |
| L4:F2405 | 6 | L4:F2405 (religious identity words, pos 6) |  words related to religious identity/affiliation or spirituality including related holidays | 7.05e-03 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| L4:F117 | 6 | L4:F117 (race/racism, Black focus, pos 6) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | 1.20e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| L4:F117 | 3 | L4:F117 (race/racism, Black focus, pos 6) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | 1.20e-02 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| L4:F14733 | 6 | L4:F14733 (Israel-Palestine content, pos 6) |  content related to the Israel-Palestine conflict and possibly some related topics like NBA trades. | 9.58e-03 | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) |
| L6:F648 | 6 | L6:F648 (religious/ethnic discrimination words, pos 3,6) |  words related to discrimination against particular religious or ethnic groups | 1.61e-02 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) |
| L6:F648 | 3 | L6:F648 (religious/ethnic discrimination words, pos 3,6) |  words related to discrimination against particular religious or ethnic groups | 1.61e-02 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) |
| L6:F1561 | 10 | L6:F1561 (respect/dignity/pride, pos 10) |  words related to respect, status, and pride, both positive and negative | 8.47e-03 | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) |
| L8:F13875 | 10 | L8:F13875 (negative sentiment / reputation-betrayal, pos 10) | negative sentiment related to reputation and betrayal of trust. | 1.02e-02 | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) |
| L8:F13197 | 6 | L8:F13197 (religion/faith, pos 6) |  words related to religion and faith | 1.35e-02 | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) |
| L8:F2483 | 3 | L8:F2483 (slavery/prejudice/disability discourse, pos 3) |  discussions of slavery, prejudice, and disabilities | 2.26e-02 | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) |
| L26:F0 | 6 | Probe score (toxicity direction) | — | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Pinned Connectivity

Edges among pinned features as recorded in BUILD. Direction: `from` → `to` (upstream → downstream). Topology only — edges denote a positive direct_effect connection between the two supernodes during tracing.

| From | To |
|------|----|
| emb_jew | l0_jew_strong |
| emb_jew | l2_race_ethnicity |
| emb_jew | l3_jew_caps |
| emb_jew | l4_religion |
| emb_jew | l4_race |
| emb_jew | l4_isrpal |
| emb_jew | l6_discrim |
| emb_jew | l8_religion |
| emb_liberal | l2_politics |
| emb_liberal | l4_religion |
| emb_hat | l1_hat_token |
| emb_hat | l3_love_hate |
| emb_self | l3_together |
| emb_stain | l6_respect |
| emb_dash | l4_race |
| l0_jew_strong | l2_race_ethnicity |
| l0_jew_strong | l3_jew_caps |
| l1_hat_token | l3_love_hate |
| l1_hat_token | l3_together |
| l2_race_ethnicity | l3_jew_caps |
| l2_race_ethnicity | l4_religion |
| l2_race_ethnicity | l4_race |
| l2_politics | l4_religion |
| l3_jew_caps | l4_religion |
| l3_jew_caps | l4_race |
| l3_jew_caps | l6_discrim |
| l3_love_hate | l4_race |
| l3_love_hate | l8_slavery |
| l3_together | l4_race |
| l4_religion | l6_discrim |
| l4_religion | l8_religion |
| l4_race | l6_discrim |
| l4_isrpal | l6_discrim |
| l6_discrim | output_probe |
| l6_respect | l8_neg_repute |
| l8_neg_repute | output_probe |
| l8_religion | output_probe |
| l8_slavery | output_probe |

## Oracle Judgment (verbatim)

The Oracle applies the answer-presence judge to each intervention in this narrative. Prompts are narrowly framed (numeric, yes/no, 'name one'); a `win` is when the required answer (or a directional approximation of it) leaks into the output, fluent and plausibly grounded — even if a suppression scaffold remains around it. `softened` = output shifted but no sign of the answer; suppression still gating in a different surface form. `no-shift` = unchanged or degenerate. Outcome ordering: `win > softened > no-shift` (with `degenerate` as a prose qualifier on no-shift when fluency broke). This narrative is the authoritative classification — see the All Interventions section below for raw before/after data.

**Analysis:** The probe's toxicity score is driven by a stack of identity-group detectors rooted overwhelmingly in the embedding of the single token "Jew" (pos 6), confirming the user's concern: the circuit is identity-term-driven rather than lexically reading the sentence's actual hate-speech content ("stain", "brethren", "country").

**Confidence:** 9

**Reasoning:** The single largest direct_effect into the output probe is **L6:F648** at pos 6 (DE=0.74, act=28.5), an autointerp-labeled "words related to discrimination against particular religious or ethnic groups." Its top upstream node is `Emb: Jew (pos 6)` with DE=19.4 — a *huge* jump that dwarfs every other feature in the graph. F648's other key feeders at pos 6 are the L3 "JEW"-ish caps feature (F12151, DE=5.9, label "capitalized common letter sequences such as SEM, ISM, WF, ISH, WE, SE" — this feature is actually responding to the sub-word "Jew"), the L4 religious-identity feature (F2405, DE=2.95, promoted token `▁Jewish`, frac_nonzero=0.007), the L4 Israel-Palestine feature (F14733, DE=2.36, promoted `▁Palestinian`), and an L4 race/racism feature (F117, DE=1.72, label "terms related to race, racism, and social justice, with a particular focus on terms related to Black people" — note the feature misfires onto "Jew" because the model has bundled identity-discourse into a single circuit).

The second-strongest output-driving feature, **L2:F13158** (DE=0.29, "race/ethnicity words," frac_nonzero=0.0099), also traces directly to `Emb: Jew (pos 6)` with DE=6.8 and to the L0 token amplifier F9026 (which gets DE=31.4 from the "Jew" embedding). L4:F2405 ("religious identity") likewise takes DE=6.75 from `Emb: liberal` and DE=3.78 from `Emb: Jew` — both identity-bearing tokens. The **L8:F13197** ("religion/faith," frac_nonzero=0.014) sends DE=0.143 directly to the probe and traces to the "Jew" embedding (DE=3.45) via L6:F648. L8:F2483 ("slavery, prejudice, disabilities") sends DE=0.174 to the probe and traces to `Emb: hat` (pos 3) and `Emb: Self` (pos 1) — this is the one feature with a real hate-speech lexical route, but its DE is small and its label reveals the "Self-hating" phrasing is being abstracted into a generic prejudice-discourse detector rather than read semantically.

The only feature with a *contentful* (non-identity) route is **L8:F13875** at pos 10 ("negative sentiment: reputation and betrayal of trust," promoted `▁disgraced`, `▁scandal`). It fires on the actual lexical content of the prompt — `Emb: stain (pos 9)` (DE=2.02) — and routes through L6:F1561 ("respect/dignity/pride," DE=3.42 from "stain" + "on"). This is the genuine lexical-semantic component of the circuit. But its DE into the probe is only 0.226, and it carries the toxicity score through an abstract "shame/disgrace" generalization rather than through reading "stain on his brethren and his country" as a coherent derogation.

**Bottom line — the user's concern is confirmed.** Of the top-20 output-driving features, the *vast majority* of total signed influence flows from `Emb: Jew` through F648 → probe (a direct ~0.74 DE), F13158 → probe, F2405 → probe, F14733 → probe, F13197 → probe, and F2483 → probe. The probe is essentially asking "is the word 'Jew' present in a context with religion/race/Palestine-discourse features?" — not "is this sentence actually toxic?" The hate-speech content ("stain," "brethren," "country," "Self-hating liberal") is read mostly by one L8 reputation feature (F13875), which contributes a minority of the probe's signal. The model is performing identity-term short-circuiting: the mere presence of "Jew" plus "liberal" plus an adjacent hate-leaning lexical token is sufficient to push the probe score up, regardless of who is being denigrated or how. This is a classic spurious-correlation failure mode where the toxicity probe has learned a shortcut: "sentence contains [protected-group identity term] + some negative valence = toxic," rather than the actual toxicity structure of the utterance.
