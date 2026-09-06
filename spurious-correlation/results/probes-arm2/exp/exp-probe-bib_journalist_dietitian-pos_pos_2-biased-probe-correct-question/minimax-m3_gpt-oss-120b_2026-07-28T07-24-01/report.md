# Circuit Oracle Report
**Date:** 2026-07-28 07:24:01 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by the presence of the feminine pronoun "She" through a multi-layer pronoun-aggregator circuit, with only a weak and indirect contribution from the actual "nutrition" topic tokens — confirming the user's concern that the probe uses a gender/spurious feature rather than the profession topic.

**Confidence:** 8

**Reasoning:** The dominant top-features for the probe direction are pronoun-anchored, not topic-anchored. The #1 feature L6:F11646 (direct_effect=0.357 at pos 1, 0.285 at pos 2, 0.137 at pos 23) fires strongly on every occurrence of the "She" token — its upstream is essentially the "She" token embedding (direct_effect=19.25 from `Emb: She (pos 1)` and 18.75 from `Emb: ' She' (pos 23)`), and it propagates to L10:F14965 (+0.16), L12:F12940 (+0.29 at pos 2, +0.11 at pos 3), and into the late-layer output driver L18:F14677 (+0.24 at pos 23, +0.20 at pos 1, +0.11 at pos 2). L18:F14677 is the main output-driving feature and its two largest upstreams are the `Emb: ' She' (pos 23)` token (14.31) and `Emb: She (pos 1)` token (6.81) — raw gender-pronoun embeddings, not topic words. L19:F9685 (direct_effect=0.146) and L12:F12940 also push the probe score upward, and both trace back to the same "She" embeddings. By contrast, the genuine profession/topic content — the "nutrition" token at pos 13 — only reaches the output through a much weaker path: it activates L4:F13412 and L6:F11327 (which has direct_effect=0.152, a positive contribution), but this topic branch never feeds the strong L18:F14677 output driver; it only weakly reaches L19:F9685. The "owner of Nutritionbybrittany.com" profession-indicating phrase is essentially absent from the top-20 features. The picture is reinforced by a competing inhibitory branch: L6:F16329 (pos 1: -0.17, pos 23: -0.13), L7:F8644 (pos 23: -0.127), L14:F12501 (pos 2: -0.148 incoming from L12), and L18:F14743 (pos 23: -0.11) all push the probe score *down* and are themselves triggered by the same "She" embeddings (e.g. L7:F8644's top upstream is `Emb: She (pos 1)` with direct_effect=8.44). Net of this within-pronoun tug-of-war, the residual signal that drives the classifier is still overwhelmingly the feminine-pronoun representation, not semantic profession content. This is precisely the spurious-correlation mechanism the user flagged: a profession probe that has learned (or a residual stream direction that aligns with) the "She → female-coded professions" prior, so any sentence opening with "She" — even a generic bio — produces a high probe score regardless of whether genuine profession vocabulary is present.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Token-level: 'She' token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | Token-level: 'She' token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 23 | Token-level: 'She' token features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 1 | Inhibitory L0 'She' features (push against probe) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 23 | Inhibitory L0 'She' features (push against probe) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Early pronoun/identity features (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | Early pronoun/identity features (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L2:F899](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/899) | 1 | Early pronoun/identity features (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/899) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Mid: 'She'/'her' pronoun aggregator (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Mid: 'She'/'her' pronoun aggregator (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Topic: 'nutrition' word-form (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 13 | Topic: 'nutrition' word-form (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Strong 'She'/gender-pronoun feature (L6:F11646) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Strong 'She'/gender-pronoun feature (L6:F11646) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 23 | Strong 'She'/gender-pronoun feature (L6:F11646) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 1 | Inhibitory 'She' feature (L6:F16329) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 2 | Inhibitory 'She' feature (L6:F16329) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 23 | Inhibitory 'She' feature (L6:F16329) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Topic: nutrition concept (L6:F11327) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 23 | Inhibitory gender-aggregator (L7:F8644) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | Inhibitory gender-aggregator (L7:F8644) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Mid-context 'She' feature (L10:F14965) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | She+has pattern feature (L12:F12940) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 3 | She+has pattern feature (L12:F12940) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L14:F12501](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) | 2 | Inhibitory feature (L14:F12501) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12501) |
| [L14:F5740](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) | 23 | Inhibitory feature (L14:F12501) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5740) |
| [L14:F13478](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) | 23 | Inhibitory feature (L14:F12501) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/13478) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 23 | Strong 'She' pronoun aggregator (L17:F5889) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Main 'She'/gender-pronoun output driver (L18:F14677) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 2 | Main 'She'/gender-pronoun output driver (L18:F14677) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 23 | Main 'She'/gender-pronoun output driver (L18:F14677) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Inhibitory pronoun feature (L18:F14743) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 23 | Secondary 'She' output feature (L19:F9685) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.357 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@23` | ❌ error | — | — | Trace upstream from L18:F14677 at position 23. What does this feature encode? Wh… |
| SA-2 | `L18:F14677@1` | ❌ error | — | — | Trace upstream from L18:F14677 at position 1. What does this feature encode? Is … |
| SA-3 | `L18:F14743@23` | ❌ error | — | — | Trace upstream from L18:F14743 at position 23 (inhibitory -0.109). What does thi… |
| SA-4 | `L19:F9685@23` | ❌ error | — | — | Trace upstream from L19:F9685 at position 23. What does this feature encode? Wha… |
| SA-5 | `L6:F11646@1` | ❌ error | — | — | Trace upstream from L6:F11646 at position 1. This feature has the highest direct… |
| SA-6 | `L12:F12940@2` | ❌ error | — | — | Trace upstream from L12:F12940 at position 2. What does this feature encode? |
| SA-7 | `L4:F15317@2` | ❌ error | — | — | Trace upstream from L4:F15317 at position 2. Early layer feature with strong eff… |
| SA-8 | `L2:F7672@1` | ❌ error | — | — | Trace upstream from L2:F7672 at position 1. Very early layer feature (0.137 dire… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@23, k=15 → Emb:" She"@23 (de=14.31) +14 more |
| 2 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"She"@1 (de=19.25) +14 more |
| 3 | `get_upstream_features` | L2:F7672@1, k=10 → Emb:"She"@1 (de=13.88) +9 more |
| 4 | `get_upstream_features` | L12:F12940@2, k=15 → Emb:"She"@1 (de=6.03) +14 more |
| 5 | `get_upstream_features` | L4:F15317@2, k=15 → Emb:"She"@1 (de=13.56) +14 more |
| 6 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"She"@1 (de=24.62) +9 more |
| 7 | `get_upstream_features` | L19:F9685@23, k=10 → Emb:" She"@23 (de=5.72) +9 more |
| 8 | `get_upstream_features` | L6:F11327@13, k=8 → Emb:" nutrition"@13 (de=21.00) +7 more |
| 9 | `get_upstream_features` | L10:F14965@2, k=8 → L4:F15317 (de=5.56) +7 more |
| 10 | `get_upstream_features` | L6:F11646@2, k=10 → L4:F15317 (de=8.75) +9 more |
| 11 | `get_upstream_features` | L6:F11646@23, k=10 → Emb:" She"@23 (de=18.75) +9 more |
| 12 | `get_upstream_features` | L18:F14743@23, k=10 → Emb:" She"@23 (de=16.62) +9 more |
| 13 | `get_upstream_features` | L14:F12501@2, k=8 → L12:F12940 (de=13.56) +7 more |
| 14 | `get_upstream_features` | L4:F13412@13, k=8 → Emb:" nutrition"@13 (de=14.06) +7 more |
| 15 | `get_upstream_features` | L7:F8644@23, k=8 → Emb:"She"@1 (de=8.44) +7 more |
| 16 | `get_upstream_features` | L6:F16329@1, k=8 → Emb:"She"@1 (de=8.94) +7 more |
| 17 | `get_upstream_features` | L0:F11646@1, k=5 → ❌ Feature (layer=0, pos=1, feature_idx=11646) not found in gra |
| 18 | `get_upstream_features` | L1:F11646@1, k=5 → ❌ Feature (layer=1, pos=1, feature_idx=11646) not found in gra |
| 19 | `get_upstream_features` | L1:F7864@1, k=5 → ❌ Feature (layer=1, pos=1, feature_idx=7864) not found in grap |
| 20 | `get_upstream_features` | L1:F15317@2, k=5 → ❌ Feature (layer=1, feature_idx=15317) not found at pos=2. Thi |
| 21 | `get_upstream_features` | L1:F15317@13, k=5 → Emb:" nutrition"@13 (de=5.94) +4 more |
| 22 | `get_upstream_features` | L0:F12519@1, k=5 → Emb:"She"@1 (de=21.88) +4 more |
| 23 | `get_upstream_features` | L0:F15382@1, k=5 → Emb:"She"@1 (de=16.88) +4 more |
| 24 | `get_upstream_features` | L17:F5889@23, k=5 → Emb:" She"@23 (de=19.12) +4 more |

### Build

`build_circuit` → 22 nodes, 40 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 35,433 | 7,025 | 85,830 | 0 | $0.0242 | — | — |
| **Total** | | **35,433** | **7,025** | **85,830** | **0** | **$0.0242** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 29s