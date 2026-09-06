# Circuit Oracle Report
**Date:** 2026-07-28 07:00:39 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is driven primarily by topic-content features detecting *nutrition/diet/health/food* (with secondary activation on *sports/weight/training*) anchored at the token `nutrition` (pos 7), not by the female-pronoun or `spokesperson` markers; gender and role tokens are weak suppressors (negative direct_effect) and carry negligible multi-hop influence (S_over_R≈0.57, well below 1).

**Confidence:** 9

**Reasoning:** Signal flows from the input token ` nutrition` (pos 7) up through a tightly coupled profession-topic pipeline. The token embedding is the dominant driver of L0:5201 ("the word `nutrition`", activation 23.75, frac_nonzero 0.00026) and the L4 topic-dictionary features L4:10494 ("health/medicine/diet/exercise", direct_effect 0.176) and L4:13412 ("diets and dietary health", direct_effect 0.142 at pos 7). These feed L6:11327 ("food or nutrition", direct_effect 0.082) and L7:13562 ("training/conditioning"), then L14:4197 ("food insecurity"-style food words, direct_effect 0.101) and L14:16195 ("physical activity and training", direct_effect 0.085), with L17:7545 ("architecture, design, nurses and healthcare") and L17:14680 adding profession/healthcare signal. The chain converges on L18:6105 and especially L19:1589 ("a context of scientific, especially nutritional, studies", activation 55.25, direct_effect 0.066 at pos 26), which is the largest single output-driving feature and whose top activating examples are *nutrition*/*dietary* in scientific contexts — i.e., a real profession-content signal, not a gender signal.

By contrast, the user's hypothesized "spurious gender" pathway runs through L0:9519 ("she/her"), L0:15322 ("herself/itself"), L0:2268 ("spokesman/spokeswoman", pos 18), and L0:8028 ("areas") — all of which appear in the top-20 but with **negative** direct_effect on the probe (L0:9519 −0.081, L0:2268 −0.081, L0:8028 −0.074, L0:15322 −0.074, L0:6051 −0.091). They mildly *suppress* the probe score, the opposite of what a gender-bias concern would predict. The `get_source_influence` multi-hop test confirms this: the "pure pronoun" subset (positions 1, 4, 18) carries S_pct_of_total = 3.0% with S_over_R = 0.57 — source far weaker than the top non-source driver, i.e., the gender/role tokens are *not* the mechanism. When the same test is widened to include all content-keyword positions (1, 2, 4, 6, 7, 9, 12, 13, 14, 18), S_pct_of_total rises to 13.8% and S_over_R = 6.6, with the top contributors being L1:6461 and L1:11764 (health/fitness words at the content positions) — i.e., the nutrition/health content tokens carry the probe, and `Her` merely rides along as a generic L0 token.

The circuit is therefore a clean *content-driven* profession classification: the model has read the explicit profession-indicating tokens (sports nutrition, weight management, disordered eating, Academy of Nutrition and Dietetics, spokesperson, dietary, Dietetics), and the probe fires on the dietetics-nutrition-healthcare concept — exactly the bio's named profession. Gender markers are present in the input and activate features, but they reduce rather than produce the probe's classification score.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 7 | Layer 0 token-identity features (profession/content keywords) |  the word "nutrition" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L0:F10254](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10254) | 6 | Layer 0 token-identity features (profession/content keywords) |  the word "sports". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10254) |
| [L0:F10148](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10148) | 1 | Layer 0 token-identity features (profession/content keywords) |  the word "entire," sometimes near the word "this" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10148) |
| [L0:F2083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2083) | 4 | Layer 0 token-identity features (profession/content keywords) |  the word "plot" referring to land or experimental zones | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2083) |
| [L0:F4030](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) | 4 | Layer 0 token-identity features (profession/content keywords) |  words related to mission statements and personal development used in career environments | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4030) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | Layer 0 pronoun / role / domain-words (provide context, weakly suppress probe) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F2268](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2268) | 18 | Layer 0 pronoun / role / domain-words (provide context, weakly suppress probe) |  mentions of people communicating information via speech | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2268) |
| [L0:F15322](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) | 4 | Layer 0 pronoun / role / domain-words (provide context, weakly suppress probe) | reflexive pronouns, particularly "herself" and "itself." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) |
| [L0:F8975](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8975) | 4 | Layer 0 pronoun / role / domain-words (provide context, weakly suppress probe) |  the word "pragma" in code | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8975) |
| [L0:F8028](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8028) | 2 | Layer 0 pronoun / role / domain-words (provide context, weakly suppress probe) | references to geographical areas in various contexts including scientific and societal | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8028) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 14 | Layer 0 pronoun / role / domain-words (provide context, weakly suppress probe) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 7 | Layer 4 nutrition/diet/health topic dictionaries |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | Layer 4 nutrition/diet/health topic dictionaries |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Layer 4 nutrition/diet/health topic dictionaries |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 26 | Layer 4 nutrition/diet/health topic dictionaries |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 7 | Layer 6-7 mid-layer semantic synthesis (food/nutrition, training) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L7:F11540](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11540) | 7 | Layer 6-7 mid-layer semantic synthesis (food/nutrition, training) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11540) |
| [L7:F13562](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13562) | 7 | Layer 6-7 mid-layer semantic synthesis (food/nutrition, training) |  terms related to physical and mental training or conditioning | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13562) |
| [L8:F7057](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7057) | 7 | Layer 6-7 mid-layer semantic synthesis (food/nutrition, training) |  terms related to exercise, biology and chemistry | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7057) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 7 | Layer 14-17 specific-topic features (food, weight, training) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F16195](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) | 7 | Layer 14-17 specific-topic features (food, weight, training) | mentions of physical activity and training. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) |
| [L14:F16195](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) | 9 | Layer 14-17 specific-topic features (food, weight, training) | mentions of physical activity and training. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) |
| [L14:F9449](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/9449) | 9 | Layer 14-17 specific-topic features (food, weight, training) |  snippets related to weight and diet | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/9449) |
| [L17:F13102](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/13102) | 9 | Layer 14-17 specific-topic features (food, weight, training) |  words related to body weight and weight loss interventions | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/13102) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 26 | Layer 14-17 specific-topic features (food, weight, training) | mentions of architecture, design, nurses and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 7 | Layer 14-17 specific-topic features (food, weight, training) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 7 | Layer 18-19 output-driving features (nutrition-context, healthcare-profession) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 26 | Layer 18-19 output-driving features (nutrition-context, healthcare-profession) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 7 | Layer 18-19 output-driving features (nutrition-context, healthcare-profession) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 26 | Layer 18-19 output-driving features (nutrition-context, healthcare-profession) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:10494 de=0.176 |
| 3 | `inspect_feature` ×17 | L4:10494, L4:13412, L14:4197, L14:16195, L19:1589, L6:11327, L0:6051, L0:8975, L0:5201, L0:2268, L0:9519, L0:8028, L0:15322, L0:10254, L0:10148, L0:2083, L0:4030 |
| 4 | `get_upstream_features` | Emb:" nutrition"@7 (de=11.25) +14 more |
| 5 | `get_upstream_features` | Emb:" nutrition"@7 (de=12.62) +14 more |
| 6 | `get_upstream_features` | Emb:" nutrition"@7 (de=32.25) +14 more |
| 7 | `get_upstream_features` | Emb:" nutrition"@7 (de=12.88) +14 more |
| 8 | `get_upstream_features` | Emb:" nutrition"@7 (de=7.97) +14 more |
| 9 | `get_upstream_features` | L17:F7545 (de=10.38) +14 more |
| 10 | `get_upstream_features` | L3:F11774 (de=4.72) +14 more |
| 11 | `get_upstream_features` | Emb:" eating"@13 (de=8.69) +14 more |
| 12 | `get_upstream_features` | Emb:" nutrition"@7 (de=17.50) +11 more |
| 13 | `get_upstream_features` | Emb:"Her"@1 (de=16.75) +9 more |
| 14 | `get_upstream_features` | Emb:" nutrition"@7 (de=27.12) +9 more |
| 15 | `get_upstream_features` | L6:F11327 (de=6.22) +14 more |
| 16 | `get_upstream_features` | ❌ Feature (layer=14, feature_idx=16195) not found at pos=26. T |
| 17 | `get_upstream_features` | Emb:"Her"@1 (de=10.06) +9 more |
| 18 | `get_upstream_features` | Emb:" expertise"@4 (de=11.88) +9 more |
| 19 | `get_upstream_features` | Emb:" expertise"@4 (de=7.53) +9 more |
| 20 | `get_upstream_features` | L8:F7057 (de=4.28) +9 more |
| 21 | `get_upstream_features` | Emb:" nutrition"@7 (de=9.50) +14 more |
| 22 | `get_upstream_features` | Emb:"Her"@1 (de=10.06) +9 more |
| 23 | `get_upstream_features` | Emb:"Her"@1 (de=16.75) +9 more |
| 24 | `inspect_feature` ×4 | L17:7545, L3:11774, L8:7057, L3:10028 |
| 25 | `get_upstream_features` | Emb:" spokesperson"@18 (de=23.50) +9 more |
| 26 | `get_upstream_features` | Emb:"."@14 (de=47.00) +9 more |
| 27 | `get_upstream_features` | Emb:" sports"@6 (de=25.50) +9 more |
| 28 | `get_upstream_features` | Emb:" expertise"@4 (de=20.88) +9 more |
| 29 | `get_upstream_features` | Emb:" areas"@2 (de=18.00) +9 more |
| 30 | `get_upstream_features` | Emb:" expertise"@4 (de=14.81) +9 more |
| 31 | `get_upstream_features` | Emb:" nutrition"@7 (de=7.97) +9 more |
| 32 | `inspect_feature` ×5 | L7:13562, L1:11764, L8:3161, L14:9449, L17:13102 |
| 33 | `get_upstream_features` | Emb:" nutrition"@7 (de=32.25) +9 more |
| 34 | `get_upstream_features` | ❌ Feature (layer=1, feature_idx=11764) not found at pos=7. Thi |
| 35 | `get_upstream_features` | Emb:" nutrition"@7 (de=7.19) +4 more |
| 36 | `get_upstream_features` | Emb:" nutrition"@7 (de=7.72) +4 more |
| 37 | `get_upstream_features` | L17:F7545 (de=10.38) +14 more |
| 38 | `get_upstream_features` | L17:F7545 (de=9.31) +4 more |
| 39 | `get_upstream_features` | Emb:" nutrition"@7 (de=31.88) +4 more |
| 40 | `get_source_influence` | {'depth': 2, 'source_positions': [1, 2, 4, 6, 7, 9, 12, 13, 14, 18], 'S_pct_of_t |
| 41 | `get_source_influence` | {'depth': 2, 'source_positions': [1, 4, 18], 'S_pct_of_total': 3.033, 'R_pct_of_ |

### Build

`build_circuit` → 16 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 80,262 | 6,812 | 622,350 | 0 | $0.0696 | — | — |
| **Total** | | **80,262** | **6,812** | **622,350** | **0** | **$0.0696** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 47s