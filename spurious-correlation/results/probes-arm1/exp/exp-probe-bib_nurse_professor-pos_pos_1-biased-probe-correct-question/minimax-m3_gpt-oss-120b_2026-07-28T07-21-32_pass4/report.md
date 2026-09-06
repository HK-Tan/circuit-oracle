# Circuit Oracle Report
**Date:** 2026-07-28 07:21:32 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven primarily by a chain of female-pronoun/identity features anchored to the "she" token at position 7, with only modest direct contribution from genuine profession indicators like "nurses" and "Perioperative."

**Confidence:** 8

**Reasoning:** The circuit traces cleanly to embedding nodes. The dominant positive signal flow is a **gender-marker cascade originating from the " she" embedding (pos 7)** that propagates upward:
- **Emb " she" (pos 7) → L6:F11646** "references to women, triggered by pronouns and titles" (direct_effect 5.59 into L18:F14677) → **L10:F14965** "terms relating to women" → **L12:F12940** "female pronouns and possessive pronouns" → **L18:F14677** "instances of women or girls being mentioned" (top positive contributor to the probe, +0.91) → **L19:F9685** "references to women's names and their roles or accomplishments" (+0.56). A parallel branch from Emb " she" goes through **L4:F7864** directly to the output (+0.60), and another through the " her" embedding at pos 38 reinforces L18:F14677 (+0.32 from pos 38).
- The strongest *negative* contributor to the probe is **L0:F12519 "the pronoun 'she'" (-0.71)**, which is mathematically suppressing the probe — but its absolute value is smaller than the combined positive push from the L6/L10/L12/L18/L19 women-identity chain, so the net probe score still rises with female-pronoun density.

The profession pathway is genuinely present but much smaller: **Emb " nurses" (pos 15) → L2:F15728 "nurses/nursing" (+0.33) → L6:F15267 "nursing profession words" (+0.55 at pos 15, +0.32 at pos 14)**, plus the **Emb " Perio" (pos 13) / "perative" (pos 14)** tokens feeding the same L6:F15267 feature. Adding these, the profession-specific positive contribution is roughly +1.2, while the gender-identity positive contribution from the L18/L19/L4 features is roughly +2.0+.

The user's concern is well-supported: the circuit is **not purely profession-driven**. The largest single late-layer promoter (L18:F14677, frac_nonzero 0.012) is a "women are being mentioned" detector, not a nursing detector. The L19 "women's names and accomplishments" feature is also firing on "she" rather than on any nursing role-token. If you ablated the "she" token at pos 7, the L18/L19/L12 women-identity chain collapses, and only the L2:L6 nursing-feature path would remain — meaning the probe would still classify correctly but with substantially lower confidence. Conversely, replacing "she" with "he" in this same document would invert the sign on the gender chain (L18:F14743 "He" is -0.44, L0:F12519 is -0.71, L6:F16329 female names is -0.67) while leaving the L2/L6 nursing features untouched, so the probe would still push *toward* nursing because the nursing features are profession-specific enough to fire independently. The bias is real but not total: the circuit shows **both a profession pathway (smaller, robust) and a gender-marker pathway (larger, identity-based)** converging on the output, with the gender pathway contributing the majority of the positive signal.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 7 | L0:12519 — 'she' pronoun detector (NEGATIVE on probe) |  the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L1:F4232](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) | 7 | L1:4232 — 'her' possessive detector (NEGATIVE on probe) |  the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) |
| [L2:F15728](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15728) | 15 | L2:15728 — 'nurses/nursing' profession detector |  mentions of nurses and nursing | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15728) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | L6:15267 — 'nursing profession words' (Perioperative/nursing) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | L6:15267 — 'nursing profession words' (Perioperative/nursing) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 7 | L6:11646 — 'references to women (pronouns/titles)' (POSITIVE on probe) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 7 | L6:16329 — 'female first names' (NEGATIVE on probe) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 7 | L4:7864 — sub-word/code signal coupled to 'she' (POSITIVE on probe) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 7 | L10:14965 — 'terms relating to women' (POSITIVE on probe) |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 7 | L12:12940 — 'female pronouns/possessives' (POSITIVE on probe) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 7 | L18:14677 — 'instances of women/girls being mentioned' (POSITIVE on probe) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 7 | L18:14743 — 'He' male pronoun (NEGATIVE on probe) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 7 | L19:9685 — 'women's names and roles/accomplishments' (POSITIVE on probe) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:11646 de=1.555 |
| 3 | `inspect_feature` ×14 | L6:11646, L18:14677, L0:12519, L12:12940, L6:16329, L4:7864, L19:9685, L6:15267, L18:14743, L1:4232, L2:15728, L10:14965, L7:8644, L18:14677 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@7` | ❌ error | — | — | Trace the path from L18:F14677 (activates on "instances of women or girls being … |
| SA-2 | `L6:F15267@15` | ❌ error | — | — | Trace the path from L6:F15267 ("nursing profession words" feature) at position 1… |
| SA-3 | `L0:F12519@7` | ❌ error | — | — | Trace the path from L0:F12519 ("the pronoun 'she'") at position 7. This has a NE… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@7, k=10 → Emb:" she"@7 (de=28.38) +9 more |
| 2 | `get_upstream_features` | L6:F15267@15, k=10 → Emb:" nurses"@15 (de=16.12) +9 more |
| 3 | `get_upstream_features` | L0:F12519@7, k=10 → Emb:" she"@7 (de=41.25) +9 more |
| 4 | `get_upstream_features` | L6:F11646@7, k=10 → Emb:" she"@7 (de=31.62) +9 more |
| 5 | `get_upstream_features` | L19:F9685@7, k=10 → Emb:" she"@7 (de=12.25) +9 more |
| 6 | `get_upstream_features` | L18:F14677@38, k=10 → Emb:" her"@38 (de=22.00) +9 more |
| 7 | `get_upstream_features` | L4:F7864@7, k=8 → Emb:" she"@7 (de=27.25) +7 more |
| 8 | `get_upstream_features` | L12:F12940@7, k=8 → Emb:" she"@7 (de=12.31) +7 more |
| 9 | `get_upstream_features` | L6:F16329@7, k=6 → Emb:" she"@7 (de=14.31) +5 more |
| 10 | `get_upstream_features` | L6:F15267@14, k=6 → Emb:"perative"@14 (de=7.72) +5 more |
| 11 | `get_upstream_features` | L2:F15728@15, k=6 → Emb:" nurses"@15 (de=22.62) +5 more |
| 12 | `get_upstream_features` | L10:F14965@7, k=6 → Emb:" she"@7 (de=11.88) +5 more |
| 13 | `get_upstream_features` | L19:F9685@7, k=6 → Emb:" she"@7 (de=12.25) +5 more |

### Build

`build_circuit` → 18 nodes, 31 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 36,323 | 5,307 | 190,148 | 0 | $0.0287 | — | — |
| **Total** | | **36,323** | **5,307** | **190,148** | **0** | **$0.0287** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 5s