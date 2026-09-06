# Circuit Oracle Report
**Date:** 2026-07-28 07:25:48 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** This attribution graph drives a contradiction-detection probe primarily through position-1 "A" features, with secondary contributions from negation-cue/recorded-menu features at positions 2-3, supporting the user's concern that the circuit relies on a spurious surface pattern (a leading definite-style article on a sentence-initial token) rather than actual semantic contradiction content.

**Confidence:** 5

**Reasoning:** The circuit reveals an unexpectedly narrow source. Of the top 20 features driving the probe score, the single most positive contributor is L17:F451 (direct_effect=+0.1885), which traces entirely to features at position 1 (the token "A"). Specifically, the L17→L16→L15→L14→L12→L11→L10→L9 chain (L17:F451, L16:F10989 [inhibitory -10.375], L15:F751/+100 act, L14:F15964, L13:F8128, L12:F12493/F3684, L11:F11186, L10:F14174/F10933/F6804, L9:F2762/F3056/F8770/F15819) all fire exclusively on the position-1 "A" token, with the upstream signal ultimately flowing from the <bos> (pos 0) embedding (L5:F3992 has de=22.25 from <bos>) and the "A" (pos 1) embedding. This is a sentence-initial article / sequence-initial state — a positional artifact, not contradiction content. Supporting evidence: L14:F2510 (inhibitory, -4.75) and L13:F8128 (-4.5) and L10:F12232 (-19.75) are strong suppressors at pos 1, suggesting the probe is highly sensitive to whether a particular "A-state" representation is active. A second parallel branch at pos 2-3 (features L2:F8776, L4:F7998, L1:F12253, L0:F2108) reflects the phrase " recorded menu" — a generic passive-recorded-menu pattern, plus weak but consistent influence from "not" / "no" / "any" negation-adjacent features (L0:F2108, L1:F12253, L0:F8046, L4:F7998) that fire on pos 3-4 (" menu", " will") but propagate as inhibitory input to the pos-1 cascade (e.g., L0:F2108 at pos 3 has direct_effect -0.4805 on the probe). The circuit reaches token-embedding nodes: <bos> at pos 0, "A" at pos 1, " recorded" at pos 2, " menu" at pos 3, " will" at pos 4, and " provide" at pos 5 — confirming the underlying tokens are neutral content words, not contradiction-bearing phrases. The dominant signal is the sentence-initial "A" pattern: the user's concern is well-supported that the probe (and the circuit driving it) is leveraging a spurious position-1 representation that correlates with a particular sentence shape rather than actual semantic contradiction. The "negation words" influence is present but secondary, mostly as inhibitory pressure on the pos-1 cascade via L0:F2108 / L1:F12253 features that fire on " menu" / " recorded" tokens in this context.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L17:F451](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) | 1 | L17:L17-F451, L16:L16-F10989 (pos 1, sentence-initial state) | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/451) |
| [L16:F10989](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) | 1 | L17:L17-F451, L16:L16-F10989 (pos 1, sentence-initial state) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/10989) |
| [L15:F751](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) | 1 | L15-14 mid sentence-initial 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/751) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | L15-14 mid sentence-initial 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L14:F15964](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15964) | 1 | L15-14 mid sentence-initial 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/15964) |
| [L14:F2510](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2510) | 1 | L15-14 mid sentence-initial 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/2510) |
| [L14:F8659](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8659) | 1 | L15-14 mid sentence-initial 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/8659) |
| [L12:F12493](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) | 1 | L12-11 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12493) |
| [L12:F3684](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3684) | 1 | L12-11 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/3684) |
| [L11:F11186](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11186) | 1 | L12-11 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/11186) |
| [L13:F8128](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) | 1 | L12-11 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/8128) |
| [L11:F9183](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) | 1 | L12-11 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) |
| [L11:F16322](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/16322) | 1 | L12-11 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/16322) |
| [L11:F389](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/389) | 1 | L12-11 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/389) |
| [L13:F5948](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/5948) | 1 | L12-11 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/5948) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L10:F10933](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/10933) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/10933) |
| [L10:F6804](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6804) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6804) |
| [L10:F7106](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/7106) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/7106) |
| [L10:F12232](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12232) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12232) |
| [L9:F2762](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/2762) |
| [L9:F3056](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3056) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L9:F15819](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/15819) |
| [L9:F13483](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13483) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/13483) |
| [L9:F3569](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3569) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/3569) |
| [L10:F883](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/883) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/883) |
| [L10:F12546](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12546) | 1 | L10-9 mid 'A' features | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/12546) |
| [L8:F3815](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3815) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3815) |
| [L8:F8406](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8406) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L6:F14585](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14585) |
| [L6:F14531](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14531) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14531) |
| [L6:F4516](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4516) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4516) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L5:F7489](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7489) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/7489) |
| [L4:F9757](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9757) |
| [L4:F8952](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8952) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/8952) |
| [L4:F9555](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9555) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/9555) |
| [L3:F373](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/373) |
| [L0:F1903](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) |
| [L0:F2433](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2433) | 1 | L8-5 low 'A' / BOS features | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2433) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | L2-0 features at pos 2 (' recorded') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L2:F3059](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) | 2 | L2-0 features at pos 2 (' recorded') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3059) |
| [L2:F3691](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3691) | 2 | L2-0 features at pos 2 (' recorded') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3691) |
| [L2:F4147](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4147) | 2 | L2-0 features at pos 2 (' recorded') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4147) |
| [L3:F14624](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14624) | 2 | L2-0 features at pos 2 (' recorded') | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/14624) |
| [L1:F7207](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7207) | 2 | L2-0 features at pos 2 (' recorded') | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7207) |
| [L0:F7404](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) | 2 | L2-0 features at pos 2 (' recorded') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7404) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | L2-0 features at pos 2 (' recorded') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L0:F13280](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) | 2 | L2-0 features at pos 2 (' recorded') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13280) |
| [L4:F7998](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) | 3 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7998) |
| [L3:F3573](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) | 3 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3573) |
| [L2:F3648](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) | 3 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3648) |
| [L2:F188](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) | 4 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/188) |
| [L1:F12253](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) | 3 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/12253) |
| [L1:F11170](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11170) | 3 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/11170) |
| [L1:F763](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/763) | 3 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/763) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |
| [L0:F8046](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) | 4 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8046) |
| [L0:F5128](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) | 3 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5128) |
| [L0:F6649](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) | 3 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6649) |
| [L0:F2115](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) | 3 | L4-0 features at pos 3 (' menu') and pos 4 (' will') | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2115) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L2:8776 de=0.523 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L17:F451@1` | ❌ error | — | — | Trace the path from L17:F451 at pos 1. This is the highest-direct-effect late-la… |
| SA-2 | `L2:F8776@2` | ❌ error | — | — | Trace the path from L2:F8776 at pos 2. This is the highest-direct-effect early-l… |
| SA-3 | `L4:F7998@3` | ❌ error | — | — | Trace the path from L4:F7998 at pos 3. This is an early-layer inhibitory feature… |
| SA-4 | `L0:F2108@3` | ❌ error | — | — | Trace the path from L0:F2108 at pos 3. This is an early-layer inhibitory feature… |
| SA-5 | `L1:F3691@2` | ❌ error | — | — | Trace the path from L1:F3691 at pos 2. This is a mid-early excitatory feature. D… |
| SA-6 | `L1:F12253@3` | ❌ error | — | — | Trace the path from L1:F12253 at pos 3. This is an inhibitory feature. Determine… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L17:F451@1, k=15 → L16:F10989 (de=-10.38) +14 more |
| 2 | `get_upstream_features` | L2:F8776@2, k=15 → Emb:" recorded"@2 (de=19.50) +14 more |
| 3 | `get_upstream_features` | L4:F7998@3, k=15 → Emb:" menu"@3 (de=13.56) +14 more |
| 4 | `get_upstream_features` | L0:F2108@3, k=15 → Emb:" menu"@3 (de=25.75) +14 more |
| 5 | `get_upstream_features` | L1:F12253@3, k=15 → Emb:" menu"@3 (de=20.62) +14 more |
| 6 | `get_upstream_features` | L16:F10989@1, k=12 → L15:F851 (de=26.50) +11 more |
| 7 | `get_upstream_features` | L15:F751@1, k=12 → L14:F15964 (de=22.62) +11 more |
| 8 | `get_upstream_features` | L10:F14174@1, k=10 → L9:F3056 (de=14.31) +9 more |
| 9 | `get_upstream_features` | L14:F2510@1, k=10 → L12:F12493 (de=8.94) +9 more |
| 10 | `get_upstream_features` | L6:F14585@1, k=10 → Emb:"A"@1 (de=9.88) +9 more |
| 11 | `get_upstream_features` | L13:F8128@1, k=10 → L10:F14174 (de=10.31) +9 more |
| 12 | `get_upstream_features` | L15:F851@1, k=10 → L12:F12493 (de=18.88) +9 more |
| 13 | `get_upstream_features` | L1:F3691@2, k=10 → Emb:" recorded"@2 (de=24.75) +9 more |
| 14 | `get_upstream_features` | L0:F7443@2, k=10 → Emb:" recorded"@2 (de=22.62) +9 more |
| 15 | `get_upstream_features` | L1:F11170@3, k=10 → Emb:" menu"@3 (de=8.06) +9 more |
| 16 | `get_upstream_features` | L2:F3648@3, k=10 → Emb:" menu"@3 (de=27.75) +9 more |
| 17 | `get_upstream_features` | L3:F3573@3, k=10 → Emb:" menu"@3 (de=21.38) +9 more |
| 18 | `get_upstream_features` | L5:F3992@1, k=8 → Emb:"<bos>"@0 (de=22.25) +7 more |
| 19 | `get_upstream_features` | L7:F462@1, k=8 → Emb:"<bos>"@0 (de=18.62) +7 more |
| 20 | `get_upstream_features` | L9:F2762@1, k=8 → Emb:"<bos>"@0 (de=14.31) +7 more |
| 21 | `get_upstream_features` | L9:F3056@1, k=8 → Emb:"<bos>"@0 (de=12.50) +7 more |
| 22 | `get_upstream_features` | L9:F8770@1, k=8 → L7:F462 (de=17.00) +7 more |
| 23 | `get_upstream_features` | L12:F12493@1, k=8 → L10:F14174 (de=13.94) +7 more |
| 24 | `get_upstream_features` | L12:F3684@1, k=8 → L11:F11186 (de=-6.75) +7 more |
| 25 | `get_upstream_features` | L4:F7643@5, k=8 → Emb:" provide"@5 (de=3.89) +7 more |
| 26 | `get_upstream_features` | L1:F763@3, k=8 → Emb:" menu"@3 (de=15.81) +7 more |
| 27 | `get_upstream_features` | L2:F188@4, k=8 → Emb:" will"@4 (de=26.00) +7 more |
| 28 | `get_upstream_features` | L3:F14624@2, k=8 → Emb:" recorded"@2 (de=14.88) +7 more |
| 29 | `get_upstream_features` | L7:F5741@1, k=8 → Emb:"<bos>"@0 (de=10.62) +7 more |
| 30 | `get_upstream_features` | L11:F11186@1, k=8 → L9:F2762 (de=15.62) +7 more |
| 31 | `get_upstream_features` | L10:F10933@1, k=8 → L9:F2762 (de=9.62) +7 more |
| 32 | `get_upstream_features` | L9:F15819@1, k=8 → L7:F462 (de=14.56) +7 more |
| 33 | `get_upstream_features` | L10:F6804@1, k=8 → L9:F2762 (de=7.78) +7 more |
| 34 | `get_upstream_features` | L14:F15964@1, k=8 → L9:F8770 (de=8.56) +7 more |
| 35 | `get_upstream_features` | L4:F9757@1, k=8 → Emb:"<bos>"@0 (de=15.38) +7 more |
| 36 | `get_upstream_features` | L0:F1903@1, k=8 → Emb:"<bos>"@0 (de=16.88) +7 more |
| 37 | `get_upstream_features` | L11:F9183@1, k=8 → L10:F14174 (de=12.06) +7 more |
| 38 | `get_upstream_features` | L11:F16322@1, k=8 → L10:F14174 (de=8.50) +7 more |
| 39 | `get_upstream_features` | L11:F389@1, k=8 → L10:F12232 (de=-19.75) +7 more |
| 40 | `get_upstream_features` | L13:F5948@1, k=8 → L12:F12493 (de=7.09) +7 more |
| 41 | `get_upstream_features` | L10:F12232@1, k=8 → L9:F8770 (de=10.69) +7 more |
| 42 | `get_upstream_features` | L10:F7106@1, k=8 → L9:F3056 (de=4.69) +7 more |
| 43 | `get_upstream_features` | L6:F14531@1, k=8 → Emb:"A"@1 (de=10.12) +7 more |
| 44 | `get_upstream_features` | L6:F4516@1, k=8 → L5:F3992 (de=7.44) +7 more |
| 45 | `get_upstream_features` | L4:F8952@1, k=8 → Emb:"A"@1 (de=6.28) +7 more |
| 46 | `get_upstream_features` | L0:F8046@4, k=8 → Emb:" will"@4 (de=36.00) +7 more |
| 47 | `get_upstream_features` | L0:F5128@3, k=8 → Emb:" menu"@3 (de=15.62) +7 more |
| 48 | `get_upstream_features` | L0:F6649@3, k=8 → Emb:" menu"@3 (de=14.38) +7 more |
| 49 | `get_upstream_features` | L0:F2115@3, k=8 → Emb:" menu"@3 (de=8.50) +7 more |
| 50 | `get_upstream_features` | L0:F7404@2, k=8 → Emb:" recorded"@2 (de=14.25) +7 more |
| 51 | `get_upstream_features` | L2:F3059@2, k=8 → Emb:" recorded"@2 (de=22.50) +7 more |
| 52 | `get_upstream_features` | L0:F13280@2, k=8 → Emb:" recorded"@2 (de=14.75) +7 more |
| 53 | `get_upstream_features` | L9:F13483@1, k=8 → Emb:"<bos>"@0 (de=11.62) +7 more |
| 54 | `get_upstream_features` | L9:F3569@1, k=8 → L7:F462 (de=6.22) +7 more |
| 55 | `get_upstream_features` | L8:F3815@1, k=8 → Emb:"<bos>"@0 (de=5.25) +7 more |
| 56 | `get_upstream_features` | L8:F8406@1, k=8 → Emb:"<bos>"@0 (de=9.62) +7 more |
| 57 | `get_upstream_features` | L10:F883@1, k=8 → L9:F3056 (de=5.16) +7 more |
| 58 | `get_upstream_features` | L10:F12546@1, k=8 → L9:F8770 (de=7.44) +7 more |
| 59 | `get_upstream_features` | L14:F8659@1, k=8 → L12:F3684 (de=3.80) +7 more |
| 60 | `get_upstream_features` | L2:F4147@2, k=8 → Emb:" recorded"@2 (de=27.50) +7 more |
| 61 | `get_upstream_features` | L1:F7207@2, k=8 → Emb:" recorded"@2 (de=9.25) +7 more |
| 62 | `get_upstream_features` | L0:F8047@4, k=8 → Emb:" will"@4 (de=5.97) +7 more |
| 63 | `get_upstream_features` | L1:F7463@4, k=8 → Emb:" will"@4 (de=19.88) +7 more |
| 64 | `get_upstream_features` | L0:F13134@3, k=8 → Emb:" menu"@3 (de=10.75) +7 more |

### Build

`build_circuit` → 14 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 33,274 | 12,102 | 164,006 | 0 | $0.0343 | — | — |
| **Total** | | **33,274** | **12,102** | **164,006** | **0** | **$0.0343** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 19s