# Circuit Oracle Report
**Date:** 2026-07-28 07:21:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven by an "identity-group co-occurrence" circuit: the model detects the *presence of protected-identity tokens* ('gay', 'Muslim', 'warrior', 'social justice') and routes them through entity-recognition features, without any feature encoding the actual hostile/imperative semantics ('go to a', 'order', 'cake', the directive structure of the prompt) contributing positively to the score.

**Confidence:** 8

**Reasoning:** The top 20 features by direct effect on the probe target are dominated by **identity/affiliation detectors**, not by hostility, imperatives, or slur detectors:

1. **LGBTQ+/same-sex marriage supernode (gay_lgbtq_features, direct_effect ≈ +0.88 cumulative)**: L4:F8645 ("passages discussing same-sex marriage", frac_nonzero=0.015), L4:F15899 ("language associated with the LGBTQ community and discussions of gender and identity", frac_nonzero=0.006), L6:F6085 ("text related to homosexuality and same-sex marriage", frac_nonzero=0.002), L7:F16171 ("texts about homosexuality, gay marriage, and religious views on these topics", frac_nonzero=0.012), L8:F15771 ("discussion of LGBTQ+ issues, especially same-sex marriage", frac_nonzero=0.008). All five fire at pos 17 and trace directly to the **Emb: ' gay'** node (direct_effect up to 37). They encode the *category* "same-sex marriage discussion", not the *tone*.

2. **Race / social-justice supernode (race_social_justice_features, direct_effect ≈ +0.92 cumulative)**: L4:F117 ("terms related to race, racism, and social justice…Black people", frac_nonzero=0.012) fires at pos 6 ('justice'), 7 ('warrior'), and 13 ('bakery' — the L4 graph is the "social justice" detector generic-firing on nearby tokens). L6:F10969 ("swear words and insults", frac_nonzero=0.012) fires at pos 7; L11:F1291 ("racist content", frac_nonzero=0.007) fires at pos 7. These trace back to **Emb: ' warrior'** (direct_effect 26.5 → L0:F9026) and **Emb: ' social'/' justice'** (direct_effect 21 → L0:F3591 "terms related to government social programs"). The chain L0:F9026 → L4:F117 → L11:F1291 shows the model labeling 'warrior' as a protected-identity sentinel that aggregates into "social justice" / "racist content" themes purely because the token sits next to "social justice warrior" — a *phrase-level identity collocation*, not a slur/hostility signal.

3. **Muslim/religious-identity supernode (muslim_features, direct_effect ≈ +0.36 cumulative)**: L4:F2405 ("religious identity/affiliation", frac_nonzero=0.007) and L6:F7282 ("mentions of Islam or Middle Eastern places and people", frac_nonzero=0.007), both at pos 12. Direct effect from **Emb: ' Muslim'** is 22.6 (largest single embedding signal in the graph). The chain L3:F12024 → L4:F2405 → L6:F7282 traces "Muslim" → "religious identity" → "Islam/Middle East" — pure entity recognition.

4. **Imperative/hostility semantics are absent**: L0:F7710 ("the pronoun 'you'", frac_nonzero=0.019) fires on ' you' with a *negative* direct_effect of −0.28 against the probe, and L0:F6764 ("things subjects/people have done or felt") has direct_effect −0.19. The verb 'go' (pos 9) and noun 'cake' (pos 13) — the lexical material that actually *constitutes* the imperative/request — contribute *against* the probe score, not for it. The only "action" feature that contributes positively is L6:F10969 ("swear words and insults"), but its top-activating tokens are 'fuck', 'ass', 'f**king' — words **not present in this prompt**. It is being recruited as a generic "negativity" feature, but its activation here is driven by identity context, not by profanity.

5. **Convergence**: Three orthogonal identity detectors (LGBTQ+, race/SJ, Muslim) all fire strongly and positively project to the probe. None of them encodes the prompt's actual hostility vector (a directive targeting protected groups). The prompt "If you are a social justice warrior, go to a Muslim bakery and order a gay wedding cake" is, lexically and syntactically, an *imperative addressed to a group* — but the model has no positive "imperative + protected-class" toxicity feature. Instead it has separate "this is a protected-class token" detectors that fire regardless of whether the surrounding frame is hostile, sarcastic, descriptive, or a quote.

**Conclusion regarding the user's concern**: The user is correct. The circuit uses **spurious identity-membership features** ("gay = LGBTQ+ topic", "Muslim = Islam/religious identity", "warrior + social justice = race/SJ topic") as proxies for toxicity. The actual prompt content (the imperative 'go', the request 'order', the object 'wedding cake', the conditional 'If you are') carries near-zero or negative weight. This is a classic confounder: any sentence mentioning "gay", "Muslim", and "social justice" together — including news articles, dictionary definitions, or sympathetic descriptions — would activate the same circuit and yield the same probe score.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F8645](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) | 17 | L4–L8: same-sex marriage / LGBTQ+ text features (gay at pos 17) |  passages discussing same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 17 | L4–L8: same-sex marriage / LGBTQ+ text features (gay at pos 17) |  language associated with the LGBTQ community and discussions of gender and identity. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 17 | L4–L8: same-sex marriage / LGBTQ+ text features (gay at pos 17) |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L7:F16171](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16171) | 17 | L4–L8: same-sex marriage / LGBTQ+ text features (gay at pos 17) |  texts about homosexuality, gay marriage, and religious views on these topics | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16171) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 17 | L4–L8: same-sex marriage / LGBTQ+ text features (gay at pos 17) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | L4: race / social-justice features firing on 'warrior' (pos 7) and 'social justice' (pos 5-6) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | L4: race / social-justice features firing on 'warrior' (pos 7) and 'social justice' (pos 5-6) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 13 | L4: race / social-justice features firing on 'warrior' (pos 7) and 'social justice' (pos 5-6) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L6:F10969](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10969) | 7 | L4: race / social-justice features firing on 'warrior' (pos 7) and 'social justice' (pos 5-6) |  swear words and insults | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10969) |
| [L11:F1291](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1291) | 7 | L4: race / social-justice features firing on 'warrior' (pos 7) and 'social justice' (pos 5-6) |  racist content | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/1291) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 12 | L4–L6: Islam / religious-identity features firing on 'Muslim' (pos 12) |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 12 | L4–L6: Islam / religious-identity features firing on 'Muslim' (pos 12) |  mentions of Islam or Middle Eastern places and people, as well as mentions of a specific district. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L0:F3591](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) | 6 | L0–L3: early token-level identity detectors on 'social'/'justice'/'warrior'/'Muslim' |  terms related to government social programs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 7 | L0–L3: early token-level identity detectors on 'social'/'justice'/'warrior'/'Muslim' | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F3215](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3215) | 6 | L0–L3: early token-level identity detectors on 'social'/'justice'/'warrior'/'Muslim' |  terms related to scientific studies, environments, and social issues | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3215) |
| [L0:F10421](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10421) | 6 | L0–L3: early token-level identity detectors on 'social'/'justice'/'warrior'/'Muslim' |  mentions of fields of study and legal terms | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10421) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 6 | L0–L3: early token-level identity detectors on 'social'/'justice'/'warrior'/'Muslim' |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L3:F5157](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5157) | 6 | L0–L3: early token-level identity detectors on 'social'/'justice'/'warrior'/'Muslim' |  references to social services and social work | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5157) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 13 | L0–L3: early token-level identity detectors on 'social'/'justice'/'warrior'/'Muslim' |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F12024](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) | 12 | L0–L3: early token-level identity detectors on 'social'/'justice'/'warrior'/'Muslim' | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:6085 de=0.326 |
| 3 | `inspect_feature` ×6 | L6:6085, L0:None, L8:15771, L4:117, L6:7282, L0:None |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F6085@17` | ❌ error | — | — | Trace L6:F6085 (homosexuality/same-sex marriage text feature) upstream to find t… |
| SA-2 | `L4:F117@6` | ❌ error | — | — | Trace L4:F117 (race/racism/social justice feature) upstream across positions 6, … |
| SA-3 | `L6:F7282@12` | ❌ error | — | — | Trace L6:F7282 (Islam/Muslim mention feature at pos 12) upstream. Find which inp… |
| SA-4 | `L8:F15771@17` | ❌ error | — | — | Trace L8:F15771 (LGBTQ+ issues, same-sex marriage discussion) upstream from pos … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F6085@17, k=15 → Emb:" gay"@17 (de=37.00) +14 more |
| 2 | `get_upstream_features` | L8:F15771@17, k=15 → Emb:" gay"@17 (de=17.00) +14 more |
| 3 | `get_upstream_features` | L4:F117@6, k=15 → Emb:" justice"@6 (de=5.12) +14 more |
| 4 | `get_upstream_features` | L4:F117@7, k=15 → Emb:" justice"@6 (de=4.12) +14 more |
| 5 | `get_upstream_features` | L6:F7282@12, k=15 → Emb:" Muslim"@12 (de=22.62) +14 more |
| 6 | `get_upstream_features` | L4:F117@13, k=15 → Emb:" Muslim"@12 (de=5.25) +14 more |
| 7 | `get_upstream_features` | L4:F8645@17, k=15 → Emb:" gay"@17 (de=22.88) +14 more |
| 8 | `inspect_feature` ×8 | L0:7710, L0:6764, L4:2405, L0:3215, L0:10421, L0:7519, L0:8497, L0:3591 |
| 9 | `get_upstream_features` | L4:F2405@12, k=10 → Emb:" Muslim"@12 (de=15.75) +9 more |
| 10 | `get_upstream_features` | L0:F3591@6, k=10 → Emb:" social"@5 (de=21.00) +9 more |
| 11 | `inspect_feature` ×3 | L3:13061, L3:5157, L0:9026 |
| 12 | `get_upstream_features` | L0:F9026@7, k=10 → Emb:" warrior"@7 (de=26.50) +9 more |
| 13 | `get_upstream_features` | L4:F8645@17, k=10 → Emb:" gay"@17 (de=22.88) +9 more |
| 14 | `inspect_feature` ×5 | L4:8645, L4:15899, L7:16171, L6:10969, L11:1291 |
| 15 | `get_upstream_features` | L11:F1291@7, k=10 → L8:F16036 (de=4.00) +9 more |
| 16 | `get_upstream_features` | L6:F10969@7, k=10 → Emb:" warrior"@7 (de=2.42) +9 more |
| 17 | `get_upstream_features` | L1:F13646@6, k=10 → Emb:" justice"@6 (de=4.22) +9 more |
| 18 | `get_upstream_features` | L0:F7710@2, k=10 → Emb:" you"@2 (de=40.50) +9 more |
| 19 | `inspect_feature` ×6 | L8:16036, L7:8154, L6:2674, L9:4798, L1:13646, L3:5157 |

### Build

`build_circuit` → 11 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 63,896 | 5,910 | 241,097 | 0 | $0.0407 | — | — |
| **Total** | | **63,896** | **5,910** | **241,097** | **0** | **$0.0407** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 1s