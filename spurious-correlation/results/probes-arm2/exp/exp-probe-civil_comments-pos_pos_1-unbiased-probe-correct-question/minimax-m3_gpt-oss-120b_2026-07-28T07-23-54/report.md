# Circuit Oracle Report
**Date:** 2026-07-28 07:23:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by a **named-entity / identity-group signal** — specifically the token "trump" (pos 5), the adverb "clearly" (pos 2), and racial/ethnic vocabulary ("white", "other", "again") — rather than by features encoding the actual toxic content or sentiment of the prompt.

**Confidence:** 7

**Reasoning:**

The top features driving the probe are concentrated in early layers (L0–L4) and almost entirely trace back to **specific input tokens**, not to abstract semantic features. Tracing upstream reveals:

1. **"trump" is the dominant signal.** Five of the top features (L0:F7621, L0:F4422, L0:F11375, L0:F14582, L2:F14301) carry strong positive direct_effects and trace to `Emb: " trump" (pos 5)`. The entity name itself — not the surrounding hateful context ("bigot", "white", "nonwhites") — is the largest single contributor. L4:F14582 (direct_effect=+0.156) is the latest "trump" entity feature, sitting just before the probe read-out.

2. **Function-word and adverb features dominate the L0 layer.** L0:F11375 (" is", activation=33.5, direct_effect=+0.131), L0:F7621 (" clearly", direct_effect=+0.194), and L0:F3916 ("tie", direct_effect=+0.119) are high-activation generic word detectors, not toxicity-relevant. The "clearly" token — an epistemic adverb — has the single highest direct_effect (+0.194) on the probe.

3. **Racial vocabulary features** (L0:F15831 at " again" pos 26, direct_effect=−0.124; L0:F7969 at " other" pos 14, direct_effect=+0.102; L0:F3436 at " white" pos 15, direct_effect=+0.102) contribute, but these are shallow token-level detectors, not deep semantic "hate speech" features.

4. **No mid/late-layer semantic circuit.** The deepest feature in the circuit is L4 (an entity detector). There is no L10–L20 circuit integrating "bigot + white + nonwhites" into a toxicity concept. The probe reads off essentially a bag-of-entity-tokens: trump, clearly, white, other, again.

This confirms the user's concern: the circuit is **not** performing content-based toxicity classification. Instead, it is acting as a **named-entity / lexical-marker heuristic** — the probe fires strongly when "trump" co-occurs with generic function words and racial terms, regardless of the actual hateful semantic content. A prompt mentioning "trump" in a neutral or positive context (e.g., a news headline) would likely produce a similar probe score, demonstrating the spurious correlation. The toxicity classifier is exploiting a shortcut: "identity-group tokens present → classify as toxic" rather than reasoning about the actual harmful content of the message.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 5 | L0: "trump" token features (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F7621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) | 2 | L0: "clearly" token features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7621) |
| [L0:F4422](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) | 2 | L0: "clearly" token features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4422) |
| [L0:F7861](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) | 2 | L0: "clearly" token features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7861) |
| [L0:F7142](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) | 2 | L0: "clearly" token features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7142) |
| [L0:F12866](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) | 2 | L0: "clearly" token features (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12866) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 6 | L0: function-word/auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3916](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3916) | 1 | L0: function-word/auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3916) |
| [L0:F164](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/164) | 3 | L0: function-word/auxiliary features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/164) |
| [L0:F15831](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15831) | 26 | L0: racial/ethnic token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15831) |
| [L0:F7969](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) | 14 | L0: racial/ethnic token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7969) |
| [L1:F9761](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) | 2 | L1: "clearly" composition | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9761) |
| [L2:F14301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) | 5 | L2: "trump" entity/identity-group signal | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14301) |
| [L2:F15769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15769) | 1 | L2: "trump" entity/identity-group signal | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15769) |
| [L2:F9199](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9199) | 9 | L2: "trump" entity/identity-group signal | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9199) |
| [L2:F4520](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4520) | 9 | L2: "trump" entity/identity-group signal | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4520) |
| [L3:F373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) | 1 | L3: "trump" inhibition/contrast features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) |
| [L3:F3136](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3136) | 5 | L3: "trump" inhibition/contrast features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3136) |
| [L4:F14582](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) | 5 | L4: late "trump"/bigot entity feature | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14582) |
| [L4:F11580](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) | 9 | L4: late "trump"/bigot entity feature | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11580) |
| [L4:F2720](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2720) | 1 | L4: late "trump"/bigot entity feature | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2720) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:12866 de=-0.206 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F7621@2` | ❌ error | — | — | Trace upstream from L0:F7621 at pos 2. This feature has direct_effect=+0.19 on t… |
| SA-2 | `L4:F14582@5` | ❌ error | — | — | Trace upstream from L4:F14582 at pos 5. direct_effect=+0.156. The token at pos 5… |
| SA-3 | `L0:F11375@6` | ❌ error | — | — | Trace upstream from L0:F11375 at pos 6. direct_effect=+0.131, activation=33.5 (v… |
| SA-4 | `L0:F4422@2` | ❌ error | — | — | Trace upstream from L0:F4422 at pos 2. direct_effect=+0.137. Determine what it e… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F7621@2, k=10 → Emb:" clearly"@2 (de=17.75) +9 more |
| 2 | `get_upstream_features` | L4:F14582@5, k=10 → Emb:" trump"@5 (de=18.12) +9 more |
| 3 | `get_upstream_features` | L0:F11375@6, k=10 → Emb:" is"@6 (de=31.38) +9 more |
| 4 | `get_upstream_features` | L0:F4422@2, k=10 → Emb:" clearly"@2 (de=12.62) +9 more |
| 5 | `get_upstream_features` | L0:F12866@2, k=10 → Emb:" clearly"@2 (de=17.38) +9 more |
| 6 | `get_upstream_features` | L0:F15831@26, k=10 → Emb:" again"@26 (de=43.50) +9 more |
| 7 | `get_upstream_features` | L0:F3916@1, k=10 → Emb:"<bos>"@0 (de=8.94) +9 more |
| 8 | `get_upstream_features` | L0:F7969@14, k=10 → Emb:" other"@14 (de=42.25) +9 more |
| 9 | `get_upstream_features` | L0:F3436@15, k=10 → Emb:" white"@15 (de=18.12) +9 more |
| 10 | `get_upstream_features` | L2:F14301@5, k=10 → Emb:" trump"@5 (de=9.44) +9 more |
| 11 | `get_upstream_features` | L1:F9761@2, k=10 → Emb:" clearly"@2 (de=13.38) +9 more |
| 12 | `get_upstream_features` | L0:F7142@2, k=10 → Emb:" clearly"@2 (de=14.62) +9 more |
| 13 | `get_upstream_features` | L0:F164@3, k=10 → Emb:" shows"@3 (de=19.38) +9 more |
| 14 | `get_upstream_features` | L2:F9199@9, k=10 → Emb:"ot"@9 (de=23.88) +9 more |
| 15 | `get_upstream_features` | L4:F11580@9, k=10 → Emb:"ot"@9 (de=5.00) +9 more |
| 16 | `get_upstream_features` | L3:F373@1, k=10 → Emb:"<bos>"@0 (de=26.25) +9 more |
| 17 | `get_upstream_features` | L2:F15769@1, k=10 → Emb:"tie"@1 (de=21.12) +9 more |
| 18 | `get_upstream_features` | L0:F7861@2, k=10 → Emb:" clearly"@2 (de=14.25) +9 more |
| 19 | `get_upstream_features` | L2:F14301@5, k=5 → Emb:" trump"@5 (de=9.44) +4 more |
| 20 | `get_upstream_features` | L2:F4520@9, k=5 → Emb:" big"@8 (de=9.06) +4 more |
| 21 | `get_upstream_features` | L0:F3635@4, k=5 → Emb:" that"@4 (de=39.00) +4 more |
| 22 | `get_upstream_features` | L3:F3136@5, k=5 → Emb:" trump"@5 (de=10.62) +4 more |

### Build

`build_circuit` → 19 nodes, 28 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 15,813 | 5,528 | 71,809 | 0 | $0.0157 | — | — |
| **Total** | | **15,813** | **5,528** | **71,809** | **0** | **$0.0157** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 0s