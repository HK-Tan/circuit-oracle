# Circuit Oracle Report
**Date:** 2026-07-28 07:18:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies the subject as a journalist/writer, driven primarily by the explicit profession tokens "writer" and "freelance" propagating through a clean journalism-feature cascade (L2→L4→L6→L14), with the pronoun "he" at pos 22 contributing a notable secondary positive push via L0:F12768.

**Confidence:** 6

**Reasoning:** The user's concern about spurious gender features is **partially validated but not the dominant story**. Here's the breakdown:

**Genuine profession signal (dominant path):** The "writer" embedding (pos 28, direct_effect=5.75) is the largest single driver and feeds a clean journalism cascade: L2:F9210 ("journalism/writing/articles", promoted: Article/article/post) → L4:F13253 ("journalism/media", promoted: Journalism/journalists/media) → L6:F12712 ("editor/publisher titles", promoted: editors) → L14:F4420 ("journalism/newspapers", promoted: journalists/journalist/journalism/reporter). The "freelance" embedding (pos 27, direct_effect=2.69) reinforces this chain. These features are semantically coherent profession indicators with low frac_nonzero (0.003–0.017), suggesting the probe IS using genuine profession vocabulary, not a shortcut.

**Gender pronoun contribution (the spurious concern):** L0:F12768 fires on the "he" embedding at pos 22 (direct_effect=40.25 upstream from the embedding—very strong) and has direct_effect=+0.075 on the probe. This feature's autointerp is "he/she in close proximity" and its promoted tokens are generic (them, I, (, them, .). While its label mentions both pronouns, the embedding upstream is specifically "he", so on this input it acts as a male-gender marker. Its contribution is non-trivial but smaller than the journalism-cascade features in aggregate (L14:F4420 alone = -0.068, plus L6:F12712 = -0.059, vs L0:F12768 = +0.075).

**Other contributors:** L0:F9297 ("government ministries/ministers", pos 7 on "Institute") and L1:F4459 ("research institutes") activate on "Royal United Services Institute" but push the probe *downward* (negative direct_effect ~-0.06), acting as suppressor features for the journalist classification. L1:F1445 ("military vehicles/weapons", pos 7) also pushes down (-0.052), and L2:F12901 ("Middle East", pos 15) pushes down (-0.054). These reflect the text's actual defence/Middle East content, not the journalist profession.

**Verdict on spuriousness:** The probe is doing *mostly* the right thing—using "writer" and "freelance" plus their associated journalism features. However, L0:F12768's gender-pronoun contribution is real and would likely also fire on "she" in a parallel text, so the probe is not purely profession-based. A probe that scored equally on "he" and "she" writers would be cleaner; here the male-pronoun context is part of the positive signal. The gender feature is a *secondary* contributor rather than the primary mechanism, so the user's concern is moderate not severe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 28 | Emb: writer (pos 28) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: freelance (pos 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: covering (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: Institute (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: Middle (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: he (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F3007](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) | 14 | L0:F3007 'the word middle' (pos 14) |  the word "middle", and sometimes the word "character", and "camp" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) |
| [L0:F10881](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) | 12 | L0:F10881 'the word coverage' (pos 12) |  the word "coverage" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) |
| [L0:F9297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) | 7 | L0:F9297 'government ministries/ministers' (pos 7) |  mentions of government ministries and ministers. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | L0:F12768 'he/she pronouns in proximity' (pos 22) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L2:F9210](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9210) | 28 | L2:F9210 'journalism/writing/articles' (pos 28) | words related to journalism, writing, and articles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9210) |
| [L2:F12901](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12901) | 15 | L2:F12901 'Middle East' (pos 15) |  the phrase "Middle East" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12901) |
| [L1:F4459](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) | 7 | L1:F4459 'research institutes' (pos 7) |  mentions of research institutes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) |
| [L3:F10489](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10489) | 7 | L3:F10489 'the word Institute' (pos 7) |  the word "Institute" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10489) |
| [L1:F1445](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1445) | 7 | L1:F1445 'military/defence vehicles/weapons' (pos 7) |  terms related to the military, especially vehicles and weapons | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1445) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | L4:F13253 'journalism/media' (pos 28) | things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 28 | L6:F12712 'editor/publisher titles' (pos 28) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | L14:F4420 'journalism/newspapers' (pos 28) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:7124 de=-0.157 |
| 3 | `inspect_feature` ×15 | L0:7124, L0:15661, L0:12768, L0:6484, L14:4420, L0:3007, L6:12712, L0:2348, L1:4459, L0:10881, L0:1229, L0:9297, L3:10489, L2:12901, L1:1445 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@28` | ✅ reported | 12 | 21 | Trace upstream from L14:F4420 ("journalism/newspaper terms", at the prediction p… |
| SA-2 | `L6:F12712@28` | ✅ reported | 3 | 8 | Trace upstream from L6:F12712 ("editors/publishers titles", at the prediction po… |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@28, k=10 | Emb:" writer"@28 (de=5.75) +9 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 5 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 6 | `get_upstream_features` | L8:F8855@28, k=10 | Emb:" writer"@28 (de=4.72) +9 more |
| 7 | `inspect_feature` | L7, F72 | " words related to writing professionally" |
| 8 | `get_upstream_features` | L4:F13253@28, k=10 | Emb:" writer"@28 (de=9.12) +9 more |
| 9 | `get_upstream_features` | L7:F72@28, k=10 | Emb:" writer"@28 (de=5.72) +9 more |
| 10 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 11 | `inspect_feature` | L6, F6721 | " html code and related tags particularly href, public, content, title," |
| 12 | `get_upstream_features` | L2:F12020@28, k=10 | Emb:" writer"@28 (de=19.25) +9 more |
| 13 | `get_upstream_features` | L6:F12712@28, k=10 | Emb:" writer"@28 (de=6.22) +9 more |

**Findings:** The journalism‑related feature L14:F4420 is driven primarily by the raw token "writer" at position 28. The signal propagates upward through a chain of lower‑layer features: the embedding of "writer" strongly excites a very low‑layer feature (2:F12020) and the lower‑third feature L4:F13253, both of which in turn activate mid‑level journalism detectors (L7:F72, L8:F8855, L6:F12712). No gender‑relate…

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 2 | `get_upstream_features` | L6:F12712@28, k=10 | Emb:" writer"@28 (de=6.22) +9 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `get_upstream_features` | L4:F13253@28, k=10 | Emb:" writer"@28 (de=9.12) +9 more |
| 5 | `inspect_feature` | L2, F9210 | "words related to journalism, writing, and articles" |
| 6 | `get_upstream_features` | L2:F9210@28, k=10 | Emb:" writer"@28 (de=10.62) +9 more |
| 7 | `inspect_feature` | L0, F7973 | "uses of the word "guarantee" and related abstract nouns." |

**Findings:** The target feature L6:F12712, which is labelled as detecting editor/publisher titles, is chiefly driven by the input token embeddings for "writer" (pos 28) and "freelance" (pos 27). Upstream features in lower layers (L4:F13253 and L2:F9210) also show the same pattern: their strongest positive upstream nodes are the same embeddings. No specific newspaper or journal names appear among the top upstre…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F12768@22, k=8 → Emb:" he"@22 (de=40.25) +7 more |
| 2 | `get_upstream_features` | L0:F3007@14, k=8 → Emb:" Middle"@14 (de=20.75) +7 more |
| 3 | `get_upstream_features` | L0:F10881@12, k=5 → Emb:" covering"@12 (de=16.25) +4 more |
| 4 | `get_upstream_features` | L0:F9297@7, k=5 → Emb:" Institute"@7 (de=11.81) +4 more |

### Build

`build_circuit` → 19 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 41,342 | 4,856 | 144,653 | 0 | $0.0269 | — | — |
| SA-2 | openai/gpt-oss-120b | 64,299 | 3,910 | 0 | 0 | $0.0120 | ✅ 3F/8E | Trace upstream from L6:F12712 ("editors/publishers titles", … |
| SA-1 | openai/gpt-oss-120b | 216,662 | 12,477 | 15,088 | 0 | $0.0402 | ✅ 12F/21E | Trace upstream from L14:F4420 ("journalism/newspaper terms",… |
| **Total** | | **322,303** | **21,243** | **159,741** | **0** | **$0.0791** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 22s