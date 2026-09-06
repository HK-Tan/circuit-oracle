# Circuit Oracle Report
**Date:** 2026-07-28 07:24:22 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction-classification probe is driven primarily by a dedicated late-layer circuit that aggregates information from the position of the negation word "No" (pos 16) and its dependent "one" (pos 17), rather than from genuine entailment-contradiction semantics like tourist-office vs walking-tour content.

**Confidence:** 8/10

**Reasoning:**

The attribution graph reveals a circuit that is strongly **anchored to the surface token "No"** at position 16 and the dependent "one" at position 17 (the start of "No one is usually at the tourist office..."). The embedding of "No" (pos 16) directly drives a chain of late-layer features all positioned at pos 16: L12:F8719, L13:F10768, L14:F336 (activation 26.9, direct_effect +0.18), L15:F13061 (activation 34.5, direct_effect +11.5 to L16:F11298), and L16:F11298 (activation 40.25, direct_effect +0.17 to the probe). These features form a near-monotonic positional aggregation pipeline that culminates in a strong positive contribution to the contradiction probe score.

The "one" embedding (pos 17) similarly feeds L0:F4438 (activation 29.9, direct_effect +13 to L1:F15800) → L1:F15800 (direct_effect +0.25) → output. L0:F1143 at pos 16 also fires on "No" and feeds the mid-circuit (L3:F3266 → L2:F2771 → L12:L16 chain).

**Confound evidence supporting the user's concern:** L0:F2238 at pos 12 ("about") and L0:F6051 at pos 15 (".") both carry *negative* direct_effects (−0.21, −0.20), while the "No"/"one" features carry the strongest *positive* direct_effects. The semantic content of the premise (tourist office, walking tours, map) is routed through scattered low-magnitude features at positions 1, 2, 4, 11, 12, 14, 15 (L0:F8566, L13092, L7727, L13354, L2238, L6051; L2:F14413, F1016, F8837) with relatively small direct_effects (mostly |d|<0.3), and they do **not** form a coherent contradiction-semantic circuit. Critically, the L14–L16 "late" features that would normally carry task-relevant semantic information for an NLI model are all at pos 16 and trace cleanly back to the "No" embedding — not to any tourist-office vs walking-tour entity comparison.

This is consistent with the user's hypothesis: the probe has latched onto the **negation cue "No"** as a shortcut for predicting contradiction, rather than performing actual semantic comparison between the premise and hypothesis. The circuit's most-late-layer (highest-attribution) features form a single positional chain tied to the negation token, with no comparable late-layer circuit comparing tourist-office entities across the two sentences.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 17 | L0 lexical token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L0:F1143](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) | 16 | L0 lexical token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1143) |
| [L0:F8566](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) | 1 | L0 lexical token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8566) |
| [L0:F13092](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13092) | 2 | L0 lexical token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13092) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 12 | L0 lexical token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | L0 lexical token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F10562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) | 2 | L0 lexical token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) |
| [L0:F10904](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) | 1 | L0 lexical token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10904) |
| [L0:F7727](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7727) | 4 | L0 lexical token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7727) |
| [L0:F13354](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13354) | 11 | L0 lexical token features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13354) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | L2 early compositional features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | L2 early compositional features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L2:F1016](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) | 14 | L2 early compositional features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) |
| [L2:F8837](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) | 17 | L2 early compositional features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8837) |
| [L2:F11769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) | 2 | L2 early compositional features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) |
| [L2:F2771](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) | 16 | L2 early compositional features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2771) |
| [L1:F15800](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) | 17 | L1 compositional features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) |
| [L1:F6872](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6872) | 14 | L1 compositional features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6872) |
| [L1:F13179](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13179) | 1 | L1 compositional features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13179) |
| [L1:F11342](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11342) | 2 | L1 compositional features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11342) |
| [L4:F10722](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10722) | 9 | Early-mid (L3-L8) features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10722) |
| [L4:F11969](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11969) | 4 | Early-mid (L3-L8) features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11969) |
| [L3:F3266](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) | 16 | Early-mid (L3-L8) features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3266) |
| [L8:F1872](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/1872) | 4 | Early-mid (L3-L8) features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/1872) |
| [L14:F336](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) | 16 | Late-layer 'No'-position aggregation circuit (L12-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/336) |
| [L16:F11298](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) | 16 | Late-layer 'No'-position aggregation circuit (L12-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/11298) |
| [L12:F8719](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) | 16 | Late-layer 'No'-position aggregation circuit (L12-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/8719) |
| [L13:F10768](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) | 16 | Late-layer 'No'-position aggregation circuit (L12-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/10768) |
| [L15:F13061](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) | 16 | Late-layer 'No'-position aggregation circuit (L12-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/13061) |
| [L15:F15582](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15582) | 16 | Late-layer 'No'-position aggregation circuit (L12-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15582) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:3116 de=-0.609 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F3116@2` | ❌ error | — | — | Trace upstream from L2:F3116 at pos 2. This is the strongest negative direct_eff… |
| SA-2 | `L0:F10562@2` | ❌ error | — | — | Trace upstream from L0:F10562 at pos 2 (+0.29). What does this feature encode an… |
| SA-3 | `L2:F14413@14` | ❌ error | — | — | Trace upstream from L2:F14413 at pos 14 (-0.28). What does this feature encode a… |
| SA-4 | `L1:F15800@17` | ❌ error | — | — | Trace upstream from L1:F15800 at pos 17 (+0.25). What does this feature encode a… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F3116@2, k=10 → Emb:"Pick"@1 (de=50.00) +9 more |
| 2 | `get_upstream_features` | L0:F10562@2, k=10 → Emb:" up"@2 (de=36.75) +9 more |
| 3 | `get_upstream_features` | L2:F14413@14, k=10 → Emb:" tours"@14 (de=28.38) +9 more |
| 4 | `get_upstream_features` | L1:F15800@17, k=10 → Emb:" one"@17 (de=15.25) +9 more |
| 5 | `get_upstream_features` | L0:F4438@17, k=8 → Emb:" No"@16 (de=29.38) +7 more |
| 6 | `get_upstream_features` | L0:F11351@17, k=8 → Emb:" one"@17 (de=38.50) +7 more |
| 7 | `get_upstream_features` | L14:F336@16, k=8 → Emb:" No"@16 (de=33.00) +7 more |
| 8 | `get_upstream_features` | L16:F11298@16, k=8 → Emb:" No"@16 (de=12.44) +7 more |

### Build

`build_circuit` → 14 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 22,983 | 4,835 | 41,822 | 0 | $0.0152 | — | — |
| **Total** | | **22,983** | **4,835** | **41,822** | **0** | **$0.0152** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 0s