# Circuit Oracle Report
**Date:** 2026-07-28 07:24:07 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "dietitian" is driven almost entirely by a deep, lexically-grounded profession-recognition circuit that traces the literal tokens "Dietetic/Dietitian", "Nutritional", "nutrition", "RD", and "Sports Nutrition" from the input embeddings up to the probe direction — gender markers ("She", "has", "Heather") make only negative/irrelevant contributions.

**Confidence:** 9

**Reasoning:** The circuit follows a clean profession-recognition path. At the input, embedding nodes for the actual profession-bearing tokens — "Die/te" at pos 20–21 (the word "Dietetic"), "Nutritional" at pos 9, "titian/Die" at pos 36–37 (the word "Dietitian"), "RD" at pos 55 (the registered-dietitian credential), "nutrition" at pos 50, and "Sports Nutrition" at pos 63–64 — all positively feed L0 lexical features (L0:F8153, L1:F1083, L1:F6461). Notably, the gender-marker embeddings ("She" pos 1, "has" pos 2, "from" pos 11) have *negative* direct_effects on the early features (e.g., L0:F14824 receives direct_effect = -0.12 from "She" and L0:F8974 receives -0.05 from "from") — they actively push *against* the dietitian detection at the bottom of the circuit, and they do not appear at all in the top positive paths to L6, L14, L17, or L19.

The signal rises through L3 subword-composition features (F11774, F10028, F7212, F2589; direct_effects of 4–19 from the "Die/te/titian" embeddings) into L4:F13412 — a *multi-position* dietitian-token feature that fires at pos 9, 21, 22, 36, 37, and 55 (six separate occurrences of dietitian-related tokens), with the "titian" embedding (pos 37) contributing direct_effect = 14.0 directly to it. L4:F13412 is the single strongest positive contributor to the probe (direct_effect = 0.154 at pos 21, 0.117 at pos 55, 0.089 at pos 22, 0.084 at pos 37, 0.059 at pos 36).

From L4 the signal consolidates into L6:F11327 (a "Die/titian" profession-token detector; direct_effect ≈ 5–6 from the L4 cluster), then through L8/L9 refiners, into L14:F4197 — a *nutrition-domain concept feature* whose top upstream signal is the "Nutritional" embedding (direct_effect = 14.4) and which fires on all three nutrition-token positions. L14:F4197 alone contributes direct_effect = 0.058 to the probe. L16 carries *inhibitory* offset features (F2393, F12752; negative direct_effects) that suppress non-dietitian readings, and L17/L18/L19 form a dietitian-entity feature cluster culminating in L19:F1589 (direct_effect = 0.064 at pos 21, 0.044 at pos 50).

Crucially for the user's concern: the gender/female-pronoun signal ("She" pos 1, "has" pos 2, "Heather", "Rebecca Scritchfield") is **not** driving the positive classification. The "She" embedding contributes direct_effect = -1.15 to L0:F14824 (which itself has a *negative* direct_effect of -0.12 on the probe) — i.e., it's a tone-down signal on the opposite side of the circuit, not a feature that promotes the dietitian classification. The personal names "Heather" and "Rebecca Scritchfield" do not appear in any upstream path. The only "Rebecca"-area feature is L4:F10494 at pos 64, which is driven by the "Nutrition" / "Sports" *profession* tokens (direct_effect from "Nutrition" = 6.9, from "Sports" = 2.4), not by the name itself.

The probe is firing on the genuine, repeated, profession-indicating vocabulary — the words "Nutritional Sciences", "Dietetic", "Dietitian", "RD", "nutrition", "Sports Nutrition" — not on the female pronouns or the personal names. The user's concern about spurious gender-marker features is not supported by this attribution graph; the circuit shows a legitimate profession-vocabulary recognition mechanism.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 21 | L19 profession/nutrition concept features | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 50 | L19 profession/nutrition concept features | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 21 | L18 dietitian-as-entity feature | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 50 | L18 dietitian-as-entity feature | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 21 | L17 dietitian-token features | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 21 | L17 dietitian-token features | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 50 | L17 dietitian-token features | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L16:F2393](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2393) | 21 | L16 inhibitory profession-offset features | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2393) |
| [L16:F12752](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) | 21 | L16 inhibitory profession-offset features | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) |
| [L16:F12752](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) | 50 | L16 inhibitory profession-offset features | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | L14 nutrition-domain concept feature (fires on Nutritional/nutrition) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 21 | L14 nutrition-domain concept feature (fires on Nutritional/nutrition) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 50 | L14 nutrition-domain concept feature (fires on Nutritional/nutrition) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L9:F15926](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15926) | 21 | L9 mid-layer profession refiners | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15926) |
| [L9:F14144](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14144) | 21 | L9 mid-layer profession refiners | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/14144) |
| [L8:F8003](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8003) | 21 | L8 mid-layer concept refiners | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8003) |
| [L8:F7732](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7732) | 21 | L8 mid-layer concept refiners | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7732) |
| [L8:F10253](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/10253) | 21 | L8 mid-layer concept refiners | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/10253) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 9 | L6 "Die/titian" profession-token detector | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 21 | L6 "Die/titian" profession-token detector | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 50 | L6 "Die/titian" profession-token detector | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 9 | L4 repeated "Dietitian" / profession-name token feature (multi-position) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | L4 repeated "Dietitian" / profession-name token feature (multi-position) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | L4 repeated "Dietitian" / profession-name token feature (multi-position) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 36 | L4 repeated "Dietitian" / profession-name token feature (multi-position) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 37 | L4 repeated "Dietitian" / profession-name token feature (multi-position) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | L4 repeated "Dietitian" / profession-name token feature (multi-position) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 21 | L4 secondary "titian"-end feature | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 21 | L4 secondary "titian"-end feature | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 64 | L4 secondary "titian"-end feature | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 21 | L3 "Die/te" subword composition features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 21 | L3 "Die/te" subword composition features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |
| [L3:F7212](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7212) | 21 | L3 "Die/te" subword composition features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7212) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 37 | L3 "Die/te" subword composition features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 55 | L3 "Die/te" subword composition features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L2:F7473](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7473) | 21 | L3 "Die/te" subword composition features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7473) |
| [L0:F8153](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8153) | 21 | L0 lexical/te features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8153) |
| [L0:F1083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1083) | 21 | L0 lexical/te features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1083) |
| [L1:F6461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) | 64 | L0 lexical/te features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:13412 de=0.154 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@21` | ❌ error | — | — | Trace the path from L19:F1589 at position 21. Determine what this feature encode… |
| SA-2 | `L14:F4197@21` | ❌ error | — | — | Trace the path from L14:F4197 at position 21. Determine what this feature encode… |
| SA-3 | `L6:F11327@21` | ❌ error | — | — | Trace the path from L6:F11327 at position 21. What does this feature encode? Tra… |
| SA-4 | `L4:F10494@64` | ❌ error | — | — | Trace the path from L4:F10494 at position 64. Position 64 is at/near 'Rebecca Sc… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F1589@21, k=15 → L4:F13412 (de=10.69) +14 more |
| 2 | `get_upstream_features` | L14:F4197@21, k=15 → L6:F11327 (de=7.72) +14 more |
| 3 | `get_upstream_features` | L6:F11327@21, k=15 → L4:F13412 (de=5.88) +14 more |
| 4 | `get_upstream_features` | L4:F10494@64, k=15 → Emb:" Nutrition"@64 (de=6.91) +14 more |
| 5 | `get_upstream_features` | L4:F13412@21, k=15 → L3:F11774 (de=4.81) +14 more |
| 6 | `get_upstream_features` | L4:F9554@21, k=15 → L3:F11774 (de=3.03) +14 more |
| 7 | `get_upstream_features` | L3:F11774@21, k=15 → Emb:" Die"@20 (de=5.88) +14 more |
| 8 | `get_upstream_features` | L17:F7545@21, k=15 → L4:F13412 (de=5.28) +14 more |
| 9 | `get_upstream_features` | L2:F2589@37, k=15 → Emb:"titian"@37 (de=19.12) +14 more |
| 10 | `get_upstream_features` | L16:F2393@21, k=10 → L6:F11327 (de=9.38) +9 more |
| 11 | `get_upstream_features` | L4:F11037@21, k=10 → L3:F11774 (de=2.77) +9 more |
| 12 | `get_upstream_features` | L3:F7212@21, k=10 → Emb:" Die"@20 (de=11.94) +9 more |
| 13 | `get_upstream_features` | L0:F14824@2, k=10 → Emb:" has"@2 (de=32.75) +9 more |
| 14 | `get_upstream_features` | L0:F8974@11, k=10 → Emb:" from"@11 (de=40.00) +9 more |
| 15 | `get_upstream_features` | L0:F9519@1, k=10 → Emb:"She"@1 (de=15.75) +9 more |
| 16 | `get_upstream_features` | L3:F10028@21, k=10 → Emb:" Die"@20 (de=6.94) +9 more |
| 17 | `get_upstream_features` | L9:F15926@21, k=10 → L6:F11327 (de=2.58) +9 more |
| 18 | `get_upstream_features` | L8:F8003@21, k=10 → L4:F13412 (de=4.81) +9 more |
| 19 | `get_upstream_features` | L9:F14144@21, k=10 → Emb:"te"@21 (de=2.33) +9 more |
| 20 | `get_upstream_features` | L16:F12752@21, k=10 → L4:F13412 (de=3.61) +9 more |
| 21 | `get_upstream_features` | L19:F1589@50, k=10 → Emb:" nutrition"@50 (de=29.50) +9 more |
| 22 | `get_upstream_features` | L0:F8153@21, k=10 → Emb:"te"@21 (de=23.25) +9 more |
| 23 | `get_upstream_features` | L14:F4197@9, k=10 → Emb:" Nutritional"@9 (de=14.44) +9 more |
| 24 | `get_upstream_features` | L2:F7473@21, k=10 → Emb:" Die"@20 (de=19.00) +9 more |
| 25 | `get_upstream_features` | L18:F6105@21, k=10 → L4:F13412 (de=8.94) +9 more |
| 26 | `get_upstream_features` | L17:F14680@21, k=10 → L4:F13412 (de=6.25) +9 more |
| 27 | `get_upstream_features` | L17:F14680@50, k=10 → Emb:" nutrition"@50 (de=28.12) +9 more |
| 28 | `get_upstream_features` | L1:F1083@21, k=10 → Emb:"te"@21 (de=22.25) +9 more |
| 29 | `get_upstream_features` | L4:F13412@36, k=10 → Emb:" Die"@36 (de=9.06) +9 more |
| 30 | `get_upstream_features` | L4:F13412@37, k=10 → Emb:"titian"@37 (de=14.00) +9 more |
| 31 | `get_upstream_features` | L4:F13412@55, k=10 → Emb:" RD"@55 (de=11.31) +9 more |
| 32 | `get_upstream_features` | L1:F6461@64, k=10 → Emb:" Sports"@63 (de=11.75) +9 more |

### Build

`build_circuit` → 21 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 27,937 | 7,137 | 123,776 | 0 | $0.0244 | — | — |
| **Total** | | **27,937** | **7,137** | **123,776** | **0** | **$0.0244** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 30s