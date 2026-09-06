# Circuit Oracle Report
**Date:** 2026-07-28 07:20:35 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession classification is driven by a small set of mostly content-true features (engineer / degree / place) plus several clearly spurious subword coincidences — *not* by explicit gender markers, but the L0:11132 "his/possessive+year" feature at pos 19 and L0:15320/L0:7905 features at pos 2 that are mis-typed for "received" are the closest things to non-profession cues in the circuit.

**Confidence:** 6

**Reasoning:**

The graph's strongest positive features are content-driven and *legitimate* profession signals, not gender:
- **L1:1372 "engineer"** at pos 9 (direct_effect 0.064) — its top upstream is the raw " Engineering" embedding (19.0), confirmed by subagent trace; the subagent explicitly notes this is a *word* detector, not a generic suffix. Direct profession signal.
- **L7:14129 / L6:2254 "academic degree / PhD context"** at pos 50 (direct_effects 0.044, −0.044) — feed from the "Ph" embedding (4.56) and "D" embedding (5.66) and L2:10852 at pos 50. Direct profession signal (engineer/PhD).
- **L14:5600 "Canadian place"** at pos 14 (direct_effect 0.064) — driven by "Waterloo" embedding (12.6) and L4:8439/L7:8870 (Canadian place detectors). The probe may have learned a *geography* shortcut (Waterloo + Engineering = Canadian engineering professor) rather than a true profession indicator, which is a *correlated* spurious cue, not gender.
- **L2:16309 "person name"** at pos 1 (0.049) — driven by "Daniel" embedding. Entity recognition, not profession per se.
- **L6:3235 "academic/University"** at pos 38 (direct_effect −0.055) — Beirut token; pushes *against* the probe, suggesting the Lebanon leg actively *reduces* the profession confidence.

The user asked specifically about **gender markers**. The closest thing is **L0:11132 at pos 19** (direct_effect −0.044, frac_nonzero 0.009), whose autointerp is "a mix of possessive pronouns like 'his', names associated with historical records, and years" — it does fire on "his" in its training distribution, but on this input it is driven by the "9" digit in "1993" (direct_effect 11.06 from the pos-18 "9" embedding) and so acts as a year/decade detector here, not as a "he/his" gender probe. **L0:2743 "later"** (pos 23, −0.069) is the strongest negative feature, but it is purely a temporal connective, not a gender cue.

The genuinely *spurious* subword-coincidence features are at **pos 2 ("received")**:
- **L0:15320 "ice"** (pos 2, +0.058) and **L0:7905 "route"** (pos 2, −0.047) — both have an autointerp totally unrelated to the input token, but their upstream shows the *real* driver is the " received" embedding (direct_effect 13.0 and 12.9). These are apparently subword co-activation artifacts where the BPE token embedding for " received" partially resembles the embeddings these features were trained on ("ice", "route"). They are not gender, but they are clear *non-profession* noise.

**Bottom line on the user's concern:** There is **no "his"/he-pronoun gender feature** in the top-15 driving the probe. The L0:11132 feature that *can* activate on "his" is here acting on a year digit. The biggest "spurious" risks in this circuit are: (1) the Waterloo/Canadian-geography feature (a geography shortcut rather than a profession indicator) and (2) the pos-2 subword-coincidence features ("ice"/"route" firing on "received") — but these are not gendered, and the dominant positive signal is genuinely the word "engineer" itself. The "Mechanic"/"He"/"his" gender concern is **not** supported by the attribution graph.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F16309](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) | 1 | L2:16309 — Person name detector (pos 1, "Daniel") |  people's names | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) |
| [L1:F1372](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) | 9 | L1:1372 / L0:6414 — Token detector for "engineer"/"Engineering" (pos 9) | the word "engineer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) |
| [L0:F6414](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6414) | 9 | L1:1372 / L0:6414 — Token detector for "engineer"/"Engineering" (pos 9) |  the job title of "engineer", sometimes in conjunction with other words such as "agreement", "endorsement", or "record" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6414) |
| [L14:F5600](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) | 14 | L14:5600 / L7:8870 / L4:8439 — Canadian place detector (pos 14, "Waterloo") |  places and regions, particularly in Canada | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) |
| [L7:F8870](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) | 14 | L14:5600 / L7:8870 / L4:8439 — Canadian place detector (pos 14, "Waterloo") | locations and names of organizations or people | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) |
| [L4:F8439](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) | 14 | L14:5600 / L7:8870 / L4:8439 — Canadian place detector (pos 14, "Waterloo") | stock ticker symbols and Canadian geography | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 50 | L7:14129 / L6:2254 / L6:3235 — Academic-degree + university context (pos 50 "Ph.D"/38 "Beirut") |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 50 | L7:14129 / L6:2254 / L6:3235 — Academic-degree + university context (pos 50 "Ph.D"/38 "Beirut") | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 38 | L7:14129 / L6:2254 / L6:3235 — Academic-degree + university context (pos 50 "Ph.D"/38 "Beirut") |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L0:F2743](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) | 23 | L0:2743 — Token "later" (pos 23) — inhibits probe | the word 'later' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) |
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | L0:15320 ("ice") / L0:7905 ("route") at pos 2 — actually driven by " received" embedding (spurious subword co-activation) |  the word "ice" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F7905](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) | 2 | L0:15320 ("ice") / L0:7905 ("route") at pos 2 — actually driven by " received" embedding (spurious subword co-activation) |  the word "route," referencing paths, directions, or means of transportation | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 18 | L0:6515 / L0:11333 / L0:11132 — Year/decade token detectors at pos 18-19 (1993) |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 19 | L0:6515 / L0:11333 / L0:11132 — Year/decade token detectors at pos 18-19 (1993) |  the 1990's | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 19 | L0:6515 / L0:11333 / L0:11132 — Year/decade token detectors at pos 18-19 (1993) |  a mix of possessive pronouns like "his", names associated with historical records, and years. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L0:F4687](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) | 14 | L0:4687 — Place-name detector (pos 14, "Waterloo") — promotes probe | place names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) |
| [L0:F12235](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) | 6 | L0:12235 (legal/hunting) / L0:2085 ("reception") at pos 6/2 — weak negative features |  words related to legal documents and hunting | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) |
| [L0:F2085](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) | 2 | L0:12235 (legal/hunting) / L0:2085 ("reception") at pos 6/2 — weak negative features |  the word "reception" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | L0:7532 / L0:6226 — Proper-noun/name detectors (pos 1, "Daniel") | proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F6226](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6226) | 1 | L0:7532 / L0:6226 — Proper-noun/name detectors (pos 1, "Daniel") | proper nouns of people | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6226) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 50 | L2:10852 — Degree-token detector (pos 50) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 3 | `inspect_feature` ×17 | L14:5600, L0:2743, L1:1372, L0:15320, L6:3235, L2:16309, L0:6515, L0:7905, L0:4687, L0:11333, L0:11132, L6:2254, L7:14129, L0:2085, L0:12235, L7:14129, L0:2743 |
| 4 | `get_upstream_features` | L7:F8870 (de=15.94) +14 more |
| 5 | `get_upstream_features` | L6:F2254 (de=7.31) +14 more |
| 6 | `get_upstream_features` | Emb:" Engineering"@9 (de=19.00) +14 more |
| 7 | `get_upstream_features` | L2:F10852 (de=12.31) +14 more |
| 8 | `get_upstream_features` | Emb:"Daniel"@1 (de=12.94) +14 more |
| 9 | `get_upstream_features` | Emb:" Beirut"@38 (de=1.85) +14 more |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F1372@9` | ✅ reported | 7 | 14 | Trace L1:F1372 (word "engineer") at pos 9 — does this feature really encode "eng… |
| SA-2 | `L14:F5600@14` | ✅ reported | 6 | 7 | Trace L14:F5600 (places/Canada) at pos 14 — what does this feature actually dete… |
| SA-3 | `L2:F16309@1` | ✅ reported | 3 | 5 | Trace L2:F16309 (people's names) at pos 1 — what is the upstream path from the "… |
| SA-4 | `L7:F14129@50` | ❌ error | — | — | Trace L7:F14129 (academic degrees/universities) at pos 50 — what feeds this and … |

<details>
<summary><b>SA-1</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F1372 | "the word "engineer"" |
| 2 | `get_upstream_features` | L1:F1372@9, k=10 | Emb:" Engineering"@9 (de=19.00) +9 more |
| 3 | `inspect_feature` | L0, F6414 | " the job title of "engineer", sometimes in conjunction with other word" |
| 4 | `inspect_feature` | L0, F15570 | " words and phrases related to medical treatment and analysis" |
| 5 | `get_upstream_features` | L0:F6414@9, k=10 | Emb:" Engineering"@9 (de=11.88) +9 more |

**Findings:** The L1 feature F1372 at position 9 is a precise word detector for "engineer". Its strongest upstream driver is the raw token embedding for " Engineering" (direct_effect 19.0), confirming that it directly reads the token representation rather than acting as a generic suffix detector. Additional positive influence comes from a low‑frequency L0 feature (F6414) that also encodes the word "engineer" as…

</details>

<details>
<summary><b>SA-2</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F5600 | " places and regions, particularly in Canada" |
| 2 | `get_upstream_features` | L14:F5600@14, k=10 | L7:F8870 (de=15.94) +9 more |
| 3 | `inspect_feature` | L7, F8870 | " locations and names of organizations or people" |
| 4 | `inspect_feature` | L4, F8439 | " stock ticker symbols and Canadian geography" |
| 5 | `get_upstream_features` | L7:F8870@14, k=10 | L4:F8439 (de=9.00) +9 more |
| 6 | `get_upstream_features` | L4:F8439@14, k=10 | Emb:" Waterloo"@14 (de=17.25) +9 more |
| 7 | `inspect_feature` | L6, F11873 | " a variety of proper nouns including organization names, locations, an" |
| 8 | `get_upstream_features` | L6:F11873@14, k=10 | L4:F8439 (de=8.56) +9 more |
| 9 | `inspect_feature` | L1, F909 | " words and phrases related to education and diversity in schools" |
| 10 | `get_upstream_features` | L1:F909@14, k=10 | Emb:" University"@12 (de=10.00) +9 more |
| 11 | `inspect_feature` | L6, F13356 | " references to Canada and Canadian news organizations" |

**Findings:** L14:F5600 is a place‑detection feature specialized for Canadian geography. Its strongest upstream drivers are the raw token embedding for "Waterloo" and two mid‑layer detectors: L7:F8870 (a generic location/organization name detector) and L4:F8439 (a Canada‑geography/ticker symbol detector). Both of these feed positive activation into the target, and each is itself driven largely by the same "Wate…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F16309 | " people's names" |
| 2 | `get_upstream_features` | L2:F16309@1, k=10 | Emb:"Daniel"@1 (de=12.94) +9 more |
| 3 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 4 | `inspect_feature` | L0, F6226 | " proper nouns of people" |
| 5 | `get_upstream_features` | L0:F7532@1, k=10 | Emb:"Daniel"@1 (de=10.12) +9 more |
| 6 | `get_upstream_features` | L0:F6226@1, k=5 | Emb:"Daniel"@1 (de=9.69) +4 more |
| 7 | `inspect_feature` | L0, F12512 | " references to blogs and intelligence" |

**Findings:** The 'people's names' feature (L2:F16309) receives its strongest positive drive from the raw token embedding of the name 'Daniel' (direct effect ~13). Two lower‑layer proper‑noun detectors (L0:F7532 and L0:F6226) also feed positively into the name feature, and each of those in turn is directly excited by the same 'Daniel' embedding (effects ~10 and ~9.7). All upstream nodes lie in layer 0 (≤ 8), sa…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F4687@14, k=10 → Emb:" Waterloo"@14 (de=16.25) +9 more |
| 2 | `get_upstream_features` | L0:F2743@23, k=10 → Emb:" later"@23 (de=42.25) +9 more |
| 3 | `get_upstream_features` | L0:F15320@2, k=10 → Emb:" received"@2 (de=13.00) +9 more |
| 4 | `get_upstream_features` | L0:F7905@2, k=10 → Emb:" received"@2 (de=12.94) +9 more |
| 5 | `get_upstream_features` | L0:F11132@19, k=10 → Emb:"9"@18 (de=11.06) +9 more |

### Build

`build_circuit` → 26 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 77,440 | 6,411 | 204,164 | 0 | $0.0432 | — | — |
| SA-3 | openai/gpt-oss-120b | 66,856 | 4,113 | 0 | 0 | $0.0125 | ✅ 3F/5E | Trace L2:F16309 (people's names) at pos 1 — what is the upst… |
| SA-1 | openai/gpt-oss-120b | 51,138 | 6,413 | 2,528 | 0 | $0.0116 | ✅ 7F/14E | Trace L1:F1372 (word "engineer") at pos 9 — does this featur… |
| SA-2 | openai/gpt-oss-120b | 125,827 | 7,502 | 5,184 | 0 | $0.0235 | ✅ 6F/7E | Trace L14:F5600 (places/Canada) at pos 14 — what does this f… |
| **Total** | | **321,261** | **24,439** | **211,876** | **0** | **$0.0907** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 16s