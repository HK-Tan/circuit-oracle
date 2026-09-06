# Circuit Oracle Report
**Date:** 2026-07-28 07:15:34 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven almost entirely by a stack of "race/social-justice" identity-detector features firing on the *content words* `white` (pos 2), `black` (pos 6), and `man` (pos 7), with negligible contribution from the toxic-action content (`stealing` at pos 4 contributes only via L2:F12341 which barely registers; the insult frame `Another…dude stealing…thunder` is essentially ignored).

**Confidence:** 8 — the user concern is strongly supported. Of the top 20 features driving the probe, ≥ 14 are race/gender/ethnicity identity detectors; the lexical-toxicity signal ("steal", "thunder") and the syntactic insulth framing ("Another…dude…stealing") have almost no influence.

**Reasoning:** The circuit reaches the token-embedding floor for every important input token. From there:

- **Identity-content token (pos 6 `black`)**: `emb_black` → L2:F13158 ("race/ethnicity words", direct_effect=10.8 at L2 and continues feeding) → L2:F9528 ("the color black", +31.9 → but pushes *against* the probe via −1.18 at L3:F13061, so net effect is identity-coded rather than color-coded) → L3:F13061 (race/gender social-issues, +15.7 emb contribution at pos 7, +1.2 at pos 3) → L3:F16373 (demographic identity, +3.9 at pos 3) → **L4:F117** ("race/racism/social-justice, focus on Black people", activation 18–20, direct_effect 0.69–0.88 — the single largest late-layer feature) → L5:F6786 (gender/race/orientation/disability bundle) → L6:F3902 (race & ethnicity terms) → L6:F5671 (people/gender) → L8:F2483 ("slavery, prejudice, disabilities", activation 17.5) → **L12:F13522** ("Black/white race & slavery", activation 19.25, direct_effect 0.25). This is a near-vertical identity-recognition column rising from the `black` token to the probe.

- **Identity-content token (pos 2 `white`)**: `emb_white` is the largest single positive direct effect into the probe-feeding path — +15.0 into L4:F117, +12.4 into L3:F13061 — again routing the "white" content word straight into the Black-focused race detector.

- **Insult frame tokens (`Another` pos 1, `dude` pos 3, `stealing` pos 4, `thunder` pos 9)**: `emb_another` activates L0:F4090 (frac_nonzero 0.021, generic "another") and L4:F9880 ("phrases indicating repetition/continuation, often 'another'", direct_effect 0.62 — this *is* one of the few non-identity top features, but it fires on the framing word, not on the toxic content). `emb_dude` does activate L6:F5671 (people/gender) with +3.6, but only because "dude" is a gendered person-noun. `emb_stealing` activates L2:F12341 (the "steal/taking" feature) at direct_effect 0.24, but this feature's promoted tokens are punctuation/generic ("<bos>", "'", "▁the") and its top activating examples are literary/crime fiction — it is **not** a toxicity or insult feature.

- **What the probe direction "hears"**: the only late-layer nodes feeding the probe logit are L4:F9880 (mild, framing-only), L6:F5671 (people/gender), L12:F13522 (race/slavery), and L2:F12341 (steal/taking). Three of the four are identity detectors; the fourth is a generic verb, not a slur/insult feature. The probe is therefore classifying the prompt as toxic on the basis that it mentions "white"/"black"/"man" in the same sentence as another demographic-coded term — i.e., a learned correlate of race-mention rather than a learned correlate of toxic intent.

This confirms the user's concern: the probe is using **spurious "identity group mention" features** (a chain of race/gender/demographic detectors at L2 → L3 → L4 → L5 → L6 → L8 → L12 all firing on the same two content nouns) rather than features that encode the actual toxic content (the "Another [X] stealing [Y]'s thunder" insult construction). A prompt with identical lexical-toxicity but different referents (e.g., "Another tall guy stealing the short man's parking spot…") would receive a substantially lower score despite being structurally and intentionally identical.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: white (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: dude (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: black (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: man (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Another (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: stealing (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4090](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) | 1 | Early 'another' feature (L0:F4090) | the word "another" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | Race/ethnicity words (L2:F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 2 | Race/ethnicity words (L2:F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 6 | Color 'black' (L2:F9528) |  the color black | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L2:F12341](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12341) | 4 | 'steal' / taking (L2:F12341) |  the word "steal" and words related to taking and basic needs | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12341) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 3 | Race/gender social-issues (L3:F13061) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 7 | Race/gender social-issues (L3:F13061) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 3 | Demographic identity mentions (L3:F16373) |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 7 | Demographic identity mentions (L3:F16373) |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L4:F9880](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) | 1 | 'another'/repetition phrase (L4:F9880) |  phrases indicating repetition or continuation which often use the word "another" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 3 | Race/social-justice (Black-focused) (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | Race/social-justice (Black-focused) (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L5:F6786](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) | 3 | Gender/race/orientation/disability bundle (L5:F6786) | terms associated with gender, race, sexual orientation, and disability | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 3 | Race & ethnicity terms (L6:F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 6 | Race & ethnicity terms (L6:F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 7 | Race & ethnicity terms (L6:F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F5671](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) | 3 | People with gender emphasis (L6:F5671) |  references to people, with an emphasis on gender and family relations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) |
| [L8:F2483](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) | 6 | Slavery, prejudice, disabilities (L8:F2483) |  discussions of slavery, prejudice, and disabilities | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) |
| [L12:F13522](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/13522) | 6 | Black/white race & slavery (L12:F13522) |  terms relating to race, specifically focusing on black and white people and slavery. | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/13522) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification logit (toxicity) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:117 de=0.875 |
| 3 | `inspect_feature` ×13 | L4:117, L3:13061, L4:9880, L3:16373, L8:2483, L2:13158, L2:9528, L6:3902, L5:6786, L12:13522, L2:12341, L6:5671, L0:4090 |
| 4 | `get_upstream_features` | Emb:" white"@2 (de=15.00) +9 more |
| 5 | `get_upstream_features` | Emb:" black"@6 (de=14.06) +9 more |
| 6 | `get_upstream_features` | Emb:" white"@2 (de=12.44) +9 more |
| 7 | `get_upstream_features` | Emb:" black"@6 (de=15.69) +9 more |
| 8 | `get_upstream_features` | Emb:"Another"@1 (de=33.25) +9 more |
| 9 | `get_upstream_features` | Emb:" black"@6 (de=10.81) +9 more |
| 10 | `get_upstream_features` | Emb:" black"@6 (de=31.88) +9 more |
| 11 | `get_upstream_features` | Emb:"Another"@1 (de=32.75) +9 more |
| 12 | `get_upstream_features` | Emb:" black"@6 (de=4.59) +7 more |
| 13 | `get_upstream_features` | Emb:" black"@6 (de=4.91) +7 more |
| 14 | `get_upstream_features` | Emb:" stealing"@4 (de=11.62) +7 more |
| 15 | `get_upstream_features` | Emb:" black"@6 (de=13.44) +5 more |
| 16 | `get_upstream_features` | L4:F117 (de=6.78) +5 more |
| 17 | `get_upstream_features` | Emb:" dude"@3 (de=3.56) +5 more |
| 18 | `get_upstream_features` | Emb:" white"@2 (de=2.30) +5 more |

### Build

`build_circuit` → 20 nodes, 38 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 33,615 | 6,393 | 128,604 | 0 | $0.0255 | — | — |
| **Total** | | **33,615** | **6,393** | **128,604** | **0** | **$0.0255** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 23s