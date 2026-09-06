# Circuit Oracle Report
**Date:** 2026-07-28 07:18:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven by an identity-aggregation circuit that escalates raw tokens like "social," "justice," "warrior," "Muslim," and "gay" up through mid-layer features specialized in social-justice, race, and political-movement language (L4:F117, F10459, L5:F14124, L6:F2674), rather than by features that read the prompt's actual semantic content (imperative construction, "go to" instruction, contradiction/harm structure, or the noun "cake").

**Confidence:** 8

**Reasoning:** The circuit traces from token embeddings through a clean identity-labeled supernode hierarchy. At L0, three of the top features at the probe are token-anchored: L0:F14006 ("the word 'social'", pos 5, frac_nonzero=0.01972, embedding→probe direct_effect −0.18 suppressing the probe? Actually F14006 is suppressive here, but the same embedding at pos 5 also drives the strong positive L4:L5:L6 path); L0:F3591 ("government social programs" but with top activations on "Sciences"/"Services" — really fires on "justice") and L0:F1526 ("social sciences" — really fires on "justice" at pos 6, direct_effect +0.099) both anchor the token "justice"; L0:F10219 ("the indefinite article 'a'", pos 16) anchors "a" in "gay". Critically, the L0 features that *should* carry prompt content (imperative + cake-shop scenario) are absent — the highest-activating L0 features for the actual semantic content (L0:F14209 "go", L0:F13756 "order", L0:F9005 dessert/pos 13, L0:F2260 medical/legal terms for "assault"-type nouns) are all in the circuit but push *against* the probe score, not for it.

The L3 supernode contains L3:F10868 ("I'm a / I am a" identity-statement detector, pos 4, direct_effect +0.135) which, despite its generic label, is the bridge that propagates the identity-token signal upward. L3:F16254 (conditional statements, pos 8, +0.104) carries the "If you are … go to" structure upward but is dominated by identity-labeled upstream contributions (per the subagent trace, "If you" contributes 9.875 vs. "warrior" only 2.4, but it still fires the conditional→action cue that the prompt's harm depends on).

The decisive supernode is L4 "social-justice / race / political movement": L4:F117 ("race, racism, social justice, terms related to Black people" — promoted tokens: racist, racism, racial; top activations "color", "cists", "color", frac_nonzero=0.012, direct_effect +0.0645 via the L6 path) and L4:F10459 ("words related to politics, especially political parties and movements like the Tea Party", direct_effect +0.066) both fire on "warrior" at pos 7 with the L5 and L6 ideological features consolidating them. L5:F14124 ("strong and opinionated political discourse", frac_nonzero=0.0105) and L6:F2674 ("political or ideological content, particularly with negative connotations", direct_effect −0.113 on the probe — i.e., suppressive, but it's the dominant ideological node) carry the identity-aggregation signal into the probe's classification direction.

The user's concern is confirmed: the *driving* positive contribution to the toxicity score comes from a chain that begins with **identity tokens as such** (social, justice, warrior, Muslim, gay) and is mediated by **identity-stereotyped mid-layer features** (F117 race/social-justice detector, F10459 political-movement detector, F14124 opinionated-political detector, F2674 ideology-with-negative-connotations) — features whose autointerp labels and promoted tokens reveal that they were trained on text where these identity labels co-occur with conflict, not text where the labels are merely being enumerated. The semantic content of the prompt (the *imperative* "go to a Muslim bakery and order a gay wedding cake" — a deliberately provocative shop-transaction) is not represented by any feature in the positive-side circuit; instead, features that would encode the *transaction/request* structure (L1:F14281 "instruction", L0:F13756 "order", L0:F14209 "go", L6:F9005 "dessert/cake", L2:F14541 code/logic "then") appear with negative or near-zero direct effects, while the identity-label features dominate. The cake/dessert feature (L6:F9005) actually pushes the *opposite* direction (direct_effect −0.113), as if a benign-cake-shopping frame is being suppressed relative to the identity-label frame. This is the classic spurious-correlation failure mode: the probe learned that text containing stacked identity-group labels (especially "social justice" + a marginalized identity) tends to be toxic in training, and so it fires on the *labels themselves* rather than on what is being said about them.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: ' social' (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: ' justice' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: ' warrior' (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: ' Muslim' (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 16 | Emb: ' gay' (pos 16) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: function words (pos 1-4, 8, 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: function words (pos 1-4, 8, 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F14006](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14006) | 5 | L0 token-level identity words |  the word "social" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14006) |
| [L0:F3591](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) | 6 | L0 token-level identity words |  terms related to government social programs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) |
| [L0:F1526](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1526) | 6 | L0 token-level identity words | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1526) |
| [L0:F2260](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) | 6 | L0 token-level identity words |  terms that are medical, legal, or related to social work | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2260) |
| [L0:F13310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) | 3 | L0 token-level identity words |  sentences that include forms of the verb "are" indicating a present state of being or necessity. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13310) |
| [L0:F13756](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) | 15 | L0 token-level identity words |  the word "order" and occasionally "period," in many different contexts from law to food | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13756) |
| [L0:F4478](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) | 6 | L0 token-level identity words |  terms related to ownership and belief systems. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4478) |
| [L0:F3850](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) | 8 | L0 token-level identity words | punctuation marks | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3850) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 10 | L0 token-level identity words | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 2 | L0 token-level identity words | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F9934](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) | 6 | L0 token-level identity words |  the word "particular" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9934) |
| [L0:F10219](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) | 16 | L0 token-level identity words |  the indefinite article "a" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) |
| [L0:F9602](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) | 6 | L0 token-level identity words |  the word "emphasis." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9602) |
| [L1:F10447](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10447) | 4 | L1 article & instruction words | articles and prepositions | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10447) |
| [L1:F14281](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14281) | 6 | L1 article & instruction words |  the word "instruction" and its plural | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14281) |
| [L1:F14576](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14576) | 13 | L1 article & instruction words |  words relating to food dishes and dining, especially those in restaurants | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14576) |
| [L1:F3305](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3305) | 6 | L1 article & instruction words |  the word "task" and related terms in the context of scientific experiments | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3305) |
| [L2:F14209](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) | 9 | L2 function/structural words (go, then, roles) | the verb "go" in its various forms. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14209) |
| [L2:F14541](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) | 8 | L2 function/structural words (go, then, roles) |  code snippets and logical statements, especially those involving "then," along with some citation markers and bracketed references. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14541) |
| [L2:F13877](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13877) | 7 | L2 function/structural words (go, then, roles) |  words related to roles, ranks, or personal characteristics of people | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13877) |
| [L2:F1537](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1537) | 6 | L2 function/structural words (go, then, roles) |  words and phrases related to political and social issues and movements | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1537) |
| [L3:F10868](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) | 4 | L3 identity-statement & conditional structure |  the phrase "I'm a" or "I am a" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10868) |
| [L3:F16254](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) | 8 | L3 identity-statement & conditional structure |  conditional statements followed by actions the speaker will take | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16254) |
| [L3:F1526](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) | 6 | L3 identity-statement & conditional structure |  references to academic disciplines related to social science | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1526) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | L4 social-justice / race / political movement features |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F10459](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10459) | 7 | L4 social-justice / race / political movement features |  words related to politics, especially political parties and movements like the Tea Party. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10459) |
| [L4:F13041](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13041) | 13 | L4 social-justice / race / political movement features |  words related to food and dining experiences | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13041) |
| [L4:F13700](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13700) | 8 | L4 social-justice / race / political movement features | conditional clauses starting with "if" and words related to business contexts | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13700) |
| [L5:F14124](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14124) | 7 | L5 opinionated political discourse |  things that indicate strong and opinionated political discourse | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/14124) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | L5 opinionated political discourse | the start of documentation blocks in code | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L6:F2674](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) | 7 | L6 ideological / negative political features (includes the cake/dessert suppressor) |  political or ideological content, particularly with negative connotations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2674) |
| [L6:F9005](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) | 13 | L6 ideological / negative political features (includes the cake/dessert suppressor) |  words and phrases related to desserts | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9005) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | L6 ideological / negative political features (includes the cake/dessert suppressor) |  the words "the" and "it" at the beginning of sentences | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |
| [L9:F2762](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) | 1 | L9 code/braces feature (incidental) |  various code snippets, especially javascript | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:8444 de=-0.224 |
| 3 | `inspect_feature` ×20 | L0:8444, L0:7710, L3:10868, L6:9005, L3:16254, L0:9934, L0:4478, L0:13310, L0:13756, L0:2260, L0:3850, L3:1526, L2:14541, L2:14209, L6:2674, L1:14281, L2:13877, L4:13700, L0:9602, L0:3591 |
| 4 | `get_source_influence` | {'depth': 2, 'source_positions': [5, 6, 7, 11, 16, 17, 18], 'S_pct_of_total': 5. |
| 5 | `get_source_influence` | {'depth': 2, 'source_positions': [1, 2, 3, 4, 8, 9, 10, 13, 14, 15], 'S_pct_of_t |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L3:F10868@4` | ✅ reported | 4 | 5 | Trace upstream from L3:F10868 at pos 4 (positive direct effect on the probe). Th… |
| SA-2 | `L3:F16254@8` | ✅ reported | 3 | 9 | Trace upstream from L3:F16254 at pos 8 (positive direct effect, "conditional sta… |
| SA-3 | `L6:F2674@7` | ✅ reported | 4 | 7 | Trace upstream from L6:F2674 at pos 7 ("political or ideological content, partic… |
| SA-4 | `L6:F9005@13` | ✅ reported | 4 | 3 | Trace upstream from L6:F9005 at pos 13 (negative direct effect, "words and phras… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F10868 | " the phrase "I'm a" or "I am a"" |
| 2 | `get_upstream_features` | L3:F10868@4, k=15 | Emb:" a"@4 (de=18.62) +14 more |
| 3 | `inspect_feature` | L2, F8867 | "the acronyms WIMP, WMS, WFS, and WCS" |
| 4 | `get_upstream_features` | L2:F8867@4, k=15 | Emb:" a"@4 (de=6.84) +14 more |
| 5 | `inspect_feature` | L1, F10447 | "articles and prepositions" |
| 6 | `inspect_feature` | L2, F346 | "C/C++ code constructs (macros, declarations, data types, network relat" |
| 7 | `get_upstream_features` | L1:F10447@4, k=15 | Emb:" a"@4 (de=16.62) +14 more |

**Findings:** The L3:F10868 feature detects the self‑reference phrase "I am a". Its strongest upstream drivers are the raw input embeddings for the token " a" (pos 4) and the preceding token " you" (pos 2), which together form the lexical pattern "I am a". Lower‑layer (L1) article‑detector (F10447) and a small contribution from a generic layer‑2 feature (F8867) shape this signal. All identified upstream nodes a…

</details>

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F16254 | " conditional statements followed by actions the speaker will take" |
| 2 | `get_upstream_features` | L3:F16254@8, k=10 | Emb:"If"@1 (de=9.88) +9 more |
| 3 | `inspect_feature` | L2, F696 | "mathematical or logical notation, especially related to theorems or pr" |
| 4 | `get_upstream_features` | L2:F696@8, k=10 | Emb:"If"@1 (de=11.12) +9 more |
| 5 | `inspect_feature` | L1, F12201 | " occurrences of parenthetical citations in scientific notation and num" |
| 6 | `get_upstream_features` | L1:F12201@8, k=10 | Emb:","@8 (de=5.81) +9 more |

**Findings:** The conditional‑statement feature (L3:F16254) is primarily driven by the token "If" and surrounding punctuation, confirming that the signal carries the conditional structure. A secondary positive contribution comes from the token "warrior" (embedding at position 7), indicating that the noun also supplies a modest boost but is not the core driver. Upstream logical‑notation (L2:696) and punctuation‑…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F2674 | " political or ideological content, particularly with negative connotat" |
| 2 | `get_upstream_features` | L6:F2674@7, k=10 | Emb:" social"@5 (de=2.12) +9 more |
| 3 | `inspect_feature` | L5, F14124 | " things that indicate strong and opinionated political discourse" |
| 4 | `inspect_feature` | L4, F10459 | " words related to politics, especially political parties and movements" |
| 5 | `get_upstream_features` | L5:F14124@7, k=10 | Emb:" warrior"@7 (de=3.41) +9 more |
| 6 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 7 | `inspect_feature` | L3, F8342 | "discussions of quality of life and health metrics, with some associati" |
| 8 | `get_upstream_features` | L4:F117@7, k=10 | Emb:" justice"@6 (de=4.12) +9 more |

**Findings:** The L6:F2674 feature aggregates political/ideological negativity and receives strong positive influence from three token embeddings that make up the phrase \"social justice warrior\" (social at pos5, justice at pos6, warrior at pos7). These embeddings excite intermediate features that specialize in political discourse (5:14124) and race/social‑justice language (4:117). Consequently, the target fea…

</details>

<details>
<summary><b>SA-4</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F9005 | " words and phrases related to desserts" |
| 2 | `get_upstream_features` | L6:F9005@13, k=10 | Emb:" bakery"@13 (de=22.38) +9 more |
| 3 | `inspect_feature` | L4, F13041 | " words related to food and dining experiences" |
| 4 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 5 | `get_upstream_features` | L6:F9005@13, k=20 | Emb:" bakery"@13 (de=22.38) +19 more |
| 6 | `get_upstream_features` | L4:F13041@13, k=10 | Emb:" bakery"@13 (de=21.38) +9 more |
| 7 | `inspect_feature` | L1, F14576 | " words relating to food dishes and dining, especially those in restaur" |
| 8 | `get_upstream_features` | L1:F14576@13, k=10 | Emb:" bakery"@13 (de=10.94) +9 more |

**Findings:** Starting from L6:F9005 (dessert detector) at token position 13, the strongest positive upstream influence is the input embedding " bakery" (direct effect +22.4), confirming that the feature fires on the "cake" token within a bakery context. Tracing upstream, the signal passes through L4:F13041 (food-and-dining detector) and then to L1:F14576 (restaurant dish detector), both in layers <=8 (the lowe…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×21 | L5:14124, L4:117, L4:10459, L1:10447, L4:13041, L1:14576, L2:14541, L2:14209, L4:13700, L2:13877, L0:3591, L3:1526, L6:2674, L5:3992, L0:14006, L0:10219, L2:1537, L1:3305, L6:14585, L9:2762, L0:2713 |

### Build

`build_circuit` → 15 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 79,704 | 6,521 | 262,096 | 0 | $0.0475 | — | — |
| SA-2 | openai/gpt-oss-120b | 59,822 | 5,465 | 8,992 | 0 | $0.0124 | ✅ 3F/9E | Trace upstream from L3:F16254 at pos 8 (positive direct effe… |
| SA-1 | openai/gpt-oss-120b | 83,620 | 5,374 | 2,528 | 0 | $0.0158 | ✅ 4F/5E | Trace upstream from L3:F10868 at pos 4 (positive direct effe… |
| SA-3 | openai/gpt-oss-120b | 86,068 | 5,352 | 0 | 0 | $0.0161 | ✅ 4F/7E | Trace upstream from L6:F2674 at pos 7 ("political or ideolog… |
| SA-4 | openai/gpt-oss-120b | 93,532 | 6,311 | 5,056 | 0 | $0.0179 | ✅ 4F/3E | Trace upstream from L6:F9005 at pos 13 (negative direct effe… |
| **Total** | | **402,746** | **29,023** | **278,672** | **0** | **$0.1097** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 27s