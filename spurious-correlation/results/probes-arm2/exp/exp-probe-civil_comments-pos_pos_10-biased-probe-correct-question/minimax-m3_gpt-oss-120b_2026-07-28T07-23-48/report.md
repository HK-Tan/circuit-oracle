# Circuit Oracle Report
**Date:** 2026-07-28 07:23:48 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_10 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven almost entirely by the mere presence of identity-group / race-related tokens (" race", " black", " people", " cops") through a shallow L0→L4→L6→probe pathway, rather than by features encoding toxicity, hostility, or the actual argumentative content of the sentence.

**Confidence:** 8

**Reasoning:** Tracing the top direct-effect features on the probe direction reveals a circuit anchored at identity-token embeddings:

- **Embedding drivers (L0):** The strongest single source is `Emb: " race" (pos 5)` feeding into L6:F3902 (direct_effect 11 at pos 6, 22.6 at pos 5) and into L2:F10509 (direct_effect 30.1, but *inhibitory*). The `Emb: " black" (pos 16)` and `Emb: " people" (pos 17)` embeddings are the top inputs to the L3 "black people" supernode (direct_effects 11.4 and 3.5). `Emb: " cops" (pos 8)` flows into L4:F117 (direct_effect 1.08). The actual toxicity-bearing phrases — "undue force", "helpless", "bad cops" — produce **no** unique upstream feature that is not also triggered by the race tokens.

- **Early-layer supernode `low_l0_token` (L0):** L0:F7820, F1823, F2961, F2848, F9026, F9076, F358 are generic identity-token detectors (e.g. F9026 on " race" pos 5, F9076 on " people" pos 17) and they funnel into both `inhib_race_pos5` and `early_identity_race`.

- **L2 inhibitory supernode:** L2:F10509 (direct_effect −0.49 to probe) is *suppressing* the probe based on the " race" token — a partial debiasing signal, but easily overwhelmed.

- **L3 "black people" supernode:** L3:F13061 (+0.19), F13493, F16373, F6517 all fire on positions 16-17 (" black"/" people") with direct positive effects on the probe. These are *purely identity-token* features, not sentiment features.

- **L4 supernode `early_identity_race`:** F117 is the strongest single contributor (direct_effect 0.27 at pos 6, 0.25 at pos 5, 0.24 at pos 17) and F5584 adds another 0.5 combined. Both fire on the identity tokens " race", " of", " black", and " people".

- **L6-7 supernode `mid_race_detector`:** F3902 is the **top single feature driving the probe** (direct_effect 0.59 at pos 6, 0.27 at pos 5), and its upstream trace is dominated by the " race" embedding (11) and L4 race detectors. F9228 (−0.21) and F8030 (−0.19) are weak suppressors of the same identity signal.

- **No toxicity / sentiment features anywhere in the top 15.** The features that win the probe are ones that activate on racial-identity vocabulary; features encoding the *content* of the sentence (e.g. "undue force", "helpless", the ironic/metalinguistic structure "not mentioning the race of the cops…") are absent from the top-k. A genuinely content-aware probe would route through features that encode critique, irony, or aggressive framing — none of which appear.

The circuit therefore confirms the user's concern: the probe relies on **spurious identity-group features** (" race", " black", " people" as standalone lexical triggers) rather than lexical or semantic features that actually encode the toxic/hostile content. The probe is essentially a race-mention detector, and the model's toxicity classification here is an artifact of that confound.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 6 | Mid-layer "race" identity-token detectors | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F3902](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) | 5 | Mid-layer "race" identity-token detectors | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3902) |
| [L6:F9228](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) | 6 | Mid-layer "race" identity-token detectors | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/9228) |
| [L7:F8030](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) | 6 | Mid-layer "race" identity-token detectors | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8030) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 5 | Early identity / race-token features (L3-4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 6 | Early identity / race-token features (L3-4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 17 | Early identity / race-token features (L3-4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L4:F5584](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) | 6 | Early identity / race-token features (L3-4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) |
| [L4:F5584](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) | 5 | Early identity / race-token features (L3-4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5584) |
| [L4:F11200](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11200) | 1 | Early identity / race-token features (L3-4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11200) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 17 | Early "black people" identity features (L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F13493](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13493) | 17 | Early "black people" identity features (L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13493) |
| [L3:F16373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) | 17 | Early "black people" identity features (L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/16373) |
| [L3:F6517](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) | 3 | Early "black people" identity features (L3) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6517) |
| [L2:F10509](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) | 5 | Inhibitory race-position features (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10509) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 5 | Inhibitory race-position features (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L2:F13158](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) | 16 | Inhibitory race-position features (L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13158) |
| [L0:F7820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7820) | 3 | Low-layer token-identity features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7820) |
| [L0:F1823](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1823) | 5 | Low-layer token-identity features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1823) |
| [L0:F2961](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) | 3 | Low-layer token-identity features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2961) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 6 | Low-layer token-identity features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L0:F9026](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) | 5 | Low-layer token-identity features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9026) |
| [L0:F9076](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9076) | 17 | Low-layer token-identity features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9076) |
| [L0:F358](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/358) | 17 | Low-layer token-identity features (L0) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/358) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L6:3902 de=0.586 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F3902@6` | ❌ error | — | — | Trace this feature upstream to identify what tokens/early-layer features it resp… |
| SA-2 | `L4:F117@17` | ❌ error | — | — | Trace this feature upstream to identify what tokens/early-layer features it resp… |
| SA-3 | `L2:F10509@5` | ❌ error | — | — | Trace this feature upstream. What does this inhibitory feature detect? Does it s… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F3902@6, k=10 → Emb:" race"@5 (de=11.00) +9 more |
| 2 | `get_upstream_features` | L4:F117@17, k=10 → Emb:" black"@16 (de=11.56) +9 more |
| 3 | `get_upstream_features` | L2:F10509@5, k=10 → Emb:" race"@5 (de=30.12) +9 more |
| 4 | `get_upstream_features` | L3:F13061@17, k=10 → Emb:" black"@16 (de=11.38) +9 more |
| 5 | `get_upstream_features` | L6:F3902@5, k=10 → Emb:" race"@5 (de=22.62) +9 more |
| 6 | `get_upstream_features` | L4:F5584@6, k=8 → Emb:" race"@5 (de=16.62) +7 more |

### Build

`build_circuit` → 13 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 14,089 | 3,812 | 29,553 | 0 | $0.0106 | — | — |
| **Total** | | **14,089** | **3,812** | **29,553** | **0** | **$0.0106** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 53s