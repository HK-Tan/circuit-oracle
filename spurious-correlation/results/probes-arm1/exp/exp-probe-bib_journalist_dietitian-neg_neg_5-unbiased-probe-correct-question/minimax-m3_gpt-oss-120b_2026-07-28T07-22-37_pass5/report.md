# Circuit Oracle Report
**Date:** 2026-07-28 07:22:37 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "reporter" classification is driven almost entirely by the word **"reporter" at position 66** (the only token whose embedding directly reaches the late-layer journalism features), with a journalism-specific feature cascade flowing from L4 (F13253 "journalism/media" and F661 "reports/documentaries") through L6 (F12712 "editors/publishers"), L7 (F13646 "news reporting", F9092 "broadcast journalism"), L8 (F8855 "mentions of reporters"), L14 (F4420 "journalism/newspapers") and into L19 (F2486 "journalistic sources/news outlets") which directly drives the probe logit.

**Confidence:** 8

**Reasoning:**

**User's concern is NOT supported by this circuit.** The user's hypothesis was that the probe uses spurious features (e.g., gender markers like "He/His") rather than genuine profession indicators. The attribution graph shows the opposite: the dominant pathway is a clean profession-specific feature chain keyed on the literal word "reporter."

**Dominant pathway (profession signal):**
- The **Emb: "reporter" (pos 66)** node has the strongest direct effects on every late-layer journalism feature: +26.6 into L4:F13253, +18.75 into L14:F4420, +28.25 into L19:F2486, +16.9 into L8:F8855, +15.1 into L7:F13646, +11.6 into L6:F12712. All five L4+ features are labeled as journalism/reporter-specific on Neuronpedia and have `frac_nonzero` values between 0.007 and 0.017 (highly selective), with promoted tokens like "journalists", "reporter", "reporting", "reporters".
- L4:F13253 ("journalism and the media", frac=0.0065) → L7:F13646 ("news reporting", frac=0.0076) + L7:F9092 ("broadcast journalism", frac=0.0095) → L8:F8855 ("mentions of news reporters", frac=0.0085) → L14:F4420 ("journalism and newspapers", frac=0.0165) → L19:F2486 ("journalistic sources and news outlets", frac=0.029) → **probe logit**.

**Where the "He" / gender signal sits:** L0:F1069 ("references to a male person, particularly 'He' or 'His'", pos=1) does appear in the top-15 with direct_effect=-0.089. But (a) it is *inhibitory* to the probe score — it pushes against the reporter classification, not toward it; (b) it sits at the layer-0 token-embedding level and does not connect into the journalism feature cascade at L4+; (c) its `frac_nonzero` is 0.0078 (very selective — the "He" feature, not a male-profession correlate). The other L0 token-level features (F4874 "preparation", F8061 "in", F8974 "from", F14824 "has", F13864 "ever", F6051 "periods/spaces", F8642 "mathematical proofs", F9397 "technical jargon") are all generic lexical/format features with direct_effects of ±0.08, and they too do not propagate into the late-layer profession features — they connect directly to the probe with weak magnitude.

**Why the probe looks clean here:** The probe is a *linear* probe on a specific layer, and the circuit shows the probe direction aligns with the residual-stream representation of "reporter" processed through genuine profession-detector features. The "He"-related feature is, if anything, slightly *anti-correlated* with the reporter probe score on this input. The profession-signal pathway is direct (single token "reporter" → L4 → L7 → L8 → L14 → L19 → logit) with no detour through gender/pronoun circuitry. The user's concern about spurious gender features is plausible a priori (professions can correlate with gender in training data) but the attribution graph on this specific prompt does not exhibit it — the classification is being driven by the semantic content of the profession noun itself.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 66 | Emb: reporter (pos 66) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 21 | Emb: freelancer (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4874](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4874) | 2 | Layer-0 token-level features (positions 1,2,6,9,16,21,22,24) |  the word "preparation" and words connected to it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4874) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Layer-0 token-level features (positions 1,2,6,9,16,21,22,24) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 6 | Layer-0 token-level features (positions 1,2,6,9,16,21,22,24) |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 9 | Layer-0 token-level features (positions 1,2,6,9,16,21,22,24) | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 16 | Layer-0 token-level features (positions 1,2,6,9,16,21,22,24) | the word "has" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F13864](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13864) | 22 | Layer-0 token-level features (positions 1,2,6,9,16,21,22,24) | the word "ever," sometimes in conjunction with comparatives or superlatives | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13864) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 24 | Layer-0 token-level features (positions 1,2,6,9,16,21,22,24) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F8642](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8642) | 2 | Layer-0 token-level features (positions 1,2,6,9,16,21,22,24) | words and symbols appearing in mathematical or logical proofs and conclusions. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8642) |
| [L0:F9397](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9397) | 21 | Layer-0 token-level features (positions 1,2,6,9,16,21,22,24) |  jargon and terminology from technical documents | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9397) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 66 | L4: journalism/media (F13253, F661) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L4:F661](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) | 66 | L4: journalism/media (F13253, F661) |  words and phrases used when referring to reports, documentaries, and television coverage of news | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/661) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 66 | L6: editors/publishers (F12712) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 21 | L6: editors/publishers (F12712) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 66 | L7: news reporting (F13646, F9092) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 66 | L7: news reporting (F13646, F9092) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 66 | L8: mentions of reporters (F8855) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 66 | L14: journalism/newspapers (F4420) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 66 | L19: journalistic sources/news outlets (F2486) |  journalistic sources and news outlets. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:4420 de=-0.196 |
| 3 | `inspect_feature` ×14 | L14:4420, L19:2486, L4:13253, L0:4874, L0:6051, L0:8642, L0:1069, L0:8974, L0:14824, L0:8061, L6:12712, L8:8855, L0:13864, L0:9397 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@66` | ❌ error | — | — | Trace upstream from L14:F4420 ("words and phrases related to journalism and news… |
| SA-2 | `L19:F2486@66` | ❌ error | — | — | Trace upstream from L19:F2486 ("journalistic sources and news outlets") at posit… |
| SA-3 | `L8:F8855@66` | ❌ error | — | — | Trace upstream from L8:F8855 ("mentions of news reporters and news reporting") a… |
| SA-4 | `L4:F13253@66` | ❌ error | — | — | Trace upstream from L4:F13253 ("things related to journalism and the media") at … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@66, k=15 → Emb:" reporter"@66 (de=18.75) +14 more |
| 2 | `get_upstream_features` | L19:F2486@66, k=15 → Emb:" reporter"@66 (de=28.25) +14 more |
| 3 | `get_upstream_features` | L8:F8855@66, k=15 → Emb:" reporter"@66 (de=16.88) +14 more |
| 4 | `get_upstream_features` | L4:F13253@66, k=15 → Emb:" reporter"@66 (de=26.62) +14 more |
| 5 | `get_upstream_features` | L7:F13646@66, k=10 → Emb:" reporter"@66 (de=15.12) +9 more |
| 6 | `get_upstream_features` | L7:F9092@66, k=10 → L4:F13253 (de=6.81) +9 more |
| 7 | `get_upstream_features` | L6:F12712@66, k=10 → Emb:" reporter"@66 (de=11.56) +9 more |
| 8 | `get_upstream_features` | L4:F661@66, k=10 → Emb:" reporter"@66 (de=18.00) +9 more |
| 9 | `inspect_feature` ×3 | L7:13646, L7:9092, L4:661 |

### Build

`build_circuit` → 10 nodes, 22 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,449 | 6,916 | 174,240 | 0 | $0.0342 | — | — |
| **Total** | | **51,449** | **6,916** | **174,240** | **0** | **$0.0342** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 17s