# Circuit Oracle Report
**Date:** 2026-07-28 07:04:18 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxic-classification score is driven almost entirely by *identity-group recognition features* (LGBTQ+, Muslim, race/social-justice, religious-affiliation) anchored on the input tokens "gay" (pos 17), "Muslim" (pos 12), and "social justice" (pos 5–6), not by features encoding the prompt's *imperative/slur structure* (e.g., "go to a … order a …") which is the actual toxic content.

**Confidence:** 8

**Reasoning:**

The output node represents the probe direction (no usable token label — `get_top_logits` returned an empty string). Driving the probe score are three **identity-recognition supernodes**, each firing on a single identity-mention token:

1. **gay_topic_L6 → lgbtq_topic_L8** (L6:F6085, L8:F15771, pos 17, "gay"). Tracing upstream, L6:F6085 receives a direct embedding contribution of 37.0 from the literal "gay" token — essentially a token-identity detector. L8:F15771 promotes tokens like "ISLAM" and the autointerp is "LGBTQ+ issues, same-sex marriage." Top direct effects: 0.326 (L6) and 0.277 (L8) toward the probe.

2. **islam_topic_L3 → religion_L4 → islam_topic_L6** (L3:F12024, L4:F2405, L6:F7282, pos 12, "Muslim"). L6:F7282 receives a 22.6 direct embedding contribution from the "Muslim" token and promotes "mosques", "Muslim", "Islamic", "Islam". Direct effects: 0.193 (L6) + 0.170 (L4).

3. **race_sj_L1 → race_sj_L3 → race_sj_L4** (L1:F13646, L3:F5157+F13061, L4:F117, firing on pos 5–7, "social justice"). L4:F117 promotes "racist/racism/Racial" and fires across pos 6, 7, 13. Direct effects: 0.264+0.260+0.143.

Other features feeding the probe are mostly **task-spurious**:
- L0:F7710 (pronoun "you", pos 2) — direct_effect −0.281, *suppresses* the probe
- L6:F10969 (swear words) — direct_effect 0.126, but the prompt contains no actual swear; the feature fires because the model mis-associates the identity-laden phrase with hostility
- L11:F1291 ("racist content", pos 7) — direct_effect 0.125, again an identity-vicinity toxicity detector

The **mechanism**: the probe direction is well-aligned with the model's internal "identity-group" feature subspace, which is the same subspace the toxicity probe picked up during training. The circuit confirms the user's concern — the probe's classification is driven by **lexical/identity triggers** ("gay", "Muslim", "social justice") rather than the prompt's imperative-imperative structure (which would require features for imperatives, conditional abuse, or refusal-relevant syntax). Spurious identity detectors (low frac_nonzero ~0.001–0.013, all high-specificity) carry the majority of the signed mass; the actual toxic content is *not* represented by any feature in the top direct-effect list.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 17 | LGBTQ+ topic discussion (gay/same-sex marriage) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 17 | Text related to homosexuality / same-sex marriage |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 12 | Islam / Middle East mentions |  mentions of Islam or Middle Eastern places and people, as well as mentions of a specific district. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L3:F12024](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) | 12 | Islam religion references |  words referencing the religion of Islam, people who practice it, and Arabic names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 12 | Religious identity / affiliation terms |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Race / racism / social-justice terms |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | Race / racism / social-justice terms |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 13 | Race / gender / social-issues vocabulary |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F5157](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5157) | 6 | Race / gender / social-issues vocabulary |  references to social services and social work | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5157) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 6 | Social-justice text |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L11:F1291](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1291) | 7 | Racist / hostile content (L11) |  racist content | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1291) |
| [L6:F10969](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10969) | 7 | Swear words / insults |  swear words and insults | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10969) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 2 | Pronoun 'you' (L0) | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token '0' is not one of the top-k next-token candidates capt |
| 3 | `get_top_features` | 20 features; top: L6:6085 de=0.326 |
| 4 | `inspect_feature` ×18 | L6:6085, L8:15771, L4:117, L6:7282, L4:2405, L3:5157, L3:12024, L3:5959, L3:13061, L0:7710, L0:3215, L0:10421, L0:6764, L0:7519, L0:8497, L1:13646, L6:10969, L11:1291 |
| 5 | `get_upstream_features` | Emb:" gay"@17 (de=37.00) +14 more |
| 6 | `get_upstream_features` | Emb:" gay"@17 (de=17.00) +14 more |
| 7 | `get_upstream_features` | Emb:" justice"@6 (de=5.12) +9 more |
| 8 | `get_upstream_features` | Emb:" justice"@6 (de=4.12) +9 more |
| 9 | `get_upstream_features` | Emb:" Muslim"@12 (de=22.62) +9 more |
| 10 | `get_upstream_features` | Emb:" Muslim"@12 (de=15.75) +9 more |

### Build

`build_circuit` → 13 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 43,715 | 3,774 | 142,169 | 0 | $0.0262 | — | — |
| **Total** | | **43,715** | **3,774** | **142,169** | **0** | **$0.0262** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 25s