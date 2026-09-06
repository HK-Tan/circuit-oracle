# Circuit Oracle Report
**Date:** 2026-07-28 07:19:13 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a sparse set of shallow, lexically grounded features — primarily the tokens "married" (pos 6), "author" (pos 2), "white" (pos 9), "guy" (pos 10), "to" (pos 7), and "Maybe" (pos 17) — with no deep semantic or compositional circuit for toxicity.

**Confidence:** 6

**Reasoning:** The top-20 features driving the probe direction have direct_effects almost entirely originating from the input token embeddings themselves. The most positive contribution comes from **L2:F3399 "words related to marriage"** (de=+0.175) and **L6:F2851 "books and associated things such as authors"** (de=+0.206), both of which trace upstream to the *raw embedding* of the token "married" (de=29) and "author" (de=11) respectively — the subagent confirmed L2:F3399 is driven by the literal token " married" (direct_effect 29.0) with only generic ancillary contributors. Similarly, **L0:F3436 "mentions of the word 'white'"** (de=+0.172) is almost purely an embedding-driven feature at pos 9 with de=18 from the "white" token; its top activating examples include neutral uses ("white paper", "white dwarf") and racially charged contexts alike, so the feature itself is a *lexical* detector, not an identity-bias detector. **L0:F2242 "the word 'guys'"** (de=+0.101) likewise fires on the "guy" token. **L3:F10004 "uncertainty/possibility"** (de=+0.139) and **L3:F11152** (de=−0.115) trace to the "Maybe" token embedding (de=43.25). **L0:F8444 "the word 'to'"** fires on the function word "to" at multiple positions. **L3:F8254 / F6262 / F494** are all marriage-family detectors (promoted tokens include "married", "marriage", "brides", "wedding") driven directly by the "married" embedding (de=26.6, 37.75, 17.75). None of these features encode hate-speech semantics, slur usage, or identity-group bias; they are surface lexical detectors. The user's concern is partially *not* supported by the circuit — there is no "spurious identity-group" feature. However, the user's concern is supported in a *different* sense: the probe appears to classify the text based on **bag-of-keywords** cues (married, white, author, guy, maybe) rather than a toxicity-aware circuit. The presence of the word "married" alone, the word "white" alone, and "Maybe" alone — all entirely benign in isolation — are the dominant drivers. This means the probe is a *shallow lexical* probe, not a semantic-toxicity probe. The fact that low-frac_nonzero marriage/author features (0.004–0.014) are doing the classification work is consistent with the model encoding these as high-precision lexical detectors (not identity-group detectors) that happen to co-occur in this text. The circuit, traced all the way to embedding nodes for "author", "married", "white", "guy", "Maybe", "to", and "appears", shows signal flow: **Emb tokens → L0 lexical features → L1–L3 mid-layer detectors → L6 author/books cluster → probe logit**. The deepest semantic feature is L6:F2851 (books/authors) at pos 2, which still traces to the "author" token embedding. There is no evidence of a deeper toxicity or hateful-attitude circuit; the classification rides on lexical co-occurrence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F2851](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) | 2 | Author/books semantic cluster (pos 2, late layer) | books and associated things such as authors and reading | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2851) |
| [L6:F13528](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13528) | 2 | Author/books semantic cluster (pos 2, late layer) |  words related to academic works and their writers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13528) |
| [L2:F14801](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14801) | 2 | Author/books semantic cluster (pos 2, late layer) |  mentions of authors and their written works. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14801) |
| [L2:F3399](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) | 6 | Marriage/lexical cluster at "married" (pos 6) |  words related to marriage | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3399) |
| [L3:F6262](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) | 6 | Marriage/lexical cluster at "married" (pos 6) | mentions of marriage | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6262) |
| [L3:F8254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) | 7 | Marriage/lexical cluster at "married" (pos 6) |  words and phrases related to marriage and family relationships | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8254) |
| [L3:F494](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) | 6 | Marriage/lexical cluster at "married" (pos 6) |  text relating to marriage, birth, death, family and religion | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/494) |
| [L1:F1431](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) | 6 | Marriage/lexical cluster at "married" (pos 6) |  instances of the word "fair" and the phrase "ends of justice" in legal documents | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1431) |
| [L0:F753](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) | 2 | Marriage/lexical cluster at "married" (pos 6) | the word "author" and words related to selling and prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/753) |
| [L0:F4408](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) | 2 | Marriage/lexical cluster at "married" (pos 6) |  the word "authors" in academic papers or similar documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4408) |
| [L1:F384](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) | 2 | Marriage/lexical cluster at "married" (pos 6) |  the string "ash" or "pund" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/384) |
| [L0:F6087](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6087) | 2 | Marriage/lexical cluster at "married" (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6087) |
| [L0:F9796](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9796) | 2 | Marriage/lexical cluster at "married" (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9796) |
| [L0:F5538](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5538) | 2 | Marriage/lexical cluster at "married" (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5538) |
| [L0:F9881](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9881) | 3 | Marriage/lexical cluster at "married" (pos 6) | the word "appear" and its variants | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9881) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 9 | "white" lexical detector (pos 9) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F2242](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) | 10 | "guy"/"guys" lexical detector (pos 10) |  the word "guys" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 7 | "to" function-word detector (pos 4,7) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 4 | "to" function-word detector (pos 4,7) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L3:F10004](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) | 17 | Uncertainty cluster (pos 17) |  words which mean or indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10004) |
| [L3:F11152](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) | 17 | Uncertainty cluster (pos 17) | words that indicate uncertainty or possibility | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11152) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:753 de=-0.275 |
| 3 | `inspect_feature` ×6 | L0:753, L6:2851, L0:8444, L2:3399, L0:3436, L3:6262 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F2851@2` | ❌ error | — | — | Trace L6:F2851 "books/authors" upstream to understand if it captures "author" co… |
| SA-2 | `L2:F3399@6` | ✅ reported | 5 | 5 | Trace L2:F3399 "marriage" upstream to find its embedding inputs. Does it activat… |
| SA-3 | `L0:F3436@9` | ❌ error | — | — | Trace L0:F3436 "white" upstream. Does it just fire on the lexical "white" token? |
| SA-4 | `L3:F10004@17` | ✅ reported | 4 | 5 | Trace L3:F10004 upstream. What does this feature encode? It's at pos 17 in the s… |
| SA-5 | `L1:F1431@6` | ❌ error | — | — | Trace L1:F1431 upstream. What does it represent and what tokens does it encode? |

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F3399 | " words related to marriage" |
| 2 | `get_upstream_features` | L2:F3399@6, k=10 | Emb:" married"@6 (de=29.00) +9 more |
| 3 | `inspect_feature` | L0, F13691 | "words of positive sentiment and verbs associated with leisure activiti" |
| 4 | `inspect_feature` | L0, F1102 | " the word study" |
| 5 | `inspect_feature` | L0, F4668 | " the word "aged" sometimes appearing near demographic words" |
| 6 | `inspect_feature` | L1, F14321 | " the word "roll" or a variation of it" |

**Findings:** The target L2:F3399 feature is primarily driven by the explicit embedding of the token " married" at position 6 (direct_effect 29.0). All other upstream contributors are generic lexical or sentiment detectors located in very early transformer layers (0‑1) and have only tiny positive effects. No broader conceptual or policy‑related circuit is involved. Hence, L2:F3399 activates purely on the lexica…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F10004 | " words which mean or indicate uncertainty or possibility" |
| 2 | `get_upstream_features` | L3:F10004@17, k=10 | Emb:" Maybe"@17 (de=43.25) +9 more |
| 3 | `inspect_feature` | L0, F5687 | "words indicating uncertainty or possibility" |
| 4 | `inspect_feature` | L0, F5152 | " the word "relief", often in a context related to legal or medical sit" |
| 5 | `get_upstream_features` | L0:F5687@17, k=10 | Emb:" Maybe"@17 (de=17.62) +9 more |
| 6 | `get_upstream_features` | L0:F5152@17, k=10 | Emb:" Maybe"@17 (de=15.38) +9 more |

**Findings:** L3:F10004 is an uncertainty detector that heavily leans on the embedding of the token "Maybe" (pos 17). The strongest upstream influence is the raw embedding itself, satisfying the lower‑third layer requirement. Two early‑layer features (L0:F5687 and L0:F5152) also feed into it, with L0:F5687 being another uncertainty cue and L0:F5152 providing a minor ancillary boost. The path shows that this cir…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F2851@2, k=10 → Emb:" author"@2 (de=11.06) +9 more |
| 2 | `get_upstream_features` | L0:F3436@9, k=8 → Emb:" white"@9 (de=18.00) +7 more |
| 3 | `get_upstream_features` | L1:F1431@6, k=10 → Emb:" married"@6 (de=19.00) +9 more |
| 4 | `inspect_feature` ×5 | L3:10004, L1:1431, L0:9881, L0:4408, L3:10004 |
| 5 | `get_upstream_features` | L3:F6262@6, k=8 → Emb:" married"@6 (de=37.75) +7 more |
| 6 | `inspect_feature` | L0, F3436 → " mentions of the word "white"" |
| 7 | `get_upstream_features` | L3:F8254@7, k=8 → Emb:" married"@6 (de=26.62) +7 more |
| 8 | `get_upstream_features` | L3:F11152@17, k=8 → Emb:" Maybe"@17 (de=41.25) +7 more |
| 9 | `get_upstream_features` | L0:F2242@10, k=8 → Emb:" guy"@10 (de=19.62) +7 more |
| 10 | `get_upstream_features` | L1:F384@2, k=8 → Emb:" author"@2 (de=13.94) +7 more |
| 11 | `inspect_feature` ×5 | L3:8254, L3:11152, L0:2242, L1:384, L6:13528 |
| 12 | `get_upstream_features` | L6:F2851@2, k=5 → Emb:" author"@2 (de=11.06) +4 more |
| 13 | `get_upstream_features` | L6:F13528@2, k=5 → Emb:" author"@2 (de=13.12) +4 more |
| 14 | `get_upstream_features` | L0:F8444@7, k=5 → Emb:" to"@7 (de=41.75) +4 more |
| 15 | `inspect_feature` ×2 | L3:494, L2:14801 |
| 16 | `get_upstream_features` | L3:F494@6, k=5 → Emb:" married"@6 (de=17.75) +4 more |
| 17 | `get_upstream_features` | L3:F8254@7, k=5 → Emb:" married"@6 (de=26.62) +4 more |
| 18 | `get_upstream_features` | L3:F10004@17, k=5 → Emb:" Maybe"@17 (de=43.25) +4 more |

### Build

`build_circuit` → 14 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 41,964 | 5,186 | 278,533 | 0 | $0.0355 | — | — |
| SA-4 | openai/gpt-oss-120b | 53,208 | 3,087 | 96 | 0 | $0.0098 | ✅ 4F/5E | Trace L3:F10004 upstream. What does this feature encode? It'… |
| SA-2 | openai/gpt-oss-120b | 56,264 | 3,341 | 2,528 | 0 | $0.0105 | ✅ 5F/5E | Trace L2:F3399 "marriage" upstream to find its embedding inp… |
| **Total** | | **151,436** | **11,614** | **281,157** | **0** | **$0.0558** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 52s