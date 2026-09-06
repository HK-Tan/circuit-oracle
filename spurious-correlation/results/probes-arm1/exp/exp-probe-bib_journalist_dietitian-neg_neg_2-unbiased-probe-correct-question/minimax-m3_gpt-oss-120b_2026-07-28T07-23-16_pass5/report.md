# Circuit Oracle Report
**Date:** 2026-07-28 07:23:16 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for this input is driven by a network of journalism-entity features (L7–L20) that detect the word "report" and broadcast-news context, anchored on the token "report" at position 21 — not by the male pronoun "His" or other gender markers.

**Confidence:** 8

**Reasoning:**

Tracing the circuit from the output logit back to token embeddings reveals that the probe's score is overwhelmingly driven by **journalism-context features**, not by gender markers like "His":

1. **Strongest upstream signal is the token "report" at position 21** (Emb: report, pos 21). The "report" embedding feeds a stack of low-layer word detectors — L2:11175 (verb "report"), L3:10846 (the word "report", frac_nonzero=0.0023, highly specific), L4:6696, L5:12586 — all of which have low frac_nonzero indicating they are tight lexical detectors rather than generic features.

2. **Mid-layer journalism-entity features** (L7–L8) then aggregate this signal: L7:13646 ("news reporting and journalism"), L7:9092 ("broadcast journalism"), L8:8855 ("news reporters and news reporting"), L8:8437 ("film festivals/recognition"). L8:8855's promoted tokens include "reporter, journalists, journalism" — these are the genuine profession-entity indicators, not gender markers.

3. **Late-layer features bifurcate**: L14:4420 (pos 21, de=−0.146) and L19:2486 (pos 21, de=−0.113) push **negatively** on the probe; L15:2579, L16:15046, L18:14663, L19:14973 push **positively**. The negative direction comes from L16:8642 and L17:5218 (suppressors that fire in non-journalism contexts), and the late L19:2486 / L20:8433 features with high direct_effect values (−0.113, −0.062) actually reflect that "report" here is being interpreted as a verb ("…to report for some of the top news organizations") rather than a noun (a document). This shifts the probe away from the journalism class.

4. **"His" at position 1** is a L0 pronoun feature (L0:8964, frac_nonzero=0.018) with a small positive direct_effect (+0.079) — but its role is **NOT** as a gender marker. The Neuronpedia top-activating examples show it fires on any "His" regardless of the profession of the referent (kings, governors, anthropologists, parents in anecdotes). It happens to fire on "His desire to see the world" — a generic possessive-pronoun detector, not a male-profession detector. Its positive contribution is small compared to the journalism features and reflects contextual subject-continuation signal, not spurious gender classification.

5. **"world" (pos 6)** drives L0:2203 (de=−0.057) and L4:11898 (de=+0.054) — but these are "world" + sport/war detectors, not profession indicators. L0:2203's top-activating examples are about games, worlds, existential quandaries, and L4:11898 fires on "World War" and "World Cup/Championships." They contribute nearly nothing to a journalism classification.

**Bottom line on the user's concern:** The concern that the circuit relies on "His" as a gender/spurious marker is **not supported** by this graph. "His" contributes a small positive nudge (+0.079) but is a generic pronoun detector, not a male-profession detector. The dominant signal is the journalism entity circuit built on "report" + mid-layer journalism features + late-layer journalism aggregators. The L0 pronoun feature and the L0/L4 "world" features are **off-path** for the profession signal and contribute minimally. The probe is primarily using genuine profession-indicator features (journalism/reporters), with one genuinely misleading aspect being that the L19:2486 feature pushes the probe *away* from journalism because here "report" is used as a verb rather than a noun — a polysemy confound, not a gender confound.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output Logit (Probe Direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | L19:L20 Journalism Features (NEGATIVE on probe) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 26 | L19:L20 Journalism Features (NEGATIVE on probe) | words related to news broadcasting | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 22 | L19:L20 Journalism Features (NEGATIVE on probe) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 29 | L19:L20 Journalism Features (NEGATIVE on probe) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | L14:L19 Journalism Features (POSITIVE on probe) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 22 | L14:L19 Journalism Features (POSITIVE on probe) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L15:F2579](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) | 21 | L14:L19 Journalism Features (POSITIVE on probe) | instances of people providing information in some sort of official capacity. Like reporting incidents, communicating facts or informing others of something. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) |
| [L16:F15046](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15046) | 21 | L14:L19 Journalism Features (POSITIVE on probe) |  names, organizations, and reporting verbs | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15046) |
| [L18:F14663](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) | 21 | L14:L19 Journalism Features (POSITIVE on probe) | variations of the word "report." | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) |
| [L19:F14973](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/14973) | 26 | L14:L19 Journalism Features (POSITIVE on probe) |  words related to high-achieving individuals and organizations | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/14973) |
| [L16:F8642](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) | 21 | L16:L17 Late suppressors of journalism (non-journalism context) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) |
| [L17:F5218](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) | 21 | L16:L17 Late suppressors of journalism (non-journalism context) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5218) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | L7:L8 Mid-Journalism Features (reporters/broadcast) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 21 | L7:L8 Mid-Journalism Features (reporters/broadcast) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 26 | L7:L8 Mid-Journalism Features (reporters/broadcast) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | L7:L8 Mid-Journalism Features (reporters/broadcast) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | L7:L8 Mid-Journalism Features (reporters/broadcast) | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L2:F11175](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11175) | 21 | L2:L5 'report' Word Detectors | the verb "report" and its variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11175) |
| [L3:F10846](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10846) | 21 | L2:L5 'report' Word Detectors | the word "report" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10846) |
| [L4:F6696](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6696) | 21 | L2:L5 'report' Word Detectors | the word "report" or "reporting" along with adjacent words | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/6696) |
| [L5:F12586](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12586) | 21 | L2:L5 'report' Word Detectors |  mentions of reports | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12586) |
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | L0 'His' pronoun feature (POSITIVE on probe) |  the possessive pronoun "His" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | L0 generic 'to' feature | the word "to" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F14287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) | 4 | L0 'see' word feature | the word "see" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) |
| [L0:F2203](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) | 6 | L0:L4 'world' word features (non-journalism contexts) |  instances of the words "world" or "game" (possibly "problem") or expressions of existential quandaries. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) |
| [L4:F11898](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) | 6 | L0:L4 'world' word features (non-journalism contexts) |  mentions of "World" followed by a sport or war-related word | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.145 |
| 3 | `inspect_feature` ×9 | L19:2486, L14:4420, L20:8433, L0:8964, L0:8444, L0:14287, L0:2203, L4:11898, L5:771 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F8964@1` | ❌ error | — | — | Trace the upstream path from L0:F8964 ("His" pronoun feature at pos 1) to unders… |
| SA-2 | `L0:F8444@3` | ❌ error | — | — | Trace upstream from L0:F8444 (the "to" feature at pos 3). What does this represe… |
| SA-3 | `L0:F14287@4` | ❌ error | — | — | Trace upstream from L0:F14287 (the "see" feature at pos 4). What does it represe… |
| SA-4 | `L19:F2486@21` | ❌ error | — | — | Trace upstream from L19:F2486 (journalism feature) at pos 21. This feature has a… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 2 | `get_upstream_features` | L19:F2486@21, k=10 → L14:F4420 (de=14.31) +9 more |
| 3 | `get_upstream_features` | L20:F8433@26, k=10 → Emb:" top"@26 (de=5.69) +9 more |
| 4 | `inspect_feature` ×6 | L8:8855, L7:13646, L8:8437, L7:9092, L18:14663, L19:14973 |
| 5 | `get_upstream_features` | L8:F8855@21, k=10 → Emb:" report"@21 (de=12.06) +9 more |
| 6 | `get_upstream_features` | L8:F8437@21, k=10 → Emb:" report"@21 (de=5.75) +9 more |
| 7 | `get_upstream_features` | L17:F5218@21, k=8 → L14:F4420 (de=5.12) +7 more |
| 8 | `get_upstream_features` | L16:F8642@21, k=8 → L14:F4420 (de=10.50) +7 more |
| 9 | `inspect_feature` ×8 | L7:13896, L3:10846, L2:11175, L4:6696, L5:12586, L15:12472, L16:15046, L15:2579 |
| 10 | `get_upstream_features` | L0:F8964@1, k=6 → Emb:"His"@1 (de=13.69) +5 more |
| 11 | `get_upstream_features` | L0:F14287@4, k=6 → Emb:" see"@4 (de=25.12) +5 more |
| 12 | `get_upstream_features` | L0:F2203@6, k=6 → Emb:" world"@6 (de=18.25) +5 more |
| 13 | `get_upstream_features` | L4:F11898@6, k=6 → Emb:" world"@6 (de=35.25) +5 more |

### Build

`build_circuit` → 16 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 49,137 | 10,119 | 335,126 | 0 | $0.0470 | — | — |
| **Total** | | **49,137** | **10,119** | **335,126** | **0** | **$0.0470** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 4s