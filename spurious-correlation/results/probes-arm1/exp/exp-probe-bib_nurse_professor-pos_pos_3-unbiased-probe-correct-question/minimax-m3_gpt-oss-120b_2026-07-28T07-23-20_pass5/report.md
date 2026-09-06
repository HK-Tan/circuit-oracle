# Circuit Oracle Report
**Date:** 2026-07-28 07:23:20 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe is classified as "nurse" primarily through genuine profession vocabulary — the word "nurse" (pos 7), "practitioner" (pos 8), "Internal Medicine" (pos 10-11), "labor"/"delivery" (pos 44/46) — which flows through nursing-specific features at layers 6-7 to late-layer "management/medicine/research" features (L14:F3985, L15:F15159); the female-pronoun feature (L0:F15382) fires but contributes *negatively* (-0.038) to the probe, not as a spurious positive signal.

**Confidence:** 8

**Reasoning:**

The positive signal is dominated by profession-grounded features, not gender. The two strongest individual positive drivers are L6:F15267 ("words referring to the nursing profession," direct_effect +0.087 at pos 8) and L14:F3985 ("terms related to management, leadership, medicine, studies, research," +0.089 at pos 8). Both trace back to genuine input tokens: L6:F15267 is most strongly fed by the "nurse" embedding at pos 7 (direct_effect 7.06) and "practitioner" at pos 8 (3.48), with the "nurse" word-piece feature L0:F8854 (frac_nonzero 0.005, fires on "nurse" tokens) as a key intermediate. L14:F3985 is fed by the "practitioner" embedding (6.19), L4:F9036 ("healthcare practitioners," 6.13), and again L6:F15267 (2.02). L15:F15159 ("medicine/healthcare") is fed overwhelmingly by the "nurse" embedding at pos 7 (direct_effect 17.5) and "She" at pos 1 (1.09, but small).

The "nurse" profession signal converges at L14:F3985 and L6:F15267 from the embeddings "nurse" (pos 7), "practitioner" (pos 8), "Medicine" (pos 11), "labor" (pos 44), and "delivery" (pos 46) — the latter two being specifically labor-and-delivery nursing vocabulary, which is exactly the profession being described. The "Internal Medicine" embedding at pos 10-11 feeds L4:F4665 ("medical environments/personnel/facilities") which then feeds L14:F3985 at pos 11 (direct_effect 13.19).

Crucially, the female-pronoun feature L0:F15382 ("mentions of a female person" / "Her") at pos 1 fires with a *negative* direct_effect on the probe (-0.038). L0:F10846 ("also" at pos 3) also contributes negatively (-0.042). The "She" embedding at pos 1 only weakly excites L15:F15159 (+1.09 out of 17.5 total) and is mostly a background signal. The user's concern about spurious gender features is not borne out by the attribution graph: the "She/Her" feature is *not* a primary driver of the nurse-profession classification; if anything, the pronoun features subtract slightly from the probe score. The classification is driven by the cluster of medical/nursing vocabulary (nurse, practitioner, Internal Medicine, labor, delivery) propagating through hierarchically deeper "nursing profession" features (L6:F15267, L7:F3979) to late-layer "medicine/management" features (L14:F3985, L15:F15159) that directly feed the probe.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: She (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: also (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: nurse (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: practitioner (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: Internal Medicine (pos 10-11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 11 | Emb: Internal Medicine (pos 10-11) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 44 | Emb: labor (pos 44) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: delivery (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 26 | Emb: spent/most/life/years (pos 26-30, 39) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 30 | Emb: spent/most/life/years (pos 26-30, 39) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 20 | Emb: clinical/research (pos 20-21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Layer 0 — Female pronoun / "Her" feature (pos 1) | mentions of a female person. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F10846](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) | 3 | Layer 0 — Female pronoun / "Her" feature (pos 1) | the word "also" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10846) |
| [L0:F8854](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) | 7 | Layer 0 — "nurse" token feature (pos 7) |  the word "nurse" as well as some pronouns | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8854) |
| [L0:F1832](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) | 44 | Layer 0 — "nurse" token feature (pos 7) | the word "labor" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1832) |
| [L0:F3175](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3175) | 11 | Layer 0 — "nurse" token feature (pos 7) |  the word "minute" and the word "voltage" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3175) |
| [L1:F7152](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7152) | 46 | Layer 1-2 — Profession / medical practice words | the word "delivery" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7152) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 8 | Layer 1-2 — Profession / medical practice words |  words related to medical practices and studies. | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L4:F12178](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12178) | 30 | Layer 1-2 — Profession / medical practice words |  phrases that include words expressing a length of time | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12178) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Layer 1-2 — Profession / medical practice words | various acronyms, IDs, and symbols, possibly related to scientific data | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 11 | Layer 4-5 — Medical environments / healthcare professionals |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 46 | Layer 4-5 — Medical environments / healthcare professionals |  words and phrases related to medical environments, treatments, personnel, and facilities. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 8 | Layer 4-5 — Medical environments / healthcare professionals |  words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 11 | Layer 4-5 — Medical environments / healthcare professionals |  words and abbreviations associated with healthcare. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 8 | Layer 4-5 — Medical environments / healthcare professionals | words related to healthcare professionals and medical fields | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 8 | Layer 4-5 — Medical environments / healthcare professionals |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 11 | Layer 4-5 — Medical environments / healthcare professionals |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L5:F9749](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) | 46 | Layer 4-5 — Medical environments / healthcare professionals |  words related to various medical conditions, procedures, and practitioners | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/9749) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 7 | Layer 6-7 — Nursing profession features |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 8 | Layer 6-7 — Nursing profession features |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 47 | Layer 6-7 — Nursing profession features |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 7 | Layer 6-7 — Nursing profession features |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 8 | Layer 6-7 — Nursing profession features |  words related to nursing and healthcare | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 11 | Layer 6-7 — Nursing profession features |  words and abbreviations associated with pediatric gastroenterology and inflammatory bowel disease. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L6:F9980](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) | 46 | Layer 6-7 — Nursing profession features |  words and abbreviations associated with pediatric gastroenterology and inflammatory bowel disease. | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9980) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 7 | Layer 14-15 — Management/medicine/research late-layer features | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 8 | Layer 14-15 — Management/medicine/research late-layer features | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 11 | Layer 14-15 — Management/medicine/research late-layer features | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 46 | Layer 14-15 — Management/medicine/research late-layer features | terms related to management, leadership, medicine, studies, and research | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 7 | Layer 14-15 — Management/medicine/research late-layer features |  words related to medicine and healthcare | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:3985 de=0.089 |
| 3 | `inspect_feature` ×14 | L14:3985, L6:15267, L15:15159, L4:4665, L4:12178, L6:9980, L4:9757, L0:1832, L0:10846, L0:15382, L0:3175, L1:7152, L5:9749, L7:3979 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@8` | ❌ error | — | — | Trace the path from L14:F3985 ("management, leadership, medicine, studies, resea… |
| SA-2 | `L6:F15267@8` | ❌ error | — | — | Trace the path from L6:F15267 ("words referring to the nursing profession") upst… |
| SA-3 | `L0:F15382@1` | ❌ error | — | — | Trace L0:F15382 ("mentions of a female person" / "Her" pronoun) upstream and dow… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@8, k=15 → Emb:" practitioner"@8 (de=6.19) +14 more |
| 2 | `get_upstream_features` | L6:F15267@8, k=15 → Emb:" nurse"@7 (de=7.06) +14 more |
| 3 | `get_upstream_features` | L15:F15159@7, k=15 → Emb:" nurse"@7 (de=17.50) +14 more |
| 4 | `inspect_feature` ×4 | L4:9036, L1:1494, L0:8854, L5:1275 |
| 5 | `get_upstream_features` | L0:F10846@3, k=10 → Emb:" also"@3 (de=33.50) +9 more |
| 6 | `get_upstream_features` | L0:F3175@11, k=10 → Emb:" Medicine"@11 (de=15.38) +9 more |
| 7 | `get_upstream_features` | L0:F15382@1, k=10 → Emb:"She"@1 (de=16.88) +9 more |
| 8 | `get_upstream_features` | L5:F9749@46, k=10 → L4:F4665 (de=2.92) +9 more |
| 9 | `get_upstream_features` | L14:F3985@46, k=10 → Emb:" delivery"@46 (de=3.50) +9 more |
| 10 | `get_upstream_features` | L14:F3985@11, k=10 → Emb:" Medicine"@11 (de=13.19) +9 more |
| 11 | `get_upstream_features` | L0:F1832@44, k=10 → Emb:" labor"@44 (de=25.00) +9 more |
| 12 | `get_upstream_features` | L6:F9980@46, k=10 → L4:F4665 (de=2.77) +9 more |
| 13 | `get_upstream_features` | L4:F12178@30, k=10 → Emb:" spent"@26 (de=10.12) +9 more |
| 14 | `get_upstream_features` | L4:F4665@46, k=10 → Emb:" labor"@44 (de=3.45) +9 more |
| 15 | `get_upstream_features` | L4:F4665@11, k=10 → Emb:" Medicine"@11 (de=4.22) +9 more |

### Build

`build_circuit` → 16 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 40,789 | 6,109 | 259,149 | 0 | $0.0351 | — | — |
| **Total** | | **40,789** | **6,109** | **259,149** | **0** | **$0.0351** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 38s