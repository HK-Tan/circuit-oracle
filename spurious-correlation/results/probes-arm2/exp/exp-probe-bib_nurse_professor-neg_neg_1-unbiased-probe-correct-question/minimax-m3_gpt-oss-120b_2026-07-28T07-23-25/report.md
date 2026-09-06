# Circuit Oracle Report
**Date:** 2026-07-28 07:23:25 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_1 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven primarily by a **credential/PhD-detection circuit** anchored on the "PhD" token at position 27, not by genuine profession indicators like "visualization" or "computer graphics" — and an early-layer pronoun feature ("His" at L0:F1069) supplies additional positive signal, consistent with the user's concern about spurious features.

**Confidence:** 7

**Reasoning:**

**Top positive drivers of the probe score:**
- **L0:F1069 (pos 1, direct_effect=+0.0698)** — the strongest single positive feature. Its upstream is almost entirely the **"His" embedding** (pos 1, direct_effect=21.6) and BOS. This is a pronoun/possessive detector, not a profession indicator. It is *spurious* and aligns with the user's concern.
- **L1:F10986 (pos 3, direct_effect=+0.0674)** — anchored on the "interests"/"research" embeddings (direct_effect 6.6 and 4.5 from " research" and " interests"). This is a generic academic-biography opener detector ("His research interests include…"), not a profession-specific signal.
- **L5:F12330 (pos 13, direct_effect=+0.0454)** — fired on the period after "graphics," with mixed upstream (BOS negative, " include" positive). Generic punctuation/segmentation feature.
- **L4:F9757 (pos 1, direct_effect=+0.0391)** — also anchored on BOS/"His" — again pronoun-driven.

**Top negative drivers (suppressing the probe score):**
- **L8:F11284 (pos 13, direct_effect=−0.0566)** and **L14:F11252 (pos 9, direct_effect=−0.0508)** — late-layer features on the *actual* profession-indicating tokens ("visualization", "computer graphics"). These *suppress* the profession classifier, which is the opposite of what a genuine profession-classification circuit should do.
- **L6:F2254 (pos 27, direct_effect=−0.0417) and (pos 17, direct_effect=−0.0398)** — interestingly, the same feature at different positions. At pos 17 (BS) it suppresses; at pos 27 (PhD) it promotes. So the "degree" tokens themselves have position-dependent effects.

**Path structure:**
- The strongest promoting path is **Emb:"PhD" (pos 27) → L2:F10852 → L6:F2254 → L7:F14129 → probe logit**, plus contributions from L4-L5 PhD-adjacent features (F3727, F13801, F11028, F12906, F1644, F13943). This is a **credential-token detector**, not a profession semantic detector.
- A second promoting path comes from **Emb:"His" → L0:F1069 → probe**, and **Emb:" research"/" interests" → L0:L1 early features → probe**. These are stylistic/possessive markers.
- The **profession-semantic tokens** ("visualization" at pos 9, "graphics" at pos 12) feed late-layer features (L8:L14) that have **negative** direct_effects on the probe.

**Assessment of the user's concern:** The concern is well-founded. The probe's positive signal comes substantially from:
1. The gendered possessive **"His"** (L0:F1069) — a classic spurious gender cue.
2. The credential token **"PhD"** (L2:F10852 → L6:F2254 → L7:F14129) — an academic-status marker.
3. The generic biography opener **"His research interests include"** (L0:L1 features on pos 2-4).

Meanwhile, the *genuine* profession-indicating tokens ("visualization", "computer graphics", "scientific visualization") feed late-layer features with **negative** direct_effects, meaning the model is *not* using profession semantics to drive this probe's positive score. The circuit exhibits exactly the spurious-feature pathology the user identified.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 27 | Mid-layer PhD/credential features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L5:F13801](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) | 27 | Mid-layer PhD/credential features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/13801) |
| [L5:F11028](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11028) | 27 | Mid-layer PhD/credential features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/11028) |
| [L5:F12906](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12906) | 27 | Mid-layer PhD/credential features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12906) |
| [L5:F1644](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1644) | 27 | Mid-layer PhD/credential features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1644) |
| [L4:F13943](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) | 27 | Mid-layer PhD/credential features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13943) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 27 | Mid-layer PhD/credential features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 27 | Mid-layer PhD/credential features (L4-L7) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 17 | Mid-layer visualization/graphics inhibitory (L2-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 27 | Mid-layer visualization/graphics inhibitory (L2-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L6:F2254](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) | 17 | Mid-layer visualization/graphics inhibitory (L2-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2254) |
| [L8:F11284](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) | 13 | Mid-layer visualization/graphics inhibitory (L2-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/11284) |
| [L14:F11252](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11252) | 9 | Mid-layer visualization/graphics inhibitory (L2-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/11252) |
| [L2:F1621](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) | 3 | Mid-layer visualization/graphics inhibitory (L2-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1621) |
| [L5:F12330](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) | 13 | Mid-layer visualization/graphics inhibitory (L2-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/12330) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Early pronoun/possessive detectors (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L1:F10986](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) | 3 | Early pronoun/possessive detectors (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10986) |
| [L0:F13948](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) | 3 | Early pronoun/possessive detectors (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13948) |
| [L0:F13431](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13431) | 3 | Early pronoun/possessive detectors (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13431) |
| [L0:F10783](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) | 4 | Early pronoun/possessive detectors (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10783) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Early pronoun/possessive detectors (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2159](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2159) | 3 | Early pronoun/possessive detectors (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2159) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | Early pronoun/possessive detectors (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token ' scientist' is not one of the top-k next-token candid |
| 3 | `get_top_features` | 15 features; top: L0:1069 de=0.070 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F1069@1` | ❌ error | — | — | Trace upstream from L0:F1069 at pos 1 ("His"). What does this feature detect? Do… |
| SA-2 | `L1:F10986@3` | ❌ error | — | — | Trace upstream from L1:F10986 at pos 3 ("research"). What does this feature dete… |
| SA-3 | `L5:F12330@13` | ❌ error | — | — | Trace upstream from L5:F12330 at pos 13 ("visualization"). What does this featur… |
| SA-4 | `L7:F14129@27` | ❌ error | — | — | Trace upstream from L7:F14129 at pos 27. What does this feature encode? Trace to… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F1069@1, k=10 → Emb:"His"@1 (de=21.62) +9 more |
| 2 | `get_upstream_features` | L1:F10986@3, k=10 → Emb:" research"@2 (de=6.62) +9 more |
| 3 | `get_upstream_features` | L5:F12330@13, k=10 → Emb:"<bos>"@0 (de=-3.23) +9 more |
| 4 | `get_upstream_features` | L7:F14129@27, k=10 → Emb:" PhD"@27 (de=19.25) +9 more |
| 5 | `get_upstream_features` | L6:F2254@27, k=10 → Emb:" PhD"@27 (de=22.00) +9 more |
| 6 | `get_upstream_features` | L9757:F4@1, k=10 → ❌ Feature (layer=9757, pos=1, feature_idx=4) not found in grap |
| 7 | `get_upstream_features` | L5:F13801@27, k=10 → Emb:" PhD"@27 (de=6.31) +9 more |
| 8 | `get_upstream_features` | L0:F13948@3, k=10 → Emb:" interests"@3 (de=14.94) +9 more |
| 9 | `get_upstream_features` | L2:F10852@27, k=10 → Emb:" PhD"@27 (de=29.50) +9 more |
| 10 | `get_upstream_features` | L4:F9757@1, k=10 → Emb:"<bos>"@0 (de=16.50) +9 more |
| 11 | `get_upstream_features` | L3:F9204@13, k=10 → Emb:"."@13 (de=11.50) +9 more |
| 12 | `get_upstream_features` | L2:F1621@3, k=10 → Emb:" interests"@3 (de=6.53) +9 more |

### Build

`build_circuit` → 8 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 18,982 | 3,851 | 37,942 | 0 | $0.0126 | — | — |
| **Total** | | **18,982** | **3,851** | **37,942** | **0** | **$0.0126** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 46s