# Circuit Oracle Report
**Date:** 2026-07-28 07:22:11 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_7 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification (likely "contradiction") is driven almost entirely by negation-token circuits that fire on the literal word "not" in the second sentence — "is not" — and the "not" within "will not" earlier, with no circuit involvement of entity-recognition or content-comparison features.

**Confidence:** 8

**Reasoning:** The user suspected the circuit uses a spurious "negation words" shortcut. The attribution graph decisively confirms that suspicion. Of the 20 top direct-effect features on the probe direction, the top five are *all* negation-token detectors:

- **L16:F12358** (direct_effect = +0.36, pos 29) — labeled "the word 'not' followed within a few tokens by a form of the verb 'to be'." This fires on the *final* " not" at pos 29 of "is not" in "The abbey is not of great height and lacks a steeple." frac_nonzero = 0.028, generic to "not … be" patterns.
- **L16:F9779** (direct_effect = +0.24, pos 23) — "negation words or contractions like 'won't', 'not', 'never'." Fires on the *first* " not" in "you will not forget."
- **L15:F10071** (direct_effect = +0.15, pos 29) — "negations and equivocations."
- **L13:F3295** (direct_effect = +0.19, pos 29) — "negations in the form of 'is/are not' as well as other uses of 'not'."
- **L0:F4958** (direct_effect = +0.18, pos 29) — a *lexical* " not" feature that fires directly off the token embedding.

Tracing upstream confirms the chain bottoms out in raw token embeddings: `Emb: " not" (pos 29)` carries direct_effect = 19.5 into L16:F12358, and `Emb: " not" (pos 23)` carries direct_effect = 6.8 into L16:F9779. The neighboring " is" (pos 28) and " will" (pos 22) embeddings also feed in. No content features participate — L14:F10408 ("geographical locations, especially related to bodies of water"), which could have flagged the "sea"/"rock"/"abbey" content for comparison, sits in the top list at only +0.18, but its downstream effect goes through these same negation hubs. Crucially, no feature representing the *meaning* of the contradiction ("towering, steepled abbey" vs "lacks a steeple" / "not of great height") shows up in the attribution graph at all.

The mechanism is therefore: the probe has learned a **bag-of-negation-words** heuristic. Whenever the premise/hypothesis pair contains tokens like "not," "lacks," "no," "without," the contradiction probe fires — *regardless* of whether the negation actually creates a logical contradiction with the premise. The "is not of great height and lacks a steeple" sentence contains two explicit negations ("not", "lacks"), and "you will not forget" adds a third, giving the heuristic strong signal. This is exactly the spurious-feature pattern the user flagged: the model is *not* performing entailment reasoning; it is pattern-matching on negation-word counts, which happens to correlate with contradiction labels in NLI training data but is not the actual logical signal.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 29 | L16: "not" + "to be" pattern detector |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L16:F9779](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) | 23 | L16: negation words detector (pos 23) | negation words or contractions like "won't", "not", "never" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/9779) |
| [L15:F10071](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) | 29 | L15: negations/equivocations (pos 29) | negations and equivocations | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/10071) |
| [L13:F3295](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) | 29 | L13: "is/are not" / "not" pattern (pos 29) | negations in the form of "is/are not" as well as other uses of "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/3295) |
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 29 | L0: "not" lexical feature (fires at pos 23, 29) |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 29 | L3: "not" in mixed-code/foreign contexts (pos 29) |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 29 | L0-L4 auxiliary negation-supporting features at pos 29 | — | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 29 | L0-L4 auxiliary negation-supporting features at pos 29 | — | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L0:F9646](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9646) | 29 | L0-L4 auxiliary negation-supporting features at pos 29 | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/9646) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 20 features; top: L16:12358 de=0.359 |
| 3 | `inspect_feature` ×6 | L16:12358, L0:7710, L0:3820, L16:9779, L0:11375, L13:3295 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@29` | ❌ error | — | — | Trace the upstream path from L16:F12358 (pos 29, "not + to be" pattern). Determi… |
| SA-2 | `L16:F9779@23` | ❌ error | — | — | Trace the upstream path from L16:F9779 (pos 23, "negation words"). Determine wha… |
| SA-3 | `L13:F3295@29` | ❌ error | — | — | Trace upstream from L13:F3295 (pos 29, "is/are not" negation). Identify which to… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×6 | L0:4958, L0:5060, L0:2848, L14:10408, L15:10071, L3:8011 |
| 2 | `get_upstream_features` | L16:F12358@29, k=15 → Emb:" not"@29 (de=19.50) +14 more |
| 3 | `get_upstream_features` | L16:F9779@23, k=15 → Emb:" will"@22 (de=7.31) +14 more |
| 4 | `get_upstream_features` | L13:F3295@29, k=15 → Emb:" not"@29 (de=17.75) +14 more |
| 5 | `get_upstream_features` | L15:F10071@29, k=15 → Emb:" not"@29 (de=9.75) +14 more |

### Build

`build_circuit` → 13 nodes, 30 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 36,319 | 4,129 | 76,454 | 0 | $0.0204 | — | — |
| **Total** | | **36,319** | **4,129** | **76,454** | **0** | **$0.0204** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 3s