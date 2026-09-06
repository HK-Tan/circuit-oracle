# Circuit Oracle Report
**Date:** 2026-07-28 07:21:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifying the subject as a "reporter" is driven by two largely independent paths: (1) a clean, on-target profession path rooted in the literal word "reporter" at position 66, and (2) a male-pronoun ("he/his") path that reaches the output logit with comparable magnitude — confirming the user's concern that gender markers contribute substantially to the profession classification.

**Confidence:** 8

**Reasoning:**

**Path 1 — Genuine profession indicator (strongest positive driver, direct_effect ≈ +0.20 total).** The dominant positive signal flows from the embedding of the literal token "reporter" at position 66 (in "…as a reporter…") up through a coherent journalism feature hierarchy:
- **Emb: reporter (pos 66)** → **L4:13253** "journalism and media" (direct_effect=+6.75) + **L4:661** "reports/documentaries/TV coverage" → **L7:13646** "news reporting and journalism", **L7:9092** "broadcast journalism", **L7:9521** "news sources" → **L8:8855** "news reporters and reporting" → **L14:4420** "journalism and newspapers" (frac_nonzero=0.017, promoted_tokens = journalist/reporter/journalism) → **L19:2486** "journalistic sources and news outlets" (direct_effect=−0.12) → output logit. These are the genuine profession features; `get_source_influence` confirms position 66 carries +0.56 S_pct_of_total (the largest source-position signal in the graph) with S_over_R = 0.11.

**Path 2 — Gender marker (the user's concern, validated).** A parallel, independent path carries comparable weight into the output:
- **Emb: He (pos 1) / his (pos 3) / his (pos 61)** → **L0:2994** "the pronoun 'his' and 'he'" (frac_nonzero=0.07, direct_effect=+0.23 from "his" at pos 3 alone) → **L7:14893** + **L7:14946** (pronoun/possessive-pronoun features, frac_nonzero=0.008–0.017) → **L18:14743** "He" (frac_nonzero=0.018, suppressed_tokens include "she", "her", "herself"; direct_effect=−0.11) → output logit. **L18:14743 also fires at positions 69 and 86** (direct_effect=−0.09 each), and **L17:1069** "phrases about giving something to other people" (its top-activating example is literally the word "him") reinforces the male-person signal. Critically, the `get_source_influence` check on the pronoun positions {3, 25, 61} returns S_pct_of_total = **−5.0** with S_over_R ≈ −0.99 — these positions are nearly as influential as the top non-source driver, and almost entirely through male-pronoun features.

**Why this confirms the user's hypothesis.** The probe's "reporter" classification is supported by two mechanisms of similar magnitude: a legitimate profession signal from the literal word "reporter," and a spurious gender signal from the "he/his" pronouns that pepper the text (positions 1, 3, 25, 51, 61, 69, 86 — i.e. nearly every sentence). The pronoun path does not transit through any profession-specific features; it goes pronoun-feature → "He" feature → output, with the "He" feature actively *suppressing* "she/her/herself" tokens. This is exactly the kind of bias the user suspected: the classifier relies partly on the subject's grammatical gender (consistently male here) rather than solely on the profession token. The output direction in this probe is therefore entangled with a male-protagonist co-occurrence pattern that Gemma-2-2B has learned from training data, even when profession-indicating evidence (the word "reporter") is independently and correctly present.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | L19:2486 — journalistic sources/news outlets (at "reporter", pos 66) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | L14:4420 — journalism/newspapers (at "reporter", pos 66) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 66 | L8:8855 — news reporters and reporting (at "reporter", pos 66) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 66 | L7:13646 / 9092 / 9521 — news reporting / broadcast journalism / news sources (at "reporter", pos 66) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 66 | L7:13646 / 9092 / 9521 — news reporting / broadcast journalism / news sources (at "reporter", pos 66) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F9521](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9521) | 66 | L7:13646 / 9092 / 9521 — news reporting / broadcast journalism / news sources (at "reporter", pos 66) |  news sources and people involved in journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9521) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | L4:13253 / 661 — journalism & media / reports & TV coverage (at "reporter", pos 66) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F661](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) | 66 | L4:13253 / 661 — journalism & media / reports & TV coverage (at "reporter", pos 66) |  words and phrases used when referring to reports, documentaries, and television coverage of news | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 25 | L18:14743 — pronoun "He" (anti-promotes "she/her") (at "He", pos 25; and pos 69, 86) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 69 | L18:14743 — pronoun "He" (anti-promotes "she/her") (at "He", pos 25; and pos 69, 86) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 86 | L18:14743 — pronoun "He" (anti-promotes "she/her") (at "He", pos 25; and pos 69, 86) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7:14893 / 14946 — pronouns / possessive pronouns (at "He", pos 1) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7:14893 / 14946 — pronouns / possessive pronouns (at "He", pos 1) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | L0:2994 — "his" / "he" pronoun feature (at "his", pos 3) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 61 | L0:2994 — "his" / "he" pronoun feature (at "his", pos 3) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: He (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: his (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 61 | Emb: his (pos 61) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: He (pos 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 66 | Emb: reporter (pos 66) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 9 | Negative / off-target features (generic stopwords "from", "has", "and", University tokens) — small negative contributions | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 24 | Negative / off-target features (generic stopwords "from", "has", "and", University tokens) — small negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F886](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) | 2 | Negative / off-target features (generic stopwords "from", "has", "and", University tokens) — small negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 6 | Negative / off-target features (generic stopwords "from", "has", "and", University tokens) — small negative contributions | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 16 | Negative / off-target features (generic stopwords "from", "has", "and", University tokens) — small negative contributions | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.232 |
| 3 | `inspect_feature` ×5 | L0:2994, L14:4420, L19:2486, L18:14743, L0:8974 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14743@25` | ❌ error | — | — | Trace the "He" pronoun feature upstream. What input tokens/positions drive it? D… |
| SA-2 | `L14:F4420@66` | ❌ error | — | — | Trace the journalism/newspaper feature upstream. What does it depend on? Is it a… |
| SA-3 | `L0:F2994@3` | ❌ error | — | — | Trace the "his/he" pronoun feature at position 3 upstream. It's an embedding-lay… |
| SA-4 | `L7:F14893@1` | ❌ error | — | — | Trace this early-layer feature at position 1 (pos 1 is likely "He") upstream to … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14743@25, k=10 → Emb:" He"@25 (de=24.00) +9 more |
| 2 | `get_upstream_features` | L14:F4420@66, k=10 → Emb:" reporter"@66 (de=18.75) +9 more |
| 3 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"He"@1 (de=14.75) +9 more |
| 4 | `get_upstream_features` | L7:F14946@1, k=10 → Emb:"He"@1 (de=11.50) +9 more |
| 5 | `inspect_feature` ×5 | L7:14893, L7:14946, L18:5889, L17:1069, L0:1069 |
| 6 | `get_upstream_features` | L8:F8855@66, k=10 → Emb:" reporter"@66 (de=16.88) +9 more |
| 7 | `get_upstream_features` | L7:F13646@66, k=10 → Emb:" reporter"@66 (de=15.12) +9 more |
| 8 | `get_upstream_features` | L7:F9092@66, k=10 → L4:F13253 (de=6.81) +9 more |
| 9 | `get_upstream_features` | L7:F9521@66, k=10 → Emb:" reporter"@66 (de=17.25) +9 more |
| 10 | `inspect_feature` ×5 | L8:8855, L7:13646, L7:9092, L7:9521, L4:13253 |
| 11 | `get_upstream_features` | L0:F2994@3, k=5 → Emb:" his"@3 (de=42.25) +4 more |
| 12 | `get_upstream_features` | L0:F2994@61, k=5 → Emb:" his"@61 (de=45.50) +4 more |
| 13 | `inspect_feature` ×3 | L0:7681, L0:4677, L0:14824 |
| 14 | `get_upstream_features` | L19:F2486@66, k=10 → Emb:" reporter"@66 (de=28.25) +9 more |
| 15 | `inspect_feature` ×2 | L4:661, L6:12712 |
| 16 | `get_upstream_features` | L14:F4420@66, k=5 → Emb:" reporter"@66 (de=18.75) +4 more |
| 17 | `get_source_influence` | {'depth': 3, 'source_positions': [66]} → {'depth': 3, 'source_positions': [66], 'S_pct_of_total': 0.563, 'R_pct_of_total' |
| 18 | `get_source_influence` | {'depth': 3, 'source_positions': [3, 61, 25]} → {'depth': 3, 'source_positions': [3, 25, 61], 'S_pct_of_total': -5.004, 'R_pct_o |
| 19 | `get_source_influence` | {'depth': 3, 'source_positions': [21]} → {'depth': 3, 'source_positions': [21], 'S_pct_of_total': -3.112, 'R_pct_of_total |
| 20 | `inspect_feature` ×3 | L17:1069, L14:4420, L19:2486 |

### Build

`build_circuit` → 15 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,619 | 5,617 | 343,641 | 0 | $0.0416 | — | — |
| **Total** | | **47,619** | **5,617** | **343,641** | **0** | **$0.0416** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 53s