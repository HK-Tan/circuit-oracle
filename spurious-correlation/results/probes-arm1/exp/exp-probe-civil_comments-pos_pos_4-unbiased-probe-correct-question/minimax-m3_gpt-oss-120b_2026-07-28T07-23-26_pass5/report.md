# Circuit Oracle Report
**Date:** 2026-07-28 07:23:26 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven by a mid-layer circuit that detects the co-occurrence of an identity-group term (the embedding node "Indians" at pos 1) with explicitly negative/predicative content (the embedding nodes "are", "abusers", "stated", "they", "is", "by", "those"), with most of the activation routed through features that key on "people as a group" rather than on the actual toxic words themselves.

**Confidence:** 8

**Reasoning:** The signal originates overwhelmingly from the input token embeddings (Emb: Indians pos 1, direct_effect 10.25→12.375; Emb: are pos 2; Emb: abusers pos 3, direct_effect 1.9→9.9; Emb: stated pos 7; Emb: they pos 5). At L0, the strongest drive comes from token-level features that are basically **identity-of-a-group** detectors sitting on the subject noun: L0:F11668 (frac 0.0088, the L0 token-feature sitting on "Indians"), L0:F10155 (frac 0.046, "words related to membership in a group" — explicitly fires on "Indians" in this prompt), and L0:F13535 (frac 0.012, generic group/people terms). These feed the L2 group-identity supernode (F1680 "people participating in an activity" — its top examples literally include "Canadians"; F2123 "-ian" suffix detector that promotes "Canadian" tokens; F5368 "legal trouble and crime"), which then activates the L3 supernode: the most positively-promoting L3 feature is F13473 (frac 0.0057) — its label is literally **"mentions of racial and ethnic groups, especially in the United States"** — and F9646 (verbs like "destroy") plus F2705 (cheating/deception) and F5853 ("stated") riding on the same subject. This L3 supernode is the core "this sentence is *about* a named group doing something bad" detector, and it is the strongest *non-embedding* contributor to the probe.

Crucially, what is *not* in the circuit is just as informative: the actual toxicity-bearing tokens ("abusers", "abusing", "destroy", "backlash") have no dedicated late-layer features driving the probe. Instead, the L4–L6 supernodes (F148 "sexual assault/abuse", F14198 "rights-violation legal/political discourse", F8793 "strong political opinions", F1600 "problems", F10545 "political rhetoric related to race and historical states") are largely *activated by* the L3 group-identity features, and they themselves are *not* highly direct drivers of the probe (their own direct_effects onto the logit are weak or negative — e.g. L6:F10545 is +0.136 but sits downstream of negative contributors like L3:F14281 at -0.157). The clearest evidence that the circuit is identity-driven rather than lexically toxic is the *inhibitory* path: L0:F3436 ("the word 'white'") and L0:F11154 ("the word 'are'") push *against* the probe score, and L0:F3498 ("they") and L0:F15956 ("those") — pure anaphoric pronouns with no toxicity content — carry positive direct effects (45.25 and 40.75 respectively) on the output purely by virtue of pointing back at the group subject. The probe is reading "is X a named demographic group being predicated of?" more than "is this sentence toxic?" — a textbook **spurious correlation / demographic-identity shortcut**, confirming the user's concern. The actual toxic verbs ("abusers", "abusing", "destroy") enter mainly via generic lexeme features (L0:F11668 base-form detector, L0:F1847, L0:F1847 generic scientific-token feature on "abusers"), not via any abuse-specific late-layer features with strong direct effect on the logit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F11668](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11668) | 1 | Token-level lexical features (L0) |  Baseball terminology | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11668) |
| [L0:F11154](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) | 2 | Token-level lexical features (L0) |  the word "are" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11154) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 8 | Token-level lexical features (L0) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 5 | Token-level lexical features (L0) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F15956](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15956) | 25 | Token-level lexical features (L0) | the word "those" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15956) |
| [L0:F8381](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8381) | 23 | Token-level lexical features (L0) |  the word 'by' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8381) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 7 | Token-level lexical features (L0) |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F6035](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6035) | 7 | Token-level lexical features (L0) | the word "depending" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6035) |
| [L0:F10155](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) | 1 | Token-level lexical features (L0) |  words related to membership in a group | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10155) |
| [L0:F1847](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1847) | 3 | Token-level lexical features (L0) | scientific terms and experimental details related to biological and chemical research | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1847) |
| [L0:F13535](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13535) | 1 | Token-level lexical features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13535) |
| [L2:F1680](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) | 1 | Group identity / membership features (L2) |  words that refer to people participating in some activity, such as consumers, patients in healthcare, or voters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) |
| [L2:F2123](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) | 1 | Group identity / membership features (L2) |  words ending in "ian", "jani", "iti", "ino", or "olan" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) |
| [L2:F5368](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5368) | 3 | Group identity / membership features (L2) |  words related to legal trouble and crime | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5368) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | Identity/hostility-mid-layer features (L3) |  mentions of racial and ethnic groups, especially in the United States | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L3:F4327](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4327) | 3 | Identity/hostility-mid-layer features (L3) | words and phrases that end with "ive", and also a few words that end in "ices" or "ishes", and also the phrase "advantage of the". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4327) |
| [L3:F2705](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2705) | 3 | Identity/hostility-mid-layer features (L3) |  words related to cheating or being deceptive | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2705) |
| [L3:F9646](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9646) | 2 | Identity/hostility-mid-layer features (L3) | verbs and associated nouns. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9646) |
| [L3:F5853](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5853) | 7 | Identity/hostility-mid-layer features (L3) |  instances of people speaking and making statements | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5853) |
| [L3:F12378](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12378) | 3 | Identity/hostility-mid-layer features (L3) | words related to medicine, law, and infection | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12378) |
| [L3:F14281](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14281) | 18 | Identity/hostility-mid-layer features (L3) |  questions about how to do things, and some French words | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14281) |
| [L4:F148](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) | 3 | Abuse / rights-violation discourse (L4) |  words and phrases related to sexual assault and abuse | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) |
| [L4:F14198](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14198) | 3 | Abuse / rights-violation discourse (L4) |  terms found in legal or political discourse, especially where rights are being violated or impinged. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14198) |
| [L4:F4021](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) | 4 | Abuse / rights-violation discourse (L4) |  code snippets or configurations with the word "as". | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) |
| [L5:F3229](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3229) | 3 | Negativity / violent-assault features (L5) |  words related to violent assault and murder | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3229) |
| [L5:F8793](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8793) | 3 | Negativity / violent-assault features (L5) |  language expressing strong opinions or negativity, potentially related to political, social, or historical issues. | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/8793) |
| [L6:F10545](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) | 3 | Political rhetoric & problem features (L6) |  political rhetoric related to race, historical states, and government control | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) |
| [L6:F1600](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1600) | 12 | Political rhetoric & problem features (L6) |  negative words and phrases related to problems and imperfections | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1600) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_candidate_vote_tally` | ❌ This tool requires ctx.sibling_graphs to be set (at least on |
| 3 | `get_top_features` | 20 features; top: L0:11375 de=0.221 |
| 4 | `rank_segment_features` | ❌ This tool requires ctx.sibling_graphs to be set (at least on |
| 5 | `inspect_feature` ×20 | L0:11375, L0:11668, L6:10545, L3:14281, L0:11154, L2:1680, L3:13473, L5:3229, L0:8381, L6:1600, L0:3498, L0:3436, L3:5853, L0:15956, L0:6035, L3:9646, L3:4327, L3:2705, L4:4021, L1:13535 |
| 6 | `get_upstream_features` | Emb:"Indians"@1 (de=10.25) +7 more |
| 7 | `get_upstream_features` | Emb:" abusers"@3 (de=1.90) +7 more |
| 8 | `get_upstream_features` | Emb:" abusers"@3 (de=1.90) +11 more |
| 9 | `inspect_feature` ×4 | L4:148, L6:1600, L2:2123, L0:10155 |
| 10 | `get_upstream_features` | Emb:"Indians"@1 (de=12.38) +11 more |
| 11 | `inspect_feature` ×2 | L0:1847, L2:5368 |
| 12 | `get_upstream_features` | Emb:"Indians"@1 (de=8.56) +9 more |
| 13 | `get_upstream_features` | Emb:" how"@17 (de=31.38) +9 more |
| 14 | `get_upstream_features` | Emb:" by"@23 (de=36.25) +9 more |
| 15 | `get_upstream_features` | Emb:" those"@25 (de=40.75) +9 more |
| 16 | `get_upstream_features` | Emb:" are"@2 (de=36.00) +9 more |
| 17 | `get_upstream_features` | Emb:" is"@8 (de=32.50) +9 more |
| 18 | `get_upstream_features` | Emb:"Indians"@1 (de=3.97) +9 more |
| 19 | `get_upstream_features` | Emb:" problems"@12 (de=21.25) +9 more |
| 20 | `get_upstream_features` | Emb:" abusers"@3 (de=9.88) +9 more |
| 21 | `get_upstream_features` | Emb:" they"@5 (de=45.25) +9 more |
| 22 | `get_upstream_features` | Emb:" stated"@7 (de=23.75) +9 more |
| 23 | `get_upstream_features` | Emb:" stated"@7 (de=10.75) +9 more |
| 24 | `get_upstream_features` | Emb:" stated"@7 (de=11.06) +9 more |
| 25 | `get_upstream_features` | Emb:"Indians"@1 (de=12.38) +9 more |
| 26 | `get_upstream_features` | Emb:" abusers"@3 (de=12.75) +9 more |
| 27 | `get_upstream_features` | Emb:"Indians"@1 (de=3.97) +9 more |
| 28 | `get_upstream_features` | Emb:" abusers"@3 (de=1.91) +9 more |
| 29 | `get_upstream_features` | ❌ Feature (layer=5, feature_idx=3229) not found at pos=4. This |
| 30 | `get_upstream_features` | Emb:" abusers"@3 (de=1.90) +9 more |
| 31 | `inspect_feature` ×3 | L5:8793, L3:12378, L4:14198 |
| 32 | `get_upstream_features` | Emb:" abusers"@3 (de=9.88) +11 more |
| 33 | `get_upstream_features` | Emb:" abusers"@3 (de=12.75) +11 more |

### Build

`build_circuit` → 16 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 58,277 | 6,424 | 396,050 | 0 | $0.0490 | — | — |
| **Total** | | **58,277** | **6,424** | **396,050** | **0** | **$0.0490** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 33s