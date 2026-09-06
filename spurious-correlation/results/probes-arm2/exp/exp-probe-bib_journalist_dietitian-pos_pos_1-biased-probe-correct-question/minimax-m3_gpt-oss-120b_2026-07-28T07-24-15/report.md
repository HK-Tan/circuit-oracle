# Circuit Oracle Report
**Date:** 2026-07-28 07:24:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit is traced back to the **'She' token embedding at pos 1** (the very first content word), which is the single largest source of positive signal flowing into the probe. The user's concern is well-supported by the circuit topology.

**Analysis:** The probe's classification is driven almost entirely by a deep "She" pronoun detection circuit originating from the feminine pronoun at position 1, with smaller contributions from the verb "loves" and the name "Sarah" — no nutrition/profession content features are present in the top contributors.

**Confidence:** 8

**Reasoning:** The circuit reveals a striking pattern: **the dominant positive signal to the probe is a "She pronoun" tower, not a profession indicator**.

Key findings from `get_top_features` on the probe target:
- **L6:F11646 at pos 1** ("She") has the highest direct_effect (0.375), activation 12.5
- **L18:F14677 at pos 1** ("She") has direct_effect 0.247 with very high activation (29.875)
- **L4:F7864 at pos 1** ("She") has direct_effect 0.229
- **L12:F12940 at pos 2** ("loves") has direct_effect 0.252

Tracing these upstream reveals the mechanism: the **"She" token embedding (Emb:'She' pos 1)** feeds into an extensive chain of pronoun features (L0:F12519 → L2:F7672 → L4:F7864 → L5:F3992 → L6:F11646 → L7:F462, F5741 → L9:F2762, F3056, F8770, F15819 → L10:F14174, F10933 → L11:F9183 → L12:F12493 → L15:F851 → L18:F14677). This is a 19-layer "She" detector chain. The embedding node at pos 1 has direct_effect ~19-27 on multiple downstream pronoun features, confirming the input is the raw "She" token.

**What is NOT in the circuit:** The tokens "nutrition", "diet", "dietetics", "recipes", "clients" — the genuine profession markers — are conspicuously absent from the top direct contributors. The only secondary contribution comes from "loves" (pos 2), which in the context "She loves educating her clients" is part of a stereotypical female caregiving/nurturing phrase pattern that the probe has apparently learned to associate with the registered-dietitian profession.

**Implication for the user's concern:** The user's hypothesis is confirmed. The linear probe has latched onto a **gender-correlated spurious feature** (the feminine pronoun "She" plus stereotypically feminine verb patterns like "loves educating") rather than profession-specific vocabulary like "Academy of Nutrition and Dietetics", "dietitian", or "nutrition". This is a classic case where a probe trained to detect a profession exploits gender/pronoun correlations in the training data, which would fail to generalize across genders and could explain biased profession classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'She' (pos 1) — feminine pronoun/gender marker | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' loves' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' Sarah' (pos 12) — proper name | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: '<bos>' (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 1 | L0: F12519 (pos 1) — generic 'She' token feature, inhibitory on circuit | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 12 | L0: F7532 (pos 12) — 'Sarah' name detector (activ 17.75) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | L2: F7672 (pos 1) — 'She' early contextual feature | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | L2: F7672 (pos 1) — 'She' early contextual feature | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | L4: F7864 (pos 1) — 'She' pronoun feature (activ 8.31, DE 0.229 to probe) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | L4: F15317 (pos 2) — 'loves' verb feature (activ 6.78, DE 0.189) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L5:F16213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) | 2 | L5: F16213 (pos 2) — 'loves' verb feature (activ 5.44, DE 0.168) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/16213) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | L5: F3992 (pos 1) — strong 'She' pronoun feature (activ 23.9) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | L6: F11646 (pos 1) — top driver of probe (activ 12.5, DE 0.375); also at pos 2 (DE 0.305) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | L6: F11646 (pos 1) — top driver of probe (activ 12.5, DE 0.375); also at pos 2 (DE 0.305) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 2 | L7: F2765 (pos 2, pos 5, pos 12) — 'loves/clients/Sarah' relational feature (activ 8.19, DE 0.162) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 5 | L7: F2765 (pos 2, pos 5, pos 12) — 'loves/clients/Sarah' relational feature (activ 8.19, DE 0.162) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 12 | L7: F2765 (pos 2, pos 5, pos 12) — 'loves/clients/Sarah' relational feature (activ 8.19, DE 0.162) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | L7: F462 (pos 1) — 'She' pronoun feature (activ 30.5) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | L7: F5741 (pos 1) — 'She' pronoun feature (activ 24.1) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L9:F2762](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) | 1 | L9: F2762 (pos 1) — 'She' pronoun (activ 37) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) |
| [L9:F3056](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) | 1 | L9: F3056 (pos 1) — 'She' pronoun (activ 45) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | L9: F8770 (pos 1) — 'She' pronoun (activ 51.5) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L9:F15819](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) | 1 | L9: F15819 (pos 1) — 'She' pronoun (activ 49.75) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | L10: F14174 (pos 1) — 'She' pronoun (activ 55) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L10:F10933](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/10933) | 1 | L10: F10933 (pos 1) — 'She' pronoun (activ 53.75) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/10933) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | L10: F14965 (pos 2) — 'loves' verb (activ 13.94) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L11:F9183](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) | 1 | L11: F9183 (pos 1) — 'She' pronoun (activ 54.25) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | L12: F12940 (pos 2) — 'loves educating' phrase (activ 12.06, DE 0.252) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 12 | L12: F14970 (pos 12) — 'Sarah' entity role (activ 6.75, DE 0.152) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L12:F12493](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) | 1 | L12: F12493 (pos 1) — 'She' pronoun (activ 61.75) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | L15: F851 (pos 1) — 'She' pronoun (activ 161) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | L18: F14677 (pos 1) — strong 'She' pronoun signal (activ 29.9, DE 0.247) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.375 |

### Dispatch: 9 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ❌ error | — | — | Trace the path from L18:F14677 at pos 1 (the "She" token). This is a high-magnit… |
| SA-2 | `L12:F12940@2` | ❌ error | — | — | Trace the path from L12:F12940 at pos 2 (the "loves" token). Activation 12.0625,… |
| SA-3 | `L6:F11646@1` | ❌ error | — | — | Trace the path from L6:F11646 at pos 1 (the "She" token). Activation 12.5, direc… |
| SA-4 | `L4:F7864@1` | ❌ error | — | — | Trace the path from L4:F7864 at pos 1 (the "She" token). Activation 8.3125, dire… |
| SA-5 | `L4:F15317@2` | ❌ error | — | — | Trace the path from L4:F15317 at pos 2 (the "loves" token). Activation 6.7812, d… |
| SA-6 | `L5:F16213@2` | ❌ error | — | — | Trace the path from L5:F16213 at pos 2 (the "loves" token). Activation 5.4375, d… |
| SA-7 | `L7:F2765@2` | ❌ error | — | — | Trace the path from L7:F2765 at pos 2 (the "loves" token). Activation 8.1875, di… |
| SA-8 | `L7:F2765@5` | ❌ error | — | — | Trace the path from L7:F2765 at pos 5 (the "clients" token). Activation 4.875, d… |
| SA-9 | `L12:F14970@12` | ❌ error | — | — | Trace the path from L12:F14970 at pos 12 (the "Sarah" token). Activation 6.75, d… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=15 → Emb:"She"@1 (de=19.25) +14 more |
| 2 | `get_upstream_features` | L18:F14677@1, k=15 → Emb:"She"@1 (de=27.12) +14 more |
| 3 | `get_upstream_features` | L12:F12940@2, k=15 → Emb:"She"@1 (de=5.31) +14 more |
| 4 | `get_upstream_features` | L4:F7864@1, k=15 → Emb:"She"@1 (de=24.62) +14 more |
| 5 | `get_upstream_features` | L4:F15317@2, k=12 → Emb:"She"@1 (de=12.44) +11 more |
| 6 | `get_upstream_features` | L5:F16213@2, k=12 → Emb:"She"@1 (de=5.44) +11 more |
| 7 | `get_upstream_features` | L7:F2765@2, k=12 → Emb:"She"@1 (de=4.16) +11 more |
| 8 | `get_upstream_features` | L15:F851@1, k=12 → L12:F12493 (de=22.38) +11 more |
| 9 | `get_upstream_features` | L12:F14970@12, k=12 → Emb:" Sarah"@12 (de=4.62) +11 more |
| 10 | `get_upstream_features` | L12:F12493@1, k=10 → L10:F14174 (de=15.38) +9 more |
| 11 | `get_upstream_features` | L11:F9183@1, k=10 → L10:F14174 (de=13.38) +9 more |
| 12 | `get_upstream_features` | L10:F14965@2, k=10 → Emb:"She"@1 (de=5.50) +9 more |
| 13 | `get_upstream_features` | L12:F14970@12, k=10 → Emb:" Sarah"@12 (de=4.62) +9 more |
| 14 | `get_upstream_features` | L10:F14174@1, k=10 → L9:F3056 (de=17.62) +9 more |
| 15 | `get_upstream_features` | L9:F2762@1, k=10 → Emb:"<bos>"@0 (de=15.62) +9 more |
| 16 | `get_upstream_features` | L7:F462@1, k=10 → Emb:"<bos>"@0 (de=21.88) +9 more |
| 17 | `get_upstream_features` | L7:F5741@1, k=10 → Emb:"<bos>"@0 (de=12.75) +9 more |
| 18 | `get_upstream_features` | L9:F3056@1, k=10 → Emb:"<bos>"@0 (de=13.62) +9 more |
| 19 | `get_upstream_features` | L5:F3992@1, k=10 → Emb:"<bos>"@0 (de=22.50) +9 more |
| 20 | `get_upstream_features` | L10:F10933@1, k=10 → L9:F2762 (de=10.38) +9 more |
| 21 | `get_upstream_features` | L9:F8770@1, k=10 → L7:F462 (de=16.62) +9 more |
| 22 | `get_upstream_features` | L10:F6804@1, k=10 → L9:F3056 (de=8.75) +9 more |
| 23 | `get_upstream_features` | L9:F15819@1, k=10 → L7:F462 (de=13.94) +9 more |
| 24 | `get_upstream_features` | L9:F13483@1, k=10 → Emb:"<bos>"@0 (de=12.75) +9 more |
| 25 | `get_upstream_features` | L11:F11186@1, k=10 → L9:F2762 (de=16.38) +9 more |
| 26 | `get_upstream_features` | L12:F3684@1, k=10 → L11:F11186 (de=-8.06) +9 more |
| 27 | `get_upstream_features` | L0:F7532@12, k=10 → Emb:" Sarah"@12 (de=21.50) +9 more |
| 28 | `get_upstream_features` | L4:F1276@12, k=10 → Emb:" Sarah"@12 (de=7.91) +9 more |
| 29 | `get_upstream_features` | L11:F3780@12, k=10 → L0:F7532 (de=4.47) +9 more |
| 30 | `get_upstream_features` | L8:F576@12, k=10 → L0:F7532 (de=4.94) +9 more |
| 31 | `get_upstream_features` | L6:F5355@12, k=10 → L0:F7532 (de=3.75) +9 more |
| 32 | `get_upstream_features` | L2:F1056@12, k=10 → L0:F7532 (de=8.62) +9 more |
| 33 | `get_upstream_features` | L2:F5859@12, k=10 → L0:F7532 (de=5.16) +9 more |
| 34 | `get_upstream_features` | L5:F10952@1, k=10 → Emb:"She"@1 (de=8.56) +9 more |
| 35 | `get_upstream_features` | L9:F2587@2, k=10 → Emb:"She"@1 (de=5.56) +9 more |

### Build

`build_circuit` → 29 nodes, 37 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 29,679 | 8,798 | 139,974 | 0 | $0.0279 | — | — |
| **Total** | | **29,679** | **8,798** | **139,974** | **0** | **$0.0279** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 42s