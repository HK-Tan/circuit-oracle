# Circuit Oracle Report
**Date:** 2026-07-28 07:21:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven almost entirely by surface-form and generic function-word features (single-word detectors for "land", "fire", "about", "set", "they", "so", "for", "to", ".", "not allowed", sentence-initial capital-letter detectors at L8 and L17, and a "not"/"allowed"/sentence-end broad-topic feature at L12) — none of the top direct-effect features encode the actual contradiction semantics (e.g., the incompatibility between "clearing land for agriculture" and "not allowed to deforest for agricultural purposes"); the "not … allowed" tokens do feed L12, but via features that simply fire on "not" or "allowed" individually, not on the negation construction.

**Confidence:** 8/10

**Reasoning:** Inspecting each of the top direct-effect features driving the probe reveals a strikingly surface-level picture:

1. **Layer 0 lexical "they" / "about" / "to" / "for" / "." detectors** (L0:F3498, F2238, F8444, F15492, F6051; activations 32–39, frac_nonzero 0.017–0.057). These are very generic single-word detectors with the broadest possible context windows — they fire on "they", "about" (often followed by a number, but here just preceding "clearing"), "to", "for", and periods. Their embeddings are dominated by Emb "they" (42.75), Emb "about" (35), Emb "to" (41), Emb "for" (39), Emb "." (47). None of these features are contradiction-specific.

2. **Layer 1–2 single-word detectors for content nouns** (L1:F461 "land", L1:F361 "agriculture", L1:F5978 "fire/boilers", L2:F11518 "land in scientific/agricultural contexts", L2:F15312 "about", L2:F10849 "set", L2:F4819 "fire", L2:F14822 "So" abbreviation). The label "land in scientific/agricultural contexts" looks topical, but in this prompt the only inputs to L2:F11518 are the bare Emb " land" token (direct_effect 28.375) and minor context — i.e., it functions as a "land" word detector, not as an agriculture/world-knowledge feature. The "fire" feature (L2:F4819, L1:F5978) is fed by Emb "fire" (direct_effect 32 / 27) without any semantic integration.

3. **Layer 3 "not / sentence fragments" feature** (L3:F6227, frac_nonzero 0.0167, "sentence fragments and informal or ungrammatical language"). Its top-activating examples and promoted tokens ("▁not", "▁NOT", "Not", "not", "▁nicht", "▁não", "▁ikkje") reveal it is essentially a multi-lingual **negation-word detector**. In this prompt its inputs are Emb "to" (pos 23, +6.75), Emb "not" (pos 21, +5.16), Emb "allowed" (pos 22, +3.45), and Emb "They" (−1.23), so it fires on the "not allowed" sub-string, not on the propositional contradiction. It contributes +0.1504 (via the L1 "land" path it adds +0.165 through L3:F15978; L3:F6227 itself contributes +0.165 in the get_top_features ranking).

4. **Layer 4 transition-word features** (L4:F12225 "transitional conclusion words, often used in legal or academic writing" with promoted "so/therefore/hence"; L4:F5450 "code snippets … words related to starting or beginning" with promoted "▁begin/▁begin/▁began/▁begin/▁beginning/▁begun"). Despite topical-sounding labels, both reduce to single-word detectors whose only meaningful inputs in this prompt are Emb "they" (pos 2, +12.75) and Emb "So" (pos 1, +12.375) for F12225 (i.e. "So"/"they" pronouns), and Emb "set"/"about" for F5450.

5. **Layer 6 generic function-word & surface-form features** (L6:F14744 "about, to, work"; L6:F4516 "the letter i" but here at pos 1 firing on capital-letter surface form, fed by L5:F3992 "start of documentation blocks in code" and Emb "So" +3.72; L6:F14585 "the words 'the' and 'it' at the beginning of sentences", fed by Emb "So" +9.25). All three are surface-form detectors that fire on the capital-letter "So" and function words.

6. **Layer 8 sentence-initial capital-letter feature** (L8:F8406 "first-person 'I' and the word 'Exactly'", but in this prompt it is fed by Emb "<bos>" (10.25) and L7:F462/L7:F5741, both of which are "code documentation and import statements" features, indicating this circuit path is essentially tracking the start-of-text token, not a content signal. Direct effect to probe is **−0.243** (suppresses contradiction score).

7. **Layer 12 broad-topic feature** (L12:F12606, label "political conspiracy/organizations, mental conditions and storytelling terms"). Despite the topical label, the only large upstream contributions in this graph are Emb "not" (3.59), Emb "<bos>" (3.38), Emb "allowed" (1.67), Emb "land" (1.54), Emb "forest" (1.5), Emb "were" (1.16), Emb "fire" (0.75) — i.e., it acts as a generic "negation + sentence-final / sentence-2" aggregator rather than anything contradiction-specific. Direct effect +0.154 to the probe.

8. **Layer 17 sentence-initial detector** (L17:F451 "start of sentences", activation 62, frac_nonzero 0.0067, top tokens all capital-word sentence-initial). Fed by Emb "So" (+3.77), L7:F462 (+3.66), and a L16:L10989 feature (−11.88, inhibitory). Direct effect +0.154. The headline label says "start of sentences" — this is a capital-letter / sentence-initial feature, not a content feature.

The user's concern is **largely validated**: the top features are overwhelmingly single-word and surface-form detectors — "land", "fire", "about", "set", "to", "for", "not", period, sentence-initial capital-letter "So" — rather than features that compose the actual contradictory content (e.g., "clearing land for agriculture" vs. "not allowed to deforest for agricultural purposes"). The strongest contribution from the negation sub-string ("not … allowed") flows through L3:F6227 ("sentence fragments … multi-lingual negation word detector") and L1:F2493 / L0:F7820 — features that detect the word "not" or "pas/nicht" in isolation, not the propositional "not allowed" construction. The only late-layer features with topical-sounding labels (L8:F8406, L12:F12606, L17:F451) all reduce to capital-letter / sentence-initial / broad-bag-of-keyword detectors whose activation in this context is driven by the same generic surface signals. There is no circuit path that integrates "clearing land for agriculture" semantically and contrasts it with the negation — the probe is largely reading generic function-word and negation-word cues as a shortcut for "contradiction".

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: So (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: they (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: set (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: about (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: clearing (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: land (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: for (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: agriculture (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: fire (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: to (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: to (pos 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: . (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: not (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: allowed (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | Layer-0 lexical word features |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | Layer-0 lexical word features |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 13 | Layer-0 lexical word features | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F15492](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) | 8 | Layer-0 lexical word features |  the word "for" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 18 | Layer-0 lexical word features | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L1:F461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) | 7 | Layer-1 single-word detectors (land, agriculture, fire+boilers) |  the word "land" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) |
| [L1:F361](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) | 9 | Layer-1 single-word detectors (land, agriculture, fire+boilers) |  words related to agriculture and ecology | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) |
| [L1:F5978](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5978) | 12 | Layer-1 single-word detectors (land, agriculture, fire+boilers) |  words related to fire and boilers | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5978) |
| [L2:F11518](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) | 7 | Layer-2 single-word detectors (land/agri, about, set, fire) |  the word "land" in scientific/agricultural contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) |
| [L2:F15312](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) | 4 | Layer-2 single-word detectors (land/agri, about, set, fire) |  the word "about." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) |
| [L2:F10849](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) | 3 | Layer-2 single-word detectors (land/agri, about, set, fire) | the word "set" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) |
| [L2:F14822](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14822) | 1 | Layer-2 single-word detectors (land/agri, about, set, fire) |  the abbreviation "SO" followed by other characters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14822) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | Layer-2 single-word detectors (land/agri, about, set, fire) | sentences containing the word "fire" or similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L3:F4464](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) | 4 | Layer-3 lexical & negation feature (about, sentence-fragments/negation) |  the word "about" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) |
| [L3:F15978](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15978) | 7 | Layer-3 lexical & negation feature (about, sentence-fragments/negation) |  mentions of land, property, and acreage. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15978) |
| [L3:F6227](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) | 23 | Layer-3 lexical & negation feature (about, sentence-fragments/negation) |  sentence fragments and informal or ungrammatical language, often including abbreviations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6227) |
| [L4:F12225](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) | 2 | Layer-4 transition/beginning-word features (so/therefore; begin/start) |  transitional conclusion words, often used in legal or academic writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) |
| [L4:F5450](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) | 4 | Layer-4 transition/beginning-word features (so/therefore; begin/start) |  code snippets from different languages and words related to starting or beginning something | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) |
| [L6:F14744](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) | 4 | Layer-6 generic function-word & surface form features |  the words "about," "to," and "work." | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) |
| [L6:F4516](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4516) | 1 | Layer-6 generic function-word & surface form features |  the letter "i." | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4516) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | Layer-6 generic function-word & surface form features |  the words "the" and "it" at the beginning of sentences | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Layer-8 sentence-initial / capital-letter "So"/"They" detector | the first-person pronoun "I" and the word "Exactly" | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 25 | Layer-12 broad-topic feature (activated by 'not', 'allowed', sentence-end tokens) |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Layer-17 sentence-initial capital-word detector | start of sentences | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3498 de=-0.621 |
| 3 | `inspect_feature` ×20 | L2:11518, L4:5450, L2:15312, L3:4464, L0:3498, L0:2238, L4:12225, L8:8406, L2:4819, L0:8444, L2:10849, L0:15492, L3:15978, L6:14744, L17:451, L12:12606, L0:6051, L2:14822, L1:461, L1:361 |
| 4 | `get_upstream_features` | Emb:"<bos>"@0 (de=10.25) +9 more |
| 5 | `get_upstream_features` | L16:F10989 (de=-11.88) +9 more |
| 6 | `get_upstream_features` | Emb:" land"@7 (de=28.38) +9 more |
| 7 | `inspect_feature` ×8 | L7:462, L7:5741, L5:3992, L6:14585, L7:3099, L6:4516, L7:1673, L5:7489 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L17:F451@1` | ❌ error | — | — | Trace the path from L17:F451 (pos 1, "start of sentences" / sentence-initial fea… |
| SA-2 | `L8:F8406@1` | ❌ error | — | — | Trace L8:F8406 (pos 1, "the first-person pronoun 'I' and the word 'Exactly'" - b… |
| SA-3 | `L12:F12606@25` | ❌ error | — | — | Trace L12:F12606 (pos 25, "phrases related to political conspiracy/organizations… |
| SA-4 | `L4:F12225@2` | ❌ error | — | — | Trace L4:F12225 (pos 2, "transitional conclusion words, often used in legal or a… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L12:F12606@25, k=10 → Emb:" not"@21 (de=3.59) +9 more |
| 2 | `get_upstream_features` | L4:F12225@2, k=10 → Emb:" they"@2 (de=12.75) +9 more |
| 3 | `get_upstream_features` | L1:F361@9, k=10 → Emb:" agriculture"@9 (de=14.31) +9 more |
| 4 | `get_upstream_features` | L1:F461@7, k=10 → Emb:" land"@7 (de=24.88) +9 more |
| 5 | `get_upstream_features` | L2:F4819@12, k=10 → Emb:" fire"@12 (de=32.00) +9 more |
| 6 | `get_upstream_features` | L3:F15978@7, k=10 → Emb:" land"@7 (de=16.12) +9 more |
| 7 | `get_upstream_features` | L6:F14744@4, k=10 → Emb:" about"@4 (de=5.81) +9 more |
| 8 | `get_upstream_features` | L2:F10849@3, k=10 → Emb:" set"@3 (de=17.12) +9 more |
| 9 | `get_upstream_features` | L2:F11518@7, k=10 → Emb:" land"@7 (de=28.38) +9 more |
| 10 | `get_upstream_features` | L4:F5450@4, k=10 → Emb:" set"@3 (de=3.31) +9 more |
| 11 | `get_upstream_features` | L6:F4516@1, k=8 → L5:F3992 (de=6.88) +7 more |
| 12 | `get_upstream_features` | L0:F3498@2, k=8 → Emb:" they"@2 (de=42.75) +7 more |
| 13 | `get_upstream_features` | L0:F2238@4, k=8 → Emb:" about"@4 (de=35.00) +7 more |
| 14 | `get_upstream_features` | L1:F5978@12, k=8 → Emb:" fire"@12 (de=27.12) +7 more |
| 15 | `get_upstream_features` | L3:F6227@23, k=8 → Emb:" to"@23 (de=6.75) +7 more |
| 16 | `get_upstream_features` | L12:F12606@25, k=8 → Emb:" not"@21 (de=3.59) +7 more |
| 17 | `inspect_feature` ×2 | L3:6227, L1:5978 |
| 18 | `get_upstream_features` | L6:F4516@1, k=8 → L5:F3992 (de=6.88) +7 more |
| 19 | `get_upstream_features` | L0:F3498@2, k=8 → Emb:" they"@2 (de=42.75) +7 more |
| 20 | `get_upstream_features` | L0:F8444@13, k=8 → Emb:" to"@13 (de=41.00) +7 more |
| 21 | `get_upstream_features` | L0:F15492@8, k=8 → Emb:" for"@8 (de=39.00) +7 more |
| 22 | `get_upstream_features` | L0:F6051@18, k=8 → Emb:"."@18 (de=47.00) +7 more |
| 23 | `get_upstream_features` | L2:F14822@1, k=8 → Emb:"So"@1 (de=19.62) +7 more |
| 24 | `get_upstream_features` | L6:F14585@1, k=8 → Emb:"So"@1 (de=9.25) +7 more |

### Build

`build_circuit` → 24 nodes, 40 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 75,664 | 9,006 | 439,574 | 0 | $0.0599 | — | — |
| **Total** | | **75,664** | **9,006** | **439,574** | **0** | **$0.0599** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 6s