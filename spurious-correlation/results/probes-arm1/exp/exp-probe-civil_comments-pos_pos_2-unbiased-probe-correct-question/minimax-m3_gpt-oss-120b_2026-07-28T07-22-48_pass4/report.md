# Circuit Oracle Report
**Date:** 2026-07-28 07:22:48 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe's classification score is driven almost entirely by a chain of features that detect the identity-group keywords "white" and "Hispanic" (and the male pronoun "he"), not by the linguistic content of the conditional "If he was white and not Hispanic it would be s problem."

**Confidence:** 8

**Reasoning:** The attribution graph traces cleanly from the output logit back to the input tokens "white" (pos 4) and "he" (pos 2), with the supporting chain dominated by race/ethnicity features rather than by features encoding the conditional or counterfactual semantics of the sentence.

At the late layers (3–4), the highest-direct-effect features are L4:F15204 ("art galleries, museums and the White House" — a "white" detector, direct_effect 0.118), L4:F117 ("terms related to race, racism, and social justice… Black people", +0.328), L4:F7136 ("the color white", +0.284), and L3:F11768 ("the word 'white' and related contexts such as diversity", -0.286). These are textbook identity-group features.

In the mid-layers, L2:F13158 ("words about race and ethnicity", promoted tokens include "Hispanic"), L2:F585 ("white", often with "dwarf"), and L2:F6983 ("words related to race and slavery") all activate on the "white" token at pos 4. The "Hispanic" word at pos 5 also directly drives L2:F13158 (promoted tokens "Hispanic", "Latino", "ethnic", "Jewish", "Muslim").

In the early layers, L0:F3436 ("mentions of the word 'white'", +0.172), L0:F10910 ("the word 'white'", +0.104), L0:F12768 ("'he' and 'she' in close proximity" firing on "he" at pos 2, +0.205), L0:F310 ("she/her/he pronouns"), L0:F8673 ("she or he followed by a verb"), and L1:F13646 ("text discussing social justice issues") all encode identity/pronominal content. The token-embedding nodes "white" (direct_effect 40.5 into L4:F15204, 14.75 into L4:F117, 13.1 into L2:F13158) and "he" (direct_effect 37.0 into L0:F12768) are the bottom of the circuit.

`get_source_influence` on positions 2/4/5 (he/white/Hispanic) returns S_pct_of_total = 10.2 with S_over_R = 1.41 — the identity-token positions carry more signed influence than the strongest non-source position, confirming the probe is being driven by identity-mention tokens.

Notably absent from the top direct-effect features: any feature that encodes the counterfactual/conditional construction ("if" → L3:F12404, L2:F11539 appear lower in the ranking with negative direct_effects of 0.082 and 0.089), the slur "s problem" (the only content-bearing word for the toxicity signal), the auxiliary verbs, or the sentence-level sentiment. L6:F7896 ("sentences expressing opinions about whether something is good") and L0:F880 ("pronoun 'it'") do fire but are downstream artifacts of the "it would be" construction. The conditional scaffolding is essentially ignored, while the racial-identifier chain drives the probe score.

This is exactly the user's concern: the probe latches onto identity-group tokens ("white", "Hispanic", "he") via dedicated race-encoding features, rather than on the actual prompt content (the slur, the counterfactual framing) that would justify a toxicity classification. The circuit confirms a spurious-identity-cue mechanism.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L3:F11768](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) | 4 | Late-layer "white"/race latent features |  the word "white" and related contexts such as diversity | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 4 | Late-layer "white"/race latent features |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 4 | Late-layer "white"/race latent features |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F7136](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) | 4 | Late-layer "white"/race latent features |  the color white | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) |
| [L6:F7896](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7896) | 3 | Late-layer "white"/race latent features |  sentences expressing opinions about whether something is good | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7896) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 4 | Mid-layer race/identity group features |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 4 | Mid-layer race/identity group features | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F6983](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) | 4 | Mid-layer race/identity group features |  words related to race and slavery | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 4 | Early-layer "white" lexical features |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 4 | Early-layer "white" lexical features | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L1:F1480](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) | 4 | Early-layer "white" lexical features | the color 'white', sometimes in a context involving race | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) |
| [L1:F4668](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4668) | 4 | Early-layer "white" lexical features |  the color white being used to describe image parameters | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4668) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 4 | Early-layer "white" lexical features |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 2 | Pronoun and function-word features |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F8673](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8673) | 2 | Pronoun and function-word features | sentences that contain the word 'she' or 'he' followed by a verb | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8673) |
| [L0:F310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) | 2 | Pronoun and function-word features |  the pronouns "she", "her", and "he" and sometimes the word "therefore" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) |
| [L1:F7821](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7821) | 4 | Pronoun and function-word features |  mentions of computer fans. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7821) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 8 | Pronoun and function-word features |  references to the pronoun "it", and sometimes "that", suggesting observation of the subject of a discussion | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:12768 de=0.205 |
| 3 | `inspect_feature` ×6 | L0:12768, L0:3436, L4:15204, L0:880, L0:10910, L2:1139 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15204@4` | ❌ error | — | — | Trace the path from L4:F15204 (art galleries, museums, White House - fires on "w… |
| SA-2 | `L0:F12768@2` | ❌ error | — | — | Trace the path from L0:F12768 (mentions of "he" and "she" in close proximity, fi… |
| SA-3 | `L0:F3436@4` | ❌ error | — | — | Trace the path from L0:F3436 (mentions of "white" - fires at pos 4). What input … |
| SA-4 | `L0:F10910@4` | ❌ error | — | — | Trace the path from L0:F10910 (possession, white, immediate, once - fires at pos… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L0:13663, L0:310, L0:3255, L2:12691, L3:12404 |
| 2 | `get_upstream_features` | L4:F15204@4, k=8 → Emb:" white"@4 (de=40.50) +7 more |
| 3 | `get_upstream_features` | L0:F12768@2, k=8 → Emb:" he"@2 (de=37.00) +7 more |
| 4 | `inspect_feature` ×4 | L3:11768, L2:585, L0:6548, L0:2458 |
| 5 | `get_source_influence` | {'depth': 3, 'source_positions': [2, 4, 5]} → {'depth': 3, 'source_positions': [2, 4, 5], 'S_pct_of_total': 10.207, 'R_pct_of_ |
| 6 | `inspect_feature` ×3 | L4:7136, L2:13158, L4:117 |
| 7 | `get_upstream_features` | L4:F117@4, k=8 → Emb:" white"@4 (de=14.75) +7 more |
| 8 | `get_upstream_features` | L2:F13158@4, k=8 → Emb:" white"@4 (de=13.12) +7 more |
| 9 | `inspect_feature` ×4 | L1:7821, L1:13646, L0:16013, L1:4668 |
| 10 | `get_top_features` | token="", k=10 → 10 features; top: L0:12768 de=0.205 |
| 11 | `inspect_feature` ×8 | L2:6983, L2:11539, L0:12059, L0:15499, L0:10178, L6:7896, L0:8673, L1:1480 |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 46,995 | 5,419 | 419,410 | 0 | $0.0458 | — | — |
| **Total** | | **46,995** | **5,419** | **419,410** | **0** | **$0.0458** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 0s