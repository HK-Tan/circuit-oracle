# Circuit Oracle Report
**Date:** 2026-07-28 07:23:36 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is overwhelmingly driven by a deep vertical chain of generic "not" / negation keyword detectors at position 21 ("were not allowed") — from L0 lexical features (L0:4958, L0:15454 "the word 'not'") up through L1, L2, L3, L4, L13, L15, and culminating in L16:12358 ("not followed by a form of 'to be'") — with virtually no content-aware features about the actual agricultural / deforestation premise and hypothesis.

**Confidence:** 9

**Reasoning:** The user's concern is confirmed by the circuit. The dominant positive signal to the probe direction is a single feature, L16:12358 (direct_effect = +0.3359), whose autointerp is "the word 'not' followed within a few tokens by a form of the verb 'to be'" — i.e., a pure negation-keyword pattern, not a semantic contradiction detector. Tracing it upstream: it is fed primarily by the embedding of the literal token " not" (pos 21, direct_effect = 19, the largest edge in the whole graph) and by L0 lexical "not" detectors (L0:4958, L0:15454; both literally labeled "the word 'not'", frac_nonzero ≈ 0.003–0.018). The L0 features activate on the same token in unrelated contexts (legal, software, scientific text), and the only L0 features that look content-specific are L0:3498 "they", L0:3820 "the", L0:8444 "to", L0:2238 "about", and L0:9646 "actually/however" — all generic lexical detectors with low direct effects (|0.19–0.39|). Below L16, the circuit replicates the same negation pattern at every layer: L13:3295 ("is/are not", frac_nonzero=0.013) and L13:14177 ("negation or dissent, often 'not' with 'am'") feed L15:10071 ("negations and equivocations", frac_nonzero=0.013), which feeds L16:12358. L4:4492 ("negations in various languages") and L4:2422 ("negations in other languages like French, Malay, and Croatian") are also present, indicating these negation features are language-agnostic keyword matchers. A striking piece of evidence: the only non-negation content feature is L2:4819 ("sentences containing the word 'fire' or similar terms", at pos 12 'fire' with direct_effect = +0.26) — this is the literal word "fire" detected as a content cue, not a semantic understanding of "setting fire to forests" vs. "not allowed to deforest". The agricultural / deforestation / permission semantics never get represented as such; only the surface word "fire" survives. Similarly, L2:2952 is a generic "out" detector. Even more telling: L15:2080 ("set about") at pos 3 ("set about clearing") and pos 11 ("set fire") has a small positive effect (+0.19), but it is a generic lexical pattern matcher for the phrase "set followed by article/preposition", not a semantic action detector. The contrast between the *content* the probe should be detecting (a permission rule violated by an action) versus the *signal that actually drives it* (the keyword "not" plus an unrelated generic "fire" token) is a textbook spurious-feature / artifact pattern: the probe has learned that the hypothesis contains the word "not" in a position that premise verbs rule out, and it keys on the surface negation rather than the entailment relationship.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: " not" (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: " were" (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: " agriculture" (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: "<bos>" (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 21 | L0 lexical "not" detectors (L0:4958, L0:15454) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F15454](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) | 21 | L0 lexical "not" detectors (L0:4958, L0:15454) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15454) |
| [L0:F12414](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12414) | 20 | L0 lexical "were" (L0:12414) |  the word "were" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12414) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | L0 lexical content features (L0:3498 "they", L0:3820 "the", L0:8444 "to", L0:2238 "about", L0:9646 "actually/however") |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 6 | L0 lexical content features (L0:3498 "they", L0:3820 "the", L0:8444 "to", L0:2238 "about", L0:9646 "actually/however") | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 13 | L0 lexical content features (L0:3498 "they", L0:3820 "the", L0:8444 "to", L0:2238 "about", L0:9646 "actually/however") | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | L0 lexical content features (L0:3498 "they", L0:3820 "the", L0:8444 "to", L0:2238 "about", L0:9646 "actually/however") |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F9646](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9646) | 21 | L0 lexical content features (L0:3498 "they", L0:3820 "the", L0:8444 "to", L0:2238 "about", L0:9646 "actually/however") |  words that indicate the degree, scale, or validity of something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9646) |
| [L1:F5108](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) | 21 | L1 negation "not" (L1:5108, L1:8332) | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) |
| [L1:F8332](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8332) | 5 | L1 negation "not" (L1:5108, L1:8332) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8332) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 21 | L2 negation detectors (L2:12021 "not", L2:15104 "negative statements", L2:4544 "not", L2:6993 "uncertainty") | "not" or negative terms, with some bonus for sports-related terms and "purpose". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L2:F15104](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15104) | 21 | L2 negation detectors (L2:12021 "not", L2:15104 "negative statements", L2:4544 "not", L2:6993 "uncertainty") | negative statements | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15104) |
| [L2:F4544](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4544) | 21 | L2 negation detectors (L2:12021 "not", L2:15104 "negative statements", L2:4544 "not", L2:6993 "uncertainty") | the word "not" or contractions including "not" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4544) |
| [L2:F6993](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) | 21 | L2 negation detectors (L2:12021 "not", L2:15104 "negative statements", L2:4544 "not", L2:6993 "uncertainty") | phrases describing uncertainty or difficulty | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | L2 content tokens (L2:4819 "fire", L2:2952 "out") | sentences containing the word "fire" or similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L2:F2952](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) | 4 | L2 content tokens (L2:4819 "fire", L2:2952 "out") |  the word "out", and sometimes activates on words relating to legal cases | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 21 | L3 negation detectors (L3:8011 "not", L3:1101 "absence/negation", L3:6374 "not/longer", L3:9803 "disproven studies") |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 21 | L3 negation detectors (L3:8011 "not", L3:1101 "absence/negation", L3:6374 "not/longer", L3:9803 "disproven studies") |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F6374](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6374) | 21 | L3 negation detectors (L3:8011 "not", L3:1101 "absence/negation", L3:6374 "not/longer", L3:9803 "disproven studies") | the word "not" or the word "longer" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6374) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 21 | L3 negation detectors (L3:8011 "not", L3:1101 "absence/negation", L3:6374 "not/longer", L3:9803 "disproven studies") | sentences describing scientific studies or experiments, particularly where something is disproven | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 21 | L4 negation detectors (L4:4492 multilingual, L4:2422 other-lang) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 21 | L4 negation detectors (L4:4492 multilingual, L4:2422 other-lang) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 21 | L13 "is/are not" detectors (L13:3295, L13:14177) | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L13:F14177](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14177) | 21 | L13 "is/are not" detectors (L13:3295, L13:14177) | negation or dissent, often using "not" with "am" or other verbs | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/14177) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 3 | L15 "set about" (L15:2080) | the phrase "set" followed by articles or prepositions | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 11 | L15 "set about" (L15:2080) | the phrase "set" followed by articles or prepositions | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 21 | L15 "negations/equivocations" (L15:10071) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 21 | L16 "not + form of to be" (L16:12358) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe logit (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:3498 de=-0.785 |
| 3 | `inspect_feature` ×11 | L0:3498, L0:2238, L3:1101, L3:8011, L16:12358, L2:2952, L4:4492, L2:4819, L0:3820, L0:8444, L15:2080 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@21` | ❌ error | — | — | Trace the upstream circuit that drives the 'not + to be' negation feature at L16… |
| SA-2 | `L4:F4492@21` | ❌ error | — | — | Trace the upstream circuit that drives the multilingual negation feature at L4:4… |
| SA-3 | `L2:F4819@12` | ❌ error | — | — | Trace the upstream circuit that drives the 'fire' sentences feature at L2:4819 p… |
| SA-4 | `L15:F2080@3` | ❌ error | — | — | Trace the upstream circuit that drives the 'set' phrase feature at L15:2080 pos … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F12358@21, k=15 → Emb:" not"@21 (de=19.00) +14 more |
| 2 | `get_upstream_features` | L4:F4492@21, k=15 → Emb:" not"@21 (de=19.12) +14 more |
| 3 | `inspect_feature` ×15 | L0:4958, L2:12021, L15:10071, L0:9646, L13:3295, L13:14177, L0:15454, L4:2422, L3:9803, L1:5108, L2:15104, L3:6374, L2:6993, L2:4544, L0:12414 |

### Build

`build_circuit` → 17 nodes, 35 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 69,003 | 6,663 | 116,018 | 0 | $0.0357 | — | — |
| **Total** | | **69,003** | **6,663** | **116,018** | **0** | **$0.0357** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 19s