# Circuit Oracle Report
**Date:** 2026-07-28 07:23:37 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies the subject as a registered dietitian/ nutritionist. The classification is driven by profession-specific content tokens ("Nutrition", "Die[tetics]", "eat", "healthier", "food") — not by gender markers. The "She/her/loves educating" tokens are present in the early layers but barely contribute to the late-layer features that feed the probe; the user-suspected spurious path is not materializing.

**Confidence:** 8

**Reasoning:**

The terminal probe direction is driven overwhelmingly by a small set of late-layer profession-content features. The strongest single driver is **L19:1589** (label: *"a context of scientific, specially nutritional, studies"*, promoted tokens: diet/food/nutrition, frac_nonzero 0.038), appearing at positions 20, 22, 23, and 35 with summed direct_effects ≈ 0.34. Its upstream is **L18:6105** (*"text related to eating and health"*, promoted: healthy/health), **L17:7545** (*"mentions of architecture, design, nurses and healthcare"*), **L16:12752**, and **L15:12472** (technical-document context). One hop deeper these pull in **L14:4197** (*"food insecurity / food words"*, frac_nonzero 0.015) and **L15:8177** (*"words associated with eating"*, promoted: eat/eating), then **L6:11327** (*"food or nutrition"*) and **L6:8984** (*"health"*), then **L4:13412** (*"terms related to diets and dietary health"* — top activating token: "ticians" / "diet"), **L4:12213** (*"health research"*), **L4:11037** (*"counseling/therapy/social work/degree programs"*, promoted: engineer), **L4:1626** (*"phrases in the context of food consumption"*, promoted: eat/eating), and **L4:9554** (*"food, rations and feeding"*).

The chain bottoms out in the expected embedding nodes: **Emb:Nutrition (pos 20)**, **Emb:Die (pos 22)**, **Emb:eat (pos 9)**, **Emb:healthier (pos 10)**, and **Emb:Academy (pos 18)** — all direct profession content. The **"Die" → "Dietetics"** path is particularly diagnostic: L3:11774, L3:10028, L3:7212 and L4:11037 (counseling/social-work/degree) all fire on this token, and the *client* of those features is L14/L15/L17/L19, not anything gender-coded.

The **client/commercial** path the user suspected IS present — **L6:6115** (*"commercial activity and customers"*, promoted: clients/customers, frac_nonzero 0.023) at pos 5 with direct_effect 0.128, plus **L5:2213** (working relationships between businesses and customers), **L4:14782** (clients/user accounts/tables), **L4:5739** (client), and **L1:15251** (client). These fire on **Emb:clients (pos 5)**. Critically, however, their positive signal into the output is mostly upstream-suppressed: L1:15251, L5:2213, L4:5739, and L4:6985 all have *negative* direct_effects on L6:6115 (−0.091, −0.073, −3.19, −1.5, −0.96), and L6:6115 itself does not appear in the late-layer L17/L18/L19 upstreams (its only positive outlet is into a non-dominant path). Of the L6:6115 features' top upstreams, only **Emb:clients (25.6)** and a small **+her (0.93)** are excitatory — *her* and the gender-marker side-roads are tiny (<<1) compared to the **+25.6 from "clients"** and the negative suppressors.

Gender/pronominal features are essentially absent from the late-layer drivers. Searching the top features by direct_effect, no feature label mentions she/her/woman/female; the only L0 features present are the word "to" (L0:8444, frac_nonzero 0.017), the word "accompanied" (L0:5697), the word "education" (L0:9888, fired on **Emb:educating** — not gender), the period (L0:6051), the word "eat" (L0:11021 at pos 9 — again profession-content), and the activity/enjoyment feature L5:3400 (fired on "loves" but contributing only −0.073 to the probe). The She/her/Academy/blog features that *are* in the circuit (L0:5697 at pos 5, the "ed" sequence at pos 22-23) flow into profession-content features, not into any gender-coded late-layer feature.

So the mechanism is: token embeddings of *Nutrition*, *Die[tetics]*, *Academy*, *eat*, *healthier*, *food* activate L4 diet/health-research and L6 food/nutrition/health features, which feed L14/L15 food-eating and L17/L18 health-care/scientific-nutrition features, which fire L19:1589 (the strongest single contributor at ~0.34 combined), which directly drives the dietitian probe. The *clients* / commercial path exists in L1–L6 but is partially self-inhibiting and does not propagate to the late layers; it contributes at most ~0.13 to the probe through L6:6115, vs. ~0.34 from L19:1589 plus ~0.27 from L14:4197 and ~0.18 from L6:11327 (all profession content). Gender markers are not load-bearing — the concern is not borne out for this particular input; the probe is correctly using profession content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 23 | L19 / L18 / L17 / L16: scientific-nutrition & health-care context (most direct late-layer drivers) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 22 | L19 / L18 / L17 / L16: scientific-nutrition & health-care context (most direct late-layer drivers) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 20 | L19 / L18 / L17 / L16: scientific-nutrition & health-care context (most direct late-layer drivers) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 35 | L19 / L18 / L17 / L16: scientific-nutrition & health-care context (most direct late-layer drivers) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 23 | L19 / L18 / L17 / L16: scientific-nutrition & health-care context (most direct late-layer drivers) | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 20 | L19 / L18 / L17 / L16: scientific-nutrition & health-care context (most direct late-layer drivers) | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 22 | L19 / L18 / L17 / L16: scientific-nutrition & health-care context (most direct late-layer drivers) | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 23 | L19 / L18 / L17 / L16: scientific-nutrition & health-care context (most direct late-layer drivers) | mentions of architecture, design, nurses and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 22 | L19 / L18 / L17 / L16: scientific-nutrition & health-care context (most direct late-layer drivers) | mentions of architecture, design, nurses and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L16:F12752](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) | 23 | L19 / L18 / L17 / L16: scientific-nutrition & health-care context (most direct late-layer drivers) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) |
| [L15:F12472](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) | 23 | L19 / L18 / L17 / L16: scientific-nutrition & health-care context (most direct late-layer drivers) | words associated with legal, academic, or technical documents, and numerical references | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | L14 / L15: food, eating, nutrition mid-layer features |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 23 | L14 / L15: food, eating, nutrition mid-layer features |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 20 | L14 / L15: food, eating, nutrition mid-layer features |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L15:F8177](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8177) | 9 | L14 / L15: food, eating, nutrition mid-layer features | words associated with eating | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8177) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 9 | L6: generic food/nutrition/health word features (low layer, broad semantic) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 23 | L6: generic food/nutrition/health word features (low layer, broad semantic) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 20 | L6: generic food/nutrition/health word features (low layer, broad semantic) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F8984](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8984) | 10 | L6: generic food/nutrition/health word features (low layer, broad semantic) |  words and phrases related to health | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8984) |
| [L6:F6115](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) | 5 | L6 / L4: client / customer / commercial-relationship features (the user-suspected spurious path) |  words related to commercial activity and customers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) |
| [L5:F2213](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2213) | 5 | L6 / L4: client / customer / commercial-relationship features (the user-suspected spurious path) |  words related to working relationships between businesses and customers or clients | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2213) |
| [L4:F14782](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14782) | 5 | L6 / L4: client / customer / commercial-relationship features (the user-suspected spurious path) |  terms related to clients, user accounts, and tables | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14782) |
| [L4:F5739](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5739) | 5 | L6 / L4: client / customer / commercial-relationship features (the user-suspected spurious path) |  the word "client" and other words related to software applications and data management | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5739) |
| [L1:F15251](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) | 5 | L6 / L4: client / customer / commercial-relationship features (the user-suspected spurious path) |  the word "client" and its plural form more often than not when capitalized as the first word of a sentence or preceded by a special character | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 9 | L4: diet/dietitian and health research word features at pos 9/10/22/23 |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 10 | L4: diet/dietitian and health research word features at pos 9/10/22/23 |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | L4: diet/dietitian and health research word features at pos 9/10/22/23 |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 23 | L4: diet/dietitian and health research word features at pos 9/10/22/23 |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F12213](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) | 10 | L4: diet/dietitian and health research word features at pos 9/10/22/23 | strings of letters followed by "ls" and "an", plus words associated with health research | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) |
| [L4:F1626](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1626) | 9 | L4: diet/dietitian and health research word features at pos 9/10/22/23 |  phrases that occur in the context of food consumption. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1626) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 23 | L4: diet/dietitian and health research word features at pos 9/10/22/23 |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 22 | L4: diet/dietitian and health research word features at pos 9/10/22/23 |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 9 | L4: diet/dietitian and health research word features at pos 9/10/22/23 |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 23 | L4: diet/dietitian and health research word features at pos 9/10/22/23 |  words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L0:F11021](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11021) | 9 | L0–L3: token-level features (eat, education, accompanied, to, period, loves…) |  mentions of eating | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11021) |
| [L0:F9888](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) | 3 | L0–L3: token-level features (eat, education, accompanied, to, period, loves…) |  words related to formal schooling | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) |
| [L0:F5697](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5697) | 5 | L0–L3: token-level features (eat, education, accompanied, to, period, loves…) | the word "accompanied" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5697) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 8 | L0–L3: token-level features (eat, education, accompanied, to, period, loves…) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 11 | L0–L3: token-level features (eat, education, accompanied, to, period, loves…) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L5:F3400](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3400) | 3 | L0–L3: token-level features (eat, education, accompanied, to, period, loves…) |  verbs, adjectives, or nouns related to the act of spending time or enjoying experiences with others | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3400) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 23 | L0–L3: token-level features (eat, education, accompanied, to, period, loves…) |  what appears to be a smattering of strings related to scientific notation, live radio, and roman numerals | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L3:F10028](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) | 23 | L0–L3: token-level features (eat, education, accompanied, to, period, loves…) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10028) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:6115 de=0.128 |
| 3 | `inspect_feature` ×14 | L6:6115, L4:13412, L14:4197, L6:11327, L19:1589, L0:6051, L4:12213, L1:15251, L0:9888, L0:5697, L0:8444, L6:8984, L15:8177, L5:3400 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F6115@5` | ❌ error | — | — | Trace the "clients / commercial activity" feature at L6:6115 pos 5 back through … |
| SA-2 | `L4:F13412@23` | ❌ error | — | — | Trace the "diet/dietary health" feature at L4:13412 pos 23 upstream. pos 23 like… |
| SA-3 | `L14:F4197@9` | ❌ error | — | — | Trace L14:4197 (food/nutrition) pos 9 upstream. pos 9 is "eat" or "eating" in th… |
| SA-4 | `L19:F1589@23` | ❌ error | — | — | Trace the late-layer "scientific nutritional studies" feature L19:1589 pos 23 up… |
| SA-5 | `L6:F11327@9` | ❌ error | — | — | Trace L6:11327 (food/nutrition) pos 9 upstream to embedding nodes. |
| SA-6 | `L4:F12213@10` | ❌ error | — | — | Trace L4:12213 (health-related) pos 10 upstream. Find what drives it and reach t… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F1589@23, k=10 → L4:F13412 (de=10.38) +9 more |
| 2 | `get_upstream_features` | L14:F4197@9, k=10 → Emb:" eat"@9 (de=17.88) +9 more |
| 3 | `get_upstream_features` | L6:F6115@5, k=10 → Emb:" clients"@5 (de=25.62) +9 more |
| 4 | `get_upstream_features` | L6:F11327@9, k=10 → Emb:" eat"@9 (de=22.12) +9 more |
| 5 | `get_upstream_features` | L4:F13412@23, k=10 → L3:F11774 (de=4.72) +9 more |
| 6 | `get_upstream_features` | L4:F12213@10, k=10 → Emb:" healthier"@10 (de=20.00) +9 more |
| 7 | `get_upstream_features` | L17:F7545@23, k=8 → L4:F13412 (de=5.25) +7 more |
| 8 | `get_upstream_features` | L15:F8177@9, k=8 → Emb:" eat"@9 (de=34.25) +7 more |
| 9 | `get_upstream_features` | L6:F8984@10, k=8 → Emb:" healthier"@10 (de=20.00) +7 more |
| 10 | `get_upstream_features` | L4:F13412@10, k=8 → Emb:" eat"@9 (de=6.53) +7 more |
| 11 | `get_upstream_features` | L4:F13412@9, k=8 → Emb:" eat"@9 (de=7.66) +7 more |
| 12 | `get_upstream_features` | L4:F11037@23, k=8 → L3:F11774 (de=2.62) +7 more |
| 13 | `get_upstream_features` | L3:F11774@23, k=6 → Emb:" Die"@22 (de=5.62) +5 more |
| 14 | `get_upstream_features` | L3:F10028@23, k=6 → Emb:" Die"@22 (de=7.19) +5 more |
| 15 | `get_upstream_features` | L16:F12752@23, k=6 → L4:F13412 (de=3.86) +5 more |
| 16 | `get_upstream_features` | L18:F6105@23, k=6 → L17:F7545 (de=9.00) +5 more |
| 17 | `get_upstream_features` | L15:F12472@23, k=6 → Emb:"<bos>"@0 (de=-18.38) +5 more |
| 18 | `get_upstream_features` | L4:F1626@9, k=6 → Emb:" eat"@9 (de=15.81) +5 more |
| 19 | `get_upstream_features` | L0:F11021@9, k=6 → Emb:" eat"@9 (de=23.75) +5 more |
| 20 | `get_upstream_features` | L14:F4197@23, k=8 → L6:F11327 (de=5.94) +7 more |
| 21 | `get_upstream_features` | L19:F1589@22, k=6 → Emb:" Nutrition"@20 (de=14.06) +5 more |
| 22 | `inspect_feature` ×10 | L17:7545, L18:6105, L15:12472, L4:11037, L4:1626, L0:11021, L4:14782, L4:5739, L4:6985, L5:2213 |
| 23 | `get_upstream_features` | L3:F11774@22, k=6 → ❌ Feature (layer=3, feature_idx=11774) not found at pos=22. Th |
| 24 | `get_upstream_features` | L1:F15251@5, k=6 → Emb:" clients"@5 (de=27.62) +5 more |
| 25 | `get_upstream_features` | L4:F14782@5, k=6 → Emb:" clients"@5 (de=16.00) +5 more |
| 26 | `get_upstream_features` | L0:F11021@5, k=6 → ❌ Feature (layer=0, feature_idx=11021) not found at pos=5. Thi |
| 27 | `get_upstream_features` | L4:F5739@5, k=6 → Emb:" clients"@5 (de=17.50) +5 more |
| 28 | `get_upstream_features` | L0:F11021@5, k=6 → ❌ Feature (layer=0, feature_idx=11021) not found at pos=5. Thi |
| 29 | `inspect_feature` ×2 | L3:11774, L4:9554 |
| 30 | `get_upstream_features` | L0:F9888@3, k=6 → Emb:" educating"@3 (de=14.88) +5 more |
| 31 | `get_upstream_features` | L0:F5697@5, k=6 → Emb:" clients"@5 (de=12.44) +5 more |
| 32 | `get_upstream_features` | L0:F8444@8, k=6 → Emb:" to"@8 (de=40.50) +5 more |
| 33 | `get_upstream_features` | L0:F6051@11, k=6 → Emb:"."@11 (de=46.50) +5 more |
| 34 | `get_upstream_features` | L5:F3400@3, k=6 → Emb:" loves"@2 (de=9.62) +5 more |
| 35 | `get_upstream_features` | L19:F1589@20, k=6 → Emb:" Nutrition"@20 (de=34.25) +5 more |
| 36 | `inspect_feature` | L3, F153 → " words and phrases related to scientific articles and reports" |
| 37 | `get_upstream_features` | L17:F7545@22, k=6 → L4:F11037 (de=3.14) +5 more |
| 38 | `get_upstream_features` | L14:F4197@22, k=6 → ❌ Feature (layer=14, feature_idx=4197) not found at pos=22. Th |
| 39 | `get_upstream_features` | L19:F1589@35, k=6 → Emb:" eat"@9 (de=10.50) +5 more |
| 40 | `get_upstream_features` | L18:F6105@23, k=6 → L17:F7545 (de=9.00) +5 more |
| 41 | `get_upstream_features` | L0:F9888@3, k=6 → Emb:" educating"@3 (de=14.88) +5 more |
| 42 | `get_upstream_features` | L5:F3400@3, k=6 → Emb:" loves"@2 (de=9.62) +5 more |

### Build

`build_circuit` → 18 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 62,102 | 9,164 | 636,529 | 0 | $0.0678 | — | — |
| **Total** | | **62,102** | **9,164** | **636,529** | **0** | **$0.0678** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 17s