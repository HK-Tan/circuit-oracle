# Circuit Oracle Report
**Date:** 2026-07-28 07:23:30 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "dietitian" is driven by a genuine, semantic nutrition/diet profession-circuit, not by gender markers — the signal flows from input token embeddings of profession terms ("Nutritional", "Diet/Dietitian", "nutrition", "RD", "Sports Nutrition") through a deep cascade of nutrition/diet-specific features up to L19's "scientific/nutritional studies" context feature (F1589).

**Confidence:** 7

**Reasoning:** The circuit has a clean profession-semantic structure with no dependency on gendered features:

- **L0–L1 "early" features (F14824 "has", F9519 "she/her", F8974 "from", F8061 "in") appear with NEGATIVE direct_effects in the top_features for the probe** (e.g. L0:F9519 has -0.05, L0:F8061 has -0.041, L0:F14824's "has" is suppressed). The only positive L0 contribution at the top is F9888 at pos 18 ("education") = +0.043, also profession-irrelevant but trivially small.
- **The strong positive signal begins at L4: F13412 ("terms related to diets and dietary health")** with direct_effect 0.154 at pos 21 ("Die" → "Dietetics"), and a ~0.12 contribution at pos 22. This is a pure diet-terminology detector, not a gendered one (promoted tokens: "diet", "diets", "DIET", "dieting"; frac_nonzero 0.012).
- **L2: F2589 ("medical professionals/specialties")** at pos 37 ("titian" / "Dietitian") provides +0.059, driven primarily by the "titian" embedding itself (19.1 direct_effect) and "Die" at pos 36. This is a true profession-title detector (promoted: "experts", "specialists", "expert").
- **L6: F11327 ("food or nutrition" concept)** at pos 21 contributes +0.068; its upstream is overwhelmingly the "Die" token embedding (2.31) and the L4 diet feature (5.88), not pronouns.
- **L8–L14 form a dietary-content cascade**: L8:7732 ("academia/scientific research"), L8:8003 ("nutrients, foods, minerals… dietary studies, children's health"), L9:15926 ("eating and meals"), L14:4197 ("food insecurity"-style eating context) all support the L19 hub.
- **L17: F14680 ("nutrition, food, diets")** is the strongest single late-layer input, with direct embedding "Nutritional" (30.9) at pos 9, and **L17: F7545 ("architecture, design, nurses and healthcare")** at pos 21 is a healthcare-profession-domain feature that the model has grouped with the dietitian context.
- **L18: F6105 ("text related to eating and health")** and the terminal **L19: F1589 ("context of scientific, specially nutritional, studies")** (frac_nonzero 0.038, promoted tokens: "diet, food, nutrition, diets, feeding, dietary, eating") drive the probe output. L19:F1589 has a substantial positive direct_effect on the probe (+0.064) at pos 21, with upstream dominated by L4:F13412 (+10.7), L6:F11327 (+8.4), L14:F4197 (+8.4), L17:F7545 (+7.2), and the "Die" embedding (+7.2) — i.e., a profession/terminology feed, not a pronoun feed.

Crucially, when tracing upstream from each strong late-layer feature, the most positive contributors are always: (a) the "Die"/"Nutritional"/"Nutrition"/"titian"/"RD" token embeddings themselves, and (b) other diet-terminology features. The pronoun feature L0:F9519 ("she"/"her") does appear in the early_layer supernode, but it is **suppressed** (it appears in the top features with negative direct_effect −0.05, and the gender-pronoun token is not a top upstream of any profession-driving feature in positive direction). If anything, the pronoun signal slightly *pushes against* the probe's diet-direction (the "te" sub-token at pos 21 and "<bos>" at pos 0 are also negative upstream contributors).

**Conclusion on the user's concern:** The user's hypothesis is *not* supported. The probe circuit is anchored in genuine profession-indicator tokens and a deep hierarchy of nutrition/dietary terminfo features. Gender markers are present only as generic L0 lexical detectors that contribute weakly and *negatively* to the classification — they are not load-bearing. If anything, the model appears to be using profession-specific vocabulary (Dietetics, Dietitian, Nutritional, nutrition, RD, Sports Nutrition) and food/eating research register to drive the dietititan probe, which is the *expected* mechanism.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 2 | Early-layer lexical features (L0–L1): 'has' (L0:14824), 'from' (L0:8974), 'she/her' pronoun (L0:9519), 'in' preposition (L0:8061), physical-activity language (L1:6461) | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | Early-layer lexical features (L0–L1): 'has' (L0:14824), 'from' (L0:8974), 'she/her' pronoun (L0:9519), 'in' preposition (L0:8061), physical-activity language (L1:6461) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 11 | Early-layer lexical features (L0–L1): 'has' (L0:14824), 'from' (L0:8974), 'she/her' pronoun (L0:9519), 'in' preposition (L0:8061), physical-activity language (L1:6461) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 8 | Early-layer lexical features (L0–L1): 'has' (L0:14824), 'from' (L0:8974), 'she/her' pronoun (L0:9519), 'in' preposition (L0:8061), physical-activity language (L1:6461) |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L1:F6461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) | 64 | Early-layer lexical features (L0–L1): 'has' (L0:14824), 'from' (L0:8974), 'she/her' pronoun (L0:9519), 'in' preposition (L0:8061), physical-activity language (L1:6461) |  technical language around physical activity, muscle function, and related studies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6461) |
| [L1:F6631](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) | 55 | Early-layer lexical features (L0–L1): 'has' (L0:14824), 'from' (L0:8974), 'she/her' pronoun (L0:9519), 'in' preposition (L0:8061), physical-activity language (L1:6461) |  words related to dietary patterns and scientific studies | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6631) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 37 | L2: medical professionals/specialties feature (F2589) at pos 37 'Dietitian' — profession/title detector |  words related to medical professionals and medical specialties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 21 | L4: diet/dietary-health term detector (F13412) — multi-position on 'Die' (Diet/Dietitian), 'Nutritional', 'Nutrition' |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | L4: diet/dietary-health term detector (F13412) — multi-position on 'Die' (Diet/Dietitian), 'Nutritional', 'Nutrition' |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 9 | L4: diet/dietary-health term detector (F13412) — multi-position on 'Die' (Diet/Dietitian), 'Nutritional', 'Nutrition' |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 50 | L4: diet/dietary-health term detector (F13412) — multi-position on 'Die' (Diet/Dietitian), 'Nutritional', 'Nutrition' |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 37 | L4: diet/dietary-health term detector (F13412) — multi-position on 'Die' (Diet/Dietitian), 'Nutritional', 'Nutrition' |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 55 | L4: diet/dietary-health term detector (F13412) — multi-position on 'Die' (Diet/Dietitian), 'Nutritional', 'Nutrition' |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 64 | L4: diet/dietary-health term detector (F13412) — multi-position on 'Die' (Diet/Dietitian), 'Nutritional', 'Nutrition' |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 64 | L4: diet/dietary-health term detector (F13412) — multi-position on 'Die' (Diet/Dietitian), 'Nutritional', 'Nutrition' | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 21 | L4: diet/dietary-health term detector (F13412) — multi-position on 'Die' (Diet/Dietitian), 'Nutritional', 'Nutrition' |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 21 | L4: diet/dietary-health term detector (F13412) — multi-position on 'Die' (Diet/Dietitian), 'Nutritional', 'Nutrition' |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 21 | L6: food/nutrition general concept (F11327) — multi-position |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 9 | L6: food/nutrition general concept (F11327) — multi-position |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 50 | L6: food/nutrition general concept (F11327) — multi-position |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 64 | L6: food/nutrition general concept (F11327) — multi-position |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 37 | L6: food/nutrition general concept (F11327) — multi-position |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L8:F7732](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7732) | 21 | L8–L9: academic/research register (F7732), nutrients (F8003), eating/meals (F15926) |  terms relating to academia and scientific research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7732) |
| [L8:F8003](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8003) | 21 | L8–L9: academic/research register (F7732), nutrients (F8003), eating/meals (F15926) |  words about nutrients, foods, and minerals, especially regarding dietary studies and children's health. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8003) |
| [L9:F15926](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15926) | 21 | L8–L9: academic/research register (F7732), nutrients (F8003), eating/meals (F15926) | mentions about eating and meals | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15926) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | L14: food insecurity/eating-context feature (F4197) — multi-position |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 50 | L14: food insecurity/eating-context feature (F4197) — multi-position |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 21 | L14: food insecurity/eating-context feature (F4197) — multi-position |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 9 | L17: nutrition/diets (F14680), architecture/design/nurses/healthcare (F7545) — profession-domain context | nutrition, food, and diets | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 50 | L17: nutrition/diets (F14680), architecture/design/nurses/healthcare (F7545) — profession-domain context | nutrition, food, and diets | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 21 | L17: nutrition/diets (F14680), architecture/design/nurses/healthcare (F7545) — profession-domain context | mentions of architecture, design, nurses and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 9 | L18: text about eating and health (F6105) | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 50 | L18: text about eating and health (F6105) | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 21 | L19: scientific/nutritional studies context (F1589) — top output-driving feature at pos 21 ('Dietetics') |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 9 | L19: scientific/nutritional studies context (F1589) — top output-driving feature at pos 21 ('Dietetics') |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 50 | L19: scientific/nutritional studies context (F1589) — top output-driving feature at pos 21 ('Dietetics') |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:13412 de=0.154 |
| 3 | `inspect_feature` ×6 | L4:13412, L19:1589, L14:4197, L6:11327, L2:2589, L0:14824 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@21` | ❌ error | — | — | Trace the upstream path from L19:F1589 at pos 21. Determine the full provenance … |
| SA-2 | `L14:F4197@21` | ❌ error | — | — | Trace the upstream path from L14:F4197 at pos 21 ("food insecurity" feature). Fi… |
| SA-3 | `L6:F11327@21` | ❌ error | — | — | Trace L6:F11327 at pos 21 ("food/nutrition" feature) upstream. Identify what tok… |
| SA-4 | `L2:F2589@37` | ❌ error | — | — | Trace L2:F2589 at pos 37 ("medical professionals/specialties" feature) upstream.… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F1589@21, k=15 → L4:F13412 (de=10.69) +14 more |
| 2 | `get_upstream_features` | L14:F4197@21, k=15 → L6:F11327 (de=7.72) +14 more |
| 3 | `get_upstream_features` | L6:F11327@21, k=15 → L4:F13412 (de=5.88) +14 more |
| 4 | `get_upstream_features` | L2:F2589@37, k=15 → Emb:"titian"@37 (de=19.12) +14 more |
| 5 | `inspect_feature` ×5 | L17:7545, L4:9554, L8:8003, L9:15926, L3:11774 |
| 6 | `get_upstream_features` | L4:F13412@21, k=12 → L3:F11774 (de=4.81) +11 more |
| 7 | `get_upstream_features` | L17:F7545@21, k=12 → L4:F13412 (de=5.28) +11 more |
| 8 | `get_upstream_features` | L4:F10494@64, k=10 → Emb:" Nutrition"@64 (de=6.91) +9 more |
| 9 | `get_upstream_features` | L0:F9888@18, k=10 → Emb:" education"@18 (de=22.75) +9 more |
| 10 | `get_upstream_features` | L0:F9026@37, k=10 → Emb:"titian"@37 (de=24.75) +9 more |
| 11 | `inspect_feature` ×4 | L1:6461, L4:11037, L3:10028, L8:7732 |
| 12 | `get_upstream_features` | L19:F1589@9, k=10 → Emb:" Nutritional"@9 (de=26.12) +9 more |
| 13 | `get_upstream_features` | L14:F4197@9, k=10 → Emb:" Nutritional"@9 (de=14.44) +9 more |
| 14 | `inspect_feature` ×2 | L17:14680, L18:6105 |
| 15 | `get_upstream_features` | L4:F13412@9, k=10 → Emb:" Nutritional"@9 (de=8.00) +9 more |
| 16 | `get_upstream_features` | L6:F11327@9, k=10 → Emb:" Nutritional"@9 (de=16.75) +9 more |
| 17 | `get_upstream_features` | L17:F14680@9, k=10 → Emb:" Nutritional"@9 (de=30.88) +9 more |
| 18 | `get_upstream_features` | L18:F6105@9, k=10 → Emb:" Nutritional"@9 (de=21.62) +9 more |
| 19 | `get_upstream_features` | L0:F14824@2, k=10 → Emb:" has"@2 (de=32.75) +9 more |
| 20 | `inspect_feature` ×4 | L0:9519, L0:8061, L0:8974, L0:9519 |
| 21 | `get_upstream_features` | L0:F9026@64, k=10 → Emb:" Nutrition"@64 (de=24.75) +9 more |
| 22 | `get_upstream_features` | L1:F6461@64, k=8 → Emb:" Sports"@63 (de=11.75) +7 more |
| 23 | `get_upstream_features` | L4:F10494@64, k=10 → Emb:" Nutrition"@64 (de=6.91) +9 more |
| 24 | `inspect_feature` | L1, F165 → " names of sports teams and words related to sports statistics, contrac" |
| 25 | `get_upstream_features` | L4:F13412@55, k=10 → Emb:" RD"@55 (de=11.31) +9 more |
| 26 | `get_upstream_features` | L4:F13412@37, k=10 → Emb:"titian"@37 (de=14.00) +9 more |
| 27 | `get_upstream_features` | L6:F11327@37, k=10 → Emb:"titian"@37 (de=9.06) +9 more |
| 28 | `inspect_feature` | L1, F6631 → " words related to dietary patterns and scientific studies" |
| 29 | `get_upstream_features` | L19:F1589@50, k=10 → Emb:" nutrition"@50 (de=29.50) +9 more |
| 30 | `get_upstream_features` | L14:F4197@50, k=10 → Emb:" nutrition"@50 (de=14.44) +9 more |
| 31 | `get_upstream_features` | L2:F2589@55, k=10 → Emb:" RD"@55 (de=6.44) +9 more |
| 32 | `get_upstream_features` | L4:F13412@50, k=10 → Emb:" nutrition"@50 (de=12.69) +9 more |
| 33 | `get_upstream_features` | L2:F2589@22, k=10 → ❌ Feature (layer=2, feature_idx=2589) not found at pos=22. Thi |
| 34 | `get_upstream_features` | L6:F11327@22, k=10 → L4:F13412 (de=4.53) +9 more |
| 35 | `get_upstream_features` | L2:F2589@36, k=10 → Emb:" Die"@36 (de=5.66) +9 more |
| 36 | `get_upstream_features` | L6:F11327@64, k=10 → Emb:" Nutrition"@64 (de=16.12) +9 more |
| 37 | `get_upstream_features` | L6:F11327@50, k=10 → Emb:" nutrition"@50 (de=19.50) +9 more |

### Build

`build_circuit` → 11 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 62,092 | 10,163 | 571,404 | 0 | $0.0651 | — | — |
| **Total** | | **62,092** | **10,163** | **571,404** | **0** | **$0.0651** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 4s