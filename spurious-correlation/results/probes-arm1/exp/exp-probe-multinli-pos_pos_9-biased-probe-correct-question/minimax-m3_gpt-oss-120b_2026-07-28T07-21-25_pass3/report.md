# Circuit Oracle Report
**Date:** 2026-07-28 07:21:25 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" classification is driven primarily by low-level negation-word detectors anchored on the token " not" at position 17, with a secondary contribution from a "recording" lexical pattern on " recorded" at position 2 — not from the model's compositional semantic understanding of the premise/hypothesis relationship.

**Confidence:** 7

**Reasoning:** The circuit shows a clear pattern that supports the user's concern. Tracing the highest-impact features driving the probe's classification score reveals a dominant "negation detector" pathway:

1. **Negation cascade (the largest signal):** The strongest features are all negation-word detectors. The single most impactful feature is L16:F6800 (direct_effect=+0.44, frac_nonzero=0.031) labeled "negations 'not', 'no', and contractions with 't'." It is directly fed by token-embedding node " not" at pos 17 (direct_effect=+11.8 in its upstream tracing) and " do" at pos 16, plus L15:F11794 ("phrases that express disagreement or negation", de=+6.0) and L14:F6648 ("speculation, possibility, or negation", de=+3.8). These late-layer negation features all fire on position 17 of the input, which is the word "not" in "do not provide any information." Also L12:F9489 (de=+0.19) at pos 17 and L2:F12257 (de=+0.24) at pos 19 ("any") reinforce this.

2. **Mid-layer negation detectors (also strong):** L4:F4492 ("negations in various languages", de=+0.38), L0:F4958 ("the word 'not'", de=+0.43, frac_nonzero=0.018), L1:F14233 ("negative sentiment markers: not, no, never", de fed through pos 17, frac_nonzero=0.014), and L3:F3534 ("n't" character sequence, frac_nonzero=0.008) all fire at position 17. The probe almost certainly learned a simple heuristic: "any sentence with the word 'not' is a contradiction."

3. **"Recording" lexical pattern (secondary positive signal):** L1:F3691 ("the word 'recording'", de=+0.82 — the single largest), L0:F7443 ("the word 'record'", de=+0.58), L2:F8776 ("words related to finance and property law" — apparently a spurious match, de=+0.64), and L5:F14641 ("words relating to recording audio/video", de=-0.24, suppresses) all anchor to position 2 (" recorded"). This pattern is content-specific but lexical, not semantic — it does not encode *what* the contradiction is, only that one of the two sentences is about "recorded menus."

4. **Long tail of miscellaneous low-impact lexical features:** L0 features on pos 2-3 like "Title", "how", "kick" (the word kick, but this fires on a code/fragment context), "trail", "computer", "domestic", "words", percentage-bracket syntax — all at very low direct_effect (~0.2-0.3), suggesting the probe picks up any sufficiently activated lexical pattern but the negation features dominate.

5. **No semantic relation features:** I found no features encoding premise-hypothesis alignment, entailment, semantic similarity, or contradiction-as-relation. The probe's classification is being driven by surface-form negation signals (specifically the token "not" in the hypothesis "do not provide any information") and a bag-of-words lexical pattern around "recorded menus" — exactly the kind of spurious cue the user described. The model is essentially counting negation words rather than performing genuine NLI reasoning.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 17 | Probe direction (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 17 | Late-layer negation features (L15-16, pos 17 "not") |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 17 | Late-layer negation features (L15-16, pos 17 "not") |  phrases that express disagreement or negation | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L14:F6648](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) | 17 | Late-layer negation features (L15-16, pos 17 "not") |  words and phrases that indicate speculation, possibility, or negation regarding facts, rules, or causality. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/6648) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Mid-layer negation/speculation features (L3-4, pos 17) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Mid-layer negation/speculation features (L3-4, pos 17) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 17 | Mid-layer negation/speculation features (L3-4, pos 17) | the character sequence "n't" or "nut" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | Mid-layer negation/speculation features (L3-4, pos 17) |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L4:F4114](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4114) | 17 | Mid-layer negation/speculation features (L3-4, pos 17) |  negative statements | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4114) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | Mid-layer negation/speculation features (L3-4, pos 17) |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 17 | Mid-layer negation/speculation features (L3-4, pos 17) |  negative sentiment markers such as "not," "no," "never," and their equivalents in other languages | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | "recording"/"record" features (L0-2, pos 2) |  the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | "recording"/"record" features (L0-2, pos 2) |  words related to finance and property law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | "recording"/"record" features (L0-2, pos 2) | the word "record" appearing in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | "recording"/"record" features (L0-2, pos 2) | the word "menu" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |
| [L1:F12253](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) | 3 | "recording"/"record" features (L0-2, pos 2) |  the word 'menu' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) |
| [L5:F14641](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14641) | 2 | "recording"/"record" features (L0-2, pos 2) |  words relating to recording audio and/or video | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14641) |
| [L6:F11757](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11757) | 2 | "recording"/"record" features (L0-2, pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11757) |
| [L0:F13938](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13938) | 2 | Miscellaneous lexical features (L0, pos 2-3) | the word "wild" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13938) |
| [L4:F7998](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) | 3 | Miscellaneous lexical features (L0, pos 2-3) |  words related to telecommunications and telephones | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) |
| [L4:F7998](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) | 2 | Miscellaneous lexical features (L0, pos 2-3) |  words related to telecommunications and telephones | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) |
| [L0:F6649](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) | 3 | Miscellaneous lexical features (L0, pos 2-3) |  the word "Title" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) |
| [L1:F763](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/763) | 3 | Miscellaneous lexical features (L0, pos 2-3) | mentions of being in bed or going to bed | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/763) |
| [L2:F15894](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15894) | 3 | Miscellaneous lexical features (L0, pos 2-3) |  words related to the shifting gears on a car | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15894) |
| [L0:F3007](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) | 2 | Miscellaneous lexical features (L0, pos 2-3) |  the word "middle", and sometimes the word "character", and "camp" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) |
| [L0:F4523](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) | 3 | Miscellaneous lexical features (L0, pos 2-3) | the word "domestic" and words associated with globalism | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) |
| [L0:F10952](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10952) | 2 | Miscellaneous lexical features (L0, pos 2-3) | the word "computer", sometimes in related contexts such as "desk" or "negatively" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10952) |
| [L0:F5128](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) | 3 | Miscellaneous lexical features (L0, pos 2-3) |  the word "words" or words that are similar in meaning (word, Word, phrases, matrix) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) |
| [L0:F1485](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1485) | 8 | Miscellaneous lexical features (L0, pos 2-3) | the word "how" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1485) |
| [L0:F2115](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) | 3 | Miscellaneous lexical features (L0, pos 2-3) |  data reported as a percentage inside brackets, especially in a laboratory or medical context, and also recognizes countries | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) |
| [L0:F15937](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15937) | 3 | Miscellaneous lexical features (L0, pos 2-3) | mentions of recreational trails and paths | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15937) |
| [L2:F12098](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12098) | 3 | Miscellaneous lexical features (L0, pos 2-3) | the word "kick" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12098) |
| [L2:F12257](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12257) | 19 | Miscellaneous lexical features (L0, pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12257) |
| [L12:F9489](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/9489) | 17 | Miscellaneous lexical features (L0, pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/9489) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: " not" (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: " recorded" (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: " any" (pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: " do" (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Emb: " not" (pos 17, low layer 0) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L1:3691 de=0.824 |
| 3 | `inspect_feature` ×15 | L1:3691, L2:8776, L0:2108, L0:7443, L1:12253, L16:6800, L0:4958, L4:4492, L0:13938, L4:2422, L4:7998, L0:6649, L3:1101, L1:763, L5:14641 |
| 4 | `get_top_features` | 30 features; top: L1:3691 de=0.824 |
| 5 | `get_upstream_features` | Emb:" not"@17 (de=11.81) +4 more |
| 6 | `get_upstream_features` | Emb:" not"@17 (de=12.75) +4 more |
| 7 | `get_upstream_features` | Emb:" not"@17 (de=8.62) +4 more |
| 8 | `get_upstream_features` | Emb:" recorded"@2 (de=18.00) +4 more |
| 9 | `get_upstream_features` | L14:F6648 (de=3.77) +4 more |
| 10 | `get_upstream_features` | Emb:" not"@17 (de=16.12) +4 more |
| 11 | `get_upstream_features` | Emb:" not"@17 (de=6.69) +4 more |
| 12 | `inspect_feature` ×3 | L15:11794, L3:3534, L1:14233 |
| 13 | `get_upstream_features` | Emb:" not"@17 (de=6.88) +4 more |
| 14 | `inspect_feature` | " words and phrases that indicate speculation, possibility, or negation" |
| 15 | `get_upstream_features` | Emb:" recorded"@2 (de=24.75) +4 more |
| 16 | `get_upstream_features` | Emb:" recorded"@2 (de=19.50) +4 more |
| 17 | `get_upstream_features` | Emb:" recorded"@2 (de=22.62) +4 more |
| 18 | `get_upstream_features` | Emb:" not"@17 (de=11.81) +4 more |
| 19 | `inspect_feature` ×11 | L2:15894, L2:12098, L0:3007, L0:4523, L0:10952, L0:5128, L0:1485, L0:2115, L0:15937, L4:4114, L3:8011 |

### Build

`build_circuit` → 11 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 56,502 | 5,385 | 246,302 | 0 | $0.0382 | — | — |
| **Total** | | **56,502** | **5,385** | **246,302** | **0** | **$0.0382** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 31s