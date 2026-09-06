# Circuit Oracle Report
**Date:** 2026-07-28 07:25:02 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven substantially by a spurious male-pronoun pathway (“his”/“He”), with a smaller genuine pathway recognizing degree/academic-field information associated with Mechanical Engineering.

**Confidence:** 9/10

**Reasoning:** The saved circuit separates two qualitatively different sources of evidence.

1. **Dominant spurious gender pathway.**  
   The largest positive direct driver of the probe is **L0:2994 at position 3** (activation 39.5, direct effect **+0.3945**). Its label is explicitly *“the pronoun ‘his’ and the pronoun ‘he’”* (frac_nonzero **0.07326**). Its strongest upstream source is the raw **Emb: “ his” (pos 3)** with direct effect **+43.25**. Thus, this is not a subtle inference from the biography; it is essentially a direct lexical gender marker feeding the probe direction.

   A second strong positive path is **L7:14893 at position 3** (activation 10.69, direct effect **+0.2041**), labeled *pronouns or possessive pronouns* (frac_nonzero **0.00885**). It is driven most strongly by the same **“ his” embedding** (**+24.38**), with only a much smaller positive contribution from “Daniel” (**+3.77**). Its promoted tokens include female pronouns such as “she”/“herself,” while it suppresses “his”/“himself”; this appears to be a grammatical gender/pronoun-direction feature whose signed alignment with the learned probe happens to raise this class score.

   The opposing **L7:14946** is also a male-pronoun feature: it is labeled *“the possessive pronoun ‘his’ (or similar pronouns like ‘he’ and ‘him’)”*, is driven by **“his”** (**+23.13**), and has a negative probe effect (**−0.1758**). This shows that the probe is not simply “all masculinity equals this class”: it has mixed internal gender directions. But the net salient contribution is nonetheless strongly gender-linked, because L0:2994’s **+0.3945** and L7:14893’s **+0.2041** are among the highest positive effects in the graph.

   There is also a later negative gender path: **L18:14743 at “He” (pos 22)**, labeled *“He”* (frac_nonzero **0.01809**), contributes **−0.1387** to the probe and is directly driven by **Emb: “ He” (pos 22)** (**+21.88**). It reinforces the conclusion that the classifier has learned multiple gender-correlated directions, some positive and some negative, rather than treating gender as irrelevant.

2. **Real educational/professional-content pathway.**  
   The circuit also contains bona fide evidence about professional background. **L6:170 at “Engineering” (pos 9)** has a positive effect of **+0.1436** and is labeled *“references to academic fields”* (frac_nonzero **0.03882**). Its main upstream cause is **L5:10392 at pos 9** (**+10.94**), a highly selective *“fields of academic study”* feature (frac_nonzero **0.00362**). That feature is fed by degree/field tokens: **“Mechanical”** (+3.08), **“achelors”** (+2.67), and **“degree”** (+2.02), plus degree-context features. This is a genuine semantic path from the education statement—Bachelor’s degree / Mechanical Engineering—to the classification score.

3. **Overall assessment of the concern.**  
   The concern is supported. The strongest single positive probe contributor is not an engineering, robotics, academic-degree, or research feature; it is **L0:2994**, a direct *“his/he”* detector. The next large positive route, **L7:14893**, is likewise pronoun-based. Genuine profession-relevant evidence exists, especially the **Mechanical / Bachelor’s / degree → L5:10392 → L6:170** path, but it is weaker than the top raw gender-marker effect. Therefore the probe’s classification is best characterized as **a mixture of legitimate education/academic-field evidence and a substantial, likely spurious gender-correlated shortcut**, not a classification based purely on profession indicators.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Male possessive-pronoun detector | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 3 | Pronoun/gender signal to probe |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 9 | Academic-field / degree evidence |  fields of academic study | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 9 | Academic-field detector to probe |  references to academic fields, especially those in the humanities | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.395 |
| 3 | `inspect_feature` ×5 | L0:2994, L7:14893, L7:14946, L6:170, L18:14743 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@3` | ❌ error | — | — | Trace the strongest positive mid-layer driver of the synthetic profession-probe … |
| SA-2 | `L6:F170@9` | ❌ error | — | — | Trace this positive driver at the 'Bachelors' area upstream to embeddings. Estab… |
| SA-3 | `L18:F14743@22` | ❌ error | — | — | Trace this high-layer negative/suppressive feature to identify counterevidence t… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@3, k=20 → Emb:" his"@3 (de=24.38) +19 more |
| 2 | `get_upstream_features` | L7:F14946@3, k=20 → Emb:" his"@3 (de=23.12) +19 more |
| 3 | `get_upstream_features` | L6:F170@9, k=20 → L5:F10392 (de=10.94) +19 more |
| 4 | `get_upstream_features` | L18:F14743@22, k=20 → Emb:" He"@22 (de=21.88) +19 more |
| 5 | `get_upstream_features` | L0:F2994@3, k=20 → Emb:" his"@3 (de=43.25) +19 more |
| 6 | `inspect_feature` ×5 | L0:1326, L0:7532, L5:10392, L6:12990, L0:1069 |
| 7 | `get_upstream_features` | L5:F10392@9, k=20 → Emb:" Mechanical"@8 (de=3.08) +19 more |
| 8 | `get_upstream_features` | L6:F12990@22, k=15 → Emb:" He"@22 (de=4.47) +14 more |

### Build

`build_circuit` → 8 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 21,601 | 2,507 | 71,448 | 0 | $0.1095 | — | — |
| **Total** | | **21,601** | **2,507** | **71,448** | **0** | **$0.1095** | | |

**Oracle wall-clock time:** 0m 37s