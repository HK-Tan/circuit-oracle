# Circuit Oracle Report
**Date:** 2026-07-28 07:23:59 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's "engineer" classification is driven by two parallel streams: a strong set of masculine-pronoun features (he/his) and a genuine engineering-content stream, with both contributing — but the gender-marker stream is unusually prominent and fires at five distinct positions.

**Confidence:** 7

**Reasoning:**

The circuit reveals two distinct supernodes feeding the output:

1. **he_markers supernode** — This is the most striking finding and directly supports the user's concern. Five separate embedding positions of male pronouns drive the probe:
   - L0:F2994 fires at pos 3, 25, 47 (all "his"), with direct_effects of 0.39, 0.13, 0.11 to the probe
   - L0:F1069 at pos 22 ("He") and L0:F12768 at pos 81 ("he")
   - L15:F3330, L17:F5889, L18:F14743, L18:F10315 all propagate "He"/"he"/"his" features to the probe with large direct_effects (e.g., L18:F14743 at pos 22 contributes −0.14, L18:F14743 at pos 81 contributes −0.11; L18:F10315 at pos 3 contributes −0.10)
   
   When tracing upstream from each pronoun feature, the dominant source is overwhelmingly the pronoun token embedding itself (e.g., "his" at pos 3 has direct_effect=43.25 to L0:F2994; "He" at pos 22 has direct_effect=37 to L0:F1069; "he" at pos 81 has direct_effect=41.25 to L0:F12768). These are not subtle — they are dedicated masculine-pronoun detectors that read out the gendered referent and feed it forward.

2. **eng_content supernode** — Genuine profession signal is also present:
   - L6:F170 at pos 9 ("Engineering", act=19.6, direct_effect=+0.14) and pos 8 ("Mechanical", act=17.4, +0.10) — these fire on the actual profession tokens
   - L2:F1440 at pos 9 reads "Engineering" (direct_effect=19.5) and "Mechanical" (1.6)
   - L4:F3727, L3:F4113, L2:F10852 read "achelors"/"degree"/"in" — academic-degree structure
   - L0:F1326 reads "University"/"Waterloo", L0:F7532 reads "Daniel" — entity/institution

3. **suppressors supernode** — Several features push AGAINST the engineer classification: L7:F14946 (pos 3, −0.18), L12:F2175 (pos 2, −0.17), L6:F12990 (pos 22, −0.17), L5:F10392 (pos 9, −0.11). These likely encode alternative-profession or pronoun-ambiguity suppressors.

**Key finding supporting user concern:** The "he/his" features carry the largest per-edge direct_effects in the entire graph (raw values 24–45 in backward traces, vs. 8–22 for engineering content). Five pronoun positions each independently push the probe score, and several late-layer pronoun features (L17, L18) directly contribute to the output. This is exactly the pattern of a probe that has learned to rely on gender co-occurrence statistics: the same biographical template ("He received his degree in...") produces strong masculine-pronoun signal that the probe weights heavily, in addition to — not instead of — the genuine "Engineering"/"Mechanical"/"Robotics" content. The presence of a legitimate engineering-content stream is reassuring, but the magnitude and breadth of the gender stream indicates the probe is partially using the subject's gender as a shortcut, which is the spurious-cue pattern the user flagged.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 3 | Masculine Pronoun Features (he/his) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 25 | Masculine Pronoun Features (he/his) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 47 | Masculine Pronoun Features (he/his) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 22 | Masculine Pronoun Features (he/his) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 81 | Masculine Pronoun Features (he/his) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 22 | Masculine Pronoun Features (he/his) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 81 | Masculine Pronoun Features (he/his) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 22 | Masculine Pronoun Features (he/his) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | Masculine Pronoun Features (he/his) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 81 | Masculine Pronoun Features (he/his) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 3 | Masculine Pronoun Features (he/his) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 9 | Engineering Content Features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L6:F170](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) | 8 | Engineering Content Features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/170) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 5 | Engineering Content Features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 7 | Engineering Content Features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L3:F4113](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) | 7 | Engineering Content Features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 5 | Engineering Content Features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L2:F1440](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1440) | 9 | Engineering Content Features | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1440) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 9 | Engineering Content Features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L0:F1326](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1326) | 14 | Engineering Content Features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1326) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 1 | Engineering Content Features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 3 | Suppression / Inhibitory Features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L12:F2175](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) | 2 | Suppression / Inhibitory Features | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/2175) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 22 | Suppression / Inhibitory Features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L5:F10392](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) | 9 | Suppression / Inhibitory Features | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10392) |
| [L0:F12351](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12351) | 2 | Suppression / Inhibitory Features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12351) |
| [L0:F13526](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13526) | 21 | Suppression / Inhibitory Features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13526) |
| [L0:F15320](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) | 2 | Suppression / Inhibitory Features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15320) |
| [L0:F13553](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) | 2 | Suppression / Inhibitory Features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13553) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | ❌ Token ' engineer' is not one of the top-k next-token candida |
| 3 | `get_top_features` | 20 features; top: L0:2994 de=0.395 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F2994@3` | ❌ error | — | — | Trace upstream from L0:F2994 at position 3 ("Daniel"). What does this feature en… |
| SA-2 | `L7:F14893@3` | ❌ error | — | — | Trace upstream from L7:F14893 at position 3. What does this feature encode? Is i… |
| SA-3 | `L6:F170@9` | ❌ error | — | — | Trace upstream from L6:F170 at position 9. This fires at high activation (19.6) … |
| SA-4 | `L5:F10392@9` | ❌ error | — | — | Trace upstream from L5:F10392 at position 9. This is a strong negative contribut… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F2994@3, k=10 → Emb:" his"@3 (de=43.25) +9 more |
| 2 | `get_upstream_features` | L7:F14893@3, k=10 → Emb:" his"@3 (de=24.38) +9 more |
| 3 | `get_upstream_features` | L6:F170@9, k=10 → L5:F10392 (de=10.94) +9 more |
| 4 | `get_upstream_features` | L5:F10392@9, k=10 → Emb:" Mechanical"@8 (de=3.08) +9 more |
| 5 | `get_upstream_features` | L4:F3727@5, k=10 → Emb:"achelors"@5 (de=22.38) +9 more |
| 6 | `get_upstream_features` | L3:F4113@7, k=10 → Emb:" in"@7 (de=12.19) +9 more |
| 7 | `get_upstream_features` | L2:F1440@9, k=8 → Emb:" Engineering"@9 (de=19.50) +7 more |
| 8 | `get_upstream_features` | L4:F11037@9, k=8 → Emb:" Engineering"@9 (de=8.25) +7 more |
| 9 | `get_upstream_features` | L0:F2994@25, k=5 → Emb:" his"@25 (de=45.75) +4 more |
| 10 | `get_upstream_features` | L0:F2994@47, k=5 → Emb:" his"@47 (de=45.25) +4 more |
| 11 | `get_upstream_features` | L18:F14743@22, k=8 → Emb:" He"@22 (de=21.88) +7 more |
| 12 | `get_upstream_features` | L12:F2175@2, k=8 → Emb:" received"@2 (de=4.09) +7 more |
| 13 | `get_upstream_features` | L0:F1069@22, k=8 → Emb:" He"@22 (de=37.00) +7 more |
| 14 | `get_upstream_features` | L6:F12990@22, k=8 → Emb:" He"@22 (de=4.47) +7 more |
| 15 | `get_upstream_features` | L18:F10315@3, k=8 → Emb:" his"@3 (de=24.88) +7 more |
| 16 | `get_upstream_features` | L18:F14743@81, k=6 → Emb:" he"@81 (de=25.12) +5 more |
| 17 | `get_upstream_features` | L17:F5889@22, k=6 → Emb:" He"@22 (de=20.75) +5 more |
| 18 | `get_upstream_features` | L2:F10852@5, k=5 → Emb:"achelors"@5 (de=19.25) +4 more |
| 19 | `get_upstream_features` | L0:F1326@14, k=5 → Emb:" University"@12 (de=7.28) +4 more |
| 20 | `get_upstream_features` | L0:F7532@1, k=5 → Emb:"Daniel"@1 (de=10.12) +4 more |
| 21 | `get_upstream_features` | L0:F12768@81, k=5 → Emb:" he"@81 (de=41.25) +4 more |
| 22 | `get_upstream_features` | L15:F3330@81, k=5 → Emb:" he"@81 (de=24.75) +4 more |

### Build

`build_circuit` → 16 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 25,125 | 5,449 | 69,283 | 0 | $0.0182 | — | — |
| **Total** | | **25,125** | **5,449** | **69,283** | **0** | **$0.0182** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 16s