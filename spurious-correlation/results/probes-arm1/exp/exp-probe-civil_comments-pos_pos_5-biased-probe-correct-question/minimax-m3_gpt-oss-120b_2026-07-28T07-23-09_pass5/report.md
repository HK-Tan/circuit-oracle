# Circuit Oracle Report
**Date:** 2026-07-28 07:23:09 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity-classification score is driven almost entirely by features that detect **identity-group / social-justice vocabulary** (LGBTQ+ topics, Muslim/Islamic identity, race & social-justice terms) — not by features that encode the prompt's actual hateful content (the imperative structure, the bigotry, the mockery). This strongly supports the user's hypothesis: the probe is using spurious "identity-group" signals as a shortcut for toxicity.

**Confidence:** 8

**Reasoning:** Tracing the attribution graph back to the input token embeddings reveals that every positive contribution to the probe's score originates from the *identity* words in the prompt and zero from the *hateful-action* structure. The top direct contributors are:

- **L6:F6085** ("text related to homosexuality and same-sex marriage", frac=0.0017, pos 17 *"gay"*, de=+0.33) and **L8:F15771** ("discussion of LGBTQ+ issues, especially same-sex marriage", frac=0.0078, pos 17, de=+0.28) — these are *topic* detectors. Their own upstreams (L4:F8645, L4:F15899, L1:F6639, L2:F4124) all trace to the bare embedding of the token *"gay"* (de=+22 to +37). The "gay" token alone drives the entire LGBTQ-branch.
- **L6:F7282** ("mentions of Islam or Middle Eastern places and people", pos 12 *"Muslim"*, de=+0.19) and **L4:F2405** ("religious identity/affiliation", pos 12, de=+0.17) trace back through **L3:F12024** ("the religion of Islam, people who practice it") and **L0:F13885/L0:F3031** (Muslim-token detectors) all the way to the *"Muslim"* embedding (de=+22.6). The "Muslim" token alone drives this branch.
- **L4:F117** ("terms related to race, racism, and social justice, with a particular focus on terms related to Black people", frac=0.012) fires on pos 6 *"justice"*, pos 7 *"warrior"*, and pos 13 *"bakery"* with a cumulative de ≈ +0.67. Its upstreams are token-identity features for *"social"*, *"justice"*, and *"warrior"* (L0:F3591, L0:F6556, L0:F9026, L1:F13646 "text discussing social justice issues") — each rooted in the corresponding embedding. The "social justice warrior" bigram is being read as a *social-justice topical concept*, not as a slur.

The only feature pointing away from the probe is **L0:F7710** ("the pronoun 'you'", pos 2, de=−0.28) — a generic grammatical feature that happens to be a non-identity lexical anchor, which slightly *suppresses* the toxicity score.

Crucially absent from the top contributors: features encoding imperative/hortative structure ("If you are …, go to …"), features encoding a recommendation or threat, features encoding mock or hostile speech acts, or any generic profanity/hate detector. The probe direction appears to align with the residual-stream subspace that lights up on "identity-group vocabulary that the model often sees in social-justice / civil-rights discourse" (note the feature labels: "race, racism, social justice", "LGBTQ+ issues", "Islam", "social justice issues"). Because this exact text contains all three such identity vocabulary items in close proximity, the probe fires strongly — regardless of the fact that the prompt uses them as targets of bigotry rather than as neutral topic markers. This is a textbook spurious-correlation failure mode: the probe has learned that sentences containing identity-group words are statistically likely to be flagged in toxicity training data, so it uses lexical identity-group presence as a proxy for the toxicity label, instead of encoding the actual hateful framing.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 17 | LGBTQ+/same-sex marriage topic feature (L8:F15771) — pos 17 'gay' | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 17 | Homosexuality/same-sex marriage feature (L6:F6085) — pos 17 'gay' |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 12 | Islam/Muslim entity feature (L6:F7282) — pos 12 'Muslim' |  mentions of Islam or Middle Eastern places and people, as well as mentions of a specific district. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 12 | Religious identity/affiliation feature (L4:F2405) — pos 12 'Muslim' |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Race/racism/social-justice entity feature (L4:F117) — pos 6, 7, 13 |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | Race/racism/social-justice entity feature (L4:F117) — pos 6, 7, 13 |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 13 | Race/racism/social-justice entity feature (L4:F117) — pos 6, 7, 13 |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F8645](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) | 17 | Gay-token identity features (L4:F8645, L4:F15899) — pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 17 | Gay-token identity features (L4:F8645, L4:F15899) — pos 17 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L3:F12024](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) | 12 | Muslim-token identity features (L3:F12024, L3:F13061) — pos 12, 13 |  words referencing the religion of Islam, people who practice it, and Arabic names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 13 | Muslim-token identity features (L3:F12024, L3:F13061) — pos 12, 13 |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 6 | Social-justice text feature (L1:F13646) — pos 6 |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 7 | Warrior-token identity feature (L0:F9026) — pos 7 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F3591](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) | 6 | Social-token / 'things done' context (L0:F3591) — pos 6 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) |
| [L0:F6556](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6556) | 6 | Justice-token feature (L0:F6556) — pos 6 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6556) |
| [L0:F13885](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) | 12 | Muslim-token identity feature (L0:F13885, L0:F3031) — pos 12 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) |
| [L0:F3031](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3031) | 12 | Muslim-token identity feature (L0:F13885, L0:F3031) — pos 12 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3031) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 2 | Pronoun 'you' feature (L0:F7710) — pos 2 (suppresses probe) | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:6085 de=0.326 |
| 3 | `inspect_feature` ×18 | L6:6085, L0:7710, L8:15771, L4:117, L6:7282, L0:6764, L4:2405, L0:3215, L0:10421, L3:5157, L3:12024, L0:7519, L0:8497, L6:10969, L11:1291, L3:5959, L3:13061, L1:13646 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F6085@17` | ❌ error | — | — | Trace the L6:F6085 (homosexuality/same-sex marriage feature firing on pos 17 'ga… |
| SA-2 | `L4:F117@6` | ❌ error | — | — | Trace L4:F117 (race/social justice feature firing on pos 6 'justice') back throu… |
| SA-3 | `L8:F15771@17` | ❌ error | — | — | Trace L8:F15771 (LGBTQ+ discussion feature firing on pos 17 'gay') back through … |
| SA-4 | `L0:F7710@2` | ❌ error | — | — | Trace L0:F7710 (the pronoun 'you' feature firing on pos 2 'you') back. Note that… |
| SA-5 | `L6:F7282@12` | ❌ error | — | — | Trace L6:F7282 (Islam/Muslim feature firing on pos 12 'Muslim') back through the… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F6085@17, k=10 → Emb:" gay"@17 (de=37.00) +9 more |
| 2 | `get_upstream_features` | L8:F15771@17, k=10 → Emb:" gay"@17 (de=17.00) +9 more |
| 3 | `get_upstream_features` | L4:F117@6, k=10 → Emb:" justice"@6 (de=5.12) +9 more |
| 4 | `get_upstream_features` | L6:F7282@12, k=10 → Emb:" Muslim"@12 (de=22.62) +9 more |
| 5 | `get_upstream_features` | L4:F2405@12, k=10 → Emb:" Muslim"@12 (de=15.75) +9 more |
| 6 | `get_upstream_features` | L11:F1291@7, k=10 → L8:F16036 (de=4.00) +9 more |
| 7 | `get_upstream_features` | L3:F13061@13, k=8 → Emb:" Muslim"@12 (de=8.06) +7 more |
| 8 | `get_upstream_features` | L6:F10969@7, k=8 → Emb:" warrior"@7 (de=2.42) +7 more |
| 9 | `get_upstream_features` | L4:F8645@17, k=8 → Emb:" gay"@17 (de=22.88) +7 more |
| 10 | `get_upstream_features` | L4:F15899@17, k=8 → Emb:" gay"@17 (de=21.12) +7 more |
| 11 | `get_upstream_features` | L0:F3591@6, k=8 → Emb:" social"@5 (de=21.00) +7 more |
| 12 | `get_upstream_features` | L0:F13885@12, k=5 → Emb:" Muslim"@12 (de=10.38) +4 more |
| 13 | `get_upstream_features` | L0:F6556@6, k=5 → Emb:" justice"@6 (de=16.88) +4 more |
| 14 | `get_upstream_features` | L4:F117@7, k=8 → Emb:" justice"@6 (de=4.12) +7 more |
| 15 | `get_upstream_features` | L4:F117@13, k=8 → Emb:" Muslim"@12 (de=5.25) +7 more |
| 16 | `get_upstream_features` | L7:F8154@7, k=5 → L6:F2674 (de=6.16) +4 more |
| 17 | `get_upstream_features` | L6:F2674@7, k=5 → Emb:" social"@5 (de=2.12) +4 more |
| 18 | `get_upstream_features` | L8:F16036@7, k=5 → L7:F8154 (de=2.61) +4 more |
| 19 | `get_upstream_features` | L2:F4124@17, k=5 → Emb:" gay"@17 (de=19.38) +4 more |
| 20 | `get_upstream_features` | L4:F10459@7, k=5 → Emb:" justice"@6 (de=1.61) +4 more |
| 21 | `get_upstream_features` | L4:F11323@7, k=5 → Emb:" warrior"@7 (de=3.61) +4 more |
| 22 | `get_upstream_features` | L4:F12425@7, k=5 → Emb:" social"@5 (de=3.81) +4 more |
| 23 | `get_upstream_features` | L5:F14124@7, k=5 → Emb:" warrior"@7 (de=3.41) +4 more |
| 24 | `get_upstream_features` | L0:F9026@7, k=5 → Emb:" warrior"@7 (de=26.50) +4 more |
| 25 | `get_upstream_features` | L0:F3031@12, k=5 → Emb:" Muslim"@12 (de=17.62) +4 more |
| 26 | `get_upstream_features` | L3:F8342@7, k=5 → Emb:" justice"@6 (de=6.22) +4 more |

### Build

`build_circuit` → 19 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 53,894 | 6,257 | 233,660 | 0 | $0.0377 | — | — |
| **Total** | | **53,894** | **6,257** | **233,660** | **0** | **$0.0377** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 16s