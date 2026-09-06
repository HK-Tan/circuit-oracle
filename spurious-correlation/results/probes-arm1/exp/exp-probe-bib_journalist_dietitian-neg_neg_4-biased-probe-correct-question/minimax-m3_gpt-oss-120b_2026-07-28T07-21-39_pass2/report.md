# Circuit Oracle Report
**Date:** 2026-07-28 07:21:39 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession classification is driven by a mix of legitimate journalism-related lexical signals and spurious male-pronoun/gender features, confirming the user's concern about spurious features.

**Confidence:** 7

**Reasoning:** The circuit shows two parallel paths converging on the probe direction. The **legitimate path** is anchored on the input token " writer" (Emb: writer at pos 28, direct_effect=5.75) and " freelance" (pos 27, direct_effect=2.69) feeding mid-layer journalism features: L4:F13253 ("journalism and the media", frac_nonzero=0.0065), L7:F72 ("words related to writing professionally", frac_nonzero=0.011), L7:F13646 ("news reporting and journalism"), and L8:F8855 ("mentions of news reporters"), which converge on L14:F4420 ("words and phrases related to journalism and newspapers", frac_nonzero=0.0165). These are topically appropriate profession cues.

However, the circuit also contains a **prominent spurious gender path** anchored on the token " he" (Emb: he at pos 22, direct_effect=28.6 into L18:F14743, and direct_effect=14.2 into L7:F14946). This activates a cascade of male-pronoun/gender features: L0:F12768 ("mentions of 'he' and 'she'"), L2:F11473 ("instances of 'he' and government/law"), L4:F14796 ("the pronoun 'he' or 'him'"), L4:F15567 ("sentences with male or female pronouns…especially ones referring to writing"), L6:F12990 ("male pronouns and titles along with descriptors associated with men", frac_nonzero=0.068 — relatively high), L13:F1937 ("pronouns used to describe people"), L14:F14097 ("occurrences of the word 'he'"), L15:F10510 ("references to males in third person"), L17:F5889 ("references to people with pronouns"), and finally L18:F14743 ("He", which fires at positions 22, 39, and 67 — i.e., every male pronoun in the prompt). Notably, L18:F14743 is the largest direct driver on the top-features list, with absolute direct_effect ~0.10-0.16 at each of three positions, while L14:F14097 also has direct_effect=-0.09 and L6:F12990 has direct_effect=-0.07.

The user's concern is validated: the probe direction reads heavily on **gendered pronoun features** (L18 "He", L14 "he", L7 "his", L6 "male pronouns and titles") alongside genuine journalism features. Since the subject happens to be male and the text is biography-style ("he has written for the Guardian…he has also been b…"), the model's profession classification conflates the consistent use of male pronouns with profession identification. Features like L6:F12990 with its relatively high frac_nonzero (0.068) and explicit label "male pronouns and titles along with descriptors associated with men" are not encoding profession at all — they encode gender, which is a spurious correlate in this biography domain.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output Logit (Probe direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | Late-layer profession-related features (L18 pronoun aggregator + L14 journalism/pronoun) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 39 | Late-layer profession-related features (L18 pronoun aggregator + L14 journalism/pronoun) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 67 | Late-layer profession-related features (L18 pronoun aggregator + L14 journalism/pronoun) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 22 | Late-layer profession-related features (L18 pronoun aggregator + L14 journalism/pronoun) |  occurrences of the word "he" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 22 | Late-layer profession-related features (L18 pronoun aggregator + L14 journalism/pronoun) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 22 | Late-layer profession-related features (L18 pronoun aggregator + L14 journalism/pronoun) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | Late-layer profession-related features (L18 pronoun aggregator + L14 journalism/pronoun) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L13:F1937](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/1937) | 22 | Mid-layer pronoun aggregators (L13/L17) |  pronouns used to describe people, including possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/1937) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 22 | Mid-layer pronoun aggregators (L13/L17) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F10510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10510) | 22 | Mid-layer pronoun aggregators (L13/L17) |  references to males in third person and first person pronouns | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10510) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 28 | Mid-layer journalism features (L4-L8) | mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | Mid-layer journalism features (L4-L8) | things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L7:F72](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/72) | 28 | Mid-layer journalism features (L4-L8) | words related to writing professionally | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/72) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 28 | Mid-layer journalism features (L4-L8) | news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L1:F15416](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15416) | 28 | Mid-layer journalism features (L4-L8) | the word "writers" or "writer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15416) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 22 | Low-layer pronoun detectors (L0-L4) | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 22 | Low-layer pronoun detectors (L0-L4) | the pronoun "he" or "him" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L2:F11473](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11473) | 22 | Low-layer pronoun detectors (L0-L4) |  instances of the word 'he' and words related to government and law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11473) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Low-layer pronoun detectors (L0-L4) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L1:F15323](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) | 1 | Low-layer lexical features at the writer/institute positions | the word "starting" in academic papers | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) |
| [L0:F5288](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5288) | 6 | Low-layer lexical features at the writer/institute positions |  the word "service" and related terms in different contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5288) |
| [L1:F4459](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) | 7 | Low-layer lexical features at the writer/institute positions |  mentions of research institutes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) |
| [L0:F7124](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) | 2 | Low-layer lexical features at the writer/institute positions | the word "at" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) |
| [L0:F15661](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) | 7 | Low-layer lexical features at the writer/institute positions | the word "spin" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Low-layer lexical features at the writer/institute positions | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F6556](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6556) | 1 | Low-layer lexical features at the writer/institute positions |  instances of the word "closing" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6556) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 11 | Low-layer lexical features at the writer/institute positions |  commas and sometimes reach (context not clear) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 38 | Low-layer lexical features at the writer/institute positions | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L2:F9293](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9293) | 12 | Low-layer lexical features at the writer/institute positions |  the word "cover" used in different contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9293) |
| [L1:F15063](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15063) | 5 | Low-layer lexical features at the writer/institute positions | mentions of the United States | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15063) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: he (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 28 | Emb: writer (pos 28) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: freelance (pos 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Starting (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: Services (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: United (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:7124 de=-0.160 |
| 3 | `inspect_feature` ×18 | L1:15323, L0:7124, L18:14743, L0:15661, L0:3820, L0:6556, L14:14097, L1:4459, L0:4870, L0:5288, L0:6051, L7:14946, L0:12768, L2:9293, L1:15063, L6:12990, L14:4420, L1:15416 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14743@22` | ❌ error | — | — | Trace upstream from L18:F14743 ("He" pronoun feature) at position 22. Identify w… |
| SA-2 | `L14:F14097@22` | ✅ reported | 6 | 6 | Trace upstream from L14:F14097 ("he" pronoun feature) at position 22. Identify w… |
| SA-3 | `L14:F4420@28` | ✅ reported | 5 | 15 | Trace upstream from L14:F4420 (journalism/newspapers feature) at position 28. Id… |
| SA-4 | `L1:F15416@28` | ✅ reported | 4 | 3 | Trace upstream from L1:F15416 ("writers/writer" feature) at position 28. Identif… |
| SA-5 | `L6:F12990@22` | ❌ error | — | — | Trace upstream from L6:F12990 (male pronouns and titles) at position 22. Confirm… |
| SA-6 | `L7:F14946@22` | ❌ error | — | — | Trace upstream from L7:F14946 (his/possessive pronoun) at position 22. Confirm t… |

<details>
<summary><b>SA-2</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F14097 | " occurrences of the word "he"" |
| 2 | `get_upstream_features` | L14:F14097@22, k=10 | Emb:" he"@22 (de=2.70) +9 more |
| 3 | `inspect_feature` | L13, F1937 | " pronouns used to describe people, including possessive pronouns" |
| 4 | `get_upstream_features` | L13:F1937@22, k=10 | Emb:" he"@22 (de=8.94) +9 more |
| 5 | `inspect_feature` | L4, F15567 | "sentences with male or female pronouns and possessives, especially one" |
| 6 | `get_upstream_features` | L4:F15567@22, k=10 | Emb:" he"@22 (de=17.75) +9 more |
| 7 | `inspect_feature` | L3, F9548 | " uses of the word "this" followed by a pause or conjunction, sometimes" |
| 8 | `inspect_feature` | L6, F6622 | " pronouns and possessive pronouns in the context of legal and athletic" |
| 9 | `inspect_feature` | L2, F9233 | " the pronouns "she" and "he"" |
| 10 | `get_upstream_features` | L3:F9548@22, k=10 | Emb:" he"@22 (de=10.31) +9 more |
| 11 | `get_upstream_features` | L6:F6622@22, k=10 | Emb:" he"@22 (de=6.88) +9 more |
| 12 | `get_upstream_features` | L2:F9233@22, k=10 | Emb:" he"@22 (de=11.00) +9 more |
| 13 | `inspect_feature` | L0, F12768 | " mentions of "he" and "she" in close proximity" |
| 14 | `inspect_feature` | L1, F2848 | " the pronouns "she" and "her" (and sometimes "his")" |
| 15 | `inspect_feature` | L2, F5925 | "verbs ending in "ing"" |

**Findings:** The male pronoun feature L14:F14097 is built from a hierarchy of upstream pronoun detectors. At the bottom, a layer‑0 feature (F12768) directly reacts to the raw token embedding of "he". This signal is propagated to a layer‑2 gender‑pronoun grouping feature (F11473), then to a layer‑3 discourse‑marker feature (F9548) that amplifies pronoun presence in context. The signal continues to a layer‑4 sen…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@28, k=10 | Emb:" writer"@28 (de=5.75) +9 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `get_upstream_features` | L8:F8855@28, k=10 | Emb:" writer"@28 (de=4.72) +9 more |
| 5 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 6 | `inspect_feature` | L7, F72 | " words related to writing professionally" |
| 7 | `get_upstream_features` | L4:F13253@28, k=10 | Emb:" writer"@28 (de=9.12) +9 more |
| 8 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 9 | `get_upstream_features` | L7:F72@28, k=10 | Emb:" writer"@28 (de=5.72) +9 more |
| 10 | `get_upstream_features` | L7:F72@28, k=10 | Emb:" writer"@28 (de=5.72) +9 more |

**Findings:** The profession signal for a journalist originates from the input token "writer" (and to a lesser extent "freelance") at position 28. That token directly excites a low‑layer media feature (layer 4) and a mid‑layer reporter feature (layer 8), which in turn feed the higher‑layer journalism feature (L14:F4420). The path therefore consists of an early lexical cue (embedding) feeding a cascade of increa…

</details>

<details>
<summary><b>SA-4</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F15416 | "the word "writers" or "writer"" |
| 2 | `get_upstream_features` | L1:F15416@28, k=10 | Emb:" writer"@28 (de=19.75) +9 more |
| 3 | `inspect_feature` | L0, F7376 | " references to writers or writing" |
| 4 | `get_upstream_features` | L0:F7376@28, k=10 | Emb:" writer"@28 (de=19.88) +9 more |
| 5 | `inspect_feature` | L0, F16167 | " the word "wire" and related words in the context of electronics" |
| 6 | `inspect_feature` | L0, F4328 | "references to consciousness, or lack thereof" |
| 7 | `get_upstream_features` | L0:F16167@28, k=10 | Emb:" writer"@28 (de=10.00) +9 more |

**Findings:** The writer signal at L1:F15416 originates almost entirely from the raw input token embedding " writer" at position 28 (direct_effect ≈ 19.7). This embedding feeds a dedicated layer‑0 feature (0:7376) that specializes in detecting references to writers/writing; this feature contributes the bulk of the positive influence (≈ 1.14) to the L1 writer feature. Two additional low‑level features (0:16167 a…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F15323@1, k=10 → Emb:"Starting"@1 (de=16.38) +9 more |
| 2 | `get_upstream_features` | L0:F5288@6, k=10 → Emb:" Services"@6 (de=14.19) +9 more |
| 3 | `get_upstream_features` | L6:F12990@22, k=10 → Emb:" he"@22 (de=6.50) +9 more |
| 4 | `get_upstream_features` | L7:F14946@22, k=10 → Emb:" he"@22 (de=14.19) +9 more |
| 5 | `get_upstream_features` | L14:F14097@22, k=8 → Emb:" he"@22 (de=2.70) +7 more |
| 6 | `get_upstream_features` | L18:F14743@22, k=8 → Emb:" he"@22 (de=28.62) +7 more |
| 7 | `inspect_feature` ×6 | L13:1937, L4:15567, L2:11473, L4:14796, L17:5889, L15:10510 |
| 8 | `get_upstream_features` | L6:F12990@22, k=8 → Emb:" he"@22 (de=6.50) +7 more |
| 9 | `get_upstream_features` | L7:F14946@22, k=8 → Emb:" he"@22 (de=14.19) +7 more |
| 10 | `get_upstream_features` | L2:F11473@22, k=8 → Emb:" he"@22 (de=33.75) +7 more |
| 11 | `get_upstream_features` | L14:F4420@28, k=12 → Emb:" writer"@28 (de=5.75) +11 more |
| 12 | `get_upstream_features` | L4:F13253@28, k=8 → Emb:" writer"@28 (de=9.12) +7 more |

### Build

`build_circuit` → 12 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 80,894 | 5,408 | 288,160 | 0 | $0.0480 | — | — |
| SA-4 | openai/gpt-oss-120b | 80,308 | 4,924 | 0 | 0 | $0.0150 | ✅ 4F/3E | Trace upstream from L1:F15416 ("writers/writer" feature) at … |
| SA-3 | openai/gpt-oss-120b | 99,676 | 8,342 | 12,576 | 0 | $0.0201 | ✅ 5F/15E | Trace upstream from L14:F4420 (journalism/newspapers feature… |
| SA-2 | openai/gpt-oss-120b | 236,885 | 15,046 | 7,616 | 0 | $0.0447 | ✅ 6F/6E | Trace upstream from L14:F14097 ("he" pronoun feature) at pos… |
| **Total** | | **497,763** | **33,720** | **308,352** | **0** | **$0.1279** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 23s