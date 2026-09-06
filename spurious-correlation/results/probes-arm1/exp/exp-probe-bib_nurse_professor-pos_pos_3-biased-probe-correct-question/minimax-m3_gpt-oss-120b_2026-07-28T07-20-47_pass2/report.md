# Circuit Oracle Report
**Date:** 2026-07-28 07:20:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The nurse-classification probe is driven by a mixture of genuine nursing signals AND prominent spurious gender/name features that fire on female-entity cues rather than profession content.

**Confidence:** 7

**Reasoning:** The top 15 features driving the probe (ranked by direct_effect) fall into two distinct streams:

**(1) Legitimate profession signal — present but not dominant.** The nursing-specific path is anchored at `L6:F15267` (label: "words in the document referring to the profession of nursing", frac_nonzero=0.016, direct_effect=+0.39) which is excited directly by the embeddings of "nurse" (pos 7, de=+7.06) and "practitioner" (pos 8, de=+3.48) via a chain of medical-vocabulary features (L5:F1275 "healthcare professionals and medical fields", L4:F11037 "counseling/therapy/social work", L1:F1494 "medical practices and studies"). This is the *only* feature in the top-15 that genuinely encodes the profession, and its downstream reach is narrow (it only fires at the "practitioner" position).

**(2) Spurious gender/name signal — dominant.** Four of the top features encode female entity references rather than profession:
- `L18:F14677` (label: "instances of women or girls being mentioned", frac_nonzero=0.012, de=+0.32 at pos 1, +0.32 at pos 55) — strongly driven by the "She" embedding (de=+27 to the feature). Its top activating examples are uniformly pronoun-based.
- `L6:F11646` (label: "references to women, potentially triggered by pronouns and titles", de=+0.49 at pos 1, +0.40 at pos 2) — same story, fed by the "She" embedding (de=+19).
- `L19:F9685` (label: "references to women's names and their roles or accomplishments", de=+0.24 at pos 24) — even its Neuronpedia top activating example (#5) is literally a nursing bio: "Debbie Gregory DNP, RN … Dr. Debbie Gregory is a national leader" — i.e., the feature has learned to detect "female-named nurse bios" as a single concept. Its upstream drivers are embeddings for "Linda" (de=+3.45), "She" (de=+2.98), and "nurse" (de=+1.80).
- `L12:F12940` (label: "references to female pronouns and possessive pronouns", de=+0.32) — pure pronoun detector, top activations all on "her/herself".

The intermediate layers (L0:L2:L4:L5 pronoun detectors L2:F2128, L4:F7864, L5:F10952) all have promoted-token lists headed by "herself/she/her", and `L4:F7864` is officially labeled "XML/source code" but its top promoted tokens are also feminine pronouns — it is being reused as a pronoun feature in this context. The "Linda" position path goes through proper-noun detectors (L0:F7532, L4:F1276, L4:F15644, L2:F5859 labeled "first names mostly female", L6:F8166 "proper names ending in a/i/e") which all carry gender associations in their promoted tokens.

**Quantitative picture of the user's concern:** Summing the direct_effects of the top gender/name features (≈0.49+0.40+0.32+0.32+0.32+0.32+0.32+0.30 ≈ 2.8) versus the only genuine profession feature (≈0.39) — the spurious gender signal contributes roughly 6–7× more to the probe score than the actual nursing vocabulary. The probe is almost certainly using female-entity cues ("She", "her", "Linda", "Daphne", "Debbie") as a shortcut for the nursing profession, because the training data presumably had heavy female pronoun/name priors in nursing bios. The `L19:F9685` "women's names and their roles" feature is particularly damning evidence: it has no profession-specificity at all, and its top activating example IS a nursing bio, showing the model has conflated "female-named professional" with "nurse" at the late-layer feature level.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: "She" (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: " nurse" (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 24 | Emb: " Linda" (pos 24) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: " practitioner" (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L2:F2128](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) | 1 | Low-layer pronoun / female-reference features (pos 1) |  pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, *ele*, and *ela* across multiple languages. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2128) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Low-layer pronoun / female-reference features (pos 1) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Low-layer pronoun / female-reference features (pos 1) | third person pronouns in varying contexts | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Low-layer pronoun / female-reference features (pos 1) |  named entities like characters or people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 24 | Low-layer name/proper-noun features (pos 24 "Linda") | proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 24 | Low-layer name/proper-noun features (pos 24 "Linda") | first names (mostly female) | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 24 | Low-layer name/proper-noun features (pos 24 "Linda") | capitalized names and titles, and names with lowercase letters in the middle of them | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L4:F15644](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15644) | 24 | Low-layer name/proper-noun features (pos 24 "Linda") | names of people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15644) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 24 | Low-layer name/proper-noun features (pos 24 "Linda") |  proper names longer than 4 characters and ending in 'a', 'i', or 'e' | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 24 | Low-layer name/proper-noun features (pos 24 "Linda") |  woman's name in a variety of contexts | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F2765](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) | 24 | Low-layer name/proper-noun features (pos 24 "Linda") |  mentions of people or characters, and their performance, roles, injuries, or personal details such as age, death, or family. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2765) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 8 | Low-layer medical/nursing features (pos 7-8 "nurse practitioner") | words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 8 | Low-layer medical/nursing features (pos 7-8 "nurse practitioner") | words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 8 | Low-layer medical/nursing features (pos 7-8 "nurse practitioner") | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 46 | Low-layer medical/nursing features (pos 7-8 "nurse practitioner") |  terms related to obstetrics and gynecology | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Mid-layer female-reference feature (pos 1) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Mid-layer female-reference feature (pos 1) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid-layer female-reference feature (pos 1) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Mid-layer nursing-specific feature (pos 8) | words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 24 | Mid-layer person-name aggregator (pos 24 "Linda") | names of people, both first and last names | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Late-layer women-references feature (pos 1) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 55 | Late-layer women-references feature (pos 1) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 24 | Late-layer women's-names + roles feature (pos 24) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=0.494 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ✅ reported | 4 | 7 | Trace this feature at pos 1 (likely "She" or " has"). This is a top driver of th… |
| SA-2 | `L18:F14677@1` | ✅ reported | 5 | 6 | Trace this late-layer feature at pos 1. Determine what it encodes - is it profes… |
| SA-3 | `L19:F9685@24` | ❌ error | — | — | Trace this late-layer feature at pos 24 (around "Linda has spent most of her lif… |
| SA-4 | `L12:F14970@24` | ✅ reported | 6 | 5 | Trace this mid-layer feature at pos 24. Determine what it encodes. Try to reach … |
| SA-5 | `L6:F15267@8` | ✅ reported | 6 | 5 | Trace this feature at pos 8. The text at that position likely relates to nurse p… |
| SA-6 | `L12:F12940@2` | ❌ error | — | — | Trace this mid-layer feature at pos 2 (likely " has"). Determine what it encodes… |

<details>
<summary><b>SA-1</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 2 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L5, F10952 | "third person pronouns in varying contexts" |
| 5 | `get_upstream_features` | L4:F7864@1, k=10 | Emb:"She"@1 (de=24.62) +9 more |
| 6 | `get_upstream_features` | L5:F10952@1, k=10 | Emb:"She"@1 (de=8.56) +9 more |
| 7 | `inspect_feature` | L2, F2128 | " pronouns, especially "he/him/it" equivalents like *er*, *ihn*, *es*, " |

**Findings:** The top driver at L6:F11646 encodes feminine pronoun/ women reference detection. Its strongest upstream source is the raw embedding for the token "She" (direct_effect ~19), which passes through a multilingual pronoun detector (L2:F2128) and more specialized intermediate features (L4:F7864, L5:F10952) before arriving at the gender‑specific gate. All paths are positive, and we have reached a lower‑t…

</details>

<details>
<summary><b>SA-2</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14677 | " instances of women or girls being mentioned" |
| 2 | `get_upstream_features` | L18:F14677@1, k=10 | Emb:"She"@1 (de=27.12) +9 more |
| 3 | `inspect_feature` | L4, F7864 | "xml or source code snippets, especially tags and possibly keywords in " |
| 4 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 5 | `get_upstream_features` | L4:F7864@1, k=5 | Emb:"She"@1 (de=24.62) +4 more |
| 6 | `inspect_feature` | L15, F851 | " code documentation blocks in various programming languages" |
| 7 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |

**Findings:** The target L18:F14677 is a gender‑related feature that fires on mentions of women/girls. Its strongest positive upstream driver is the raw embedding for the pronoun "She" (direct_effect ~27), confirming a direct gender encoding. Secondary upstream contributors include another gender‑related feature in layer 6 (references to women) and a code‑snippet detector in layer 4, which have only modest posi…

</details>

<details>
<summary><b>SA-4</b> — tool trace (16 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F14970 | " names of people, both first and last names" |
| 2 | `get_upstream_features` | L12:F14970@24, k=10 | Emb:"<bos>"@0 (de=-3.17) +9 more |
| 3 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 4 | `inspect_feature` | L7, F2765 | " mentions of people or characters, and their performance, roles, injur" |
| 5 | `inspect_feature` | L4, F1276 | "capitalized names and titles, and names with lowercase letters in the " |
| 6 | `get_upstream_features` | L0:F7532@24, k=10 | Emb:" Linda"@24 (de=19.00) +9 more |
| 7 | `get_upstream_features` | L7:F2765@24, k=10 | Emb:"She"@1 (de=3.12) +9 more |
| 8 | `inspect_feature` | L2, F5859 | " first names (mostly female)" |
| 9 | `inspect_feature` | L6, F11646 | " references to women, potentially triggered by pronouns and titles" |
| 10 | `get_upstream_features` | L6:F11646@1, k=10 | Emb:"She"@1 (de=19.25) +9 more |
| 11 | `inspect_feature` | L6, F8166 | " proper names longer than 4 characters and ending in 'a', 'i', or 'e'" |
| 12 | `get_upstream_features` | L2:F5859@24, k=10 | Emb:" Linda"@24 (de=4.75) +9 more |
| 13 | `get_upstream_features` | L4:F1276@24, k=10 | Emb:" Linda"@24 (de=4.97) +9 more |
| 14 | `inspect_feature` | L8, F2181 | " proper nouns, especially people's names" |
| 15 | `get_upstream_features` | L6:F8166@24, k=10 | L5:F6637 (de=-3.17) +9 more |
| 16 | `inspect_feature` | L4, F15644 | "names of people" |

**Findings:** The mid‑layer feature L12:F14970 aggregates lower‑layer name detectors. Positive upstream influence comes from a concrete name embedding ('Linda') that excites L0:F7532 (proper noun), L4:F1276, L2:F5859, and L4:F15644. Additionally, the pronoun 'She' drives L7:F2765, a generic person‑reference detector. All contributing upstream features lie in layers ≤ 8, and the path terminates at embedding node…

</details>

<details>
<summary><b>SA-5</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F15267 | " words in the document referring to the profession of nursing" |
| 2 | `get_upstream_features` | L6:F15267@8, k=10 | Emb:" nurse"@7 (de=7.06) +9 more |
| 3 | `inspect_feature` | L5, F1275 | "words related to healthcare professionals and medical fields" |
| 4 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |
| 5 | `inspect_feature` | L1, F1494 | " words related to medical practices and studies." |
| 6 | `get_upstream_features` | L5:F1275@8, k=10 | Emb:" nurse"@7 (de=2.30) +9 more |
| 7 | `get_upstream_features` | L4:F11037@8, k=10 | Emb:" practitioner"@8 (de=7.03) +9 more |
| 8 | `get_upstream_features` | L1:F1494@8, k=10 | Emb:" nurse"@7 (de=10.75) +9 more |

**Findings:** Feature L6:F15267 at position 8 strongly responds to the word "nurse" and related variants. Its most influential upstream drivers are the raw token embeddings for "nurse" (direct effect 7.06) and "practitioner" (3.48), plus higher‑level features that detect healthcare professional language (L5:F1275), multidisciplinary care team language (L4:F11037), and generic medical practice language (L1:F1494…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×9 | L19:9685, L12:12940, L4:7864, L4:15317, L18:14677, L7:2765, L7:8644, L4:13803, L6:8166 |
| 2 | `get_upstream_features` | L19:F9685@24, k=5 → Emb:" Linda"@24 (de=3.45) +4 more |
| 3 | `inspect_feature` ×2 | L6:11646, L4:15317 |

### Build

`build_circuit` → 13 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 36,985 | 4,436 | 69,733 | 0 | $0.0206 | — | — |
| SA-2 | openai/gpt-oss-120b | 64,332 | 4,611 | 5,056 | 0 | $0.0125 | ✅ 5F/6E | Trace this late-layer feature at pos 1. Determine what it en… |
| SA-1 | openai/gpt-oss-120b | 58,799 | 3,728 | 10,112 | 0 | $0.0112 | ✅ 4F/7E | Trace this feature at pos 1 (likely "She" or " has"). This i… |
| SA-5 | openai/gpt-oss-120b | 86,996 | 5,797 | 5,056 | 0 | $0.0166 | ✅ 6F/5E | Trace this feature at pos 8. The text at that position likel… |
| SA-4 | openai/gpt-oss-120b | 268,716 | 11,927 | 7,616 | 0 | $0.0476 | ✅ 6F/5E | Trace this mid-layer feature at pos 24. Determine what it en… |
| **Total** | | **515,828** | **30,499** | **97,573** | **0** | **$0.1085** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 31s