# Circuit Oracle Report
**Date:** 2026-07-28 07:24:44 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven by a mix of genuine content features (clearing/fire/land/agriculture scene description) and a prominent early-layer discourse / negation-suppressor pathway, but the dominant direct-effect contributors are *not* the explicit "not/allowed" negation tokens — they are content-word embeddings and a "set about…" construction feature.

**Confidence:** 4

**Reasoning:** 

The probe's direct positive drivers (content_features supernode) include:
- L4:F12225 (pos 2, "they", +direct effect), L4:F5450 (pos 4, "about", +0.21), L3:F4464 (pos 4, "about", +0.18), L2:F10849 (pos 3, "set", +0.17) — all "set about…" narrative-construction features
- L2:F11518 (pos 7, "land", +0.25), L1:F461 (pos 7, "land", +0.18), L1:F361 (pos 9, "agriculture", +0.15), L2:F4819 (pos 12, "fire", +0.18), L0:F2909/9337 (fire/agriculture detectors, ~+0.5–0.8) — genuine content-word features
- L0:F8444 (pos 13, "to", +0.18), L0:F15492 (pos 8, "for", +0.17) — function-word features
- L12:F12606 (pos 25, fires on "not/were/allowed" tokens, +0.15) — the *only* feature directly tied to the actual contradiction cue "were not allowed"
- L17:F451 (pos 1, "So", +0.15) — late-layer sentence-initial feature

The suppressors (neg_discourse supernode) include L0:F3498 (pos 2, "they", -0.62), L0:F2238 (pos 4, "about", -0.34), L8:F8406 (pos 1, "So", -0.24), L2:F14822 (pos 1, "So", -0.15), L0:F6051 (pos 18, -0.15).

**Assessment of the user concern:** The user's worry is partially validated. Although the user flags "negation word signals" as spurious, the actual circuit is the opposite — the "not" token at pos 21 contributes only weakly (via L12:F12606, +0.15) and travels through *generic* function-word embeddings ("to", "for", "about", "So") rather than dedicated negation detectors. The probe is primarily fired by **scene-content features** (land, clearing, fire, agriculture, forest) and a **"set about…" narrative-construction** signal — both of which are *content-driven* rather than negation-driven. The early-layer tokens "So", "they", "about" carry BOTH positive content contribution and negative suppressor contributions, reflecting the model's distributed parsing of the sentence — not a spurious negation shortcut.

However, the circuit does rely heavily on the "set about clearing the land for agriculture, setting fire to massive tracts of forest" segment, and the contradiction cue "were not allowed to deforest" reaches the probe mostly through generic content tokens. So while no dedicated "not=contradiction" feature is the dominant driver (the user's hypothesis is **not** strongly confirmed), the probe also does **not** cleanly read the contradiction — it largely recapitulates the scene description, which is semantically consistent with contradiction but not the explicit cue. Confidence is moderate because the late-layer feature L17:F451 was only traced one hop and deeper chain effects are uncertain.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | Negation / discourse suppressors (push AWAY from contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | Negation / discourse suppressors (push AWAY from contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | Negation / discourse suppressors (push AWAY from contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L2:F14822](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14822) | 1 | Negation / discourse suppressors (push AWAY from contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14822) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 18 | Negation / discourse suppressors (push AWAY from contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L4:F12225](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) | 2 | Content / scene-description features (push TOWARD contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) |
| [L4:F5450](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) | 4 | Content / scene-description features (push TOWARD contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) |
| [L3:F4464](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) | 4 | Content / scene-description features (push TOWARD contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4464) |
| [L2:F10849](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) | 3 | Content / scene-description features (push TOWARD contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10849) |
| [L6:F14744](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) | 4 | Content / scene-description features (push TOWARD contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14744) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 25 | Content / scene-description features (push TOWARD contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | Content / scene-description features (push TOWARD contradiction) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L2:F11518](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) | 7 | Early word-embedding features (fire on content words) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) |
| [L2:F15312](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) | 4 | Early word-embedding features (fire on content words) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/15312) |
| [L3:F15978](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15978) | 7 | Early word-embedding features (fire on content words) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15978) |
| [L2:F2952](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) | 4 | Early word-embedding features (fire on content words) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2952) |
| [L1:F361](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) | 9 | Early word-embedding features (fire on content words) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/361) |
| [L1:F461](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) | 7 | Early word-embedding features (fire on content words) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/461) |
| [L0:F2909](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2909) | 12 | Early word-embedding features (fire on content words) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2909) |
| [L0:F9337](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9337) | 9 | Early word-embedding features (fire on content words) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9337) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 13 | Early word-embedding features (fire on content words) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F15492](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) | 8 | Early word-embedding features (fire on content words) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15492) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | Early word-embedding features (fire on content words) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3498 de=-0.621 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F11518@7` | ❌ error | — | — | Trace this feature which fires on pos 7 ("land"). Determine what it encodes - is… |
| SA-2 | `L4:F5450@4` | ❌ error | — | — | Trace this feature which fires on pos 4 ("about"). Determine what it encodes - i… |
| SA-3 | `L1:F461@7` | ❌ error | — | — | Trace this feature which fires on pos 7 ("land"). Determine what it encodes and … |
| SA-4 | `L2:F4819@12` | ❌ error | — | — | Trace this feature which fires on pos 12 ("fire"). Determine what it encodes - i… |
| SA-5 | `L17:F451@1` | ❌ error | — | — | Trace this late-layer feature at pos 1 ("So"). Determine what it encodes - does … |
| SA-6 | `L0:F3498@2` | ❌ error | — | — | Trace this top negative-effect feature at pos 2 ("they"). Determine what it enco… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F11518@7, k=10 → Emb:" land"@7 (de=28.38) +9 more |
| 2 | `get_upstream_features` | L4:F5450@4, k=10 → Emb:" set"@3 (de=3.31) +9 more |
| 3 | `get_upstream_features` | L2:F15312@4, k=8 → Emb:" about"@4 (de=13.69) +7 more |
| 4 | `get_upstream_features` | L2:F4819@12, k=8 → Emb:" fire"@12 (de=32.00) +7 more |
| 5 | `get_upstream_features` | L17:F451@1, k=8 → L16:F10989 (de=-11.88) +7 more |
| 6 | `get_upstream_features` | L1:F461@7, k=8 → Emb:" land"@7 (de=24.88) +7 more |
| 7 | `get_upstream_features` | L3:F4464@4, k=8 → Emb:" set"@3 (de=10.19) +7 more |
| 8 | `get_upstream_features` | L2:F10849@3, k=8 → Emb:" set"@3 (de=17.12) +7 more |
| 9 | `get_upstream_features` | L1:F361@9, k=8 → Emb:" agriculture"@9 (de=14.31) +7 more |
| 10 | `get_upstream_features` | L3:F15978@7, k=8 → Emb:" land"@7 (de=16.12) +7 more |
| 11 | `get_upstream_features` | L12:F12606@25, k=8 → Emb:" not"@21 (de=3.59) +7 more |
| 12 | `get_upstream_features` | L6:F14744@4, k=8 → Emb:" about"@4 (de=5.81) +7 more |
| 13 | `get_upstream_features` | L4:F12225@2, k=8 → Emb:" they"@2 (de=12.75) +7 more |
| 14 | `get_upstream_features` | L2:F2952@4, k=6 → Emb:" set"@3 (de=13.50) +5 more |
| 15 | `get_upstream_features` | L0:F2909@12, k=6 → Emb:" fire"@12 (de=18.88) +5 more |
| 16 | `get_upstream_features` | L0:F8444@13, k=6 → Emb:" to"@13 (de=41.00) +5 more |
| 17 | `get_upstream_features` | L8:F8406@1, k=8 → Emb:"<bos>"@0 (de=10.25) +7 more |
| 18 | `get_upstream_features` | L0:F15492@8, k=6 → Emb:" for"@8 (de=39.00) +5 more |
| 19 | `get_upstream_features` | L0:F2238@4, k=6 → Emb:" about"@4 (de=35.00) +5 more |
| 20 | `get_upstream_features` | L2:F14822@1, k=6 → Emb:"So"@1 (de=19.62) +5 more |
| 21 | `get_upstream_features` | L0:F9337@9, k=6 → Emb:" agriculture"@9 (de=13.12) +5 more |
| 22 | `get_upstream_features` | L8:F8406@1, k=10 → Emb:"<bos>"@0 (de=10.25) +9 more |
| 23 | `get_upstream_features` | L17:F451@1, k=10 → L16:F10989 (de=-11.88) +9 more |

### Build

`build_circuit` → 17 nodes, 18 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 10,114 | 8,043 | 114,679 | 0 | $0.0196 | — | — |
| **Total** | | **10,114** | **8,043** | **114,679** | **0** | **$0.0196** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 17s