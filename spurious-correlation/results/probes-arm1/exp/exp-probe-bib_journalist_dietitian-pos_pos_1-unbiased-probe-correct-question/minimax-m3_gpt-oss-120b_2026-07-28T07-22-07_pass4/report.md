# Circuit Oracle Report
**Date:** 2026-07-28 07:22:07 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The RD probe classification is driven by genuine food/nutrition content features (L4:13412 "diets and dietary health", L6:11327 "food/nutrition", L14:4197 "food/eating context", L19:1589 "scientific nutritional studies") anchored to the tokens "eat", "healthier", "Nutrition", "Dietetics", and "food" — there is no gender-based or other spurious feature in the top of the circuit, and the "She/her/educating" tokens contribute only marginally (S_over_R ≈ 1.5, well within range) and via generic lexical features like L0:9888 ("education") and L0:8444 ("to").

**Confidence:** 8

**Reasoning:** The top-scoring features by direct_effect on the probe are all content-specific: L6:6115 "commercial activity and customers" (+0.128, driven by the token "clients" at pos 5, with direct_effect 25.6 from the embedding), L4:13412 "diets and dietary health" (+0.125, driven by "Dietetics"/"Nutrition" at pos 20-23 and "eat"/"healthier" at pos 9-10, frac_nonzero=0.012 — highly specific), L14:4197 "food/eating context" (+0.122, driven by "eat"), L6:11327 "food/nutrition" (+0.119, driven by "eat" with embedding direct_effect 22.1), and L19:1589 "scientific/nutritional studies" (+0.109, driven by the "Nutrition" token with embedding direct_effect 34.25 and "Dietetics" tokens). The "clients" branch is about the dietitian's professional service relationship (advice-giving to clients), not a gendered cue. The two negative-direct_effect features are L0:6051 "period/punctuation" (-0.096, a generic syntactic feature firing on the period at pos 11) and L1:15251 "client/clients (capitalized/start of sentence)" (-0.091, a low-frac_nonzero 0.003 feature that actually *suppresses* the client feature, partially because the token here is lowercase "clients" mid-sentence). The user's concern about gender-based spurious features is not supported: the pronouns "She" and "her" appear as upstream sources with very small signed contributions and low S_over_R (1.49, modest). Their main route is through the generic L0 lexical layer ("education" feature on "educating", "to" feature on "to") which are not profession-specific. Multi-hop source-influence from the food/nutrition positions (9, 10, 20, 22, 23, 29) carries S_pct_of_total = 17.1% with S_over_R = 4.7, decisively indicating the source tokens (Nutrition vocabulary + "eat healthier") drive the probe, while pronoun positions (1-4) carry only 6.9% with S_over_R = 1.5. The circuit converges through a clean content supernode hierarchy: token embeddings → L4 diet-terms → L6 food → L14 food-focus → L19 nutrition-studies → probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: clients (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: eat (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: healthier (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: educating (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: Nutrition (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: Die+tics (pos 22-23) 'Dietetics' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: Die+tics (pos 22-23) 'Dietetics' | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 29 | Emb: food (pos 29) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F9888](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) | 3 | Layer 0 lexical features |  words related to formal schooling | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9888) |
| [L0:F5697](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5697) | 5 | Layer 0 lexical features | the word "accompanied" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5697) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 8 | Layer 0 lexical features | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L1:F15251](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) | 5 | L1:15251 'client/clients (capitalized/start of sentence)' (inhibitory) |  the word "client" and its plural form more often than not when capitalized as the first word of a sentence or preceded by a special character | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15251) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 9 | L4:13412 'diets and dietary health' |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 10 | L4:13412 'diets and dietary health' |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 22 | L4:13412 'diets and dietary health' |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 23 | L4:13412 'diets and dietary health' |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F12213](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) | 10 | L4:12213 'healthier/health-related' | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12213) |
| [L5:F3400](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3400) | 3 | L5:3400 'verbs of spending time / experiences' (inhibitory) |  verbs, adjectives, or nouns related to the act of spending time or enjoying experiences with others | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3400) |
| [L6:F6115](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) | 5 | L6:6115 'commercial activity and customers' |  words related to commercial activity and customers | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6115) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 9 | L6:11327 'food/nutrition' |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 20 | L6:11327 'food/nutrition' |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 22 | L6:11327 'food/nutrition' |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 23 | L6:11327 'food/nutrition' |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 11 | L0:6051 'period/punctuation' (inhibitory) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 9 | L14:4197 'food/eating context' |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 20 | L14:4197 'food/eating context' |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 23 | L14:4197 'food/eating context' |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L15:F8177](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8177) | 9 | L15:8177 'healthier/health-related' | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8177) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 20 | L19:1589 'scientific/nutritional studies context' |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 22 | L19:1589 'scientific/nutritional studies context' |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 23 | L19:1589 'scientific/nutritional studies context' |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 35 | L19:1589 'scientific/nutritional studies context' |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe direction (RD classification score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:6115 de=0.128 |
| 3 | `inspect_feature` ×6 | L6:6115, L4:13412, L14:4197, L6:11327, L19:1589, L0:6051 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F1589@23` | ❌ error | — | — | Trace the path upstream from L19:F1589 at position 23. This feature encodes a co… |
| SA-2 | `L14:F4197@9` | ❌ error | — | — | Trace the path upstream from L14:F4197 at position 9. This feature encodes food/… |
| SA-3 | `L6:F6115@5` | ❌ error | — | — | Trace the path upstream from L6:F6115 at position 5. This feature encodes commer… |
| SA-4 | `L4:F13412@23` | ❌ error | — | — | Trace the path upstream from L4:F13412 at position 23. This feature encodes diet… |
| SA-5 | `L6:F11327@9` | ❌ error | — | — | Trace the path upstream from L6:F11327 at position 9. This feature encodes food … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F1589@23, k=12 → L4:F13412 (de=10.38) +11 more |
| 2 | `get_upstream_features` | L14:F4197@9, k=12 → Emb:" eat"@9 (de=17.88) +11 more |
| 3 | `get_upstream_features` | L6:F6115@5, k=12 → Emb:" clients"@5 (de=25.62) +11 more |
| 4 | `get_upstream_features` | L4:F13412@23, k=12 → L3:F11774 (de=4.72) +11 more |
| 5 | `get_upstream_features` | L6:F11327@9, k=12 → Emb:" eat"@9 (de=22.12) +11 more |
| 6 | `get_upstream_features` | L19:F1589@20, k=10 → Emb:" Nutrition"@20 (de=34.25) +9 more |
| 7 | `get_upstream_features` | L19:F1589@22, k=10 → Emb:" Nutrition"@20 (de=14.06) +9 more |
| 8 | `get_upstream_features` | L19:F1589@35, k=10 → Emb:" eat"@9 (de=10.50) +9 more |
| 9 | `get_upstream_features` | L4:F13412@10, k=10 → Emb:" eat"@9 (de=6.53) +9 more |
| 10 | `get_upstream_features` | L4:F13412@22, k=10 → Emb:" Nutrition"@20 (de=8.56) +9 more |
| 11 | `get_upstream_features` | L4:F13412@9, k=10 → Emb:" eat"@9 (de=7.66) +9 more |
| 12 | `get_upstream_features` | L4:F12213@10, k=10 → Emb:" healthier"@10 (de=20.00) +9 more |
| 13 | `get_upstream_features` | L6:F8984@10, k=10 → Emb:" healthier"@10 (de=20.00) +9 more |
| 14 | `get_upstream_features` | L15:F8177@9, k=10 → Emb:" eat"@9 (de=34.25) +9 more |
| 15 | `inspect_feature` ×6 | L1:15251, L5:3400, L0:9888, L0:5697, L0:8444, L0:6051 |
| 16 | `get_upstream_features` | L0:F6051@11, k=10 → Emb:"."@11 (de=46.50) +9 more |
| 17 | `get_upstream_features` | L1:F15251@5, k=10 → Emb:" clients"@5 (de=27.62) +9 more |
| 18 | `get_upstream_features` | L0:F9888@3, k=10 → Emb:" educating"@3 (de=14.88) +9 more |
| 19 | `get_upstream_features` | L0:F5697@5, k=10 → Emb:" clients"@5 (de=12.44) +9 more |
| 20 | `get_upstream_features` | L0:F8444@8, k=10 → Emb:" to"@8 (de=40.50) +9 more |
| 21 | `get_upstream_features` | L5:F3400@3, k=10 → Emb:" loves"@2 (de=9.62) +9 more |
| 22 | `get_source_influence` | {'source_positions': [9, 10, 20, 22, 23, 29]} → {'depth': 2, 'source_positions': [9, 10, 20, 22, 23, 29], 'S_pct_of_total': 17.0 |
| 23 | `get_source_influence` | {'source_positions': [1, 2, 4, 3]} → {'depth': 2, 'source_positions': [1, 2, 3, 4], 'S_pct_of_total': 6.852, 'R_pct_o |
| 24 | `get_top_features` | token="", k=10 → 10 features; top: L6:6115 de=0.128 |
| 25 | `get_upstream_features` | L6:F11327@20, k=5 → Emb:" Nutrition"@20 (de=18.12) +4 more |
| 26 | `get_upstream_features` | L14:F4197@20, k=5 → Emb:" Nutrition"@20 (de=13.69) +4 more |

### Build

`build_circuit` → 19 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 40,651 | 10,029 | 224,776 | 0 | $0.0377 | — | — |
| **Total** | | **40,651** | **10,029** | **224,776** | **0** | **$0.0377** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 0s