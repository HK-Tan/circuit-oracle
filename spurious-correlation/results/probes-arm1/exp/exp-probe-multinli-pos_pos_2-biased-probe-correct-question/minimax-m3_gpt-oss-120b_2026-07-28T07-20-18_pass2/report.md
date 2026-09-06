# Circuit Oracle Report
**Date:** 2026-07-28 07:20:19 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven by a bag of surface-level conversational/discourse cues (negation, fillers, hedging) rather than by entity-level or propositional content.

**Confidence:** 8

**Reasoning:** The circuit reveals a clear pipeline from raw input embeddings to the contradiction probe logit, organized into three supernodes.

**Token embedding inputs (layer 0):** The most upstream drivers are raw input tokens at positions 1 ("yeah"), 2 ("well"), 4 ("uh"), 6 ("double" — as in "NC double A"), 8 ("tournament"), the "haven't" triplet (pos 35-37, with direct effects 18.25/16.75/11.875 into the negation detector), and "because" (pos 25, direct_effect=40.75 into the "because" feature). The two highest-impact embedding drivers are the "haven't" token triplet (which feeds the negation pathway) and the single token "because" — both classic surface cues to negation/contrast rather than topic or entity.

**L0 lexical supernode:** Token embeddings feed word-identity features like L0:15972 "yeah" (activation 18.375, pos 1), L0:8352 "well" (pos 2), L0:6236 "n't" (pos 37, activation 35.5, direct_effect 0.535; promoted_tokens include "not", "Not", "nicht" — i.e., this is a pure syntactic negation marker), L0:16366 "because" (pos 25, activation 36.25, direct_effect 0.373), L0:3820 "the" (pos 3), L0:4541 "obviously" (pos 1, fires on "yeah"), and L0:7893/10780 firing on "double". These are all shallow, surface-form detectors — none encode Louisville, the tournament, or any event-specific entity.

**L1–L2 discourse supernode:** Aggregates L0 cues into higher-level discourse patterns: L1:177 (pos 6, "double"), L1:13255 (pos 8, "season"), L1:6846 (pos 8, "due"), L1:4373 (pos 37, "t after apostrophe"), L2:752 (pos 4, hedging/opinion phrases), L2:9629 (pos 4, "interjections and hesitation"), L2:1337 (pos 37 AND pos 20, "negated verbs with personal pronouns" — abstracting the lexical "n't" into a clause-level negation pattern), L2:5201 (pos 8, "sports awards/championships" — fires primarily on the bare "tournament" token embedding with direct_effect 16.375; it is content-lexical but still a generic sports-competition cue, not specific to Louisville or Sweet 16), and L2:1759 (pos 2, "know" with interjections). L2:1337 is the key content-abstraction step that moves from "isn't" to a higher-level "negated verb with pronoun" — but it remains a syntactic/syntactic-pattern feature, not a semantic one.

**L3–L4 interjection/hedging/negation aggregators:** L3:4735 (pos 2, scientific "well"), L3:2663 (pos 2, interjections), L3:7140/16039 (pos 4, "uh" associated tokens), L4:9602 (pos 4, "interjections and filler words" — direct_effect −0.629 to logit), L4:12126 (pos 2, "well/yeah" — direct_effect −0.488), L4:4492 (pos 37 AND pos 20, "negations in various languages" — direct_effect +0.310), L4:4847 (pos 2, "conversational Q&A words" — direct_effect +0.338), L4:1768 (pos 1, "affirmations/agreements"), L4:13748 (pos 2, "discourse markers/conjunctions" — promotes "because"), and L4:2740 (pos 2, "conversational language"). L4:4492 is a high-level multilingual negation detector whose top activating examples are all *just negation tokens* (tak, je, pas, n'a, n't, etc.) and whose upstream features are pure lexical "t after apostrophe" detectors (L0:6236, L1:4373, L2:1337) — i.e., the negation pathway is a pure surface-cue pipeline. The aggregator L2:1337 does add a *tiny* content-level abstraction (pronoun + negated verb), but its only inputs are the raw "haven" / "t" / "'" embeddings — it never sees what is being negated.

**Source-influence check:** `get_source_influence` on the negation/contrast token positions (20, 25, 33, 34, 37) returned S_pct_of_total=5.46% with S_over_R=1.26 — at the low end of "driven" but still comparable to the top non-source position. The top content-bearing positions (NC, tournament, A, Louisville at 5,7,8,26,27,28) returned S_pct_of_total=5.13% with S_over_R=1.19 — essentially the same as the negation/contrast positions. This means content words (NCAA, tournament, Louisville) and surface markers (haven't, because, uh, well) contribute roughly equally to the probe, but both are dominated by shallow lexical signals: the "haven't" negation pipeline is the cleanest sub-circuit, and it is purely surface-form.

**Mechanism:** The contradiction probe is a surface-cue detector. The two highest-magnitude upstream signals into the probe are (a) a dedicated negation pipeline (haven't → L0:6236 "n't" → L1:4373 apostrophe-t → L2:1337 negated-verb-with-pronoun → L4:4492 cross-lingual negations), which contributes +0.310 to the logit at pos 37 alone and another +0.310 at pos 20 ("haven't"); and (b) a hedging/filler pipeline (uh, well, yeah) feeding interjection and affirmation aggregators that contribute large negative direct_effects (L4:9602 −0.629, L4:12126 −0.488) but also positive contributions from the "because" pathway and the sports-tournament L2:5201. The "because" feature (L0:16366) alone promotes tokens ' " 2 u e T 1 i \n a — pure punctuation/connective tokens, again surface-level. Crucially, *no feature in the circuit encodes Louisville, the team being out, the Sweet 16, or any specific factual claim* — the only "content-adjacent" feature (L2:5201) is a generic "sports awards/championships" detector that fires on the bare word "tournament" with direct_effect 16.375 from its embedding and does not distinguish this Louisville-specific event from any other NCAA tournament mention.

**Conclusion:** The user is correct. The circuit heavily relies on spurious surface features — primarily the negation marker "haven't" (which the speaker uses twice, "haven't watched" and "I haven't missed"), the conjunction "because" (which introduces the contrast), and discourse fillers (yeah, well, uh) — rather than on entity-specific or propositional content. The negation sub-circuit is fully traceable to bare word-identity detectors (L0:6236 promoting "not/Not/nicht") and never reaches a semantic understanding of *what* is being negated. The "tournament/sports" content branch (L2:5201) is generic to NCAA-style sporting events and equally fires for any "tournament" mention. Together, the circuit is a classical bag-of-cues classifier: presence of negation + hedging + a sports context = contradiction prediction, independent of the specific entailment relationship between the claims.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F15972](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) | 1 | Lexical word-identity features (L0) | the word "yeah" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) |
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | Lexical word-identity features (L0) |  the word "well" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 37 | Lexical word-identity features (L0) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 20 | Lexical word-identity features (L0) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Lexical word-identity features (L0) |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Lexical word-identity features (L0) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F4541](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) | 1 | Lexical word-identity features (L0) |  adverbs of certainty such as "obviously" and related words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) |
| [L0:F7893](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) | 6 | Lexical word-identity features (L0) | the word "double" and words related to entrances and entering | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) |
| [L0:F10780](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) | 6 | Lexical word-identity features (L0) |  LaTeX commands for including packages and defining document class | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) |
| [L1:F177](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) | 6 | Discourse / hesitation / negation-pattern features (L1-L2) |  the word "double" and words that begin with "multi" or "doubly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| [L1:F13255](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13255) | 8 | Discourse / hesitation / negation-pattern features (L1-L2) |  the word "season" and words associated with it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13255) |
| [L1:F6846](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6846) | 8 | Discourse / hesitation / negation-pattern features (L1-L2) | the word "due" in a technical or scientific context | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6846) |
| [L1:F4373](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4373) | 37 | Discourse / hesitation / negation-pattern features (L1-L2) | the letter "t" when it is an apostrophe and attached to another word | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4373) |
| [L2:F752](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) | 4 | Discourse / hesitation / negation-pattern features (L1-L2) | phrases expressing personal opinions or viewpoints, often using words like "I," "think," "kind of," and related terms. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) |
| [L2:F9629](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) | 4 | Discourse / hesitation / negation-pattern features (L1-L2) |  interjections and sounds of hesitation or acknowledgment | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) |
| [L2:F1337](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) | 37 | Discourse / hesitation / negation-pattern features (L1-L2) | negated verbs with personal pronouns, and foreign language pronouns | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) |
| [L2:F1337](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) | 20 | Discourse / hesitation / negation-pattern features (L1-L2) | negated verbs with personal pronouns, and foreign language pronouns | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) |
| [L2:F5201](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) | 8 | Discourse / hesitation / negation-pattern features (L1-L2) | awards and accomplishments in the context of sports | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) |
| [L2:F1759](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) | 2 | Discourse / hesitation / negation-pattern features (L1-L2) | occurrences of the word "know" with emphasis words or interjections nearby | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) |
| [L3:F7140](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7140) | 4 | Interjection / hedging / negation aggregators (L3-L4) | words or parts of words containing "man", "ent", "per", or "mate" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7140) |
| [L3:F16039](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16039) | 4 | Interjection / hedging / negation aggregators (L3-L4) |  section delimiters and incomplete quotes | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16039) |
| [L3:F4735](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4735) | 2 | Interjection / hedging / negation aggregators (L3-L4) |  references to multi-well plates and software used in scientific experiments | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4735) |
| [L3:F2663](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2663) | 2 | Interjection / hedging / negation aggregators (L3-L4) | interjections and words expressing feeling or emotion, as well as the word "button" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2663) |
| [L4:F9602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) | 4 | Interjection / hedging / negation aggregators (L3-L4) |  interjections and filler words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) |
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Interjection / hedging / negation aggregators (L3-L4) |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 37 | Interjection / hedging / negation aggregators (L3-L4) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 20 | Interjection / hedging / negation aggregators (L3-L4) | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Interjection / hedging / negation aggregators (L3-L4) |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L4:F1768](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1768) | 1 | Interjection / hedging / negation aggregators (L3-L4) |  affirmations or agreements | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1768) |
| [L4:F13748](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13748) | 2 | Interjection / hedging / negation aggregators (L3-L4) |  discourse markers or conjunctions | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13748) |
| [L4:F2740](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2740) | 2 | Interjection / hedging / negation aggregators (L3-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2740) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:9602 de=-0.629 |
| 3 | `inspect_feature` ×19 | L4:9602, L0:8352, L0:6236, L4:12126, L0:3820, L1:177, L2:5201, L0:16366, L4:4847, L0:10780, L0:4541, L4:4492, L2:9629, L0:7893, L1:13255, L0:15972, L5:2740, L2:752, L1:6846 |
| 4 | `get_upstream_features` | Emb:"t"@37 (de=6.53) +7 more |
| 5 | `get_upstream_features` | Emb:"t"@37 (de=18.25) +7 more |
| 6 | `get_upstream_features` | Emb:" because"@25 (de=40.75) +7 more |
| 7 | `get_upstream_features` | Emb:" tournament"@8 (de=16.38) +7 more |
| 8 | `get_upstream_features` | Emb:" uh"@4 (de=11.44) +7 more |
| 9 | `get_upstream_features` | Emb:" well"@2 (de=30.88) +7 more |
| 10 | `get_upstream_features` | Emb:"t"@20 (de=6.38) +7 more |
| 11 | `get_upstream_features` | Emb:" tournament"@8 (de=18.50) +7 more |
| 12 | `get_upstream_features` | Emb:" double"@6 (de=15.62) +7 more |
| 13 | `get_upstream_features` | Emb:" well"@2 (de=14.62) +7 more |
| 14 | `get_upstream_features` | Emb:" double"@6 (de=24.00) +7 more |
| 15 | `get_upstream_features` | Emb:"yeah"@1 (de=26.62) +7 more |
| 16 | `get_upstream_features` | Emb:" well"@2 (de=8.06) +7 more |
| 17 | `get_upstream_features` | Emb:" double"@6 (de=18.62) +7 more |
| 18 | `get_upstream_features` | Emb:"yeah"@1 (de=6.66) +7 more |
| 19 | `get_upstream_features` | Emb:" uh"@4 (de=15.12) +7 more |
| 20 | `get_upstream_features` | Emb:" uh"@4 (de=10.38) +7 more |
| 21 | `get_upstream_features` | Emb:" the"@3 (de=32.75) +7 more |
| 22 | `get_upstream_features` | Emb:"yeah"@1 (de=12.38) +7 more |
| 23 | `get_upstream_features` | Emb:" tournament"@8 (de=15.00) +7 more |
| 24 | `get_source_influence` | {'depth': 2, 'source_positions': [20, 25, 33, 34, 37], 'S_pct_of_total': 5.457,  |
| 25 | `get_source_influence` | {'depth': 2, 'source_positions': [5, 7, 8, 9, 10, 11, 26, 27, 28], 'S_pct_of_tot |
| 26 | `get_upstream_features` | Emb:" haven"@35 (de=28.75) +7 more |
| 27 | `get_upstream_features` | Emb:"t"@37 (de=19.00) +7 more |
| 28 | `get_upstream_features` | Emb:" well"@2 (de=12.56) +7 more |
| 29 | `inspect_feature` ×5 | L2:1337, L1:4373, L2:1759, L1:2623, L4:1768 |
| 30 | `get_upstream_features` | Emb:"yeah"@1 (de=24.38) +7 more |
| 31 | `inspect_feature` ×3 | L0:15183, L0:12164, L1:11938 |
| 32 | `get_upstream_features` | Emb:" tournament"@8 (de=13.00) +7 more |
| 33 | `inspect_feature` | "the word "foundation" in different contexts, including religious, lega" |
| 34 | `get_upstream_features` | Emb:" tournament"@8 (de=20.88) +7 more |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F4492@37` | ✅ reported | 3 | 7 | Trace this "negations" feature fully to its origins. Identify what tokens drive … |
| SA-2 | `L2:F5201@8` | ✅ reported | 5 | 6 | Trace the "awards and accomplishments in sports" feature. Find what drives it - … |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4492 | "negations in various languages" |
| 2 | `get_upstream_features` | L4:F4492@37, k=10 | Emb:"t"@37 (de=6.53) +9 more |
| 3 | `inspect_feature` | L0, F6236 | "the letter "t" when it follows the word "isn'" or "doesn'"" |
| 4 | `inspect_feature` | L2, F1337 | "negated verbs with personal pronouns, and foreign language pronouns" |
| 5 | `get_upstream_features` | L0:F6236@37, k=10 | Emb:"t"@37 (de=18.25) +9 more |
| 6 | `get_upstream_features` | L2:F1337@37, k=10 | Emb:" haven"@35 (de=28.75) +9 more |
| 7 | `get_upstream_features` | L0:F6236@37, k=10 | Emb:"t"@37 (de=18.25) +9 more |

**Findings:** The negations feature (L4:F4492) is driven primarily by a low‑layer lexical cue: the token "t" that follows an apostrophe after words like "isn'", "doesn'", "haven'". This is captured by L0:6236, which directly promotes the token "not" and other language‑specific negation words, indicating a syntactic negation detector. A second upstream signal comes from L2:1337, which abstracts the lexical cue i…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F5201 | "awards and accomplishments in the context of sports" |
| 2 | `get_upstream_features` | L2:F5201@8, k=10 | Emb:" tournament"@8 (de=16.38) +9 more |
| 3 | `inspect_feature` | L1, F11938 | "mentions of meals, restaurants, and food" |
| 4 | `inspect_feature` | L0, F15183 | " the word "fighting"" |
| 5 | `get_upstream_features` | L1:F11938@8, k=10 | Emb:" tournament"@8 (de=13.00) +9 more |
| 6 | `get_upstream_features` | L0:F15183@8, k=10 | Emb:" tournament"@8 (de=19.38) +9 more |
| 7 | `inspect_feature` | L0, F12164 | " words related to the legal system" |
| 8 | `inspect_feature` | L0, F8659 | "the word "foundation" in different contexts, including religious, lega" |

**Findings:** The "awards and accomplishments in sports" feature (L2:F5201) is primarily driven by the raw input token embedding for "tournament" at position 8, which supplies a large positive direct effect (16.375). This indicates the feature activates when the prompt mentions a tournament, especially NCAA tournament contexts seen in its top activating examples. Secondary contributions come from lower-layer fe…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F1768@2, k=8 → ❌ Feature (layer=4, feature_idx=1768) not found at pos=2. This |
| 2 | `get_upstream_features` | L3:F7140@4, k=5 → Emb:" uh"@4 (de=10.69) +4 more |
| 3 | `get_upstream_features` | L3:F16039@4, k=5 → L2:F752 (de=9.69) +4 more |
| 4 | `inspect_feature` ×2 | L3:7140, L3:16039 |
| 5 | `get_upstream_features` | L4:F1768@1, k=8 → Emb:"yeah"@1 (de=24.38) +7 more |
| 6 | `get_upstream_features` | L4:F4847@1, k=8 → ❌ Feature (layer=4, feature_idx=4847) not found at pos=1. This |
| 7 | `get_upstream_features` | L3:F4735@2, k=5 → Emb:" well"@2 (de=25.75) +4 more |
| 8 | `inspect_feature` | L3, F4735 → " references to multi-well plates and software used in scientific exper" |
| 9 | `get_upstream_features` | L3:F5329@1, k=5 → Emb:"yeah"@1 (de=12.06) +4 more |
| 10 | `get_upstream_features` | L2:F9327@1, k=5 → Emb:"yeah"@1 (de=11.19) +4 more |
| 11 | `get_upstream_features` | L0:F10317@1, k=5 → Emb:"<bos>"@0 (de=19.88) +4 more |
| 12 | `get_upstream_features` | L3:F4720@1, k=5 → ❌ Feature (layer=3, pos=1, feature_idx=4720) not found in grap |
| 13 | `inspect_feature` ×3 | L1:14137, L2:11077, L0:10317 |
| 14 | `get_upstream_features` | L1:F14137@1, k=5 → Emb:"<bos>"@0 (de=26.62) +4 more |
| 15 | `get_upstream_features` | L4:F13748@2, k=5 → Emb:" well"@2 (de=6.09) +4 more |
| 16 | `get_upstream_features` | L3:F2663@2, k=5 → Emb:"yeah"@1 (de=10.06) +4 more |
| 17 | `inspect_feature` ×2 | L3:2663, L4:13748 |
| 18 | `get_upstream_features` | L0:F6236@20, k=8 → Emb:"t"@20 (de=17.88) +7 more |
| 19 | `get_upstream_features` | L2:F1337@20, k=8 → Emb:" haven"@18 (de=28.38) +7 more |
| 20 | `get_upstream_features` | L4:F4847@2, k=8 → Emb:" well"@2 (de=8.06) +7 more |
| 21 | `get_upstream_features` | L0:F15183@8, k=5 → Emb:" tournament"@8 (de=19.38) +4 more |
| 22 | `inspect_feature` | L0, F5748 → "the word "appreciated" and words with negative connotations" |
| 23 | `get_upstream_features` | L0:F15972@1, k=5 → Emb:"yeah"@1 (de=26.62) +4 more |
| 24 | `get_upstream_features` | L0:F8352@2, k=5 → Emb:" well"@2 (de=30.88) +4 more |
| 25 | `get_upstream_features` | L0:F16366@25, k=5 → Emb:" because"@25 (de=40.75) +4 more |
| 26 | `get_upstream_features` | L0:F3820@3, k=5 → Emb:" the"@3 (de=32.75) +4 more |
| 27 | `get_upstream_features` | L0:F4541@1, k=5 → Emb:"yeah"@1 (de=12.38) +4 more |
| 28 | `get_upstream_features` | L0:F7893@6, k=5 → Emb:" double"@6 (de=18.62) +4 more |
| 29 | `get_upstream_features` | L0:F10780@6, k=5 → Emb:" double"@6 (de=15.62) +4 more |
| 30 | `get_upstream_features` | L1:F177@6, k=5 → Emb:" double"@6 (de=24.00) +4 more |
| 31 | `get_upstream_features` | L5:F2740@2, k=5 → Emb:"yeah"@1 (de=6.66) +4 more |
| 32 | `get_upstream_features` | L0:F10780@6, k=5 → Emb:" double"@6 (de=15.62) +4 more |
| 33 | `get_upstream_features` | L0:F15972@1, k=5 → Emb:"yeah"@1 (de=26.62) +4 more |
| 34 | `inspect_feature` ×2 | L0:16080, L0:4823 |

### Build

`build_circuit` → 11 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 93,274 | 15,675 | 1,399,264 | 0 | $0.1307 | — | — |
| SA-2 | openai/gpt-oss-120b | 83,795 | 4,881 | 2,528 | 0 | $0.0155 | ✅ 5F/6E | Trace the "awards and accomplishments in sports" feature. Fi… |
| SA-1 | openai/gpt-oss-120b | 62,159 | 3,838 | 5,056 | 0 | $0.0117 | ✅ 3F/7E | Trace this "negations" feature fully to its origins. Identif… |
| **Total** | | **239,228** | **24,394** | **1,406,848** | **0** | **$0.1580** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 10s