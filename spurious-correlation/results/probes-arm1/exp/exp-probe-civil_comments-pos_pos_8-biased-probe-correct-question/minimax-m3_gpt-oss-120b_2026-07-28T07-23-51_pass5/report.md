# Circuit Oracle Report
**Date:** 2026-07-28 07:23:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_8 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven primarily by a chain of Islam/religion-identity features anchored to the embedding of the word "Islam" (pos 4), with secondary contributions from generic religion/faith features, "problem with X" structural context, and a late-layer generic "negative-language-denigrating-groups" feature — identity-group signal, not slur or invective content, dominates the score.

**Confidence:** 8

**Reasoning:** The top features driving the probe are all religion- or Islam-anchored identity detectors, not toxicity or slur detectors. The single largest contributor is L6:F7282 ("mentions of Islam or Middle Eastern places and people", frac_nonzero=0.007, direct_effect=0.41), fed at pos 4 by the embedding of "Islam" itself (direct_effect 18.5 to F7282, 21.5 to F2405). L4:F2405 ("religious identity/affiliation", direct_effect=0.32), L8:F13197 ("religion and faith", direct_effect=0.26), L6:F3265 ("religion, religious figures, and related concepts"), L6:F8487 ("terrorism, security, policing"), L7:F14049 ("international political conflicts… regarding Muslims, slavery, race, terrorism"), L7:F12448 ("religion"), and L10:F2716 ("religion, faith, parenting, family") form a vertical religion-identity stack that propagates "Islam" → "religion" → "Muslim" → "religion-related discourse" from the input embedding upward into the probe direction. The early-layer L0:F13885 ("names of people and places, specifically those related to the middle east") and L1:F4314 ("the word Muslim") plus L2:F7214 ("countries or regions associated with Islam") confirm the signal originates from identity terms in the prompt.

The other branch is structural, not invective: L0:F14656 ("problem") and L0:F880 ("it") supply the "X is the problem with Y" construction, reinforced by L3:L4 problem/issue/advantage features (F14698, F4011, F15997) — these fire on the assertion-frame "The problem with Islam is…" rather than on a slur.

Crucially, the actual denigrating content ("false", "Lucifer") is only weakly represented: only L12:F7779 ("negative language denigrating groups of people", direct_effect=0.14) at pos 10 ("false") enters the top, and it is a *generic* group-denigration detector, not a religion-specific slur or profanity feature. There is no "Lucifer/Satan" feature, no profanity feature, and no "false religion" feature visible at the top of the ranking. The probe's score is dominated by a stack whose first hop is the bare "Islam" embedding and whose intermediate layers are religion- and Islam-specific identity detectors.

This confirms the user's concern: the probe uses spurious identity-group signals (specifically Islam/Muslim/religion features) rather than actual prompt-level toxicity content (slurs, profanity, or denigrating lexical content) to drive its classification. The "Islam" token alone, independent of any invective, would substantially activate this circuit. Replacing "Islam" with any other religion/identity term would likely produce a similar high probe score, demonstrating the bias.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: Islam (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: Allah (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: . (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: problem (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: it (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: false (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F13885](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) | 4 | Early-layer Islam-identity features (L0–L2) |  names of people and places, specifically those related to the middle east | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) |
| [L0:F13885](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) | 13 | Early-layer Islam-identity features (L0–L2) |  names of people and places, specifically those related to the middle east | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13885) |
| [L1:F4314](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4314) | 4 | Early-layer Islam-identity features (L0–L2) |  the word Muslim | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4314) |
| [L1:F2352](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2352) | 4 | Early-layer Islam-identity features (L0–L2) |  words associated with Islam | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2352) |
| [L2:F7214](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7214) | 4 | Early-layer Islam-identity features (L0–L2) |  references to countries or regions associated with Islam | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7214) |
| [L2:F15887](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15887) | 13 | Early-layer Islam-identity features (L0–L2) |  Arabic words mentioning Allah and Quranic passages | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15887) |
| [L1:F2235](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2235) | 13 | Early-layer Islam-identity features (L0–L2) |  passages from the Quran | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2235) |
| [L3:F12024](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) | 4 | Mid-layer religion/identity features (L3–L6) |  words referencing the religion of Islam, people who practice it, and Arabic names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12024) |
| [L4:F2405](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) | 4 | Mid-layer religion/identity features (L3–L6) |  words related to religious identity/affiliation or spirituality including related holidays | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2405) |
| [L5:F6331](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6331) | 4 | Mid-layer religion/identity features (L3–L6) |  words about race, religion, and slavery | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6331) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 4 | Mid-layer religion/identity features (L3–L6) |  mentions of Islam or Middle Eastern places and people, as well as mentions of a specific district. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L6:F7282](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) | 13 | Mid-layer religion/identity features (L3–L6) |  mentions of Islam or Middle Eastern places and people, as well as mentions of a specific district. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/7282) |
| [L6:F5764](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5764) | 4 | Mid-layer religion/identity features (L3–L6) | various proper nouns and adjectives, including ethnic groups, nationalities, religions, job titles, deities, and locations. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5764) |
| [L6:F3265](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3265) | 4 | Mid-layer religion/identity features (L3–L6) |  religion, religious figures, and related concepts and groups | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3265) |
| [L6:F8487](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8487) | 4 | Mid-layer religion/identity features (L3–L6) |  words and phrases related to terrorism, security, and policing. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8487) |
| [L0:F14656](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14656) | 2 | Mid-layer problem/issue context (L3–L4) |  the word "problem" and words associated with it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14656) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 12 | Mid-layer problem/issue context (L3–L4) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L3:F14698](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14698) | 3 | Mid-layer problem/issue context (L3–L4) | expressions of disagreement or problems with something | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14698) |
| [L4:F4011](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4011) | 3 | Mid-layer problem/issue context (L3–L4) |  words and phrases related to challenges, advantages, and other main points | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4011) |
| [L4:F15997](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15997) | 3 | Mid-layer problem/issue context (L3–L4) |  discussion of advantages and/or disadvantages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15997) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 7 | Mid-layer problem/issue context (L3–L4) |  references to the pronoun "it", and sometimes "that", suggesting observation of the subject of a discussion | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |
| [L7:F12448](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12448) | 4 | Late-layer religion/identity features (L7–L10) | words and phrases related to religion | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/12448) |
| [L7:F14049](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14049) | 4 | Late-layer religion/identity features (L7–L10) |  discussion of international political conflicts, especially those regarding Muslims, slavery, race, terrorism and cultural groups. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14049) |
| [L8:F13197](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) | 4 | Late-layer religion/identity features (L7–L10) |  words related to religion and faith | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13197) |
| [L10:F2716](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/2716) | 4 | Late-layer religion/identity features (L7–L10) | mentions of religion, faith, parenting, and family when they appear together. | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/2716) |
| [L12:F7779](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/7779) | 10 | Late-layer negative-group-denigration feature (L12) |  negative language denigrating groups of people | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/7779) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:7282 de=0.410 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F7282@4` | ❌ error | — | — | Trace L6:F7282 (pos 4) upstream. This is the top feature driving the probe (dire… |
| SA-2 | `L4:F2405@4` | ❌ error | — | — | Trace L4:F2405 (pos 4) upstream. This is the #2 feature driving the probe (direc… |
| SA-3 | `L8:F13197@4` | ❌ error | — | — | Trace L8:F13197 (pos 4) upstream (direct_effect=0.26). Determine what it encodes… |
| SA-4 | `L6:F7282@13` | ❌ error | — | — | Trace L6:F7282 at pos 13 (direct_effect=0.15) — the same feature index as the to… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L6:7282, L4:2405, L8:13197, L0:6051 |
| 2 | `get_upstream_features` | L6:F7282@4, k=15 → Emb:" Islam"@4 (de=18.50) +14 more |
| 3 | `get_upstream_features` | L4:F2405@4, k=15 → Emb:" Islam"@4 (de=21.50) +14 more |
| 4 | `get_upstream_features` | L8:F13197@4, k=15 → Emb:" Islam"@4 (de=9.25) +14 more |
| 5 | `get_upstream_features` | L0:F13885@4, k=10 → Emb:" Islam"@4 (de=12.25) +9 more |
| 6 | `get_upstream_features` | L3:F12024@4, k=10 → Emb:" Islam"@4 (de=8.44) +9 more |
| 7 | `get_upstream_features` | L0:F6051@12, k=10 → Emb:"."@12 (de=46.50) +9 more |
| 8 | `get_upstream_features` | L0:F14656@2, k=10 → Emb:" problem"@2 (de=16.38) +9 more |
| 9 | `inspect_feature` ×2 | L0:13885, L3:12024 |
| 10 | `get_upstream_features` | L0:F14656@2, k=10 → Emb:" problem"@2 (de=16.38) +9 more |
| 11 | `inspect_feature` | L0, F14656 → " the word "problem" and words associated with it" |
| 12 | `get_upstream_features` | L0:F880@7, k=10 → Emb:" it"@7 (de=44.00) +9 more |
| 13 | `inspect_feature` ×9 | L0:880, L4:15997, L4:4011, L7:12448, L7:14049, L12:7779, L1:4314, L0:9026, L0:2158 |
| 14 | `get_upstream_features` | L6:F7282@13, k=10 → Emb:" Allah"@13 (de=15.81) +9 more |
| 15 | `inspect_feature` ×6 | L1:2235, L6:8487, L6:5764, L6:3265, L10:2716, L5:6331 |
| 16 | `get_upstream_features` | L0:F9026@4, k=8 → Emb:" Islam"@4 (de=17.62) +7 more |
| 17 | `get_upstream_features` | L4:F15997@3, k=8 → L3:F14698 (de=3.64) +7 more |
| 18 | `get_upstream_features` | L12:F7779@10, k=8 → Emb:" false"@10 (de=7.16) +7 more |
| 19 | `inspect_feature` ×4 | L3:14698, L3:8595, L3:1395, L8:16036 |
| 20 | `get_upstream_features` | L4:F4011@3, k=5 → Emb:"The"@1 (de=6.69) +4 more |
| 21 | `get_upstream_features` | L6:F5764@4, k=8 → Emb:" Islam"@4 (de=4.50) +7 more |
| 22 | `get_upstream_features` | L6:F8487@4, k=8 → Emb:" Islam"@4 (de=6.84) +7 more |
| 23 | `get_upstream_features` | L6:F3265@4, k=8 → Emb:" Islam"@4 (de=6.12) +7 more |
| 24 | `get_upstream_features` | L10:F2716@4, k=8 → Emb:" Islam"@4 (de=3.03) +7 more |
| 25 | `inspect_feature` ×6 | L6:2267, L2:7214, L1:2352, L1:12107, L4:7696, L2:15887 |

### Build

`build_circuit` → 12 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 78,363 | 6,044 | 376,306 | 0 | $0.0533 | — | — |
| **Total** | | **78,363** | **6,044** | **376,306** | **0** | **$0.0533** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 54s