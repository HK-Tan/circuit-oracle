# Circuit Oracle Report
**Date:** 2026-07-28 07:24:04 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe classifies Daniel as an engineering/academic profession primarily through genuine profession-relevant features: the "Engineering" / "Mechanical" field tokens (L1:F1372, direct_effect +0.064), PhD-degree features (L2:F10852, L5:F13801), and "University of Waterloo" entity features (L4:F8439, L6:F11873, L7:F8870, L14:F5600) — all of which are legitimate profession indicators, not gender markers.

**Confidence:** 7

**Reasoning:** The circuit traces cleanly from input tokens to the probe direction. The strongest positive contributors to the probe score are:
- **L1:F1372 (pos 9, +0.064)** — "Engineering" field-of-degree detector, driven directly by the " Engineering" embedding (pos 9, +19.0). This is a genuine profession indicator.
- **L14:F5600 (pos 14, +0.064)** — late-layer "Waterloo" university-concept feature, built from a chain Waterloo-emb → L4:F8439 → L7:F8870 → L14:F5600. This encodes the *institutional* signal (research university in engineering), not a profession per se but still relevant to an academic/engineer identity.
- **L0:F15320 (pos 2, +0.058)** and **L0:F4687 (pos 14, +0.047)** — narrative-verb and university-name detectors driven by " received" and " Waterloo" embeddings.
- **L2:F16309 (pos 1, +0.049)** — name-token detector for "Daniel".

The negative contributors include **L0:F6515 (pos 18, -0.048)**, **L0:F11333 (pos 19, -0.045)**, **L0:F11132 (pos 19, -0.044)** — all driven by year digits "1"/"9"/"9" (1993), which suppress the probe. **L0:F2743 (pos 23, -0.069)** is driven by " later" (direct_effect +42.25) and pushes against the classification. **L0:F7905 (pos 2)** and **L0:F2085 (pos 2)** are narrative-verb suppressors. **L6:F3235 (pos 38, -0.055)** is a "Beirut" suppressor.

**Crucially, no gendered or pronoun-based features appear in the circuit.** The pronoun "He" at pos 22 has near-zero direct_effect on every top feature (e.g., L0:F2743 shows " He" with +0.30 vs " later" with +42.25). The model is NOT using gender markers like "he/his/him" as shortcuts here. Instead, the probe's positive signal comes from:
1. The field-of-degree tokens ("Mechanical Engineering") — a direct profession indicator.
2. The institutional research context (Waterloo university, PhD) — a strong correlate of an academic/researcher profession.

The user concern about spurious gender features is not supported by this attribution graph. The "his" pronoun embeddings appear only as minor cross-context cues with small direct_effects. The dominant positive drivers are semantically appropriate: engineering field tokens and research-university/PhD features. This suggests the probe has learned a reasonable profession signal rather than a gender shortcut on this particular input.

One caveat: the strong reliance on "Waterloo" (a specific institution) rather than generic research-university features means the probe may have learned institution-profession correlations specific to the training distribution, which is a different form of spurious correlation than gender — but the user's specific concern (gender markers) is not borne out by this circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4687](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) | 14 | Early-layer name / verb / degree-token feature detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4687) |
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | Early-layer name / verb / degree-token feature detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F7905](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) | 2 | Early-layer name / verb / degree-token feature detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7905) |
| [L0:F2085](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) | 2 | Early-layer name / verb / degree-token feature detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2085) |
| [L0:F12235](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) | 6 | Early-layer name / verb / degree-token feature detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12235) |
| [L0:F16309](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16309) | 1 | Early-layer name / verb / degree-token feature detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16309) |
| [L0:F2743](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) | 23 | Early-layer name / verb / degree-token feature detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2743) |
| [L0:F6515](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) | 18 | Early-layer name / verb / degree-token feature detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6515) |
| [L0:F11333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) | 19 | Early-layer name / verb / degree-token feature detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11333) |
| [L0:F11132](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) | 19 | Early-layer name / verb / degree-token feature detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11132) |
| [L1:F1372](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) | 9 | Field-of-degree 'Engineering' detector at L1 | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1372) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 50 | PhD token detector at L2 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L4:F8439](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) | 14 | University-name 'Waterloo' detector at L4 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8439) |
| [L4:F13886](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13886) | 38 | University-name 'Waterloo' detector at L4 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13886) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 50 | PhD / advanced-degree features at L5 | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L6:F11873](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11873) | 14 | University-context features at L6 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11873) |
| [L6:F3235](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) | 38 | University-context features at L6 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3235) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 50 | University-context features at L6 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F8870](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) | 14 | Higher-level 'Waterloo' abstraction at L7 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8870) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 50 | Higher-level 'Waterloo' abstraction at L7 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L14:F5600](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) | 14 | Late-layer 'Waterloo' university-concept feature | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/5600) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2743 de=-0.069 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F5600@14` | ❌ error | — | — | Trace from L14:F5600 at pos 14. This is one of the top positive contributors to … |
| SA-2 | `L1:F1372@9` | ❌ error | — | — | Trace from L1:F1372 at pos 9. This is a top positive contributor to the probe sc… |
| SA-3 | `L0:F4687@14` | ❌ error | — | — | Trace from L0:F4687 at pos 14. This is a top positive contributor to the probe s… |
| SA-4 | `L0:F15320@2` | ❌ error | — | — | Trace from L0:F15320 at pos 2. This is a top positive contributor. Position 2 is… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F5600@14, k=12 → L7:F8870 (de=15.94) +11 more |
| 2 | `get_upstream_features` | L1:F1372@9, k=12 → Emb:" Engineering"@9 (de=19.00) +11 more |
| 3 | `get_upstream_features` | L0:F4687@14, k=12 → Emb:" Waterloo"@14 (de=16.25) +11 more |
| 4 | `get_upstream_features` | L0:F15320@2, k=12 → Emb:" received"@2 (de=13.00) +11 more |
| 5 | `get_upstream_features` | L7:F8870@14, k=12 → L4:F8439 (de=9.00) +11 more |
| 6 | `get_upstream_features` | L4:F8439@14, k=12 → Emb:" Waterloo"@14 (de=17.25) +11 more |
| 7 | `get_upstream_features` | L6:F11873@14, k=10 → L4:F8439 (de=8.56) +9 more |
| 8 | `get_upstream_features` | L0:F2743@23, k=10 → Emb:" later"@23 (de=42.25) +9 more |
| 9 | `get_upstream_features` | L6:F3235@38, k=10 → Emb:" Beirut"@38 (de=1.85) +9 more |
| 10 | `get_upstream_features` | L6:F2254@50, k=10 → L2:F10852 (de=12.31) +9 more |
| 11 | `get_upstream_features` | L7:F14129@50, k=10 → L6:F2254 (de=7.31) +9 more |
| 12 | `get_upstream_features` | L2:F16309@1, k=10 → Emb:"Daniel"@1 (de=12.94) +9 more |
| 13 | `get_upstream_features` | L0:F6515@18, k=10 → Emb:"1"@17 (de=29.38) +9 more |
| 14 | `get_upstream_features` | L0:F7905@2, k=10 → Emb:" received"@2 (de=12.94) +9 more |
| 15 | `get_upstream_features` | L0:F11333@19, k=10 → Emb:"9"@18 (de=11.31) +9 more |
| 16 | `get_upstream_features` | L0:F11132@19, k=10 → Emb:"9"@18 (de=11.06) +9 more |
| 17 | `get_upstream_features` | L4:F13886@38, k=10 → Emb:" University"@36 (de=6.25) +9 more |
| 18 | `get_upstream_features` | L2:F10852@50, k=10 → Emb:" Ph"@48 (de=14.75) +9 more |
| 19 | `get_upstream_features` | L5:F13801@50, k=10 → L2:F10852 (de=7.25) +9 more |
| 20 | `get_upstream_features` | L1:F10132@50, k=10 → Emb:" Ph"@48 (de=16.38) +9 more |
| 21 | `get_upstream_features` | L0:F2085@2, k=10 → Emb:" received"@2 (de=17.75) +9 more |
| 22 | `get_upstream_features` | L0:F12235@6, k=10 → Emb:" degree"@6 (de=13.38) +9 more |

### Build

`build_circuit` → 20 nodes, 21 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 19,855 | 5,742 | 59,110 | 0 | $0.0164 | — | — |
| **Total** | | **19,855** | **5,742** | **59,110** | **0** | **$0.0164** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 22s