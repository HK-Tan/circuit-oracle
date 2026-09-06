# Circuit Oracle Report
**Date:** 2026-07-28 07:02:46 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven almost entirely by an identity-group signal that originates from the literal tokens "white" (pos 4) and "Hispanic" (pos 7); the rest of the sentence (the conditional scaffolding "If he was… and not… it would be a problem") has no detectable contribution to the probe.

**Confidence:** 9

**Reasoning:** The attribution graph reveals a remarkably narrow, identity-centric circuit that supports the user's concern almost perfectly.

**Late layer → output.** The strongest direct driver of the probe score is `L6:F3902` ("terms referring to race and ethnicity," frac_nonzero 0.018) firing on the token "Hispanic" at pos 7 (direct_effect 0.57) and "white" at pos 4 (direct_effect 0.56). The next strongest contributor is `L2:F13158` ("words about race and ethnicity," frac_nonzero 0.010) firing on both "white" and "Hispanic" (direct_effect ≈ 0.52). `L4:F117` ("race, racism, and social justice," frac_nonzero 0.012) fires on the same two identity tokens (direct_effect ≈ 0.22–0.51). `L0:F2458` ("was") pushes the score *negatively* (direct_effect -0.66), which is the only counter-signal of note, and `L7:F8030` ("words about people's races, origins, demographic groups," frac_nonzero 0.11) is also inhibitory on these positions (direct_effect ≈ -0.19 to -0.24).

**Mid layer.** `L7:F5125` ("mentions of demographics") and `L6:F3077` ("places and categorizations of people by place") and `L5:F3924` ("words relating to race, ethnicity, and/or religion") all encode the same identity-group concept, propagating the signal.

**Embedding roots.** Tracing back to the token-embedding layer confirms the source: `L6:F3902@pos7` receives direct_effect 12.81 from the "Hispanic" embedding and 2.69 from the "white" embedding; `L2:F13158@pos4` receives 13.13 from the "white" embedding. The largest single edge in the entire graph is `Emb:"was"@pos3 → L0:F2458` (direct_effect 36.75) — but L0:F2458 is the suppressor noted above.

**Lexical content absent.** No feature in the top-20 list detects any of the actually-toxic or evaluative words in the prompt: "problem" (the toxic-complaint payload), "s" (typo), "it would be" (the conditional), "if"/"he" (the conditional antecedent). The text "it would be s problem" is structurally an explicit racial-prejudice statement, yet the model attributes the toxicity signal solely to the identity nouns "white" and "Hispanic."

**Suppression noted.** L7:F8030 actually inhibits the probe (it fires on the same tokens but pushes the score *down*), suggesting the model has both a generic race-mention detector that pushes toward toxicity and a slightly more specific demographic-group detector that partially offsets it. Even so, the net push from the identity-token features is strongly positive.

**Conclusion.** The user's concern is well-founded: the probe classifies the sentence as toxic based almost exclusively on the presence of two racial-identity tokens, not on any lexical or semantic feature of the surrounding "it would be a problem" structure. The circuit is a textbook case of a spurious-correlation shortcut: a toxicity detector wired to "an identity group is mentioned" rather than to "the statement is harmful."

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L11:F1913](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1913) | 5 | Late-layer race-related controversy features |  emotional, controversial, or political issues especially relating to race | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1913) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 4 | Mid-layer race / demographic-group features |  words about people's races, origins, and demographic groups | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 7 | Mid-layer race / demographic-group features |  words about people's races, origins, and demographic groups | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L7:F5125](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5125) | 7 | Mid-layer race / demographic-group features | mentions of demographics | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5125) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 4 | Mid-layer race / demographic-group features |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 7 | Mid-layer race / demographic-group features |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L5:F3924](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3924) | 7 | Mid-layer race / demographic-group features |  words relating to race, ethnicity, and/or religion | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3924) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 4 | Early-layer race-lexicon features |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | Early-layer race-lexicon features |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F10174](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10174) | 7 | Early-layer race-lexicon features |  words referring to racial and/or supernatural identity | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10174) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 4 | Early-layer race-lexicon features |  art galleries, museums and the White House | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L3:F3248](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) | 4 | Early-layer race-lexicon features |  words and phrases related to race and ethnic groups, especially in the context of social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) |
| [L3:F3248](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) | 7 | Early-layer race-lexicon features |  words and phrases related to race and ethnic groups, especially in the context of social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3248) |
| [L3:F11768](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) | 4 | Early-layer race-lexicon features |  the word "white" and related contexts such as diversity | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11768) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 4 | Early-layer race-lexicon features |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 7 | Early-layer race-lexicon features |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 4 | Early-layer race-lexicon features | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F1708](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) | 4 | Early-layer race-lexicon features |  mentions of colors | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1708) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 4 | Generic token / social-justice features |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L1:F1480](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) | 4 | Generic token / social-justice features | the color 'white', sometimes in a context involving race | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1480) |
| [L1:F4668](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4668) | 4 | Generic token / social-justice features |  the color white being used to describe image parameters | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4668) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 4 | Generic token / social-justice features |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L1:F15969](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15969) | 4 | Generic token / social-justice features |  terms related to the Civil War and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15969) |
| [L1:F7821](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7821) | 4 | Generic token / social-justice features |  mentions of computer fans. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7821) |
| [L0:F2458](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) | 3 | Generic token / social-justice features |  the word "was" and sometimes "were." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) |
| [L0:F3255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) | 5 | Generic token / social-justice features |  the word "and" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3255) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 8 | Generic token / social-justice features |  references to the pronoun "it", and sometimes "that", suggesting observation of the subject of a discussion | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 4 | Generic token / social-justice features |  mentions of the word "white" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F16013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) | 4 | Generic token / social-justice features |  mentions of the color blue, and perhaps colors in general or the components of a graphic image | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2458 de=-0.660 |
| 3 | `inspect_feature` ×4 | L6:3902, L2:13158, L4:117, L0:2458 |
| 4 | `get_upstream_features` | Emb:" Hispanic"@7 (de=12.81) +9 more |
| 5 | `get_upstream_features` | Emb:" white"@4 (de=13.12) +9 more |
| 6 | `get_upstream_features` | Emb:" white"@4 (de=14.75) +9 more |
| 7 | `get_upstream_features` | Emb:" was"@3 (de=36.75) +9 more |
| 8 | `inspect_feature` ×16 | L5:3924, L4:10174, L4:13434, L3:3248, L2:585, L1:7821, L0:880, L0:3255, L7:8030, L11:1913, L7:5125, L4:2398, L2:1708, L0:16013, L3:11768, L1:9113 |
| 9 | `get_upstream_features` | L6:F3902 (de=5.62) +7 more |
| 10 | `get_upstream_features` | L6:F3902 (de=5.91) +7 more |
| 11 | `get_upstream_features` | Emb:" Hispanic"@7 (de=10.88) +9 more |
| 12 | `get_upstream_features` | Emb:"<bos>"@0 (de=-4.81) +9 more |
| 13 | `inspect_feature` ×7 | L4:15204, L6:3077, L1:1480, L1:4668, L1:13646, L1:15969, L0:3436 |

### Build

`build_circuit` → 9 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 61,768 | 4,513 | 144,264 | 0 | $0.0326 | — | — |
| **Total** | | **61,768** | **4,513** | **144,264** | **0** | **$0.0326** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 0s