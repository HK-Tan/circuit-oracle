# Circuit Oracle Report
**Date:** 2026-07-28 07:11:04 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven by a bag of *surface-form* signals (entity name "Congress", function words "began/to/include", possessive "our", and single-word tokens) at L0–L4, with no semantic relation-detection features present in the circuit.

**Confidence:** 7

**Reasoning:** The probe's classification is supported by token-level and bag-of-words features rather than contradiction-specific semantics. Tracing shows three supernodes feeding the output:

- **`ent_congress_late`** (L2–L3): L2:F2701 (de=+0.85, "words related to the U.S. Congress") and L3:F123 (de=+0.25, "mentions of the United States Congress") are strongly *promoting* the contradiction score, with **Emb:Congress(pos 2)** as the dominant upstream (direct_effect 28.1 and 20.6 respectively). L2:F6735 (political parties/politicians) pushes in the opposite direction, indicating the same entity is read inconsistently by different sub-circuits.

- **`include_late`** (L3): L3:F5753 ("includes/containing", de=+0.53) and L3:F8351 ("including", de=−0.35) trace directly to **Emb:include(pos 12)**. The premise says "began to include many members who did not support" — a literal lexical match, not a contradiction-aware relation.

- **`began_to_late`** (L1–L4): L4:F59 ("phrases with 'to' preceded by start/begin", de=+0.41) and L3:F12596 (de=+0.83 in chain) trace to **Emb:began(pos 10)** and **Emb:to(pos 11)** — a collocational pattern, not a contradiction cue.

- **`wordlevel_l0`** (L0): an entire layer of single-word detectors — "yield", "Congress", "registration", "who", "which", "include", "to", "funding", "levels", "our", "comma", "level" — each contributing small but positive direct effects. These are pure bag-of-words; none encode relation/semantic content.

Critically, **the hypothesis contains the word "Congress"** and the phrase "controls our funding levels" — many of the same lexical items as the premise. The probe appears to fire whenever premise and hypothesis share *vocabulary* (Congress, include, funding, levels, our, who) rather than detecting a logical contradiction. There is no feature in the circuit that encodes negation, entailment direction, polarity reversal, or any contradiction-specific relation — the few features that do (L0:F195 "who" with direct_effect −0.205, L4:F7775 "various forms of punctuation" +0.21) are structural rather than semantic. This is consistent with the user concern: the classifier relies on spurious single-word and entity-name surface features, not on actual contradiction content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | Late-layer entity features about Congress / political bodies |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | Late-layer entity features about Congress / political bodies |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L2:F6735](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) | 2 | Late-layer entity features about Congress / political bodies |  political parties and politicians | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) |
| [L3:F5753](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) | 12 | Late-layer 'includes/includes members' features |  the word "includes" or "containing". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5753) |
| [L3:F8351](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8351) | 12 | Late-layer 'includes/includes members' features |  words related to including and code language symbols | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8351) |
| [L4:F59](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) | 11 | Late-layer 'began to ...' sequence features |  phrases with the word 'to' preceded by a verb or the word 'start' or 'begin'. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/59) |
| [L3:F12596](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) | 11 | Late-layer 'began to ...' sequence features |  actions or methods, sometimes preceeded by the preposition 'a' or 'to'. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12596) |
| [L2:F11469](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11469) | 11 | Late-layer 'began to ...' sequence features |  the word "to" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11469) |
| [L3:F4374](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4374) | 11 | Late-layer 'began to ...' sequence features |  instances of the word "to" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4374) |
| [L1:F13759](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13759) | 11 | Late-layer 'began to ...' sequence features | the word 'to' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13759) |
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F15411](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) | 2 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) |  terms relating to political bodies, figures, and processes | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15411) |
| [L0:F10198](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) | 2 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) |  the word "Congress" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10198) |
| [L0:F7021](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7021) | 2 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) |  the word "Congress" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7021) |
| [L0:F14517](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14517) | 12 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) | the word "including" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14517) |
| [L0:F10783](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) | 12 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) |  the word "include" (and variations of the word) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 11 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F13437](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) | 15 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) |
| [L0:F13564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13564) | 4 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) | the word "which" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13564) |
| [L0:F11640](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11640) | 7 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11640) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 9 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) |  commas and sometimes reach (context not clear) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L0:F14818](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14818) | 8 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) | the word "level" when referring to a level of government or societal organization | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14818) |
| [L0:F15773](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15773) | 6 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) |  the possessive pronoun "our" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15773) |
| [L0:F195](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/195) | 15 | Layer-0 single-word features (yield, Congress, funding, our, which, who, comma) | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/195) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:2701 de=0.848 |
| 3 | `inspect_feature` ×5 | L2:2701, L3:5753, L0:6044, L0:15411, L4:59 |
| 4 | `get_top_features` | 50 features; top: L2:2701 de=0.848 |
| 5 | `inspect_feature` ×10 | L0:10401, L2:6735, L3:8351, L0:9557, L3:123, L0:10783, L0:195, L0:13564, L0:13437, L1:4224 |
| 6 | `get_upstream_features` | Emb:" include"@12 (de=41.00) +14 more |
| 7 | `get_upstream_features` | Emb:" Congress"@2 (de=28.12) +14 more |
| 8 | `get_upstream_features` | Emb:" began"@10 (de=13.31) +14 more |
| 9 | `get_upstream_features` | Emb:" include"@12 (de=28.38) +14 more |
| 10 | `get_upstream_features` | Emb:" Congress"@2 (de=9.12) +14 more |
| 11 | `get_upstream_features` | Emb:" to"@11 (de=21.62) +14 more |
| 12 | `get_upstream_features` | Emb:" began"@10 (de=10.88) +14 more |
| 13 | `get_upstream_features` | Emb:" began"@10 (de=10.50) +14 more |
| 14 | `get_upstream_features` | Emb:" include"@12 (de=25.50) +9 more |
| 15 | `get_upstream_features` | Emb:" Congress"@2 (de=17.00) +9 more |
| 16 | `get_upstream_features` | Emb:" Congress"@2 (de=17.00) +9 more |
| 17 | `inspect_feature` ×2 | L1:3276, L3:12596 |
| 18 | `get_upstream_features` | Emb:" Congress"@2 (de=17.00) +9 more |
| 19 | `get_upstream_features` | Emb:"The"@1 (de=6.84) +9 more |
| 20 | `get_upstream_features` | Emb:" Congress"@2 (de=17.25) +9 more |
| 21 | `get_upstream_features` | Emb:" Congress"@2 (de=17.00) +9 more |
| 22 | `inspect_feature` ×6 | L0:8444, L1:13759, L2:11469, L3:4374, L0:9557, L0:195 |
| 23 | `get_upstream_features` | Emb:" began"@10 (de=10.50) +9 more |
| 24 | `get_upstream_features` | Emb:" Congress"@2 (de=20.62) +9 more |
| 25 | `get_upstream_features` | Emb:","@9 (de=4.94) +9 more |
| 26 | `inspect_feature` | " various forms of punctuation" |
| 27 | `get_upstream_features` | Emb:" who"@15 (de=35.25) +9 more |
| 28 | `get_upstream_features` | Emb:" which"@4 (de=37.00) +9 more |
| 29 | `get_upstream_features` | Emb:" funding"@7 (de=13.19) +9 more |
| 30 | `get_upstream_features` | Emb:" levels"@8 (de=14.69) +9 more |
| 31 | `inspect_feature` ×3 | L0:14818, L0:4870, L0:15773 |
| 32 | `get_upstream_features` | Emb:" funding"@7 (de=13.19) +9 more |
| 33 | `get_upstream_features` | Emb:" levels"@8 (de=14.69) +9 more |
| 34 | `inspect_feature` ×3 | L4:101, L0:10198, L0:15773 |
| 35 | `get_upstream_features` | Emb:" to"@11 (de=8.19) +9 more |
| 36 | `get_upstream_features` | Emb:" include"@12 (de=25.50) +7 more |
| 37 | `inspect_feature` ×24 | L2:11734, L0:11738, L1:3271, L0:14517, L1:2493, L0:8444, L0:5585, L2:13152, L0:7021, L1:14850, L1:2335, L1:6853, L1:3231, L1:4020, L1:13759, L3:12596, L1:5475, L0:13168, L0:13417, L1:2408, L0:14818, L1:14028, L0:14517, L0:13437 |
| 38 | `get_upstream_features` | Emb:","@9 (de=5.28) +9 more |
| 39 | `get_upstream_features` | Emb:" who"@15 (de=35.25) +9 more |
| 40 | `inspect_feature` | "the word "including"" |
| 41 | `get_upstream_features` | Emb:" began"@10 (de=13.31) +7 more |
| 42 | `get_upstream_features` | Emb:" include"@12 (de=12.88) +7 more |
| 43 | `get_upstream_features` | Emb:" to"@11 (de=17.50) +7 more |

### Build

`build_circuit` → 14 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 110,048 | 8,084 | 1,038,409 | 0 | $0.1050 | — | — |
| **Total** | | **110,048** | **8,084** | **1,038,409** | **0** | **$0.1050** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 21s