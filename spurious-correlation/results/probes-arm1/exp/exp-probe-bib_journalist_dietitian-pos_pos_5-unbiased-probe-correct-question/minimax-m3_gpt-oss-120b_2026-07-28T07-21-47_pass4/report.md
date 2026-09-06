# Circuit Oracle Report
**Date:** 2026-07-28 07:21:47 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_5 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's positive classification score is driven primarily by profession-specific nutrition/medical vocabulary (the tokens "nutrition", "eating", "disordered", "weight", "management", and the Academy of Nutrition and Dietetics name), not by gendered markers — the female-pronoun features contribute *negatively* to the score.

**Confidence:** 7

**Reasoning:** Tracing the circuit reveals two distinct causal streams. **Profession-positive (the dominant signal):** the embedding of " nutrition" at pos 7 (direct_effect = 12.6 into L4:F13412) feeds a chain of genuine content features — L4:F13412 "diets and dietary health" (top activation token: "dieticians"; frac_nonzero=0.012, highly selective; direct_effect=0.14 at pos 7), L4:F10494 "health, medicine, diet, drugs, exercise" (de=0.18), L6:F11327 "food or nutrition" (de=0.082), L14:F4197 "food/nutrition words" (de=0.10), L14:F16195 "physical activity and training" (de=0.085, fired by the adjacent "sports" embedding), and the most semantically specific L19:F1589 "context of scientific, especially nutritional, studies" (de=0.069, promoted tokens include "nutrition/dietary/diet"). The same L4:F13412 also fires on the second occurrence of nutrition-related terms (pos 13 "disordered eating", de=0.107; pos 10 "weight management", de=0.058; pos 26 "Nutrition/Dietetics" in the Academy name, de=0.083) and on the embedding tokens "disordered" (de=6.1) and "eating" (de=8.7). The Academy-of-Nutrition-and-Dietetics name tokens ("Nutrition"/"Die" at pos 23/25) directly drive both L4:F13412 (de=4.3) and L19:F1589 (de=9.5), making this a textbook professional credential signal. **Gender-marker (negative):** the female-pronoun stream runs through L0:F9519 "she/her" (de=−0.08 at pos 1 "Her") and L6:F11646 "references to women, potentially triggered by pronouns and titles" (de=−0.057, promoted tokens: "she/her/herself"). The reflexive L0:F15322 ("herself/itself") also contributes negatively (de=−0.074). Crucially, L0:F9519 *suppresses* tokens like "She"/"Shepherd" — and here it pushes the probe score *down*. So while gendered tokens are present in the circuit, they are *not* the mechanism carrying the classification; the classification rests on nutrition-domain vocabulary, credentialed institution names, and the sports-nutrition framing. The user's concern that the circuit relies on spurious gender markers is not supported by the attribution — the gender features are load-bearing in the *opposite* direction. Minor caveats: L0:F2268 "spokesman/spokesperson" (de=−0.08) and L0:F10254 "sports" word detector (de=−0.065) fire on legitimate profession text but contribute negatively, suggesting some early-layer literal-token features compete with the later-layer semantic features; this is a generic rather than gender bias.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 7 | L0: literal "nutrition" word detector (negative contribution) |  the word "nutrition" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | L0: female pronoun "she"/"her" detector (negative contribution) |  the pronoun "she" and the possessive pronoun "her" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F15322](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) | 4 | L0: reflexive pronoun "herself"/"itself" (negative contribution) | reflexive pronouns, particularly "herself" and "itself." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15322) |
| [L0:F8028](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8028) | 2 | L0: "areas" (negative contribution) | references to geographical areas in various contexts including scientific and societal | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8028) |
| [L0:F8975](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8975) | 4 | L0: "pragma" code token (negative) |  the word "pragma" in code | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8975) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 14 | L0: periods/period punctuation (negative) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F2268](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2268) | 18 | L0: people communicating information via speech / "spokesman" (negative) |  mentions of people communicating information via speech | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2268) |
| [L0:F10254](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10254) | 6 | L0: literal "sports" word detector (negative) |  the word "sports". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10254) |
| [L0:F10148](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10148) | 1 | L0: "entire" word (positive contribution) |  the word "entire," sometimes near the word "this" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10148) |
| [L0:F2083](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2083) | 4 | L0: "plot" / land / experimental zones (positive) |  the word "plot" referring to land or experimental zones | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2083) |
| [L0:F8850](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8850) | 9 | L0: "weight" word (negative) | the word "weight" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8850) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 7 | L4: dietary / nutrition vocabulary (multi-position) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | L4: dietary / nutrition vocabulary (multi-position) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 10 | L4: dietary / nutrition vocabulary (multi-position) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 26 | L4: dietary / nutrition vocabulary (multi-position) |  terms related to diets and dietary health | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 7 | L4: health, medicine, diet, exercise vocabulary |  words related to health, medicine, diet, drugs, age groups, and excercise | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F11355](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11355) | 10 | L4: body mass index / weight mentions |  mentions of body mass index and weight | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11355) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 7 | L6: food or nutrition words |  words or phrases related to food or nutrition | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | L6: references to women (pronouns/titles) — negative contribution |  references to women, potentially triggered by pronouns and titles | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 7 | L14: food/nutrition words (food insecurity context) |  words and phrases related to food insecurity. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F16195](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) | 7 | L14: physical activity and training | mentions of physical activity and training. | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/16195) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 7 | L19: scientific / nutritional study context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 26 | L19: scientific / nutritional study context |  a context of scientific, specially nutritional, studies | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:10494 de=0.176 |
| 3 | `inspect_feature` ×6 | L4:10494, L4:13412, L14:4197, L14:16195, L6:11327, L19:1589 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13412@7` | ❌ error | — | — | Trace upstream from L4:F13412 (dietary health terms). This is the top feature at… |
| SA-2 | `L14:F4197@7` | ❌ error | — | — | Trace upstream from L14:F4197 (food/nutrition terms) at position 7. Trace 5-6 ho… |
| SA-3 | `L19:F1589@7` | ❌ error | — | — | Trace upstream from L19:F1589 (scientific/nutritional study context) at position… |
| SA-4 | `L14:F16195@7` | ❌ error | — | — | Trace upstream from L14:F16195 (physical activity/training) at position 7. Trace… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F13412@7, k=15 → Emb:" nutrition"@7 (de=12.62) +14 more |
| 2 | `get_upstream_features` | L14:F4197@7, k=15 → Emb:" nutrition"@7 (de=12.88) +14 more |
| 3 | `get_upstream_features` | L19:F1589@7, k=15 → Emb:" nutrition"@7 (de=32.25) +14 more |
| 4 | `get_upstream_features` | L14:F16195@7, k=15 → Emb:" nutrition"@7 (de=7.97) +14 more |
| 5 | `get_upstream_features` | L6:F11327@7, k=15 → Emb:" nutrition"@7 (de=17.50) +14 more |
| 6 | `get_upstream_features` | L4:F10494@7, k=15 → Emb:" nutrition"@7 (de=11.25) +14 more |
| 7 | `get_upstream_features` | L0:F5201@7, k=8 → Emb:" nutrition"@7 (de=27.12) +7 more |
| 8 | `get_upstream_features` | L4:F13412@13, k=10 → Emb:" eating"@13 (de=8.69) +9 more |
| 9 | `get_upstream_features` | L4:F13412@26, k=10 → L3:F11774 (de=4.72) +9 more |
| 10 | `inspect_feature` ×7 | L0:5201, L0:6051, L0:8975, L0:2268, L0:9519, L0:10148, L0:2083 |
| 11 | `get_top_features` | token="", k=30 → 30 features; top: L4:10494 de=0.176 |
| 12 | `inspect_feature` ×10 | L0:8028, L0:15322, L0:4030, L0:10254, L0:16048, L0:8850, L0:3988, L0:15785, L6:11646, L4:11355 |
| 13 | `get_upstream_features` | L19:F1589@26, k=10 → L17:F7545 (de=10.38) +9 more |
| 14 | `get_upstream_features` | L4:F13412@10, k=10 → Emb:" weight"@9 (de=6.62) +9 more |

### Build

`build_circuit` → 29 nodes, 47 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 41,892 | 7,246 | 274,553 | 0 | $0.0377 | — | — |
| **Total** | | **41,892** | **7,246** | **274,553** | **0** | **$0.0377** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 33s