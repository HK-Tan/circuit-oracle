# Circuit Oracle Report
**Date:** 2026-07-28 07:20:41 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven primarily by a narrow "political/ideological content" detector (L6:F2674) that fires on the phrase "social justice warrior" — the probe weights the **identity-label tokens** themselves, not the actual provocative action (ordering a cake from a Muslim bakery).

**Confidence:** 7

**Reasoning:** The circuit that drives the probe's positive classification is surprisingly thin and is anchored almost entirely on the identity-words at positions 5–7 (" social", " justice", " warrior"). The strongest direct edge to the probe at the top of the graph is **L6:F2674 ("political or ideological content, particularly with negative connotations", direct_effect=+0.067 at pos 7)**, and tracing it upstream confirms it is driven by the literal token embeddings of " social" (pos 5) and " justice" (pos 6) plus " warrior" (pos 7) — its upstream chain includes the **L2:F1537 "political and social issues and movements"** feature, the **L3:F1526 "social science academic disciplines"** feature, and a stark L4:F117 "race, racism, and social justice" detector (promoted tokens: *racial, racist, racism*). Even F1526's upstream decomposition is direct: the " social" token contributes +9.6, " justice" +3.9, and a generic L0:F3591 "government social programs" feature adds another +1.78 — i.e., the *social*-prefix is being read as a sociopolitical-group marker. The comic/normative content of the prompt — the *imperative* "If you are X, go do Y" structure (positions 1–4 and 9) — is carried by generic lexical features (L2:F14209 "go", L0:F13310 "are", L0:F3850 punctuation) that contribute weakly and **do not encode harmful intent**. Most strikingly, the "actual prompt content" tokens — " Muslim" (pos 12), " bakery" (pos 13), " wedding" (14), " cake" (15) — feed almost exclusively into a single **suppressive** L6:F9005 "dessert" feature (direct_effect=−0.11), which the model has learned as a benign food/commercial context and which pushes *away* from toxicity. Identity-group words also appear in the suppressors: L0:F4478 ("sexual orientation", "religious organizations", direct_effect=−0.092) and L0:F13756 ("order" in legal/food sense) point the other way, but lose. So the probe reads "SJW" as a slur-shaped identity label and reacts to the *noun phrase*, not to the *action* "go order a cake at a Muslim bakery." This is exactly the spurious-cue pattern the user flagged: a single high-level "political/ideological content" feature (L6:F2674) plus the L4 "race/social-justice" detector (F117) function as a "contains an identity group" gate, while the actual commercial-transaction semantics ("bakery", "wedding cake", "order") are *inhibiting* the probe. The circuit substantiates the concern that the probe is using a *bag-of-identity-words* shortcut rather than evaluating the actual hateful imperative.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F2674](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) | 7 | Political/ideological discourse with negative connotations (driven by 'social justice' + 'warrior') |  political or ideological content, particularly with negative connotations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) |
| [L3:F1526](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) | 6 | 'social justice' / social-science academic discourse |  references to academic disciplines related to social science | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) |
| [L3:F16254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) | 8 | 'social justice' / social-science academic discourse |  conditional statements followed by actions the speaker will take | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) |
| [L3:F10868](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) | 4 | 'social justice' / social-science academic discourse |  the phrase "I'm a" or "I am a" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) |
| [L2:F14209](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) | 9 | Generic lexical cues: verb 'go', conditional code/then, role 'warrior' | the verb "go" in its various forms. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) |
| [L2:F14541](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) | 8 | Generic lexical cues: verb 'go', conditional code/then, role 'warrior' |  code snippets and logical statements, especially those involving "then," along with some citation markers and bracketed references. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) |
| [L2:F13877](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13877) | 7 | Generic lexical cues: verb 'go', conditional code/then, role 'warrior' |  words related to roles, ranks, or personal characteristics of people | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13877) |
| [L0:F13310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) | 3 | Generic L0 lexical: 'are', 'particular', punctuation, 'social'-related |  sentences that include forms of the verb "are" indicating a present state of being or necessity. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) |
| [L0:F9934](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) | 6 | Generic L0 lexical: 'are', 'particular', punctuation, 'social'-related |  the word "particular" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) |
| [L0:F3850](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) | 8 | Generic L0 lexical: 'are', 'particular', punctuation, 'social'-related | punctuation marks | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) |
| [L0:F3591](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) | 6 | Generic L0 lexical: 'are', 'particular', punctuation, 'social'-related |  terms related to government social programs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 10 | Suppressive L0 generic lexical ('to', 'you', 'order', 'emphasis', 'instructions') | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 2 | Suppressive L0 generic lexical ('to', 'you', 'order', 'emphasis', 'instructions') | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F13756](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) | 15 | Suppressive L0 generic lexical ('to', 'you', 'order', 'emphasis', 'instructions') |  the word "order" and occasionally "period," in many different contexts from law to food | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) |
| [L0:F9602](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) | 6 | Suppressive L0 generic lexical ('to', 'you', 'order', 'emphasis', 'instructions') |  the word "emphasis." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) |
| [L0:F2260](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) | 6 | Suppressive L0 generic lexical ('to', 'you', 'order', 'emphasis', 'instructions') |  terms that are medical, legal, or related to social work | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) |
| [L0:F4478](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) | 6 | Suppressive L0 generic lexical ('to', 'you', 'order', 'emphasis', 'instructions') |  terms related to ownership and belief systems. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) |
| [L1:F14281](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14281) | 6 | Suppressive mid-layer ('instructions', 'if/then' conditionals) |  the word "instruction" and its plural | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14281) |
| [L4:F13700](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13700) | 8 | Suppressive mid-layer ('instructions', 'if/then' conditionals) | conditional clauses starting with "if" and words related to business contexts | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13700) |
| [L6:F9005](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) | 13 | Suppressive: dessert/bakery lexical feature (dampens probe) |  words and phrases related to desserts | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:8444 de=-0.224 |
| 3 | `inspect_feature` ×20 | L0:8444, L0:7710, L3:10868, L6:9005, L3:16254, L0:9934, L0:4478, L0:13310, L0:13756, L0:2260, L0:3850, L3:1526, L2:14541, L2:14209, L6:2674, L1:14281, L2:13877, L4:13700, L0:9602, L0:3591 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F2674@7` | ❌ error | — | — | This feature (L6:F2674) is described as 'political or ideological content, parti… |
| SA-2 | `L3:F1526@6` | ✅ reported | 3 | 4 | This feature (L3:F1526) is described as 'references to academic disciplines rela… |
| SA-3 | `L0:F4478@6` | ❌ error | — | — | This feature (L0:F4478) is 'terms related to ownership and belief systems' and i… |
| SA-4 | `L3:F10868@4` | ❌ error | — | — | This feature (L3:F10868) is 'the phrase "I'm a" or "I am a"' and has +0.1348 dir… |
| SA-5 | `L6:F9005@13` | ❌ error | — | — | This feature (L6:F9005) is 'words and phrases related to desserts' — odd to be i… |

<details>
<summary><b>SA-2</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F1526 | " references to academic disciplines related to social science" |
| 2 | `get_upstream_features` | L3:F1526@6, k=10 | Emb:" social"@5 (de=9.62) +9 more |
| 3 | `inspect_feature` | L2, F1537 | " words and phrases related to political and social issues and movement" |
| 4 | `inspect_feature` | L0, F3591 | " terms related to government social programs" |
| 5 | `get_upstream_features` | L2:F1537@6, k=5 | Emb:" social"@5 (de=5.91) +4 more |

**Findings:** The L3:F1526 feature, originally described as detecting social‑science academic references, receives its strongest positive drive from the raw tokens " social" (pos 5) and " justice" (pos 6), confirming that it is indeed firing on the phrase "social justice". The upstream path includes a lower‑layer (L2) political‑issue detector (F1537) and an even earlier lexical cue detector (L0:F3591) that both…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F2674@7, k=10 → Emb:" social"@5 (de=2.12) +9 more |
| 2 | `get_upstream_features` | L0:F4478@6, k=10 → Emb:" social"@5 (de=13.31) +9 more |
| 3 | `get_upstream_features` | L3:F10868@4, k=10 → Emb:" a"@4 (de=18.62) +9 more |
| 4 | `get_upstream_features` | L6:F9005@13, k=10 → Emb:" bakery"@13 (de=22.38) +9 more |
| 5 | `get_upstream_features` | L3:F16254@8, k=10 → Emb:"If"@1 (de=9.88) +9 more |
| 6 | `get_upstream_features` | L2:F14209@9, k=8 → Emb:" go"@9 (de=18.38) +7 more |
| 7 | `get_upstream_features` | L2:F13877@7, k=8 → Emb:" warrior"@7 (de=7.72) +7 more |
| 8 | `inspect_feature` ×11 | L5:14124, L4:10459, L2:1537, L2:8867, L0:10219, L2:12652, L0:9026, L4:13041, L4:117, L4:11323, L4:12425 |
| 9 | `get_upstream_features` | L5:F14124@7, k=6 → Emb:" warrior"@7 (de=3.41) +5 more |
| 10 | `get_upstream_features` | L4:F10459@7, k=6 → Emb:" justice"@6 (de=1.61) +5 more |
| 11 | `get_upstream_features` | L4:F117@7, k=6 → Emb:" justice"@6 (de=4.12) +5 more |

### Build

`build_circuit` → 11 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 77,340 | 6,456 | 242,379 | 0 | $0.0455 | — | — |
| SA-2 | openai/gpt-oss-120b | 40,652 | 3,075 | 2,560 | 0 | $0.0080 | ✅ 3F/4E | This feature (L3:F1526) is described as 'references to acade… |
| **Total** | | **117,992** | **9,531** | **244,939** | **0** | **$0.0535** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 1s