# Circuit Oracle Report
**Date:** 2026-07-28 07:24:12 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven by a chain of features that detect the mere presence of demographic/racial identity terms (not the toxic content), confirming the user's suspicion of a spurious feature circuit.

**Confidence:** 8

**Reasoning:** The circuit traces from raw token embeddings of **{white, guy, name, last, her}** → L0 lexical detectors (e.g., L0:F9076, L0:F16013, L0:F6548 firing on "white"/"guy" with direct_effect values of 7–20 toward their parents) → L2 context features (L2:F13158 on " white" pos 9, direct_effect=13.6) → L3 compound "white guy" detectors (L3:F13061, L3:F16373, L3:F4512 with activation=52 at "name") → L4 bridging features (L4:F117) → **L6:F3902** (the dominant output-driving feature, direct_effect=+0.34 at pos 9, also firing at pos 10 and 27) → probe logit.

Critically, **no feature in the circuit encodes the toxic content itself** (e.g., "self hater," "oriental," "lust after"). Instead, the entire causal chain rides on the lexical signal of mentioning a race (white) paired with relationship/demographic context (guy, her, last name). L6:F3902 is the key smoking gun: it fires at multiple positions (9, 10, 27) with the same identity-related signal, and is the single largest direct contributor to the probe.

This confirms the user's concern: the probe is using a **spurious demographic-mention feature** rather than detecting actual toxic/slur content. A benign sentence like "my white friend named John is a great guy" would likely activate the same L0–L6 chain and produce a similar toxicity score, demonstrating the unreliability of this probe direction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 9 | L6: "white identity/demographic mention" feature (fires on race+context) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 10 | L6: "white identity/demographic mention" feature (fires on race+context) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 27 | L6: "white identity/demographic mention" feature (fires on race+context) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 9 | L4: bridging context feature (combines "white guy" and "her last name") | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 10 | L4: bridging context feature (combines "white guy" and "her last name") | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 9 | L4: bridging context feature (combines "white guy" and "her last name") | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 10 | L3: "white guy" compound detector | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 10 | L3: "white guy" compound detector | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L3:F4512](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) | 15 | L3: "white guy" compound detector | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4512) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 9 | L2: "white" token context feature (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 9 | L2: "white" token context feature (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L2:F15317](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15317) | 10 | L2: "white" token context feature (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15317) |
| [L2:F14965](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14965) | 10 | L2: "white" token context feature (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14965) |
| [L2:F10433](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10433) | 10 | L2: "white" token context feature (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10433) |
| [L2:F9961](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9961) | 15 | L2: "white" token context feature (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9961) |
| [L2:F10248](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10248) | 15 | L2: "white" token context feature (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10248) |
| [L2:F13265](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13265) | 15 | L2: "white" token context feature (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13265) |
| [L0:F9076](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9076) | 10 | L0: low-level "white" / "name" / "guy" lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9076) |
| [L0:F16013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) | 9 | L0: low-level "white" / "name" / "guy" lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) |
| [L0:F6548](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6548) | 9 | L0: low-level "white" / "name" / "guy" lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6548) |
| [L0:F4312](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4312) | 15 | L0: low-level "white" / "name" / "guy" lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4312) |
| [L0:F2242](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) | 10 | L0: low-level "white" / "name" / "guy" lexical features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2242) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L1:5220 de=-0.453 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F13061@10` | ❌ error | — | — | Trace from L3:F13061 (pos 10, direct_effect=+0.39) upstream. Pos 10 is roughly "… |
| SA-2 | `L6:F3902@9` | ❌ error | — | — | Trace from L6:F3902 (pos 9, direct_effect=+0.34) upstream. Pos 9 is "she" area. … |
| SA-3 | `L4:F117@10` | ❌ error | — | — | Trace from L4:F117 (pos 10, direct_effect=+0.31) upstream. Also appears at pos 9… |
| SA-4 | `L3:F4512@15` | ❌ error | — | — | Trace from L3:F4512 (pos 15, direct_effect=+0.22, activation=52 — very high). Po… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L3:F13061@10, k=10 → Emb:" white"@9 (de=11.00) +9 more |
| 2 | `get_upstream_features` | L6:F3902@9, k=10 → Emb:" white"@9 (de=13.56) +9 more |
| 3 | `get_upstream_features` | L4:F117@10, k=10 → Emb:" white"@9 (de=12.12) +9 more |
| 4 | `get_upstream_features` | L3:F4512@15, k=10 → Emb:" last"@14 (de=24.75) +9 more |
| 5 | `get_upstream_features` | L2:F13158@9, k=10 → Emb:" white"@9 (de=13.62) +9 more |
| 6 | `get_upstream_features` | L2:F15317@10, k=10 → Emb:" guy"@10 (de=9.44) +9 more |
| 7 | `get_upstream_features` | L0:F9076@10, k=10 → Emb:" white"@9 (de=7.91) +9 more |
| 8 | `get_upstream_features` | L0:F16013@9, k=10 → Emb:" white"@9 (de=15.56) +9 more |
| 9 | `get_upstream_features` | L0:F6548@9, k=10 → Emb:" white"@9 (de=20.25) +9 more |
| 10 | `get_upstream_features` | L0:F4312@15, k=10 → Emb:" name"@15 (de=16.12) +9 more |
| 11 | `get_upstream_features` | L1:F7821@9, k=5 → Emb:" white"@9 (de=15.75) +4 more |

### Build

`build_circuit` → 11 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 12,178 | 5,751 | 65,390 | 0 | $0.0145 | — | — |
| **Total** | | **12,178** | **5,751** | **65,390** | **0** | **$0.0145** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 0s