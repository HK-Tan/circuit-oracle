# Circuit Oracle Report
**Date:** 2026-07-28 07:25:25 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven predominantly by a male-pronoun/gender circuit centered on “His” and “He,” rather than by the text’s genuine historian/business-history indicators.

**Confidence:** 9/10

**Reasoning:** The strongest direct effects into the probe direction are overwhelmingly pronoun features:

- **L7:14893 at pos 1** contributes **+0.4902**. It is a selective pronoun feature (frac_nonzero **0.00885**) that detects possessive/person pronouns; its promoted tokens are female-coded (*“she,” “herself”*) and it suppresses *“his/himself.”* Thus, it appears to represent a direction in the pronoun/gender subspace that the probe has assigned a strong positive weight.
- **L7:14946 at pos 1** contributes **−0.4883** and explicitly detects *“his/he/him”* (frac_nonzero **0.01669**), promoting *“his,” “himself”* and suppressing *“she/her.”* This is the complementary male-coded direction, strongly weighted in the opposite direction by the probe.
- **L0:2994** is also a direct driver at both the first *“His”* (**+0.2578**) and the later *“his”* (**+0.3809**) token. It is an early detector for *“his/he”* (frac_nonzero **0.07326**). At pos 12, its dominant upstream source is exactly **Emb: “ his” (pos 12)** with direct effect **+44.5**.
- **L6:12990** is a male-reference feature (frac_nonzero **0.06766**) that detects male pronouns/titles, with opposing probe effects at positions 1 (**−0.3398**) and 10 (**−0.2031**).
- Later, **L18:14743 at “He” (pos 10)** is an explicit *He* detector (frac_nonzero **0.01809**) and contributes **−0.2852**. Its principal input is **Emb: “ He” (pos 10)** with a very large positive causal connection (**+22.375**).
- **L19:8814 at pos 1** contributes **+0.2949**. Although broadly labelled as a person/pronoun feature (frac_nonzero **0.08655**), its upstream attribution is again dominated by **Emb: “His” (pos 1; +9.3125)**, plus L7 male/female-pronoun directions.

The saved circuit shows a direct route from **Emb: His (pos 1)** through early male-pronoun detection (**L0:2994**), pronoun relaying (**L4:4315**, frac_nonzero 0.02624), and male-reference detection (**L6:12990**) into the opposing L7 pronoun directions. These then either directly affect the probe or feed later pronoun/person features (**L18:10315**, **L19:8814**). Independently, **Emb: He (pos 10)** drives **L0:1069** and the late **L18:14743 “He”** feature into the score.

Critically, the leading features do **not** identify “transnational business history,” “research interests,” “Ph.D. in History,” “Harvard,” “Economics,” “Chicago,” “M.B.A.,” or “Stanford.” The inspected top features instead consistently encode pronouns and gendered reference. The raw embedding-to-feature edges make this especially clear: “His” directly excites both L7 features (**+23.5** to L7:14893; **+18.375** to L7:14946), L4:4315 (**+23.5**), L18:10315 (**+21.375**), and L19:8814 (**+9.3125**).

Therefore, the concern is supported: this classification probe is substantially using a **spurious gender-marker shortcut**. There may be smaller untraced contributions from professional or educational language, but none appear among the highest direct probe-driving features, whereas multiple pronoun features dominate both positive and negative evidence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Early male-pronoun detector (L0:2994, pos 1; L0:1069, pos 10) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 10 | Early male-pronoun detector (L0:2994, pos 1; L0:1069, pos 10) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Pronoun cue relay (L4:4315, pos 1) |  mentions of "his" and other associated pronouns like he, him, or hers. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Male-reference detector (L6:12990, pos 1) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Female-coded pronoun direction (L7:14893, pos 1) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Male-coded his/he direction (L7:14946, pos 1) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 10 | Late He detector (L18:14743, pos 10) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Late possessive-pronoun detector (L18:10315, pos 1) |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Person/pronoun feature (L19:8814, pos 1) |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L7:14893 de=0.490 |
| 3 | `inspect_feature` ×6 | L7:14893, L7:14946, L0:2994, L6:12990, L19:8814, L18:14743 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace this strongest positive probe-driving feature upstream to embeddings. Dete… |
| SA-2 | `L7:F14946@1` | ❌ error | — | — | Trace this strongest negative probe-driving feature upstream to embeddings. Iden… |
| SA-3 | `L19:F8814@1` | ❌ error | — | — | Trace this positive late feature upstream to embeddings, focusing on whether it … |
| SA-4 | `L18:F14743@10` | ❌ error | — | — | Trace this negative late feature upstream to embeddings. Establish its semantic … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@1, k=15 → Emb:"His"@1 (de=23.50) +14 more |
| 2 | `get_upstream_features` | L7:F14946@1, k=15 → Emb:"His"@1 (de=18.38) +14 more |
| 3 | `get_upstream_features` | L19:F8814@1, k=15 → Emb:"His"@1 (de=9.31) +14 more |
| 4 | `get_upstream_features` | L18:F14743@10, k=15 → Emb:" He"@10 (de=22.38) +14 more |
| 5 | `get_upstream_features` | L0:F2994@1, k=15 → Emb:"His"@1 (de=19.75) +14 more |
| 6 | `get_upstream_features` | L0:F2994@12, k=15 → Emb:" his"@12 (de=44.50) +14 more |
| 7 | `inspect_feature` ×4 | L4:4315, L18:7400, L18:10315, L0:1069 |
| 8 | `get_upstream_features` | L18:F7400@1, k=10 → Emb:"His"@1 (de=13.00) +9 more |
| 9 | `get_upstream_features` | L18:F10315@1, k=10 → Emb:"His"@1 (de=21.38) +9 more |
| 10 | `get_upstream_features` | L4:F4315@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |

### Build

`build_circuit` → 12 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 22,147 | 2,689 | 70,556 | 0 | $0.1133 | — | — |
| **Total** | | **22,147** | **2,689** | **70,556** | **0** | **$0.1133** | | |

**Oracle wall-clock time:** 1m 3s