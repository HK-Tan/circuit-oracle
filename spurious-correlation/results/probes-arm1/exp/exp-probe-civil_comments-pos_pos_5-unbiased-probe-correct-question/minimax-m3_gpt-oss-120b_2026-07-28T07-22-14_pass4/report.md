# Circuit Oracle Report
**Date:** 2026-07-28 07:22:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a stacked "identity-group" / social-justice signal chain — embeddings of "social", "justice", "warrior" feed a L0 lexical cluster (incl. F3591 "government social programs", F7710 "you", F13310 "are") which propagates upward through L1:F13646 "text discussing social justice issues", L2:F1537 "political and social issues and movements", L3:F10868 "I'm a"/F1526 "social sciences", into a L4 cluster anchored by F117 "terms related to race, racism, and social justice" + F10459 "Tea Party/political parties" + F6752 "victimhood and social criticism", then through L5:F14124 "strong opinionated political discourse" and finally L6:F2674 "political or ideological content with negative connotations" and L6:F9005 "desserts" (firing on "bakery"/"wedding cake") — the L7+ logit is the probe's classification direction.

**Confidence:** 7

**Reasoning:** The circuit is dominated by **identity-group signaling**, not lexical/semantic content of the prompt. The single most active path is the "social justice warrior" bigram (positions 5-7): the `social` token (emb direct_effect=21 to F3591) and `justice` token (emb direct_effect=4.47 to F3591, ~4.13 to F117, ~3.91 to F1526) dominate F3591 (L0, "government social programs"), which then fans into F13646 (L1, "social justice issues", ~3.0 direct_effect from F3591 at pos 6) and F1537 (L2, "political and social issues", direct_effect=2.0 from F13646) and F1526 (L3, "social sciences", direct_effect=9.6 from `social` emb and 3.9 from `justice` emb). The peak output driver L6:F2674 ("political or ideological content with negative connotations") is reached by stacking F14124 ("strong opinionated political discourse", L5, de=1.93) ← F117 ("race, racism, social justice", L4, de=1.50, frac_nonzero=0.012) ← F10459 ("Tea Party/political parties", L4, de=1.52, frac_nonzero=0.021) ← F3591 (L0, "government social programs", de=0.89), with F2674's strongest direct upstream being the `social` embedding (de=2.13). The `warrior` token (emb de=3.41 to F14124, de=3.06 to F10459, de=3.36 to F8342) supplies almost as much as `social` does. The parallel "bakery" path (emb `bakery` de=22.4 to F9005, de=21.4 to F13041) is purely lexical/food (F9005="desserts", F13041="food and dining", F14576="food dishes") and not identity-driven — it contributes the L6 dessert detector but doesn't pass through the political/race stack. 

This is exactly the user's concern: the probe score is largely a function of the "social justice warrior" + "Muslim bakery" co-occurrence of **identity-group vocabulary** (social, justice, warrior, race/racism features, political-partisan Tea Party features, victimhood-and-social-criticism features) rather than semantic content like slurs, threats, or explicit toxicity. Neutral paraphrases ("a politically engaged person", "a community organizer", "go to a nearby bakery") would not activate F117, F10459, F13646, F6752, or F14124, yet an equivalent message about, say, "ordering pizza" or "buying flowers" would still be non-toxic — so the probe is reading off identity-group membership markers as a proxy for toxicity. The circuit is a textbook spurious-correlation artifact: `social`+`justice`+`warrior` together form a stereotyped slur-adjacent phrase whose presence alone drives the classifier. The food/dessert branch (bakery→F9005) is the only part that is genuinely lexical, and even it is anchored on the "bakery"/"cake" surface form rather than any toxic semantic.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: 'social' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: 'justice' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: 'warrior' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: 'a' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: 'you' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: 'bakery' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: 'Muslim' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F3591](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) | 6 | L0 lexical/function features at 'social justice' (pos 5-6) |  terms related to government social programs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 6 | L0 lexical/function features at 'social justice' (pos 5-6) | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F11685](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11685) | 6 | L0 lexical/function features at 'social justice' (pos 5-6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11685) |
| [L0:F9934](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) | 6 | L0 lexical/function features at 'social justice' (pos 5-6) |  the word "particular" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 2 | L0 lexical/function features at 'social justice' (pos 5-6) | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F13310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) | 3 | L0 lexical/function features at 'social justice' (pos 5-6) |  sentences that include forms of the verb "are" indicating a present state of being or necessity. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) |
| [L0:F13756](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) | 15 | L0 lexical/function features at 'social justice' (pos 5-6) |  the word "order" and occasionally "period," in many different contexts from law to food | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) |
| [L0:F2260](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) | 6 | L0 lexical/function features at 'social justice' (pos 5-6) |  terms that are medical, legal, or related to social work | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) |
| [L0:F3850](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) | 8 | L0 lexical/function features at 'social justice' (pos 5-6) | punctuation marks | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 6 | L1 social-justice / food-features at 'social justice warrior' |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L1:F14576](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14576) | 13 | L1 social-justice / food-features at 'social justice warrior' |  words relating to food dishes and dining, especially those in restaurants | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14576) |
| [L1:F14281](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14281) | 6 | L1 social-justice / food-features at 'social justice warrior' | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14281) |
| [L1:F10447](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10447) | 4 | L1 social-justice / food-features at 'social justice warrior' | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10447) |
| [L2:F1537](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1537) | 6 | L2 political/social-issues features |  words and phrases related to political and social issues and movements | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1537) |
| [L2:F14541](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) | 8 | L2 political/social-issues features |  code snippets and logical statements, especially those involving "then," along with some citation markers and bracketed references. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) |
| [L2:F14209](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) | 9 | L2 political/social-issues features | the verb "go" in its various forms. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) |
| [L2:F8867](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8867) | 4 | L2 political/social-issues features | the acronyms WIMP, WMS, WFS, and WCS | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8867) |
| [L2:F12263](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12263) | 13 | L2 political/social-issues features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12263) |
| [L3:F10868](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) | 4 | L3 'I'm a'/identity, conditional, social-science features at 'social justice warrior' |  the phrase "I'm a" or "I am a" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) |
| [L3:F16254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) | 8 | L3 'I'm a'/identity, conditional, social-science features at 'social justice warrior' |  conditional statements followed by actions the speaker will take | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) |
| [L3:F1526](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) | 6 | L3 'I'm a'/identity, conditional, social-science features at 'social justice warrior' |  references to academic disciplines related to social science | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) |
| [L3:F8342](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8342) | 7 | L3 'I'm a'/identity, conditional, social-science features at 'social justice warrior' | discussions of quality of life and health metrics, with some association with interventions | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8342) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | L4 race/social-justice + political-partisan features at 'warrior' |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F10459](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10459) | 7 | L4 race/social-justice + political-partisan features at 'warrior' |  words related to politics, especially political parties and movements like the Tea Party. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10459) |
| [L4:F11323](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11323) | 7 | L4 race/social-justice + political-partisan features at 'warrior' |  text from blog posts about political and fashion topics. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11323) |
| [L4:F6752](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6752) | 7 | L4 race/social-justice + political-partisan features at 'warrior' |  phrases expressing victimhood and social criticism | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6752) |
| [L4:F11526](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11526) | 7 | L4 race/social-justice + political-partisan features at 'warrior' |  words and short phrases related to political and military conflict | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11526) |
| [L4:F11211](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11211) | 7 | L4 race/social-justice + political-partisan features at 'warrior' |  language related to consumer advocacy and environmentalism | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11211) |
| [L4:F9008](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9008) | 7 | L4 race/social-justice + political-partisan features at 'warrior' | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9008) |
| [L4:F13041](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13041) | 13 | L4 race/social-justice + political-partisan features at 'warrior' |  words related to food and dining experiences | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13041) |
| [L4:F12425](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12425) | 7 | L4 race/social-justice + political-partisan features at 'warrior' | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12425) |
| [L5:F14124](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14124) | 7 | L5 strong opinionated political discourse / suppressors |  things that indicate strong and opinionated political discourse | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14124) |
| [L5:F1062](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1062) | 7 | L5 strong opinionated political discourse / suppressors | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1062) |
| [L5:F14212](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14212) | 13 | L5 strong opinionated political discourse / suppressors | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14212) |
| [L5:F4109](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4109) | 13 | L5 strong opinionated political discourse / suppressors | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4109) |
| [L5:F6565](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6565) | 13 | L5 strong opinionated political discourse / suppressors | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6565) |
| [L6:F2674](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) | 7 | L6 political-with-negative-connotation + desserts at 'bakery'/'warrior' |  political or ideological content, particularly with negative connotations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) |
| [L6:F9005](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) | 13 | L6 political-with-negative-connotation + desserts at 'bakery'/'warrior' |  words and phrases related to desserts | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'probe_target' is not one of the top-k next-token cand |
| 3 | `get_top_features` | 15 features; top: L0:8444 de=-0.224 |
| 4 | `inspect_feature` ×15 | L0:8444, L0:7710, L3:10868, L6:9005, L3:16254, L0:9934, L0:4478, L0:13310, L0:13756, L0:2260, L0:3850, L3:1526, L2:14541, L2:14209, L6:2674 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F2674@7` | ❌ error | — | — | Trace this political/ideological-with-negative-connotation feature upstream. Wha… |
| SA-2 | `L6:F9005@13` | ❌ error | — | — | Trace this desserts/cake feature upstream — why is it firing on position 13 (lik… |
| SA-3 | `L3:F10868@4` | ❌ error | — | — | Trace this "I'm a"/identity-phrase feature upstream. Position 4 in the prompt "I… |
| SA-4 | `L3:F16254@8` | ❌ error | — | — | Trace this conditional/imperative-action feature upstream. Position 8 in the pro… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F2674@7, k=12 → Emb:" social"@5 (de=2.12) +11 more |
| 2 | `get_upstream_features` | L6:F9005@13, k=12 → Emb:" bakery"@13 (de=22.38) +11 more |
| 3 | `get_upstream_features` | L3:F10868@4, k=12 → Emb:" a"@4 (de=18.62) +11 more |
| 4 | `get_upstream_features` | L3:F16254@8, k=12 → Emb:"If"@1 (de=9.88) +11 more |
| 5 | `get_upstream_features` | L3:F1526@6, k=12 → Emb:" social"@5 (de=9.62) +11 more |
| 6 | `inspect_feature` ×9 | L5:14124, L4:10459, L4:11323, L4:117, L0:3591, L0:9026, L4:13041, L2:8867, L2:1537 |
| 7 | `get_upstream_features` | L5:F14124@7, k=10 → Emb:" warrior"@7 (de=3.41) +9 more |
| 8 | `get_upstream_features` | L4:F10459@7, k=10 → Emb:" justice"@6 (de=1.61) +9 more |
| 9 | `get_upstream_features` | L4:F117@7, k=10 → Emb:" justice"@6 (de=4.12) +9 more |
| 10 | `get_upstream_features` | L4:F13041@13, k=10 → Emb:" bakery"@13 (de=21.38) +9 more |
| 11 | `get_upstream_features` | L2:F1537@6, k=10 → Emb:" social"@5 (de=5.91) +9 more |
| 12 | `get_upstream_features` | L0:F3591@6, k=10 → Emb:" social"@5 (de=21.00) +9 more |
| 13 | `get_upstream_features` | L3:F8342@7, k=10 → Emb:" justice"@6 (de=6.22) +9 more |
| 14 | `get_upstream_features` | L4:F9008@7, k=10 → Emb:" social"@5 (de=3.67) +9 more |
| 15 | `get_upstream_features` | L1:F13646@6, k=8 → Emb:" justice"@6 (de=4.22) +7 more |
| 16 | `inspect_feature` ×6 | L3:8342, L4:6752, L4:11526, L4:11211, L1:13646, L1:14576 |

### Build

`build_circuit` → 15 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 64,100 | 6,576 | 298,651 | 0 | $0.0450 | — | — |
| **Total** | | **64,100** | **6,576** | **298,651** | **0** | **$0.0450** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 18s