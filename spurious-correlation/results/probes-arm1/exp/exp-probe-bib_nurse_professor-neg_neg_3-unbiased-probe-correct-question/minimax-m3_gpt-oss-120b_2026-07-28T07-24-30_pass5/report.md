# Circuit Oracle Report
**Date:** 2026-07-28 07:24:30 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit is saved. Now I have a comprehensive picture of the probe classification.

**Analysis:** The probe's "professor" classification score is driven by a multi-path circuit, not by gender markers — the primary signal comes from degree/credential recognition features across L0–L7, with parallel contributions from entity-recognizing features driven by the "Peking" token (L6 proper-noun/geo-name features) and a "he"-pronoun circuit (L1 F12922) that fires on the "He" tokens (pos 1, 21, 42) common to most academic biographies. The "he" pronoun path is spurious in the sense that it's a generic narrative-pronoun pattern, not a gender signal per se, and the high-layer L20 academic-credentials feature actually *inhibits* the probe — meaning the probe fires on the "received his B.A./Ph.D. degree" template as a *style* of academic-biography text, not on the profession itself.

**Confidence:** 5

**Reasoning:** Examining the attribution graph: (1) **L2 F10852** ("academic titles and degrees", frac_nonzero=0.008, low-frac, fires on "B.A.", "M.S.", "Ph.D." tokens at positions 6, 26, 47, 52) is the strongest single contributor at direct_effect=−0.0535 and is suppressed by the probe direction — meaning the probe is *anti-correlated* with explicit degree tokens. (2) **L0 features** at "B" (pos 4, emb_ba_4 direct_effect=12.1), "A" (pos 6), "Ph" (pos 50), and "D" (pos 52) feed L2 F10852 and L1 F10132 (the "D"-as-PhD-abbreviation feature, frac_nonzero=0.0023, fires specifically on the "D" in "Ph.D."), but these are again degree-recognition features, not profession-specific. (3) **L6 F3774** ("proper nouns with unusual capitalization", direct_effect=−0.053) and **L6 F6811** ("newly-discovered microorganism/place names", direct_effect=−0.045) are driven almost entirely by the "Peking" token at pos 12 (emb_peking_12→F6811 direct_effect=17.25), and they inhibit the probe — suggesting the model treats "Peking University" as a foreign/geo entity rather than a profession signal. (4) **L7 F14129** ("academic degrees, universities, and people", frac_nonzero=0.004, direct_effect=+0.043) is the most positively-correlated late-layer feature, but its upstream is the L6 F2254 degree-reference supernode plus the L5 F10392 "fields of academic study" supernode (which fires on "Mathematics" at pos 10 with direct_effect=11.4 from the embedding). (5) The **L1 F12922 "he/she" pronoun** path is real but mild: it appears at pos 1, 21, 42 (the three "He received his..." sentence starts) with direct_effect≈23 each on the feature but only +0.024–0.032 on the probe — the pronoun itself is not gender-encoding (the autointerp explicitly notes it fires equally on "he" and "she" in narrative contexts). (6) The **L20 F14235 "academic credentials and institutions"** supernode is paradoxically *inhibitory* (direct_effect=−0.0215 at pos 58) — i.e. by the time the model has built a high-level "academic biography" representation, that representation pushes *against* the probe. (7) The L15 F15159 "medicine/healthcare" feature (driven by the "Biomedical" continuation token at pos 120) provides a small positive push (+0.029) — but this is from text *outside* the truncated prompt, so it's context-only.

**The user's concern about "spurious gender markers" is partially validated but reframed:** the L1 F12922 pronoun feature is a genuine component of the circuit, but it is *not* a gender marker — it is a generic "narrative third-person pronoun" detector (autointerp: "the pronoun 'he' or 'she' in a narrative context", promoted tokens do not include gendered profession terms; it fires in both male and female biographies). Its direct contribution to the probe is small (~+0.024–0.032). The *real* spurious mechanism is that the probe is driven by a *textual template* — "He received his B.A./M.S./Ph.D. degree from [University]" — rather than by the profession itself. The probe classification is essentially a "is this an academic biography in standard CV format?" classifier. The "he" pronouns contribute because academic-biography templates more often use "he", but the L1 F12922 feature itself is pronoun-agnostic; any gendered correlation arises from co-occurrence with the biographical template, not from a learned gender→profession mapping. The probe does *not* appear to encode "he = professor, she = other profession"; it encodes a template that happens to use "he" historically.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'He' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: 'He' (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 42 | Emb: 'He' (pos 42) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L1:F12922](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12922) | 1 | L1 F12922 — 'he/she' pronoun in narrative context (drives the pronoun circuit) |  the pronoun "he" or "she" in a narrative context | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12922) |
| [L1:F12922](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12922) | 21 | L1 F12922 — 'he/she' pronoun in narrative context (drives the pronoun circuit) |  the pronoun "he" or "she" in a narrative context | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12922) |
| [L1:F12922](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12922) | 42 | L1 F12922 — 'he/she' pronoun in narrative context (drives the pronoun circuit) |  the pronoun "he" or "she" in a narrative context | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12922) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: 'B' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: 'A' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 50 | Emb: 'Ph' (pos 50) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 52 | Emb: 'D' (pos 52) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: 'Peking' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: 'Mathematics' (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F9263](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9263) | 8 | L0 features — degree/academic terms (low-frac features at token positions 6, 8, 10, 12, 17, 18) |  mentions of academic qualifications and precise temperature values | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9263) |
| [L0:F6127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) | 8 | L0 features — degree/academic terms (low-frac features at token positions 6, 8, 10, 12, 17, 18) |  instances of the word "degree" and words associated with academia, especially higher education | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 12 | L0 features — degree/academic terms (low-frac features at token positions 6, 8, 10, 12, 17, 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 17 | L0 features — degree/academic terms (low-frac features at token positions 6, 8, 10, 12, 17, 18) |  the year 199X or 200X. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 18 | L0 features — degree/academic terms (low-frac features at token positions 6, 8, 10, 12, 17, 18) |  a mix of possessive pronouns like "his", names associated with historical records, and years. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 18 | L0 features — degree/academic terms (low-frac features at token positions 6, 8, 10, 12, 17, 18) |  the 1990's | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F14934](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14934) | 18 | L0 features — degree/academic terms (low-frac features at token positions 6, 8, 10, 12, 17, 18) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14934) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 52 | L1 F10132 — abbreviation 'D' for Ph.D. (specific to 'D' token at pos 52) |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 6 | L2 F10852 — academic titles/degrees (low-frac 0.008, frac_nonzero=0.008) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 26 | L2 F10852 — academic titles/degrees (low-frac 0.008, frac_nonzero=0.008) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 47 | L2 F10852 — academic titles/degrees (low-frac 0.008, frac_nonzero=0.008) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 52 | L2 F10852 — academic titles/degrees (low-frac 0.008, frac_nonzero=0.008) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 11 | L3 F4213 — mentions of degree qualifications/awards (low-frac 0.012) |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 31 | L3 F4213 — mentions of degree qualifications/awards (low-frac 0.012) |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 49 | L3 F4213 — mentions of degree qualifications/awards (low-frac 0.012) |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 58 | L3 F4213 — mentions of degree qualifications/awards (low-frac 0.012) |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L3:F11994](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) | 52 | L3 F11994 — academic degrees/professional titles (PhD context) |  academic degrees and professional titles, especially involving "Ph.D." | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) |
| [L3:F11994](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) | 6 | L3 F11994 — academic degrees/professional titles (PhD context) |  academic degrees and professional titles, especially involving "Ph.D." | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) |
| [L3:F11994](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) | 26 | L3 F11994 — academic degrees/professional titles (PhD context) |  academic degrees and professional titles, especially involving "Ph.D." | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11994) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 6 | L4 F3727 — mentions of academic degrees (drives 'B.A.', 'Ph.D.' tokens) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 26 | L4 F3727 — mentions of academic degrees (drives 'B.A.', 'Ph.D.' tokens) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 47 | L4 F3727 — mentions of academic degrees (drives 'B.A.', 'Ph.D.' tokens) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 52 | L4 F3727 — mentions of academic degrees (drives 'B.A.', 'Ph.D.' tokens) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L5:F5725](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) | 6 | L5 F5725 — educational history incl. degrees and schools (inhibits downstream) |  people's educational history including degrees and schools | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) |
| [L5:F5725](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) | 26 | L5 F5725 — educational history incl. degrees and schools (inhibits downstream) |  people's educational history including degrees and schools | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) |
| [L5:F5725](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) | 47 | L5 F5725 — educational history incl. degrees and schools (inhibits downstream) |  people's educational history including degrees and schools | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) |
| [L5:F5725](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) | 52 | L5 F5725 — educational history incl. degrees and schools (inhibits downstream) |  people's educational history including degrees and schools | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 52 | L5 F13801 — abbreviations for degrees (M.S., PhD, etc.) | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | L5 F10392 — fields of academic study ('Computer Science', 'Mathematics') |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 30 | L5 F10392 — fields of academic study ('Computer Science', 'Mathematics') |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 6 | L6 F2254 — references to academic degrees ('M.Sc.', 'Doctor') | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 26 | L6 F2254 — references to academic degrees ('M.Sc.', 'Doctor') | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 47 | L6 F2254 — references to academic degrees ('M.Sc.', 'Doctor') | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 52 | L6 F2254 — references to academic degrees ('M.Sc.', 'Doctor') | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | L6 F170 — references to academic fields (especially humanities) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 30 | L6 F170 — references to academic fields (especially humanities) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 57 | L6 F170 — references to academic fields (especially humanities) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 12 | L6 F3235 — academic publications, math & scientific institutions (inhibitory) |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 13 | L6 F3235 — academic publications, math & scientific institutions (inhibitory) |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 12 | L6 F3774 — proper nouns/names with unusual capitalization (driven by 'Peking') |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 13 | L6 F3774 — proper nouns/names with unusual capitalization (driven by 'Peking') |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L6:F6811](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) | 12 | L6 F6811 — newly discovered microorganism/place names (driven by 'Peking') |  names of newly discovered microorganisms and places | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) |
| [L6:F6811](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) | 13 | L6 F6811 — newly discovered microorganism/place names (driven by 'Peking') |  names of newly discovered microorganisms and places | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6811) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 26 | L7 F14129 — academic degrees, universities, and people associated with them (drives the probe POSITIVELY) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 47 | L7 F14129 — academic degrees, universities, and people associated with them (drives the probe POSITIVELY) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 52 | L7 F14129 — academic degrees, universities, and people associated with them (drives the probe POSITIVELY) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 58 | L7 F14129 — academic degrees, universities, and people associated with them (drives the probe POSITIVELY) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L14:F12274](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12274) | 12 | L14 F12274 — mentions of China, Korea, technology (driven by 'Peking', inhibitory to probe) |  mentions of China, Korea, technology, and conflict | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/12274) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 120 | L15 F15159 — words related to medicine/healthcare (driven by 'Biomedical' pos 120, POSITIVELY) |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 31 | L17 F11003 — 'university' feature (drives L19/L20 supernodes) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 58 | L17 F11003 — 'university' feature (drives L19/L20 supernodes) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 31 | L19 F2496 — mentions of universities and degrees (drives L20) |  mentions of universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 58 | L19 F2496 — mentions of universities and degrees (drives L20) |  mentions of universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 31 | L20 F14235 — references to academic credentials and institutions (HIGHLY INHIBITORY to probe) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 58 | L20 F14235 — references to academic credentials and institutions (HIGHLY INHIBITORY to probe) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 91 | L20 F14235 — references to academic credentials and institutions (HIGHLY INHIBITORY to probe) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:3235 de=-0.054 |
| 3 | `inspect_feature` ×18 | L6:3235, L2:10852, L6:3774, L0:15320, L0:6270, L6:6811, L0:11132, L0:11333, L3:4213, L6:170, L2:14934, L0:6515, L0:9263, L0:12235, L7:14129, L0:618, L0:2085, L0:6127 |
| 4 | `get_upstream_features` | L6:F2254 (de=6.97) +9 more |
| 5 | `inspect_feature` | " the word "ice"" |
| 6 | `get_top_features` | 50 features; top: L6:3235 de=-0.054 |
| 7 | `get_upstream_features` | L2:F10852 (de=12.06) +9 more |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F12274@12` | ❌ error | — | — | Trace this mid-layer feature upstream. What tokens/earlier features drive it? Is… |
| SA-2 | `L15:F15159@120` | ❌ error | — | — | Trace this late-layer feature upstream. What does it encode and what input featu… |
| SA-3 | `L7:F14129@26` | ❌ error | — | — | Trace this L7 feature upstream. What does it encode about academic credentials a… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F2254@6, k=10 → L5:F5725 (de=-15.75) +9 more |
| 2 | `get_upstream_features` | L6:F2254@26, k=10 → L4:F3727 (de=18.88) +9 more |
| 3 | `inspect_feature` | L6, F2254 → "references to academic degrees" |
| 4 | `get_upstream_features` | L14:F12274@12, k=10 → Emb:" Peking"@12 (de=19.00) +9 more |
| 5 | `get_upstream_features` | L15:F15159@120, k=10 → Emb:" Biomedical"@120 (de=22.12) +9 more |
| 6 | `inspect_feature` | L6, F2254 → "references to academic degrees" |
| 7 | `get_upstream_features` | L1:F12922@21, k=10 → Emb:" He"@21 (de=23.12) +9 more |
| 8 | `get_upstream_features` | L1:F12922@1, k=10 → Emb:"He"@1 (de=19.25) +9 more |
| 9 | `inspect_feature` ×5 | L1:12922, L6:3631, L6:3558, L6:11173, L6:12933 |
| 10 | `get_upstream_features` | L15:F15159@120, k=10 → Emb:" Biomedical"@120 (de=22.12) +9 more |
| 11 | `inspect_feature` | L15, F15159 → " words related to medicine and healthcare" |
| 12 | `get_upstream_features` | L14:F12274@12, k=10 → Emb:" Peking"@12 (de=19.00) +9 more |
| 13 | `inspect_feature` | L14, F12274 → " mentions of China, Korea, technology, and conflict" |
| 14 | `get_upstream_features` | L1:F10132@52, k=10 → Emb:" Ph"@50 (de=16.25) +9 more |
| 15 | `get_upstream_features` | L5:F13801@52, k=10 → L2:F10852 (de=7.38) +9 more |
| 16 | `get_upstream_features` | L4:F3727@6, k=10 → L2:F10852 (de=14.06) +9 more |
| 17 | `get_upstream_features` | L4:F3727@26, k=10 → L2:F10852 (de=12.19) +9 more |
| 18 | `inspect_feature` ×5 | L4:3727, L5:5725, L5:13801, L3:11994, L6:4490 |
| 19 | `get_upstream_features` | L2:F10852@52, k=10 → Emb:" Ph"@50 (de=14.75) +9 more |
| 20 | `get_upstream_features` | L2:F10852@6, k=10 → Emb:" B"@4 (de=12.12) +9 more |
| 21 | `inspect_feature` ×2 | L0:1636, L1:2415 |
| 22 | `get_upstream_features` | L1:F10132@52, k=10 → Emb:" Ph"@50 (de=16.25) +9 more |
| 23 | `inspect_feature` | L1, F10132 → " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 24 | `get_upstream_features` | L3:F8294@52, k=10 → L2:F10852 (de=7.44) +9 more |
| 25 | `inspect_feature` | L3, F8294 → " words and phrases related to advanced education, research, and high-l" |
| 26 | `get_upstream_features` | L4:F13943@52, k=10 → L2:F10852 (de=7.66) +9 more |
| 27 | `inspect_feature` | L4, F13943 → " words and abbreviations related to academic research" |
| 28 | `get_upstream_features` | L3:F4213@11, k=10 → Emb:" from"@11 (de=10.69) +9 more |
| 29 | `inspect_feature` | L3, F4213 → " mentions of degree qualifications or awards" |
| 30 | `get_upstream_features` | L6:F170@10, k=10 → L5:F10392 (de=11.38) +9 more |
| 31 | `get_upstream_features` | L6:F3235@12, k=10 → Emb:" Peking"@12 (de=4.53) +9 more |
| 32 | `get_upstream_features` | L6:F6811@12, k=10 → Emb:" Peking"@12 (de=17.25) +9 more |
| 33 | `get_upstream_features` | L6:F3774@12, k=10 → Emb:" Peking"@12 (de=10.12) +9 more |
| 34 | `inspect_feature` ×2 | L4:4257, L5:10392 |
| 35 | `get_upstream_features` | L6:F170@30, k=10 → L5:F10392 (de=9.75) +9 more |
| 36 | `get_upstream_features` | L0:F9026@12, k=10 → Emb:" Peking"@12 (de=46.75) +9 more |
| 37 | `get_upstream_features` | L3:F4213@31, k=10 → Emb:" from"@31 (de=11.44) +9 more |
| 38 | `get_upstream_features` | L3:F4213@49, k=5 → L2:F10852 (de=5.03) +4 more |
| 39 | `get_top_features` | token="", k=100 → 100 features; top: L6:3235 de=-0.054 |
| 40 | `get_upstream_features` | L20:F14235@58, k=10 → L17:F11003 (de=29.75) +9 more |
| 41 | `inspect_feature` ×2 | L20:14235, L7:14291 |
| 42 | `get_upstream_features` | L20:F14235@31, k=10 → L17:F11003 (de=30.00) +9 more |
| 43 | `get_upstream_features` | L14:F3956@58, k=10 → Emb:"<bos>"@0 (de=-5.81) +9 more |
| 44 | `inspect_feature` ×3 | L14:3956, L17:11003, L19:2496 |
| 45 | `get_upstream_features` | L17:F11003@58, k=10 → Emb:"<bos>"@0 (de=-9.19) +9 more |
| 46 | `get_upstream_features` | L17:F11003@31, k=10 → Emb:"<bos>"@0 (de=-7.16) +9 more |
| 47 | `get_upstream_features` | L19:F2496@58, k=10 → L17:F11003 (de=13.94) +9 more |
| 48 | `get_upstream_features` | L19:F2496@31, k=10 → L17:F11003 (de=13.88) +9 more |
| 49 | `get_upstream_features` | L1:F12922@42, k=5 → Emb:" He"@42 (de=23.12) +4 more |
| 50 | `inspect_feature` | L0, F8974 → "the word "from"" |
| 51 | `get_upstream_features` | L6:F2254@47, k=5 → L4:F3727 (de=19.38) +4 more |
| 52 | `get_upstream_features` | L6:F3631@12, k=5 → Emb:" Peking"@12 (de=6.09) +4 more |
| 53 | `get_upstream_features` | L6:F3631@13, k=5 → L5:F16220 (de=2.05) +4 more |
| 54 | `inspect_feature` ×2 | L5:16220, L5:4052 |
| 55 | `get_upstream_features` | L6:F2254@52, k=5 → L2:F10852 (de=12.06) +4 more |
| 56 | `get_upstream_features` | L0:F11132@18, k=5 → Emb:"9"@17 (de=11.06) +4 more |
| 57 | `get_upstream_features` | L0:F11132@39, k=5 → Emb:"9"@38 (de=10.94) +4 more |
| 58 | `get_upstream_features` | L2:F14934@18, k=5 → L0:F6515 (de=8.25) +4 more |
| 59 | `get_upstream_features` | L0:F11333@18, k=5 → Emb:"9"@17 (de=11.38) +4 more |

### Build

`build_circuit` → 31 nodes, 42 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 117,069 | 12,023 | 1,114,787 | 0 | $0.1164 | — | — |
| **Total** | | **117,069** | **12,023** | **1,114,787** | **0** | **$0.1164** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 54s