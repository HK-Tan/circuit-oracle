# Circuit Oracle Report
**Date:** 2026-07-28 07:23:45 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe's classification is driven by transcoder features that fire on identity-group language — primarily LGBTQ+ topics (activated by the token "Gay" at pos 9 and the "Pride" token) and racial/color terms (activated by "Black" at pos 1 and "White" at pos 17) — with no features responding to the genuinely toxic tokens "NAZI", "Hypocrisy", "racism", or the equal-sign structure that encodes the actual hateful comparison.

**Confidence:** 8

**Reasoning:** The circuit confirms the user's concern almost exactly. The terminal node is L8:F15771 ("discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics," frac_nonzero=0.0078, direct_effect=+0.32) — a high-level detector of identity-group discourse rather than toxicity. It is fed by L7:F10287 (LGBTQ rights), L7:F16171 (homosexuality/gay marriage), and L7:F7263 (homosexuality/bisexuality/gay culture), which themselves are built from L6:F6085 (homosexuality/same-sex marriage) and L6:F15295 (HIV/AIDS terms, which promoted tokens include "gays"/"homosexuality"). Below that, L4:F15899 (LGBTQ community/gender identity language) and L4:F8645 (same-sex marriage) take the strongest input from the `Emb: Gay (pos 9)` token (+21.75 on F6085, +13.8 on F15899) — the word "Gay" itself.

A second parallel path runs on the race axis. L2:F13158 (race/ethnicity words) is excited by `Emb: White (pos 17)` (+13.6) and `Emb:  black (pos 5)` (+10.75) and propagates to L4:F117 (race/racism/Black-people terms at pos 17, +0.20 direct effect) and L6:F3902 (race/ethnicity terms at pos 17, +0.20). L2:F585 (word "white") and L2:F11363 (color words) are also driven by these same identity-token embeddings.

The negative side of the circuit is just as telling. L3:F7993 (word "black"/"blacks," direct_effect=−0.17), L2:F9528 ("the color black," direct_effect=−0.23), and L1:F9113 ("discussions about race and slavery," direct_effect=−0.32) all *suppress* the probe, and their strongest input is the `Emb: Black (pos 1)` token (+23.5, +30, +16.9 respectively). Critically, **no feature in the top 20 is activated by or even receives meaningful positive direct effect from "NAZI", "Hypocrisy", "racism", or "worse"** — the actually-toxic content of the prompt. The phrase "White Pride = NAZI" and the conclusion "Hypocrisy is worse than racism" leave essentially no causal trace on the probe direction; instead, the probe is being driven by the *topic* of the input (presence of an identity-group label like "Gay" or "White/Black") rather than the *valence* of the statement about that topic.

This is a textbook spurious-correlation pattern: the linear probe has learned that prompts containing identity-group vocabulary (regardless of whether the surrounding sentence is celebratory, neutral, or explicitly hateful) tend to co-occur with toxicity in its training data, and the attribution graph shows the model encoding exactly that confound. The user's concern is borne out — the circuit uses identity-group topic features (LGBTQ+ discourse, racial terms, color words) as a proxy for toxicity, and the actual toxicity-bearing tokens "NAZI" and "racism" are absent from the positive circuit. A debiasing intervention would need to suppress the L8:F15771 / L7 / L4 LGBTQ+ and L4:F117 / L2:F13158 race-ethnicity supernodes while preserving whatever (currently near-absent) signal comes from the NAZI/racism tokens.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 9 | LGBTQ+ issues / same-sex marriage (high-level) | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L7:F10287](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/10287) | 9 | LGBTQ rights / homosexuality |  mentions and terms related to LGBTQ rights | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/10287) |
| [L7:F16171](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16171) | 9 | LGBTQ rights / homosexuality |  texts about homosexuality, gay marriage, and religious views on these topics | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16171) |
| [L7:F7263](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7263) | 9 | LGBTQ rights / homosexuality |  mentions of homosexuality, bisexuality, and gay culture. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7263) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 9 | Homosexuality / same-sex marriage |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F15295](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) | 2 | Homosexuality / same-sex marriage |  words and abbreviations related to HIV/AIDS and viral infections. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15295) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 9 | LGBTQ community / gender identity language |  language associated with the LGBTQ community and discussions of gender and identity. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L4:F8645](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) | 9 | LGBTQ community / gender identity language |  passages discussing same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 17 | Race terms (white, ethnicity) at pos 17 (White Pride line) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 17 | Race terms (white, ethnicity) at pos 17 (White Pride line) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 17 | Race / ethnicity terms at pos 17 |  terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 17 | Word "white" detector | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 17 | Race/ethnicity word detector |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 5 | Race/ethnicity word detector |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F11363](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) | 1 | Color/race words at pos 1 (Black) |  colors and words like Diamond. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11363) |
| [L2:F9528](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) | 1 | Color "black" detector (suppresses probe) |  the color black | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9528) |
| [L3:F7993](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7993) | 1 | Word "black"/"blacks" detector (suppresses probe) | the word "black" and its plural form "blacks" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7993) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 2 | Race/gender/social-issues words at pos 2 (Pride) |  words related to race, gender and social issues | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L2:F1644](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) | 2 | Word "pride" detector |  different forms of the word "pride" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1644) |
| [L1:F9113](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) | 1 | Race/slavery detector (suppresses probe at pos 1) |  discussions about race and slavery | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9113) |
| [L1:F12542](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12542) | 2 | Race/slavery detector (suppresses probe at pos 1) | mentions of the word "proud" or words relating to TV shows and TV seasons. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12542) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 17 | Social justice text detector at pos 17 |  text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:15771 de=0.324 |
| 3 | `inspect_feature` ×14 | L8:15771, L1:9113, L2:11363, L2:13158, L3:13061, L2:9528, L1:12542, L6:6085, L4:15899, L6:3902, L4:117, L2:1644, L6:15295, L3:7993 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F15771@9` | ❌ error | — | — | Trace L8:F15771 (LGBTQ+ issues / same-sex marriage feature at pos 9 "Gay") upstr… |
| SA-2 | `L2:F11363@1` | ❌ error | — | — | Trace L2:F11363 (color words including "White" feature at pos 1) upstream to tok… |
| SA-3 | `L1:F9113@1` | ❌ error | — | — | Trace L1:F9113 (race/slavery feature, pos 1) upstream to token embeddings. This … |
| SA-4 | `L2:F1644@2` | ❌ error | — | — | Trace L2:F1644 (pride feature at pos 2) upstream to token embeddings. Identify w… |
| SA-5 | `L6:F6085@9` | ❌ error | — | — | Trace L6:F6085 (homosexuality / same-sex marriage feature at pos 9) upstream to … |
| SA-6 | `L3:F7993@1` | ❌ error | — | — | Trace L3:F7993 (word "black" / "blacks" feature at pos 1) upstream to token embe… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L8:F15771@9, k=15 → Emb:"Gay"@9 (de=10.38) +14 more |
| 2 | `get_upstream_features` | L2:F11363@1, k=15 → Emb:"Black"@1 (de=25.00) +14 more |
| 3 | `get_upstream_features` | L2:F1644@2, k=15 → Emb:" Pride"@2 (de=16.62) +14 more |
| 4 | `get_upstream_features` | L1:F9113@1, k=15 → Emb:"Black"@1 (de=16.88) +14 more |
| 5 | `get_upstream_features` | L3:F7993@1, k=10 → Emb:"Black"@1 (de=23.50) +9 more |
| 6 | `get_upstream_features` | L4:F117@17, k=10 → Emb:"White"@17 (de=10.25) +9 more |
| 7 | `get_upstream_features` | L6:F3902@17, k=10 → Emb:"White"@17 (de=7.12) +9 more |
| 8 | `get_upstream_features` | L6:F6085@9, k=10 → Emb:"Gay"@9 (de=21.75) +9 more |
| 9 | `get_upstream_features` | L2:F13158@17, k=10 → Emb:"White"@17 (de=13.56) +9 more |
| 10 | `get_upstream_features` | L3:F13061@2, k=10 → Emb:"Black"@1 (de=12.06) +9 more |
| 11 | `get_upstream_features` | L4:F15899@9, k=10 → Emb:"Gay"@9 (de=13.81) +9 more |
| 12 | `get_upstream_features` | L2:F9528@1, k=10 → Emb:"Black"@1 (de=30.00) +9 more |
| 13 | `get_upstream_features` | L1:F12542@2, k=10 → Emb:" Pride"@2 (de=13.75) +9 more |
| 14 | `get_upstream_features` | L6:F15295@2, k=10 → Emb:" Pride"@2 (de=10.75) +9 more |
| 15 | `inspect_feature` ×4 | L4:8645, L7:10287, L7:16171, L1:13646 |
| 16 | `get_upstream_features` | L7:F16171@9, k=8 → L6:F6085 (de=5.03) +7 more |
| 17 | `get_upstream_features` | L7:F7263@9, k=8 → L6:F6085 (de=7.59) +7 more |
| 18 | `get_upstream_features` | L2:F585@17, k=8 → Emb:"White"@17 (de=27.88) +7 more |
| 19 | `get_upstream_features` | L2:F13158@5, k=8 → Emb:" black"@5 (de=10.75) +7 more |
| 20 | `inspect_feature` ×2 | L7:7263, L2:585 |
| 21 | `get_upstream_features` | L3:F13061@2, k=8 → Emb:"Black"@1 (de=12.06) +7 more |
| 22 | `get_upstream_features` | L3:F7993@1, k=8 → Emb:"Black"@1 (de=23.50) +7 more |

### Build

`build_circuit` → 21 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 53,362 | 6,639 | 347,191 | 0 | $0.0448 | — | — |
| **Total** | | **53,362** | **6,639** | **347,191** | **0** | **$0.0448** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 50s