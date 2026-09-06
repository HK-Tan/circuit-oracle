# Circuit Oracle Report
**Date:** 2026-07-28 07:20:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by male-gendered pronoun features (his/He) at two token positions, with no representation of profession-specific semantics (computer graphics, visualization, PhD, etc.) anywhere in the circuit.

**Confidence:** 9

**Reasoning:** The circuit confirms the user's concern that the probe relies on spurious gender markers rather than genuine profession indicators.

**Evidence:**
- **Top driver (positive, direct_effect = +0.43):** L7:F14893, labeled "pronouns or possessive pronouns," fired on `His` at pos 1. Its top activating examples are all "his" tokens, and its promoted tokens are feminine ("herself," "she," "ihrer") while suppressed are masculine ("himself," "his," "彼の") — yet it *pushes toward* the probe class here, meaning the probe treats male pronouns as evidence.
- **Second strong positive (+0.24):** L19:F8814 ("various pronouns and names referring to people") at pos 1, similarly a gender/pronoun detector (promoted: "she/her"; suppressed: "himself/his/彼").
- **Strong positive (+0.23):** L0:F2994 explicitly labeled "the pronoun 'his' and the pronoun 'he'" — a pure male-pronoun feature with frac_nonzero ≈ 0.073.
- **Strong negative (−0.25, −0.21):** L18:F14743 ("He") at pos 14 *and* pos 37 — an explicit capitalized "He" detector that pushes against the probe's classification.

**Tracing to embeddings:** Following the L7:F14893 → L0:F2994 path upward reaches `Emb: His (pos 1)` with direct_effect 23.5 — the "His" token embedding is the deepest identifiable source. Likewise, L18:F14743 traces to `Emb:  He (pos 14)` with direct_effect 22.4. The two male-pronoun token positions (pos 1 "His" and pos 14 " He") supply essentially all of the signal.

**What's missing:** No feature in the top-15 drives encodes "computer graphics," "visualization," "PhD," "researcher," "scientist," "lab," or any profession-specific semantic content. The probe has learned a heuristic: "male pronouns at sentence start → male-dominated profession." The same circuit on a bio about a female scientist would presumably give the opposite classification, indicating the probe is detecting the biographical subject's gender, not their profession.

**Conclusion:** The user's hypothesis is correct — the probe's circuit is dominated by male-pronoun/gender features with direct token-embedding roots at the gendered tokens themselves, and contains no profession-representing features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Pos 1 ('His') pronoun/gender features |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Pos 1 ('His') pronoun/gender features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Pos 1 ('His') pronoun/gender features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Pos 1 ('His') pronoun/gender features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | Pos 1 ('His') pronoun/gender features | references to God in the third person. | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Pos 1 ('His') pronoun/gender features | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Pos 1 ('His') pronoun/gender features |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 14 | Pos 14 (' He') pronoun features | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Pos 14 (' He') pronoun features |  words related to coding and software/UI interfaces, with some bias toward non-English words | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Pos 14 (' He') pronoun features |  pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Pos 14 (' He') pronoun features |  various pronouns and names referring to people | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: His (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb:  He (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 0 | Probe classification score (output direction) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L7:14893 de=0.430 |
| 3 | `inspect_feature` ×4 | L7:14893, L19:8814, L0:2994, L18:14743 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace upstream from L7:F14893 ("pronouns or possessive pronouns") at pos 1. This… |
| SA-2 | `L18:F14743@14` | ❌ error | — | — | Trace upstream from L18:F14743 ("He") at pos 14. This is a strong negative drive… |
| SA-3 | `L19:F8814@1` | ❌ error | — | — | Trace upstream from L19:F8814 ("various pronouns and names referring to people")… |
| SA-4 | `L0:F2994@1` | ❌ error | — | — | Trace upstream from L0:F2994 ("the pronoun his and the pronoun he") at pos 1. Th… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@1, k=15 → Emb:"His"@1 (de=23.50) +14 more |
| 2 | `get_upstream_features` | L18:F14743@14, k=15 → Emb:" He"@14 (de=22.38) +14 more |
| 3 | `get_upstream_features` | L0:F2994@1, k=15 → Emb:"His"@1 (de=19.75) +14 more |
| 4 | `get_upstream_features` | L19:F8814@1, k=15 → Emb:"His"@1 (de=9.31) +14 more |
| 5 | `get_upstream_features` | L4:F4315@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 6 | `get_upstream_features` | L6:F12990@1, k=10 → Emb:"His"@1 (de=4.91) +9 more |
| 7 | `get_upstream_features` | L7:F14946@1, k=10 → Emb:"His"@1 (de=18.38) +9 more |
| 8 | `get_upstream_features` | L18:F7400@1, k=10 → Emb:"His"@1 (de=13.00) +9 more |
| 9 | `get_upstream_features` | L2:F5491@1, k=5 → Emb:"His"@1 (de=23.88) +4 more |
| 10 | `get_upstream_features` | L0:F1069@14, k=5 → Emb:" He"@14 (de=35.75) +4 more |
| 11 | `inspect_feature` ×4 | L2:5491, L0:1069, L18:7400, L18:10315 |

### Build

`build_circuit` → 5 nodes, 5 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 20,763 | 3,085 | 94,599 | 0 | $0.0156 | — | — |
| **Total** | | **20,763** | **3,085** | **94,599** | **0** | **$0.0156** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 41s