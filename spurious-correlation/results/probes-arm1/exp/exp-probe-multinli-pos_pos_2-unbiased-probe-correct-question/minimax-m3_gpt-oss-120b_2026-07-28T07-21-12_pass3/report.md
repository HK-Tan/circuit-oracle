# Circuit Oracle Report
**Date:** 2026-07-28 07:21:12 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by low-layer (L0–L1) lexical features that fire on the **literal tokens** of the input — "haven't" (negation, via L0:F6236 with promoted tokens "not/Not/NOT"), "because" (L0:F16366), "well/yeah" discourse markers (L0:F8352, L4:F12126, L4:F4847), "tournament" (L0:F12862), and "double" / "A" / "now" / "year" — most of which are content-bearing sports-event and discourse words from the prompt. The strongest single direct effect on the probe is the **negation-token feature L0:F6236 at pos 20** (the apostrophe-t closing the word "haven't"), whose label and promoted tokens ("not/Not/NOT") confirm it is a dedicated detector of the English contraction negation construction. Supporting "because", "tournament", "well" and "year" features also fire at L0 and feed signal upward. The mid-layer cluster (L1:L3:L4) re-uses several of these same lexical detectors (L1:F177 "double", L3:F12849 "double/-hyphen", L3:F9770 science, L4:F5709 astronomy/'now', L4:F3730 batteries, L6:F11557 discourse markers, L0:F8659 "foundation"), and the late layer (L3:L4) consolidates them into a "conversational well/yeah agreement" detector (L4:F12126, L4:F4847, L3:F14620). The user's hypothesis is **partially correct but overstated**: the circuit IS heavy on the negation construction "haven't" (L0:F6236, the largest negative direct effect on the probe) — this is a *token-level spelling pattern* (apostrophe-t), not a semantic entity-recognizer, and it functions essentially as a heuristic "negation cue". However, the circuit is *not* purely a generic negation-detector: it also activates on the content nouns "tournament", "double", "A", "year", and the discourse markers "well" / "yeah" / "and", plus causal "because". So the mechanism is a mix of (a) a spurious surface-form "haven't" negation feature (which is exactly the "spurious feature" the user flagged) and (b) genuine lexical content tokens from the NCAA tournament sentence. The probe direction is therefore not driven by a clean semantic entity-recognizer (no "Louisville", "Sweet 16", or "NCAA" entity features appear) but by a bundle of low-level lexical detectors with a heavy weight on the negation construction — a classic spurious-correlation signature.

**Confidence:** 6

**Reasoning:** The circuit confirms the user's concern is well-founded on one specific feature: **L0:F6236** (the apostrophe-t of "haven't" at pos 20) is the single largest direct effect feeding the probe (-0.648) and is, by autointerp label and promoted tokens, a pure "isn't/doesn't contraction" detector that promotes "not/NOT/Not". This is precisely the kind of surface-form shortcut the user is worried about — a model classifying the sentence as "contradiction" partly because it sees the substring `n't`, not because it understands the meaning of "I haven't watched it this year because Louisville's out of it". The other large negative contributions come from lexical "well/yeah" discourse features (L4:F12126 -0.648, L1:F177 "double" -0.268, L0:F12862 "tournament" -0.236, L3:F9770 off-target "neuroscience" -0.315, L4:F5709 off-target "astronomy/now" -0.277, L4:F3730 off-target "batteries" -0.218) — and importantly several of these mid-layer features (9770 neuroscience, 5709 astronomy, 3730 batteries, 8659 "foundation") are **off-topic domain detectors** that happen to fire spuriously on these tokens. Embedding traces confirm the direct lineage: " well"→L4:F12126 (de=14.6), " yeah"→L4:F12126 (de=4.6), " haven'+'t"→L0:F6236 (de=17.9+16.6+12.1), " because"→L0:F16366 (de=40.8), " tournament"→L0:F12862 (de=20.6), " double"→L0:F8083 (de=19.6) and L1:F177 (de=24), " now"→L4:F5709 (de=40.8), " year"→L0:F5912 (de=18.6). Positively-pushing features (L3:F14620 "well/and" +0.231, L0:F3820 "the" +0.215, L0:F16366 "because" +0.293, L6:F11557 discourse markers +0.201, L0:F15682 "okay" +0.193) are generic function-word features, not entity features. The probe therefore relies on: (1) a real negation surface feature (L0:F6236 on "haven't" — this is the spurious cue the user identified), (2) a small set of sports-lexical features ("tournament", "double", "A", "year", "because"), and (3) several off-target domain features (neuroscience, astronomy, batteries, "foundation") that fired accidentally. There is no evidence of a "Louisville / Sweet 16 / NCAA" entity circuit — the model never recognizes the *entities* in the prompt. This is exactly the failure mode the user suspected: the probe uses a negation-construction cue (and a few other shallow lexical shortcuts) rather than the actual semantic content (sports-team identity, tournament identity, the claim "I haven't missed a single game" being contradicted by "I haven't watched it this year"). The user's intuition is correct: the contradiction classification is being driven by `haven't` (and to a lesser extent "tournament/double/well") rather than by understanding that the speaker contradicted themselves.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: ' haven ' (pos 18) + ' (pos 19) + t (pos 20) — NEGATION token 'haven't' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: ' because ' (pos 25) — causal connector | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: ' tournament ' (pos 8) — sports event noun | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' double ' (pos 6) + ' A ' (pos 7) — NCAA compound tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: ' now ' (pos 14) + ' right ' (pos 13) — temporal adverb | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 24 | Emb: ' year ' (pos 24) + ' this ' (pos 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' well ' (pos 2) + 'yeah' (pos 1) — discourse markers | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 20 | Negation token feature: apostrophe-t apostrophe (haven't spelling) (L0:F6236, pos 20) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Lexical 'because' feature (L0:F16366, pos 25) |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L0:F12862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) | 8 | Lexical 'tournament' feature (L0:F12862, pos 8) |  the word "tournament" and related words such as "winning", but not always | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) |
| [L0:F8083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) | 6 | Lexical 'double' feature (L0:F8083, pos 6) | the word "double" and surrounding words when numbers are also present | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| [L0:F5912](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) | 24 | Lexical 'year' feature (L0:F5912, pos 24) | "year" but also sometimes finds related words that include "day", "living", or "sold" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) |
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | Lexical 'well' + 'yeah' discourse markers (L0:F8352, pos 2) |  the word "well" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L1:F177](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) | 6 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') |  the word "double" and words that begin with "multi" or "doubly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| [L3:F12849](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) | 7 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') |  words or phrases that include the word "double", or contain a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) |
| [L3:F9770](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) | 7 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') |  technical and scientific writing about neuroscience and chemistry, possibly about calcium | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 14 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') | astronomy terms | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L4:F3730](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) | 7 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') |  text relating to lithium-ion batteries | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) |
| [L6:F11557](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) | 4 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') |  frequently used words such as conjunctions, pronouns, or discourse markers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) |
| [L0:F8659](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) | 8 | Mid-layer negation/contrast features (L1:F177 'double', L3:F12849 'double', L3:F9770 'science/neuro', L4:F5709 'now-astronomy', L4:F3730 'batteries', L4:F11557 'discourse markers', L0:F8659 'foundation') | the word "foundation" in different contexts, including religious, legal, and abstract senses. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) |
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Late-layer discourse / contrast features (L4:F12126 'well/yeah agreement', L4:F4847 'conversational Q/A', L3:F14620 'well/and') |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Late-layer discourse / contrast features (L4:F12126 'well/yeah agreement', L4:F4847 'conversational Q/A', L3:F14620 'well/and') |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L3:F14620](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) | 2 | Late-layer discourse / contrast features (L4:F12126 'well/yeah agreement', L4:F4847 'conversational Q/A', L3:F14620 'well/and') |  the word "well" and conjunctions like "and" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:12126 de=-0.648 |
| 3 | `inspect_feature` ×20 | L4:12126, L0:6236, L4:4847, L0:8083, L3:9770, L0:16366, L0:8659, L4:5709, L1:177, L0:12862, L3:12849, L3:14620, L4:3730, L0:3820, L1:5112, L6:11557, L0:8352, L1:4365, L0:5912, L0:15682 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F12126@2` | ❌ error | — | — | Trace this feature (L4:F12126, "well/yeah" agreement) upstream to identify which… |
| SA-2 | `L0:F6236@20` | ❌ error | — | — | Trace this L0:F6236 feature (the "isn't/doesn't" letter t detector, at pos 20 = … |
| SA-3 | `L0:F16366@25` | ❌ error | — | — | Trace this L0:F16366 feature (the word "because", at pos 25) upstream to identif… |
| SA-4 | `L0:F8659@8` | ❌ error | — | — | Trace L0:F8659 ("foundation" word, at pos 8) upstream. Pos 8 should be "foundati… |
| SA-5 | `L3:F9770@7` | ❌ error | — | — | Trace L3:F9770 (neuroscience/chemistry/science writing, at pos 7) upstream. Pos … |
| SA-6 | `L4:F5709@14` | ❌ error | — | — | Trace L4:F5709 (astronomy terms, at pos 14) upstream. Pos 14 likely is "Sweet" o… |
| SA-7 | `L0:F8083@6` | ❌ error | — | — | Trace L0:F8083 ("double" word, at pos 6) upstream. Pos 6 is "double" in "NC doub… |
| SA-8 | `L0:F12862@8` | ❌ error | — | — | Trace L0:F12862 ("tournament" word, at pos 8) upstream. Pos 8 is "tournament" in… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F12126@2, k=15 → Emb:" well"@2 (de=14.62) +14 more |
| 2 | `get_upstream_features` | L0:F6236@20, k=10 → Emb:"t"@20 (de=17.88) +9 more |
| 3 | `get_upstream_features` | L0:F16366@25, k=10 → Emb:" because"@25 (de=40.75) +9 more |
| 4 | `get_upstream_features` | L0:F12862@8, k=10 → Emb:" tournament"@8 (de=20.62) +9 more |
| 5 | `get_upstream_features` | L0:F8083@6, k=10 → Emb:" double"@6 (de=19.62) +9 more |
| 6 | `get_upstream_features` | L4:F4847@2, k=15 → Emb:" well"@2 (de=8.06) +14 more |
| 7 | `inspect_feature` ×2 | L2:1759, L3:4735 |
| 8 | `get_upstream_features` | L1:F177@6, k=10 → Emb:" double"@6 (de=24.00) +9 more |
| 9 | `get_upstream_features` | L3:F12849@7, k=10 → Emb:" double"@6 (de=25.75) +9 more |
| 10 | `get_upstream_features` | L3:F9770@7, k=10 → Emb:" double"@6 (de=18.00) +9 more |
| 11 | `get_upstream_features` | L4:F5709@14, k=10 → Emb:" now"@14 (de=40.75) +9 more |
| 12 | `get_upstream_features` | L0:F5912@24, k=10 → Emb:" year"@24 (de=18.62) +9 more |
| 13 | `get_upstream_features` | L4:F3730@7, k=10 → Emb:" A"@7 (de=13.19) +9 more |
| 14 | `get_upstream_features` | L0:F8352@2, k=10 → Emb:" well"@2 (de=30.88) +9 more |
| 15 | `get_upstream_features` | L0:F15682@1, k=10 → Emb:"yeah"@1 (de=15.56) +9 more |
| 16 | `get_upstream_features` | L1:F4365@1, k=10 → ❌ Feature (layer=1, pos=1, feature_idx=4365) not found in grap |
| 17 | `get_upstream_features` | L1:F5112@1, k=10 → ❌ Feature (layer=1, pos=1, feature_idx=5112) not found in grap |
| 18 | `get_upstream_features` | L3:F14620@2, k=10 → Emb:" well"@2 (de=9.75) +9 more |
| 19 | `get_upstream_features` | L6:F11557@4, k=10 → Emb:" uh"@4 (de=11.19) +9 more |
| 20 | `inspect_feature` ×8 | L4:10592, L4:3528, L1:2623, L3:3927, L2:15133, L4:279, L4:15162, L4:5458 |
| 21 | `get_upstream_features` | L3:F3927@7, k=5 → Emb:" double"@6 (de=16.00) +4 more |
| 22 | `inspect_feature` | L0, F1636 → " the letter A" |
| 23 | `get_upstream_features` | L0:F5232@14, k=5 → Emb:" now"@14 (de=35.25) +4 more |
| 24 | `inspect_feature` ×2 | L3:7449, L3:1438 |

### Build

`build_circuit` → 16 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 83,508 | 7,421 | 352,263 | 0 | $0.0551 | — | — |
| **Total** | | **83,508** | **7,421** | **352,263** | **0** | **$0.0551** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 2s