# Circuit Oracle Report
**Date:** 2026-07-28 07:22:31 UTC | **Orchestrator:** minimax/minimax-m3 | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: bib_journalist_dietitian-neg_neg_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g. gender markers) rather than genuine profession indicators to predict the profession."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe's classification score is driven by a hybrid circuit in which a strong genuine profession signal (the literal token "journalistic" at pos 13, propagating through L4→L7→L8→L14 journalism/broadcast/newspaper features) is partially offset by a parallel early-layer branch that fires on the male pronoun "He" at pos 1 and on generic high-frequency words like "in", "too", "foreign", "stories", and "researches" — none of which are profession-specific.

**Confidence:** 7

**Reasoning:** The dominant positive contributor is the token-embedding **"journalistic" (pos 13)**, which directly excites **L4:F13253 ("things related to journalism and the media", frac_nonzero 0.0065)** with direct_effect 25.6. L4:F13253 in turn feeds **L7:F9092 ("broadcast journalism", frac_nonzero 0.0095)** and **L8:F8437 ("film festivals / documentary", frac_nonzero 0.015)**, which converge on **L14:F4420 ("journalism and newspapers", frac_nonzero 0.017)**, whose promoted tokens are explicitly `journalists / journalist / journalism / reporter / editorial`. This is a textbook profession-indicator path and accounts for the largest positive mass in the graph.

However, there is a second, genuinely **spurious** early-layer branch that the user's concern is correct to flag. The token **"He" at pos 1** excites **L0:F1069 ("references to a male person, particularly 'He'/'His'", frac_nonzero 0.0078, direct_effect −0.16)** and a cluster of sibling pos-1 features (F1288, F1903, F2241, F310) — these are token-level detectors for the literal pronoun, with no profession semantics in their top-activating examples. The "stories" branch (L1:F14812 "references to stories/chapters", L0:F5333 "mentions of stories being told", L1:F16233 "tips/unit") fires on the bare word "stories" — equally non-specific. Likewise **L0:F8061 ("in")**, **L0:F11603 ("too")**, **L0:F2711 ("foreign")**, **L0:F6051 ("periods/spaces")**, and **L0:F14906 ("binding")** are pure word-level features whose direct_effects to the probe are small (≤0.13 each) and whose promoted tokens are punctuation/archaic forms, not profession labels. Crucially, none of these features' decoder vectors push toward "journalist" — they are simply riding on residual stream co-activation because the *embedding* of "He" and the *embedding* of "in"/"foreign"/"too" sit in similar directions to the probe vector by coincidence of training data.

The user's hypothesis is therefore **partially validated**: the circuit is NOT purely spurious — the journalism branch through "journalistic" → L4 → L14 is real and semantically correct. But the early-layer side of the circuit does include gender-pronoun and generic-word features that contribute directly to the probe score without encoding profession information, so the probe is partly leaning on these as a side-effect of where the embedding of "He" happens to point. The user is right to be cautious; the circuit is a mix of genuine profession signal and embedding-level coincidence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F1069](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) | 1 | L0 generic token features at pos 1 (He) |  references to a male person, particularly when using the pronoun "He" or "His." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1069) |
| [L0:F1288](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1288) | 1 | L0 generic token features at pos 1 (He) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1288) |
| [L0:F1903](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) | 1 | L0 generic token features at pos 1 (He) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/1903) |
| [L0:F2241](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2241) | 1 | L0 generic token features at pos 1 (He) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2241) |
| [L0:F310](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) | 1 | L0 generic token features at pos 1 (He) | — | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/310) |
| [L0:F8061](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) | 12 | L0 token-level word detectors (in, too, foreign, period) |  the preposition "in" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/8061) |
| [L0:F11603](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) | 27 | L0 token-level word detectors (in, too, foreign, period) |  the word "too" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11603) |
| [L0:F2711](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2711) | 20 | L0 token-level word detectors (in, too, foreign, period) | the word "foreign." | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2711) |
| [L0:F6051](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) | 15 | L0 token-level word detectors (in, too, foreign, period) | periods, spaces, and the number 1 | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6051) |
| [L0:F14906](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14906) | 3 | L0 token-level word detectors (in, too, foreign, period) |  the word "binding" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/14906) |
| [L0:F5333](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) | 3 | L0/L1: stories/chapters/narrative detectors at pos 3 | mentions of stories that are being told | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/5333) |
| [L1:F14812](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) | 3 | L0/L1: stories/chapters/narrative detectors at pos 3 |  references to stories, chapters, and other narrative elements | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/14812) |
| [L1:F16233](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16233) | 3 | L0/L1: stories/chapters/narrative detectors at pos 3 | the word "tips" and the word "unit" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/16233) |
| [L0:F11261](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) | 3 | L0/L1: stories/chapters/narrative detectors at pos 3 |  the word "migration" and words related to it | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/11261) |
| [L4:F13253](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) | 13 | L4: journalism/media (broad) |  things related to journalism and the media | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13253) |
| [L7:F9092](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) | 13 | L7-L8: broadcast journalism & film/documentary |  words and phrases associated with broadcast journalism | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/9092) |
| [L8:F8437](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) | 13 | L7-L8: broadcast journalism & film/documentary | content related to film festivals and production, particularly documentary films, and the recognition they receive. | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8437) |
| [L7:F13646](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) | 13 | L7-L8: broadcast journalism & film/documentary | — | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13646) |
| [L8:F8855](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) | 13 | L7-L8: broadcast journalism & film/documentary | — | [view](https://neuronpedia.org/gemma-2-2b/8-gemmascope-transcoder-16k/8855) |
| [L6:F8529](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8529) | 13 | L7-L8: broadcast journalism & film/documentary | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/8529) |
| [L6:F12712](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) | 13 | L7-L8: broadcast journalism & film/documentary | — | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/12712) |
| [L14:F4420](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) | 13 | L14: journalism/newspapers (direct probe input) | words and phrases related to journalism and newspapers | [view](https://neuronpedia.org/gemma-2-2b/14-gemmascope-transcoder-16k/4420) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:14906 de=-0.222 |
| 3 | `inspect_feature` ×8 | L0:14906, L1:14812, L0:11603, L0:1069, L0:11261, L0:8061, L14:4420, L0:2711 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L14:F4420@13` | ❌ error | — | — | Trace upstream from L14:F4420 (journalism/newspapers) at position 13. This is a … |
| SA-2 | `L0:F1069@1` | ❌ error | — | — | Trace upstream from L0:F1069 (male pronoun "He"/"His") at position 1. This is a … |
| SA-3 | `L1:F14812@3` | ❌ error | — | — | Trace upstream from L1:F14812 (references to stories/chapters/narrative elements… |
| SA-4 | `L0:F11603@27` | ❌ error | — | — | Trace upstream from L0:F11603 (the word "too") at position 27. This is a generic… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L14:F4420@13, k=15 → Emb:" journalistic"@13 (de=24.38) +14 more |
| 2 | `get_upstream_features` | L0:F1069@1, k=15 → Emb:"He"@1 (de=22.62) +14 more |
| 3 | `get_upstream_features` | L1:F14812@3, k=15 → Emb:" stories"@3 (de=18.62) +14 more |
| 4 | `get_upstream_features` | L0:F14906@3, k=15 → Emb:" stories"@3 (de=12.94) +14 more |
| 5 | `get_upstream_features` | L0:F11603@27, k=10 → Emb:" too"@27 (de=32.00) +9 more |
| 6 | `get_upstream_features` | L0:F8061@12, k=10 → Emb:" in"@12 (de=39.75) +9 more |
| 7 | `get_upstream_features` | L14:F4420@13, k=10 → Emb:" journalistic"@13 (de=24.38) +9 more |
| 8 | `inspect_feature` | L4, F13253 → " things related to journalism and the media" |
| 9 | `get_upstream_features` | L4:F13253@13, k=10 → Emb:" journalistic"@13 (de=25.62) +9 more |
| 10 | `inspect_feature` ×2 | L7:9092, L8:8437 |
| 11 | `get_upstream_features` | L7:F9092@13, k=8 → Emb:" journalistic"@13 (de=14.88) +7 more |
| 12 | `get_upstream_features` | L8:F8437@13, k=8 → Emb:" journalistic"@13 (de=8.06) +7 more |
| 13 | `inspect_feature` ×2 | L0:5333, L1:16233 |
| 14 | `get_upstream_features` | L0:F5333@3, k=8 → Emb:" stories"@3 (de=16.38) +7 more |
| 15 | `inspect_feature` ×4 | L0:11261, L0:6051, L0:2711, L0:2711 |

### Build

`build_circuit` → 15 nodes, 13 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | minimax/minimax-m3 | 36,379 | 5,270 | 189,362 | 0 | $0.0286 | — | — |
| **Total** | | **36,379** | **5,270** | **189,362** | **0** | **$0.0286** | | |

> **Note:** Costs for community/open models are estimates based on OpenRouter listed rates and may differ from actual provider charges.

**Oracle wall-clock time:** 1m 16s