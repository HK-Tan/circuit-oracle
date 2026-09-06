# Circuit Oracle Report
**Date:** 2026-07-28 07:20:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by generic lexical / topical features (author/book, married, white, guy, Maybe) rather than by features encoding identity-group concepts — the circuit traces word content, not demographic targeting.

**Confidence:** 7

**Reasoning:** The graph's late-layer features (L5–L6) driving the probe direction are exclusively topical/lexical: **L6:F2851** ("books and associated things such as authors and reading", frac=0.014, direct_effect=+0.21), **L6:F13528** ("words related to academic works and their writers", frac=0.014, de=+0.11), **L5:F13407** ("words related to writing and publishing a scientific paper, including authors and funding", frac=0.082), **L4:F8371** ("words and phrases related to authorship of articles and academic papers", frac=0.032), **L3:F3214** ("authors or writers", frac=0.003), and **L2:F14801** ("mentions of authors and their written works", frac=0.014) — all activated on the "**author**" token at pos 2 (embedding direct_effect 11.06, 13.13). Their promoted tokens are "books", "authors", "brides", "wedding" — no identity-group vocabulary. The mid-layer cluster (**L3:F6262** "mentions of marriage" frac=0.0007, de=−0.16; **L3:F8254** "words and phrases related to marriage and family relationships" frac=0.005, de=−0.15; **L3:F494** "text relating to marriage, birth, death, family and religion" frac=0.018, de=+0.11; **L2:F3399** "words related to marriage" frac=0.004, de=+0.17; **L2:F15558** "forms of 'settle' and the word 'married'" frac=0.005; **L1:F10492** "the word 'divorce'"; **L1:F1431** "the word 'fair' and the phrase 'ends of justice'") trace cleanly back to the **married** token at pos 6 (embedding de=37.75) and **to** at pos 7 — all activated by the literal verb "married." The hedging features **L3:F10004** (de=+0.14) and **L3:F11152** (de=−0.12) come directly from the **Maybe** embedding (de=43.25). Crucially, **L0:F3436** (the "white" feature, frac=0.06, de=+0.17) fires on the literal token "white" at pos 9 with direct_effect=18 from its embedding, and **L0:F2242** ("the word 'guys'") fires on "guy" at pos 10 (de=19.6) — these are word-identity features, not identity-group classifiers. No features in the circuit have labels like "Asian women," "interracial relationships," "derogatory language about an ethnic group," or anything encoding protected-class targeting; everything reduces to surface-level token recognition of "author/married/Maybe/white/guy" with the same activated examples being from neutral academic and biographical contexts. The user's concern is **not supported by this circuit**: the probe's signal is carried by *lexical* features that would activate identically on benign sentences like "The author is married and writes about her family" or "Maybe the white dwarf is 1.4 solar masses." The pathological part of the text (slurs, demographic stereotyping) does not appear to flow through identity-class features in this attribution graph — the toxicity signal, if present, is being driven by incidental vocabulary overlap with toxicity-training distributions (the word "white," the construction "married to a white guy," the hedge "Maybe") rather than by the model having learned a spurious identity-group detector.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score (toxicity/racial direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L6:F2851](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) | 2 | Late-layer authorship/book features (L3-L6) | books and associated things such as authors and reading | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) |
| [L6:F13528](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13528) | 2 | Late-layer authorship/book features (L3-L6) |  words related to academic works and their writers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13528) |
| [L5:F13407](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13407) | 2 | Late-layer authorship/book features (L3-L6) |  words related to writing and publishing a scientific paper, including authors and funding | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13407) |
| [L4:F8371](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8371) | 2 | Late-layer authorship/book features (L3-L6) |  words and phrases related to authorship of articles and academic papers | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8371) |
| [L3:F3214](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3214) | 2 | Late-layer authorship/book features (L3-L6) |  authors or writers | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3214) |
| [L2:F14801](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14801) | 2 | Late-layer authorship/book features (L3-L6) |  mentions of authors and their written works. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14801) |
| [L3:F6262](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) | 6 | Mid-layer marriage / family features (L3) | mentions of marriage | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) |
| [L3:F8254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) | 7 | Mid-layer marriage / family features (L3) |  words and phrases related to marriage and family relationships | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) |
| [L3:F494](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) | 6 | Mid-layer marriage / family features (L3) |  text relating to marriage, birth, death, family and religion | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) |
| [L2:F3399](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) | 6 | Mid-layer marriage / family features (L3) |  words related to marriage | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) |
| [L2:F15558](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15558) | 6 | Mid-layer marriage / family features (L3) |  forms of the word "settle" and the word "married." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15558) |
| [L2:F15558](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15558) | 7 | Mid-layer marriage / family features (L3) |  forms of the word "settle" and the word "married." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15558) |
| [L1:F10492](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10492) | 6 | Mid-layer marriage / family features (L3) | the word 'divorce' | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10492) |
| [L1:F1431](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) | 6 | Mid-layer marriage / family features (L3) |  instances of the word "fair" and the phrase "ends of justice" in legal documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) |
| [L1:F384](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) | 2 | Mid-layer marriage / family features (L3) |  the string "ash" or "pund" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) |
| [L3:F10004](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) | 17 | Uncertainty / hedging features (L3, pos 17 'Maybe') |  words which mean or indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) |
| [L3:F11152](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) | 17 | Uncertainty / hedging features (L3, pos 17 'Maybe') | words that indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) |
| [L0:F753](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) | 2 | Layer-0 lexical features | the word "author" and words related to selling and prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) |
| [L0:F4408](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) | 2 | Layer-0 lexical features |  the word "authors" in academic papers or similar documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) |
| [L0:F9796](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9796) | 2 | Layer-0 lexical features |  the word "ordinary" and related words like "authors" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9796) |
| [L0:F5538](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5538) | 2 | Layer-0 lexical features |  the word "hero" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5538) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 9 | Layer-0 lexical features |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 1 | Layer-0 lexical features |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F6087](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6087) | 2 | Layer-0 lexical features |  mentions of performers or artists, and sometimes "man." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6087) |
| [L0:F2242](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) | 10 | Layer-0 lexical features |  the word "guys" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) |
| [L0:F11570](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11570) | 5 | Layer-0 lexical features | the word "be" and words that can be associated with obligation | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11570) |
| [L0:F1102](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1102) | 6 | Layer-0 lexical features |  the word study | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1102) |
| [L0:F4668](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4668) | 6 | Layer-0 lexical features |  the word "aged" sometimes appearing near demographic words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4668) |
| [L0:F1847](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1847) | 6 | Layer-0 lexical features | scientific terms and experimental details related to biological and chemical research | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1847) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 4 | Layer-0 lexical features | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 7 | Layer-0 lexical features | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F9881](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9881) | 3 | Layer-0 lexical features | the word "appear" and its variants | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9881) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:753 de=-0.275 |
| 3 | `inspect_feature` ×19 | L6:2851, L2:3399, L0:3436, L0:4408, L3:10004, L1:384, L0:753, L0:8444, L3:6262, L3:8254, L3:11152, L3:494, L1:1431, L6:13528, L0:9881, L0:2242, L0:6087, L0:5538, L0:9796 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F2851@2` | ❌ error | — | — | Trace the upstream path from L6:F2851 ("books and associated things such as auth… |
| SA-2 | `L3:F6262@6` | ❌ error | — | — | Trace the upstream path from L3:F6262 ("mentions of marriage") at pos 6. Find wh… |
| SA-3 | `L3:F8254@7` | ❌ error | — | — | Trace the upstream path from L3:F8254 ("words and phrases related to marriage an… |
| SA-4 | `L3:F494@6` | ❌ error | — | — | Trace the upstream path from L3:F494 ("text relating to marriage, birth, death, … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F2851@2, k=15 → Emb:" author"@2 (de=11.06) +14 more |
| 2 | `get_upstream_features` | L3:F6262@6, k=15 → Emb:" married"@6 (de=37.75) +14 more |
| 3 | `get_upstream_features` | L3:F8254@7, k=15 → Emb:" married"@6 (de=26.62) +14 more |
| 4 | `get_upstream_features` | L3:F494@6, k=15 → Emb:" married"@6 (de=17.75) +14 more |
| 5 | `get_upstream_features` | L3:F10004@17, k=15 → Emb:" Maybe"@17 (de=43.25) +14 more |
| 6 | `get_upstream_features` | L2:F3399@6, k=15 → Emb:" married"@6 (de=29.00) +14 more |
| 7 | `inspect_feature` ×10 | L2:14801, L5:13407, L3:3214, L4:8371, L1:10492, L0:11570, L0:4668, L2:15558, L0:1847, L0:1102 |
| 8 | `get_upstream_features` | L0:F4408@2, k=10 → Emb:" author"@2 (de=15.94) +9 more |
| 9 | `get_upstream_features` | L0:F3436@9, k=10 → Emb:" white"@9 (de=18.00) +9 more |
| 10 | `get_upstream_features` | L3:F11152@17, k=10 → Emb:" Maybe"@17 (de=41.25) +9 more |
| 11 | `get_upstream_features` | L1:F1431@6, k=10 → Emb:" married"@6 (de=19.00) +9 more |
| 12 | `get_upstream_features` | L0:F2242@10, k=10 → Emb:" guy"@10 (de=19.62) +9 more |
| 13 | `get_upstream_features` | L0:F8444@7, k=8 → Emb:" to"@7 (de=41.75) +7 more |
| 14 | `get_upstream_features` | L0:F8444@4, k=8 → Emb:" to"@4 (de=40.25) +7 more |
| 15 | `get_upstream_features` | L0:F3436@7, k=5 → ❌ Feature (layer=0, feature_idx=3436) not found at pos=7. This |
| 16 | `get_upstream_features` | L3:F10004@17, k=5 → Emb:" Maybe"@17 (de=43.25) +4 more |
| 17 | `get_upstream_features` | L6:F13528@2, k=10 → Emb:" author"@2 (de=13.12) +9 more |
| 18 | `get_upstream_features` | L0:F3436@1, k=5 → Emb:"The"@1 (de=7.62) +4 more |

### Build

`build_circuit` → 16 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 62,078 | 6,321 | 449,822 | 0 | $0.0532 | — | — |
| **Total** | | **62,078** | **6,321** | **449,822** | **0** | **$0.0532** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 27s