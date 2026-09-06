# Circuit Oracle Report
**Date:** 2026-07-28 07:23:35 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven predominantly by a chain of female-pronoun and female-name features originating from the tokens "Her" (pos 1), "She" (pos 15), and "Heather" (pos 46), with only a small secondary contribution from genuine profession-related content tokens (nutrition, disordered eating, expertise).

**Confidence:** 7

**Reasoning:** The circuit confirms the user's concern — the prediction is largely **gender-driven rather than profession-driven**. The dominant signal path is:

1. **Embedding sources (gender markers):** The strongest direct-effect features feed from the **"Her" (pos 1)** token (direct_effect 18.1 into L6:F11646, 23.1 into L0:F15382, 14.75 into L4:F7864), the **"She" (pos 15)** token (direct_effect 15.25 into L18:F14677, 18.5 into L6:F11646@pos15, 20.25 into L17:F5889, 6.13 into L19:F9685), and the **"Heather" (pos 46)** female first name (direct_effect 11.1 into L4:F1276, 18.6 into L0:F7532, 4.6 into L19:F9685, 4.7 into L18:F14677).

2. **Early pronoun features (L0–L4):** L0:F15382 (fires on "Her"/"She"), L0:F10148 and L0:F7532 (fire on the name "Heather"), L0:F5686 and L4:F7864 amplify the pronoun signal. These act as female-subject detectors rather than profession detectors.

3. **Mid-layer female-subject features (L6–L7):** L6:F11646 is the **single largest direct contributor to the probe** (direct_effect 0.28 at pos 1, 0.20 at pos 15) and receives its top input from the "Her" and "She" embeddings (direct_effect 18.1 and 18.5 respectively), not from profession words. L7:F2765 and L7:F8644 also fire on the name/pronoun positions and feed into L12:F14970 (direct_effect 0.155, 1.37) and then into L18:L19 features.

4. **Late-layer subject features (L17–L19):** L18:F14677 (direct_effect 0.17/0.10), L19:F9685 (direct_effect 0.13/0.10), and L17:F5889 all sit at positions 15 ("She") and 46 ("Heather") — they encode female-subject representations, not "registered dietitian" or "nutritionist."

5. **Genuine profession signal is present but small:** L4:F13412 does fire on the actual content tokens "nutrition" (pos 7, direct_effect 12.6), "disordered" (pos 12), and "eating" (pos 13, direct_effect 8.7), with downstream direct_effect of 0.14/0.10. L12:F14970 contributes 0.155 and is supported by the "expertise" embedding (direct_effect 14) and the "nutrition"/"disordered eating" topic. However, this profession-related branch is **numerically dwarfed** by the pronoun/name branch — e.g. L6:F11646 alone (0.28 + 0.20) out-scales the entire topic branch, and the L18–L19 female-subject features add another 0.10–0.17 each.

6. **The output (pos 1, predicted token) sees the pronoun stack first:** the prediction is generated at a position immediately following "Her" and conditioned on the female-subject context, which biases the model toward a profession stereotypically associated with women.

**Conclusion:** The probe's classification is **substantially confounded by gender markers**. The circuit shows the model/pipeline is using the female pronoun and female first name as a proxy for the profession (likely a stereotype like "dietitian" or "nutritionist"). The genuine content-bearing features (nutrition, disordered eating, expertise) exist in the circuit but contribute a smaller share of the total score. This is consistent with the user's concern about spurious features rather than genuine profession indicators driving the classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Her (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: She (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: Heather (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: expertise (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: nutrition (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: disordered (pos 12) + eating (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: disordered (pos 12) + eating (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Early pronoun/name detection (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F10148](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10148) | 1 | Early pronoun/name detection (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10148) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 46 | Early pronoun/name detection (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F5686](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5686) | 4 | Early pronoun/name detection (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5686) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 14 | Early pronoun/name detection (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Early pronoun/name detection (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 46 | Early pronoun/name detection (L0-L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | Topic/keyword features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Topic/keyword features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer pronoun/female features (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 15 | Mid-layer pronoun/female features (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 46 | Mid-layer pronoun/female features (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 46 | Mid-layer pronoun/female features (L6-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 46 | Mid-layer profession-relevant (L12) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 15 | Late-layer female subject features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 15 | Late-layer female subject features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 46 | Late-layer female subject features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 15 | Late-layer female subject features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 46 | Late-layer female subject features (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.283 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ❌ error | — | — | Trace the path upstream from L6:F11646 at pos 1 (which has direct_effect 0.28 on… |
| SA-2 | `L18:F14677@15` | ❌ error | — | — | Trace the path upstream from L18:F14677 at pos 15 (direct_effect 0.17). What doe… |
| SA-3 | `L19:F9685@46` | ❌ error | — | — | Trace the path upstream from L19:F9685 at pos 46 (direct_effect 0.13). What does… |
| SA-4 | `L4:F13412@7` | ❌ error | — | — | Trace the path upstream from L4:F13412 at pos 7 (direct_effect 0.14). What does … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"Her"@1 (de=18.12) +9 more |
| 2 | `get_upstream_features` | L18:F14677@15, k=10 → Emb:" She"@15 (de=15.25) +9 more |
| 3 | `get_upstream_features` | L19:F9685@46, k=10 → Emb:" Heather"@46 (de=4.62) +9 more |
| 4 | `get_upstream_features` | L4:F13412@7, k=10 → Emb:" nutrition"@7 (de=12.62) +9 more |
| 5 | `get_upstream_features` | L4:F1276@46, k=10 → Emb:" Heather"@46 (de=11.12) +9 more |
| 6 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"Her"@1 (de=14.75) +9 more |
| 7 | `get_upstream_features` | L6:F11646@15, k=10 → Emb:" She"@15 (de=18.50) +9 more |
| 8 | `get_upstream_features` | L0:F15382@1, k=10 → Emb:"Her"@1 (de=23.12) +9 more |
| 9 | `get_upstream_features` | L12:F14970@46, k=10 → Emb:"<bos>"@0 (de=-5.22) +9 more |
| 10 | `get_upstream_features` | L7:F2765@46, k=10 → Emb:" She"@15 (de=1.65) +9 more |
| 11 | `get_upstream_features` | L19:F9685@15, k=10 → Emb:" She"@15 (de=6.12) +9 more |
| 12 | `get_upstream_features` | L18:F14677@46, k=10 → Emb:"Her"@1 (de=6.16) +9 more |
| 13 | `get_upstream_features` | L17:F5889@15, k=8 → Emb:" She"@15 (de=20.25) +7 more |
| 14 | `get_upstream_features` | L0:F6051@14, k=8 → Emb:"."@14 (de=47.00) +7 more |
| 15 | `get_upstream_features` | L0:F5686@4, k=8 → Emb:" expertise"@4 (de=14.00) +7 more |
| 16 | `get_upstream_features` | L0:F7532@46, k=8 → Emb:" Heather"@46 (de=18.62) +7 more |
| 17 | `get_upstream_features` | L4:F7864@1, k=8 → Emb:"Her"@1 (de=14.75) +7 more |
| 18 | `get_upstream_features` | L7:F8644@46, k=8 → Emb:" She"@15 (de=3.98) +7 more |
| 19 | `get_upstream_features` | L4:F13412@13, k=8 → Emb:" eating"@13 (de=8.69) +7 more |
| 20 | `get_upstream_features` | L0:F10148@1, k=8 → Emb:"Her"@1 (de=10.06) +7 more |
| 21 | `get_upstream_features` | L14:F12501@13, k=8 → Emb:" eating"@13 (de=-6.28) +7 more |

### Build

`build_circuit` → 12 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 31,467 | 5,285 | 64,891 | 0 | $0.0197 | — | — |
| **Total** | | **31,467** | **5,285** | **64,891** | **0** | **$0.0197** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 58s