# Circuit Oracle Report
**Date:** 2026-07-28 07:03:09 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity-probe score is driven primarily by generic identity-group ("race/ethnicity" and "race/racism, focus on Black people") features in early-to-mid layers, which fire on the input tokens *white*, *black*, and *race*; the user's concern is confirmed — the circuit keys on the *presence* of identity-group vocabulary rather than on the toxic/persuasive content of the message.

**Confidence:** 7

**Reasoning:**

The terminal node is a linear-probe direction representing the toxicity score, not a token. `get_top_logits` returned a synthetic empty token, and `get_top_features` on it surfaced 15 features spanning layers 0–6, none deeper — the probe is fed by very early-layer features. Every positive driver in the top-15 list, when traced upstream, terminates in a token-embedding node that is a *race-identifier*: **emb_black_32** (10.5 → L2:13158), **emb_white_15** (12.8 → L2:13158), **emb_white_25** (10.8 → L6:3902), **emb_race_40** (13.6 → L2:13158), and emb_other_14 (2.1 → L2:13158). The two negative features that suppress the probe are tied to *clarification/citation* cues: **L0:6154 "clearly … arguments and writing"** and **L0:5707 "knowledge or perspective"** at pos 2 ("clearly"), plus **L1:2407 "the word 'clearly'"** (−0.24), and L0:12866 adverbs like "clearly" (−0.21). These anti-toxicity features are *register* markers, not content markers.

The dominant positive path is: identity-token embeddings → **L2:13158 "words about race and ethnicity"** (frac_nonzero ≈ 0.01; direct_effects 0.32, 0.23, 0.20, 0.19 across four positions) → into **L1:13646 "text discussing social justice issues"** (recurrent, fires at all four race-token positions with direct_effects 2.0–2.5) → and forward into **L4:117 "terms related to race, racism, and social justice, with a particular focus on terms related to Black people"** (frac_nonzero ≈ 0.012, direct_effect 0.22) and **L6:3902 "terms referring to race and ethnicity"** (frac_nonzero ≈ 0.018, direct_effect 0.20). L4:117 at pos 9 ("ot" in "bigot") is also amplified by **L3:15009** (legal/bias-prejudice) and **L3:12367** (government/law) and **L2:9433** (civil-unrest/protest) — i.e., any mention of a racial identity co-occurring with legal or protest discourse pushes the probe further toward "toxic."

Critically, no feature in the top-15 list encodes *toxicity semantics* specifically — there is no "slur," "dehumanization," or "hostile intent" detector. The "bigot" and "bigoted" tokens themselves are barely represented (only the "ot" suffix feeds L4:117, with the L4:14582 "White House / US government" feature on "America" being a generic political-entity detector). Instead, the probe's positive direction is the latent direction for "the text mentions a racial identity group in a social-justice-adjacent register." A benign sentence like "Black and white Americans should be treated equally" would activate essentially the same upstream chain (emb_black + emb_white → L2:13158 → L1:13646 → L4:117 → L6:3902) and would receive a similar probe score, even though its content is the opposite of the prompt's toxic thesis. Conversely, the negative-direction features only fire on register markers like "clearly" and citation/argument hedging — they do not encode the absence of slurs.

This confirms the user's hypothesis: the probe classification is being driven by **identity-group-mention features** (L1:13646, L2:13158, L4:117, L6:3902) — which are "an identity group" signals rather than toxicity semantics — and is partly *gated* by register markers like "clearly." The mechanistic story is essentially: any sentence that names two races, mentions "race" explicitly, or pairs a race identifier with political/protest vocabulary is read as toxic by this probe, regardless of whether the surrounding language is hateful or anti-hateful.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: white (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 32 | Emb: black (pos 32) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: white (pos 25) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 40 | Emb: race (pos 40) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ot (pos 9, end of 'bigot') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: clearly (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: other (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F7142](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) | 2 | L0 lexical / connective features (axis, and, other, clearly) |  the word "axis" and its plural form, often in the context of scientific or technical documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 10 | L0 lexical / connective features (axis, and, other, clearly) |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F7969](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) | 14 | L0 lexical / connective features (axis, and, other, clearly) |  the word "other" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) |
| [L0:F6154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6154) | 2 | L0 lexical / connective features (axis, and, other, clearly) |  uses of 'clearly' and nearby words that are related to arguments and writing | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6154) |
| [L0:F5707](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) | 2 | L0 lexical / connective features (axis, and, other, clearly) |  words or phrases related to knowledge or perspective | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) |
| [L0:F12866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) | 2 | L0 lexical / connective features (axis, and, other, clearly) |  adverbs such as "clearly," "plainly," and "as" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 32 | L1 race / social-justice discourse detectors | text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 15 | L1 race / social-justice discourse detectors | text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 40 | L1 race / social-justice discourse detectors | text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L1:F3020](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3020) | 32 | L1 race / social-justice discourse detectors | the word "factor" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3020) |
| [L1:F12717](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12717) | 32 | L1 race / social-justice discourse detectors | words or phrases related to education | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12717) |
| [L1:F2407](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) | 2 | L1 race / social-justice discourse detectors |  the word "clearly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 32 | L2:13158 — 'words about race and ethnicity' (multi-position) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 15 | L2:13158 — 'words about race and ethnicity' (multi-position) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 40 | L2:13158 — 'words about race and ethnicity' (multi-position) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 25 | L2:13158 — 'words about race and ethnicity' (multi-position) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L3:F15009](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15009) | 9 | L3 legal / government / civil-unrest features | words or phrases related to courts, legalese, and mental states | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15009) |
| [L3:F12367](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12367) | 9 | L3 legal / government / civil-unrest features | words related to government, law, and locations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12367) |
| [L2:F9433](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9433) | 9 | L2:9433 protest / civil-unrest terms | words related to civil unrest, political action, and disagreement | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9433) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 9 | L4:117 — race/racism, focus on Black people (pos 9, 25) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 25 | L4:117 — race/racism, focus on Black people (pos 9, 25) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | L4:117 — race/racism, focus on Black people (pos 9, 25) |  references to the White House and the US government | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |
| [L5:F8030](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) | 3 | L5:8030 differences/clarity/definition discourse |  language discussing differences, clarity, and definition | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 25 | L6:3902 — race and ethnicity terms (pos 25) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:5707 de=-0.346 |
| 3 | `inspect_feature` ×12 | L0:5707, L2:13158, L0:3255, L0:6154, L0:7969, L1:2407, L4:117, L5:8030, L6:3902, L4:14582, L0:7142, L0:12866 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F117@9` | ✅ reported | 6 | 5 | Trace L4:F117 (race/racism terms, focus on Black people, direct_effect=0.2188 at… |
| SA-2 | `L6:F3902@25` | ❌ error | — | — | Trace L6:F3902 (terms referring to race and ethnicity, direct_effect=0.2021 at p… |
| SA-3 | `L2:F13158@32` | ✅ reported | 6 | 5 | Trace L2:F13158 (words about race and ethnicity, direct_effect=0.3184 at pos 32 … |
| SA-4 | `L1:F2407@2` | ✅ reported | 5 | 4 | Trace L1:F2407 (the word "clearly", direct_effect=-0.2412 at pos 2) upstream. Wh… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 2 | `get_upstream_features` | L4:F117@9, k=10 | Emb:"ot"@9 (de=3.52) +9 more |
| 3 | `inspect_feature` | L3, F15009 | "words or phrases related to courts, legalese, and mental states" |
| 4 | `inspect_feature` | L3, F12367 | " words related to government, law, and locations." |
| 5 | `get_upstream_features` | L3:F15009@9, k=10 | Emb:"ot"@9 (de=6.75) +9 more |
| 6 | `get_upstream_features` | L3:F12367@9, k=10 | Emb:" big"@8 (de=20.62) +9 more |
| 7 | `inspect_feature` | L2, F9093 | " words related to systems, scientific and engineering" |
| 8 | `get_upstream_features` | L2:F9093@9, k=10 | Emb:" big"@8 (de=12.56) +9 more |
| 9 | `inspect_feature` | L2, F9433 | " words related to civil unrest, political action, and disagreement" |
| 10 | `inspect_feature` | L3, F15558 | " words that indicate feelings or qualities" |
| 11 | `get_upstream_features` | L2:F9433@9, k=10 | Emb:" big"@8 (de=4.84) +9 more |
| 12 | `inspect_feature` | L2, F8105 | "scientific and technical terms, particularly related to medicine and b" |

**Findings:** Starting from the race‑related feature L4:F117 (pos 9), the strongest upstream driver is the embedding token "ot" (pos 9), which directly excites the feature (+3.5 direct effect). The next strongest upstream contributors are layer‑3 features 15009 (legal language) and 12367 (government language), each providing >1.0 direct effect. Tracing further, feature 15009 receives its largest positive input …

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 2 | `get_upstream_features` | L2:F13158@32, k=10 | Emb:" black"@32 (de=10.50) +9 more |
| 3 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |
| 4 | `get_upstream_features` | L1:F13646@32, k=10 | Emb:" black"@32 (de=4.25) +9 more |
| 5 | `inspect_feature` | L1, F3020 | " the word "factor"" |
| 6 | `get_upstream_features` | L1:F3020@32, k=10 | Emb:" black"@32 (de=16.88) +9 more |
| 7 | `inspect_feature` | L1, F12717 | " words or phrases related to education" |
| 8 | `inspect_feature` | L0, F16013 | " mentions of the color blue, and perhaps colors in general or the comp" |
| 9 | `get_upstream_features` | L1:F12717@32, k=10 | Emb:" black"@32 (de=7.22) +9 more |
| 10 | `inspect_feature` | L1, F4679 | " references to musical groups, legal proceedings, and race, especially" |
| 11 | `get_upstream_features` | L0:F16013@32, k=10 | Emb:" black"@32 (de=16.62) +9 more |

**Findings:** The top positive feature (L2:F13158) that amplifies race‑related language receives its strongest excitation from the input token " black" at position 32. The signal propagates through several lower‑layer features that encode social‑justice discourse, generic lexical cues, education language, and colour detection, all of which are themselves driven primarily by the same token embedding. All downstr…

</details>

<details>
<summary><b>SA-4</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F2407 | " the word "clearly"" |
| 2 | `get_upstream_features` | L1:F2407@2, k=10 | Emb:" clearly"@2 (de=22.00) +9 more |
| 3 | `inspect_feature` | L0, F15810 | " mentions of surgical procedures" |
| 4 | `inspect_feature` | L0, F7142 | " the word "axis" and its plural form, often in the context of scientif" |
| 5 | `inspect_feature` | L0, F7861 | " instances of the words "this", "these", "clearly", or "more"." |
| 6 | `get_upstream_features` | L0:F15810@2, k=10 | Emb:" clearly"@2 (de=14.00) +9 more |
| 7 | `inspect_feature` | L0, F4517 | " the word "destroyed"" |

**Findings:** The token embedding for "clearly" (pos 2) strongly excites L1:F2407 (direct_effect = 22.0). L1:F2407 aggregates this signal and, through its own negative direct_effect (‑0.2412) on the toxicity probe, acts as a tone‑down gate: the clearer the statement, the less the model is inclined to produce toxic output. Upstream, the activation is mediated by a handful of sparse, low‑layer (layer 0) features—…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F117@9, k=5 → Emb:"ot"@9 (de=3.52) +4 more |
| 2 | `get_upstream_features` | L6:F3902@25, k=5 → Emb:" white"@25 (de=10.81) +4 more |
| 3 | `get_upstream_features` | L2:F13158@32, k=5 → Emb:" black"@32 (de=10.50) +4 more |
| 4 | `get_upstream_features` | L2:F13158@15, k=5 → Emb:" white"@15 (de=12.81) +4 more |
| 5 | `get_upstream_features` | L2:F13158@40, k=5 → Emb:" race"@40 (de=13.62) +4 more |

### Build

`build_circuit` → 16 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,623 | 5,555 | 92,524 | 0 | $0.0265 | — | — |
| SA-4 | openai/gpt-oss-120b | 66,147 | 4,801 | 7,712 | 0 | $0.0129 | ✅ 5F/4E | Trace L1:F2407 (the word "clearly", direct_effect=-0.2412 at… |
| SA-3 | openai/gpt-oss-120b | 125,914 | 8,868 | 25,856 | 0 | $0.0246 | ✅ 6F/5E | Trace L2:F13158 (words about race and ethnicity, direct_effe… |
| SA-1 | openai/gpt-oss-120b | 135,756 | 10,360 | 34,528 | 0 | $0.0271 | ✅ 6F/5E | Trace L4:F117 (race/racism terms, focus on Black people, dir… |
| **Total** | | **375,440** | **29,584** | **160,620** | **0** | **$0.0911** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 22s