# Circuit Oracle Report
**Date:** 2026-07-28 07:19:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit is already well-traced. Embeddings are present. Let me finalize the analysis.

**Analysis:** The probe's classification score is driven almost entirely by a cascade of identity-term detectors that fire on the words "Another," "white," "dude," "black," and "man" — i.e., the demographic/identity vocabulary of the prompt — while the actual toxic content (e.g., "stealing…thunder") is never represented in the top of the circuit. This confirms the user's hypothesis: the probe is using spurious identity-group signal, not toxic content.

**Confidence:** 9

**Reasoning:** The top direct-effect features driving the probe direction are all identity/race-related. The circuit flows as follows:

1. **Token embeddings → L0–L3 lexical identity detectors.** The "Another" embedding (pos 1) directly drives L0:F4090 (the literal word "another," frac_nonzero=0.02, direct_effect 32.75 to itself, and ~0.65 to L3:F13061). The "white" embedding (pos 2) directly drives L3:F13061 (race/gender/social-issues words, direct_effect 12.44), L3:F16373 (demographic identity, direct_effect 23.1), L2:F13158 (race/ethnicity, direct_effect ~1+), and L4:F117. The "black" embedding (pos 6) directly drives L2:F13158 (10.8), L8:F2483 (4.6), and L12:F13522 (4.9). The "man" embedding (pos 7) drives L4:F117 at pos 7 (4.4) and L3:F16373 at pos 7 (2.6). Notably **no embedding of the words "stealing," "thunder," or "the" appears as a top positive driver** — "the" at pos 5 contributes 1.14 to L2:F13158 but nothing to higher layers, and "stealing" at pos 4 actually *inhibits* L2:F13158 (-1.02).

2. **L2–L4 generic race/ethnicity features** (L2:F13158, L3:F13061, L3:F16373, L4:F117, L4:F9880 for "another/again") all promote vocabulary like "racial," "racist," "racism," "ethnic," "Hispanic," "Latino," "Muslim" (per the promoted_tokens fields) and have frac_nonzero in 0.006–0.012 — they are *category-specific* (race/ethnicity) but not *content-specific* (no encoding of what is being said about the group).

3. **L5–L8 policy-style identity features** (L5:F6786 gender/race/sexual-orientation/disability; L6:F3902 race/ethnicity aggregator with direct_effect 0.40 at pos 3 to the probe; L8:F2483 slavery/prejudice/disabilities with direct_effect 0.39 at pos 6) carry these identity signals upward.

4. **L12:F13522** ("terms relating to race, specifically focusing on black and white people and slavery," frac_nonzero=0.003, very selective) sits at the top of the chain with direct_effect 0.25 to the probe and is driven by the " black" embedding plus L2, L6, and L8 race features.

5. The **probe output** is fed by L5:F6786 (0.26), L6:F3902 (0.40), and L12:F13522 (0.25) — every one of which is an identity-term detector, not a content/sentiment detector.

The functional content of the prompt — "stealing the … man's thunder" (the actual toxic/derogatory claim) — has no feature among the top ~20 positive direct effects at any layer. The lone "dude" and "man" embeddings serve only as additional identity-category evidence (L4:F117 promoted_token list is "racial," "racist," "racism," ""). The result is a probe whose score is essentially "this sentence mentions a racial identity group," which is exactly the spurious-correlation failure mode the user suspected: identity mentions, not the harmful speech act, drive the toxicity score.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Another (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: white (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: dude (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: black (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: man (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4090](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) | 1 | L0: 'Another' word detector (pos 1) | the word "another" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | L2: Race/ethnicity word detector (black) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 2 | L2: Race/ethnicity word detector (black) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 3 | L2: Race/ethnicity word detector (black) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 3 | L3: Demographic identity (race/gender) detector |  mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 3 | L3: Demographic identity (race/gender) detector |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 7 | L3: Demographic identity (race/gender) detector |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 3 | L4: Race/social-justice terms, focus on Black people |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | L4: Race/social-justice terms, focus on Black people |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 2 | L4: Race/social-justice terms, focus on Black people |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F9880](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) | 1 | L4: Race/social-justice terms, focus on Black people |  phrases indicating repetition or continuation which often use the word "another" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) |
| [L5:F6786](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) | 3 | L5: Gender/race/sexual-orientation/disability terms | terms associated with gender, race, sexual orientation, and disability | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 3 | L6: Race/ethnicity terminology aggregator |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 7 | L6: Race/ethnicity terminology aggregator |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F5671](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) | 3 | L6: Race/ethnicity terminology aggregator | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) |
| [L8:F2483](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) | 6 | L8: Slavery, prejudice, disabilities discussion |  discussions of slavery, prejudice, and disabilities | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) |
| [L12:F13522](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/13522) | 6 | L12: Black/white race + slavery-specific feature |  terms relating to race, specifically focusing on black and white people and slavery. | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/13522) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:117 de=0.875 |
| 3 | `inspect_feature` ×10 | L4:117, L3:13061, L4:9880, L3:16373, L8:2483, L2:13158, L5:6786, L12:13522, L6:3902, L0:4090 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F13061@3` | ❌ error | — | — | Trace from L3:F13061 (race/gender/social-issues terms) upstream to find which in… |
| SA-2 | `L4:F117@3` | ❌ error | — | — | Trace from L4:F117 (race/Black-people terms) upstream to find which input tokens… |
| SA-3 | `L12:F13522@6` | ✅ reported | 4 | 4 | Trace from L12:F13522 (black/white race + slavery) at pos 6 upstream to find whi… |
| SA-4 | `L0:F4090@1` | ❌ error | — | — | Trace from L0:F4090 (the word "another") at pos 1 upstream — confirm it directly… |

<details>
<summary><b>SA-3</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F13522 | " terms relating to race, specifically focusing on black and white peop" |
| 2 | `get_upstream_features` | L12:F13522@6, k=10 | Emb:" black"@6 (de=4.91) +9 more |
| 3 | `inspect_feature` | L8, F2483 | " discussions of slavery, prejudice, and disabilities" |
| 4 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 5 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |

**Findings:** Tracing from the target race‑policy feature (L12:F13522) reveals a clear upstream chain: the raw token embedding for " black" at position 6 supplies the strongest excitatory drive, followed by a mid‑layer (L8:F2483) that aggregates slavery‑ and prejudice‑related cues, and earlier layers (L2:F13158, L6:F3902) that act as generic race/ethnicity detectors. The path reaches both a lower‑third layer (L…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L3:F13061@3, k=12 → Emb:" white"@2 (de=12.44) +11 more |
| 2 | `get_upstream_features` | L4:F117@3, k=12 → Emb:" white"@2 (de=15.00) +11 more |
| 3 | `get_upstream_features` | L2:F13158@6, k=10 → Emb:" black"@6 (de=10.81) +9 more |
| 4 | `get_upstream_features` | L0:F4090@1, k=8 → Emb:"Another"@1 (de=32.75) +7 more |
| 5 | `get_upstream_features` | L3:F16373@3, k=10 → Emb:" white"@2 (de=23.12) +9 more |
| 6 | `get_upstream_features` | L6:F3902@3, k=10 → L4:F117 (de=6.78) +9 more |
| 7 | `get_upstream_features` | L5:F6786@3, k=10 → Emb:" white"@2 (de=2.30) +9 more |
| 8 | `get_upstream_features` | L8:F2483@6, k=10 → Emb:" black"@6 (de=4.59) +9 more |
| 9 | `get_upstream_features` | L4:F117@7, k=10 → Emb:" black"@6 (de=14.06) +9 more |

### Build

`build_circuit` → 14 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 40,612 | 4,703 | 122,904 | 0 | $0.0252 | — | — |
| SA-3 | openai/gpt-oss-120b | 42,865 | 3,129 | 2,576 | 0 | $0.0083 | ✅ 4F/4E | Trace from L12:F13522 (black/white race + slavery) at pos 6 … |
| **Total** | | **83,477** | **7,832** | **125,480** | **0** | **$0.0335** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 26s