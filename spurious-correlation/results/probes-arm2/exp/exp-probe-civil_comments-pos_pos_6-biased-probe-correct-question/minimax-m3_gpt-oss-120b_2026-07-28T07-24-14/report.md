# Circuit Oracle Report
**Date:** 2026-07-28 07:24:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven almost entirely by features that encode the presence of racial-identity group tokens ("white" at pos 2 and "black" at pos 6) rather than the lexical content of the slur, the word "stealing," or the surrounding sentence semantics.

**Confidence:** 8

**Reasoning:** The circuit traces cleanly from embedding nodes up to the probe output:

- **Emb: white (pos 2)** is the dominant upstream driver of the largest positive feature, **L4:F117 at pos 3** (direct_effect=15.0 from the embedding). L4:F117 is the single largest contributor to the probe (direct_effect=0.875), and it fires on both the "white" token and the downstream "dude"/"man" positions — it is a "white identity" detector, not a toxicity detector.
- **Emb: black (pos 6)** drives a parallel "black identity" supernode centered on pos 6. L8:F2483 (direct_effect=0.387) and L7:F7215/F9100 (direct_effect≈2.8 each) all receive their largest upstream direct_effect from the "black" embedding (e.g. 12.06, 9.81, 4.59). These features form the "mid_blacksignal" supernode and feed the probe output.
- The "stealing" / "thunder" tokens, which carry the actual hostile framing, are represented in the graph mainly through L2:F12341 at pos 4 (activation 10, direct_effect=0.239), but this feature is comparatively small in the probe-driving circuit and does not have a strong chain into the output.
- The L0:F4090 "Another" feature is a generic start-of-sentence detector (direct_effect=0.222) and adds little signal about content.

**Key mechanism:** Two parallel identity-detector supernodes (one keyed on "white", one keyed on "black") carry nearly all the attribution mass. The probe classifies this text as toxic primarily because the model registers that *two racial group nouns appear in proximity*, not because it recognizes the slur or the threatening framing. The user's concern is confirmed: the circuit is dominated by spurious identity-group signal (race-token detection), not by lexical/semantic content (the slur, "stealing," "thunder," or the negative stereotyping frame). This is a textbook example of a probe relying on demographic-correlated shortcut features rather than the actual toxic content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L8:F2483](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) | 6 | Black-entity / race concept (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) |
| [L7:F7215](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7215) | 6 | Black-entity / race concept (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7215) |
| [L7:F9100](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9100) | 6 | Black-entity / race concept (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9100) |
| [L11:F2332](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/2332) | 6 | Black-entity / race concept (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/2332) |
| [L12:F13522](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/13522) | 6 | Black-entity / race concept (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/13522) |
| [L9:F8462](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8462) | 6 | Black-entity / race concept (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8462) |
| [L6:F1163](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1163) | 6 | Black-entity / race concept (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1163) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 3 | White-entity / race concept (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 3 | White-entity / race concept (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | White-entity / race concept (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 3 | White-entity / race concept (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 3 | White-entity / race concept (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 7 | White-entity / race concept (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F5671](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) | 3 | White-entity / race concept (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5671) |
| [L5:F6786](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) | 3 | White-entity / race concept (pos 2-3) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6786) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | Lexical black/race features (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 6 | Lexical black/race features (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 2 | Lexical black/race features (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 2 | Lexical black/race features (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 3 | Lexical black/race features (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L2:F12341](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12341) | 4 | Lexical/early features (pos 1, 4) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12341) |
| [L4:F9880](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) | 1 | Lexical/early features (pos 1, 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9880) |
| [L0:F4090](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) | 1 | Lexical/early features (pos 1, 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4090) |
| [L3:F12848](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12848) | 1 | Lexical/early features (pos 1, 4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12848) |
| [L0:F6548](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6548) | 2 | Lexical/early features (pos 1, 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6548) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:117 de=0.875 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F117@3` | ❌ error | — | — | Trace the path from L4:F117 at pos 3. What does this feature encode and what tok… |
| SA-2 | `L3:F13061@3` | ❌ error | — | — | Trace the path from L3:F13061 at pos 3. What does this feature encode and what t… |
| SA-3 | `L4:F9880@1` | ❌ error | — | — | Trace the path from L4:F9880 at pos 1. What does this feature encode and what to… |
| SA-4 | `L2:F13158@6` | ❌ error | — | — | Trace the path from L2:F13158 at pos 6. What does this feature encode and what t… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F117@3, k=10 → Emb:" white"@2 (de=15.00) +9 more |
| 2 | `get_upstream_features` | L3:F13061@3, k=10 → Emb:" white"@2 (de=12.44) +9 more |
| 3 | `get_upstream_features` | L4:F9880@1, k=10 → Emb:"Another"@1 (de=33.25) +9 more |
| 4 | `get_upstream_features` | L2:F13158@6, k=10 → Emb:" black"@6 (de=10.81) +9 more |
| 5 | `get_upstream_features` | L3:F16373@3, k=10 → Emb:" white"@2 (de=23.12) +9 more |
| 6 | `get_upstream_features` | L6:F3902@3, k=10 → L4:F117 (de=6.78) +9 more |
| 7 | `get_upstream_features` | L8:F2483@6, k=10 → Emb:" black"@6 (de=4.59) +9 more |
| 8 | `get_upstream_features` | L2:F12341@4, k=10 → Emb:" stealing"@4 (de=11.62) +9 more |
| 9 | `get_upstream_features` | L2:F9528@6, k=10 → Emb:" black"@6 (de=31.88) +9 more |
| 10 | `get_upstream_features` | L6:F5671@3, k=10 → Emb:" dude"@3 (de=3.56) +9 more |
| 11 | `get_upstream_features` | L0:F4090@1, k=10 → Emb:"Another"@1 (de=32.75) +9 more |
| 12 | `get_upstream_features` | L12:F13522@6, k=10 → Emb:" black"@6 (de=4.91) +9 more |
| 13 | `get_upstream_features` | L5:F6786@3, k=10 → Emb:" white"@2 (de=2.30) +9 more |
| 14 | `get_upstream_features` | L0:F6548@2, k=10 → Emb:" white"@2 (de=19.62) +9 more |
| 15 | `get_upstream_features` | L2:F1708@2, k=10 → Emb:" white"@2 (de=18.38) +9 more |
| 16 | `get_upstream_features` | L3:F12848@1, k=10 → Emb:"Another"@1 (de=19.12) +9 more |
| 17 | `get_upstream_features` | L7:F7215@6, k=10 → Emb:" black"@6 (de=9.81) +9 more |
| 18 | `get_upstream_features` | L7:F9100@6, k=10 → Emb:" black"@6 (de=12.06) +9 more |
| 19 | `get_upstream_features` | L11:F2332@6, k=10 → Emb:" black"@6 (de=3.00) +9 more |
| 20 | `get_upstream_features` | L2:F9301@3, k=10 → Emb:" dude"@3 (de=10.38) +9 more |
| 21 | `get_upstream_features` | L6:F1163@6, k=8 → Emb:" black"@6 (de=12.25) +7 more |
| 22 | `get_upstream_features` | L9:F8462@6, k=8 → Emb:" black"@6 (de=4.91) +7 more |

### Build

`build_circuit` → 11 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 19,269 | 4,390 | 80,931 | 0 | $0.0159 | — | — |
| **Total** | | **19,269** | **4,390** | **80,931** | **0** | **$0.0159** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 8s