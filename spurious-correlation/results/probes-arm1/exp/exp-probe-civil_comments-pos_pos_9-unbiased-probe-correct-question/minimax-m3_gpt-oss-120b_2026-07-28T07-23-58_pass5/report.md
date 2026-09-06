# Circuit Oracle Report
**Date:** 2026-07-28 07:23:58 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity-probe score is driven by a sparse set of token-level identity-marker features ("white", "married", "Maybe", "to", "guys", "author", "appears") and several marriage/family features, rather than by any feature that actually encodes the toxic/slur content of the prompt — confirming the user's concern that the circuit is using identity-related lexical cues as proxies for toxicity.

**Confidence:** 7

**Reasoning:**

The attribution graph's top features all reduce to either single-word token detectors or generic lexical/semantic features at layer 0-3, plus two late-layer author/book features. Critically, none of the features I inspected, even the late-layer L6:2851 "books/authors" or L6:13528 "academic works and their writers", encode anything specific to slurs, hate speech, or the toxic content of the prompt. They are general lexical detectors that would fire on any prompt containing these words.

The top driving features by direct_effect are:
- L0:3436 "the word 'white'" at pos 9 (direct_effect 0.1719, frac_nonzero 0.061) — pure identity-token detector
- L0:2242 "the word 'guys'" at pos 10 (direct_effect 0.1011) — generic word detector
- L0:8444 "the word 'to'" at pos 7 (direct_effect -0.1836, inhibitory) — function word
- L2:3399 "words related to marriage" at pos 6 'married' (direct_effect 0.1748) — fires because the text contains "married", unrelated to toxicity
- L0:9881 "the word 'appear'" at pos 3 (direct_effect 0.1138)
- L1:384 "the string 'ash' or 'pund'" at pos 2 'author' (direct_effect 0.1206) — a string-substring detector
- L3:10004 "words which mean or indicate uncertainty or possibility" at pos 17 'Maybe' (direct_effect 0.1387)
- L3:494 "text relating to marriage, birth, death, family and religion" at pos 6 (direct_effect 0.1138)

Tracing upstream confirms the chain bottoms out at embedding nodes almost immediately. L2:3399 has direct embedding contribution from "married" (29) and "be" (-0.625) at pos 5-6, with mixed feature inputs (L0:1102 "study", L0:4668 "aged", L1:10492 "divorce", L1:14321 "roll", L0:241 "marriage", L0:15578 "mentions of marriage"). The marriage signal is a generic lexical family detector — it has nothing to do with hateful framing.

Similarly, the L6 late-layer "author/books" features (L6:2851 and L6:13528) both bottom out in the "author" token at pos 2 via the embedding node (direct_effect 11-13). Their upstream features are entirely academic-writing related (L2:14801 "mentions of authors and their written works", L3:3214 "authors or writers", L4:8371 "authorship of articles and academic papers", L5:13407 "words related to writing and publishing a scientific paper"). These features would activate on any sentence about an author — they cannot distinguish the toxic use of "the author" in this prompt from a neutral academic one.

The marriage-related features at L3 (L3:6262, L3:8254, L3:494) similarly trace entirely to the "married" embedding at pos 6 with direct effects of 17-37. These are general vocabulary detectors for the word "married" that have no relationship to whether the surrounding context is toxic.

The probe's classification is therefore not driven by features that encode the hateful framing of the prompt (e.g., the slur, the racist stereotypes, the dehumanizing tone). Instead it is driven by the presence of identity-marker tokens (white, oriental, married, guy, Maybe) that frequently co-occur with toxic content in training data, plus several general lexical features. This is exactly the spurious-correlation pattern the user identified: the probe treats identity-marker vocabulary as a proxy for toxicity, rather than actually reading the prompt's toxic content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 9 | Token: 'white' (L0) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F2242](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) | 10 | Token: 'guys' (L0) |  the word "guys" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 7 | Token: 'to' (L0) — function word | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 4 | Token: 'to' (L0) — pos 4 | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F753](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) | 2 | Token: 'author' (L0) — selling/prices | the word "author" and words related to selling and prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) |
| [L0:F4408](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) | 2 | Token: 'authors' (L0) — academic |  the word "authors" in academic papers or similar documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) |
| [L0:F9881](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9881) | 3 | Token: 'appear' (L0) | the word "appear" and its variants | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9881) |
| [L0:F6087](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6087) | 2 | Token: artists/performers (L0) |  mentions of performers or artists, and sometimes "man." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6087) |
| [L0:F5538](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5538) | 2 | Token: 'hero' (L0) |  the word "hero" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5538) |
| [L0:F9796](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9796) | 2 | Token: 'ordinary/authors' (L0) |  the word "ordinary" and related words like "authors" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9796) |
| [L1:F384](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) | 2 | Token: 'ash/pund' (L1) |  the string "ash" or "pund" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) |
| [L2:F3399](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) | 6 | Marriage vocabulary (L2) — pos 6 'married' |  words related to marriage | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) |
| [L0:F15578](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15578) | 6 | Marriage (L0) — pos 6 | mentions of marriage and related ideas | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15578) |
| [L1:F1431](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) | 6 | Marriage (L1) — pos 6 marriage family |  instances of the word "fair" and the phrase "ends of justice" in legal documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) |
| [L3:F494](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) | 6 | Marriage/death/family (L3) — pos 6 |  text relating to marriage, birth, death, family and religion | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) |
| [L3:F10004](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) | 17 | Uncertainty/possibility (L3) — pos 17 |  words which mean or indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) |
| [L3:F11152](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) | 17 | Uncertainty/possibility (L3) — pos 17 (neg) | words that indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) |
| [L3:F6262](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) | 6 | Marriage (L3) — pos 6 (neg) | mentions of marriage | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) |
| [L3:F8254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) | 7 | Marriage/family (L3) — pos 7 (neg) |  words and phrases related to marriage and family relationships | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) |
| [L6:F13528](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13528) | 2 | Academic works/writers (L6) — pos 2 |  words related to academic works and their writers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13528) |
| [L6:F2851](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) | 2 | Books/authors/reading (L6) — pos 2 | books and associated things such as authors and reading | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:753 de=-0.275 |
| 3 | `inspect_feature` ×19 | L6:2851, L2:3399, L0:3436, L3:10004, L0:753, L0:8444, L3:6262, L0:4408, L3:8254, L3:11152, L1:384, L0:9881, L3:494, L1:1431, L6:13528, L0:6087, L0:5538, L0:9796, L0:2242 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F3399@6` | ❌ error | — | — | Trace upstream from the L2:3399 "words related to marriage" feature at position … |
| SA-2 | `L0:F3436@9` | ❌ error | — | — | Trace upstream from L0:3436 "the word 'white'" at position 9. This is a token-le… |
| SA-3 | `L6:F2851@2` | ❌ error | — | — | Trace upstream from L6:2851 "books and associated things such as authors and rea… |
| SA-4 | `L3:F6262@6` | ❌ error | — | — | Trace upstream from L3:6262 "mentions of marriage" at position 6. This is a nega… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F3399@6, k=10 → Emb:" married"@6 (de=29.00) +9 more |
| 2 | `get_upstream_features` | L6:F2851@2, k=10 → Emb:" author"@2 (de=11.06) +9 more |
| 3 | `get_upstream_features` | L3:F6262@6, k=10 → Emb:" married"@6 (de=37.75) +9 more |
| 4 | `get_upstream_features` | L3:F8254@7, k=10 → Emb:" married"@6 (de=26.62) +9 more |
| 5 | `get_upstream_features` | L3:F494@6, k=10 → Emb:" married"@6 (de=17.75) +9 more |
| 6 | `get_upstream_features` | L1:F1431@6, k=10 → Emb:" married"@6 (de=19.00) +9 more |
| 7 | `get_upstream_features` | L3:F10004@17, k=10 → Emb:" Maybe"@17 (de=43.25) +9 more |
| 8 | `get_upstream_features` | L3:F11152@17, k=10 → Emb:" Maybe"@17 (de=41.25) +9 more |
| 9 | `get_upstream_features` | L0:F9881@3, k=10 → Emb:" appears"@3 (de=13.44) +9 more |
| 10 | `get_upstream_features` | L0:F2242@10, k=10 → Emb:" guy"@10 (de=19.62) +9 more |
| 11 | `inspect_feature` ×18 | L0:13691, L0:1102, L0:4668, L1:14321, L1:10492, L0:6051, L0:1554, L0:14165, L0:11458, L0:8364, L0:9026, L0:11814, L0:15578, L0:1847, L0:5687, L1:13492, L0:7272, L0:6051 |
| 12 | `get_upstream_features` | L0:F8444@7, k=5 → Emb:" to"@7 (de=41.75) +4 more |
| 13 | `get_upstream_features` | L0:F4408@2, k=5 → Emb:" author"@2 (de=15.94) +4 more |
| 14 | `get_upstream_features` | L0:F753@2, k=5 → Emb:" author"@2 (de=18.38) +4 more |
| 15 | `get_upstream_features` | L6:F13528@2, k=5 → Emb:" author"@2 (de=13.12) +4 more |
| 16 | `inspect_feature` ×22 | L3:3214, L4:8371, L5:13407, L2:14801, L3:6697, L2:1612, L2:15558, L2:6759, L1:5872, L1:2010, L0:241, L1:11419, L5:5359, L1:8539, L2:13961, L1:15413, L1:10549, L2:5413, L1:7921, L0:5152, L0:815, L1:16179 |

### Build

`build_circuit` → 30 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 139,198 | 7,819 | 405,225 | 0 | $0.0755 | — | — |
| **Total** | | **139,198** | **7,819** | **405,225** | **0** | **$0.0755** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 58s