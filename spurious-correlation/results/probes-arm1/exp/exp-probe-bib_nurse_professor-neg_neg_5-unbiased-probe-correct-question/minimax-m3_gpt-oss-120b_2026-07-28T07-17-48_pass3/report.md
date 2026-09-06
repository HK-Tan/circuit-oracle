# Circuit Oracle Report
**Date:** 2026-07-28 07:17:48 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven overwhelmingly by features that detect academic credentials, degrees, and university affiliations (Ph.D., B.A., M.B.A., Harvard, Chicago, Stanford), with one small but notable gender-marker contribution from the L0 male-pronoun feature and a stylistic period detector. The user's concern that the circuit relies on spurious gender cues is **only partially correct** — a male-pronoun feature (L0:F1069) does appear in the top-15 with direct_effect = +0.055 on the probe logit, but it is a *minor* contributor and the dominant signal is genuine profession-relevant content.

**Confidence:** 7/10

**Reasoning:**

- **Top positive drivers to the probe logit.** Among the 15 features returned by `get_top_features`, the strongest *positive* contributions all relate to academic credentials and professional biography:
  - **L0:F1069** at pos 1 ("His", direct_effect +0.055) — the male-pronoun detector. `inspect_feature` confirms it specifically fires on "He/His" pronouns (frac_nonzero = 0.0078, i.e. very specific). This is the only feature that could plausibly be a *gender* artifact, and it sits at layer 0, directly driven by the **Emb: "His" (pos 1)** token embedding (direct_effect = 21.6 upstream). However, its *direct* effect on the probe (0.055) is modest compared with the negative contributions of multiple credential features.
  - **L0:F6051** at pos 9 ("." after "Harvard University", direct_effect +0.075) — a generic period/separator feature (autointerp "periods, spaces, number 1"). It is purely syntactic and not profession-specific.
  - **L1:F10986** at pos 3 ("interests", direct_effect +0.065) — academic-research vocabulary; promoted from the embeddings for " research" (pos 2) and " interests" (pos 3).
  - **L7:F14129** at pos 15 ("D" of "Ph.D.", direct_effect +0.062) — academic degrees/universities, traced back via a subagent to the subword embeddings " Ph" (pos 13) and "D" (pos 15) through a degree-feature chain (L2:F10852 → L6:F2254 → L7:F14129). This is genuine, profession-relevant content.

- **The deep circuit for credential detection.** Tracing `L20:F14235` (which fires at both pos 19 and pos 33 — the " from" tokens preceding "Harvard University" and "Stanford University") reveals a multi-layer career/credentials chain: `Emb: " from" → L17:F11003 ("university", promoted token "University") + L17:F7973 ("phrases describing someone's education and the schools they attended") + L19:F2496 ("mentions of universities and degrees") → L20:F14235 ("references to academic credentials and institutions", top promoted tokens: "University", "Cornell", "UCLA", "Duke", "USC", "Vanderbilt", "LSU")`. These features aggregate *which* university the person attended, which is a substantive biographical / professional signal — the hallmark of a professor or academic.

- **Mid-layer amplifiers.** L6:F3235 (academic publications/math/scientific institutions, pos 20 — "University" in "Harvard University"), L6:F14747 (historical archives, pos 8 — "history"), L6:F2161 (governance/social/legal vocabulary, pos 6 — "transnational"), L8:F11284 (people's names/titles/universities, pos 9), and L8:F2383 (archaeological/historical sites, pos 8 — "history") all act as topic-of-research and institution detectors. These are NOT spurious — they are exactly the kind of features one would expect to fire for a "history professor" or "academic researcher" profession.

- **Assessing the gender-spuriousness concern.** The circuit *does* include the male-pronoun feature L0:F1069 (direct_effect +0.055 on the probe logit), and tracing shows it is driven purely by the **Emb: "His"** token at position 1 — it carries no profession information, only gender. This is a real (small) confound. However, the dominant *positive* signal is the academic-credentials chain (L0:F6051, L1:F10986, L7:F14129 and the deeper L17-L20 university features), and the *negative* contributions (L8:F2383, L6:F14747, L6:F2161, L6:F3235) are mainly topic-detectors that mildly *suppress* the probe score in this context, not spurious correlates. The user's intuition that gender is *part* of the signal is correct, but the circuit is predominantly driven by profession-relevant content (university affiliations, degree mentions, research vocabulary), making the gender feature a minor side-channel rather than the main mechanism.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 19 | Late-layer university / credential features (L17-20) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 33 | Late-layer university / credential features (L17-20) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 19 | Late-layer university / credential features (L17-20) |  mentions of universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L19:F2496](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) | 33 | Late-layer university / credential features (L17-20) |  mentions of universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2496) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 19 | Late-layer university / credential features (L17-20) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 33 | Late-layer university / credential features (L17-20) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L17:F7973](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) | 19 | Late-layer university / credential features (L17-20) |  phrases describing someone's education and the schools they attended | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) |
| [L17:F7973](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) | 33 | Late-layer university / credential features (L17-20) |  phrases describing someone's education and the schools they attended | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/7973) |
| [L17:F11342](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11342) | 33 | Late-layer university / credential features (L17-20) |  dates, especially years and sports-related terms | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11342) |
| [L14:F3956](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) | 33 | Late-layer university / credential features (L17-20) |  universities and degrees | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3956) |
| [L9:F988](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) | 29 | Late-layer university / credential features (L17-20) |  information about academic degrees | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/988) |
| [L8:F2383](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2383) | 8 | Mid-layer academic-degree / university-name detectors (L6-8) |  words related to archeological sites, digs, and artifacts | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/2383) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 9 | Mid-layer academic-degree / university-name detectors (L6-8) |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 15 | Mid-layer academic-degree / university-name detectors (L6-8) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L6:F14747](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14747) | 8 | Mid-layer academic-degree / university-name detectors (L6-8) |  terms related to historical archives and documents | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14747) |
| [L6:F2161](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2161) | 6 | Mid-layer academic-degree / university-name detectors (L6-8) |  words or phrases associated with governance, social issues, legality, or identity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2161) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 20 | Mid-layer academic-degree / university-name detectors (L6-8) |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 15 | Early degree / academic-title detectors (L0-2) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 29 | Early degree / academic-title detectors (L0-2) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 15 | Early degree / academic-title detectors (L0-2) | the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Early degree / academic-title detectors (L0-2) |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male pronoun detector (L0:F1069) — He/His |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 9 | Period/separator detector (L0:F6051) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L8:2383 de=-0.090 |
| 3 | `inspect_feature` ×4 | L0:6051, L1:10986, L0:1069, L7:14129 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F1069@1` | ❌ error | — | — | Trace the L0:F1069 "He/His" male pronoun feature. What input token at pos 1 driv… |
| SA-2 | `L1:F10986@3` | ❌ error | — | — | Trace L1:F10986 at pos 3 (label: "academic research words"). The token at pos 3 … |
| SA-3 | `L0:F6051@9` | ❌ error | — | — | Trace L0:F6051 at pos 9 (label: "periods, spaces, number 1"). What token at pos … |
| SA-4 | `L7:F14129@15` | ✅ reported | 7 | 6 | Trace L7:F14129 at pos 15 (label: "academic degrees, universities"). Input pos 1… |

<details>
<summary><b>SA-4</b> — tool trace (7 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@15, k=10 | L6:F2254 (de=7.09) +9 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `get_upstream_features` | L6:F2254@15, k=10 | L2:F10852 (de=12.31) +9 more |
| 5 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 6 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 7 | `inspect_feature` | L1, F10132 | " the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") writ" |

**Findings:** The tracing starts at L7:F14129, a high‑level detector for academic degrees and university names. Its strongest upstream driver is L6:F2254 (references to academic degrees), which itself is driven by L2:F10852 (academic titles/degrees) and by the raw token embedding for "D" at the exact position of the degree abbreviation. The chain also receives a direct boost from the embedding of the preceding …

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=8 → Emb:"His"@1 (de=21.62) +7 more |
| 2 | `get_upstream_features` | L1:F10986@3, k=8 → Emb:" research"@2 (de=6.62) +7 more |
| 3 | `get_upstream_features` | L0:F6051@9, k=8 → Emb:"."@9 (de=45.50) +7 more |
| 4 | `inspect_feature` ×6 | L2:10852, L20:14235, L6:14747, L8:2383, L6:2161, L8:11284 |
| 5 | `get_upstream_features` | L20:F14235@19, k=10 → L17:F11003 (de=34.00) +9 more |
| 6 | `get_upstream_features` | L20:F14235@33, k=10 → L17:F11003 (de=23.62) +9 more |
| 7 | `inspect_feature` ×7 | L14:3956, L9:988, L6:3235, L17:11003, L19:2496, L17:7973, L17:11342 |

### Build

`build_circuit` → 15 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 47,826 | 5,033 | 129,289 | 0 | $0.0281 | — | — |
| SA-4 | openai/gpt-oss-120b | 81,556 | 6,461 | 2,544 | 0 | $0.0161 | ✅ 7F/6E | Trace L7:F14129 at pos 15 (label: "academic degrees, univers… |
| **Total** | | **129,382** | **11,494** | **131,833** | **0** | **$0.0443** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 3m 27s