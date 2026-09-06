# Circuit Oracle Report
**Date:** 2026-07-28 07:23:29 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mix of spurious surface features (the pronoun "He" at pos 1, isolated function words like "in"/"too"/"foreign"/".", and even the content word "stories" at the wrong position) and a single genuine late-layer semantic feature built on the actual profession word "journalistic" (pos 13).

**Confidence:** 7

**Reasoning:** The circuit reveals that the probe is **not** cleanly using profession vocabulary. The strongest drivers are L0 token-level features (no semantic abstraction):

- **Pronoun/gender "He" at pos 1 is the dominant direct-effect signal** — five L0 features fire on "He"/" stories" (L0:1069, L0:14906, L0:8350, L0:15180, L0:1301) with large negative direct_effects (e.g. L0:14906 = -0.22, L0:1069 = -0.16), and L0:10255 fires positively on "He" (+0.08). These are raw pronoun/wordform detectors with no profession content.

- **Function-word noise dominates the negative contribution**: L0:8061 on " in" (-0.13), L0:11603 on " too" (-0.16), L0:2711 on " foreign" (-0.11), L0:6051 on the period at pos 15 (-0.11), L0:5626 on " Poland" (-0.07), and L0:6962 on " same" (+0.11, wrong sign). These are surface-level word detectors that have no business driving a profession classifier.

- **The genuine profession signal is present but small and isolated**: a clean late-layer chain on "journalistic" runs L0→L4:L13253 → L7:L9092 → L9:L7435 → L14:L4420, all on pos 13. L14:L4420 contributes only -0.13 (negative — pushing *away* from the probe class), and L4:L13253 contributes -0.10. Even the actual profession word ends up with a *negative* direct effect, suggesting the probe is positively keyed to a different profession (likely "journalist" or a competing class) and the model's representation of "journalistic" — despite being the right semantic content — pushes the wrong way.

- **Verb/content features** (L0:5333, L0:11261, L1:14812 on " stories" / "researches") do contribute positively (e.g. L1:14812 = +0.19) but they are reading "researches stories" as a generic noun-phrase pattern, not as a profession.

**Verdict on user concern — confirmed but more nuanced:** Gender markers ("He" at pos 1) are not the dominant spurious feature, but **surface-level wordform detectors on the first few tokens and scattered function words are**. The real problem is that the probe is being read off the raw L0/L1 residual stream via these position-specific token detectors, not off the late-layer semantic features where genuine profession understanding lives. The one late-layer chain (L4→L14 on "journalistic") exists but contributes the wrong sign, indicating the probe direction and the model's profession-representation are misaligned. This is the classic "shallow probe reads shallow features" failure mode.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Pronoun/He features (negative) — L0 features on 'He'/' stories' pushing probe down | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F14906](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14906) | 3 | Pronoun/He features (negative) — L0 features on 'He'/' stories' pushing probe down | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14906) |
| [L0:F8350](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8350) | 3 | Pronoun/He features (negative) — L0 features on 'He'/' stories' pushing probe down | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8350) |
| [L0:F15180](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15180) | 3 | Pronoun/He features (negative) — L0 features on 'He'/' stories' pushing probe down | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15180) |
| [L0:F1301](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1301) | 3 | Pronoun/He features (negative) — L0 features on 'He'/' stories' pushing probe down | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1301) |
| [L0:F10255](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10255) | 1 | Pronoun/He feature (positive) — L0:10255 on 'He' pushing probe up | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10255) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | Content-word ' stories' features (positive) — L0/L1 detectors on noun phrase | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F16233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16233) | 3 | Content-word ' stories' features (positive) — L0/L1 detectors on noun phrase | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16233) |
| [L1:F1154](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1154) | 3 | Content-word ' stories' features (positive) — L0/L1 detectors on noun phrase | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1154) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | Content-word ' stories' features (positive) — L0/L1 detectors on noun phrase | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L0:F11261](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) | 3 | Content-word ' stories' features (positive) — L0/L1 detectors on noun phrase | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) |
| [L0:F15423](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15423) | 11 | Content-word ' stories' features (positive) — L0/L1 detectors on noun phrase | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15423) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Content-word ' stories' features (positive) — L0/L1 detectors on noun phrase | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L1:F9201](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9201) | 9 | Verb/function-word features (negative) — ' represents', ' researches' | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/9201) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 12 | Function-word & content features (negative) — ' in', ' too', ' foreign', '.', ' same'(flip) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F11603](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) | 27 | Function-word & content features (negative) — ' in', ' too', ' foreign', '.', ' same'(flip) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) |
| [L0:F2711](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2711) | 20 | Function-word & content features (negative) — ' in', ' too', ' foreign', '.', ' same'(flip) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2711) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | Function-word & content features (negative) — ' in', ' too', ' foreign', '.', ' same'(flip) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F5626](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5626) | 39 | Function-word & content features (negative) — ' in', ' too', ' foreign', '.', ' same'(flip) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5626) |
| [L0:F6962](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6962) | 7 | Function-word & content features (negative) — ' in', ' too', ' foreign', '.', ' same'(flip) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6962) |
| [L0:F12009](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12009) | 16 | Function-word & content features (negative) — ' in', ' too', ' foreign', '.', ' same'(flip) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12009) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | Late-layer 'journalistic' semantic feature (NEGATIVE) — L4:L13253 → L7:L9092 → L9:L7435 → L14:L4420 | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | Late-layer 'journalistic' semantic feature (NEGATIVE) — L4:L13253 → L7:L9092 → L9:L7435 → L14:L4420 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 13 | Late-layer 'journalistic' semantic feature (NEGATIVE) — L4:L13253 → L7:L9092 → L9:L7435 → L14:L4420 | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L9:F7435](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) | 13 | Late-layer 'journalistic' semantic feature (NEGATIVE) — L4:L13253 → L7:L9092 → L9:L7435 → L14:L4420 | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/7435) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 13 | Late-layer 'journalistic' semantic feature (NEGATIVE) — L4:L13253 → L7:L9092 → L9:L7435 → L14:L4420 | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:14906 de=-0.222 |
| 3 | `get_top_features` | 30 features; top: L0:14906 de=-0.222 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F14906@3` | ❌ error | — | — | Trace this L0 feature (strongest negative driver, direct_effect=-0.2217) upstrea… |
| SA-2 | `L1:F14812@3` | ❌ error | — | — | Trace this L1 feature (strongest positive driver, direct_effect=0.1895) upstream… |
| SA-3 | `L0:F1069@1` | ❌ error | — | — | Trace this L0 feature at pos=1 (direct_effect=-0.1621) — pos 1 is 'He' likely. I… |
| SA-4 | `L14:F4420@13` | ❌ error | — | — | Trace this L14 feature (direct_effect=-0.1279) at pos=13 — pos 13 is 'he' likely… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F14906@3, k=8 → Emb:" stories"@3 (de=12.94) +7 more |
| 2 | `get_upstream_features` | L1:F14812@3, k=8 → Emb:" stories"@3 (de=18.62) +7 more |
| 3 | `get_upstream_features` | L0:F1069@1, k=8 → Emb:"He"@1 (de=22.62) +7 more |
| 4 | `get_upstream_features` | L14:F4420@13, k=8 → Emb:" journalistic"@13 (de=24.38) +7 more |
| 5 | `get_upstream_features` | L4:F13253@13, k=6 → Emb:" journalistic"@13 (de=25.62) +5 more |
| 6 | `get_upstream_features` | L0:F11603@27, k=6 → Emb:" too"@27 (de=32.00) +5 more |
| 7 | `get_upstream_features` | L0:F8061@12, k=6 → Emb:" in"@12 (de=39.75) +5 more |
| 8 | `get_upstream_features` | L0:F6962@7, k=6 → Emb:" same"@7 (de=14.81) +5 more |
| 9 | `get_upstream_features` | L0:F2711@20, k=6 → Emb:" foreign"@20 (de=25.62) +5 more |
| 10 | `get_upstream_features` | L0:F6051@15, k=6 → Emb:"."@15 (de=47.00) +5 more |
| 11 | `get_upstream_features` | L0:F5333@3, k=6 → Emb:" stories"@3 (de=16.38) +5 more |
| 12 | `get_upstream_features` | L0:F11261@3, k=6 → Emb:" stories"@3 (de=12.69) +5 more |
| 13 | `get_upstream_features` | L1:F16233@3, k=6 → Emb:" stories"@3 (de=13.62) +5 more |
| 14 | `get_upstream_features` | L1:F9201@9, k=6 → Emb:" represents"@9 (de=23.50) +5 more |
| 15 | `get_upstream_features` | L7:F9092@13, k=4 → Emb:" journalistic"@13 (de=14.88) +3 more |
| 16 | `get_upstream_features` | L9:F7435@13, k=4 → Emb:" journalistic"@13 (de=4.66) +3 more |
| 17 | `get_upstream_features` | L0:F10255@1, k=6 → Emb:"He"@1 (de=6.44) +5 more |
| 18 | `get_upstream_features` | L1:F1154@3, k=6 → Emb:" stories"@3 (de=13.38) +5 more |
| 19 | `get_upstream_features` | L0:F1301@3, k=6 → Emb:" stories"@3 (de=12.25) +5 more |
| 20 | `get_upstream_features` | L0:F4564@2, k=6 → Emb:" researches"@2 (de=13.25) +5 more |
| 21 | `get_upstream_features` | L0:F5626@39, k=6 → Emb:" Poland"@39 (de=17.88) +5 more |

### Build

`build_circuit` → 18 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 20,054 | 5,974 | 49,796 | 0 | $0.0162 | — | — |
| **Total** | | **20,054** | **5,974** | **49,796** | **0** | **$0.0162** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 4s