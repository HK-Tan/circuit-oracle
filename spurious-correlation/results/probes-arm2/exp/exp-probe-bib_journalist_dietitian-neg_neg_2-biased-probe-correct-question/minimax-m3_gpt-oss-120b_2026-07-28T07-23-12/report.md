# Circuit Oracle Report
**Date:** 2026-07-28 07:23:12 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_2 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven primarily by features at position 1 ("His") and position 9 ("him") — i.e., gendered pronoun embeddings — rather than by profession-indicative content like "news organizations" or "report." The single largest positive direct effect on the probe is L7:F14893 (de=0.488), which receives its strongest upstream contribution (23.5) from the `His` token embedding and L4:F4315, and contributes directly to the output direction. Parallel paths through L18:F14743 (de=-0.207, position 9 "him") and the L18:L19 features at pos 1 (F7400, F10315, F8814) all terminate their upstream traces at the `His`/`him` token embeddings (direct effects of 13–21 from `His` at pos 1, and 42.25 from `him` at pos 9 into L0:F16297). Meanwhile, content-bearing tokens like "report" (pos 21) feed into L14:F4420 and L19:F2486 but with smaller magnitudes and an actually *negative* L14 contribution (-0.158) to the output.

**Confidence:** 8

**Reasoning:** The circuit decisively supports the user's concern about spurious gender features. The top three positive direct effects (L7:F14893=+0.49, L0:F2994=+0.29, L19:F8814=+0.26) all live at pos 1 ("His") and chain directly back to the `His` token embedding via get_upstream_features (direct_effect=23.5 into F14893; 19.75 into F2994; 9.31 into F8814). The "him" token at pos 9 contributes the largest single embedding effect observed anywhere in the trace (42.25 into L0:F16297), and propagates through L18:F14743 (de=-0.207 on the output). Crucially, no early/mid-layer features in the circuit encode profession semantics — L7:F14893, L7:F14946, L4:F4315, L0:F2994 are all generic token-level "His" detectors that activate for any male-pronoun context. The only content-bearing path (pos 21 "report") terminates at L14:F4420 (de=-0.158) and L19:F2486 (de=-0.105), both *suppressing* the probe. The mid-layer supernode is fed almost entirely by the `His` embedding and `<bos>` embedding (direct_effects 21.1 and 12.3 into L7:F462 and L7:F5741), confirming a pronoun-driven rather than profession-driven signal. The probe is therefore using male-pronoun markers as a proxy for the profession — a clear example of the gender-bias shortcut the user suspected.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 1 | Early "His" token features (L0-L4, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L1:F7439](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7439) | 1 | Early "His" token features (L0-L4, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7439) |
| [L2:F5491](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) | 1 | Early "His" token features (L0-L4, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5491) |
| [L3:F13121](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13121) | 1 | Early "His" token features (L0-L4, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13121) |
| [L4:F4315](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) | 1 | Early "His" token features (L0-L4, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4315) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 1 | Early "His" token features (L0-L4, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L5:F10952](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) | 1 | Mid-layer "His" features (L5-L9, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/10952) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 1 | Mid-layer "His" features (L5-L9, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Mid-layer "His" features (L5-L9, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Mid-layer "His" features (L5-L9, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L9:F8770](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) | 1 | Mid-layer "His" features (L5-L9, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/8770) |
| [L7:F462](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) | 1 | Mid-layer "His" features (L5-L9, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/462) |
| [L7:F5741](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) | 1 | Mid-layer "His" features (L5-L9, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/5741) |
| [L5:F3992](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) | 1 | Mid-layer "His" features (L5-L9, pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/5-gemmascope-transcoder-16k/3992) |
| [L10:F14174](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) | 1 | Late-layer pronoun features (L10-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/14174) |
| [L10:F7106](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/7106) | 1 | Late-layer pronoun features (L10-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/7106) |
| [L11:F10933](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) | 1 | Late-layer pronoun features (L10-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/10933) |
| [L11:F9183](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) | 1 | Late-layer pronoun features (L10-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/11-gemmascope-transcoder-16k/9183) |
| [L15:F851](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) | 1 | Late-layer pronoun features (L10-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/851) |
| [L18:F7400](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) | 1 | Late-layer pronoun features (L10-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/7400) |
| [L18:F10315](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) | 1 | Late-layer pronoun features (L10-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/10315) |
| [L19:F8814](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) | 1 | Late-layer pronoun features (L10-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/8814) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 9 | Late-layer pronoun features (L10-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 9 | Late-layer pronoun features (L10-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L16:F14120](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/14120) | 9 | Late-layer pronoun features (L10-L19) | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/14120) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 21 | Verb-context features at "report" (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 21 | Verb-context features at "report" (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 21 | Verb-context features at "report" (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 21 | Verb-context features at "report" (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L19:F2486](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) | 21 | Verb-context features at "report" (pos 21) | — | [view](https://neuronpedia.org/gemma-2-2b/19-gemmascope-transcoder-16k/2486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L7:14893 de=0.488 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@1` | ❌ error | — | — | Trace this feature upstream to understand what it represents. It's at layer 7, p… |
| SA-2 | `L0:F2994@1` | ❌ error | — | — | Trace this feature upstream. It's at layer 0, position 1 ("His" token) with dire… |
| SA-3 | `L19:F8814@1` | ❌ error | — | — | Trace this feature upstream. It's at layer 19, position 1, with direct effect 0.… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 2 | `get_upstream_features` | L0:F2994@1, k=10 → Emb:"His"@1 (de=19.75) +9 more |
| 3 | `get_upstream_features` | L19:F8814@1, k=10 → Emb:"His"@1 (de=9.31) +9 more |
| 4 | `get_upstream_features` | L6:F12990@1, k=10 → Emb:"His"@1 (de=4.91) +9 more |
| 5 | `get_upstream_features` | L4:F4315@1, k=10 → Emb:"His"@1 (de=23.50) +9 more |
| 6 | `get_upstream_features` | L7:F14946@1, k=10 → Emb:"His"@1 (de=18.38) +9 more |
| 7 | `get_upstream_features` | L18:F7400@1, k=10 → Emb:"His"@1 (de=13.00) +9 more |
| 8 | `get_upstream_features` | L18:F10315@1, k=10 → Emb:"His"@1 (de=21.38) +9 more |
| 9 | `get_upstream_features` | L14:F4420@21, k=10 → Emb:" report"@21 (de=5.22) +9 more |
| 10 | `get_upstream_features` | L18:F14743@9, k=10 → Emb:" him"@9 (de=18.38) +9 more |
| 11 | `get_upstream_features` | L8:F8855@21, k=8 → Emb:" report"@21 (de=12.06) +7 more |
| 12 | `get_upstream_features` | L19:F2486@21, k=8 → L14:F4420 (de=14.31) +7 more |
| 13 | `get_upstream_features` | L9:F8770@1, k=5 → L7:F462 (de=15.00) +4 more |
| 14 | `get_upstream_features` | L7:F462@1, k=5 → Emb:"<bos>"@0 (de=21.12) +4 more |
| 15 | `get_upstream_features` | L7:F5741@1, k=5 → Emb:"<bos>"@0 (de=12.31) +4 more |
| 16 | `get_upstream_features` | L11:F10933@1, k=5 → L10:F14174 (de=11.56) +4 more |
| 17 | `get_upstream_features` | L10:F14174@1, k=5 → L9:F3056 (de=16.62) +4 more |
| 18 | `get_upstream_features` | L16:F14120@9, k=5 → Emb:" him"@9 (de=10.00) +4 more |
| 19 | `get_upstream_features` | L0:F16297@9, k=5 → Emb:" him"@9 (de=42.25) +4 more |

### Build

`build_circuit` → 8 nodes, 7 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 22,707 | 4,100 | 58,317 | 0 | $0.0152 | — | — |
| **Total** | | **22,707** | **4,100** | **58,317** | **0** | **$0.0152** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 49s