# Circuit Oracle Report
**Date:** 2026-07-28 07:25:16 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven primarily by shallow lexical-token detectors—especially *“Pick up,” “No one,” “usually,” “so,”* and *“here”*—rather than by a composed representation of the contradiction between the two tourist-office statements.

**Confidence:** 8/10

**Reasoning:** The saved circuit shows two competing sets of direct contributors to the synthetic probe direction.

* The **positive probe-direction surface-cue** node contains L0:7321 at *“so”* (pos 25; direct effect **+0.383**, frac_nonzero **0.02377**), L0:306 at *“tourist”* (pos 7; **+0.192**), and L0:7204 at *“here”* (pos 9; **+0.155**, frac_nonzero **0.00968**). These are not contradiction representations. L0:7321 is a highly token-specific detector for *“so”* (with incidental suffix matches); L0:7204 is directly a *“here”* feature. Their embedding paths are correspondingly simple: `Emb: so → L0:7321`, `Emb: tourist → L0:306`, and `Emb: here → L0:7204`. In particular, the *“so”* embedding alone has a very large upstream effect on L0:7321 (**+40.5**).

* The strongest **opposing** contributors are also largely lexical. L0:8974 at *“from”* has direct effect **−0.408** and is a sparse, specific *“from”* detector (frac_nonzero **0.02366**), with its activation sourced almost entirely by `Emb: from` (**+38.75**). L2:3116 at *“up”* has direct effect **−0.350**, is a selective *“pick up”* phrasal-verb detector (frac_nonzero **0.00615**; promotes *pickup* forms), and receives its main positive inputs directly from `Emb: Pick` (**+50**) and `Emb: up` (**+20.75**). The related L2:11769 is simply an *“up”* detector (direct effect **−0.203**, frac_nonzero **0.00530**). These are clear evidence of lexical-template reliance, not a comparison between propositions.

* There is some signal from content that is relevant to contradiction. L2:13586 at *“one”* (direct effect **−0.210**, frac_nonzero **0.00411**) is driven directly by `Emb: No` (**+14**) and `Emb: one` (**+12.875**). L1:8159 at *“usually”* (direct effect **−0.176**, frac_nonzero **0.00523**) is directly sourced by `Emb: usually` (**+24.25**). Thus the probe does react to the phrase *“No one is usually at the tourist office,”* which is semantically relevant: it expresses the unavailability that conflicts with the preceding instruction to obtain a map there.

  However, these features remain a **quantifier/word detector** (*one*) and a **habituality adverb detector** (*usually*), rather than an identified circuit encoding something like “the same office is asserted available and unavailable.” Their autointerp promoted tokens also do not indicate a contradiction concept: L2:13586 promotes generic person/quantifier words such as *anyone/everyone*, while L1:8159 suppresses *usually/normally/typically*.

* L2:14413, a genuine *“tour/tours”* detector (frac_nonzero **0.01117**), also contributes negatively (**−0.174**) and is overwhelmingly sourced by `Emb: tours` (**+28.375**). This confirms that topical lexical content enters the probe, but it does not establish semantic reasoning about the repeated tourist-office relation.

Consequently, the probe is **not driven solely by a spurious negation word**—indeed, there is no ordinary *“not”* detector among the leading features, while *“No one”* and *“usually”* are genuinely relevant parts of the contradiction. But the circuit provides stronger evidence for a shallow classifier that combines isolated lexical correlates and local templates: *pick up*, *up*, *from*, *so*, *here*, *tours*, *No one*, and *usually*. It does **not** show a higher-level, entity-linked comparison tying the first instance of *tourist office* to the later claim that nobody is there, nor a feature specifically representing incompatibility between the two sentences.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F7321](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) | 25 | Positive probe-direction surface cues (so/tourist/here) |  the word "so," and also matches some words ending in "ware" and "such" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7321) |
| [L0:F306](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) | 7 | Positive probe-direction surface cues (so/tourist/here) | the word "adoption" in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/306) |
| [L0:F7204](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) | 9 | Positive probe-direction surface cues (so/tourist/here) | the word "here" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7204) |
| [L0:F8974](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) | 5 | Opposing probe direction: from/pick-up/tours lexical detectors | the word "from" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8974) |
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | Opposing probe direction: from/pick-up/tours lexical detectors |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L2:F11769](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) | 2 | Opposing probe direction: from/pick-up/tours lexical detectors | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11769) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | Opposing probe direction: from/pick-up/tours lexical detectors | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L2:F13586](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) | 17 | Opposing probe direction: No one / usually cues |  words ending in 'thing' and 'one' often with preceding words indicating the presence of something | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/13586) |
| [L1:F8159](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) | 19 | Opposing probe direction: No one / usually cues |  the word "usually" and, to a lesser extent, words that sometimes accompany it | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/8159) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:8974 de=-0.408 |
| 3 | `inspect_feature` ×6 | L0:8974, L0:7321, L2:3116, L2:13586, L0:6051, L0:10904 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F3116@2` | ❌ error | — | — | Trace the strongest negative driver of the probe score upstream to embeddings. D… |
| SA-2 | `L2:F13586@17` | ❌ error | — | — | Trace this negative probe-driving feature upstream to embeddings; determine whet… |
| SA-3 | `L0:F7321@25` | ❌ error | — | — | Trace this strongest positive early feature to its token embedding and character… |
| SA-4 | `L0:F8974@5` | ❌ error | — | — | Trace this strongest negative early feature to its token embedding and character… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L2:F3116@2, k=20 → Emb:"Pick"@1 (de=50.00) +19 more |
| 2 | `get_upstream_features` | L2:F13586@17, k=20 → Emb:" No"@16 (de=14.00) +19 more |
| 3 | `get_upstream_features` | L2:F11769@2, k=20 → Emb:" up"@2 (de=19.50) +19 more |
| 4 | `get_upstream_features` | L2:F14413@14, k=20 → Emb:" tours"@14 (de=28.38) +19 more |
| 5 | `get_upstream_features` | L0:F8974@5, k=20 → Emb:" from"@5 (de=38.75) +19 more |
| 6 | `get_upstream_features` | L0:F7321@25, k=20 → Emb:" so"@25 (de=40.50) +19 more |
| 7 | `inspect_feature` ×6 | L2:11769, L2:14413, L1:8159, L0:306, L0:7204, L0:10562 |
| 8 | `get_upstream_features` | L0:F306@7, k=10 → Emb:" tourist"@7 (de=22.00) +9 more |
| 9 | `get_upstream_features` | L0:F7204@9, k=10 → Emb:" here"@9 (de=41.00) +9 more |
| 10 | `get_upstream_features` | L1:F8159@19, k=10 → Emb:" usually"@19 (de=24.25) +9 more |

### Build

`build_circuit` → 13 nodes, 10 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 29,858 | 3,344 | 75,558 | 0 | $0.1437 | — | — |
| **Total** | | **29,858** | **3,344** | **75,558** | **0** | **$0.1437** | | |

**Oracle wall-clock time:** 0m 45s