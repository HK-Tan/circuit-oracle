# Circuit Oracle Report
**Date:** 2026-07-28 07:02:36 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "engineer / academic" is driven not by a single professional-content feature but by *four parallel supernodes* — (1) a thin profession-word detector triggered by the literal token "Engineering" and the proper name "Daniel", (2) a strong Canadian-geography cascade triggered by "Waterloo", (3) a biographical-format cascade triggered by the tokens "Ph" and "D" in "Ph.D", and (4) a generic biography scaffold (dates, "later", "his"/"he" pronouns) — meaning the probe is largely reading biographical *scaffolding* and *named places*, with only modest input from a genuine profession word.

**Confidence:** 7

**Reasoning:**

The `get_top_features` ranking at the probe node shows the profession-word signal (L1:F1372 "the word engineer", direct_effect +0.064 at pos 9; L2:F16309 "people's names", direct_effect +0.049 at pos 1) is real but is matched or exceeded by *content-independent* signals. Tracing downstream:

- **Profession word (genuine but thin):** L1:F1372 is fed almost entirely by the raw embedding of "Engineering" (pos 9, direct_effect ~19), with the preceding "Mechanical" token contributing only 0.75. Downstream L0:F6414 "the job title of engineer" adds a smaller secondary boost. This is the only path that genuinely encodes the profession lexically, but it is a single-token cue (frac_nonzero 0.0077 → low-frequency "engineer"-detector).

- **Canadian-place cascade (spurious by profession):** L14:F5600 "places and regions, particularly in Canada" (+0.064) is the probe's single largest direct contributor, fed by L7:F8870 "locations and names of organizations or people" and L4:F8439 "stock ticker symbols and Canadian geography" — both ultimately driven by the "Waterloo" embedding (direct_effect 17.25 → F8439, 12.625 → F5600). The autointerp label explicitly mentions "particularly in Canada" and promoted tokens are "▁Canada/Canadians/Ontario/Toronto". This is a *country* cue, not a *profession* cue. On a Wikipedia biography template, a Canadian place name and an academic profession co-occur so reliably that the probe treats the place as evidence of the profession.

- **Academic-degree cascade (spurious by profession):** L7:F14129 "academic degrees, universities, and people associated with them" (+0.044 at pos 50) plus the negative L6:F3235 "academic publications, math, and scientific institutions" (–0.055) and L2:F13360 "academic titles and positions" all originate from the "Ph" (pos 48) and "D" (pos 50) token embeddings via L2:F10852 / L1:F10132 "the abbreviation for Doctorate of Philosophy, 'D'". This chain detects the *biographical format* "Ph.D. in <field> at <university>" — it would fire for any doctorate-holder regardless of profession (engineer, historian, biologist). The L2:F13360 "academic titles" feature (promoted tokens: "Professors, professors, Profess, postdoctoral") reinforces a generic *academic-persona* template.

- **Year/biography scaffold (pure format cue):** L0:F6515 "the year 199X or 200X" (–0.048, pos 18), L0:F11333 "the 1990's" (–0.045, pos 19), L0:F11132 "a mix of possessive pronouns like 'his' … and years" (–0.044), and L2:F14934 "years in the 1900s" (+0.036) are all generic date detectors driven by the digit embeddings of "1993" / "2002" / "2006". L0:F2994 "the pronoun 'his' and the pronoun 'he'" (–0.036) at pos 3 ("He later") and L0:F2743 "the word 'later'" at pos 23 are pure biographical-grammar cues with frac_nonzero ~0.07–0.18, not profession content. Note: **none of these fire on gender markers specifically** — the "his/he" feature is a generic possessive, not a gendered profession prior — but the user's broader concern (spurious scaffolding) is well-founded because *most* of the probe's input is date/format/place rather than profession vocabulary.

**Verdict on the user's concern:** The user's specific worry about *gender markers* is not supported here — L0:F2994 fires on "his" but is a generic possessive, and its direct_effect on the probe is *negative* (–0.036), so it actually pushes *against* the classification. However, the broader concern that the probe relies on *spurious scaffolding* is well-supported: the Canadian-place feature (L14:F5600) and the biographical-format degree chain (L7:F14129 ← L1:F10132 "D as PhD") each carry direct_effects comparable to or exceeding the literal "engineer" detector, and a generic year/scaffold cluster (L0:F6515, L0:F11333, L0:F2994, L0:F2743) provides additional non-professional signal. A robust profession probe should show the "engineer" supernode dominating; instead it is one of several roughly coequal contributors, with the rest being biography-template cues that would also fire for any Canadian PhD-holder.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F1372](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) | 9 | Profession/degree token detectors | the word "engineer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) |
| [L2:F16309](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) | 1 | Profession/degree token detectors |  people's names | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) |
| [L14:F5600](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) | 14 | Canadian-place / geography features |  places and regions, particularly in Canada | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) |
| [L7:F8870](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) | 14 | Canadian-place / geography features |  locations and names of organizations or people | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) |
| [L4:F8439](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) | 14 | Canadian-place / geography features |  stock ticker symbols and Canadian geography | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) |
| [L0:F4687](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) | 14 | Canadian-place / geography features | place names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 50 | Academic-degree / biographical-format detectors |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 50 | Academic-degree / biographical-format detectors | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 50 | Academic-degree / biographical-format detectors | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 50 | Academic-degree / biographical-format detectors |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 50 | Academic-degree / biographical-format detectors |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L2:F13360](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) | 50 | Academic-degree / biographical-format detectors |  words related to academic titles and positions. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 18 | Year / 199X/200X detectors (date format) |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 19 | Year / 199X/200X detectors (date format) |  the 1990's | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 19 | Year / 199X/200X detectors (date format) |  a mix of possessive pronouns like "his", names associated with historical records, and years. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L2:F14934](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) | 19 | Year / 199X/200X detectors (date format) |  years in the 1900s | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Biography scaffold / pronoun / verb features | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F13553](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) | 2 | Biography scaffold / pronoun / verb features |  verbs in the past tense or past participle | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) |
| [L0:F2743](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) | 23 | Biography scaffold / pronoun / verb features | the word 'later' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) |
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | Biography scaffold / pronoun / verb features |  the word "ice" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2743 de=-0.069 |
| 3 | `inspect_feature` ×5 | L1:1372, L14:5600, L0:15320, L2:16309, L0:4687 |
| 4 | `get_upstream_features` | Emb:" Engineering"@9 (de=19.00) +9 more |
| 5 | `get_upstream_features` | L7:F8870 (de=15.94) +9 more |
| 6 | `get_upstream_features` | L4:F8439 (de=9.00) +9 more |
| 7 | `inspect_feature` ×2 | L4:8439, L7:8870 |
| 8 | `get_upstream_features` | Emb:" Waterloo"@14 (de=17.25) +4 more |
| 9 | `get_upstream_features` | L6:F2254 (de=7.31) +7 more |
| 10 | `inspect_feature` | " academic degrees, universities, and people associated with them" |
| 11 | `get_upstream_features` | L2:F10852 (de=12.31) +7 more |
| 12 | `inspect_feature` | "references to academic degrees" |
| 13 | `get_upstream_features` | Emb:" Beirut"@38 (de=1.85) +7 more |
| 14 | `get_upstream_features` | Emb:" Ph"@48 (de=14.75) +7 more |
| 15 | `get_upstream_features` | Emb:" Ph"@48 (de=16.38) +4 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F5600@14` | ✅ reported | 3 | 6 | Trace the path from L14:F5600 (Canadian places/regions) back to the embedding. F… |
| SA-2 | `L7:F14129@50` | ✅ reported | 5 | 13 | Trace the path from L7:F14129 (academic degrees, universities, people). Determin… |
| SA-3 | `L1:F1372@9` | ✅ reported | 6 | 8 | Trace the path from L1:F1372 (the word 'engineer') at pos 9 ('Engineering'). Thi… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F5600 | " places and regions, particularly in Canada" |
| 2 | `get_upstream_features` | L14:F5600@14, k=10 | L7:F8870 (de=15.94) +9 more |
| 3 | `inspect_feature` | L7, F8870 | " locations and names of organizations or people" |
| 4 | `inspect_feature` | L4, F8439 | " stock ticker symbols and Canadian geography" |
| 5 | `get_upstream_features` | L7:F8870@14, k=10 | L4:F8439 (de=9.00) +9 more |
| 6 | `get_upstream_features` | L4:F8439@14, k=10 | Emb:" Waterloo"@14 (de=17.25) +9 more |

**Findings:** The trace shows that the high‑level Canadian‑place feature L14:F5600 receives its strongest excitatory input from the mid‑layer entity detector L7:F8870 and the early‑layer Canadian‑geography detector L4:F8439. Both of those features are driven directly by the raw token embedding for 'Waterloo' (pos 14), which has large positive direct_effects (17.25 to L4:F8439, 8.25 to L7:F8870, 12.625 to L14:F5…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@50, k=10 | L6:F2254 (de=7.31) +9 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 5 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 6 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 7 | `get_upstream_features` | L2:F10852@50, k=10 | Emb:" Ph"@48 (de=14.75) +9 more |
| 8 | `get_upstream_features` | L1:F10132@50, k=10 | Emb:" Ph"@48 (de=16.38) +9 more |
| 9 | `get_upstream_features` | L6:F2254@50, k=10 | L2:F10852 (de=12.31) +9 more |

**Findings:** The traced path shows L7:F14129 relying on a cascade of degree‑related features (L6:F2254, L5:F13801, L2:F10852, L1:F10132) that ultimately originate from the raw token embeddings for " Ph" (pos 48) and "D" (pos 50). The chain captures the biographical format of academic credentials (e.g., "PhD at University X") rather than a generic profession signal. Thus the feature encodes a BIOGRAPHICAL‑FORMA…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F1372 | "the word "engineer"" |
| 2 | `get_upstream_features` | L1:F1372@9, k=10 | Emb:" Engineering"@9 (de=19.00) +9 more |
| 3 | `inspect_feature` | L0, F6414 | " the job title of "engineer", sometimes in conjunction with other word" |
| 4 | `inspect_feature` | L0, F15570 | " words and phrases related to medical treatment and analysis" |
| 5 | `inspect_feature` | L0, F5362 | " words related to sporting events, audio equipment, or multimedia and " |
| 6 | `get_upstream_features` | L0:F6414@9, k=10 | Emb:" Engineering"@9 (de=11.88) +9 more |

**Findings:** The path reveals that the dominant positive influence on L1:F1372 (the 'engineer' detector) comes directly from the raw embedding of the token 'Engineering' at position 9 (direct_effect ~19). The preceding token 'Mechanical' provides a much smaller boost (~0.75). Lower‑layer (layer 0) features that also detect the word 'engineer' (6414) and a few generic features contribute modestly, but none appr…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F16309@1, k=5 → Emb:"Daniel"@1 (de=12.94) +4 more |
| 2 | `get_upstream_features` | L2:F14934@19, k=5 → L0:F6515 (de=8.31) +4 more |
| 3 | `inspect_feature` | L2, F14934 → " years in the 1900s" |
| 4 | `get_upstream_features` | L0:F15320@2, k=5 → Emb:" received"@2 (de=13.00) +4 more |
| 5 | `get_upstream_features` | L0:F6515@18, k=5 → Emb:"1"@17 (de=29.38) +4 more |
| 6 | `inspect_feature` ×6 | L0:11333, L0:6515, L0:11132, L0:15320, L0:4687, L0:12235 |
| 7 | `get_upstream_features` | L0:F4687@14, k=5 → Emb:" Waterloo"@14 (de=16.25) +4 more |
| 8 | `inspect_feature` ×5 | L0:2085, L0:7905, L0:13553, L0:2994, L0:2743 |
| 9 | `get_upstream_features` | L0:F2743@23, k=5 → Emb:" later"@23 (de=42.25) +4 more |
| 10 | `inspect_feature` ×7 | L6:3235, L2:13360, L6:2254, L1:10132, L2:10852, L5:13801, L4:8439 |
| 11 | `get_upstream_features` | L6:F3235@38, k=10 → Emb:" Beirut"@38 (de=1.85) +9 more |

### Build

`build_circuit` → 16 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 61,913 | 5,934 | 474,559 | 0 | $0.0542 | — | — |
| SA-1 | openai/gpt-oss-120b | 54,700 | 4,733 | 12,768 | 0 | $0.0112 | ✅ 3F/6E | Trace the path from L14:F5600 (Canadian places/regions) back… |
| SA-3 | openai/gpt-oss-120b | 50,679 | 3,711 | 5,376 | 0 | $0.0099 | ✅ 6F/8E | Trace the path from L1:F1372 (the word 'engineer') at pos 9 … |
| SA-2 | openai/gpt-oss-120b | 94,776 | 5,522 | 7,936 | 0 | $0.0176 | ✅ 5F/13E | Trace the path from L7:F14129 (academic degrees, universitie… |
| **Total** | | **262,068** | **19,900** | **500,639** | **0** | **$0.0930** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 43s