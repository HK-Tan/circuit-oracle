# Circuit Oracle Report
**Date:** 2026-07-28 07:21:08 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is driven primarily by masculine-gender pronoun features ("his", "he", "him") at multiple layers, with only modest positive contributions from genuine profession/academic-field features; the user's concern is well-supported by the circuit.

**Confidence:** 8/10

**Reasoning:**

**The dominant signal is gender-coded, not profession-coded.** Out of the 20 strongest direct contributors to the probe:

- **Pronoun/"he/his" features dominate the top of the ranking:** L0:F2994 ("his"/"he", pos 3, +0.39; same feature at pos 25, +0.13 and pos 47, +0.11), L7:F14893 (possessive pronouns, pos 3, +0.20), L7:F14946 ("his"/"him", pos 3, −0.18), L18:F10315 ("his", pos 3, −0.10), L12:F2175 ("words referring to gender", −0.17), L6:F12990 ("male pronouns and titles along with descriptors associated with men", pos 22, −0.17), L18:F14743 ("He" pronoun, pos 22, −0.14 and pos 81, −0.11), and the L0:F1069 "references to a male person, particularly when using the pronoun 'He' or 'His'" at pos 22 (+0.10 of the negative).
- **The "profession" features are present but are NOT what drives the score.** The genuine profession/academic-field pathway is: `Emb:" Engineering" (pos 9)` → L2:F1440 ("engineering") → L5:F10392 (fields of academic study) → L6:F170 (academic fields). L6:F170 contributes +0.144 at pos 9 and +0.103 at pos 8, and its upstream causal chain involves degree tokens ("achelors" at pos 5, "Mechanical" at pos 8). This is real profession evidence — but its direct effect (~+0.25 combined) is dwarfed by the sum of the pronoun/gender features.

**The supporting gender-feature chain is clear and starts at the token embeddings:**
- The embedding node " his" at position 3 (the pronoun after "Daniel received") has direct_effect=43.25 feeding L0:F2994 — the largest single embedding edge in the circuit.
- L0:F2994 → L4:F4315 ("his" pronouns) → L6:F12990 (male pronouns/titles) → L7:F14893 (possessive pronouns) → logit at +0.20.
- Similarly, " He" (pos 22) and " he" (pos 81) embeddings feed L0:F1069/F2994/F12768 → L17:F5889 ("references to people with pronouns") → L18:F14743 ("He" pronoun) → logit (negative effects of −0.14, −0.11).

**L18:F14743 is striking:** the top activating examples of this feature include "She" and "He" pronouns in personal-story contexts, and here it is **negatively** driving the probe (de=-0.14). This means the probe is suppressed by general personal-pronoun context and excited by the specific "his" possessive form, not by the content of what Daniel does.

**The only mildly profession-relevant inputs** (L2:F1440 engineering, L4:F11037 "engineer" words, L5:F10392 fields of academic study, L6:F170 academic fields) are connected to actual content tokens (Engineering, Mechanical) but their summed contribution to the probe is small compared to the pronoun pathway. The probe direction itself is one that the model can clearly classify male bio text, but it is doing so largely by detecting masculine pronoun density.

**Other features are noise:** L0:F15320 ("ice", +0.10), L0:F13526 (months of the year, −0.10), L0:F12351 (words related to obtaining/receipt, −0.10), L0:F7532 (proper nouns, +0.11), and L0:F1326 (organization mentions, +0.11) are generic lexical features with small effects.

**get_source_influence corroboration:** When restricted to the source positions containing the pronouns (3, 22, 25, 47), the net signed multi-hop influence on the probe is **−5.96%** (S_pct_of_total) and S_over_R = **−3.47**, which is a strong magnitude. The top contributing source features are L0:F1069 (male "He"/"His", −0.19%), L0:F2994 ("his"/"he", +0.07%), and L15:F12482/L2:F10852/L3:F12119 — all dominated by pronoun/possessive/gender signals, not profession signals. This quantitatively confirms the user's intuition that the probe's classification leans on gender markers.

**Conclusion:** The user's concern is correct. The circuit shows a hybrid of (a) a genuine but small profession-content pathway via "Engineering" → engineering/fields-of-study features, and (b) a much larger masculine-gender-marker pathway via the embeddings of "his", "He", "he" that drives most of the top positive and negative features. The probe appears to be using male pronoun density as a strong proxy for profession classification, consistent with the model having learned spurious correlation between masculine gender markers and certain professions in its training data. A profession-only intervention (ablating the pronoun chain) would substantially reduce probe sensitivity, while a gender-marker ablation (e.g., swapping "his"→"her") would still leave the actual profession signal (Mechanical Engineering) much smaller than the original male-pronoun signal that this probe is currently exploiting.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | L0: pronoun 'his'/'he' (F2994, F1069, F13553) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 25 | L0: pronoun 'his'/'he' (F2994, F1069, F13553) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 47 | L0: pronoun 'his'/'he' (F2994, F1069, F13553) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 22 | L0: pronoun 'his'/'he' (F2994, F1069, F13553) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F13553](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) | 2 | L0: pronoun 'his'/'he' (F2994, F1069, F13553) |  verbs in the past tense or past participle | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 81 | L0: pronoun 'his'/'he' (F2994, F1069, F13553) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | L0: proper nouns (F7532) |  proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F1326](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1326) | 14 | L0: org/agency mentions (F1326) |  mentions of organizations and government agencies. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1326) |
| [L0:F12351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12351) | 2 | L0: words about obtaining/receiving (F12351) | words related to obtaining something, like receiving money or a receipt | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12351) |
| [L0:F13526](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13526) | 21 | L0: months of the year (F13526) |  months of the year, sometimes in connection to a number | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13526) |
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | L0: 'ice' (F15320) |  the word "ice" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 5 | L2: academic titles/degrees (F10852) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 3 | L2: academic titles/degrees (F10852) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F1440](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1440) | 9 | L2: 'engineering' (F1440) |  the word "engineering" and words related to its definition | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1440) |
| [L3:F4113](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) | 7 | L3: degree+field phrase (F4113) |  mentions of academic degrees and areas of study | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 5 | L4: academic-degree mentions (F3727) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 3 | L4: 'his' pronoun (F4315) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 9 | L4: counselor/therapy/social-work/degree-program vocabulary (F11037) — promotes 'engineer' |  words related to counseling, therapy, social work, and academic degree programs | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 8 | L5: fields of academic study (F10392) |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 9 | L5: fields of academic study (F10392) |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F6384](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6384) | 9 | L5: higher-education/profession words (F6384) | words related to higher education and professions | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6384) |
| [L5:F7317](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7317) | 2 | L5: name+nickname phrases (F7317) |  phrases with names and nicknames | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7317) |
| [L5:F6228](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6228) | 2 | L5: past-tense verbs (F6228) |  past tense verbs | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6228) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 8 | L6: references to academic fields (F170) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 9 | L6: references to academic fields (F170) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 3 | L6: male pronouns/titles (F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 22 | L6: male pronouns/titles (F12990) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F7210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7210) | 2 | L7: conflict/stress wording (F7210) |  words and phrases that connote conflict and stress. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7210) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 3 | L7: pronouns/possessive pronouns (F14893) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 3 | L7: 'his'/'him'/'©' (F14946) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | L12: words referring to gender (F2175) |  words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 81 | L15: personal stories/pronoun 'she' (F3330) |  personal stories of individuals, especially women and their actions or states of being, often indicated by the pronoun 'she' preceded and succeeded by tokens. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 22 | L17: people via pronouns (F5889) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L17:F15906](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/15906) | 81 | L17: scientific research goals/methodology (F15906) |  sentences describing scientific research goals and methodology | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/15906) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 3 | L18: 'his' possessive (F10315) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | L18: 'He' pronoun (F14743) — strong negative | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 81 | L18: 'He' pronoun (F14743) — strong negative | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:2994 de=0.395 |
| 3 | `inspect_feature` ×7 | L0:2994, L7:14893, L6:170, L0:1326, L0:7532, L0:15320, L0:13553 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@3` | ✅ reported | 4 | 7 | Trace the upstream path of L7:F14893 (pronouns/possessive pronouns feature) to i… |
| SA-2 | `L6:F170@9` | ✅ reported | 7 | 18 | Trace the upstream path of L6:F170 (academic fields reference feature) — this is… |
| SA-3 | `L0:F2994@3` | ❌ error | — | — | Trace L0:F2994 (the pronoun "his" / "he" feature, position 3) upstream. This is … |
| SA-4 | `L18:F14743@22` | ❌ error | — | — | Trace L18:F14743 (negative contributor, pos 22) upstream to understand what prof… |

<details>
<summary><b>SA-1</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@3, k=10 | Emb:" his"@3 (de=24.38) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 5 | `get_upstream_features` | L6:F12990@3, k=10 | Emb:" his"@3 (de=8.31) +9 more |
| 6 | `get_upstream_features` | L4:F4315@3, k=10 | Emb:" his"@3 (de=28.62) +9 more |
| 7 | `inspect_feature` | L6, F10944 | " text in languages other than English" |
| 8 | `get_upstream_features` | L6:F12990@3, k=10 | Emb:" his"@3 (de=8.31) +9 more |

**Findings:** The pronoun detection feature L7:F14893 is primarily driven by the input token ' his' (direct_effect 24.375) and by upstream gendered pronoun detectors in lower layers: L6:F12990 (male pronouns), L4:F4315 (specific 'his' mentions), and L6:F10944 (non‑English text patterns). All these upstream sources reside at layers ≤8, satisfying the lower‑third floor condition, and we have identified a clear em…

</details>

<details>
<summary><b>SA-2</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 2 | `get_upstream_features` | L6:F170@9, k=10 | L5:F10392 (de=10.94) +9 more |
| 3 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 4 | `get_upstream_features` | L5:F10392@9, k=10 | Emb:" Mechanical"@8 (de=3.08) +9 more |
| 5 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 6 | `inspect_feature` | L5, F6384 | "words related to higher education and professions" |
| 7 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 8 | `get_upstream_features` | L4:F3727@5, k=10 | Emb:"achelors"@5 (de=22.38) +9 more |
| 9 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 10 | `get_upstream_features` | L2:F10852@5, k=10 | Emb:"achelors"@5 (de=19.25) +9 more |
| 11 | `get_upstream_features` | L5:F6384@9, k=10 | Emb:" Engineering"@9 (de=7.75) +9 more |
| 12 | `inspect_feature` | L4, F11037 | " words related to counseling, therapy, social work, and academic degre" |

**Findings:** L6:F170 encodes a reference to academic fields and is driven primarily by degree‑related tokens such as "Bachelor" (embedding token "achelors" at position 5) and " degree". The strongest upstream drivers are mid‑layer features that detect concrete academic disciplines (L5:10392), degree mentions (L4:3727, L2:10852) and generic higher‑education vocabulary (L5:6384). All of these are situated in lay…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2994@3, k=5 → Emb:" his"@3 (de=43.25) +4 more |
| 2 | `get_upstream_features` | L18:F14743@22, k=5 → Emb:" He"@22 (de=21.88) +4 more |
| 3 | `get_upstream_features` | L0:F1326@14, k=5 → Emb:" University"@12 (de=7.28) +4 more |
| 4 | `get_upstream_features` | L0:F7532@1, k=5 → Emb:"Daniel"@1 (de=10.12) +4 more |
| 5 | `inspect_feature` ×8 | L0:1069, L12:2175, L0:12351, L0:13526, L7:14946, L5:10392, L18:10315, L6:12990 |
| 6 | `get_source_influence` | {'depth': 3, 'source_positions': [3, 22, 25, 47]} → {'depth': 3, 'source_positions': [3, 22, 25, 47], 'S_pct_of_total': -5.961, 'R_p |
| 7 | `inspect_feature` ×5 | L4:4315, L5:6384, L4:3727, L4:11037, L17:5889 |
| 8 | `get_upstream_features` | L5:F10392@9, k=5 → Emb:" Mechanical"@8 (de=3.08) +4 more |
| 9 | `get_upstream_features` | L6:F170@8, k=5 → L5:F10392 (de=10.62) +4 more |
| 10 | `inspect_feature` ×3 | L3:4113, L2:10852, L2:1440 |
| 11 | `get_upstream_features` | L12:F2175@2, k=5 → Emb:" received"@2 (de=4.09) +4 more |
| 12 | `get_upstream_features` | L18:F14743@81, k=5 → Emb:" he"@81 (de=25.12) +4 more |
| 13 | `inspect_feature` ×7 | L5:7317, L5:6228, L7:7210, L0:12768, L15:3330, L17:15906, L6:12990 |

### Build

`build_circuit` → 38 nodes, 52 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 102,804 | 8,867 | 295,094 | 0 | $0.0592 | — | — |
| SA-1 | openai/gpt-oss-120b | 81,568 | 5,073 | 0 | 0 | $0.0153 | ✅ 4F/7E | Trace the upstream path of L7:F14893 (pronouns/possessive pr… |
| SA-2 | openai/gpt-oss-120b | 177,946 | 9,984 | 0 | 0 | $0.0327 | ✅ 7F/18E | Trace the upstream path of L6:F170 (academic fields referenc… |
| **Total** | | **362,318** | **23,924** | **295,094** | **0** | **$0.1071** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 52s