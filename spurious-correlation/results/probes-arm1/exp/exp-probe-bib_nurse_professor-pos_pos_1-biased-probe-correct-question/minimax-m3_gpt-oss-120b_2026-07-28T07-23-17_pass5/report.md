# Circuit Oracle Report
**Date:** 2026-07-28 07:23:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_1 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification score is driven overwhelmingly by female-pronoun / female-name features, with the nursing profession feature contributing only weakly; the probe is relying on gender markers as a spurious proxy for "nurse" rather than genuine profession semantics.

**Confidence:** 8/10

**Reasoning:**

**Top positive features driving the probe (all women/gender-related):**
- **L6:F11646** (direct_effect=+1.55) — "references to women, potentially triggered by pronouns and titles" at pos 7 ("she")
- **L18:F14677** (+0.91, +0.32, +0.27 at pos 7/38/53) — "instances of women or girls being mentioned"
- **L12:F12940** (+0.69) — "references to female pronouns and possessive pronouns"
- **L4:F7864** (+0.60) — mixed-code feature, but receives +4.16 from the "she" embedding
- **L19:F9685** (+0.56) — "references to women's names and their roles or accomplishments"
- **L6:F15267** (+0.55, +0.32) — **the only true profession feature** ("words referring to nursing"), but small effect
- **L10:F14965** (+0.31) — "terms relating to women"
- **L15:F12956** (+0.27 via L18) — "female names and female-related words"

**Negative (suppressive) features:**
- **L0:F12519** (-0.71) — "the pronoun she" but its *suppressed tokens* list shows "▁she/she/She" are suppressed — this is a generic "non-she" token feature that is *inhibiting* because the she-token is present
- **L6:F16329** (-0.67) — "female first names and possessive forms" (suppresses "herself", "she", "her")
- **L18:F14743** (-0.44) — "He" — the male-pronoun feature is firing slightly and pushing the probe *away* from its direction (consistent with a "female-stereotyped profession" encoding)

**Tracing the path to embeddings confirms this:**
- L6:F11646 ← embedding "she" (pos 7, direct_effect=+31.6) and "she" (pos 53, +34.25) and "her" (pos 38, -2.19)
- L18:F14677 ← embedding "she" pos 7 (+28.4), "her" pos 38 (+22.0), "she" pos 53 (+22.6) — *all three* female pronoun tokens, plus some downstream boost from the nursing-profession feature (L6:15267 → "nurses" pos 15, +2.4)
- L19:F9685 ← embedding "her" pos 38 (+7.66), "nurses" pos 15 (+2.42), "she" pos 7 (+2.17)

**Spurious-cue structure:** The most-upstream causes of the positive score are the three input tokens "she" (pos 7), "her" (pos 38), "she" (pos 53). These flow through a clean L0→L6→L12→L18→L19 hierarchy of increasingly abstract "woman/female-person" features, with the generic male-pronoun feature L18:F14743 ("He") acting as a counter-balance (negative direct_effect) — classic male/female-association contrast. The genuine profession feature L6:F15267 ("nursing") appears, but its direct_effect is only ~+0.55 — an order of magnitude smaller than the cumulative contribution of the pronoun features. Even where the nursing feature feeds forward into L18:F14677, it does so by *strengthening the "woman" abstraction*, not by representing the profession independently.

**Conclusion:** The user's concern is well-founded. The probe classifies "nurse" primarily because the passage is about a woman — the three female pronouns ("she", "her", "she") drive a stacked hierarchy of female-gender detectors (L0:12519 → L1:4232 → L4:7864 → L6:11646 → L10:14965 → L12:12940 → L15:12956 → L17:5889 → L18:14677 → L19:9685), with the actual "nursing" profession feature (L6:15267) playing a minor supporting role and even contributing to the gender abstraction rather than providing an independent profession signal.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Emb: she (pos 7) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 38 | Emb: her (pos 38) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 53 | Emb: she (pos 53) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 15 | Emb: nurses (pos 15) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 14 | Emb: perative (pos 14) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 7 | Early-layer 'she' detectors |  the pronoun "she" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L0:F7509](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) | 7 | Early-layer 'she' detectors |  female pronouns and words like daughter and husband that refer to women | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7509) |
| [L1:F4232](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) | 7 | Early-layer 'she' detectors |  the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4232) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 7 | Mid-layer gender/pronoun aggregation (L4-L12) | xml or source code snippets, especially tags and possibly keywords in other languages besides English | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 7 | Mid-layer gender/pronoun aggregation (L4-L12) |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F16329](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) | 7 | Mid-layer gender/pronoun aggregation (L4-L12) | female first names and their possessive forms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/16329) |
| [L10:F14965](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) | 7 | Mid-layer gender/pronoun aggregation (L4-L12) |  terms relating to women | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14965) |
| [L12:F12940](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) | 7 | Mid-layer gender/pronoun aggregation (L4-L12) | references to female pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12940) |
| [L15:F12956](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12956) | 7 | Mid-layer pronoun features (L15-L17) | female names and female-related words in the document. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12956) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 7 | Mid-layer pronoun features (L15-L17) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L16:F15679](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15679) | 38 | Mid-layer pronoun features (L15-L17) | his/her | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15679) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 15 | Profession feature: nursing (L6:15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 14 | Profession feature: nursing (L6:15267) |  words in the document referring to the profession of nursing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 7 | Late-layer 'women/girls' detectors (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 38 | Late-layer 'women/girls' detectors (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 53 | Late-layer 'women/girls' detectors (L18-L19) |  instances of women or girls being mentioned | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 7 | Late-layer 'women/girls' detectors (L18-L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 38 | Late-layer 'women/girls' detectors (L18-L19) |  references to women's names and their roles or accomplishments. | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 7 | Late-layer 'women/girls' detectors (L18-L19) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11646 de=1.555 |
| 3 | `inspect_feature` ×10 | L6:11646, L18:14677, L12:12940, L4:7864, L19:9685, L0:12519, L6:16329, L6:15267, L18:14743, L1:4232 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11646@7` | ❌ error | — | — | Trace the path from L6:F11646 (women/pronouns reference) upstream. What tokens i… |
| SA-2 | `L18:F14677@7` | ❌ error | — | — | Trace the path from L18:F14677 (instances of women/girls) upstream. Identify wha… |
| SA-3 | `L19:F9685@7` | ❌ error | — | — | Trace L19:F9685 (women's names and roles) upstream to its source. Reach embeddin… |
| SA-4 | `L6:F15267@15` | ❌ error | — | — | Trace L6:F15267 (nursing profession words) upstream. Is this genuine profession … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11646@7, k=15 → Emb:" she"@7 (de=31.62) +14 more |
| 2 | `get_upstream_features` | L18:F14677@7, k=15 → Emb:" she"@7 (de=28.38) +14 more |
| 3 | `get_upstream_features` | L19:F9685@7, k=15 → Emb:" she"@7 (de=12.25) +14 more |
| 4 | `get_upstream_features` | L6:F15267@15, k=10 → Emb:" nurses"@15 (de=16.12) +9 more |
| 5 | `get_upstream_features` | L6:F11646@15, k=5 → ❌ Feature (layer=6, feature_idx=11646) not found at pos=15. Th |
| 6 | `get_upstream_features` | L6:F11646@53, k=5 → Emb:" she"@53 (de=34.25) +4 more |
| 7 | `inspect_feature` ×2 | L17:5889, L15:12956 |
| 8 | `get_upstream_features` | L19:F9685@15, k=10 → ❌ Feature (layer=19, feature_idx=9685) not found at pos=15. Th |
| 9 | `get_upstream_features` | L18:F14677@38, k=8 → Emb:" her"@38 (de=22.00) +7 more |
| 10 | `get_upstream_features` | L18:F14677@53, k=8 → Emb:" she"@53 (de=22.62) +7 more |
| 11 | `inspect_feature` | L10, F14965 → " terms relating to women" |
| 12 | `get_upstream_features` | L19:F9685@38, k=8 → Emb:" her"@38 (de=7.66) +7 more |
| 13 | `inspect_feature` ×2 | L16:15679, L0:7509 |
| 14 | `get_upstream_features` | L6:F15267@14, k=8 → Emb:"perative"@14 (de=7.72) +7 more |

### Build

`build_circuit` → 11 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 33,517 | 4,825 | 186,919 | 0 | $0.0271 | — | — |
| **Total** | | **33,517** | **4,825** | **186,919** | **0** | **$0.0271** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 37s