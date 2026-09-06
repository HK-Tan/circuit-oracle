# Circuit Oracle Report
**Date:** 2026-07-28 07:22:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "journalist" classification is driven by a hybrid signal: the genuine profession-indicating token "journalistic" at pos 13 directly excites a chain of journalism/media features (L4 → L7 broadcast → L9 news → L14 journalism words → L18 pronoun/persisting-media concept), but the same pronoun chain is also strongly seeded by male-pronoun tokens ("He/him/his" at positions 1, 23, 46, 52) through dedicated his/he features at L0 and L7, making the masculine-pronoun pattern a co-equal — and arguably confoundable — circuit leg.

**Confidence:** 7

**Reasoning:**

**Genuine profession circuit (the "real" signal).** The strongest positive direct effects on the probe are L14:F4420 (journalism/newspaper words, +0.1318) and L4:F13253 (journalism/media, -0.1543 / but exciting its downstream). Their dominant upstream is the `journalistic` token embedding at pos 13 (direct_effect 24.375 into L14:F4420; 25.625 into L4:F13253) — i.e., the single word "journalistic" is the load-bearing input. This token seeds the L4 media feature, the L7 broadcast-news feature (F9092, "broadcasting/newsroom/director"), the L9 general news-production feature (F7435, frac_nonzero 0.22), and ultimately L14:F4420 which promotes tokens like `journalists`, `journalism`, `reporter`, `editorial`. This is a textbook, content-grounded profession circuit.

**The spurious gender-marker leg (the user's concern).** In parallel, the prompt is densely seeded with male-pronoun tokens: `He` (pos 1), `he` (pos 23), `him` (pos 46), `his` (pos 52). Each directly drives male-pronoun features — L0:F2994 ("his"/"he"), L0:F12768 ("he" in proximity), L0:F16297 ("him"), L0:F61 ("stories" but suppressed→vocab gender-arc tokens). These feed L7:F14893 and L7:F14946 (possessive/male pronouns, promoted tokens = `his`/`himself`/`He`, suppressed = `herself`/`she`/`her`), then L17:F5889 (pronoun/possessive references at pos 23, activation 27.4, direct upstream = `he` token with direct_effect 33.75), and finally L18:F14743 ("He" pronoun feature, frac_nonzero 0.018). The L7 pronouns contribute substantially to the probe: F14893@pos46 has direct_effect +0.1963 and F14893@pos1 +0.1631.

**How they converge.** Crucially, the L17:F5889 pronoun/persisting-reference feature does NOT just carry gender — its top activating examples include sustained "He"-anchored narratives and it feeds the L18 concept node, which is the highest-level node in the circuit before the output. So the model has fused a "male protagonist + journalism-setting" composite concept: when `He ... journalistic ... he ... him ... his` co-occur, L17:L18 light up and push the probe. The same L14:L18 chain that genuinely represents "journalist" also partly represents "a male subject in a journalism context." This is the precise mechanism the user flagged: the probe is partially riding on a male-pronoun pattern, not purely on the profession word.

**Quantification.** The male-pronoun embeddings contribute direct_effects of 14.75 (He@1 → L7:F14946), 11.5 (He@1 → L7:F14893), 41.5 (`he`@23 → L0:F12768), 43.25 (`him`@46 → L0:F16297), 45.0 (`his`@52 → L0:F2994). These are large in absolute terms but L0 features are diffuse (high frac_nonzero 0.07 for F2994) and the genuine profession signal from `journalistic` (direct_effect 25.6 into L4) is comparably large. The probe is mostly but not exclusively driven by the profession word; a non-trivial share flows through the pronoun pathway, validating the user's concern that gender markers are a confounder in the circuit.

**Verdict.** The user's worry is correct but partial: the circuit does use a male-pronoun pathway, but the dominant profession content ("journalistic" → L4 media → L7 broadcast → L9 news → L14 journalism) is genuine. The spuriousness is concentrated at L7-L18 where pronoun features and profession features converge in a single composite "male journalist" concept node.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Journalism/media profession concept (L14-L18) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | Journalism/newspaper words (L14) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 13 | Broadcast journalism phrases (L7) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L9:F7435](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) | 13 | News production/media (L9) |  words and phrases related to news production and media | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | Journalism/media (L4) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 23 | Pronoun/possessive references (L17-L18) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 52 | Male pronouns (his/he) (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 23 | Male pronouns (his/he) (L0) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 46 | Male pronouns (his/he) (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 46 | Possessive/male pronoun features (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Possessive/male pronoun features (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Possessive/male pronoun features (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 52 | Possessive/male pronoun features (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Research/stories/representation words (L0-L1) | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | Research/stories/representation words (L0-L1) | mentions of stories that are being told | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L0:F61](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) | 3 | Research/stories/representation words (L0-L1) | the word "stories" sometimes along with apostrophes and common names. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | Research/stories/representation words (L0-L1) |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F7449](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) | 9 | Research/stories/representation words (L0-L1) | instances of the word "representation" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) |
| [L0:F10036](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10036) | 2 | Research/stories/representation words (L0-L1) |  words about scientific research and scientists | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10036) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 4 | Function-word features (and, time, on, ., same) (L0) |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F10187](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10187) | 8 | Function-word features (and, time, on, ., same) (L0) | the word "time" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10187) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | Function-word features (and, time, on, ., same) (L0) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F7696](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7696) | 18 | Function-word features (and, time, on, ., same) (L0) | the word "on" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7696) |
| [L0:F14216](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14216) | 7 | Function-word features (and, time, on, ., same) (L0) |  the word "signs" and horizontal lines | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14216) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:6051 de=-0.256 |
| 3 | `inspect_feature` ×19 | L1:14812, L1:7449, L0:4564, L0:5333, L0:61, L7:14893, L0:2994, L0:10036, L0:3255, L0:10187, L0:6051, L0:7696, L0:9121, L0:1301, L0:14216, L7:14946, L4:13253, L14:4420, L18:14743 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@13` | ❌ error | — | — | Trace the upstream circuit from L14:F4420 (journalism/newspaper words) at pos 13… |
| SA-2 | `L18:F14743@23` | ❌ error | — | — | Trace upstream from L18:F14743 ("He" pronoun feature) at pos 23, which has direc… |
| SA-3 | `L7:F14893@46` | ❌ error | — | — | Trace upstream from L7:F14893 (pronouns/possessive pronouns feature) at pos 46. … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@13, k=15 → Emb:" journalistic"@13 (de=24.38) +14 more |
| 2 | `get_upstream_features` | L4:F13253@13, k=15 → Emb:" journalistic"@13 (de=25.62) +14 more |
| 3 | `get_upstream_features` | L18:F14743@23, k=15 → Emb:" he"@23 (de=25.50) +14 more |
| 4 | `get_upstream_features` | L7:F14946@1, k=15 → Emb:"He"@1 (de=11.50) +14 more |
| 5 | `get_upstream_features` | L7:F14893@46, k=15 → Emb:" him"@46 (de=12.56) +14 more |
| 6 | `get_upstream_features` | L7:F14893@1, k=15 → Emb:"He"@1 (de=14.75) +14 more |
| 7 | `get_upstream_features` | L0:F2994@52, k=15 → Emb:" his"@52 (de=45.00) +14 more |
| 8 | `get_upstream_features` | L0:F4564@2, k=12 → Emb:" researches"@2 (de=13.25) +11 more |
| 9 | `get_upstream_features` | L1:F7449@9, k=10 → Emb:" represents"@9 (de=20.50) +9 more |
| 10 | `get_upstream_features` | L1:F14812@3, k=10 → Emb:" stories"@3 (de=18.62) +9 more |
| 11 | `get_upstream_features` | L0:F5333@3, k=10 → Emb:" stories"@3 (de=16.38) +9 more |
| 12 | `get_upstream_features` | L0:F61@3, k=10 → Emb:" stories"@3 (de=17.38) +9 more |
| 13 | `inspect_feature` ×4 | L7:9092, L9:7435, L17:5889, L0:12768 |
| 14 | `get_upstream_features` | L0:F14216@7, k=10 → Emb:" same"@7 (de=18.25) +9 more |
| 15 | `get_upstream_features` | L7:F14946@52, k=10 → Emb:" his"@52 (de=24.25) +9 more |
| 16 | `get_upstream_features` | L4:F13253@13, k=8 → Emb:" journalistic"@13 (de=25.62) +7 more |
| 17 | `get_upstream_features` | L17:F5889@23, k=10 → Emb:" he"@23 (de=33.75) +9 more |
| 18 | `get_upstream_features` | L0:F12768@23, k=8 → Emb:" he"@23 (de=41.50) +7 more |
| 19 | `get_upstream_features` | L0:F16297@46, k=8 → Emb:" him"@46 (de=43.25) +7 more |

### Build

`build_circuit` → 20 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 63,006 | 6,528 | 395,124 | 0 | $0.0504 | — | — |
| **Total** | | **63,006** | **6,528** | **395,124** | **0** | **$0.0504** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 34s