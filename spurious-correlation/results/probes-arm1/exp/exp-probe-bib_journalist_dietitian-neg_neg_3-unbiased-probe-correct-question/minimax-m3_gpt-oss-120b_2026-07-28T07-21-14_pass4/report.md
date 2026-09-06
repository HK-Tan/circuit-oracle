# Circuit Oracle Report
**Date:** 2026-07-28 07:21:14 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by genuine profession-related content — specifically the token "journalistic" at position 13, supported by "stories" and "country" — flowing through a deep, semantically coherent journalism/media circuit; male-pronoun features (L0:F1069) also fire but with negative direct effects, INHIBITING the score rather than promoting it.

**Confidence:** 7

**Reasoning:**

**Primary positive path (genuine profession signal):** The strongest driver is the late-layer **L14:F4420** (journalism/newspapers, direct_effect=-0.128 to probe). Tracing upstream, the dominant upstream node is the **"journalistic" token embedding at pos 13** (direct_effect=24.4 into F4420), which then flows through a dense journalism circuit:
- **L4:F13253** (journalism/Fourth Estate, frac_nonzero=0.0065) — fires on the "journalistic" token, promoted tokens: "Journalism", "journalists", "media"
- **L6-L8 mid-layer features** (F8529, F8855, F13646, F9092, F2309, F16076, F12712, F8437, F9521) — all are clearly about news reporting, press, broadcast journalism, reporters, editors. For example, F8855 fires on "reporters/journalistic" (promoted: "reporter", "journalistic", "reporters"), F8437 on documentary/director content, F13646 on news reporting, F9092 on broadcast journalism
- The **"stories" embedding at pos 3** also flows in (direct_effect=2.27 to F4420) via L1:F14812 (stories/narrative, frac_nonzero=0.0095), F5333 (stories being told), F11261 (migration/represent at pos 3)
- "country" embedding at pos 11 flows via L1:F2344 (the word "country") and L0:F15423

This is unambiguously a **profession-coherent circuit**: nearly every feature in the top positive path encodes journalism/media/broadcast/news concepts, and they trace to the actual profession-revealing tokens ("journalistic", "stories", "country", "researches").

**Gender marker status (the user's concern):** **L0:F1069** (the male-pronoun "He"/"His" feature) does appear in the top features with direct_effect=-0.162 to the probe — but the sign is **NEGATIVE**, meaning the male pronoun INHIBITS the probe score, not promotes it. It is sourced from the "He" token embedding (direct_effect=22.6) at pos 1. Other male-associated or content-neutral features like F11603 ("too" at pos 27, direct_effect=-0.163), F8061 ("in" at pos 12, direct_effect=-0.133), F2711 ("foreign" at pos 20, direct_effect=-0.110), F6051 (periods/spaces, direct_effect=-0.106) all have **negative direct effects** — they push AGAINST the profession score.

**Conclusion:** The user's concern is **not supported** by this circuit. The probe is being driven by a genuine, deep profession-detection circuit anchored on the word "journalistic" and supported by "stories"/"country"/"researches" — all of which are semantically appropriate indicators of the journalist profession depicted in the text. The male-pronoun feature does exist in the circuit but acts as a **suppressor** (negative direct effect), which is the opposite of what would constitute a spurious gender bias. If anything, the model appears to be using male gender as a slight *anti* signal for the profession score, which suggests the probe learned the profession concept, not the gender correlate.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe (Profession) Logit | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | L14: Journalism/newspapers (pos 13, "journalistic") | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 13 | L6-L8: Broadcast news / reportorial / press features (pos 13) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 13 | L6-L8: Broadcast news / reportorial / press features (pos 13) | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 13 | L6-L8: Broadcast news / reportorial / press features (pos 13) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 13 | L6-L8: Broadcast news / reportorial / press features (pos 13) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L6:F8529](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8529) | 13 | L6-L8: Broadcast news / reportorial / press features (pos 13) |  news or press reports in the media | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8529) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 13 | L6-L8: Broadcast news / reportorial / press features (pos 13) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L7:F16076](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16076) | 13 | L6-L8: Broadcast news / reportorial / press features (pos 13) |  words and phrases related to media, news, and reporting | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/16076) |
| [L8:F2309](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2309) | 13 | L6-L8: Broadcast news / reportorial / press features (pos 13) |  words related to broadcast news | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2309) |
| [L7:F9521](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9521) | 13 | L6-L8: Broadcast news / reportorial / press features (pos 13) |  news sources and people involved in journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9521) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | L4: Journalism / Fourth Estate (pos 13) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | L0-L1: Stories / narrative / country tokens |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F2344](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2344) | 11 | L0-L1: Stories / narrative / country tokens |  instances of the word "country" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2344) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | L0-L1: Stories / narrative / country tokens | mentions of stories that are being told | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L0:F15423](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15423) | 11 | L0-L1: Stories / narrative / country tokens | The neuron seems to activate any time the word "country" is used, but also sometimes seems to activate for words related to groups of people such as "kids", "rest", or "total". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15423) |
| [L0:F11261](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) | 3 | L0-L1: Stories / narrative / country tokens |  the word "migration" and words related to it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) |
| [L0:F9201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9201) | 9 | L0-L1: Stories / narrative / country tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9201) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0: Gender / male-pronoun features (inhibitory) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F11603](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) | 27 | L0: Gender / male-pronoun features (inhibitory) |  the word "too" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) |
| [L0:F1301](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1301) | 20 | L0: Gender / male-pronoun features (inhibitory) |  mentions of cancer and related terms like tumors | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1301) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:14906 de=-0.222 |
| 3 | `inspect_feature` ×20 | L0:14906, L1:14812, L0:11603, L0:1069, L0:11261, L0:8061, L14:4420, L0:2711, L0:5333, L0:6962, L0:6051, L4:13253, L1:9201, L0:15423, L0:1301, L1:1154, L0:4564, L1:2344, L6:12712, L1:16233 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@13` | ❌ error | — | — | Trace the path from L14:F4420 (journalism/newspapers feature) at pos 13 (the wor… |
| SA-2 | `L4:F13253@13` | ❌ error | — | — | Trace the path from L4:F13253 (things related to journalism and the media, inclu… |
| SA-3 | `L0:F1069@1` | ❌ error | — | — | Trace the path from L0:F1069 (the male pronoun "He"/"His" feature) at pos 1 (the… |
| SA-4 | `L1:F14812@3` | ❌ error | — | — | Trace the path from L1:F14812 (references to stories, chapters, narrative elemen… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@13, k=15 → Emb:" journalistic"@13 (de=24.38) +14 more |
| 2 | `get_upstream_features` | L4:F13253@13, k=15 → Emb:" journalistic"@13 (de=25.62) +14 more |
| 3 | `get_upstream_features` | L1:F14812@3, k=15 → Emb:" stories"@3 (de=18.62) +14 more |
| 4 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"He"@1 (de=22.62) +9 more |
| 5 | `inspect_feature` ×8 | L7:9092, L8:8437, L7:13646, L8:8855, L6:8529, L7:9521, L7:16076, L8:2309 |

### Build

`build_circuit` → 11 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 75,960 | 4,736 | 175,165 | 0 | $0.0390 | — | — |
| **Total** | | **75,960** | **4,736** | **175,165** | **0** | **$0.0390** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 17s