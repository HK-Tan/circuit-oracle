# Circuit Oracle Report
**Date:** 2026-07-28 07:23:28 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven by a mix of (a) a true lexical/structural negation signal from the contraction "haven't" in the second clause ("I haven't missed…") and (b) a large weight on surface-level "spoken / hedging" features — the casual filler "uh", the acknowledgement word "well", the conversational interjection "yeah" at the start, and generic L2–L4 "informal-conversation" detectors — with only weak representation of the actual NC-double-A / Louisville / Sweet 16 entity content (a single L2:F5201 "awards in sports" feature at pos 8 and scattered L0–L1 "double" detectors, all with small magnitudes and many of them off-context for "NC double A").

**Confidence:** 7

**Reasoning:** The single most positive output-driving feature is **L4:F4492** at pos 37, "negations in various languages" (frac_nonzero ≈ 0.038, activation 7.28, direct_effect +0.31). Its top-1 upstream is the embedding of token "t" (pos 37, the final t of "haven't") with direct_effect 6.53, then the embedding of "haven" (pos 35, +1.30), and then **L0:F6236** at pos 37 — a feature whose autointerp is "the letter 't' when it follows the word 'isn'' or 'doesn''", promoted tokens are "▁not / Not / NOT / nicht / niet / ikke" (multilingual negation), and frac_nonzero = 0.0026. Tracing one further hop into L2:F1337 ("negated verbs with personal pronouns, and foreign language pronouns", promoted tokens "▁been / has / have / had", frac_nonzero ≈ 0.01) confirms the signal is the genuine English contraction "haven't" plus a secondary "I haven't" pronoun slot. So the *negation branch* of the circuit is anchored to actual prompt content ("haven't" at pos 35–37 and the subject "I" at pos 34) and is legitimate.

The two other output-driving L4 features, however, are pure surface-form: **L4:F9602** at pos 4 (autointerp "interjections and filler words", max-activations on "umm / mmm / hem / hmm", activation 27, direct_effect −0.63) and **L4:F12126** at pos 2 + **L4:F4847** at pos 2 (autointerp "expressions of agreement or acknowledgement, particularly 'well' and 'yeah'"). Their top upstream traces cleanly to the embeddings of token "uh" (pos 4, direct_effect 11.4) and tokens "well" (pos 2) and "yeah" (pos 1) — the model's *opening* filler "yeah well the uh" and the discourse-marker "well". The L2–L3 intermediate "informal conversation / opinions / hedges" cluster (L2:F859, L2:F752, L1:F2623, L3:F16039, L3:F3767, etc.) reinforces that the probe is partially keying on a *conversational register* signature, not on what the speaker said.

Crucially, the entity content the user might expect to see (Louisville, NCAA tournament, Sweet 16, the contradiction "I haven't watched… but I haven't missed a single game of the Sweet 16") is almost absent from the top of the circuit. L2:F5201 at pos 8 ("awards and accomplishments in the context of sports", promoted "▁honors / henne") is the only content-bearing feature with non-trivial magnitude, and it lives at "tournament" — not at the contradiction site. The "double" detectors (L0:F7893, L1:F177) are at pos 6 ("NC double A") but fire on the generic substring "double", not on NCAA specifically (their autointerp/supp-tokens show "double/multi-" math/science contexts, not sports). There is no circuit node aggregating "I haven't watched it… I haven't missed…" as a self-contradictory pair; the contradiction is detected as the bare presence of the contraction "haven't" plus a "negation in various languages" feature, with casual-filler "well/uh/yeah" features contributing most of the remaining signal.

**Mechanism summary:** The probe classifies this as contradiction primarily because (1) a multilingual-lexical negation detector fires on the "t" in "haven't" (legitimate content), and (2) a strong *spoken-discourse* signature accumulates from the opening "yeah well uh" and the interjection "well" at pos 2 (spurious — this register signature would fire on any hedged conversational utterance). The user is correct that the circuit uses "negation/spoken-discourse" surface features rather than a real semantic representation of the contradictory claim. The contradiction is read off "haven't + haven't" surface, with the contradiction's semantic content (watched vs. missed, tournament scope) essentially absent from the causal graph.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: 'uh' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 37 | Emb: 't' (pos 37, final t of haven't) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 35 | Emb: 'haven' (pos 35) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: 'well' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'yeah' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 34 | Emb: 'I' (pos 34) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: 'Louisville' (pos 26) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 29 | Emb: 'out' (pos 29) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: 'this' (pos 23/32) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | Layer 0-1: discourse filler / interjection detectors |  the word "well" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L0:F15972](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) | 1 | Layer 0-1: discourse filler / interjection detectors | the word "yeah" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) |
| [L2:F9629](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) | 4 | Layer 0-1: discourse filler / interjection detectors |  interjections and sounds of hesitation or acknowledgment | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Layer 0-1: discourse filler / interjection detectors | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L1:F4373](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4373) | 37 | Layer 0-1: discourse filler / interjection detectors | the letter "t" when it is an apostrophe and attached to another word | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4373) |
| [L1:F14233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) | 37 | Layer 0-1: discourse filler / interjection detectors | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14233) |
| [L1:F2532](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2532) | 35 | Layer 0-1: discourse filler / interjection detectors | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2532) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 37 | Layer 0-1: the final 't' of negation contractions (isn't/haven't) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L2:F1337](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) | 37 | Layer 1-3: negated verbs with personal pronouns / foreign language pronouns | negated verbs with personal pronouns, and foreign language pronouns | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 37 | Layer 1-3: negated verbs with personal pronouns / foreign language pronouns |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L3:F15210](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15210) | 37 | Layer 1-3: negated verbs with personal pronouns / foreign language pronouns |  the phrase "yet to be" (or variations with similar words) indicating something is pending or not fully realized. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15210) |
| [L2:F6993](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) | 37 | Layer 1-3: negated verbs with personal pronouns / foreign language pronouns | phrases describing uncertainty or difficulty | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6993) |
| [L3:F11632](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11632) | 37 | Layer 1-3: negated verbs with personal pronouns / foreign language pronouns |  code related to nil checks and storage | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11632) |
| [L1:F177](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) | 6 | Layer 1-3: 'double' / NCAA / tournament sports content (weak) |  the word "double" and words that begin with "multi" or "doubly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| [L0:F7893](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) | 6 | Layer 1-3: 'double' / NCAA / tournament sports content (weak) | the word "double" and words related to entrances and entering | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) |
| [L2:F5201](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) | 8 | Layer 1-3: 'double' / NCAA / tournament sports content (weak) | awards and accomplishments in the context of sports | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) |
| [L1:F2623](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2623) | 4 | Layer 2-4: casual conversation / opinion / interjection compounds |  words in the context of someone talking or expressing opinions. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2623) |
| [L2:F752](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) | 4 | Layer 2-4: casual conversation / opinion / interjection compounds | phrases expressing personal opinions or viewpoints, often using words like "I," "think," "kind of," and related terms. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) |
| [L2:F859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/859) | 4 | Layer 2-4: casual conversation / opinion / interjection compounds |  words that appear frequently in informal conversation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/859) |
| [L3:F7140](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7140) | 4 | Layer 2-4: casual conversation / opinion / interjection compounds | words or parts of words containing "man", "ent", "per", or "mate" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7140) |
| [L3:F16039](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16039) | 4 | Layer 2-4: casual conversation / opinion / interjection compounds |  section delimiters and incomplete quotes | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16039) |
| [L3:F2448](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2448) | 4 | Layer 2-4: casual conversation / opinion / interjection compounds |  multiple disparate things: youtube videos, computer terminology, links, sports teams, and short French sentences | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2448) |
| [L3:F3767](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3767) | 4 | Layer 2-4: casual conversation / opinion / interjection compounds |  specific phrases such as "e.g.", "array}", "for example", and "for instance" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3767) |
| [L0:F10780](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) | 6 | Layer 2-4: casual conversation / opinion / interjection compounds |  LaTeX commands for including packages and defining document class | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) |
| [L0:F4541](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) | 1 | Layer 2-4: casual conversation / opinion / interjection compounds |  adverbs of certainty such as "obviously" and related words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Layer 2-4: casual conversation / opinion / interjection compounds |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 37 | Layer 4: 'negations in various languages' (multilingual negation detector) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F9602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) | 4 | Layer 4: 'interjections and filler words' (uh/um/hmm) |  interjections and filler words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) |
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Layer 4: 'expressions of agreement or acknowledgement, particularly well and yeah' |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Layer 4: 'expressions of agreement or acknowledgement, particularly well and yeah' |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:9602 de=-0.629 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F9602@4` | ❌ error | — | — | Trace the path upstream from L4:F9602 at position 4. What does this feature enco… |
| SA-2 | `L0:F8352@2` | ❌ error | — | — | Trace the path upstream from L0:F8352 at position 2. What does this feature enco… |
| SA-3 | `L0:F6236@37` | ❌ error | — | — | Trace the path upstream from L0:F6236 at position 37. What does this feature enc… |
| SA-4 | `L4:F12126@2` | ❌ error | — | — | Trace the path upstream from L4:F12126 at position 2. What does this feature enc… |
| SA-5 | `L0:F3820@3` | ❌ error | — | — | Trace the path upstream from L0:F3820 at position 3. What does this feature enco… |
| SA-6 | `L1:F177@6` | ❌ error | — | — | Trace the path upstream from L1:F177 at position 6. What does this feature encod… |
| SA-7 | `L0:F16366@25` | ❌ error | — | — | Trace the path upstream from L0:F16366 at position 25. What does this feature en… |
| SA-8 | `L2:F5201@8` | ❌ error | — | — | Trace the path upstream from L2:F5201 at position 8. What does this feature enco… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×15 | L4:9602, L0:8352, L0:6236, L4:12126, L0:3820, L1:177, L2:5201, L0:16366, L4:4847, L0:10780, L0:4541, L4:4492, L0:7893, L2:9629, L0:15972 |
| 2 | `get_upstream_features` | L4:F4492@37, k=10 → Emb:"t"@37 (de=6.53) +9 more |
| 3 | `get_upstream_features` | L0:F6236@37, k=10 → Emb:"t"@37 (de=18.25) +9 more |
| 4 | `get_upstream_features` | L4:F9602@4, k=10 → Emb:" uh"@4 (de=11.44) +9 more |
| 5 | `get_upstream_features` | L2:F1337@37, k=10 → Emb:" haven"@35 (de=28.75) +9 more |
| 6 | `inspect_feature` ×13 | L2:752, L3:7140, L3:16039, L2:859, L1:2623, L3:2448, L3:3767, L2:1337, L1:4373, L3:1101, L3:15210, L2:6993, L3:11632 |

### Build

`build_circuit` → 18 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 85,108 | 7,123 | 112,121 | 0 | $0.0408 | — | — |
| **Total** | | **85,108** | **7,123** | **112,121** | **0** | **$0.0408** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 24s