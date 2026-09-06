# Circuit Oracle Report
**Date:** 2026-07-28 07:15:39 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a stacked chain of features that fire on academic-degree and educational-credential cues (the "Ph.D." abbreviation at pos 50–52, the "B.A.", "degree", "Mathematics", and "from University" spans at pos 2–13, and graduation years at pos 16–18), not by gender markers.

**Confidence:** 7

**Reasoning:** Tracing from the top probe-driving feature L7:F14129 ("academic degrees, universities, and people associated with them", frac_nonzero ≈ 0.004, pos 52), every upstream node leads back to degree/credential detectors, not gender:

- The most positive direct path into the output is L7:F14129 ← L6:F2254 "references to academic degrees" (direct_effect 6.97, pos 52) ← L2:F10852 "academic titles and degrees" (12.06, pos 52) and the `Ph`/`D`/`.'` token embeddings at pos 50/52/51, plus L1:F10132 (frac_nonzero ≈ 0.002, "the abbreviation for Doctorate of Philosophy, 'Ph.D.' written as 'D'"). L5:F13801 ("abbreviations for degrees and mentions of educational attainment") and L5:F11028 ("terms and phrases related to academic study and institutions") reinforce the same Ph.D. position.

- A second path through L6:F170 ("references to academic fields, especially those in the humanities") ← L5:F10392 ("fields of academic study") ← L3:F4113 ("mentions of academic degrees and areas of study") originates from the `Mathematics` token at pos 10, the `degree` token at pos 8, and `in` at pos 9. Again: credential/field vocabulary.

- The Layer-0 features are also credential-related: L0:F9263 ("mentions of academic qualifications and precise temperature values") and L0:F6127 ("instances of the word 'degree' and words associated with academia, especially higher education") fire on `degree` (pos 8); L0:F6270 ("the word 'whom'") and L0:F15320 ("the word 'ice'") both feed the output, but the former is acting as a generic surface-token detector and the latter appears to be a multi-use feature attached to `received` (pos 2); neither encodes gender. Year-related features L0:F6515 ("the year 199X or 200X"), L0:F618 ("years"), L0:F11333 ("the 1990's"), L0:F11132 ("possessive pronouns...and years") are date/graduation-year detectors, also gender-neutral.

- The negative-effect features in the output (L0:F11132, L0:F11333, L0:F9263, L0:F618, L0:F6127, L0:F12235, L6:F3235, L6:F3774, L6:F6811, L6:F170, L3:F4213 at pos 11) all relate to "University", proper-noun/profession-context or degree-list patterns. None of the inspected features in the top 20 by direct effect have a gender-related label; the only "his/possessive" mention in L0:F11132 is incidental to a years/historical-records feature.

So the user's worry is not borne out by this circuit: the dominant signal is the presence and stacking of explicit academic-degree tokens ("B.A.", "M.S.", "Ph.D.", "degree", "Mathematics", "from", "University", graduation years), which are arguably *legitimate* features for predicting "professor/academic profession" — though one caveat is that the circuit shows the probe is driven more by the *credential boilerplate template* than by profession-specific vocabulary (no "Professor", "Assistant Professor", "research", or field-of-CS words appear among the top features), so the probe is closer to a "this text looks like an academic biography" detector than a genuine "this person is a professor" classifier. That is a different concern from gender bias, and worth flagging, but it is not what the user asked about.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | Emb: ' received' (pos 2) |  the word "ice" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 13 | Layer-0 surface tokens: 'received', 'University', years, 'Mathematics' | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 18 | Layer-0 surface tokens: 'received', 'University', years, 'Mathematics' |  a mix of possessive pronouns like "his", names associated with historical records, and years. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 18 | Layer-0 surface tokens: 'received', 'University', years, 'Mathematics' |  the 1990's | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 17 | Layer-0 surface tokens: 'received', 'University', years, 'Mathematics' |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F618](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/618) | 18 | Layer-0 surface tokens: 'received', 'University', years, 'Mathematics' |  years | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/618) |
| [L0:F9263](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9263) | 8 | Layer-0 surface tokens: 'received', 'University', years, 'Mathematics' |  mentions of academic qualifications and precise temperature values | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9263) |
| [L0:F12235](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) | 8 | Layer-0 surface tokens: 'received', 'University', years, 'Mathematics' |  words related to legal documents and hunting | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) |
| [L0:F6127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) | 8 | Layer-0 surface tokens: 'received', 'University', years, 'Mathematics' |  instances of the word "degree" and words associated with academia, especially higher education | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) |
| [L0:F2085](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) | 2 | Layer-0 surface tokens: 'received', 'University', years, 'Mathematics' |  the word "reception" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 52 | Layer-1 'Ph.D.' abbreviation detector (D token) |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L1:F14298](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14298) | 52 | Layer-1 'Ph.D.' abbreviation detector (D token) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14298) |
| [L1:F11924](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11924) | 52 | Layer-1 'Ph.D.' abbreviation detector (D token) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11924) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 52 | Layer-2 academic titles & degrees detector |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 6 | Layer-2 academic titles & degrees detector |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F14934](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) | 18 | Layer-2 academic titles & degrees detector |  years in the 1900s | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) |
| [L2:F12115](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12115) | 9 | Layer-2 academic titles & degrees detector | the word "in" and abbreviations "nc" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12115) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 11 | Layer-3 advanced education, degrees, qualifications |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L3:F4113](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) | 9 | Layer-3 advanced education, degrees, qualifications |  mentions of academic degrees and areas of study | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) |
| [L3:F8294](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8294) | 52 | Layer-3 advanced education, degrees, qualifications |  words and phrases related to advanced education, research, and high-level concepts | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8294) |
| [L3:F11994](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) | 52 | Layer-3 advanced education, degrees, qualifications |  academic degrees and professional titles, especially involving "Ph.D." | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 9 | Layer-4 academic degrees / research abbreviations |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F13943](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) | 52 | Layer-4 academic degrees / research abbreviations |  words and abbreviations related to academic research | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | Layer-5 academic fields of study, degree abbreviations |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 52 | Layer-5 academic fields of study, degree abbreviations | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L5:F11028](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11028) | 52 | Layer-5 academic fields of study, degree abbreviations |  terms and phrases related to academic study and institutions | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11028) |
| [L5:F15490](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15490) | 10 | Layer-5 academic fields of study, degree abbreviations | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15490) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 13 | Layer-6 academic-degree, publications, math/science institutions (active and inhibiting) |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 12 | Layer-6 academic-degree, publications, math/science institutions (active and inhibiting) |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 12 | Layer-6 academic-degree, publications, math/science institutions (active and inhibiting) |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L6:F6811](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) | 12 | Layer-6 academic-degree, publications, math/science institutions (active and inhibiting) |  names of newly discovered microorganisms and places | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) |
| [L6:F6811](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) | 13 | Layer-6 academic-degree, publications, math/science institutions (active and inhibiting) |  names of newly discovered microorganisms and places | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | Layer-6 academic-degree, publications, math/science institutions (active and inhibiting) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 52 | Layer-6 academic-degree, publications, math/science institutions (active and inhibiting) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F8285](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8285) | 52 | Layer-6 academic-degree, publications, math/science institutions (active and inhibiting) |  text related to scientific publications and author information. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8285) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 52 | Layer-7 'academic degrees, universities, associated people' hub |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:3235 de=-0.054 |
| 3 | `inspect_feature` ×4 | L6:3235, L2:10852, L6:3774, L0:15320 |
| 4 | `get_upstream_features` | Emb:" Ph"@50 (de=14.75) +9 more |
| 5 | `get_upstream_features` | Emb:" received"@2 (de=13.00) +4 more |
| 6 | `get_upstream_features` | Emb:" University"@13 (de=22.88) +4 more |
| 7 | `get_upstream_features` | L6:F2254 (de=6.97) +9 more |
| 8 | `inspect_feature` ×4 | L6:2254, L5:13801, L3:8294, L1:10132 |
| 9 | `get_upstream_features` | L2:F10852 (de=12.06) +4 more |
| 10 | `inspect_feature` ×7 | L6:6811, L3:4213, L6:170, L2:14934, L0:11132, L0:11333, L0:9263 |
| 11 | `get_upstream_features` | L5:F10392 (de=11.38) +4 more |
| 12 | `get_upstream_features` | Emb:" from"@11 (de=10.69) +4 more |
| 13 | `get_upstream_features` | L0:F6515 (de=8.25) +4 more |
| 14 | `inspect_feature` ×6 | L0:6270, L0:6515, L0:12235, L0:6127, L0:2085, L0:618 |
| 15 | `get_upstream_features` | L3:F4113 (de=3.34) +4 more |
| 16 | `get_upstream_features` | Emb:" in"@9 (de=11.94) +4 more |
| 17 | `get_upstream_features` | Emb:" B"@4 (de=12.12) +4 more |
| 18 | `get_upstream_features` | L6:F2254 (de=6.97) +4 more |
| 19 | `inspect_feature` ×6 | L6:8285, L5:10392, L3:4113, L7:14129, L5:11028, L4:13943 |
| 20 | `get_upstream_features` | L6:F2254 (de=6.97) +9 more |
| 21 | `get_upstream_features` | L2:F10852 (de=12.06) +9 more |
| 22 | `get_upstream_features` | Emb:" received"@2 (de=13.00) +4 more |
| 23 | `inspect_feature` ×4 | L4:3727, L2:12115, L5:11028, L3:11994 |

### Build

`build_circuit` → 20 nodes, 26 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 58,283 | 6,519 | 231,213 | 0 | $0.0392 | — | — |
| **Total** | | **58,283** | **6,519** | **231,213** | **0** | **$0.0392** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 22s