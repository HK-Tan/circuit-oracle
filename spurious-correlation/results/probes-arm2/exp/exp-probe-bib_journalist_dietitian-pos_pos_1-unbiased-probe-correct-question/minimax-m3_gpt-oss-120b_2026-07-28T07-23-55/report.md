# Circuit Oracle Report
**Date:** 2026-07-28 07:23:55 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of the dietitian profession is driven by genuine profession-indicative vocabulary ("Nutrition," "Die/tes/Dietetics," "eat," "healthier," "educating") flowing through a clear hierarchy from token embeddings → subword detectors → nutrition-word detectors → dietitian concept aggregators, with **no evidence of spurious gender-marker features** (no "She"/"her"-driven paths appear in the top direct-effect features).

**Confidence:** 8

**Reasoning:**

The top features driving the probe score are all anchored in **profession-specific vocabulary**, not gender pronouns:

- **L6:F6115** (pos 5, direct_effect=0.1279) — the top feature, despite firing on the " clients" token, is gated by upstream food-context features (L4:F12213 on "healthier," L4:F13412 on multiple food words). Its upstream is dominated by the " clients" embedding (25.6) and negative food-word contributions, not "She"/"her" embeddings.
- **L4:F13412** (direct_effect 0.074–0.124) fires at positions 9, 10, 22, 23 — all food/profession terms ("eat," "healthier," "Die/tes," "te"). This is a **nutrition/dietetics vocabulary detector**.
- **L19:F1589** (direct_effect 0.080–0.109) fires at positions 20, 22, 23 with very high activation (50–60). Upstream: L17:F7545 and L18:F6105 are both fed by the "Die" (pos 22, de=13.25), "Nutrition" (pos 20, de=14.06), and "te" (pos 23) embeddings — this is a **"Dietitian"/"Nutrition" concept recognizer**.
- **L14:F4197** (direct_effect 0.122) fires at "eat" (pos 9), "Nutrition" (pos 20), and "Die/tes" (pos 22/23) — aggregating food/nutrition context across positions.

Crucially, the user's concern is **not supported** by this circuit:
- "She" (pos 1) and "her" (pos 4) appear as embeddings in the upstream of a few features (L6:F6115 has "her" de=0.93, L1:F15251 has "She" de=-1.45 — i.e., **inhibitory**), but these contributions are tiny compared to the profession-vocabulary embeddings.
- The two features with **negative direct_effect** on the probe (L0:F6051 at pos 11 "." with de=-0.096, L1:F15251 at pos 5 with de=-0.091) are **suppressing** non-profession signals, not driving spurious gender predictions.
- The two highest-magnitude embedding contributions at the output are "Nutrition" (de=8.19) and "Die" (de=8.69) — both core profession terms.

The circuit topology: token embeddings → L0–3 subword features → L4 nutrition-word detector (F13412) → L6 food-context (F11327) → L14 profession aggregator (F4197) → L17–18 dietitian concept (F7545, F6105) → L19 dietitian recognizer (F1589) → output logit. The "Die" and "te" subword embeddings (pos 22/23 = "Dietetics") are the strongest single-token drivers, consistent with a legitimate profession indicator.

**The probe is using genuine profession-indicative content (the words "Nutrition," "Dietetics," "eat healthier," "educating") rather than the gendered pronouns "She"/"her."** The concern about spurious gender-marker usage is not supported by this attribution graph.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | Mid-layer profession context aggregators | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 20 | Mid-layer profession context aggregators | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 23 | Mid-layer profession context aggregators | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 20 | Late-layer dietitian/Academy recognizer | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 22 | Late-layer dietitian/Academy recognizer | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 23 | Late-layer dietitian/Academy recognizer | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 20 | Dietitian concept aggregators (layer 17-18) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 22 | Dietitian concept aggregators (layer 17-18) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 23 | Dietitian concept aggregators (layer 17-18) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 20 | Dietitian concept aggregators (layer 17-18) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 22 | Dietitian concept aggregators (layer 17-18) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 23 | Dietitian concept aggregators (layer 17-18) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 9 | Nutrition/Dietetics word detector (layer 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 10 | Nutrition/Dietetics word detector (layer 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | Nutrition/Dietetics word detector (layer 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 23 | Nutrition/Dietetics word detector (layer 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 23 | Nutrition/Dietetics word detector (layer 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F12213](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) | 10 | Nutrition/Dietetics word detector (layer 4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 9 | Eat/healthier food context detector (layer 6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 20 | Eat/healthier food context detector (layer 6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 23 | Eat/healthier food context detector (layer 6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F6115](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) | 5 | Eat/healthier food context detector (layer 6) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 23 | Subword token features (layers 0-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 23 | Subword token features (layers 0-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |
| [L3:F9216](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9216) | 9 | Subword token features (layers 0-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9216) |
| [L3:F2310](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2310) | 5 | Subword token features (layers 0-3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2310) |
| [L0:F11021](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11021) | 9 | Subword token features (layers 0-3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11021) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 10 | Subword token features (layers 0-3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F9888](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) | 3 | Subword token features (layers 0-3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) |
| [L0:F3106](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3106) | 5 | Subword token features (layers 0-3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3106) |
| [L0:F2175](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2175) | 9 | Subword token features (layers 0-3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2175) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:6115 de=0.128 |
| 3 | `get_upstream_features` | Emb:" clients"@5 (de=25.62) +9 more |
| 4 | `get_upstream_features` | Emb:" eat"@9 (de=17.88) +9 more |
| 5 | `get_upstream_features` | L4:F13412 (de=10.38) +9 more |
| 6 | `get_upstream_features` | L3:F11774 (de=4.72) +9 more |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F6115@5` | ❌ error | — | — | Trace L6:F6115 at pos 5 upstream. This is the highest direct_effect feature (0.1… |
| SA-2 | `L19:F1589@23` | ❌ error | — | — | Trace L19:F1589 at pos 23 upstream. This feature fires at multiple positions (20… |
| SA-3 | `L4:F13412@23` | ❌ error | — | — | Trace L4:F13412 at pos 23 upstream. This feature fires at many positions (9, 10,… |
| SA-4 | `L14:F4197@9` | ❌ error | — | — | Trace L14:F4197 at pos 9 upstream. This has direct_effect 0.1221. Determine what… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11327@9, k=10 → Emb:" eat"@9 (de=22.12) +9 more |
| 2 | `get_upstream_features` | L4:F12213@10, k=10 → Emb:" healthier"@10 (de=20.00) +9 more |
| 3 | `get_upstream_features` | L0:F9888@3, k=10 → Emb:" educating"@3 (de=14.88) +9 more |
| 4 | `get_upstream_features` | L0:F6051@11, k=10 → Emb:"."@11 (de=46.50) +9 more |
| 5 | `get_upstream_features` | L1:F15251@5, k=10 → Emb:" clients"@5 (de=27.62) +9 more |
| 6 | `get_upstream_features` | L5:F2213@5, k=10 → Emb:" clients"@5 (de=10.19) +9 more |
| 7 | `get_upstream_features` | L5:F3400@3, k=10 → Emb:" loves"@2 (de=9.62) +9 more |
| 8 | `get_upstream_features` | L3:F2310@5, k=10 → Emb:" clients"@5 (de=11.12) +9 more |
| 9 | `get_upstream_features` | L17:F7545@23, k=10 → L4:F13412 (de=5.25) +9 more |
| 10 | `get_upstream_features` | L3:F11774@23, k=10 → Emb:" Die"@22 (de=5.62) +9 more |
| 11 | `get_upstream_features` | L3:F10028@23, k=10 → Emb:" Die"@22 (de=7.19) +9 more |
| 12 | `get_upstream_features` | L3:F9216@9, k=10 → Emb:" eat"@9 (de=19.50) +9 more |
| 13 | `get_upstream_features` | L19:F1589@20, k=10 → Emb:" Nutrition"@20 (de=34.25) +9 more |
| 14 | `get_upstream_features` | L18:F6105@23, k=8 → L17:F7545 (de=9.00) +7 more |
| 15 | `get_upstream_features` | L4:F11037@23, k=8 → L3:F11774 (de=2.62) +7 more |
| 16 | `get_upstream_features` | L0:F11021@9, k=8 → Emb:" eat"@9 (de=23.75) +7 more |
| 17 | `get_upstream_features` | L0:F9026@10, k=8 → Emb:" healthier"@10 (de=27.25) +7 more |
| 18 | `get_upstream_features` | L4:F14782@5, k=8 → Emb:" clients"@5 (de=16.00) +7 more |
| 19 | `get_upstream_features` | L0:F3106@5, k=5 → Emb:" clients"@5 (de=22.00) +4 more |
| 20 | `get_upstream_features` | L0:F2175@9, k=5 → Emb:" eat"@9 (de=19.62) +4 more |
| 21 | `get_upstream_features` | L1:F15251@1, k=5 → ❌ Feature (layer=1, feature_idx=15251) not found at pos=1. Thi |
| 22 | `get_upstream_features` | L19:F1589@22, k=5 → Emb:" Nutrition"@20 (de=14.06) +4 more |

### Build

`build_circuit` → 15 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 29,283 | 6,093 | 98,687 | 0 | $0.0220 | — | — |
| **Total** | | **29,283** | **6,093** | **98,687** | **0** | **$0.0220** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 23s