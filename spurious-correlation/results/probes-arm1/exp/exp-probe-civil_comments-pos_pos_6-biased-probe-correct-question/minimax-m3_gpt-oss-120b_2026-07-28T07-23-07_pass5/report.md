# Circuit Oracle Report
**Date:** 2026-07-28 07:23:07 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a chain of features that detect *racial/demographic identity terms* (e.g. "white", "black", "dude") and the *discourse of race/racism*, not by any feature that captures the prompt's toxicity-relevant semantics (e.g. "stealing", "thunder", the structural meaning of the sentence).

**Confidence:** 8

**Reasoning:**

The attribution graph traces a clear identity-detection circuit that flows from input token embeddings up to the probe direction:

- **Token embeddings (Emb: white pos 2, Emb: dude pos 3, Emb: black pos 6, Emb: Another pos 1)** are the floor of the circuit. The `white` token at pos 2 has very large direct effects (e.g. +23.1 into L3:F16373, +15 into L4:F117, +12.4 into L3:F13061), and `black` at pos 6 dominates L12:F13522 (direct_effect ≈ +4.9) and L11:F2332 (≈ +3.0). These are the only input tokens meaningfully driving the score.

- **Early layer (L0–L2)**: L0:F4090 (the word "another", frac_nonzero ≈ 0.021) and L2:F13158 ("words about race and ethnicity", frac_nonzero ≈ 0.010, promoted tokens `ethnic`, `queer`, `LGBT`, `Hispanic`, `Latino`, `Muslim`, `Jewish`) detect the identity-laden tokens.

- **Mid layer (L3–L4)**: L3:F16373 ("mentions of demographic identity, especially race and gender", frac_nonzero ≈ 0.006), L3:F13061 ("words related to race, gender and social issues", frac_nonzero ≈ 0.009), and L4:F117 ("terms related to race, racism, and social justice, with a particular focus on terms related to Black people", frac_nonzero ≈ 0.012, promoted tokens `racial`, `Racism`, `racist`) form the core identity-detector block. L4:F117 alone contributes +0.875 (pos 3) and +0.687 (pos 7) to the probe score — the largest single contributors in the entire graph.

- **Mid layer (L5–L6)**: L5:F6786 ("terms associated with gender, race, sexual orientation, and disability", frac_nonzero ≈ 0.022) and L6:F3902 ("terms referring to race and ethnicity", frac_nonzero ≈ 0.018) further refine the identity signal.

- **Late layer (L8–L12)**: L8:F2483 ("discussions of slavery, prejudice, and disabilities"), L9:F8462 ("language related to the Black community"), L11:F2332 ("text related to race", frac_nonzero ≈ 0.002, extremely specific), and L12:F13522 ("terms relating to race, specifically focusing on black and white people and slavery", frac_nonzero ≈ 0.003) all encode the same race/discourse concept. The most specific of these (L11, L12 with frac_nonzero < 0.005) carry the signal into the probe direction.

- **What is missing from the circuit**: The semantically toxic elements of the sentence — "stealing", "thunder", the possessive framing "Another X stealing the Y's Z" (a known microaggression / complaint-template pattern) — are barely represented. L2:F12341 ("the word 'steal'") appears but with a *negative* direct_effect (−0.264 in the top features). The structural "another [out-group member] doing [negative thing] to [in-group]" template that makes the sentence toxic is not detected by any feature in the top contributors.

- **Spurious-feature diagnosis confirmed**: The user's concern is supported. The probe is essentially a race/demographic-identity detector dressed up as a toxicity probe. Because the prompt happens to contain the words "white" and "black" in proximity, the identity-detector features light up, the probe scores high, and the actual toxicity-driving structure of the sentence (the comparative-complaint template) is ignored. The signal pathway goes Emb:"white"/"black" → race/ethnicity features (L2–L6) → race/discourse features (L8–L12) → probe logit, with no meaningful contribution from features that would encode the sentence's interpersonal-attack semantics. A neutral sentence containing the same two race tokens (e.g. "A white man and a black woman were co-workers") would likely produce a similar probe score, demonstrating the spuriousness.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | Early race/ethnicity detectors (L0, L2) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 2 | Early race/ethnicity detectors (L0, L2) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L0:F4090](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) | 1 | Early race/ethnicity detectors (L0, L2) | the word "another" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) |
| [L0:F6548](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6548) | 2 | Early race/ethnicity detectors (L0, L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6548) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 3 | Mid-layer race/demographic identity features (L3-L4) |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 3 | Mid-layer race/demographic identity features (L3-L4) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 7 | Mid-layer race/demographic identity features (L3-L4) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 3 | Mid-layer race/demographic identity features (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | Mid-layer race/demographic identity features (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 2 | Mid-layer race/demographic identity features (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Mid-layer race/demographic identity features (L3-L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F9880](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) | 1 | Mid-layer race/demographic identity features (L3-L4) |  phrases indicating repetition or continuation which often use the word "another" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) |
| [L5:F6786](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) | 3 | Mid-layer race/ethnicity/identity features (L5-L6) | terms associated with gender, race, sexual orientation, and disability | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 3 | Mid-layer race/ethnicity/identity features (L5-L6) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 7 | Mid-layer race/ethnicity/identity features (L5-L6) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F5671](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) | 3 | Mid-layer race/ethnicity/identity features (L5-L6) |  references to people, with an emphasis on gender and family relations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) |
| [L2:F12341](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12341) | 4 | Mid-layer race/ethnicity/identity features (L5-L6) |  the word "steal" and words related to taking and basic needs | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12341) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 6 | Mid-layer race/ethnicity/identity features (L5-L6) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L8:F2483](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) | 6 | Late-layer race/discourse features (L8-L9) |  discussions of slavery, prejudice, and disabilities | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) |
| [L9:F8462](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8462) | 6 | Late-layer race/discourse features (L8-L9) |  language related to the Black community and multicultural marketing. | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8462) |
| [L11:F2332](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/2332) | 6 | Late-layer composed race features (L11-L12) |  text related to race. | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/2332) |
| [L12:F13522](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/13522) | 6 | Late-layer composed race features (L11-L12) |  terms relating to race, specifically focusing on black and white people and slavery. | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/13522) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:117 de=0.875 |
| 3 | `inspect_feature` ×12 | L4:117, L3:13061, L4:9880, L3:16373, L8:2483, L12:13522, L2:13158, L2:12341, L6:5671, L6:3902, L5:6786, L0:4090 |
| 4 | `get_upstream_features` | Emb:" white"@2 (de=15.00) +9 more |
| 5 | `get_upstream_features` | Emb:" white"@2 (de=12.44) +9 more |
| 6 | `get_upstream_features` | Emb:" black"@6 (de=4.91) +9 more |
| 7 | `get_upstream_features` | Emb:" white"@2 (de=23.12) +9 more |
| 8 | `get_upstream_features` | Emb:" black"@6 (de=4.59) +9 more |
| 9 | `get_upstream_features` | L4:F117 (de=6.78) +9 more |
| 10 | `get_upstream_features` | Emb:"Another"@1 (de=33.25) +9 more |
| 11 | `inspect_feature` ×2 | L11:2332, L9:8462 |
| 12 | `get_upstream_features` | Emb:" black"@6 (de=3.00) +9 more |
| 13 | `get_upstream_features` | Emb:" black"@6 (de=10.81) +9 more |
| 14 | `get_upstream_features` | Emb:" stealing"@4 (de=11.62) +9 more |
| 15 | `get_upstream_features` | Emb:" dude"@3 (de=3.56) +9 more |

### Build

`build_circuit` → 10 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 37,846 | 3,992 | 127,681 | 0 | $0.0238 | — | — |
| **Total** | | **37,846** | **3,992** | **127,681** | **0** | **$0.0238** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 14s