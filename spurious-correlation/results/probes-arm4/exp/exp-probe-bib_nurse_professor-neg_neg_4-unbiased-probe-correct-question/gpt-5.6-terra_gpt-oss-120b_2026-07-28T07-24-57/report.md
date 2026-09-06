# Circuit Oracle Report
**Date:** 2026-07-28 07:24:57 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven by a mixed biography/academic-profession circuit—explicit academic and technical-role cues are present, but the strongest listed features also include Korean affiliation and a male-pronoun cue, so the classification is not cleanly profession-specific.

**Confidence:** 8/10

**Reasoning:**  
The saved circuit separates several independent streams into the **Probe classification score**:

- **Genuine profession/academic evidence**
  - **Emb: “Director” (pos 4) → Directorship/authority cue**: L2:F4627 is a highly selective detector for *“director”* (frac_nonzero **0.00347**) and is driven overwhelmingly by the literal `Director` embedding (positive upstream direct effect **27.5**). It has a negative direct effect on the probe score (**−0.0474**), meaning this title pushes against the probe’s selected class/direction rather than supporting it. Regardless of its sign, it is clearly occupation-relevant evidence.
  - **Emb: “Grid” (pos 7) → Grid/computing-research lexical cue**: L1:F14934 detects *grid* (frac_nonzero **0.00919**) and is driven by the `Grid` embedding (**+18.25**). It positively drives the probe (**+0.0479**). In this text, “Mobile Grid and Cloud Computing Laboratory” is meaningful technical/professional evidence, though the feature is lexical and not necessarily specific to computer science.
  - **Emb: “Ph” / “D” (positions 38/40) → Academic-degree detector → Academic credential/university evidence**: L2:F10852 detects academic degrees (frac_nonzero **0.00801**; promoted tokens include `degree`, `PhD`, `doctorate`) and is directly supported by `Ph` (**+14.125**) and `D` (**+9.75**). It positively feeds L7:F14129 (**+2.6094**), a selective academic-degree/university feature (frac_nonzero **0.00417**) whose examples include PhD holders, professors, and universities. L7:F14129 has a positive direct effect on the probe (**+0.0435**). This is the strongest evidence that the probe reflects scholarly/academic-professional status rather than only surface demographics.

- **Likely spurious or dataset-correlated evidence**
  - **Emb: “He” (pos 1) → Male-pronoun detector**: L0:F1069 is explicitly a male-reference feature, firing on `He`/`His` (frac_nonzero **0.0078**), and it is strongly driven by the input `He` embedding (**+22.625**). Its direct effect on the probe is **+0.0420**. Thus, male gender marking increases the probe score. This directly substantiates the user’s concern: gender is causally used by the probe, not merely correlated elsewhere in the text.
  - **Emb: “Korea” (pos 46) → Korea/national-affiliation feature → Late Korea/Korean reference feature**: L6:F3774 is a generic unusual-proper-noun/capitalization feature (frac_nonzero **0.03078**) but is strongly driven by the `Korea` embedding (**+18.375**). It feeds L14:F15086 (**+6.2188**), which is a selective Korea/Korean detector (frac_nonzero **0.01904**) and is itself driven primarily by `Korea` (**+28.875**). L14:F15086 has the largest-magnitude listed direct effect on the probe (**−0.0613**). This is not evidence of profession; it is nationality/institutional-location information. Its negative sign means it suppresses the selected probe class, but its magnitude shows the classification relies substantially on it.

The circuit therefore supports a **mixed-mechanism diagnosis**. The positive academic path—especially `Ph.D.` → L2:F10852 → L7:F14129—shows that genuine academic credentials help produce the score. The title and technical term features provide additional profession-related lexical evidence. However, L0:F1069 proves that the model/probe direction also reads the male pronoun, and L14:F15086 shows a very strong dependence on `Korea`. These latter features encode demographic or nationality/affiliation signals rather than the person’s profession.

Importantly, the signs are heterogeneous: male pronoun, Grid, and academic credentials push the score upward, whereas Director and Korea push downward. So this is not simply “the probe predicts profession from male gender.” Rather, the linear probe direction appears to combine several correlated biography templates—male academic biographies, degree/university evidence, technical vocabulary, and Korean affiliation—with some cues supporting and others opposing its selected class. That makes the classification vulnerable to spurious correlations and unlikely to be a robust, profession-only representation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Male-pronoun detector |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L2:F4627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) | 4 | Directorship/authority cue | the word "director" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4627) |
| [L1:F14934](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) | 7 | Grid/computing-research lexical cue | the word "grid" and some related terms related to "grids" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14934) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 40 | Academic-degree detector |  academic titles and degrees | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 40 | Academic credential/university evidence |  academic degrees, universities, and people associated with them | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L6:F3774](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) | 46 | Korea/national-affiliation feature |  proper nouns or names with unusual capitalization | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3774) |
| [L14:F15086](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) | 46 | Late Korea/Korean reference feature |  references to Korea/Korean | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15086) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L14:15086 de=-0.061 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F15086@46` | ❌ error | — | — | Trace this strongest late feature upstream to embeddings. Determine whether it r… |
| SA-2 | `L6:F3774@46` | ❌ error | — | — | Trace upstream to embeddings; identify semantic mechanism and source text, espec… |
| SA-3 | `L0:F10846@3` | ❌ error | — | — | Inspect and trace this early feature at the likely gender-pronoun position. Esta… |
| SA-4 | `L7:F14129@40` | ❌ error | — | — | Trace this positive mid-layer driver upstream to embeddings. Determine which inp… |
| SA-5 | `L1:F14934@7` | ❌ error | — | — | Trace this positive early feature upstream to input embedding(s); determine whet… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×12 | L14:15086, L6:3774, L0:10846, L2:10852, L1:14934, L2:4627, L0:8658, L7:14129, L0:12904, L0:1069, L0:1242, L0:15160 |
| 2 | `get_upstream_features` | L14:F15086@46, k=20 → Emb:" Korea"@46 (de=28.88) +19 more |
| 3 | `get_upstream_features` | L7:F14129@40, k=20 → L6:F2254 (de=7.12) +19 more |
| 4 | `get_upstream_features` | L6:F3774@46, k=20 → Emb:" Korea"@46 (de=18.38) +19 more |
| 5 | `get_upstream_features` | L2:F10852@40, k=20 → Emb:" Ph"@38 (de=14.12) +19 more |
| 6 | `get_upstream_features` | L2:F4627@4, k=20 → Emb:" Director"@4 (de=27.50) +19 more |
| 7 | `get_upstream_features` | L1:F14934@7, k=20 → Emb:" Grid"@7 (de=18.25) +19 more |
| 8 | `get_upstream_features` | L0:F1069@1, k=20 → Emb:"He"@1 (de=22.62) +19 more |

### Build

`build_circuit` → 14 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 29,402 | 2,740 | 68,556 | 0 | $0.1317 | — | — |
| **Total** | | **29,402** | **2,740** | **68,556** | **0** | **$0.1317** | | |

**Oracle wall-clock time:** 0m 35s