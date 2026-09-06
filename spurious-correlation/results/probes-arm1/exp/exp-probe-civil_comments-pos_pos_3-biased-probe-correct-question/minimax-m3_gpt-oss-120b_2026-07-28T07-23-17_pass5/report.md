# Circuit Oracle Report
**Date:** 2026-07-28 07:23:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven almost entirely by the token `Jew` (pos 6) activating a stack of identity-group features — race/ethnicity (L2:F13158, +0.29), religious identity (L4:F2405, +0.24), Israel/Palestine context (L4:F14733), and culminating in the top driver L6:F648 "discrimination vs religious/ethnic groups" (+0.74) — with secondary contributions from `stain` (pos 9) feeding a "reputation/betrayal" path (L8:F13875, +0.23), while off-token subword artifacts (`hat`, ` -`, LaTeX patterns) and the suppression-leaning L3:Latex feature dilute rather than construct the score.

**Confidence:** 8

**Reasoning:** The circuit traces cleanly to embedding nodes. The dominant supernode `discrim_l6` (L6:F648, direct_effect=+0.74, frac_nonzero=0.016) is essentially a single-token detector for `Jew` — its #1 upstream node is the ` Jew` embedding at pos 6 with direct_effect=19.4, and the next strongest inputs are the identity-cluster letter/suffix feature L3:F12151 (also "JE/JEW" pattern, frac_nonzero=0.003) and L4:F14733 ("Israel-Palestine conflict", promoted_tokens include Palestinian/Palestine). L2:F13158 ("race/ethnicity words", +0.29) and L4:F2405 ("religious identity/affiliation", +0.24) at the same position reinforce the same `Jew` signal. The user is correct: the probe treats the *presence* of an identity-group token (`Jew`, `liberal`) as a near-sufficient signal of toxicity, rather than reading the pejorative verb "stain" or the negative framing "Self-hating … a stain on his brethren and his country." Notably, the "stain" path does exist (Emb ` stain` → L5:F7488 "legal language/stains" → L6:F1561 "respect/status/pride" → L8:F13875 "reputation/betrayal", total ~+0.23) but it is dwarfed by the identity-token path (~+1.3 in direct effects on the top feature alone). Off-target subword noise (L1:F1774 "LaTeX text", L2:F3983 "hat" substring) actually pushes the probe score *negatively* (-0.20, -0.20) because the token `hat` inside "hating" looks like the common English word "hat" / a LaTeX command `\hat` to low-level features. The mechanism is: **identity-token → identity-feature stack → probe**, with the actual insulting semantics ("stain", "Self-hating", "brethren") playing a secondary role. This confirms the user's concern that the probe latches on to *group-mention* features rather than toxic content.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 6 | L0-F9026: 'jew' letter fragment (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F9369](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9369) | 7 | L0-F9369: subtraction symbol ' -' (pos 7) |  subtraction symbols | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9369) |
| [L0:F8736](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8736) | 3 | L0-F8736: 'hat' token (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8736) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 6 | L2-F13158: 'race/ethnicity words' (pos 6, +0.29) |  words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F3983](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3983) | 3 | L2-F3983: 'hat' substring detector (pos 3, -0.20) | the word "hat" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3983) |
| [L1:F1774](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1774) | 3 | L1-F1774: LaTeX text (pos 3, -0.20) |  text in a Latex document | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1774) |
| [L3:F12151](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) | 6 | L3-F12151: 'JE/JEW' letter pattern (pos 6) |  capitalized common letter sequences such as "SEM", "ISM", "WF", "ISH", "WE", "SE" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12151) |
| [L3:F13819](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13819) | 3 | L3-F13819: 'interconnectedness/together' (pos 3, +0.17) |  words and phrases about interconnectedness, self-similarity, and things holding together. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13819) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 6 | L4-F2405: religious identity words (pos 6, +0.24) |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L4:F14733](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) | 6 | L4-F14733: Israel-Palestine conflict (pos 6) |  content related to the Israel-Palestine conflict and possibly some related topics like NBA trades. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14733) |
| [L4:F8407](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) | 4 | L4-F8407: antagonists/fighting (pos 4, +0.16) |  words related to antagonists and fighting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8407) |
| [L6:F648](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) | 6 | L6-F648: discrimination vs religious/ethnic groups (pos 6, +0.74) |  words related to discrimination against particular religious or ethnic groups | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/648) |
| [L5:F7488](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7488) | 10 | L5-F7488: legal language / 'stain/stains' (pos 10) |  legal language, specifically terms related to evidence and accusations | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7488) |
| [L6:F1561](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) | 10 | L6-F1561: respect/status/pride words (pos 10) |  words related to respect, status, and pride, both positive and negative | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1561) |
| [L8:F13875](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) | 10 | L8-F13875: negative sentiment, reputation/betrayal (pos 10, +0.23) | negative sentiment related to reputation and betrayal of trust. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13875) |
| [L8:F13197](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) | 6 | L8-F13197: religion/faith words (pos 6, +0.14) |  words related to religion and faith | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) |
| [L8:F2483](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) | 3 | L8-F2483: slavery/prejudice/disability (pos 3, +0.17) |  discussions of slavery, prejudice, and disabilities | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2483) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:648 de=0.738 |
| 3 | `inspect_feature` ×6 | L6:648, L2:13158, L4:2405, L8:13875, L2:3983, L1:1774 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F648@6` | ❌ error | — | — | Trace the upstream path from L6:F648 (label: "words related to discrimination ag… |
| SA-2 | `L8:F13875@10` | ❌ error | — | — | Trace the upstream path from L8:F13875 (label: "negative sentiment related to re… |
| SA-3 | `L2:F13158@6` | ❌ error | — | — | Trace the upstream path from L2:F13158 (label: "words about race and ethnicity",… |
| SA-4 | `L4:F2405@6` | ❌ error | — | — | Trace the upstream path from L4:F2405 (label: "words related to religious identi… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F648@6, k=15 → Emb:" Jew"@6 (de=19.38) +14 more |
| 2 | `get_upstream_features` | L2:F13158@6, k=15 → Emb:" Jew"@6 (de=6.81) +14 more |
| 3 | `get_upstream_features` | L4:F2405@6, k=15 → Emb:" liberal"@5 (de=6.75) +14 more |
| 4 | `get_upstream_features` | L8:F13875@10, k=15 → L6:F1561 (de=3.42) +14 more |
| 5 | `get_upstream_features` | L3:F12151@6, k=10 → Emb:" Jew"@6 (de=11.00) +9 more |
| 6 | `get_upstream_features` | L4:F14733@6, k=10 → Emb:" Jew"@6 (de=5.47) +9 more |
| 7 | `get_upstream_features` | L4:F117@6, k=10 → L3:F12151 (de=2.80) +9 more |
| 8 | `get_upstream_features` | L6:F1561@10, k=10 → L5:F7488 (de=6.19) +9 more |
| 9 | `get_upstream_features` | L5:F7488@10, k=10 → Emb:" stain"@9 (de=6.59) +9 more |
| 10 | `get_upstream_features` | L0:F9369@7, k=10 → Emb:" -"@7 (de=21.50) +9 more |
| 11 | `get_upstream_features` | L3:F592@3, k=10 → Emb:"hat"@3 (de=14.56) +9 more |
| 12 | `get_upstream_features` | L2:F3983@3, k=10 → Emb:"hat"@3 (de=25.12) +9 more |
| 13 | `inspect_feature` ×12 | L3:12151, L4:14733, L6:1561, L5:7488, L3:13819, L4:8407, L8:13197, L8:2483, L0:9369, L0:7460, L2:9871, L2:3588 |

### Build

`build_circuit` → 23 nodes, 29 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 69,533 | 6,593 | 128,462 | 0 | $0.0365 | — | — |
| **Total** | | **69,533** | **6,593** | **128,462** | **0** | **$0.0365** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 26s