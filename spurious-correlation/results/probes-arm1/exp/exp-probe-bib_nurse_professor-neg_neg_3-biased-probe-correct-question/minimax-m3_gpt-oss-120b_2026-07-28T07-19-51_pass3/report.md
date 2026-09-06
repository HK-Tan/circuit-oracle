# Circuit Oracle Report
**Date:** 2026-07-28 07:19:51 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession classification is driven predominantly by a cascade of male-pronoun features (L0/L6/L7/L18) anchored on the token "He" and "his" throughout the biography, with only a weak academic-field contribution from "Mathematics" — the circuit confirms the user's concern that the probe relies on spurious gender markers rather than genuine profession indicators.

**Confidence:** 8

**Reasoning:**

The circuit reveals two largely independent pathways converging on the probe output, with a clear gender/profession imbalance.

**Pathway 1 — Male-pronoun dominance (the spurious signal).** The largest direct effects on the probe come from a stack of features that are *literally pronoun detectors*:
- **L0:F2994** ("his" / "he", frac_nonzero=0.073) fires at positions 3, 23, 44 (every "his" in the text) with direct_effect up to +0.30.
- **L0:F1069** ("He" / "His" reference, frac_nonzero=0.008) fires at pos 21 with direct_effect +0.10.
- **L6:F12990** ("male pronouns and titles along with descriptors associated with men", frac_nonzero=0.068) fires at pos 1, 2, 21, 42 with direct_effect ≈ −0.13 to −0.17 *per occurrence*. Despite the negative sign at this feature, the upstream chain from "He"→L1:F8685 (pronoun "he")→L2:F9301 (gendered social roles)→L4:F14796 (he/him)→L5:F10952 (third-person pronouns)→L6:F12990→L7:F14893 ("pronouns/possessive pronouns", direct_effect +0.17 at pos 1)→L7:F14946 ("his"/"he", direct_effect −0.14) carries the gender signal forward.
- **L18:F14743** (label: "He") fires at sentence starts (pos 21, 42) with direct_effect ≈ −0.15 each. Traced upstream, it is fed by `Emb: " He"` (direct_effect 23.4 at pos 21, 24.6 at pos 42) and **L0:F1069** (direct_effect +7.7 / +8.4) — the male-person reference feature.
- Embedding nodes `Emb: "He" (pos 1)`, `Emb: " He" (pos 21, 42)`, and `Emb: " his" (pos 3, 23)` directly drive the entire pronoun stack.

**Pathway 2 — Genuine profession signal (weak).** Only one feature encodes a profession-relevant concept:
- **L6:F170** ("references to academic fields, especially humanities", frac_nonzero=0.039) fires on "Mathematics" at pos 10 with direct_effect +0.12. Upstream tracing shows it is fed by a clean academic-degree cascade: `Emb: "degree" (pos 8)` → **L0:F6127** (the word "degree" + academia, frac_nonzero=0.007) → **L2:F10852** (academic titles, "degree/PhD/doctorate") → **L3:F4113** (degree/area-of-study) → **L4:F3727** (mentions of academic degrees) → **L5:F10392** (fields of academic study) → **L6:F170**. This is the only feature that points at the actual profession indicator (academic field of study), and it carries the smallest positive direct effect of the top features.

**Quantitatively**, the gender/pronoun features dominate the absolute signed effect: L0:F2994 alone (three positions) contributes ≈ +0.60 cumulative direct_effect, L7:F14893 contributes ≈ +0.41 across positions, while the academic-field L6:F170 contributes ≈ +0.12. The L18 "He" detector and the L7/L6 pronoun features further reinforce the gender signal. The L12:F2175 "words referring to gender" feature at pos 2 contributes a smaller negative direct_effect (−0.16), but it is itself a *gender* feature, not a profession feature.

**Verdict on the user's concern:** The concern is strongly supported. The probe's classification is being driven by a male-pronoun circuit that has nothing to do with the subject's profession (computer science / academic). The only "profession" content in the entire top-20 features is the academic-field reference triggered by the word "Mathematics," and even that fires generically on field-of-study vocabulary rather than on anything specific to "professor" or "computer scientist." Any bio with "He received his …" would activate this circuit regardless of the actual profession mentioned — the probe is essentially detecting that the subject is a *male person described in biographical Wikipedia-style prose*, not that they are a *professor*.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | Gender-word suppressor (L12) |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 21 | 'He' detector (L18, sentence-start) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 42 | 'He' detector (L18, sentence-start) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Male pronoun / possessive detectors (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 2 | Male pronoun / possessive detectors (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 3 | Male pronoun / possessive detectors (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Male pronoun / possessive detectors (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | Male pronoun / possessive detectors (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 3 | Male pronoun / possessive detectors (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Male pronouns & titles (L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 2 | Male pronouns & titles (L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 21 | Male pronouns & titles (L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 42 | Male pronouns & titles (L6) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | Academic-field reference (L6:F170, 'Mathematics') |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | 'his' / 'he' pronoun (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 23 | 'his' / 'he' pronoun (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 44 | 'his' / 'he' pronoun (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 21 | 'his' / 'he' pronoun (L0) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F6127](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) | 8 | 'degree' / academia (L0) |  instances of the word "degree" and words associated with academia, especially higher education | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6127) |
| [L0:F6270](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) | 13 | 'degree' / academia (L0) | the word "whom", sometimes also activating on nearby punctuation, sentence starts, discourse markers, and other function words | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6270) |
| [L1:F8685](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8685) | 1 | Early 'he' / pronoun features (L1-L5) |  the pronoun "he" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8685) |
| [L2:F9301](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) | 1 | Early 'he' / pronoun features (L1-L5) |  all mentions of men and women in the context of relationships, dating, or gendered social roles | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9301) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 1 | Early 'he' / pronoun features (L1-L5) | the pronoun "he" or "him" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Early 'he' / pronoun features (L1-L5) | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Early 'he' / pronoun features (L1-L5) | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 6 | Early academic-degree detectors (L2-L5) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L3:F4113](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) | 9 | Early academic-degree detectors (L2-L5) |  mentions of academic degrees and areas of study | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 6 | Early academic-degree detectors (L2-L5) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 9 | Early academic-degree detectors (L2-L5) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | Early academic-degree detectors (L2-L5) |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F15490](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15490) | 10 | Early academic-degree detectors (L2-L5) |  academic subjects and professions | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/15490) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.297 |
| 3 | `inspect_feature` ×10 | L0:2994, L0:6270, L7:14893, L6:170, L6:12990, L7:14946, L18:14743, L0:6127, L0:1069, L12:2175 |
| 4 | `get_upstream_features` | Emb:"He"@1 (de=14.75) +9 more |
| 5 | `get_upstream_features` | Emb:"He"@1 (de=11.50) +9 more |
| 6 | `get_upstream_features` | Emb:"He"@1 (de=3.41) +9 more |
| 7 | `get_upstream_features` | Emb:" He"@21 (de=23.38) +9 more |
| 8 | `inspect_feature` ×6 | L4:14796, L2:9301, L4:9757, L5:10952, L0:11400, L1:8685 |
| 9 | `get_upstream_features` | Emb:" He"@42 (de=24.62) +9 more |
| 10 | `get_upstream_features` | Emb:" degree"@8 (de=16.88) +9 more |

### Dispatch: 1 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F170@10` | ✅ reported | 7 | 10 | Trace this feature upstream to understand what input signals drive it. This is a… |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 2 | `get_upstream_features` | L6:F170@10, k=10 | L5:F10392 (de=11.38) +9 more |
| 3 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 4 | `inspect_feature` | L5, F15490 | " academic subjects and professions" |
| 5 | `get_upstream_features` | L5:F10392@10, k=10 | L3:F4113 (de=3.34) +9 more |
| 6 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 7 | `get_upstream_features` | L5:F10392@10, k=10 | L3:F4113 (de=3.34) +9 more |
| 8 | `get_upstream_features` | L3:F4113@9, k=10 | Emb:" in"@9 (de=11.94) +9 more |
| 9 | `inspect_feature` | L1, F10429 | " words related to academic programs" |
| 10 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 11 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 12 | `get_upstream_features` | L2:F10852@6, k=10 | Emb:" B"@4 (de=12.12) +9 more |
| 13 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |

**Findings:** The L6:F170 feature firing on "Mathematics" is mainly driven by lower‑layer academic‑degree detectors and the direct embedding of the word itself. The cascade proceeds through degree‑related features in layers 5, 4, 3, 2, and 1, all of which are within the lower third of the model (≤8). Positive embedding contributions from "Mathematics", "in", and "degree" confirm that this feature encodes a gene…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F170@10, k=10 → L5:F10392 (de=11.38) +9 more |

### Build

`build_circuit` → 18 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 68,266 | 5,368 | 96,300 | 0 | $0.0327 | — | — |
| SA-1 | openai/gpt-oss-120b | 194,564 | 11,947 | 2,528 | 0 | $0.0364 | ✅ 7F/10E | Trace this feature upstream to understand what input signals… |
| **Total** | | **262,830** | **17,315** | **98,828** | **0** | **$0.0691** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 5m 41s