# Circuit Oracle Report
**Date:** 2026-07-28 07:07:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by lexical detectors of the word "white" (and adjacent "he" pronouns), which propagate through low/mid-layer race/identity features (F6983 "race & slavery", F13158 "race & ethnicity", F11768 "white in diversity context") into the probe — the toxic/negative sentiment implied by the conditional ("would be s problem") is barely represented; instead, the model is using the *identity label* "white" as a proxy trigger.

**Confidence:** 7

**Reasoning:** The top direct-effect features at the prediction site are all identity-marker detectors anchored on the token "white" at position 4. The most positive direct effects come from L0:12768 (he/she pronoun proximity, 0.205), L0:3436 ("mentions of the word 'white'", 0.172), and L4:15204 ("art galleries / White House", 0.118) — all of which are lexical/identity features, not toxicity or sentiment features. The negative contributors (L0:13663 "pregnancy", L0:3255 "and", L1:1480 "color white") cancel some of the signal but do not change its nature.

Tracing upstream confirms this. L4:15204 receives a huge direct push from the raw embedding of the token " white" (direct_effect 40.5), and is further driven by L0:10910 ("word 'white'", 1.38), L0:3436 ("mentions of 'white'", 0.97), and L0:2458 ("was"). L4:7136 ("the color white") receives an even larger embedding push (43.5) from " white". L2:6983 ("words related to race and slavery") gets direct_effect 8.19 from the embedding of " white" plus contributions from L1:13007 ("mentions of 'white' and 'black'") and L1:3436. L3:11768 ("the word 'white' and related contexts such as diversity") sits between these layers and the probe output. The dominant signal therefore travels: `Emb:' white' (pos 4) → L0 lexical 'white' (F3436/F10910/F1480) → L1 race detectors (F13007) → L2 race/identity (F6983, F13158, F585) → L3 'white' + diversity (F11768) → L4 color/White House (F7136, F15204) → probe logit`.

No feature in the top-15 list encodes toxicity, slur, insult, profanity, or negative sentiment directed at the group. The phrase "would be s problem" is essentially absent from the circuit — only F12059 ("words related to purpose and intent", activation 9.6) tangentially touches the verb semantics, and F2458 ("was"), F3255 ("and"), F11539 ("if") are function-word detectors with small direct effects. The conditional scaffold "If he was… and not Hispanic" (handled by L2:1139 "so" and L2:11539/L3:12404 "if" features) does contribute, but these features carry the same race-adjacent embeddings upstream and do not encode the *harm* being conditioned.

This corroborates the user's concern: the probe classification is largely a **spurious identity-trigger mechanism**. The mere presence of the race label "white" (and to a lesser extent the pronoun "he") in proximity to a counterfactual "if…not Hispanic" template is sufficient to push the probe score. The actual hateful/harmful content — the assertion that being "white and not Hispanic" makes something "a problem" — contributes comparatively little. The circuit is essentially a "white identity term → toxicity probe" shortcut, not a semantic understanding of the conditional insult.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 4 | L0 lexical 'white' detectors (F3436 'word white', F10910 'word white', F1480 'color white', F880 'pronoun it') |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 4 | L0 lexical 'white' detectors (F3436 'word white', F10910 'word white', F1480 'color white', F880 'pronoun it') | the word "possession" and the words "white", "immediate" and "once" regardless of context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L1:F1480](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) | 4 | L0 lexical 'white' detectors (F3436 'word white', F10910 'word white', F1480 'color white', F880 'pronoun it') | the color 'white', sometimes in a context involving race | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 8 | L0 lexical 'white' detectors (F3436 'word white', F10910 'word white', F1480 'color white', F880 'pronoun it') |  references to the pronoun "it", and sometimes "that", suggesting observation of the subject of a discussion | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 2 | L0 pronoun detectors (F12768 'he/she proximity', F310 'she/her/he') |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) | 2 | L0 pronoun detectors (F12768 'he/she proximity', F310 'she/her/he') |  the pronouns "she", "her", and "he" and sometimes the word "therefore" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) |
| [L0:F12059](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12059) | 4 | L0 other lexical: F12059 'objective/purpose', F3255 'and', F2458 'was' |  words related to purpose and intent | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12059) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 5 | L0 other lexical: F12059 'objective/purpose', F3255 'and', F2458 'was' |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F2458](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) | 3 | L0 other lexical: F12059 'objective/purpose', F3255 'and', F2458 'was' |  the word "was" and sometimes "were." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) |
| [L1:F13007](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13007) | 4 | L1 race detectors (F13007 'mentions of white/black', F10336 'grand', F3079 'politics/protests') | mentions of the word "white" and to a lesser extent "black" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13007) |
| [L1:F10336](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10336) | 4 | L1 race detectors (F13007 'mentions of white/black', F10336 'grand', F3079 'politics/protests') | the word "grand" in legal documents or health questionnaires | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10336) |
| [L1:F3079](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3079) | 4 | L1 race detectors (F13007 'mentions of white/black', F10336 'grand', F3079 'politics/protests') | words related to politics and protests | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3079) |
| [L2:F11539](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11539) | 1 | L1 conditional/so features (F11539 'if', F1139 'so/come') | the word "if" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11539) |
| [L2:F1139](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) | 3 | L1 conditional/so features (F11539 'if', F1139 'so/come') |  various usages of the word "so", as well as some instances of the word "come" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1139) |
| [L3:F12404](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12404) | 1 | L1 conditional/so features (F11539 'if', F1139 'so/come') |  instances of the conditional word "if" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12404) |
| [L2:F6983](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) | 4 | L2 race/identity features (F6983 'race & slavery', F585 'white (often dwarf)', F1708 'colors', F13158 'race & ethnicity') |  words related to race and slavery | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6983) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 4 | L2 race/identity features (F6983 'race & slavery', F585 'white (often dwarf)', F1708 'colors', F13158 'race & ethnicity') | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 4 | L2 race/identity features (F6983 'race & slavery', F585 'white (often dwarf)', F1708 'colors', F13158 'race & ethnicity') |  mentions of colors | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 4 | L2 race/identity features (F6983 'race & slavery', F585 'white (often dwarf)', F1708 'colors', F13158 'race & ethnicity') |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L3:F11768](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) | 4 | L3 'white' in race context (F11768 'white, often with diversity') |  the word "white" and related contexts such as diversity | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) |
| [L4:F7136](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) | 4 | L4 'color white' features (F7136 'color white', F15204 'art galleries/museums/White House') |  the color white | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 4 | L4 'color white' features (F7136 'color white', F15204 'art galleries/museums/White House') |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'probe' is not one of the top-k next-token candidates  |
| 3 | `get_top_features` | 15 features; top: L0:12768 de=0.205 |
| 4 | `inspect_feature` ×15 | L0:12768, L0:3436, L0:13663, L4:15204, L0:880, L0:10910, L2:1139, L2:6983, L2:11539, L0:310, L0:3255, L1:1480, L4:7136, L3:12404, L0:12059 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F15204@4` | ✅ reported | 3 | 4 | Trace upstream from L4:F15204 (art galleries/museums/White House feature at pos … |
| SA-2 | `L4:F7136@4` | ❌ error | — | — | Trace upstream from L4:F7136 (color white feature at pos 4='white'). Identify wh… |
| SA-3 | `L2:F6983@4` | ✅ reported | 5 | 10 | Trace upstream from L2:F6983 (race/slavery words feature at pos 4='white'). Iden… |
| SA-4 | `L0:F12768@2` | ❌ error | — | — | Trace upstream from L0:F12768 (he/she pronoun proximity at pos 2='he'). Identify… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15204 | " art galleries, museums and the White House" |
| 2 | `get_upstream_features` | L4:F15204@4, k=10 | Emb:" white"@4 (de=40.50) +9 more |
| 3 | `inspect_feature` | L0, F10910 | "the word "possession" and the words "white", "immediate" and "once" re" |
| 4 | `inspect_feature` | L0, F2458 | " the word "was" and sometimes "were."" |
| 5 | `get_upstream_features` | L0:F10910@4, k=5 | Emb:" white"@4 (de=14.56) +4 more |
| 6 | `inspect_feature` | L0, F2458 | " the word "was" and sometimes "were."" |
| 7 | `inspect_feature` | L0, F3436 | " mentions of the word "white"" |
| 8 | `get_upstream_features` | L0:F2458@4, k=5 | ❌ Feature (layer=0, feature_idx=2458) not found at pos=4. This |
| 9 | `get_upstream_features` | L0:F2458@3, k=10 | Emb:" was"@3 (de=36.75) +9 more |
| 10 | `get_upstream_features` | L0:F3436@4, k=5 | Emb:" white"@4 (de=18.00) +4 more |

**Findings:** The target L4:F15204 (art galleries/museums/White House) receives a strong positive drive from the input token embedding " white" (direct_effect 40.5), establishing a direct race‑identity pathway. Additional low‑layer features (L0:10910 and L0:3436) also detect the literal token "white" and modestly boost the target. These upstream nodes reside in layer 0, satisfying the lower‑third requirement, a…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F6983 | " words related to race and slavery" |
| 2 | `get_upstream_features` | L2:F6983@4, k=10 | Emb:" white"@4 (de=8.19) +9 more |
| 3 | `inspect_feature` | L1, F10336 | " the word "grand" in legal documents or health questionnaires" |
| 4 | `get_upstream_features` | L1:F10336@4, k=10 | Emb:" white"@4 (de=11.50) +9 more |
| 5 | `inspect_feature` | L1, F13007 | " mentions of the word "white" and to a lesser extent "black"" |
| 6 | `inspect_feature` | L1, F3079 | "words related to politics and protests" |
| 7 | `inspect_feature` | L0, F3436 | " mentions of the word "white"" |
| 8 | `get_upstream_features` | L0:F3436@4, k=5 | Emb:" white"@4 (de=18.00) +4 more |

**Findings:** The race‑related feature L2:F6983 (layer 2) is driven primarily by the raw token embedding of the word "white" at position 4. That embedding feeds a direct low‑level detector L0:F3436 (layer 0) and higher‑level detectors L1:F13007, L1:F10336, and L1:F3079, which in turn contribute to L2:F6983. The path reaches a token‑embedding with a large positive direct effect (18.0) at layer 0, satisfying the …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F15204@4, k=10 → Emb:" white"@4 (de=40.50) +9 more |
| 2 | `get_upstream_features` | L4:F7136@4, k=10 → Emb:" white"@4 (de=43.50) +9 more |
| 3 | `get_upstream_features` | L0:F12768@2, k=10 → Emb:" he"@2 (de=37.00) +9 more |
| 4 | `get_upstream_features` | L0:F3436@4, k=10 → Emb:" white"@4 (de=18.00) +9 more |
| 5 | `get_upstream_features` | L1:F13007@4, k=10 → Emb:" white"@4 (de=16.25) +9 more |
| 6 | `get_upstream_features` | L2:F1139@3, k=5 → Emb:"If"@1 (de=27.62) +4 more |
| 7 | `inspect_feature` ×6 | L2:585, L3:11768, L2:1708, L0:2458, L0:6548, L2:13158 |
| 8 | `get_upstream_features` | L2:F1708@4, k=5 → Emb:" white"@4 (de=17.88) +4 more |
| 9 | `get_upstream_features` | L2:F13158@4, k=5 → Emb:" white"@4 (de=13.12) +4 more |
| 10 | `inspect_feature` ×3 | L1:7821, L0:13663, L2:1139 |
| 11 | `get_upstream_features` | L2:F1139@3, k=5 → Emb:"If"@1 (de=27.62) +4 more |
| 12 | `get_upstream_features` | L0:F13663@4, k=5 → Emb:" white"@4 (de=15.00) +4 more |
| 13 | `get_upstream_features` | L3:F12404@1, k=5 → Emb:"If"@1 (de=15.75) +4 more |
| 14 | `get_upstream_features` | L0:F3255@5, k=5 → Emb:" and"@5 (de=35.75) +4 more |

### Build

`build_circuit` → 14 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 70,579 | 7,689 | 288,474 | 0 | $0.0477 | — | — |
| SA-1 | openai/gpt-oss-120b | 107,210 | 5,239 | 7,776 | 0 | $0.0193 | ✅ 3F/4E | Trace upstream from L4:F15204 (art galleries/museums/White H… |
| SA-3 | openai/gpt-oss-120b | 100,388 | 8,626 | 64 | 0 | $0.0202 | ✅ 5F/10E | Trace upstream from L2:F6983 (race/slavery words feature at … |
| **Total** | | **278,177** | **21,554** | **296,314** | **0** | **$0.0873** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 25s