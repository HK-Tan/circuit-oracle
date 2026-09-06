# Circuit Oracle Report
**Date:** 2026-07-28 07:21:50 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by genuine profession/credentials features (degrees, universities, academic fields, and the specific institution "Peking University") — not by gender markers.

**Confidence:** 8

**Reasoning:** The circuit cleanly traces the probe's score to a hierarchy of legitimate academic-career signals, not to "he/his" pronouns or other spurious features.

**Key flow into the output node:**
- **L7:F14129 (academic degrees, universities, people; pos 50/52) — direct_effect via L6:F2254 (6.97) and L2:F10852 (2.63).** Fires on the "Ph.D." token at pos 50–52, fed by:
  - **Emb:"Ph" (pos 50, direct 12.44)** and **Emb:"D" (pos 52, direct 10.13)** — the literal Ph.D. abbreviation
  - **L1:F10132** "Ph.D. abbreviation written as D" (very specific, frac_nonzero=0.002)
  - **L2:F10852** "academic titles and degrees" (frac_nonzero=0.008) promoted tokens include "degree", "PhD", "doctorate"
  - **L5:F13801** "abbreviations for degrees and educational attainment" (fires on "D", "doctorate")
- **L6:F3235 (academic publications/math/scientific institutions, pos 12/13, "Peking"/"University")** — fed by Emb:"Peking" (direct 4.53) and Emb:"University" via L4:F5150 (specific universities). Promoted: "University".
- **L6:F170 (academic fields, pos 10 "Mathematics")** — fed by Emb:"Mathematics" → L5:F10392 (fields of academic study). Top tokens: "science", "literature", "Writing".
- **L6:F3774 (proper nouns/unusual capitalization, pos 12 "Peking")** — directly from Emb:"Peking" (direct 10.13).
- **L6:F6811 (newly named places/entities, pos 12/13)** — fires on "Peking"/"University" as a specific location entity.
- **L3:F4213 (degree qualifications/awards, pos 11 "from")** — fed by Emb:"from" (direct 10.69), Emb:"degree" (5.28), Emb:"received" (3.16), and L2:F10852 (academic titles, 3.03). This is the bio-style "He received his X degree in Y from Z" template detector.

**What is NOT in the circuit:** The pronoun "He" at pos 1, "his" at pos 3, and "He" at pos 15/22/27 are **not** among the top features driving the probe. The only L0 features that are top are F6270 (function-word detector, incidentally fires on "University"), F15320 ("ice", clearly incidental noise on "received" at pos 2), and F11132 (pos 18, weak). None of these encode male gender. L0:F6270's top examples are "whom" — it's a generic function-word detector, not a pronoun-gender feature (its label literally reads "the word 'whom'"). L0:F11132's label mentions "possessive pronouns like 'his'", but its direct_effect on the probe is only -0.047, and it fires on the "9" digit at pos 18, not "his".

The user concern about gender-marker spurious features is **not supported** by this circuit. The dominant features are degree/credential/university/field detectors that genuinely correlate with "Computer Science professor" profession. The probe appears to learn the academic-bio template ("received his B.A./M.S./Ph.D. from University X in Field Y"), not gendered pronouns.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 13 | L0: F6270 'whom' function word detector (pos 13, University) | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | L0: F15320 'ice' (pos 2, incidental) |  the word "ice" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 18 | L0: F11132 possessive/years (pos 18) |  a mix of possessive pronouns like "his", names associated with historical records, and years. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L0:F14877](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14877) | 52 | L0: F14877 uppercase initials (pos 52, D) |  single uppercase letters, sometimes followed by other characters, which frequently represent author initials. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14877) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 52 | L1: F10132 'D' = Ph.D. abbreviation (pos 52) |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 52 | L2: F10852 academic titles/degrees (pos 6,8,52) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 6 | L2: F10852 academic titles/degrees (pos 6,8,52) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 8 | L2: F10852 academic titles/degrees (pos 6,8,52) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 11 | L3: F4213 degree qualifications/awards (pos 11) |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L4:F5150](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) | 13 | L4: F5150 specific universities/colleges (pos 12,13) |  mentions of specific universities and colleges | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) |
| [L4:F5150](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) | 12 | L4: F5150 specific universities/colleges (pos 12,13) |  mentions of specific universities and colleges | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | L5: F10392 fields of academic study (pos 10, Mathematics) |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 52 | L5: F13801 degree abbreviations/educational attainment (pos 50,52) | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 50 | L5: F13801 degree abbreviations/educational attainment (pos 50,52) | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | L6: F170 academic fields (humanities) (pos 10) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 52 | L6: F2254 references to academic degrees (pos 50,52) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 50 | L6: F2254 references to academic degrees (pos 50,52) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 13 | L6: F3235 academic publications/math/scientific institutions (pos 12,13) |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 12 | L6: F3235 academic publications/math/scientific institutions (pos 12,13) |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 12 | L6: F3774 proper nouns/unusual capitalization (pos 12, Peking) |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L6:F6811](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) | 12 | L6: F6811 newly named places/entities (pos 12,13) |  names of newly discovered microorganisms and places | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) |
| [L6:F6811](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) | 13 | L6: F6811 newly named places/entities (pos 12,13) |  names of newly discovered microorganisms and places | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 52 | L7: F14129 academic degrees/universities/people (pos 50,52) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 50 | L7: F14129 academic degrees/universities/people (pos 50,52) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:3235 de=-0.054 |
| 3 | `inspect_feature` ×18 | L6:3235, L2:10852, L6:3774, L0:15320, L0:11132, L0:6270, L6:6811, L0:11333, L7:14129, L0:6515, L0:9263, L3:4213, L0:12235, L6:170, L2:14934, L0:618, L0:2085, L0:6127 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14129@52` | ❌ error | — | — | Trace the path from L7:F14129 (academic degrees, universities, people). This fir… |
| SA-2 | `L6:F170@10` | ❌ error | — | — | Trace the path from L6:F170 (academic fields, humanities) at pos 10. This fires … |
| SA-3 | `L6:F3235@13` | ❌ error | — | — | Trace the path from L6:F3235 (academic publications, math, scientific institutio… |
| SA-4 | `L3:F4213@11` | ❌ error | — | — | Trace the path from L3:F4213 (mentions of degree qualifications or awards) at po… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14129@52, k=10 → L6:F2254 (de=6.97) +9 more |
| 2 | `get_upstream_features` | L6:F170@10, k=10 → L5:F10392 (de=11.38) +9 more |
| 3 | `get_upstream_features` | L6:F3235@13, k=10 → L4:F5150 (de=2.88) +9 more |
| 4 | `get_upstream_features` | L3:F4213@11, k=10 → Emb:" from"@11 (de=10.69) +9 more |
| 5 | `inspect_feature` ×6 | L6:2254, L5:13801, L1:10132, L5:10392, L4:5150, L0:8974 |
| 6 | `get_upstream_features` | L6:F3235@12, k=10 → Emb:" Peking"@12 (de=4.53) +9 more |
| 7 | `get_upstream_features` | L0:F6270@13, k=10 → Emb:" University"@13 (de=22.88) +9 more |
| 8 | `get_upstream_features` | L2:F10852@52, k=10 → Emb:" Ph"@50 (de=14.75) +9 more |
| 9 | `get_upstream_features` | L6:F3774@12, k=10 → Emb:" Peking"@12 (de=10.12) +9 more |
| 10 | `get_upstream_features` | L7:F14129@52, k=10 → L6:F2254 (de=6.97) +9 more |
| 11 | `get_upstream_features` | L7:F14129@51, k=10 → ❌ Feature (layer=7, feature_idx=14129) not found at pos=51. Th |
| 12 | `get_upstream_features` | L7:F14129@50, k=5 → Emb:" Ph"@50 (de=12.44) +4 more |
| 13 | `inspect_feature` ×3 | L0:9026, L4:4257, L0:14877 |

### Build

`build_circuit` → 26 nodes, 38 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 58,620 | 6,728 | 300,334 | 0 | $0.0437 | — | — |
| **Total** | | **58,620** | **6,728** | **300,334** | **0** | **$0.0437** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 27s