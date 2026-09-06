# Circuit Oracle Report
**Date:** 2026-07-28 07:23:54 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mixture of strong suppressor circuits anchored on the profession-indicating tokens (" report" and " top") and several direct positive contributions from low-layer token-embedding features — most notably the **male pronoun "His"** at position 1 and the function word " to" at position 3 — rather than by a single coherent profession-feature pathway.

**Confidence:** 6

**Reasoning:**

The circuit has two distinct regimes and the user's concern is well-founded.

**Regime 1 — The profession-anchored suppressors (the "genuine" path, but inverted).** The token ` report` (pos 21) is the dominant signal. Its embedding feeds a tall stack of features at the same position: L0:F1579 → L5:F12586 → L7:F13646 → L8:F8855/F8437 → L15:F2579 → L18:F14663 (direct_effect 51.5 from the ` report` embed). But L18:F14663 then feeds **L14:F4420 (direct_effect +2.53 → 14.3 to the logit, but L14:F4420's own direct effect on the probe is −0.146) and L19:F2486 (direct_effect +2.84 → fires at positions 21, 22, 26, 27, 28, 29 with cumulative direct_effect ≈ −0.45)**. So the model *recognizes* "report" + "news organizations" as a profession-bearing context (the L8/L15/L18 "report" detectors all fire with high activations 16.75/36.75/74), but the late-layer features that get excited are net **suppressors** of the probe's profession score. L19:F2486 is the largest single contributor and it suppresses. L20:F8433 (activation 39.75 at " top", pos 26) also directly suppresses (−0.062). Meanwhile L16:F8642 is a mild anti-inhibitor (+0.05-ish inside the suppressor chain). The net effect of this entire "report / news organizations" path is to push the probe score **down** — which is suspicious on its own: a profession probe should not be suppressed by its own clearest profession evidence, suggesting the probe direction itself may be partially misaligned, or the "top news organizations" surface form is being down-weighted.

**Regime 2 — The spurious positive contributions (the user's concern).** Independently of the report-context path, several early-layer token-embedding features contribute positively to the probe *with no profession content at all*:
- **L0:F8964 on "His" (pos 1): +0.079** — the largest single positive direct effect, and it traces purely to the `His` embedding (direct_effect 13.69 from the embed, no further upstream signal). This is a male-gender-pronoun signal.
- **L0:F8444 on " to" (pos 3): +0.076** — pure function-word signal (embed direct_effect 39.5).
- **L0:F14287 on " see" (pos 4): +0.064**, **L0:F2011/F13948 on " desire" (pos 2): ~+0.05 each**, **L4:F11898/L7:F3085 on " world" (pos 6): +0.054/+0.051**.

Summing just the known positives (≈ 0.08 + 0.08 + 0.06 + 0.05 + 0.05 + 0.05 + 0.05 ≈ **+0.42**) versus the known negatives from the suppressor path (L19:F2486 ≈ −0.45, L14:F4420 ≈ −0.15, L20:F8433 ≈ −0.06 ≈ **−0.66**), the net probe score is slightly negative — but the *positive* score is being carried entirely by the male pronoun, the preposition "to", and generic content words. None of the positive contributors encode a profession. The genuine profession evidence (the "report" / "news organizations" stack) is actively being *cancelled* by the L14/L19/L20 suppressors.

**Conclusion regarding the user's concern:** The concern is correct but slightly understated. The probe is not merely using gender markers alongside genuine profession indicators — the suppressor features on the profession tokens (L14:F4420, L19:F2486, L20:F8433) are pushing the profession-evidence pathway *below zero*, leaving the male pronoun "His", the preposition "to", and a few generic content words as the dominant positive drivers. This is a textbook spurious-feature failure: the classifier's positive evidence is gender and function-word content, while the actual profession evidence is being filtered out by late-layer suppressor features.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | L19:F2486 — report-context suppressor (pos 21/22/26-29) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 22 | L19:F2486 — report-context suppressor (pos 21/22/26-29) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 26 | L19:F2486 — report-context suppressor (pos 21/22/26-29) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 27 | L19:F2486 — report-context suppressor (pos 21/22/26-29) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 28 | L19:F2486 — report-context suppressor (pos 21/22/26-29) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 29 | L19:F2486 — report-context suppressor (pos 21/22/26-29) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | L14:F4420 — report-context suppressor (pos 21/22) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 22 | L14:F4420 — report-context suppressor (pos 21/22) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L20:F8433](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) | 26 | L20:F8433 — top-news suppressor (pos 26) | — | [view](https://neuronpedia.org/gemma-2-2b/20-gemmascope-transcoder-16k/8433) |
| [L16:F8642](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) | 21 | L16:F8642 — report-suppressor inhibitor (anti-inhibitory) (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/8642) |
| [L19:F14973](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/14973) | 26 | L19:F14973 — top-pos feature (pos 26) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/14973) |
| [L18:F14663](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) | 21 | L18:F14663 — report-activator (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14663) |
| [L15:F2579](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) | 21 | L15:F2579 — report-activator (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2579) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | L8:F8855 / L8:F8437 — report-context detectors (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | L8:F8855 / L8:F8437 — report-context detectors (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | L7:F13646 — report-token detector (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L5:F12586](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12586) | 21 | L5:F12586 — report-token detector (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12586) |
| [L0:F1579](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1579) | 21 | L0:F1579 — "report" embed-feature (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1579) |
| [L0:F12801](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12801) | 21 | L0:F1579 — "report" embed-feature (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12801) |
| [L0:F8964](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) | 1 | L0:F8964 — "His" male-pronoun feature (pos 1, +0.079 direct_effect) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8964) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 3 | L0:F8444 — "to" function-word feature (pos 3, +0.076) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F14287](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) | 4 | L0:F14287 — "see" content-verb feature (pos 4, +0.064) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14287) |
| [L0:F2011](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) | 2 | L0:F2011 / F13948 — "desire" feature (pos 2, +0.05 each) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2011) |
| [L0:F13948](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) | 2 | L0:F2011 / F13948 — "desire" feature (pos 2, +0.05 each) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) |
| [L4:F11898](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) | 6 | L4:F11898 / L7:F3085 — "world" content-word features (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11898) |
| [L7:F3085](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3085) | 6 | L4:F11898 / L7:F3085 — "world" content-word features (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3085) |
| [L0:F2203](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) | 6 | L0:F2203 / L5:F771 — "world" negative-direction features (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2203) |
| [L5:F771](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) | 6 | L0:F2203 / L5:F771 — "world" negative-direction features (pos 6) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/771) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L14:4420 de=-0.145 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L19:F2486@21` | ❌ error | — | — | Trace the path from L19:F2486 at position 21. This is a strongly negative (suppr… |
| SA-2 | `L14:F4420@21` | ❌ error | — | — | Trace the path from L14:F4420 at position 21. This is a strongly negative (suppr… |
| SA-3 | `L0:F8964@1` | ❌ error | — | — | Trace the path from L0:F8964 at position 1 (the token "His"). This is a strongly… |
| SA-4 | `L0:F8444@3` | ❌ error | — | — | Trace the path from L0:F8444 at position 3 (the token "to"). Determine what this… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L19:F2486@21, k=15 → L14:F4420 (de=14.31) +14 more |
| 2 | `get_upstream_features` | L14:F4420@21, k=15 → Emb:" report"@21 (de=5.22) +14 more |
| 3 | `get_upstream_features` | L0:F8964@1, k=10 → Emb:"His"@1 (de=13.69) +9 more |
| 4 | `get_upstream_features` | L0:F8444@3, k=10 → Emb:" to"@3 (de=39.50) +9 more |
| 5 | `get_upstream_features` | L8:F8855@21, k=10 → Emb:" report"@21 (de=12.06) +9 more |
| 6 | `get_upstream_features` | L8:F8437@21, k=10 → Emb:" report"@21 (de=5.75) +9 more |
| 7 | `get_upstream_features` | L7:F13646@21, k=10 → Emb:" report"@21 (de=7.22) +9 more |
| 8 | `get_upstream_features` | L15:F2579@21, k=10 → Emb:" report"@21 (de=38.25) +9 more |
| 9 | `get_upstream_features` | L5:F12586@21, k=8 → Emb:" report"@21 (de=32.25) +7 more |
| 10 | `get_upstream_features` | L3:F10846@21, k=8 → Emb:" report"@21 (de=24.75) +7 more |
| 11 | `get_upstream_features` | L4:F661@21, k=8 → Emb:" report"@21 (de=14.38) +7 more |
| 12 | `get_upstream_features` | L4:F6696@21, k=8 → Emb:" report"@21 (de=21.88) +7 more |
| 13 | `get_upstream_features` | L2:F11175@21, k=8 → Emb:" report"@21 (de=32.50) +7 more |
| 14 | `get_upstream_features` | L1:F14511@21, k=8 → Emb:" report"@21 (de=20.62) +7 more |
| 15 | `get_upstream_features` | L4:F11898@6, k=8 → Emb:" world"@6 (de=35.25) +7 more |
| 16 | `get_upstream_features` | L7:F3085@6, k=8 → Emb:" world"@6 (de=9.56) +7 more |
| 17 | `get_upstream_features` | L0:F14287@4, k=8 → Emb:" see"@4 (de=25.12) +7 more |
| 18 | `get_upstream_features` | L0:F2011@2, k=8 → Emb:" desire"@2 (de=12.94) +7 more |
| 19 | `get_upstream_features` | L0:F13948@2, k=8 → Emb:" desire"@2 (de=14.44) +7 more |
| 20 | `get_upstream_features` | L0:F2203@6, k=8 → Emb:" world"@6 (de=18.25) +7 more |
| 21 | `get_upstream_features` | L20:F8433@26, k=8 → Emb:" top"@26 (de=5.69) +7 more |
| 22 | `get_upstream_features` | L5:F771@6, k=8 → Emb:" see"@4 (de=6.16) +7 more |
| 23 | `get_upstream_features` | L0:F12801@21, k=8 → Emb:" to"@20 (de=6.94) +7 more |
| 24 | `get_upstream_features` | L1:F12838@21, k=8 → Emb:" report"@21 (de=13.81) +7 more |
| 25 | `get_upstream_features` | L0:F1579@21, k=6 → Emb:" report"@21 (de=24.00) +5 more |
| 26 | `get_upstream_features` | L1:F8335@21, k=6 → Emb:" report"@21 (de=14.38) +5 more |
| 27 | `get_upstream_features` | L4:F6653@6, k=6 → Emb:" world"@6 (de=27.25) +5 more |
| 28 | `get_upstream_features` | L16:F8642@21, k=8 → L14:F4420 (de=10.50) +7 more |
| 29 | `get_upstream_features` | L17:F5218@26, k=8 → Emb:" report"@21 (de=2.09) +7 more |
| 30 | `get_upstream_features` | L19:F14973@26, k=8 → Emb:" top"@26 (de=7.19) +7 more |
| 31 | `get_upstream_features` | L18:F14663@21, k=8 → Emb:" report"@21 (de=51.50) +7 more |
| 32 | `get_upstream_features` | L1:F5893@6, k=6 → Emb:" world"@6 (de=26.38) +5 more |

### Build

`build_circuit` → 25 nodes, 38 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 43,432 | 7,574 | 92,958 | 0 | $0.0277 | — | — |
| **Total** | | **43,432** | **7,574** | **92,958** | **0** | **$0.0277** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 31s