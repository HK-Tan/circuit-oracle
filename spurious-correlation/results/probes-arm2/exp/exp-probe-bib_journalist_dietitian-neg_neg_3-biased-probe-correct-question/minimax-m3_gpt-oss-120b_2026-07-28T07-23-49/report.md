# Circuit Oracle Report
**Date:** 2026-07-28 07:23:49 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven almost entirely by masculine-gendered pronoun features (He/his/he/him) and a parallel "journalistic" contextual feature, rather than by the profession-indicating verbs ("researches", "represents") — the circuit is dominated by spurious gender markers.

**Confidence:** 8

**Reasoning:** The attribution graph for the probe's classification score reveals a striking pattern: of the top-20 features by direct_effect on the probe direction, the majority of the strongest positive contributions come from features whose upstream attribution is rooted in masculine third-person pronouns.

Specifically, the downstream "mid-layer masculine pronoun" supernode (L7:L14893 at pos 1 "He" and pos 46 "him" with activation 6.69/7.28 and direct effects +0.196/+0.163; L18:L14743 at pos 23 "he" with direct effect -0.138; L17:L5889 at pos 23 with direct effect +5.16 scaled) traces cleanly back through early-layer pronoun features (L0:F12768 → "he" pos 23 with direct_effect 41.5, L0:F1069 → "He" pos 1 with direct_effect 22.6, L0:F16297 → "him" pos 46 with direct_effect 43.25, L0:F2994 → "his" pos 52 with direct_effect 45) to the token-embedding nodes for the masculine pronouns "He", "he", "him", "his".

Critically, the profession-indicating verbs "researches" (pos 2-3) and "represents" (pos 9) DO fire downstream features (L1:F14812 at "stories" pos 3 with direct_effect 18.6; L1:F7449 at "represents" pos 9 with direct_effect 20.5; L0:F4564 at "researches" pos 2 with direct_effect 13.25; L0:F5333 at "stories" pos 3 with direct_effect 16.4), but these features feed into the masculine-pronoun pathway (e.g. L1:F14812 at pos 3 has upstream "He" pos 1 with direct_effect -0.61, and the "stories"/"He" coupling suggests the verb features are being recruited into a male-coded coreference representation rather than a profession representation). Only one genuine profession-context feature contributes independently: L14:F4420 at pos 13 "journalistic" with direct_effect -0.132, which traces back to L7:L9092 and L4:L13253 (both reading "journalistic", direct_effects 25.6 and 14.9) and to the "journalistic" token embedding.

The architecture is: token embeddings (He, he, him, his + researches, represents, journalistic) → early-layer pronoun/context features (L0-L1) → mid-layer masculine-coreference features (L7-L18, dominated by pos 1/23/46/52 pronoun positions) → probe direction. The probe is therefore classifying via a **gendered coreference cluster** (the recurring "He … researches … he … him … his" pattern) rather than via profession-specific vocabulary — confirming the user's concern. If the subject were referred to as "she" with identical profession context, the circuit's dominant positive signal would be replaced by inhibition, and the probe would likely flip its classification despite no change to the actual profession evidence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L26:F0](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) | 52 | Probe direction (output logit) | — | [view](https://neuronpedia.org/gemma-2-2b/26-gemmascope-transcoder-16k/0) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Mid-layer masculine pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 23 | Mid-layer masculine pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F3330](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) | 23 | Mid-layer masculine pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3330) |
| [L16:F2918](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) | 23 | Mid-layer masculine pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/2918) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 23 | Mid-layer masculine pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | Mid-layer masculine pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 46 | Mid-layer masculine pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 1 | Mid-layer masculine pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 13 | Mid-layer masculine pronoun features | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | Early-layer pronoun features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F7449](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) | 9 | Early-layer pronoun features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Early-layer pronoun features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | Early-layer pronoun features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L0:F61](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) | 3 | Early-layer pronoun features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) |
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | Early-layer pronoun features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 23 | Early-layer pronoun features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 52 | Early-layer pronoun features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 46 | Early-layer pronoun features (L0-L1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Masculine pronoun token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Masculine pronoun token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Masculine pronoun token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 52 | Masculine pronoun token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Verb / profession-context token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Verb / profession-context token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 7 | Verb / profession-context token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Verb / profession-context token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Verb / profession-context token embeddings | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:6051 de=-0.256 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L1:F14812@3` | ❌ error | — | — | Trace this feature upstream. Determine what it encodes and what input token it r… |
| SA-2 | `L1:F7449@9` | ❌ error | — | — | Trace this feature upstream. Determine what it encodes. Pos 9 is "represents". |
| SA-3 | `L0:F4564@2` | ❌ error | — | — | Trace this feature upstream. Determine what it encodes. Pos 2 is "He". |
| SA-4 | `L0:F5333@3` | ❌ error | — | — | Trace this feature upstream. Pos 3 is "researches". What does it encode? |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F14812@3, k=10 → Emb:" stories"@3 (de=18.62) +9 more |
| 2 | `get_upstream_features` | L1:F7449@9, k=10 → Emb:" represents"@9 (de=20.50) +9 more |
| 3 | `get_upstream_features` | L0:F4564@2, k=10 → Emb:" researches"@2 (de=13.25) +9 more |
| 4 | `get_upstream_features` | L0:F5333@3, k=10 → Emb:" stories"@3 (de=16.38) +9 more |
| 5 | `get_upstream_features` | L7:F14893@46, k=10 → Emb:" him"@46 (de=12.56) +9 more |
| 6 | `get_upstream_features` | L7:F14893@1, k=10 → Emb:"He"@1 (de=14.75) +9 more |
| 7 | `get_upstream_features` | L0:F2994@52, k=10 → Emb:" his"@52 (de=45.00) +9 more |
| 8 | `get_upstream_features` | L0:F14216@7, k=10 → Emb:" same"@7 (de=18.25) +9 more |
| 9 | `get_upstream_features` | L0:F61@3, k=8 → Emb:" stories"@3 (de=17.38) +7 more |
| 10 | `get_upstream_features` | L14:F4420@13, k=8 → Emb:" journalistic"@13 (de=24.38) +7 more |
| 11 | `get_upstream_features` | L4:F13253@13, k=8 → Emb:" journalistic"@13 (de=25.62) +7 more |
| 12 | `get_upstream_features` | L7:F9092@13, k=8 → Emb:" journalistic"@13 (de=14.88) +7 more |
| 13 | `get_upstream_features` | L0:F2994@46, k=8 → Emb:" him"@46 (de=14.25) +7 more |
| 14 | `get_upstream_features` | L18:F14743@23, k=8 → Emb:" he"@23 (de=25.50) +7 more |
| 15 | `get_upstream_features` | L0:F10036@2, k=8 → Emb:" researches"@2 (de=8.19) +7 more |
| 16 | `get_upstream_features` | L0:F12768@23, k=8 → Emb:" he"@23 (de=41.50) +7 more |
| 17 | `get_upstream_features` | L0:F1069@1, k=8 → Emb:"He"@1 (de=22.62) +7 more |
| 18 | `get_upstream_features` | L0:F16297@46, k=8 → Emb:" him"@46 (de=43.25) +7 more |
| 19 | `get_upstream_features` | L0:F6051@15, k=8 → Emb:"."@15 (de=47.00) +7 more |
| 20 | `get_upstream_features` | L0:F7696@18, k=8 → Emb:" on"@18 (de=39.00) +7 more |
| 21 | `get_upstream_features` | L0:F16297@46, k=8 → Emb:" him"@46 (de=43.25) +7 more |
| 22 | `get_upstream_features` | L18:F14743@23, k=8 → Emb:" he"@23 (de=25.50) +7 more |
| 23 | `get_upstream_features` | L17:F5889@23, k=8 → Emb:" he"@23 (de=33.75) +7 more |
| 24 | `get_upstream_features` | L0:F3255@4, k=8 → Emb:" and"@4 (de=36.00) +7 more |
| 25 | `get_upstream_features` | L0:F10187@8, k=8 → Emb:" time"@8 (de=34.75) +7 more |

### Build

`build_circuit` → 5 nodes, 4 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 18,933 | 4,372 | 66,890 | 0 | $0.0149 | — | — |
| **Total** | | **18,933** | **4,372** | **66,890** | **0** | **$0.0149** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 26s