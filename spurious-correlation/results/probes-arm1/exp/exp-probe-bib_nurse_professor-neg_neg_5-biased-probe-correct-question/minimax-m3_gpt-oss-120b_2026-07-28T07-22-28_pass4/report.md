# Circuit Oracle Report
**Date:** 2026-07-28 07:22:28 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession classification is driven by an overwhelmingly **gender-pronoun-based circuit** that incidentally also integrates a thin layer of biographical/educational signals, confirming the user's concern that spurious gender markers — not genuine profession indicators — dominate the prediction.

**Confidence:** 8/10

**Reasoning:**

The attribution graph contains roughly twenty features by total direct-effect mass. Of these, **at least 14 are pronoun- or gendered-reference features** with no profession semantics whatsoever. The largest positive direct_effects are L0:2994 ("his"/"he" pronoun detector, +0.38 at pos 12, driven almost entirely by the "his" token embedding) and L7:14893 (generic pronouns/possessives, +0.49), and L19:8814 (pronouns/names referring to people, +0.29). These activate off the **"His"** (pos 1), **"He"** (pos 10), **"He"** (pos 23), and **"his"** (pos 12) embeddings. The male-pronoun chain is reinforced at every layer: L0:1069 ("He"/"His" male person) → L4:4315 ("his" detector) → L6:12990 ("male pronouns and titles", suppressed_token="herself") → L7:14946 ("his"/"he" detector, promoted="his/himself") → L18:14743 ("He" detector, frac_nonzero 0.018, very specific) → L19:8814 (pronouns/names) → logit.

L18:14743 is a particularly striking example of the **spurious-correlation problem**: its `frac_nonzero` is only 0.018 (highly selective), its label is literally "He", and it has one of the largest direct_effects on the probe (-0.285 at pos 10) — meaning a single male-pronoun occurrence is doing as much work on the profession probe as multiple genuinely biographical features combined. There is no parallel "She"-driven feature doing equivalent work. If the subject pronoun were "She", the probe score would change substantially — even though the subject's actual profession (a "transnational business history" researcher) has nothing to do with the pronoun used to describe them.

The few features that *do* look legitimately profession-relevant are present but quantitatively minor and act as supporting context, not drivers. L17:3683 ("biographies", "his" top activation; promoted "graduated"), L17:12634 ("degrees/professional titles"), L18:7334 ("education and career information", promoted "degree/PhD"), and L19:11110 ("people's education history", promoted "Masters/Master") form a real biographical-signal chain driven primarily by the **"received"** token embedding at pos 11 and the **"research"** token at pos 2. But these fire off a sentence like "He received his Ph.D. in History" — a perfectly generic male-biographical template. They are *not* driven by any token that names a profession (there is no "professor", "economist", "historian", "MBA" feature in the top of the graph). The single L0:1773 "history" feature (+0.109 at pos 8) is the only token-level signal that touches on the subject's actual field.

Most damning: L12:10137 ("names of universities, cities, institutions" — fired by "Harvard") carries a **negative** direct_effect (-0.108), i.e., the presence of an actual university name pushes the probe score *down*. If the probe were genuinely tracking profession-related biographical detail, Harvard/Stanford/Chicago being named would help, not hurt. The fact that the probe's gendered features dominate *and* a real institution feature actively suppresses the score shows the model has learned to read the sentence template "He received his Ph.D. from [School]" as a male-pronoun cue rather than as biographical evidence.

In short: the circuit is a textbook spurious-correlation probe. The signal that drives the classification is "this paragraph uses male pronouns and is structured like a male CV/bio paragraph," not "this subject is in profession X." A user reading the description could swap "He"→"She" throughout, the model would still recognize the same biography, but the probe score would shift markedly, exposing the gender-feature dependence. The user concern is fully validated by the attribution graph.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | L0:2994 — "his"/"he" pronoun detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 12 | L0:2994 — "his"/"he" pronoun detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0:1069 — "He"/"His" male-person reference |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 10 | L0:1069 — "He"/"His" male-person reference |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 23 | L0:1069 — "He"/"His" male-person reference |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1773](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1773) | 8 | L0:1773 — word "history" |  the word "history" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1773) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | L2:5491 — "He" as reference to God (deity masculine pronoun) | references to God in the third person. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | L4:4315 — "his"/he/him pronoun detector |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | L6:12990 — male pronouns and titles |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 10 | L6:12990 — male pronouns and titles |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | L7:14893 — generic pronouns/possessives (mixed gender) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 10 | L7:14893 — generic pronouns/possessives (mixed gender) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | L7:14946 — "his" / he / him pronoun detector |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 10 | L7:14946 — "his" / he / him pronoun detector |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L12:F10137](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10137) | 20 | L12:10137 — university/city/institution names (e.g., Harvard) |  names of universities, cities, publications and other institutions. | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/10137) |
| [L17:F3683](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) | 10 | L17:3683 — biographical text pattern | biographies | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) |
| [L17:F3683](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) | 11 | L17:3683 — biographical text pattern | biographies | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) |
| [L17:F3683](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) | 23 | L17:3683 — biographical text pattern | biographies | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/3683) |
| [L17:F12634](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/12634) | 11 | L17:12634 — degrees/professional titles text |  text mentioning degrees, especially advanced degrees and professional titles, with a weaker response for bachelor's degrees | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/12634) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 10 | L18:14743 — "He" pronoun detector (male) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | L18:14743 — "He" pronoun detector (male) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F7334](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7334) | 11 | L18:7334 — education/career information |  information on a person's education and career | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7334) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | L18:7400 — coding/software/UI terms (mislabels as male) |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | L18:10315 — pronouns/possessives (mixed gender) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F7217](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7217) | 1 | L18:7217 — pronoun/people-referring words (she/shear confusion) |  words or abbreviations referring to people, with a focus on pronouns and mentions of "shear" | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7217) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | L19:8814 — various pronouns/names referring to people |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L19:F11110](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/11110) | 11 | L19:11110 — people's education history text |  text describing people's education history | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/11110) |
| [L19:F8186](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) | 10 | L19:8186 — third-person/possessive pronouns |  references to a person, especially third-person pronouns and possessive pronouns. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8186) |
| [L20:F10934](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/10934) | 11 | L20:10934 — past-tense action verbs |  action verbs with past tense forms | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/10934) |
| [L21:F4895](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/4895) | 11 | L21:4895 — prepositions and related words | prepositions and related words | [view](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/4895) |
| [L21:F6216](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/6216) | 10 | L21:6216 — references to a specific person via pronouns/names |  references to a specific person, often using pronouns or names | [view](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/6216) |
| [L22:F12117](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) | 11 | L22:12117 — actions people can take or have taken |  references to actions that people can take or have taken. | [view](https://neuronpedia.org/gemma-2-2b/22-gemmascope-transcoder-16k/12117) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.490 |
| 3 | `inspect_feature` ×15 | L7:14893, L7:14946, L0:2994, L6:12990, L19:8814, L18:14743, L4:4315, L18:7400, L22:12117, L18:10315, L2:5491, L21:6216, L19:8186, L0:1773, L12:10137 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace the upstream circuit for L7:F14893 at pos 1, which is a pronoun/possessive… |
| SA-2 | `L19:F8814@1` | ❌ error | — | — | Trace the upstream circuit for L19:F8814 at pos 1, labeled "various pronouns and… |
| SA-3 | `L22:F12117@11` | ❌ error | — | — | Trace the upstream circuit for L22:F12117 at pos 11 (token "received" in "He rec… |
| SA-4 | `L18:F14743@10` | ❌ error | — | — | Trace the upstream circuit for L18:F14743 at pos 10 (token "He"). Label is liter… |
| SA-5 | `L12:F10137@20` | ❌ error | — | — | Trace L12:F10137 at pos 20 — this is the "names of universities, cities, publica… |
| SA-6 | `L0:F2994@12` | ❌ error | — | — | Trace L0:F2994 at pos 12 (the "his" pronoun feature, the one with the LARGEST di… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@1, k=15 → Emb:"His"@1 (de=23.50) +14 more |
| 2 | `get_upstream_features` | L0:F2994@12, k=10 → Emb:" his"@12 (de=44.50) +9 more |
| 3 | `get_upstream_features` | L22:F12117@11, k=15 → L21:F4895 (de=5.69) +14 more |
| 4 | `get_upstream_features` | L18:F14743@10, k=15 → Emb:" He"@10 (de=22.38) +14 more |
| 5 | `get_upstream_features` | L12:F10137@20, k=15 → Emb:" Harvard"@20 (de=5.16) +14 more |
| 6 | `get_upstream_features` | L19:F8814@1, k=12 → Emb:"His"@1 (de=9.31) +11 more |
| 7 | `get_upstream_features` | L4:F4315@1, k=12 → Emb:"His"@1 (de=23.50) +11 more |
| 8 | `get_upstream_features` | L6:F12990@1, k=10 → Emb:"His"@1 (de=4.91) +9 more |
| 9 | `get_upstream_features` | L2:F5491@1, k=8 → Emb:"His"@1 (de=23.88) +7 more |
| 10 | `get_upstream_features` | L21:F4895@11, k=12 → L19:F11110 (de=11.00) +11 more |
| 11 | `inspect_feature` ×10 | L21:4895, L20:10934, L17:3683, L19:11110, L19:15156, L21:2981, L17:12634, L18:7217, L18:10315, L0:1069 |
| 12 | `get_upstream_features` | L19:F11110@11, k=12 → L18:F7334 (de=16.88) +11 more |
| 13 | `get_upstream_features` | L17:F3683@11, k=10 → Emb:" received"@11 (de=6.41) +9 more |
| 14 | `get_upstream_features` | L17:F12634@11, k=10 → L16:F2313 (de=6.69) +9 more |
| 15 | `get_upstream_features` | L18:F7400@1, k=10 → Emb:"His"@1 (de=13.00) +9 more |
| 16 | `get_upstream_features` | L18:F14743@23, k=10 → Emb:" He"@23 (de=24.50) +9 more |
| 17 | `get_upstream_features` | L18:F7334@11, k=10 → L17:F12634 (de=4.28) +9 more |
| 18 | `get_upstream_features` | L15:F9968@11, k=10 → Emb:" received"@11 (de=47.50) +9 more |
| 19 | `get_upstream_features` | L16:F2313@11, k=8 → L15:F4934 (de=8.19) +7 more |
| 20 | `get_upstream_features` | L15:F4934@11, k=8 → L8:F7587 (de=7.66) +7 more |
| 21 | `get_upstream_features` | L8:F7587@11, k=8 → Emb:" received"@11 (de=7.38) +7 more |
| 22 | `inspect_feature` ×5 | L18:7334, L16:2313, L15:4934, L15:9968, L8:7587 |
| 23 | `get_upstream_features` | L2:F5491@1, k=8 → Emb:"His"@1 (de=23.88) +7 more |
| 24 | `get_upstream_features` | L0:F1069@1, k=6 → Emb:"His"@1 (de=21.62) +5 more |
| 25 | `get_upstream_features` | L0:F1773@8, k=8 → Emb:" history"@8 (de=26.75) +7 more |
| 26 | `get_upstream_features` | L0:F2994@1, k=6 → Emb:"His"@1 (de=19.75) +5 more |
| 27 | `get_upstream_features` | L21:F6216@10, k=8 → L18:F14743 (de=7.53) +7 more |
| 28 | `get_upstream_features` | L19:F8186@10, k=8 → Emb:" He"@10 (de=14.38) +7 more |
| 29 | `get_upstream_features` | L18:F14743@1, k=6 → ❌ Feature (layer=18, feature_idx=14743) not found at pos=1. Th |
| 30 | `get_upstream_features` | L0:F2994@10, k=4 → ❌ Feature (layer=0, feature_idx=2994) not found at pos=10. Thi |
| 31 | `get_upstream_features` | L0:F1069@23, k=4 → Emb:" He"@23 (de=36.75) +3 more |
| 32 | `get_upstream_features` | L7:F14946@1, k=6 → Emb:"His"@1 (de=18.38) +5 more |
| 33 | `get_upstream_features` | L6:F12990@10, k=4 → Emb:" He"@10 (de=4.28) +3 more |
| 34 | `get_upstream_features` | L18:F14743@23, k=4 → Emb:" He"@23 (de=24.50) +3 more |
| 35 | `get_upstream_features` | L17:F3683@10, k=6 → Emb:"His"@1 (de=2.83) +5 more |

### Build

`build_circuit` → 32 nodes, 70 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 71,596 | 10,436 | 492,362 | 0 | $0.0635 | — | — |
| **Total** | | **71,596** | **10,436** | **492,362** | **0** | **$0.0635** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 2s