# Circuit Oracle Report
**Date:** 2026-07-28 07:23:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a circuit that extracts female-pronoun signals from the subject token "She" (pos 1) and the pronoun "she" (pos 55), with profession terms ("nurse", "practitioner", "labor", "delivery") providing a secondary, weaker contribution.

**Confidence:** 7

**Reasoning:** The circuit reveals that the top features driving the probe's score are organized into two parallel pathways, with the female-pronoun path dominating:

**Female-pronoun pathway (primary driver):**
- The token "She" at pos 1 has direct embedding effects of 19.25 on L6:F11646, 24.6 on L4:F7864, and 27.1 on L18:F14677 — these are among the largest direct effects in the entire graph.
- L4:F7864 (pos 1, direct_effect 0.33) and L6:F11646 (pos 1, direct_effect 0.49, pos 2: 0.40) aggregate early subject/pronoun information from the "She" embedding.
- A deep chain of mid-layer features (L9:F2762, F3056, F8770, F15819; L10:F14174, F10933; L11:F9183; L12:F12493; L15:F851) all fire exclusively on the "She" token at pos 1, with the most prominent being L18:F14677 (direct_effect 0.32 at pos 1, 0.32 at pos 55) and L19:F9685 (direct_effect 0.24 at pos 55, 0.21 at pos 24).
- The lowercase "she" at pos 55 has direct embedding effects of 32.75 on L6:F11646, 29.4 on L4:F7864, and 23.9 on L18:F14677 — also among the highest in the graph.
- The "her" token at pos 29 contributes with direct_effect -1.49 on L4:F7864 at pos 55 (inhibitory but small).

**Profession pathway (secondary):**
- "nurse" at pos 7 drives L4:F13803 (pos 46, direct_effect 0.29), L4:F15317 (pos 8, 0.23), L6:F15267 (pos 8, 0.39), L19:F9685 (pos 24, 0.21), and L12:F14970 (pos 24, 0.32).
- "practitioner" at pos 8 contributes to L6:F15267 (direct_effect 3.48) and L4:F15317 (1.43).
- "labor" (pos 44, 10.19) and "delivery" (pos 46, 13.81) embeddings directly feed L4:F13803 with large effects.

**Key observations supporting the spurious-correlation concern:**
1. The top three features (L6:F11646 at pos 1, L7:F8644 at pos 24, L6:F11646 at pos 2) all center on the subject position, with two of the top three being "She"-token features.
2. The female-pronoun pathway has 9+ dedicated mid-layer features (L9–L15) that fire only on the "She" token, forming an unusually deep and dedicated circuit for this single token — far more elaborate than the profession-token pathway.
3. L18:F14677 fires on both "She" (pos 1) and "she" (pos 55) with comparable direct_effects (0.32 each), suggesting it specifically detects female-pronoun subjects wherever they appear.
4. L19:F9685 fires on three positions: pos 24 (with 3.45 from "Linda" + nurse signals), pos 55 (she), and its direct_effect 0.21–0.24 suggests it integrates both profession and pronoun signals but is most strongly associated with female-pronoun contexts.

While profession terms do contribute, the female-pronoun circuit is disproportionately large and deep, with dedicated feature chains spanning L4–L19 that activate specifically on "She"/"she". This is consistent with the user concern: the probe's classification leverages gender markers as a spurious shortcut alongside (or even more than) genuine profession indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 55 | Emb: she (pos 55) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 29 | Emb: her (pos 29) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: nurse (pos 7, 47) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: practitioner (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 44 | Emb: labor (44) / delivery (46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: labor (44) / delivery (46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 24 | Emb: Linda (pos 24) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Early subject/pronoun detectors on "She" (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early subject/pronoun detectors on "She" (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Early subject/pronoun detectors on "She" (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | Early subject/pronoun detectors on "She" (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | Early subject/pronoun detectors on "She" (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | Early subject/pronoun detectors on "She" (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L9:F2762](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) | 1 | Mid-layer female-pronoun / subject-continuation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) |
| [L9:F3056](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) | 1 | Mid-layer female-pronoun / subject-continuation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | Mid-layer female-pronoun / subject-continuation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L9:F15819](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) | 1 | Mid-layer female-pronoun / subject-continuation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | Mid-layer female-pronoun / subject-continuation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L10:F10933](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/10933) | 1 | Mid-layer female-pronoun / subject-continuation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/10933) |
| [L11:F9183](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) | 1 | Mid-layer female-pronoun / subject-continuation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) |
| [L12:F12493](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) | 1 | Mid-layer female-pronoun / subject-continuation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | Mid-layer female-pronoun / subject-continuation features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Late-layer female-subject aggregators (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Late-layer female-subject aggregators (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer female-subject aggregators (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 55 | Late-layer female-pronoun aggregators (pos 55) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 55 | Late-layer female-pronoun aggregators (pos 55) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 55 | Late-layer female-pronoun aggregators (pos 55) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 55 | Late-layer female-pronoun aggregators (pos 55) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 46 | Profession / nursing specialty tokens | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Profession / nursing specialty tokens | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 8 | Profession / nursing specialty tokens | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 8 | Profession / nursing specialty tokens | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 46 | Profession / nursing specialty tokens | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 24 | Profession / nursing specialty tokens | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 24 | Profession / nursing specialty tokens | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.494 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ❌ error | — | — | Trace this feature back to the input tokens. What does L6:F11646 encode? Where d… |
| SA-2 | `L18:F14677@1` | ❌ error | — | — | Trace this feature back to the input tokens. What does L18:F14677 encode? Where … |
| SA-3 | `L12:F14970@24` | ❌ error | — | — | Trace this feature back to the input tokens. What does L12:F14970 encode? Where … |
| SA-4 | `L4:F13803@46` | ❌ error | — | — | Trace this feature back to the input tokens. What does L4:F13803 at pos 46 encod… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 2 | `get_upstream_features` | L18:F14677@1, k=10 → Emb:"She"@1 (de=27.12) +9 more |
| 3 | `get_upstream_features` | L12:F14970@24, k=10 → Emb:"<bos>"@0 (de=-3.17) +9 more |
| 4 | `get_upstream_features` | L4:F13803@46, k=10 → Emb:" delivery"@46 (de=13.81) +9 more |
| 5 | `get_upstream_features` | L6:F15267@8, k=10 → Emb:" nurse"@7 (de=7.06) +9 more |
| 6 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:"She"@1 (de=6.03) +9 more |
| 7 | `get_upstream_features` | L19:F9685@24, k=10 → Emb:" Linda"@24 (de=3.45) +9 more |
| 8 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"She"@1 (de=24.62) +9 more |
| 9 | `get_upstream_features` | L4:F15317@2, k=10 → Emb:"She"@1 (de=13.56) +9 more |
| 10 | `get_upstream_features` | L2:F7672@1, k=10 → Emb:"She"@1 (de=13.88) +9 more |
| 11 | `get_upstream_features` | L4:F7864@2, k=8 → ❌ Feature (layer=4, feature_idx=7864) not found at pos=2. This |
| 12 | `get_upstream_features` | L15:F851@1, k=8 → L12:F12493 (de=22.38) +7 more |
| 13 | `get_upstream_features` | L11:F9183@1, k=8 → L10:F14174 (de=13.38) +7 more |
| 14 | `get_upstream_features` | L4:F15317@8, k=8 → Emb:" nurse"@7 (de=5.03) +7 more |
| 15 | `get_upstream_features` | L12:F12940@55, k=8 → ❌ Feature (layer=12, feature_idx=12940) not found at pos=55. T |
| 16 | `get_upstream_features` | L18:F14677@55, k=8 → Emb:" she"@55 (de=23.88) +7 more |
| 17 | `get_upstream_features` | L9:F9183@1, k=5 → ❌ Feature (layer=9, pos=1, feature_idx=9183) not found in grap |
| 18 | `get_upstream_features` | L9:F2762@1, k=5 → Emb:"<bos>"@0 (de=15.62) +4 more |
| 19 | `get_upstream_features` | L9:F8770@1, k=5 → L7:F462 (de=16.62) +4 more |
| 20 | `get_upstream_features` | L4:F7864@55, k=8 → Emb:" she"@55 (de=29.38) +7 more |
| 21 | `get_upstream_features` | L18:F14677@79, k=5 → Emb:" She"@79 (de=15.38) +4 more |
| 22 | `get_upstream_features` | L7:F462@1, k=5 → Emb:"<bos>"@0 (de=21.88) +4 more |
| 23 | `get_upstream_features` | L7:F5741@1, k=5 → Emb:"<bos>"@0 (de=12.75) +4 more |
| 24 | `get_upstream_features` | L5:F3992@1, k=5 → Emb:"<bos>"@0 (de=22.50) +4 more |
| 25 | `get_upstream_features` | L10:F14174@1, k=5 → L9:F3056 (de=17.62) +4 more |
| 26 | `get_upstream_features` | L10:F12232@1, k=5 → L9:F8770 (de=10.69) +4 more |
| 27 | `get_upstream_features` | L9:F3056@1, k=5 → Emb:"<bos>"@0 (de=13.62) +4 more |
| 28 | `get_upstream_features` | L9:F15819@1, k=5 → L7:F462 (de=13.94) +4 more |
| 29 | `get_upstream_features` | L4:F15317@79, k=5 → ❌ Feature (layer=4, feature_idx=15317) not found at pos=79. Th |
| 30 | `get_upstream_features` | L6:F11646@55, k=5 → Emb:" she"@55 (de=32.75) +4 more |
| 31 | `get_upstream_features` | L10:F10933@1, k=5 → L9:F2762 (de=10.38) +4 more |
| 32 | `get_upstream_features` | L12:F12493@1, k=5 → L10:F14174 (de=15.38) +4 more |
| 33 | `get_upstream_features` | L4:F15317@25, k=5 → Emb:" has"@25 (de=3.83) +4 more |
| 34 | `get_upstream_features` | L7:F8644@8, k=5 → Emb:" nurse"@7 (de=4.38) +4 more |

### Build

`build_circuit` → 13 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 25,450 | 5,966 | 93,270 | 0 | $0.0204 | — | — |
| **Total** | | **25,450** | **5,966** | **93,270** | **0** | **$0.0204** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 2s