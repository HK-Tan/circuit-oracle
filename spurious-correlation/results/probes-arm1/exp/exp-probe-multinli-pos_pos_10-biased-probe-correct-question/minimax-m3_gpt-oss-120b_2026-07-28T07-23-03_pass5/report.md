# Circuit Oracle Report
**Date:** 2026-07-28 07:23:03 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This is a probe-classification attribution graph whose positive direction is driven almost entirely by surface-level negation/absence features at the "not" token in the second sentence, with no engagement with the actual premise/hypothesis semantic content (the "role reversal"/democracy topic or the word "strange").

**Confidence:** 9

**Reasoning:** The top of the circuit is dominated by L16:F12358 ("not" followed by a form of "to be," act 28.25, frac_nonzero 0.028) which alone carries the largest direct_effect to the probe (0.656). Its upstream path is overwhelmingly the raw "not" token embedding at pos 17 (direct_effect 23.125 from `emb_not`, plus 8.125 from L0:F4958 — literally "the word 'not'") combined with the "is" embedding at pos 16 (direct_effect 4.375) that precedes it. Below it, an entire deep negation tower funnels the same signal: L15:F6160 ("is there") and L15:F10071 ("negations and equivocations") → L9:F14687 ("not" + because/but) → L4:F2422 + F4492 + F13171 (multilingual / generic negation detectors, all at pos 17) → L3:F1101/F8011/F12079/F2232/F9803 (negation/absence/error-message features at pos 17) → L2:F12021 ("not"/negative terms) → L1:F14233 (negative sentiment markers "not/no/never") → L0:F4958 ("the word 'not'") → token embedding `not` (pos 17). Notably, the very strongest single upstream contribution to L16:F12358 is the raw `not` token embedding (23.1) with `is` second (4.4); the only other token-embedding contribution is "reversal" (pos 4, direct_effect 1.76) and "role" (pos 3, −1.19), which are tiny. The few non-negation, content-related features (L1:F15749 "strange" at pos 2 with direct_effect 0.279, L2:F16097 "superlative / est" at pos 2 with direct_effect −0.397, and L3:F3669 "ordinal rankings" at pos 2 with direct_effect 0.381) are minor and are at the topic-position, not driving the probe score. Almost every feature in the top-15 — L0:F4958, L1:F14233, L2:F12021, L3:F1101/F8011/F12079/F2232/F9803, L4:F2422/F4492, L9:F14687, L15:F10071, L16:F12358 — has a label that is some variant of "negation" or "absence/negative sentiment," and the few with off-topic labels (L3:F1101 "error messages," L3:F8011 "code fragments from different languages," L3:F9803 "experiments where something is disproven") fire because the token "not" co-occurs with their typical training contexts. The user's concern is fully confirmed: the probe direction is being driven by a shallow "I see the word 'not'" detector chain anchored on the negation word of the second sentence ("There is not role reversal going on…"), with no circuit path that reads the premise "strangest role reversal / democracy" or compares premise to hypothesis. The contradiction classification is essentially being inferred from the lexical cue of negation, not from entailment content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | L0:F4958 — "the word 'not'" (act 30.6) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 17 | L1:F14233 — negative sentiment markers ('not', 'no', 'never', etc.) (act 5.25) |  negative sentiment markers such as "not," "no," "never," and their equivalents in other languages | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L1:F15749](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) | 2 | L1:F15749 — the word "strange" (pos 2) (act 9.94) |  the word "strange", or related words | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15749) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 17 | L2:F12021 — 'not' / negative terms (act 14.9) | "not" or negative terms, with some bonus for sports-related terms and "purpose". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | L2:F16097 — superlative adjectives / 'est' (pos 2) (act 16.75) | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 17 | L3 negation/absence features (cluster at pos 17) |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 17 | L3 negation/absence features (cluster at pos 17) |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | L3 negation/absence features (cluster at pos 17) | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L3:F2232](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) | 17 | L3 negation/absence features (cluster at pos 17) |  character sequences like "NOC", "NO", "ORES", "NOS", "OF", "UNCH", and "oooooooo" within a series of hexadecimal codes, sometimes also picking up on related words such as "dangerously", "Bantus", "slave", and "plantation" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2232) |
| [L3:F9803](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) | 17 | L3 negation/absence features (cluster at pos 17) | sentences describing scientific studies or experiments, particularly where something is disproven | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9803) |
| [L3:F3669](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3669) | 2 | L3 negation/absence features (cluster at pos 17) |  references to ordinal rankings of things | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3669) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | L4 multilingual negation features (pos 17) | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | L4 multilingual negation features (pos 17) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F13171](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13171) | 17 | L4 multilingual negation features (pos 17) |  passages where something is negated | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13171) |
| [L9:F14687](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) | 17 | L9:F14687 — 'not' followed by 'because'/'but' (act 9.25) | phrases using the word "not", often followed by "because" or "but." | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14687) |
| [L15:F6160](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/6160) | 17 | L15 negation features (pos 17) |  occurrences of "is there" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/6160) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 17 | L15 negation features (pos 17) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 17 | L16:F12358 — 'not' followed by a form of 'to be' (act 28.25) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:2422 de=-1.273 |
| 3 | `inspect_feature` ×15 | L4:2422, L4:4492, L3:1101, L3:8011, L3:12079, L3:2232, L0:4958, L3:9803, L2:16097, L3:3669, L0:11375, L16:12358, L1:14233, L1:15749, L9:14687 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@17` | ❌ error | — | — | Trace upstream from L16:F12358 ("not" followed by a form of "to be") to find wha… |
| SA-2 | `L4:F2422@17` | ❌ error | — | — | Trace upstream from L4:F2422 (negations in foreign languages) to find what input… |
| SA-3 | `L4:F4492@17` | ❌ error | — | — | Trace upstream from L4:F4492 (negations in various languages) to find what input… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F12358@17, k=15 → Emb:" not"@17 (de=23.12) +14 more |
| 2 | `get_upstream_features` | L4:F2422@17, k=15 → Emb:" not"@17 (de=16.50) +14 more |
| 3 | `get_upstream_features` | L4:F4492@17, k=15 → Emb:" not"@17 (de=18.00) +14 more |
| 4 | `get_upstream_features` | L16:F12358@17, k=10 → Emb:" not"@17 (de=23.12) +9 more |
| 5 | `inspect_feature` ×4 | L15:6160, L15:10071, L2:12021, L4:13171 |

### Build

`build_circuit` → 15 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,401 | 4,829 | 154,605 | 0 | $0.0305 | — | — |
| **Total** | | **51,401** | **4,829** | **154,605** | **0** | **$0.0305** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 1s