# Circuit Oracle Report
**Date:** 2026-07-28 07:20:53 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction classification is driven almost entirely by surface-level lexical/orthographic features (discourse fillers, single-letter negation tokens, the word "because," the token "double," the noun "tournament") rather than by any deep semantic understanding of the claim being contradicted.

**Confidence:** 8

**Reasoning:**

The top-feature call returned a set of transcoder features whose direct effects on the probe are dominated by **shallow lexical detectors** that fire on individual tokens or subword fragments, not on meaning:

- **Negation-by-orthography (the user's main concern, confirmed):** L0:F6236 (frac_nonzero 0.0026, *very* specific) detects the letter "t" when it follows "isn'" or "doesn'". Its upstream driver is literally the **token embedding of "t" at pos 20 (direct_effect 17.9)** plus the embedding of " haven" at pos 18 (16.6) and the apostrophe "'" at pos 19 (12.1). This is a *purely orthographic* detector for the apostrophe-t contraction ending — the model is treating the surface form "haven't" as a contradiction cue, not interpreting what the speaker is actually negating. The "neither" feature L0:F4365 (pos 1, activation 11.9) and the "okay" feature L0:F15682 (pos 1) similarly add light contribution. This directly validates the user's concern: the probe treats *negation words* themselves as evidence of contradiction, irrespective of whether the content is semantically contradicting anything.

- **Discourse-marker / filler words being read as a contradiction signature:** The biggest single driver is L4:F12126 (direct_effect −0.65), labeled "expressions of agreement or acknowledgement, particularly 'well' and 'yeah'", traced back through the subagent to the embeddings of " well" (pos 2, direct_effect 14.6) and "yeah" (pos 1, direct_effect 4.6). Its partner L4:F4847 (+0.39, "words or short phrases often used in conversation, especially questions and answers") and L3:F14620 ("the word 'well' and conjunctions like 'and'") are also pure filler/conversation detectors. So conversational openers — "yeah well the uh" — are themselves being weighted as evidence of contradiction. The "uh" at pos 4 feeds L6:F11557 (conjunctions / discourse markers), again a generic surface pattern.

- **Topic-name lexical hits, not semantic content:** L0:F12862 ("the word 'tournament' and related words such as 'winning'", pos 8, +0.29), L0:F8659 ("the word 'foundation'", pos 8, +0.29), L0:F16366 ("the word 'because'", pos 25, +0.29), and L0:F8083 / L1:F177 ("the word 'double'", pos 6, −0.33) are all single-word lexical detectors. The "double" branch is particularly notable — it actually pushes *against* the contradiction direction (negative direct effects at L0:8083, L1:177, L3:12849), which is consistent with "NC double A tournament" being a benign proper-noun phrase that the model has no contradiction handle for.

- **Causal connector as contradiction signal:** L0:F16366 fires on the literal token "because" (embedding direct_effect 40.75 to the feature). The model is reading the *presence of a causal connective* in the second sentence ("because Louisville's out of it this year") as another contradiction cue, rather than the actual content of the cause.

In short, every late-layer feature driving the contradiction score decomposes into either (a) single-token lexical detectors (tournament, because, double, year, the, okay, neither) or (b) discourse/filler detectors (yeah, well, uh) or (c) an orthographic contraction-ending detector (apostrophe-t). The only feature that could plausibly encode *meaning* of the contradiction itself — the idea that "I haven't watched it because Louisville's out of it" negates the prior "I haven't missed a single game" — would need to integrate the semantic relation between clauses, but no such feature is in the top-20. The circuit is dominated by surface-form artifacts (negation orthography + filler words + topic nouns), which is exactly the spurious-feature failure mode the user flagged.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Mid-layer discourse/conversation detectors (pos 2) |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Mid-layer discourse/conversation detectors (pos 2) |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L3:F14620](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) | 2 | Mid-layer discourse/conversation detectors (pos 2) |  the word "well" and conjunctions like "and" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) |
| [L2:F1759](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) | 2 | Mid-layer discourse/conversation detectors (pos 2) | occurrences of the word "know" with emphasis words or interjections nearby | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) |
| [L2:F7222](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7222) | 2 | Mid-layer discourse/conversation detectors (pos 2) | the word "well" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7222) |
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | Mid-layer discourse/conversation detectors (pos 2) |  the word "well" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L0:F15972](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) | 1 | Mid-layer discourse/conversation detectors (pos 2) | the word "yeah" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 20 | Negation 't' detector (isn't/haven't) at pos 20 | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Causal connector 'because' (pos 25) |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L0:F8083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) | 6 | 'double' / number token detectors (pos 6) | the word "double" and surrounding words when numbers are also present | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| [L1:F177](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) | 6 | 'double' / number token detectors (pos 6) |  the word "double" and words that begin with "multi" or "doubly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| [L3:F12849](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) | 7 | 'double' / number token detectors (pos 6) |  words or phrases that include the word "double", or contain a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) |
| [L3:F9770](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) | 7 | 'double' / number token detectors (pos 6) |  technical and scientific writing about neuroscience and chemistry, possibly about calcium | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| [L2:F15133](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15133) | 7 | 'double' / number token detectors (pos 6) |  capital letters, especially those that are used as labels on figures, tables, experimental conditions, or chemical compounds | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15133) |
| [L0:F12862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) | 8 | 'tournament' / 'foundation' / 'resolution' lexical detectors (pos 8) |  the word "tournament" and related words such as "winning", but not always | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) |
| [L0:F8659](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) | 8 | 'tournament' / 'foundation' / 'resolution' lexical detectors (pos 8) | the word "foundation" in different contexts, including religious, legal, and abstract senses. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) |
| [L0:F5112](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) | 1 | 'tournament' / 'foundation' / 'resolution' lexical detectors (pos 8) |  the word "resolution", sometimes in the context of displaying images or patterns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) |
| [L6:F11557](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) | 4 | Filler 'uh' / discourse-marker at pos 4 |  frequently used words such as conjunctions, pronouns, or discourse markers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) |
| [L0:F15682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15682) | 1 | Filler 'uh' / discourse-marker at pos 4 |  the word "okay" plus a few related expressions. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15682) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Filler 'uh' / discourse-marker at pos 4 | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F4365](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4365) | 1 | Filler 'uh' / discourse-marker at pos 4 | the word "neither" and related negative terms. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4365) |
| [L0:F5912](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) | 24 | Filler 'uh' / discourse-marker at pos 4 | "year" but also sometimes finds related words that include "day", "living", or "sold" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:12126 de=-0.648 |
| 3 | `inspect_feature` ×20 | L4:12126, L0:6236, L4:4847, L0:8083, L3:9770, L0:16366, L0:8659, L4:5709, L1:177, L0:12862, L3:12849, L3:14620, L4:3730, L0:3820, L0:5112, L6:11557, L0:8352, L0:4365, L0:5912, L0:15682 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F12126@2` | ✅ reported | 4 | 8 | Trace upstream from L4:F12126 (the "yeah/well" acknowledgement feature at positi… |
| SA-2 | `L0:F6236@20` | ❌ error | — | — | Trace upstream from L0:F6236 (the "isn't/doesn't" negation-t feature at pos 20, … |
| SA-3 | `L4:F4847@2` | ✅ reported | 6 | 9 | Trace upstream from L4:F4847 (the conversation/Well feature at pos 2, direct_eff… |
| SA-4 | `L0:F16366@25` | ❌ error | — | — | Trace upstream from L0:F16366 (the "because" feature at pos 25, direct_effect +0… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F12126 | " expressions of agreement or acknowledgement, particularly "well" and " |
| 2 | `get_upstream_features` | L4:F12126@2, k=10 | Emb:" well"@2 (de=14.62) +9 more |
| 3 | `inspect_feature` | L2, F1759 | "occurrences of the word "know" with emphasis words or interjections ne" |
| 4 | `inspect_feature` | L3, F13677 | " text from law transcripts (with "sir", "ubuntu" with version numbers," |
| 5 | `inspect_feature` | L3, F15027 | " snippets of code or time-stamps within text" |
| 6 | `get_upstream_features` | L2:F1759@2, k=10 | Emb:" well"@2 (de=12.56) +9 more |
| 7 | `get_upstream_features` | L3:F13677@2, k=10 | Emb:"yeah"@1 (de=6.88) +9 more |
| 8 | `inspect_feature` | L0, F15972 | "the word "yeah"" |

**Findings:** Tracing upstream from the acknowledgement feature L4:F12126 (position 2) quickly reaches the raw token embeddings for "well" (pos 2) and "yeah" (pos 1), which provide the strongest positive drive (direct effects 14.6 and 4.6). The next strongest non‑embedding driver is L2:F1759, a modest emphasis‑around‑"know" detector, which itself is promoted by the same embeddings and a low‑level "yeah" feature…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4847 | " words or short phrases often used in conversation, and especially que" |
| 2 | `get_upstream_features` | L4:F4847@2, k=10 | Emb:" well"@2 (de=8.06) +9 more |
| 3 | `inspect_feature` | L2, F7222 | "the word "well"" |
| 4 | `inspect_feature` | L2, F1759 | "occurrences of the word "know" with emphasis words or interjections ne" |
| 5 | `inspect_feature` | L2, F1759 | "occurrences of the word "know" with emphasis words or interjections ne" |
| 6 | `inspect_feature` | L3, F9271 | " a varied set of conversational interjections and questions." |
| 7 | `get_upstream_features` | L2:F7222@2, k=10 | Emb:" well"@2 (de=20.25) +9 more |
| 8 | `inspect_feature` | L0, F15972 | "the word "yeah"" |
| 9 | `get_upstream_features` | L2:F7222@2, k=10 | Emb:" well"@2 (de=20.25) +9 more |
| 10 | `inspect_feature` | L3, F8423 | " words within messages in a chat or messaging system" |

**Findings:** Tracing from L4:F4847 (conversation‑filler detector) shows its strongest upstream driver is the raw embedding of the input token " well" (positive direct_effect ~20). The next most influential upstream features are L2:F7222 (the word "well" detector), L2:F1759 (emphatic "know" detector), and L3 features capturing interjections. All paths reach a lower‑layer (≤8) feature and include a direct embedd…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F6236@20, k=8 → Emb:"t"@20 (de=17.88) +7 more |
| 2 | `get_upstream_features` | L0:F16366@25, k=8 → Emb:" because"@25 (de=40.75) +7 more |
| 3 | `get_upstream_features` | L0:F8083@6, k=8 → Emb:" double"@6 (de=19.62) +7 more |
| 4 | `get_upstream_features` | L0:F12862@8, k=8 → Emb:" tournament"@8 (de=20.62) +7 more |
| 5 | `get_upstream_features` | L3:F9770@7, k=8 → Emb:" double"@6 (de=18.00) +7 more |
| 6 | `get_upstream_features` | L0:F8659@8, k=8 → Emb:" tournament"@8 (de=15.25) +7 more |
| 7 | `get_upstream_features` | L3:F14620@2, k=8 → Emb:" well"@2 (de=9.75) +7 more |
| 8 | `get_upstream_features` | L0:F4365@1, k=8 → Emb:"yeah"@1 (de=14.81) +7 more |
| 9 | `get_upstream_features` | L0:F5912@24, k=8 → Emb:" year"@24 (de=18.62) +7 more |
| 10 | `get_upstream_features` | L0:F3820@3, k=8 → Emb:" the"@3 (de=32.75) +7 more |
| 11 | `get_upstream_features` | L0:F15682@1, k=8 → Emb:"yeah"@1 (de=15.56) +7 more |
| 12 | `get_upstream_features` | L6:F11557@4, k=5 → Emb:" uh"@4 (de=11.19) +4 more |
| 13 | `get_upstream_features` | L4:F5709@14, k=5 → Emb:" now"@14 (de=40.75) +4 more |
| 14 | `get_upstream_features` | L3:F12849@7, k=5 → Emb:" double"@6 (de=25.75) +4 more |
| 15 | `get_upstream_features` | L4:F3730@7, k=5 → Emb:" A"@7 (de=13.19) +4 more |
| 16 | `get_upstream_features` | L0:F5112@1, k=5 → Emb:"yeah"@1 (de=11.50) +4 more |
| 17 | `get_upstream_features` | L0:F8352@2, k=5 → Emb:" well"@2 (de=30.88) +4 more |
| 18 | `get_upstream_features` | L1:F177@6, k=5 → Emb:" double"@6 (de=24.00) +4 more |
| 19 | `get_upstream_features` | L2:F2039@2, k=5 → Emb:" well"@2 (de=27.12) +4 more |
| 20 | `inspect_feature` ×6 | L4:10592, L4:3528, L2:7222, L2:15133, L2:1766, L1:2623 |

### Build

`build_circuit` → 17 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 70,096 | 8,119 | 334,735 | 0 | $0.0509 | — | — |
| SA-3 | openai/gpt-oss-120b | 158,678 | 8,796 | 2,528 | 0 | $0.0291 | ✅ 6F/9E | Trace upstream from L4:F4847 (the conversation/Well feature … |
| SA-1 | openai/gpt-oss-120b | 82,673 | 6,143 | 7,648 | 0 | $0.0162 | ✅ 4F/8E | Trace upstream from L4:F12126 (the "yeah/well" acknowledgeme… |
| **Total** | | **311,447** | **23,058** | **344,911** | **0** | **$0.0962** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 33s