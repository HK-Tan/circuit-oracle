# Circuit Oracle Report
**Date:** 2026-07-28 07:24:58 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession probe is driven principally by genuine academic/research-profile evidence—especially “research interests” and a PhD—while a smaller but salient direct male-pronoun feature also contributes, confirming some gender shortcut use.

**Confidence:** 8/10

**Reasoning:** The saved circuit separates three mechanisms feeding the **Profession-classification probe score**:

1. **Research-context evidence:** `Emb: research (pos 2)` and `Emb: interests (pos 3)` directly excite L1:10986 at position 3, a relatively broad academic-research feature (label: *words related to academic research*, `frac_nonzero=0.03796`). Its strongest upstream embedding effects are `research` (+6.63) and `interests` (+4.47), whereas `His` is mildly inhibitory (−0.33). This feature has a substantial direct positive effect on the probe (+0.0674), so the “research interests” construction is genuine classification evidence rather than an inferred demographic correlate.

2. **Academic credential / biography evidence:** `Emb: PhD (pos 27)` strongly drives the credential pathway. It directly excites:
   - L2:10852 at the PhD position (+29.5); and
   - L6:2254 (+22.0), a rare and highly specific academic-degree detector (*references to academic degrees*, `frac_nonzero=0.00412`).
   
   L6:2254 also receives positive support from L2:10852 (+10.13), forming a coherent degree-recognition path. L6:2254 then feeds L7:14129 (+7.63), the rare academic-profile feature (*academic degrees, universities, and people associated with them*, `frac_nonzero=0.00417`). L7:14129 is itself a positive direct driver of the probe (+0.0403). Its top activating examples include “PhD,” “Professor,” and university-associated people, so this is a genuine education/academic-career representation—not a gender feature. The input’s BS, University, and PhD details all accord with this mechanism.

3. **Gender shortcut:** `Emb: His (pos 1)` very strongly activates L0:1069 (+21.63). L0:1069 is an unusually selective male-pronoun feature (*references to a male person, particularly “He” or “His”*, `frac_nonzero=0.0078`). It has the single largest positive direct effect on the probe score (+0.0698), comparable to the research feature. Thus the probe direction does explicitly assign positive weight to a male-marker representation. This is spurious with respect to profession: “His” supplies no occupation-specific information. Its presence means that replacing male pronouns with a neutral or female referent could lower the score, all else equal.

There is also countervailing technical-content evidence: L14:11252, a code/coordinate-geometry feature (`frac_nonzero=0.02487`), is negative on the probe (−0.0508) and is driven primarily by `visualization` (+6.06). That indicates the probe does not simply reward every technical/scientific topic; it distinguishes an **academic-biography / credential** profile from some technical-topic representations.

Overall, the strongest interpretable positive evidence is substantively relevant—research interests and academic degrees—but the direct L0 male-pronoun contribution is large enough to substantiate the user’s concern. The circuit is therefore **mixed**: mostly profession-adjacent academic-profile signals, with a meaningful spurious gender-marker shortcut embedded in the probe’s decision.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male-pronoun detector |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Research-interest / academic-context detector |  words related to academic research | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 27 | Education/career and degree representation | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F1621](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) | 13 | Education/career and degree representation |  information about people's education and career | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 27 | Academic-degree detector | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 27 | Academic degrees/university profile |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:1069 de=0.070 |
| 3 | `inspect_feature` ×6 | L0:1069, L1:10986, L8:11284, L14:11252, L5:12330, L7:14129 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F10986@3` | ❌ error | — | — | Trace this strong positive driver of the probe score to embedding tokens. Determ… |
| SA-2 | `L5:F12330@13` | ❌ error | — | — | Trace this positive profession-probe driver upstream to embeddings; identify the… |
| SA-3 | `L7:F14129@27` | ❌ error | — | — | Trace this positive driver upstream to embeddings, checking for profession evide… |
| SA-4 | `L14:F11252@9` | ❌ error | — | — | Trace this strong negative driver upstream to embeddings. Identify what evidence… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F10986@3, k=20 → Emb:" research"@2 (de=6.62) +19 more |
| 2 | `get_upstream_features` | L5:F12330@13, k=20 → Emb:"<bos>"@0 (de=-3.23) +19 more |
| 3 | `get_upstream_features` | L7:F14129@27, k=20 → Emb:" PhD"@27 (de=19.25) +19 more |
| 4 | `get_upstream_features` | L14:F11252@9, k=20 → Emb:" visualization"@9 (de=6.06) +19 more |
| 5 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"His"@1 (de=21.62) +9 more |
| 6 | `inspect_feature` ×4 | L4:9757, L2:1621, L3:9204, L6:2254 |
| 7 | `get_upstream_features` | L3:F9204@13, k=20 → Emb:"."@13 (de=11.50) +19 more |
| 8 | `get_upstream_features` | L6:F2254@27, k=20 → Emb:" PhD"@27 (de=22.00) +19 more |
| 9 | `get_upstream_features` | L2:F10852@27, k=15 → Emb:" PhD"@27 (de=29.50) +14 more |

### Build

`build_circuit` → 10 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 21,898 | 2,434 | 74,531 | 0 | $0.1099 | — | — |
| **Total** | | **21,898** | **2,434** | **74,531** | **0** | **$0.1099** | | |

**Oracle wall-clock time:** 0m 41s