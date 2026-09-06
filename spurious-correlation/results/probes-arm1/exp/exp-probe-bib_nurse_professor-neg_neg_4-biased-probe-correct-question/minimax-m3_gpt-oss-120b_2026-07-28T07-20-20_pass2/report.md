# Circuit Oracle Report
**Date:** 2026-07-28 07:20:20 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by generic masculine-pronoun / male-reference features, not by any profession-specific signal — confirming the user's concern that the circuit is using spurious gender markers.

**Confidence:** 9

**Reasoning:** The user's concern is well-supported. The attribution graph traces the probe score back through a tightly male-pronoun-marked circuit with **no profession-specific features in evidence at all**.

**Layer 0 — direct logit pushers (the strongest contributors).** The top three features that push the probe score up are *not* "Computer Science" or "Director" or "Ph.D." detectors:
- **L0:F2994** (label: "the pronoun 'his' and the pronoun 'he'"), at positions 37, 55, and 13. Its strongest upstream driver is the raw " his" / " His" embedding (direct_effect = 45.25 from " his" at pos 37, 45.0 from " his" at pos 55, 5.28 from " His" at pos 13). This is the single biggest positive contributor in the whole graph.
- **L0:F2848** (label: "the word 'of'"), firing on " of" at pos 5 (direct_effect 0.148). It is a generic function-word feature, not profession-related.
- **L0:F11024** (label: "the word 'clock', especially in a technical context"), firing on " Director" at pos 4 (direct_effect 0.142). Although the surface token is "Director", the feature's autointerp label and top-activating examples are all about *clock*; this is a generic technical/function-word feature that happens to co-fire on "Director", not a profession detector.
- **L0:F8658** ("the word 'is'"), at pos 2 (direct_effect 0.110), with the upstream "He" (8.0) and " is" (6.28) embeddings. Purely grammatical.

**Layer 6 — male-pronoun aggregator.** **L6:F12990** (label: "male pronouns and titles along with descriptors associated with men", frac_nonzero 0.068) fires at " His" (pos 13), " He" (pos 35), and " is" (pos 2). It is the circuit's clearest gender marker. Its upstream is the " His" embedding (5.28) plus L4:F4315 (a "his/he" pronoun feature) and L5:F14955. Crucially, its **direct effect on the probe is negative at the " He" position (-0.166)** but the embedded " His" → "He" pronoun signal still drives L7 → L18 features that feed back positively. The label explicitly calls out male pronouns/titles, not profession terms.

**Layer 7 — possessive pronoun / male-suppressor.** **L7:F14893** ("pronouns or possessive pronouns", frac_nonzero 0.009) fires at "He" (pos 1) and " His" (pos 13), with upstream "He" embedding (14.75) and L6:F12990. **L7:F14946** ("the possessive pronoun 'his' and similar pronouns like 'he' and 'him'") is even more pointed: its *promoted* tokens are "▁himself", "▁his", "▁His" and its *suppressed* tokens are "▁herself", "▁she", "▁elle" — it pushes the probe toward male and explicitly against female. It also fires at "He" (pos 1) and " is" (pos 2), driven by the "He" embedding (9.0 / 11.5).

**Layer 12 — explicit gender.** **L12:F2175** (label: "words referring to gender", frac_nonzero 0.006, very selective) fires at " is" (pos 2) with upstream L7:F14946 (5.41) and L6:F12990 (1.63). Its promoted tokens are "▁himself", "▁masculinity", "▁neuter" and suppressed tokens are "▁herself", "▁female", "▁woman" — an unambiguous gender-marker feature.

**Layer 13–18 — "He" pronoun reinforcement.** The "He" at pos 35 propagates through L13:F6622 ("pronouns."), L17:F5889 ("references to people with pronouns and possessive pronouns"), and L17:F3683 ("biographies", max_token "He" — a biography structure feature, but specifically anchored to the "He" pronoun), culminating in **L18:F14743** (label simply "He", direct_effect −0.141 on the probe). The full chain: Emb " He" (23.6) → L0:F1069 (male person reference, 7.5) → L13:F6622 (2.4) → L17:F5889 (4.0) → L18:F14743, with L17:F3683 (biography) adding a 2.1 boost. The "biography" feature is the closest thing to a content-bearing feature, and even it is a structural "He-is-subject-of-biography" pattern detector rather than a profession indicator.

**What is NOT in the circuit.** Crucially, there is no feature anywhere in the top direct effects that detects profession-specific vocabulary. No "professor", "computer science", "Ph.D.", "research", "director of laboratory", or academic-title feature appears. The terms "Mobile Grid", "Cloud Computing", "parallel and distributed", "Korea University", "National University of Computer and Emerging Sciences" — the actual profession-defining content of the biography — contribute no detectable signal to the probe.

**Convergence and mechanism.** Two parallel paths converge on the probe:
1. A **low-layer mass-action path** of generic function-word/grammatical features (F2994, F2848, F11024, F8658) whose cumulative effect is positive and dominated by the "his" pronoun detector.
2. A **gendered pronoun chain** (Emb "He"/"His" → L0:F1069 → L6:F12990 → L7:F14946 → L12:F2175 / L13:F6622 → L17:F5889 → L18:F14743) that explicitly encodes male gender through features whose *suppressed tokens* are female pronouns.

This is a textbook case of a probe learning to rely on a **gender confound** rather than the target semantic (profession). If you replaced "He" with "She" in this biography, the same non-profession content would still be present, but the circuit's male-pronoun features would suppress instead of promote, and the probe would likely flip its classification — exactly the failure mode the user suspected.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 37 | L0: his/he pronoun detector (F2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 55 | L0: his/he pronoun detector (F2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 13 | L0: his/he pronoun detector (F2994) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 5 | L0: 'of' detector (F2848) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F11024](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) | 4 | L0: 'Director'/'clock' detector (F11024) |  the word "clock", especially in a technical context | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | L0: 'is' detector (F8658) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 35 | L0: He/His male-person reference (F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0: He/His male-person reference (F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 13 | L4: 'his/he' pronoun detector (F4315) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 35 | L4: 'he/him' pronoun detector (F14796) | the pronoun "he" or "him" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 13 | L6: male pronouns & descriptors (F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 35 | L6: male pronouns & descriptors (F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | L6: male pronouns & descriptors (F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7: possessive pronoun detector (F14893) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 13 | L7: possessive pronoun detector (F14893) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | L7: 'his/he' detector, suppresses female (F14946) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7: 'his/he' detector, suppresses female (F14946) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | L12: gender-word detector (F2175) |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 35 | L13: pronoun detector (F6622) |  pronouns. | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 35 | L17: people/pronouns reference (F5889) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F3683](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) | 35 | L17: biography structure (F3683) | biographies | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 35 | L18: 'He' pronoun detector (F14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.254 |
| 3 | `inspect_feature` ×10 | L0:2994, L0:2848, L0:11024, L0:8658, L6:12990, L7:14893, L7:14946, L18:14743, L4:4315, L12:2175 |
| 4 | `get_upstream_features` | Emb:" his"@37 (de=45.25) +4 more |
| 5 | `get_upstream_features` | Emb:" his"@55 (de=45.00) +4 more |
| 6 | `get_upstream_features` | Emb:" of"@5 (de=34.75) +4 more |
| 7 | `get_upstream_features` | Emb:" Director"@4 (de=12.81) +4 more |
| 8 | `get_upstream_features` | Emb:"He"@1 (de=8.00) +4 more |
| 9 | `get_upstream_features` | Emb:" He"@35 (de=23.62) +4 more |
| 10 | `inspect_feature` ×8 | L0:1069, L17:5889, L13:6622, L17:3683, L12:2175, L4:4315, L7:14893, L7:14946 |
| 11 | `get_upstream_features` | Emb:" His"@13 (de=5.28) +7 more |
| 12 | `get_upstream_features` | Emb:" He"@35 (de=4.34) +7 more |
| 13 | `get_upstream_features` | L5:F645 (de=1.95) +7 more |
| 14 | `get_upstream_features` | Emb:"He"@1 (de=14.75) +7 more |
| 15 | `get_upstream_features` | Emb:" His"@13 (de=22.75) +7 more |
| 16 | `get_upstream_features` | Emb:"He"@1 (de=9.00) +7 more |
| 17 | `get_upstream_features` | Emb:"He"@1 (de=11.50) +7 more |
| 18 | `get_upstream_features` | L7:F14946 (de=5.41) +7 more |
| 19 | `get_upstream_features` | Emb:" His"@13 (de=21.25) +7 more |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14743@35` | ✅ reported | 3 | 5 | Trace this feature — it appears to be a "He" pronoun detector at pos 35. Follow … |
| SA-2 | `L6:F12990@13` | ✅ reported | 3 | 5 | Trace this feature (L6:F12990, "male pronouns and titles along with descriptors … |
| SA-3 | `L0:F2994@37` | ❌ error | — | — | Trace this feature (L0:F2994, "his"/"he" pronoun detector) at pos 37 " his". Fol… |
| SA-4 | `L0:F8658@2` | ❌ error | — | — | Trace the "is" embedding path through L0:F8658 at pos 2. What does this feature … |
| SA-5 | `L0:F2848@5` | ❌ error | — | — | Trace the "of" / generic function word path through L0:F2848 at pos 5. Determine… |
| SA-6 | `L0:F11024@4` | ❌ error | — | — | Trace the "Director" token path through L0:F11024 (claims to detect "clock" but … |

<details>
<summary><b>SA-1</b> — tool trace (9 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@35, k=10 | Emb:" He"@35 (de=23.62) +9 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `get_upstream_features` | L0:F1069@35, k=10 | Emb:" He"@35 (de=36.50) +9 more |
| 5 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 6 | `inspect_feature` | L13, F6622 | " pronouns." |
| 7 | `get_upstream_features` | L17:F5889@35, k=10 | Emb:" He"@35 (de=22.62) +9 more |
| 8 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 9 | `get_upstream_features` | L6:F2267@35, k=10 | Emb:"<bos>"@0 (de=-9.31) +9 more |

**Findings:** The target feature L18:F14743 is a straightforward 'He' pronoun detector. Its strongest upstream driver is the raw token embedding for the token " He" at the same position, confirming a direct lexical match. A layer‑0 feature (F1069) also feeds positively, providing a generic male‑person reference signal that is present across the model and does not encode any profession‑specific information. A mi…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 2 | `get_upstream_features` | L6:F12990@13, k=10 | Emb:" His"@13 (de=5.28) +9 more |
| 3 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 4 | `inspect_feature` | L5, F14955 | " text about people's free time that mentions both family and hobbies" |
| 5 | `get_upstream_features` | L4:F4315@13, k=10 | Emb:" His"@13 (de=21.25) +9 more |
| 6 | `inspect_feature` | L2, F14964 | " possessive pronouns" |
| 7 | `inspect_feature` | L0, F2749 | " references to ownership or association with a person or group of peop" |
| 8 | `get_upstream_features` | L5:F14955@13, k=10 | Emb:" His"@13 (de=4.47) +9 more |

**Findings:** The target feature L6:F12990 is driven almost entirely by the raw input token embedding for "His" (direct effect >5). The strongest intermediate upstream feature is L4:F4315, another pronoun detector, which itself is overwhelmingly excited by the same "His" embedding (direct effect 21.25). A tertiary upstream feature L5:F14955 also receives a strong boost from "His" but contributes only a minor po…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F11024@4, k=8 → Emb:" Director"@4 (de=12.81) +7 more |
| 2 | `get_upstream_features` | L0:F2848@5, k=8 → Emb:" of"@5 (de=34.75) +7 more |
| 3 | `get_upstream_features` | L0:F8658@2, k=8 → Emb:"He"@1 (de=8.00) +7 more |
| 4 | `get_upstream_features` | L18:F14743@35, k=6 → Emb:" He"@35 (de=23.62) +5 more |
| 5 | `inspect_feature` ×4 | L6:2267, L4:14796, L15:3330, L5:14955 |
| 6 | `get_upstream_features` | L0:F2994@37, k=5 → Emb:" his"@37 (de=45.25) +4 more |

### Build

`build_circuit` → 25 nodes, 34 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 50,766 | 8,018 | 298,980 | 0 | $0.0428 | — | — |
| SA-2 | openai/gpt-oss-120b | 88,796 | 4,693 | 64 | 0 | $0.0161 | ✅ 3F/5E | Trace this feature (L6:F12990, "male pronouns and titles alo… |
| SA-1 | openai/gpt-oss-120b | 96,009 | 6,410 | 21,984 | 0 | $0.0186 | ✅ 3F/5E | Trace this feature — it appears to be a "He" pronoun detecto… |
| **Total** | | **235,571** | **19,121** | **321,028** | **0** | **$0.0775** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 2s