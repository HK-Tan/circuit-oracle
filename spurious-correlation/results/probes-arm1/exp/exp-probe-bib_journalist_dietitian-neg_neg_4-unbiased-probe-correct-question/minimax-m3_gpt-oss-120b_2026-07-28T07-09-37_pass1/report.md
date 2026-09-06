# Circuit Oracle Report
**Date:** 2026-07-28 07:09:37 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mix of genuine profession-context signals (journalism/writing concepts anchored to the token "writer") and strong spurious surface-level cues (e.g., a "he"-pronoun feature, an "Institute" word detector, period/comma features, and the Middle East phrase), with the journalism-related late-layer features pushing the probe *negatively* (i.e., distinguishing the subject from a generic journalist category).

**Confidence:** 7

**Reasoning:** The circuit reaches embedding nodes at positions 28 ("writer"), 27 ("freelance"), 7 ("Institute"), 22 ("he"), 14/15 ("Middle"/"East"), and 12 ("covering"). The most causally influential late-layer feature is **L14:F4420 (pos 28) — "words and phrases related to journalism and newspapers"** with direct_effect = -0.0679 (NEGATIVE on the probe). Its traceback shows the signal is driven by the raw token "writer" (embedding direct_effect ≈ 5.75) propagating through **L0:F7376 (writers/writing, frac_nonzero=0.052)** → **L4:F13253 (journalism/media, frac_nonzero=0.0065)** → **L7:F72 (professional writing, frac_nonzero=0.011)** → **L8:F8855 (reporters/reporting, frac_nonzero=0.0085)** → L14:F4420. **L6:F12712 (editor/publisher titles, frac_nonzero=0.0175)** at pos 28 is also a major negative contributor (direct_effect = -0.0593) and is itself fed by the "writer" embedding (direct_effect = 6.22) and "freelance" (3.38) plus a media-context feature. So far the profession-related signal is real — the "writer" token genuinely connects through journalism-relevant concepts.

However, the user's concern about spurious features is well-founded. The **top of the feature list** is dominated by L0 surface detectors, not by profession-encoding features:
- **L0:F12768** at pos 22 (he/she pronoun feature, direct_effect = +0.0747, the single largest positive contributor) — this fires on the pronoun "he" (embedding direct_effect = 40.25) and is literally a **gender marker**, not a profession indicator. Its autointerp label explicitly says "mentions of 'he' and 'she' in close proximity."
- **L0:F7124** at pos 2 ("at", direct_effect = -0.1572, the single largest negative contributor overall) — a trivial preposition detector driven by the embedding "at" (31.4).
- **L0:F15661, L0:F6484** at pos 7 (both "Institute"-related detectors, direct_effect = -0.0942 and -0.0684) — these are driven by the literal embedding "Institute" (19.4 and 15.1 direct_effect) and label themselves as "the word 'spin'" and "the word 'sky'" — likely noise/polysemy artifacts.
- **L0:F13096** at pos 3 ("the", direct_effect = -0.051) — generic article detector.
- **L0:F10881** at pos 12 ("coverage", direct_effect = +0.0586) and **L0:F15880** at pos 15 (Middle East, direct_effect = +0.0432) — **topic/domain** detectors (defence coverage topics) rather than profession indicators.
- **L0:F3007** at pos 14 ("middle", direct_effect = +0.0596) and **L0:F1229** at pos 14 ("middle", direct_effect = -0.0574) — the *word* "middle" is being detected (autointerp confirms: "the word 'middle'…") in the context of "Middle East" — a geographic token, not a profession cue.
- **L0:F6051** at pos 38 (periods/spaces, direct_effect = -0.0505), **L0:F14824** at pos 40 ("has", direct_effect = -0.041), **L0:F4870** at pos 11 (commas, direct_effect = -0.042) — pure punctuation/function-word detectors.

A parallel spurious path operates via **L1:F4459 (pos 7, "research institutes", direct_effect = -0.0588, frac_nonzero=0.003)** → **L3:F10489 (pos 7, "the word 'Institute'", direct_effect = -0.0542, frac_nonzero=0.0036)**, both fed by the "Institute" embedding (27.1, 27.5) — these are encoding institutional affiliation context, not the profession. **L2:F12901** at pos 15 ("Middle East", direct_effect = -0.054, frac_nonzero=0.0045) is a pure geographic-phrase detector.

**Convergence/conclusion:** The profession-related sub-circuit (writer → journalism → editors) is *real but predominantly NEGATIVE* on the probe, meaning the probe is actually classifying the subject as *not a journalist* despite the writing evidence. The largest positive drivers are spurious or off-target: the **he-pronoun feature** (gender), the **"Middle" word detector** (geography), the **"coverage" word detector** (domain), and the **"at" preposition detector**. This strongly validates the user's concern: the probe is leaning heavily on the gender marker "he", topic tokens (Middle East, Institute, defence, coverage), and syntactic particles (at, the, commas, periods), with the genuine profession signal (the journalism/writing chain) working *against* the classification rather than for it.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | Journalism/newspapers feature (drives probe negatively) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 28 | Reporters/reporting feature |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L7:F72](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/72) | 28 | Professional writing terms |  words related to writing professionally | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/72) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 28 | Professional writing terms |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 28 | Editor/publisher titles + Broadcasting/TV/radio |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L6:F10984](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10984) | 71 | Editor/publisher titles + Broadcasting/TV/radio |  mentions of TV and radio broadcasting | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10984) |
| [L6:F5849](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5849) | 28 | Editor/publisher titles + Broadcasting/TV/radio |  references to blogs and blog posts | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/5849) |
| [L6:F6721](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6721) | 28 | Editor/publisher titles + Broadcasting/TV/radio |  html code and related tags particularly href, public, content, title, website and related terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6721) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | Media/journalism concepts + Reports/documentaries |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F661](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) | 28 | Media/journalism concepts + Reports/documentaries |  words and phrases used when referring to reports, documentaries, and television coverage of news | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) |
| [L4:F5060](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5060) | 7 | Media/journalism concepts + Reports/documentaries | references to institutions and technology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5060) |
| [L4:F7056](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7056) | 71 | Media/journalism concepts + Reports/documentaries | references to radio broadcasting | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7056) |
| [L3:F10489](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10489) | 7 | The word 'Institute' |  the word "Institute" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/10489) |
| [L2:F9995](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) | 28 | Occupations/Middle East phrase/writing terms |  terms related to occupations and fields of study | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) |
| [L2:F9210](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9210) | 28 | Occupations/Middle East phrase/writing terms | words related to journalism, writing, and articles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9210) |
| [L2:F12901](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12901) | 15 | Occupations/Middle East phrase/writing terms |  the phrase "Middle East" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12901) |
| [L2:F13783](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13783) | 7 | Occupations/Middle East phrase/writing terms |  the word "Institute" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13783) |
| [L2:F12068](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12068) | 2 | Occupations/Middle East phrase/writing terms |  words related to starting points, beginnings, or initiations in various contexts. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12068) |
| [L1:F4459](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) | 7 | Research institutes + writers + starting |  mentions of research institutes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) |
| [L1:F15416](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15416) | 28 | Research institutes + writers + starting | the word "writers" or "writer" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15416) |
| [L1:F15323](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) | 1 | Research institutes + writers + starting | the word "starting" in academic papers | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) |
| [L1:F1445](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1445) | 7 | Research institutes + writers + starting | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1445) |
| [L1:F14993](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14993) | 7 | Research institutes + writers + starting |  words related to drainage systems | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14993) |
| [L0:F7124](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) | 2 | Layer-0 word detectors driving the probe | the word "at" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) |
| [L0:F15661](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) | 7 | Layer-0 word detectors driving the probe | the word "spin" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) |
| [L0:F6484](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6484) | 7 | Layer-0 word detectors driving the probe |  the word "sky" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6484) |
| [L0:F2348](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2348) | 4 | Layer-0 word detectors driving the probe |  the word "rapid" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2348) |
| [L0:F13096](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13096) | 3 | Layer-0 word detectors driving the probe |  instances of the word "the", often followed by nouns or other determiners | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13096) |
| [L0:F8690](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8690) | 10 | Layer-0 word detectors driving the probe |  mentions of research studies | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8690) |
| [L0:F10881](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) | 12 | Layer-0 word detectors driving the probe |  the word "coverage" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) |
| [L0:F1229](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1229) | 14 | Layer-0 word detectors driving the probe |  the word "shake," and words related to the middle of something | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1229) |
| [L0:F9297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) | 7 | Layer-0 word detectors driving the probe | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Layer-0 word detectors driving the probe |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F3007](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) | 14 | Layer-0 word detectors driving the probe |  the word "middle", and sometimes the word "character", and "camp" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) |
| [L0:F15880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15880) | 15 | Layer-0 word detectors driving the probe | mentions of the Middle East | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15880) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 40 | Layer-0 word detectors driving the probe | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 38 | Layer-0 word detectors driving the probe | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F4870](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) | 11 | Layer-0 word detectors driving the probe |  commas and sometimes reach (context not clear) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4870) |
| [L0:F7376](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7376) | 28 | Layer-0 word detectors driving the probe |  references to writers or writing | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7376) |
| [L0:F12713](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12713) | 15 | Layer-0 word detectors driving the probe | mentions of "New York City." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12713) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:7124 de=-0.157 |
| 3 | `inspect_feature` ×4 | L0:7124, L0:15661, L0:12768, L14:4420 |
| 4 | `get_top_features` | 30 features; top: L0:7124 de=-0.157 |
| 5 | `inspect_feature` ×10 | L0:6484, L0:3007, L0:10881, L0:1229, L0:2348, L6:12712, L1:4459, L0:13096, L0:8690, L0:15880 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@28` | ✅ reported | 9 | 12 | Trace the path from L14:F4420 (journalism/newspapers feature at pos 28) upstream… |
| SA-2 | `L6:F12712@28` | ✅ reported | 4 | 9 | Trace the path from L6:F12712 (editor/publisher titles feature at pos 28) upstre… |
| SA-3 | `L0:F12768@22` | ❌ error | — | — | Trace the path from L0:F12768 (he/she gender mentions feature at pos 22) upstrea… |
| SA-4 | `L6:F10984@71` | ✅ reported | 4 | 3 | Trace the path from L6:F10984 (at pos 71) upstream through the circuit. This is … |

<details>
<summary><b>SA-1</b> — tool trace (15 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@28, k=10 | Emb:" writer"@28 (de=5.75) +9 more |
| 3 | `inspect_feature` | L8, F8855 | " mentions of news reporters and news reporting" |
| 4 | `get_upstream_features` | L8:F8855@28, k=10 | Emb:" writer"@28 (de=4.72) +9 more |
| 5 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 6 | `inspect_feature` | L7, F72 | " words related to writing professionally" |
| 7 | `get_upstream_features` | L7:F72@28, k=10 | Emb:" writer"@28 (de=5.72) +9 more |
| 8 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 9 | `get_upstream_features` | L4:F13253@28, k=10 | Emb:" writer"@28 (de=9.12) +9 more |
| 10 | `inspect_feature` | L6, F6721 | " html code and related tags particularly href, public, content, title," |
| 11 | `get_upstream_features` | L6:F12712@28, k=10 | Emb:" writer"@28 (de=6.22) +9 more |
| 12 | `inspect_feature` | L0, F7376 | " references to writers or writing" |
| 13 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 14 | `inspect_feature` | L6, F6721 | " html code and related tags particularly href, public, content, title," |
| 15 | `inspect_feature` | L4, F661 | " words and phrases used when referring to reports, documentaries, and " |

**Findings:** The trace from L14:F4420 is driven primarily by the embedding token "writer" at position 28 (direct_effect ≈5.8). This propagates through lower‑layer features that specialise: L0:F7376 → L4:F13253 → L7:F72 → L8:F8855 → L14:F4420, with auxiliary branches (L7:F13646, L6:F12712, L6:F6721, L4:F661) providing complementary news‑coverage cues. The path reaches layer 7 (≤ 8) and includes a concrete embed…

</details>

<details>
<summary><b>SA-2</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F12712 | " titles of editors and publishers in scientific publications" |
| 2 | `get_upstream_features` | L6:F12712@28, k=10 | Emb:" writer"@28 (de=6.22) +9 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `get_upstream_features` | L4:F13253@28, k=10 | Emb:" writer"@28 (de=9.12) +9 more |
| 5 | `inspect_feature` | L2, F9995 | " terms related to occupations and fields of study" |
| 6 | `get_upstream_features` | L2:F9995@28, k=10 | Emb:" freelance"@27 (de=8.06) +9 more |
| 7 | `inspect_feature` | L2, F9210 | "words related to journalism, writing, and articles" |
| 8 | `inspect_feature` | L1, F15416 | "the word "writers" or "writer"" |

**Findings:** The editorial‑title feature L6:F12712 is driven primarily by the raw input token "writer" at position 28 (and to a lesser extent "freelance" at 27). These embeddings also feed an upstream media‑related feature (L4:F13253) and an occupational feature (L2:F9995), which in turn connect to a writer‑specific lower‑layer feature (L1:F15416). All traced paths stay within the lower third of the model (lay…

</details>

<details>
<summary><b>SA-4</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F10984 | " mentions of TV and radio broadcasting" |
| 2 | `get_upstream_features` | L6:F10984@71, k=10 | Emb:" broadcasting"@71 (de=13.06) +9 more |
| 3 | `inspect_feature` | L4, F7056 | " references to radio broadcasting" |
| 4 | `inspect_feature` | L4, F13482 | " references to news broadcasts" |
| 5 | `inspect_feature` | L4, F9065 | " the dates of TV or film broadcasts and premieres" |
| 6 | `get_upstream_features` | L4:F7056@71, k=10 | Emb:" broadcasting"@71 (de=12.81) +9 more |
| 7 | `inspect_feature` | L2, F11625 | " a variety of words related to podcasts, video production, and discuss" |
| 8 | `inspect_feature` | L5, F119 | " TV and radio broadcast companies, stations, channels and programs" |
| 9 | `get_upstream_features` | L4:F7056@71, k=10 | Emb:" broadcasting"@71 (de=12.81) +9 more |
| 10 | `get_upstream_features` | L4:F13482@71, k=10 | Emb:" broadcasting"@71 (de=22.62) +9 more |
| 11 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 12 | `get_upstream_features` | L2:F11625@71, k=10 | Emb:" broadcasting"@71 (de=6.84) +9 more |
| 13 | `inspect_feature` | L5, F4319 | " terms related to telecommunications" |
| 14 | `inspect_feature` | L1, F10525 | " words followed by "er". " |

**Findings:** The tracing starts from the late‑position feature L6:F10984 (broadcasting detector). Its strongest positive upstream drivers are L4:F7056 (radio listening) and L4:F13482 (news broadcast references). Both of these, in turn, receive direct positive signal from the raw token embedding " broadcasting" and, for the radio‑listening path, from a low‑layer technical feature L0:F9026. This satisfies the te…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F12768@22, k=10 → Emb:" he"@22 (de=40.25) +9 more |
| 2 | `get_upstream_features` | L0:F3007@14, k=10 → Emb:" Middle"@14 (de=20.75) +9 more |
| 3 | `get_upstream_features` | L0:F10881@12, k=10 → Emb:" covering"@12 (de=16.25) +9 more |
| 4 | `get_upstream_features` | L0:F15880@15, k=10 → Emb:" Middle"@14 (de=17.12) +9 more |
| 5 | `get_upstream_features` | L0:F7124@2, k=10 → Emb:" at"@2 (de=31.38) +9 more |
| 6 | `get_upstream_features` | L0:F15661@7, k=10 → Emb:" Institute"@7 (de=19.38) +9 more |
| 7 | `get_upstream_features` | L0:F6484@7, k=10 → Emb:" Institute"@7 (de=15.12) +9 more |
| 8 | `get_upstream_features` | L0:F2348@4, k=10 → Emb:" Royal"@4 (de=14.44) +9 more |
| 9 | `get_upstream_features` | L0:F1229@14, k=10 → Emb:" Middle"@14 (de=19.88) +9 more |
| 10 | `inspect_feature` ×12 | L0:7376, L8:8855, L4:13253, L2:9995, L2:9210, L1:15416, L7:72, L7:13646, L4:661, L6:6721, L6:10984, L6:5849 |
| 11 | `get_upstream_features` | L0:F13096@3, k=10 → Emb:" the"@3 (de=28.00) +9 more |
| 12 | `get_upstream_features` | L0:F8690@10, k=10 → Emb:" Studies"@10 (de=11.88) +9 more |
| 13 | `get_upstream_features` | L0:F4870@11, k=10 → Emb:","@11 (de=30.00) +9 more |
| 14 | `get_upstream_features` | L3:F10489@7, k=10 → Emb:" Institute"@7 (de=27.12) +9 more |
| 15 | `get_upstream_features` | L2:F12901@15, k=10 → Emb:" East"@15 (de=26.75) +9 more |
| 16 | `get_upstream_features` | L4:F5060@7, k=10 → Emb:" Institute"@7 (de=16.12) +9 more |
| 17 | `get_upstream_features` | L0:F9297@7, k=10 → Emb:" Institute"@7 (de=11.81) +9 more |
| 18 | `get_upstream_features` | L1:F15323@1, k=10 → Emb:"Starting"@1 (de=16.38) +9 more |
| 19 | `get_upstream_features` | L1:F4459@7, k=10 → Emb:" Institute"@7 (de=27.50) +9 more |
| 20 | `get_upstream_features` | L3:F10489@7, k=5 → Emb:" Institute"@7 (de=27.12) +4 more |
| 21 | `inspect_feature` ×3 | L3:10489, L2:12901, L4:5060 |
| 22 | `get_upstream_features` | L0:F14824@40, k=8 → Emb:" has"@40 (de=35.25) +7 more |
| 23 | `get_upstream_features` | L0:F6051@38, k=8 → Emb:"."@38 (de=47.50) +7 more |
| 24 | `get_upstream_features` | L1:F1445@7, k=5 → Emb:" Institute"@7 (de=5.25) +4 more |
| 25 | `get_upstream_features` | L2:F13783@7, k=5 → Emb:" Institute"@7 (de=27.12) +4 more |
| 26 | `get_upstream_features` | L1:F14993@7, k=5 → Emb:" Institute"@7 (de=17.00) +4 more |
| 27 | `inspect_feature` ×11 | L2:13783, L1:14993, L0:14824, L0:6051, L1:15323, L0:4308, L2:12068, L0:2127, L0:4870, L0:12713, L0:15865 |
| 28 | `get_upstream_features` | L0:F3007@14, k=5 → Emb:" Middle"@14 (de=20.75) +4 more |
| 29 | `get_upstream_features` | L0:F12768@22, k=5 → Emb:" he"@22 (de=40.25) +4 more |
| 30 | `get_upstream_features` | L0:F10881@12, k=5 → Emb:" covering"@12 (de=16.25) +4 more |
| 31 | `get_upstream_features` | L0:F15880@15, k=5 → Emb:" Middle"@14 (de=17.12) +4 more |
| 32 | `get_upstream_features` | L0:F9297@7, k=5 → Emb:" Institute"@7 (de=11.81) +4 more |
| 33 | `get_top_features` | token="", k=15 → 15 features; top: L0:7124 de=-0.157 |

### Build

`build_circuit` → 22 nodes, 35 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 132,472 | 12,762 | 672,745 | 0 | $0.0954 | — | — |
| SA-2 | openai/gpt-oss-120b | 76,002 | 5,528 | 2,528 | 0 | $0.0148 | ✅ 4F/9E | Trace the path from L6:F12712 (editor/publisher titles featu… |
| SA-4 | openai/gpt-oss-120b | 193,008 | 9,972 | 37,920 | 0 | $0.0355 | ✅ 4F/3E | Trace the path from L6:F10984 (at pos 71) upstream through t… |
| SA-1 | openai/gpt-oss-120b | 247,139 | 15,122 | 18,304 | 0 | $0.0464 | ✅ 9F/12E | Trace the path from L14:F4420 (journalism/newspapers feature… |
| **Total** | | **648,621** | **43,384** | **731,497** | **0** | **$0.1921** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 10m 43s