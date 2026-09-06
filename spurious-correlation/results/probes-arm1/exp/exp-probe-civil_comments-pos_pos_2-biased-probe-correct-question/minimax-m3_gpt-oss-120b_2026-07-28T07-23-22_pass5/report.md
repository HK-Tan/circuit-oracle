# Circuit Oracle Report
**Date:** 2026-07-28 07:23:23 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven almost entirely by a chain of race/ethnicity-feature detectors that activate on the literal identity tokens "white" (pos 4) and "Hispanic" (pos 7), with no circuit pathway that reads the surrounding "If he was … and not … it would be a problem" counterfactual structure for its actual semantic content.

**Confidence:** 8

**Reasoning:** Every major positive contributor to the probe is a race/ethnicity-encoding feature, not a toxicity-encoding one. The dominant path starts at the embeddings `Emb: white (pos 4)` (direct_effect +13.1 into L2:F13158, +14.4 into L4:F117, +11.5 into L6:F3077, +14.7 into L4:F117) and `Emb: Hispanic (pos 7)` (+12.8 into L6:F3902, +10.9 into L7:F5125, +6.2 into L4:F13434). These feed L1-2 early detectors L1:F9113 ("discussions about race and slavery", frac=0.019, pos 4, fires on "white" used racially), L2:F13158 ("words about race and ethnicity", frac=0.010), L2:F585 ("the word 'white'", frac=0.005), and L2:F1708 (mentions of colors) — all hitting both pos 4 and pos 7. They propagate up through L3:F3248 ("race and ethnic groups, especially in the context of social issues", frac=0.08) and L4:F117 ("terms related to race, racism, and social justice, with a particular focus on terms related to Black people", frac=0.012, promoted "racial/racist/racism"), and from L4:F117 alone the signal splits: it goes to L4:F10174 (racial/supernatural identity), L6:F3902 ("terms referring to race and ethnicity", frac=0.018, promoted "minorities/ethnicity/Hispanic"), and L7:F8030 (race/origin/demographic groups) and L7:F5125 (demographics, promoted "ethnic/Language"). The direct top-of-graph hits on the probe itself are dominated by exactly these race terms at pos 4 and pos 7: L6:F3902 (+0.57, +0.56), L2:F13158 (+0.52, +0.51), L4:F117 (+0.51, +0.22), L2:F585 (+0.19), L7:F5125 (+0.15), L7:F8030 (-0.24 suppressive).

The "what would be" / counterfactual frame is encoded separately by L6:F550 ("clauses that convey some kind of condition or past regret", promoted "would"), L7:F15213 (conditional clauses with "would/had/have"), L8:F616 (conditions/circumstances), and L4:F8840 ("were/been") — but the strongest direct conduit from these conditional features into the late aggregator runs *through* the race features: e.g. L11:F1913's top upstream at pos 5 is L10:F2249, L9:F8939, L6:F3902@pos4, then the race embeddings. The late aggregator L11:F1913 ("emotional, controversial, or political issues especially relating to race", frac=0.003, very specific) sits at the top of the chain and is the only feature firing near the probe output. Crucially, there is no feature on this path whose autointerp names a *toxicity* or *slur* or *harm* concept — the closest the model gets to "problem" is L11:F1913's "controversial or political issues relating to race," and the only content words in the sentence that activate it are "white" and "Hispanic."

The user's concern is confirmed: the probe's classification is essentially "two race/ethnicity identity tokens co-occur inside an 'If … and not …' conditional frame." The grammatical scaffolding ("If/was/and/it/would/problem") contributes to the score only by providing a conditional/counterfactual context that the race-aggregator L11:F1913 exploits; the specific content "problem" (pos 9, a generic noun) does not appear in the attribution path. The probe therefore fires on identity-mention *form* rather than on toxicity, slur, or harmful-intent *semantics*.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L11:F1913](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1913) | 5 | L11: Race-political / controversial context aggregator |  emotional, controversial, or political issues especially relating to race | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1913) |
| [L11:F1913](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1913) | 4 | L11: Race-political / controversial context aggregator |  emotional, controversial, or political issues especially relating to race | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1913) |
| [L10:F2249](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/2249) | 5 | L9-10: Conditional-frame + identity aggregation | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/2249) |
| [L9:F8939](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8939) | 5 | L9-10: Conditional-frame + identity aggregation | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8939) |
| [L9:F3438](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3438) | 5 | L9-10: Conditional-frame + identity aggregation | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3438) |
| [L9:F12707](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12707) | 4 | L9-10: Conditional-frame + identity aggregation | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12707) |
| [L8:F616](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/616) | 5 | L6-8: Conditional / counterfactual grammar detectors |  phrases about the conditions or circumstances surrounding some event | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/616) |
| [L7:F15213](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15213) | 5 | L6-8: Conditional / counterfactual grammar detectors | sentences using conditional clauses including "would", "had" and "have" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15213) |
| [L6:F550](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/550) | 5 | L6-8: Conditional / counterfactual grammar detectors |  clauses that convey some kind of condition or past regret | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/550) |
| [L4:F8840](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8840) | 3 | L6-8: Conditional / counterfactual grammar detectors | sentences including the word "were" or "been" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8840) |
| [L8:F616](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/616) | 8 | L6-8: Conditional / counterfactual grammar detectors |  phrases about the conditions or circumstances surrounding some event | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/616) |
| [L7:F15213](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15213) | 8 | L6-8: Conditional / counterfactual grammar detectors | sentences using conditional clauses including "would", "had" and "have" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15213) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 7 | L6-7: Strong race/ethnicity / demographics terms |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 4 | L6-7: Strong race/ethnicity / demographics terms |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L7:F5125](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5125) | 7 | L6-7: Strong race/ethnicity / demographics terms | mentions of demographics | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5125) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 4 | L6-7: Strong race/ethnicity / demographics terms |  words about people's races, origins, and demographic groups | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 7 | L6-7: Strong race/ethnicity / demographics terms |  words about people's races, origins, and demographic groups | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 4 | L3-4: Race / racism / social-justice terms |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | L3-4: Race / racism / social-justice terms |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F10174](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10174) | 7 | L3-4: Race / racism / social-justice terms |  words referring to racial and/or supernatural identity | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10174) |
| [L4:F13434](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13434) | 7 | L3-4: Race / racism / social-justice terms |  descriptions of a person's size, particularly height and weight | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13434) |
| [L3:F3248](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) | 4 | L3-4: Race / racism / social-justice terms |  words and phrases related to race and ethnic groups, especially in the context of social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) |
| [L3:F3248](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) | 7 | L3-4: Race / racism / social-justice terms |  words and phrases related to race and ethnic groups, especially in the context of social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 4 | L1-2: Early race/ethnicity / color word detectors |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 7 | L1-2: Early race/ethnicity / color word detectors |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 4 | L1-2: Early race/ethnicity / color word detectors | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 4 | L1-2: Early race/ethnicity / color word detectors |  mentions of colors | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 4 | L1-2: Early race/ethnicity / color word detectors |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L1:F7821](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7821) | 4 | L1-2: Early race/ethnicity / color word detectors | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7821) |
| [L0:F2458](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) | 3 | L0-1: Function words / generic context |  the word "was" and sometimes "were." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 8 | L0-1: Function words / generic context |  references to the pronoun "it", and sometimes "that", suggesting observation of the subject of a discussion | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 5 | L0-1: Function words / generic context |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2458 de=-0.660 |
| 3 | `inspect_feature` ×14 | L0:2458, L6:3902, L2:13158, L4:117, L0:880, L0:3255, L1:9113, L7:8030, L2:585, L3:3248, L4:2398, L11:1913, L7:5125, L2:1708 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@7` | ❌ error | — | — | Trace from L6:F3902 (race/ethnicity terms) at pos 7 (Hispanic) upstream to find … |
| SA-2 | `L2:F13158@4` | ❌ error | — | — | Trace from L2:F13158 (race/ethnicity words) at pos 4 (white) upstream to find wh… |
| SA-3 | `L11:F1913@5` | ❌ error | — | — | Trace from L11:F1913 (race-related political issues) at pos 5 (and) upstream. Fi… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L11:F1913@5, k=10 → Emb:"<bos>"@0 (de=-4.81) +9 more |
| 2 | `get_upstream_features` | L6:F3902@7, k=10 → Emb:" Hispanic"@7 (de=12.81) +9 more |
| 3 | `get_upstream_features` | L2:F13158@4, k=10 → Emb:" white"@4 (de=13.12) +9 more |
| 4 | `get_upstream_features` | L4:F117@4, k=10 → Emb:" white"@4 (de=14.75) +9 more |
| 5 | `get_upstream_features` | L10:F2249@5, k=10 → Emb:"If"@1 (de=4.34) +9 more |
| 6 | `get_upstream_features` | L9:F8939@5, k=10 → Emb:" was"@3 (de=1.76) +9 more |
| 7 | `get_upstream_features` | L9:F3438@5, k=10 → L8:F616 (de=4.84) +9 more |
| 8 | `get_upstream_features` | L6:F7233@5, k=10 → Emb:" and"@5 (de=1.79) +9 more |
| 9 | `inspect_feature` ×7 | L8:616, L6:550, L7:15213, L4:8840, L2:1139, L4:13434, L4:10174 |
| 10 | `get_upstream_features` | L7:F5125@7, k=10 → Emb:" Hispanic"@7 (de=10.88) +9 more |
| 11 | `get_upstream_features` | L4:F13434@7, k=10 → Emb:" Hispanic"@7 (de=6.16) +9 more |
| 12 | `get_upstream_features` | L7:F8030@4, k=10 → L6:F3902 (de=5.62) +9 more |
| 13 | `get_upstream_features` | L7:F8030@7, k=10 → L6:F3902 (de=5.91) +9 more |
| 14 | `get_upstream_features` | L0:F880@8, k=8 → Emb:" it"@8 (de=42.50) +7 more |
| 15 | `get_upstream_features` | L0:F2458@3, k=8 → Emb:" was"@3 (de=36.75) +7 more |
| 16 | `get_upstream_features` | L1:F9113@4, k=8 → Emb:" white"@4 (de=14.44) +7 more |
| 17 | `get_upstream_features` | L7:F8030@5, k=8 → L6:F3902 (de=3.16) +7 more |
| 18 | `get_upstream_features` | L11:F1913@4, k=8 → Emb:"<bos>"@0 (de=-3.25) +7 more |
| 19 | `get_upstream_features` | L11:F1913@7, k=8 → ❌ Feature (layer=11, feature_idx=1913) not found at pos=7. Thi |
| 20 | `get_upstream_features` | L7:F5125@4, k=8 → ❌ Feature (layer=7, feature_idx=5125) not found at pos=4. This |
| 21 | `get_upstream_features` | L7:F5125@5, k=8 → ❌ Feature (layer=7, feature_idx=5125) not found at pos=5. This |
| 22 | `get_upstream_features` | L10:F2249@4, k=8 → ❌ Feature (layer=10, feature_idx=2249) not found at pos=4. Thi |
| 23 | `get_upstream_features` | L9:F12707@4, k=8 → Emb:" white"@4 (de=5.38) +7 more |
| 24 | `get_upstream_features` | L6:F3077@4, k=8 → Emb:" white"@4 (de=11.50) +7 more |
| 25 | `get_upstream_features` | L1:F9113@7, k=8 → ❌ Feature (layer=1, feature_idx=9113) not found at pos=7. This |
| 26 | `get_upstream_features` | L11:F1913@8, k=8 → Emb:"<bos>"@0 (de=-6.22) +7 more |
| 27 | `get_upstream_features` | L9:F12707@5, k=8 → Emb:" white"@4 (de=5.06) +7 more |
| 28 | `get_upstream_features` | L9:F8939@4, k=8 → Emb:" was"@3 (de=1.50) +7 more |
| 29 | `get_upstream_features` | L2:F585@4, k=8 → Emb:" white"@4 (de=29.38) +7 more |
| 30 | `get_upstream_features` | L10:F2249@8, k=8 → Emb:"If"@1 (de=4.09) +7 more |
| 31 | `get_upstream_features` | L9:F8939@8, k=8 → Emb:" it"@8 (de=3.36) +7 more |
| 32 | `get_upstream_features` | L9:F3438@8, k=8 → L8:F616 (de=6.16) +7 more |
| 33 | `get_upstream_features` | L7:F12891@8, k=8 → Emb:" it"@8 (de=3.97) +7 more |

### Build

`build_circuit` → 16 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 62,211 | 7,160 | 446,279 | 0 | $0.0540 | — | — |
| **Total** | | **62,211** | **7,160** | **446,279** | **0** | **$0.0540** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 34s