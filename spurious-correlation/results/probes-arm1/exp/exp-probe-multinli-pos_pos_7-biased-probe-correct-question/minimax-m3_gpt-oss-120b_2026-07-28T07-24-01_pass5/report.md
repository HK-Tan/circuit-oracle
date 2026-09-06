# Circuit Oracle Report
**Date:** 2026-07-28 07:24:01 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven primarily by a cluster of late-layer features that detect the surface pattern "not … is/will" (negation word followed by a form of "to be"), not by any feature encoding the semantic incompatibility between "towering, steepled abbey" and "lacks a steeple/great height."

**Confidence:** 8

**Reasoning:** The circuit tells a very clear story that **supports the user's concern** — the probe is using a spurious lexical cue.

1. **The dominant late-layer driver is a pure negation-clause detector.** L16:F12358 (direct_effect +0.36, the single largest contributor) is autointerp-labeled *"the word 'not' followed within a few tokens by a form of the verb 'to be'"* (frac_nonzero ≈ 0.028). L16:F9779 (+0.24) is *"negation words or contractions like 'won't', 'not', 'never'"* (frac_nonzero ≈ 0.017). L15:F10071 (+0.15), L15:F3521 (+0.15), and L13:F3295 (+0.19) are all variants of the same pattern: *"negations and equivocations," "is/are not," "not in past/future tense."* All five fire at the "not … is not" / "will not" spans in the second sentence.

2. **Tracing upstream confirms this is a surface cue, not entity knowledge.** The upstream of L16:F12358 is dominated by the **embedding of the literal token "not"** (pos 29, direct_effect 19.5), then the "is" embedding (pos 28, 4.4), then the L0 "not" feature L0:F4958 (6.8), with the L0 "is" feature L0:F11375 (3.1) also contributing. None of the entity-relevant tokens — "abbey," "steeple," "towering," "height," "rock," "sea" — appear as upstream features for any of these negation-clause detectors.

3. **Source-influence decomposition confirms the driver.** `get_source_influence` on the negation positions {18, 23, 28, 29} returns **S_pct_of_total = 13.3%** with S/R = 3.0 (the source positions carry about 3× more signed influence than the strongest non-source position), and the top source features are L3:F8011 (a multi-language "not" detector, top_logits = "not/NOT/Not/ikke/nicht/geen"), L0:F9646, and L0:F4958 (the "not" word feature). Conversely, the entity positions {6,9,10,14,17} ("towering," "abbey," "steepled," "sea," "rock") score S_pct_of_total = 2.1% with S/R = 0.32 — **3× weaker** than the yardstick single non-source driver, so the geography/structure of the building is essentially *not* feeding the probe.

4. **What the entity-side features actually do is generic.** The only mid-layer path that touches content is L14:F10408 at pos 14 ("geographical locations… related to bodies of water," frac_nonzero 0.015, promoted_tokens = "sea, seawater, ocean, beach, marine"), fed by a chain of marine-biology/oceans features (L4:F4173, L6:F3848, L8:F3174). This is a generic *sea-word* detector — it fires on "sea" anywhere and contributes a modest +0.18, not a feature recognizing that "sea-cliff abbey" contradicts "lacks great height/steeple." The remaining top-20 features are pure function-word detectors ("the" L0:F3820 +0.18, "of" L0:F2848 +0.18, "That" L0:F5060 +0.18, "you" L0:F7710 −0.25, "first" L6:F5342 +0.15, "is" L0:F11375 +0.19, courtroom/narrative L4:F3833 +0.17, "yet/ly/but" L1:F15005 −0.15) — none of which encode the contradiction between *towering steepled* and *lacks a steeple/is not of great height*.

5. **The user is correct.** The contradiction signal in this graph is carried by *"the model noticed the word 'not' followed by 'is/will/be'"* — a bag-of-words cue. The features with the highest direct effects on the probe (L16:F12358, L16:F9779, L13:F3295, L15:F10071) are all narrow negation-clause detectors (frac_nonzero 0.01–0.03) that fire on the *word* "not," not on the proposition "the abbey has no steeple, contradicting 'towering, steepled abbey.'" The actual content words that would have to be integrated to recognize the contradiction ("steeple," "height," "towering," "steepled") do not appear as upstream features of any probe-driving feature, and the "sea" feature that *does* fire is generic marine vocabulary, not an entity-attribute binding. This is exactly the spurious-pattern failure mode the user flagged.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 29 | Negation-clause features (L15–L16) |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L16:F9779](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) | 23 | Negation-clause features (L15–L16) | negation words or contractions like "won't", "not", "never" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 29 | Negation-clause features (L15–L16) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L15:F3521](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3521) | 23 | Negation-clause features (L15–L16) | sentences containing words expressing negation or uncertainty in past or future tense | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/3521) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 29 | Negation-clause features (L15–L16) | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 29 | \"not\" token features (L0) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 23 | \"not\" token features (L0) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 29 | \"not\" token features (L0) |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L0:F11375](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) | 18 | \"is\" token feature (L0:11375) |  the word "is" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11375) |
| [L0:F7710](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) | 21 | \"you\" pronoun feature (L0:7710) | the pronoun "you" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7710) |
| [L0:F3820](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) | 5 | \"the\" function-word feature (L0:3820) | the word "the" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3820) |
| [L0:F5060](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5060) | 1 | \"That\" opener feature (L0:5060) | mentions of dinner or breakfast | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5060) |
| [L0:F2848](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) | 4 | \"of\" function-word feature (L0:2848) | the word "of" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2848) |
| [L14:F10408](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) | 14 | \"sea\" geographic feature chain (L14:10408) |  geographical locations, especially related to bodies of water | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/10408) |
| [L4:F4173](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4173) | 14 | \"sea\" geographic feature chain (L14:10408) |  words and phrases related to marine environments or legal terminology related to maritime issues. | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4173) |
| [L6:F3848](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3848) | 14 | \"sea\" geographic feature chain (L14:10408) |  words related to marine biology and fishing | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/3848) |
| [L8:F3174](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3174) | 14 | \"sea\" geographic feature chain (L14:10408) |  words and phrases related to tides and shorelines | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/3174) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L16:12358 de=0.359 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@29` | ❌ error | — | — | Trace upstream from L16:F12358 at pos 29. Determine what this feature encodes (i… |
| SA-2 | `L16:F9779@23` | ❌ error | — | — | Trace upstream from L16:F9779 at pos 23. This is the 4th most important feature … |
| SA-3 | `L0:F7710@21` | ❌ error | — | — | Trace upstream from L0:F7710 at pos 21. This feature has the largest NEGATIVE di… |
| SA-4 | `L0:F3820@5` | ❌ error | — | — | Trace upstream from L0:F3820 at pos 5. This is a layer-0 feature with direct_eff… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L16:12358, L16:9779, L0:7710, L0:3820 |
| 2 | `get_upstream_features` | L16:F12358@29, k=15 → Emb:" not"@29 (de=19.50) +14 more |
| 3 | `get_upstream_features` | L16:F9779@23, k=15 → Emb:" will"@22 (de=7.31) +14 more |
| 4 | `inspect_feature` ×7 | L0:4958, L13:3295, L15:10071, L3:8011, L15:3521, L0:11375, L14:10408 |
| 5 | `get_upstream_features` | L0:F11375@18, k=10 → Emb:" is"@18 (de=32.50) +9 more |
| 6 | `get_upstream_features` | L14:F10408@14, k=10 → Emb:" sea"@14 (de=22.88) +9 more |
| 7 | `get_upstream_features` | L0:F2848@4, k=10 → Emb:" of"@4 (de=35.25) +9 more |
| 8 | `get_upstream_features` | L0:F5060@1, k=10 → Emb:"That"@1 (de=11.88) +9 more |
| 9 | `inspect_feature` ×8 | L4:4173, L6:3848, L8:3174, L0:2848, L0:5060, L3:16223, L4:3833, L4:11810 |
| 10 | `get_upstream_features` | L0:F7710@21, k=10 → Emb:" you"@21 (de=42.25) +9 more |
| 11 | `get_upstream_features` | L0:F3820@5, k=10 → Emb:" the"@5 (de=34.25) +9 more |
| 12 | `get_upstream_features` | L0:F4958@29, k=8 → Emb:" not"@29 (de=34.25) +7 more |
| 13 | `get_upstream_features` | L4:F3833@3, k=8 → Emb:" glimpse"@3 (de=13.56) +7 more |
| 14 | `inspect_feature` ×3 | L6:5342, L4:4605, L1:15005 |
| 15 | `get_source_influence` | {'depth': 3, 'source_positions': [29, 23, 28, 18]} → {'depth': 3, 'source_positions': [18, 23, 28, 29], 'S_pct_of_total': 13.329, 'R_ |
| 16 | `get_source_influence` | {'depth': 3, 'source_positions': [10, 14, 17, 6, 9]} → {'depth': 3, 'source_positions': [6, 9, 10, 14, 17], 'S_pct_of_total': 2.137, 'R |

### Build

`build_circuit` → 20 nodes, 19 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 58,192 | 5,778 | 297,019 | 0 | $0.0422 | — | — |
| **Total** | | **58,192** | **5,778** | **297,019** | **0** | **$0.0422** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 43s