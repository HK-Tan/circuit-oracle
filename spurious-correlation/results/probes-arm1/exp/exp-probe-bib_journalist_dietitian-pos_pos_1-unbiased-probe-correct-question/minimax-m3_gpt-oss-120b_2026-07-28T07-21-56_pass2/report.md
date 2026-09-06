# Circuit Oracle Report
**Date:** 2026-07-28 07:21:56 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is classified via a late-layer nutrition-studies concept feature that aggregates multiple profession-genuine diet/health signals from "eat," "healthier," and the full "Academy of Nutrition and Dietetics" span — with no reliance on gendered pronoun features.

**Confidence:** 7

**Reasoning:** The single strongest output-driving node is **L19:1589** ("a context of scientific, specially nutritional, studies", frac_nonzero=0.038, promoted: diet/food/nutrition), which fires at three positions in the "Academy of Nutrition and Dietetics" span (pos 20 "Nutrition", pos 22 "Die", pos 23 "tetics"). Its top upstream inputs are: the raw token embeddings of "Nutrition" (direct_effect 34.25) and "Die" (13.25) plus the profession-defining L17:7545 ("registered nurse" / healthcare design context, 6.4–6.6), L17:465 ("di" prefix detector that latches onto "Die/tetics", 4.25), L18:6105 ("eating and health", 6.4), and L4:13412 ("terms related to diets and dietary health" — fires on "eat", "healthier", "Nutrition", "Die", "tetics"). The L4:13412 feature itself is anchored in the input by Emb:"healthier" (20.0), Emb:"Nutrition" (13.1), and Emb:"Academy" (2.06) — concrete profession vocabulary.

A second, more peripheral pathway runs through **L6:6115** ("commercial activity and customers", promoted: clients/clients/Customers). This is the only feature that even approaches a "service-provider" signal, and it derives directly from the **Emb:"clients"** token at pos 5 (direct_effect 25.6) plus a small nudge from Emb:"her" (0.93) — i.e. it is driven by the literal noun "clients", not by gendered morphology. Its own upstream drivers (L4:14782 "clients/user accounts", L5:2009 "audience/jury") are all client-relationship concepts, not pronoun or gender features. The pronoun **"her"** (pos 4) appears as an embedding but only contributes 0.93 to the clients node and does not propagate further; **"She"** (pos 1) does not appear in the top-20 feature list at all. Likewise, the only "education" feature (L0:9888 at "educating" pos 3) is a small, generic schooling detector — not a "female-coded helping" feature.

Concerning the user's worry about spurious gender features: I find no evidence that the circuit routes through a pronoun/gender feature. The two negative direct_effects near the output are L0:6051 ("periods/spaces/1", generic formatting) and L1:15251 (the dedicated "Client" capitalized-feature, which is *suppressing* rather than promoting L6:6115). L5:3400 ("verbs about enjoying experiences") has a mild negative effect and is a generic activity-feature, not gendered. The positive signal is overwhelmingly carried by topic-anchored features (food/nutrition/diet/health) and the literal tokens "eat," "healthier," "Nutrition," "Die," "tetics," "Academy," and "clients" — all genuine profession-discriminative lexical items. In short, the probe is reading "dietitian/RD" semantics from the word "eat healthier" and the explicit "Academy of Nutrition and Dietetics" mention, not from any gendered or otherwise spurious surface feature.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 23 | Output: probe classification score (synthetic logit) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 23 | L19:1589 — scientific/nutritional studies context (fires on "nutrition" pos20, "Die/tetics" pos22-23) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 22 | L19:1589 — scientific/nutritional studies context (fires on "nutrition" pos20, "Die/tetics" pos22-23) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 20 | L19:1589 — scientific/nutritional studies context (fires on "nutrition" pos20, "Die/tetics" pos22-23) |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 23 | L18:6105 — eating & health | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 22 | L18:6105 — eating & health | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 20 | L18:6105 — eating & health | text related to eating and health | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 23 | L17:7545 — architecture/design/nurses/healthcare | mentions of architecture, design, nurses and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 22 | L17:7545 — architecture/design/nurses/healthcare | mentions of architecture, design, nurses and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L17:F7545](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) | 20 | L17:7545 — architecture/design/nurses/healthcare | mentions of architecture, design, nurses and healthcare. | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7545) |
| [L17:F465](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/465) | 22 | L17:465 — "di" prefix (e.g., "Die/tetics") | di | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/465) |
| [L15:F8177](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8177) | 9 | L15:8177 — words associated with eating | words associated with eating | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8177) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | L14:4197 — food/food-insecurity topic feature (pos9 "eat", pos23 "tetics") |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 23 | L14:4197 — food/food-insecurity topic feature (pos9 "eat", pos23 "tetics") |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 20 | L14:4197 — food/food-insecurity topic feature (pos9 "eat", pos23 "tetics") |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L6:F6115](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) | 5 | L6:6115 — commercial activity / clients |  words related to commercial activity and customers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 9 | L6:11327 — food / nutrition (pos9 "eat", pos20/22/23) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 20 | L6:11327 — food / nutrition (pos9 "eat", pos20/22/23) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 22 | L6:11327 — food / nutrition (pos9 "eat", pos20/22/23) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 23 | L6:11327 — food / nutrition (pos9 "eat", pos20/22/23) |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F8984](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8984) | 10 | L6:8984 — health words |  words and phrases related to health | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8984) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 9 | L4:13412 — diet / dietary-health terms (pos9 "eat", pos10 "healthier", pos20 "Nutrition", pos22 "Die", pos23 "tetics") |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 10 | L4:13412 — diet / dietary-health terms (pos9 "eat", pos10 "healthier", pos20 "Nutrition", pos22 "Die", pos23 "tetics") |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 20 | L4:13412 — diet / dietary-health terms (pos9 "eat", pos10 "healthier", pos20 "Nutrition", pos22 "Die", pos23 "tetics") |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | L4:13412 — diet / dietary-health terms (pos9 "eat", pos10 "healthier", pos20 "Nutrition", pos22 "Die", pos23 "tetics") |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 23 | L4:13412 — diet / dietary-health terms (pos9 "eat", pos10 "healthier", pos20 "Nutrition", pos22 "Die", pos23 "tetics") |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F1626](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1626) | 9 | L4:1626 — food consumption verbs ("eat", "eating") | phrases that occur in the context of food consumption. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1626) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 9 | L4:9554 — food / rations / feeding | words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 23 | L4:9554 — food / rations / feeding | words related to food, rations and feeding | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 23 | L4:11037 — counseling/social work/academic degree programs |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L4:F12213](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) | 10 | L4:12213 — health research / medical context (pos10 "healthier") | strings of letters followed by "ls" and "an", plus words associated with health research | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) |
| [L4:F14782](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14782) | 5 | L4:14782 — clients / user accounts / tables (pos5 "clients") |  terms related to clients, user accounts, and tables | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14782) |
| [L5:F2009](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2009) | 5 | L5:2009 — audience / jury / legal |  mentions of an audience or jury, especially in legal contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/2009) |
| [L0:F9888](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) | 3 | L0:9888 — formal-schooling / education words |  words related to formal schooling | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) |
| [L0:F11021](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11021) | 9 | L0:11021 — "eat" / eating verb | mentions of eating | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11021) |
| [L2:F12264](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12264) | 9 | L2:12264 — words associated with communication, food, and parental influence | words associated with communication, food, and parental influence | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12264) |
| [L3:F11774](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) | 23 | L3:11774 — "Die" subword detector (boundary of "Dietetics") | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11774) |
| [L1:F15251](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) | 5 | L1:15251 — "client" capitalized/special (suppressing here) |  the word "client" and its plural form more often than not when capitalized as the first word of a sentence or preceded by a special character | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 8 | L0:8444 — word "to" (pos8) | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 11 | L0:6051 — periods / spaces / "1" (inhibitory) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F5697](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5697) | 5 | L0:5697 — word "accompanied" (pos5) | the word "accompanied" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5697) |
| [L5:F3400](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3400) | 3 | L5:3400 — verbs/nouns about spending time/enjoying experiences (inhibitory) |  verbs, adjectives, or nouns related to the act of spending time or enjoying experiences with others | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3400) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:6115 de=0.128 |
| 3 | `inspect_feature` ×14 | L6:6115, L14:4197, L4:13412, L19:1589, L6:11327, L4:12213, L0:6051, L1:15251, L0:9888, L0:5697, L0:8444, L6:8984, L15:8177, L5:3400 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@23` | ❌ error | — | — | Trace the L19:1589 nutritional studies feature upstream through the circuit. Ide… |
| SA-2 | `L14:F4197@9` | ✅ reported | 8 | 12 | Trace L14:4197 (food/nutrition topic feature) upstream. This feature fires on po… |
| SA-3 | `L6:F6115@5` | ❌ error | — | — | Trace L6:6115 ("clients"/commercial activity feature) upstream. This feature fir… |

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4197 | " words and phrases related to food insecurity." |
| 2 | `get_upstream_features` | L14:F4197@9, k=10 | Emb:" eat"@9 (de=17.88) +9 more |
| 3 | `inspect_feature` | L6, F11327 | " words or phrases related to food or nutrition" |
| 4 | `get_upstream_features` | L6:F11327@9, k=10 | Emb:" eat"@9 (de=22.12) +9 more |
| 5 | `inspect_feature` | L4, F1626 | " phrases that occur in the context of food consumption." |
| 6 | `inspect_feature` | L4, F13412 | " terms related to diets and dietary health" |
| 7 | `get_upstream_features` | L4:F1626@9, k=10 | Emb:" eat"@9 (de=15.81) +9 more |
| 8 | `inspect_feature` | L0, F11021 | " mentions of eating" |
| 9 | `inspect_feature` | L2, F12264 | "words associated with communication, food, and parental influence" |
| 10 | `inspect_feature` | L7, F311 | " terms related to diet and race" |
| 11 | `get_upstream_features` | L0:F11021@9, k=5 | Emb:" eat"@9 (de=23.75) +4 more |
| 12 | `inspect_feature` | L4, F9554 | " words related to food, rations and feeding" |

**Findings:** The target food‑insecurity feature (L14:4197) receives its strongest excitatory drive directly from the raw token embedding of "eat" and from a cascade of earlier food‑related detectors. The chain begins at layer‑0 feature 11021, which directly amplifies the "eat" token (embedding → 11021). That early lexical signal feeds into a mid‑layer nutrition detector (L6:11327), which itself is boosted by t…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F1589@23, k=15 → L4:F13412 (de=10.38) +14 more |
| 2 | `get_upstream_features` | L6:F6115@5, k=15 → Emb:" clients"@5 (de=25.62) +14 more |
| 3 | `get_upstream_features` | L4:F13412@23, k=15 → L3:F11774 (de=4.72) +14 more |
| 4 | `get_upstream_features` | L4:F13412@22, k=15 → Emb:" Nutrition"@20 (de=8.56) +14 more |
| 5 | `get_upstream_features` | L14:F4197@9, k=15 → Emb:" eat"@9 (de=17.88) +14 more |
| 6 | `get_upstream_features` | L14:F4197@23, k=15 → L6:F11327 (de=5.94) +14 more |
| 7 | `get_upstream_features` | L6:F11327@9, k=12 → Emb:" eat"@9 (de=22.12) +11 more |
| 8 | `get_upstream_features` | L6:F11327@23, k=12 → L4:F13412 (de=6.50) +11 more |
| 9 | `get_upstream_features` | L17:F7545@23, k=10 → L4:F13412 (de=5.25) +9 more |
| 10 | `get_upstream_features` | L3:F11774@23, k=10 → Emb:" Die"@22 (de=5.62) +9 more |
| 11 | `get_upstream_features` | L4:F13412@20, k=10 → Emb:" Nutrition"@20 (de=13.12) +9 more |
| 12 | `get_upstream_features` | L4:F1626@9, k=10 → Emb:" eat"@9 (de=15.81) +9 more |
| 13 | `get_upstream_features` | L4:F9554@23, k=10 → Emb:" Nutrition"@20 (de=4.19) +9 more |
| 14 | `inspect_feature` ×2 | L17:7545, L4:11037 |
| 15 | `get_upstream_features` | L4:F11037@23, k=8 → L3:F11774 (de=2.62) +7 more |
| 16 | `get_upstream_features` | L19:F1589@22, k=12 → Emb:" Nutrition"@20 (de=14.06) +11 more |
| 17 | `get_upstream_features` | L19:F1589@20, k=12 → Emb:" Nutrition"@20 (de=34.25) +11 more |
| 18 | `inspect_feature` ×4 | L18:6105, L18:6105, L17:465, L15:8177 |
| 19 | `get_upstream_features` | L6:F8984@10, k=10 → Emb:" healthier"@10 (de=20.00) +9 more |
| 20 | `get_upstream_features` | L4:F12213@10, k=10 → Emb:" healthier"@10 (de=20.00) +9 more |
| 21 | `inspect_feature` ×2 | L4:14782, L5:2009 |

### Build

`build_circuit` → 36 nodes, 45 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 88,452 | 8,460 | 281,629 | 0 | $0.0536 | — | — |
| SA-2 | openai/gpt-oss-120b | 173,677 | 12,523 | 18,912 | 0 | $0.0338 | ✅ 8F/12E | Trace L14:4197 (food/nutrition topic feature) upstream. This… |
| **Total** | | **262,129** | **20,983** | **300,541** | **0** | **$0.0874** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 44s