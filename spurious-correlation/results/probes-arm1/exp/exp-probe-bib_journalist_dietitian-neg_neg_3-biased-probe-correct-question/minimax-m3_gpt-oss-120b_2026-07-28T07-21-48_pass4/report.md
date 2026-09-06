# Circuit Oracle Report
**Date:** 2026-07-28 07:21:48 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by two parallel pathways: a legitimate profession-related signal rooted in journalism/media vocabulary, and a competing spurious signal rooted in masculine pronouns that the user suspected.

**Confidence:** 7

**Reasoning:** The circuit reveals two distinct pathways feeding the probe output:

**Legitimate profession pathway (token → concept → output):**
- `Emb: researches/stories/represents/journalistic (pos 2,3,9,13)` → token-level features L0:L4564 ("research"), L0:L61 ("stories"), L0:L5333 ("stories being told"), L1:L14812 ("references to stories"), L1:L7449 ("representation") → `sn_journalism_l4` (L4:F13253, "journalism and the media") → branches into `sn_broadcast_l7` (L7:F9092, "broadcast journalism") and `sn_journalism_l14` (L14:F4420, "journalism and newspapers", promoted tokens: journalists/journalist/reporter) → output. The L4/L7/L14 features are the genuine profession indicators, with frac_nonzero ≈ 0.006–0.017 (highly specific) and promoted tokens explicitly listing "journalists, journalism, reporter, journalism, media."

**Spurious gender pathway (masculine pronouns → output):**
- `Emb: he/him/his (pos 1, 23, 46, 52)` → masculine pronoun token features L0:L2994 ("his/he"), L0:L16297 ("him"), L0:L12768 ("he/she") → `sn_gender_l7` (L7:F14893 "pronouns/possessive pronouns", L7:F14946 "his/he/him") → `sn_he_l18` (L18:F14743, "He" — high activation 421, frac_nonzero 0.018, suppresses "she/her/ihr/their") → output. The L18 feature explicitly *suppresses* feminine pronouns and promotes only masculine self-reference. Its top activating examples all involve "He" as a masculine protagonist.

The user's concern is partially confirmed: the probe does use a masculine-pronoun pathway (L0 pronouns → L7 pronoun consolidator → L18 "He" feature). However, it also uses a genuine journalism-concept pathway (L4 media → L7 broadcast → L14 journalist/reporter). The two pathways are roughly comparable in direct-effect magnitude: the journalism L14 feature has +0.20 direct effect while the L18 "He" feature has -0.14 (negative — but the L7 pronoun features contribute +0.20 positively). The probe is therefore genuinely driven by a mix of (a) correct profession semantics and (b) a co-occurring gender signal that the L18 "He" feature may be using as a spurious correlate. The embedding for "He" at pos 1 and "he" at pos 23 both feed the L7 pronoun node, indicating the model is picking up on the grammatical subject's gender rather than purely the professional vocabulary. This is a legitimate finding for the user's concern: the circuit is **not purely** spurious — it has a real profession path — but it **does contain** a parallel spurious gender path that, without the journalism features, would likely misfire.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 1 | Emb: He (pos 1) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 2 | Emb: researches (pos 2) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 3 | Emb: stories (pos 3) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 9 | Emb: represents (pos 9) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 13 | Emb: journalistic (pos 13) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 23 | Emb: he (pos 23) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 46 | Emb: him (pos 46) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F0](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) | 52 | Emb: his (pos 52) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/0) |
| [L0:F4564](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) | 2 | Token features: 'research' / 'stories' / 'representation' | the word "research." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4564) |
| [L0:F61](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) | 3 | Token features: 'research' / 'stories' / 'representation' | the word "stories" sometimes along with apostrophes and common names. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/61) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | Token features: 'research' / 'stories' / 'representation' | mentions of stories that are being told | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | Token features: 'research' / 'stories' / 'representation' |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F7449](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) | 9 | Token features: 'research' / 'stories' / 'representation' | instances of the word "representation" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/7449) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | Journalism / media concept (L4) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 13 | Broadcast journalism (L7) |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | Journalism / newspapers (L14) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |
| [L0:F2994](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) | 52 | Masculine pronoun token features (L0) | the pronoun "his" and the pronoun "he." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2994) |
| [L0:F16297](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) | 46 | Masculine pronoun token features (L0) |  the pronoun "him" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/16297) |
| [L0:F12768](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) | 23 | Masculine pronoun token features (L0) |  mentions of "he" and "she" in close proximity | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/12768) |
| [L7:F14893](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) | 46 | Pronoun/possessive pronoun features (L7) |  pronouns or possessive pronouns | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14893) |
| [L7:F14946](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) | 1 | Pronoun/possessive pronoun features (L7) |  the possessive pronoun "his" (or similar pronouns like "he" and "him") and some non-ascii characters, especially "©" | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/14946) |
| [L18:F14743](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) | 23 | Pronoun 'He' concept (L18) | He | [view](https://neuronpedia.org/gemma-2-2b/18-gemmascope-transcoder-16k/14743) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L0:6051 de=-0.256 |
| 3 | `inspect_feature` ×8 | L1:14812, L1:7449, L0:4564, L0:5333, L0:61, L0:2994, L7:14893, L0:6051 |
| 4 | `get_upstream_features` | Emb:" his"@52 (de=45.00) +9 more |
| 5 | `get_upstream_features` | Emb:" him"@46 (de=12.56) +9 more |
| 6 | `get_upstream_features` | Emb:" researches"@2 (de=13.25) +9 more |
| 7 | `inspect_feature` ×2 | L7:14946, L7:14893 |

### Dispatch: 2 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L7:F14893@46` | ❌ error | — | — | Trace this pronoun feature (L7:F14893) upstream to find what semantic content it… |
| SA-2 | `L7:F14946@1` | ❌ error | — | — | Trace this possessive pronoun feature (L7:F14946) at position 1 (He) upstream. W… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L1:F14812@3, k=10 → Emb:" stories"@3 (de=18.62) +9 more |
| 2 | `get_upstream_features` | L1:F7449@9, k=10 → Emb:" represents"@9 (de=20.50) +9 more |
| 3 | `get_upstream_features` | L0:F61@3, k=8 → Emb:" stories"@3 (de=17.38) +7 more |
| 4 | `get_upstream_features` | L0:F5333@3, k=8 → Emb:" stories"@3 (de=16.38) +7 more |
| 5 | `get_upstream_features` | L1:F14812@3, k=8 → Emb:" stories"@3 (de=18.62) +7 more |
| 6 | `inspect_feature` ×6 | L0:6051, L0:7696, L0:14216, L18:14743, L14:4420, L4:13253 |
| 7 | `get_upstream_features` | L18:F14743@23, k=8 → Emb:" he"@23 (de=25.50) +7 more |
| 8 | `get_upstream_features` | L14:F4420@13, k=8 → Emb:" journalistic"@13 (de=24.38) +7 more |
| 9 | `get_upstream_features` | L7:F14946@1, k=8 → Emb:"He"@1 (de=11.50) +7 more |
| 10 | `get_upstream_features` | L4:F13253@13, k=8 → Emb:" journalistic"@13 (de=25.62) +7 more |
| 11 | `get_upstream_features` | L17:F5889@23, k=8 → Emb:" he"@23 (de=33.75) +7 more |
| 12 | `inspect_feature` ×10 | L0:12768, L7:9092, L18:14743, L17:5889, L15:3330, L0:16297, L0:10036, L0:9121, L0:10187, L0:3255 |
| 13 | `get_upstream_features` | L7:F9092@13, k=8 → Emb:" journalistic"@13 (de=14.88) +7 more |
| 14 | `get_upstream_features` | L0:F16297@46, k=5 → Emb:" him"@46 (de=43.25) +4 more |
| 15 | `get_upstream_features` | L0:F12768@23, k=5 → Emb:" he"@23 (de=41.50) +4 more |

### Build

`build_circuit` → 16 nodes, 16 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 51,738 | 5,582 | 330,875 | 0 | $0.0421 | — | — |
| **Total** | | **51,738** | **5,582** | **330,875** | **0** | **$0.0421** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 53s