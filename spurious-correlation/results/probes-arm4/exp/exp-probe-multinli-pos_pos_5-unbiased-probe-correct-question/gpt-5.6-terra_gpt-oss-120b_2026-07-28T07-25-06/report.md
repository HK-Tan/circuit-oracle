# Circuit Oracle Report
**Date:** 2026-07-28 07:25:06 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven mainly by surface-form/syntactic cues—especially the “not only … but also” construction—rather than by a composed representation of the later sentence’s semantic contradiction.

**Confidence:** 8/10

**Reasoning:** The output is an injected linear probe direction, not a vocabulary prediction. Its largest direct contributors are mixed-sign lexical/construction detectors:

- The strongest negative feature is **L15:F12905 at pos 13** (direct effect **−0.3555**), a highly selective (**frac_nonzero 0.00526**) detector for **“but”** and contrast/consequence constructions. Its promoted tokens include “also,” consistent with the literal **“not only … but also”** template. Upstream attribution reaches **Emb: “ not” (pos 6)**, **Emb: “ only” (pos 7)**, and especially **Emb: “ but” (pos 13)**, as well as intermediate contrast features **L4:F2884** and **L14:F11020**. Thus this is a direct lexical-template circuit, and it *opposes* the probe direction on this example.

- The most important positive late contribution, **L17:F3763 at pos 7** (direct effect **+0.1670**, activation 46.5), is labeled **“only”** (**frac_nonzero 0.07178**) and has top activating examples dominated by *not only … but also*. Its main upstream inputs are **L15:F1990**, **L14:F10765**, **L9:F12274**, and **L2:F5627**, all at the same `only` position, plus direct support from **Emb: “ not” (pos 6)** and **Emb: “ only” (pos 7)**. This provides the positive branch from the same construction into the probe.

- There are also shallow, non-contradiction lexical cues. **L2:F13565 at pos 5** is a very selective detector for **“program(me)s”** (**frac_nonzero 0.00116**) and positively affects the score (**+0.1973**); it is overwhelmingly driven by **Emb: “ program” (pos 5)** (upstream direct effect **+16.75**). This detects a topic word, not whether the two statements disagree.

- The positive **L5:F7144 at pos 3** (**+0.2168**) detects a proper noun followed by **“said”** (**frac_nonzero 0.02023**). It is driven directly by **Emb: “ said” (pos 3)** and contributes to a reporting-clause pathway with **L4:F12847**, whose label is reporting verbs plus “that.” Again, this is discourse/reporting syntax rather than contradiction content.

The constructed circuit therefore has three material routes into the probe: (1) the `not`/`only` construction route, which contributes positively; (2) the `but`/contrast-template route, which contributes negatively; and (3) shallow `program` and reporting-verb lexical/syntactic features. The contrast route’s cancellation with the `not only` route is especially revealing: the probe is sensitive to components of an idiomatic construction whose presence does **not** itself mean semantic negation or contradiction.

The input genuinely contains a contradiction at the semantic level: the first sentence says the program *will improve* lawyers’ public image, while the final sentence says it *isn’t going to improve* it. But among the high-effect inspected features there is no clear circuit that binds the repeated subject/topic (“the program” / “lawyers’ public image”), aligns the two propositions, and applies negation to the shared predicate. Instead, the visible dominant circuit originates at token embeddings for **“not,” “only,” “but,” “program,” and “said.”**

So the user concern is substantially supported: this probe’s classification is at least heavily confounded by superficial lexical and constructional features, particularly the incidental **“not only … but also”** phrase in the first statement. The presence of a real contradiction in this example prevents concluding that the score is *entirely* spurious, but the traced attribution does not provide evidence that semantic contradiction detection is the mechanism driving it.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F12847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) | 3 | Reporting-clause / attribution syntax | sentences with some reporting verb and the word 'that' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12847) |
| [L5:F7144](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) | 3 | Reporting-clause / attribution syntax |  proper nouns followed by the word "said" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7144) |
| [L2:F13565](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) | 5 | Program lexical detector |  the word "program(me)s" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13565) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | Not-only construction detectors | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 7 | Not-only construction detectors | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L15:F1990](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) | 7 | Not-only construction detectors | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/1990) |
| [L17:F3763](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) | 7 | Not-only construction detectors | only | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3763) |
| [L4:F2884](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) | 13 | But / contrast-construction detector (opposes probe direction) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2884) |
| [L14:F11020](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) | 13 | But / contrast-construction detector (opposes probe direction) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11020) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | But / contrast-construction detector (opposes probe direction) |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L15:12905 de=-0.355 |
| 3 | `inspect_feature` ×5 | L15:12905, L17:3763, L0:8046, L5:7144, L2:13565 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L15:F12905@13` | ❌ error | — | — | Trace the major negative contributor to the synthetic probe score upstream, iden… |
| SA-2 | `L17:F3763@7` | ❌ error | — | — | Trace the positive late-layer contribution to the synthetic probe score upstream… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L15:F12905@13, k=15 → Emb:" only"@7 (de=5.97) +14 more |
| 2 | `get_upstream_features` | L17:F3763@7, k=15 → L15:F1990 (de=10.38) +14 more |
| 3 | `get_upstream_features` | L5:F7144@3, k=15 → L3:F16191 (de=2.97) +14 more |
| 4 | `get_upstream_features` | L2:F13565@5, k=15 → Emb:" program"@5 (de=16.75) +14 more |
| 5 | `get_upstream_features` | L4:F12847@3, k=10 → Emb:" said"@3 (de=4.41) +9 more |
| 6 | `inspect_feature` | L4, F12847 → "sentences with some reporting verb and the word 'that'" |

### Build

`build_circuit` → 10 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 13,161 | 2,384 | 42,426 | 0 | $0.0793 | — | — |
| **Total** | | **13,161** | **2,384** | **42,426** | **0** | **$0.0793** | | |

**Oracle wall-clock time:** 0m 34s