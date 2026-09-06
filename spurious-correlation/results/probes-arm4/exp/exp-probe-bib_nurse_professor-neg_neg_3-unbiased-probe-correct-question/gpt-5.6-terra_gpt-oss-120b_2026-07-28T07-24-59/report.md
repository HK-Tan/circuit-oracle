# Circuit Oracle Report
**Date:** 2026-07-28 07:24:59 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The profession-probe score is driven chiefly by an academic-biography/credential pattern—especially the explicit “Ph.D.” and university-attendance text—not by the gender marker “He.”

**Confidence:** 8/10

**Reasoning:** The saved circuit identifies two main, competing academic-context pathways into the synthetic profession-probe direction.

1. **Explicit degree pathway (strongest semantically grounded route).**  
   The embeddings for **“Ph” (pos 50)** and **“D” (pos 52)** feed the early **Explicit Ph.D. / degree detector**:
   - L1:10132 at pos 52, a highly selective Ph.D. spelling detector (*frac_nonzero* 0.00233), which activates specifically on the `D` in “Ph.D.”;
   - L2:10852 at pos 52, an academic-titles/degrees detector (*frac_nonzero* 0.00801), whose promoted tokens include **“degree,” “PhD,” and “doctorate.”**

   These then drive the **Academic-degree aggregation** node:
   - L6:2254 at pos 52, “references to academic degrees” (*frac_nonzero* 0.00412);
   - L7:14129 at pos 52, “academic degrees, universities, and people associated with them” (*frac_nonzero* 0.00417).

   The causal evidence is especially direct: the `Ph` and `D` embeddings contribute strongly and positively to L2:10852 (14.75 and 10.125 respectively), and to L1:10132 (16.25 and 13.125). L2:10852 positively feeds L6:2254 (12.06), which positively feeds L7:14129 (6.97), and L7:14129 is itself a positive direct driver of the probe score (+0.0432). This is a generic but genuine **academic credential signal**, rather than recognition of a particular person or profession title.

2. **University/institution pathway, with an opposite signed contribution.**  
   **“Peking” (pos 12)** and **“University” (pos 13)** feed L4:5150, the named-university detector (*frac_nonzero* 0.00399). Its top promoted tokens are **University**, **College**, and **universities**, and its upstream attribution is dominated by `University` (+17.75) and `Peking` (+5.94). This feature feeds L6:3235, a broader academic-publication/math/scientific-institution feature (*frac_nonzero* 0.03885). L6:3235 is among the largest direct contributors to the final score, but its sign is **negative** (-0.054). Thus, the probe is not simply using “more academic language = more of the predicted profession”; it contrasts different academic-profile patterns.

3. **Gender-marker concern.**  
   There is only weak evidence of a gender shortcut in the traced high-impact circuit. The specific `He` embedding at pos 1 appears as a small positive upstream contribution to L3:4213 (+0.656), a degree/award feature, while that node is centered on degree qualifications and not pronouns. It is not a principal route to the output in the constructed circuit. Likewise, L0:6270, despite some local activation, is a function-word/“whom” feature and has a negative rather than supportive relation in the university branch. I therefore do **not** find evidence that the classification is primarily produced by gender.

Overall, the probe appears to classify from a **template-like academic CV signal**: Ph.D. notation, repeated degrees, named universities, mathematics/computer-science education, and institutional affiliation. This is substantially more profession-relevant than gender, but it is still partly a **spurious proxy** for profession: the circuit detects credentials and academic-biographical writing style more directly than it detects the explicit occupation phrase (“Assistant Professor of Computer Science”).

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L1:F10132](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) | 52 | Explicit Ph.D. / degree detector |  the abbreviation for Doctorate of Philosophy, "Ph.D." (or "PhD") written as "D" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10132) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 52 | Explicit Ph.D. / degree detector |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 52 | Academic-degree aggregation | references to academic degrees | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 52 | Academic-degree aggregation |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L4:F5150](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) | 13 | Named-university recognition |  mentions of specific universities and colleges | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5150) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 13 | Academic/publication/institution context (negative score driver) |  academic publications, math, and scientific institutions | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:3235 de=-0.054 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14129@52` | ❌ error | — | — | Trace this positive driver of the synthetic profession-probe score upstream to e… |
| SA-2 | `L6:F3235@13` | ❌ error | — | — | Trace this strongest negative driver of the probe score upstream to embeddings. … |
| SA-3 | `L2:F10852@52` | ❌ error | — | — | Trace this strong negative probe driver at end of the biography upstream, seekin… |
| SA-4 | `L6:F3774@12` | ❌ error | — | — | Trace this negative driver upstream. Assess whether it is driven by the pronoun … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L0:15320, L0:6270, L3:4213, L7:14129, L6:3235, L2:10852, L6:3774 |
| 2 | `get_upstream_features` | L7:F14129@52, k=20 → L6:F2254 (de=6.97) +19 more |
| 3 | `get_upstream_features` | L6:F3235@13, k=20 → L4:F5150 (de=2.88) +19 more |
| 4 | `get_upstream_features` | L2:F10852@52, k=20 → Emb:" Ph"@50 (de=14.75) +19 more |
| 5 | `get_upstream_features` | L6:F3774@12, k=20 → Emb:" Peking"@12 (de=10.12) +19 more |
| 6 | `get_upstream_features` | L3:F4213@11, k=20 → Emb:" from"@11 (de=10.69) +19 more |
| 7 | `inspect_feature` ×3 | L6:2254, L1:10132, L4:5150 |
| 8 | `get_upstream_features` | L6:F2254@52, k=15 → L2:F10852 (de=12.06) +14 more |
| 9 | `get_upstream_features` | L1:F10132@52, k=15 → Emb:" Ph"@50 (de=16.25) +14 more |
| 10 | `get_upstream_features` | L4:F5150@13, k=15 → Emb:" University"@13 (de=17.75) +14 more |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 22,026 | 2,710 | 68,155 | 0 | $0.1128 | — | — |
| **Total** | | **22,026** | **2,710** | **68,155** | **0** | **$0.1128** | | |

**Oracle wall-clock time:** 0m 39s