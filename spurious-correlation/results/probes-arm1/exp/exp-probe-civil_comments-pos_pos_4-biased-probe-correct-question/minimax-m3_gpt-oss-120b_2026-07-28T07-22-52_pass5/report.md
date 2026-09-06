# Circuit Oracle Report
**Date:** 2026-07-28 07:22:52 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven by a circuit that primarily fires on token-embedding signals from "Indians" and "abusers" (the identity+noun and the toxic-action noun), routed through L0 identity/group-membership features and L2 "abuse"-keyword features, and consolidated by an L3 US-ethnic-group-mentions feature — confirming the user's hypothesis that the classification is triggered by co-occurrence of an identity-group token with a slur-like verb rather than the prompt's overall semantics.

**Confidence:** 7

**Reasoning:** The circuit is anchored at the input by two hot embeddings: `Indians` (pos 1) and `abusers` (pos 3). The "Indians" token drives a *cluster* of low-layer identity features — **L0:F14740** (names of places/people/orgs, frac_nonzero 0.017), **L0:F3283** (mentions of India/Delhi, 0.020), and **L0:F10155** at both pos 1 and pos 3 ("membership in a group" — autointerp examples include "anians", "riders", "natives", i.e. generic group-membership morphology; 0.046). These group-membership features feed into **L3:F13473** ("mentions of racial and ethnic groups, especially in the United States", 0.0057), which has the single highest non-abuse direct effect on the probe direction. The "abusers" embedding drives **L2:F1003** ("the word 'abuse'", 0.007) and **L2:F6255** ("the word 'abuse' or phrases related to genitalia", 0.007) — a stacked, redundant pair where F1003 pushes the probe score up and F6255 partially counteracts (note the strongly negative direct_effects of L0:F4448, L0:F13269, L0:F15504, and L0:F1847 on the abuse features, suggesting learned inhibition). Together these converge on **L7:F15690** ("public sentiment and action in response to a problem", 0.078), which closes the loop back to the probe.

Crucially, the remaining top-15 features are *not* semantic toxicity content. **L0:F11154** (pos 2, "are", +0.65), **L0:F1053** (pos 4, "as", −0.33), **L0:F4199** (pos 7, "quantity", −0.20), **L0:F10389** (pos 12, "problems"/"faults", −0.21), **L0:F3564** (pos 13, mathematical-notation "." +0.19), and **L4:F4021** (pos 4, code-snippet "as", +0.21) are all function-word or high-frequency lexical features with low frac_nonzero that happen to fire on adjacent tokens — they contribute noise around the core identity+abuse signal without representing any coherent semantic content. **L1:F7492** (administrative divisions, −0.24) and the technical-document features L0:F9026/F11835 are similarly off-target.

The circuit is therefore a **two-track coincidence detector**: an identity-token track ("Indians" → L0 group-membership features → L3 ethnic-group-mentions feature) and a slur-track ("abusers" → L2 abuse-keyword features), with the probe direction firing on their conjunction. This is precisely the "spurious identity-group signal" failure mode the user flagged: the probe classifies the text as toxic primarily because an identity label token co-occurs with a negative-action token, not because the model has read the full proposition. The lexical content driving the decision is `[Indians] + [abusers]` plus the lightweight function-word scaffolding around them — not the message-level claim that "Indians are abusers because they only know how to deal with problems by abusing."

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Indians (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: are (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: abusers (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: as (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: stated (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: problems (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: . (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F14740](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14740) | 1 | Identity / group-membership features (L0) |  names of places, people, and organizations | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14740) |
| [L0:F3283](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3283) | 1 | Identity / group-membership features (L0) |  mentions of India and related concepts like Delhi, but sometimes only finds a word indicating importance | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3283) |
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 1 | Identity / group-membership features (L0) |  words related to membership in a group | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 3 | Identity / group-membership features (L0) |  words related to membership in a group | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L2:F1003](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) | 3 | Abuse-keyword features (L2) |  the word "abuse" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1003) |
| [L2:F6255](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6255) | 3 | Abuse-keyword features (L2) |  the word "abuse", or phrases related to genitalia | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6255) |
| [L0:F11154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) | 2 | Function-word / generic lexical features (L0-L4) |  the word "are" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) |
| [L0:F1053](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1053) | 4 | Function-word / generic lexical features (L0-L4) |  the word "as." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1053) |
| [L0:F4199](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4199) | 7 | Function-word / generic lexical features (L0-L4) |  the word "quantity" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4199) |
| [L0:F10389](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10389) | 12 | Function-word / generic lexical features (L0-L4) |  words related to legal disputes and technical issues such as device malfunctions or program errors | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10389) |
| [L4:F4021](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) | 4 | Function-word / generic lexical features (L0-L4) |  code snippets or configurations with the word "as". | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) |
| [L0:F3564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3564) | 13 | Function-word / generic lexical features (L0-L4) | mathematical notation symbols | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3564) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | US ethnic-group mentions feature (L3) |  mentions of racial and ethnic groups, especially in the United States | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L7:F15690](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) | 3 | Public-sentiment/response feature (L7) |  text related to public sentiment and action in response to a problem | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15690) |
| [L1:F7492](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7492) | 1 | Misc L1 / L2 features (administrative-divisions, etc.) | words referring to administrative divisions, animals, or commercial elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7492) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:11154 de=0.652 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F11154@2` | ❌ error | — | — | Trace the path from L0:F11154 (pos 2) — this has the highest direct_effect (+0.6… |
| SA-2 | `L2:F1003@3` | ❌ error | — | — | Trace the path from L2:F1003 (pos 3) — direct_effect +0.30. What does this featu… |
| SA-3 | `L3:F13473@2` | ❌ error | — | — | Trace the path from L3:F13473 (pos 2) — direct_effect +0.29. What does this feat… |
| SA-4 | `L0:F1053@4` | ❌ error | — | — | Trace the path from L0:F1053 (pos 4) — has the largest NEGATIVE direct_effect (-… |
| SA-5 | `L0:F10155@3` | ❌ error | — | — | Trace the path from L0:F10155 (pos 3) — direct_effect +0.21. What does this feat… |
| SA-6 | `L4:F4021@4` | ❌ error | — | — | Trace the path from L4:F4021 (pos 4) — direct_effect +0.21. What does this featu… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×14 | L0:11154, L2:1003, L3:13473, L0:1053, L4:4021, L0:10155, L0:14740, L0:3283, L0:10389, L0:4199, L7:15690, L1:7492, L2:6255, L0:3564 |
| 2 | `get_upstream_features` | L0:F11154@2, k=10 → Emb:" are"@2 (de=36.00) +9 more |
| 3 | `get_upstream_features` | L2:F1003@3, k=10 → Emb:" abusers"@3 (de=14.00) +9 more |
| 4 | `get_upstream_features` | L3:F13473@2, k=10 → Emb:"Indians"@1 (de=10.25) +9 more |
| 5 | `get_upstream_features` | L0:F1053@4, k=10 → Emb:" as"@4 (de=34.25) +9 more |
| 6 | `get_upstream_features` | L4:F4021@4, k=10 → Emb:" as"@4 (de=27.00) +9 more |
| 7 | `get_upstream_features` | L0:F10155@3, k=10 → Emb:" abusers"@3 (de=13.88) +9 more |
| 8 | `get_upstream_features` | L0:F10389@12, k=10 → Emb:" problems"@12 (de=17.38) +9 more |
| 9 | `get_upstream_features` | L0:F4199@7, k=10 → Emb:" stated"@7 (de=15.31) +9 more |
| 10 | `get_upstream_features` | L0:F3283@1, k=10 → Emb:"Indians"@1 (de=7.34) +9 more |
| 11 | `get_upstream_features` | L0:F14740@1, k=10 → Emb:"Indians"@1 (de=8.75) +9 more |
| 12 | `get_upstream_features` | L7:F15690@3, k=10 → Emb:" abusers"@3 (de=1.68) +9 more |
| 13 | `get_upstream_features` | L1:F7492@1, k=10 → Emb:"Indians"@1 (de=9.31) +9 more |
| 14 | `get_upstream_features` | L2:F6255@3, k=10 → Emb:" abusers"@3 (de=14.06) +9 more |
| 15 | `get_upstream_features` | L0:F3564@13, k=10 → Emb:" ."@13 (de=35.75) +9 more |
| 16 | `get_upstream_features` | L0:F11835@3, k=5 → Emb:" abusers"@3 (de=7.09) +4 more |
| 17 | `get_upstream_features` | L0:F9026@3, k=5 → Emb:" abusers"@3 (de=22.50) +4 more |
| 18 | `get_upstream_features` | L0:F10155@1, k=5 → Emb:"Indians"@1 (de=13.12) +4 more |
| 19 | `inspect_feature` ×2 | L0:11835, L0:9026 |

### Build

`build_circuit` → 14 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 37,118 | 5,417 | 148,194 | 0 | $0.0265 | — | — |
| **Total** | | **37,118** | **5,417** | **148,194** | **0** | **$0.0265** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 1s