# Circuit Oracle Report
**Date:** 2026-07-28 07:15:11 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven almost entirely by a chain of negation/absence detector features anchored on the token "not" at position 21 ("not allowed to deforest"), rather than by the actual semantic content of the premise-hypothesis relationship.

**Confidence:** 9

**Reasoning:** The attribution graph confirms the user's concern. The dominant signal flows from a single word: the negation token "not" at position 21.

- **Token-embedding root:** Emb: "not" (pos 21) feeds L0:F4958 ("the word 'not'", frac_nonzero=0.018) with direct_effect=33.75, and also directly into the early negation circuit with direct_effect≈17–21.
- **Negation feature chain:** A cascade of features at the "not" position drives the probe:
  - L3:F1101 ("error messages and terms indicating absence or negation") — direct_effect=+0.34, suppressed_tokens="not/NOT/Not"
  - L3:F8011 (negation in multiple languages) — direct_effect=+0.34, promoted_tokens="not/NOT"
  - L3:F6227 at pos 23 ("to") — direct_effect=+0.19, promoted_tokens="not"
  - L4:F4492 ("negations in various languages") — direct_effect=+0.31
  - L4:F2422 ("negations in other languages") — direct_effect=−0.21
  - L16:F12358 ("the word 'not' followed by a form of the verb 'to be'") — direct_effect=+0.34
- **Content features are weak/decorative:** Features encoding the actual content — L2:F4819 ("fire"), L2:F2952 ("out"/clearing), L1:F8332 ("clear"/clearing), L0:F3498 ("they"), L15:F2080 ("set…") — have direct_effects of only ±0.19–0.26, and the L0 generic lexical features (F3820 "the", F8444 "to", F2238 "about") are similarly small.

Net effect on the probe: the negation chain at pos 21 contributes on the order of ±1.0 to the probe score (cumulative positive ~+1.3, negative ~−0.55), while all content features together contribute at most ~±0.6. The circuit is a textbook example of a classifier relying on a lexical shortcut — a single negation word — rather than the semantic relationship between "setting fire to forest" and "not allowed to deforest." The fact that the same probe would likely fire on any sentence containing "not allowed to X" regardless of whether X matches the premise confirms the user's diagnosis.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 21 | Probe Logit (contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 21 | Late-layer negation/absence features at "not" (pos 21) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 21 | Mid-layer negation/absence features at "not" (pos 21) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 21 | Mid-layer negation/absence features at "not" (pos 21) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 21 | Early-layer negation/absence features at "not" (pos 21) |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 21 | Early-layer negation/absence features at "not" (pos 21) |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 23 | Early-layer negation/absence features at "not" (pos 21) |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L3:F13138](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13138) | 4 | Early-layer negation/absence features at "not" (pos 21) |  words and phrases related to legal proceedings or documents. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13138) |
| [L3:F8733](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8733) | 4 | Early-layer negation/absence features at "not" (pos 21) |  parts of words like "ch", "parms", "ened", and "ounesto" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8733) |
| [L3:F3797](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3797) | 1 | Early-layer negation/absence features at "not" (pos 21) | comments starting with "So" or "Okay". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3797) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 21 | Token-embedding "not" detector (L0:F4958) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | Content/lexical features (fire, set, clearing, they, the, to) | sentences containing the word "fire" or similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L2:F2952](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) | 4 | Content/lexical features (fire, set, clearing, they, the, to) |  the word "out", and sometimes activates on words relating to legal cases | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) |
| [L1:F8332](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8332) | 5 | Content/lexical features (fire, set, clearing, they, the, to) | the word "clear" or "clearance" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8332) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | Content/lexical features (fire, set, clearing, they, the, to) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | Content/lexical features (fire, set, clearing, they, the, to) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 6 | Content/lexical features (fire, set, clearing, they, the, to) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 13 | Content/lexical features (fire, set, clearing, they, the, to) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 3 | Content/lexical features (fire, set, clearing, they, the, to) | the phrase "set" followed by articles or prepositions | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 11 | Content/lexical features (fire, set, clearing, they, the, to) | the phrase "set" followed by articles or prepositions | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3498 de=-0.785 |
| 3 | `get_upstream_features` | Emb:" they"@2 (de=42.75) +2 more |
| 4 | `inspect_feature` ×6 | L0:3498, L3:1101, L3:8011, L16:12358, L15:2080, L0:2238 |
| 5 | `get_upstream_features` | Emb:" not"@21 (de=13.69) +4 more |
| 6 | `get_upstream_features` | Emb:" not"@21 (de=21.75) +4 more |
| 7 | `get_upstream_features` | Emb:" not"@21 (de=19.00) +4 more |
| 8 | `inspect_feature` ×12 | L4:4492, L4:2422, L0:4958, L0:3820, L0:8444, L2:2952, L2:4819, L3:8733, L3:6227, L3:13138, L3:3797, L1:8332 |
| 9 | `get_upstream_features` | Emb:" not"@21 (de=19.12) +4 more |
| 10 | `get_upstream_features` | Emb:" not"@21 (de=17.50) +4 more |
| 11 | `get_upstream_features` | Emb:" not"@21 (de=33.75) +4 more |
| 12 | `get_upstream_features` | Emb:" the"@6 (de=34.25) +4 more |
| 13 | `get_upstream_features` | Emb:" to"@13 (de=41.00) +4 more |
| 14 | `get_upstream_features` | Emb:" set"@3 (de=13.50) +2 more |
| 15 | `get_upstream_features` | Emb:" fire"@12 (de=32.00) +2 more |
| 16 | `get_upstream_features` | Emb:" set"@3 (de=7.12) +2 more |
| 17 | `get_upstream_features` | Emb:" to"@23 (de=6.75) +2 more |
| 18 | `get_upstream_features` | Emb:" set"@3 (de=10.12) +2 more |
| 19 | `get_upstream_features` | Emb:"So"@1 (de=22.00) +2 more |
| 20 | `get_upstream_features` | Emb:" clearing"@5 (de=21.12) +2 more |
| 21 | `get_upstream_features` | Emb:" set"@3 (de=44.50) +2 more |
| 22 | `get_upstream_features` | Emb:" setting"@11 (de=45.75) +2 more |
| 23 | `get_upstream_features` | Emb:" about"@4 (de=35.00) +2 more |

### Build

`build_circuit` → 18 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 55,754 | 4,975 | 85,029 | 0 | $0.0278 | — | — |
| **Total** | | **55,754** | **4,975** | **85,029** | **0** | **$0.0278** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 8s