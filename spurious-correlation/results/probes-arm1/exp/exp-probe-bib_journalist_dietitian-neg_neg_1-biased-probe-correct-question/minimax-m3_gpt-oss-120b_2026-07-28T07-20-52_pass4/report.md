# Circuit Oracle Report
**Date:** 2026-07-28 07:20:52 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit has been built. I have enough information for the final analysis.

**Analysis:** The probe's "journalist/reporter" classification is driven by a **mixture of two co-active pathways**: a genuine profession-signal pathway anchored on the word "report" (pos 21), and a much larger spurious gender-pronoun pathway anchored on the possessive "His" (pos 1) and objective "him" (pos 9). The gender pathway quantitatively dominates.

**Confidence:** 7

**Reasoning:**

**Pathway 1 — Genuine profession signal (pos 21, the word "report"):**
A coherent chain of journalism-specific transcoder features fires at the "report" token and propagates up:
- L7:F13646 ("news reporting and journalism", promoted: ▁reporter, ▁journalist, frac_nonzero=0.0076)
- L7:F9092 ("broadcast journalism", frac_nonzero=0.0095)
- L8:F8855 ("mentions of news reporters and news reporting", promoted: ▁reporter, ▁journalist, frac_nonzero=0.0085)
- L8:F8437 (film/documentary context, promoted: ▁journalistic)
- L11:F5996 ("references to news publications and their staff", frac_nonzero=0.002)
- L14:F4420 ("words and phrases related to journalism and newspapers", promoted: ▁journalists, ▁journalism, ▁reporter, frac_nonzero=0.0165)

These are low-frac_nonzero, highly specific profession-anchor features. They promote the journalist/reporter vocabulary and fire on the *content* of the sentence ("report for some of the top news organizations"). The L14:F4420 feature pushes the probe with direct_effect = −0.159, but its upstream path is well-grounded in the "report" token embedding.

**Pathway 2 — Spurious gender signal (pos 1 "His" / pos 9 "him"):**
The dominant signal comes from masculine-pronoun features at the start of the sentence:
- L0:F2994 (label: "the pronoun 'his' and the pronoun 'he'", frac_nonzero=0.073, direct_effect +0.285 at pos 1, +0.114 at pos 9)
- L2:F9301 ("mentions of men and women in relationships/dating…", direct_effect −0.108)
- L4:F4315 ("mentions of 'his' and other associated pronouns", direct_effect −0.182)
- L6:F12990 ("male pronouns and titles along with descriptors associated with men", direct_effect −0.297)
- L7:F14893 (pronouns, promoted: ▁herself, ▁elle, ▁she — *opposite-gender*, direct_effect +0.471)
- L7:F14946 ("the possessive pronoun 'his'", direct_effect −0.467)
- L18:L14743 ("He", direct_effect −0.187 at pos 9)
- L18:L10315 (pronouns, direct_effect −0.162 at pos 1)
- L18:L7400 (oddly labeled "coding/UI" but promoted: ▁himself, ▁his — actually a his-promoter, direct_effect −0.155)
- L19:L8814 ("various pronouns and names referring to people", promoted: ▁she/▁her, direct_effect +0.232)

Critically, all upstream traces of L7:F14893 and L0:F2994 reach the "His" token embedding (pos 1) with direct_effect = 23.5 and 19.75 respectively — the largest single-edge contributions in the entire circuit. The "him" at pos 9 also feeds L0:F2994 with direct_effect = 13.94. The "report" embedding only contributes 5.2–12.1 to the journalism path.

**Interpretation of the user's concern:** The concern is **substantiated but with nuance**. The circuit *does* contain genuine profession indicators (L7–L14 journalism features anchored on "report"). However, the probe's score is *additionally and largely* driven by a co-active masculine-pronoun pathway whose inputs are the gendered possessive "His" (pos 1) and the masculine pronoun "him" (pos 9). Multiple late-layer pronoun features (L18, L19) carry large direct_effects and they fire specifically because the subject of the biographical sentence is referred to with masculine pronouns. The two pathways are roughly balanced in feature count, but the gender-pathway's early-layer edges from the "His"/"him" embeddings are the largest in the graph (23.5, 19.75, 13.94). This means the probe is partly using "the subject is male" as evidence for "the subject is a journalist" — a clear spurious-correlation shortcut. The model has not been forced to choose between the pathways: both run in parallel, and the journalist/reporter classification receives votes from both genuine profession semantics (the journalism features anchored on "report") and from the gender-pronoun statistics. A debiased probe would need to verify that the journalism path alone is sufficient, and indeed L14:F4420's upstream chain is fully grounded in the "report" token — so the profession signal *can* stand on its own, but in this graph it is entangled with a powerful male-pronoun co-feature.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification (journalist/reporter) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Mid-layer: journalism/reporter context (genuine profession signal) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Mid-layer: journalism/reporter context (genuine profession signal) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | Mid-layer: journalism/reporter context (genuine profession signal) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 21 | Mid-layer: journalism/reporter context (genuine profession signal) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | Mid-layer: journalism/reporter context (genuine profession signal) | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L11:F5996](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) | 21 | Mid-layer: journalism/reporter context (genuine profession signal) |  references to news publications and their staff. | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/5996) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Mid-layer: masculine-pronoun features (gender/spurious signal) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Mid-layer: masculine-pronoun features (gender/spurious signal) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Mid-layer: masculine-pronoun features (gender/spurious signal) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Mid-layer: masculine-pronoun features (gender/spurious signal) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | Mid-layer: masculine-pronoun features (gender/spurious signal) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Mid-layer: masculine-pronoun features (gender/spurious signal) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Mid-layer: masculine-pronoun features (gender/spurious signal) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Mid-layer: masculine-pronoun features (gender/spurious signal) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | Mid-layer: masculine-pronoun features (gender/spurious signal) |  all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Early-layer lexical features at pos 1 (His) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 9 | Early-layer lexical features at pos 1 (His) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | Early-layer lexical features at pos 1 (His) |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | Early-layer lexical features at pos 1 (His) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F7927](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) | 8 | Early-layer lexical features at pos 1 (His) |  past-participle verbs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7927) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: His (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: him (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: report (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.471 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace this feature upstream. What does it encode? Does it relate to profession/j… |
| SA-2 | `L0:F2994@1` | ❌ error | — | — | Trace this feature upstream. What does it encode? Is it a gender marker, profess… |
| SA-3 | `L19:F8814@1` | ❌ error | — | — | Trace this feature upstream. What does it encode? Profession context or gender/s… |
| SA-4 | `L0:F2994@9` | ❌ error | — | — | Trace this feature from pos 9 upstream. What does it encode at that position? To… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×14 | L7:14893, L0:2994, L19:8814, L7:14946, L6:12990, L18:14743, L18:10315, L14:4420, L18:7400, L4:4315, L0:2011, L0:8444, L0:7927, L2:9301 |
| 2 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 3 | `get_upstream_features` | L0:F2994@1, k=10 → Emb:"His"@1 (de=19.75) +9 more |
| 4 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (de=9.31) +9 more |
| 5 | `get_upstream_features` | L0:F2994@9, k=10 → Emb:" him"@9 (de=13.94) +9 more |
| 6 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 7 | `inspect_feature` ×5 | L8:8855, L7:13646, L8:8437, L7:9092, L11:5996 |
| 8 | `get_upstream_features` | L8:F8855@21, k=10 → Emb:" report"@21 (de=12.06) +9 more |
| 9 | `get_upstream_features` | L7:F14893@9, k=10 → Emb:" him"@9 (de=9.75) +9 more |

### Build

`build_circuit` → 7 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 45,753 | 4,468 | 123,428 | 0 | $0.0265 | — | — |
| **Total** | | **45,753** | **4,468** | **123,428** | **0** | **$0.0265** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 58s