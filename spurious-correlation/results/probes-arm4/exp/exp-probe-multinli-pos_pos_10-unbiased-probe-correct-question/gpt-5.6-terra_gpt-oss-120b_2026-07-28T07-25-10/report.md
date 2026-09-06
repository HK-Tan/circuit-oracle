# Circuit Oracle Report
**Date:** 2026-07-28 07:25:10 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_10 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s contradiction score is driven primarily by lexical/template cues—especially the second-sentence word **“not”**—plus unrelated surface features such as *strangest*, rather than by a clean representation that the two propositions negate one another.

**Confidence:** 8/10

**Reasoning:** The saved circuit identifies a strong **Lexical negation detector** path from `Emb: not (pos 17)` into `L0:4958` and `L3:12079`, then into the probe score. `L0:4958` is a highly selective literal-*not* feature (`frac_nonzero=0.0184`), and `L3:12079` is labelled “negations and Chinese names” (`frac_nonzero=0.00976`), with multiple top activations directly on *not/no*. Critically, the direct upstream attribution to `L3:12079` is dominated by the raw embeddings `There` at position 15 (+15) and `not` at position 17 (+6.22). This is evidence for recognizing the local construction **“There is not …”**, not for comparing the semantic truth conditions of both sentences.

A second path reinforces this conclusion: `L4:4492` is a multilingual-negation feature (`frac_nonzero=0.03828`) and is itself positively fed by the `not` embedding (+6.56). It contributes to the late **generic/topic/template** node containing `L10:6670` and `L12:12606`. However, those late features do not provide convincing contradiction semantics: `L10:6670` is labelled technical/scientific terminology (`frac_nonzero=0.07189`), despite occurring at the repeated word *reversal* in the second sentence, while `L12:12606` mixes political-conspiracy, mental-condition, and storytelling associations (`frac_nonzero=0.01623`). Both receive their largest positive embedding contribution from *not* (+6.78 and +6.56, respectively); *reversal* gives much smaller positive support (+2.34 / +1.88), and *democracy* is only +1.27 into `L12:12606`. Thus the late path appears to blend negation with generic topical/template activity, not compute “the same relation is asserted, then denied.”

There is also a separate, evidently spurious lexical route: `Emb: strangest (pos 2)` strongly excites `L4:12799` (+31). `L4:12799` is a rare strangeness/-ly feature (`frac_nonzero=0.00827`) whose promoted tokens include **“Weird,” “strangely,” “strange,”** and **“weirdly.”** Its antecedent `L2:16097` is a superlative feature (`frac_nonzero=0.00952`) promoting **“highest,” “largest,” “best,”** etc. This path directly affects the probe, but *strangest* is not logically diagnostic of contradiction. It suggests that stylistic or unusual-language markers can move the classifier score independently of entailment structure.

The score also contains substantial opposing contributions, including `L4:5709` (−0.371; astronomy-labelled, but locally dominated by the token *now*, with upstream embedding effect +40.25) and `L6:12420` (−0.342; “breaking conventions,” locally fed chiefly by *role*, +5.59). These are further signs that the probe direction is a mixture of incidental lexical directions rather than an interpretable contradiction-specific computation.

Overall, the circuit supports the user’s concern. The positive classification mechanism is principally **“a negated second sentence / `There is not` pattern,”** supplemented by **surface superlative/oddness** and weak topic/template signals. It does use some prompt content—particularly *not*, *There*, and to a lesser degree *reversal*—but there is no clear high-level comparison circuit tying the first sentence’s claim (“role reversal … concerns democracy”) to the second sentence’s denial of that same claim.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Lexical negation detector |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L3:F12079](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) | 17 | Lexical negation detector | negations and Chinese names | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/12079) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Cross-sentence negation feature | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L2:F16097](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) | 2 | Superlative/strangeness lexical feature | superlative adjectives and the words "test" or "point" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/16097) |
| [L4:F12799](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) | 2 | Superlative/strangeness lexical feature |  words ending in "-ly" along with phrases that contain the word 'odd' or 'oddities' | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12799) |
| [L10:F6670](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) | 19 | Late generic/topic/template features | technical terms, especially within scientific or medical contexts | [view](https://neuronpedia.org/gemma-2-2b/10-gemmascope-transcoder-16k/6670) |
| [L12:F12606](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) | 21 | Late generic/topic/template features |  phrases related to political conspiracy/organizations, mental conditions and storytelling terms | [view](https://neuronpedia.org/gemma-2-2b/12-gemmascope-transcoder-16k/12606) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:5709 de=-0.371 |
| 3 | `inspect_feature` ×6 | L10:6670, L12:12606, L4:12799, L3:12079, L4:5709, L6:12420 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L10:F6670@19` | ❌ error | — | — | Trace this positive probe-driving feature to embeddings. Determine whether it de… |
| SA-2 | `L12:F12606@21` | ❌ error | — | — | Trace this positive probe-driving late feature upstream to embeddings; determine… |
| SA-3 | `L4:F12799@2` | ❌ error | — | — | Trace this early positive probe-driving feature to token embeddings and identify… |
| SA-4 | `L3:F12079@17` | ❌ error | — | — | Trace this positive probe-driving feature at the second sentence upstream to emb… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L3:F12079@17, k=15 → Emb:" There"@15 (de=15.00) +14 more |
| 2 | `get_upstream_features` | L12:F12606@21, k=15 → Emb:" not"@17 (de=6.56) +14 more |
| 3 | `get_upstream_features` | L10:F6670@19, k=15 → Emb:" not"@17 (de=6.78) +14 more |
| 4 | `get_upstream_features` | L4:F12799@2, k=15 → Emb:" strangest"@2 (de=31.00) +14 more |
| 5 | `get_upstream_features` | L6:F12420@4, k=15 → Emb:" role"@3 (de=5.59) +14 more |
| 6 | `get_upstream_features` | L4:F5709@9, k=15 → Emb:" now"@9 (de=40.25) +14 more |
| 7 | `inspect_feature` ×5 | L4:4492, L0:4958, L4:6072, L2:16097, L7:905 |

### Build

`build_circuit` → 9 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 22,422 | 2,488 | 72,150 | 0 | $0.1114 | — | — |
| **Total** | | **22,422** | **2,488** | **72,150** | **0** | **$0.1114** | | |

**Oracle wall-clock time:** 0m 37s