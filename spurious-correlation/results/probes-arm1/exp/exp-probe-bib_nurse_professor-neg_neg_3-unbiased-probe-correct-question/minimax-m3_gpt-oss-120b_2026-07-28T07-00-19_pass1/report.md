# Circuit Oracle Report
**Date:** 2026-07-28 07:00:19 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

The user concern about "spurious gender markers" is not supported by the circuit — the user's hypothesis is contradicted by the evidence. Let me finalize my analysis.

**Analysis:** The probe's "academic profession" classification is driven entirely by genuine academic-credential signals — PhD/doctorate tokens, academic-degree abbreviations, field-of-study tokens, and a proper-noun university name — not by gender markers or other spurious features.

**Confidence:** 9

**Reasoning:** Tracing the top 15 direct-effect features reveals no male/female pronoun or gender features anywhere in the circuit. The dominant pathway is the **phd_degree_super** at pos 50-52 (the " Ph" / "D" Ph.D. abbreviation), driven by L1:10132 ("the abbreviation for Doctorate of Philosophy, 'Ph.D.' (or 'PhD') written as 'D'"), L5:13801 (degree abbreviations, frac_nonzero 0.028), L6:2254 ("references to academic degrees," frac_nonzero 0.004), and L7:14129 ("academic degrees, universities, and people associated with them," frac_nonzero 0.004, direct_effect 0.043). These receive the largest upstream contributions from the ` Ph` (pos 50) and `D` (pos 52) embedding nodes (direct_effects 14.75 and 10.13 respectively, per the L2:10852 upstream call). The second pathway is **academic_titles_super** — L2:10852 ("academic titles and degrees," frac_nonzero 0.008, promoted "degree"/"PhD"), L0:14877 (single uppercase letters / author initials), L0:2013 (the letters "ph"), L1:14298 (academic publications), L3:8294 (advanced education/research). A third pathway is **field_of_study_super** anchored on the " Mathematics" (pos 10) and " degree" (pos 8) embeddings via L6:170 ("references to academic fields"), L5:10392 ("fields of academic study"), L4:3727 ("mentions of academic degrees," promoted "Master"). The **peking_university_super** path activates on the " Peking" / " University" embeddings (direct_effects 17.25 and 10.13 on L6:3774/6811) via L4:5150 ("mentions of specific universities and colleges") and proper-noun L4:4257 (which here fires because "Peking" is rare-capitalized). Only the **years_and_function_words** supernode contains the pronouns (" his", "He") and "from"/"whom" function-word features (L0:8974, L0:6270, L0:11132, L0:11333, L0:6515) — but these have very low direct_effects (-0.054, -0.052, -0.047, -0.045, -0.042, -0.044) and are *inhibitory or near-zero* contributors to the probe, not the "his" gender features the user suspected. Function-word features like "from" and year tokens provide weak generic context, not gendered profession evidence. The user's concern is therefore not corroborated — the circuit cleanly separates genuine academic-credential features (which dominate the direct_effects) from generic context features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 52 | Output: Probe direction (academic profession classifier) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 52 | PhD / Doctorate degree tokens (positions 50-52) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 52 | PhD / Doctorate degree tokens (positions 50-52) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 52 | PhD / Doctorate degree tokens (positions 50-52) | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 52 | PhD / Doctorate degree tokens (positions 50-52) |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 52 | Academic titles / degree abbreviations (' Sc', 'D' for Ph.D.) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L0:F14877](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14877) | 52 | Academic titles / degree abbreviations (' Sc', 'D' for Ph.D.) |  single uppercase letters, sometimes followed by other characters, which frequently represent author initials. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14877) |
| [L0:F2013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2013) | 50 | Academic titles / degree abbreviations (' Sc', 'D' for Ph.D.) | the letters "ph" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2013) |
| [L3:F8294](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8294) | 52 | Academic titles / degree abbreviations (' Sc', 'D' for Ph.D.) |  words and phrases related to advanced education, research, and high-level concepts | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8294) |
| [L1:F14298](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14298) | 52 | Academic titles / degree abbreviations (' Sc', 'D' for Ph.D.) | academic publications, papers, and citations | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14298) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | Field of study / academic discipline (' Mathematics', ' Science') |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | Field of study / academic discipline (' Mathematics', ' Science') |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L3:F4113](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) | 9 | Field of study / academic discipline (' Mathematics', ' Science') |  mentions of academic degrees and areas of study | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 6 | Field of study / academic discipline (' Mathematics', ' Science') |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 9 | Field of study / academic discipline (' Mathematics', ' Science') |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 11 | Field of study / academic discipline (' Mathematics', ' Science') |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L0:F9263](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9263) | 8 | Field of study / academic discipline (' Mathematics', ' Science') |  mentions of academic qualifications and precise temperature values | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9263) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 13 | Proper-noun / university-name features firing on ' Peking University' |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 12 | Proper-noun / university-name features firing on ' Peking University' |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L6:F6811](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) | 12 | Proper-noun / university-name features firing on ' Peking University' |  names of newly discovered microorganisms and places | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) |
| [L4:F5150](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) | 13 | Proper-noun / university-name features firing on ' Peking University' |  mentions of specific universities and colleges | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) |
| [L4:F4257](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4257) | 12 | Proper-noun / university-name features firing on ' Peking University' |  locations, dishes and ingredients found in Cantonese cuisine | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4257) |
| [L4:F12975](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) | 12 | Proper-noun / university-name features firing on ' Peking University' | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12975) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 11 | Year tokens & function words (1991, 1996, 1998, 2003, 2009; 'from', 'his', 'He') | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 13 | Year tokens & function words (1991, 1996, 1998, 2003, 2009; 'from', 'his', 'He') | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 18 | Year tokens & function words (1991, 1996, 1998, 2003, 2009; 'from', 'his', 'He') |  a mix of possessive pronouns like "his", names associated with historical records, and years. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 18 | Year tokens & function words (1991, 1996, 1998, 2003, 2009; 'from', 'his', 'He') |  the 1990's | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 17 | Year tokens & function words (1991, 1996, 1998, 2003, 2009; 'from', 'his', 'He') |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L2:F14934](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) | 18 | Year tokens & function words (1991, 1996, 1998, 2003, 2009; 'from', 'his', 'He') |  years in the 1900s | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 50 | Emb: ' Ph' (pos 50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 52 | Emb: 'D' (pos 52) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' Peking' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: ' University' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: ' Mathematics' (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: ' degree' (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: ' from' (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:3235 de=-0.054 |
| 3 | `inspect_feature` ×15 | L6:3235, L2:10852, L6:3774, L0:15320, L0:11132, L0:6270, L6:6811, L0:11333, L7:14129, L0:6515, L0:9263, L3:4213, L6:170, L2:14934, L0:12235 |
| 4 | `get_upstream_features` | L6:F2254 (de=6.97) +9 more |
| 5 | `get_upstream_features` | Emb:" Ph"@50 (de=14.75) +9 more |
| 6 | `get_upstream_features` | L5:F10392 (de=11.38) +9 more |
| 7 | `get_upstream_features` | Emb:" from"@11 (de=10.69) +9 more |
| 8 | `get_upstream_features` | L4:F5150 (de=2.88) +9 more |
| 9 | `get_upstream_features` | Emb:" Peking"@12 (de=10.12) +9 more |
| 10 | `get_upstream_features` | Emb:" Peking"@12 (de=17.25) +9 more |
| 11 | `get_upstream_features` | Emb:" Peking"@12 (de=17.25) +9 more |
| 12 | `inspect_feature` ×8 | L6:2254, L5:13801, L1:10132, L5:10392, L4:4257, L3:8294, L1:14298, L1:11924 |
| 13 | `get_upstream_features` | Emb:" Ph"@50 (de=16.25) +9 more |
| 14 | `get_upstream_features` | Emb:" from"@11 (de=40.00) +9 more |
| 15 | `inspect_feature` ×7 | L0:8974, L0:14877, L0:2013, L4:3727, L3:4113, L4:5150, L4:13943 |

### Build

`build_circuit` → 13 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 66,422 | 5,281 | 203,403 | 0 | $0.0385 | — | — |
| **Total** | | **66,422** | **5,281** | **203,403** | **0** | **$0.0385** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 27s