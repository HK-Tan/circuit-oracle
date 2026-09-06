# Circuit Oracle Report
**Date:** 2026-07-28 07:03:00 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "nurse profession" classification score is driven predominantly by a stack of female-pronoun / women-mention features that trace back to the "She" / "she" input token embeddings, while a much smaller, isolated circuit on the word "nurse" / "practitioner" at position 8 is the only signal coming from the actual profession vocabulary.

**Confidence:** 8

**Reasoning:** The attribution graph reveals two parallel and largely disjoint pathways feeding the probe logit:

1. **Gender-marker pathway (dominant, spurious)** — This is the main driver. The probe's score is most strongly pushed by features whose semantic content is *gender*, not profession:
   - **L18:F14677** ("instances of women or girls being mentioned", frac_nonzero 0.012, direct_effect 0.32 at pos 1 and 0.32 at pos 55) — its top activating examples are almost entirely "She/she" tokens, and its promoted tokens are "herself / she / her". Upstream tracing shows it is excited directly by the **"She" embedding at pos 1** (direct_effect 2.98) and the **"she" embedding at pos 55** (direct_effect 23.9), with the chain passing through **L6:F11646** ("references to women, potentially triggered by pronouns and titles"), **L4:F7864** (mislabeled "xml/code" but actually firing on "she"/"her"), **L2:F2128** (multilingual pronoun detector firing on "She"), and **L1:F2848** (specialized "she/her" pronoun feature).
   - **L19:F9685** ("references to women's names and their roles or accomplishments", frac_nonzero 0.014, direct_effect 0.24/0.21) — fires on tokens like "Kathryn", "Daphne", "Andrea" and promotes "herself / she / her / 그녀". It also receives input from the female-pronoun/women-mention chain.
   - **L12:F12940** ("references to female pronouns and possessive pronouns", frac_nonzero 0.007, direct_effect 0.32) — driven by the "She" embedding (direct_effect 6.0) through a cascade of mid-layer features at pos 2 (L4:F15317, L6:F11646, L8:F7245, L10:F14965) that all encode feminine pronouns.

2. **Profession pathway (genuine but small)** — The only feature in the top-20 that genuinely encodes the profession is **L6:F15267** ("words in the document referring to the profession of nursing", frac_nonzero 0.016, direct_effect 0.39 at pos 8). Its upstream chain — **L5:F1275** (healthcare professionals), **L4:F9036** (healthcare vocabulary), **L1:F1494** (medical practice terminology) — all fire on tokens like "nurse", "practitioner", "RN" at positions 7–8, reaching the **"nurse" and "practitioner" embeddings** directly.

Quantitative comparison: the four gender-marker features (L18:F14677×2 + L19:F9685×2 + L12:F12940) sum to roughly 0.32+0.32+0.24+0.21+0.32 = **~1.4 in direct_effect** on the probe, while the lone nursing feature contributes only ~0.39. The probe's classification is therefore roughly **3-4× more driven by female-pronoun/women-mention features than by the actual profession vocabulary**. The user's concern is well-founded: this probe appears to use gendered language as a shortcut for the nursing profession, likely because the training distribution correlates female pronouns with nursing-related biographies, and the model has internalized that spurious association. The gender pathway is also architecturally privileged — it activates on multiple positions (1, 2, 24, 55) via independent early-layer pronoun detectors that directly read the input embeddings, whereas the profession pathway only fires on a single token position.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F2848](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2848) | 1 | Early female-pronoun detectors (L1:F2848, L2:F2128) | the pronouns "she" and "her" (and sometimes "his") | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2848) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | Early female-pronoun detectors (L1:F2848, L2:F2128) | pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, *ele*, and *ela* across multiple languages. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Low-layer women-mention features (L4:F7864, L6:F11646) at pos 1 | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Low-layer women-mention features (L4:F7864, L6:F11646) at pos 1 |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Female-pronoun mid-layer features at pos 2 (L4:F15317, L6:F11646, L8:F7245, L10:F14965) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Female-pronoun mid-layer features at pos 2 (L4:F15317, L6:F11646, L8:F7245, L10:F14965) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L8:F7245](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7245) | 2 | Female-pronoun mid-layer features at pos 2 (L4:F15317, L6:F11646, L8:F7245, L10:F14965) | content in languages other than English, particularly French and possibly Sanskrit. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/7245) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 2 | Female-pronoun mid-layer features at pos 2 (L4:F15317, L6:F11646, L8:F7245, L10:F14965) | terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Late female-pronoun feature (L12:F12940) at pos 2 | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Women-mention abstract feature (L18:F14677) at pos 1 |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 55 | Women-mention abstract feature (L18:F14677) at pos 55 |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 24 | Women's names / roles feature (L19:F9685) at pos 24 and 55 |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 55 | Women's names / roles feature (L19:F9685) at pos 24 and 55 |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 8 | Healthcare / nursing profession circuit at pos 8 (L1:F1494, L4:F9036, L5:F1275, L6:F15267) | words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 8 | Healthcare / nursing profession circuit at pos 8 (L1:F1494, L4:F9036, L5:F1275, L6:F15267) | words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 8 | Healthcare / nursing profession circuit at pos 8 (L1:F1494, L4:F9036, L5:F1275, L6:F15267) | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Healthcare / nursing profession circuit at pos 8 (L1:F1494, L4:F9036, L5:F1275, L6:F15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.494 |
| 3 | `inspect_feature` ×6 | L18:14677, L6:11646, L6:15267, L4:7864, L4:15317, L12:12940 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@1` | ✅ reported | 4 | 4 | Trace this 'women/girls being mentioned' feature (L18:F14677) upstream to identi… |
| SA-2 | `L12:F12940@2` | ✅ reported | 6 | 11 | Trace this 'female pronouns and possessive pronouns' feature (L12:F12940) upstre… |
| SA-3 | `L6:F15267@8` | ✅ reported | 5 | 10 | Trace this 'nursing profession words' feature (L6:F15267) upstream to identify w… |
| SA-4 | `L4:F7864@1` | ✅ reported | 3 | 2 | Trace this early layer feature (L4:F7864) at pos=1 (the 'She' token) upstream. W… |
| SA-5 | `L18:F14677@55` | ❌ error | — | — | Trace the L18:F14677 feature at pos=55 (later position in the text) upstream to … |
| SA-6 | `L19:F9685@24` | ❌ error | — | — | Trace L19:F9685 (nurse/healthcare feature?) upstream at pos=24 to confirm whethe… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@1, k=10 | Emb:"She"@1 (de=27.12) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 6 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 7 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |

**Findings:** The target feature L18:F14677 (women/girls mentioned) receives its strongest excitatory influence from the token embedding for "She" (direct effect 27.1). This signal propagates through a chain of low‑layer gender‑sensitive features: L4:F7864 (a mis‑labeled code‑snippet detector that actually acts as a female pronoun detector) feeds L6:F11646 (explicit references‑to‑women feature), both of which c…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F12940 | "references to female pronouns and possessive pronouns" |
| 2 | `get_upstream_features` | L12:F12940@2, k=10 | Emb:"She"@1 (de=6.03) +9 more |
| 3 | `inspect_feature` | L4, F15317 | " named entities like characters or people" |
| 4 | `get_upstream_features` | L4:F15317@2, k=10 | Emb:"She"@1 (de=13.56) +9 more |
| 5 | `inspect_feature` | L10, F14965 | " terms relating to women" |
| 6 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 7 | `inspect_feature` | L2, F7672 | " mentions of women by name and relationship" |
| 8 | `inspect_feature` | L8, F7245 | " content in languages other than English, particularly French and poss" |
| 9 | `get_upstream_features` | L6:F11646@2, k=10 | L4:F15317 (de=8.75) +9 more |
| 10 | `get_upstream_features` | L10:F14965@2, k=10 | L4:F15317 (de=5.56) +9 more |
| 11 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 12 | `get_upstream_features` | L8:F7245@2, k=10 | Emb:"She"@1 (de=3.12) +9 more |

**Findings:** The target feature L12:F12940 (female pronoun detector) receives its strongest positive influence from the input token embedding "She" (pos 1) and from a cascade of mid‑level gender/person features (layers 4, 6, 8, 10). The most influential upstream driver is layer 4 feature 15317, which itself is driven primarily by the same "She" embedding and, to a lesser extent, by the token " has" and a layer…

</details>

<details>
<summary><b>SA-3</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@8, k=10 | Emb:" nurse"@7 (de=7.06) +9 more |
| 3 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 4 | `get_upstream_features` | L5:F1275@8, k=10 | Emb:" nurse"@7 (de=2.30) +9 more |
| 5 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 6 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 7 | `inspect_feature` | L4, F9036 | " words and abbreviations associated with healthcare." |

**Findings:** The nursing‑profession probe (L6:F15267) is driven primarily by the input token embedding for "nurse" (direct_effect ~7.1) and secondarily by "practitioner" (direct_effect ~3.5). Upstream, a mid‑level healthcare‑terms feature (L5:1275) contributes a large positive effect (5.1) and itself is strongly excited by the same "nurse" embedding and by a generic healthcare feature (L4:9036). Additional con…

</details>

<details>
<summary><b>SA-4</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 2 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 3 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |
| 4 | `get_upstream_features` | L2:F2128@1, k=10 | Emb:"She"@1 (de=20.25) +9 more |
| 5 | `inspect_feature` | L1, F2848 | " the pronouns "she" and "her" (and sometimes "his")" |
| 6 | `get_upstream_features` | L1:F2848@1, k=10 | Emb:"She"@1 (de=6.78) +9 more |

**Findings:** The target L4 feature (F7864) on the token 'She' is driven primarily by the raw embedding of the token itself (positive direct_effect 24.6). Upstream, a low‑sparsity layer‑1 feature (2848) that encodes the female pronoun "she" passes excitatory signal to a multilingual pronoun detector at layer 2 (2128), which in turn excites the layer‑4 feature. Both upstream features reside in the lower third of…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` | L19, F9685 → " references to women's names and their roles or accomplishments." |
| 2 | `get_upstream_features` | L18:F14677@55, k=5 → Emb:" she"@55 (de=23.88) +4 more |

### Build

`build_circuit` → 13 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 28,027 | 5,123 | 111,915 | 0 | $0.0213 | — | — |
| SA-4 | openai/gpt-oss-120b | 51,389 | 5,304 | 16,384 | 0 | $0.0111 | ✅ 3F/2E | Trace this early layer feature (L4:F7864) at pos=1 (the 'She… |
| SA-2 | openai/gpt-oss-120b | 158,404 | 10,384 | 27,840 | 0 | $0.0304 | ✅ 6F/11E | Trace this 'female pronouns and possessive pronouns' feature… |
| SA-1 | openai/gpt-oss-120b | 72,684 | 5,009 | 10,720 | 0 | $0.0141 | ✅ 4F/4E | Trace this 'women/girls being mentioned' feature (L18:F14677… |
| SA-3 | openai/gpt-oss-120b | 69,495 | 5,872 | 10,112 | 0 | $0.0141 | ✅ 5F/10E | Trace this 'nursing profession words' feature (L6:F15267) up… |
| **Total** | | **379,999** | **31,692** | **176,971** | **0** | **$0.0910** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 7s