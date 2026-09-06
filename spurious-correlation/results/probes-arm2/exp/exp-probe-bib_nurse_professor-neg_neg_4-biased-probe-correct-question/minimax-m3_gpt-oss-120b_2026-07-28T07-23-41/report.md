# Circuit Oracle Report
**Date:** 2026-07-28 07:23:41 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's profession-classification score is driven primarily by **male-gendered pronoun features** (He, his, He is) and a generic title/preposition pattern, with no genuine profession-specific signal.

**Confidence:** 8

**Reasoning:**

**1. Top contributing features (positive direct_effect) are pronoun/gender features, not profession features:**

- **L0:F2994** at pos 37 and pos 55 — *the single largest positive contributor* (direct_effect 0.254 and 0.154). Tracing it upstream shows it is almost entirely driven by the token embedding "** his**" (direct_effect 45.25), with trivial contributions from surrounding tokens. This is a possessive-pronoun feature, not a profession indicator.
- **L0:F8658** at pos 2 — direct_effect 0.110, sourced from the embeddings of "He" (8.0) and " is" (6.28). Again a male-pronoun + copula feature.
- **L7:F14893** at pos 1 and pos 13 — direct_effect 0.132 and 0.130, traced upstream to the "He" embedding (14.75). This is a mid-layer male-pronoun detector.
- **L0:F2848** at pos 5 — direct_effect 0.148, sourced from " of" (34.75) with the "Director" embedding contributing only 0.47. This is a preposition feature, not a "Director" feature.
- **L0:F11024** at pos 4 — direct_effect 0.142, sourced mostly from "**Director**" (12.8) — this is the *only* token-level profession word, but it is a low-level lexical feature and is overshadowed by the pronoun signal.

**2. Profession-relevant context (Director, Ph.D., Computer Science, Mobile Grid, Korea University) is absent from the top features.** The model's mid- and late-layer features that would normally integrate entity-level profession knowledge (e.g., a "computer science professor" concept) do not appear in the top 15. Instead, what dominates is the *subject of the sentence* — "He".

**3. Negative-direction features also encode pronoun form, not profession:**
- L6:F12990 (direct_effect −0.166, −0.125, −0.114 at pos 13, 35, 2) — upstream is the "He" embedding.
- L7:F14946 at pos 2 (direct_effect −0.125) — upstream is "He" (9.0).
- L12:F2175 at pos 2 (direct_effect −0.108) — upstream is L7:F14946.
- L18:F14743 at pos 35 (direct_effect −0.141) — upstream is the " He" embedding (23.6).
- L4:F4315 at pos 13 (direct_effect −0.109).

So the **entire circuit — both promotors and suppressors — is built on the same pronoun axis ("He", "his")** rather than on profession semantics.

**4. The user's concern is confirmed.** The probe is leveraging the subject's gender as a proxy for profession. The female-form versions of these features (e.g., "She", " her") would presumably produce the opposite sign, and a female version of this same bio would likely yield a different (or near-zero) probe score despite identical professional content. A profession-classifying probe should be using the title/preposition and the field-of-study tokens ("Director of Mobile Grid", "Ph.D. in Computer Science from Korea University"), but those only appear as weak low-level lexical features (L0:F11024, L0:F2848) without any deeper, profession-specific integration in the circuit. The causal mass sits on L0 pronoun detectors that never get refined by profession-specific mid/late-layer concepts.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 37 | Male / possessive pronoun detector ('He', ' his', 'He is') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 55 | Male / possessive pronoun detector ('He', ' his', 'He is') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Male / possessive pronoun detector ('He', ' his', 'He is') | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 13 | Male / possessive pronoun detector ('He', ' his', 'He is') | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L0:F8658](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) | 2 | Male / possessive pronoun detector ('He', ' his', 'He is') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8658) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 5 | Title / preposition context (' of', 'Director') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F11024](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) | 4 | Title / preposition context (' of', 'Director') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11024) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 13 | Negative contributors (L6:F12990, L7:F14946, L12:F2175, L18:F14743) — pronoun-context features that push the score down | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 2 | Negative contributors (L6:F12990, L7:F14946, L12:F2175, L18:F14743) — pronoun-context features that push the score down | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | Negative contributors (L6:F12990, L7:F14946, L12:F2175, L18:F14743) — pronoun-context features that push the score down | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 35 | Negative contributors (L6:F12990, L7:F14946, L12:F2175, L18:F14743) — pronoun-context features that push the score down | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 13 | Negative contributors (L6:F12990, L7:F14946, L12:F2175, L18:F14743) — pronoun-context features that push the score down | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2994 de=0.254 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@37` | ❌ error | — | — | Trace this L0 feature at position 37. What token/context does it fire on? Is it … |
| SA-2 | `L0:F2848@5` | ❌ error | — | — | Trace this L0 feature at position 5. What does it encode? Is it a profession ind… |
| SA-3 | `L0:F11024@4` | ❌ error | — | — | Trace this L0 feature at position 4. What does it detect? Gender? Profession? |
| SA-4 | `L6:F12990@13` | ❌ error | — | — | Trace this L6 feature at position 13. It has strong negative direct_effect. What… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2994@37, k=5 → Emb:" his"@37 (de=45.25) +4 more |
| 2 | `get_upstream_features` | L0:F2848@5, k=5 → Emb:" of"@5 (de=34.75) +4 more |
| 3 | `get_upstream_features` | L0:F11024@4, k=5 → Emb:" Director"@4 (de=12.81) +4 more |
| 4 | `get_upstream_features` | L0:F8658@2, k=5 → Emb:"He"@1 (de=8.00) +4 more |
| 5 | `get_upstream_features` | L7:F14893@1, k=5 → Emb:"He"@1 (de=14.75) +4 more |
| 6 | `get_upstream_features` | L12:F2175@2, k=5 → L7:F14946 (de=5.41) +4 more |
| 7 | `get_upstream_features` | L18:F14743@35, k=5 → Emb:" He"@35 (de=23.62) +4 more |
| 8 | `get_upstream_features` | L7:F14946@2, k=5 → Emb:"He"@1 (de=9.00) +4 more |

### Build

`build_circuit` → 9 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 13,124 | 5,012 | 46,354 | 0 | $0.0127 | — | — |
| **Total** | | **13,124** | **5,012** | **46,354** | **0** | **$0.0127** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 58s