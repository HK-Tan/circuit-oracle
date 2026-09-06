# Circuit Oracle Report
**Date:** 2026-07-28 07:22:08 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by a stack of features that detect *race / ethnicity vocabulary and identity-group discourse*, triggered specifically by the tokens "white" (pos 4) and "Hispanic" (pos 7); content-word features describing what the sentence actually *does* to the subject (negation, conditional "would be", generic lexical anchors) play only a minor, mostly modulatory role.

**Confidence:** 9

**Reasoning:** The user concern is strongly supported by the attribution circuit. The highest-magnitude feature on the probe (L6:F3902, direct_effect 0.57) is labeled *"terms referring to race and ethnicity"* and is directly fed by the embedding of "Hispanic" (direct_effect 12.81) and the embedding of "white" (2.69). The next-strongest features are L2:F13158 (*"words about race and ethnicity,"* 0.52) and L4:F117 (*"terms related to race, racism, and social justice, with a particular focus on terms related to Black people,"* 0.51), both of which are *upstream* of L6:F3902 and are likewise dominated by the white/Hispanic token embeddings (white→L2:F13158: 13.13; white→L4:F117: 14.75; Hispanic→L4:F117: 4.91). Together these L2–L7 features form a deep "race / demographic vocabulary" chain with frac_nonzero values from 0.009 to 0.11 — i.e., they are selectively tuned to race-related vocabulary, not to syntactic negation or counterfactual structure. At L11, F1913 (*"emotional, controversial, or political issues especially relating to race"*, frac_nonzero 0.003) inherits this signal and contributes +0.15 to the probe. Throughout, *no feature with a non-race-related label contributes a positive direct effect above noise*: the "was" / "and" / "it" lexical features (L0:F2458, L0:F3255, L0:F880) are generic (frac_nonzero ≈ 0.025–0.03) and have small or negative effects (-0.66, +0.18, -0.23). The "not" token, which is what *makes* the sentence counterfactually protective of the white subject, is not picked up by any positively-contributing feature. The circuit's signal flow — Emb: white/Hispanic → L2-L3 color/race features → L4 race/racism features → L6-L7 demographic features → L10-L11 controversial-race features → probe — is a textbook identity-cue pathway, not a toxicity-content pathway. Even though this particular sentence is arguably *non-toxic* (it explicitly wishes the subject were not Hispanic), the probe lights up on the demographic vocabulary alone, which confirms the user's suspicion that the model is using spurious "identity group present" features rather than lexical/semantic indicators of harmful content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 9 | Probe direction (toxicity / hate-speech classification score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L11:F1913](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1913) | 5 | Late-layer identity-group / controversial-race features (L10-L11) |  emotional, controversial, or political issues especially relating to race | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1913) |
| [L10:F2249](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/2249) | 5 | Late-layer identity-group / controversial-race features (L10-L11) |  words related to legal or policy language, potentially with a negative opinion | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/2249) |
| [L9:F8939](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8939) | 5 | Late-layer identity-group / controversial-race features (L10-L11) |  equations involving variables being replaced with other variables | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8939) |
| [L9:F3438](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3438) | 5 | Late-layer identity-group / controversial-race features (L10-L11) |  conditional phrases and clauses | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3438) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 4 | Mid-layer race / ethnicity / demographic features (L6-L7) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 7 | Mid-layer race / ethnicity / demographic features (L6-L7) |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 4 | Mid-layer race / ethnicity / demographic features (L6-L7) |  words about people's races, origins, and demographic groups | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 7 | Mid-layer race / ethnicity / demographic features (L6-L7) |  words about people's races, origins, and demographic groups | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L7:F5125](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5125) | 7 | Mid-layer race / ethnicity / demographic features (L6-L7) | mentions of demographics | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5125) |
| [L6:F7233](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7233) | 5 | Mid-layer race / ethnicity / demographic features (L6-L7) |  language around racial and ethnic identity, healthcare, and prejudice. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7233) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 4 | Early-layer race / racism / social-justice features (L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | Early-layer race / racism / social-justice features (L4) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F10174](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10174) | 7 | Early-layer race / racism / social-justice features (L4) |  words referring to racial and/or supernatural identity | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10174) |
| [L4:F13434](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13434) | 7 | Early-layer race / racism / social-justice features (L4) |  descriptions of a person's size, particularly height and weight | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13434) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 4 | Early-layer race / ethnic-group / color features (L2-L3) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 7 | Early-layer race / ethnic-group / color features (L2-L3) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 4 | Early-layer race / ethnic-group / color features (L2-L3) | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 4 | Early-layer race / ethnic-group / color features (L2-L3) |  mentions of colors | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L3:F11768](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) | 4 | Early-layer race / ethnic-group / color features (L2-L3) |  the word "white" and related contexts such as diversity | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) |
| [L3:F3248](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) | 4 | Early-layer race / ethnic-group / color features (L2-L3) |  words and phrases related to race and ethnic groups, especially in the context of social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) |
| [L3:F3248](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) | 7 | Early-layer race / ethnic-group / color features (L2-L3) |  words and phrases related to race and ethnic groups, especially in the context of social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) |
| [L0:F2458](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) | 3 | Generic lexical features (L0-L1: was, and, it) |  the word "was" and sometimes "were." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 5 | Generic lexical features (L0-L1: was, and, it) |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 8 | Generic lexical features (L0-L1: was, and, it) |  references to the pronoun "it", and sometimes "that", suggesting observation of the subject of a discussion | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 4 | Generic lexical features (L0-L1: was, and, it) |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L5:F3924](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3924) | 7 | Generic lexical features (L0-L1: was, and, it) |  words relating to race, ethnicity, and/or religion | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3924) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: white (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: Hispanic (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: was (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: and (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: not (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: it (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2458 de=-0.660 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@7` | ❌ error | — | — | Trace the path from L6:F3902 at pos 7 (activation 18.75, direct_effect 0.57). Th… |
| SA-2 | `L2:F13158@4` | ❌ error | — | — | Trace the path from L2:F13158 at pos 4 (activation 11.19, direct_effect 0.52). T… |
| SA-3 | `L4:F117@4` | ❌ error | — | — | Trace the path from L4:F117 at pos 4 (activation 14.375, direct_effect 0.51). Th… |
| SA-4 | `L11:F1913@5` | ❌ error | — | — | Trace the path from L11:F1913 at pos 5 (activation 27.375, direct_effect 0.15). … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×14 | L6:3902, L2:13158, L4:117, L11:1913, L0:2458, L0:880, L0:3255, L7:8030, L3:3248, L4:2398, L7:5125, L2:585, L2:1708, L1:9113 |
| 2 | `get_upstream_features` | L6:F3902@7, k=10 → Emb:" Hispanic"@7 (de=12.81) +9 more |
| 3 | `get_upstream_features` | L2:F13158@4, k=10 → Emb:" white"@4 (de=13.12) +9 more |
| 4 | `get_upstream_features` | L4:F117@4, k=10 → Emb:" white"@4 (de=14.75) +9 more |
| 5 | `get_upstream_features` | L11:F1913@5, k=10 → Emb:"<bos>"@0 (de=-4.81) +9 more |
| 6 | `inspect_feature` ×8 | L3:11768, L10:2249, L9:8939, L4:10174, L4:13434, L6:7233, L9:3438, L5:3924 |
| 7 | `get_upstream_features` | L2:F13158@7, k=10 → Emb:" Hispanic"@7 (de=11.12) +9 more |
| 8 | `get_upstream_features` | L4:F117@7, k=8 → Emb:" white"@4 (de=6.00) +7 more |
| 9 | `get_upstream_features` | L7:F8030@4, k=8 → L6:F3902 (de=5.62) +7 more |

### Build

`build_circuit` → 12 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 52,629 | 5,607 | 169,022 | 0 | $0.0327 | — | — |
| **Total** | | **52,629** | **5,607** | **169,022** | **0** | **$0.0327** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 19s