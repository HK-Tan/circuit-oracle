# Circuit Oracle Report
**Date:** 2026-07-28 07:19:46 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by identity-group-mention features that fire on the tokens "white" and "black", with a secondary boost from the word "Another" — not by features encoding the actual harmful/accusatory content (e.g. "stealing", "dude", "thunder") or toxicity-related sentiment.

**Confidence:** 9

**Reasoning:** The attribution graph is dominated by race/ethnicity features rather than semantic-toxicity features.

**Top-3 features feeding the probe (by direct_effect):**
1. **L4:F117** (frac_nonzero 0.012) — "terms related to race, racism, and social justice, with a particular focus on terms related to Black people". Upstream trace: it is *exclusively* anchored to the **Emb: white (pos 2)** token (direct_effect 15.0) and the **Emb: dude (pos 3)** token (direct_effect 2.6). Promoted tokens include `racist`, `racial`, `racism`. The bare presence of the word "white" activates a feature whose promoted-token distribution is racialized slurs/identity terms — i.e. the model has bound the word "white" to a "race-discourse" subspace.
2. **L4:F117 at pos 7** (the final period position) — same feature activates on the late position after the prompt ends, propagating the race-discourse signal beyond the literal identity tokens.
3. **L3:F13061** (frac_nonzero 0.009) — "words related to race, gender and social issues"; also traced back to Emb:white / Emb:dude.

**Supporting features:**
- **L3:F16373** (demographic identity) — fires on pos 3 "dude" with direct_effect 0.39.
- **L6:F3902** (race/ethnicity) at pos 3 and pos 7 — direct_effect 0.40 and 0.25.
- **L5:F6786** (gender/race/sexual-orientation/disability) at pos 3.
- **L2:F13158** (race/ethnicity) at pos 6 — receives a direct upstream edge of 10.8 from **Emb: black (pos 6)** (i.e. the *literal word* "black" is the trigger, not a learned notion of the group).
- **L2:F9528** (the color black) at pos 6 — fires on the same token with direct_effect 13.4, but it represents the literal color (its top-activating examples are AMOLED pixels, tea, etc.) and is SUPPRESSING identity terms (its suppressed_token list includes "Black", "BLACK", "黑", "ブラック", "的黑") — yet it still gets routed into the race-discourse downstream feature, amplifying the signal.

**The "stealing"/content path is essentially decoupled:** L2:F12341 ("the word 'steal'") activates at pos 4 (direct_effect 0.24) but only weakly propagates onward. Crucially, **no feature in the top-15 promotes toxicity/slur tokens directly**; instead, identity-mention features are the *promoted_token direction* of these features (L4:F117 promotes `racist`, `racial`, `racism`; L6:F3902 promotes `minorities`, `ethnicity`; L3:F13061 promoted list is degenerate but its activation is high on race-discourse text). The mid-layer (L8:F2483 "slavery/prejudice/disabilities", L9:F8462 "Black community", L11:F2332 "text related to race") and late-layer (L12:F13522 "race/black-white/slavery") features further refine the signal.

**Spurious-correlation mechanism:** A completely anodyne sentence containing the words "white" and "black" — even a sentence about weather, geography, or art — would produce nearly the same circuit, because the L2/L3 race features activate on the raw embeddings of the words themselves (Emb:black has direct_effect 10.8 into L2:F13158, Emb:white has direct_effect 15.0 into L4:F117). The model has learned a "two-identity-words-present" detector and routed it to the toxicity direction. The probe is therefore not measuring *toxicity* in the prompt — it is measuring *whether the prompt names two racial groups*, which is a feature of the input's lexical content but a spurious proxy for the semantic property the probe claims to encode.

**Note on the user's hypothesis:** The user is correct. The circuit is overwhelmingly identity-group-mention-driven, not driven by features encoding the actual harmful/accusatory content of the prompt ("dude stealing thunder"). The toxicity-direction signal here is essentially a "two-race-words-near-each-other" detector.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L12:F13522](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/13522) | 6 | race/slavery/black-white discourse (L12) |  terms relating to race, specifically focusing on black and white people and slavery. | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/13522) |
| [L8:F2483](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) | 6 | race/slavery/disability discourse (L8-L9) |  discussions of slavery, prejudice, and disabilities | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) |
| [L9:F8462](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8462) | 6 | race/slavery/disability discourse (L8-L9) |  language related to the Black community and multicultural marketing. | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8462) |
| [L11:F2332](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/2332) | 6 | race/slavery/disability discourse (L8-L9) |  text related to race. | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/2332) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 3 | race/ethnicity terms (L4, L6) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | race/ethnicity terms (L4, L6) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 3 | race/ethnicity terms (L4, L6) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 7 | race/ethnicity terms (L4, L6) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | race/ethnicity terms (L4, L6) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 3 | race/ethnicity terms (L4, L6) |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 3 | race/ethnicity terms (L4, L6) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 7 | race/ethnicity terms (L4, L6) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L5:F6786](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) | 3 | race/ethnicity terms (L4, L6) | terms associated with gender, race, sexual orientation, and disability | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 6 | literal color 'black' (L2) |  the color black | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L4:F9880](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) | 1 | 'Another' repetition/continuation (L4) |  phrases indicating repetition or continuation which often use the word "another" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) |
| [L2:F12341](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12341) | 4 | 'steal' word-form (L2) |  the word "steal" and words related to taking and basic needs | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12341) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:117 de=0.875 |
| 3 | `inspect_feature` ×12 | L4:117, L3:13061, L4:9880, L3:16373, L6:3902, L8:2483, L2:13158, L2:9528, L12:13522, L5:6786, L2:12341, L6:5671 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L12:F13522@6` | ❌ error | — | — | Trace the upstream circuit from L12:F13522 (race/slavery feature at pos 6 'man''… |
| SA-2 | `L8:F2483@6` | ❌ error | — | — | Trace the upstream circuit from L8:F2483 (slavery/prejudice/disabilities at pos … |
| SA-3 | `L4:F117@3` | ❌ error | — | — | Trace the upstream circuit from L4:F117 (race/Black people feature) at pos 3 (to… |
| SA-4 | `L4:F9880@1` | ❌ error | — | — | Trace the upstream circuit from L4:F9880 ('another' repetition/continuation feat… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L12:F13522@6, k=12 → Emb:" black"@6 (de=4.91) +11 more |
| 2 | `get_upstream_features` | L8:F2483@6, k=12 → Emb:" black"@6 (de=4.59) +11 more |
| 3 | `get_upstream_features` | L4:F117@3, k=12 → Emb:" white"@2 (de=15.00) +11 more |
| 4 | `get_upstream_features` | L4:F9880@1, k=12 → Emb:"Another"@1 (de=33.25) +11 more |
| 5 | `get_upstream_features` | L2:F13158@6, k=12 → Emb:" black"@6 (de=10.81) +11 more |
| 6 | `get_upstream_features` | L6:F3902@6, k=12 → Emb:" black"@6 (de=13.44) +11 more |
| 7 | `get_upstream_features` | L5:F6786@3, k=12 → Emb:" white"@2 (de=2.30) +11 more |
| 8 | `get_upstream_features` | L2:F12341@4, k=12 → Emb:" stealing"@4 (de=11.62) +11 more |
| 9 | `inspect_feature` ×2 | L11:2332, L9:8462 |
| 10 | `get_upstream_features` | L11:F2332@6, k=10 → Emb:" black"@6 (de=3.00) +9 more |

### Build

`build_circuit` → 13 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 31,648 | 4,644 | 150,935 | 0 | $0.0241 | — | — |
| **Total** | | **31,648** | **4,644** | **150,935** | **0** | **$0.0241** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 4s