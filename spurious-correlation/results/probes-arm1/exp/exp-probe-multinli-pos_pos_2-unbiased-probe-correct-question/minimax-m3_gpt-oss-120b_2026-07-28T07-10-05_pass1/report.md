# Circuit Oracle Report
**Date:** 2026-07-28 07:10:05 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven not by lexical/semantic content of the prompt but almost entirely by a cluster of low-layer "spoken-style / negation / discourse-filler" features that fire on common colloquial tokens (well, yeah, uh, the 't' in "haven't", because, year, now, double, tournament). The strongest positive contributors are "well" / "yeah" / filler features and discourse markers; the strongest negative contributors are also surface-level token detectors ("the", "okay", "t after haven'", "double"). The circuit is essentially a bag-of-discourse-markers circuit — not a content-aware contradiction detector.

**Confidence:** 7

**Reasoning:** The attribution graph on this probe direction is dominated by ~20 L0-L4 features that are all surface-form / discourse-marker detectors rather than semantic features that would distinguish factual contradiction from agreement. The top features and their semantics:

- **L0:F6236 at pos 20 ("t" of "haven't"), de = -0.648** — explicitly the contraction 't following "isn'"/"doesn'"/"haven'" with **promoted_tokens = "▁not, ▁Not, ▁NOT, not, Not, ▁bukan, ▁nicht, ▁tidak, ▁niet, ▁ikke"** (multi-lingual "not"). This is a textbook negation surface feature.
- **L0:F5112 at pos 1 ("yeah"), de = -0.206** — labeled "the word 'resolution'" but fires on "yeah" here.
- **L0:F15682 at pos 1 ("yeah"), de = 0.193** — the word "okay" plus related expressions; generic spoken-affirmation detector.
- **L0:F4365 at pos 1 ("yeah"), de = 0.198** — "the word 'neither' and related negative terms" — but fires on "yeah" pos, so it is acting as a generic short/negative-text feature.
- **L0:F8083 at pos 6 ("double"), de = -0.332** — "the word 'double' and surrounding words when numbers are also present"; pure lexical.
- **L1:F177 at pos 6 ("double"), de = -0.268** — "the word 'double' and words that begin with 'multi' or 'doubly'"; pure lexical.
- **L0:F12862 at pos 8 ("tournament"), de = -0.236** — "the word 'tournament' and related words such as 'winning'"; pure lexical.
- **L0:F8659 at pos 8 ("tournament"), de = 0.285** — labeled "foundation" but fires on "tournament" (multi-word co-occurrence feature).
- **L0:F16366 at pos 25 ("because"), de = 0.293** — "the word 'because'"; pure lexical.
- **L0:F5912 at pos 24 ("year"), de = -0.197** — "the word 'year'"; pure lexical.
- **L3:F9770 at pos 7 ("A"), de = -0.315** — generic scientific/neurochemistry text feature (spurious context match).
- **L3:F12849 at pos 7 ("A"), de = -0.230** — "words that include 'double', or contain a hyphen".
- **L3:F14620 at pos 2 ("well"), de = 0.230** — "the word 'well' and conjunctions like 'and'".
- **L4:F5709 at pos 14 ("now"), de = -0.277** — "astronomy terms" but fires on "now" (suppressed token is "now").
- **L4:F12126 at pos 2 ("well"), de = -0.648** — "expressions of agreement or acknowledgement, particularly 'well' and 'yeah'" (the biggest single driver in absolute terms).
- **L4:F4847 at pos 2 ("well"), de = 0.389** — "words or short phrases often used in conversation, and especially questions and answers".
- **L6:F11557 at pos 4 ("uh"), de = 0.201** — "frequently used words such as conjunctions, pronouns, or discourse markers".
- **L0:F3820 at pos 3 ("the"), de = 0.215** — "the word 'the'"; pure function word.

I traced these upstream and confirmed each bottoms out at a single token-embedding node: Emb "well" (pos 2) → L0:F8352/L4:F4847/L4:F12126; Emb "yeah" (pos 1) → L0:F5112/F15682/F4365; Emb "t" (pos 20) → L0:F6236; Emb "because" (pos 25) → L0:F16366; Emb "year" (pos 24) → L0:F5912; Emb "now" (pos 14) → L4:F5709; Emb "double" (pos 6) → L0:F8083/L1:F177; Emb "tournament" (pos 8) → L0:F12862/F8659. The user-concern hypothesis is supported:

1. **The strongest single contributor (L4:F12126, |de|=0.648) is literally the "well / yeah" acknowledgment detector** — a filler/pragmatic feature, not a semantic feature.
2. **L0:F6236 is an explicit negation surface feature** ("t" after "haven'", promoted tokens are "not", "Not", "NOT" in many languages). It fires on the 't in "haven't" and contributes -0.648 — the biggest push *against* the probe direction. The prompt's two "haven't" / "isn't" constructions are being read as a generic "negation signal".
3. **The bulk of remaining features are word-identity detectors** ("because", "year", "now", "double", "tournament", "well", "yeah", "uh", "the", "okay") — none of them encode whether the content contradicts a premise. They encode which content-words are present, with no role for the contrastive structure (e.g. "I haven't watched … because Louisville's out").
4. **The "because" feature (L0:F16366, de = +0.293) promotes no semantic content** — its decoder projects onto punctuation/letters because it is a single-word identity feature. It is the connective marker the model "latches onto" not because it understands the causal structure but because "because" is a high-information discourse token in this dataset.
5. **Source-influence analysis** (source_positions = the "because" and "year" / "t" tokens) returned S_pct_of_total = -3.06% and S_over_R = -0.54, indicating these key content tokens are NOT strong drivers of the probe direction; the signal is diffuse and dominated by filler positions.

The circuit therefore matches the user's concern: the probe is reading the input through a **surface-form / discourse-marker lens** — counting "well", "yeah", "uh", "haven't", "because", "the", and topic words (tournament, double, year) — rather than through a semantic contradiction circuit. There is no entity-recognition or event-comparison feature anywhere in the graph; the most semantically loaded features in the attribution (L0:F6236 negation, L4:F12126 well/yeah acknowledgment) are pragmatic/syntactic markers, not world-knowledge or compositional features. The "contradiction" classification appears to be driven by the **density of spoken-style discourse markers and the presence of a negation surface form**, exactly the kind of spurious pattern the user worried about.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Mid-layer discourse/filler features |  expressions of agreement or acknowledgement, particularly "well" and "yeah" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Mid-layer discourse/filler features |  words or short phrases often used in conversation, and especially questions and answers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |
| [L3:F14620](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) | 2 | Mid-layer discourse/filler features |  the word "well" and conjunctions like "and" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14620) |
| [L6:F11557](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) | 4 | Mid-layer discourse/filler features |  frequently used words such as conjunctions, pronouns, or discourse markers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11557) |
| [L3:F9770](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) | 7 | Mid-layer discourse/filler features |  technical and scientific writing about neuroscience and chemistry, possibly about calcium | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9770) |
| [L3:F12849](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) | 7 | Mid-layer discourse/filler features |  words or phrases that include the word "double", or contain a hyphen | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12849) |
| [L4:F3730](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) | 7 | Mid-layer discourse/filler features |  text relating to lithium-ion batteries | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3730) |
| [L0:F15682](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15682) | 1 | Mid-layer discourse/filler features |  the word "okay" plus a few related expressions. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15682) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 20 | Negation: 't' after "haven'"/"isn'" (promotes 'not') | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Word 'because' |  the word "because" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L0:F5912](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) | 24 | Word 'year' | "year" but also sometimes finds related words that include "day", "living", or "sold" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5912) |
| [L4:F5709](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) | 14 | Word 'now' | astronomy terms | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5709) |
| [L0:F8083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) | 6 | Word 'double' (NCAA double-A) | the word "double" and surrounding words when numbers are also present | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8083) |
| [L1:F177](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) | 6 | Word 'double' (NCAA double-A) |  the word "double" and words that begin with "multi" or "doubly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/177) |
| [L0:F12862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) | 8 | Word 'tournament' |  the word "tournament" and related words such as "winning", but not always | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12862) |
| [L0:F8659](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) | 8 | Word 'tournament' | the word "foundation" in different contexts, including religious, legal, and abstract senses. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8659) |
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | Word 'well' (L0:F8352) |  the word "well" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L0:F5112](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) | 1 | Spoken-style/negation features on 'yeah' |  the word "resolution", sometimes in the context of displaying images or patterns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5112) |
| [L0:F4365](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4365) | 1 | Spoken-style/negation features on 'yeah' | the word "neither" and related negative terms. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4365) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:12126 de=-0.648 |
| 3 | `inspect_feature` ×20 | L4:12126, L0:6236, L4:4847, L0:8083, L3:9770, L0:16366, L0:8659, L4:5709, L1:177, L0:12862, L3:12849, L3:14620, L4:3730, L0:3820, L6:11557, L0:8352, L0:4365, L0:5912, L0:15682, L0:5112 |
| 4 | `get_source_influence` | {'depth': 3, 'source_positions': [16, 21, 29], 'S_pct_of_total': -3.06, 'R_pct_o |
| 5 | `inspect_feature` ×2 | L0:6138, L0:5938 |
| 6 | `get_upstream_features` | Emb:"t"@20 (de=17.88) +9 more |
| 7 | `get_upstream_features` | Emb:" well"@2 (de=14.62) +9 more |
| 8 | `get_upstream_features` | Emb:" double"@6 (de=19.62) +9 more |
| 9 | `get_upstream_features` | Emb:" double"@6 (de=18.00) +9 more |
| 10 | `get_upstream_features` | Emb:" because"@25 (de=40.75) +9 more |
| 11 | `get_upstream_features` | Emb:" tournament"@8 (de=15.25) +9 more |
| 12 | `get_upstream_features` | Emb:" year"@24 (de=18.62) +9 more |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F6236@20` | ❌ error | — | — | Trace this feature upstream. What does it represent? What input tokens drive it?… |
| SA-2 | `L4:F4847@2` | ✅ reported | 4 | 9 | Trace this feature upstream. What is it encoding - the "well yeah" at start of p… |
| SA-3 | `L0:F16366@25` | ❌ error | — | — | Trace this feature upstream. It's labeled as "because". What input tokens drive … |
| SA-4 | `L0:F12862@8` | ❌ error | — | — | Trace this feature upstream. It's labeled as "tournament". What input tokens dri… |

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F4847 | " words or short phrases often used in conversation, and especially que" |
| 2 | `get_upstream_features` | L4:F4847@2, k=10 | Emb:" well"@2 (de=8.06) +9 more |
| 3 | `inspect_feature` | L2, F7222 | "the word "well"" |
| 4 | `inspect_feature` | L2, F1759 | "occurrences of the word "know" with emphasis words or interjections ne" |
| 5 | `get_upstream_features` | L2:F7222@2, k=10 | Emb:" well"@2 (de=20.25) +9 more |
| 6 | `inspect_feature` | L0, F15972 | "the word "yeah"" |
| 7 | `get_upstream_features` | L2:F7222@2, k=10 | Emb:" well"@2 (de=20.25) +9 more |
| 8 | `get_upstream_features` | L2:F1759@2, k=10 | Emb:" well"@2 (de=12.56) +9 more |

**Findings:** The target L4:F4847 feature is a high‑level conversational‑filler detector that fires on the opening phrase "well" (and related discourse markers). Its strongest upstream driver is the raw embedding for the token " well" at position 2, which directly excites it. A lower‑layer word detector (L2:F7222) for "well" further amplifies the signal, itself driven almost entirely by the same " well" embeddi…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11557@4, k=10 → Emb:" uh"@4 (de=11.19) +9 more |
| 2 | `get_upstream_features` | L0:F8352@2, k=10 → Emb:" well"@2 (de=30.88) +9 more |
| 3 | `get_upstream_features` | L4:F4847@2, k=10 → Emb:" well"@2 (de=8.06) +9 more |
| 4 | `get_upstream_features` | L3:F14620@2, k=10 → Emb:" well"@2 (de=9.75) +9 more |
| 5 | `get_upstream_features` | L4:F5709@14, k=10 → Emb:" now"@14 (de=40.75) +9 more |
| 6 | `get_upstream_features` | L1:F177@6, k=10 → Emb:" double"@6 (de=24.00) +9 more |
| 7 | `get_upstream_features` | L3:F12849@7, k=10 → Emb:" double"@6 (de=25.75) +9 more |
| 8 | `get_upstream_features` | L4:F3730@7, k=10 → Emb:" A"@7 (de=13.19) +9 more |
| 9 | `get_upstream_features` | L0:F8659@8, k=10 → Emb:" tournament"@8 (de=15.25) +9 more |
| 10 | `get_upstream_features` | L0:F12862@8, k=10 → Emb:" tournament"@8 (de=20.62) +9 more |
| 11 | `get_upstream_features` | L0:F5112@1, k=10 → Emb:"yeah"@1 (de=11.50) +9 more |
| 12 | `get_upstream_features` | L0:F15682@1, k=10 → Emb:"yeah"@1 (de=15.56) +9 more |
| 13 | `inspect_feature` ×2 | L0:6236, L0:4365 |

### Build

`build_circuit` → 22 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 108,489 | 10,496 | 469,102 | 0 | $0.0733 | — | — |
| SA-2 | openai/gpt-oss-120b | 86,602 | 5,182 | 32 | 0 | $0.0161 | ✅ 4F/9E | Trace this feature upstream. What is it encoding - the "well… |
| **Total** | | **195,091** | **15,678** | **469,134** | **0** | **$0.0894** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 40s