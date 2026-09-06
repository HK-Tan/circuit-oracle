# Circuit Oracle Report
**Date:** 2026-07-28 07:15:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score (engineer profession) is driven primarily by genuine profession/academic-domain features (the words "Engineering" and "Ph.D", Canadian university locations, and academic-title/degree features), but the circuit also includes gender-pronoun and "received"/"his" features that contribute small additional effects. The user's concern is partially supported: gendered pronouns ("his"/"he") and possessives DO appear, but they are NOT the dominant signal — profession-indicating features (engineering, Ph.D., Canadian university, academic degrees) carry the bulk of the direct effect.

**Confidence:** 7

**Reasoning:** Tracing from the top late-layer features:
- The **largest positive direct effect** comes from L1:1372 ("the word 'engineer'" — frac_nonzero=0.008, suppresses "▁engineering" via transcoder decoder — but fires on "▁Engineering" in pos 9) with direct_effect=0.064. Its top upstream node is the " Engineering" embedding (pos 9, direct_effect=19) followed by " Mechanical" (pos 8, +0.75) — these are GENUINE profession tokens, not gender markers.
- The **second largest** positive contributor is L14:5600 ("places and regions, particularly in Canada", frac_nonzero=0.017, promotes "▁Canada") with direct_effect=0.064. Tracing upstream: L7:8870 ("locations and names of organizations or people", promotes "▁Canada", "▁Ottawa") → L4:8439 ("stock tickers / Canadian geography", promotes "▁Canadians", "▁Canadian", "▁Montreal", "▁Quebec", "▁Toronto") → " Waterloo" embedding (pos 14, +12.6). This is a Canadian-institution signal, not a gender signal — but it IS spurious as a profession indicator (location ≠ profession).
- The **third tier** includes L2:16309 ("people's names", pos 1) at +0.049 — this is a generic name-recognition feature that fires on "Daniel" (a man's first name), giving some implicit gender signal but fundamentally a name-token feature, not a he/his pronoun.
- The **Ph.D./academic-degree chain** contributes positively: Emb:"Ph" (pos 48) → L1:10132 → L2:10852 ("PhD" token) → L6:2254 ("references to academic degrees") → L7:14129 ("academic degrees, universities, and people") at +0.044.
- **Gender-marker features**: L0:2994 ("the pronoun 'his' and pronoun 'he'", pos 3, fires on "▁his", frac_nonzero=0.073 — high) with direct_effect=-0.036 (NEGATIVE — actually pushes AWAY from the probe direction, not toward it). L0:13553 ("verbs in past tense or past participle", pos 2) with direct_effect=+0.036 — its promoted tokens include "▁his", "▁himself", "▁him", "He", but its top examples are past-tense verbs ("left", "s"), not pronouns. L0:11132 ("a mix of possessive pronouns like 'his', names... and years", pos 19, direct_effect=-0.044) is again NEGATIVE.

The user is correct that gendered/male-coded features (his, he, "Daniel") appear in the circuit, but they contribute NEGATIVE direct_effects to the probe, or — in the case of L0:13553 — are a generic past-tense feature whose promoted-token list happens to include "his". The dominant POSITIVE drivers are profession words ("Engineering"), academic-degree words ("Ph.D"), and Canadian-university geography. The "received", "route", "reception", "brief" features are generic vocabulary features (broad frac_nonzero, semantic content unrelated to profession) — these contribute small effects but aren't gender markers either.

In short: the probe's classification of "engineer" is driven by the actual word "Engineering" and the academic-context features (Ph.D., Canadian university, degree tokens), with the pronoun/possessive features contributing only minor and partly NEGATIVE effects. The gender-marker concern is largely a red herring on this particular input — though the L2:16309 name-recognition feature firing on "Daniel" does encode some male-name signal, and the high-level his/he feature's strong presence in the input means it WILL fire in the residual stream even when it subtracts from the score.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F1372](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) | 9 | L1:1372 - "engineer/engineering" | the word "engineer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) |
| [L14:F5600](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) | 14 | L14:5600 - places/regions in Canada |  places and regions, particularly in Canada | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) |
| [L7:F8870](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) | 14 | L7:8870 - locations/orgs/people |  locations and names of organizations or people | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) |
| [L4:F8439](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) | 14 | L4:8439 - stock tickers / Canadian geography |  stock ticker symbols and Canadian geography | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 50 | L7:14129 - academic degrees/universities/people |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 50 | L6:2254 - references to academic degrees | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 50 | L2:10852 - "PhD" token/phrase | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 50 | L1:10132 - "Ph.D" subword | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | L0:2994 - pronoun "his"/"he" | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F13553](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) | 2 | L0:13553 - past tense / possessives |  verbs in the past tense or past participle | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) |
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | L0:15320 - "received" |  the word "ice" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F4687](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) | 14 | L0:4687 - place names | place names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) |
| [L2:F16309](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) | 1 | L2:16309 - people's names |  people's names | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 19 | L0:11333 - the 1990s |  the 1990's | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 18 | L0:6515 - year 199X/200X |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L2:F14934](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) | 19 | L2:14934 - years in the 1900s |  years in the 1900s | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) |
| [L2:F13360](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) | 50 | L2:13360 - academic titles/positions |  words related to academic titles and positions. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) |
| [L0:F2743](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) | 23 | L0:2743 - "later" | the word 'later' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) |
| [L0:F7905](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) | 2 | L0:7905 - "route" |  the word "route," referencing paths, directions, or means of transportation | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) |
| [L0:F2085](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) | 2 | L0:2085 - "reception" |  the word "reception" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) |
| [L0:F12235](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) | 6 | L0:12235 - legal docs / "brief" |  words related to legal documents and hunting | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 38 | L6:3235 - academic publications/math |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 19 | L0:11132 - possessives/years |  a mix of possessive pronouns like "his", names associated with historical records, and years. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2743 de=-0.069 |
| 3 | `inspect_feature` ×4 | L1:1372, L14:5600, L0:15320, L0:2743 |
| 4 | `get_upstream_features` | Emb:" Engineering"@9 (de=19.00) +9 more |
| 5 | `get_upstream_features` | L7:F8870 (de=15.94) +9 more |
| 6 | `get_upstream_features` | Emb:" received"@2 (de=13.00) +9 more |
| 7 | `inspect_feature` ×2 | L7:8870, L4:8439 |
| 8 | `get_upstream_features` | L4:F8439 (de=9.00) +9 more |
| 9 | `inspect_feature` ×6 | L0:4687, L0:6515, L2:16309, L0:11333, L0:11132, L7:14129 |
| 10 | `get_upstream_features` | L6:F2254 (de=7.31) +9 more |
| 11 | `inspect_feature` ×9 | L0:7905, L0:2085, L0:12235, L2:13360, L2:14934, L0:2994, L0:13553, L6:2254, L6:3235 |
| 12 | `get_upstream_features` | Emb:" Waterloo"@14 (de=17.25) +7 more |
| 13 | `get_upstream_features` | L2:F10852 (de=12.31) +7 more |
| 14 | `get_upstream_features` | Emb:" Ph"@48 (de=14.75) +5 more |
| 15 | `get_upstream_features` | Emb:" Ph"@48 (de=16.38) +5 more |

### Build

`build_circuit` → 31 nodes, 29 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 44,375 | 6,005 | 199,906 | 0 | $0.0325 | — | — |
| **Total** | | **44,375** | **6,005** | **199,906** | **0** | **$0.0325** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 31s