# Circuit Oracle Report
**Date:** 2026-07-28 07:20:53 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven primarily by lexical identity-token features (multiple "white"-detector features at L0–L4) acting on the input token "white" at position 4, supplemented by generic function-word/pronoun detectors — not by any semantic or compositional understanding of the conditional-frame toxicity in the prompt.

**Confidence:** 7

**Reasoning:**

The attribution graph for this toxicity probe is almost entirely driven by **identity-token / lexical detectors**, exactly the pattern the user suspected.

**The dominant signal chain (pushes the probe toward "toxic"):**
- **Emb: white (pos 4)** activates multiple "white"-detecting features at the embedding layer with very large direct effects:
  - **L0:F3436** "mentions of the word 'white'" — direct_effect 0.172, activation 15.25. This feature's top activating examples are explicitly race-discussion contexts (black/white wage gaps, racial slurs, slavery debates) — i.e., it has learned the *co-occurrence* of "white" with toxic racial discourse.
  - **L0:F10910** "the words 'white', 'possession', 'immediate' and 'once' regardless of context" — direct_effect 0.104. Despite the "regardless of context" label, its exemplars cluster around legal/criminal-possession language co-occurring with "white" in racially charged text.
  - **L4:F15204** "art galleries, museums and the White House" — direct_effect 0.118. Although labeled with non-racial examples, the top activating tokens are `White`/`white` and the exemplars include explicitly racial content.
  - **L1:F1480** "the color 'white', sometimes in a context involving race" (frac_nonzero 0.004, very selective) and **L4:F7136** "the color white" (frac_nonzero 0.003, very selective) — both pure lexical detectors with race-heavy exemplars.

These features are the four largest positive contributors to the probe (de 0.172, 0.118, 0.104, plus L0:880 "it/that" reference at de 0.114 and L0:F12768 "he/she in proximity" at de 0.205 — both pushed by `Emb: he` and `Emb: it`). Their **upstream traces confirm they are anchored to single token embeddings** (`white` at pos 4 with direct_effect 18, `he` at pos 2 with de 37, `it` at pos 8 with de 42.5) — not to compositional context.

**The counter-signal (pushes probe away from "toxic"):**
- **L2:F6983** "words related to race and slavery" (direct_effect -0.093) fires on the *same* "white" token but pushes the probe *away* from toxic. This is the only feature that actually *integrates* identity words with broader racial-discourse context (its top examples are extended discussions of slavery, racial violence). Its strong suppression here is exactly the mechanism by which a real "understands racial content" feature would temper the surface-level identity-token response — but its magnitude is smaller than the combined identity-token push.

**What's notably absent:** No features encode the conditional-hypothetical structure ("If he was white and not Hispanic it would be a problem"), the harm-implicating verb "would be a problem," the counterfactual framing, or any semantic understanding of *why* this sentence is or isn't toxic. The mid-layer features (**L2:F1139** "so/come", **L2:F11539** "if", **L3:F12404** "if") are shallow function-word detectors (frac_nonzero 0.001–0.012) carrying small effects.

**Conclusion on the user's concern:** The user is correct. The probe's classification is being driven by a **bag of identity-token and pronoun detectors** (L0–L4, all anchored to embedding nodes for `white`, `he`, `it`, `Hispanic`) rather than by any compositional semantic analysis of the prompt. The most harmful finding is that L0:F3436 — the single largest positive contributor — has been trained (per its top activating examples) on text that *co-occurs* "white" with racially toxic language, so it fires a toxic signal on *any* mention of "white," regardless of the actual sentence meaning. This is the textbook "identity group" spurious feature the user identified: presence of a demographic-identity word alone is sufficient to drive the probe, and the *content* of the toxicity (the conditional "it would be a problem" clause) is not represented anywhere in the active circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 15 | probe logit (toxicity) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 4 | Identity-token / lexical-race features at late layers |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L1:F1480](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) | 4 | Identity-token / lexical-race features at late layers | the color 'white', sometimes in a context involving race | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) |
| [L4:F7136](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) | 4 | Identity-token / lexical-race features at late layers |  the color white | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 4 | Lexical 'white' features (L0) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 4 | Lexical 'white' features (L0) | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L0:F12059](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12059) | 4 | Lexical 'white' features (L0) |  words related to purpose and intent | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12059) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 2 | Other lexical / function-word features (L0) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 8 | Other lexical / function-word features (L0) |  references to the pronoun "it", and sometimes "that", suggesting observation of the subject of a discussion | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |
| [L0:F310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) | 2 | Other lexical / function-word features (L0) |  the pronouns "she", "her", and "he" and sometimes the word "therefore" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 5 | Other lexical / function-word features (L0) |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F13663](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13663) | 4 | Other lexical / function-word features (L0) | mentions of pregnancy and related terms | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13663) |
| [L2:F1139](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) | 3 | Conditional / function-word features (L2-L3) |  various usages of the word "so", as well as some instances of the word "come" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) |
| [L2:F11539](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11539) | 1 | Conditional / function-word features (L2-L3) | the word "if" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11539) |
| [L3:F12404](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12404) | 1 | Conditional / function-word features (L2-L3) |  instances of the conditional word "if" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12404) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: white (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: he (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: was (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: If (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: and (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: it (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: Hispanic (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:12768 de=0.205 |
| 3 | `inspect_feature` ×15 | L0:12768, L0:3436, L0:880, L0:13663, L4:15204, L2:1139, L0:3255, L0:10910, L2:6983, L1:1480, L0:310, L4:7136, L0:12059, L2:11539, L3:12404 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15204@4` | ❌ error | — | — | Trace from L4:F15204 (art galleries/White House) at pos 4 (the word 'white'). De… |
| SA-2 | `L2:F6983@4` | ❌ error | — | — | Trace from L2:F6983 (race/slavery) at pos 4. This feature pushes the probe AWAY … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L0, F3436 → " mentions of the word "white"" |
| 2 | `get_upstream_features` | L0:F3436@4, k=10 → Emb:" white"@4 (de=18.00) +9 more |
| 3 | `get_upstream_features` | L0:F12768@2, k=10 → Emb:" he"@2 (de=37.00) +9 more |
| 4 | `get_upstream_features` | L0:F880@8, k=10 → Emb:" it"@8 (de=42.50) +9 more |
| 5 | `get_upstream_features` | L2:F1139@3, k=10 → Emb:"If"@1 (de=27.62) +9 more |
| 6 | `get_upstream_features` | L4:F15204@4, k=10 → Emb:" white"@4 (de=40.50) +9 more |
| 7 | `get_upstream_features` | L3:F12404@1, k=8 → Emb:"If"@1 (de=15.75) +7 more |
| 8 | `get_upstream_features` | L0:F10910@4, k=8 → Emb:" white"@4 (de=14.56) +7 more |
| 9 | `inspect_feature` ×5 | L0:2303, L0:2458, L2:6983, L0:3255, L2:11539 |
| 10 | `get_upstream_features` | L0:F12768@2, k=5 → Emb:" he"@2 (de=37.00) +4 more |
| 11 | `get_upstream_features` | L0:F310@2, k=5 → Emb:" he"@2 (de=10.00) +4 more |
| 12 | `get_upstream_features` | L2:F1139@3, k=5 → Emb:"If"@1 (de=27.62) +4 more |
| 13 | `get_upstream_features` | L0:F3255@5, k=5 → Emb:" and"@5 (de=35.75) +4 more |
| 14 | `get_upstream_features` | L0:F10910@4, k=5 → Emb:" white"@4 (de=14.56) +4 more |

### Build

`build_circuit` → 12 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 56,758 | 6,843 | 272,782 | 0 | $0.0416 | — | — |
| **Total** | | **56,758** | **6,843** | **272,782** | **0** | **$0.0416** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 23s