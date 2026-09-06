# Circuit Oracle Report
**Date:** 2026-07-28 07:22:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mix of genuine profession-indicative features (journalism/writer at pos 28) and spurious surface features including the male pronoun "he" (pos 22) and topical phrase "Middle East" (pos 14–15).

**Confidence:** 7

**Reasoning:** The circuit reveals that the probe's classification is NOT purely spurious — it draws on at least one legitimate profession signal. However, the user's concern is partially validated: spurious gender and topical features do contribute substantially.

**Genuine profession signal:** The strongest journalist/writer signal flows from `Emb: writer (pos 28)` and `Emb: freelance (pos 27)` → L4:F13253 ("journalism and the media", activation 7.03) → L8:F8855 ("mentions of news reporters", activation 12.69) → L6:F12712 ("titles of editors and publishers", activation 8.69) → L14:F4420 ("words and phrases related to journalism and newspapers", activation 23.13). L14:F4420 has a direct_effect of −0.0679 (inhibitory) on the probe, while L8:F8855 contributes +3.70 to it. These features trace unambiguously to the word "writer" — a genuine profession marker.

**Spurious signals:** The single largest direct-effect feature on the probe is L0:F7124 (the word "at" at pos 2, direct_effect −0.157) — this is a pure function word. More concerning is L0:F12768 ("mentions of 'he' and 'she' in close proximity", frac_nonzero 0.011) at pos 22, which has direct_effect +0.0747 and traces directly to `Emb: he (pos 22)` (direct_effect 40.25). This is a gender-pronoun feature acting as a proxy signal. The "Middle East" features (L0:F3007 "middle" +0.060, L2:F12901 "Middle East" phrase, L0:F1229 "middle/shake" +0.057) fire on topical content, not profession.

**Verdict:** The probe uses BOTH genuine profession features (writer/journalism cluster at pos 28) AND spurious features (gender pronoun "he", topical "Middle East", function word "at"). The user's concern is valid — the gender marker is the third-largest positive direct contributor — but the circuit is not purely spurious; the journalism feature chain at the token "writer" is the most semantically coherent path. The probe is partially well-calibrated to the journalism profession but contaminated by co-occurring surface cues.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 28 | Probe direction (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | L14: Journalism/newspaper features (pos 28, 'writer') | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 28 | L14: Journalism/newspaper features (pos 28, 'writer') |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | L14: Journalism/newspaper features (pos 28, 'writer') |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 28 | L14: Journalism/newspaper features (pos 28, 'writer') |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | L0: 'he' pronoun feature (pos 22) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F3007](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) | 14 | L0/L2: 'Middle East' and related phrases (pos 14, 15) |  the word "middle", and sometimes the word "character", and "camp" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) |
| [L2:F12901](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12901) | 15 | L0/L2: 'Middle East' and related phrases (pos 14, 15) |  the phrase "Middle East" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12901) |
| [L0:F1229](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1229) | 14 | L0/L2: 'Middle East' and related phrases (pos 14, 15) |  the word "shake," and words related to the middle of something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1229) |
| [L0:F2348](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2348) | 4 | L0/L2: 'Middle East' and related phrases (pos 14, 15) |  the word "rapid" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2348) |
| [L0:F7124](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) | 2 | L0: Generic context word features (pos 2, 7, 12) | the word "at" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) |
| [L0:F10881](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) | 12 | L0: Generic context word features (pos 2, 7, 12) |  the word "coverage" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) |
| [L0:F9297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) | 7 | L0: Generic context word features (pos 2, 7, 12) |  mentions of government ministries and ministers. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) |
| [L0:F6484](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6484) | 7 | L0: Generic context word features (pos 2, 7, 12) |  the word "sky" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6484) |
| [L1:F4459](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) | 7 | L0: Generic context word features (pos 2, 7, 12) |  mentions of research institutes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) |
| [L3:F10489](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10489) | 7 | L0: Generic context word features (pos 2, 7, 12) |  the word "Institute" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10489) |
| [L1:F1445](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1445) | 7 | L0: Generic context word features (pos 2, 7, 12) |  terms related to the military, especially vehicles and weapons | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1445) |
| [L0:F15661](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) | 7 | L0: Generic context word features (pos 2, 7, 12) | the word "spin" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 22 | Emb: he (pos 22) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: Middle (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: East (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 28 | Emb: writer (pos 28) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: freelance (pos 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: Institute (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: covering (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: at (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:7124 de=-0.157 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F12768@22` | ❌ error | — | — | Trace L0:F12768 at pos 22. This is the strongest positive driver of the probe cl… |
| SA-2 | `L0:F3007@14` | ❌ error | — | — | Trace L0:F3007 at pos 14. Second strongest positive driver. What does this featu… |
| SA-3 | `L0:F10881@12` | ❌ error | — | — | Trace L0:F10881 at pos 12. Third positive driver. What does this feature encode?… |
| SA-4 | `L0:F9297@7` | ❌ error | — | — | Trace L0:F9297 at pos 7. Fourth positive driver. What does this feature encode? … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×15 | L0:12768, L0:3007, L0:10881, L0:9297, L0:7124, L0:15661, L0:6484, L0:2348, L0:1229, L1:4459, L3:10489, L1:1445, L2:12901, L6:12712, L14:4420 |
| 2 | `get_upstream_features` | L0:F12768@22, k=5 → Emb:" he"@22 (de=40.25) +4 more |
| 3 | `get_upstream_features` | L0:F3007@14, k=5 → Emb:" Middle"@14 (de=20.75) +4 more |
| 4 | `get_upstream_features` | L14:F4420@28, k=5 → Emb:" writer"@28 (de=5.75) +4 more |
| 5 | `get_upstream_features` | L2:F12901@15, k=5 → Emb:" East"@15 (de=26.75) +4 more |
| 6 | `get_upstream_features` | L8:F8855@28, k=5 → Emb:" writer"@28 (de=4.72) +4 more |
| 7 | `get_upstream_features` | L4:F13253@28, k=5 → Emb:" writer"@28 (de=9.12) +4 more |
| 8 | `inspect_feature` ×2 | L8:8855, L4:13253 |
| 9 | `get_upstream_features` | L0:F10881@12, k=3 → Emb:" covering"@12 (de=16.25) +2 more |
| 10 | `get_upstream_features` | L0:F9297@7, k=3 → Emb:" Institute"@7 (de=11.81) +2 more |
| 11 | `get_upstream_features` | L0:F7124@2, k=3 → Emb:" at"@2 (de=31.38) +2 more |
| 12 | `get_upstream_features` | L1:F4459@7, k=3 → Emb:" Institute"@7 (de=27.50) +2 more |
| 13 | `get_upstream_features` | L14:F4420@28, k=8 → Emb:" writer"@28 (de=5.75) +7 more |
| 14 | `get_upstream_features` | L6:F12712@28, k=5 → Emb:" writer"@28 (de=6.22) +4 more |

### Build

`build_circuit` → 13 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 39,936 | 4,744 | 233,282 | 0 | $0.0317 | — | — |
| **Total** | | **39,936** | **4,744** | **233,282** | **0** | **$0.0317** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 32s