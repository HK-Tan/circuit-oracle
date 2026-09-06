# Circuit Oracle Report
**Date:** 2026-07-28 07:23:26 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is classified positively primarily because the model detects academic/biographical credentials (PhD, M.B.A., B.A., universities) and historical research content, but it is *also* independently driven by a male-pronoun feature ("His"/"He") — confirming the user concern that gender markers contribute alongside genuine profession indicators.

**Confidence:** 7

**Reasoning:**

The attribution graph for this probe direction reveals **three parallel pathways** feeding into the output node at layer 26:

**Pathway 1 — Academic credentials (the dominant, legitimate signal):** This is the strongest, most explicit signal. The probe is driven by a tightly linked stack of "education/credentials" features that originates at the literal tokens "Ph.D." (pos 13–15), "B.A." (pos 27–29), and "from" before each university name (pos 19, 33). The signal flows: 
- `emb_ph` + `emb_D` (pos 13, 15) → **L1:F10132** (Ph.D. "D" token) → **L2:F10852** (academic titles & degrees, frac_nonzero 0.008) → **L5:F13801** (degree abbreviations) → **L6:F2254** (references to academic degrees) and **L7:F14129** (academic degrees & universities) → **L9:F988** (info about academic degrees) → **L14:F3956** (universities & degrees) → **L18:F1714** (academic publications/biographies), **L18:F13264** (earning advanced degrees), **L18:F13805** (universities), **L17:F11003** (university) → **L19:F2496** (university education) → **L20:F14235** (academic credentials & institutions; promoted tokens "▁UC", "▁Cornell", "▁University", "▁UCLA"… — strong university-evidence) and **L21:F194** (people's education info) → output.

This pathway is **genuine**: the features fire on the actual education tokens and on the bio's structure (PhD/MBA/BA from named universities). The probe correctly identifies "academic researcher with history PhD + business/economics BA + MBA" as a professor-style credential pattern.

**Pathway 2 — Humanities/history field (legitimate but field-level, not profession-level):** A second stream from `emb_history` (pos 8) → **L1:F1505** ("certified" generic, but in this context the "history" sub-token) → **L6:F170** (academic fields, especially humanities) and **L6:F14747** (historical archives/documents) → **L14:F2379** (historical preservation/societies) → **L18:F1714** → output. This detects "this is a humanities field bio", which contributes positively to the "academic" probe.

**Pathway 3 — Gender/spurious signal (user's concern is validated):** The feature **L0:F1069** at pos 1, with direct_effect = +0.0554, fires on the embedding node **`emb_his`** ("His", pos 1) with direct_effect = 21.6. The autointerp label is "references to a male person, particularly when using the pronoun 'He' or 'His'." frac_nonzero = 0.0078 (specific). This feature connects **directly to the probe output** with no intermediate profession/education context. Similarly, **L0:F2994** at pos 12 ("his" pronoun again) and **L1:F3795** (for-profit companies) appear. The male-pronoun feature is a shallow, generic, surface-level cue — it does not pass through any education/credential features; it bypasses the academic-content pathway entirely.

**Why the user's concern is valid but partial:** The graph shows that the probe is *not* solely relying on gender. The education-credentials pathway (Pathway 1) is large in absolute direct-effect and has many more nodes (the entire degree/university stack). However, **L0:F1069 is the 9th-largest direct contributor** and it activates on a single male-pronoun token. It is a real, distinct channel — meaning the probe is *additionally* tracking gender. Replacing "He/His" with "She/Her" in this identical bio would reduce L0:F1069's contribution while leaving the education pathway intact, so the probe's score would shift. The probe thus uses **spurious gender features as a real but non-dominant signal** alongside substantive profession indicators (degrees, universities, humanities field). This is a real fairness/reliability concern even though the profession signal is present and stronger in absolute magnitude.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male pronoun feature (L0:F1069 pos 1) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 12 | Male pronoun feature (L0:F1069 pos 1) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Word 'research' (L0:F4564 pos 2) | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Academic research words (L1:F10986 pos 3) |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L1:F1505](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1505) | 8 | Word 'history'/'certified' (L1:F1505 pos 8) | the word "certified" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1505) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 15 | PhD abbreviation 'D' token (L1:F10132 pos 15) |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 15 | Academic titles & degrees (L2:F10852 pos 15,29) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 29 | Academic titles & degrees (L2:F10852 pos 15,29) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 15 | Degree abbreviations (L5:F13801 pos 15) | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 15 | References to academic degrees (L6:F2254 pos 15,29) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 29 | References to academic degrees (L6:F2254 pos 15,29) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 15 | Academic degrees & universities (L7:F14129 pos 15) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L5:F5725](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) | 29 | People's educational history (L5:F5725 pos 29) |  people's educational history including degrees and schools | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/5725) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 8 | References to academic fields, humanities (L6:F170 pos 8,18) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 18 | References to academic fields, humanities (L6:F170 pos 8,18) |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F13001](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13001) | 8 | References to academic fields, humanities (L6:F170 pos 8,18) |  references to academic disciplines and studies | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13001) |
| [L14:F2379](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2379) | 8 | Historical preservation/societies (L14:F2379 pos 8) |  terms related to historical preservation and societies | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2379) |
| [L9:F988](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) | 15 | Information about academic degrees (L9:F988 pos 15,29) |  information about academic degrees | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) |
| [L9:F988](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) | 29 | Information about academic degrees (L9:F988 pos 15,29) |  information about academic degrees | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) |
| [L6:F14747](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14747) | 8 | Historical archives & documents (L6:F14747 pos 8) |  terms related to historical archives and documents | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14747) |
| [L14:F3956](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) | 19 | Universities & degrees (L14:F3956 pos 19,33) |  universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) |
| [L14:F3956](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) | 33 | Universities & degrees (L14:F3956 pos 19,33) |  universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) |
| [L17:F4013](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/4013) | 15 | Advanced academic degrees (L17:F4013 pos 15) |  advanced academic degrees | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/4013) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 19 | University (L17:F11003 pos 19,33) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 33 | University (L17:F11003 pos 19,33) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L18:F1714](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/1714) | 17 | Academic publications/biographies, fields & degrees (L18:F1714 pos 17,31) | academic publications or biographies, focusing on fields of study, departments, and degrees | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/1714) |
| [L18:F1714](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/1714) | 31 | Academic publications/biographies, fields & degrees (L18:F1714 pos 17,31) | academic publications or biographies, focusing on fields of study, departments, and degrees | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/1714) |
| [L18:F13805](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13805) | 19 | Universities (L18:F13805 pos 19,33) | Universities | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13805) |
| [L18:F13805](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13805) | 33 | Universities (L18:F13805 pos 19,33) | Universities | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13805) |
| [L18:F13264](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13264) | 19 | Earning advanced academic degrees (L18:F13264 pos 19) |  words and phrases associated with earning advanced academic degrees like PhD and completing doctoral dissertations | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13264) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 19 | University education (L19:F2496 pos 19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 19 | Academic credentials & institutions (L20:F14235 pos 19,33,46) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 33 | Academic credentials & institutions (L20:F14235 pos 19,33,46) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 46 | Academic credentials & institutions (L20:F14235 pos 19,33,46) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L21:F194](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/194) | 33 | People's education info (L21:F194 pos 33) | information about people's education | [view](https://neuronpedia.org/gemma-2-2b/21-gemmascope-transcoder-16k/194) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token ' probe' is not one of the top-k next-token candidates |
| 3 | `get_top_features` | 20 features; top: L8:2383 de=-0.090 |
| 4 | `inspect_feature` ×4 | L0:6051, L1:10986, L0:1069, L1:1505 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F1069@1` | ❌ error | — | — | Trace L0:F1069 (male pronoun "He/His" feature) all the way upstream. Determine i… |
| SA-2 | `L1:F10986@3` | ❌ error | — | — | Trace L1:F10986 (academic research feature at pos 3, likely "research interests"… |
| SA-3 | `L0:F6051@9` | ❌ error | — | — | Trace L0:F6051 (periods/spaces/1 feature at pos 9) upstream. This is the stronge… |
| SA-4 | `L1:F1505@8` | ❌ error | — | — | Trace L1:F1505 ("certified" feature at pos 8) upstream. Determine why this is fi… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"His"@1 (de=21.62) +9 more |
| 2 | `get_upstream_features` | L1:F10986@3, k=10 → Emb:" research"@2 (de=6.62) +9 more |
| 3 | `get_upstream_features` | L0:F6051@9, k=10 → Emb:"."@9 (de=45.50) +9 more |
| 4 | `get_upstream_features` | L1:F1505@8, k=10 → Emb:" history"@8 (de=10.75) +9 more |
| 5 | `get_top_features` | token="", k=40 → 40 features; top: L8:2383 de=-0.090 |
| 6 | `inspect_feature` ×15 | L8:2383, L6:14747, L2:10852, L7:14129, L8:11284, L20:14235, L6:2161, L6:3235, L14:3956, L9:988, L4:9757, L9:228, L6:170, L5:5725, L0:4564 |
| 7 | `get_upstream_features` | L20:F14235@19, k=8 → L17:F11003 (de=34.00) +7 more |
| 8 | `get_upstream_features` | L7:F14129@15, k=8 → L6:F2254 (de=7.09) +7 more |
| 9 | `inspect_feature` ×3 | L0:2994, L0:13431, L1:3795 |
| 10 | `get_upstream_features` | L17:F11003@19, k=8 → Emb:"<bos>"@0 (de=-6.72) +7 more |
| 11 | `get_upstream_features` | L19:F2496@19, k=8 → L17:F11003 (de=15.69) +7 more |
| 12 | `get_upstream_features` | L1:F10132@15, k=8 → Emb:" Ph"@13 (de=16.25) +7 more |
| 13 | `inspect_feature` ×13 | L6:2254, L5:13801, L18:1714, L17:4013, L17:11003, L21:194, L6:13001, L4:16301, L6:10459, L14:2379, L9:14876, L4:6047, L6:1069 |
| 14 | `get_upstream_features` | L9:F988@29, k=8 → L6:F2254 (de=5.50) +7 more |
| 15 | `get_upstream_features` | L14:F3956@33, k=8 → Emb:"<bos>"@0 (de=-5.06) +7 more |
| 16 | `get_upstream_features` | L2:F10852@29, k=8 → Emb:" B"@27 (de=12.38) +7 more |
| 17 | `inspect_feature` ×3 | L1:10132, L18:13264, L18:13805 |
| 18 | `get_upstream_features` | L9:F988@15, k=8 → L6:F2254 (de=5.41) +7 more |
| 19 | `get_upstream_features` | L7:F14129@19, k=8 → L5:F11028 (de=4.56) +7 more |
| 20 | `get_upstream_features` | L2:F10852@15, k=8 → Emb:" Ph"@13 (de=14.00) +7 more |
| 21 | `get_upstream_features` | L18:F1714@17, k=8 → L17:F16360 (de=7.34) +7 more |
| 22 | `get_upstream_features` | L17:F11003@31, k=8 → ❌ Feature (layer=17, feature_idx=11003) not found at pos=31. T |
| 23 | `get_upstream_features` | L21:F194@33, k=8 → L20:F14235 (de=28.38) +7 more |

### Build

`build_circuit` → 37 nodes, 35 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 85,092 | 8,765 | 342,403 | 0 | $0.0566 | — | — |
| **Total** | | **85,092** | **8,765** | **342,403** | **0** | **$0.0566** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 46s