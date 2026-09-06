# Circuit Oracle Report
**Date:** 2026-07-28 07:10:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven primarily by two parallel, lexically-triggered cascades: (1) a dedicated "No" detection chain that fires on the single token "No" at position 30, and (2) a conspiracy/ideology chain that fires on the word "Conspiracy" at positions 1-3, with a sprinkling of generic surface-form features ("is", "that", "your", "personal", "card", "chip") that act as weak background contributors.

**Confidence:** 7/10

**Reasoning:**

The circuit I built confirms the user's concern. Two distinct, lexically-triggered pathways dominate the probe's positive score:

**Pathway 1 — "No" detection (the dominant driver).** The probe's strongest direct effects come from L16:F11298 (direct_effect=0.24), L15:F13061 (0.21), and L14:F336 (0.20) — all three are pure negation detectors. Tracing upstream reveals the cascade:

`Emb: " No" (pos 30) → L0:F1143 / L0:F14862 (frac_nonzero ~0.002-0.014) → L2:F2771 / L3:F3266 → L6:F15886 → L12:F8719 / L13:F10768 → L14:F336 → L15:F13061 → L16:F11298 → probe_logit`

Every feature in this path is specifically about the word "no." The literal token " No" contributes direct_effect=27.0 to L0:F1143, 33.75 to L14:F336, 14.81 to L6:F15886, 12.69 to L15:F13061, and 12.0 to L16:F11298. These are the largest single-edge effects in the entire circuit, and they all originate from a single token.

**Pathway 2 — "Conspiracy" detection.** L10:F16373 ("bigoted statements about minority groups", direct_effect=0.207), L2:F16028 (speculation/conspiracy, 0.207), L3:F9739 (conspiracy words, 0.20), L0:F44 and L0:F14625 (both "Cons"-prefix detectors with direct_effect -0.53 and 0.29 at position 1) all fire on the token "Conspiracy." The upstream trace shows L2:F16028 receives direct_effect=11.75 from Emb " theorists" (pos 3) and 8.0 from Emb "piracy" (pos 2), then L8:F12761 ("QAnon conspiracy theory" detector) and L9:F13961 ("Trump and elections" commentary) propagate a thematic conspiracy/political signal that ultimately feeds L10:F16373.

**Pathway 3 — Surface-form noise.** The remaining features (L0:F11375="is", L0:F3635="that", L0:F14574="your", L0:F13292="personal", L0:F351="expert", L2:F16230="semiconductor chip", L2:F7725="card") are generic lexical detectors with small individual effects (~0.2) that act as scattered background contributors.

**Mechanism summary.** The probe classifies this as "contradiction" not because of any deep semantic comparison between premise and hypothesis, but because the input happens to contain (a) a capitalized "No" at sentence start, and (b) the word "Conspiracy" — both of which the model has been trained to associate with argumentative, refutational, or oppositional text. The probe has learned a **spurious lexical shortcut**: presence of explicit negation markers + conspiracy vocabulary = contradiction. This is precisely the failure mode the user suspected. The "contradiction" label is being driven by surface form rather than by the actual semantic relationship between the claim and its refutation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 30 | Emb: ' No' (pos 30) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'Cons' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: 'piracy' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' theorists' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 18 | Emb: 'your' (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: ' personal' (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' chip' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: 'Master' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' that' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1143](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) | 30 | Low-level 'No'/negation detectors (L0-L2) |  the word "no" and related words like "nobody" and "trust" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) |
| [L0:F14862](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) | 30 | Low-level 'No'/negation detectors (L0-L2) | the word "no" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14862) |
| [L2:F2771](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) | 30 | Low-level 'No'/negation detectors (L0-L2) | the word "no" as well as words and phrases that are conceptually related to negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) |
| [L3:F3266](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) | 30 | Low-level 'No'/negation detectors (L0-L2) | the abbreviation "No." for Number | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) |
| [L0:F44](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) | 1 | Low-level conspiracy / 'Conspiracy' detectors (L0-L3) | words starting with "cons" that might indicate a constitution or consolidated standard, alongside "pride" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/44) |
| [L0:F14625](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) | 1 | Low-level conspiracy / 'Conspiracy' detectors (L0-L3) |  the abbreviation "Cons" or "AC" followed by other letters | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14625) |
| [L0:F1927](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1927) | 3 | Low-level conspiracy / 'Conspiracy' detectors (L0-L3) | words and phrases related to the social sciences, research, and historical studies. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1927) |
| [L0:F13169](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13169) | 3 | Low-level conspiracy / 'Conspiracy' detectors (L0-L3) | words referring to people in positions of authority | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13169) |
| [L1:F12471](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12471) | 3 | Low-level conspiracy / 'Conspiracy' detectors (L0-L3) | words and phrases relating to mechanics, publications, community and math | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12471) |
| [L3:F9739](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) | 2 | Low-level conspiracy / 'Conspiracy' detectors (L0-L3) |  words related to conspiracies | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9739) |
| [L5:F559](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) | 2 | Mid-layer negation aggregators (L5-L13) |  words frequently related to legal conspiracies and co-conspirators | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/559) |
| [L6:F15886](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15886) | 30 | Mid-layer negation aggregators (L5-L13) | the word "no" and related negative words like "not" or "never," often near other important keywords. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15886) |
| [L12:F8719](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) | 30 | Mid-layer negation aggregators (L5-L13) | phrases that start with "no." | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) |
| [L13:F10768](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) | 30 | Mid-layer negation aggregators (L5-L13) | negative sentiments and words like "no" in the context of a discussion or argument. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) |
| [L2:F16028](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) | 3 | Mid-layer conspiracy/ideology aggregators (L7-L10) |  terms related to speculation, lies, false information, and conspiracy theories | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16028) |
| [L2:F16230](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) | 11 | Mid-layer conspiracy/ideology aggregators (L7-L10) |  mentions of semiconductor chips and devices | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16230) |
| [L2:F7725](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) | 6 | Mid-layer conspiracy/ideology aggregators (L7-L10) | the word "card" when used in a technical context | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7725) |
| [L2:F8142](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8142) | 31 | Mid-layer conspiracy/ideology aggregators (L7-L10) | words related to places, managing, and negation | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8142) |
| [L4:F15764](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) | 31 | Mid-layer conspiracy/ideology aggregators (L7-L10) |  fragments of sentences that contain a pronoun, a verb, and the word "one", or words with similar meanings | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15764) |
| [L8:F12761](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) | 3 | Mid-layer conspiracy/ideology aggregators (L7-L10) | words associated with the QAnon conspiracy theory | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12761) |
| [L9:F13961](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13961) | 3 | Mid-layer conspiracy/ideology aggregators (L7-L10) | political commentary related to Trump and elections | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13961) |
| [L10:F16373](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/16373) | 7 | Mid-layer conspiracy/ideology aggregators (L7-L10) | bigoted statements about minority groups | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/16373) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 30 | Late-layer negation features (L14-L16) | the word "no" and related negative words | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 30 | Late-layer negation features (L14-L16) |  uses of the word "no" or similar negative statements and words associated with "one" | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 30 | Late-layer negation features (L14-L16) | no | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 7 | Misc surface-form features (lexical/structural) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3635](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) | 12 | Misc surface-form features (lexical/structural) | the word "that" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3635) |
| [L0:F14574](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) | 18 | Misc surface-form features (lexical/structural) | the possessive adjective "your." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14574) |
| [L0:F2115](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) | 2 | Misc surface-form features (lexical/structural) |  data reported as a percentage inside brackets, especially in a laboratory or medical context, and also recognizes countries | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) |
| [L1:F13292](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) | 11 | Misc surface-form features (lexical/structural) |  the word "personal" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13292) |
| [L1:F13684](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) | 3 | Misc surface-form features (lexical/structural) |  the word "theory" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13684) |
| [L0:F351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) | 11 | Misc surface-form features (lexical/structural) |  the word "expert" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/351) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:44 de=-0.527 |
| 3 | `inspect_feature` ×20 | L0:44, L0:11375, L0:3635, L0:14574, L0:14625, L1:13292, L0:351, L2:16028, L3:9739, L0:2115, L5:559, L4:15764, L10:16373, L2:16230, L2:8142, L2:7725, L1:13684, L16:11298, L15:13061, L14:336 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F11298@30` | ✅ reported | 5 | 11 | Trace the path from L16:F11298 (a "No" feature) upstream. What is the full upstr… |
| SA-2 | `L15:F13061@30` | ✅ reported | 4 | 6 | Trace the path from L15:F13061 ("No" + "one" feature) upstream. What tokens and … |
| SA-3 | `L14:F336@30` | ✅ reported | 7 | 8 | Trace the path from L14:F336 ("No" / negation feature) upstream to the embedding… |
| SA-4 | `L10:F16373@7` | ✅ reported | 4 | 23 | Trace L10:F16373 ("bigoted statements about minority groups") upstream. What inp… |
| SA-5 | `L3:F9739@2` | ❌ error | — | — | Trace L3:F9739 (conspiracy words) upstream to find what tokens/context drive thi… |
| SA-6 | `L2:F16028@3` | ✅ reported | 5 | 15 | Trace L2:F16028 (speculation/conspiracy) upstream to find what tokens drive it. |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L16, F11298 | "no" |
| 2 | `get_upstream_features` | L16:F11298@30, k=10 | L15:F13061 (de=14.00) +9 more |
| 3 | `inspect_feature` | L15, F13061 | " uses of the word "no" or similar negative statements and words associ" |
| 4 | `inspect_feature` | L14, F336 | "the word "no" and related negative words" |
| 5 | `inspect_feature` | L0, F1143 | " the word "no" and related words like "nobody" and "trust"" |
| 6 | `get_upstream_features` | L15:F13061@30, k=10 | L14:F336 (de=13.00) +9 more |
| 7 | `get_upstream_features` | L14:F336@30, k=10 | Emb:" No"@30 (de=33.75) +9 more |
| 8 | `get_upstream_features` | L0:F1143@30, k=10 | Emb:" No"@30 (de=27.00) +9 more |
| 9 | `inspect_feature` | L6, F15886 | " the word "no" and related negative words like "not" or "never," often" |
| 10 | `get_upstream_features` | L6:F15886@30, k=10 | Emb:" No"@30 (de=14.81) +9 more |
| 11 | `inspect_feature` | L12, F8719 | " phrases that start with "no."" |
| 12 | `inspect_feature` | L13, F10768 | " negative sentiments and words like "no" in the context of a discussio" |

**Findings:** The "No" feature at L16:F11298 is driven primarily by the literal token "No" in the prompt (pos 30). The token embeds directly into several lower‑layer detectors. The strongest upstream pathway is: Embedding "No" → early detector L0:F1143 (layer 0) → mid‑layer aggregator L14:F336 (layer 14) → higher aggregator L15:F13061 (layer 15) → final refusal gate L16:F11298. A parallel path goes through L6:F…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L15, F13061 | " uses of the word "no" or similar negative statements and words associ" |
| 2 | `get_upstream_features` | L15:F13061@30, k=15 | L14:F336 (de=13.00) +14 more |
| 3 | `inspect_feature` | L14, F336 | "the word "no" and related negative words" |
| 4 | `inspect_feature` | L12, F8719 | " phrases that start with "no."" |
| 5 | `get_upstream_features` | L14:F336@30, k=15 | Emb:" No"@30 (de=33.75) +14 more |
| 6 | `inspect_feature` | L6, F15886 | " the word "no" and related negative words like "not" or "never," often" |
| 7 | `inspect_feature` | L13, F10768 | " negative sentiments and words like "no" in the context of a discussio" |
| 8 | `get_upstream_features` | L6:F15886@30, k=15 | Emb:" No"@30 (de=14.81) +14 more |
| 9 | `inspect_feature` | L0, F1143 | " the word "no" and related words like "nobody" and "trust"" |
| 10 | `get_upstream_features` | L0:F1143@30, k=10 | Emb:" No"@30 (de=27.00) +9 more |
| 11 | `inspect_feature` | L2, F2771 | " the word "no" as well as words and phrases that are conceptually rela" |

**Findings:** The "No + one" feature at L15:F13061 is driven primarily by a cascade of negation detectors. The strongest upstream driver is a mid‑layer detector (L14:F336) that receives a large excitatory signal directly from the raw token embedding for " No". Additional upstream contributions come from earlier‑layer negation gates at L6 and L0, both of which also receive strong positive influence from the same…

</details>

<details>
<summary><b>SA-3</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F336 | "the word "no" and related negative words" |
| 2 | `get_upstream_features` | L14:F336@30, k=10 | Emb:" No"@30 (de=33.75) +9 more |
| 3 | `inspect_feature` | L0, F1143 | " the word "no" and related words like "nobody" and "trust"" |
| 4 | `get_upstream_features` | L0:F1143@30, k=10 | Emb:" No"@30 (de=27.00) +9 more |
| 5 | `inspect_feature` | L13, F10768 | " negative sentiments and words like "no" in the context of a discussio" |
| 6 | `get_upstream_features` | L13:F10768@30, k=10 | Emb:" No"@30 (de=12.06) +9 more |
| 7 | `inspect_feature` | L12, F8719 | " phrases that start with "no."" |
| 8 | `inspect_feature` | L2, F2771 | " the word "no" as well as words and phrases that are conceptually rela" |
| 9 | `inspect_feature` | L0, F14862 | "the word "no"" |
| 10 | `inspect_feature` | L3, F3266 | " the abbreviation "No." for Number" |
| 11 | `get_upstream_features` | L12:F8719@30, k=10 | Emb:" No"@30 (de=16.50) +9 more |
| 12 | `inspect_feature` | L6, F15886 | " the word "no" and related negative words like "not" or "never," often" |

**Findings:** The negation/refusal feature L14:F336 is driven primarily by the input token "No" at position 30 (direct_effect 33.75). The signal propagates through a hierarchy of low‑level "no" detectors (layers 0, 2, 3, 12, 13) that each contribute positive direct_effects, culminating in the high‑level gate. All traced upstream features reside in layers ≤13, with several in the lower third (layers 0‑3), satisf…

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L10, F16373 | "bigoted statements about minority groups" |
| 2 | `get_upstream_features` | L10:F16373@7, k=10 | Emb:" theorists"@3 (de=1.91) +9 more |
| 3 | `inspect_feature` | L9, F13961 | "political commentary related to Trump and elections" |
| 4 | `get_upstream_features` | L9:F13961@3, k=10 | L8:F12761 (de=6.88) +9 more |
| 5 | `inspect_feature` | L8, F12761 | " words associated with the QAnon conspiracy theory" |
| 6 | `get_upstream_features` | L8:F12761@3, k=10 | Emb:" theorists"@3 (de=4.56) +9 more |
| 7 | `inspect_feature` | L2, F16028 | " terms related to speculation, lies, false information, and conspiracy" |
| 8 | `inspect_feature` | L7, F14725 | " references to religious groups and leaders, particularly instances re" |
| 9 | `get_upstream_features` | L2:F16028@3, k=10 | Emb:" theorists"@3 (de=11.75) +9 more |

**Findings:** The bigoted‑statement feature (L10:F16373) is driven primarily by a cascade of upstream signals: high‑level political commentary (L9:F13961), conspiracy‑theory detectors (L8:F12761, L2:F16028), and a religious‑group reference gate (L7:F14725). The strongest excitatory paths originate from raw input tokens such as "theorists", "piracy", and "Cons" which directly feed the bigoted feature. The tracin…

</details>

<details>
<summary><b>SA-6</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F16028 | " terms related to speculation, lies, false information, and conspiracy" |
| 2 | `get_upstream_features` | L2:F16028@3, k=10 | Emb:" theorists"@3 (de=11.75) +9 more |
| 3 | `inspect_feature` | L0, F13169 | " words referring to people in positions of authority" |
| 4 | `inspect_feature` | L1, F12471 | "words and phrases relating to mechanics, publications, community and m" |
| 5 | `get_upstream_features` | L0:F13169@3, k=5 | Emb:" theorists"@3 (de=10.25) +4 more |
| 6 | `inspect_feature` | L0, F1927 | " words and phrases related to the social sciences, research, and histo" |
| 7 | `get_upstream_features` | L0:F1927@3, k=5 | Emb:" theorists"@3 (de=7.78) +4 more |
| 8 | `get_upstream_features` | L1:F12471@3, k=5 | Emb:" theorists"@3 (de=5.19) +4 more |
| 9 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 10 | `get_upstream_features` | L0:F9026@3, k=5 | Emb:" theorists"@3 (de=25.38) +4 more |

**Findings:** Tracing from the speculation/conspiracy detector (L2:F16028) shows its strongest excitatory drivers are token embeddings " theorists" (pos 3) and "piracy" (pos 2). These feed directly into the target feature and cascade through lower‑layer features (L0:F13169, L0:F1927, L1:F12471, L0:F9026). All intermediate features reside in layers 0‑1, satisfying the lower‑third floor requirement, and the path …

</details>

### Build

`build_circuit` → 17 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 59,402 | 5,526 | 142,907 | 0 | $0.0330 | — | — |
| SA-2 | openai/gpt-oss-120b | 132,701 | 6,028 | 12,768 | 0 | $0.0237 | ✅ 4F/6E | Trace the path from L15:F13061 ("No" + "one" feature) upstre… |
| SA-3 | openai/gpt-oss-120b | 151,912 | 8,820 | 5,120 | 0 | $0.0282 | ✅ 7F/8E | Trace the path from L14:F336 ("No" / negation feature) upstr… |
| SA-1 | openai/gpt-oss-120b | 106,531 | 7,146 | 48,576 | 0 | $0.0210 | ✅ 5F/11E | Trace the path from L16:F11298 (a "No" feature) upstream. Wh… |
| SA-4 | openai/gpt-oss-120b | 90,031 | 7,323 | 5,088 | 0 | $0.0180 | ✅ 4F/23E | Trace L10:F16373 ("bigoted statements about minority groups"… |
| SA-6 | openai/gpt-oss-120b | 122,148 | 10,004 | 2,560 | 0 | $0.0244 | ✅ 5F/15E | Trace L2:F16028 (speculation/conspiracy) upstream to find wh… |
| **Total** | | **662,725** | **44,847** | **217,019** | **0** | **$0.1482** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 15s