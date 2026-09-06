# Circuit Oracle Report
**Date:** 2026-07-28 07:20:04 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's contradiction score is driven almost entirely by surface-level negation tokens ("No" and "No one" at the end of the prompt) and lexical conspiracy-topic cues ("Conspiracy", "theorists", "piracy"), with very little signal from the actual semantic content of the premise (MasterCard, chip, card, medical history).

**Confidence:** 8

**Reasoning:** The circuit splits into four supernodes converging on the probe output. The dominant drive comes from the **late negation cascade** at position 30 — eight stacked features (L0:1143 → L2:2771 → L6:15886 → L12:8719 → L13:10768 → L14:336 → L15:13061 → L16:11298) that all detect the token "No" / negation. L16:F11298 alone contributes direct_effect 0.24 to the probe, and L15:F13061 contributes 0.21. Tracing confirms these are rooted in the raw " No" embedding (direct_effect 33.75 into L14:336). The **"no one" detector** at pos 31 (L4:F15764, plus L2:F8837/F8142/F13586) adds another 0.29 + 0.20 + 0.19 + 0.19 = ~0.87 of direct effect, also driven entirely by the "No" + " one" embeddings. The **conspiracy topic** supernode (L5:F559 "conspiracy/co-conspirator", L3:F9739 "conspiracies", L4:F367 "political conflict", L2:F16028 "speculation/lies", plus L0:F44 and F14625 firing on "Cons" as a substring) contributes ~0.27 + 0.20 + 0.20 = ~0.67 of direct effect, all originating from the literal substrings "Cons", "piracy", "theorists". Only the **topic_entities** supernode (L2:F16230 "chip", L2:F7725 "card", L1:F13292 "personal", L0:F14574 "your", etc., ~0.24 + 0.21 + 0.20 + 0.20 = ~0.85) reflects prompt content — but these are shallow lexical detectors (frac_nonzero mostly < 0.01, just "chip" or "card" as a token) rather than integrated semantic representations. The user's concern is confirmed: the probe's contradiction classification is largely a shallow lexical heuristic. The negative-polarity word "No" and the negation construction "No one" provide the single largest push toward the contradiction label, and "Conspiracy" / "piracy" substrings provide a second large push. The actual proposition being negated (MasterCard building a chip storing medical history) is barely represented — it appears only as detached content-word detectors for individual tokens, not as an integrated entity-level representation. This is a textbook spurious-correlation failure mode: the probe has learned "negation words + conspiracy-themed words ⇒ contradiction" rather than reasoning about semantic entailment.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 30 | Probe output (contradiction classification score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 30 | Late-layer negation cascade (pos 30, 'No' / 'No one') | no | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 30 | Late-layer negation cascade (pos 30, 'No' / 'No one') |  uses of the word "no" or similar negative statements and words associated with "one" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 30 | Late-layer negation cascade (pos 30, 'No' / 'No one') | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L13:F10768](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) | 30 | Late-layer negation cascade (pos 30, 'No' / 'No one') | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) |
| [L12:F8719](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) | 30 | Late-layer negation cascade (pos 30, 'No' / 'No one') | phrases that start with "no." | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) |
| [L6:F15886](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15886) | 30 | Late-layer negation cascade (pos 30, 'No' / 'No one') |  the word "no" and related negative words like "not" or "never," often near other important keywords. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15886) |
| [L2:F2771](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) | 30 | Late-layer negation cascade (pos 30, 'No' / 'No one') | the word "no" as well as words and phrases that are conceptually related to negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) |
| [L0:F1143](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) | 30 | Late-layer negation cascade (pos 30, 'No' / 'No one') | the word "no" and related words like "nobody" and "trust" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) |
| [L4:F15764](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) | 31 | Mid-layer 'no one' / pronoun+verb+one detector (pos 31) |  fragments of sentences that contain a pronoun, a verb, and the word "one", or words with similar meanings | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 31 | Mid-layer 'no one' / pronoun+verb+one detector (pos 31) | the word "one" or "body" when preceded by the words "no" or "every." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L2:F8142](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8142) | 31 | Mid-layer 'no one' / pronoun+verb+one detector (pos 31) | words related to places, managing, and negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8142) |
| [L2:F13586](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) | 31 | Mid-layer 'no one' / pronoun+verb+one detector (pos 31) | words ending in 'thing' and 'one' often with preceding words indicating the presence of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 31 | Mid-layer 'no one' / pronoun+verb+one detector (pos 31) | the word "one". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L5:F559](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) | 2 | Conspiracy / QAnon topic detectors (pos 1-3, 'Conspiracy theorists') |  words frequently related to legal conspiracies and co-conspirators | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | Conspiracy / QAnon topic detectors (pos 1-3, 'Conspiracy theorists') |  words related to conspiracies | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L4:F367](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/367) | 2 | Conspiracy / QAnon topic detectors (pos 1-3, 'Conspiracy theorists') | words related to political conflict or discord | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/367) |
| [L2:F16028](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) | 3 | Conspiracy / QAnon topic detectors (pos 1-3, 'Conspiracy theorists') |  terms related to speculation, lies, false information, and conspiracy theories | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) |
| [L2:F16241](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) | 2 | Conspiracy / QAnon topic detectors (pos 1-3, 'Conspiracy theorists') | partial strings of the word "constructor" or words ending in "dering" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16241) |
| [L0:F44](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) | 1 | Conspiracy / QAnon topic detectors (pos 1-3, 'Conspiracy theorists') | words starting with "cons" that might indicate a constitution or consolidated standard, alongside "pride" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) |
| [L0:F14625](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) | 1 | Conspiracy / QAnon topic detectors (pos 1-3, 'Conspiracy theorists') |  the abbreviation "Cons" or "AC" followed by other letters | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Content-word topic detectors (MasterCard / chip / card / personal) |  mentions of semiconductor chips and devices | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L2:F7725](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) | 6 | Content-word topic detectors (MasterCard / chip / card / personal) | the word "card" when used in a technical context | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) |
| [L1:F13292](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) | 11 | Content-word topic detectors (MasterCard / chip / card / personal) |  the word "personal" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) |
| [L0:F14574](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) | 18 | Content-word topic detectors (MasterCard / chip / card / personal) | the possessive adjective "your." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) |
| [L1:F13684](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) | 3 | Content-word topic detectors (MasterCard / chip / card / personal) |  the word "theory" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) |
| [L0:F351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) | 11 | Content-word topic detectors (MasterCard / chip / card / personal) |  the word "expert" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | Content-word topic detectors (MasterCard / chip / card / personal) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | Content-word topic detectors (MasterCard / chip / card / personal) | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 30 | Emb: ' No' (pos 30) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 31 | Emb: ' one' (pos 31) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'Cons' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: 'theorists' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: 'piracy' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:44 de=-0.527 |
| 3 | `inspect_feature` ×20 | L0:11375, L0:3635, L4:15764, L0:14625, L5:559, L0:44, L0:14574, L16:11298, L15:13061, L0:351, L1:13292, L2:16028, L10:16373, L2:16230, L3:9739, L0:2115, L2:8142, L14:336, L2:7725, L1:13684 |

### Dispatch: 14 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F11298@30` | ✅ reported | 6 | 8 | Trace the 'no' word feature at L16, F11298, pos 30 upstream. What drives this fe… |
| SA-2 | `L15:F13061@30` | ✅ reported | 6 | 9 | Trace the 'no' / negative statement feature at L15, F13061, pos 30 upstream to e… |
| SA-3 | `L14:F336@30` | ✅ reported | 4 | 8 | Trace the 'no' word feature at L14, F336, pos 30 upstream to embeddings. |
| SA-4 | `L10:F16373@7` | ✅ reported | 4 | 4 | Trace the 'bigoted statements about minority groups' feature at L10, F16373, pos… |
| SA-5 | `L5:F559@2` | ✅ reported | 4 | 9 | Trace the 'conspiracies' feature at L5, F559, pos 2 upstream to embeddings. |
| SA-6 | `L4:F15764@31` | ✅ reported | 5 | 11 | Trace the 'pronoun+verb+one' feature at L4, F15764, pos 31 upstream to embedding… |
| SA-7 | `L0:F11375@7` | ❌ error | — | — | Trace the 'is' word feature at L0, F11375, pos 7 upstream to understand. |
| SA-8 | `L2:F16230@11` | ❌ error | — | — | Trace the 'chip' semiconductor feature at L2, F16230, pos 11 upstream to embeddi… |
| SA-9 | `L1:F13292@11` | ❌ error | — | — | Trace the 'personal' word feature at L1, F13292, pos 11 upstream. |
| SA-10 | `L0:F14574@18` | ❌ error | — | — | Trace the 'your' possessive feature at L0, F14574, pos 18 upstream. |
| SA-11 | `L2:F16028@3` | ❌ error | — | — | Trace the 'speculation/lies' feature at L2, F16028, pos 3 upstream to embeddings… |
| SA-12 | `L0:F14625@1` | ❌ error | — | — | Trace the 'Cons' abbreviation feature at L0, F14625, pos 1 upstream. |
| SA-13 | `L2:F7725@6` | ❌ error | — | — | Trace the 'card' technical feature at L2, F7725, pos 6 upstream. |
| SA-14 | `L1:F13684@3` | ❌ error | — | — | Trace the 'theory' word feature at L1, F13684, pos 3 upstream. |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F11298 | "no" |
| 2 | `get_upstream_features` | L16:F11298@30, k=10 | L15:F13061 (de=14.00) +9 more |
| 3 | `inspect_feature` | L15, F13061 | " uses of the word "no" or similar negative statements and words associ" |
| 4 | `get_upstream_features` | L15:F13061@30, k=10 | L14:F336 (de=13.00) +9 more |
| 5 | `inspect_feature` | L14, F336 | "the word "no" and related negative words" |
| 6 | `inspect_feature` | L6, F15886 | " the word "no" and related negative words like "not" or "never," often" |
| 7 | `inspect_feature` | L12, F8719 | " phrases that start with "no."" |
| 8 | `get_upstream_features` | L6:F15886@30, k=10 | Emb:" No"@30 (de=14.81) +9 more |

**Findings:** The 'no' token at position 30 is driven primarily by its raw embedding (token ' No'), which directly excites the L16 feature 11298. Upstream, a cascade of negation‑detecting features amplifies this signal: L15:13061 aggregates many negative statements, feeding from L14:336 and the same embedding. L14:336 receives a strong boost from the early‑layer L6:15886, an early‑layer cue detector for 'no' an…

</details>

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F13061 | " uses of the word "no" or similar negative statements and words associ" |
| 2 | `get_upstream_features` | L15:F13061@30, k=10 | L14:F336 (de=13.00) +9 more |
| 3 | `inspect_feature` | L14, F336 | "the word "no" and related negative words" |
| 4 | `inspect_feature` | L6, F15886 | " the word "no" and related negative words like "not" or "never," often" |
| 5 | `get_upstream_features` | L14:F336@30, k=10 | Emb:" No"@30 (de=33.75) +9 more |
| 6 | `inspect_feature` | L12, F8719 | " phrases that start with "no."" |
| 7 | `get_upstream_features` | L6:F15886@30, k=10 | Emb:" No"@30 (de=14.81) +9 more |
| 8 | `inspect_feature` | L13, F10768 | " negative sentiments and words like "no" in the context of a discussio" |
| 9 | `inspect_feature` | L0, F1143 | " the word "no" and related words like "nobody" and "trust"" |
| 10 | `get_upstream_features` | L12:F8719@30, k=10 | Emb:" No"@30 (de=16.50) +9 more |

**Findings:** Tracing from L15:F13061 (pos 30) reveals a concentrated negation circuit. The strongest upstream driver is the mid‑layer feature L14:F336, itself driven mainly by the raw " No" token embedding. The signal propagates through earlier layers: L13:F10768 (negative‑sentiment detector), L12:F8719 (phrases beginning with "No"), and down to early‑layer detectors L6:F15886 and L0:F1143 (layers ≤8). These p…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F336 | "the word "no" and related negative words" |
| 2 | `get_upstream_features` | L14:F336@30, k=10 | Emb:" No"@30 (de=33.75) +9 more |
| 3 | `inspect_feature` | L0, F1143 | " the word "no" and related words like "nobody" and "trust"" |
| 4 | `get_upstream_features` | L0:F1143@30, k=10 | Emb:" No"@30 (de=27.00) +9 more |
| 5 | `inspect_feature` | L13, F10768 | " negative sentiments and words like "no" in the context of a discussio" |
| 6 | `inspect_feature` | L2, F2771 | " the word "no" as well as words and phrases that are conceptually rela" |

**Findings:** The target feature L14:F336 is a mid‑layer detector for the token 'no' and related negations. Its strongest upstream driver is the raw input embedding for the token "No" (direct effect 33.75), confirming that the signal originates directly from the input token. Additional upstream features in early layers (L0:1143, L2:2771, L3:3266) also specialize in detecting negation cues and feed positively in…

</details>

<details>
<summary><b>SA-4</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L10, F16373 | "bigoted statements about minority groups" |
| 2 | `get_upstream_features` | L10:F16373@7, k=10 | Emb:" theorists"@3 (de=1.91) +9 more |
| 3 | `inspect_feature` | L9, F13961 | "political commentary related to Trump and elections" |
| 4 | `get_upstream_features` | L9:F13961@3, k=10 | L8:F12761 (de=6.88) +9 more |
| 5 | `inspect_feature` | L8, F12761 | " words associated with the QAnon conspiracy theory" |
| 6 | `inspect_feature` | L2, F16028 | " terms related to speculation, lies, false information, and conspiracy" |
| 7 | `get_upstream_features` | L8:F12761@3, k=10 | Emb:" theorists"@3 (de=4.56) +9 more |
| 8 | `inspect_feature` | L7, F14725 | " references to religious groups and leaders, particularly instances re" |

**Findings:** The bigoted output feature (L10:F16373) receives strong positive contribution from a political commentary feature (L9:13961) which itself is driven by a QAnon‑conspiracy detector (L8:12761). The QAnon feature is seeded by a low‑layer speculative/false‑information detector (L2:16028). Along this path we also see direct positive contributions from raw input embeddings such as the token 'theorists' (…

</details>

<details>
<summary><b>SA-5</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F559 | " words frequently related to legal conspiracies and co-conspirators" |
| 2 | `get_upstream_features` | L5:F559@2, k=10 | Emb:"piracy"@2 (de=6.72) +9 more |
| 3 | `inspect_feature` | L3, F9739 | " words related to conspiracies" |
| 4 | `get_upstream_features` | L3:F9739@2, k=10 | Emb:"Cons"@1 (de=8.75) +9 more |
| 5 | `inspect_feature` | L2, F1741 | "fragments of words ending in "ction", "notes," or "ual."" |
| 6 | `inspect_feature` | L4, F367 | " words related to political conflict or discord" |
| 7 | `get_upstream_features` | L4:F367@2, k=10 | Emb:"piracy"@2 (de=6.34) +9 more |
| 8 | `inspect_feature` | L2, F16241 | " partial strings of the word "constructor" or words ending in "dering"" |
| 9 | `inspect_feature` | L2, F16241 | " partial strings of the word "constructor" or words ending in "dering"" |

**Findings:** The target L5:F559 (conspiracy detector) receives its strongest excitatory input from the token embedding for 'piracy' and from a higher‑level conspiracy feature L3:F9739. L3:F9739 in turn is driven chiefly by the embeddings for 'Cons' and 'piracy'. A parallel pathway flows through a political‑conflict feature L4:F367, which also channels strong positive influence from the 'piracy' embedding and f…

</details>

<details>
<summary><b>SA-6</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F15764 | " fragments of sentences that contain a pronoun, a verb, and the word "" |
| 2 | `get_upstream_features` | L4:F15764@31, k=10 | Emb:" one"@31 (de=10.75) +9 more |
| 3 | `inspect_feature` | L2, F8837 | " the word "one" or "body" when preceded by the words "no" or "every."" |
| 4 | `inspect_feature` | L2, F8142 | "words related to places, managing, and negation" |
| 5 | `inspect_feature` | L2, F13586 | " words ending in 'thing' and 'one' often with preceding words indicati" |
| 6 | `inspect_feature` | L0, F4438 | "the word "one"." |
| 7 | `get_upstream_features` | L2:F8837@31, k=10 | Emb:" No"@30 (de=19.75) +9 more |
| 8 | `get_upstream_features` | L4:F15764@31, k=10 | Emb:" one"@31 (de=10.75) +9 more |
| 9 | `get_upstream_features` | L2:F8142@31, k=10 | Emb:" No"@30 (de=14.62) +9 more |
| 10 | `get_upstream_features` | L0:F4438@31, k=10 | Emb:" No"@30 (de=29.38) +9 more |
| 11 | `get_upstream_features` | L2:F13586@31, k=10 | Emb:" No"@30 (de=16.00) +9 more |

**Findings:** The target L4 feature that flags pronoun‑verb‑'one' constructions receives strong excitatory input from the raw token embeddings for 'one' (direct_effect 10.75) and, to a lesser extent, from the preceding token 'No' (direct_effect 1.97). Upstream, a layer‑2 negation detector (F8837) and related layer‑2 features (F8142, F13586) also drive the target, with F8837 showing a clear refusal‑relevant patt…

</details>

### Build

`build_circuit` → 10 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 91,254 | 7,393 | 163,110 | 0 | $0.0460 | — | — |
| SA-1 | openai/gpt-oss-120b | 82,144 | 5,256 | 2,528 | 0 | $0.0155 | ✅ 6F/8E | Trace the 'no' word feature at L16, F11298, pos 30 upstream.… |
| SA-3 | openai/gpt-oss-120b | 54,307 | 4,498 | 64 | 0 | $0.0108 | ✅ 4F/8E | Trace the 'no' word feature at L14, F336, pos 30 upstream to… |
| SA-5 | openai/gpt-oss-120b | 95,417 | 5,607 | 2,592 | 0 | $0.0177 | ✅ 4F/9E | Trace the 'conspiracies' feature at L5, F559, pos 2 upstream… |
| SA-2 | openai/gpt-oss-120b | 147,844 | 10,112 | 0 | 0 | $0.0282 | ✅ 6F/9E | Trace the 'no' / negative statement feature at L15, F13061, … |
| SA-4 | openai/gpt-oss-120b | 96,845 | 7,490 | 0 | 0 | $0.0190 | ✅ 4F/4E | Trace the 'bigoted statements about minority groups' feature… |
| SA-6 | openai/gpt-oss-120b | 135,777 | 6,668 | 2,560 | 0 | $0.0244 | ✅ 5F/11E | Trace the 'pronoun+verb+one' feature at L4, F15764, pos 31 u… |
| **Total** | | **703,588** | **47,024** | **170,854** | **0** | **$0.1618** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 52s