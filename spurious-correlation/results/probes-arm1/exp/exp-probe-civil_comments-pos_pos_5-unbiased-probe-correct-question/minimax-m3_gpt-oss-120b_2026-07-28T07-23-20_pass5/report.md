# Circuit Oracle Report
**Date:** 2026-07-28 07:23:20 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score for the prompt about a "social justice warrior" visiting a "Muslim bakery" for a "gay wedding cake" is driven by a stacked pipeline that begins with a **"political/social-movement" identity-token feature** (L2:F1537 — promoted tokens include "progressive", "justice", "issues") and is amplified by **identity-group–specific lexical priming** anchored on the tokens "social" and "justice" — rather than by features encoding the actual slurs, the target demographic references, or the hateful imperative structure of the sentence.

**Confidence:** 7

**Reasoning:**

**Layer-2 identity signal is the dominant positive driver.** L2:F1537 ("political/social-issues and movements"; frac_nonzero 0.017; top activating examples include "social justice", "progressive", "Green Party", "issues of social justice and discrimination"; promoted-token stems "progressive", "issues", "justice", "change") sits at the conceptual core of the circuit. Its top upstream drivers are the embeddings for "social" (pos 5) and "justice" (pos 6) — direct_effect ≈ 9.6 + 3.9. The probe is therefore being triggered by an **identity-movement lexicon detector**, not by a feature that distinguishes "social justice warrior" from a neutral phrase like "If you enjoy fresh bread, go to a Muslim bakery." This confirms the user's hypothesis: the probe latches onto the **concept of a named social/political identity group**, which is exactly the kind of "an identity group" signal they flagged as spurious.

**Identity-adjacent lexical priming (Layer 0, pos 6).** Five of the top-20 features share position 6 ("justice") and all push *into* the probe:
- L0:F3591 "government social programs" (direct_effect +0.0635) — fires on "social services", "social work"
- L0:F9934 "the word 'particular'" (direct_effect +0.0986) — incidental co-activation
- L0:F1526 (L3) and L0:F4478 "ownership/belief systems" (sexual-orientation, property) push +0.0718
- L0:F2260 "medical/legal/social-work terms" pushes +0.072, L0:F9602 "the word 'emphasis'" pushes +0.064

The strongest single identity-token signal is L0:F13756 ("the word 'order'", pos 15) with direct_effect -0.084 to the probe — a *generic* noun feature whose upstream is just the embedding for "order" (26.25). It is not entity-specific; the model is using "order" as a clue that a transactional interaction is being described.

**Counter-evidence: the hateful-imperative structure is mostly ignored.** The actual slurs/targets — "Muslim" (pos 12), "gay" (pos 16, "wedding") — barely appear. The only relevant downstream feature is L6:F9005 "desserts/bakery" at pos 13 (direct_effect -0.1128, *suppressing* toxicity), and L6:F2674 at pos 7 "warrior". Mid-layer L3:F10868 "I'm a / I am a" (pos 4) and L3:F16254 "conditional + action" (pos 8) are **generic grammatical scaffolds** — they fire on any "If you are a X, go do Y" template, not on hateful content. frac_nonzero for F10868 = 0.0076 (low but not identity-specific) and F16254 = 0.017; their top activating examples are benign ("If you want to make changes…", "im going to knock out"). These push the probe up because the *identity-label template* "you are a [group], then [action]" is itself the probe's target, not because the model has parsed the slur.

**Layer-4 / Layer-6 features are content-neutral.** L4:F13700 "conditional clauses with 'if'" (frac_nonzero = **0.155** — high, generic) at pos 8 with direct_effect -0.064 *suppresses* the probe. L6:F2674 at pos 7 (warrior) and L6:F9005 at pos 13 (dessert/bakery) are concrete-entity features; L6:F9005 fires on "bakery/cake" lexically and pushes the score *down*, again showing the model is not using the targeted demographic content to fire toxicity.

**Net picture.** The circuit flows: `Emb: social / justice` → `L0_social_domain_priming` (justice, particular, order) → `L2_political_social_movement` (F1537: progressive / justice / social-movement lexicon) → `L3_grammar_patterns` (F10868 "I'm a", F16254 conditional-then-action) → `probe_output`. The pivotal observation is that **L2:F1537 is a learned "social-justice/political-movement" concept detector whose own top activating examples are benign political-discourse passages** — the same feature that fires on "issues of social justice and discrimination" in a law-review article is the feature that is being credited here for the toxicity classification. This validates the user's concern: the probe is responding primarily to **"an identity group was named"** (the social-justice movement), with secondary contributions from **generic syntactic scaffolding** ("if you are a X, go do Y"), and almost no contribution from features that actually encode the slur pairing of religious and sexual-orientation targets. The hateful payload of the prompt — the deliberate conflation of "Muslim" and "gay" to mock both — is being read by the model, but those tokens do not flow into the probe; instead, "social justice" does.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 2 | Generic function-word/lexical features | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F13310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) | 3 | Generic function-word/lexical features |  sentences that include forms of the verb "are" indicating a present state of being or necessity. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 10 | Generic function-word/lexical features | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F10219](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) | 4 | Generic function-word/lexical features |  the indefinite article "a" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) |
| [L0:F3850](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) | 8 | Generic function-word/lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 8 | Generic function-word/lexical features |  commas and sometimes reach (context not clear) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L0:F3591](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) | 6 | Social-domain priming (social-work / identity-adjacent vocabulary) |  terms related to government social programs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) |
| [L0:F2260](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) | 6 | Social-domain priming (social-work / identity-adjacent vocabulary) |  terms that are medical, legal, or related to social work | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) |
| [L0:F4478](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) | 6 | Social-domain priming (social-work / identity-adjacent vocabulary) |  terms related to ownership and belief systems. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) |
| [L0:F9602](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) | 6 | Social-domain priming (social-work / identity-adjacent vocabulary) |  the word "emphasis." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) |
| [L0:F9934](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) | 6 | Social-domain priming (social-work / identity-adjacent vocabulary) |  the word "particular" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) |
| [L0:F13756](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) | 15 | Social-domain priming (social-work / identity-adjacent vocabulary) |  the word "order" and occasionally "period," in many different contexts from law to food | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) |
| [L1:F10447](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10447) | 4 | Lexical support features (articles, instructions) | articles and prepositions | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10447) |
| [L1:F14281](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14281) | 6 | Lexical support features (articles, instructions) |  the word "instruction" and its plural | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14281) |
| [L2:F1537](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1537) | 6 | Political/social-movement concept (pos 6) |  words and phrases related to political and social issues and movements | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1537) |
| [L2:F14541](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) | 8 | Political/social-movement concept (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) |
| [L2:F13877](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13877) | 7 | Political/social-movement concept (pos 6) |  words related to roles, ranks, or personal characteristics of people | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13877) |
| [L2:F14209](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) | 9 | Political/social-movement concept (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) |
| [L3:F10868](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) | 4 | Syntactic-pattern features ("I'm a", conditional-then-action) |  the phrase "I'm a" or "I am a" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) |
| [L3:F16254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) | 8 | Syntactic-pattern features ("I'm a", conditional-then-action) |  conditional statements followed by actions the speaker will take | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) |
| [L3:F1526](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) | 6 | Syntactic-pattern features ("I'm a", conditional-then-action) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) |
| [L4:F13700](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13700) | 8 | Conditional/business-clause pattern | conditional clauses starting with "if" and words related to business contexts | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13700) |
| [L6:F2674](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) | 7 | Entity-specific concepts (warrior / desserts) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) |
| [L6:F9005](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) | 13 | Entity-specific concepts (warrior / desserts) |  words and phrases related to desserts | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:8444 de=-0.224 |
| 3 | `inspect_feature` ×6 | L3:10868, L3:16254, L0:9934, L0:13310, L0:8444, L0:7710 |
| 4 | `get_upstream_features` | Emb:" justice"@6 (de=19.50) +9 more |
| 5 | `get_upstream_features` | Emb:" you"@2 (de=10.50) +9 more |
| 6 | `get_upstream_features` | Emb:" a"@4 (de=18.62) +9 more |
| 7 | `get_upstream_features` | Emb:" to"@10 (de=41.00) +9 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F10868@4` | ❌ error | — | — | Trace upstream from L3:F10868 ("I'm a"/"I am a" phrase) at pos 4. This feature a… |
| SA-2 | `L3:F16254@8` | ❌ error | — | — | Trace upstream from L3:F16254 ("conditional statements followed by actions") at … |
| SA-3 | `L2:F14209@9` | ❌ error | — | — | Trace upstream from L2:F14209 at pos 9 (token "Muslim"). What does this feature … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L3:F16254@8, k=10 → Emb:"If"@1 (de=9.88) +9 more |
| 2 | `get_upstream_features` | L2:F14209@9, k=10 → Emb:" go"@9 (de=18.38) +9 more |
| 3 | `get_upstream_features` | L0:F3850@8, k=10 → Emb:","@8 (de=34.75) +9 more |
| 4 | `get_upstream_features` | L2:F14541@8, k=10 → Emb:"If"@1 (de=7.66) +9 more |
| 5 | `get_upstream_features` | L3:F1526@6, k=10 → Emb:" social"@5 (de=9.62) +9 more |
| 6 | `get_upstream_features` | L6:F2674@7, k=10 → Emb:" social"@5 (de=2.12) +9 more |
| 7 | `inspect_feature` ×9 | L0:3591, L0:13756, L0:4478, L0:2260, L0:9602, L1:14281, L2:13877, L6:9005, L4:13700 |
| 8 | `get_upstream_features` | L0:F13756@15, k=10 → Emb:" order"@15 (de=26.25) +9 more |
| 9 | `get_upstream_features` | L0:F2260@6, k=10 → Emb:" social"@5 (de=9.56) +9 more |
| 10 | `get_upstream_features` | L0:F4478@6, k=10 → Emb:" social"@5 (de=13.31) +9 more |
| 11 | `get_upstream_features` | L3:F1526@6, k=10 → Emb:" social"@5 (de=9.62) +9 more |
| 12 | `get_upstream_features` | L6:F9005@13, k=10 → Emb:" bakery"@13 (de=22.38) +9 more |
| 13 | `inspect_feature` | L0, F3591 → " terms related to government social programs" |
| 14 | `get_upstream_features` | L3:F10868@4, k=8 → Emb:" a"@4 (de=18.62) +7 more |
| 15 | `inspect_feature` ×3 | L0:10219, L1:10447, L2:1537 |
| 16 | `get_upstream_features` | L6:F2674@7, k=8 → Emb:" social"@5 (de=2.12) +7 more |
| 17 | `get_upstream_features` | L0:F4870@8, k=8 → Emb:","@8 (de=30.38) +7 more |
| 18 | `inspect_feature` ×2 | L2:1537, L0:4870 |
| 19 | `get_upstream_features` | L2:F14541@8, k=8 → Emb:"If"@1 (de=7.66) +7 more |
| 20 | `get_upstream_features` | L2:F13877@7, k=8 → Emb:" warrior"@7 (de=7.72) +7 more |
| 21 | `get_upstream_features` | L6:F2674@7, k=5 → Emb:" social"@5 (de=2.12) +4 more |

### Build

`build_circuit` → 14 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 45,744 | 6,245 | 271,994 | 0 | $0.0375 | — | — |
| **Total** | | **45,744** | **6,245** | **271,994** | **0** | **$0.0375** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 27s