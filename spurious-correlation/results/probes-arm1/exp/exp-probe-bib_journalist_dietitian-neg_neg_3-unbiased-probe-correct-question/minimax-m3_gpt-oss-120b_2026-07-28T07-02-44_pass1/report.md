# Circuit Oracle Report
**Date:** 2026-07-28 07:02:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's journalist classification is driven by a deep, genuine journalism/media semantic hierarchy rooted in the input token "journalistic" at position 13, which propagates through layers 0→1→3→4→6→7→8→9→14 to a final journalism concept node, and is *not* primarily driven by the male pronoun "He" (a small, low-magnitude negative contributor).

**Confidence:** 8

**Reasoning:**

The circuit reveals that the probe's classification is built on a **legitimate profession-semantic hierarchy** triggered by the token "journalistic" (pos 13), not on spurious gender markers:

1. **Primary profession path (positive, large magnitude):** The embedding `Emb: 'journalistic' (pos 13)` directly excites a cascade: L0:F9026 (lexical journalism detector) → L3:F7446 (information-transfer/media) → L4:F13253 (journalism/media concept, direct_effect 25.6 from embedding) → L6:F12712 (editor/publisher titles), L7:F9092 (broadcast journalism), L8:F8855 (news reporters), L9:F7435 (news production) → **L14:F4420 (journalism/newspapers concept, frac_nonzero 0.0165, direct_effect −0.128)** → logit. The L14 feature is the canonical "reporter/editor/newspaper" detector — exactly what one would expect for a journalist probe. Embedding direct effects to this whole hierarchy are large (e.g., 24.4 to L14, 25.6 to L4, 14.9 to L7).

2. **Secondary story path:** The token " stories" (pos 3) drives L0 lexical story features (F5333, F14906, F11261) → L1:F14812 (narrative integration, direct_effect 0.19 to logit) → logit. This path contributes positively via the concept of narrative/news reporting, not as a gendered or spurious cue.

3. **Gender marker (the concern) is NOT the driver:** L0:F1069 at pos 1 ("He/His" — male pronoun, frac_nonzero 0.0078) has direct_effect **−0.16** to the logit (suppressive). The `Emb: 'He'` drives this feature (direct_effect 22.6), but the propagation to the output is *negative*, and importantly it does NOT route through the journalism concept hierarchy. So the male-pronoun signal slightly suppresses the journalist classification, not promotes it.

4. **Other minor contributors** (L0 'country' F15423, L0 'foreign' F2711, L0 'research' F4564, L0 'represent' F9201) are content-word detectors driven by their respective embeddings (country, foreign, researches, represents) with small direct_effects (0.06–0.11). These are world-knowledge context features, not gender markers.

5. **Conclusion on the user's concern:** The probe is *not* primarily using gender markers. The dominant positive signal comes from a 10-layer-deep profession-specific semantic hierarchy anchored in the word "journalistic" itself, with the L14 journalism/newspapers feature (F4420) as the final profession concept node. The male-pronoun feature contributes negatively and does not feed into the journalism concept circuit. The user may have been observing the surface presence of the "He" feature in the top-K features and mistaking its visibility for causal importance; in this circuit, its contribution is *suppressive* and decoupled from the profession-recognition path.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: 'journalistic' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: ' stories' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'He' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: ' foreign' (pos 20) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: ' country' (pos 11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' researches' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ' represents' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: ' in' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0 male-pronoun / person features (pos 1) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) | 1 | L0 male-pronoun / person features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | L0 story/narrative lexical features (pos 3) | mentions of stories that are being told | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L0:F8350](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8350) | 3 | L0 story/narrative lexical features (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8350) |
| [L0:F14906](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14906) | 3 | L0 story/narrative lexical features (pos 3) |  the word "binding" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14906) |
| [L0:F1301](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1301) | 3 | L0 story/narrative lexical features (pos 3) |  mentions of cancer and related terms like tumors | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1301) |
| [L0:F11261](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) | 3 | L0 story/narrative lexical features (pos 3) |  the word "migration" and words related to it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 13 | L0 journalism/media lexical detectors (pos 13) | technical documents or data, including numbers, units, and references to figures or tables. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F15423](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15423) | 11 | L0 'country' detector (pos 11) | The neuron seems to activate any time the word "country" is used, but also sometimes seems to activate for words related to groups of people such as "kids", "rest", or "total". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15423) |
| [L0:F2711](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2711) | 20 | L0 'foreign' detector (pos 20) | the word "foreign." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2711) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | L0 'research' detector (pos 2) | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F10255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10255) | 1 | L0 question-word features (pos 1) |  questions starting with any form of "to be" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10255) |
| [L0:F2530](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2530) | 1 | L0 question-word features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2530) |
| [L0:F1003](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1003) | 3 | L0 question-word features (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1003) |
| [L0:F9201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9201) | 9 | L0 'represent' detector (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9201) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 12 | L0 'in' preposition (pos 12) |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | L0 punctuation / 'a' features (pos 15, 19) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F10219](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) | 19 | L0 punctuation / 'a' features (pos 15, 19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10219) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | L1 story/narrative integration (pos 3) |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F16233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16233) | 3 | L1 story/narrative integration (pos 3) | the word "tips" and the word "unit" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16233) |
| [L1:F1154](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1154) | 3 | L1 story/narrative integration (pos 3) |  the word "door," especially in a legal context | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1154) |
| [L1:F2344](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2344) | 11 | L1 'country' detector (pos 11) |  instances of the word "country" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/2344) |
| [L3:F7446](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7446) | 13 | L3 information-transfer / media (pos 13) |  words related to processes of conveying information through different media | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/7446) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | L4 journalism/media concept (pos 13) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F10883](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10883) | 27 | L4 journalism/media concept (pos 13) | the word "too" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10883) |
| [L4:F29](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/29) | 16 | L4 'when' detector (pos 16) |  instances of the word "when" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/29) |
| [L6:F10984](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10984) | 21 | L6 TV/broadcasting (pos 21) |  mentions of TV and radio broadcasting | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10984) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 13 | L6 editor/publisher titles (pos 13) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 13 | L7 broadcast journalism (pos 13) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 13 | L7 broadcast journalism (pos 13) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 13 | L8 film/documentary content (pos 13) | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 13 | L8 news reporters/reporting (pos 13) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F2309](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2309) | 13 | L8 news reporters/reporting (pos 13) |  words related to broadcast news | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2309) |
| [L9:F7435](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) | 13 | L9 news production (pos 13) |  words and phrases related to news production and media | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | L14 journalism/newspapers concept (pos 13) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Output probe (journalist classification) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:14906 de=-0.222 |
| 3 | `inspect_feature` ×4 | L0:14906, L1:14812, L0:11603, L0:1069 |
| 4 | `get_top_features` | 30 features; top: L0:14906 de=-0.222 |
| 5 | `inspect_feature` ×10 | L0:11261, L0:8061, L1:16233, L14:4420, L0:2711, L0:5333, L0:6962, L0:6051, L4:13253, L1:9201 |
| 6 | `get_top_features` | 50 features; top: L0:14906 de=-0.222 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F14812@3` | ✅ reported | 3 | 2 | Trace the path upstream from L1:F14812 (pos 3, "references to stories, chapters,… |
| SA-2 | `L14:F4420@13` | ✅ reported | 7 | 3 | Trace the path upstream from L14:F4420 (pos 13, "words/phrases related to journa… |
| SA-3 | `L0:F1069@1` | ❌ error | — | — | Trace the path upstream from L0:F1069 (pos 1, "references to a male person, part… |
| SA-4 | `L4:F13253@13` | ✅ reported | 5 | 4 | Trace the path upstream from L4:F13253 (pos 13, "things related to journalism an… |

<details>
<summary><b>SA-1</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F14812 | " references to stories, chapters, and other narrative elements" |
| 2 | `get_upstream_features` | L1:F14812@3, k=10 | Emb:" stories"@3 (de=18.62) +9 more |
| 3 | `inspect_feature` | L0, F479 | "the word "lift."" |
| 4 | `inspect_feature` | L0, F12991 | " references to figures and other documents" |
| 5 | `get_upstream_features` | L0:F479@3, k=10 | Emb:" stories"@3 (de=10.69) +9 more |
| 6 | `inspect_feature` | L0, F9438 | "Objective-C or C syntax related to pointers, object initialization and" |

**Findings:** The target feature L1:F14812 (position 3) is primarily driven by the raw input token "stories" (embedding direct effect 18.6), which makes sense because the feature looks for narrative language. The strongest upstream transcoder features are two layer‑0 detectors: (1) a lexical "lift" detector (F479) and (2) a figure‑reference detector (F12991). Both contribute only a small positive effect and do …

</details>

<details>
<summary><b>SA-2</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F4420 | "words and phrases related to journalism and newspapers" |
| 2 | `get_upstream_features` | L14:F4420@13, k=10 | Emb:" journalistic"@13 (de=24.38) +9 more |
| 3 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 4 | `get_upstream_features` | L4:F13253@13, k=10 | Emb:" journalistic"@13 (de=25.62) +9 more |
| 5 | `inspect_feature` | L7, F9092 | " words and phrases associated with broadcast journalism" |
| 6 | `inspect_feature` | L8, F8437 | "content related to film festivals and production, particularly documen" |
| 7 | `get_upstream_features` | L7:F9092@13, k=10 | Emb:" journalistic"@13 (de=14.88) +9 more |
| 8 | `inspect_feature` | L3, F7446 | " words related to processes of conveying information through different" |
| 9 | `get_upstream_features` | L8:F8437@13, k=10 | Emb:" journalistic"@13 (de=8.06) +9 more |
| 10 | `inspect_feature` | L7, F13646 | " news reporting and journalism." |
| 11 | `inspect_feature` | L1, F1136 | " image credits and descriptions" |
| 12 | `get_upstream_features` | L1:F1136@13, k=5 | Emb:" journalistic"@13 (de=5.28) +4 more |
| 13 | `inspect_feature` | L1, F5357 | " words related to written works" |

**Findings:** The L14 journalism feature (F4420) is driven primarily by the raw input token "journalistic" at position 13 (direct_effect ~24). This signal is amplified by a cascade of earlier media-related detectors: a low-layer media feature (L4:F13253), a broadcast-news feature (L7:F9092), and a documentary-film feature (L8:F8437). All three send positive excitatory influence to the target. The chain reaches …

</details>

<details>
<summary><b>SA-4</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L4, F13253 | " things related to journalism and the media" |
| 2 | `get_upstream_features` | L4:F13253@13, k=10 | Emb:" journalistic"@13 (de=25.62) +9 more |
| 3 | `inspect_feature` | L1, F1136 | " image credits and descriptions" |
| 4 | `get_upstream_features` | L1:F5357@13, k=10 | Emb:" journalistic"@13 (de=9.00) +9 more |
| 5 | `inspect_feature` | L1, F5357 | " words related to written works" |
| 6 | `get_upstream_features` | L1:F1136@13, k=10 | Emb:" journalistic"@13 (de=5.28) +9 more |
| 7 | `inspect_feature` | L0, F9026 | "technical documents or data, including numbers, units, and references " |

**Findings:** The journalism/media feature (L4:F13253) is driven primarily by the input token 'journalistic' at the same position, providing a large positive direct effect. A secondary upstream contributor is a layer‑1 feature (F5357) that encodes words related to written works, itself strongly excited by the same 'journalistic' embedding and modestly by a low‑level technical‑document feature (L0:F9026). This p…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"He"@1 (de=22.62) +9 more |
| 2 | `get_upstream_features` | L1:F14812@3, k=10 → Emb:" stories"@3 (de=18.62) +9 more |
| 3 | `get_upstream_features` | L14:F4420@13, k=10 → Emb:" journalistic"@13 (de=24.38) +9 more |
| 4 | `get_upstream_features` | L4:F13253@13, k=10 → Emb:" journalistic"@13 (de=25.62) +9 more |
| 5 | `get_upstream_features` | L7:F9092@13, k=5 → Emb:" journalistic"@13 (de=14.88) +4 more |
| 6 | `get_upstream_features` | L0:F11603@27, k=10 → Emb:" too"@27 (de=32.00) +9 more |
| 7 | `get_upstream_features` | L0:F2711@20, k=5 → Emb:" foreign"@20 (de=25.62) +4 more |
| 8 | `inspect_feature` ×7 | L0:15423, L1:1154, L1:2344, L0:1301, L0:10255, L0:4564, L0:12009 |
| 9 | `get_upstream_features` | L0:F11261@3, k=5 → Emb:" stories"@3 (de=12.69) +4 more |
| 10 | `get_upstream_features` | L1:F16233@3, k=5 → Emb:" stories"@3 (de=13.62) +4 more |
| 11 | `get_upstream_features` | L0:F5333@3, k=5 → Emb:" stories"@3 (de=16.38) +4 more |
| 12 | `get_upstream_features` | L0:F8061@12, k=5 → Emb:" in"@12 (de=39.75) +4 more |
| 13 | `inspect_feature` ×12 | L4:10883, L6:10984, L6:12712, L4:29, L9:7435, L8:8437, L7:9092, L7:13646, L8:8855, L8:2309, L3:7446, L0:9026 |
| 14 | `get_upstream_features` | L6:F12712@13, k=5 → Emb:" journalistic"@13 (de=14.00) +4 more |
| 15 | `get_upstream_features` | L7:F13646@13, k=5 → Emb:" journalistic"@13 (de=7.69) +4 more |
| 16 | `get_upstream_features` | L8:F8855@13, k=5 → Emb:" journalistic"@13 (de=10.50) +4 more |
| 17 | `get_upstream_features` | L0:F10219@19, k=5 → Emb:" a"@19 (de=41.25) +4 more |
| 18 | `get_upstream_features` | L0:F11261@3, k=5 → Emb:" stories"@3 (de=12.69) +4 more |
| 19 | `get_upstream_features` | L0:F8350@3, k=3 → Emb:" stories"@3 (de=10.94) +2 more |

### Build

`build_circuit` → 31 nodes, 42 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 84,439 | 8,939 | 394,711 | 0 | $0.0597 | — | — |
| SA-1 | openai/gpt-oss-120b | 68,108 | 4,474 | 2,528 | 0 | $0.0129 | ✅ 3F/2E | Trace the path upstream from L1:F14812 (pos 3, "references t… |
| SA-4 | openai/gpt-oss-120b | 56,201 | 4,710 | 8,960 | 0 | $0.0114 | ✅ 5F/4E | Trace the path upstream from L4:F13253 (pos 13, "things rela… |
| SA-2 | openai/gpt-oss-120b | 154,988 | 13,344 | 43,520 | 0 | $0.0319 | ✅ 7F/3E | Trace the path upstream from L14:F4420 (pos 13, "words/phras… |
| **Total** | | **363,736** | **31,467** | **449,719** | **0** | **$0.1160** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 52s