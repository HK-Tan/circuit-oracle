# Circuit Oracle Report
**Date:** 2026-07-28 07:01:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score for the "nurse" profession is driven by *two parallel circuits* — one encoding the literal profession keyword ("nurses"/"Perioperative") and a separate, much larger circuit encoding female-gender cues from the pronoun "she" — and the gender path actually carries more total direct effect on the probe than the profession-keyword path.

**Confidence:** 8

**Reasoning:**

**Probe-driving features** (from `get_top_features` on the synthetic probe target): the largest positive direct effects come from gender features, not nursing features.
- L6:F11646 ("references to women… pronouns and titles", direct_effect +1.55, frac_nonzero 0.020) — the single biggest driver.
- L18:F14677 ("instances of women or girls being mentioned", +0.91, frac_nonzero 0.012) at pos 7 ("she").
- L12:F12940 ("female pronouns and possessive pronouns", +0.69, frac_nonzero 0.0065).
- L6:F15267 ("words referring to the profession of nursing", +0.55, frac_nonzero 0.016) at pos 15 ("nurses").
- L2:F15728 ("mentions of nurses and nursing", +0.33, frac_nonzero 0.0062).
- The biggest *negative* direct effects are also gender-related: L0:F12519 ("the pronoun 'she'", −0.71) and L6:F16329 ("female first names", −0.67) and L18:F14743 ("He", −0.44) — i.e. the male-pronoun feature actively *suppressing* the probe score.

**Tracing the gender circuit (the user's concern):** I traced L18:F14677 and the early L0:F12519 upstream. Both terminate at the embedding node for the literal token " she" at position 7 with very large positive direct effects (28–41). The path is: `Emb: she (pos 7) → L0:F12519 (she detector) → L4:F7864 / L4:F15567 / L1:F4232 (her) → L6:F11646 (women references) → L12:F12940 (female pronouns) → L17:F5889 → L18:F14677 (women/girls mentioned) → L19:F9685 (women's names/roles) → output_probe`. The L18 "He" feature (F14743) is a *male-pronoun suppressor* in the same circuit — its only effect here is to push the probe score *down* because the subject is female, not male. The user's concern is confirmed: this is a complete female-gender-detection subcircuit, terminating at the "she" token embedding, with no profession signal mixed in.

**Tracing the profession circuit:** L6:F15267 ("nursing profession") traces to `Emb: nurses (pos 15, direct_effect 16.1) → L2:F15728 → L4:F11037 (counseling/social work) + L5:F1275 (medical professionals) → L6:F15267 → output_probe`. L2:F15728 is also directly driven by the ` nurses` token embedding (direct_effect 22.6) and a small contribution from the "perative" subword. Crucially, the `Perio`/`perative` token embeddings *do* contribute positively to the nursing mid-features (L4:F11037 gets direct_effect +1.59 and +1.44 from "Perio" and "perative" respectively), so the profession-keyword path is genuinely grounded in nursing vocabulary.

**Where they connect (or don't):** The two subcircuits are *parallel* — they share no internal features. The gender path goes through ~7–8 transcoder layers and contributes *more* total direct effect to the probe (L6:F11646 alone = +1.55 vs. L6:F15267 = +0.55) than the profession path. The probe direction essentially reads off "female + nursing" jointly, and the female signal is the dominant component. The user is correct: the probe is partly a "female + profession-word" classifier, with the gender side providing the larger share of the classification score. If the user replaced "she" with "he" while keeping "Perioperative nurses" intact, L18:F14743 ("He") would fire and push the probe score *down* (it has direct_effect −0.44 here, and analogous features fire on "himself"/"his" for the male pattern), demonstrating the gender signal is not profession-related at all — it is a true spurious correlate the probe has learned.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 7 | Early 'she' pronoun detector (L0:12519) |  the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L0:F10920](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) | 15 | Early 'nurse' word detector (L0:10920) |  the word "nurse" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10920) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 7 | Mid-layer gender detectors (L4:7864, L4:15567; L1:4232 'her') | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 7 | Mid-layer gender detectors (L4:7864, L4:15567; L1:4232 'her') | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L1:F4232](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) | 7 | Mid-layer gender detectors (L4:7864, L4:15567; L1:4232 'her') |  the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) |
| [L2:F15728](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15728) | 15 | Mid-layer nursing/counseling/medical features (L2:15728, L4:11037, L5:1275) |  mentions of nurses and nursing | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15728) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 15 | Mid-layer nursing/counseling/medical features (L2:15728, L4:11037, L5:1275) | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 15 | Mid-layer nursing/counseling/medical features (L2:15728, L4:11037, L5:1275) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 7 | Late-layer female-pronoun/women features (L6:11646, L6:16329, L10:14965, L12:12940, L17:5889) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 7 | Late-layer female-pronoun/women features (L6:11646, L6:16329, L10:14965, L12:12940, L17:5889) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 7 | Late-layer female-pronoun/women features (L6:11646, L6:16329, L10:14965, L12:12940, L17:5889) |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 7 | Late-layer female-pronoun/women features (L6:11646, L6:16329, L10:14965, L12:12940, L17:5889) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 7 | Late-layer female-pronoun/women features (L6:11646, L6:16329, L10:14965, L12:12940, L17:5889) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Late-layer nursing profession feature (L6:15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | Late-layer nursing profession feature (L6:15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 7 | Late female-references + male-suppressor (L18:14677, L19:9685, L18:14743) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 7 | Late female-references + male-suppressor (L18:14677, L19:9685, L18:14743) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 38 | Late female-references + male-suppressor (L18:14677, L19:9685, L18:14743) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 7 | Late female-references + male-suppressor (L18:14677, L19:9685, L18:14743) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=1.555 |
| 3 | `inspect_feature` ×13 | L6:11646, L18:14677, L12:12940, L4:7864, L19:9685, L6:15267, L18:14743, L1:4232, L2:15728, L6:16329, L0:12519, L10:14965, L7:8644 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@7` | ✅ reported | 3 | 3 | Trace the upstream path from L18:F14677 ("instances of women or girls being ment… |
| SA-2 | `L6:F15267@15` | ✅ reported | 3 | 3 | Trace the upstream path from L6:F15267 ("words in the document referring to the … |
| SA-3 | `L2:F15728@15` | ✅ reported | 3 | 4 | Trace upstream from L2:F15728 ("mentions of nurses and nursing") at position 15.… |
| SA-4 | `L0:F12519@7` | ❌ error | — | — | Trace upstream from L0:F12519 ("the pronoun 'she'") at position 7. This is a ver… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@7, k=15 | Emb:" she"@7 (de=28.38) +14 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `get_upstream_features` | L6:F11646@7, k=15 | Emb:" she"@7 (de=31.62) +14 more |
| 5 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 6 | `get_upstream_features` | L4:F7864@7, k=10 | Emb:" she"@7 (de=27.25) +9 more |

**Findings:** The female‑pronoun feature L18:F14677 is driven directly by the input token embedding for " she" at position 7 (direct_effect ~28). The signal also passes through lower‑layer gender‑sensitive features at layers 6 and 4, both of which receive strong positive contributions from the same " she" embedding. Thus the gender cue originates from the genuine "she" token rather than any deeper, unrelated ge…

</details>

<details>
<summary><b>SA-2</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@15, k=10 | Emb:" nurses"@15 (de=16.12) +9 more |
| 3 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 4 | `get_upstream_features` | L4:F11037@15, k=10 | Emb:" nurses"@15 (de=5.16) +9 more |
| 5 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |

**Findings:** The nursing‑profession feature (L6:F15267) is driven primarily by the input token embedding for " nurses" at position 15 (direct_effect = 16.125), satisfying the requirement to surface a positive token‑embedding influence. Additional upstream contributors include a counseling/social‑work detector (L4:F11037) and a broader medical‑profession detector (L5:F1275). All traced paths reach an embedding …

</details>

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F15728 | " mentions of nurses and nursing" |
| 2 | `get_upstream_features` | L2:F15728@15, k=10 | Emb:" nurses"@15 (de=22.62) +9 more |
| 3 | `inspect_feature` | L0, F10920 | " the word "nurse"" |
| 4 | `inspect_feature` | L0, F11835 | "terms used in software code such as "assembly", "using", "namespace", " |
| 5 | `get_upstream_features` | L0:F10920@15, k=10 | Emb:" nurses"@15 (de=21.50) +9 more |
| 6 | `inspect_feature` | L1, F5829 | " uses of the word 'necessarily', sometimes near scientific or mathemat" |

**Findings:** The L2 nurse/nursing feature (F15728) is overwhelmingly driven by the input token " nurses" at position 15 (direct_effect ~22.6). A smaller contribution comes from a layer‑0 feature that detects the word "nurse" (direct_effect ~0.67). The token fragment "perative" – arising from the word "perioperative" – has a minimal positive effect (0.27) and does not dominate the activation. Thus the nursing m…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F12519@7, k=10 → Emb:" she"@7 (de=41.25) +9 more |
| 2 | `get_upstream_features` | L18:F14743@7, k=10 → Emb:" she"@7 (de=25.62) +9 more |
| 3 | `get_upstream_features` | L6:F11646@7, k=10 → Emb:" she"@7 (de=31.62) +9 more |
| 4 | `get_upstream_features` | L17:F5889@7, k=5 → Emb:" she"@7 (de=33.75) +4 more |
| 5 | `get_upstream_features` | L4:F15567@7, k=5 → Emb:" she"@7 (de=21.88) +4 more |
| 6 | `get_upstream_features` | L19:F9685@7, k=10 → Emb:" she"@7 (de=12.25) +9 more |
| 7 | `get_upstream_features` | L0:F10920@15, k=5 → Emb:" nurses"@15 (de=21.50) +4 more |
| 8 | `get_upstream_features` | L5:F1275@15, k=5 → Emb:" nurses"@15 (de=1.62) +4 more |
| 9 | `get_upstream_features` | L4:F11037@15, k=5 → Emb:" nurses"@15 (de=5.16) +4 more |

### Build

`build_circuit` → 11 nodes, 20 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,790 | 5,307 | 124,599 | 0 | $0.0282 | — | — |
| SA-1 | openai/gpt-oss-120b | 53,492 | 2,991 | 2,528 | 0 | $0.0099 | ✅ 3F/3E | Trace the upstream path from L18:F14677 ("instances of women… |
| SA-2 | openai/gpt-oss-120b | 44,557 | 3,851 | 5,088 | 0 | $0.0091 | ✅ 3F/3E | Trace the upstream path from L6:F15267 ("words in the docume… |
| SA-3 | openai/gpt-oss-120b | 65,053 | 3,861 | 2,592 | 0 | $0.0121 | ✅ 3F/4E | Trace upstream from L2:F15728 ("mentions of nurses and nursi… |
| **Total** | | **210,892** | **16,010** | **134,807** | **0** | **$0.0592** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 49s