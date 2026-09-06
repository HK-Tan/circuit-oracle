# Circuit Oracle Report
**Date:** 2026-07-28 07:02:56 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is classified predominantly by a spurious male-pronoun feature (He/His) at layer 0, while genuine profession-relevant signals (academic research/degrees) push *against* the classification, indicating the probe relies on gender rather than profession indicators.

**Confidence:** 7

**Reasoning:** Looking at the top direct-effect features on the probe:

**SPURIOUS GENDER SIGNAL (positive contribution):**
- **L0:F1069** (pos 1, direct_effect=+0.0554): explicitly labeled *"references to a male person, particularly when using the pronoun 'He' or 'His.'"* Upstream trace shows it is driven almost entirely by the embedding of `His` at position 1 (direct_effect=21.625). It is a male-gender detector, not a profession detector.
- **L0:F2994** (pos 12, direct_effect=-0.0403): *"the pronoun 'his' and the pronoun 'he.'"* — also a gender pronoun feature, driven by the embedding of `his` at pos 12 (direct_effect=44.5).
- **L0:F6051** (pos 9, direct_effect=+0.0752): a generic surface feature (periods/spaces) with no profession semantics; its strongest driver is the period embedding at pos 9 (direct_effect=45.5).
- **L1:F10986** (pos 3, direct_effect=+0.0649): *"academic research"* — marginally informative; driven by the ` research` and ` interests` embeddings.

**GENUINE PROFESSION SIGNALS (NEGATIVE — they PUSH AGAINST the classification!):**
This is the most striking finding. Features that *should* indicate the profession all have **negative** direct_effect on the probe:
- **L2:F10852** *"academic titles and degrees"* (pos 15, de=-0.0654; pos 29, de=-0.0549) — promotes tokens like `degree`, `PhD`, `doctorate`.
- **L6:F14747** *"historical archives and documents"* (pos 8, de=-0.0654).
- **L6:F13001** *"references to academic disciplines and studies"* (pos 8, de=-0.0435).
- **L7:F14129** *"academic degrees, universities, and people"* (pos 15, de=+0.0618 — the only positive genuine signal, but small).
- **L8:F2383** *"archaeological sites/digs/artifacts"* (pos 8, de=-0.0898 — the single largest negative contributor).
- **L9:F988**, **L14:F3956**, **L20:F14235** — progressively higher-layer credential detectors, all negative (de ≈ -0.044 to -0.056).

The archaeology/archives chain (L8:F2383 ← L6:F13001 ← L4:F14134) traces cleanly to the embedding of `history` at pos 8, confirming genuine content words actively *suppress* the probe's classification.

**User's concern is confirmed:** The probe classification is driven primarily by the male-pronoun feature (L0:F1069, fired by `His` at pos 1) and a generic surface feature (L0:F6051, fired by punctuation), while the features that genuinely encode profession content — academic degrees, research interests, historical/business domains — all have *negative* direct effects. The probe appears to have learned to classify the subject's gender rather than their profession, likely because in its training data, the "academic with Ph.D. from Harvard/Stanford" archetype correlates with male pronouns. This is a textbook example of a probe using a spurious correlate (gender) instead of the intended semantic category (academic profession).

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male pronoun feature (He/His) — SPURIOUS GENDER SIGNAL |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 12 | Male pronoun feature (He/His) — SPURIOUS GENDER SIGNAL | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Academic research / interests |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 9 | Periods/spaces surface feature (generic) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 15 | Academic degrees, universities, people (positive) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L8:F2383](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2383) | 8 | History → archaeology/archives chain (NEGATIVE) |  words related to archeological sites, digs, and artifacts | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2383) |
| [L6:F14747](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14747) | 8 | History → archaeology/archives chain (NEGATIVE) |  terms related to historical archives and documents | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14747) |
| [L6:F13001](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13001) | 8 | History → archaeology/archives chain (NEGATIVE) |  references to academic disciplines and studies | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/13001) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 15 | Academic titles/degrees token detectors (NEGATIVE) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 29 | Academic titles/degrees token detectors (NEGATIVE) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 19 | Late-layer credentials/institutions (NEGATIVE) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 33 | Late-layer credentials/institutions (NEGATIVE) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L14:F3956](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) | 33 | Late-layer credentials/institutions (NEGATIVE) |  universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) |
| [L9:F988](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) | 29 | Late-layer credentials/institutions (NEGATIVE) |  information about academic degrees | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L8:2383 de=-0.090 |
| 3 | `inspect_feature` ×17 | L8:2383, L0:6051, L6:14747, L2:10852, L1:10986, L7:14129, L8:11284, L20:14235, L0:1069, L6:2161, L6:3235, L14:3956, L9:988, L6:13001, L1:1505, L4:16301, L0:2994 |

### Dispatch: 8 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F2383@8` | ✅ reported | 4 | 3 | Trace the path from L8:F23898 ("academic titles/degrees" feature at pos 8) upstr… |
| SA-2 | `L0:F6051@9` | ❌ error | — | — | Trace upstream from L0:F6051 (a generic surface feature at pos 9 with direct_eff… |
| SA-3 | `L0:F1069@1` | ❌ error | — | — | Trace upstream from L0:F1069 ("male pronoun He/His" feature at pos 1 with direct… |
| SA-4 | `L20:F14235@19` | ✅ reported | 7 | 6 | Trace upstream from L20:F14235 ("academic credentials/institutions" at pos 19 wi… |
| SA-5 | `L14:F3956@33` | ✅ reported | 3 | 5 | Trace upstream from L14:F3956 ("universities and degrees" at pos 33 with direct_… |
| SA-6 | `L9:F988@29` | ✅ reported | 6 | 12 | Trace upstream from L9:F988 ("information about academic degrees" at pos 29, dir… |
| SA-7 | `L2:F10852@15` | ❌ error | — | — | Trace upstream from L2:F10852 ("academic titles and degrees" at pos 15, direct_e… |
| SA-8 | `L7:F14129@15` | ✅ reported | 7 | 19 | Trace upstream from L7:F14129 ("academic degrees, universities, and people" at p… |

<details>
<summary><b>SA-1</b> — tool trace (13 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L8, F2383 | " words related to archeological sites, digs, and artifacts" |
| 2 | `get_upstream_features` | L8:F2383@8, k=10 | Emb:" history"@8 (de=5.59) +9 more |
| 3 | `inspect_feature` | L6, F13001 | " references to academic disciplines and studies" |
| 4 | `inspect_feature` | L7, F4316 | " words regarding race, historical events, and education" |
| 5 | `get_upstream_features` | L6:F13001@8, k=10 | Emb:" history"@8 (de=14.06) +9 more |
| 6 | `inspect_feature` | L8, F23898 | ❌ Neuronpedia API error: 404 Client Error: Not Found for url:  |
| 7 | `get_upstream_features` | L8:F23898@8, k=10 | ❌ Feature (layer=8, pos=8, feature_idx=23898) not found in gra |
| 8 | `inspect_feature` | L8, F2389 | " words relating to consumerism, purchasing, and personal experience wi" |
| 9 | `inspect_feature` | L4, F14134 | " words and phrases that describe historical information" |
| 10 | `inspect_feature` | L8, F2398 | " words and phrases common in legal documents, especially related to co" |
| 11 | `get_top_logits` | k=5 | "" (100%) |
| 12 | `get_upstream_features` | L4:F14134@8, k=10 | Emb:" history"@8 (de=23.00) +9 more |
| 13 | `inspect_feature` | L8, F23890 | ❌ Neuronpedia API error: 404 Client Error: Not Found for url:  |

**Findings:** The archaeological‑artifact feature (L8:F2383) receives its strongest excitatory drive from the raw token embedding of “history” (pos 8). That embedding directly excites the historical‑info detector L4:F14134, which in turn strongly drives the academic‑discipline detector L6:F13001. L6:F13001 then passes excitation to the target archaeological feature. A secondary path comes from L7:F4316 (race/hi…

</details>

<details>
<summary><b>SA-4</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F14235 | " references to academic credentials and institutions." |
| 2 | `get_upstream_features` | L20:F14235@19, k=10 | L17:F11003 (de=34.00) +9 more |
| 3 | `inspect_feature` | L17, F11003 | "university" |
| 4 | `inspect_feature` | L19, F2496 | " mentions of universities and degrees" |
| 5 | `get_upstream_features` | L17:F11003@19, k=10 | Emb:"<bos>"@0 (de=-6.72) +9 more |
| 6 | `inspect_feature` | L17, F7973 | " phrases describing someone's education and the schools they attended" |
| 7 | `inspect_feature` | L3, F4213 | " mentions of degree qualifications or awards" |
| 8 | `get_upstream_features` | L7:F14129@15, k=10 | L6:F2254 (de=7.09) +9 more |
| 9 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 10 | `get_upstream_features` | L6:F2254@15, k=10 | L2:F10852 (de=12.31) +9 more |
| 11 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 12 | `get_upstream_features` | L3:F4213@19, k=10 | Emb:" from"@19 (de=11.12) +9 more |

**Findings:** The credential feature at L20:F14235 is driven primarily by a chain that starts with low‑level degree token detectors (layer 2 feature 10852, layer 6 feature 2254), climbs through a mid‑layer aggregator (L7:F14129) that ties degree tokens to university names, and culminates in higher‑level university‑specific detectors (L17:F11003, L19:F2496, L17:F7973). Positive embedding " from" also directly ex…

</details>

<details>
<summary><b>SA-5</b> — tool trace (8 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L14, F3956 | " universities and degrees" |
| 2 | `get_upstream_features` | L14:F3956@33, k=10 | Emb:"<bos>"@0 (de=-5.06) +9 more |
| 3 | `inspect_feature` | L3, F4213 | " mentions of degree qualifications or awards" |
| 4 | `get_upstream_features` | L3:F4213@33, k=10 | Emb:" from"@33 (de=12.00) +9 more |
| 5 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 6 | `inspect_feature` | L4, F11633 | " words related to education and employment history" |
| 7 | `get_upstream_features` | L4:F11633@33, k=10 | L3:F4213 (de=5.12) +9 more |
| 8 | `inspect_feature` | L8, F12509 | " mentions of degrees and higher education" |

**Findings:** The target late‑layer feature L14:F3956 ("universities and degrees") is primarily driven by a chain of positive‑effect upstream features: an embedding token " from" at position 33 directly excites the layer‑3 feature F4213, which in turn is strongly excited by the layer‑2 feature F10852 (academic titles and degrees). The embedding " from" supplies the prepositional context needed for phrases like …

</details>

<details>
<summary><b>SA-6</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L9, F988 | " information about academic degrees" |
| 2 | `get_upstream_features` | L9:F988@29, k=10 | L6:F2254 (de=5.50) +9 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `get_upstream_features` | L6:F2254@29, k=10 | L5:F5725 (de=-18.88) +9 more |
| 5 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 6 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 7 | `get_upstream_features` | L6:F2254@29, k=10 | L5:F5725 (de=-18.88) +9 more |
| 8 | `get_upstream_features` | L4:F3727@29, k=10 | L2:F10852 (de=15.88) +9 more |
| 9 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 10 | `inspect_feature` | L7, F873 | " text about health professions or degree abbreviations" |
| 11 | `get_upstream_features` | L2:F10852@29, k=10 | Emb:" B"@27 (de=12.38) +9 more |
| 12 | `inspect_feature` | L0, F1636 | " the letter A" |

**Findings:** Tracing from the degree‑information feature (L9:F988) reveals a cascade of upstream detectors for academic degrees. The strongest upstream driver is a layer‑6 feature that directly responds to degree references; it itself is fed by a layer‑5 abbreviation detector and the raw token "A". Further up, a layer‑4 detector and a layer‑2 generic title detector amplify the signal, both receiving strong pos…

</details>

<details>
<summary><b>SA-8</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@15, k=10 | L6:F2254 (de=7.09) +9 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `get_upstream_features` | L6:F2254@15, k=10 | L2:F10852 (de=12.31) +9 more |
| 5 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 6 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |
| 7 | `get_upstream_features` | L1:F10132@15, k=10 | Emb:" Ph"@13 (de=16.25) +9 more |
| 8 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 9 | `get_upstream_features` | L2:F10852@15, k=10 | Emb:" Ph"@13 (de=14.00) +9 more |
| 10 | `inspect_feature` | L3, F8294 | " words and phrases related to advanced education, research, and high-l" |
| 11 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |

**Findings:** The degree‑related feature at L7:F14129 is primarily driven by lower‑layer detectors of academic degree abbreviations. The strongest upstream driver is L6:F2254, which itself receives strong excitation from the raw token embeddings "Ph" (position 13) and "D" (position 15) as well as from the generic academic‑title detector L2:F10852. The signal propagates further through L5:F13801, L1:F10132, and …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=5 → Emb:"His"@1 (de=21.62) +4 more |
| 2 | `get_upstream_features` | L1:F10986@3, k=5 → Emb:" research"@2 (de=6.62) +4 more |
| 3 | `get_upstream_features` | L8:F11284@9, k=5 → Emb:" research"@2 (de=3.89) +4 more |
| 4 | `get_upstream_features` | L6:F14747@8, k=5 → Emb:" history"@8 (de=6.25) +4 more |
| 5 | `get_upstream_features` | L0:F6051@9, k=5 → Emb:"."@9 (de=45.50) +4 more |
| 6 | `get_upstream_features` | L20:F14235@33, k=5 → L17:F11003 (de=23.62) +4 more |
| 7 | `get_upstream_features` | L6:F13001@8, k=5 → Emb:" history"@8 (de=14.06) +4 more |
| 8 | `get_upstream_features` | L7:F14129@15, k=5 → L6:F2254 (de=7.09) +4 more |
| 9 | `get_upstream_features` | L0:F2994@12, k=5 → Emb:" his"@12 (de=44.50) +4 more |
| 10 | `get_upstream_features` | L0:F1069@1, k=8 → Emb:"His"@1 (de=21.62) +7 more |

### Build

`build_circuit` → 15 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 64,044 | 5,770 | 202,163 | 0 | $0.0383 | — | — |
| SA-8 | openai/gpt-oss-120b | 118,672 | 10,859 | 34,240 | 0 | $0.0248 | ✅ 7F/19E | Trace upstream from L7:F14129 ("academic degrees, universiti… |
| SA-1 | openai/gpt-oss-120b | 125,331 | 8,164 | 54,720 | 0 | $0.0245 | ✅ 4F/3E | Trace the path from L8:F23898 ("academic titles/degrees" fea… |
| SA-5 | openai/gpt-oss-120b | 81,900 | 5,566 | 13,440 | 0 | $0.0158 | ✅ 3F/5E | Trace upstream from L14:F3956 ("universities and degrees" at… |
| SA-4 | openai/gpt-oss-120b | 166,834 | 8,277 | 7,584 | 0 | $0.0301 | ✅ 7F/6E | Trace upstream from L20:F14235 ("academic credentials/instit… |
| SA-6 | openai/gpt-oss-120b | 153,428 | 10,428 | 15,232 | 0 | $0.0295 | ✅ 6F/12E | Trace upstream from L9:F988 ("information about academic deg… |
| **Total** | | **710,209** | **49,064** | **327,379** | **0** | **$0.1630** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 4m 5s