# Circuit Oracle Report
**Date:** 2026-07-28 07:24:30 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_nurse_professor-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by two parallel pathways: a dominant **name/pronoun/gender pathway** that propagates from "Melissa"/"She"/"her" embeddings up through L0–L17 identity-context features to the top contributors (L18:F14677, L19:F9685), and a weaker **profession pathway** from "midwife"/"nurse"/"Labor"/"Delivery" embeddings through L4–L13 features (L13:F11685 is the only profession word directly pushing the probe, but with a *negative* direct effect of −0.37).

**Confidence:** 8

**Reasoning:** The user's concern is strongly supported by the circuit topology. 

**Pathway 1 — Name/Pronoun/Gender (dominant, positive):** The largest positive direct effects come from L18:F14677 (+0.447 at pos 54) and L19:F9685 (+0.441 at pos 31, +0.279 at pos 54, +0.268 at pos 86). Tracing upstream, L19:F9685 (pos 31) is driven by Emb: "Melissa" (pos 31, direct_effect 2.19) and Emb: "nurse" (pos 12, 2.33). L18:F14677 (pos 54) is overwhelmingly driven by Emb: " She" (pos 54, direct_effect 14.56) — the female pronoun itself. Further upstream, L17:F5889, L15:F3330, L13:F6622 all receive their top input from Emb: "She" (pos 54) with direct_effects of 19.9, 16.1, and 13.4 respectively. L0 features F15382, F9519, F3232, F12519 all select almost exclusively for "She" (pos 54), with direct_effects of 23.5, 25.75, 24.0, etc. The "Melissa" path at pos 5 feeds L0:F7532 (direct_effect 21.25 to "Melissa"), then L4:F1276 (9.625 to "Melissa"), L5:F4957, L6:F11646, L6:F8166, L12:F14970 — a long identity-propagation chain.

**Pathway 2 — Profession (weak, mostly inhibitory):** The strongest profession-word features are L7:F2861, L7:F7389, L8:F1746, L8:F10019, all driven primarily by Emb: "midwife" (pos 66) with direct_effects of 17.25, 13.4, 12.4, 8.4. L4:F13803 (pos 11) is driven by "Delivery" (12.19) and "Labor" (8.81). However, the terminal profession feature L13:F11685 (pos 66) has direct_effect −0.37 — it actually *suppresses* the probe score. L7:F8644 also has direct_effect −0.44 at pos 12. 

**Conclusion:** The probe's classification is being driven primarily by **gender/identity markers** (the female name "Melissa" and the female pronoun "She") rather than by genuine profession indicators. The words "nurse", "midwife", "Labor", "Delivery" are present in the circuit but their contribution to the probe direction is either weak or actively negative. This is precisely the spurious-correlation pattern the user suspected: the linear probe has learned to associate "female subject" with this profession, and the model reinforces this by routing female-coded tokens through high-magnitude features (direct_effects of 14–25) that feed the probe, while the actual profession vocabulary either doesn't reach the late layers with positive sign or is suppressed en route.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 31 | Late pronoun/gender features (L18-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 54 | Late pronoun/gender features (L18-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L19:F9685](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) | 86 | Late pronoun/gender features (L18-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/9685) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 54 | Late pronoun/gender features (L18-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 31 | Late pronoun/gender features (L18-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L18:F14677](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) | 68 | Late pronoun/gender features (L18-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14677) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 54 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 54 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L13:F6622](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) | 54 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/6622) |
| [L18:F3679](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) | 31 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/3679) |
| [L18:F9023](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) | 31 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/9023) |
| [L15:F4709](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4709) | 31 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/4709) |
| [L13:F15487](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/15487) | 31 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/15487) |
| [L13:F4753](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4753) | 31 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4753) |
| [L12:F15193](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/15193) | 31 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/15193) |
| [L8:F576](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/576) | 31 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/576) |
| [L7:F1674](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1674) | 30 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/1674) |
| [L11:F8266](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/8266) | 54 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/8266) |
| [L6:F2267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2267) | 54 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2267) |
| [L6:F6493](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6493) | 31 | Mid pronoun/name context features (L13-L17) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6493) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 5 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F7532](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) | 31 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7532) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 54 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 54 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F3232](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3232) | 54 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3232) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 54 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L2:F5859](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) | 5 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5859) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 30 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L4:F1276](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) | 5 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/1276) |
| [L5:F4957](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4957) | 5 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/4957) |
| [L5:F6228](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6228) | 6 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/6228) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 5 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L6:F8166](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) | 5 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8166) |
| [L12:F14970](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) | 5 | Name/identity early features (L0-L2) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/14970) |
| [L13:F11685](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) | 66 | Midwife profession late feature (L13) | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/11685) |
| [L8:F10019](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/10019) | 66 | Midwife mid-layer features (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/10019) |
| [L8:F1746](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/1746) | 66 | Midwife mid-layer features (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/1746) |
| [L7:F2861](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2861) | 66 | Midwife mid-layer features (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/2861) |
| [L7:F7389](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7389) | 66 | Midwife mid-layer features (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/7389) |
| [L6:F11360](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11360) | 66 | Midwife mid-layer features (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11360) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 66 | Midwife mid-layer features (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L6:F15267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) | 12 | Midwife mid-layer features (L6-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/15267) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 66 | Midwife/token base features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L4:F13803](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) | 11 | Midwife/token base features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13803) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 12 | Midwife/token base features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L7:F8644](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) | 66 | Midwife/token base features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/8644) |
| [L3:F9008](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) | 11 | Midwife/token base features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/9008) |
| [L1:F12174](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12174) | 11 | Midwife/token base features (L4) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12174) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L4:1276 de=0.559 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14677@54` | ❌ error | — | — | Trace L18:F14677 upstream. This feature has the highest direct_effect and fires … |
| SA-2 | `L19:F9685@31` | ❌ error | — | — | Trace L19:F9685 upstream. It fires at multiple positions (31, 54, 86). Determine… |
| SA-3 | `L4:F13803@11` | ❌ error | — | — | Trace L4:F13803 upstream. Fires at pos 11 with high activation (19.875) and at p… |
| SA-4 | `L4:F1276@5` | ❌ error | — | — | Trace L4:F1276 upstream. Fires at pos 5 with high activation. Pos 5 is likely 'M… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14677@54, k=10 → Emb:" She"@54 (de=14.56) +9 more |
| 2 | `get_upstream_features` | L19:F9685@31, k=10 → Emb:" nurse"@12 (de=2.33) +9 more |
| 3 | `get_upstream_features` | L4:F13803@11, k=10 → Emb:" Delivery"@11 (de=12.19) +9 more |
| 4 | `get_upstream_features` | L4:F1276@5, k=10 → Emb:" Melissa"@5 (de=9.62) +9 more |
| 5 | `get_upstream_features` | L7:F8644@12, k=10 → Emb:" nurse"@12 (de=5.62) +9 more |
| 6 | `get_upstream_features` | L13:F11685@66, k=10 → Emb:" midwife"@66 (de=7.97) +9 more |
| 7 | `get_upstream_features` | L6:F8166@5, k=10 → L4:F1276 (de=5.19) +9 more |
| 8 | `get_upstream_features` | L6:F11646@5, k=10 → Emb:" Melissa"@5 (de=6.94) +9 more |
| 9 | `get_upstream_features` | L12:F14970@5, k=10 → L4:F1276 (de=3.36) +9 more |
| 10 | `get_upstream_features` | L0:F7532@5, k=10 → Emb:" Melissa"@5 (de=21.25) +9 more |
| 11 | `get_upstream_features` | L6:F15267@12, k=10 → Emb:" nurse"@12 (de=20.50) +9 more |
| 12 | `get_upstream_features` | L17:F5889@54, k=10 → Emb:" She"@54 (de=19.88) +9 more |
| 13 | `get_upstream_features` | L15:F3330@54, k=10 → Emb:" She"@54 (de=16.12) +9 more |
| 14 | `get_upstream_features` | L18:F9023@31, k=10 → Emb:"<bos>"@0 (de=-4.44) +9 more |
| 15 | `get_upstream_features` | L13:F4753@31, k=10 → Emb:"<bos>"@0 (de=4.00) +9 more |
| 16 | `get_upstream_features` | L18:F3679@31, k=10 → L17:F3558 (de=3.61) +9 more |
| 17 | `get_upstream_features` | L3:F9008@11, k=10 → Emb:" Delivery"@11 (de=11.19) +9 more |
| 18 | `get_upstream_features` | L0:F15382@54, k=10 → Emb:" She"@54 (de=23.50) +9 more |
| 19 | `get_upstream_features` | L0:F9519@54, k=10 → Emb:" She"@54 (de=25.75) +9 more |
| 20 | `get_upstream_features` | L13:F6622@54, k=10 → Emb:" She"@54 (de=13.38) +9 more |
| 21 | `get_upstream_features` | L2:F5859@5, k=10 → L0:F7532 (de=5.28) +9 more |
| 22 | `get_upstream_features` | L6:F2267@54, k=10 → Emb:"<bos>"@0 (de=-9.75) +9 more |
| 23 | `get_upstream_features` | L0:F7532@31, k=10 → Emb:" Melissa"@31 (de=22.25) +9 more |
| 24 | `get_upstream_features` | L17:F7837@31, k=10 → Emb:"<bos>"@0 (de=-2.61) +9 more |
| 25 | `get_upstream_features` | L15:F4709@31, k=10 → L13:F15487 (de=3.20) +9 more |
| 26 | `get_upstream_features` | L13:F15487@31, k=10 → L7:F1674 (de=1.88) +9 more |
| 27 | `get_upstream_features` | L12:F15193@31, k=10 → L8:F576 (de=1.91) +9 more |
| 28 | `get_upstream_features` | L11:F8266@54, k=10 → Emb:" She"@54 (de=-3.16) +9 more |
| 29 | `get_upstream_features` | L7:F1674@30, k=10 → Emb:"."@30 (de=-2.97) +9 more |
| 30 | `get_upstream_features` | L8:F576@31, k=10 → Emb:" Melissa"@31 (de=-4.75) +9 more |
| 31 | `get_upstream_features` | L8:F10019@66, k=10 → L7:F2861 (de=11.31) +9 more |
| 32 | `get_upstream_features` | L8:F1746@66, k=10 → Emb:" midwife"@66 (de=12.44) +9 more |
| 33 | `get_upstream_features` | L7:F2861@66, k=10 → Emb:" midwife"@66 (de=17.25) +9 more |
| 34 | `get_upstream_features` | L7:F7389@66, k=10 → Emb:" midwife"@66 (de=13.44) +9 more |
| 35 | `get_upstream_features` | L1:F12174@11, k=10 → Emb:" Labor"@9 (de=7.06) +9 more |
| 36 | `get_upstream_features` | L6:F15267@66, k=10 → Emb:" midwife"@66 (de=11.62) +9 more |
| 37 | `get_upstream_features` | L0:F6051@30, k=10 → Emb:"."@30 (de=47.50) +9 more |
| 38 | `get_upstream_features` | L6:F11360@66, k=10 → L4:F13803 (de=8.94) +9 more |
| 39 | `get_upstream_features` | L6:F6493@31, k=10 → Emb:" Melissa"@31 (de=-3.81) +9 more |
| 40 | `get_upstream_features` | L0:F3232@54, k=10 → Emb:" She"@54 (de=24.00) +9 more |
| 41 | `get_upstream_features` | L5:F16213@6, k=10 → Emb:" Melissa"@5 (de=1.75) +9 more |
| 42 | `get_upstream_features` | L4:F15317@6, k=10 → Emb:" Melissa"@5 (de=2.50) +9 more |
| 43 | `get_upstream_features` | L5:F6228@6, k=10 → L0:F7532 (de=4.12) +9 more |
| 44 | `get_upstream_features` | L5:F4957@5, k=10 → L4:F1276 (de=3.75) +9 more |

### Build

`build_circuit` → 15 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 28,267 | 7,038 | 174,720 | 0 | $0.0274 | — | — |
| **Total** | | **28,267** | **7,038** | **174,720** | **0** | **$0.0274** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 38s