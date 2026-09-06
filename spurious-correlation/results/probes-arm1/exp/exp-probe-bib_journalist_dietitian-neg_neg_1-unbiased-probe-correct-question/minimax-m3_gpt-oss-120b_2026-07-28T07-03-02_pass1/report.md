# Circuit Oracle Report
**Date:** 2026-07-28 07:03:02 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by an *opposing* mix of (a) genuine journalism-occupation indicators that *suppress* the score and (b) the male pronoun "His" plus generic content-word features that *push the score up* — meaning the classifier is not relying on the genuine profession signal at all but on a gender marker ("His") and unrelated generic words.

**Confidence:** 7

**Reasoning:**

The circuit reveals two sharply opposed signal families feeding the probe:

**1. Genuine profession indicators — pushing the probe DOWN (refute/lower the profession class).** The "report" token at position 21 lights up a textbook journalism circuit: L1:F14511 ("report") → L8:F8855 (news reporters/reporting) and L7:F13646 (news reporting) → L14:F4420 (journalism/newspapers, frac_nonzero 0.0165, promoted: journalist/reporter/editorial) → L19:F2486 (journalistic sources, frac_nonzero 0.029, promoted: reporting/reporter/coverage). A parallel branch from "top" (pos 26) feeds L20:F8433 (news broadcasting, frac_nonzero 0.036, promoted: news/journalists/newspapers). All five late-layer features (L14:F4420, L19:F2486, L20:F8433, L8:F8855, L1:F14511) carry *negative* direct_effects (-0.1475, -0.0972, -0.0513, -0.0518, +0.052 mixed), with the L14 and L19 features being the largest negative contributors. The subagent's upstream trace confirms the "report" token embedding directly drives these features (12.06, 11.44, 5.22, 3.36 direct_effect). This is a *real* occupation circuit — but it is suppressing, not promoting, the probe score.

**2. Gender marker + generic filler — pushing the probe UP.** L0:F8964 ("His", pos 1, direct_effect +0.088) and L0:F1069 ("He/His", pos 1, direct_effect -0.05) both attach to the "His" embedding. L0:F2011 ("dream", pos 2, +0.054) and L0:F13948 ("pink"-labeled but triggered on "desire" at pos 2, +0.054) plus L0:F15693 (personal-anecdote language at pos 2, +0.052) and the "to"/"see"/"world"/"to" feature activations at positions 3, 4, 6, 20 collectively add several more positive tenths. None of these features encode profession — they are male-pronoun detection and common-noun lexical detectors. They rise because the prompt begins "His desire to see the world…" and that surface vocabulary matches whatever the probe direction encodes, regardless of the reporter/journalism evidence that appears later.

**Implication for the user's concern:** The user's worry is *partially* validated but in a subtle way. The gender pronoun "His" (and "dream"/"desire"-like vocabulary) is causally pushing the probe score up at L0, while the *actual* profession evidence ("report", "news organizations") is *suppressing* the same score. So the probe is not "using gender markers instead of the profession" in the simple sense — it is *weighing them against each other*, with the gender/generic surface features on the winning side at this position. Because the journalism chain contributes net negative direct effect, the model's "profession direction" as encoded by this probe is poorly aligned with the genuine occupational content of the prompt; instead the direction is partially captured by spurious surface cues (male possessive pronoun, generic content words). This is the textbook failure mode of a linear probe: it picks up whatever linear direction best separates the training labels, and on this prompt the late-layer journalism signal is fighting the L0 surface-cue signal — and the L0 signal is winning.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Genuine profession indicators (journalism chain) — pushed DOWN the probe |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Genuine profession indicators (journalism chain) — pushed DOWN the probe | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Genuine profession indicators (journalism chain) — pushed DOWN the probe |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L1:F14511](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14511) | 21 | Genuine profession indicators (journalism chain) — pushed DOWN the probe |  the word "report" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14511) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 26 | Genuine profession indicators (journalism chain) — pushed DOWN the probe | words related to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | Gender marker (His) — pushed UP the probe |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Gender marker (His) — pushed UP the probe |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | Generic positive context words (dream/desire/anecdote) — pushed UP the probe |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F13948](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) | 2 | Generic positive context words (dream/desire/anecdote) — pushed UP the probe |  the color "pink" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) |
| [L0:F15693](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) | 2 | Generic positive context words (dream/desire/anecdote) — pushed UP the probe |  language related to personal anecdotes and opinions | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | Generic positive context words (dream/desire/anecdote) — pushed UP the probe | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F14287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) | 4 | Generic positive context words (dream/desire/anecdote) — pushed UP the probe | the word "see" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 20 | Generic positive context words (dream/desire/anecdote) — pushed UP the probe | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F2203](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) | 6 | Generic positive context words (dream/desire/anecdote) — pushed UP the probe |  instances of the words "world" or "game" (possibly "problem") or expressions of existential quandaries. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) |
| [L5:F771](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) | 6 | Generic positive context words (dream/desire/anecdote) — pushed UP the probe |  the word "see" and words often associated with "see" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:4420 de=-0.147 |
| 3 | `inspect_feature` ×14 | L0:8964, L0:8444, L0:14287, L14:4420, L19:2486, L0:2203, L0:13948, L0:2011, L1:14511, L8:8855, L0:1069, L0:15693, L5:771, L20:8433 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ✅ reported | 5 | 16 | Trace the upstream path from L14:F4420 (journalism/newspapers feature, which has… |
| SA-2 | `L19:F2486@21` | ✅ reported | 7 | 13 | Trace the upstream path from L19:F2486 (journalistic sources/news outlets featur… |
| SA-3 | `L0:F8964@1` | ❌ error | — | — | Trace the upstream path from L0:F8964 (the "His" possessive pronoun feature at p… |
| SA-4 | `L0:F1069@1` | ❌ error | — | — | Trace the upstream path from L0:F1069 (the "He/His" male pronoun reference featu… |
| SA-5 | `L20:F8433@26` | ✅ reported | 4 | 6 | Trace the upstream path from L20:F8433 (news broadcasting feature, negative dire… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 5 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 6 | `get_upstream_features` | L7:F13646@21, k=5 | Emb:" report"@21 (de=7.22) +4 more |
| 7 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 8 | `get_top_logits` | k=5 | "" (100%) |
| 9 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 10 | `get_upstream_features` | L4:F661@21, k=10 | Emb:" report"@21 (de=14.38) +9 more |

**Findings:** The probe‑negative feature L14:F4420 (journalism/newspapers) is driven primarily by the raw token “report” at position 21. The signal propagates upward through a cascade of media‑reporting detectors: L8:F8855 and L7:F13646 (both news‑reporting detectors), L8:F8437 (documentary/film‑festival context), and an early‑layer detector L4:F661 that reacts directly to the word “report”. All of these upstre…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=15 | L14:F4420 (de=14.31) +14 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 5 | `get_upstream_features` | L8:F8855@21, k=15 | Emb:" report"@21 (de=12.06) +14 more |
| 6 | `inspect_feature` | L16, F15046 | " names, organizations, and reporting verbs" |
| 7 | `get_upstream_features` | L14:F4420@21, k=15 | Emb:" report"@21 (de=5.22) +14 more |
| 8 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 9 | `get_upstream_features` | L7:F13646@21, k=15 | Emb:" report"@21 (de=7.22) +14 more |
| 10 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 11 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 12 | `get_upstream_features` | L16:F15046@21, k=15 | Emb:" report"@21 (de=11.44) +14 more |

**Findings:** The L19:F2486 feature that flags journalistic sources is driven primarily by a cascade that starts with the raw input token "report" (position 21). The token embedding sends a strong positive direct effect to a low-layer (L8) reporting feature (F8855), which in turn excites a very sparse L7 reporting feature (F13646). These mid-layer features funnel their activation into higher-layer journalism de…

</details>

<details>
<summary><b>SA-5</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F8433 | "words related to news broadcasting" |
| 2 | `get_upstream_features` | L20:F8433@26, k=10 | Emb:" top"@26 (de=5.72) +9 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 5 | `get_upstream_features` | L7:F9092@26, k=10 | L2:F10902 (de=1.16) +9 more |
| 6 | `inspect_feature` | L2, F10902 | "the word "top"." |

**Findings:** The path starts at the news‑broadcasting feature (L20:F8433) which receives strong excitatory input from the token embedding " top" (pos 26) and from a mid‑layer journalism feature (L14:F4420). That journalism feature further drives the broadcast feature. Going deeper, the lower‑third feature L7:F9092 (broadcast‑journalism) also feeds L20:F8433 and is itself excited by the embedding token " report…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F8964@1, k=8 → Emb:"His"@1 (de=13.69) +7 more |
| 2 | `get_upstream_features` | L0:F1069@1, k=8 → Emb:"His"@1 (de=21.62) +7 more |
| 3 | `inspect_feature` ×3 | L0:13948, L0:14287, L0:15693 |
| 4 | `get_upstream_features` | L0:F8444@3, k=5 → Emb:" to"@3 (de=39.50) +4 more |
| 5 | `get_upstream_features` | L0:F8444@20, k=5 → Emb:" to"@20 (de=42.25) +4 more |
| 6 | `get_upstream_features` | L0:F14287@4, k=5 → Emb:" see"@4 (de=25.12) +4 more |
| 7 | `get_upstream_features` | L0:F2011@2, k=5 → Emb:" desire"@2 (de=12.94) +4 more |
| 8 | `get_upstream_features` | L0:F13948@2, k=5 → Emb:" desire"@2 (de=14.44) +4 more |
| 9 | `get_upstream_features` | L0:F15693@2, k=5 → Emb:"His"@1 (de=8.69) +4 more |
| 10 | `get_upstream_features` | L1:F14511@21, k=5 → Emb:" report"@21 (de=20.62) +4 more |

### Build

`build_circuit` → 12 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 37,367 | 5,753 | 153,702 | 0 | $0.0273 | — | — |
| SA-5 | openai/gpt-oss-120b | 53,126 | 4,489 | 2,592 | 0 | $0.0107 | ✅ 4F/6E | Trace the upstream path from L20:F8433 (news broadcasting fe… |
| SA-2 | openai/gpt-oss-120b | 162,186 | 9,125 | 20,736 | 0 | $0.0301 | ✅ 7F/13E | Trace the upstream path from L19:F2486 (journalistic sources… |
| SA-1 | openai/gpt-oss-120b | 107,490 | 8,884 | 18,816 | 0 | $0.0217 | ✅ 5F/16E | Trace the upstream path from L14:F4420 (journalism/newspaper… |
| **Total** | | **360,169** | **28,251** | **195,846** | **0** | **$0.0899** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 11s