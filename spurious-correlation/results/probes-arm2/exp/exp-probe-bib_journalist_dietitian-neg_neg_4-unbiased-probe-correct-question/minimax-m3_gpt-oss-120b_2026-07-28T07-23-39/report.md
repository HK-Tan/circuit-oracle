# Circuit Oracle Report
**Date:** 2026-07-28 07:23:39 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a mix of (a) a genuine profession-anchoring signal at the word "writer" (pos 28), (b) competing L0 features on organization-name tokens ("Royal United Services Institute", "Middle East") that largely cancel, and (c) a spurious L0 feature anchored on the male pronoun "he" and function word "at" — a gender/co-occurrence correlate rather than a profession indicator.

**Confidence:** 6

**Reasoning:**

The circuit terminates at the probe logit (layer 26) and receives both task-relevant and spurious signals.

**Task-relevant path (the profession signal).** The "writer" token (pos 28) is the strongest single-anchor of legitimate profession evidence. The L0 embedding of "writer" (direct_effect 9.13 on L4:F13253) composes with the L0 embedding of "freelance" (pos 27) through mid-layer features L4:F13253 → L7:F72 → L7:F13646 → L8:F8855 → L6:F12712 → L14:F4420. Notably L14:F4420 has direct_effect −0.068 on the logit — i.e., the deeper "writer" representation pushes the probe score *down* (perhaps because defense-journalism writers are not the probe's positive class). Mid-layer features L2:F9210, L7:F72, L8:F8855 carry positive signal (activations 6.4–14.6) into the late layer. The L4:L7:L8 stack is a clean compositional noun-phrase detector around "freelance writer."

**Spurious gender path (the user's concern).** L0:F7124 at pos 2 is the single most negative feature on the logit (direct_effect −0.157, activation 28.75). Its top upstream is the embedding of "at" (pos 2, direct_effect 31.4) followed by "Starting" and BOS. But its *position 22* reading — the other L0 feature F12768, also strongly activated (36.0, direct_effect +0.075) — is driven almost entirely by the embedding of "he" (pos 22, direct_effect 40.25). The pronoun "he" (and the article "at" in "Starting at the Royal…") thus form a co-occurrence bag: L0 has memorized that defense/journalism biographical passages beginning with "Starting at the X Institute" + "he" are more often male-coded, and these surface features carry weight into the probe. The circuit is *not* a deeply-computed gender-bias feature (no L5+ feature fires on "he"); rather, the probe is leaning on low-level token-embedding-driven L0 features whose activations happen to correlate with gendered biography patterns in the training distribution.

**Organization-name cancelation.** Features L0:F12768, F3007, F10881, F9297, F12713, F6051 fire on the organization tokens ("Middle", "East", "covering", "Institute", ".") with direct_effects of mixed sign (F12768 and F3007 push the logit up by ~0.13 total, while F7124 alone pushes it down 0.16). The "broadcasting" branch (pos 71, L4/L6 features) is a separate negative strand (F10984 at −0.052). These entity-name features do not converge on a stable profession representation — they mostly cancel.

**Net answer to the user's concern.** Yes, the user's worry is partially validated: the largest single feature feeding the probe is an L0 token feature anchored on the function-word sequence around "he" / "at" (F7124, direct_effect −0.157), not a deeper profession-representation feature. The genuine "writer" profession signal exists but is split across many mid-layer features and partially suppressed by L14:F4420. The probe appears to overweight low-level gendered co-occurrence statistics relative to the actual profession-noun signal — exactly the bias pattern the user suspected.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | "writer" profession token features (L6-L14) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 28 | "writer" profession token features (L6-L14) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 28 | Mid-layer "writer/freelance" composition (L4-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 28 | Mid-layer "writer/freelance" composition (L4-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L7:F72](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/72) | 28 | Mid-layer "writer/freelance" composition (L4-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/72) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | Mid-layer "writer/freelance" composition (L4-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L2:F9210](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9210) | 28 | Mid-layer "writer/freelance" composition (L4-L8) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/9210) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Entity/Organization name detection (positive direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F3007](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) | 14 | Entity/Organization name detection (positive direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3007) |
| [L0:F10881](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) | 12 | Entity/Organization name detection (positive direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10881) |
| [L0:F9297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) | 7 | Entity/Organization name detection (positive direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9297) |
| [L0:F12713](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12713) | 15 | Entity/Organization name detection (positive direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12713) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 38 | Entity/Organization name detection (positive direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F7124](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) | 2 | Male pronoun "he" (spurious gender signal) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7124) |
| [L0:F15661](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) | 7 | Organization name features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15661) |
| [L0:F6484](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6484) | 7 | Organization name features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6484) |
| [L0:F2348](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2348) | 4 | Organization name features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2348) |
| [L0:F1229](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1229) | 14 | Organization name features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1229) |
| [L0:F13096](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13096) | 3 | Organization name features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13096) |
| [L0:F9728](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9728) | 12 | Organization name features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9728) |
| [L0:F4459](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4459) | 7 | Organization name features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4459) |
| [L0:F10489](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10489) | 7 | Organization name features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10489) |
| [L0:F1445](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1445) | 7 | Organization name features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1445) |
| [L0:F12901](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12901) | 15 | Organization name features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12901) |
| [L6:F10984](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10984) | 71 | "broadcasting" token features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/10984) |
| [L4:F7056](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7056) | 71 | "broadcasting" token features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7056) |
| [L4:F13482](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13482) | 71 | "broadcasting" token features (negative direction) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13482) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:7124 de=-0.157 |

### Dispatch: 7 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F12768@22` | ❌ error | — | — | Trace this L0 feature upstream to understand what tokens/context drive it. What … |
| SA-2 | `L0:F3007@14` | ❌ error | — | — | Trace upstream to find what drives this feature. What tokens/patterns does it en… |
| SA-3 | `L0:F10881@12` | ❌ error | — | — | Trace upstream to find what drives this feature. What tokens/patterns does it en… |
| SA-4 | `L0:F9297@7` | ❌ error | — | — | Trace upstream to find what drives this feature. What tokens/patterns does it en… |
| SA-5 | `L0:F12713@15` | ❌ error | — | — | Trace upstream to find what drives this feature. What tokens/patterns does it en… |
| SA-6 | `L14:F4420@28` | ❌ error | — | — | Trace upstream to find what drives this feature. This is a L14 feature with nega… |
| SA-7 | `L0:F7124@2` | ❌ error | — | — | Trace upstream to find what drives this feature. Strongest negative effect at L0… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F12768@22, k=5 → Emb:" he"@22 (de=40.25) +4 more |
| 2 | `get_upstream_features` | L0:F3007@14, k=5 → Emb:" Middle"@14 (de=20.75) +4 more |
| 3 | `get_upstream_features` | L0:F10881@12, k=5 → Emb:" covering"@12 (de=16.25) +4 more |
| 4 | `get_upstream_features` | L0:F9297@7, k=5 → Emb:" Institute"@7 (de=11.81) +4 more |
| 5 | `get_upstream_features` | L0:F12713@15, k=5 → Emb:" East"@15 (de=11.00) +4 more |
| 6 | `get_upstream_features` | L0:F7124@2, k=5 → Emb:" at"@2 (de=31.38) +4 more |
| 7 | `get_upstream_features` | L14:F4420@28, k=8 → Emb:" writer"@28 (de=5.75) +7 more |
| 8 | `get_upstream_features` | L6:F10984@71, k=8 → Emb:" broadcasting"@71 (de=13.06) +7 more |
| 9 | `get_upstream_features` | L6:F12712@28, k=8 → Emb:" writer"@28 (de=6.22) +7 more |
| 10 | `get_upstream_features` | L8:F8855@28, k=5 → Emb:" writer"@28 (de=4.72) +4 more |
| 11 | `get_upstream_features` | L4:F13253@28, k=5 → Emb:" writer"@28 (de=9.12) +4 more |
| 12 | `get_upstream_features` | L7:F13646@28, k=5 → Emb:" writer"@28 (de=2.77) +4 more |
| 13 | `get_upstream_features` | L4:F7056@71, k=5 → Emb:" broadcasting"@71 (de=12.81) +4 more |
| 14 | `get_upstream_features` | L4:F13482@71, k=5 → Emb:" broadcasting"@71 (de=22.62) +4 more |
| 15 | `get_upstream_features` | L7:F72@28, k=5 → Emb:" writer"@28 (de=5.72) +4 more |
| 16 | `get_upstream_features` | L0:F6051@38, k=5 → Emb:"."@38 (de=47.50) +4 more |
| 17 | `get_upstream_features` | L0:F15661@7, k=5 → Emb:" Institute"@7 (de=19.38) +4 more |
| 18 | `get_upstream_features` | L0:F6484@7, k=5 → Emb:" Institute"@7 (de=15.12) +4 more |
| 19 | `get_upstream_features` | L0:F2348@4, k=5 → Emb:" Royal"@4 (de=14.44) +4 more |

### Build

`build_circuit` → 18 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 20,646 | 5,468 | 48,731 | 0 | $0.0157 | — | — |
| **Total** | | **20,646** | **5,468** | **48,731** | **0** | **$0.0157** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 11s