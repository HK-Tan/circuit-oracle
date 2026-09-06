# Circuit Oracle Report
**Date:** 2026-07-28 07:22:21 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven almost entirely by generic "identity group" topic features (LGBTQ discussion, race/ethnicity vocabulary, racism/Black-focused social-justice terms) that fire on mere mentions of identity words — not on the actually toxic content ("NAZI!", "Hypocrisy is worse than racism").

**Confidence:** 8

**Reasoning:**

The attribution circuit is strikingly clean and validates the user's concern. The output logit (probe direction) receives its positive contributions from a small set of features that are essentially "topic detectors" for identity-related content, not toxicity detectors.

**The two main excitatory paths:**

1. **LGBTQ-topic path** (largest single contributor, sum of direct_effects ≈ 0.74): The token embedding for "Gay" (pos 9, direct_effect=10.4 to L8:F15771) and " Pride" (pos 2, direct_effect=3.8) feed into **L4:F15899** ("LGBTQ/gender/identity language", frac_nonzero=0.006), then **L6:F6085** ("homosexuality/same-sex marriage", frac_nonzero=0.002), then **L8:F15771** ("LGBTQ-issues discussion", frac_nonzero=0.008). All three of these features are highly *specific* to LGBTQ content but are *not* specifically tied to toxic contexts — their top activating examples include neutral, positive, and negative LGBTQ coverage. L6:F6085 also fires on a side path from the " Pride" token to L6:F15295, a "HIV/AIDS" feature (the only one that even hints at negativity via its suppression of "<bos>" / common tokens), which is again a *topic* signal, not a *toxicity* signal.

2. **Race/ethnicity topic path** (sum of direct_effects ≈ 0.6): The "White" token (pos 17) feeds **L2:F13158** ("race/ethnicity vocabulary", frac_nonzero=0.01) → **L4:F117** ("race/racism/Black-focused social-justice terms", promoted tokens: "racist", "racism", "racial", frac_nonzero=0.012) → **L6:F3902** ("race/ethnicity terms", frac_nonzero=0.018). The "Black" token (pos 1) also feeds L2:F13158, L3:F13061 ("race/gender/social issues", frac_nonzero=0.009), and L2:F11363 ("color words including Black/White"). These features fire on *any* mention of race — neutral demographic descriptions ("racial makeup of the town"), academic race studies, etc.

**The inhibitory side (which is telling):** The "Black" token embedding also drives two features that push the probe *down* — L2:F9528 ("the color black", frac_nonzero=0.002, suppressed_tokens: "Black", "black", "Black", i.e. the literal-color reading suppresses toxicity scoring) and L1:F9113 ("discussions about race and slavery", promoted tokens don't include toxic vocabulary, and it has *negative* direct_effect to the probe despite firing on "Black"). The model has separate features for "Black-as-color" and "Black-as-race-in-discussion" that are *not* what the probe picks up; the probe listens to the *generic race-topic* features (L2:F13158, L4:F117, L6:F3902) rather than any feature specifically tuned to racism/hate content.

**Critical observations for the user's hypothesis:**
- The word "NAZI!" (pos 9 — wait, the tokenization puts "Gay" at pos 9 of the second line; "NAZI" is the last token of the third line) and the word "Hypocrisy" / "racism" in the final line do **not** appear as direct drivers. The circuit traces back to "Gay", "Black", "White", and " Pride" — purely identity-mention tokens.
- The " Pride" and "Black Pride" tokens specifically drive L3:F13061 ("race/gender/social-issues vocabulary") with direct_effect=+0.24, and the L2:F1644 "pride"-detector feeds into it.
- L4:F117 explicitly promotes "racist"/"racism" vocabulary in its decoder direction, yet *the feature's direct_effect on the probe is positive even when the text doesn't contain "racist"* — meaning the probe treats the *topic of race* itself as the signal, not the *linguistic marker of racism*.
- No feature in the top-20 drivers encodes "slur," "insult," "equating X to Nazis," or any genuinely toxic-content pattern.

**Conclusion:** The circuit confirms the user's concern. The toxicity probe is reading off coarse **identity-topic detectors** (LGBTQ discussion, race/ethnicity vocabulary, social-justice terminology) rather than anything resembling a "hateful content" or "rhetorical device" detector. The features that *would* capture the actual toxic moves — "NAZI!" as a slur-equation, the moralizing sentence "Hypocrisy is worse than racism" — have no positive pathway to the probe. This is a textbook spurious-feature circuit: the probe has learned "text about marginalized groups → toxic" as a shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F1644](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) | 2 | Pride-token detector (L2:F1644) |  different forms of the word "pride" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) |
| [L1:F12542](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12542) | 2 | 'proud' / TV-season words (L1:F12542) | mentions of the word "proud" or words relating to TV shows and TV seasons. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12542) |
| [L3:F7993](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7993) | 1 | word 'black'/'blacks' literal (L3:F7993) | the word "black" and its plural form "blacks" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7993) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 1 | literal color 'black' (L2:F9528) — PUSHES DOWN |  the color black | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 5 | literal color 'black' (L2:F9528) — PUSHES DOWN |  the color black | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 1 | race/slavery discussions (L1:F9113) — PUSHES DOWN |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L2:F11363](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) | 1 | color words including Black/White (L2:F11363) |  colors and words like Diamond. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 2 | race/gender/social-issues vocabulary (L3:F13061) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 5 | race/ethnicity vocabulary (L2:F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 17 | race/ethnicity vocabulary (L2:F13158) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 17 | race/racism/Black-focused social-justice terms (L4:F117) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 5 | race/ethnicity terms (L6:F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 17 | race/ethnicity terms (L6:F3902) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 9 | LGBTQ/gender/identity language (L4:F15899) |  language associated with the LGBTQ community and discussions of gender and identity. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 9 | homosexuality/same-sex-marriage topic (L6:F6085) |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 13 | homosexuality/same-sex-marriage topic (L6:F6085) |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 2 | LGBTQ-issues discussion (L8:F15771) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 9 | LGBTQ-issues discussion (L8:F15771) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 13 | LGBTQ-issues discussion (L8:F15771) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L6:F15295](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) | 2 | HIV/AIDS medical vocabulary (L6:F15295) |  words and abbreviations related to HIV/AIDS and viral infections. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:15771 de=0.324 |
| 3 | `inspect_feature` ×14 | L8:15771, L6:6085, L2:13158, L4:15899, L1:9113, L2:11363, L3:13061, L6:3902, L2:9528, L1:12542, L4:117, L2:1644, L6:15295, L3:7993 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F15771@9` | ❌ error | — | — | Trace from L8:F15771 (LGBTQ topic feature at pos 9, i.e. "NAZI!"). This is the l… |
| SA-2 | `L2:F13158@17` | ❌ error | — | — | Trace from L2:F13158 (race/ethnicity words at pos 17 = "Hypocrisy"). Find what t… |
| SA-3 | `L2:F9528@1` | ❌ error | — | — | Trace from L2:F9528 (the color black at pos 1 = "Black" in "Black Pride"). Find … |
| SA-4 | `L1:F9113@1` | ❌ error | — | — | Trace from L1:F9113 (race/slavery discussions at pos 1 = "Black"). Find what tok… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L8:F15771@9, k=10 → Emb:"Gay"@9 (de=10.38) +9 more |
| 2 | `get_upstream_features` | L2:F13158@17, k=10 → Emb:"White"@17 (de=13.56) +9 more |
| 3 | `get_upstream_features` | L2:F9528@1, k=10 → Emb:"Black"@1 (de=30.00) +9 more |
| 4 | `get_upstream_features` | L1:F9113@1, k=10 → Emb:"Black"@1 (de=16.88) +9 more |
| 5 | `get_upstream_features` | L6:F6085@9, k=10 → Emb:"Gay"@9 (de=21.75) +9 more |
| 6 | `get_upstream_features` | L4:F117@17, k=10 → Emb:"White"@17 (de=10.25) +9 more |
| 7 | `get_upstream_features` | L4:F15899@9, k=10 → Emb:"Gay"@9 (de=13.81) +9 more |
| 8 | `get_upstream_features` | L6:F3902@17, k=8 → Emb:"White"@17 (de=7.12) +7 more |
| 9 | `get_upstream_features` | L2:F11363@1, k=8 → Emb:"Black"@1 (de=25.00) +7 more |
| 10 | `get_upstream_features` | L3:F13061@2, k=8 → Emb:"Black"@1 (de=12.06) +7 more |
| 11 | `get_upstream_features` | L1:F12542@2, k=8 → Emb:" Pride"@2 (de=13.75) +7 more |
| 12 | `get_upstream_features` | L6:F15295@2, k=8 → Emb:" Pride"@2 (de=10.75) +7 more |
| 13 | `get_upstream_features` | L2:F1644@2, k=8 → Emb:" Pride"@2 (de=16.62) +7 more |
| 14 | `get_upstream_features` | L3:F7993@1, k=5 → Emb:"Black"@1 (de=23.50) +4 more |
| 15 | `get_upstream_features` | L2:F1644@2, k=5 → Emb:" Pride"@2 (de=16.62) +4 more |
| 16 | `get_upstream_features` | L2:F1644@5, k=5 → ❌ Feature (layer=2, feature_idx=1644) not found at pos=5. This |

### Build

`build_circuit` → 18 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 41,657 | 5,845 | 171,849 | 0 | $0.0298 | — | — |
| **Total** | | **41,657** | **5,845** | **171,849** | **0** | **$0.0298** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 24s