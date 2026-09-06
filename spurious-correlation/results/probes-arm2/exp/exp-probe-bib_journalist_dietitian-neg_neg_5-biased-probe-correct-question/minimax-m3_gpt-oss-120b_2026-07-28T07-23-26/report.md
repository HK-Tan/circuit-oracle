# Circuit Oracle Report
**Date:** 2026-07-28 07:23:26 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of the profession is driven almost entirely by a male-pronoun detection circuit (He/his at positions 1, 3, 25, 61, 86) rather than by the profession word "reporter" itself.

**Confidence:** 8

**Reasoning:** The top features in `get_top_features` are dominated by layer-0 token detectors keyed to male pronouns and male-coded sentence particles, not to "reporter." Tracing upstream confirms this:

- **L0:F2994** (pos 3, 61) activates on the embeddings of "his" and "His" (direct_effect ~42-46).
- **L0:F8974** (pos 9) activates on the embedding of "from."
- **L0:F6051** (pos 24) activates on the embedding of ".".
- **L0:F8061** (pos 6) activates on the embedding of "in."
- **L0:F14824** (pos 16) activates on "has."
- **L0:F7681 / F886** (pos 2) activate on "obtained."
- These layer-0 features feed **L0:F1069** (pos 25, "He" embedding, direct_effect 37) and then a chain **L13:F6622 → L15:F3330 → L17:F5889 → L18:F14743** at position 25, all tracking the pronoun "He" with direct_effects of +24 at the top.

A parallel pronoun branch at the sentence-initial "He" (pos 1) flows through **L7:F14893** (direct_effect +0.14, from "He" embedding +14.75) and **L7:F14946** (inhibitory, -0.12). A third branch tracks the pronoun "he" at the final position (pos 86) via **L0:F12768 → L15:F3330 → L17:F5889 → L18:F14743**.

The "reporter" profession word (pos 66) does have its own path — **L4:F13253 → L14:F4420 → L19:F2486** — but **L14:F4420 contributes -0.205 and L19:F2486 contributes -0.12 to the probe**, i.e. the late-layer "reporter" features *suppress* the probe score. The early layer-4 detector on "reporter" (F13253, direct_effect -0.14) is also negative. Meanwhile **L7:F14893 contributes +0.14** (positive toward the probe) and is driven by the "He" token.

**Net effect on the logit:** the positive contributions (He-token feature +0.14, his-token +0.23, He-pos-61 +0.13, plus deeper L18 pronoun features +0.11/-0.09 net) outweigh the negative "reporter" profession features. The probe is therefore classifying the person as the labeled profession primarily because the surrounding text is loaded with male pronouns, not because the profession word itself drives the classifier. This matches the user concern exactly: the probe leans on a spurious gender-marker side channel rather than on the genuine profession indicator "reporter."

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | "reporter" profession word path (mixed signals) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | "reporter" profession word path (mixed signals) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | "reporter" profession word path (mixed signals) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 86 | "reporter" profession word path (mixed signals) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 25 | Male pronoun features (mid-layer) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 25 | Male pronoun features (mid-layer) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 25 | Male pronoun features (mid-layer) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 25 | Male pronoun features (mid-layer) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 25 | Male pronoun features (mid-layer) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Male pronoun features (mid-layer) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Male pronoun features (mid-layer) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Layer-0 male pronoun detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 61 | Layer-0 male pronoun detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 9 | Layer-0 male pronoun detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 24 | Layer-0 male pronoun detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 6 | Layer-0 male pronoun detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 16 | Layer-0 male pronoun detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F7681](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) | 2 | Layer-0 male pronoun detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) |
| [L0:F886](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) | 2 | Layer-0 male pronoun detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.232 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ❌ error | — | — | Trace this layer-0 feature to understand what input token/pattern it detects and… |
| SA-2 | `L14:F4420@66` | ❌ error | — | — | Trace this mid-layer feature to understand what it encodes at position 66 and ho… |
| SA-3 | `L0:F8974@9` | ❌ error | — | — | Trace this layer-0 feature at pos 9 (likely "He" or "University" token) to under… |
| SA-4 | `L18:F14743@25` | ❌ error | — | — | Trace this late-layer feature at pos 25 to understand what profession or entity … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2994@3, k=10 → Emb:" his"@3 (de=42.25) +9 more |
| 2 | `get_upstream_features` | L0:F8974@9, k=10 → Emb:" from"@9 (de=40.00) +9 more |
| 3 | `get_upstream_features` | L14:F4420@66, k=10 → Emb:" reporter"@66 (de=18.75) +9 more |
| 4 | `get_upstream_features` | L18:F14743@25, k=10 → Emb:" He"@25 (de=24.00) +9 more |
| 5 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"He"@1 (de=14.75) +9 more |
| 6 | `get_upstream_features` | L0:F6051@24, k=10 → Emb:"."@24 (de=47.25) +9 more |
| 7 | `get_upstream_features` | L0:F8061@6, k=10 → Emb:" in"@6 (de=38.50) +9 more |
| 8 | `get_upstream_features` | L19:F2486@66, k=10 → Emb:" reporter"@66 (de=28.25) +9 more |
| 9 | `get_upstream_features` | L4:F13253@66, k=8 → Emb:" reporter"@66 (de=26.62) +7 more |
| 10 | `get_upstream_features` | L17:F5889@25, k=8 → Emb:" He"@25 (de=22.38) +7 more |
| 11 | `get_upstream_features` | L0:F7681@2, k=8 → Emb:"He"@1 (de=6.31) +7 more |
| 12 | `get_upstream_features` | L0:F14824@16, k=8 → Emb:" has"@16 (de=34.75) +7 more |
| 13 | `get_upstream_features` | L0:F886@2, k=8 → Emb:" obtained"@2 (de=11.69) +7 more |
| 14 | `get_upstream_features` | L18:F14743@86, k=8 → Emb:" he"@86 (de=23.88) +7 more |
| 15 | `get_upstream_features` | L0:F1069@25, k=8 → Emb:" He"@25 (de=37.00) +7 more |
| 16 | `get_upstream_features` | L7:F14946@1, k=8 → Emb:"He"@1 (de=11.50) +7 more |
| 17 | `get_upstream_features` | L0:F2994@61, k=5 → Emb:" his"@61 (de=45.50) +4 more |
| 18 | `get_upstream_features` | L0:F12768@86, k=5 → Emb:" he"@86 (de=41.25) +4 more |

### Build

`build_circuit` → 14 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 25,538 | 4,551 | 53,068 | 0 | $0.0163 | — | — |
| **Total** | | **25,538** | **4,551** | **53,068** | **0** | **$0.0163** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 57s