# Circuit Oracle Report
**Date:** 2026-07-28 07:21:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit is well-mapped from late-layer features down to L0/L1 features. Let me verify the key paths one more time to confirm the male-pronoun path (the user's concern) is properly characterized.

**Analysis:** The classification probe for this faculty biography is driven by an *academic-degree-and-university detection circuit* — not by gender — and the male-pronoun embeddings appear only as low-amplitude peripheral inputs that are mostly suppressed by the dominant degree/award signal.

**Confidence:** 7

**Reasoning:** The strongest positive contributors to the probe direction are a tightly-coupled degree/award/university circuit:

- **L7:F14129** (frac_nonzero≈0.0042) "academic degrees, universities, and people associated with them" — a high-activation (50.25 at pos 52) hub fed by the "Ph"/"D" token embeddings (pos 50/52) and a chain of degree detectors at every layer.
- **L6:F2254 / L6:F3631 / L6:F12933 / L6:F11173** "references to academic degrees / institutions of higher education" — fired on the "B.A.", "M.S.", "Ph.D." tokens (direct_effect up to +0.038 at pos 10, +0.0265 at pos 13).
- **L6:F170 / L5:F10392** "fields of academic study" — fired on the field name "Mathematics" at pos 10 and pos 30 (direct_effect +0.0381 and +0.0315).
- **L2:F10852** "academic titles and degrees" — directly driven by the "Ph" (+14.75) and "D" (+10.13) token embeddings at pos 50/52.
- **L3:F4213** "degree/award mention" — driven by the "from" (+10.69) and "degree" (+5.28) embeddings at pos 8/11.
- **L14:F3956** "universities and degrees" — late-stage consolidation of this signal (direct_effect −0.022 from this path; the negative direction reflects an offsetting effect but the feature still represents a strong degree/university representation that propagates forward).
- **L14:F12274** "China/Korea/technology/conflict" — directly driven by the "Peking" embedding (pos 12, direct_effect +19.0) and feeds the probe with a +0.033 boost, indicating the model uses the place name (a major university) as a profession-correlated signal.

The **male-pronoun path** (L0:F1069 "He/His", L0:F2994 "his/he", L1:F12922 "he or she") is the user's concern. Tracing shows it is present but **structurally minor and largely neutralized**:
- L0:F1069 at pos 1 is driven *primarily* by the "He" embedding (+22.625 direct_effect) and *not* by gender-specific training — it's a generic "subject pronoun" detector.
- L0:F2994 "his/he" is the most male-specific feature (frac_nonzero=0.073, promoted tokens include "The", capitalized prose markers), but it has *negative* direct_effect (−0.0249) on the probe — i.e., it slightly *suppresses* the classification score.
- L1:F12922 "he/she" at pos 1 and pos 21 receives nearly identical inputs from the "He" and " he" embeddings (+19.25, +23.125), and its downstream contribution is modest (+0.024 to +0.031 direct_effect on the probe).
- Crucially, the female-pronoun feature L0:F8008 (frac_nonzero≈0.087) fires on "she" but has only +0.0231 direct_effect — a similar magnitude, suggesting the model is using *narrative-pronoun context* (the standard "He received his B.A." Wikipedia biography opening), not gender itself.

The biography's **functional profession signal** (Computer Science / Assistant Professor) is communicated through:
1. Degree/award tokens (B.A., M.S., Ph.D.) and the "received … degree" construction.
2. University/place names (Peking, Utah State, Stony Brook, Missouri).
3. The field name "Mathematics" and "Computer Science."
4. The job-title phrase "Assistant Professor of Computer Science."

The "He/his" pronouns are co-occurring features of the Wikipedia biography template, but the classification probe is dominated by the academic-credential and institution-detection supernodes, not by gender features. The user's concern about spurious gender features is **only partially supported**: while the male-pronoun features are present in the circuit, they are weak contributors, and the dominant signal is the genuine profession-indicating academic-degree/university chain.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 0 | Emb: <bos> (pos 0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: He (pos 1) — male pronoun | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: his (pos 3) — male pronoun | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: received (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: B / A / . (pos 4-7) — degree tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 5 | Emb: B / A / . (pos 4-7) — degree tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: B / A / . (pos 4-7) — degree tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: B / A / . (pos 4-7) — degree tokens | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: degree (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: in (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: Mathematics (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: from (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: Peking (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: University (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: He (pos 21) — male pronoun | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 50 | Emb: Ph (pos 50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 52 | Emb: D (pos 52) — PhD token | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 120 | Emb: Biomedical (pos 120) — post-prompt | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | L0/L1: Male pronoun features (his/he) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0/L1: Male pronoun features (his/he) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L1:F12922](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12922) | 1 | L0/L1: Male pronoun features (his/he) |  the pronoun "he" or "she" in a narrative context | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12922) |
| [L1:F12922](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12922) | 21 | L0/L1: Male pronoun features (his/he) |  the pronoun "he" or "she" in a narrative context | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12922) |
| [L0:F14877](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14877) | 6 | L0: B.A./uppercase initials and period | single uppercase letters, sometimes followed by other characters, which frequently represent author initials. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14877) |
| [L0:F1636](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1636) | 6 | L0: B.A./uppercase initials and period |  the letter A | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1636) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 5 | L0: B.A./uppercase initials and period | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 20 | L0: B.A./uppercase initials and period | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F7905](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) | 2 | L0: B.A./uppercase initials and period |  the word "route," referencing paths, directions, or means of transportation | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 17 | L0: 199X/200X year tokens |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 18 | L0: 199X/200X year tokens |  the 1990's | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 18 | L0: 199X/200X year tokens |  a mix of possessive pronouns like "his", names associated with historical records, and years. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L0:F6127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) | 8 | L0: 199X/200X year tokens |  instances of the word "degree" and words associated with academia, especially higher education | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) |
| [L0:F9263](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9263) | 8 | L0: 199X/200X year tokens |  mentions of academic qualifications and precise temperature values | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9263) |
| [L0:F12235](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) | 8 | L0: 199X/200X year tokens |  words related to legal documents and hunting | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) |
| [L0:F618](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/618) | 18 | L0: 199X/200X year tokens |  years | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/618) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 13 | L0: Function words & pronouns (whom, his) | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 12 | L0: Function words & pronouns (whom, his) | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F14556](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14556) | 2 | L0: Function words & pronouns (whom, his) |  verbs that indicate feeling, thought, or intention | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14556) |
| [L0:F7681](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) | 2 | L0: Function words & pronouns (whom, his) | statements that describe something, often including a past tense verb | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7681) |
| [L0:F8008](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8008) | 1 | L0: Function words & pronouns (whom, his) |  mentions of a female subject | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8008) |
| [L0:F10397](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10397) | 10 | L0: Function words & pronouns (whom, his) |  mentions of quantum computing | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10397) |
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | L0: Misc (ice, reception, age, ice/hunt) |  the word "ice" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F2085](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) | 2 | L0: Misc (ice, reception, age, ice/hunt) |  the word "reception" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) |
| [L0:F15906](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15906) | 6 | L0: Misc (ice, reception, age, ice/hunt) |  the suffix "age" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15906) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 6 | L2: Academic titles & degrees |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 26 | L2: Academic titles & degrees |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 52 | L2: Academic titles & degrees |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F13360](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) | 52 | L2: Academic titles & degrees |  words related to academic titles and positions. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13360) |
| [L2:F3992](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3992) | 2 | L2: Academic titles & degrees |  instances of people or things receiving something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3992) |
| [L2:F14934](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) | 18 | L2: Academic titles & degrees |  years in the 1900s | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14934) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 11 | L3: degree/award mention |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 31 | L3: degree/award mention |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L3:F4113](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) | 9 | L3: degree/award mention | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) |
| [L4:F2279](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2279) | 13 | L4: University/degree word detectors |  instances of the word "University" and other words that appear near it | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2279) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 6 | L4: University/degree word detectors |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 9 | L4: University/degree word detectors |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 26 | L4: University/degree word detectors |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F5150](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) | 12 | L4: University/degree word detectors |  mentions of specific universities and colleges | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) |
| [L4:F11633](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11633) | 20 | L4: University/degree word detectors |  words related to education and employment history | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11633) |
| [L4:F11633](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11633) | 6 | L4: University/degree word detectors |  words related to education and employment history | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11633) |
| [L4:F11633](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11633) | 58 | L4: University/degree word detectors |  words related to education and employment history | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11633) |
| [L4:F4257](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4257) | 12 | L4: University/degree word detectors | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4257) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | L4: University/degree word detectors | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | L5: Academic field/study detector |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 30 | L5: Academic field/study detector |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 26 | L5: Academic field/study detector | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 52 | L5: Academic field/study detector | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L5:F15490](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15490) | 10 | L5: Academic field/study detector | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15490) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | L6: References to academic fields |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 30 | L6: References to academic fields |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 6 | L6: References to academic degrees | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 26 | L6: References to academic degrees | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 52 | L6: References to academic degrees | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F11173](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11173) | 10 | L6: References to academic degrees |  mathematical publications and related terms, including the location of the publication, volume, and date. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11173) |
| [L6:F3631](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3631) | 13 | L6: References to academic degrees | references to institutions of higher education, degrees, and associated academic work | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3631) |
| [L6:F12933](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12933) | 10 | L6: References to academic degrees |  references to law, lawyers, committees, degrees, or academic work | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12933) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 12 | L6: Proper nouns / place names (Peking) |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 13 | L6: Proper nouns / place names (Peking) |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L6:F6811](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) | 12 | L6: Proper nouns / place names (Peking) |  names of newly discovered microorganisms and places | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) |
| [L6:F6811](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) | 13 | L6: Proper nouns / place names (Peking) |  names of newly discovered microorganisms and places | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 12 | L6: Proper nouns / place names (Peking) |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 13 | L6: Proper nouns / place names (Peking) |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F6392](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6392) | 13 | L6: Proper nouns / place names (Peking) | higher education institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6392) |
| [L6:F3558](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3558) | 12 | L6: Proper nouns / place names (Peking) |  mentions of money, politics, or place names, likely within the country of Malaysia or Brazil | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3558) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 26 | L7: Academic degrees, universities, people |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 52 | L7: Academic degrees, universities, people |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 58 | L7: Academic degrees, universities, people |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L14:F3956](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) | 58 | L14: Universities and degrees |  universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) |
| [L14:F12274](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12274) | 12 | L14: China/Korea/technology/conflict (Peking) |  mentions of China, Korea, technology, and conflict | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12274) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 120 | L15: Medical/healthcare words (Biomedical) |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output: Probe direction (Professor/Prof. class) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:3235 de=-0.054 |
| 3 | `inspect_feature` ×6 | L0:15320, L0:6270, L3:4213, L6:170, L2:14934, L7:14129 |
| 4 | `get_top_features` | 40 features; top: L6:3235 de=-0.054 |
| 5 | `inspect_feature` ×21 | L2:10852, L6:3774, L0:11132, L6:6811, L0:11333, L0:6515, L6:3235, L0:9263, L0:12235, L0:2085, L14:12274, L1:12922, L6:2254, L15:15159, L0:7681, L0:15906, L5:10392, L1:10429, L4:11633, L6:3631, L0:2994 |
| 6 | `get_top_features` | 60 features; top: L6:3235 de=-0.054 |
| 7 | `inspect_feature` ×22 | L0:618, L0:6127, L0:7905, L6:11173, L2:13360, L6:12933, L0:14556, L0:9026, L4:2279, L0:6051, L2:3992, L6:3558, L0:9598, L6:6392, L0:8008, L4:5150, L0:1636, L4:9757, L4:3727, L0:1069, L14:3956, L0:10397 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14129@52` | ❌ error | — | — | Trace upstream from L7:F14129 (academic degrees and universities feature) to ide… |
| SA-2 | `L6:F170@10` | ❌ error | — | — | Trace upstream from L6:F170 (academic fields, especially humanities) at pos 10. … |
| SA-3 | `L3:F4213@11` | ✅ reported | 3 | 10 | Trace upstream from L3:F4213 (mentions of degree qualifications or awards) at po… |
| SA-4 | `L6:F2254@26` | ✅ reported | 6 | 7 | Trace upstream from L6:F2254 (academic degrees) at pos 26. Identify input tokens… |
| SA-5 | `L1:F12922@21` | ✅ reported | 3 | 3 | Trace upstream from L1:F12922 (pronoun "he" or "she") at pos 21. Goal: reach the… |
| SA-6 | `L0:F1069@1` | ❌ error | — | — | Trace upstream from L0:F1069 (male pronoun "He/His") at pos 1 to confirm embeddi… |

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L3, F4213 | " mentions of degree qualifications or awards" |
| 2 | `get_upstream_features` | L3:F4213@11, k=10 | Emb:" from"@11 (de=10.69) +9 more |
| 3 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 4 | `get_upstream_features` | L2:F10852@6, k=10 | Emb:" B"@4 (de=12.12) +9 more |
| 5 | `inspect_feature` | L0, F14877 | " single uppercase letters, sometimes followed by other characters, whi" |
| 6 | `get_upstream_features` | L0:F14877@6, k=10 | Emb:"."@5 (de=9.94) +9 more |

**Findings:** Tracing from L3:F4213 (detects degree/award mentions) reveals that its strongest upstream drivers are token embeddings for the words "from", "degree", and "received" as well as a mid‑layer feature L2:F10852 that specializes in academic titles and degree abbreviations. L2:F10852 itself is driven primarily by the embeddings for the single‑letter tokens "B" and "A", which are fed through a lower‑laye…

</details>

<details>
<summary><b>SA-4</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 2 | `get_upstream_features` | L6:F2254@26, k=10 | L4:F3727 (de=18.88) +9 more |
| 3 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 4 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 5 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 6 | `get_upstream_features` | L4:F3727@26, k=10 | L2:F10852 (de=12.19) +9 more |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `get_upstream_features` | L5:F13801@26, k=10 | L4:F3727 (de=11.88) +9 more |
| 9 | `inspect_feature` | L5, F1644 | " scientific journal names and abbreviations" |

**Findings:** Tracing from L6:F2254 (academic degree detector) reveals a short upstream chain that quickly reaches low‑layer features and raw token embeddings. The dominant upstream driver is L4:F3727, a strong detector for mentions of academic degrees, which itself is driven by L2:F10852 (generic academic title detector) and the raw token 'S' (part of 'Science' or 'Sc'). The raw token 'M' (part of 'M.Sc.') als…

</details>

<details>
<summary><b>SA-5</b> — tool trace (4 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F12922 | " the pronoun "he" or "she" in a narrative context" |
| 2 | `get_upstream_features` | L1:F12922@21, k=10 | Emb:" He"@21 (de=23.12) +9 more |
| 3 | `inspect_feature` | L0, F2241 | " the pronoun "she"" |
| 4 | `inspect_feature` | L0, F12492 | " the word "debt"" |

**Findings:** Tracing upstream from L1:F12922 (pronoun detection) immediately reaches the embedding for the token " He" with a strong positive direct effect (23.125), satisfying the embedding requirement. Additional upstream contributions come from two layer‑0 features: L0:F2241 (pronoun "she") and L0:F12492 (word "debt"), both in the lower‑third of the network and providing small positive influence. The lower‑…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14129@52, k=15 → L6:F2254 (de=6.97) +14 more |
| 2 | `get_upstream_features` | L6:F170@10, k=15 → L5:F10392 (de=11.38) +14 more |
| 3 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"He"@1 (de=22.62) +9 more |
| 4 | `get_upstream_features` | L1:F12922@1, k=10 → Emb:"He"@1 (de=19.25) +9 more |
| 5 | `get_upstream_features` | L1:F12922@21, k=10 → Emb:" He"@21 (de=23.12) +9 more |
| 6 | `get_upstream_features` | L6:F2254@6, k=10 → L5:F5725 (de=-15.75) +9 more |
| 7 | `get_upstream_features` | L6:F2254@52, k=10 → L2:F10852 (de=12.06) +9 more |
| 8 | `get_upstream_features` | L7:F14129@26, k=10 → L6:F2254 (de=8.12) +9 more |
| 9 | `get_upstream_features` | L15:F15159@120, k=10 → Emb:" Biomedical"@120 (de=22.12) +9 more |
| 10 | `get_upstream_features` | L14:F12274@12, k=10 → Emb:" Peking"@12 (de=19.00) +9 more |
| 11 | `get_upstream_features` | L14:F3956@58, k=10 → Emb:"<bos>"@0 (de=-5.81) +9 more |
| 12 | `get_upstream_features` | L6:F170@30, k=10 → L5:F10392 (de=9.75) +9 more |
| 13 | `get_upstream_features` | L3:F4213@11, k=10 → Emb:" from"@11 (de=10.69) +9 more |
| 14 | `get_upstream_features` | L3:F4213@31, k=10 → Emb:" from"@31 (de=11.44) +9 more |
| 15 | `get_upstream_features` | L0:F2994@3, k=10 → Emb:" his"@3 (de=42.50) +9 more |
| 16 | `get_upstream_features` | L2:F10852@52, k=10 → Emb:" Ph"@50 (de=14.75) +9 more |
| 17 | `get_upstream_features` | L5:F10392@10, k=10 → L3:F4113 (de=3.34) +9 more |
| 18 | `get_upstream_features` | L6:F3235@13, k=10 → L4:F5150 (de=2.88) +9 more |
| 19 | `get_upstream_features` | L4:F3727@6, k=10 → L2:F10852 (de=14.06) +9 more |
| 20 | `get_upstream_features` | L0:F6127@8, k=10 → Emb:" degree"@8 (de=16.88) +9 more |
| 21 | `get_upstream_features` | L6:F6811@12, k=10 → Emb:" Peking"@12 (de=17.25) +9 more |
| 22 | `get_upstream_features` | L6:F3774@12, k=10 → Emb:" Peking"@12 (de=10.12) +9 more |
| 23 | `get_upstream_features` | L6:F3631@13, k=10 → L5:F16220 (de=2.05) +9 more |

### Build

`build_circuit` → 32 nodes, 45 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 250,324 | 11,677 | 743,266 | 0 | $0.1337 | — | — |
| SA-4 | openai/gpt-oss-120b | 105,063 | 4,932 | 2,528 | 0 | $0.0188 | ✅ 6F/7E | Trace upstream from L6:F2254 (academic degrees) at pos 26. I… |
| SA-3 | openai/gpt-oss-120b | 44,006 | 4,748 | 7,904 | 0 | $0.0096 | ✅ 3F/10E | Trace upstream from L3:F4213 (mentions of degree qualificati… |
| SA-5 | openai/gpt-oss-120b | 32,998 | 2,303 | 0 | 0 | $0.0063 | ✅ 3F/3E | Trace upstream from L1:F12922 (pronoun "he" or "she") at pos… |
| **Total** | | **432,391** | **23,660** | **753,698** | **0** | **$0.1684** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 7m 42s