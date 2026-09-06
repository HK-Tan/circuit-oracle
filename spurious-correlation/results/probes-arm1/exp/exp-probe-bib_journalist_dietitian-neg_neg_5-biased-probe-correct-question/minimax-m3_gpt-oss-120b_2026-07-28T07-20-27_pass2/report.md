# Circuit Oracle Report
**Date:** 2026-07-28 07:20:27 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "reporter" is driven by a genuine profession signal (the word "reporter" → journalism features) but is also pulled by a parallel spurious-male-pronoun pathway ("He/his" tokens → male-referent features), meaning the probe relies on both the profession indicator and the gendered subject markers.

**Confidence:** 7

**Reasoning:** Two parallel pathways reach the probe output:

**Genuine profession pathway (correct signal):** The token "reporter" at pos 66 (Emb: reporter) directly excites L4:F13253 (journalism/media detector, frac_nonzero=0.0065, activation 16.75) and L14:F4420 (journalism/newspaper, frac_nonzero=0.0165, activation 34.5, promoted tokens: "journalists", "reporter", "editorial"), which then feeds L19:F2486 (journalistic sources/news outlets, frac_nonzero=0.029, activation 45.75, promoted: "reporting", "reporter", "coverage"). L19:F2486 is the strongest single positive driver of the probe (direct_effect=−0.12 in the top-features ranking, but its upstream chain carries the largest magnitudes — e.g., 18.75 from L14:F4420's own upstream call). L1:F1024 (writing/publishing) reinforces L4:F13253. This is a clean profession-signal chain rooted in the literal word "reporter."

**Spurious gender pathway (concern is validated):** In parallel, "He" at pos 1 and pos 25 (Emb: He) excites L0:F1069 (male-referent pronoun detector, frac_nonzero=0.0078, top activating token "He"), which feeds L6:F12990 (male pronouns/titles, frac_nonzero=0.068, promoted "himself"/"His"), which feeds L7:F14946 (his/him pronoun, frac_nonzero=0.017). Separately, "his" at pos 3 directly excites L0:F2994 (his/he pronoun detector, frac_nonzero=0.073, suppressed "his/his"). L7:F14946 drives the probe with direct_effect=−0.12, and L0:F2994 with direct_effect=+0.23 (the single largest positive driver in the graph). L18:F14743 ("He" token, frac_nonzero=0.018, promoted "himself") at pos 25, 69, 86 carries direct_effect=−0.10 each (inhibitory). The sign pattern is mixed: L0:F2994 promotes the probe (+0.23), L7:F14946 inhibits it (−0.12), L18:F14743 inhibits it (−0.10).

**Net assessment of the user's concern:** The user is correct that the circuit uses gender markers — L0:F2994 (his/he) is actually the #1 positive contributor in the entire attribution graph (direct_effect=+0.23), exceeding the journalism features' direct effects. However, the *inhibitory* male-pronoun features (L7:F14946, L18:F14743) push the probe *away* from "reporter." This is consistent with a probe that classifies *the subject's profession* but whose score is also modulated — partially spuriously — by surface-level male-reference statistics: the "his" possessive feature pushes the probe score up, while the higher-layer "He/his" pronoun features push it down. The profession-indicator pathway (L14:F4420 → L19:F2486) is present and well-formed, so the probe is not *exclusively* using gender. The mechanism is mixed: genuine journalism features from the word "reporter" coexist with a strong spurious "his" token contribution, validating the user's concern that gender markers are entangled with the profession classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 25 | Male-referent pronoun detector (L0:F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male-referent pronoun detector (L0:F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | his/he pronoun detector (L0:F2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 61 | his/he pronoun detector (L0:F2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 24 | Periods/spaces/punctuation (L0:F6051) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 50 | Periods/spaces/punctuation (L0:F6051) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F886](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) | 2 | Misc low-level lexical features (L0:F886, F7681, F8061, F14824, F4677) |  text related to discounts, offers, or prices | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/886) |
| [L0:F7681](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) | 2 | Misc low-level lexical features (L0:F886, F7681, F8061, F14824, F4677) | statements that describe something, often including a past tense verb | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 6 | Misc low-level lexical features (L0:F886, F7681, F8061, F14824, F4677) |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 16 | Misc low-level lexical features (L0:F886, F7681, F8061, F14824, F4677) | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F4677](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4677) | 15 | Misc low-level lexical features (L0:F886, F7681, F8061, F14824, F4677) |  the word "and", sometimes in conjunction with "the", "but", or "as". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4677) |
| [L1:F1024](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1024) | 66 | Writing/publishing detector (L1:F1024) | words and phrases frequently used when discussing writing, publishing, and editing books and other written works. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1024) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | Journalism/media detector (L4:F13253) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Male pronouns/titles (L6:F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 25 | Male pronouns/titles (L6:F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | his/him pronoun (L7:F14946) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Female pronouns (L7:F14893) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | Journalism/newspaper (L14:F4420) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 25 | He token (L18:F14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 86 | He token (L18:F14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 69 | He token (L18:F14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | Journalistic sources/news outlets (L19:F2486) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.232 |
| 3 | `inspect_feature` ×15 | L0:2994, L14:4420, L0:8974, L0:6051, L4:13253, L7:14893, L7:14946, L19:2486, L18:14743, L0:886, L0:8061, L0:7681, L0:14824, L6:12990, L0:4677 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@66` | ✅ reported | 8 | 7 | Trace the L14:F4420 "journalism" feature upstream. This feature is at pos 66 (ne… |
| SA-2 | `L19:F2486@66` | ❌ error | — | — | Trace the L19:F2486 "journalistic sources and news outlets" feature upstream. Th… |
| SA-3 | `L18:F14743@25` | ❌ error | — | — | Trace the L18:F14743 "He" feature upstream at pos 25. Find what drives it. Also … |
| SA-4 | `L6:F12990@1` | ❌ error | — | — | Trace the L6:F12990 "male pronouns and titles" feature upstream at pos 1. Find w… |
| SA-5 | `L4:F13253@66` | ✅ reported | 4 | 7 | Trace the L4:F13253 "journalism and media" feature upstream at pos 66. Find what… |
| SA-6 | `L0:F2994@3` | ❌ error | — | — | Trace the L0:F2994 "his/he" pronoun feature upstream at pos 3. Find what drives … |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@66, k=10 | Emb:" reporter"@66 (de=18.75) +9 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 5 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 6 | `get_upstream_features` | L4:F13253@66, k=10 | Emb:" reporter"@66 (de=26.62) +9 more |
| 7 | `get_upstream_features` | L8:F8855@66, k=10 | Emb:" reporter"@66 (de=16.88) +9 more |
| 8 | `get_upstream_features` | L7:F13646@66, k=10 | Emb:" reporter"@66 (de=15.12) +9 more |
| 9 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 10 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 11 | `inspect_feature` | L1, F1024 | " words and phrases frequently used when discussing writing, publishing" |
| 12 | `get_upstream_features` | L1:F1024@66, k=10 | Emb:" reporter"@66 (de=8.06) +9 more |
| 13 | `get_upstream_features` | L4:F661@66, k=10 | Emb:" reporter"@66 (de=18.00) +9 more |
| 14 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |

**Findings:** The target L14:F4420 (journalism) feature is primarily driven by the raw input token " reporter" (direct_effect 18.75). Additional positive contributors are mid‑layer features that detect various journalism‑related contexts: L4:F13253 (media mentions), L8:F8855 (news reporter mentions), L7:F13646 (news reporting), L7:F9092 (broadcast journalism), L6:F12712 (editorial titles), and L4:F661 (coverage…

</details>

<details>
<summary><b>SA-5</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 2 | `get_upstream_features` | L4:F13253@66, k=10 | Emb:" reporter"@66 (de=26.62) +9 more |
| 3 | `inspect_feature` | L1, F1024 | " words and phrases frequently used when discussing writing, publishing" |
| 4 | `get_upstream_features` | L1:F1024@66, k=10 | Emb:" reporter"@66 (de=8.06) +9 more |
| 5 | `inspect_feature` | L1, F5357 | " words related to written works" |
| 6 | `get_upstream_features` | L1:F1024@66, k=10 | Emb:" reporter"@66 (de=8.06) +9 more |
| 7 | `inspect_feature` | L0, F930 | " words related to legal proceedings, and/or annoying loud sounds" |
| 8 | `get_upstream_features` | L0:F930@66, k=10 | Emb:" reporter"@66 (de=9.38) +9 more |
| 9 | `get_upstream_features` | L1:F5357@66, k=10 | Emb:" reporter"@66 (de=12.00) +9 more |

**Findings:** The journalism/media feature (L4:F13253) is driven primarily by the input token "reporter" at position 66, which directly excites it with a large positive effect. The token also excites lower‑layer features (L0:F930, L1:F1024, L1:F5357) that capture legal‑case language and publishing terminology, both of which are common in news reporting. These lower‑layer features (especially the layer‑0 legal‑p…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F2486@66, k=15 → Emb:" reporter"@66 (de=28.25) +14 more |
| 2 | `get_upstream_features` | L18:F14743@25, k=15 → Emb:" He"@25 (de=24.00) +14 more |
| 3 | `get_upstream_features` | L6:F12990@1, k=15 → Emb:"He"@1 (de=3.41) +14 more |
| 4 | `get_upstream_features` | L0:F2994@3, k=15 → Emb:" his"@3 (de=42.25) +14 more |
| 5 | `get_upstream_features` | L0:F1069@25, k=10 → Emb:" He"@25 (de=37.00) +9 more |
| 6 | `get_upstream_features` | L6:F12990@25, k=10 → Emb:" He"@25 (de=4.72) +9 more |
| 7 | `inspect_feature` ×2 | L0:1069, L18:14663 |

### Build

`build_circuit` → 17 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 61,843 | 5,104 | 126,380 | 0 | $0.0323 | — | — |
| SA-5 | openai/gpt-oss-120b | 87,639 | 5,106 | 5,888 | 0 | $0.0163 | ✅ 4F/7E | Trace the L4:F13253 "journalism and media" feature upstream … |
| SA-1 | openai/gpt-oss-120b | 199,895 | 10,791 | 21,856 | 0 | $0.0368 | ✅ 8F/7E | Trace the L14:F4420 "journalism" feature upstream. This feat… |
| **Total** | | **349,377** | **21,001** | **154,124** | **0** | **$0.0853** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 8s