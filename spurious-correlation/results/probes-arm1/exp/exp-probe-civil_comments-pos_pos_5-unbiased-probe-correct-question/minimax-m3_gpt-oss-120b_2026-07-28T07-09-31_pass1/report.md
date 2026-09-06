# Circuit Oracle Report
**Date:** 2026-07-28 07:09:31 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity/identity-attack score is driven primarily by a cluster of mid-layer features that fire on the *identity-group* words "social justice warrior" — specifically the L1 social-justice text detector (13646), L2 political/social-issues language (1537), L3 social-science reference (1526), and L2 role/identity detector for "warrior" (13877), all sourced from the token embeddings of "social", "justice", and "warrior" — together with the L6 political/ideological content-with-negative-connotation feature (2674), which is fed by a stack of L4–L5 features (L4:117 race/social-justice vocabulary, L4:10459 political-movement language, L5:14124 opinionated political discourse) that were *not* trained to fire on this prompt but happen to activate on "warrior"/"justice" because those words are lexical neighbors of identity-politics vocabulary. The probe essentially never reads the actual toxic content of the sentence ("Muslim bakery", "gay wedding cake", "order a … cake") — those tokens are absent from the upstream graph; the L6 dessert feature (9005) on "bakery" actively *suppresses* the score, and the L3 "I'm a" feature, the L0 "you" pronoun, the L0 "to"/"order"/"legal"/"ownership" features all push *against* the probe, with no path reaching "Muslim", "gay", "wedding", or "cake" with positive direct_effect. The classification is therefore a spurious "identity-group" shortcut, not a content-based reading of the insult.

**Confidence:** 8

**Reasoning:** The top-20 features driving the probe split cleanly into two camps. Toward the probe (positive direct_effect): L3:16254 "conditional clauses" (+0.104) and the L2/L3 social-justice / political-movement / social-science chain — L2:1537 social-and-political-issues (0.066, fed by "social" and "justice" embeddings at +5.9/+2.7), L3:1526 social-science references (+0.072, fed by the same embeddings via the L0:3591 government-social-programs hub), L2:13877 role/identity words (+0.066, fed directly by the "warrior" embedding at +7.7 and indirectly through L0:4327 authority/role nouns at +0.76), L6:2674 political/ideological-negative-content (+0.067, fed at pos7 "warrior" by a fan-in of L4:117 race-and-social-justice vocabulary +1.5, L4:10459 political-movement language +1.5, L4:11323 political-blog discourse +1.3, L4:12425 environmentalism +1.2, and L5:14124 strong-opinionated-political-discourse +1.9, whose own inputs are L4:6752 victimhood/social-criticism +0.46 and L4:11526 political-military-conflict +0.36), and finally small generic pushes from L2:14209 "go to" (0.069), L3:16254 (0.104), L0:3850 punctuation (0.072), L0:13310 "are" (0.085) and L0:9934 "particular" (0.099). Away from the probe (negative direct_effect): L0:8444 "to" (−0.224), L0:7710 "you" (−0.154), L0:4478 ownership/belief (−0.092), L0:13756 "order" (−0.084), L0:2260 medical/legal/social-work (−0.073), L0:9602 "emphasis" (−0.064), L4:13700 "if"-conditional-business (−0.065), L6:9005 desserts (−0.113 on "bakery"), and L3:10868 "I'm a" (−0.155) — i.e., function words and the *content* of the actual sentence. Crucially, the embeddings for "Muslim" (pos 12), "gay" (pos 17), "wedding" (pos 18), and "cake" (pos 19) are essentially absent from any positive-contribution path; "bakery" and "Muslim" only appear in the upstream of L6:9005 (the *dessert* feature, which pushes away from the probe). The probe reads the noun phrase "social justice warrior" as the signal — a stereotyped identity label — and ignores the targeted slur. This is exactly the "spurious identity-group cue" failure mode the user suspected: the high-firing features (L0:3591, L1:13646, L4:117, L4:10459, L5:14124) are all *trained* on social-justice / race / political-movement text, so when "warrior" follows "social justice" the entire pipeline lights up, and the probe — being a linear classifier over the residual stream — inherits that misfire.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L3:F10868](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) | 4 | L3:10868 — phrase 'I'm a' / 'I am a' (pos4) — -0.155, neg toward probe |  the phrase "I'm a" or "I am a" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) |
| [L3:F16254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) | 8 | L3:16254 — conditional clauses (pos8 ',') — 0.104 toward probe |  conditional statements followed by actions the speaker will take | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) |
| [L2:F14209](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) | 9 | L2:14209 — 'go to' (pos9 'go') — 0.069 toward probe | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) |
| [L2:F1537](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1537) | 6 | L2:1537 — political/social-issues and movement language (pos6) — feeds L3:1526 |  words and phrases related to political and social issues and movements | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1537) |
| [L3:F1526](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) | 6 | L3:1526 — social-science / academic discipline references (pos6) — 0.072 toward probe |  references to academic disciplines related to social science | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) |
| [L2:F13877](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13877) | 7 | L2:13877 — role/identity words ('warrior') (pos7) — 0.066 toward probe | words related to roles, ranks, or personal characteristics of people | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13877) |
| [L6:F2674](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) | 7 | L6:2674 — political/ideological content w/ negative connotation (pos7) — 0.067 toward probe |  political or ideological content, particularly with negative connotations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) |
| [L6:F9005](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) | 13 | L6:9005 — dessert/lexical 'cake' (pos13) — -0.113 away from probe |  words and phrases related to desserts | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | L4:117 — race / racism / social-justice vocabulary, esp. Black (pos7) — 1.5 toward L6:2674 |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F10459](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10459) | 7 | L4:10459 — political parties / movements (pos7) — 1.52 toward L6:2674 |  words related to politics, especially political parties and movements like the Tea Party. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10459) |
| [L4:F11323](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11323) | 7 | L4:11323 — political/fashion blog discourse (pos7) — 1.34 toward L6:2674 |  text from blog posts about political and fashion topics. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11323) |
| [L5:F14124](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14124) | 7 | L5:14124 — strong opinionated political discourse (pos7) — 1.93 toward L6:2674 |  things that indicate strong and opinionated political discourse | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14124) |
| [L4:F6752](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6752) | 7 | L4:6752 — victimhood / social criticism (pos7) — 0.46 toward L5:14124 |  phrases expressing victimhood and social criticism | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6752) |
| [L4:F11526](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11526) | 7 | L4:11526 — political/military conflict words (pos7) — 0.36 toward L5:14124 |  words and short phrases related to political and military conflict | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11526) |
| [L4:F12425](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12425) | 7 | L4:12425 — environmentalism / green advocacy (pos7) — 1.23 toward L6:2674 (off-topic) |  words and phrases related to environmental consciousness, sustainability, and "green" business practices | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12425) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 6 | L1:13646 — social-justice text (pos6) — +1.12 to L4:117, +0.61 to L4:11323 |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L0:F3591](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) | 6 | L0:3591 — government social-programs (pos6 'justice') — hub feeding many downstream |  terms related to government social programs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) |
| [L0:F4327](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4327) | 7 | L0:4327 — authority/role nouns (pos7 'warrior') — 0.76 to L2:13877 |  terms related to people in positions of authority and/or roles in an organization | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4327) |
| [L0:F9934](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) | 6 | L0:9934 — the word 'particular' (pos6) — 0.099 toward probe |  the word "particular" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 10 | L0:8444 — the word 'to' (pos10) — -0.224 away from probe | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 2 | L0:7710 — pronoun 'you' (pos2) — -0.154 away from probe | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F13310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) | 3 | L0:13310 — 'are' (pos3) — +0.085 toward probe |  sentences that include forms of the verb "are" indicating a present state of being or necessity. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) |
| [L0:F13756](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) | 15 | L0:13756 — the word 'order' (pos15) — -0.084 away from probe |  the word "order" and occasionally "period," in many different contexts from law to food | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) |
| [L0:F2260](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) | 6 | L0:2260 — medical/legal/social-work terms (pos6) — -0.073 away from probe |  terms that are medical, legal, or related to social work | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) |
| [L0:F9602](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) | 6 | L0:9602 — the word 'emphasis' (pos6) — -0.064 away from probe |  the word "emphasis." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) |
| [L0:F4478](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) | 6 | L0:4478 — ownership/belief terms (pos6) — -0.092 away from probe |  terms related to ownership and belief systems. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) |
| [L0:F3850](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) | 8 | L0:3850 — punctuation marks (pos8) — 0.072 toward probe | punctuation marks | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) |
| [L4:F13700](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13700) | 8 | L4:13700 — 'if'-conditional business contexts (pos8) — -0.065 away from probe | conditional clauses starting with "if" and words related to business contexts | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13700) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:8444 de=-0.224 |
| 3 | `inspect_feature` ×6 | L0:8444, L0:7710, L3:10868, L6:9005, L3:16254, L0:9934 |
| 4 | `get_upstream_features` | Emb:" a"@4 (de=18.62) +9 more |
| 5 | `get_upstream_features` | Emb:"If"@1 (de=9.88) +9 more |
| 6 | `get_upstream_features` | Emb:"If"@1 (de=7.66) +9 more |
| 7 | `get_upstream_features` | Emb:" go"@9 (de=18.38) +9 more |
| 8 | `get_upstream_features` | Emb:" warrior"@7 (de=7.72) +9 more |
| 9 | `get_upstream_features` | Emb:" social"@5 (de=2.12) +9 more |
| 10 | `get_upstream_features` | Emb:" bakery"@13 (de=22.38) +9 more |
| 11 | `inspect_feature` ×10 | L4:13700, L3:1526, L0:3850, L0:4478, L0:13310, L0:13756, L0:2260, L1:14281, L0:9602, L0:3591 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F7710@2` | ❌ error | — | — | Trace this L0 'you' pronoun feature to understand how it contributes to the prob… |
| SA-2 | `L2:F13877@7` | ✅ reported | 4 | 3 | Trace L2:13877 at pos 7 ('warrior') to determine what group/identity signal it p… |
| SA-3 | `L3:F1526@6` | ✅ reported | 6 | 10 | Trace L3:1526 'social science' feature to understand how it contributes to the c… |
| SA-4 | `L6:F2674@7` | ❌ error | — | — | Trace L6:2674 from pos 7 ('warrior') to understand its role in the circuit. |

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13877 | " words related to roles, ranks, or personal characteristics of people" |
| 2 | `get_upstream_features` | L2:F13877@7, k=15 | Emb:" warrior"@7 (de=7.72) +14 more |
| 3 | `inspect_feature` | L0, F4327 | " terms related to people in positions of authority and/or roles in an " |
| 4 | `get_upstream_features` | L0:F4327@7, k=10 | Emb:" warrior"@7 (de=5.03) +9 more |
| 5 | `inspect_feature` | L0, F15442 | " words denoting people with professions or titles" |
| 6 | `inspect_feature` | L1, F10447 | "articles and prepositions" |
| 7 | `get_upstream_features` | L0:F15442@7, k=10 | Emb:" warrior"@7 (de=8.94) +9 more |
| 8 | `inspect_feature` | L0, F11154 | " the word "are"" |
| 9 | `get_upstream_features` | L1:F10447@4, k=10 | Emb:" a"@4 (de=16.62) +9 more |

**Findings:** The L2:13877 feature that the probe queries is a role/identity detector. Its strongest upstream driver is the raw token embedding for the word 'warrior' (direct effect ≈7.7). This signal is funneled through two low‑layer (layer 0) role‑related features – 4327 and 15442 – both of which are highly sparse and specialize in detecting occupation‑type words. A smaller contribution also arrives from a ge…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F1526 | " references to academic disciplines related to social science" |
| 2 | `get_upstream_features` | L3:F1526@6, k=10 | Emb:" social"@5 (de=9.62) +9 more |
| 3 | `inspect_feature` | L2, F1537 | " words and phrases related to political and social issues and movement" |
| 4 | `get_upstream_features` | L2:F1537@6, k=10 | Emb:" social"@5 (de=5.91) +9 more |
| 5 | `inspect_feature` | L0, F3591 | " terms related to government social programs" |
| 6 | `get_upstream_features` | L0:F3591@6, k=10 | Emb:" social"@5 (de=21.00) +9 more |
| 7 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** The L3:1526 feature flags references to social‑science disciplines. Its strongest positive drivers are the raw token embeddings for "social" (pos5) and "justice" (pos6), which cascade through a mid‑level political‑issues detector (L2:1537) and a low‑level government‑program detector (L0:3591). All three layers are within the lower third of the model (≤8), satisfying the termination condition, and …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F7710@2, k=10 → Emb:" you"@2 (de=40.50) +9 more |
| 2 | `get_upstream_features` | L6:F2674@7, k=10 → Emb:" social"@5 (de=2.12) +9 more |
| 3 | `get_upstream_features` | L4:F10459@7, k=10 → Emb:" justice"@6 (de=1.61) +9 more |
| 4 | `get_upstream_features` | L5:F14124@7, k=10 → Emb:" warrior"@7 (de=3.41) +9 more |
| 5 | `get_upstream_features` | L2:F13877@7, k=10 → Emb:" warrior"@7 (de=7.72) +9 more |
| 6 | `inspect_feature` ×7 | L0:4327, L4:10459, L5:14124, L4:11323, L4:117, L4:12425, L4:1602 |
| 7 | `get_upstream_features` | L2:F1537@6, k=10 → Emb:" social"@5 (de=5.91) +9 more |
| 8 | `get_upstream_features` | L0:F4327@7, k=10 → Emb:" warrior"@7 (de=5.03) +9 more |
| 9 | `get_upstream_features` | L4:F117@7, k=10 → Emb:" justice"@6 (de=4.12) +9 more |
| 10 | `get_upstream_features` | L4:F12425@7, k=10 → Emb:" social"@5 (de=3.81) +9 more |
| 11 | `get_upstream_features` | L4:F1602@7, k=10 → Emb:" warrior"@7 (de=4.12) +9 more |
| 12 | `get_upstream_features` | L4:F11323@7, k=10 → Emb:" warrior"@7 (de=3.61) +9 more |
| 13 | `inspect_feature` ×4 | L2:1537, L1:13646, L3:8342, L6:9005 |
| 14 | `get_upstream_features` | L5:F14124@7, k=10 → Emb:" warrior"@7 (de=3.41) +9 more |
| 15 | `get_upstream_features` | L4:F11323@7, k=10 → Emb:" warrior"@7 (de=3.61) +9 more |
| 16 | `get_upstream_features` | L3:F16254@8, k=10 → Emb:"If"@1 (de=9.88) +9 more |
| 17 | `get_upstream_features` | L2:F14209@9, k=10 → Emb:" go"@9 (de=18.38) +9 more |
| 18 | `inspect_feature` ×10 | L6:2674, L4:11526, L4:6752, L4:11211, L3:7746, L2:12652, L2:696, L1:13592, L4:9008, L0:2303 |
| 19 | `get_upstream_features` | L0:F13310@3, k=10 → Emb:" you"@2 (de=10.50) +9 more |
| 20 | `inspect_feature` ×3 | L1:3604, L0:3215, L0:8497 |
| 21 | `get_upstream_features` | L1:F10447@4, k=10 → Emb:" a"@4 (de=16.62) +9 more |

### Build

`build_circuit` → 49 nodes, 55 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 95,721 | 10,076 | 575,151 | 0 | $0.0753 | — | — |
| SA-3 | openai/gpt-oss-120b | 51,340 | 5,070 | 13,344 | 0 | $0.0109 | ✅ 6F/10E | Trace L3:1526 'social science' feature to understand how it … |
| SA-2 | openai/gpt-oss-120b | 89,709 | 6,590 | 24,384 | 0 | $0.0178 | ✅ 4F/3E | Trace L2:13877 at pos 7 ('warrior') to determine what group/… |
| **Total** | | **236,770** | **21,736** | **612,879** | **0** | **$0.1040** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 33s