# Circuit Oracle Report
**Date:** 2026-07-28 07:20:05 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven almost entirely by a *legitimate profession indicator* (the journalism-related meaning of the word "report") plus a *gender confounder* (the pronoun "His" / "he"), with the journalism channel dominating and the gender channel contributing a smaller spurious positive push.

**Confidence:** 7

**Reasoning:** The late-layer features that feed the output (L19:F2486 "journalistic sources and news outlets", L14:F4420 "journalism and newspapers", L20:F8433 "news broadcasting", L19:F14973) are all *profession-true* journalism detectors, not gendered artifacts. Tracing L19:F2486 upstream shows it is excited at multiple positions (21, 22, 26–30) almost entirely by the **raw embedding of the token "report" at pos 21** (direct_effect ≈ +5.22 into L14:F4420 and +3.36 into L19:F2486), with intermediate journalism features (L8:F8855 "reporter mentions", L7:F13646 "news reporting", L16:F15046 "names/orgs/reporting verbs") sitting between the embedding and the late-layer nodes. The token "report" is genuinely the strongest and most profession-specific lexical cue in the prompt — the sentence says "...report for some of the top news organizations", and "report" → journalism is a clean, *causal* profession signal, not a confound.

However, **the user's concern is partially confirmed at the very bottom of the circuit**. L0:F8964 ("the possessive pronoun 'His'", pos 1, direct_effect +0.088) and L0:F1069 ("references to a male person, particularly the pronoun 'He' or 'His'", pos 1, direct_effect −0.050) — explicitly gendered/pronoun detectors — appear in the top-20 features driving the probe. The L0-gender supernode also includes generic-function-word features ("see" L0:F14287, "to" L0:F8444, "world" L0:F2203, "dream" L0:F2011, "pink" L0:F13948, "experience" L0:F15693) at unrelated positions 2–6 that have no semantic connection to journalism — they are presumably co-firing in the residual stream and their decoder weights happen to project onto the probe direction. The net gender contribution is small and mixed in sign (F8964 is positive, F1069 is negative), so it does not strongly skew the probe, but it is a genuine spurious channel.

Net assessment: the probe's classification is *primarily* a true profession signal (the "report for top news organizations" cluster), and the gender-pronoun contribution is real but secondary and largely cancelling. The "His" pronoun nudges the score slightly positively while "He/His" as a generic male reference slightly inhibits it, so there is a small spurious gender leak in the input-level features but it is dominated by the journalism evidence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | Early layer features (L0-1): His/He pronouns, 'see', 'to', generic article words |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Early layer features (L0-1): His/He pronouns, 'see', 'to', generic article words |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F14287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) | 4 | Early layer features (L0-1): His/He pronouns, 'see', 'to', generic article words | the word "see" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | Early layer features (L0-1): His/He pronouns, 'see', 'to', generic article words | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 20 | Early layer features (L0-1): His/He pronouns, 'see', 'to', generic article words | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | Early layer features (L0-1): His/He pronouns, 'see', 'to', generic article words |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F13948](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) | 2 | Early layer features (L0-1): His/He pronouns, 'see', 'to', generic article words |  the color "pink" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) |
| [L0:F15693](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) | 2 | Early layer features (L0-1): His/He pronouns, 'see', 'to', generic article words |  language related to personal anecdotes and opinions | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) |
| [L0:F2203](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) | 6 | Early layer features (L0-1): His/He pronouns, 'see', 'to', generic article words |  instances of the words "world" or "game" (possibly "problem") or expressions of existential quandaries. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) |
| [L1:F14511](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14511) | 21 | Early layer features (L0-1): His/He pronouns, 'see', 'to', generic article words |  the word "report" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14511) |
| [L2:F10902](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10902) | 26 | Word 'top' (L2) | the word "top". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10902) |
| [L5:F771](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) | 6 | Word 'see' (L5) |  the word "see" and words often associated with "see" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 21 | Editor/publisher titles (L6) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | News reporting / journalism (L7) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 26 | News reporting / journalism (L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Reporter mentions / news writing (L8) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | Reporter mentions / news writing (L8) | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Journalism/newspaper vocabulary (L14) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F2781](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2781) | 26 | Journalism/newspaper vocabulary (L14) |  words that describe degrees of importance or influence, especially in professional settings | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2781) |
| [L16:F15046](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15046) | 21 | Names, orgs, reporting verbs (L16) |  names, organizations, and reporting verbs | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15046) |
| [L17:F11691](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11691) | 26 | Prepositions/possessives in complex sentences (L17) | prepositions and possessive pronouns in long, complex sentences, especially when discussing legal matters, company specifics, or sports | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11691) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Journalism news-outlets cluster (L19) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 22 | Journalism news-outlets cluster (L19) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 27 | Journalism news-outlets cluster (L19) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2483](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2483) | 28 | Journalism news-outlets cluster (L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2483) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 29 | Journalism news-outlets cluster (L19) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 30 | Journalism news-outlets cluster (L19) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 26 | Journalism news-outlets cluster (L19) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F14973](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/14973) | 26 | Journalism news-outlets cluster (L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/14973) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 26 | News broadcasting (L20) | words related to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:4420 de=-0.147 |
| 3 | `inspect_feature` ×14 | L14:4420, L19:2486, L0:8964, L0:8444, L0:14287, L0:2203, L0:13948, L0:2011, L0:15693, L0:1069, L1:14511, L8:8855, L20:8433, L5:771 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F2486@21` | ✅ reported | 5 | 10 | Trace the path from L19:F2486 (journalistic sources/news outlets) upstream. What… |
| SA-2 | `L14:F4420@21` | ✅ reported | 4 | 5 | Trace the path from L14:F4420 (journalism/newspaper words) upstream. What tokens… |
| SA-3 | `L0:F8964@1` | ❌ error | — | — | Trace L0:F8964 (possessive pronoun 'His') upstream at position 1. What other fea… |
| SA-4 | `L0:F1069@1` | ❌ error | — | — | Trace L0:F1069 (references to male person / He/His) upstream at position 1. What… |
| SA-5 | `L20:F8433@26` | ❌ error | — | — | Trace L20:F8433 (news broadcasting) upstream at position 26. What feeds it? |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=10 | L14:F4420 (de=14.31) +9 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |

**Findings:** The journalism‑related feature L19:F2486 is driven primarily by the token embedding for the word "report" at position 21. This embedding excites a cascade of lower‑layer features: an early news‑reporting detector (L7:13646), a more specific reporter‑mention detector (L8:8855), and a mid‑layer journalism‑vocabulary detector (L14:4420). These in turn strongly activate the target L19 feature. The pat…

</details>

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 5 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 6 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |

**Findings:** The L14 journalism feature (F4420) is primarily driven by the raw token embedding for "report" at position 21. This token directly contributes a large positive effect (5.22) and also strongly excites an intermediate L8 feature (8855) that detects mentions of reporters and reporting (+12.06). The L8 feature pushes the L14 node. A parallel L7 feature (13646) representing generic news reporting also …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L20:F8433@26, k=10 → Emb:" top"@26 (de=5.72) +9 more |
| 2 | `inspect_feature` ×3 | L16:15046, L7:13646, L8:8437 |
| 3 | `get_upstream_features` | L17:F5218@26, k=10 → Emb:" report"@21 (de=2.09) +9 more |
| 4 | `get_upstream_features` | L7:F9092@26, k=10 → L2:F10902 (de=1.16) +9 more |
| 5 | `get_upstream_features` | L19:F14973@26, k=10 → Emb:" top"@26 (de=7.22) +9 more |
| 6 | `inspect_feature` ×4 | L17:11691, L14:2781, L2:10902, L6:12712 |

### Build

`build_circuit` → 16 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 42,915 | 7,940 | 273,824 | 0 | $0.0388 | — | — |
| SA-1 | openai/gpt-oss-120b | 51,837 | 3,689 | 2,624 | 0 | $0.0100 | ✅ 5F/10E | Trace the path from L19:F2486 (journalistic sources/news out… |
| SA-2 | openai/gpt-oss-120b | 64,913 | 4,392 | 0 | 0 | $0.0124 | ✅ 4F/5E | Trace the path from L14:F4420 (journalism/newspaper words) u… |
| **Total** | | **159,665** | **16,021** | **276,448** | **0** | **$0.0612** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 47s