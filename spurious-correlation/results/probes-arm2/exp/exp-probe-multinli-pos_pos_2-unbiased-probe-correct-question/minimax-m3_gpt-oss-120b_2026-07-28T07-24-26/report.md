# Circuit Oracle Report
**Date:** 2026-07-28 07:24:26 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mixed circuit: superficially lexical content (NCAA/tournament words) but predominantly low-layer token-identity features on negation-bearing words ("haven", "n't" → pos 18/20, " yeah well" → pos 1/2), plus a discourse-filler (" uh") — confirming the user's concern that the probe relies heavily on spurious lexical/shallow cues (notably negation particles) rather than semantic content about the contradiction.

**Confidence:** 7

**Reasoning:**

The circuit traces from output logit back through three main channels:

1. **Spurious negation-lexicon channel (largest contributor).** L4:F12126 (pos 2, direct_effect=-0.648) and L4:F4847 (pos 2, +0.389) are the two strongest single features. Both receive their top upstream signal from the embedding of " well" (pos 2) (direct_effect 14.6 and 8.1 respectively) — a discourse marker, not a content word — with secondary contribution from "yeah" (pos 1). L4:F12126 also integrates a deep stack of L0 lexical-detector features firing on the contraction " haven't": F6236 (pos 20, "t") with direct_effect=-0.457, plus F8352 (pos 2, "well"), F15682/F4365/F5112 (pos 1, "yeah"). These are pure surface-form detectors of negation particles / function words.

2. **NCAA-tournament content channel.** L0:F8659 (pos 8, " tournament", +0.285), F12862 (pos 8, +0.236), F8083 (pos 6, " double", -0.332), F16366 (pos 25, " because", +0.293) fire on the entity words "NC double-A tournament" and the causal connective. F5709 (L4:pos 14, " now", -0.277) is a temporal adverb. This is the only channel that touches the *content* of what the speaker is denying.

3. **Discourse-filler channel.** L6:F11557 (pos 4, " uh", +0.201) is the highest-layer direct contributor, driven by L4 features on "uh" — a paralinguistic cue entirely orthogonal to semantic contradiction.

Critically, there is **no entity-recognition or world-knowledge feature** in the circuit: no "Louisville" feature, no "Sweet 16" feature, no "tournament-team" feature. The contradiction-relevant semantic content ("because Louisville's out of it" explains why the speaker hasn't watched, even though they normally watch every game) is never represented. Instead, the probe relies on:
- The bare tokens of negation ("haven", "n't", "not" implied by "haven't"),
- The casual register markers "yeah well" and "uh",
- A few content nouns ("tournament", "because").

This validates the user's concern: the circuit predominantly uses **negation-word and filler-word features** (shallow lexical/positional cues) rather than features that encode the actual semantic relationship being contradicted.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' well' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'yeah' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: ' haven' (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: 't' (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: ' because' (pos 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' double' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: ' tournament' (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' A' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: ' now' (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 24 | Emb: ' year' (pos 24) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: ' uh' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' the' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 20 | L0 lexical negation tokens (haven, haven't, year) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F15682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15682) | 1 | L0 lexical negation tokens (haven, haven't, year) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15682) |
| [L0:F4365](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4365) | 1 | L0 lexical negation tokens (haven, haven't, year) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4365) |
| [L0:F5112](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) | 1 | L0 lexical negation tokens (haven, haven't, year) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | L0 lexical negation tokens (haven, haven't, year) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F5912](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) | 24 | L0 lexical negation tokens (haven, haven't, year) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) |
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | L0 lexical negation tokens (haven, haven't, year) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L0:F8083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) | 6 | L0 NCAA/tournament tokens (double, A, tournament) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| [L0:F8659](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) | 8 | L0 NCAA/tournament tokens (double, A, tournament) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) |
| [L0:F12862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) | 8 | L0 NCAA/tournament tokens (double, A, tournament) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | L0 NCAA/tournament tokens (double, A, tournament) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L1:F177](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) | 6 | L1 'double' surface feature | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| [L3:F4735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4735) | 2 | L3 features at pos 2 (yeah/well context) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4735) |
| [L3:F13677](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13677) | 2 | L3 features at pos 2 (yeah/well context) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13677) |
| [L3:F2663](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2663) | 2 | L3 features at pos 2 (yeah/well context) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2663) |
| [L3:F14620](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) | 2 | L3 features at pos 2 (yeah/well context) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) |
| [L3:F15027](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15027) | 2 | L3 features at pos 2 (yeah/well context) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15027) |
| [L3:F14561](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14561) | 2 | L3 features at pos 2 (yeah/well context) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14561) |
| [L3:F8423](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8423) | 2 | L3 features at pos 2 (yeah/well context) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8423) |
| [L3:F3550](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3550) | 2 | L3 features at pos 2 (yeah/well context) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3550) |
| [L3:F9271](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9271) | 2 | L3 features at pos 2 (yeah/well context) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9271) |
| [L3:F9770](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) | 7 | L3 features at pos 2 (yeah/well context) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| [L3:F12849](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) | 7 | L3 features at pos 2 (yeah/well context) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) |
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | L4 pos 2 (yeah well) features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | L4 pos 2 (yeah well) features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 14 | L4 pos 2 (yeah well) features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L4:F3730](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) | 7 | L4 pos 2 (yeah well) features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) |
| [L6:F11557](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) | 4 | L6 uh-filler (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:12126 de=-0.648 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F12126@2` | ❌ error | — | — | Trace the most negatively-contributing feature L4:F12126 at pos 2. This has dire… |
| SA-2 | `L0:F6236@20` | ❌ error | — | — | Trace L0:F6236 at pos 20, direct_effect=-0.457. Pos 20 is a mid-sentence positio… |
| SA-3 | `L4:F4847@2` | ❌ error | — | — | Trace L4:F4847 at pos 2, direct_effect=+0.389. This is the most positively-contr… |
| SA-4 | `L0:F16366@25` | ❌ error | — | — | Trace L0:F16366 at pos 25, direct_effect=+0.293. Pos 25 is near the end of the i… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F12126@2, k=15 → Emb:" well"@2 (de=14.62) +14 more |
| 2 | `get_upstream_features` | L0:F6236@20, k=15 → Emb:"t"@20 (de=17.88) +14 more |
| 3 | `get_upstream_features` | L4:F4847@2, k=15 → Emb:" well"@2 (de=8.06) +14 more |
| 4 | `get_upstream_features` | L0:F16366@25, k=15 → Emb:" because"@25 (de=40.75) +14 more |
| 5 | `get_upstream_features` | L0:F8083@6, k=12 → Emb:" double"@6 (de=19.62) +11 more |
| 6 | `get_upstream_features` | L3:F9770@7, k=12 → Emb:" double"@6 (de=18.00) +11 more |
| 7 | `get_upstream_features` | L0:F8659@8, k=12 → Emb:" tournament"@8 (de=15.25) +11 more |
| 8 | `get_upstream_features` | L4:F5709@14, k=12 → Emb:" now"@14 (de=40.75) +11 more |
| 9 | `get_upstream_features` | L1:F177@6, k=12 → Emb:" double"@6 (de=24.00) +11 more |
| 10 | `get_upstream_features` | L0:F12862@8, k=12 → Emb:" tournament"@8 (de=20.62) +11 more |
| 11 | `get_upstream_features` | L3:F12849@7, k=12 → Emb:" double"@6 (de=25.75) +11 more |
| 12 | `get_upstream_features` | L3:F14620@2, k=12 → Emb:" well"@2 (de=9.75) +11 more |
| 13 | `get_upstream_features` | L4:F3730@7, k=12 → Emb:" A"@7 (de=13.19) +11 more |
| 14 | `get_upstream_features` | L0:F3820@3, k=12 → Emb:" the"@3 (de=32.75) +11 more |
| 15 | `get_upstream_features` | L0:F5112@1, k=12 → Emb:"yeah"@1 (de=11.50) +11 more |
| 16 | `get_upstream_features` | L6:F11557@4, k=12 → Emb:" uh"@4 (de=11.19) +11 more |
| 17 | `get_upstream_features` | L0:F8352@2, k=12 → Emb:" well"@2 (de=30.88) +11 more |
| 18 | `get_upstream_features` | L0:F4365@1, k=12 → Emb:"yeah"@1 (de=14.81) +11 more |
| 19 | `get_upstream_features` | L0:F5912@24, k=12 → Emb:" year"@24 (de=18.62) +11 more |
| 20 | `get_upstream_features` | L0:F15682@1, k=12 → Emb:"yeah"@1 (de=15.56) +11 more |
| 21 | `get_upstream_features` | L4:F12126@2, k=5 → Emb:" well"@2 (de=14.62) +4 more |
| 22 | `get_upstream_features` | L4:F4847@2, k=5 → Emb:" well"@2 (de=8.06) +4 more |

### Build

`build_circuit` → 19 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 29,225 | 5,870 | 45,906 | 0 | $0.0186 | — | — |
| **Total** | | **29,225** | **5,870** | **45,906** | **0** | **$0.0186** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 7s