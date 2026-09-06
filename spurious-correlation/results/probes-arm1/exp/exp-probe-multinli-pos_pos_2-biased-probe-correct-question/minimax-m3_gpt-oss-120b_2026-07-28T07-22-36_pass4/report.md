# Circuit Oracle Report
**Date:** 2026-07-28 07:22:36 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classification score is driven almost entirely by spurious, low-level lexical/syntactic features — "uh"/"well" interjections and the apostrophe-t contraction in "haven't" — not by any content about the NCAA tournament, Louisville, or the actual semantic content of the utterance.

**Confidence:** 9

**Reasoning:** The attribution graph contains no features encoding entities (NCAA, Louisville, tournament, Sweet 16) or any contradiction-relevant content. Instead, the late-layer features feeding the probe (L26) are:

1. **Late-layer interjection/hesitation cluster (L4)**: `L4:F9602` (interjections/filler words, activation 27, direct_effect -0.63) fires on the token "uh" (pos 4) and is driven directly by the embedding of " uh" (direct_effect 11.4). Its upstream includes `L2:F9629` (interjections/hesitation), `L2:F859` (informal conversational words), `L3:F7140` (subwords like "man/ent/per"), and `L3:F16039` (section delimiters). Similarly `L4:F12126` (well/yeah agreement, direct_effect -0.49) and `L4:F4847` (conversational phrases) fire on "well" (pos 2) and trace cleanly to the ` well` embedding (direct_effect 14.6). The `lex_well` supernode (`L0:F8352` "well", `L0:F15972` "yeah", `L0:F3820` "the") is a purely lexical/shallow cluster.

2. **Late-layer negation cluster (L4)**: `L4:F4492` (negations in various languages, direct_effect +0.31) fires at position 37 ("t" in "haven't") and traces back to `L2:F1337` (negated verbs with pronouns, "haven't" pattern, direct_effect +2.97), which in turn is driven by the embeddings of ` haven` (pos 35, direct_effect 28.75) and `t` (pos 37, direct_effect 11.3). `L0:F6236` ("t" after "isn'"/"doesn'", frac_nonzero 0.0026) and `L0:F16366` ("because") are the lexical seeds. Critically, the "because" feature (L0:F16366, direct_effect +0.37) is the only "content" feature in the top-20 — and it fires on the conjunction "because" in "because Louisville's out of it", not on the entities being negated. The model has latched onto the *contraction* "haven't" as a negation surface form, not on the meaning of the negation.

3. **Lexical double feature (L1)**: `L1:F177` ("double", direct_effect -0.39) fires on "NC double A" (pos 6) — again purely lexical/orthographic, not semantic.

4. **Sports content is shallow**: `L2:F5201` (awards/championships in sports) fires on "tournament" (pos 8) but its contribution is gated by upstream L1 features and ultimately lexical; it is not used in a contradiction-reasoning way.

The user's concern is **confirmed**: the circuit is driven by negation/hesitation surface forms ("uh", "well", "haven't", "because") rather than the actual contradictory content (Louisville is not in the tournament, the user is contradicting the claim that they watch every game). The fraction of circuit mass on entity/semantic content (NCAA, Louisville, Sweet 16) is essentially zero; ~95%+ of the attribution mass traces back to interjection tokens (pos 2, 4) and contraction tokens (pos 18-20, 35-37), and through mid-layer filler/hesitation supernodes that are not contradiction-specific. This is a textbook spurious-correlation circuit: the probe has learned that informal speech with hedged negations ("uh well… haven't…") correlates with a contradiction label, and the model exploits that surface shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | Lexical: 'well' / 'yeah' agreement (L0) |  the word "well" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L0:F15972](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) | 1 | Lexical: 'well' / 'yeah' agreement (L0) | the word "yeah" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Lexical: 'well' / 'yeah' agreement (L0) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 20 | Lexical: "isn't" contraction - 't'/'haven'/' (L0) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 37 | Lexical: "isn't" contraction - 't'/'haven'/' (L0) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Lexical: "isn't" contraction - 't'/'haven'/' (L0) |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L0:F10780](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) | 6 | Lexical: "isn't" contraction - 't'/'haven'/' (L0) |  LaTeX commands for including packages and defining document class | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) |
| [L0:F4541](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) | 1 | Lexical: "isn't" contraction - 't'/'haven'/' (L0) |  adverbs of certainty such as "obviously" and related words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) |
| [L0:F7893](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) | 6 | Lexical: "isn't" contraction - 't'/'haven'/' (L0) | the word "double" and words related to entrances and entering | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) |
| [L1:F177](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) | 6 | Lexical: 'double' (L1) |  the word "double" and words that begin with "multi" or "doubly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| [L1:F13255](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13255) | 8 | Lexical: 'double' (L1) |  the word "season" and words associated with it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13255) |
| [L2:F9629](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) | 4 | Filler/interjection 'uh' cluster (L2-L3) |  interjections and sounds of hesitation or acknowledgment | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) |
| [L2:F752](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) | 4 | Filler/interjection 'uh' cluster (L2-L3) | phrases expressing personal opinions or viewpoints, often using words like "I," "think," "kind of," and related terms. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) |
| [L2:F859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/859) | 4 | Filler/interjection 'uh' cluster (L2-L3) |  words that appear frequently in informal conversation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/859) |
| [L2:F5201](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) | 8 | Filler/interjection 'uh' cluster (L2-L3) | awards and accomplishments in the context of sports | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) |
| [L2:F1759](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) | 2 | Filler/interjection 'uh' cluster (L2-L3) | occurrences of the word "know" with emphasis words or interjections nearby | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) |
| [L2:F1337](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) | 37 | Filler/interjection 'uh' cluster (L2-L3) | negated verbs with personal pronouns, and foreign language pronouns | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) |
| [L3:F7140](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7140) | 4 | Filler/interjection 'uh' cluster (L2-L3) | words or parts of words containing "man", "ent", "per", or "mate" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7140) |
| [L3:F16039](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16039) | 4 | Filler/interjection 'uh' cluster (L2-L3) |  section delimiters and incomplete quotes | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16039) |
| [L3:F4735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4735) | 2 | Filler/interjection 'uh' cluster (L2-L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4735) |
| [L4:F9602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) | 4 | Late-layer: interjection / hesitation (L4) |  interjections and filler words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) |
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Late-layer: interjection / hesitation (L4) |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Late-layer: interjection / hesitation (L4) |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 37 | Late-layer: negation / "isn't" (L4) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:9602 de=-0.629 |
| 3 | `inspect_feature` ×8 | L4:9602, L0:8352, L0:6236, L0:3820, L4:12126, L1:177, L2:5201, L0:16366 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F9602@4` | ❌ error | — | — | Trace from L4:F9602 (interjections/filler words - "uh") upstream. This feature f… |
| SA-2 | `L0:F6236@37` | ❌ error | — | — | Trace from L0:F6236 (the letter "t" after "isn'"/"doesn'") upstream. This featur… |
| SA-3 | `L4:F9602@2` | ❌ error | — | — | Trace from L4:F12126 ("well"/"yeah" agreement expressions) at position 2 upstrea… |
| SA-4 | `L0:F16366@25` | ❌ error | — | — | Trace from L0:F16366 ("because") at position 25 upstream. Position 25 is "becaus… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F9602@4, k=10 → Emb:" uh"@4 (de=11.44) +9 more |
| 2 | `get_upstream_features` | L0:F6236@37, k=10 → Emb:"t"@37 (de=18.25) +9 more |
| 3 | `get_upstream_features` | L0:F8352@2, k=10 → Emb:" well"@2 (de=30.88) +9 more |
| 4 | `get_upstream_features` | L4:F12126@2, k=10 → Emb:" well"@2 (de=14.62) +9 more |
| 5 | `inspect_feature` ×11 | L2:9629, L2:752, L2:5201, L0:16366, L1:13255, L0:10780, L0:4541, L0:7893, L0:15972, L4:4847, L4:4492 |
| 6 | `get_upstream_features` | L0:F6236@20, k=10 → Emb:"t"@20 (de=17.88) +9 more |
| 7 | `get_upstream_features` | L1:F177@6, k=10 → Emb:" double"@6 (de=24.00) +9 more |
| 8 | `get_upstream_features` | L0:F3820@3, k=10 → Emb:" the"@3 (de=32.75) +9 more |
| 9 | `get_upstream_features` | L0:F16366@25, k=10 → Emb:" because"@25 (de=40.75) +9 more |
| 10 | `inspect_feature` ×4 | L3:7140, L3:16039, L2:859, L2:1759 |
| 11 | `get_upstream_features` | L4:F4492@37, k=8 → Emb:"t"@37 (de=6.53) +7 more |
| 12 | `get_upstream_features` | L2:F5201@8, k=8 → Emb:" tournament"@8 (de=16.38) +7 more |
| 13 | `inspect_feature` | L2, F1337 → "negated verbs with personal pronouns, and foreign language pronouns" |
| 14 | `get_upstream_features` | L2:F1337@37, k=5 → Emb:" haven"@35 (de=28.75) +4 more |

### Build

`build_circuit` → 19 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 66,983 | 5,828 | 289,125 | 0 | $0.0444 | — | — |
| **Total** | | **66,983** | **5,828** | **289,125** | **0** | **$0.0444** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 34s