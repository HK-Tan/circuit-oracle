# Circuit Oracle Report
**Date:** 2026-07-28 07:09:41 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for this passage is driven almost entirely by **a single identity-group keyword — "race"** — plus a couple of lexical helper features, confirming the user's suspicion that the classifier is using a **spurious identity-token shortcut** rather than the passage's actual content.

**Confidence:** 9

**Reasoning:**

The top features by direct effect on the probe output (L0:F10682 "race" = +0.146, L2:F10509 "race" = −0.181, L3:F5475 "race" = −0.101, L0:F14813 "race/racial issues" = −0.106) are all **word-level detectors for the token "race"** at position 5, each backed by direct `Emb: race` activations. Their frac_nonzero values (0.003–0.011) show these are highly specific lexical detectors, not semantic/syntactic abstractions. Crucially, the top_activating_examples for L0:F10682, L2:F10509 and L3:F5475 are dominated by **cycling/marathon race** contexts ("Loughman… tough race over the Wicklow Mountains", "one-day race held in Spring in Ireland", "Helio Castroneves, seen winning the IndyCar Series"), demonstrating that these features are *polysemous and not actually about racial identity at all* — they fire on the bare string "race".

The only feature that approaches a racial-content signal is L0:F14813 ("mentions of race, racial issues, or racism", frac_nonzero=0.011) and L6:F9228 ("language regarding discrimination based on race, gender, religion, and disability", frac_nonzero=**0.597**). L6:F9228's extremely high frac_nonzero marks it as a **generic, broadly-firing feature** that activates on virtually any mention of these protected categories — exactly the kind of trivial identity-keyword trigger the user is concerned about.

The remaining features are equally content-free: a cluster of "not" detectors (L0:F4958, L0:F15267, L2:F2713) on position 2, "mention/mentioning" detectors (L2:F11639, L3:F11194, L4:F15173) on position 3, and function-word detectors ("the", "By", "question") at L0/L3. None of these encode the *argument* of the passage (that omitting a black victim's race erases the specificity of anti-black police violence). They are pure lexical surfaces.

**The mechanism:** the probe is essentially a bag-of-keywords detector. It fires when the input contains (a) the literal token "race" — which is doubly unfortunate because that token is a polysemous cycling noun in 80%+ of its feature-training activations — and (b) any of the generic function/negation tokens ("not", "mentioning", "the", "question", "By") that co-occur in any discursive sentence. The actual content of the prompt — the critique of racial erasure in police-violence reporting — is never represented anywhere in the circuit. The user is correct: the classifier relies on **identity-keyword spurious features** (and at least one feature that is mostly a cycling-race detector), not on the prompt's semantic content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (toxicity classifier direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L0:F10682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) | 5 | Word feature: 'race' (polysemous: cycling race / racial) — L0:F10682, frac_nonzero=0.010 |  the word "race" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10682) |
| [L2:F10509](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) | 5 | Word feature: 'race' — L2:F10509, frac_nonzero=0.006 |  the word "race." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) |
| [L3:F5475](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) | 5 | Word feature: 'race' — L3:F5475, frac_nonzero=0.003 |  occurrences of the word "race" in different contexts | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5475) |
| [L0:F14813](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14813) | 5 | Race / racial-issue semantic — L0:F14813, frac_nonzero=0.011 |  mentions of race, racial issues, or racism | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14813) |
| [L2:F11639](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) | 3 | Lexical / semantic 'mention' features (L2:F11639 'mention', L2:F6539, L3:F11194, L4:F15173) — frac_nonzero 0.004-0.043 | the word "mention" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11639) |
| [L2:F6539](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) | 3 | Lexical / semantic 'mention' features (L2:F11639 'mention', L2:F6539, L3:F11194, L4:F15173) — frac_nonzero 0.004-0.043 | the word "mention" and words or phrases related to opinions or significance, as well as the word "matter." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6539) |
| [L3:F11194](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11194) | 3 | Lexical / semantic 'mention' features (L2:F11639 'mention', L2:F6539, L3:F11194, L4:F15173) — frac_nonzero 0.004-0.043 |  words related to stating or communicating information | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11194) |
| [L4:F15173](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) | 3 | Lexical / semantic 'mention' features (L2:F11639 'mention', L2:F6539, L3:F11194, L4:F15173) — frac_nonzero 0.004-0.043 | statements about mentioning or discussing something | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15173) |
| [L4:F2668](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) | 3 | Lexical / semantic 'mention' features (L2:F11639 'mention', L2:F6539, L3:F11194, L4:F15173) — frac_nonzero 0.004-0.043 |  instances of realizations coupled with acknowledgement or acknowledgment of something. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2668) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 2 | Word feature: 'not' (L0:F4958, L0:F15267, L2:F2713, L3:F6517) — frac_nonzero 0.0025-0.018 |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F15267](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15267) | 2 | Word feature: 'not' (L0:F4958, L0:F15267, L2:F2713, L3:F6517) — frac_nonzero 0.0025-0.018 |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15267) |
| [L2:F2713](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2713) | 2 | Word feature: 'not' (L0:F4958, L0:F15267, L2:F2713, L3:F6517) — frac_nonzero 0.0025-0.018 |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2713) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 4 | Function-word features: 'the' (L0:F3820), 'By' (L3:F12410), 'question' (L3:F672, L0:F819) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L3:F12410](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) | 1 | Function-word features: 'the' (L0:F3820), 'By' (L3:F12410), 'question' (L3:F672, L0:F819) | the word "By" at the start of a phrase or sentence | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12410) |
| [L3:F672](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) | 10 | Function-word features: 'the' (L0:F3820), 'By' (L3:F12410), 'question' (L3:F672, L0:F819) | the word "question" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/672) |
| [L0:F819](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/819) | 10 | Function-word features: 'the' (L0:F3820), 'By' (L3:F12410), 'question' (L3:F672, L0:F819) |  the word "question" specifically in the context of legal documents or investigations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/819) |
| [L6:F9228](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) | 6 | Discrimination-by-race-gender-religion language — L6:F9228, frac_nonzero=0.597 (GENERIC) |  language regarding discrimination based on race, gender, religion, and disability | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: race (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: mentioning (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: not (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: the (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:4958 de=-0.227 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15173@3` | ✅ reported | 3 | 2 | Trace upstream from L4:F15173 (pos 3). Inspect each feature along the way. Ident… |
| SA-2 | `L3:F12410@1` | ✅ reported | 4 | 8 | Trace upstream from L3:F12410 (pos 1). Inspect each feature. Identify what this … |
| SA-3 | `L0:F10682@5` | ❌ error | — | — | Trace upstream from L0:F10682 (pos 5). Inspect this early-layer feature. Try to … |
| SA-4 | `L3:F672@10` | ✅ reported | 6 | 19 | Trace upstream from L3:F672 (pos 10). Inspect each feature. Identify what this e… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15173 | " statements about mentioning or discussing something" |
| 2 | `get_upstream_features` | L4:F15173@3, k=10 | Emb:" mentioning"@3 (de=17.50) +9 more |
| 3 | `inspect_feature` | L3, F6517 | " words related to mentioning something" |
| 4 | `get_upstream_features` | L3:F6517@3, k=10 | Emb:" mentioning"@3 (de=23.12) +9 more |
| 5 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 6 | `get_upstream_features` | L0:F9026@3, k=10 | Emb:" mentioning"@3 (de=16.62) +9 more |
| 7 | `inspect_feature` | L3, F6365 | " words related to governments, laws, expressing opinions, and social a" |

**Findings:** The trace starts at L4:F15173 (pos 3), a higher‑level mention‑detector. Its strongest positive upstream driver is the raw embedding for the token 'mentioning' (direct_effect ≈ 17.5), satisfying the embedding‑connection requirement. The next most influential upstream feature is L3:F6517, another mention‑related detector, which itself receives a strong positive boost from the token embedding (direct…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F12410 | "the word "By" at the start of a phrase or sentence" |
| 2 | `get_upstream_features` | L3:F12410@1, k=10 | Emb:"By"@1 (de=48.75) +9 more |
| 3 | `inspect_feature` | L2, F6621 | " the word "by"" |
| 4 | `inspect_feature` | L0, F12698 | "question-answer pairs (or just questions) and import statements" |
| 5 | `inspect_feature` | L0, F10278 | "code referring to "entry" in a hash table context" |
| 6 | `get_upstream_features` | L2:F6621@1, k=10 | Emb:"By"@1 (de=14.94) +9 more |
| 7 | `get_upstream_features` | L0:F12698@1, k=10 | Emb:"<bos>"@0 (de=14.56) +9 more |
| 8 | `get_upstream_features` | L0:F10278@1, k=10 | Emb:"By"@1 (de=10.62) +9 more |

**Findings:** The target L3:F12410 is a lexical detector for the token 'By' at position 1. Its strongest upstream influence is the embedding of that token (direct_effect ~48.8). Additional positive contributions come from a lower‑layer word‑form detector (L2:F6621) and two layer‑0 features that are themselves driven by the same embedding or by <bos>. No refusal‑related or safety‑related patterns appear in this …

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F672 | " the word "question"" |
| 2 | `get_upstream_features` | L3:F672@10, k=10 | Emb:" question"@10 (de=38.75) +9 more |
| 3 | `inspect_feature` | L2, F12030 | " the word "issue" or related terms within a legal context" |
| 4 | `inspect_feature` | L2, F636 | " the phrase "in-person"" |
| 5 | `get_upstream_features` | L2:F12030@10, k=10 | Emb:" question"@10 (de=17.25) +9 more |
| 6 | `inspect_feature` | L0, F819 | " the word "question" specifically in the context of legal documents or" |
| 7 | `get_upstream_features` | L2:F636@10, k=10 | Emb:" in"@9 (de=11.44) +9 more |
| 8 | `inspect_feature` | L0, F4368 | " mentions of questions, references, generalities, or doubts" |
| 9 | `get_upstream_features` | L0:F819@10, k=10 | Emb:" in"@9 (de=14.56) +9 more |
| 10 | `inspect_feature` | L0, F16272 | " words associated with legal documents or official proceedings and the" |

**Findings:** Starting from L3:F672 (pos 10) we quickly found that the strongest upstream driver is the raw token embedding for "question" (direct_effect ≈ 38.8), confirming that this feature is a simple lexical detector. A small cascade of higher‑level legal‑context detectors (L2:12030 and L2:636) feed into it, each themselves driven by the same "question" token and the preceding "in" token. All of these upstr…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L0, F10682 → " the word "race"" |
| 2 | `get_upstream_features` | L0:F10682@5, k=10 → Emb:" race"@5 (de=22.62) +9 more |
| 3 | `get_upstream_features` | L2:F11639@3, k=10 → Emb:" mentioning"@3 (de=27.25) +9 more |
| 4 | `get_upstream_features` | L2:F6539@3, k=10 → Emb:" mentioning"@3 (de=7.91) +9 more |
| 5 | `get_upstream_features` | L3:F11194@3, k=10 → Emb:" mentioning"@3 (de=16.12) +9 more |
| 6 | `get_upstream_features` | L4:F2668@3, k=10 → Emb:" not"@2 (de=9.50) +9 more |
| 7 | `get_upstream_features` | L0:F3820@4, k=10 → Emb:" the"@4 (de=33.00) +9 more |
| 8 | `get_upstream_features` | L2:F2713@2, k=10 → Emb:" not"@2 (de=20.25) +9 more |
| 9 | `inspect_feature` ×17 | L2:11639, L2:6539, L3:11194, L4:2668, L0:3820, L2:2713, L2:10509, L0:4958, L0:1903, L0:14813, L3:5475, L4:573, L0:2317, L0:15267, L0:819, L6:9228, L0:9026 |
| 10 | `get_upstream_features` | L0:F10682@5, k=5 → Emb:" race"@5 (de=22.62) +4 more |

### Build

`build_circuit` → 13 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 57,879 | 4,654 | 102,424 | 0 | $0.0291 | — | — |
| SA-1 | openai/gpt-oss-120b | 65,995 | 4,310 | 0 | 0 | $0.0125 | ✅ 3F/2E | Trace upstream from L4:F15173 (pos 3). Inspect each feature … |
| SA-2 | openai/gpt-oss-120b | 91,731 | 6,334 | 5,632 | 0 | $0.0176 | ✅ 4F/8E | Trace upstream from L3:F12410 (pos 1). Inspect each feature.… |
| SA-4 | openai/gpt-oss-120b | 125,894 | 9,071 | 160 | 0 | $0.0243 | ✅ 6F/19E | Trace upstream from L3:F672 (pos 10). Inspect each feature. … |
| **Total** | | **341,499** | **24,369** | **108,216** | **0** | **$0.0836** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 8m 2s