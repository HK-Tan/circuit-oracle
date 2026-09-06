# Circuit Oracle Report
**Date:** 2026-07-28 07:21:36 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven by a chain of identity-group-mention features (white, black, bigot, race, nonwhites) that activate as a generic "race/ethnicity vocabulary" detector, with clarity/argumentative structure features providing minor additional signal.

**Confidence:** 7

**Reasoning:**

The circuit traces a clear identity-token → race-feature → probe pipeline, not a content-aware toxicity mechanism:

**Token level (Emb):** Direct_effect on early features is dominated by identity-group embeddings: the `black` token at pos 32 (direct_effect 10.5 → L2:F13158), `white` at pos 25 (10.8 → L6:F3902), `white` at pos 15 (12.8 → L2:F13158), `race` at pos 40 (13.6), and `other` at pos 14. The structural/argumentative connectors (`and` at pos 10, `clearly` at pos 2, `clearly` at pos 3) carry smaller but non-trivial effects.

**Feature-level trace:**
- **L1:F13646** ("social justice issues", frac_nonzero 0.012) fires at every race-token position (pos 15, 32, 40).
- **L2:F13158** ("words about race and ethnicity", frac_nonzero 0.010, promoted tokens: ethnic, queer, LGBT, Hispanic, Muslim, Jewish) fires at the same positions — promoted tokens reveal it's a general identity-group vocabulary detector, not a toxicity detector.
- **L4:F117** ("terms related to race, racism, and social justice… focus on terms related to Black people", frac_nonzero 0.012, promoted: racially, racial, Racism, racist, racism) consolidates the signal at pos 9 ("bigot") and pos 25 ("white").
- **L6:F3902** ("terms referring to race and ethnicity", frac_nonzero 0.018, promoted: minorities, ethnicity, minority) is the deepest race-specific feature in the top set, feeding the probe.
- **L0:F3255** (`and`, frac_nonzero 0.030), **L0:F7969** (`other`, frac_nonzero 0.014), **L0:F5707** (perception/knowledge language), **L0:F6154** (`clearly` in arguments), **L1:F2407** (`clearly`), and **L5:F8030** ("differences, clarity, definition") are all generic lexical/structural features with no semantic connection to toxic content.

**Spurious-cue diagnosis (consistent with the user's concern):** The probe is driven primarily by *the mere presence of identity-group vocabulary* (white, black, bigot, race, nonwhites) routed through a chain of "race/ethnicity detector" features whose promoted tokens are *identity labels*, not toxicity signals. The "social justice" feature (L1:F13646), the "racism-focused" feature (L4:F117), and the "race/ethnicity terms" feature (L6:F3902) are essentially a stacked identity-recognition circuit. Any sentence containing words like "white," "black," "race," "ethnicity," "bigot" — even neutral descriptive discussion or anti-racist argumentation — would light up the same features and push the probe score up. The generic connector words (and, other, clearly) provide additional weak signal, but the dominant, well-motivated path is identity-vocabulary → race detector → probe.

This is exactly the spurious-cue mechanism the user suspects: the probe uses an "identity group is mentioned" feature rather than encoding actual toxic content, lexical slurs, or semantic toxicity cues. A counterfactual sentence like "I have white and black friends of many races" would likely score similarly.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Identity group tokens (white, black, bigot, race, nonwhites) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 15 | Early race/identity recognition features |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 32 | Early race/identity recognition features |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 40 | Early race/identity recognition features |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 15 | Mid-layer race/ethnicity features (activated at multiple identity positions) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 25 | Mid-layer race/ethnicity features (activated at multiple identity positions) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 32 | Mid-layer race/ethnicity features (activated at multiple identity positions) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 40 | Mid-layer race/ethnicity features (activated at multiple identity positions) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 9 | Race/racism/social-justice features |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 25 | Race/racism/social-justice features |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L5:F8030](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) | 3 | Clarity/difference language features (clearly, and, other) |  language discussing differences, clarity, and definition | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8030) |
| [L4:F15009](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15009) | 9 | Clarity/difference language features (clearly, and, other) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15009) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 25 | Late-layer race/ethnicity terms feature |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (toxicity classification score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:5707 de=-0.346 |
| 3 | `inspect_feature` ×8 | L0:5707, L2:13158, L1:2407, L0:6154, L0:3255, L0:7969, L6:3902, L5:8030 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F13158@32` | ❌ error | — | — | Trace upstream from L2:F13158 (race/ethnicity words) at pos 32. Identify what to… |
| SA-2 | `L6:F3902@25` | ❌ error | — | — | Trace upstream from L6:F3902 (race/ethnicity terms) at pos 25. Identify which ea… |
| SA-3 | `L0:F7969@14` | ❌ error | — | — | Trace upstream from L0:F7969 (the word "other") at pos 14. Identify which tokens… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F13158@32, k=10 → Emb:" black"@32 (de=10.50) +9 more |
| 2 | `get_upstream_features` | L6:F3902@25, k=10 → Emb:" white"@25 (de=10.81) +9 more |
| 3 | `get_upstream_features` | L0:F7969@14, k=8 → Emb:" other"@14 (de=42.25) +7 more |
| 4 | `get_upstream_features` | L0:F3255@10, k=8 → Emb:" and"@10 (de=36.75) +7 more |
| 5 | `get_upstream_features` | L4:F117@9, k=5 → Emb:"ot"@9 (de=3.52) +4 more |
| 6 | `get_upstream_features` | L5:F8030@3, k=5 → Emb:" clearly"@2 (de=18.25) +4 more |
| 7 | `get_upstream_features` | L2:F13158@40, k=5 → Emb:" race"@40 (de=13.62) +4 more |
| 8 | `get_upstream_features` | L2:F13158@15, k=5 → Emb:" white"@15 (de=12.81) +4 more |
| 9 | `inspect_feature` ×3 | L4:117, L1:13646, L3:15009 |

### Build

`build_circuit` → 7 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 25,416 | 3,429 | 115,691 | 0 | $0.0187 | — | — |
| **Total** | | **25,416** | **3,429** | **115,691** | **0** | **$0.0187** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 59s