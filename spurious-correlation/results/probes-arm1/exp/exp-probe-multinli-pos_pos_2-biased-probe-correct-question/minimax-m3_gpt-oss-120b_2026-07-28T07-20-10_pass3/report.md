# Circuit Oracle Report
**Date:** 2026-07-28 07:20:10 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" classification is driven primarily by **spurious surface-level features** — negation tokens ("haven't", "isn't"-style apostrophe-t), discourse markers ("yeah", "well", "uh"), and the word "because" — rather than by the prompt's actual semantic content (e.g., NCAA tournament, Louisville, Sweet 16). The circuit is built almost entirely on conversational/hesitation signals.

**Confidence:** 8

**Reasoning:**

The top features driving the probe (sorted by absolute direct_effect on the contradiction logit) are:

**Strongest POSITIVE drivers (toward contradiction):**
- **L0:6236** (pos 37, "t" — fires after "isn'" or "doesn'", promoted tokens: "not", "Not", "NOT"; frac_nonzero 0.0026): the apostrophe-t of "haven't". Direct effect +0.535.
- **L0:3820** (pos 3, "the", frac 0.030): generic "the" detector. +0.459.
- **L0:16366** (pos 25, "because", suppressed token: "because"; frac 0.018): the word "because" used as a causal connector. +0.373.
- **L0:15972** (pos 1, "yeah", frac 0.0013): the filler "yeah". +0.289.
- **L4:4492** (pos 37, **"negations in various languages"** — fires on "n't"/"pas"/"tak"/"nicht", frac 0.038): a multilingual negation detector. +0.311.
- **L4:430** (pos 14, on token like "it" / "I haven't…") and **L4:5862** (pos 2): additional positive contributions at layer 4.

**Strongest NEGATIVE drivers (against contradiction):**
- **L4:9602** (pos 4, "interjections and filler words" — "uh"/"hmm"/"ahem", frac 0.006): filler "uh" suppresses the contradiction score. −0.629.
- **L0:8352** (pos 2, "well", frac 0.004): the discourse marker "well" suppresses it. −0.547.
- **L4:12126** (pos 2, "expressions of agreement or acknowledgement, particularly 'well' and 'yeah'", frac 0.012): another agreement-marker detector. −0.488.
- **L2:5201** (pos 8, "awards and accomplishments in the context of sports" — "championship"/"NCAA Championship"): the actual sports content slightly *reduces* the contradiction score. −0.377.
- **L1:177** (pos 6, "double"/"multi-"): also negative. −0.387.
- **L5:2740** (pos 2, "conversational language"): slightly negative. −0.266.

**Mechanism summary:** The "contradiction" probe picks up the *presence of negation words* (L0:6236 on "t" of "haven't", L4:4492 explicit "negations in various languages") and *causal/junction words* (L0:16366 "because") as positive evidence, while *filler words and agreement markers* (L4:9602 "uh", L0:8352 "well", L4:12126 "well/yeah") act as suppressors. There is no entity-specific feature for "Louisville", "NCAA", or "Sweet 16" — the only sports-related feature (L2:5201, "championships in sports") actually pushes *against* the contradiction label.

This is **exactly the user concern**: the probe is latching onto **shallow lexical cues — negation, conjunctions, and discourse markers — rather than the actual semantic content of the premise** (the contradiction should be about not watching the tournament because Louisville was eliminated, not about the mere presence of "haven't" and "because"). The circuit is a textbook example of a probe relying on a spurious "negation-words ⇒ contradiction" shortcut, with the "yeah well uh" conversational preamble simultaneously reducing the score through its own discourse-marker features — a tug-of-war between two surface-level heuristics, neither of which engages the propositional content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' double' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: ' because' (pos 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 35 | Emb: ' haven' (pos 35) and 't' (pos 37) - "haven't" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 37 | Emb: ' haven' (pos 35) and 't' (pos 37) - "haven't" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' the' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'yeah' (pos 1), 'well' (pos 2), ' uh' (pos 4) - discourse markers | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: 'yeah' (pos 1), 'well' (pos 2), ' uh' (pos 4) - discourse markers | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: 'yeah' (pos 1), 'well' (pos 2), ' uh' (pos 4) - discourse markers | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: ' tournament' (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 37 | Layer 0 lexical features (spurious/formatting detectors) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Layer 0 lexical features (spurious/formatting detectors) |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Layer 0 lexical features (spurious/formatting detectors) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | Layer 0 lexical features (spurious/formatting detectors) |  the word "well" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L0:F15972](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) | 1 | Layer 0 lexical features (spurious/formatting detectors) | the word "yeah" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) |
| [L0:F10780](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) | 6 | Layer 0 lexical features (spurious/formatting detectors) |  LaTeX commands for including packages and defining document class | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) |
| [L0:F7893](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) | 6 | Layer 0 lexical features (spurious/formatting detectors) | the word "double" and words related to entrances and entering | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) |
| [L0:F4541](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) | 1 | Layer 0 lexical features (spurious/formatting detectors) |  adverbs of certainty such as "obviously" and related words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) |
| [L1:F177](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) | 6 | Layer 1 'double'/'NCAA' specific feature |  the word "double" and words that begin with "multi" or "doubly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| [L1:F13255](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13255) | 8 | Layer 1 'double'/'NCAA' specific feature |  the word "season" and words associated with it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13255) |
| [L2:F5201](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) | 8 | Layer 2 sports/negation/hesitation features | awards and accomplishments in the context of sports | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) |
| [L2:F9629](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) | 4 | Layer 2 sports/negation/hesitation features |  interjections and sounds of hesitation or acknowledgment | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) |
| [L2:F752](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) | 4 | Layer 2 sports/negation/hesitation features | phrases expressing personal opinions or viewpoints, often using words like "I," "think," "kind of," and related terms. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) |
| [L3:F7140](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7140) | 4 | Layer 3 negation-context features (e.g., L3:7140 on 'uh', L3:16039 on 'uh') | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7140) |
| [L3:F16039](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16039) | 4 | Layer 3 negation-context features (e.g., L3:7140 on 'uh', L3:16039 on 'uh') | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16039) |
| [L4:F9602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) | 4 | Layer 4 discourse/interjection/negation features (the main positive drivers) |  interjections and filler words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) |
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Layer 4 discourse/interjection/negation features (the main positive drivers) |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 37 | Layer 4 discourse/interjection/negation features (the main positive drivers) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Layer 4 discourse/interjection/negation features (the main positive drivers) |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L4:F430](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/430) | 14 | Layer 4 discourse/interjection/negation features (the main positive drivers) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/430) |
| [L4:F5862](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5862) | 2 | Layer 4 discourse/interjection/negation features (the main positive drivers) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5862) |
| [L5:F2740](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2740) | 2 | Layer 5 conversational language feature |  conversational language | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2740) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe (contradiction) logit | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'contradiction' is not one of the top-k next-token can |
| 3 | `get_top_features` | 25 features; top: L4:9602 de=-0.629 |
| 4 | `inspect_feature` ×10 | L0:6236, L0:3820, L0:16366, L4:9602, L0:8352, L4:12126, L4:4492, L4:4847, L2:5201, L1:177 |
| 5 | `get_upstream_features` | Emb:" uh"@4 (de=11.44) +9 more |
| 6 | `get_upstream_features` | Emb:"t"@37 (de=18.25) +9 more |
| 7 | `get_upstream_features` | Emb:" because"@25 (de=40.75) +9 more |
| 8 | `get_upstream_features` | Emb:"t"@37 (de=6.53) +9 more |
| 9 | `get_upstream_features` | Emb:" double"@6 (de=15.62) +9 more |
| 10 | `get_upstream_features` | Emb:"yeah"@1 (de=26.62) +9 more |
| 11 | `inspect_feature` ×8 | L0:10780, L0:15972, L0:4541, L0:7893, L1:13255, L2:9629, L2:752, L5:2740 |
| 12 | `get_upstream_features` | Emb:" the"@3 (de=32.75) +9 more |
| 13 | `get_upstream_features` | Emb:" tournament"@8 (de=16.38) +9 more |
| 14 | `get_upstream_features` | Emb:" double"@6 (de=24.00) +9 more |
| 15 | `get_upstream_features` | Emb:" well"@2 (de=30.88) +9 more |
| 16 | `get_upstream_features` | Emb:" well"@2 (de=14.62) +9 more |
| 17 | `inspect_feature` ×2 | L0:6236, L0:16366 |

### Build

`build_circuit` → 13 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 42,437 | 5,081 | 118,379 | 0 | $0.0259 | — | — |
| **Total** | | **42,437** | **5,081** | **118,379** | **0** | **$0.0259** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 7s