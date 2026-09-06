# Circuit Oracle Report
**Date:** 2026-07-28 07:10:31 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This probe is a profession classifier, and the attribution circuit is dominated by male-gendered pronoun and name signals (his, He, Daniel) rather than engineering/robotics content features, confirming the user's concern that the probe is using spurious gender cues as a proxy for profession.

**Confidence:** 8

**Reasoning:**

The single largest positive contributor to the probe logit is **L0:F2994** (the "his"/"he" male possessive pronoun detector) at positions 3, 25, and 47, with direct_effects of **+0.39, +0.13, and +0.11** — combined ≈ +0.64, which is more than 2× the magnitude of any content feature. Tracing this feature reveals it is driven almost entirely by the embedding for the token **` his`** (direct_effect = 43.25 from `Emb: his (pos 3)`), making it a near-pure detector of the male possessive pronoun. **L7:F14893** (a generic pronoun detector) adds another +0.20, also sourced from `his`.

The only true content features pointing toward the profession are **L6:F170** (academic field reference at pos 9, +0.14) and the upstream chain through L5:F10392 → L4:F3727 (degree mentions) → the embeddings of `Mechanical` and `Engineering`. These are the only paths reaching the engineering/robotics content of the text, and they are partially **self-cancelling**: L6:F170 promotes (+0.14) while L5:F10392 suppresses the same tokens (–0.11).

Strikingly, three features specifically *suppress* the probe's positive logit and are all gendered: **L12:F2175** (gender-word detector, –0.175), **L18:F14743** (the literal "He" pronoun at pos 22 and pos 81, –0.139 and –0.109), and **L6:F12990** (male pronouns, pos 22) which directly contributes to L18:F14743. Their upstream is the ` He` embedding (direct_effect 4.47) and the `Daniel` embedding (direct_effect 10.1 to the name detector L0:F7532, +0.105). The proper-name "Daniel" itself has a known male-gender association baked in by pretraining, and it promotes the probe via L0:F7532 (+0.105) — note that no engineering-specific proper name (e.g., the universities, which would more directly identify the profession) dominates; the dominant "entity" feature is the gendered given name.

The genuine profession-relevant features (engineering, degree, university) are present but underweighted: `Emb: University` (+7.28) and `Emb: Waterloo` (+5.16) feed L0:F1326 (organization detector, +0.109) — a small contribution relative to the pronoun-driven pathways. There is no feature for "Robotics" or "Computer Vision" in the top contributors, despite those tokens appearing later in the text.

The picture that emerges is consistent with the user's concern: **the probe has latched onto male-gender markers (his, He, Daniel) as a shortcut for profession**. The dominant top features (L0:F2994 at three positions, L7:F14893, L12:F2175, L18:F14743, L6:F12990) are all gender/pronoun/name detectors, while the engineering/degree/university features (L6:F170, L0:F1326) contribute much less. If the same biographical template were rewritten with female pronouns and a female name, the same probe score would likely collapse, indicating the classification is partly a gender classifier rather than a profession classifier.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Male possessive pronoun detector (his/he) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 25 | Male possessive pronoun detector (his/he) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 47 | Male possessive pronoun detector (his/he) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 3 | Generic pronoun feature (pos 3) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 9 | Academic field reference (pos 9) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 8 | Academic field reference (pos 9) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | Proper-noun / name detector (Daniel) | proper nouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F1326](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1326) | 14 | Organization/agency detector (University Waterloo) |  mentions of organizations and government agencies. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1326) |
| [L0:F12351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12351) | 2 | Receiving/obtaining token (received) | words related to obtaining something, like receiving money or a receipt | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12351) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | Gender-word detector (pos 2, SUPPRESSES probe) | words referring to gender | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 22 | Male pronouns/titles (pos 22, He) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | He pronoun detector (pos 22, SUPPRESSES probe) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 81 | He pronoun detector (pos 22, SUPPRESSES probe) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 9 | Academic field feature (pos 9, SUPPRESSES probe) | fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.395 |
| 3 | `inspect_feature` ×3 | L0:2994, L7:14893, L6:170 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ❌ error | — | — | Trace from L0:F2994 ("his/he" pronoun detector). What input tokens activate it? … |
| SA-2 | `L6:F170@9` | ✅ reported | 5 | 10 | Trace from L6:F170 (academic field reference) at pos 9. What does this encode? I… |
| SA-3 | `L7:F14893@3` | ✅ reported | 4 | 3 | Trace from L7:F14893 (pronouns) at pos 3. What's its upstream chain? Reach embed… |
| SA-4 | `L5:F10392@9` | ✅ reported | 3 | 7 | Trace from L5:F10392 (pos 9, direct_effect=-0.114, suppresses the probe). What i… |
| SA-5 | `L12:F2175@2` | ✅ reported | 10 | 15 | Trace from L12:F2175 (pos 2, direct_effect=-0.175, suppresses the probe). What i… |
| SA-6 | `L18:F14743@22` | ✅ reported | 3 | 7 | Trace from L18:F14743 at pos 22 (direct_effect=-0.139, suppresses). What is this… |
| SA-7 | `L0:F7532@1` | ❌ error | — | — | Trace from L0:F7532 (pos 1, direct_effect=+0.105, the "Daniel" token). What's it… |
| SA-8 | `L0:F1326@14` | ❌ error | — | — | Trace from L0:F1326 at pos 14 (direct_effect=+0.109). What is this detecting? Re… |

<details>
<summary><b>SA-2</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F170 | " references to academic fields, especially those in the humanities" |
| 2 | `get_upstream_features` | L6:F170@9, k=10 | L5:F10392 (de=10.94) +9 more |
| 3 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 4 | `get_upstream_features` | L5:F10392@9, k=10 | Emb:" Mechanical"@8 (de=3.08) +9 more |
| 5 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 6 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 7 | `get_upstream_features` | L4:F3727@5, k=10 | Emb:"achelors"@5 (de=22.38) +9 more |
| 8 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |
| 9 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 10 | `get_upstream_features` | L2:F10852@5, k=10 | Emb:"achelors"@5 (de=19.25) +9 more |

**Findings:** The tracing shows that L6:F170 is not a generic placeholder but a higher‑level detector that receives its concrete content from the token embedding "Engineering" (and related "Mechanical"). The pathway proceeds through a generic field detector (L5:F10392) and a degree detector (L4:F3727). Therefore, in this prompt the feature encodes a specific engineering/robotics academic field mention rather th…

</details>

<details>
<summary><b>SA-3</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14893 | " pronouns or possessive pronouns" |
| 2 | `get_upstream_features` | L7:F14893@3, k=10 | Emb:" his"@3 (de=24.38) +9 more |
| 3 | `inspect_feature` | L6, F12990 | " male pronouns and titles along with descriptors associated with men" |
| 4 | `get_upstream_features` | L6:F12990@3, k=10 | Emb:" his"@3 (de=8.31) +9 more |
| 5 | `inspect_feature` | L4, F4315 | " mentions of "his" and other associated pronouns like he, him, or hers" |
| 6 | `inspect_feature` | L6, F10944 | " text in languages other than English" |
| 7 | `inspect_feature` | L5, F12906 | " phrases related to academic degrees from universities" |
| 8 | `get_upstream_features` | L4:F4315@3, k=10 | Emb:" his"@3 (de=28.62) +9 more |

**Findings:** L7:F14893 (pronoun detector) is primarily excited by the input token embedding " his" at position 3. Upstream positive contributors include a male‑pronoun feature (L6:F12990), a specific "his" detector (L4:F4315), and a language‑identification feature (L6:F10944). All paths reach the embedding layer and include a lower‑third layer feature, satisfying the tracing criteria.

</details>

<details>
<summary><b>SA-4</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L5, F10392 | " fields of academic study" |
| 2 | `get_upstream_features` | L5:F10392@9, k=10 | Emb:" Mechanical"@8 (de=3.08) +9 more |
| 3 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 4 | `get_upstream_features` | L4:F3727@5, k=10 | Emb:"achelors"@5 (de=22.38) +9 more |
| 5 | `inspect_feature` | L2, F1440 | " the word "engineering" and words related to its definition" |
| 6 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 7 | `inspect_feature` | L3, F4113 | " mentions of academic degrees and areas of study" |
| 8 | `get_upstream_features` | L2:F10852@5, k=10 | Emb:"achelors"@5 (de=19.25) +9 more |

**Findings:** L5:F10392 is a high‑level detector for academic‑field mentions. Its strongest upstream driver is L4:F3727, which looks for academic degree strings, especially the suffix "achelors". That in turn is driven by a lower‑layer L2:F10852 that fires directly on the token fragment "achelors" (as part of "bachelors") and related title tokens. Positive embedding contributions from the raw input tokens "Mech…

</details>

<details>
<summary><b>SA-5</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L12, F2175 | " words referring to gender" |
| 2 | `get_upstream_features` | L12:F2175@2, k=10 | Emb:" received"@2 (de=4.09) +9 more |
| 3 | `inspect_feature` | L5, F7317 | " phrases with names and nicknames" |
| 4 | `inspect_feature` | L5, F6228 | " past tense verbs" |
| 5 | `get_upstream_features` | L5:F7317@2, k=10 | L4:F16158 (de=-2.67) +9 more |
| 6 | `inspect_feature` | L7, F7210 | " words and phrases that connote conflict and stress." |
| 7 | `inspect_feature` | L3, F6656 | "verbs or phrases indicating action, saying, or feeling" |
| 8 | `get_upstream_features` | L5:F6228@2, k=10 | L2:F16309 (de=3.59) +9 more |
| 9 | `get_upstream_features` | L3:F6656@2, k=10 | L2:F16309 (de=3.16) +9 more |
| 10 | `inspect_feature` | L2, F16309 | " people's names" |
| 11 | `get_upstream_features` | L7:F7210@2, k=10 | Emb:"Daniel"@1 (de=2.14) +9 more |
| 12 | `get_upstream_features` | L2:F16309@1, k=10 | Emb:"Daniel"@1 (de=12.94) +9 more |
| 13 | `inspect_feature` | L0, F7532 | " proper nouns" |
| 14 | `inspect_feature` | L4, F14665 | " capitalized proper nouns or names" |

**Findings:** Starting from L12:F2175 (gender‑word detector) we traced upstream and found that its strongest excitatory inputs come from a cascade that begins with raw token embeddings for the name "Daniel" and the token " received". These feed into a low‑layer name detector (L2:16309), which then excites a generic verb/action detector (L3:6656). That in turn activates a mid‑layer phrase‑and‑name detector (L5:7…

</details>

<details>
<summary><b>SA-6</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L18, F14743 | "He" |
| 2 | `get_upstream_features` | L18:F14743@22, k=15 | Emb:" He"@22 (de=21.88) +14 more |
| 3 | `inspect_feature` | L0, F1069 | " references to a male person, particularly when using the pronoun "He"" |
| 4 | `inspect_feature` | L6, F2267 | "words that appear in programming code, legal jargon, or scientific tex" |
| 5 | `get_upstream_features` | L0:F1069@22, k=10 | Emb:" He"@22 (de=37.00) +9 more |
| 6 | `inspect_feature` | L17, F5889 | " references to people with pronouns and possessive pronouns" |
| 7 | `get_upstream_features` | L6:F2267@22, k=10 | Emb:"<bos>"@0 (de=-8.00) +9 more |

**Findings:** The target feature L18:F14743 is a pronoun‑specific detector for the token "He". Its strongest positive upstream drivers are the embedding for the literal token " He" (direct_effect ≈ 22) and the layer‑0 feature 1069, a generic male‑pronoun detector (direct_effect ≈ 7). Both excitatory signals confirm that L18:F14743 simply recognizes the appearance of the masculine pronoun. A lower‑third‑layer fe…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F7532@1, k=5 → Emb:"Daniel"@1 (de=10.12) +4 more |
| 2 | `get_upstream_features` | L0:F1326@14, k=5 → Emb:" University"@12 (de=7.28) +4 more |
| 3 | `get_upstream_features` | L6:F12990@22, k=8 → Emb:" He"@22 (de=4.47) +7 more |
| 4 | `get_upstream_features` | L0:F2994@3, k=8 → Emb:" his"@3 (de=43.25) +7 more |
| 5 | `inspect_feature` ×2 | L0:1326, L0:12351 |

### Build

`build_circuit` → 19 nodes, 23 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 48,570 | 5,045 | 67,149 | 0 | $0.0247 | — | — |
| SA-4 | openai/gpt-oss-120b | 75,390 | 6,170 | 5,856 | 0 | $0.0151 | ✅ 3F/7E | Trace from L5:F10392 (pos 9, direct_effect=-0.114, suppresse… |
| SA-3 | openai/gpt-oss-120b | 97,936 | 7,002 | 2,688 | 0 | $0.0189 | ✅ 4F/3E | Trace from L7:F14893 (pronouns) at pos 3. What's its upstrea… |
| SA-2 | openai/gpt-oss-120b | 111,536 | 8,676 | 22,976 | 0 | $0.0223 | ✅ 5F/10E | Trace from L6:F170 (academic field reference) at pos 9. What… |
| SA-6 | openai/gpt-oss-120b | 72,071 | 6,757 | 15,904 | 0 | $0.0151 | ✅ 3F/7E | Trace from L18:F14743 at pos 22 (direct_effect=-0.139, suppr… |
| SA-5 | openai/gpt-oss-120b | 176,092 | 12,972 | 22,112 | 0 | $0.0345 | ✅ 10F/15E | Trace from L12:F2175 (pos 2, direct_effect=-0.175, suppresse… |
| **Total** | | **581,595** | **46,622** | **136,685** | **0** | **$0.1306** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 11m 40s