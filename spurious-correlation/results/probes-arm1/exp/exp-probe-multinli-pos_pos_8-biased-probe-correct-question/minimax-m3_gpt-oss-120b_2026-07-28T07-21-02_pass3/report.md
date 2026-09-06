# Circuit Oracle Report
**Date:** 2026-07-28 07:21:02 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "contradiction" score is driven by content-bearing political/legal vocabulary features — primarily entities ("Congress"), nouns ("funding", "levels", "control", "many", "who"), and the domain concept of political parties/legal counsel — not by negation or function-word heuristics.

**Confidence:** 6

**Reasoning:** All upstream traces bottom out in **token-embedding nodes** for content words from the premise sentence: `Emb: ' Congress' (pos 2)` (direct_effect=20.6→L3:F123, 28.1→L2:F2701, 9.1→L2:F6735, 13.8→L6:F6096), `Emb: ' funding' (pos 7)` (20.1→L0:F11606, 14.1→L1:F2116), `Emb: ' levels' (pos 8)` (28.0→L2:F156), `Emb: ' many' (pos 13)` (23.5→L3:F8382), `Emb: ' controls' (pos 5)` (18.5→L3:F13271), and `Emb: ' who' (pos 15)` (35.3→L0:F13437). The features driving the probe are semantic entity/role detectors: **L3:F123** "U.S. Congress" (direct_effect=+0.36), **L3:F13271** "control" (+0.36), **L3:F8382** "many" (+0.33), **L2:F156** "amount/intensity (levels)" (+0.37 pushing *away*), **L2:F2701** "U.S. Congress" (+0.38), **L2:F6735** "political parties/politicians" (-0.40), **L6:F6096** "political parties/affiliations" (+0.45), and **L1:F2116** "legal counsel/representation" (+0.38). Notably, no "negation" feature appears; the inhibitory features (L2:F156 "levels", L2:F6735 "parties") are content words from the *hypothesis* sentence (which lacks "Congress" as a specific named entity and reframes "controls funding" as "no responsibility...funding"), not negation signals. The user's concern is **not supported** by this circuit: the probe's classification of the SNLI-style premise/hypothesis pair is grounded in overlap of political/legal vocabulary entities between the two sentences, not in spurious negation cues. The only mildly concerning element is that some L0 detectors (e.g., L0:F13437 "who" at frac_nonzero=0.013, L0:F11606 "fund" at 0.016) are generic word-identity features rather than deep semantic features — but they feed into a legitimate content-recognition path (who→legal counsel, fund→counsel/representation) that is consistent with NLI reasoning, not a heuristic shortcut.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F6044](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) | 2 | L0: 'Congress'/'yield' word detectors (pos 2) | the word "yield" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6044) |
| [L0:F6948](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6948) | 2 | L0: 'Congress'/'yield' word detectors (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6948) |
| [L0:F9557](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) | 2 | L0: 'Congress'/'yield' word detectors (pos 2) | the word "clean" and words/phrases associated with people | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9557) |
| [L0:F11606](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11606) | 7 | L0: 'fund'/'who'/'physical' word detectors |  the word "fund" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11606) |
| [L0:F13437](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) | 15 | L0: 'fund'/'who'/'physical' word detectors | the word "who" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13437) |
| [L0:F9529](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9529) | 5 | L0: 'fund'/'who'/'physical' word detectors | the word "physical" and words related to programming | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9529) |
| [L1:F2116](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) | 7 | L1: legal counsel/representation (pos 7) |  words and phrases related to legal counsel or representation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2116) |
| [L2:F2701](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) | 2 | L2: U.S. Congress / political parties (pos 2) |  words related to the U.S. Congress | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2701) |
| [L2:F6735](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) | 2 | L2: U.S. Congress / political parties (pos 2) |  political parties and politicians | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6735) |
| [L2:F156](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) | 8 | L2: U.S. Congress / political parties (pos 2) |  words related to the amount or intensity of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/156) |
| [L3:F123](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) | 2 | L3: Congress / control / many word detectors |  mentions of the United States Congress | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/123) |
| [L3:F13271](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) | 5 | L3: Congress / control / many word detectors |  the word "control." | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13271) |
| [L3:F8382](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) | 13 | L3: Congress / control / many word detectors |  the word "many", and sometimes "times" or "people" when near it | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8382) |
| [L6:F6096](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) | 2 | L6: political parties/affiliations (pos 2) |  political parties and affiliations | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6096) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:6044 de=0.789 |
| 3 | `inspect_feature` ×14 | L0:6044, L0:13437, L6:6096, L2:6735, L1:2116, L1:6948, L2:2701, L3:123, L3:13271, L3:8382, L2:156, L0:11606, L0:9557, L0:9529 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F6096@2` | ❌ error | — | — | Trace this feature upstream to find what tokens/features drive it. Look for embe… |
| SA-2 | `L3:F123@2` | ❌ error | — | — | Trace upstream to find what drives the US Congress feature. Look for embedding n… |
| SA-3 | `L3:F8382@13` | ❌ error | — | — | Trace upstream to find what drives the 'many' feature. Look for embedding nodes. |
| SA-4 | `L3:F13271@5` | ❌ error | — | — | Trace upstream to find what drives the 'control' feature. Look for embedding nod… |
| SA-5 | `L2:F156@8` | ❌ error | — | — | Trace upstream to find what drives the 'levels' feature. Look for embedding node… |
| SA-6 | `L1:F2116@7` | ❌ error | — | — | Trace upstream to find what drives the 'legal counsel' feature. Look for embeddi… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F6096@2, k=15 → Emb:" Congress"@2 (de=13.81) +14 more |
| 2 | `get_upstream_features` | L3:F123@2, k=15 → Emb:" Congress"@2 (de=20.62) +14 more |
| 3 | `get_upstream_features` | L3:F8382@13, k=15 → Emb:" many"@13 (de=23.50) +14 more |
| 4 | `get_upstream_features` | L3:F13271@5, k=15 → Emb:" controls"@5 (de=18.50) +14 more |
| 5 | `get_upstream_features` | L2:F156@8, k=15 → Emb:" levels"@8 (de=28.00) +14 more |
| 6 | `get_upstream_features` | L1:F2116@7, k=15 → Emb:" funding"@7 (de=14.12) +14 more |
| 7 | `get_upstream_features` | L0:F13437@15, k=15 → Emb:" who"@15 (de=35.25) +14 more |
| 8 | `get_upstream_features` | L2:F6735@2, k=10 → Emb:" Congress"@2 (de=9.12) +9 more |
| 9 | `get_upstream_features` | L2:F2701@2, k=10 → Emb:" Congress"@2 (de=28.12) +9 more |
| 10 | `get_upstream_features` | L0:F6044@2, k=10 → Emb:" Congress"@2 (de=17.00) +9 more |
| 11 | `get_upstream_features` | L0:F11606@7, k=10 → Emb:" funding"@7 (de=20.12) +9 more |

### Build

`build_circuit` → 13 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 37,456 | 4,212 | 140,982 | 0 | $0.0248 | — | — |
| **Total** | | **37,456** | **4,212** | **140,982** | **0** | **$0.0248** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 9s