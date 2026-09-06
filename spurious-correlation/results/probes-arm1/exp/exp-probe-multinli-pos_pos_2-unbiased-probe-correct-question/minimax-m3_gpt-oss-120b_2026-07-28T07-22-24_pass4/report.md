# Circuit Oracle Report
**Date:** 2026-07-28 07:22:24 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a sparse, early-layer circuit dominated by negation-form tokens (haven't, isn't), discourse markers (yeah, well, uh), and incidental surface tokens (NC, double, year) — not by any deep semantic representation of the prompt's actual content about NCAA basketball / Louisville.

**Confidence:** 6

**Reasoning:** The circuit is heavily concentrated in layers 0–4 with a few L6 aggregators, and the strongest direct-effect features are functional/surface rather than semantic. The top driver is **L4:F12126** at pos 2 (the "well" discourse marker, frac_nonzero 0.012, effect −0.65) and **L0:F6236** at pos 20 (the literal "t" completing "haven't" in "haven't missed a single game", frac_nonzero 0.003, effect −0.46) — both classic negation/discourse surface features. Their upstream traces confirm this: L0:F6236 is driven by the embeddings of `t` (pos 20), `haven` (pos 18), `'` (pos 19) — i.e. the bare surface form of the contraction. The strongly positive feature **L4:F4847** (pos 2, +0.39) and **L3:F14620** (pos 2, +0.23) both fire on "well"/discourse-acknowledgement context, and their upstream feeds are the "well" and "yeah" embeddings. Even the content-word features (**L0:F8083** "double" with effect −0.33; **L0:F12862** "tournament"; **L0:F5912** "year"; **L0:F16366** "because") are pure lexical lookups for the literal token strings "double", "tournament", "year", "because" — they do not aggregate to a sports/NCAATournament semantic concept, but instead propagate into the **L1–L3 "double" / hyphen feature cluster** (F177 "double/multi", F12849 "double/hyphen", F9770 hyphen-related, F9247 hyphenated) which then feeds the L4 discourse features and ultimately the output. The late-layer features are all generic function-word / connective aggregators (L6:F11557 "frequently used words such as conjunctions, pronouns, or discourse markers", L6:F12415 "umm / words implying difficulty"). 

This is exactly the failure mode the user flagged: the strongest single contributor (L0:F6236, the "t"-of-"haven't" feature) is a textbook **negation-surface feature**, and its negative direct_effect on the probe direction means the presence of "haven't" pushes the probe toward contradiction. The discourse markers (well, yeah, uh) and the literal "NC double" tokens contribute the bulk of the remaining signal. None of the traced features encode a genuine contradiction semantics — they encode **lexical surface features** for negation/contracted-"not", discourse markers, and content nouns — which is why this probe would be fooled by paraphrases that preserve the surface negation while flipping the meaning, or by negated statements that are not contradictions. The user's concern is well-supported by the circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: well (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: yeah (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: haven't (pos 18-20) - negation | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 19 | Emb: haven't (pos 18-20) - negation | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: haven't (pos 18-20) - negation | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: NC double (pos 5-6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: NC double (pos 5-6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: this year (pos 23-24) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 24 | Emb: this year (pos 23-24) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: because (pos 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 20 | Negation-form features (haven't / t after isn't/doesn't) | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | Negation-form features (haven't / t after isn't/doesn't) |  the word "well" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L0:F5112](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) | 1 | Discourse markers: yeah/well/uh |  the word "resolution", sometimes in the context of displaying images or patterns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) |
| [L0:F15612](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15612) | 1 | Discourse markers: yeah/well/uh | mentions of dollar amounts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15612) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Discourse markers: yeah/well/uh | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F15682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15682) | 1 | Discourse markers: yeah/well/uh |  the word "okay" plus a few related expressions. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15682) |
| [L0:F8083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) | 6 | Content words: double/tournament/because/year/foundation | the word "double" and surrounding words when numbers are also present | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Content words: double/tournament/because/year/foundation |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L0:F12862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) | 8 | Content words: double/tournament/because/year/foundation |  the word "tournament" and related words such as "winning", but not always | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) |
| [L0:F5912](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) | 24 | Content words: double/tournament/because/year/foundation | "year" but also sometimes finds related words that include "day", "living", or "sold" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) |
| [L0:F8659](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) | 8 | Content words: double/tournament/because/year/foundation | the word "foundation" in different contexts, including religious, legal, and abstract senses. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) |
| [L0:F4365](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4365) | 1 | Content words: double/tournament/because/year/foundation | the word "neither" and related negative terms. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4365) |
| [L1:F177](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) | 6 | Double / hyphen features (L1-L3) |  the word "double" and words that begin with "multi" or "doubly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| [L1:F13255](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13255) | 8 | Double / hyphen features (L1-L3) |  the word "season" and words associated with it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13255) |
| [L1:F7762](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7762) | 8 | Double / hyphen features (L1-L3) |  the word "inspection" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7762) |
| [L2:F5201](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) | 8 | Double / hyphen features (L1-L3) | awards and accomplishments in the context of sports | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5201) |
| [L2:F2629](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2629) | 1 | Double / hyphen features (L1-L3) |  the word "doubt" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2629) |
| [L2:F15282](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15282) | 1 | Double / hyphen features (L1-L3) | the words "anyway" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15282) |
| [L3:F9770](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) | 7 | Double / hyphen mid-layer features (L3-L4) |  technical and scientific writing about neuroscience and chemistry, possibly about calcium | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| [L3:F12849](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) | 7 | Double / hyphen mid-layer features (L3-L4) |  words or phrases that include the word "double", or contain a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) |
| [L3:F14620](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) | 2 | Double / hyphen mid-layer features (L3-L4) |  the word "well" and conjunctions like "and" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) |
| [L3:F9247](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9247) | 7 | Double / hyphen mid-layer features (L3-L4) |  hyphenated words related to building and tools | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9247) |
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Discourse/well features (L4) |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Discourse/well features (L4) |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 14 | Discourse/well features (L4) | astronomy terms | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L4:F3730](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) | 7 | Discourse/well features (L4) |  text relating to lithium-ion batteries | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) |
| [L4:F6072](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) | 14 | Discourse/well features (L4) |  the word "now" followed by a verb | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6072) |
| [L6:F11557](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) | 4 | Late-layer function-word aggregators (L6) |  frequently used words such as conjunctions, pronouns, or discourse markers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) |
| [L6:F12415](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12415) | 4 | Late-layer function-word aggregators (L6) |  expressions of mild emotion or acknowledgement, particularly "umm" and similar sounds, and also words implying difficulty or problems | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12415) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:12126 de=-0.648 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F12126@2` | ❌ error | — | — | Trace the strongest negative feature L4:F12126 at position 2. What does this fea… |
| SA-2 | `L0:F6236@20` | ❌ error | — | — | Trace the feature L0:F6236 at position 20 (strong negative effect). What token d… |
| SA-3 | `L4:F4847@2` | ❌ error | — | — | Trace the strongest positive feature L4:F4847 at position 2. What does this feat… |
| SA-4 | `L0:F8083@6` | ❌ error | — | — | Trace L0:F8083 at position 6 (negative effect). What token/word does this featur… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×20 | L4:12126, L0:6236, L4:4847, L0:8083, L3:9770, L0:16366, L0:8659, L4:5709, L1:177, L0:12862, L3:12849, L3:14620, L4:3730, L0:3820, L0:5112, L6:11557, L0:8352, L0:4365, L0:5912, L0:15682 |
| 2 | `get_upstream_features` | L0:F6236@20, k=5 → Emb:"t"@20 (de=17.88) +4 more |
| 3 | `get_upstream_features` | L0:F8083@6, k=3 → Emb:" double"@6 (de=19.62) +2 more |
| 4 | `get_upstream_features` | L4:F5709@14, k=3 → Emb:" now"@14 (de=40.75) +2 more |
| 5 | `get_upstream_features` | L3:F9770@7, k=3 → Emb:" double"@6 (de=18.00) +2 more |
| 6 | `get_upstream_features` | L1:F177@6, k=3 → Emb:" double"@6 (de=24.00) +2 more |
| 7 | `get_upstream_features` | L4:F3730@7, k=3 → Emb:" A"@7 (de=13.19) +2 more |
| 8 | `get_upstream_features` | L3:F12849@7, k=3 → Emb:" double"@6 (de=25.75) +2 more |
| 9 | `get_upstream_features` | L3:F14620@2, k=3 → Emb:" well"@2 (de=9.75) +2 more |
| 10 | `get_upstream_features` | L0:F5912@24, k=3 → Emb:" year"@24 (de=18.62) +2 more |
| 11 | `get_upstream_features` | L0:F4365@1, k=3 → Emb:"yeah"@1 (de=14.81) +2 more |
| 12 | `get_top_features` | token="", k=30 → 30 features; top: L4:12126 de=-0.648 |
| 13 | `inspect_feature` ×11 | L0:16366, L0:12164, L2:15282, L0:15612, L1:13255, L1:7762, L2:5201, L2:2629, L3:9247, L4:6072, L6:12415 |

### Build

`build_circuit` → 14 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 77,265 | 5,738 | 237,333 | 0 | $0.0443 | — | — |
| **Total** | | **77,265** | **5,738** | **237,333** | **0** | **$0.0443** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 22s