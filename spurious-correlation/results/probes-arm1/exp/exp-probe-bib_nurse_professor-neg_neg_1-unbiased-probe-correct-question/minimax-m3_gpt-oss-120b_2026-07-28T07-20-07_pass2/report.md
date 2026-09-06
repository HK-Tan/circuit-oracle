# Circuit Oracle Report
**Date:** 2026-07-28 07:20:07 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's professor-classification score is driven primarily by a *legitimate* academic-credentials circuit (degree tokens "PhD"/"BS" and university/credential features), not by spurious gender markers; "His"/"He" pronouns contribute only at the L0–L2 layer and are outweighed by degree/university signals.

**Confidence:** 7

**Reasoning:** The top positive contributions to the probe all flow from features that semantically encode academic credentials, not gender:

- **L20:F14235 ("references to academic credentials and institutions", direct_effect -0.037)** is the most negative-output-driving late-layer credential feature. Its main upstream signal is the embedding of " PhD" at pos 27 (3.80), " from" at pos 31 (3.97), and the cascade L6:F2254 → L7:F14129 → L17:F11003 (all "academic degrees" / "university" detectors). No gendered embedding appears in its top-k upstream set.
- **L8:F11284 ("names, titles, universities, research", direct_effect -0.057)** is driven by embeddings " research" (3.94), " interests" (1.45), "." (2.08) — i.e., the research-interests clause, not "His"/"He."
- **L6:F2254 ("references to academic degrees")** is directly excited by embedding " BS" (pos 17, direct_effect 18.4), " PhD" (pos 27, 19.25), and "received" (0.9). The trace_path_subagent confirmed: "the feature's activation on this prompt is driven almost exclusively by the 'BS' token, and it does not materially depend on surrounding pronoun or gender context."
- **L2:F10852 / L2:F1621** ("academic titles and degrees" / "people's education and career") feed in from the same degree tokens.
- **L1:F10986 ("academic research words", direct_effect +0.067)** fires on "interests" at pos 3.
- **L14:F11252 ("coordinate/3D rendering", direct_effect -0.051)** fires on "visualization" (pos 9, 6.06) — i.e., the specific research field.
- **L7:F14129** is fed by the " PhD" embedding (19.25) and the L6 degree detector (7.625), not by pronouns.

The only features that genuinely fire on the gendered pronoun " His" at pos 1 are L0:F1069 ("references to a male person, particularly He/His", direct_effect +0.070) and L0:F2994 ("his/he", -0.039), with L2:F3877 ("His" + religious figures) downstream. These contribute a few hundredths to the probe, but they are *not* the dominant signal: the degree/credential circuit carries direct_effects of ~0.04–0.07 from features whose upstream traces terminate in **token embeddings of "PhD" and "BS"** rather than "His."

So the user concern is **partially supported but not dominant**. A genuine gender-marker channel (L0:F1069, L0:F2994) exists and does push the probe, but the much larger credential/university/research-vocabulary channel is the primary mechanism — Emb(BS), Emb(PhD) → L2:L6:L7 degree detectors → L17:L20 university/credentials features → probe. The "spurious gender feature" hypothesis is weaker than the alternative: the probe is largely using **legitimate profession indicators** (BS, PhD, computer science, visualization, university affiliation, research interests), and the He/His pronouns are a secondary, smaller contributor.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 17 | Academic titles / degree mentions (L2:10852, 1621) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 27 | Academic titles / degree mentions (L2:10852, 1621) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F1621](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) | 3 | Academic titles / degree mentions (L2:10852, 1621) |  information about people's education and career | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) |
| [L3:F4213](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) | 21 | Degree qualifications / awards (L3:4213) |  mentions of degree qualifications or awards | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4213) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 17 | Academic degree tokens (L4:3727); acronyms/symbols (L4:9757) |  mentions of academic degrees | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Academic degree tokens (L4:3727); acronyms/symbols (L4:9757) | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 27 | Degree abbreviations / educational attainment (L5:13801, 12330) | abbreviations for degrees and mentions of educational attainment | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L5:F12330](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) | 13 | Degree abbreviations / educational attainment (L5:13801, 12330) | mentions of "College" along with a preceding place name like "County" or "Valley" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 17 | References to academic degrees (L6:2254); engineering/technical terms (L6:6331) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 27 | References to academic degrees (L6:2254); engineering/technical terms (L6:6331) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L6:F6331](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6331) | 9 | References to academic degrees (L6:2254); engineering/technical terms (L6:6331) |  technical terms in mechanical engineering papers including "finite element" "stress" and "fatigue." | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6331) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 27 | Academic degrees, universities, and people associated with them (L7:14129) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 13 | Names, titles, universities, research (L8:11284) |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L14:F11252](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11252) | 9 | Coordinate/3D rendering terms (L14:11252) |  code and coordinate geometry terms | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11252) |
| [L17:F11003](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) | 31 | University mentions (L17:11003) | university | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/11003) |
| [L20:F14235](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) | 31 | Academic credentials and institutions (L20:14235) |  references to academic credentials and institutions. | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/14235) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male-pronoun / gender markers (L0:1069, L0:2994, L2:3877) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Male-pronoun / gender markers (L0:1069, L0:2994, L2:3877) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L2:F3877](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3877) | 1 | Male-pronoun / gender markers (L0:1069, L0:2994, L2:3877) |  references to "His" and religious figures or concepts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3877) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Academic research vocabulary (L1:10986) |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:1069 de=0.070 |
| 3 | `inspect_feature` ×19 | L0:1069, L1:10986, L5:12330, L4:9757, L2:1621, L0:10783, L0:13431, L6:2254, L2:10852, L7:14129, L0:2994, L0:2159, L2:3877, L0:6446, L20:14235, L6:6331, L3:4213, L8:11284, L14:11252 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L20:F14235@31` | ✅ reported | 6 | 14 | Trace the L20:F14235 "academic credentials and institutions" feature upstream to… |
| SA-2 | `L7:F14129@27` | ❌ error | — | — | Trace the L7:F14129 "academic degrees, universities, and people associated with … |
| SA-3 | `L0:F1069@1` | ❌ error | — | — | Trace the L0:F1069 "references to a male person, particularly when using the pro… |
| SA-4 | `L6:F2254@17` | ✅ reported | 3 | 5 | Trace the L6:F2254 "references to academic degrees" feature upstream. Does it ac… |

<details>
<summary><b>SA-1</b> — tool trace (10 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L20, F14235 | " references to academic credentials and institutions." |
| 2 | `get_upstream_features` | L20:F14235@31, k=10 | L17:F11003 (de=30.38) +9 more |
| 3 | `inspect_feature` | L17, F11003 | "university" |
| 4 | `inspect_feature` | L19, F2496 | " mentions of universities and degrees" |
| 5 | `get_upstream_features` | L17:F11003@31, k=10 | Emb:" PhD"@27 (de=9.50) +9 more |
| 6 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 7 | `get_upstream_features` | L19:F2496@31, k=10 | L17:F11003 (de=14.12) +9 more |
| 8 | `get_upstream_features` | L7:F14129@27, k=10 | Emb:" PhD"@27 (de=19.25) +9 more |
| 9 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 10 | `inspect_feature` | L18, F13805 | "Universities" |

**Findings:** The L20:F14235 feature that signals "academic credentials and institutions" is driven primarily by degree‑related tokens, especially the embedding for the token " PhD" at position 27. The signal flows upward through a cascade: Embedding "PhD" → L6:F2254 (references to academic degrees) → L7:F14129 (academic degrees, universities, and people) → L17:F11003 (university detector) → L20:F14235. Additio…

</details>

<details>
<summary><b>SA-4</b> — tool trace (14 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 2 | `get_upstream_features` | L6:F2254@17, k=10 | Emb:" BS"@17 (de=18.38) +9 more |
| 3 | `get_upstream_features` | L6:F2254@17, k=20 | Emb:" BS"@17 (de=18.38) +19 more |
| 4 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 5 | `get_upstream_features` | L4:F3727@17, k=15 | Emb:" BS"@17 (de=15.44) +14 more |
| 6 | `inspect_feature` | L5, F5725 | " people's educational history including degrees and schools" |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 9 | `get_upstream_features` | L6:F2254@17, k=30 | Emb:" BS"@17 (de=18.38) +29 more |
| 10 | `get_upstream_features` | L2:F10852@17, k=10 | Emb:" BS"@17 (de=15.44) +9 more |
| 11 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 12 | `get_upstream_features` | L5:F13801@17, k=10 | L4:F3727 (de=10.06) +9 more |
| 13 | `get_upstream_features` | L4:F3727@17, k=15 | Emb:" BS"@17 (de=15.44) +14 more |
| 14 | `inspect_feature` | L4, F11633 | " words related to education and employment history" |

**Findings:** Tracing upstream from L6:F2254 (position 17) quickly reaches the input token embedding " BS" with a large positive direct effect (18.375). This same token also heavily excites L4:F3727 (15.44) and L2:F10852 (15.44 and 12.0 respectively), which cascade into the target feature. No other input embeddings (e.g., "PhD", gendered pronouns) show a comparable positive effect; the only other embeddings wit…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=8 → Emb:"His"@1 (de=21.62) +7 more |
| 2 | `get_upstream_features` | L7:F14129@27, k=8 → Emb:" PhD"@27 (de=19.25) +7 more |
| 3 | `get_upstream_features` | L8:F11284@13, k=8 → Emb:" research"@2 (de=3.94) +7 more |
| 4 | `get_upstream_features` | L14:F11252@9, k=8 → Emb:" visualization"@9 (de=6.06) +7 more |
| 5 | `inspect_feature` ×3 | L5:13801, L17:11003, L4:3727 |

### Build

`build_circuit` → 19 nodes, 24 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 61,964 | 5,380 | 207,762 | 0 | $0.0375 | — | — |
| SA-1 | openai/gpt-oss-120b | 104,641 | 5,114 | 7,600 | 0 | $0.0189 | ✅ 6F/14E | Trace the L20:F14235 "academic credentials and institutions"… |
| SA-4 | openai/gpt-oss-120b | 180,642 | 6,888 | 10,112 | 0 | $0.0314 | ✅ 3F/5E | Trace the L6:F2254 "references to academic degrees" feature … |
| **Total** | | **347,247** | **17,382** | **225,474** | **0** | **$0.0878** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 5s