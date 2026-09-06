# Circuit Oracle Report
**Date:** 2026-07-28 07:20:55 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive toxicity classification is driven by late-layer "race/ethnicity identity group" detector features (L2:F13158, L4:F117, L6:F3902) that are excited by the mere presence of identity-group noun tokens like "white," "black," and "nonwhites" — not by the actual toxic content of the message.

**Confidence:** 8

**Reasoning:** The circuit confirms the user's concern. The terminal node is the toxicity probe direction; the strongest direct contributors are **L2:F13158** ("words about race and ethnicity," pos 15/25/32/40) and **L4:F117** ("terms related to race, racism, and social justice, with a particular focus on terms related to Black people," pos 9/32) and **L6:F3902** ("terms referring to race and ethnicity," pos 25/40). These features promote tokens like "racial," "racist," "racism," "minorities," "ethnicity" — generic identity-group vocabulary rather than slur, threat, or attack language.

Crucially, these detectors are activated almost entirely by **token-embedding nodes** for identity nouns:
- L2:F13158 at pos 32 is driven by the "black" embedding (direct_effect 10.5 from Emb, plus Emb "nonwhites" at pos 40 with direct_effect 0.32 and "white" at pos 15 with direct_effect 1.19).
- L6:F3902 at pos 25 is driven by the "white" embedding (direct_effect 10.81) plus the "America" embedding (1.26) and an upstream L4:F117 race/racism feature also excited by the same "white" token.
- L4:F117 at pos 9 is driven by the "ot" subword embedding (3.52, the negation "not" inside "bigot") and by L3:F15009 ("courts, legalese, mental states" — actually promoting "prejudice/bias") and L3:F12367 (government/law) — note this is triggered by the word **"bigot"**, which is the only true toxicity-bearing content in the prompt.

The low-layer supernode (sn_low_lex) contains generic function-word and entity detectors — "clearly" (L0:5707, L1:2407, L0:6154), "and" (L0:3255), "other" (L0:7969), "trump" (L4:14582 driven by Emb "trump" at 18.13), "." (L0:6051), and a color detector (L0:16013 firing on "black" as a color). The mid-layer supernode (sn_mid_context) adds social-justice and protest amplifiers (L1:F13646, L2:F9433) that inflate the late-layer race detectors' signal.

In short, the probe fires because the sentence **names racial groups** ("trump," "white bigots," "white," "black," "nonwhites," "Obama") — identity-group vocabulary the model has learned is statistically correlated with toxicity training labels. The actual toxic content is just the word "bigot" plus structural markers like "tie clearly shows" and "hence." The mechanism is **identity-group token detection**, not toxicity-content detection: this is the textbook "spurious correlate" the user flagged, and it would misfire on benign sentences that simply discuss racial groups (e.g., a sociology article, a census description, or a statement like "Black and white voters both turned out").

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (toxicity direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 25 | Late-layer race/ethnicity detectors (push probe toward positive class) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 40 | Late-layer race/ethnicity detectors (push probe toward positive class) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 9 | Late-layer race/ethnicity detectors (push probe toward positive class) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 32 | Late-layer race/ethnicity detectors (push probe toward positive class) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 15 | Late-layer race/ethnicity detectors (push probe toward positive class) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 25 | Late-layer race/ethnicity detectors (push probe toward positive class) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 32 | Late-layer race/ethnicity detectors (push probe toward positive class) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 40 | Late-layer race/ethnicity detectors (push probe toward positive class) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L5:F8030](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) | 3 | Mid-layer social-context amplifiers (social justice, protest, legal, technical) |  language discussing differences, clarity, and definition | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 32 | Mid-layer social-context amplifiers (social justice, protest, legal, technical) | text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L3:F15009](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15009) | 9 | Mid-layer social-context amplifiers (social justice, protest, legal, technical) | words or phrases related to courts, legalese, and mental states | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15009) |
| [L3:F12367](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12367) | 9 | Mid-layer social-context amplifiers (social justice, protest, legal, technical) | words related to government, law, and locations. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12367) |
| [L2:F9433](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9433) | 9 | Mid-layer social-context amplifiers (social justice, protest, legal, technical) | words related to civil unrest, political action, and disagreement | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9433) |
| [L2:F9093](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9093) | 9 | Mid-layer social-context amplifiers (social justice, protest, legal, technical) | words related to systems, scientific and engineering | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9093) |
| [L0:F5707](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) | 2 | Low-layer generic lexical detectors (function words, color/name tokens) |  words or phrases related to knowledge or perspective | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5707) |
| [L1:F2407](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) | 2 | Low-layer generic lexical detectors (function words, color/name tokens) |  the word "clearly" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2407) |
| [L0:F6154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6154) | 2 | Low-layer generic lexical detectors (function words, color/name tokens) |  uses of 'clearly' and nearby words that are related to arguments and writing | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6154) |
| [L0:F16013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) | 32 | Low-layer generic lexical detectors (function words, color/name tokens) | mentions of the color blue, and perhaps colors in general or the components of a graphic image | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 10 | Low-layer generic lexical detectors (function words, color/name tokens) |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F7969](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) | 14 | Low-layer generic lexical detectors (function words, color/name tokens) |  the word "other" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 18 | Low-layer generic lexical detectors (function words, color/name tokens) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F7142](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) | 2 | Low-layer generic lexical detectors (function words, color/name tokens) |  the word "axis" and its plural form, often in the context of scientific or technical documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) |
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | Low-layer generic lexical detectors (function words, color/name tokens) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |
| [L6:F1707](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1707) | 1 | Low-layer generic lexical detectors (function words, color/name tokens) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1707) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:5707 de=-0.346 |
| 3 | `inspect_feature` ×10 | L2:13158, L0:5707, L0:3255, L4:117, L0:6154, L0:7142, L5:8030, L0:7969, L1:2407, L6:3902 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F13158@32` | ✅ reported | 3 | 7 | Trace upstream from L2:F13158 ("words about race and ethnicity") at position 32.… |
| SA-2 | `L6:F3902@25` | ❌ error | — | — | Trace upstream from L6:F3902 ("terms referring to race and ethnicity") at positi… |
| SA-3 | `L4:F117@9` | ✅ reported | 8 | 10 | Trace upstream from L4:F117 ("terms related to race, racism, and social justice,… |

<details>
<summary><b>SA-1</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 2 | `get_upstream_features` | L2:F13158@32, k=10 | Emb:" black"@32 (de=10.50) +9 more |
| 3 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |
| 4 | `get_upstream_features` | L1:F13646@32, k=10 | Emb:" black"@32 (de=4.25) +9 more |
| 5 | `inspect_feature` | L0, F16013 | " mentions of the color blue, and perhaps colors in general or the comp" |

**Findings:** The strongest positive driver of the race/ethnicity detector (L2:F13158) is the raw token embedding for "black" (direct_effect 10.5). A secondary upstream feature in layer 1 (F13646) captures social‑justice language and also receives strong excitation from the same "black" embedding (4.25). Both paths converge on the target feature, and the chain reaches layer 0 (F16013), a generic color detector,…

</details>

<details>
<summary><b>SA-3</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 2 | `get_upstream_features` | L4:F117@9, k=10 | Emb:"ot"@9 (de=3.52) +9 more |
| 3 | `inspect_feature` | L3, F15009 | "words or phrases related to courts, legalese, and mental states" |
| 4 | `inspect_feature` | L3, F12367 | " words related to government, law, and locations." |
| 5 | `inspect_feature` | L2, F9433 | " words related to civil unrest, political action, and disagreement" |
| 6 | `get_upstream_features` | L3:F15009@9, k=10 | Emb:"ot"@9 (de=6.75) +9 more |
| 7 | `get_upstream_features` | L3:F12367@9, k=10 | Emb:" big"@8 (de=20.62) +9 more |
| 8 | `inspect_feature` | L2, F9093 | " words related to systems, scientific and engineering" |
| 9 | `get_upstream_features` | L3:F15009@9, k=10 | Emb:"ot"@9 (de=6.75) +9 more |
| 10 | `inspect_feature` | L2, F8105 | "scientific and technical terms, particularly related to medicine and b" |
| 11 | `get_upstream_features` | L2:F9093@9, k=10 | Emb:" big"@8 (de=12.56) +9 more |

**Findings:** The race‑related L4:F117 feature receives its strongest positive push from the input subword embedding "ot" (part of the negation word "not"), indicating that a negation cue can amplify race‑topic detection. Additional upstream drivers include mid‑level legal/government features (L3:15009, L3:12367) and a civil‑unrest detector (L2:9433). These in turn are fed by low‑layer embeddings such as "big" …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F3902@25, k=15 → Emb:" white"@25 (de=10.81) +14 more |
| 2 | `get_upstream_features` | L5:F8030@3, k=15 → Emb:" clearly"@2 (de=18.25) +14 more |
| 3 | `get_upstream_features` | L4:F14582@5, k=10 → Emb:" trump"@5 (de=18.12) +9 more |
| 4 | `get_upstream_features` | L6:F1707@1, k=10 → L4:F8223 (de=4.09) +9 more |
| 5 | `get_upstream_features` | L0:F7969@14, k=10 → Emb:" other"@14 (de=42.25) +9 more |
| 6 | `get_upstream_features` | L0:F3255@10, k=10 → Emb:" and"@10 (de=36.75) +9 more |
| 7 | `get_upstream_features` | L0:F6051@18, k=10 → Emb:"."@18 (de=45.75) +9 more |

### Build

`build_circuit` → 6 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 25,159 | 3,633 | 113,639 | 0 | $0.0187 | — | — |
| SA-1 | openai/gpt-oss-120b | 42,029 | 3,326 | 32 | 0 | $0.0083 | ✅ 3F/7E | Trace upstream from L2:F13158 ("words about race and ethnici… |
| SA-3 | openai/gpt-oss-120b | 114,097 | 8,230 | 20,352 | 0 | $0.0224 | ✅ 8F/10E | Trace upstream from L4:F117 ("terms related to race, racism,… |
| **Total** | | **181,285** | **15,189** | **134,023** | **0** | **$0.0494** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 13s