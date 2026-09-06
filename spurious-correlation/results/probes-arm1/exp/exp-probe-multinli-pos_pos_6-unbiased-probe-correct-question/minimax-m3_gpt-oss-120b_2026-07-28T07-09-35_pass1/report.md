# Circuit Oracle Report
**Date:** 2026-07-28 07:09:35 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe fires on a heterogeneous mix of generic lexical word-form detectors (e.g., L0:F2238 "about", L0:F15492 "for", L0:F8444 "to", L2:F11518 "land", L2:F4819 "fire", L1:F361 "agriculture/ecology", L2:F10849 "set") and sentence-structure features (L17:F451 sentence-start, L0:F6051 punctuation, L12:F12606 political/narrative), with **no semantic, sentential, or negation-aware feature** in the top-20 — directly supporting the user's concern.

**Confidence:** 9

**Reasoning:** The probe is driven by a noisy bag of single-word lexical detectors rather than a meaning-bearing circuit. Of the 20 top features by direct-effect magnitude, **at least 14 are pure word-form features** (activated on individual surface tokens like "about", "for", "to", "land", "fire", "set", "agriculture", "they", "I/Exactly") with frac_nonzero in the 0.002–0.057 range — typical of generic vocabulary detectors, not contradiction-specific reasoning. Specifically:

- The **largest single positive contribution** comes from L2:F11518 ("land" in agricultural contexts, direct_effect=+0.252) and L2:F15312 (the word "about", direct_effect=+0.21), but these are activated by *any* occurrence of the word in any context.
- The **largest negative contributions** (L0:F3498 "they" pronoun, direct_effect=−0.621; L0:F2238 "about", direct_effect=−0.342; L4:F12225 "transitional conclusion" words like "so"/"therefore", direct_effect=−0.275; L8:F8406 "I/Exactly", direct_effect=−0.243) push the probe *away* from the contradiction direction.
- Critical absence: there is **no feature encoding negation, semantic incompatibility, or sentence-pair contradiction** in the top-20. The lexical "fire" feature (L2:F4819) and "land" (L3:F15978) features would fire on *any* sentence containing those words regardless of whether the pair is contradictory. Sentence-level features like L17:F451 (sentence-start words) and L0:F6051 (periods/spaces) are purely syntactic.

Tracing upstream from the mid-layer features confirms this: L2:F4819 ("fire") receives its dominant activation directly from the embedding of the token "fire" at pos 12 (direct_effect=32), and L2:F11518 ("land") is driven by the "land" embedding at pos 7 (direct_effect=28.375). The signal flows **raw token-embedding → single-word lexical detector → probe**, with no compositional or semantic-reasoning layer. The so-called "negation signal" the user suspected is absent; what the probe actually uses is even shallower — a *spurious lexical bag* that happens to contain contradiction-correlated vocabulary in the training set, not the model recognizing that "setting fire to forest" contradicts "not allowed to deforest".

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | Lexical: pronoun 'they' (L0:F3498) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | Lexical: 'about' (L0:F2238) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F15492](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) | 8 | Lexical: 'for' (L0:F15492) |  the word "for" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 13 | Lexical: 'to' (L0:F8444) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L2:F14822](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14822) | 1 | Lexical: 'SO' abbrev (L2:F14822) |  the abbreviation "SO" followed by other characters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14822) |
| [L2:F15312](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) | 4 | Lexical: 'about' word (L2:F15312) |  the word "about." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) |
| [L3:F4464](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) | 4 | Lexical: 'about' (L3:F4464) |  the word "about" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) |
| [L1:F461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) | 7 | Lexical: 'land' (L1:F461) |  the word "land" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) |
| [L2:F11518](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) | 7 | Lexical: 'land' in agricultural context (L2:F11518) |  the word "land" in scientific/agricultural contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) |
| [L3:F15978](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15978) | 7 | Lexical: land/property/acreage (L3:F15978) |  mentions of land, property, and acreage. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15978) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | Lexical: 'fire' sentences (L2:F4819) | sentences containing the word "fire" or similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L2:F10849](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) | 3 | Lexical: 'set' (L2:F10849) | the word "set" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) |
| [L4:F5450](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) | 4 | Lexical: 'begin/start' (L4:F5450) |  code snippets from different languages and words related to starting or beginning something | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) |
| [L6:F14744](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) | 4 | Lexical: 'about'/'to'/'work' cluster (L6:F14744) |  the words "about," "to," and "work." | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Lexical: 'I'/'Exactly' (L8:F8406) | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L4:F12225](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) | 2 | Lexical: transitional conclusion (L4:F12225) |  transitional conclusion words, often used in legal or academic writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) |
| [L1:F361](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) | 9 | Lexical: agriculture/ecology words (L1:F361) |  words related to agriculture and ecology | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Lexical: sentence-start words (L17:F451) | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 18 | Lexical: punctuation/period (L0:F6051) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 25 | Lexical: political/conspiracy/storytelling (L12:F12606) |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3498 de=-0.621 |
| 3 | `inspect_feature` ×20 | L0:3498, L0:2238, L4:12225, L2:11518, L8:8406, L4:5450, L2:15312, L3:4464, L1:461, L2:4819, L0:8444, L2:10849, L0:15492, L3:15978, L6:14744, L17:451, L12:12606, L0:6051, L2:14822, L1:361 |
| 4 | `get_upstream_features` | Emb:" fire"@12 (de=32.00) +9 more |
| 5 | `get_upstream_features` | Emb:" land"@7 (de=28.38) +9 more |
| 6 | `get_upstream_features` | Emb:" about"@4 (de=13.69) +9 more |
| 7 | `get_upstream_features` | Emb:"<bos>"@0 (de=10.25) +9 more |
| 8 | `get_upstream_features` | Emb:" they"@2 (de=12.75) +9 more |

### Build

`build_circuit` → 34 nodes, 48 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 62,171 | 6,063 | 108,078 | 0 | $0.0324 | — | — |
| **Total** | | **62,171** | **6,063** | **108,078** | **0** | **$0.0324** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 4s