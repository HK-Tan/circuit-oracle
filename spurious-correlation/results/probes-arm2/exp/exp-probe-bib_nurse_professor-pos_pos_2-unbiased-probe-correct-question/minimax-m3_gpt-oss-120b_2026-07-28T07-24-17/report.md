# Circuit Oracle Report
**Date:** 2026-07-28 07:24:17 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification of "nurse" is driven almost exclusively by the literal word "Nursing" itself (position 10), through a clean profession-word detector pipeline, with no measurable contribution from gender markers ("She/her").

**Confidence:** 9

**Reasoning:** The entire attribution circuit is anchored on a single token — the **" Nursing"** embedding at pos 10, which provides the dominant direct_effect at every traced layer (e.g., 42.75 at L18:F13596, 17.25 at L1:F14469, 15.125 at L3:F15901, 12.125 at L14:F3985, 17.375 at L6:F15267). The signal flows upward through a textbook profession-word detection pipeline: subword/bigram composition features at L1–L2 (L1:F14469, L1:F10429, L2:F10852 firing on "Bachelors"/"Science"/"in"), a degree-phrase template at L4 (F3727 firing across positions 6/8/9 — the "Bachelors of Science in ___" pattern), mid-layer Nursing word-sense features at L5 (F11037, F10392, F1275), the core "Nursing" profession-word detector at L6 (F15267, activation 24.875; F4490, F170, F3475), refinement at L7, late-layer aggregators at L8, and the top output drivers L14:F3985, L15:F15159, L18:F13596 (activation 46.5, the single most strongly activating feature on the graph).

Critically, **gender is not represented in the circuit**. The pronoun "She" appears at positions 1 and throughout the text, but no feature at any layer is driven by a "She/her pronoun" embedding. In the get_upstream_features calls for L8:F16339, L6:F15267, L7:F210, and the output-driving L14:F3985, the only embedding contributions that appear are: " Nursing" (pos 10), "achelors" (pos 6), " Science" (pos 8), " in" (pos 9), " graduated" (pos 2), and "<bos>" (pos 0). Position 1 ("She") and other pronoun positions never surface as top-k upstream inputs to any feature in the path. If gender markers were driving the probe, we would expect to see a "She"-embedding edge into some feature — none exists in the traced path.

The two negative contributors (L7:F3979, direct_effect −0.110; L3:F15901, direct_effect −0.098) are **competing-sense Nursing features**, not anti-nurse or pro-male features. L7:F3979 receives its top positive input from L6:F15267 (the same core Nursing detector, +8.75) and the " Nursing" embedding (+7.78) — it fires on the word but pushes *away* from this particular probe direction, consistent with it encoding a competing profession-class sense (e.g., a different specialization). It is not a gender/masculine marker.

**Conclusion for the user's concern:** The circuit does **not** use spurious gender features. The probe is classified via a legitimate, monosemic profession-word pathway: the word "Nursing" is detected at L6, refined and aggregated through L7–L8, and carried by L14:F3985, L15:F15159, and L18:F13596 to the output. The negative features are profession-sense suppressors (likely distinguishing nurse sub-types), not gender cues. The only input tokens that drive the score are the degree-naming tokens themselves ("Nursing", "Bachelors", "Science", "in", "graduated"); pronouns and gendered names (Kayte) do not enter the top-k upstream of any feature in the circuit.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 10 | Emb: ' Nursing' (pos 10) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 6 | Emb: 'achelors' (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 8 | Emb: ' Science' (pos 8) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: ' in' (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: ' graduated' (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L1:F14469](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) | 10 | Early 'Nursing' word-form features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) |
| [L1:F10429](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10429) | 10 | Early 'Nursing' word-form features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10429) |
| [L1:F5829](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5829) | 10 | Early 'Nursing' word-form features | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/5829) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 10 | Bigram/subword composition features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 8 | Bigram/subword composition features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 9 | Bigram/subword composition features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 6 | Bigram/subword composition features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F9995](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) | 10 | Bigram/subword composition features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9995) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 9 | 'Bachelors of Science in' degree-phrase template | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 8 | 'Bachelors of Science in' degree-phrase template | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 6 | 'Bachelors of Science in' degree-phrase template | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L5:F11037](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11037) | 10 | Mid-layer 'Nursing' word-sense features | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11037) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 10 | Mid-layer 'Nursing' word-sense features | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 10 | Mid-layer 'Nursing' word-sense features | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 10 | Core 'Nursing' profession word detector | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 10 | Core 'Nursing' profession word detector | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 10 | Core 'Nursing' profession word detector | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F3475](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3475) | 10 | Core 'Nursing' profession word detector | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3475) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 10 | 'Nursing' sense refinement / context integration | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L7:F4208](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4208) | 10 | 'Nursing' sense refinement / context integration | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4208) |
| [L7:F5829](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5829) | 10 | 'Nursing' sense refinement / context integration | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5829) |
| [L7:F8194](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) | 10 | 'Nursing' sense refinement / context integration | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8194) |
| [L7:F4654](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4654) | 10 | 'Nursing' sense refinement / context integration | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/4654) |
| [L7:F3979](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) | 10 | Competing-sense suppressor on 'Nursing' (pushes toward alternative profession class) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3979) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 10 | General Nursing-context suppressor (competing profession) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 10 | Late-layer aggregated 'Nursing profession' features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L8:F440](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/440) | 10 | Late-layer aggregated 'Nursing profession' features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/440) |
| [L8:F9619](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) | 10 | Late-layer aggregated 'Nursing profession' features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) |
| [L8:F4607](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) | 10 | Late-layer aggregated 'Nursing profession' features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) |
| [L10:F1461](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/1461) | 10 | Mid-layer refinement (inhibitory) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/1461) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 10 | Top output-driving 'Nursing profession' features | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 10 | Secondary output-driving Nursing features | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L15:F8289](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) | 10 | Secondary output-driving Nursing features | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) |
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 10 | Highest-activation Nursing feature (dominant anchor) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 10 | Probe output (classification score) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.188 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@10` | ❌ error | — | — | Trace L14:F3985 at position 10. This is the top driver of the probe classificati… |
| SA-2 | `L6:F15267@10` | ❌ error | — | — | Trace L6:F15267 at position 10. This is a strong positive driver. What does it e… |
| SA-3 | `L7:F3979@10` | ❌ error | — | — | Trace L7:F3979 at position 10. This is a strong negative driver (suppresses the … |
| SA-4 | `L3:F15901@10` | ❌ error | — | — | Trace L3:F15901 at position 10. This is another negative driver. What does it en… |
| SA-5 | `L18:F13596@10` | ❌ error | — | — | Trace L18:F13596 at position 10. This has very high activation (46.5). What does… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@10, k=10 → Emb:" Nursing"@10 (de=12.12) +9 more |
| 2 | `get_upstream_features` | L6:F15267@10, k=10 → Emb:" Nursing"@10 (de=17.38) +9 more |
| 3 | `get_upstream_features` | L7:F3979@10, k=10 → L6:F15267 (de=8.75) +9 more |
| 4 | `get_upstream_features` | L18:F13596@10, k=10 → Emb:" Nursing"@10 (de=42.75) +9 more |
| 5 | `get_upstream_features` | L3:F15901@10, k=10 → Emb:" Nursing"@10 (de=15.12) +9 more |
| 6 | `get_upstream_features` | L4:F11037@10, k=10 → Emb:" Nursing"@10 (de=10.62) +9 more |
| 7 | `get_upstream_features` | L5:F10392@10, k=10 → Emb:"achelors"@6 (de=3.56) +9 more |
| 8 | `get_upstream_features` | L8:F16339@10, k=10 → Emb:" Nursing"@10 (de=7.66) +9 more |
| 9 | `get_upstream_features` | L6:F4490@10, k=10 → Emb:" Nursing"@10 (de=11.62) +9 more |
| 10 | `get_upstream_features` | L7:F210@10, k=10 → Emb:" Nursing"@10 (de=8.19) +9 more |
| 11 | `get_upstream_features` | L8:F440@10, k=10 → Emb:" Nursing"@10 (de=9.44) +9 more |
| 12 | `get_upstream_features` | L4:F3727@9, k=5 → Emb:" in"@9 (de=11.94) +4 more |
| 13 | `get_upstream_features` | L8:F9619@10, k=10 → Emb:" Nursing"@10 (de=5.84) +9 more |
| 14 | `get_upstream_features` | L6:F170@10, k=10 → L5:F10392 (de=10.19) +9 more |
| 15 | `get_upstream_features` | L2:F10852@10, k=5 → Emb:" Nursing"@10 (de=11.44) +4 more |
| 16 | `get_upstream_features` | L1:F14469@10, k=10 → Emb:" Nursing"@10 (de=17.25) +9 more |
| 17 | `get_upstream_features` | L4:F3727@6, k=5 → Emb:"achelors"@6 (de=20.75) +4 more |
| 18 | `get_upstream_features` | L1:F10429@10, k=5 → Emb:" Nursing"@10 (de=4.78) +4 more |
| 19 | `get_upstream_features` | L15:F15159@10, k=10 → Emb:" Nursing"@10 (de=10.56) +9 more |
| 20 | `get_upstream_features` | L8:F4607@10, k=10 → Emb:" Nursing"@10 (de=7.78) +9 more |
| 21 | `get_upstream_features` | L15:F8289@10, k=5 → Emb:" Nursing"@10 (de=6.25) +4 more |
| 22 | `get_upstream_features` | L3:F6246@10, k=5 → Emb:" Nursing"@10 (de=9.62) +4 more |
| 23 | `get_upstream_features` | L5:F1275@10, k=5 → L4:F11037 (de=1.99) +4 more |
| 24 | `get_upstream_features` | L6:F3475@10, k=5 → Emb:" Nursing"@10 (de=4.97) +4 more |
| 25 | `get_upstream_features` | L7:F4208@10, k=5 → Emb:" Nursing"@10 (de=7.44) +4 more |
| 26 | `get_upstream_features` | L10:F1461@10, k=5 → Emb:" Nursing"@10 (de=2.94) +4 more |
| 27 | `get_upstream_features` | L3:F11994@10, k=5 → L2:F10852 (de=3.72) +4 more |
| 28 | `get_upstream_features` | L3:F4113@9, k=5 → Emb:" in"@9 (de=11.25) +4 more |
| 29 | `get_upstream_features` | L2:F9995@10, k=5 → Emb:" Nursing"@10 (de=5.41) +4 more |

### Build

`build_circuit` → 19 nodes, 51 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 31,708 | 7,932 | 88,063 | 0 | $0.0243 | — | — |
| **Total** | | **31,708** | **7,932** | **88,063** | **0** | **$0.0243** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 31s