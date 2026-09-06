# Circuit Oracle Report
**Date:** 2026-07-28 07:23:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven almost entirely by the presence of identity-group words — particularly the token "white" and, to a lesser extent, "he" and "If" — with no feature in the circuit actually encoding the toxic content of the statement (the conditional framing, the negation, or the slur-like subject matter).

**Confidence:** 8

**Reasoning:** The attribution graph is remarkable for what is *absent* rather than what is present. Of the ~20 top features driving the probe score, every single one is a generic lexical/syntactic detector:

- **Identity-word detectors dominate the top of the ranking.** The #1 feature (L0:F12768, "he/she in close proximity," direct_effect=+0.205), the #2 feature (L0:F3436, "mentions of the word 'white'," +0.172), the #4 feature (L4:F15204, "art galleries, museums and the White House," +0.118), the #5 feature (L0:F880, "the pronoun 'it'"), the #9 feature (L0:F310, "pronouns she/her/he," -0.089), and the #13 feature (L4:F7136, "the color white," -0.083) all activate on demographic-identity tokens ("white", "he") with no reference to the surrounding semantic context.
- **The two strongest promoters of the probe direction are the pronouns "he" (pos 2) and the word "white" (pos 4) — but framed as lexical identity mentions, not as components of a biased statement.** F3436's top-activating examples show the "white" detector firing on sentences about wages, discrimination, and racial discussion generally, with no discrimination between neutral and hateful uses. F15204 ("White House") and F7136 ("the color white") are even more clearly content-agnostic lexical detectors.
- **Tracing upstream confirms the circuit bottoms out on raw token embeddings, not on toxicity-relevant reasoning.** Both L4:F15204 and L4:F7136 receive their dominant direct_effect (40.5 and 43.5 respectively) from the **Emb: white (pos 4)** node directly. L3:F12404 ("conditional word 'if'") receives its full signal (15.75) from **Emb: If (pos 1)**. L2:F1139 ("so/come") receives 27.6 from **Emb: If (pos 1)** and 21.4 from **Emb: was (pos 3)**. The signal flow is: token-embedding → lexical identity detector → probe direction, with no intermediate feature encoding the *meaning* of the sentence (e.g., a feature for "counterfactual racial bias", "would-be-problem framing", or "racial slur + negation").
- **The only contextually-interesting features fire in the wrong direction.** L2:F6983 ("words related to race and slavery," -0.093 at pos 4) and L1:F1480 ("color 'white', sometimes in a context involving race," -0.084) *suppress* the probe score — they fire on the race-relevant semantic content of the prompt but push the probe *away* from toxicity. The "inhibitory at this pos" L2 node actually inhibits the L4 museum/whitehouse and L4 color-white features, so the race-semantic content is being filtered out before reaching the probe.
- **The negation/hypothetical structure is captured only by shallow, generic features.** "If" appears as L2:F11539 and L3:F12404, both pure "the word 'if'" detectors with no sensitivity to whether the conditional is benign or hateful. The final "s" (in "s problem", a possible typo for "a problem") triggers F15499 ("the letter 's' followed by a non-whitespace character"), a pure orthographic feature that contributes nothing semantic.

This is exactly the failure mode the user suspected: **the toxicity probe reads off an "identity group" axis rather than a "toxic content" axis.** The model has features (F6983, F1480) that *do* encode race-related semantic content, but they push the probe in the *non-toxic* direction here, while the lexical identity detectors (F3436, F15204, F7136, F12768) — which fire on the same words regardless of context — drive the probe toward the toxic classification. The result is that a sentence like "If he was white and not Hispanic it would be a problem" (which is itself a sentence about racial bias) is scored as toxic primarily because it contains the words *white* and *he*, not because the model has identified any toxic *content*. This is a textbook spurious-correlation probe: the classification direction aligns with lexical identity-term statistics in the training data rather than with any semantic notion of harm.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 4 | L0: 'mentions of "white"' |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 4 | L0: 'possession, white, immediate, once' | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L0:F12059](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12059) | 4 | L0: 'words related to purpose and intent (objective)' |  words related to purpose and intent | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12059) |
| [L0:F8673](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8673) | 2 | L0: 'sentences that contain she/he followed by a verb' | sentences that contain the word 'she' or 'he' followed by a verb | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8673) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 2 | L0: 'mentions of he/she in close proximity' |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F15499](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15499) | 11 | L0: 'letter s followed by a non-whitespace character' | the letter "s" followed by a non-whitespace character | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15499) |
| [L1:F1480](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) | 4 | L1: "color 'white', sometimes in a context involving race" | the color 'white', sometimes in a context involving race | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) |
| [L2:F6983](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) | 4 | L2: 'words related to race and slavery' (inhibitory at this pos) |  words related to race and slavery | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) |
| [L2:F1139](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) | 3 | L2: "various usages of the word 'so' / 'come'" |  various usages of the word "so", as well as some instances of the word "come" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) |
| [L2:F11539](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11539) | 1 | L2: 'the word if' | the word "if" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11539) |
| [L2:F12691](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12691) | 8 | L2: 'programming/math contexts of showing, using, finding' |  programming or mathematics contexts of showing, using, finding, needing, letting, and being able to do something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12691) |
| [L3:F12404](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12404) | 1 | L3: 'conditional word if' |  instances of the conditional word "if" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12404) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 4 | L4: 'art galleries, museums and the White House' |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L4:F7136](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) | 4 | L4: 'the color white' |  the color white | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) |
| [L6:F7896](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7896) | 3 | L6: 'sentences expressing opinions about whether something is good' |  sentences expressing opinions about whether something is good | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7896) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:12768 de=0.205 |
| 3 | `inspect_feature` ×12 | L0:12768, L0:3436, L4:15204, L0:880, L0:13663, L0:10910, L2:1139, L4:7136, L0:3255, L3:12404, L2:12691, L0:10178 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15204@4` | ❌ error | — | — | Trace the path upstream from L4:F15204 (label: "art galleries, museums and the W… |
| SA-2 | `L4:F7136@4` | ❌ error | — | — | Trace upstream from L4:F7136 (label: "the color white", fires on "white" at pos … |
| SA-3 | `L3:F12404@1` | ❌ error | — | — | Trace upstream from L3:F12404 (label: "instances of the conditional word 'if'", … |
| SA-4 | `L2:F1139@3` | ❌ error | — | — | Trace upstream from L2:F1139 (label: "various usages of the word 'so'", fires at… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F15204@4, k=10 → Emb:" white"@4 (de=40.50) +9 more |
| 2 | `get_upstream_features` | L4:F7136@4, k=10 → Emb:" white"@4 (de=43.50) +9 more |
| 3 | `get_upstream_features` | L3:F12404@1, k=10 → Emb:"If"@1 (de=15.75) +9 more |
| 4 | `get_upstream_features` | L2:F1139@3, k=10 → Emb:"If"@1 (de=27.62) +9 more |
| 5 | `inspect_feature` ×8 | L1:1480, L0:15499, L0:8673, L0:12059, L0:310, L2:6983, L2:11539, L6:7896 |
| 6 | `get_upstream_features` | L0:F8673@2, k=5 → Emb:"If"@1 (de=8.31) +4 more |
| 7 | `get_upstream_features` | L0:F15499@11, k=5 → Emb:" s"@11 (de=17.62) +4 more |
| 8 | `get_upstream_features` | L0:F12059@4, k=5 → Emb:" white"@4 (de=13.69) +4 more |
| 9 | `get_upstream_features` | L2:F6983@4, k=5 → Emb:" white"@4 (de=8.19) +4 more |
| 10 | `get_upstream_features` | L1:F1480@4, k=5 → Emb:" white"@4 (de=15.75) +4 more |
| 11 | `get_upstream_features` | L6:F7896@3, k=5 → Emb:"If"@1 (de=14.38) +4 more |

### Build

`build_circuit` → 21 nodes, 40 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,290 | 7,249 | 215,965 | 0 | $0.0370 | — | — |
| **Total** | | **51,290** | **7,249** | **215,965** | **0** | **$0.0370** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 25s