# Circuit Oracle Report
**Date:** 2026-07-28 07:23:42 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's nurse-classification score is driven primarily by repeated female-pronoun tokens ("She") and generic bio sentence patterns, with a smaller genuine-profession contribution from the word "Nursing" — confirming the user's concern about spurious gender-marker reliance.

**Confidence:** 7

**Reasoning:**

The circuit traces three parallel input streams into the probe direction:

1. **Gender/spurious stream (dominant).** `Emb: She (pos 1)` (direct_effect 19.25) and `Emb: She (pos 19)` (direct_effect 15.3 into L18:F14677) feed a chain of pronoun-detecting features: **L4:F7864** (direct_effect 4.4, fires exclusively on "She" at pos 1) → **L6:F11646** (direct_effect 0.498 at pos 1; also fires at pos 2 and pos 19, all "She"). L6:F11646 then feeds **L18:F14677** (direct_effect 0.377), which is a multi-position "She"-detector firing at pos 1, 19, and 50, and **L19:F9685** (direct_effect 0.26). Crucially, L18:F14677 and L19:F9685 have *no* upstream connection to the word "Nursing" or any other profession vocabulary — their only strong upstream is the "She" embedding node and the L6:F11646 pronoun feature. The L17:F5889 and L15:F3330 features upstream of L18:F14677 also trace exclusively back to the " She" embedding (direct_effect 21.4 and 18.0 respectively). This is a pure gender-marker pathway.

2. **Genuine profession stream (minor).** `Emb: Nursing (pos 10)` (direct_effect 17.4) feeds **L4:F11037** → **L6:F15267** (direct_effect 0.473, activation 24.9), which genuinely encodes the word "Nursing." This is the only profession-vocabulary pathway in the top of the circuit.

3. **Sentence-pattern stream (spurious).** **L4:F15317** (pos 2, direct_effect 0.34) and **L12:F12940** (pos 2, direct_effect 0.30) fire on the "graduated" token in a "She graduated with her..." bio sentence — a generic biographical-narrative pattern, not a profession indicator. These features also receive a large direct contribution from the "She" embedding (pos 1, direct_effect 3.9 into L12:F12940), compounding the gender bias.

The top direct_effect values in the graph (L6:F11646 = 0.498, L6:F15267 = 0.473, L18:F14677 = 0.377) are split roughly evenly between the **gender stream** (F11646 at "She") and the **profession stream** (F15267 at "Nursing"). However, the L18:F14677 feature — the largest single mid-layer driver — is *itself* fed only by "She" embeddings and pronoun features, so its 0.377 contribution is entirely gender-mediated. Summing, roughly half the probe's positive score is attributable to the repeated female pronoun, with the rest coming from the single token "Nursing" and a generic bio-sentence template that itself correlates with female-gendered bios.

**The user's concern is validated:** the probe relies on gender markers ("She" at pos 1, 19, 50) as heavily as on the actual profession word "Nursing," and the late-layer aggregating features (L18:F14677, L19:F9685) are downstream of the pronoun pathway with no compensating profession-vocabulary input. A simple gender swap (male pronoun) would likely keep a large fraction of the probe's score active.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 19 | Mid/Late layer aggregation features (L12-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 1 | Mid/Late layer aggregation features (L12-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 50 | Mid/Late layer aggregation features (L12-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 19 | Mid/Late layer aggregation features (L12-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 140 | Mid/Late layer aggregation features (L12-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 2 | Mid/Late layer aggregation features (L12-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 19 | Mid/Late layer aggregation features (L12-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 19 | Mid/Late layer aggregation features (L12-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 19 | Mid/Late layer aggregation features (L12-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Female pronoun detector (L6:F11646) — fires on "She" | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 2 | Female pronoun detector (L6:F11646) — fires on "She" | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 19 | Female pronoun detector (L6:F11646) — fires on "She" | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Female pronoun feature (L4:F7864) — direct from "She" emb | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L4:F15317](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) | 2 | Sentence-pattern feature (L4:F15317) — pos 2 "graduated" | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15317) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | Profession word feature (L6:F15267) — fires on " Nursing" | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 10 | Profession word feature (L6:F15267) — fires on " Nursing" | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | Profession word feature (L6:F15267) — fires on " Nursing" | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L0:F16075](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) | 15 | Early-layer token-level features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16075) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 1 | Early-layer token-level features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Early-layer token-level features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 19 | Early-layer token-level features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 19 | Early-layer token-level features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L2:F7672](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) | 1 | Early-layer token-level features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/7672) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=0.498 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@1` | ❌ error | — | — | Trace upstream from L6:F11646 at pos 1 ("She"). This feature fires with high dir… |
| SA-2 | `L6:F15267@10` | ❌ error | — | — | Trace upstream from L6:F15267 at pos 10. This has high activation (24.875) and d… |
| SA-3 | `L18:F14677@19` | ❌ error | — | — | Trace upstream from L18:F14677 at pos 19. This feature has direct_effect 0.377 a… |
| SA-4 | `L4:F15317@2` | ❌ error | — | — | Trace upstream from L4:F15317 at pos 2. Direct_effect 0.344. This is an early-la… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@1, k=10 → Emb:"She"@1 (de=19.25) +9 more |
| 2 | `get_upstream_features` | L6:F15267@10, k=10 → Emb:" Nursing"@10 (de=17.38) +9 more |
| 3 | `get_upstream_features` | L18:F14677@19, k=10 → Emb:" She"@19 (de=15.31) +9 more |
| 4 | `get_upstream_features` | L4:F15317@2, k=10 → Emb:"She"@1 (de=10.94) +9 more |
| 5 | `get_upstream_features` | L19:F9685@19, k=10 → Emb:" She"@19 (de=6.19) +9 more |
| 6 | `get_upstream_features` | L12:F12940@2, k=10 → Emb:" graduated"@2 (de=4.81) +9 more |
| 7 | `get_upstream_features` | L4:F7864@1, k=10 → Emb:"She"@1 (de=24.62) +9 more |
| 8 | `get_upstream_features` | L6:F8166@81, k=10 → L5:F6637 (de=-6.31) +9 more |
| 9 | `get_upstream_features` | L4:F11037@10, k=10 → Emb:" Nursing"@10 (de=10.62) +9 more |
| 10 | `get_upstream_features` | L17:F5889@19, k=8 → Emb:" She"@19 (de=21.38) +7 more |
| 11 | `get_upstream_features` | L15:F3330@19, k=8 → Emb:" She"@19 (de=18.00) +7 more |

### Build

`build_circuit` → 11 nodes, 11 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 11,217 | 4,741 | 47,048 | 0 | $0.0119 | — | — |
| **Total** | | **11,217** | **4,741** | **47,048** | **0** | **$0.0119** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 54s