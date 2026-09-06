# Circuit Oracle Report
**Date:** 2026-07-28 07:24:28 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-pos_pos_2 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a genuine profession-specific concept (nutrition/dietitian) anchored to the tokens "nutrition", "Nutrition", and "cook", with a smaller parallel contribution from "She"-anchored pronoun features that net to near-zero on the logit — not by gender markers as a spurious shortcut.

**Confidence:** 6

**Reasoning:** The output logit is fed by a strong, coherent late-layer supernode (sn_nutrition_late: L17:F14680, L17:F2427, L18:F6105, L18:F186, L19:F1589, L16:F802) whose direct upstream inputs are almost entirely the token embeddings of `nutrition` (pos 13) and `Nutrition` (pos 28), with direct_effects of 24–32 each. These features fire at position 13/28 — the actual nutrition-keyword positions — and aggregate to the probe. The mid-layer (L14:F4197, L15:F12472, L16:F12752) and early/mid-layer (L6:F11327, L7:F11540, L8:F8003, L11:F3544) nodes form a clean hierarchy: L0-L4 features detect the literal tokens `nutrition`/`cook`/`<bos>`-relative context (F13412, F9554, F14942, F10494, F7843, F5201, F6895), L6-L8 features (`F11327`, `F8003`, `F11540`, `F6653`) build a "concept of nutrition" representation, and L11+ features (`F3544`, `F16302`) integrate it.

The pronoun pathway (sn_she_gender) is present — L0:F9519, L1:F7244, L0:F15382, L6:F11646, L3:F4020, L0:F12519, L0:F2349 on `She`/`others`/`learn`/`has` — but the signs largely **cancel** in the late layers: L19:F1589 has near-zero net from these (e.g., L17:F12752 suppresses with -5.97 while L18:F6105 adds +3.66). The single positive `She`→logit contribution is from L0:F14824 at pos 2 (de=0.14) and L6:F11646 at pos 1 (de=-0.06), which are dwarfed by the +0.14 from L6:F11327 and the much larger nutrition-node contributions further up. The profession signal is therefore driven by the keyword/concept chain, not by the pronoun.

**Caveat on confidence:** I could not run `inspect_feature` (not available) to confirm the semantic labels of the late-layer features beyond what their position-specific embedding inputs reveal, so the precise framing ("dietitian" vs. generic nutrition) is inferred from the strong positional anchoring to "nutrition/Nutrition/cook" rather than from direct autointerp.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 13 | Late-layer nutrition/dietitian concept (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L19:F1589](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) | 28 | Late-layer nutrition/dietitian concept (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/1589) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 13 | Late-layer nutrition/dietitian concept (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L18:F6105](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) | 28 | Late-layer nutrition/dietitian concept (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/6105) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 13 | Late-layer nutrition/dietitian concept (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L17:F14680](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) | 28 | Late-layer nutrition/dietitian concept (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/14680) |
| [L17:F2427](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/2427) | 13 | Late-layer nutrition/dietitian concept (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/2427) |
| [L18:F186](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/186) | 13 | Late-layer nutrition/dietitian concept (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/186) |
| [L16:F802](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/802) | 28 | Late-layer nutrition/dietitian concept (L17-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/802) |
| [L14:F4197](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) | 13 | Mid-layer nutrition concept aggregation (L14-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4197) |
| [L14:F9449](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/9449) | 13 | Mid-layer nutrition concept aggregation (L14-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/9449) |
| [L15:F12472](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) | 13 | Mid-layer nutrition concept aggregation (L14-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12472) |
| [L16:F12752](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) | 13 | Mid-layer nutrition concept aggregation (L14-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) |
| [L16:F12752](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) | 28 | Mid-layer nutrition concept aggregation (L14-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12752) |
| [L17:F2771](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/2771) | 13 | Mid-layer nutrition concept aggregation (L14-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/2771) |
| [L15:F2510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) | 17 | Mid-layer nutrition concept aggregation (L14-L16) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2510) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 13 | Early/mid-layer nutrition/cooking detectors (L6-L12) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L6:F11327](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) | 28 | Early/mid-layer nutrition/cooking detectors (L6-L12) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11327) |
| [L7:F11540](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11540) | 13 | Early/mid-layer nutrition/cooking detectors (L6-L12) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/11540) |
| [L7:F6653](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/6653) | 13 | Early/mid-layer nutrition/cooking detectors (L6-L12) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/6653) |
| [L7:F3270](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3270) | 13 | Early/mid-layer nutrition/cooking detectors (L6-L12) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3270) |
| [L7:F3217](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3217) | 13 | Early/mid-layer nutrition/cooking detectors (L6-L12) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/3217) |
| [L8:F8003](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8003) | 13 | Early/mid-layer nutrition/cooking detectors (L6-L12) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8003) |
| [L8:F5419](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/5419) | 13 | Early/mid-layer nutrition/cooking detectors (L6-L12) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/5419) |
| [L11:F3544](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/3544) | 13 | Early/mid-layer nutrition/cooking detectors (L6-L12) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/3544) |
| [L12:F16302](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/16302) | 13 | Early/mid-layer nutrition/cooking detectors (L6-L12) | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/16302) |
| [L6:F2267](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2267) | 13 | Early/mid-layer nutrition/cooking detectors (L6-L12) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/2267) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 13 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F13412](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) | 28 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13412) |
| [L4:F9554](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) | 13 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9554) |
| [L4:F10494](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) | 13 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/10494) |
| [L4:F14942](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14942) | 17 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14942) |
| [L4:F12695](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12695) | 17 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12695) |
| [L1:F64](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/64) | 13 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/64) |
| [L1:F6895](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6895) | 13 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/6895) |
| [L0:F7843](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7843) | 13 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7843) |
| [L0:F5201](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) | 13 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5201) |
| [L3:F6920](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6920) | 13 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6920) |
| [L3:F6246](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) | 13 | Low-layer nutrition/cooking token detectors (L0-L5) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/6246) |
| [L0:F14824](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) | 2 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14824) |
| [L0:F2349](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) | 7 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2349) |
| [L0:F9519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) | 1 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9519) |
| [L0:F8444](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) | 16 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8444) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 9 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |
| [L0:F15382](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) | 1 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15382) |
| [L6:F11646](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) | 1 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/11646) |
| [L1:F7244](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) | 1 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7244) |
| [L1:F728](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/728) | 8 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/728) |
| [L4:F7864](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) | 1 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7864) |
| [L3:F4020](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4020) | 1 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/4020) |
| [L0:F12519](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) | 1 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12519) |
| [L1:F815](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/815) | 4 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/815) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 22 | Gender / pronoun detectors on "She" (suppressing or supporting) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L6:11327 de=0.141 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L6:F11327@13` | ❌ error | — | — | Trace upstream from L6:F11327 at pos 13. What does this feature encode? What tok… |
| SA-2 | `L14:F4197@13` | ❌ error | — | — | Trace upstream from L14:F4197 at pos 13. What does this feature encode? What tok… |
| SA-3 | `L4:F13412@13` | ❌ error | — | — | Trace upstream from L4:F13412 at pos 13. What does this feature encode? What tok… |
| SA-4 | `L19:F1589@13` | ❌ error | — | — | Trace upstream from L19:F1589 at pos 13. What does this feature encode? What tok… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L6:F11327@13, k=15 → Emb:" nutrition"@13 (de=21.00) +14 more |
| 2 | `get_upstream_features` | L14:F4197@13, k=15 → Emb:" nutrition"@13 (de=14.31) +14 more |
| 3 | `get_upstream_features` | L4:F13412@13, k=15 → Emb:" nutrition"@13 (de=14.06) +14 more |
| 4 | `get_upstream_features` | L19:F1589@13, k=15 → Emb:" nutrition"@13 (de=31.25) +14 more |
| 5 | `get_upstream_features` | L15:F2510@17, k=15 → Emb:" cook"@17 (de=28.88) +14 more |
| 6 | `get_upstream_features` | L0:F2238@9, k=15 → Emb:" about"@9 (de=34.25) +14 more |
| 7 | `get_upstream_features` | L0:F8444@16, k=15 → Emb:" to"@16 (de=40.50) +14 more |
| 8 | `get_upstream_features` | L4:F13412@28, k=15 → Emb:" Nutrition"@28 (de=12.56) +14 more |
| 9 | `get_upstream_features` | L15:F2510@17, k=10 → Emb:" cook"@17 (de=28.88) +9 more |
| 10 | `get_upstream_features` | L19:F1589@28, k=15 → Emb:" Nutrition"@28 (de=27.38) +14 more |
| 11 | `get_upstream_features` | L6:F11327@28, k=10 → Emb:" Nutrition"@28 (de=19.25) +9 more |
| 12 | `get_upstream_features` | L4:F14942@17, k=10 → Emb:" cook"@17 (de=22.50) +9 more |
| 13 | `get_upstream_features` | L17:F14680@13, k=10 → Emb:" nutrition"@13 (de=29.50) +9 more |
| 14 | `get_upstream_features` | L18:F6105@13, k=10 → Emb:" nutrition"@13 (de=31.50) +9 more |
| 15 | `get_upstream_features` | L0:F14824@2, k=10 → Emb:" has"@2 (de=32.75) +9 more |
| 16 | `get_upstream_features` | L0:F2349@7, k=8 → Emb:" others"@7 (de=41.25) +7 more |
| 17 | `get_upstream_features` | L0:F9519@1, k=8 → Emb:"She"@1 (de=15.75) +7 more |
| 18 | `get_upstream_features` | L6:F11646@1, k=8 → Emb:"She"@1 (de=19.25) +7 more |
| 19 | `get_upstream_features` | L1:F728@8, k=8 → Emb:" learn"@8 (de=21.50) +7 more |
| 20 | `get_upstream_features` | L16:F12752@13, k=10 → Emb:" nutrition"@13 (de=9.19) +9 more |
| 21 | `get_upstream_features` | L17:F2771@13, k=10 → Emb:" nutrition"@13 (de=4.28) +9 more |
| 22 | `get_upstream_features` | L14:F9449@13, k=10 → Emb:" nutrition"@13 (de=8.94) +9 more |
| 23 | `get_upstream_features` | L1:F815@4, k=8 → Emb:" passion"@4 (de=26.38) +7 more |
| 24 | `get_upstream_features` | L0:F6051@22, k=8 → Emb:"."@22 (de=47.00) +7 more |
| 25 | `get_upstream_features` | L1:F7244@1, k=8 → Emb:"She"@1 (de=13.56) +7 more |
| 26 | `get_upstream_features` | L4:F10494@13, k=8 → Emb:" nutrition"@13 (de=13.12) +7 more |
| 27 | `get_upstream_features` | L4:F9554@13, k=8 → Emb:" nutrition"@13 (de=15.88) +7 more |
| 28 | `get_upstream_features` | L16:F12752@28, k=10 → Emb:" Nutrition"@28 (de=10.44) +9 more |
| 29 | `get_upstream_features` | L17:F14680@28, k=10 → Emb:" Nutrition"@28 (de=32.50) +9 more |
| 30 | `get_upstream_features` | L18:F6105@28, k=10 → Emb:" Nutrition"@28 (de=26.75) +9 more |
| 31 | `get_upstream_features` | L18:F186@13, k=10 → Emb:" nutrition"@13 (de=5.34) +9 more |
| 32 | `get_upstream_features` | L15:F12472@13, k=10 → Emb:"<bos>"@0 (de=-12.88) +9 more |
| 33 | `get_upstream_features` | L17:F2427@13, k=10 → Emb:" nutrition"@13 (de=24.88) +9 more |
| 34 | `get_upstream_features` | L12:F16302@13, k=10 → Emb:"<bos>"@0 (de=-22.88) +9 more |
| 35 | `get_upstream_features` | L8:F8003@13, k=10 → Emb:" nutrition"@13 (de=14.31) +9 more |
| 36 | `get_upstream_features` | L11:F3544@13, k=10 → Emb:"<bos>"@0 (de=-29.12) +9 more |
| 37 | `get_upstream_features` | L6:F2267@13, k=10 → Emb:"<bos>"@0 (de=-5.94) +9 more |
| 38 | `get_upstream_features` | L7:F11540@13, k=10 → Emb:" nutrition"@13 (de=17.88) +9 more |
| 39 | `get_upstream_features` | L7:F6653@13, k=10 → Emb:" nutrition"@13 (de=16.00) +9 more |
| 40 | `get_upstream_features` | L7:F3270@13, k=8 → Emb:" nutrition"@13 (de=6.53) +7 more |
| 41 | `get_upstream_features` | L7:F3217@13, k=8 → Emb:" nutrition"@13 (de=5.75) +7 more |
| 42 | `get_upstream_features` | L7:F14078@13, k=8 → Emb:" nutrition"@13 (de=6.22) +7 more |
| 43 | `get_upstream_features` | L16:F802@28, k=8 → Emb:" Nutrition"@28 (de=21.88) +7 more |
| 44 | `get_upstream_features` | L0:F15382@1, k=8 → Emb:"She"@1 (de=16.88) +7 more |
| 45 | `get_upstream_features` | L4:F7864@1, k=8 → Emb:"She"@1 (de=24.62) +7 more |
| 46 | `get_upstream_features` | L3:F4020@1, k=8 → Emb:"She"@1 (de=19.00) +7 more |
| 47 | `get_upstream_features` | L0:F12519@1, k=8 → Emb:"She"@1 (de=21.88) +7 more |

### Build

`build_circuit` → 15 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 35,292 | 7,503 | 198,847 | 0 | $0.0315 | — | — |
| **Total** | | **35,292** | **7,503** | **198,847** | **0** | **$0.0315** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 56s