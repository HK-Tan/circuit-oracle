# Circuit Oracle Report
**Date:** 2026-07-28 07:24:15 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This is a probe-classification graph where the score for "profession = nurse" is driven almost entirely by genuine, profession-specific lexical and semantic features centered on the words "Nursing" (pos 18), "nurse practitioner" (pos 32-33), "operating room" (pos 51-52), and "Bachelors" (pos 13-17) — with essentially no role for the name "Lori" or any gender marker.

**Confidence:** 9

**Reasoning:** The circuit's two strongest direct-effect features are L14:F3985 (0.1572) and L6:F15267 (0.1187) at position 18, both of which are "Nursing"-token features (their upstreams are dominated by the "Nursing" embedding with direct_effect >10). These feed into a late-layer supernode (L18:F13596, L15:F15159, L15:F8289, L14:F3985) whose "Nursing" embedding contribution alone is 43 (L18:F13596), confirming the probe reads a "nursing" concept from the profession-degree phrase. A parallel path traces through L4:F9036 and L7:F15132 at position 33, which trace back to the "practitioner" (11.125) and "nurse" (8.6875) embeddings via L1:F1494, L2:F2589, and L4:F11037 — i.e., the "nurse practitioner" title itself. A third supporting path runs through L4:F4665 (and L3:F11871) at positions 51-52, both pointing to the "operating room" embeddings ("operating"=20, "room"=8.625), which is a workplace feature specific to this profession. Degree-context features (L4:F3727 from "achelors"=20.875, L2:F10852 from "Nursing"=11.625, L3:F4113 from "in"=11.75) complete the profession signaling. By contrast, the "Lori" embedding at pos 1 contributes only 0.4492 to L0:F5038 (which itself is a "graduated"-dominated feature, direct_effect 22.25 from the "graduated" embedding) and does not propagate into any late-layer nursing concept. There are no female-pronoun, gendered, or name-driven features in the top contributors; the "She" pronoun (pos 7) is absent from the circuit. The user's concern that the probe relies on spurious gender markers is *not* supported by this attribution graph — the circuit is dominated by explicit profession vocabulary (degree title, license, job setting), which is exactly what a profession-classification probe *should* attend to.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F13596](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) | 18 | Late-layer 'Nursing' concept (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/13596) |
| [L15:F15159](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) | 18 | Late-layer 'Nursing' concept (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/15159) |
| [L15:F8289](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) | 18 | Late-layer 'Nursing' concept (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/8289) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 18 | Late-layer 'Nursing' concept (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L8:F16339](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) | 18 | Mid-layer 'Nursing' word features (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/16339) |
| [L8:F440](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/440) | 18 | Mid-layer 'Nursing' word features (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/440) |
| [L8:F4607](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) | 18 | Mid-layer 'Nursing' word features (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/4607) |
| [L8:F9619](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) | 18 | Mid-layer 'Nursing' word features (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) |
| [L7:F210](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) | 18 | Mid-layer 'Nursing' word features (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/210) |
| [L6:F4490](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) | 18 | Mid-layer 'Nursing' word features (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4490) |
| [L7:F5829](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5829) | 18 | Mid-layer 'Nursing' word features (pos 18) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5829) |
| [L14:F3985](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) | 33 | Mid-layer 'nurse practitioner' features (pos 33) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/3985) |
| [L8:F9619](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) | 33 | Mid-layer 'nurse practitioner' features (pos 33) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/9619) |
| [L8:F12680](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12680) | 33 | Mid-layer 'nurse practitioner' features (pos 33) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/12680) |
| [L7:F15132](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) | 33 | Mid-layer 'nurse practitioner' features (pos 33) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/15132) |
| [L7:F14129](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) | 33 | Mid-layer 'nurse practitioner' features (pos 33) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14129) |
| [L5:F1275](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) | 33 | Mid-layer 'nurse practitioner' features (pos 33) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/1275) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 18 | Core 'nurse/Nursing' concept feature | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 33 | Core 'nurse/Nursing' concept feature | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 52 | 'operating room' / workplace features (pos 51-52) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L4:F4665](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) | 51 | 'operating room' / workplace features (pos 51-52) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4665) |
| [L3:F11871](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11871) | 52 | 'operating room' / workplace features (pos 51-52) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/11871) |
| [L1:F1889](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1889) | 52 | 'operating room' / workplace features (pos 51-52) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1889) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 13 | 'Bachelors' / degree features (pos 13-17) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 15 | 'Bachelors' / degree features (pos 13-17) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L4:F3727](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) | 17 | 'Bachelors' / degree features (pos 13-17) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/3727) |
| [L3:F4113](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) | 17 | 'Bachelors' / degree features (pos 13-17) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4113) |
| [L2:F10852](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) | 18 | 'Bachelors' / degree features (pos 13-17) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/10852) |
| [L4:F9036](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) | 33 | 'nurse practitioner' token features (pos 32-33) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9036) |
| [L4:F11037](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) | 33 | 'nurse practitioner' token features (pos 32-33) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/11037) |
| [L2:F2589](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) | 33 | 'nurse practitioner' token features (pos 32-33) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/2589) |
| [L1:F1494](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) | 33 | 'nurse practitioner' token features (pos 32-33) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1494) |
| [L1:F15395](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) | 33 | 'nurse practitioner' token features (pos 32-33) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) |
| [L1:F12131](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12131) | 33 | 'nurse practitioner' token features (pos 32-33) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12131) |
| [L3:F15901](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) | 18 | 'Nursing' / 'nurse' token features (pos 18, 32) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/15901) |
| [L3:F5611](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5611) | 33 | 'Nursing' / 'nurse' token features (pos 18, 32) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/5611) |
| [L1:F10429](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10429) | 18 | 'Nursing' / 'nurse' token features (pos 18, 32) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/10429) |
| [L1:F15795](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15795) | 18 | 'Nursing' / 'nurse' token features (pos 18, 32) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15795) |
| [L1:F14469](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) | 18 | 'Nursing' / 'nurse' token features (pos 18, 32) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14469) |
| [L1:F15395](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) | 18 | 'Nursing' / 'nurse' token features (pos 18, 32) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15395) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L14:3985 de=0.157 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F3985@18` | ❌ error | — | — | Trace the path upstream from L14:F3985 at position 18 (the feature with the high… |
| SA-2 | `L14:F3985@33` | ❌ error | — | — | Trace the path upstream from L14:F3985 at position 33 (direct_effect 0.1309 on p… |
| SA-3 | `L6:F15267@33` | ❌ error | — | — | Trace the path upstream from L6:F15267 at position 33 (direct_effect 0.1187 on p… |
| SA-4 | `L0:F5038@2` | ❌ error | — | — | Trace the path upstream from L0:F5038 at position 2 (direct_effect 0.0767 on pro… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F3985@18, k=10 → Emb:" Nursing"@18 (de=11.56) +9 more |
| 2 | `get_upstream_features` | L14:F3985@33, k=10 → L4:F9036 (de=6.41) +9 more |
| 3 | `get_upstream_features` | L6:F15267@33, k=10 → Emb:" nurse"@32 (de=5.66) +9 more |
| 4 | `get_upstream_features` | L0:F5038@2, k=10 → Emb:" graduated"@2 (de=22.25) +9 more |
| 5 | `get_upstream_features` | L0:F6270@6, k=10 → Emb:" University"@6 (de=22.38) +9 more |
| 6 | `get_upstream_features` | L4:F4665@52, k=10 → Emb:" room"@52 (de=10.75) +9 more |
| 7 | `get_upstream_features` | L4:F9036@33, k=10 → Emb:" practitioner"@33 (de=14.00) +9 more |
| 8 | `get_upstream_features` | L3:F15901@18, k=10 → Emb:" Nursing"@18 (de=15.19) +9 more |
| 9 | `get_upstream_features` | L7:F3979@18, k=10 → L6:F15267 (de=9.19) +9 more |
| 10 | `get_upstream_features` | L8:F9619@33, k=10 → L6:F15267 (de=5.53) +9 more |
| 11 | `get_upstream_features` | L18:F13596@18, k=10 → Emb:" Nursing"@18 (de=43.00) +9 more |
| 12 | `get_upstream_features` | L15:F15159@18, k=10 → Emb:" Nursing"@18 (de=10.81) +9 more |
| 13 | `get_upstream_features` | L7:F15132@33, k=10 → Emb:" practitioner"@33 (de=11.12) +9 more |
| 14 | `get_upstream_features` | L8:F16339@18, k=10 → Emb:" Nursing"@18 (de=7.28) +9 more |
| 15 | `get_upstream_features` | L15:F8289@18, k=10 → Emb:" Nursing"@18 (de=6.38) +9 more |
| 16 | `get_upstream_features` | L8:F440@18, k=10 → Emb:" Nursing"@18 (de=9.19) +9 more |
| 17 | `get_upstream_features` | L8:F4607@18, k=10 → Emb:" Nursing"@18 (de=7.47) +9 more |
| 18 | `get_upstream_features` | L5:F1275@33, k=10 → L4:F9036 (de=1.70) +9 more |
| 19 | `get_upstream_features` | L1:F1494@33, k=10 → Emb:" nurse"@32 (de=8.69) +9 more |
| 20 | `get_upstream_features` | L4:F11037@33, k=10 → Emb:" practitioner"@33 (de=6.47) +9 more |
| 21 | `get_upstream_features` | L4:F11037@18, k=10 → Emb:" Nursing"@18 (de=10.38) +9 more |
| 22 | `get_upstream_features` | L5:F10392@18, k=10 → Emb:" Nursing"@18 (de=-2.70) +9 more |
| 23 | `get_upstream_features` | L6:F4490@18, k=10 → Emb:" Nursing"@18 (de=11.56) +9 more |
| 24 | `get_upstream_features` | L7:F210@18, k=10 → Emb:" Nursing"@18 (de=7.88) +9 more |
| 25 | `get_upstream_features` | L0:F5038@6, k=10 → ❌ Feature (layer=0, feature_idx=5038) not found at pos=6. This |
| 26 | `get_upstream_features` | L0:F5038@1, k=10 → ❌ Feature (layer=0, feature_idx=5038) not found at pos=1. This |
| 27 | `get_upstream_features` | L4:F9036@32, k=10 → ❌ Feature (layer=4, feature_idx=9036) not found at pos=32. Thi |
| 28 | `get_upstream_features` | L8:F12680@33, k=10 → L7:F15132 (de=4.56) +9 more |
| 29 | `get_upstream_features` | L4:F4665@51, k=10 → Emb:" operating"@51 (de=20.00) +9 more |
| 30 | `get_upstream_features` | L4:F4665@48, k=10 → ❌ Feature (layer=4, feature_idx=4665) not found at pos=48. Thi |
| 31 | `get_upstream_features` | L4:F4665@51, k=10 → Emb:" operating"@51 (de=20.00) +9 more |
| 32 | `get_upstream_features` | L4:F4665@30, k=10 → Emb:" acute"@30 (de=15.00) +9 more |
| 33 | `get_upstream_features` | L4:F4665@31, k=10 → Emb:" acute"@30 (de=14.31) +9 more |
| 34 | `get_upstream_features` | L7:FNone@33, k=10 → ❌ get_upstream_features failed: 'feature_idx' |
| 35 | `get_upstream_features` | L7:F15132@33, k=10 → Emb:" practitioner"@33 (de=11.12) +9 more |
| 36 | `get_upstream_features` | L3:F11871@52, k=10 → Emb:" operating"@51 (de=24.25) +9 more |
| 37 | `get_upstream_features` | L1:F1889@52, k=10 → Emb:" operating"@51 (de=4.25) +9 more |
| 38 | `get_upstream_features` | L3:F13175@52, k=10 → Emb:" operating"@51 (de=5.84) +9 more |
| 39 | `get_upstream_features` | L4:F3727@13, k=10 → Emb:"achelors"@13 (de=20.88) +9 more |
| 40 | `get_upstream_features` | L2:F10852@18, k=10 → Emb:" Nursing"@18 (de=11.62) +9 more |
| 41 | `get_upstream_features` | L3:F4113@17, k=10 → Emb:" in"@17 (de=11.75) +9 more |
| 42 | `get_upstream_features` | L2:F2589@33, k=10 → Emb:" practitioner"@33 (de=13.00) +9 more |
| 43 | `get_upstream_features` | L1:F10429@18, k=10 → Emb:" Nursing"@18 (de=4.69) +9 more |
| 44 | `get_upstream_features` | L1:F15795@18, k=10 → Emb:" Nursing"@18 (de=4.59) +9 more |
| 45 | `get_upstream_features` | L1:F14469@18, k=10 → Emb:" Nursing"@18 (de=17.62) +9 more |
| 46 | `get_upstream_features` | L1:F15395@33, k=10 → Emb:" nurse"@32 (de=7.75) +9 more |
| 47 | `get_upstream_features` | L1:F12131@33, k=10 → Emb:" nurse"@32 (de=6.22) +9 more |

### Build

`build_circuit` → 18 nodes, 17 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 28,184 | 6,976 | 162,244 | 0 | $0.0266 | — | — |
| **Total** | | **28,184** | **6,976** | **162,244** | **0** | **$0.0266** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 24s