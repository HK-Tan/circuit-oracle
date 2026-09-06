# Circuit Oracle Report
**Date:** 2026-07-28 07:02:57 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by two parallel streams: a genuine profession indicator (the word "journalistic" / "journalism" features) and a parallel stream of masculine-pronoun detectors ("He", "he", "him", "his") that load onto the same profession concept — the user's concern is largely confirmed: gendered pronouns are overrepresented in the signal relative to profession-specific vocabulary.

**Confidence:** 7

**Reasoning:**

The attribution graph reveals two main paths feeding the probe direction, both originating in the very first sentence of the prompt.

**Path 1 — Genuine profession signal (weaker than expected):**
- **Emb: journalistic (pos 13)** → directly excites L1:F1136 (image/photo credits, but relaying the token; direct_effect 5.28), L4:F13253 (journalism/media concept, direct_effect 25.6), and L7:F9092 (broadcast journalism, direct_effect 14.9).
- L4:F13253 and L7:F9092 both feed L14:F4420 ("journalism and newspapers", direct_effect 6.0 and 4.9 respectively), which is also directly excited by the "journalistic" embedding (24.4).
- L14:F4420 → output logit. This is the *intended* profession signal.

**Path 2 — Gendered pronoun signal (prominent, exactly as the user suspected):**
- **Emb: He (pos 1)** → L0:F12768's neighborhood; L4:F14796 ("he" or "him"), L4:F10952, L6:F12990 ("male pronouns and titles…men"), L2:F9301 ("mentions of men and women in relationships, dating, gendered social roles"), L7:F14893 (pronouns/possessives, including feminine forms). Direct effects 11.5 (He) and 14.75 (He→L7:F14893) are large.
- **Emb: he (pos 23)** → L0:F12768 (direct_effect 41.5) → L4:F15567 (17.0) → L17:F5889 (33.75) and L18:F14743 (25.5).
- L17:F5889 (pronoun-reference aggregator) and L0:F12768 (early "he"/"she" proximity detector) both feed L18:F14743 ("He") with direct_effects 5.16 and 3.5.
- L18:F14743 → output logit. A whole cascade of masculine-coding features (L2:F9301 men/women relationships, L6:F12990 male pronouns+titles+men-descriptors, L4:F14796 he/him, L7:F14893 pronouns) all sit in this branch.
- **Emb: him (pos 46)** and **Emb: his (pos 52)** also feed L7:F14893 (12.56, 23.6) and L0:F2994 (45) and L0:F16297 ("him" detector, 43.25) — these are bare lexical pronoun detectors with no profession semantics.

The two paths converge at the probe output. Crucially, the pronoun path contains *no profession-specific information* — it only encodes "this text is about a male individual." L2:F9301 ("men and women in relationships, dating, gendered social roles") and L6:F12990 ("male pronouns and titles along with descriptors associated with men") are explicitly gender features, not profession features. The user's concern is substantiated: the probe classification is being driven in part by a set of features whose only content is the protagonist's gender (he/him/his/He across positions 1, 23, 46, 52), independent of the journalism content. If "she" were substituted throughout, the journalism path would remain intact while the pronoun path would collapse or flip sign, suggesting the probe's profession score is not purely occupational.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | Journalism & Media concept (L14) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | Journalism & Media features (L4-L7) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 13 | Journalism & Media features (L4-L7) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L1:F1136](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1136) | 13 | Journalism & Media features (L4-L7) |  image credits and descriptions | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1136) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | "He" pronoun detector (L17-L18) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 23 | "He" pronoun detector (L17-L18) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 23 | "He" pronoun detector (L17-L18) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L16:F2918](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) | 23 | "He" pronoun detector (L17-L18) | Pronouns | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Pronoun / possessive features (L4-L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 46 | Pronoun / possessive features (L4-L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Pronoun / possessive features (L4-L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 23 | Pronoun / possessive features (L4-L7) | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 52 | Pronoun / possessive features (L4-L7) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 1 | Pronoun / possessive features (L4-L7) | the pronoun "he" or "him" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Pronoun / possessive features (L4-L7) | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Pronoun / possessive features (L4-L7) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | Pronoun / possessive features (L4-L7) |  all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 23 | Early pronoun tokens (L0) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 46 | Early pronoun tokens (L0) |  the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 52 | Early pronoun tokens (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Early pronoun tokens (L0) | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | Early pronoun tokens (L0) | mentions of stories that are being told | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L0:F61](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) | 3 | Early pronoun tokens (L0) | the word "stories" sometimes along with apostrophes and common names. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) |
| [L0:F10036](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10036) | 2 | Early pronoun tokens (L0) |  words about scientific research and scientists | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10036) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | Early pronoun tokens (L0) |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F7449](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) | 9 | Early pronoun tokens (L0) | instances of the word "representation" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) |
| [L0:F14216](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14216) | 7 | Early pronoun tokens (L0) |  the word "signs" and horizontal lines | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14216) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:6051 de=-0.256 |
| 3 | `inspect_feature` ×19 | L1:14812, L1:7449, L0:4564, L0:5333, L0:61, L7:14893, L0:2994, L0:10036, L7:14946, L0:14216, L14:4420, L18:14743, L0:6051, L0:7696, L0:3255, L0:10187, L4:13253, L0:9121, L0:1301 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@13` | ✅ reported | 3 | 6 | Trace the journalism/reporter feature (L14:F4420 at pos 13 "journalistic") upstr… |
| SA-2 | `L18:F14743@23` | ✅ reported | 4 | 5 | Trace the "He" pronoun feature (L18:F14743 at pos 23) upstream to find which inp… |
| SA-3 | `L7:F14893@46` | ✅ reported | 4 | 3 | Trace the pronoun feature (L7:F14893 at pos 46) upstream to find which input tok… |
| SA-4 | `L4:F13253@13` | ✅ reported | 4 | 8 | Trace the journalism/media feature (L4:F13253 at pos 13) upstream to find which … |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@13, k=10 | Emb:" journalistic"@13 (de=24.38) +9 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `get_upstream_features` | L4:F13253@13, k=10 | Emb:" journalistic"@13 (de=25.62) +9 more |
| 5 | `inspect_feature` | L1, F1136 | " image credits and descriptions" |
| 6 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 7 | `get_upstream_features` | L14:F4420@13, k=15 | Emb:" journalistic"@13 (de=24.38) +14 more |
| 8 | `get_upstream_features` | L7:F9092@13, k=10 | Emb:" journalistic"@13 (de=14.88) +9 more |
| 9 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |

**Findings:** The journalism/reporter feature (L14:F4420) is driven primarily by the input token "journalistic" at position 13, which directly excites it (direct_effect 24.375). A lower‑layer media‑oriented feature (L4:F13253) and a broadcast‑journalism feature (L7:F9092) also feed into it. Tracing further upstream shows that the same "journalistic" token directly excites the L4 feature, confirming the original…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@23, k=10 | Emb:" he"@23 (de=25.50) +9 more |
| 3 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 4 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 5 | `inspect_feature` | L0, F12768 | " mentions of "he" and "she" in close proximity" |
| 6 | `get_upstream_features` | L4:F15567@23, k=10 | Emb:" he"@23 (de=17.00) +9 more |
| 7 | `get_upstream_features` | L17:F5889@23, k=10 | Emb:" he"@23 (de=33.75) +9 more |
| 8 | `get_upstream_features` | L4:F15567@23, k=10 | Emb:" he"@23 (de=17.00) +9 more |
| 9 | `inspect_feature` | L15, F3330 | " personal stories of individuals, especially women and their actions o" |
| 10 | `inspect_feature` | L3, F5748 | " proper nouns" |
| 11 | `inspect_feature` | L1, F8685 | " the pronoun "he"" |
| 12 | `get_upstream_features` | L0:F12768@23, k=10 | Emb:" he"@23 (de=41.50) +9 more |

**Findings:** The target feature L18:F14743 encodes the masculine pronoun "He" at position 23. Its strongest upstream driver is the raw embedding for the token " he" (direct effect 25.5). The signal propagates through a cascade of pronoun‑reference detectors: a mid‑layer sentence‑level feature (L4:F15567), an early raw proximity detector (L0:F12768), and a higher‑level pronoun‑reference aggregator (L17:F5889). …

</details>

<details>
<summary><b>SA-3</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@46, k=10 | Emb:" him"@46 (de=12.56) +9 more |
| 3 | `inspect_feature` | L0, F16297 | " the pronoun "him"" |
| 4 | `inspect_feature` | L4, F11391 | " pronouns referring to people and words related to negative experience" |
| 5 | `get_upstream_features` | L0:F16297@46, k=10 | Emb:" him"@46 (de=43.25) +9 more |
| 6 | `inspect_feature` | L4, F4017 | " words and short phrases in French" |
| 7 | `get_upstream_features` | L0:F16297@46, k=10 | Emb:" him"@46 (de=43.25) +9 more |
| 8 | `get_upstream_features` | L4:F11391@46, k=10 | Emb:" him"@46 (de=21.12) +9 more |
| 9 | `get_upstream_features` | L4:F4017@46, k=10 | Emb:" him"@46 (de=16.38) +9 more |

**Findings:** The L7 pronoun feature (F14893) primarily aggregates gendered pronoun signals. Its strongest upstream driver is the low‑layer (0) feature 16297, a dedicated detector for the masculine pronoun "him" (direct_effect 3.02). Additional upstream contributions come from mid‑layer (4) features 11391 and 4017, which capture broader pronoun usage and French pronoun fragments, respectively. Crucially, the em…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 2 | `get_upstream_features` | L4:F13253@13, k=10 | Emb:" journalistic"@13 (de=25.62) +9 more |
| 3 | `get_upstream_features` | L4:F13253@13, k=20 | Emb:" journalistic"@13 (de=25.62) +19 more |
| 4 | `inspect_feature` | L1, F1136 | " image credits and descriptions" |
| 5 | `inspect_feature` | L0, F9121 | " the word "nice" and words with positive sentiment, sometimes related " |
| 6 | `get_upstream_features` | L1:F1136@13, k=10 | Emb:" journalistic"@13 (de=5.28) +9 more |
| 7 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 8 | `get_upstream_features` | L1:F1136@13, k=10 | Emb:" journalistic"@13 (de=5.28) +9 more |
| 9 | `get_upstream_features` | L0:F9026@13, k=10 | Emb:" journalistic"@13 (de=35.50) +9 more |
| 10 | `inspect_feature` | L0, F13988 | " proper nouns, code syntax, and scientific words related to medicine, " |

**Findings:** The journalism/media feature (L4:F13253) is primarily driven by the raw token "journalistic" at position 13. The token first activates a layer‑0 lexical detector (F9026) which passes activation to a layer‑1 bridge feature (F1136); both contribute positively to the target. A smaller boost comes from a proper‑noun detector (F13988). The path includes an embedding‑to‑feature connection (meeting requi…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_features` | token="", k=10 → 10 features; top: L0:6051 de=-0.256 |
| 2 | `get_upstream_features` | L0:F16297@46, k=5 → Emb:" him"@46 (de=43.25) +4 more |
| 3 | `get_upstream_features` | L18:F14743@23, k=3 → Emb:" he"@23 (de=25.50) +2 more |
| 4 | `get_upstream_features` | L7:F14893@1, k=5 → Emb:"He"@1 (de=14.75) +4 more |
| 5 | `get_upstream_features` | L7:F14893@3, k=5 → ❌ Feature (layer=7, feature_idx=14893) not found at pos=3. Thi |
| 6 | `get_upstream_features` | L14:F4420@13, k=3 → Emb:" journalistic"@13 (de=24.38) +2 more |
| 7 | `get_upstream_features` | L17:F5889@23, k=5 → Emb:" he"@23 (de=33.75) +4 more |
| 8 | `get_upstream_features` | L1:F1136@13, k=5 → Emb:" journalistic"@13 (de=5.28) +4 more |
| 9 | `get_upstream_features` | L7:F9092@13, k=3 → Emb:" journalistic"@13 (de=14.88) +2 more |
| 10 | `get_upstream_features` | L0:F12768@23, k=5 → Emb:" he"@23 (de=41.50) +4 more |
| 11 | `get_upstream_features` | L4:F15567@23, k=3 → Emb:" he"@23 (de=17.00) +2 more |
| 12 | `get_upstream_features` | L7:F9092@13, k=3 → Emb:" journalistic"@13 (de=14.88) +2 more |
| 13 | `get_upstream_features` | L7:F14946@1, k=5 → Emb:"He"@1 (de=11.50) +4 more |
| 14 | `get_upstream_features` | L0:F2994@52, k=3 → Emb:" his"@52 (de=45.00) +2 more |
| 15 | `inspect_feature` ×6 | L17:5889, L0:12768, L4:15567, L0:16297, L7:9092, L1:1136 |
| 16 | `get_upstream_features` | L7:F14893@46, k=3 → Emb:" him"@46 (de=12.56) +2 more |
| 17 | `get_upstream_features` | L7:F14893@52, k=3 → Emb:" his"@52 (de=23.62) +2 more |
| 18 | `inspect_feature` | L4, F4315 → " mentions of "his" and other associated pronouns like he, him, or hers" |
| 19 | `get_upstream_features` | L7:F14946@1, k=5 → Emb:"He"@1 (de=11.50) +4 more |
| 20 | `inspect_feature` ×7 | L4:14796, L6:12990, L5:10952, L2:9301, L4:9757, L15:3330, L16:2918 |

### Build

`build_circuit` → 14 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 70,414 | 6,314 | 560,272 | 0 | $0.0623 | — | — |
| SA-2 | openai/gpt-oss-120b | 149,081 | 7,446 | 10,688 | 0 | $0.0270 | ✅ 4F/5E | Trace the "He" pronoun feature (L18:F14743 at pos 23) upstre… |
| SA-1 | openai/gpt-oss-120b | 83,752 | 5,393 | 13,504 | 0 | $0.0160 | ✅ 3F/6E | Trace the journalism/reporter feature (L14:F4420 at pos 13 "… |
| SA-4 | openai/gpt-oss-120b | 104,399 | 7,266 | 21,696 | 0 | $0.0203 | ✅ 4F/8E | Trace the journalism/media feature (L4:F13253 at pos 13) ups… |
| SA-3 | openai/gpt-oss-120b | 85,255 | 5,171 | 10,976 | 0 | $0.0161 | ✅ 4F/3E | Trace the pronoun feature (L7:F14893 at pos 46) upstream to … |
| **Total** | | **492,901** | **31,590** | **617,136** | **0** | **$0.1417** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 6s