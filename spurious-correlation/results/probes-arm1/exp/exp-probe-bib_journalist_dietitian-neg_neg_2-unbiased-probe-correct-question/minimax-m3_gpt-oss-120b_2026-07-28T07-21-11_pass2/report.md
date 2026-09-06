# Circuit Oracle Report
**Date:** 2026-07-28 07:21:11 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The journalist probe's classification score is driven by a *mixed* circuit in which the negative-direction signal comes from genuine journalism vocabulary features (L14:4420, L19:2486, L20:8433, L21:4401) all anchored on the word "report" and the phrase "top news organizations," but the *largest single positive-direction contributor* is L0:8964 — a pure lexical detector for the possessive pronoun "His" at position 1, with direct_effect = +0.0791 to the probe and frac_nonzero = 0.018.

**Confidence:** 6

**Reasoning:** The circuit splits into two clearly distinguishable streams. The "legitimate" profession stream flows Emb:"report" (pos 21) → L8:8855 "news reporters and reporting" → L14:4420 "journalism/newspaper vocabulary" → L19:2486 "journalistic sources/outlets" → L20:8433 "news broadcasting" / L21:4401 "government, news, reporting." These features all promote tokens like `reporter`, `journalism`, `CNN`, `Reuters` and have low frac_nonzero (0.005–0.05), showing they are real, content-specific profession detectors — but they contribute *negatively* to the probe here (e.g. L14:4420 direct_effect = −0.146 at pos 21), meaning the probe direction actively *discounts* clear journalism content in this particular sentence. Meanwhile the strongest *positive* push comes from L0:8964, which is literally just the embedding of "His" (autointerp: "the possessive pronoun 'His'", frac_nonzero = 0.018, promoted tokens are all punctuation/stopwords — not profession-related at all). The "His" embedding is the only top-3 positive feature that has no profession content; the other positives (L0:8444 "to", L0:14287 "see", L0:2011 "dream", L0:13948 "pink", L4:11898 "World+sport/war") are similarly generic lexical features, many of which simply co-occur with male-coded bio templates ("His desire to see the world has taken him to countries…"). So the user's concern is **partially confirmed**: there is no single strong "male" feature, but the probe is *not* primarily reading the "journalist" profession vocabulary — it is reading generic bio-template lexical cues (especially the leading "His") *while* discounting the actual profession words. The picture is more subtle than pure gender bias (L0:8964 is a "His" detector, not a "male profession" detector per se, and the second- and third-strongest positives are "to" and "see"), but the circuit does not strongly support the "journalist" classification from in-context evidence — instead it leans on co-occurring biographical scaffolding, which is exactly the kind of spurious correlation the user suspected. The deeper L0–L21 journalism features (4420, 2486, 8433, 4401) form a real profession-recognition pathway, but on this input they are pulling *against* the probe's classification, not toward it, indicating the probe has likely learned a "generic-male-bio" direction rather than a true "journalist" direction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: His (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: desire (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: to (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: see (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: world (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: report (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: news / organizations (pos 26-27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: news / organizations (pos 26-27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | L0:8964 - "His" possessive pronoun detector (pos 1) |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | L0 lexical detectors (pos 2) - dream/Left/etc. |  the word "dream" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F13948](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) | 2 | L0 lexical detectors (pos 2) - dream/Left/etc. |  the color "pink" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) |
| [L0:F15693](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) | 2 | L0 lexical detectors (pos 2) - dream/Left/etc. |  language related to personal anecdotes and opinions | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15693) |
| [L0:F15185](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15185) | 2 | L0 lexical detectors (pos 2) - dream/Left/etc. | the word "do" alongside references to figures, types, and the pronouns "we" and "us", possibly in the context of scientific studies and collaborative efforts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15185) |
| [L0:F14582](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14582) | 6 | L0 lexical detectors (pos 2) - dream/Left/etc. | the word "left" and sometimes "center" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14582) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | L0:8444 "to" / L0:14287 "see" (pos 3-4) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F14287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) | 4 | L0:8444 "to" / L0:14287 "see" (pos 3-4) | the word "see" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 20 | L0:8444 "to" / L0:14287 "see" (pos 3-4) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L4:F11898](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) | 6 | L4:11898 "World" + sport/war context (pos 6) |  mentions of "World" followed by a sport or war-related word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) |
| [L5:F771](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) | 6 | L5:771 "see" / L5:12586 (pos 6, 21) |  the word "see" and words often associated with "see" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) |
| [L5:F12586](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12586) | 21 | L5:771 "see" / L5:12586 (pos 6, 21) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12586) |
| [L6:F4923](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4923) | 6 | L6:4923 "wanting a profession" (pos 6) |  descriptions of someone wanting to work in a specific profession | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4923) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 22 | L6:12712 editor/publisher titles (pos 22) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L7:F3085](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3085) | 6 | L7:3085 "world/societal" + L7:13646 "news reporting" (pos 6, 21) |  words and phrases related to societal ills as well as human efforts to understand their world. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3085) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | L7:3085 "world/societal" + L7:13646 "news reporting" (pos 6, 21) | news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 26 | L7:9092 broadcast journalism phrasing (pos 26) | words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | L8:8855 "news reporters and reporting" (pos 21) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | L8:8855 "news reporters and reporting" (pos 21) | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | L14:4420 journalism/newspaper vocabulary (pos 21) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 22 | L14:4420 journalism/newspaper vocabulary (pos 21) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 26 | L14:4420 journalism/newspaper vocabulary (pos 21) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 25 | L14:4420 journalism/newspaper vocabulary (pos 21) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L15:F2579](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) | 21 | L15:2579 "reporting/official capacity" (pos 21) | instances of people providing information in some sort of official capacity. Like reporting incidents, communicating facts or informing others of something. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | L19:2486 journalistic sources/outlets (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 22 | L19:2486 journalistic sources/outlets (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 25 | L19:2486 journalistic sources/outlets (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 26 | L19:2486 journalistic sources/outlets (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 27 | L19:2486 journalistic sources/outlets (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 28 | L19:2486 journalistic sources/outlets (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 29 | L19:2486 journalistic sources/outlets (pos 21-29) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F5251](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/5251) | 22 | L19:2486 journalistic sources/outlets (pos 21-29) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/5251) |
| [L19:F531](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/531) | 22 | L19:2486 journalistic sources/outlets (pos 21-29) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/531) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 22 | L20:8433 news broadcasting (pos 22, 26) | words related to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 26 | L20:8433 news broadcasting (pos 22, 26) | words related to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |
| [L21:F4401](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/4401) | 22 | L21:4401 government/news/reporting (pos 22) | words and phrases connected to government, news, and reporting | [view](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/4401) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:4420 de=-0.145 |
| 3 | `inspect_feature` ×8 | L14:4420, L19:2486, L0:8964, L0:8444, L0:14287, L20:8433, L4:11898, L0:2011 |
| 4 | `get_top_features` | 30 features; top: L14:4420 de=-0.145 |
| 5 | `inspect_feature` ×6 | L15:2579, L7:3085, L0:13948, L8:8855, L0:2203, L5:771 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@21` | ✅ reported | 7 | 8 | Trace L14:F4420 ("words and phrases related to journalism and newspapers") at po… |
| SA-2 | `L19:F2486@21` | ✅ reported | 4 | 7 | Trace L19:F2486 ("journalistic sources and news outlets") at pos 21 upstream. Th… |
| SA-3 | `L0:F8964@1` | ✅ reported | 3 | 2 | Trace L0:F8964 ("the possessive pronoun 'His'") at pos 1 upstream. This is the s… |
| SA-4 | `L20:F8433@26` | ✅ reported | 6 | 15 | Trace L20:F8433 ("words related to news broadcasting") at pos 26 upstream. Pos 2… |

<details>
<summary><b>SA-1</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@21, k=15 | Emb:" report"@21 (de=5.22) +14 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `get_upstream_features` | L8:F8855@21, k=15 | Emb:" report"@21 (de=12.06) +14 more |
| 5 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 6 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 7 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |
| 8 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 9 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |
| 10 | `inspect_feature` | L6, F12624 | "words related to art, architecture, or law." |
| 11 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 12 | `inspect_feature` | L0, F12801 | " verbs related to communication, help, enabling, and allowing" |
| 13 | `get_upstream_features` | L4:F661@21, k=10 | Emb:" report"@21 (de=14.38) +9 more |
| 14 | `get_upstream_features` | L4:F661@21, k=20 | Emb:" report"@21 (de=14.38) +19 more |

**Findings:** The journalism gate (L14:F4420) is strongly driven by the lexical token "report" (embedding) and by mid‑layer features that detect reporters and news reporting (L8:F8855, L7:F13646). The path reaches layer 8, satisfying the lower‑third requirement, and includes positive embedding contributions. Gendered pronouns "His" and "him" also feed the gate, indicating a possible bias toward male subjects, t…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 2 | `get_upstream_features` | L19:F2486@21, k=10 | L14:F4420 (de=14.31) +9 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |
| 5 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 6 | `inspect_feature` | L16, F15046 | " names, organizations, and reporting verbs" |
| 7 | `get_upstream_features` | L8:F8855@21, k=10 | Emb:" report"@21 (de=12.06) +9 more |
| 8 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 9 | `get_upstream_features` | L7:F13646@21, k=10 | Emb:" report"@21 (de=7.22) +9 more |

**Findings:** The L19:F2486 journalism‑source feature is primarily driven by generic journalism vocabulary (L14:F4420) and a concrete reporting token embedding (" report"). The token embedding feeds into a low‑layer news‑reporting feature (L7:F13646) which cascades upward through L8:F8855 and L14:F4420, culminating in the target. No specific outlet names are involved; the signal originates from the word "report…

</details>

<details>
<summary><b>SA-3</b> — tool trace (2 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L0, F8964 | " the possessive pronoun "His"" |
| 2 | `get_upstream_features` | L0:F8964@1, k=10 | Emb:"His"@1 (de=13.69) +9 more |

**Findings:** Tracing from L0:F8964 at position 1 reveals that its strongest upstream driver is the raw embedding of the token 'His' (direct_effect 13.69), confirming that this feature is essentially a lexical detector for the possessive pronoun. The pronoun 'His' typically functions as a gender marker for male entities, so the feature captures gendered reference. A secondary, much smaller contribution comes fr…

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F8433 | "words related to news broadcasting" |
| 2 | `get_upstream_features` | L20:F8433@26, k=10 | Emb:" top"@26 (de=5.69) +9 more |
| 3 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 4 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 5 | `inspect_feature` | L19, F2486 | " journalistic sources and news outlets." |
| 6 | `get_upstream_features` | L7:F9092@26, k=10 | Emb:" top"@26 (de=-1.06) +9 more |
| 7 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 8 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 9 | `get_upstream_features` | L14:F4420@21, k=10 | Emb:" report"@21 (de=5.22) +9 more |

**Findings:** Starting from L20:F8433 (news‑broadcast detector) we traced upstream to several mid‑layer journalism‑related features (L14:F4420, L19:F2486, L7:F9092) and finally to lower‑third features at layer 7 and 6 (broadcast journalism phrasing and editorial titles). Positive embedding connections (e.g., the token " top" at position 26) provide direct lexical support. The path demonstrates a hierarchy: raw …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2011@2, k=8 → Emb:" desire"@2 (de=12.94) +7 more |
| 2 | `get_upstream_features` | L0:F13948@2, k=8 → Emb:" desire"@2 (de=14.44) +7 more |
| 3 | `get_upstream_features` | L0:F8444@3, k=5 → Emb:" to"@3 (de=39.50) +4 more |
| 4 | `get_upstream_features` | L0:F14287@4, k=5 → Emb:" see"@4 (de=25.12) +4 more |
| 5 | `get_upstream_features` | L4:F11898@6, k=8 → Emb:" world"@6 (de=35.25) +7 more |
| 6 | `get_upstream_features` | L7:F3085@6, k=5 → Emb:" world"@6 (de=9.56) +4 more |
| 7 | `inspect_feature` ×6 | L0:15185, L0:15693, L0:14582, L21:4401, L6:4923, L6:12712 |
| 8 | `get_upstream_features` | L21:F4401@22, k=8 → Emb:"<bos>"@0 (de=-6.81) +7 more |
| 9 | `get_upstream_features` | L8:F8855@21, k=5 → Emb:" report"@21 (de=12.06) +4 more |
| 10 | `get_upstream_features` | L15:F2579@21, k=5 → Emb:" report"@21 (de=38.25) +4 more |

### Build

`build_circuit` → 23 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 57,146 | 11,196 | 262,264 | 0 | $0.0463 | — | — |
| SA-3 | openai/gpt-oss-120b | 15,368 | 1,364 | 0 | 0 | $0.0031 | ✅ 3F/2E | Trace L0:F8964 ("the possessive pronoun 'His'") at pos 1 ups… |
| SA-2 | openai/gpt-oss-120b | 97,690 | 4,650 | 0 | 0 | $0.0174 | ✅ 4F/7E | Trace L19:F2486 ("journalistic sources and news outlets") at… |
| SA-1 | openai/gpt-oss-120b | 209,417 | 7,113 | 2,528 | 0 | $0.0357 | ✅ 7F/8E | Trace L14:F4420 ("words and phrases related to journalism an… |
| SA-4 | openai/gpt-oss-120b | 99,028 | 6,958 | 5,056 | 0 | $0.0191 | ✅ 6F/15E | Trace L20:F8433 ("words related to news broadcasting") at po… |
| **Total** | | **478,649** | **31,281** | **269,848** | **0** | **$0.1217** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 53s