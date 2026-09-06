# Circuit Oracle Report
**Date:** 2026-07-28 07:22:35 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by lexical-topic features (single-word detectors for "recorded", "record", "menu", "will", "code", finance/Title/domestic-related vocabulary) and a small mid-layer integration supernode for the menu/recording/UI domain, anchored almost entirely on the content-noun tokens themselves rather than on negation/contradiction cues.

**Confidence:** 6

**Reasoning:** The output is a contradiction-classification probe score on the SNLI-style premise "A recorded menu will provide information on how to obtain these lists. Recorded menus do not provide any information at this time." The top direct-effect features on the probe are exclusively word-detector features for the content vocabulary: **L0:F2108 "menu"** (DE=+0.32), **L0:F7443 "record"** (DE=+0.32), **L0:F8046 "will"** (DE=+0.34) and the parallel **L1:F12253 "menu"** (DE=−0.43) and **L1:F3691 "recording"** (DE=+0.34). The deepest feature is the very early **L2:F8776 "finance/property-law"** (DE=+0.52, frac=0.011), which upstream-traces to the raw **" recorded"** token embedding (pos 2, DE=+19.5) with secondary contributions from **"A"** (−1.65) and **"<bos>"** (+1.35). L1:F3691 "recording" and L0:F2108 "menu" similarly trace directly to the " recorded" (DE=+24.75) and " menu" (DE=+25.75) embeddings respectively. Mid-layer integrations L3:F3573 "menu in interface elements" and L2:F3648 "code snippets about menus" are menu/UI topic detectors — the "menu" token in this SNLI prompt is from a topic about telephone-recorded menus (a telephone-IVR domain), which the L4:F7998 telecom feature (DE=−0.23) and L2:F8776 finance/law feature pick up on, along with L2:F9012 "failed" (DE=−0.29) which is activated by the *style* of the legal/UI corpora these vocabulary features co-occur in, not by any actual negation in the premise. L0:F4523 "domestic/globalism" (DE=−0.19) and L2:F188 "will" (DE=−0.21) similarly fire on co-occurring register words. There is no detected feature whose label, top activating examples, or promoted tokens correspond to a negation word ("no", "not", "never", "any"), a contradiction cue, or a polarity-reversal pattern. The user's hypothesis that the probe is using "negation words" is *not* supported by this attribution graph: instead, the circuit shows the probe is using **content-domain lexical features** (recorded/menu/will) plus a handful of co-occurrence-driven features (finance-law, code snippets, telecom, "failed" in legal opinions, "domestic") that all piggyback on the *vocabulary* of the premise rather than its semantic structure. This is "lexical" rather than "negation" — the model appears to associate the *telephone-IVR / menu / recorded information* topic with a contradiction class label (likely because in the NLI training data, premise–hypothesis pairs about telephone recorded-menu systems are often contradictions or entailments tied to that surface vocabulary), but it does so via topic-feature detection, not via explicit negation detection. The strongest causal paths are all from embedding(" recorded") → L1:F3691/L0:F7443 → L2:F8776 and embedding(" menu") → L0:F2108/L1:F12253 → L3:F3573 → probe, with the "failed" and finance-law features being weaker secondary contributors. Because every feature identified is a content or topic detector rather than a contradiction cue, the user's specific concern (that the probe uses "spurious negation signals") is *not* confirmed by this graph; if anything, the probe appears to be using *spurious topic/vocabulary* features — a related but distinct failure mode (lexical shortcut learning) rather than negation-feature shortcut learning.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | Lexical: "recorded/record/menu/will" features (domain topic words) |  the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | Lexical: "recorded/record/menu/will" features (domain topic words) | the word "record" appearing in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | Lexical: "recorded/record/menu/will" features (domain topic words) | the word "menu" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |
| [L1:F12253](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) | 3 | Lexical: "recorded/record/menu/will" features (domain topic words) |  the word 'menu' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 4 | Lexical: "recorded/record/menu/will" features (domain topic words) |  the word "will." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | Lexical secondary: finance/finance-law, "Title", "word", "domestic", "record" verb, "will" future, "faith", code/Java snippets |  words related to finance and property law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L0:F6649](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) | 3 | Lexical secondary: finance/finance-law, "Title", "word", "domestic", "record" verb, "will" future, "faith", code/Java snippets |  the word "Title" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) |
| [L0:F7404](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) | 2 | Lexical secondary: finance/finance-law, "Title", "word", "domestic", "record" verb, "will" future, "faith", code/Java snippets |  the word "faith", sometimes in association with related ideas like "links" or "opportunities" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) |
| [L0:F5128](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) | 3 | Lexical secondary: finance/finance-law, "Title", "word", "domestic", "record" verb, "will" future, "faith", code/Java snippets |  the word "words" or words that are similar in meaning (word, Word, phrases, matrix) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) |
| [L0:F4523](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) | 3 | Lexical secondary: finance/finance-law, "Title", "word", "domestic", "record" verb, "will" future, "faith", code/Java snippets | the word "domestic" and words associated with globalism | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4523) |
| [L2:F3059](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) | 2 | Lexical secondary: finance/finance-law, "Title", "word", "domestic", "record" verb, "will" future, "faith", code/Java snippets |  the verb "record" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) |
| [L2:F188](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) | 4 | Lexical secondary: finance/finance-law, "Title", "word", "domestic", "record" verb, "will" future, "faith", code/Java snippets | the word "will" in various contexts, sometimes alongside words related to consequences or legal matters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) |
| [L0:F12200](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12200) | 2 | Lexical secondary: finance/finance-law, "Title", "word", "domestic", "record" verb, "will" future, "faith", code/Java snippets |  a variety of specific nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12200) |
| [L0:F13280](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) | 2 | Lexical secondary: finance/finance-law, "Title", "word", "domestic", "record" verb, "will" future, "faith", code/Java snippets |  passages discussing real estate | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) |
| [L1:F14137](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14137) | 2 | Lexical secondary: finance/finance-law, "Title", "word", "domestic", "record" verb, "will" future, "faith", code/Java snippets |  words or phrases that appear in legal or technical documents, like names of laws, legal terms (pleaded, testified), and technical terms, especially when abbreviated or in code | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14137) |
| [L3:F3573](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) | 3 | "menu"/"code menu"/"failed"/telecom: late-layer integrations of menu/recorded/recording topic | the word "menu" often in conjunction with interface elements | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) |
| [L2:F3648](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) | 3 | "menu"/"code menu"/"failed"/telecom: late-layer integrations of menu/recorded/recording topic | code snippets related to menus and restaurants | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) |
| [L4:F7998](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) | 3 | "menu"/"code menu"/"failed"/telecom: late-layer integrations of menu/recorded/recording topic |  words related to telecommunications and telephones | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) |
| [L2:F4147](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4147) | 2 | "menu"/"code menu"/"failed"/telecom: late-layer integrations of menu/recorded/recording topic |  the word "recorded" (and related reporting terms) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4147) |
| [L2:F9012](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9012) | 3 | "menu"/"code menu"/"failed"/telecom: late-layer integrations of menu/recorded/recording topic |  instances where something was not successful | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9012) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L2:8776 de=0.523 |
| 3 | `inspect_feature` ×6 | L2:8776, L0:2108, L1:12253, L0:8046, L1:3691, L0:7443 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F8776@2` | ❌ error | — | — | Trace the upstream path from L2:F8776 (pos 2). What input token does this featur… |
| SA-2 | `L1:F3691@2` | ❌ error | — | — | Trace the upstream path from L1:F3691 (pos 2) — the "recording" feature. What in… |
| SA-3 | `L0:F2108@3` | ❌ error | — | — | Trace the upstream path from L0:F2108 (pos 3) — the "menu" feature. What does it… |
| SA-4 | `L0:F8046@4` | ❌ error | — | — | Trace the upstream path from L0:F8046 (pos 4) — the "will" feature. What does it… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F8776@2, k=10 → Emb:" recorded"@2 (de=19.50) +9 more |
| 2 | `get_upstream_features` | L1:F3691@2, k=10 → Emb:" recorded"@2 (de=24.75) +9 more |
| 3 | `get_upstream_features` | L0:F2108@3, k=10 → Emb:" menu"@3 (de=25.75) +9 more |
| 4 | `get_upstream_features` | L0:F8046@4, k=10 → Emb:" will"@4 (de=36.00) +9 more |
| 5 | `get_upstream_features` | L0:F7443@2, k=10 → Emb:" recorded"@2 (de=22.62) +9 more |
| 6 | `get_upstream_features` | L1:F12253@3, k=10 → Emb:" menu"@3 (de=20.62) +9 more |
| 7 | `inspect_feature` ×17 | L0:7404, L0:6649, L2:3059, L0:5128, L3:3573, L4:7998, L0:4523, L2:3648, L2:188, L1:7207, L0:14478, L1:14137, L0:6421, L0:13938, L0:4823, L0:12200, L0:13280 |
| 8 | `get_upstream_features` | L3:F3573@3, k=10 → Emb:" menu"@3 (de=21.38) +9 more |
| 9 | `get_upstream_features` | L2:F3648@3, k=8 → Emb:" menu"@3 (de=27.75) +7 more |
| 10 | `get_upstream_features` | L2:F188@4, k=8 → Emb:" will"@4 (de=26.00) +7 more |
| 11 | `get_upstream_features` | L2:F3059@2, k=8 → Emb:" recorded"@2 (de=22.50) +7 more |
| 12 | `get_upstream_features` | L0:F4523@3, k=8 → Emb:" menu"@3 (de=11.69) +7 more |
| 13 | `get_upstream_features` | L4:F7998@3, k=8 → Emb:" menu"@3 (de=13.56) +7 more |
| 14 | `inspect_feature` ×11 | L2:9012, L1:763, L2:4147, L0:11835, L1:581, L2:1838, L1:7463, L0:8047, L0:1903, L1:6817, L1:11170 |

### Build

`build_circuit` → 9 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 60,613 | 5,154 | 268,538 | 0 | $0.0405 | — | — |
| **Total** | | **60,613** | **5,154** | **268,538** | **0** | **$0.0405** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 24s