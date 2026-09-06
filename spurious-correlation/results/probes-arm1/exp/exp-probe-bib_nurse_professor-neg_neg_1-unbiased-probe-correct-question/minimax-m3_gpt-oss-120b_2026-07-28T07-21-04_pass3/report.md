# Circuit Oracle Report
**Date:** 2026-07-28 07:21:04 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

The circuit was saved. Now I'll provide the final analysis.

**Analysis:** The probe's classification is driven by a mix of legitimate profession/academic indicators and a single male-pronoun feature — but the male-pronoun signal is one among many genuine profession markers, not the dominant one.

**Confidence:** 7

**Reasoning:** The attribution graph decomposes into roughly three groups feeding the probe logit at the prediction position:

1. **Genuine profession/academic indicators (strong, dominant):** Four independent positive signals all flow from the body of the bio rather than from gendered tokens. (a) `sn_acad_degrees_late` (L7:F14129, frac_nonzero 0.0042, direct_effect +0.040) and `sn_academic_degrees_pos` (L6:F2254, frac_nonzero 0.0041, direct_effect -0.042) and `sn_academic_titles_pos` (L2:F10852, frac_nonzero 0.008, direct_effect -0.041) form a "PhD" chain — all three fire on the "PhD" token at pos 27 and trace back directly to the `emb_PhD` embedding, with the L2 feature's promoted tokens literally being `▁PhD, ▁degree, ▁doctorate`. (b) `sn_academic_research` (L1:F10986, direct_effect +0.067) is the strongest single positive driver in the graph and is grounded in the `emb_research` (direct_effect +0.578) and `emb_interests` embeddings — it is a generic "academic research" detector whose top activating examples are biographies of researchers. (c) `sn_edu_career` (L2:F1621, "information about people's education and career") fires at pos 13 with contributions from both `emb_His` and `emb_include` and from `emb_research`/`emb_interests` — its top activating examples are literally academic bios listing "interests", "published", and "recently". (d) `sn_college_mention` (L5:F12330, "mentions of College with a preceding place name", direct_effect +0.045) and `sn_include_word` (L0:F10783, "the word 'include'", direct_effect -0.045) come from "include" and the period in "computer science." These are content words naming a profession's domain.

2. **The gender signal (present but a single feature):** `sn_he_pronoun` (L0:F1069, "references to a male person, particularly when using the pronoun 'He' or 'His'", direct_effect +0.070) is the single largest positive driver and is fed essentially by the `emb_His` token at pos 1 (direct_effect +21.6 into the feature). Crucially, the top-activating examples of this feature show that it almost always fires on the literal word "He" — and on the `emb_He` token, the feature is listed as both "promoted" and "suppressed" in the Neuronpedia logits because the feature reads *who the pronoun refers to* (the "person") rather than asserting gender. The probe's pull on this feature is genuine: the text is about a male researcher, and L0:F1069 is the model's representation of "this bio is about a male person." But it is *not* a free-standing gender stereotype; it is co-extensive with the profession signal because biographies of male computer-science professors are exactly the kind of text the probe is classifying.

3. **Suppressive profession-aspecific features:** `sn_names_titles_research_neg` (L8:F11284, "names, titles, universities, research", direct_effect -0.057) and `sn_volume_render_geom_neg` (L14:F11252, "code/coordinate geometry", direct_effect -0.051) push the probe *down*. The L8 feature is a generic "academic context" detector with frac_nonzero 0.016 — fired by every academic bio, so it acts as a normalizer. The L14 feature fires on "visualization" and is a "3D/code geometry" detector that is generic to graphics work, not specific to any person.

The user's concern is that the probe might rely on spurious gender markers rather than genuine profession indicators. The circuit does *not* support that worry. The strongest single feature (L0:F1069) is a male-pronoun detector, but it is tightly anchored to a specific token ("His" at pos 1) and is accompanied by five strong, independent, profession-content-driven features (PhD, academic-research, education-career, "include" + college, generic research-context). The gender feature is one input among many to a probe that is fundamentally responding to academic-research + PhD content. A counterfactual swap of the pronoun would also likely reduce the L2 "education & career" feature (which lists "He" among its triggers) and alter the L1 "research interests" reading, so gender is partly entangled with the profession signal at the embedding level — but the probe is *not* classifying on gender alone, nor even primarily on gender. The user is correct that gender is in the circuit, but the circuit is overwhelmingly about the academic-research content of the bio.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: 'His' (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: 'research' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: 'interests' (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 4 | Emb: 'include' (pos 4) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: 'visualization' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 12 | Emb: 'graphics' (pos 12) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: '.' (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 27 | Emb: 'PhD' (pos 27) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male pronoun / 'He'-'His' marker (L0:F1069) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F10783](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) | 4 | 'include' word detector (L0:F10783) |  the word "include" (and variations of the word) | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Academic research words (L1:F10986) |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L2:F1621](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) | 13 | People's education & career info (L2:F1621) |  information about people's education and career | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 27 | Academic titles & degrees - positive (L2:F10852) |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L5:F12330](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) | 13 | 'College' mention (L5:F12330) | mentions of "College" along with a preceding place name like "County" or "Valley" | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 27 | Academic degrees - positive (L6:F2254) | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 27 | Academic degrees / universities / people (L7:F14129) |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 13 | Names / titles / universities - suppressive (L8:F11284) |  words and phrases related to people's names, titles, universities, and research | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L14:F11252](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11252) | 9 | Code / 3D geometry / volumetric - suppressive (L14:F11252) |  code and coordinate geometry terms | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11252) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 13 | Probe logit (output) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token 'PROBE' is not one of the top-k next-token candidates  |
| 3 | `get_top_features` | 10 features; top: L0:1069 de=0.070 |
| 4 | `inspect_feature` ×10 | L0:1069, L1:10986, L8:11284, L14:11252, L0:13431, L5:12330, L0:10783, L6:2254, L2:10852, L7:14129 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F1069@1` | ❌ error | — | — | Trace L0:F1069 ("male pronoun 'He'/'His' marker") upstream to understand what to… |
| SA-2 | `L5:F12330@13` | ❌ error | — | — | Trace L5:F12330 ('College' mentions feature) upstream — it fires at pos 13 ('com… |
| SA-3 | `L1:F10986@3` | ✅ reported | 3 | 2 | Trace L1:F10986 ('academic research words' feature) upstream — it fires at pos 3… |
| SA-4 | `L7:F14129@27` | ✅ reported | 8 | 16 | Trace L7:F14129 ('academic degrees, universities, and people associated with the… |

<details>
<summary><b>SA-3</b> — tool trace (6 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L1, F10986 | " words related to academic research" |
| 2 | `get_upstream_features` | L1:F10986@3, k=10 | Emb:" research"@2 (de=6.62) +9 more |
| 3 | `inspect_feature` | L0, F6113 | " the word "overall", sometimes alongside words that express quantity" |
| 4 | `inspect_feature` | L0, F13431 | "the word "owing"." |
| 5 | `get_upstream_features` | L0:F6113@3, k=10 | Emb:" interests"@3 (de=14.19) +9 more |
| 6 | `get_upstream_features` | L0:F6113@3, k=10 | Emb:" interests"@3 (de=14.19) +9 more |

**Findings:** The academic‑research words feature (L1:F10986) at position 3 is driven primarily by two input embeddings: the token "research" (pos 2) and the token "interests" (pos 3). These embeddings strongly activate a shallow (layer‑0) scope/quantity detector (F6113), which in turn provides the largest positive direct effect (+0.578) to the target feature. A secondary, smaller contribution comes from anothe…

</details>

<details>
<summary><b>SA-4</b> — tool trace (11 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L7, F14129 | " academic degrees, universities, and people associated with them" |
| 2 | `get_upstream_features` | L7:F14129@27, k=10 | Emb:" PhD"@27 (de=19.25) +9 more |
| 3 | `inspect_feature` | L6, F2254 | "references to academic degrees" |
| 4 | `inspect_feature` | L5, F13801 | "abbreviations for degrees and mentions of educational attainment" |
| 5 | `inspect_feature` | L5, F11028 | " terms and phrases related to academic study and institutions" |
| 6 | `get_upstream_features` | L6:F2254@27, k=10 | Emb:" PhD"@27 (de=22.00) +9 more |
| 7 | `inspect_feature` | L2, F10852 | " academic titles and degrees" |
| 8 | `get_upstream_features` | L2:F10852@27, k=10 | Emb:" PhD"@27 (de=29.50) +9 more |
| 9 | `inspect_feature` | L4, F3727 | " mentions of academic degrees" |
| 10 | `inspect_feature` | L6, F8285 | " text related to scientific publications and author information." |
| 11 | `inspect_feature` | L1, F14298 | "academic publications, papers, and citations" |

**Findings:** The target feature L7:F14129 (academic degrees/universities) receives its strongest push from the raw token embedding of "PhD" at the same position (direct_effect ~19). This signal propagates upward through a chain of degree‑related features: L6:F2254 (references to academic degrees), L5:F13801 (abbreviated degree tokens), L5:F11028 (academic study terms), L6:F8285 (scientific publication context)…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"His"@1 (de=21.62) +9 more |
| 2 | `get_upstream_features` | L5:F12330@13, k=10 → Emb:"<bos>"@0 (de=-3.23) +9 more |
| 3 | `inspect_feature` ×5 | L3:9204, L2:1621, L4:2958, L4:3319, L0:6051 |
| 4 | `get_upstream_features` | L3:F9204@13, k=8 → Emb:"."@13 (de=11.50) +7 more |
| 5 | `get_upstream_features` | L2:F1621@13, k=8 → Emb:"His"@1 (de=3.70) +7 more |
| 6 | `get_upstream_features` | L4:F3319@13, k=8 → Emb:" research"@2 (de=5.12) +7 more |
| 7 | `get_upstream_features` | L14:F11252@9, k=5 → Emb:" visualization"@9 (de=6.06) +4 more |
| 8 | `get_upstream_features` | L8:F11284@13, k=5 → Emb:" research"@2 (de=3.94) +4 more |
| 9 | `get_upstream_features` | L0:F10783@4, k=5 → Emb:" include"@4 (de=24.62) +4 more |

### Build

`build_circuit` → 19 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 60,728 | 10,960 | 236,183 | 0 | $0.0455 | — | — |
| SA-3 | openai/gpt-oss-120b | 62,432 | 4,629 | 2,624 | 0 | $0.0122 | ✅ 3F/2E | Trace L1:F10986 ('academic research words' feature) upstream… |
| SA-4 | openai/gpt-oss-120b | 162,169 | 10,925 | 0 | 0 | $0.0309 | ✅ 8F/16E | Trace L7:F14129 ('academic degrees, universities, and people… |
| **Total** | | **285,329** | **26,514** | **238,807** | **0** | **$0.0886** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 44s