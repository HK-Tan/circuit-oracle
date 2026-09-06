# Circuit Oracle Report
**Date:** 2026-07-28 07:22:20 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity score is driven by a stack of identity-group detectors rooted overwhelmingly in the embedding of the single token "Jew" (pos 6), confirming the user's concern: the circuit is identity-term-driven rather than lexically reading the sentence's actual hate-speech content ("stain", "brethren", "country").

**Confidence:** 9

**Reasoning:** The single largest direct_effect into the output probe is **L6:F648** at pos 6 (DE=0.74, act=28.5), an autointerp-labeled "words related to discrimination against particular religious or ethnic groups." Its top upstream node is `Emb: Jew (pos 6)` with DE=19.4 — a *huge* jump that dwarfs every other feature in the graph. F648's other key feeders at pos 6 are the L3 "JEW"-ish caps feature (F12151, DE=5.9, label "capitalized common letter sequences such as SEM, ISM, WF, ISH, WE, SE" — this feature is actually responding to the sub-word "Jew"), the L4 religious-identity feature (F2405, DE=2.95, promoted token `▁Jewish`, frac_nonzero=0.007), the L4 Israel-Palestine feature (F14733, DE=2.36, promoted `▁Palestinian`), and an L4 race/racism feature (F117, DE=1.72, label "terms related to race, racism, and social justice, with a particular focus on terms related to Black people" — note the feature misfires onto "Jew" because the model has bundled identity-discourse into a single circuit).

The second-strongest output-driving feature, **L2:F13158** (DE=0.29, "race/ethnicity words," frac_nonzero=0.0099), also traces directly to `Emb: Jew (pos 6)` with DE=6.8 and to the L0 token amplifier F9026 (which gets DE=31.4 from the "Jew" embedding). L4:F2405 ("religious identity") likewise takes DE=6.75 from `Emb: liberal` and DE=3.78 from `Emb: Jew` — both identity-bearing tokens. The **L8:F13197** ("religion/faith," frac_nonzero=0.014) sends DE=0.143 directly to the probe and traces to the "Jew" embedding (DE=3.45) via L6:F648. L8:F2483 ("slavery, prejudice, disabilities") sends DE=0.174 to the probe and traces to `Emb: hat` (pos 3) and `Emb: Self` (pos 1) — this is the one feature with a real hate-speech lexical route, but its DE is small and its label reveals the "Self-hating" phrasing is being abstracted into a generic prejudice-discourse detector rather than read semantically.

The only feature with a *contentful* (non-identity) route is **L8:F13875** at pos 10 ("negative sentiment: reputation and betrayal of trust," promoted `▁disgraced`, `▁scandal`). It fires on the actual lexical content of the prompt — `Emb: stain (pos 9)` (DE=2.02) — and routes through L6:F1561 ("respect/dignity/pride," DE=3.42 from "stain" + "on"). This is the genuine lexical-semantic component of the circuit. But its DE into the probe is only 0.226, and it carries the toxicity score through an abstract "shame/disgrace" generalization rather than through reading "stain on his brethren and his country" as a coherent derogation.

**Bottom line — the user's concern is confirmed.** Of the top-20 output-driving features, the *vast majority* of total signed influence flows from `Emb: Jew` through F648 → probe (a direct ~0.74 DE), F13158 → probe, F2405 → probe, F14733 → probe, F13197 → probe, and F2483 → probe. The probe is essentially asking "is the word 'Jew' present in a context with religion/race/Palestine-discourse features?" — not "is this sentence actually toxic?" The hate-speech content ("stain," "brethren," "country," "Self-hating liberal") is read mostly by one L8 reputation feature (F13875), which contributes a minority of the probe's signal. The model is performing identity-term short-circuiting: the mere presence of "Jew" plus "liberal" plus an adjacent hate-leaning lexical token is sufficient to push the probe score up, regardless of who is being denigrated or how. This is a classic spurious-correlation failure mode where the toxicity probe has learned a shortcut: "sentence contains [protected-group identity term] + some negative valence = toxic," rather than the actual toxicity structure of the utterance.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: Jew (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: liberal (pos 5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: hat (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: Self (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: stain (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: - (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 6 | L0:F9026 (Jew-token amplifier, pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L1:F14516](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14516) | 3 | L1:F14516 (hat-token, pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14516) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | L2:F13158 (race/ethnicity words, pos 6) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F3588](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3588) | 5 | L2:F3588 (political terms, pos 5) |  terms related to politics and political parties | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3588) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 3 | L3:F592 (love/hate words, pos 3,4) | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F592](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) | 4 | L3:F592 (love/hate words, pos 3,4) | words related to love, affection, and hate, including foreign language | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/592) |
| [L3:F12151](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) | 6 | L3:F12151 (capitalized ISH/EM/WE patterns incl. Jew, pos 6) |  capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH", "WE", "SE" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) |
| [L3:F13819](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13819) | 3 | L3:F13819 (interconnectedness/brethren, pos 3) |  words and phrases about interconnectedness, self-similarity, and things holding together. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13819) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 6 | L4:F2405 (religious identity words, pos 6) |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | L4:F117 (race/racism, Black focus, pos 6) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 3 | L4:F117 (race/racism, Black focus, pos 6) |  terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F14733](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) | 6 | L4:F14733 (Israel-Palestine content, pos 6) |  content related to the Israel-Palestine conflict and possibly some related topics like NBA trades. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) |
| [L6:F648](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) | 6 | L6:F648 (religious/ethnic discrimination words, pos 3,6) |  words related to discrimination against particular religious or ethnic groups | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) |
| [L6:F648](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) | 3 | L6:F648 (religious/ethnic discrimination words, pos 3,6) |  words related to discrimination against particular religious or ethnic groups | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) |
| [L6:F1561](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) | 10 | L6:F1561 (respect/dignity/pride, pos 10) |  words related to respect, status, and pride, both positive and negative | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) |
| [L8:F13875](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) | 10 | L8:F13875 (negative sentiment / reputation-betrayal, pos 10) | negative sentiment related to reputation and betrayal of trust. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) |
| [L8:F13197](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) | 6 | L8:F13197 (religion/faith, pos 6) |  words related to religion and faith | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) |
| [L8:F2483](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) | 3 | L8:F2483 (slavery/prejudice/disability discourse, pos 3) |  discussions of slavery, prejudice, and disabilities | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 6 | Probe score (toxicity direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:648 de=0.738 |
| 3 | `inspect_feature` ×8 | L6:648, L2:13158, L4:2405, L8:13875, L0:9369, L2:3983, L1:1774, L3:592 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F648@6` | ❌ error | — | — | Trace the path from L6:F648 (religious/ethnic discrimination words). Identify wh… |
| SA-2 | `L2:F13158@6` | ❌ error | — | — | Trace the path from L2:F13158 (race/ethnicity words). Identify whether it termin… |
| SA-3 | `L4:F2405@6` | ❌ error | — | — | Trace the path from L4:F2405 (religious identity words). Identify whether it ter… |
| SA-4 | `L8:F13875@10` | ❌ error | — | — | Trace the path from L8:F13875 (negative sentiment: reputation/betrayal). This on… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F648@6, k=15 → Emb:" Jew"@6 (de=19.38) +14 more |
| 2 | `get_upstream_features` | L2:F13158@6, k=15 → Emb:" Jew"@6 (de=6.81) +14 more |
| 3 | `get_upstream_features` | L4:F2405@6, k=15 → Emb:" liberal"@5 (de=6.75) +14 more |
| 4 | `get_upstream_features` | L8:F13875@10, k=15 → L6:F1561 (de=3.42) +14 more |
| 5 | `get_upstream_features` | L3:F12151@6, k=15 → Emb:" Jew"@6 (de=11.00) +14 more |
| 6 | `get_upstream_features` | L4:F117@6, k=15 → L3:F12151 (de=2.80) +14 more |
| 7 | `get_upstream_features` | L3:F13819@3, k=15 → Emb:"Self"@1 (de=13.19) +14 more |
| 8 | `get_upstream_features` | L8:F2483@3, k=15 → L3:F9615 (de=3.08) +14 more |
| 9 | `get_upstream_features` | L2:F3588@5, k=15 → Emb:" liberal"@5 (de=11.44) +14 more |
| 10 | `inspect_feature` ×6 | L3:12151, L3:13819, L8:2483, L2:3588, L4:117, L4:14733 |
| 11 | `get_upstream_features` | L3:F592@3, k=15 → Emb:"hat"@3 (de=14.56) +14 more |
| 12 | `get_upstream_features` | L2:F3588@5, k=15 → Emb:" liberal"@5 (de=11.44) +14 more |
| 13 | `get_upstream_features` | L4:F8407@4, k=15 → Emb:"hat"@3 (de=10.75) +14 more |
| 14 | `get_upstream_features` | L6:F1561@10, k=15 → L5:F7488 (de=6.19) +14 more |
| 15 | `get_upstream_features` | L8:F13197@6, k=15 → L6:F648 (de=5.56) +14 more |
| 16 | `get_upstream_features` | L1:F14516@3, k=15 → Emb:"hat"@3 (de=19.50) +14 more |
| 17 | `get_upstream_features` | L2:F9871@7, k=15 → Emb:" -"@7 (de=25.75) +14 more |
| 18 | `get_upstream_features` | L0:F7460@7, k=15 → Emb:" -"@7 (de=16.38) +14 more |
| 19 | `get_upstream_features` | L5:F7488@10, k=15 → Emb:" stain"@9 (de=6.59) +14 more |
| 20 | `get_upstream_features` | L0:F9026@6, k=15 → Emb:" Jew"@6 (de=31.38) +14 more |
| 21 | `inspect_feature` ×5 | L2:9871, L6:1561, L8:13197, L4:8407, L3:592 |

### Build

`build_circuit` → 22 nodes, 38 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 48,148 | 6,922 | 189,724 | 0 | $0.0341 | — | — |
| **Total** | | **48,148** | **6,922** | **189,724** | **0** | **$0.0341** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 31s