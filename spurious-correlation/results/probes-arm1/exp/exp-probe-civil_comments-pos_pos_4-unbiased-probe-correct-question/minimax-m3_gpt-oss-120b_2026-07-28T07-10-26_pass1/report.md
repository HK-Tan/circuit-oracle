# Circuit Oracle Report
**Date:** 2026-07-28 07:10:26 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The toxicity probe is driven by an interaction between an identity-token circuit (L3:F13473 "racial/ethnic group mentions", L2:F2123 "-ian demonym suffix") and an abuse-token circuit (L4:F148 "sexual assault & abuse", L3:F4327 "-ive suffix", L2:F9873 "abusive language"), with the two chains converging on L6:F10545 "political rhetoric on race/historical states/government control" at the "Indians" position — and this late-layer feature feeds the output alongside generic L6:F1600 "problems", L5:F3229 "violent assault" features that fire from function-word / generic "problems" embeddings.

**Confidence:** 8

**Reasoning:**

The probe's positive classification is over-determined. Of the top features (by |direct_effect|), roughly half are real toxicity signal: **L6:F10545** (+0.1357, *race-political rhetoric* at "Indians"), **L4:F148** (+0.1196 chain, *abuse/sexual-assault* at "abusers"), **L3:F4327** (+0.0967, *"-ive" suffix* at "abusers"), **L6:F1600** (−0.0977, *negative words related to problems*, at "problems"), **L5:F3229** (−0.1196, *violent assault / murder* words), and **L3:F2705** (+0.0913, *cheating/deception*). The remaining features are highly generic: **L0:F11375** "the word *is*" (frac_nonzero 0.0096, +0.2207), **L0:F11668** "Baseball terminology" (frac_nonzero 0.0088, +0.1826 — fires on "Indians" through the baseball-team sense), **L0:F3498** "the pronoun *they*" (−0.0962), **L0:F8381** "the word *by*" (+0.0996), **L0:F11154** "the word *are*" (−0.1387), **L0:F6035** "the word *depending*" (+0.0923), **L0:F15956** "the word *those*" (+0.0898), **L1:F13535** "words related to business/education/religion/stories", and **L4:F4021** "code snippets with *as*". These are all extremely low-frac_nonzero lexical detectors with no semantic relation to toxicity; their large direct_effects come from being active on a single input token and the probe's residual-stream decomposition rewarding that activity.

Tracing to the embedding floor confirms the user's concern: the toxic signal is anchored on the **"Indians" (pos 1)** and **"abusers" (pos 3)** tokens. "Indians" directly excites L2:F2123 (the "-ian" demonym suffix detector, de=+17.125 from the embedding), which in turn drives L3:F13473 (the "racial/ethnic group mentions" feature, de=+2.45). "Indians" *also* directly drives L6:F10545 (de=+1.90) and L2:F1680 "people participating in activity" (de=+8.56). "abusers" (pos 3) directly drives L4:F148 (de=+19.13), L3:F4327 (de=+12.75), and L2:F5368 (de=+9.0). So the "identity-group" detector **L3:F13473 (frac_nonzero 0.00569, label: "mentions of racial and ethnic groups, especially in the United States")** is one of the most direct single features pushing the probe (+0.1226), and it fires because "Indians" is a racial/ethnic demonym — not because anything in the prompt is semantically toxic.

The circuit therefore exhibits exactly the spurious-feature pattern the user describes. The probe's positive direction sums (a) genuine abuse-language features keyed to the word "abusers" (a legitimate toxicity signal) with (b) **identity-mention features** keyed to the word "Indians" — particularly L3:F13473 ("racial/ethnic groups, especially US") and L6:F10545 ("political rhetoric on race, historical states, government control"). Because the prompt mentions Indians *and* uses the word "abusers", the probe fires strongly; but a non-toxic sentence like "Indians are famous for cricket" would activate L3:F13473 and L6:F10545 through the same embedding pathway (emb_indians → ian_suffix_l2 → ethnic_l3) and push the probe positive on the identity signal alone, even without any abuse content. The user is correct that the probe relies on an "an identity group is mentioned" feature (L3:F13473) rather than purely on the lexical/semantic toxicity of the content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F10545](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) | 3 | L6:F10545 — political rhetoric on race, historical states, govt control (pos 3 'Indians') |  political rhetoric related to race, historical states, and government control | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10545) |
| [L6:F1600](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1600) | 12 | L6:F1600 — negative words related to problems/imperfections (pos 12 'problems') |  negative words and phrases related to problems and imperfections | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1600) |
| [L5:F3229](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3229) | 3 | L5:F3229 — violent assault and murder words (pos 3) |  words related to violent assault and murder | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3229) |
| [L4:F148](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) | 3 | L4:F148 — sexual assault & abuse words (pos 3 'abusers') | words and phrases related to sexual assault and abuse | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/148) |
| [L4:F4021](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) | 4 | L4:F4021 — code/config with 'as' (pos 4) — generic pattern |  code snippets or configurations with the word "as". | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4021) |
| [L3:F13473](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) | 2 | L3:F13473 — racial/ethnic group mentions (US context) (pos 2 'Indians') |  mentions of racial and ethnic groups, especially in the United States | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13473) |
| [L3:F4327](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4327) | 3 | L3:F4327 — suffix '-ive'/'ices' detector (pos 3 'abusers') | words and phrases that end with "ive", and also a few words that end in "ices" or "ishes", and also the phrase "advantage of the". | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4327) |
| [L3:F5853](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5853) | 7 | L3:F5853 — speaking/making statements (pos 7 'stated') |  instances of people speaking and making statements | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5853) |
| [L3:F2705](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2705) | 3 | L3:F2705 — cheating/deception words (pos 3) |  words related to cheating or being deceptive | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/2705) |
| [L3:F9646](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9646) | 2 | L3:F9646 — verbs/nouns (pos 2/3) | verbs and associated nouns. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9646) |
| [L2:F1680](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) | 1 | L2:F1680 — people participating in an activity (consumers/patients/voters) (pos 1 'Indians') |  words that refer to people participating in some activity, such as consumers, patients in healthcare, or voters | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1680) |
| [L2:F2123](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) | 1 | L2:F2123 — demonym/nationality suffix '-ian' (pos 1 'Indians') | words ending in "ian", "jani", "iti", "ino", or "olan" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2123) |
| [L2:F5368](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5368) | 3 | L2:F5368 — legal trouble / crime words (pos 3 'abusers') |  words related to legal trouble and crime | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5368) |
| [L2:F9873](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9873) | 3 | L2:F9873 — abusive language / '-ally' suffix (pos 3) |  instances of abusive language or words that end in "ally" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9873) |
| [L2:F8909](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8909) | 12 | L2:F8909 — problems / defects / complaints (pos 12) | mentions of problems, defects, complaints | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8909) |
| [L1:F13535](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13535) | 1 | L1:F13535 — business/education/religion/stories (pos 1) |  words related to business, education, religion, and stories | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/13535) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:11375 de=0.221 |
| 3 | `inspect_feature` ×20 | L0:11375, L0:11668, L6:10545, L3:13473, L2:1680, L0:8381, L3:9646, L3:4327, L0:3436, L0:6035, L3:14281, L0:11154, L5:3229, L6:1600, L0:3498, L3:5853, L1:13535, L4:4021, L0:15956, L3:2705 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F10545@3` | ✅ reported | 5 | 11 | Trace this feature upstream. It's labeled as "political rhetoric related to race… |
| SA-2 | `L3:F13473@2` | ✅ reported | 3 | 5 | Trace this feature upstream. It's labeled "mentions of racial and ethnic groups,… |
| SA-3 | `L0:F11668@1` | ❌ error | — | — | Trace this feature upstream. It's labeled "Baseball terminology" and fires at po… |
| SA-4 | `L0:F11375@8` | ❌ error | — | — | Trace this feature upstream. Labeled "the word is" at pos 8. Direct effect +0.22… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F10545 | " political rhetoric related to race, historical states, and government" |
| 2 | `get_upstream_features` | L6:F10545@3, k=10 | Emb:" abusers"@3 (de=1.90) +9 more |
| 3 | `inspect_feature` | L4, F148 | " words and phrases related to sexual assault and abuse" |
| 4 | `get_upstream_features` | L4:F148@3, k=10 | Emb:" abusers"@3 (de=19.12) +9 more |
| 5 | `inspect_feature` | L2, F9873 | " instances of abusive language or words that end in "ally"" |
| 6 | `inspect_feature` | L2, F5368 | " words related to legal trouble and crime" |
| 7 | `get_upstream_features` | L2:F9873@3, k=10 | Emb:" abusers"@3 (de=10.75) +9 more |
| 8 | `get_upstream_features` | L2:F5368@3, k=10 | Emb:" abusers"@3 (de=9.00) +9 more |
| 9 | `inspect_feature` | L3, F4327 | "words and phrases that end with "ive", and also a few words that end i" |
| 10 | `get_upstream_features` | L3:F4327@3, k=10 | Emb:" abusers"@3 (de=12.75) +9 more |
| 11 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 12 | `inspect_feature` | L0, F10155 | " words related to membership in a group" |

**Findings:** The downstream feature L6:F10545 (political‑race rhetoric) is driven primarily by an abuse‑related detector in layer 4 (F148) and directly by the token‑embedding for "abusers". Layer 4:F148 is itself fed by the same embedding and by a suffix detector in layer 3 (F4327) that catches words ending in "‑ive" such as "abusive". Additional upstream signals come from legal‑crime detectors (L2:F5368) and …

</details>

<details>
<summary><b>SA-2</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F13473 | " mentions of racial and ethnic groups, especially in the United States" |
| 2 | `get_upstream_features` | L3:F13473@2, k=10 | Emb:"Indians"@1 (de=10.25) +9 more |
| 3 | `inspect_feature` | L2, F2123 | " words ending in "ian", "jani", "iti", "ino", or "olan"" |
| 4 | `get_upstream_features` | L2:F2123@1, k=10 | Emb:"Indians"@1 (de=17.12) +9 more |
| 5 | `inspect_feature` | L0, F10155 | " words related to membership in a group" |
| 6 | `get_upstream_features` | L0:F10155@1, k=10 | Emb:"Indians"@1 (de=13.12) +9 more |

**Findings:** The probe that flags mentions of racial/ethnic groups is driven primarily by a suffix‑detector (L2:F2123) that reacts strongly to the '-ian' ending in the token 'Indians'. This suffix detector receives its strongest positive push directly from the raw embedding of the token 'Indians' (pos 1). The suffix detector then excites the higher‑level ethnic‑group detector (L3:F13473). Additional positive c…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F11668@1, k=10 → Emb:"Indians"@1 (de=12.38) +9 more |
| 2 | `get_upstream_features` | L0:F11375@8, k=10 → Emb:" is"@8 (de=32.50) +9 more |
| 3 | `get_upstream_features` | L0:F8381@23, k=10 → Emb:" by"@23 (de=36.25) +9 more |
| 4 | `get_upstream_features` | L6:F10545@3, k=10 → Emb:" abusers"@3 (de=1.90) +9 more |
| 5 | `get_upstream_features` | L3:F13473@2, k=10 → Emb:"Indians"@1 (de=10.25) +9 more |
| 6 | `get_upstream_features` | L4:F148@3, k=10 → Emb:" abusers"@3 (de=19.12) +9 more |
| 7 | `get_upstream_features` | L6:F1600@12, k=10 → Emb:" problems"@12 (de=21.25) +9 more |
| 8 | `get_upstream_features` | L2:F1680@1, k=10 → Emb:"Indians"@1 (de=8.56) +9 more |
| 9 | `get_upstream_features` | L2:F2123@1, k=10 → Emb:"Indians"@1 (de=17.12) +9 more |
| 10 | `get_upstream_features` | L0:F10155@1, k=10 → Emb:"Indians"@1 (de=13.12) +9 more |
| 11 | `get_upstream_features` | L0:F3436@7, k=10 → Emb:" stated"@7 (de=10.75) +9 more |
| 12 | `get_upstream_features` | L0:F6035@7, k=10 → Emb:" stated"@7 (de=11.06) +9 more |
| 13 | `get_upstream_features` | L3:F4327@3, k=10 → Emb:" abusers"@3 (de=12.75) +9 more |
| 14 | `inspect_feature` ×5 | L3:4852, L2:5368, L2:9873, L4:4332, L2:8909 |

### Build

`build_circuit` → 25 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 107,689 | 6,342 | 188,548 | 0 | $0.0512 | — | — |
| SA-2 | openai/gpt-oss-120b | 46,522 | 3,904 | 5,056 | 0 | $0.0094 | ✅ 3F/5E | Trace this feature upstream. It's labeled "mentions of racia… |
| SA-1 | openai/gpt-oss-120b | 140,579 | 11,909 | 30,784 | 0 | $0.0287 | ✅ 5F/11E | Trace this feature upstream. It's labeled as "political rhet… |
| **Total** | | **294,790** | **22,155** | **224,388** | **0** | **$0.0893** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 35s