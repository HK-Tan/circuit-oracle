# Circuit Oracle Report
**Date:** 2026-07-28 07:22:43 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven almost entirely by a single token — the word "not" at position 17 — and a vertical tower of ~12 features at layers 0/1/3/4/13/15/16 whose only consistent semantic content is detecting that one negation token (plus ancillary features for "recorded/menu" that cancel each other out).

**Confidence:** 9

**Reasoning:** The user's concern is confirmed and is even more extreme than they framed it. The top features driving the probe (`get_top_features`) are: **L0:F4958 (de=0.43)** = "the word 'not'", **L16:F6800 (de=0.44)** = "negations 'not', 'no', and contractions with 't'", **L4:F4492 (de=0.38)** = "negations in various languages", **L0:F2108 (de=-0.63)** = "the word 'menu'" (suppressing), **L0:F13938 (de=-0.37)** = "the word 'wild'" (suppressing — false-positive on the substring inside "not"). All causal influence flows down to a single embedding node: **Emb: ' not' (pos 17)**. Tracing upstream from L16:F6800 confirms it: its top positive direct_effects are `not` (pos 17, +11.8), `do` (pos 16, +5.4 — just lexical adjacency to the "do not" bigram), and L15:F11794 ("phrases that express disagreement or negation", +6.0). L15:F11794 itself feeds from L13:F102 ("phrases containing 'not' or negative connotations") and ultimately L0:F4958. The same ` not` embedding also directly drives L0:F4958 (+33.5), L4:F4492 (+17.4), L4:F2422 (+16.1), L3:F1101 (+12.9), and the lower-layer "not" detectors (L0:F4434, L0:F15925, L1:F5108, L1:F14233, L3:F3534, L3:F8011) — every one of which has the autointerp label "the word 'not'" or "negations in various languages". The supporting menu/record/middle/domestic/Title/finance/recording/single/Title features (L0:F2108, L1:F3691, L0:F7443, L1:F12253, L0:F3007, L0:F4523, L2:F8776, L0:F6649, L2:F12257) collectively have small direct effects and many of the larger ones (the menu detector at de=-0.63, the "wild" detector at de=-0.37, the "record" detector at de=+0.58, the "menu" detector at de=-0.63) are PUSHING AGAINST or merely counting substrings, not encoding sentence-level contradiction. The literal text content "A recorded menu will provide information… Recorded menus do not provide any information at this time" is a near-tautology (the two sentences say the same thing), so a well-functioning contradiction probe should output ~0; instead it lights up a "not" feature tower. The circuit contains zero features that encode premise/hypothesis semantic relationship, zero entity-matching features, and zero features for the content words "provide", "information", "lists", "obtain", "recorded" in any integrated way — every one of those features appears only as an isolated, low-frac_nonzero single-word detector that contributes marginally and inconsistently. The probe has learned the heuristic "negation word present → contradiction", which on this prompt is exactly wrong: the "not" cancels the content rather than contradicting it. This is a textbook spurious-feature / shortcut failure mode: a probe that has latched onto a single lexical cue (the word "not") and a single position (pos 17) rather than modeling the actual entailment relation between the two sentences.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 21 | Probe output (contradiction score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 17 | Late negation feature at 'not' (pos 17) |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 17 | Mid negation phrases ('not', contractions) |  phrases that express disagreement or negation | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L13:F102](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) | 17 | Mid negation phrases ('not', negative connotations) |  phrases containing "not" or negative connotations | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/102) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Multilingual negation detector | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Foreign-language negations (French/Malay) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | Polylingual negation/code-fragment detector |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 17 | Studies with negation/disproven context | sentences describing scientific studies or experiments, particularly where something is disproven | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 17 | Subword "n't" / "nut" | the character sequence "n't" or "nut" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | "Not found" / absence/negation in software |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 17 | Cross-lingual negation markers |  negative sentiment markers such as "not," "no," "never," and their equivalents in other languages | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L1:F5108](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) | 17 | Word 'not' | the word "not" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5108) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Word 'not' (L0) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F4434](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4434) | 17 | Word 'not' / negation (L0) | negation and words that indicate additional information | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4434) |
| [L0:F15925](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15925) | 17 | Word 'not' (L0) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15925) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L1:3691 de=0.824 |
| 3 | `inspect_feature` ×10 | L1:3691, L2:8776, L0:2108, L0:7443, L1:12253, L16:6800, L0:4958, L4:4492, L0:13938, L4:2422 |
| 4 | `get_upstream_features` | Emb:" not"@17 (de=11.81) +9 more |
| 5 | `get_upstream_features` | Emb:" not"@17 (de=33.50) +9 more |
| 6 | `inspect_feature` ×3 | L15:11794, L3:3534, L13:102 |
| 7 | `get_upstream_features` | Emb:" not"@17 (de=17.38) +9 more |
| 8 | `get_upstream_features` | Emb:" not"@17 (de=12.94) +9 more |
| 9 | `get_upstream_features` | Emb:" not"@17 (de=16.12) +9 more |
| 10 | `inspect_feature` ×15 | L3:1101, L3:8011, L3:9803, L1:5108, L1:14233, L0:4434, L0:15925, L1:763, L0:3007, L0:4523, L4:7998, L2:12257, L2:15894, L0:6649, L5:14641 |

### Build

`build_circuit` → 17 nodes, 39 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 54,611 | 7,776 | 255,025 | 0 | $0.0410 | — | — |
| **Total** | | **54,611** | **7,776** | **255,025** | **0** | **$0.0410** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 33s