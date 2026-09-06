# Circuit Oracle Report
**Date:** 2026-07-28 07:21:48 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-classification probe is driven by a mix of genuine profession-relevant signals (degree titles, "Engineering" word, university names) and a substantial amount of spurious surface/contextual evidence (years, the word "later", the subject name "Daniel", Canadian geographic markers), with no profession-specific concept features present.

**Confidence:** 7

**Reasoning:**

The circuit splits into three roughly separable evidence streams that all push the probe score:

**(1) Genuine profession / academic-context signal** — the largest and most legitimate component. The probe reads the PhD credential at pos 48-50 ("Ph.D.") through a deep chain: Embeddings " Ph" and "D" → L1:10132 ("Ph.D." written as "D", frac_nonzero=0.0023) → L2:10852 ("academic titles and degrees", frac=0.008) → L5:13801 (degree abbreviations, frac=0.028) → L6:2254 (academic degrees, frac=0.004) and L6:8285 (scientific publication context, frac=0.058) → L7:14129 ("academic degrees, universities, and people associated with them", frac=0.0042). These features encode the *concept* of academic credentialing — promoted tokens are "degree", "degrees", "doctorate", "PhD" — which is a legitimate (though profession-implicit) signal. The word "Engineering" at pos 9 is read via L1:1372 (label "the word 'engineer'", frac=0.0077, suppressed tokens are "engineer"/"engineering" — the encoder-direction feature) and feeds the probe directly.

**(2) Geographic / university-name signal** — partially legitimate but heavily nationality-coded. The token "Waterloo" at pos 14 lights up a chain that runs L4:8439 ("stock ticker symbols and Canadian geography", promoted: "Canada/Canadian/Canadians/Montreal/Quebec/Ontario/Toronto", frac=0.010) → L6/L7 features → L7:8870 ("locations and names of organizations or people", promoted: "Canada/Canadian/Canada/Ottawa/Edmonton", frac=0.0065) → L14:5600 ("places and regions, particularly in Canada", promoted: "▁Canada/Canadians/Canadian/Toronto", frac=0.017). The same token "Waterloo" alone activates what is essentially a Canadian-ness detector rather than a Waterloo-the-university detector. L4:13886 ("US universities and their locations", activated at "Beirut" pos 38 — misfiring) and L6:3235 ("academic publications, math, and scientific institutions", also at "Beirut") are weaker, university-specific contributions.

**(3) Pure surface / subject-identity features with no profession content** — this is where the user's concern is borne out. The top-15 features include L0:15320 ("the word 'ice'") at " received" (pos 2, direct_effect=+0.058), L0:2085 ("the word 'reception'") at " received" (–0.041), L0:7905 ("the word 'route'") at " received" (–0.047), L0:2743 ("the word 'later'") at pos 23 (–0.069), L0:6515 ("the year 199X or 200X") at pos 18 (–0.048), L0:11333 ("the 1990's") at pos 19 (–0.045), L0:11132 ("possessive pronouns… and years") at pos 19 (–0.044), L0:4687 ("place names") at pos 14 (–0.054), and L0:12235 ("words related to legal documents and hunting") at pos 6 (–0.039). L2:16309 ("people's names", activated on "Daniel", pos 1) directly drives the probe (+0.049). All upstream of these resolve cleanly to embeddings of " received", " later", "9"/"1" (year digits), "Daniel" — none of them encode profession.

Notably the **subject token "He" / "his"** and the proper name "Daniel" both feed the probe via gender-pronoun-adjacent L0:11132 ("his", "names associated with historical records, and years") and L2:16309 ("people's names"). These are not gender-marker *pronoun* features per se, but they are *male-coded* name/possessive features that ride along. The strongest single positive non-degree contribution to the probe is L0:15320 (the "ice" word-feature firing on " received"), L0:6515 (199X year detector) — these are textbook surface artifacts.

**Net assessment relative to the user's concern:** The probe is *not* primarily driven by gender markers (no dedicated "he/his" features at high direct_effect), but the user's underlying worry is correct in spirit. The probe leans heavily on (a) the *subject's first name* and *possessive pronouns* (L2:16309, L0:11132), (b) the *country of affiliation* (L4:8439, L7:8870, L14:5600 — all Canadian-geography features keyed off "Waterloo"), and (c) generic *year-of-degree* and *templated "X received his..."* surface patterns (L0:6515, L0:11333, L0:11132, L0:15320/2085/7905 all firing on " received"). The genuine profession-discriminative content (degree tokens, the literal word "Engineering", academic-context features) is present but is matched in total magnitude by this web of biographical-template and nationality/identity side-channel features. So the probe's classification is partially explainable by "this text looks like a Canadian male academic's CV boilerplate" rather than purely by profession-specific concepts — a meaningful failure mode for profession classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | L0: Surface token / year detectors at subject/verb/YEAR/POS slots |  the word "ice" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F2085](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) | 2 | L0: Surface token / year detectors at subject/verb/YEAR/POS slots |  the word "reception" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) |
| [L0:F7905](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) | 2 | L0: Surface token / year detectors at subject/verb/YEAR/POS slots |  the word "route," referencing paths, directions, or means of transportation | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) |
| [L0:F2743](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) | 23 | L0: Surface token / year detectors at subject/verb/YEAR/POS slots | the word 'later' | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 18 | L0: Surface token / year detectors at subject/verb/YEAR/POS slots |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 19 | L0: Surface token / year detectors at subject/verb/YEAR/POS slots |  the 1990's | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 19 | L0: Surface token / year detectors at subject/verb/YEAR/POS slots |  a mix of possessive pronouns like "his", names associated with historical records, and years. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L0:F4687](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) | 14 | L0: Surface token / year detectors at subject/verb/YEAR/POS slots | place names | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) |
| [L0:F12235](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) | 6 | L0: Surface token / year detectors at subject/verb/YEAR/POS slots |  words related to legal documents and hunting | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) |
| [L2:F16309](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) | 1 | L2: 'Daniel' name detector (pos 1) |  people's names | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16309) |
| [L1:F1372](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) | 9 | L1: 'Engineering' word detector (pos 9) | the word "engineer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 50 | L1: 'Ph.D.' (token D) detector (pos 50) |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 50 | L2: Academic-degree titles (pos 50) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L3:F8294](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8294) | 50 | L3-4: Advanced-research / Canadian-geog / US-university features |  words and phrases related to advanced education, research, and high-level concepts | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8294) |
| [L4:F13943](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) | 50 | L3-4: Advanced-research / Canadian-geog / US-university features |  words and abbreviations related to academic research | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) |
| [L4:F8439](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) | 14 | L3-4: Advanced-research / Canadian-geog / US-university features |  stock ticker symbols and Canadian geography | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) |
| [L4:F13886](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13886) | 38 | L3-4: Advanced-research / Canadian-geog / US-university features |   US universities and their locations | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13886) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 50 | L5-6: Degree abbreviations, universities, scientific publications | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 50 | L5-6: Degree abbreviations, universities, scientific publications | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F8285](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8285) | 50 | L5-6: Degree abbreviations, universities, scientific publications |  text related to scientific publications and author information. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8285) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 38 | L5-6: Degree abbreviations, universities, scientific publications |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 50 | L7: Academic-degree / Canadian-place features |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F8870](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) | 14 | L7: Academic-degree / Canadian-place features |  locations and names of organizations or people | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) |
| [L14:F5600](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) | 14 | L14: Places and regions, particularly in Canada (pos 14 'Waterloo') |  places and regions, particularly in Canada | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |
| 3 | `inspect_feature` ×15 | L0:2743, L1:1372, L14:5600, L0:15320, L6:3235, L2:16309, L0:6515, L0:7905, L0:4687, L0:11333, L0:11132, L6:2254, L7:14129, L0:2085, L0:12235 |
| 4 | `get_upstream_features` | Emb:" Engineering"@9 (de=19.00) +9 more |
| 5 | `get_upstream_features` | L7:F8870 (de=15.94) +9 more |
| 6 | `get_upstream_features` | L6:F2254 (de=7.31) +9 more |
| 7 | `get_upstream_features` | L2:F10852 (de=12.31) +9 more |
| 8 | `get_upstream_features` | Emb:" received"@2 (de=13.00) +9 more |
| 9 | `get_upstream_features` | Emb:"Daniel"@1 (de=12.94) +9 more |
| 10 | `get_upstream_features` | Emb:" Waterloo"@14 (de=16.25) +9 more |
| 11 | `get_upstream_features` | L4:F8439 (de=9.00) +7 more |
| 12 | `get_upstream_features` | Emb:" Waterloo"@14 (de=17.25) +7 more |
| 13 | `get_upstream_features` | Emb:" Beirut"@38 (de=1.85) +7 more |
| 14 | `get_upstream_features` | Emb:" Ph"@48 (de=14.75) +5 more |
| 15 | `get_upstream_features` | Emb:"9"@18 (de=11.06) +5 more |
| 16 | `get_upstream_features` | Emb:"9"@18 (de=11.31) +5 more |
| 17 | `get_upstream_features` | Emb:"1"@17 (de=29.38) +5 more |
| 18 | `inspect_feature` ×9 | L7:8870, L4:8439, L2:10852, L1:10132, L4:13886, L5:13801, L6:8285, L3:8294, L4:13943 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14129@50` | ❌ error | — | — | Trace this PhD-related feature upstream. The model is classifying profession, an… |
| SA-2 | `L14:F5600@14` | ❌ error | — | — | Trace this "places in Canada" feature upstream — what feeds it? Is the Canadian-… |
| SA-3 | `L6:F2254@50` | ❌ error | — | — | Trace this academic-degrees feature upstream at pos 50. What drives it? Is it ge… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F15320@2, k=15 → Emb:" received"@2 (de=13.00) +14 more |
| 2 | `get_upstream_features` | L0:F2743@23, k=10 → Emb:" later"@23 (de=42.25) +9 more |
| 3 | `get_upstream_features` | L0:F2085@2, k=10 → Emb:" received"@2 (de=17.75) +9 more |
| 4 | `get_upstream_features` | L0:F7905@2, k=10 → Emb:" received"@2 (de=12.94) +9 more |

### Build

`build_circuit` → 19 nodes, 25 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 48,772 | 7,163 | 294,422 | 0 | $0.0409 | — | — |
| **Total** | | **48,772** | **7,163** | **294,422** | **0** | **$0.0409** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 30s