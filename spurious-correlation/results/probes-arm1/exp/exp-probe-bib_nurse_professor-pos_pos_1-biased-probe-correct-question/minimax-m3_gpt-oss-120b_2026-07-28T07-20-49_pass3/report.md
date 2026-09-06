# Circuit Oracle Report
**Date:** 2026-07-28 07:20:49 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession classification score is driven primarily by a stack of female-gender/female-pronoun detector features (the pronoun "she" at pos 7, plus a downstream "her" at pos 38), with only a secondary, much smaller contribution from genuine nursing-vocabulary features; the user's concern is confirmed.

**Confidence:** 8

**Reasoning:** The attribution graph shows the top feature by direct effect is **L6:F11646** ("references to women, potentially triggered by pronouns and titles", direct_effect=1.55, frac_nonzero=0.02) followed by **L18:F14677** ("instances of women or girls being mentioned", direct_effect=0.91) and **L12:F12940** ("references to female pronouns and possessive pronouns", direct_effect=0.69). All three of these autointerp labels and their top-activating examples are about female gender references (she/her/herself), not about nursing or healthcare. Tracing upstream from L18:F14677 confirms the signal originates at the **token embedding for " she" (pos 7)**, which feeds directly into L6:F11646 (direct_effect=31.6 from embedding), then into L12:F12940, and finally into L18:F14677. The L19:F9685 feature ("references to women's names and their roles or accomplishments") further propagates the same female-gender signal. 

The genuine profession signal is comparatively small: L6:F15267 ("words referring to the profession of nursing", direct_effect=0.55+0.32) and L2:F15728 ("mentions of nurses and nursing", direct_effect=0.33) are present but rank 8th-11th by direct effect and originate from the token " nurses" (pos 15) and "Perio" (pos 13). Meanwhile, two **anti-male / He-features** (L6:F16329, direct_effect=-0.67 and L18:F14743 "He", direct_effect=-0.44) actively *suppress* the profession score — i.e., the model would score this prompt higher for the profession if the subject were male, which is the opposite of a profession indicator. 

The dominant circuit (Supernodes `emb_she` → `early_gender_detectors` → `mid_pronoun` → `she_gender_late` → `output`) is a gender-detection pathway, not a profession-recognition pathway. The probe direction has evidently learned to use the female-gender cue as a shortcut for a profession that is female-dominated in its training distribution (nursing), rather than relying on the explicit profession vocabulary. This validates the user's concern: the circuit is using spurious gender markers rather than genuine profession indicators as the primary driver of the classification.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 7 | Output: probe direction (profession classifier) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 7 | Late-layer female-reference detectors (L18-L19) — promote profession score |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 7 | Late-layer female-reference detectors (L18-L19) — promote profession score |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 7 | Mid-layer female-pronoun aggregators (L10-L12) — promote profession score | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 7 | Mid-layer female-pronoun aggregators (L10-L12) — promote profession score |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 7 | Early female-reference detectors (L0-L6) — fire on "she" |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L1:F4232](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) | 7 | Early female-reference detectors (L0-L6) — fire on "she" |  the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 7 | Early female-reference detectors (L0-L6) — fire on "she" |  the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 7 | Early female-reference detectors (L0-L6) — fire on "she" | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 7 | Anti-male / 'He' features — suppress profession score (negative direct_effect) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 7 | Anti-male / 'He' features — suppress profession score (negative direct_effect) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Nursing-specific signal (L2-L6) — actual profession word 'nurses' |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | Nursing-specific signal (L2-L6) — actual profession word 'nurses' |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L2:F15728](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15728) | 15 | Nursing-specific signal (L2-L6) — actual profession word 'nurses' |  mentions of nurses and nursing | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15728) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=1.555 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@7` | ❌ error | — | — | Trace this L6 feature upstream. Determine what it encodes and whether it relates… |
| SA-2 | `L18:F14677@7` | ✅ reported | 5 | 7 | Trace this L18 feature upstream. Determine what it encodes. Report all features … |
| SA-3 | `L12:F12940@7` | ❌ error | — | — | Trace this L12 feature upstream. Determine what it encodes. Report all features … |
| SA-4 | `L4:F7864@7` | ❌ error | — | — | Trace this L4 feature upstream. Determine what it encodes. Report all features a… |
| SA-5 | `L19:F9685@7` | ❌ error | — | — | Trace this L19 feature upstream. Determine what it encodes. Report all features … |

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@7, k=10 | Emb:" she"@7 (de=28.38) +9 more |
| 3 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 4 | `get_upstream_features` | L6:F11646@7, k=10 | Emb:" she"@7 (de=31.62) +9 more |
| 5 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 6 | `get_upstream_features` | L6:F11646@7, k=10 | Emb:" she"@7 (de=31.62) +9 more |
| 7 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 8 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 9 | `get_upstream_features` | L12:F12940@7, k=10 | Emb:" she"@7 (de=12.31) +9 more |
| 10 | `get_upstream_features` | L4:F7864@7, k=10 | Emb:" she"@7 (de=27.25) +9 more |

**Findings:** The target L18:F14677 fires strongly when the prompt contains the pronoun 'she' at position 7, indicating it encodes a detection of female mentions. Upstream, the signal originates directly from the input embedding of the token ' she' (large positive direct effect). Intermediate layers further process this pronoun signal: a low‑layer gender‑specific detector (L6:F11646) and a mid‑layer pronoun agg…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×13 | L6:11646, L18:14677, L12:12940, L19:9685, L4:7864, L0:12519, L6:16329, L6:15267, L18:14743, L1:4232, L2:15728, L10:14965, L7:8644 |
| 2 | `get_upstream_features` | L18:F14677@7, k=8 → Emb:" she"@7 (de=28.38) +7 more |
| 3 | `get_upstream_features` | L6:F11646@7, k=8 → Emb:" she"@7 (de=31.62) +7 more |
| 4 | `get_upstream_features` | L19:F9685@7, k=8 → Emb:" she"@7 (de=12.25) +7 more |
| 5 | `get_upstream_features` | L12:F12940@7, k=8 → Emb:" she"@7 (de=12.31) +7 more |
| 6 | `get_upstream_features` | L6:F15267@15, k=8 → Emb:" nurses"@15 (de=16.12) +7 more |
| 7 | `get_upstream_features` | L6:F15267@14, k=8 → Emb:"perative"@14 (de=7.72) +7 more |
| 8 | `get_upstream_features` | L18:F14677@38, k=8 → Emb:" her"@38 (de=22.00) +7 more |
| 9 | `get_upstream_features` | L2:F15728@15, k=8 → Emb:" nurses"@15 (de=22.62) +7 more |
| 10 | `get_upstream_features` | L10:F14965@7, k=8 → Emb:" she"@7 (de=11.88) +7 more |

### Build

`build_circuit` → 8 nodes, 6 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 27,895 | 3,461 | 103,876 | 0 | $0.0188 | — | — |
| SA-2 | openai/gpt-oss-120b | 108,668 | 6,589 | 5,088 | 0 | $0.0203 | ✅ 5F/7E | Trace this L18 feature upstream. Determine what it encodes. … |
| **Total** | | **136,563** | **10,050** | **108,964** | **0** | **$0.0391** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 31s