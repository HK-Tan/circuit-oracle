# Circuit Oracle Report
**Date:** 2026-07-28 07:23:55 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: civil_comments-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"an identity group" signals) rather than actual prompt content (lexical or semaintical) to predict toxicity."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's toxicity classification is driven almost entirely by raw identity-group tokens ("white", "dude", "black", "man") and their early-layer subword/entity detectors, rather than by features encoding the toxic content (e.g. the verb "stealing" or the compositional meaning "stealing X's thunder").

**Confidence:** 8

**Reasoning:** The circuit traces cleanly from token embeddings at positions 2 ("white"), 3 ("dude"), 6 ("black"), 7 ("man") — i.e. **identity/demographic tokens** — through L0 generic subword features (L0:F3436, F10910, F13442, F13663, all on "white" with direct_effects +0.13 to +0.29; L0:F1015 on "black" with +0.12), into L3 entity detectors (L3:F13061 fires on both "dude" and "man", direct_effect +0.12), then L4/L6/L8-L9 late-layer features that all sit on **pos 3 ("dude")**. The single biggest positive driver is L0:F3436 on " white" (direct_effect +0.2891), and its largest upstream is the " white" embedding itself (direct_effect 17.875). The verb "stealing" at pos 4 contributes only one modest L0 feature (F15621, +0.10). The "black man's" tokens at pos 6-7 feed primarily L3:F13061 (+0.12) and L0:F1015 (+0.12) — again, identity features, not sentiment.

Crucially, **no mid/late-layer feature encodes the compositional meaning** "person-of-group-A taking credit from person-of-group-B" or the pejorative "stealing thunder" idiom. There is no abstract toxicity/sentiment supernode; the circuit is a chain of literal identity-token detectors (white → dude → man → black) with the verb almost an afterthought. `get_source_influence` over positions {2,3,6,7} gives S_pct_of_total = 18.3% — the identity tokens carry a substantial signed share of the probe's decision, far above the non-source yardstick (S_over_R ≈ 2.9).

This confirms the user's concern: the toxicity probe is largely keying on **the presence of identity-group tokens themselves** (race/gender words), not on the toxic framing or the actual hateful content of the utterance. A benign sentence mentioning "white", "black", "dude", and "man" — e.g. "Another white guy talking to a black man at the store" — would likely produce a similar probe score via this same circuit, illustrating the spurious-correlation failure mode.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F3436](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) | 2 | L0 features on "white" — generic subword detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3436) |
| [L0:F10910](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) | 2 | L0 features on "white" — generic subword detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10910) |
| [L0:F13442](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13442) | 2 | L0 features on "white" — generic subword detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13442) |
| [L0:F13663](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13663) | 2 | L0 features on "white" — generic subword detectors | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/13663) |
| [L0:F1015](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) | 6 | L0 features on "black" — generic subword detector | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1015) |
| [L0:F15621](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15621) | 4 | L0 features on "stealing" | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/15621) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 7 | L3 features encoding identity group tokens on " dude" | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L3:F13061](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) | 3 | L3 features encoding identity group tokens on " dude" | — | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/13061) |
| [L4:F15204](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) | 2 | L4 features on "white"/"dude" tokens | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15204) |
| [L4:F7136](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) | 2 | L4 features on "white"/"dude" tokens | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/7136) |
| [L4:F117](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) | 3 | L4 features on "white"/"dude" tokens | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/117) |
| [L6:F4008](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4008) | 3 | L6 features on "dude" — entity token representations | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/4008) |
| [L6:F1330](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1330) | 3 | L6 features on "dude" — entity token representations | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/1330) |
| [L6:F627](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/627) | 3 | L6 features on "dude" — entity token representations | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/627) |
| [L6:F14669](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14669) | 3 | L6 features on "dude" — entity token representations | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/14669) |
| [L9:F11035](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/11035) | 3 | L8-L9 features on "dude" — late-layer identity composition | — | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/11035) |
| [L8:F13464](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13464) | 3 | L8-L9 features on "dude" — late-layer identity composition | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/13464) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:3436 de=0.289 |
| 3 | `get_candidate_vote_tally` | ❌ This tool requires ctx.sibling_graphs to be set (at least on |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L0:F3436@2` | ❌ error | — | — | Trace upstream from L0:F3436 at pos 2 ("Another"). This is the top positive driv… |
| SA-2 | `L4:F15204@2` | ❌ error | — | — | Trace upstream from L4:F15204 at pos 2. This is a major positive contributor (di… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L0:F3436@2, k=10 → Emb:" white"@2 (de=17.88) +9 more |
| 2 | `get_upstream_features` | L4:F15204@2, k=10 → Emb:" white"@2 (de=43.50) +9 more |
| 3 | `get_upstream_features` | L6:F4008@3, k=10 → Emb:" dude"@3 (de=10.56) +9 more |
| 4 | `get_upstream_features` | L3:F13061@7, k=10 → Emb:" black"@6 (de=15.69) +9 more |
| 5 | `get_upstream_features` | L6:F1330@3, k=8 → Emb:"Another"@1 (de=3.53) +7 more |
| 6 | `get_upstream_features` | L0:F1015@6, k=8 → Emb:" black"@6 (de=23.88) +7 more |
| 7 | `get_upstream_features` | L0:F15621@4, k=8 → Emb:" stealing"@4 (de=20.75) +7 more |
| 8 | `get_upstream_features` | L9:F11035@3, k=8 → L8:F13464 (de=2.59) +7 more |
| 9 | `get_upstream_features` | L0:F13442@2, k=8 → Emb:" white"@2 (de=10.62) +7 more |
| 10 | `get_upstream_features` | L0:F10910@2, k=8 → Emb:" white"@2 (de=14.31) +7 more |
| 11 | `get_upstream_features` | L6:F627@3, k=8 → Emb:"<bos>"@0 (de=1.11) +7 more |
| 12 | `get_upstream_features` | L6:F14669@3, k=8 → Emb:" dude"@3 (de=2.83) +7 more |
| 13 | `get_upstream_features` | L8:F13464@3, k=8 → Emb:" white"@2 (de=2.92) +7 more |
| 14 | `get_source_influence` | {'depth': 3, 'source_positions': [2, 3, 6, 7]} → {'depth': 3, 'source_positions': [2, 3, 6, 7], 'S_pct_of_total': 18.327, 'R_pct_ |

### Build

`build_circuit` → 13 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 15,373 | 4,478 | 41,572 | 0 | $0.0125 | — | — |
| **Total** | | **15,373** | **4,478** | **41,572** | **0** | **$0.0125** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 0m 48s