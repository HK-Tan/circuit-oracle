# Circuit Oracle Report
**Date:** 2026-07-28 07:23:28 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification is driven by a mix of profession-relevant content (journalism features detecting "freelance writer", "Institute") AND a prominent chain of male-pronoun ("he/his/him") features that originate from position 22 and trace back to the " he" token embedding, supporting the user concern that gender markers are central to the circuit.

**Confidence:** 7

**Reasoning:** The circuit reveals a striking asymmetry. On the *profession* side, the **journalism_chain** (L14:F4420 "journalism/newspapers", L8:F8855 "news reporters", L7:F13646 "news reporting", L6:F12712 "editors/publishers", L4:F13253 "journalism/media") drives the probe from the "writer" / "freelance" token embeddings at positions 27-28 (direct_effect ≈ -0.071 at L14, all negative). The **institute_feature** (L1:F4459) fires on the "Institute" token embedding at position 7 (direct_effect = -0.088) and encodes the research-institute name. These are legitimate profession indicators.

However, the **dominant** late-layer signal is a chain of **male-pronoun features** all firing at *position 22* (the " he" token): L0:F12768 (he/she in proximity, frac_nonzero 0.011), L1:F8685 (the pronoun "he", frac_nonzero 0.003), L2:F6155, L4:F14796 ("he/him"), L4:F15567 (pronouns+writing, frac_nonzero 0.017), L6:F12990 (male pronouns+titles, frac_nonzero 0.068), L6:F6622 (pronouns+legal, frac_nonzero 0.098), L7:F14946 (his/he/him, frac_nonzero 0.017), L13:F1937, L14:F14097 ("he"), L15:F10510, L17:F5889, and culminating in L18:F14743 ("He", frac_nonzero 0.018) with direct_effect = -0.12 on the probe. This chain traces cleanly back to **Emb: he (pos 22)** with direct_effect 40.25 at L0 and 28.6 at L18, and the BPE-token-level signal is so strong it survives 18+ layers of refinement as a pure "is the subject male" feature.

The user's concern is **valid**: the male-pronoun chain (a) originates almost exclusively from a single token (pos 22 "he") with no profession/role content, (b) spans 6+ distinct features across 14 layers (heavy representation in the top-20 list: L18:F14743, L14:F14097, L7:F14946, L6:F12990, L0:F12768, L0:F6556, L1:F4459, L0:F4870), and (c) competes with — and arguably outweighs — the actual profession-relevance features. Note L0:F12768 suppresses "he" (promoted: punctuation) while firing on contextually-he tokens; combined with L6:F12990 (male titles) and L18:F14743 (He pronoun), the circuit encodes "male subject" as a strong, redundant signal. A female journalist (e.g., "she has written for the Guardian...") would lack this entire chain at pos 22, suggesting the probe is partially picking up subject gender rather than the journalistic profession alone. The profession content (journalism_chain + institute_feature) is real and present, but the male-pronoun chain is the more redundantly-encoded and earlier-grounded signal in the attribution graph.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 22 | "He"-pronoun late features (tone-down suppressors, pos=22) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |
| [L17:F5889](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) | 22 | "He"-pronoun late features (tone-down suppressors, pos=22) |  references to people with pronouns and possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/17-gemmascope-transcoder-16k/5889) |
| [L15:F10510](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10510) | 22 | "He"-pronoun late features (tone-down suppressors, pos=22) |  references to males in third person and first person pronouns | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10510) |
| [L14:F14097](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) | 22 | "He"-pronoun late features (tone-down suppressors, pos=22) |  occurrences of the word "he" | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/14097) |
| [L13:F1937](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/1937) | 22 | Mid-layer male-pronoun features (pos=22) |  pronouns used to describe people, including possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/1937) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 22 | Mid-layer male-pronoun features (pos=22) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L6:F12990](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) | 22 | Mid-layer male-pronoun features (pos=22) |  male pronouns and titles along with descriptors associated with men | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12990) |
| [L6:F6622](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6622) | 22 | Mid-layer male-pronoun features (pos=22) |  pronouns and possessive pronouns in the context of legal and athletic situations | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/6622) |
| [L4:F14796](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) | 22 | Mid-layer male-pronoun features (pos=22) | the pronoun "he" or "him" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/14796) |
| [L4:F15567](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) | 22 | Mid-layer male-pronoun features (pos=22) | sentences with male or female pronouns and possessives, especially ones referring to writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15567) |
| [L1:F8685](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8685) | 22 | Early male-pronoun features (pos=22) |  the pronoun "he" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8685) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 22 | Early male-pronoun features (pos=22) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L2:F6155](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6155) | 22 | Early male-pronoun features (pos=22) |  references to people, especially pronouns like "he" or "she" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/6155) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 28 | Journalism/newspaper profession features (pos=28, profession-relevant) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 28 | Journalism/newspaper profession features (pos=28, profession-relevant) |  mentions of news reporters and news reporting | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 28 | Journalism/newspaper profession features (pos=28, profession-relevant) |  news reporting and journalism. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 28 | Journalism/newspaper profession features (pos=28, profession-relevant) |  titles of editors and publishers in scientific publications | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 28 | Journalism/newspaper profession features (pos=28, profession-relevant) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L1:F4459](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) | 7 | Research-institute name feature (pos=7) |  mentions of research institutes | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/4459) |
| [L1:F15323](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) | 1 | "starting" academic-paper opener (pos=1) | the word "starting" in academic papers | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15323) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:7124 de=-0.160 |
| 3 | `inspect_feature` ×15 | L0:7124, L18:14743, L1:15323, L0:15661, L0:3820, L14:14097, L7:14946, L6:12990, L14:4420, L0:12768, L1:4459, L0:6556, L0:4870, L0:5288, L0:6051 |

### Dispatch: 6 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L18:F14743@22` | ❌ error | — | — | Trace the upstream path from L18:F14743 (the "He" male-pronoun feature, pos 22).… |
| SA-2 | `L14:F4420@28` | ❌ error | — | — | Trace the upstream path from L14:F4420 (the "journalism/newspapers" feature, pos… |
| SA-3 | `L1:F4459@7` | ❌ error | — | — | Trace the upstream path from L1:F4459 (the "research institutes" feature, pos 7,… |
| SA-4 | `L18:F14743@22` | ❌ error | — | — | Trace the upstream path from L18:F14743 (the "He" male-pronoun feature, pos 22).… |
| SA-5 | `L14:F4420@28` | ❌ error | — | — | Trace the upstream path from L14:F4420 (the "journalism/newspapers" feature, pos… |
| SA-6 | `L1:F4459@7` | ❌ error | — | — | Trace the upstream path from L1:F4459 (the "research institutes" feature, pos 7,… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L18:F14743@22, k=12 → Emb:" he"@22 (de=28.62) +11 more |
| 2 | `get_upstream_features` | L14:F4420@28, k=12 → Emb:" writer"@28 (de=5.75) +11 more |
| 3 | `get_upstream_features` | L1:F4459@7, k=12 → Emb:" Institute"@7 (de=27.50) +11 more |
| 4 | `get_upstream_features` | L14:F14097@22, k=12 → Emb:" he"@22 (de=2.70) +11 more |
| 5 | `get_upstream_features` | L7:F14946@22, k=12 → Emb:" he"@22 (de=14.19) +11 more |
| 6 | `get_upstream_features` | L6:F12990@22, k=12 → Emb:" he"@22 (de=6.50) +11 more |
| 7 | `get_upstream_features` | L1:F15323@1, k=10 → Emb:"Starting"@1 (de=16.38) +9 more |
| 8 | `get_upstream_features` | L0:F12768@22, k=8 → Emb:" he"@22 (de=40.25) +7 more |
| 9 | `get_upstream_features` | L0:F12768@22, k=10 → Emb:" he"@22 (de=40.25) +9 more |
| 10 | `get_upstream_features` | L6:F12990@22, k=8 → Emb:" he"@22 (de=6.50) +7 more |
| 11 | `inspect_feature` ×3 | L17:5889, L13:1937, L4:15567 |
| 12 | `get_upstream_features` | L17:F5889@22, k=8 → Emb:" he"@22 (de=37.50) +7 more |
| 13 | `get_upstream_features` | L14:F4420@28, k=10 → Emb:" writer"@28 (de=5.75) +9 more |
| 14 | `get_upstream_features` | L13:F1937@22, k=8 → Emb:" he"@22 (de=8.94) +7 more |
| 15 | `inspect_feature` ×4 | L8:8855, L4:13253, L7:13646, L6:12712 |
| 16 | `get_upstream_features` | L4:F14796@22, k=8 → Emb:" he"@22 (de=21.25) +7 more |
| 17 | `get_upstream_features` | L15:F10510@22, k=8 → Emb:" he"@22 (de=7.19) +7 more |
| 18 | `inspect_feature` ×2 | L4:14796, L15:10510 |
| 19 | `get_upstream_features` | L1:F8685@22, k=8 → Emb:" he"@22 (de=29.00) +7 more |
| 20 | `get_upstream_features` | L8:F8855@28, k=8 → Emb:" writer"@28 (de=4.72) +7 more |
| 21 | `get_upstream_features` | L6:F12712@28, k=8 → Emb:" writer"@28 (de=6.22) +7 more |
| 22 | `get_upstream_features` | L7:F13646@28, k=8 → Emb:" writer"@28 (de=2.77) +7 more |
| 23 | `inspect_feature` | L1, F8685 → " the pronoun "he"" |
| 24 | `get_upstream_features` | L14:F14097@22, k=8 → Emb:" he"@22 (de=2.70) +7 more |
| 25 | `get_upstream_features` | L1:F15323@1, k=8 → Emb:"Starting"@1 (de=16.38) +7 more |
| 26 | `get_upstream_features` | L0:F12768@22, k=8 → Emb:" he"@22 (de=40.25) +7 more |
| 27 | `get_upstream_features` | L6:F6622@22, k=8 → Emb:" he"@22 (de=6.88) +7 more |
| 28 | `inspect_feature` ×3 | L3:9548, L2:6155, L6:6622 |
| 29 | `get_upstream_features` | L13:F1937@22, k=8 → Emb:" he"@22 (de=8.94) +7 more |
| 30 | `get_upstream_features` | L6:F643@28, k=8 → ❌ Feature (layer=6, pos=28, feature_idx=643) not found in grap |
| 31 | `get_upstream_features` | L6:F1515@28, k=8 → ❌ Feature (layer=6, pos=28, feature_idx=1515) not found in gra |
| 32 | `get_upstream_features` | L2:F11473@22, k=8 → Emb:" he"@22 (de=33.75) +7 more |
| 33 | `get_upstream_features` | L7:F11318@22, k=8 → L0:F12768 (de=1.41) +7 more |
| 34 | `get_upstream_features` | L6:F5941@22, k=8 → Emb:" he"@22 (de=4.47) +7 more |
| 35 | `get_upstream_features` | L2:F11473@22, k=8 → Emb:" he"@22 (de=33.75) +7 more |
| 36 | `get_upstream_features` | L7:F11318@22, k=8 → L0:F12768 (de=1.41) +7 more |

### Build

`build_circuit` → 14 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 69,993 | 6,925 | 621,235 | 0 | $0.0666 | — | — |
| **Total** | | **69,993** | **6,925** | **621,235** | **0** | **$0.0666** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 2m 11s