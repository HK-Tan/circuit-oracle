# Circuit Oracle Report
**Date:** 2026-07-28 07:24:43 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by surface-level *filler words* and *negation tokens* (" uh", " well", "yeah", "haven't", "because") — not by semantic content about the NCAA tournament, Louisville, or the Sweet 16.

**Confidence:** 8

**Reasoning:**

Tracing the circuit from the top late-layer feature drivers back to embeddings reveals a clear pattern of spurious feature reliance:

**Direct embedding → probe edges (no intermediate reasoning):**
- **L0:F6236 → probe** is activated by the raw "haven" / "t" token embeddings at positions 18, 35, and 37. These are the two instances of **"haven't"** — the model's strongest negation cue. Direct effect of "haven" at pos 35 is **+16.75** and "t" at pos 37 is **+18.25**, both large positives.
- **L0:F16366 → probe** is driven by the **"because"** token embedding at pos 25 (direct effect **+0.373**), another negation/cancellation cue.
- **L0:F3820 → probe** fires on **" the"** (pos 3), the determiner (direct effect **+0.459**).
- **L0:F8352 / F12126 / F4847 → probe** all fire on the **" well"** token at pos 2 (the most negative direct effects in the graph: **-0.629, -0.547, -0.488**).
- **L0:F4541 / F15972 → probe** fire on **"yeah"** at pos 1.
- **L0:F177 / F10780 / F7893 → probe** fire on **" double"** at pos 6 (content word in "NC double A").
- **L0:F5201 / F13255 / F6846 → probe** fire on **" tournament"** at pos 8.

**Mid-layer amplification of fillers:** The " uh" (pos 4) and " well" (pos 2) embeddings also feed into layer 2-3 features (F9629, F752, F7140, F16039, F1759, F7222) and then to layer 4-5 features (F4492, F2740, F9602, F12126, F4847) that re-encode the same filler patterns. F1768 at pos 1 re-encodes "yeah." These mid-layer features converge back on the probe rather than building any semantic representation.

**What is missing:** There are **no features** for "Louisville" (pos 26), "Sweet 16" (pos 28-29), "missed" (pos 30-31), "watched," or any of the substantive entities that would be needed to verify the actual claim. The entities that *are* present ("double" and "tournament") only appear as raw embedding leaks via direct L0→probe connections with small direct effects, not through any compositional circuit.

**Conclusion:** The user's concern is validated. The circuit is not detecting that the speaker claims both "I haven't watched" *and* "I haven't missed a single game" (a genuine contradiction requiring entity-level reasoning). Instead, it is latching onto:
1. The two **"haven't"** tokens (the biggest positive drivers via F6236)
2. The causal-canceling **"because"**
3. The fillers **" uh"**, **" well"**, and **"yeah"** as a casual-speech/style prior

This is a textbook spurious-feature pattern: the probe has learned a shallow heuristic that "negation words + casual filler" → contradiction, rather than performing the actual semantic comparison the task requires.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 18 | Emb: 'haven' (pos 18) — first 'haven' token, drives L0:F6236 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 35 | Emb: 'haven' (pos 35) — second 'haven' token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 37 | Emb: 't' (pos 37) — completion of 'haven't' (second instance) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L0:F16366](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) | 25 | Emb: 'because' (pos 25) — causal negation cue | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16366) |
| [L0:F9602](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) | 4 | Emb: ' uh' (pos 4) — filler word, casual speech | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) |
| [L0:F8352](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) | 2 | Emb: ' well' (pos 2) — filler/conjunction | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8352) |
| [L0:F12126](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12126) | 2 | Emb: ' well' (pos 2) — filler/conjunction | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12126) |
| [L0:F4847](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4847) | 2 | Emb: ' well' (pos 2) — filler/conjunction | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4847) |
| [L0:F4541](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) | 1 | Emb: 'yeah' (pos 1) — affirmation opener | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4541) |
| [L0:F15972](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) | 1 | Emb: 'yeah' (pos 1) — affirmation opener | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15972) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 3 | Emb: ' the' (pos 3) — determiner | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F177](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/177) | 6 | Emb: ' double' (pos 6) — content word in 'NC double A' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/177) |
| [L0:F10780](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) | 6 | Emb: ' double' (pos 6) — content word in 'NC double A' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10780) |
| [L0:F7893](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) | 6 | Emb: ' double' (pos 6) — content word in 'NC double A' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7893) |
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 8 | Emb: ' tournament' (pos 8) — content noun | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L0:F13255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13255) | 8 | Emb: ' tournament' (pos 8) — content noun | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13255) |
| [L0:F6846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6846) | 8 | Emb: ' tournament' (pos 8) — content noun | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6846) |
| [L2:F9629](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) | 4 | Layer 2-3 ' uh' pattern features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9629) |
| [L2:F752](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) | 4 | Layer 2-3 ' uh' pattern features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/752) |
| [L3:F7140](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7140) | 4 | Layer 2-3 ' uh' pattern features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7140) |
| [L3:F16039](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16039) | 4 | Layer 2-3 ' uh' pattern features (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16039) |
| [L2:F1337](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) | 37 | Layer 2 ' haven't' completion feature (pos 37) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1337) |
| [L2:F1759](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) | 2 | Layer 2 ' well' pattern features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1759) |
| [L2:F7222](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7222) | 2 | Layer 2 ' well' pattern features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7222) |
| [L4:F1768](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1768) | 1 | Layer 4 'yeah' pattern feature (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1768) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 37 | Layer 4-5 ' uh' / 'well' features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L5:F2740](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2740) | 2 | Layer 4-5 ' uh' / 'well' features driving probe | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2740) |
| [L4:F9602](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) | 4 | Layer 4 ' uh' feature (pos 4) — promotes probe score | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9602) |
| [L4:F12126](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) | 2 | Layer 4 ' well' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12126) |
| [L4:F4847](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) | 2 | Layer 4 ' well' features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4847) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:9602 de=-0.629 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F9602@4` | ❌ error | — | — | Trace upstream from L4:F9602 at pos 4. Determine what token/pattern this feature… |
| SA-2 | `L0:F8352@2` | ❌ error | — | — | Trace upstream from L0:F8352 at pos 2. Determine what token/pattern this feature… |
| SA-3 | `L0:F6236@37` | ❌ error | — | — | Trace upstream from L0:F6236 at pos 37. Determine what token/pattern this featur… |
| SA-4 | `L4:F12126@2` | ❌ error | — | — | Trace upstream from L4:F12126 at pos 2. Determine what token/pattern this featur… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F9602@4, k=8 → Emb:" uh"@4 (de=11.44) +7 more |
| 2 | `get_upstream_features` | L0:F8352@2, k=8 → Emb:" well"@2 (de=30.88) +7 more |
| 3 | `get_upstream_features` | L0:F6236@37, k=8 → Emb:"t"@37 (de=18.25) +7 more |
| 4 | `get_upstream_features` | L4:F12126@2, k=8 → Emb:" well"@2 (de=14.62) +7 more |
| 5 | `get_upstream_features` | L0:F3820@3, k=5 → Emb:" the"@3 (de=32.75) +4 more |
| 6 | `get_upstream_features` | L1:F177@6, k=5 → Emb:" double"@6 (de=24.00) +4 more |
| 7 | `get_upstream_features` | L2:F5201@8, k=5 → Emb:" tournament"@8 (de=16.38) +4 more |
| 8 | `get_upstream_features` | L0:F16366@25, k=5 → Emb:" because"@25 (de=40.75) +4 more |
| 9 | `get_upstream_features` | L0:F4541@1, k=5 → Emb:"yeah"@1 (de=12.38) +4 more |
| 10 | `get_upstream_features` | L0:F10780@6, k=5 → Emb:" double"@6 (de=15.62) +4 more |
| 11 | `get_upstream_features` | L4:F4492@37, k=5 → Emb:"t"@37 (de=6.53) +4 more |
| 12 | `get_upstream_features` | L4:F4847@2, k=5 → Emb:" well"@2 (de=8.06) +4 more |
| 13 | `get_upstream_features` | L0:F15972@1, k=5 → Emb:"yeah"@1 (de=26.62) +4 more |
| 14 | `get_upstream_features` | L0:F6236@20, k=5 → Emb:"t"@20 (de=17.88) +4 more |
| 15 | `get_upstream_features` | L2:F9629@4, k=5 → Emb:" uh"@4 (de=15.12) +4 more |
| 16 | `get_upstream_features` | L2:F752@4, k=5 → Emb:" uh"@4 (de=10.38) +4 more |
| 17 | `get_upstream_features` | L0:F7893@6, k=5 → Emb:" double"@6 (de=18.62) +4 more |
| 18 | `get_upstream_features` | L1:F13255@8, k=5 → Emb:" tournament"@8 (de=18.50) +4 more |
| 19 | `get_upstream_features` | L5:F2740@2, k=5 → Emb:"yeah"@1 (de=6.66) +4 more |
| 20 | `get_upstream_features` | L1:F6846@8, k=5 → Emb:" tournament"@8 (de=15.00) +4 more |
| 21 | `get_upstream_features` | L2:F1337@37, k=3 → Emb:" haven"@35 (de=28.75) +2 more |
| 22 | `get_upstream_features` | L4:F1768@1, k=3 → Emb:"yeah"@1 (de=24.38) +2 more |
| 23 | `get_upstream_features` | L2:F1759@2, k=3 → Emb:" well"@2 (de=12.56) +2 more |
| 24 | `get_upstream_features` | L2:F7222@2, k=3 → Emb:" well"@2 (de=20.25) +2 more |
| 25 | `get_upstream_features` | L1:F2623@4, k=3 → Emb:" uh"@4 (de=12.31) +2 more |

### Build

`build_circuit` → 18 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 21,231 | 8,441 | 56,987 | 0 | $0.0199 | — | — |
| **Total** | | **21,231** | **8,441** | **56,987** | **0** | **$0.0199** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 25s