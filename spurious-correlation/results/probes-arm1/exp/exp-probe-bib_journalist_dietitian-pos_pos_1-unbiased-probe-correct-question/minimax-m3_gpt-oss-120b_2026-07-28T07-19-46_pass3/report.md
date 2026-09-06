# Circuit Oracle Report
**Date:** 2026-07-28 07:19:46 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for "Registered Dietitian" is driven primarily by **genuine domain content** (food, nutrition, diet, eating) rather than spurious gender markers — the signal flows from tokens like "clients," "eat," "healthier," "Nutrition," and "Diet" through a hierarchy of nutrition-context features culminating in L19:F1589, with only one tangential non-domain feature (L5:F3400) hinting at interpersonal verbs.

**Confidence:** 8

**Reasoning:** The circuit (built via build_circuit) shows the dominant pathway is content-driven, not gender-driven. Token embeddings for domain terms — `eat` (pos 9, direct_effect ~22 to L6:F11327), `healthier` (pos 10, ~20 to L4:F12213), `clients` (pos 5, ~25.6 to L6:F6115), `Nutrition` (pos 20, ~8.2 to L19:F1589), and `Diet` (pos 22, ~8.7 to L19:F1589) — drive mid-layer food/diet features (L4:F1626 "food consumption", L4:F13412 "diets and dietary health" frac_nonzero=0.012, L4:F12213 "health research" frac_nonzero=0.009, L6:F11327 "food/nutrition" frac_nonzero=0.012, L6:F6115 "commercial activity" frac_nonzero=0.023). These aggregate upward to L14:F4197 "food insecurity/eating phrases" (frac_nonzero=0.015), L17:F7545 "nurses/healthcare" (frac_nonzero=0.004), and finally L19:F1589 "context of scientific nutritional studies" (frac_nonzero=0.038) — all low-frac_nonzero domain features, not generic patterns. L19:F1589 carries the largest direct_effects (0.087-0.109) into the output.

The user's specific concern about **gender markers** is largely unsubstantiated by this circuit. I found no features encoding "she/her" or female pronouns as positive drivers. The L1:F15251 "client" feature (pos 5) and L3:F592 "love/affect" (pos 2, "loves") are the closest candidates, but they fire on lexical content (client, loves), not on gendered pronouns. The single non-domain positive contributor to the output is L5:F3400 (spending time/interpersonal verbs at pos 3, "educating") with a modest negative direct_effect (-0.0732) — it actually *suppresses* the probe score, not enhances it. L0:F6051 (pos 11, periods) similarly has a negative direct_effect (-0.0957). The minor "loves" feature does route through L3:F592 → L5:F3400, but the dominant chain is entirely nutrition-domain. **Conclusion:** the probe classifies "Registered Dietitian" based on legitimate profession content (nutrition, diet, food, healthcare, education), not on spurious gender correlates.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: clients (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: eat (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: healthier (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: educating (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: loves (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: . (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: Nutrition (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: Diet (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F9888](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) | 3 | L0: early lexical cues (educating, eat, client) |  words related to formal schooling | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) |
| [L0:F11021](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11021) | 9 | L0: early lexical cues (educating, eat, client) | mentions of eating | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11021) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 11 | L0: early lexical cues (educating, eat, client) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L1:F15251](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) | 5 | L1: client/love lexical features |  the word "client" and its plural form more often than not when capitalized as the first word of a sentence or preceded by a special character | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 2 | L3: love/affect context | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L4:F1626](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1626) | 9 | L4: food-consumption + diet/health chain |  phrases that occur in the context of food consumption. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1626) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 9 | L4: food-consumption + diet/health chain |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 10 | L4: food-consumption + diet/health chain |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 23 | L4: food-consumption + diet/health chain |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F14782](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14782) | 5 | L4: food-consumption + diet/health chain | terms related to clients, user accounts, and tables | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14782) |
| [L4:F12213](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) | 10 | L4: food-consumption + diet/health chain | strings of letters followed by "ls" and "an", plus words associated with health research | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) |
| [L5:F3400](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3400) | 3 | L5: spending time / interpersonal verbs |  verbs, adjectives, or nouns related to the act of spending time or enjoying experiences with others | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3400) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 9 | L6: food/nutrition + clients (commercial) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 23 | L6: food/nutrition + clients (commercial) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F6115](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) | 5 | L6: food/nutrition + clients (commercial) |  words related to commercial activity and customers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | L14: food-insecurity/eating phrases |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 23 | L14: food-insecurity/eating phrases |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 23 | L17: nurses/healthcare/architecture mix | mentions of architecture, design, nurses and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 20 | L19: nutritional scientific studies context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 22 | L19: nutritional scientific studies context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 23 | L19: nutritional scientific studies context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:6115 de=0.128 |
| 3 | `inspect_feature` ×5 | L6:6115, L4:13412, L14:4197, L6:11327, L19:1589 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@23` | ✅ reported | 6 | 6 | Trace the path upstream from L19:F1589 at position 23 (activates on nutritional … |
| SA-2 | `L14:F4197@9` | ✅ reported | 5 | 6 | Trace the path upstream from L14:F4197 at position 9 (food/nutrition context). I… |
| SA-3 | `L6:F11327@9` | ✅ reported | 10 | 19 | Trace the path upstream from L6:F11327 at position 9 (food/nutrition words). Ide… |
| SA-4 | `L6:F6115@5` | ✅ reported | 3 | 4 | Trace the path upstream from L6:F6115 at position 5 (clients/commercial activity… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L19, F1589 | " a context of scientific, specially nutritional, studies" |
| 2 | `get_upstream_features` | L19:F1589@23, k=10 | L4:F13412 (de=10.38) +9 more |
| 3 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 4 | `get_upstream_features` | L4:F13412@23, k=10 | L3:F11774 (de=4.72) +9 more |
| 5 | `inspect_feature` | L17, F7545 | "mentions of architecture, design, nurses and healthcare." |
| 6 | `inspect_feature` | L3, F11774 | " what appears to be a smattering of strings related to scientific nota" |
| 7 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 8 | `get_upstream_features` | L17:F7545@23, k=10 | L4:F13412 (de=5.25) +9 more |
| 9 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 10 | `inspect_feature` | L7, F10463 | " phrases related to scientific publications, names, and medical contex" |
| 11 | `get_upstream_features` | L3:F11774@23, k=10 | Emb:" Die"@22 (de=5.62) +9 more |
| 12 | `get_upstream_features` | L6:F11327@23, k=10 | L4:F13412 (de=6.50) +9 more |

**Findings:** Tracing upstream from L19:F1589 (nutrition‑context probe) quickly reaches lower‑third layers. The strongest upstream drivers are a mid‑layer diet‑detector (L4:F13412) and a healthcare‑profession detector (L17:F7545), both feeding strong positive influence into the target. Crucially, two raw token embeddings – the German article "Die" (pos 22) and the explicit token "Nutrition" (pos 20) – each cont…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 2 | `get_upstream_features` | L14:F4197@9, k=10 | Emb:" eat"@9 (de=17.88) +9 more |
| 3 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 4 | `get_upstream_features` | L6:F11327@9, k=10 | Emb:" eat"@9 (de=22.12) +9 more |
| 5 | `inspect_feature` | L4, F1626 | " phrases that occur in the context of food consumption." |
| 6 | `get_upstream_features` | L4:F1626@9, k=10 | Emb:" eat"@9 (de=15.81) +9 more |
| 7 | `inspect_feature` | L2, F12264 | "words associated with communication, food, and parental influence" |
| 8 | `inspect_feature` | L0, F11021 | " mentions of eating" |

**Findings:** Tracing upstream from L14:F4197 (food‑insecurity detector) reveals a clear cascade rooted in the raw token embedding for the word “eat" at position 9. The strongest positive upstream influence comes from the embedding itself (direct_effect ~17‑22), followed by a mid‑layer food‑concept feature (L6:11327) and a lower‑layer consumption phrase feature (L4:1626). Both of these feed further down to an e…

</details>

<details>
<summary><b>SA-3</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 2 | `get_upstream_features` | L6:F11327@9, k=10 | Emb:" eat"@9 (de=22.12) +9 more |
| 3 | `inspect_feature` | L4, F1626 | " phrases that occur in the context of food consumption." |
| 4 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 5 | `inspect_feature` | L0, F11021 | " mentions of eating" |
| 6 | `get_upstream_features` | L4:F1626@9, k=10 | Emb:" eat"@9 (de=15.81) +9 more |
| 7 | `inspect_feature` | L2, F12264 | "words associated with communication, food, and parental influence" |
| 8 | `get_upstream_features` | L4:F13412@9, k=10 | Emb:" eat"@9 (de=7.66) +9 more |
| 9 | `get_upstream_features` | L2:F12264@9, k=10 | Emb:" eat"@9 (de=7.03) +9 more |
| 10 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |

**Findings:** The trace starts at L6:F11327 (food/nutrition detector). Its strongest positive upstream drivers are:
1) L4:F1626 – a mid‑layer food‑consumption context gate, itself driven by the raw token embedding " eat" and by L2:F12264.
2) L4:F13412 – diet/health related feature, also fed by the same " eat" embedding.
3) L0:F11021 – an early‑layer cue that the token "eat" appears.
All three paths converge on …

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F6115 | " words related to commercial activity and customers" |
| 2 | `get_upstream_features` | L6:F6115@5, k=10 | Emb:" clients"@5 (de=25.62) +9 more |
| 3 | `inspect_feature` | L4, F14782 | " terms related to clients, user accounts, and tables" |
| 4 | `inspect_feature` | L5, F2009 | " mentions of an audience or jury, especially in legal contexts" |
| 5 | `get_upstream_features` | L4:F14782@5, k=10 | Emb:" clients"@5 (de=16.00) +9 more |
| 6 | `inspect_feature` | L2, F12676 | "the word "client" and its plural form" |

**Findings:** The target feature L6:F6115 (position 5) that signals commercial activity is primarily driven by the input token "clients" (direct_effect 25.6). A downstream feature in layer 4 (F14782) also contributes positively and is itself strongly activated by the same token "clients" and by a low‑frequency lexical detector in layer 2 (F12676) that fires on the word "client". All traced nodes lie in layers ≤…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L0:6051, L1:15251, L0:9888, L4:12213, L5:3400, L4:1626 |
| 2 | `get_upstream_features` | L0:F6051@11, k=5 → Emb:"."@11 (de=46.50) +4 more |
| 3 | `get_upstream_features` | L1:F15251@5, k=5 → Emb:" clients"@5 (de=27.62) +4 more |
| 4 | `get_upstream_features` | L14:F4197@9, k=8 → Emb:" eat"@9 (de=17.88) +7 more |
| 5 | `get_upstream_features` | L6:F11327@9, k=8 → Emb:" eat"@9 (de=22.12) +7 more |
| 6 | `get_upstream_features` | L6:F6115@5, k=8 → Emb:" clients"@5 (de=25.62) +7 more |
| 7 | `get_upstream_features` | L19:F1589@23, k=8 → L4:F13412 (de=10.38) +7 more |
| 8 | `get_upstream_features` | L4:F13412@23, k=8 → L3:F11774 (de=4.72) +7 more |
| 9 | `inspect_feature` | L17, F7545 → "mentions of architecture, design, nurses and healthcare." |
| 10 | `get_upstream_features` | L4:F12213@10, k=5 → Emb:" healthier"@10 (de=20.00) +4 more |
| 11 | `get_upstream_features` | L0:F9888@3, k=5 → Emb:" educating"@3 (de=14.88) +4 more |
| 12 | `get_upstream_features` | L5:F3400@3, k=5 → Emb:" loves"@2 (de=9.62) +4 more |
| 13 | `inspect_feature` | L3, F592 → "words related to love, affection, and hate, including foreign language" |
| 14 | `get_upstream_features` | L0:F9888@11, k=8 → ❌ Feature (layer=0, feature_idx=9888) not found at pos=11. Thi |
| 15 | `get_upstream_features` | L0:F6051@11, k=5 → Emb:"."@11 (de=46.50) +4 more |
| 16 | `get_upstream_features` | L4:F12213@9, k=5 → ❌ Feature (layer=4, feature_idx=12213) not found at pos=9. Thi |

### Build

`build_circuit` → 18 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 39,143 | 5,319 | 257,333 | 0 | $0.0336 | — | — |
| SA-2 | openai/gpt-oss-120b | 103,636 | 6,263 | 2,528 | 0 | $0.0193 | ✅ 5F/6E | Trace the path upstream from L14:F4197 at position 9 (food/n… |
| SA-4 | openai/gpt-oss-120b | 48,879 | 3,401 | 5,056 | 0 | $0.0094 | ✅ 3F/4E | Trace the path upstream from L6:F6115 at position 5 (clients… |
| SA-1 | openai/gpt-oss-120b | 148,523 | 6,085 | 12,736 | 0 | $0.0261 | ✅ 6F/6E | Trace the path upstream from L19:F1589 at position 23 (activ… |
| SA-3 | openai/gpt-oss-120b | 133,078 | 10,690 | 10,112 | 0 | $0.0265 | ✅ 10F/19E | Trace the path upstream from L6:F11327 at position 9 (food/n… |
| **Total** | | **473,259** | **31,758** | **287,765** | **0** | **$0.1150** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 32s