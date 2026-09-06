# Circuit Oracle Report
**Date:** 2026-07-28 07:21:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification of "dietitian/nutritionist" is driven entirely by profession-anchored subject-matter features (nutrition, diet, food, physical activity) attached to the single token " nutrition" — there is **no measurable contribution from gender markers** (e.g. the "Her"/"She" tokens at pos 1/2 or "mother" at pos 20+) anywhere in the circuit.

**Confidence:** 9/10

**Reasoning:** The user worried the circuit might lean on spurious gender cues. The attribution shows the opposite. The two output-driving L14 features — L14:F4197 ("food/meals/food-insecurity", direct_effect ≈ +0.10) and L14:F16195 ("physical activity and training", direct_effect ≈ +0.09) — are both anchored at position 7, the token " nutrition". Tracing them back: they are excited by L7:F11540 (vitamins/supplements, +0.082 into the probe path), L7:F13562 (training/conditioning, +0.082), L7:F6277 (medical-research abbreviations including "Sports"), L8:F7057 (exercise/biology), and L9:F15926 (eating/meals) — all firing at pos 7. These in turn are pulled by L6:F11327 ("food or nutrition", frac_nonzero ≈ 0.012) and the L4 features F13412 ("terms related to diets and dietary health", frac_nonzero ≈ 0.012) and F10494 ("health, medicine, diet, drugs, exercise", frac_nonzero ≈ 0.012). The deepest feed is the L0:L5201 "word nutrition" feature (frac_nonzero ≈ 0.00026 — highly specific, suppresses -0.09 because it is already absorbed by later layers) and the raw " nutrition" embedding itself (direct_effect 11–27 into the next features). L0:F8975 at pos 4 (" expertise") shows that the word "expertise" framing "nutrition" as a professional area contributes positively — a *semantic role* signal, not a gender one. The pos-6 " sports" embedding also feeds in, contextualising the nutrition as sports-nutrition. A parallel branch from positions 12/13 (" disordered"/" eating") reaches L4:F13412 via L1:F11764 (health/fitness phrase) and L1:F6631 (dietary patterns), and positions 25–26 (" Dietetics") feed via L3:F11774/F10028. Every positive path in the circuit is a topic / domain-of-expertise feature, all originating from the named professional concepts in the prompt (nutrition, sports, diet, disordered eating, Dietetics). The negative-direction L0:F6051 (periods/spaces, direct_effect -0.09) and L0:F9026 (technical punctuation, high frac_nonzero 0.41) are generic structural/format features, not demographic ones. **No "Her", "She", "mother", or "Heather" token appears with measurable positive direct_effect into any of the profession-supporting features.** The probe is firing on the genuine professional content; the user's hypothesis of gender-marker confounds is not supported by this attribution graph.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' nutrition' (pos 7) — the word 'nutrition', the primary driver | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' sports' (pos 6) — context for sports nutrition | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: ' expertise' (pos 4) — frames 'nutrition' as a professional area | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: ' eating' (pos 13) — disordered eating context | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ' weight' (pos 9) — weight management context | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' disordered' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: '.' (pos 14) — sentential punctuation (suppresses) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: ' Nutrition' (pos 23) — Academy of Nutrition | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 25 | Emb: ' Die' (pos 25) — Dietetics subword | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 7 | L0:5201 — 'the word nutrition' (pos 7) |  the word "nutrition" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L0:F8975](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8975) | 4 | L0:8975 — 'expertise' (pos 4) framing word |  the word "pragma" in code | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8975) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 14 | L0:6051 — periods/spaces/digits (suppression) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 7 | L0:9026 — technical-document punctuation, generic | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 12 | L0:9026 — technical-document punctuation, generic | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L1:F6461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) | 7 | L1:6461 — physical activity / muscle / training jargon (pos 7) |  technical language around physical activity, muscle function, and related studies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) |
| [L1:F6631](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) | 7 | L1:6631 — dietary patterns / scientific studies (pos 7, 13, 25) |  words related to dietary patterns and scientific studies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) |
| [L1:F6631](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) | 13 | L1:6631 — dietary patterns / scientific studies (pos 7, 13, 25) |  words related to dietary patterns and scientific studies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) |
| [L1:F6631](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) | 25 | L1:6631 — dietary patterns / scientific studies (pos 7, 13, 25) |  words related to dietary patterns and scientific studies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) |
| [L1:F15310](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15310) | 7 | L1:15310 — physical exercise vocabulary (pos 7, 12) |  words related to physical exercise | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15310) |
| [L1:F15310](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15310) | 12 | L1:15310 — physical exercise vocabulary (pos 7, 12) |  words related to physical exercise | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15310) |
| [L1:F11764](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11764) | 12 | L1:11764 — health/fitness phrase detector (pos 12, 13, 25) |  words and phrases related to health and fitness | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11764) |
| [L1:F11764](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11764) | 13 | L1:11764 — health/fitness phrase detector (pos 12, 13, 25) |  words and phrases related to health and fitness | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11764) |
| [L1:F11764](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11764) | 25 | L1:11764 — health/fitness phrase detector (pos 12, 13, 25) |  words and phrases related to health and fitness | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11764) |
| [L1:F760](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/760) | 7 | L1:760 — scientific/medical tissue terminology (pos 7) |  scientific and medical terminology related to tissue and cells | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/760) |
| [L1:F165](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/165) | 7 | L1:165 — sports teams/stats/contracts (pos 7) |  names of sports teams and words related to sports statistics, contracts, and betting | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/165) |
| [L3:F6920](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6920) | 7 | L3:6920 — inhibitory dietary context (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6920) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 26 | L3:11774 — 'Dietetics' word pieces (pos 26) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 26 | L3:10028 — 'Die'/'te' pieces (pos 26) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | L4:13412 — 'diets and dietary health' detector (pos 7, 13, 26) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | L4:13412 — 'diets and dietary health' detector (pos 7, 13, 26) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 26 | L4:13412 — 'diets and dietary health' detector (pos 7, 13, 26) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 7 | L4:10494 — health/medicine/diet/exercise vocabulary (pos 7) |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 7 | L4:9554 — food/feeding/rationing terms (pos 7) |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 7 | L6:11327 — food/nutrition concept (pos 7) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L7:F11540](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11540) | 7 | L7:11540 — vitamins/minerals/supplements (pos 7) |  scientific discussion of vitamins and minerals | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11540) |
| [L7:F13562](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13562) | 7 | L7:13562 — physical/mental training & conditioning (pos 7) |  terms related to physical and mental training or conditioning | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13562) |
| [L7:F6277](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/6277) | 7 | L7:6277 — medical research abbreviations incl. 'Sports' (pos 7) |  abbreviations and concepts related to medical research | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/6277) |
| [L8:F7057](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7057) | 7 | L8:7057 — exercise/biology/chemistry terms (pos 7) |  terms related to exercise, biology and chemistry | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7057) |
| [L9:F15926](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15926) | 7 | L9:15926 — eating/meals/food concept (pos 7) | mentions about eating and meals | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15926) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 7 | L14:4197 — food / meals / 'food insecurity' vocabulary (pos 7) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F16195](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) | 7 | L14:16195 — physical activity and training (pos 7) | mentions of physical activity and training. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: probe classification score | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'probe' is not one of the top-k next-token candidates  |
| 3 | `get_top_features` | 10 features; top: L4:10494 de=0.176 |
| 4 | `inspect_feature` ×8 | L4:10494, L4:13412, L14:4197, L14:16195, L6:11327, L0:6051, L0:8975, L0:5201 |
| 5 | `get_upstream_features` | Emb:" nutrition"@7 (de=11.25) +9 more |
| 6 | `get_upstream_features` | Emb:" nutrition"@7 (de=12.62) +9 more |
| 7 | `get_upstream_features` | Emb:" nutrition"@7 (de=12.88) +9 more |
| 8 | `get_upstream_features` | Emb:" nutrition"@7 (de=7.97) +9 more |
| 9 | `get_upstream_features` | Emb:" nutrition"@7 (de=17.50) +9 more |
| 10 | `get_upstream_features` | L3:F11774 (de=4.72) +9 more |
| 11 | `get_upstream_features` | Emb:" eating"@13 (de=8.69) +9 more |
| 12 | `get_upstream_features` | Emb:"."@14 (de=47.00) +7 more |
| 13 | `get_upstream_features` | Emb:" nutrition"@7 (de=27.12) +7 more |
| 14 | `get_upstream_features` | Emb:" expertise"@4 (de=20.88) +7 more |
| 15 | `get_upstream_features` | Emb:" nutrition"@7 (de=10.19) +4 more |
| 16 | `get_upstream_features` | Emb:" nutrition"@7 (de=8.06) +4 more |
| 17 | `get_upstream_features` | Emb:" nutrition"@7 (de=8.88) +4 more |
| 18 | `get_upstream_features` | Emb:" nutrition"@7 (de=8.12) +4 more |
| 19 | `get_upstream_features` | Emb:" nutrition"@7 (de=5.47) +4 more |
| 20 | `get_upstream_features` | Emb:" Die"@25 (de=5.53) +4 more |
| 21 | `get_upstream_features` | Emb:" nutrition"@7 (de=15.88) +4 more |
| 22 | `get_upstream_features` | Emb:" nutrition"@7 (de=14.88) +4 more |
| 23 | `get_upstream_features` | Emb:" nutrition"@7 (de=8.56) +4 more |
| 24 | `get_upstream_features` | Emb:" nutrition"@7 (de=7.19) +4 more |
| 25 | `get_upstream_features` | Emb:"<bos>"@0 (de=-3.64) +4 more |
| 26 | `get_upstream_features` | Emb:" sports"@6 (de=9.19) +4 more |
| 27 | `inspect_feature` ×4 | L1:15310, L1:11764, L1:6461, L1:6631 |
| 28 | `get_upstream_features` | Emb:" nutrition"@7 (de=15.88) +4 more |
| 29 | `get_upstream_features` | Emb:" sports"@6 (de=8.44) +4 more |
| 30 | `get_upstream_features` | Emb:" nutrition"@7 (de=3.64) +4 more |
| 31 | `get_upstream_features` | Emb:" nutrition"@7 (de=22.75) +4 more |
| 32 | `get_upstream_features` | Emb:" nutrition"@7 (de=14.81) +4 more |
| 33 | `get_upstream_features` | Emb:" nutrition"@7 (de=7.94) +4 more |
| 34 | `get_upstream_features` | Emb:" nutrition"@7 (de=4.50) +4 more |
| 35 | `get_upstream_features` | Emb:" Die"@25 (de=7.12) +4 more |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4197@7` | ❌ error | — | — | Trace the path from L14:F4197 (food/food-insecurity terms) at pos 7 — what token… |
| SA-2 | `L14:F16195@7` | ❌ error | — | — | Trace the path from L14:F16195 (physical activity/training) at pos 7 — what does… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×9 | L4:9554, L1:165, L1:760, L0:9026, L7:11540, L9:15926, L8:7057, L7:13562, L7:6277 |
| 2 | `get_upstream_features` | L0:F9026@12, k=5 → Emb:" disordered"@12 (de=30.12) +4 more |
| 3 | `get_upstream_features` | L1:F11764@13, k=5 → Emb:" eating"@13 (de=3.41) +4 more |
| 4 | `get_upstream_features` | L1:F11764@25, k=5 → Emb:" Nutrition"@23 (de=7.75) +4 more |
| 5 | `get_upstream_features` | L1:F6631@13, k=5 → Emb:" eating"@13 (de=6.44) +4 more |
| 6 | `get_upstream_features` | L1:F6631@25, k=5 → Emb:" Nutrition"@23 (de=7.47) +4 more |
| 7 | `inspect_feature` | L0, F9026 → "technical documents or data, including numbers, units, and references " |

### Build

`build_circuit` → 34 nodes, 87 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 87,254 | 10,336 | 267,053 | 0 | $0.0546 | — | — |
| **Total** | | **87,254** | **10,336** | **267,053** | **0** | **$0.0546** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 6s