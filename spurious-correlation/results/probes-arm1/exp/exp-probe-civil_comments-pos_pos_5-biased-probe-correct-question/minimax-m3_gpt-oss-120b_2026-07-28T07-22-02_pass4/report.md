# Circuit Oracle Report
**Date:** 2026-07-28 07:22:02 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit has reached embedding nodes for the key identity tokens. Building the final analysis.

**Analysis:** The probe's toxicity score is driven by four parallel feature paths that each fire on the *named identity groups* in the prompt (gay, Muslim, social-justice, "warrior") rather than on the prompt's actual toxic content (the call to harass a bakery).

**Confidence:** 7

**Reasoning:** The attribution graph decomposes cleanly into four circuit paths that converge on the probe output:

1. **LGBTQ path (pos 17 "gay"):** `Emb: ' gay'` → L4:8645 (same-sex marriage passages, frac 0.015) and L6:6085 (homosexuality/same-sex marriage, frac 0.0017, very specific) → L8:15771 (LGBTQ+ issues, frac 0.0078) → probe. The dominant upstream signal is the raw "gay" embedding with direct_effect=37 onto L6:6085. The feature is purely a *topic detector* for LGBTQ content — its top activating examples are neutral news passages about same-sex marriage legislation. It carries no signal about whether the surrounding sentence is hateful.

2. **Islam path (pos 12 "Muslim"):** `Emb: ' Muslim'` (direct_effect=22.6) → L6:7282 (Islam/Middle East, frac 0.007) → probe. Again, this is a religious-identity topic feature, not a toxicity feature. Its top examples are about mosques, Muslim conquest, and Ottoman history.

3. **Race/social-justice path (pos 5-7 "social justice warrior"):** `Emb: ' social'` + `Emb: ' justice'` → L0:3591 (government social programs) + L1:13646 (identity category) + L3:5157 (social services) → L4:117 (race/racism/social-justice terms, frac 0.012) → probe. L4:117 fires on the literal words "social" and "justice" and propagates a race/discrimination frame. Its promoted tokens are explicitly "racist / racism / racial" — so encountering the *phrase* "social justice" alone injects a racism signal, independent of any actual racist content in the text.

4. **"Warrior" path (pos 7 "warrior"):** `Emb: ' warrior'` → L6:2674 (political/ideological content, neg. connotation) → L7:8154 (right-wing political commentary) → L8:16036 (Israel/Zionism — apparently an idiosyncratic association of "warrior" in the training corpus) → L9:4798 (racial issues / slavery) → L11:1291 (racist content, frac 0.007) → probe. This is the closest path to a "real" toxicity feature, but even here L11:1291's top activating examples include neutral phrases like "indoctrinated" and "false rape accusations" — it fires on racial-discourse vocabulary, not on hateful intent.

The user's concern is well-supported by the circuit. The probe is essentially aggregating four independent *identity-topic detectors* (LGBTQ, Muslim, social-justice, right-wing/political), each of which fires on the mere mention of a protected/adversarial group name. None of the four paths pass through features that encode the prompt's actual semantic content — the imperative "go to a Muslim bakery and order a gay wedding cake" never reaches any hate-speech, threat, or harassment detector. The model classifies the prompt as toxic because the input contains the *names* of stereotyped identity groups co-occurring, not because it parsed the directive structure. This is a textbook spurious-correlation failure: the probe has learned "identity-group vocabulary ≈ toxic" rather than "harmful directive ≈ toxic." Note that the strongly negative direct effects (L0:7710 "you" at -0.28, L0:6764 experiences at -0.19, L0:3215 social issues at -0.165, L0:8497 "go" at -0.126) partially reflect inhibition from the surrounding imperative scaffolding, but they do not flow through any feature that counters the identity-driven signal at the probe output — by layer 26 the positive identity-group contributions dominate.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 17 | Emb: ' gay' (pos 17) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' Muslim' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' justice' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' social' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' warrior' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F3591](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) | 6 | L0:3591 - 'government social programs' (pos 6) |  terms related to government social programs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 6 | L1:13646 - identity/social category (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L3:F5157](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5157) | 6 | L3:5157 - social services / social work (pos 6) |  references to social services and social work | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5157) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 13 | L3:13061 - race/gender/social-issues vocabulary (pos 13 'bakery', pos 12) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F12024](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) | 12 | L3:13061 - race/gender/social-issues vocabulary (pos 13 'bakery', pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | L4:117 - race/racism/social-justice terms (pos 6,7,13) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | L4:117 - race/racism/social-justice terms (pos 6,7,13) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 13 | L4:117 - race/racism/social-justice terms (pos 6,7,13) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 12 | L4:2405 - religious identity/spirituality (pos 12) |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L4:F8645](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) | 17 | L4:8645 - same-sex marriage passages (pos 17) |  passages discussing same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 17 | L6:6085 - homosexuality / same-sex marriage (pos 17) |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 12 | L6:7282 - Islam / Muslim / Middle East (pos 12) |  mentions of Islam or Middle Eastern places and people, as well as mentions of a specific district. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L6:F2674](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) | 7 | L6:2674 - political/ideological content, neg. connotation (pos 7) |  political or ideological content, particularly with negative connotations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) |
| [L7:F8154](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8154) | 7 | L7:8154 - right-wing political commentary (pos 7) |  highly charged political commentary, particularly with a right-leaning perspective | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8154) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 17 | L8:15771 - LGBTQ+ issues / same-sex marriage (pos 17) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L8:F16036](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16036) | 7 | L8:16036 - Israel/Zionism/political-state references (pos 7) |  words and phrases related to Israel, Zionism, and related political topics. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16036) |
| [L9:F4798](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/4798) | 7 | L9:4798 - racial issues / slavery / discrimination (pos 7) |  references to racial issues, particularly slavery and discrimination | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/4798) |
| [L11:F1291](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1291) | 7 | L11:1291 - racist content (pos 7) |  racist content | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1291) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe output (toxicity direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:6085 de=0.326 |
| 3 | `inspect_feature` ×11 | L6:6085, L8:15771, L4:117, L6:7282, L4:2405, L3:5157, L11:1291, L0:7710, L0:6764, L0:3215, L3:13061 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L11:F1291@7` | ❌ error | — | — | Trace the upstream path of L11:F1291 (racist content). Find what tokens and earl… |
| SA-2 | `L6:F6085@17` | ❌ error | — | — | Trace the upstream path of L6:F6085 (homosexuality / gay content). Find which to… |
| SA-3 | `L6:F7282@12` | ❌ error | — | — | Trace the upstream path of L6:F7282 (Islam/Muslim content). Find which tokens an… |
| SA-4 | `L4:F117@6` | ❌ error | — | — | Trace the upstream path of L4:F117 (race/racism social justice terms). Find whic… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L11:F1291@7, k=12 → L8:F16036 (de=4.00) +11 more |
| 2 | `get_upstream_features` | L6:F6085@17, k=12 → Emb:" gay"@17 (de=37.00) +11 more |
| 3 | `get_upstream_features` | L6:F7282@12, k=12 → Emb:" Muslim"@12 (de=22.62) +11 more |
| 4 | `get_upstream_features` | L4:F117@6, k=12 → Emb:" justice"@6 (de=5.12) +11 more |
| 5 | `inspect_feature` ×6 | L8:16036, L7:8154, L6:2674, L9:4798, L4:8645, L0:3591 |

### Build

`build_circuit` → 21 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 34,618 | 5,388 | 146,397 | 0 | $0.0256 | — | — |
| **Total** | | **34,618** | **5,388** | **146,397** | **0** | **$0.0256** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 8s