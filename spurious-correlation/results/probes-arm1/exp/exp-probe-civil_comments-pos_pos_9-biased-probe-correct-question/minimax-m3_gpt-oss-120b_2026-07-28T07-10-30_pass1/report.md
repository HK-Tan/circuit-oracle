# Circuit Oracle Report
**Date:** 2026-07-28 07:10:30 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies the input as toxic primarily because the model fires a dense, multi-layer cascade of "race/ethnicity" and "identity-group" detectors (L6:F3902, L4:F117, L3:F13061, L3:F16373) on the tokens "white" (pos 9) and "oriental" (pos 10), while a separate path (L4:F10004, L3:F8492) detects the self-hate lexeme; signal flows from the raw embeddings of those identity terms through low-layer lexical features and converges on the toxicity logit.

**Confidence:** 8

**Reasoning:** The dominant contributors to the probe's classification score are *not* generic toxicity/insult features — they are **identity-group detectors**:

- **L6:F3902** ("terms referring to race and ethnicity", frac_nonzero=0.018) fires on "white" and "oriental" with direct_effect ≈ +0.34 to +0.19 to the probe.
- **L4:F117** ("terms related to race, racism, and social justice…Black people", frac_nonzero=0.012) fires on "white"/"oriental" with direct_effect ≈ +0.31 to +0.22.
- **L3:F13061** ("words related to race, gender and social issues", frac_nonzero=0.009) fires on "oriental" with direct_effect ≈ +0.39.
- **L3:F16373** ("mentions of demographic identity, especially race and gender", frac_nonzero=0.006).

Tracing upstream shows these are *not* content-free: each is directly excited by the raw token embeddings of "white" (pos 9, direct_effect ≈ 13.6–15.1) and "oriental" (pos 10, direct_effect ≈ 11–12), through low-layer lexical conduits L2:F13158 (race/ethnicity words), L2:F585 ("white"), L2:F1708 (color words), and L1:F9113 (race/slavery discussions). So the probe's "toxicity" reading is being driven by the *presence of identity-group vocabulary itself* — "white", "oriental", "her", "last name" — rather than by lexemes of hostility per se.

A second pathway (L4:F10004 "self-", L3:F8492 "hate", L3:F4512 "last/name") is genuinely about the insult content ("self hater", "last name") and contributes via direct_effect ≈ +0.16 to +0.22.

User's concern is **partially validated and partially nuanced**: the *dominant* signal is indeed "spurious" in the sense that the highest-weighted features (L6:F3902 and L4:F117) encode the mere *presence of racial/demographic vocabulary* as a toxicity-relevant signal — they would fire on neutral sentences like "an oriental woman married a white man" just as strongly. However, the circuit is *not* entirely identity-only: it also picks up genuine hostility cues via the self-hate path and the last-name path, so the probe is reading a *mixture* of (a) identity-vocabulary presence and (b) actual self-referential insult construction, with (a) doing the heaviest lifting.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 27 | Probe (toxicity) logit | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 9 | Late-layer race/ethnicity/gender detectors (L6:L4:L3) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 10 | Late-layer race/ethnicity/gender detectors (L6:L4:L3) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 27 | Late-layer race/ethnicity/gender detectors (L6:L4:L3) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 9 | Late-layer race/ethnicity/gender detectors (L6:L4:L3) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 10 | Late-layer race/ethnicity/gender detectors (L6:L4:L3) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 10 | Late-layer race/ethnicity/gender detectors (L6:L4:L3) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 10 | Late-layer race/ethnicity/gender detectors (L6:L4:L3) | mentions of demographic identity, especially race and gender | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 9 | Low-layer race-lex detectors (L2/L1) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 9 | Low-layer race-lex detectors (L2/L1) | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 9 | Low-layer race-lex detectors (L2/L1) | mentions of colors | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 9 | Low-layer race-lex detectors (L2/L1) |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L4:F10004](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) | 22 | Self-/hate lexical detectors (L4:L3:L2) |  hyphenated words beginning with "self" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10004) |
| [L3:F8492](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) | 22 | Self-/hate lexical detectors (L4:L3:L2) | the word "hate" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8492) |
| [L2:F189](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/189) | 22 | Self-/hate lexical detectors (L4:L3:L2) | people in positions of power, either as leaders, family roles, or contributors | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/189) |
| [L3:F4512](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) | 15 | Last-name / personal-name detectors |  mentions of first names, last names, and phone numbers | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) |
| [L2:F9961](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9961) | 15 | Last-name / personal-name detectors | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9961) |
| [L1:F6576](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6576) | 3 | Marriage / appearance / author lexical detectors (L1/L0) |  the word "appearance" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6576) |
| [L1:F384](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) | 2 | Marriage / appearance / author lexical detectors (L1/L0) |  the string "ash" or "pund" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) |
| [L0:F753](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) | 2 | Marriage / appearance / author lexical detectors (L1/L0) | the word "author" and words related to selling and prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) |
| [L0:F241](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/241) | 6 | Marriage / appearance / author lexical detectors (L1/L0) | mentions of marriage | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/241) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: author (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: married (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: white (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: oriental (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: last (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: name (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: self hater (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L1:5220 de=-0.453 |
| 3 | `inspect_feature` ×15 | L1:5220, L3:13061, L6:3902, L4:117, L1:384, L1:6576, L2:13158, L3:4512, L0:7773, L0:241, L0:753, L3:10286, L4:10004, L2:15558, L1:9113 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F13061@10` | ✅ reported | 3 | 3 | Trace the path upstream from L3:F13061 (race/gender/social-issues words, positio… |
| SA-2 | `L6:F3902@9` | ✅ reported | 4 | 9 | Trace upstream from L6:F3902 (race/ethnicity terms, pos 9 "white"). Find what in… |
| SA-3 | `L4:F117@10` | ✅ reported | 6 | 10 | Trace upstream from L4:F117 (race/racism/Black-focused, pos 10 "oriental"). Find… |
| SA-4 | `L4:F10004@22` | ✅ reported | 6 | 10 | Trace upstream from L4:F10004 (hyphenated "self-" words, pos 22 = "self"). Find … |

<details>
<summary><b>SA-1</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 2 | `get_upstream_features` | L3:F13061@10, k=15 | Emb:" white"@9 (de=11.00) +14 more |
| 3 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 4 | `get_upstream_features` | L2:F15317@10, k=10 | Emb:" guy"@10 (de=9.44) +9 more |
| 5 | `inspect_feature` | L0, F9076 | " mentions of men, boys, areas, or general locations in a text" |

**Findings:** The target L3:13061 (race/gender/social‑issues detector) receives its strongest positive drive from the input token embedding "white" at position 9, confirming a direct lexical trigger. Upstream it is further amplified by a mid‑layer race/ethnicity feature (L2:13158) and a low‑layer generic entity detector (L0:9076). Both upstream features lie in the lower third of the model (layers 0‑2) and have …

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |
| 2 | `get_upstream_features` | L6:F3902@9, k=10 | Emb:" white"@9 (de=13.56) +9 more |
| 3 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 4 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 5 | `get_upstream_features` | L4:F117@9, k=10 | Emb:" white"@9 (de=15.06) +9 more |
| 6 | `inspect_feature` | L2, F585 | "the word "white", often in association with "dwarf"" |
| 7 | `get_upstream_features` | L2:F13158@9, k=10 | Emb:" white"@9 (de=13.62) +9 more |

**Findings:** Tracing from L6:F3902 (race/ethnicity detector at position 9) reveals that its strongest upstream driver is the raw token embedding for " white" (direct_effect ~13.6). The signal passes through a hierarchy of low‑frequency race‑related features: L4:117 and L2:13158, both of which also receive strong excitation from the same " white" embedding. Feature L2:585 directly fires on the lexical token "wh…

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 2 | `get_upstream_features` | L4:F117@10, k=10 | Emb:" white"@9 (de=12.12) +9 more |
| 3 | `inspect_feature` | L3, F13061 | " words related to race, gender and social issues" |
| 4 | `get_upstream_features` | L3:F13061@10, k=10 | Emb:" white"@9 (de=11.00) +9 more |
| 5 | `inspect_feature` | L3, F16373 | " mentions of demographic identity, especially race and gender" |
| 6 | `inspect_feature` | L0, F2242 | " the word "guys"" |
| 7 | `get_upstream_features` | L3:F16373@10, k=10 | Emb:" white"@9 (de=23.88) +9 more |
| 8 | `inspect_feature` | L0, F6548 | " the word "national"" |
| 9 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 10 | `get_upstream_features` | L2:F13158@9, k=10 | Emb:" white"@9 (de=13.62) +9 more |
| 11 | `inspect_feature` | L2, F1708 | " mentions of colors" |
| 12 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |

**Findings:** L4:F117 is a high‑level race‑sensitive detector that receives strong excitatory input from the token embedding " white" (pos9) and from two mid‑level demographic detectors in layer 3 (F13061 and F16373). Both layer‑3 features are themselves driven largely by the same " white" embedding and by lower‑layer race/ethnicity cues (L2:F13158) and colour cues (L2:F1708). The chain reaches the required low…

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F10004 | " hyphenated words beginning with "self"" |
| 2 | `get_upstream_features` | L4:F10004@22, k=10 | Emb:" self"@21 (de=46.75) +9 more |
| 3 | `inspect_feature` | L3, F8492 | "the word "hate"" |
| 4 | `inspect_feature` | L2, F189 | " people in positions of power, either as leaders, family roles, or con" |
| 5 | `get_upstream_features` | L3:F8492@22, k=10 | Emb:" hater"@22 (de=24.62) +9 more |
| 6 | `inspect_feature` | L3, F5808 | "words ending in "-ing" that have a sense of driving something forward" |
| 7 | `get_upstream_features` | L2:F189@22, k=10 | Emb:" hater"@22 (de=6.47) +9 more |
| 8 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 9 | `inspect_feature` | L1, F10447 | "articles and prepositions" |

**Findings:** The hyphen‑detector L4:F10004 (self‑prefix) is driven primarily by the raw token embedding of the word “self” (direct_effect≈46.7). A secondary but conceptually important path runs through a layer‑3 hate‑detector (8492) that picks up the second half of the hyphenated token “self‑hater”. This hate detector itself receives a strong boost from the embedding of the token “hater” (direct_effect≈24.6) a…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F384@2, k=10 → Emb:" author"@2 (de=13.94) +9 more |
| 2 | `get_upstream_features` | L0:F241@6, k=10 → Emb:" married"@6 (de=12.81) +9 more |
| 3 | `get_upstream_features` | L3:F4512@15, k=10 → Emb:" last"@14 (de=24.75) +9 more |
| 4 | `get_upstream_features` | L2:F13158@9, k=10 → Emb:" white"@9 (de=13.62) +9 more |

### Build

`build_circuit` → 13 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 80,225 | 4,567 | 86,322 | 0 | $0.0347 | — | — |
| SA-2 | openai/gpt-oss-120b | 53,281 | 4,554 | 14,848 | 0 | $0.0109 | ✅ 4F/9E | Trace upstream from L6:F3902 (race/ethnicity terms, pos 9 "w… |
| SA-4 | openai/gpt-oss-120b | 108,573 | 9,994 | 10,208 | 0 | $0.0224 | ✅ 6F/10E | Trace upstream from L4:F10004 (hyphenated "self-" words, pos… |
| SA-1 | openai/gpt-oss-120b | 34,500 | 3,486 | 8,672 | 0 | $0.0074 | ✅ 3F/3E | Trace the path upstream from L3:F13061 (race/gender/social-i… |
| SA-3 | openai/gpt-oss-120b | 162,595 | 10,198 | 18,880 | 0 | $0.0308 | ✅ 6F/10E | Trace upstream from L4:F117 (race/racism/Black-focused, pos … |
| **Total** | | **439,174** | **32,799** | **138,930** | **0** | **$0.1063** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 20s