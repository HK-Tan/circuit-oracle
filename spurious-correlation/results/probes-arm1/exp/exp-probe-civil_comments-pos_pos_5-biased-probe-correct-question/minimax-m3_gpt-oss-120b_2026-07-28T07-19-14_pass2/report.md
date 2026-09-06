# Circuit Oracle Report
**Date:** 2026-07-28 07:19:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification score is driven by entity/identity-group features (homosexuality/LGBTQ, Islam/Muslim, race/racism, social-justice) detected from input tokens "gay" (pos 17), "Muslim" (pos 12), and "social justice" (pos 5-6), rather than by features encoding the actual hateful framing/command structure of the prompt.

**Confidence:** 8

**Reasoning:** The top 20 features driving the probe's score are almost entirely identity/topic detectors:
- **L8:F15771** (direct_effect=0.277, pos 17) — "discussion of LGBTQ+ issues, especially same-sex marriage, adoption" — driven by the embedding of the word "gay" (direct_effect 17) plus L6:F6085.
- **L6:F6085** (direct_effect=0.326, pos 17) — "text related to homosexuality and same-sex marriage" — driven by Emb:"gay" (direct_effect 37!) plus L4 same-sex-marriage phrase detectors F8645 and F15899.
- **L6:F7282** (direct_effect=0.193, pos 12) — "mentions of Islam or Middle Eastern places" — driven overwhelmingly by Emb:"Muslim" (direct_effect 22.6) plus a religion-identity feature L4:F2405.
- **L4:F117** (direct_effect=0.26, pos 6/7) — "terms related to race, racism, and social justice" — driven by Emb:"justice" (pos 6, de=4.1) and Emb:"social" (pos 5, de=2.9), passing through L1:F13646 ("text discussing social justice issues") and L0:F3591 (government social programs).

All four supernodes ("gay_l6", "lgbtq_l8", "islam_l6", "race_l4") are **lexically triggered by identity-token embeddings** (gay, Muslim, social, justice) and are **content/topic classifiers**, not sentiment, framing, or pragmatic-condemnation detectors. Notably absent from the top drivers: any feature for "imperative/command", "slur usage", "hostile tone", "irony", or "targeted group derogation". The feature F117's label even explicitly says it fires on "social justice" (a contested political identifier), and its promoted tokens are "racist/racism/racial" — meaning the model is using *the presence of identity vocabulary* itself as a toxicity signal.

This confirms the user's concern: the probe's classification is overwhelmingly produced by **spurious identity-group/keyword features** rather than by features representing the prompt's actual semantic content (the bait-and-switch hostile imperative telling a hypothetical person to act in a way that would generate conflict). The circuit is a near-textbook example of a keyword-bag classifier where any passage mentioning "gay + Muslim + social justice" would likely receive a high score, even neutral or affirming passages. The signal flow is: **input token embeddings → identity-topic features at L0-L4 → identity-topic amplifiers at L6-L8 → probe score**, with virtually no layer of "is this text actually hostile/derogatory toward these groups?" features intervening.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score (toxicity) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L8:F15771](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) | 17 | L8 LGBTQ+ issues / same-sex marriage detector (pos 17 'wedding') | discussion of LGBTQ+ issues, especially same-sex marriage, adoption, and related topics | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/15771) |
| [L6:F6085](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) | 17 | L6 homosexuality / same-sex marriage text detector (pos 17) |  text related to homosexuality and same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6085) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 12 | L6 Islam / Middle Eastern mention detector (pos 12) |  mentions of Islam or Middle Eastern places and people, as well as mentions of a specific district. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | L4 race/racism/social-justice terms detector (pos 6 'justice', 7 'warrior', 13) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | L4 race/racism/social-justice terms detector (pos 6 'justice', 7 'warrior', 13) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 13 | L4 race/racism/social-justice terms detector (pos 6 'justice', 7 'warrior', 13) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F8645](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) | 17 | L4 same-sex marriage phrase detectors (pos 17) |  passages discussing same-sex marriage | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8645) |
| [L4:F15899](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) | 17 | L4 same-sex marriage phrase detectors (pos 17) |  language associated with the LGBTQ community and discussions of gender and identity. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15899) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 12 | L4 religious identity / affiliation detector (pos 12) |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L1:F13646](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) | 6 | L1 social-justice discourse detector (pos 6) | text discussing social justice issues | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13646) |
| [L0:F3591](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) | 6 | L0 government social programs / justice detector (pos 6) | terms related to government social programs | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3591) |
| [L0:F13885](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) | 12 | L0 Middle Eastern names/places detector (pos 12) |  names of people and places, specifically those related to the middle east | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:6085 de=0.326 |
| 3 | `inspect_feature` ×4 | L6:6085, L8:15771, L4:117, L6:7282 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F6085@17` | ✅ reported | 3 | 5 | Trace from L6:F6085 (text related to homosexuality and same-sex marriage) backwa… |
| SA-2 | `L4:F117@6` | ✅ reported | 5 | 5 | Trace from L4:F117 (terms related to race, racism, and social justice) at positi… |
| SA-3 | `L6:F7282@12` | ✅ reported | 4 | 5 | Trace from L6:F7282 (mentions of Islam or Middle Eastern) at position 12. The to… |
| SA-4 | `L8:F15771@17` | ✅ reported | 5 | 9 | Trace from L8:F15771 (LGBTQ+ issues, same-sex marriage) at pos 17 backward. Find… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F6085 | " text related to homosexuality and same-sex marriage" |
| 2 | `get_upstream_features` | L6:F6085@17, k=10 | Emb:" gay"@17 (de=37.00) +9 more |
| 3 | `inspect_feature` | L4, F8645 | " passages discussing same-sex marriage" |
| 4 | `inspect_feature` | L4, F15899 | " language associated with the LGBTQ community and discussions of gende" |
| 5 | `get_upstream_features` | L4:F8645@17, k=10 | Emb:" gay"@17 (de=22.88) +9 more |
| 6 | `inspect_feature` | L2, F4124 | " mentions of gay, bisexual and related topics" |
| 7 | `get_upstream_features` | L4:F15899@17, k=10 | Emb:" gay"@17 (de=21.12) +9 more |
| 8 | `inspect_feature` | L2, F103 | " words and phrases related to imprisonment, criminal justice, mental a" |

**Findings:** The target feature L6:F6085 (detecting homosexuality / same‑sex marriage content) is driven primarily by the input token embedding for the word 'gay' at position 17, providing a large positive direct effect (37.0). Intermediate mid‑layer features in layer 4 (F8645 and F15899) further amplify this signal, each also receiving strong excitation from the same 'gay' token embedding (22.9 and 21.1 respe…

</details>

<details>
<summary><b>SA-2</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 2 | `get_upstream_features` | L4:F117@6, k=10 | Emb:" justice"@6 (de=5.12) +9 more |
| 3 | `inspect_feature` | L0, F3591 | " terms related to government social programs" |
| 4 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |
| 5 | `get_upstream_features` | L0:F3591@6, k=10 | Emb:" social"@5 (de=21.00) +9 more |
| 6 | `get_upstream_features` | L1:F13646@6, k=10 | Emb:" justice"@6 (de=4.22) +9 more |
| 7 | `inspect_feature` | L3, F5157 | " references to social services and social work" |
| 8 | `get_upstream_features` | L3:F5157@6, k=10 | Emb:" social"@5 (de=24.12) +9 more |
| 9 | `inspect_feature` | L0, F11685 | " words related to social justice" |

**Findings:** The target L4:F117 (race/social‑justice detector) receives strong positive influence from the token embeddings for "justice" (pos 6) and "social" (pos 5), confirming that the phrase "social justice" directly drives it. Upstream, a low‑layer feature L0:F3591 (government‑social‑program detector) and L1:F13646 (social‑justice discourse detector) also receive the same embeddings and pass excitatory si…

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F7282 | " mentions of Islam or Middle Eastern places and people, as well as men" |
| 2 | `get_upstream_features` | L6:F7282@12, k=10 | Emb:" Muslim"@12 (de=22.62) +9 more |
| 3 | `inspect_feature` | L0, F13885 | " names of people and places, specifically those related to the middle " |
| 4 | `get_upstream_features` | L0:F13885@12, k=10 | Emb:" Muslim"@12 (de=10.38) +9 more |
| 5 | `inspect_feature` | L4, F2405 | " words related to religious identity/affiliation or spirituality inclu" |
| 6 | `get_upstream_features` | L4:F2405@12, k=10 | Emb:" Muslim"@12 (de=15.75) +9 more |

**Findings:** The target feature L6:F7282 (Islam/Middle‑Eastern mention) is overwhelmingly driven by the input token embedding for 'Muslim' (direct_effect >22). Additional low‑level contributors include L0:F13885, a detector for Middle‑Eastern names, and L4:F2405, a religious‑identity detector. All major upstream nodes sit at layers 0–4 (≤8), satisfying the lower‑third layer requirement, and a direct positive e…

</details>

<details>
<summary><b>SA-4</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F15771 | "discussion of LGBTQ+ issues, especially same-sex marriage, adoption, a" |
| 2 | `get_upstream_features` | L8:F15771@17, k=10 | Emb:" gay"@17 (de=17.00) +9 more |
| 3 | `inspect_feature` | L6, F6085 | " text related to homosexuality and same-sex marriage" |
| 4 | `inspect_feature` | L7, F16171 | " texts about homosexuality, gay marriage, and religious views on these" |
| 5 | `get_upstream_features` | L6:F6085@17, k=10 | Emb:" gay"@17 (de=37.00) +9 more |
| 6 | `inspect_feature` | L4, F8645 | " passages discussing same-sex marriage" |
| 7 | `get_upstream_features` | L7:F16171@17, k=10 | L6:F6085 (de=5.72) +9 more |
| 8 | `inspect_feature` | L4, F15899 | " language associated with the LGBTQ community and discussions of gende" |
| 9 | `inspect_feature` | L6, F15295 | " words and abbreviations related to HIV/AIDS and viral infections." |
| 10 | `get_upstream_features` | L4:F8645@17, k=10 | Emb:" gay"@17 (de=22.88) +9 more |

**Findings:** The L8 feature 15771, which flags LGBTQ+ discussion (especially same‑sex marriage), is driven primarily by the token embedding for "gay" and a cascade of lower‑layer detectors. The strongest upstream mid‑level detector is L6:F6085, a sparse (frac 0.0017) feature that activates on homosexuality‑related language. Its own strongest drivers are the same "gay" embedding and the L4 phrase detector F8645…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F6085@17, k=8 → Emb:" gay"@17 (de=37.00) +7 more |
| 2 | `get_upstream_features` | L4:F117@7, k=8 → Emb:" justice"@6 (de=4.12) +7 more |
| 3 | `get_upstream_features` | L4:F117@13, k=8 → Emb:" Muslim"@12 (de=5.25) +7 more |
| 4 | `get_upstream_features` | L6:F7282@12, k=8 → Emb:" Muslim"@12 (de=22.62) +7 more |
| 5 | `inspect_feature` ×3 | L4:2405, L4:8645, L4:15899 |

### Build

`build_circuit` → 14 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 20,959 | 3,931 | 83,896 | 0 | $0.0160 | — | — |
| SA-1 | openai/gpt-oss-120b | 73,323 | 4,409 | 10,224 | 0 | $0.0138 | ✅ 3F/5E | Trace from L6:F6085 (text related to homosexuality and same-… |
| SA-3 | openai/gpt-oss-120b | 50,194 | 3,779 | 2,560 | 0 | $0.0098 | ✅ 4F/5E | Trace from L6:F7282 (mentions of Islam or Middle Eastern) at… |
| SA-2 | openai/gpt-oss-120b | 86,201 | 7,391 | 24,336 | 0 | $0.0177 | ✅ 5F/5E | Trace from L4:F117 (terms related to race, racism, and socia… |
| SA-4 | openai/gpt-oss-120b | 111,888 | 6,521 | 5,088 | 0 | $0.0208 | ✅ 5F/9E | Trace from L8:F15771 (LGBTQ+ issues, same-sex marriage) at p… |
| **Total** | | **342,565** | **26,031** | **126,104** | **0** | **$0.0782** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 2s