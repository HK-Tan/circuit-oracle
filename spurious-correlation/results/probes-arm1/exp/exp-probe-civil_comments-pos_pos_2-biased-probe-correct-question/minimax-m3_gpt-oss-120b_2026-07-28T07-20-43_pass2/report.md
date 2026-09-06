# Circuit Oracle Report
**Date:** 2026-07-28 07:20:43 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a coherent content-based circuit that detects explicit racial/ethnic identity tokens ("white", "Hispanic") and routes them through successive race-concept features into the output — i.e., the circuit *does* use the actual prompt content (lexical race references) rather than spurious abstract "identity group" shortcuts.

**Confidence:** 7

**Reasoning:**

The top positive drivers are L6:F3902 (de=0.57) and L2:F13158 (de=0.52) at positions 4 and 7 — the two race tokens. Subagent tracing of L6:F3902 shows it is a "terms referring to race and ethnicity" feature (frac_nonzero=0.018, promoted tokens include "minorities", "ethnicity", "Hispanic") whose signal flows:

**Emb "Hispanic" (pos 7) + Emb "white" (pos 4) → L2:F13158** (race/ethnicity detector, frac=0.01, promotes "ethnic", "Hispanic", "Latino", "Muslim") **→ L4:F117** (race/racism/social-justice aggregator, frac=0.012, promotes "racial", "racist", "racism") **→ L6:F3902** (top driver) **→ output logit.**

Every feature along this path is a *content* detector for race/ethnicity vocabulary, and every one traces back to the concrete input tokens "white" (pos 4) and "Hispanic" (pos 7) via embedding nodes with very large direct effects (Emb "white"→L4:F117 de=14.75; Emb "white"→L2:F585 de=29.4; Emb "white"→L2:F13158 de=13.1). L2:F585 is literally labeled "the word 'white'" (frac=0.005). L0:F16013/F1708 are color-word detectors activated by "white" as a color word — these are lexical, not abstract.

The negative drivers (L0:F2458 "was" de=-0.66; L0:F880 "it" de=-0.23) are equally concrete: pure stopword/function-word detectors that push *against* the probe classification. There is no abstract "identity group" meta-feature upstream of the race tokens — the race signal *originates* at the identity-token embeddings and propagates upward through increasingly abstract race-concept features.

**Caveat on the user's concern:** The features in this circuit are specifically tuned to *named racial/ethnic identity tokens* (frac_nonzero ≈ 0.01–0.02, promoting "Hispanic", "ethnic", "racial", etc.). While these are lexically grounded in the input rather than a learned spurious abstraction, a probe that classifies toxicity based on *mere presence of race terms* (rather than on toxic *context* around them) is itself a form of bias — the tokens that drive the score are the same tokens the model would flag whenever race is mentioned, regardless of whether the surrounding text is toxic. The circuit is "content-based" in the sense that the features are real lexical/semantic detectors, but the *probe direction* appears to equate "racial identity terms present" with "toxic," which is a substantive fairness concern even if the internal features are not themselves spurious shortcuts.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F16013](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) | 4 | L0: color / "white" lexical detector | mentions of the color blue, and perhaps colors in general or the components of a graphic image | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16013) |
| [L0:F1708](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1708) | 4 | L0: color / "white" lexical detector | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1708) |
| [L2:F585](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) | 4 | L2: "white" word detector | the word "white", often in association with "dwarf" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/585) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 4 | L2: race/ethnicity term detector | words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 7 | L2: race/ethnicity term detector | words about race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 4 | L4: race/racism/social-justice amplifier | terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 7 | L4: race/racism/social-justice amplifier | terms related to race, racism, and social justice, with a particular focus on terms related to Black people | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F10174](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10174) | 7 | L4: race/racism/social-justice amplifier | words referring to racial and/or supernatural identity | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10174) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 7 | L6: race/ethnicity concept feature (top driver) | terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 4 | L6: race/ethnicity concept feature (top driver) | terms referring to race and ethnicity | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L0:F2458](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) | 3 | L0: "was" (top negative driver) |  the word "was" and sometimes "were." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2458) |
| [L0:F880](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) | 8 | L0: "it" pronoun (top negative driver) |  references to the pronoun "it", and sometimes "that", suggesting observation of the subject of a discussion | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/880) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2458 de=-0.660 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@7` | ✅ reported | 6 | 27 | Trace L6:F3902 upstream. This is the top positive driver (direct_effect=0.57) fo… |
| SA-2 | `L2:F13158@4` | ✅ reported | 4 | 3 | Trace L2:F13158 upstream. This is a major positive driver (direct_effect=0.52) f… |
| SA-3 | `L4:F117@4` | ❌ error | — | — | Trace L4:F117 upstream. Strong positive driver (direct_effect=0.51) at pos 4. Wh… |
| SA-4 | `L0:F2458@3` | ❌ error | — | — | Trace L0:F2458 upstream. This is the TOP negative driver (direct_effect=-0.66) a… |

<details>
<summary><b>SA-1</b> — tool trace (12 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L6, F3902 | " terms referring to race and ethnicity" |
| 2 | `get_upstream_features` | L6:F3902@7, k=10 | Emb:" Hispanic"@7 (de=12.81) +9 more |
| 3 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 4 | `get_upstream_features` | L2:F13158@7, k=10 | Emb:" Hispanic"@7 (de=11.12) +9 more |
| 5 | `inspect_feature` | L4, F117 | " terms related to race, racism, and social justice, with a particular " |
| 6 | `get_upstream_features` | L4:F117@7, k=10 | Emb:" white"@4 (de=6.00) +9 more |
| 7 | `inspect_feature` | L1, F12717 | " words or phrases related to education" |
| 8 | `inspect_feature` | L4, F10174 | " words referring to racial and/or supernatural identity" |
| 9 | `get_upstream_features` | L1:F12717@7, k=10 | Emb:" Hispanic"@7 (de=9.06) +9 more |
| 10 | `inspect_feature` | L0, F1847 | "scientific terms and experimental details related to biological and ch" |
| 11 | `get_upstream_features` | L0:F1847@7, k=5 | Emb:" Hispanic"@7 (de=5.66) +4 more |
| 12 | `get_upstream_features` | L4:F10174@7, k=10 | Emb:" Hispanic"@7 (de=4.03) +9 more |

**Findings:** The probe's strongest upstream driver, L6:F3902, is a race/ethnicity detector. Its signal originates from the input token embedding "Hispanic" (position 7) and, to a lesser extent, the token "white" (position 4). The embedding excites a low‑level race-word feature L2:F13158, which in turn feeds into mid‑level race‑social‑justice features (L4:F117 and L4:F10174). These mid‑level features amplify th…

</details>

<details>
<summary><b>SA-2</b> — tool trace (5 calls)</summary>

| # | Tool | Input | Output |
|---|------|-------|--------|
| 1 | `inspect_feature` | L2, F13158 | " words about race and ethnicity" |
| 2 | `get_upstream_features` | L2:F13158@4, k=10 | Emb:" white"@4 (de=13.12) +9 more |
| 3 | `inspect_feature` | L1, F7821 | " mentions of computer fans." |
| 4 | `inspect_feature` | L0, F16013 | " mentions of the color blue, and perhaps colors in general or the comp" |
| 5 | `inspect_feature` | L1, F13646 | " text discussing social justice issues" |

**Findings:** The target feature L2:F13158 is a race/ethnicity detector that fires strongly on the token "white". Its strongest upstream driver is the raw token embedding for " white" (direct_effect 13.125), confirming that the signal originates from the input word itself rather than a hidden spurious cue. Additional upstream contributors include a generic color detector (L0:F16013) and a social‑justice discour…

</details>

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L4:F117@4, k=8 → Emb:" white"@4 (de=14.75) +7 more |
| 2 | `get_upstream_features` | L0:F2458@3, k=8 → Emb:" was"@3 (de=36.75) +7 more |
| 3 | `get_upstream_features` | L0:F880@8, k=8 → Emb:" it"@8 (de=42.50) +7 more |
| 4 | `get_upstream_features` | L2:F585@4, k=8 → Emb:" white"@4 (de=29.38) +7 more |
| 5 | `inspect_feature` ×4 | L0:2458, L0:880, L2:585, L2:1708 |

### Build

`build_circuit` → 11 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 25,427 | 3,275 | 44,005 | 0 | $0.0142 | — | — |
| SA-2 | openai/gpt-oss-120b | 37,503 | 3,545 | 7,584 | 0 | $0.0079 | ✅ 4F/3E | Trace L2:F13158 upstream. This is a major positive driver (d… |
| SA-1 | openai/gpt-oss-120b | 180,799 | 16,242 | 7,648 | 0 | $0.0370 | ✅ 6F/27E | Trace L6:F3902 upstream. This is the top positive driver (di… |
| **Total** | | **243,729** | **23,062** | **59,237** | **0** | **$0.0590** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 6m 23s