# Circuit Oracle Report
**Date:** 2026-07-28 07:25:22 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction-probe score is driven mainly by a mixture of shallow lexical/topic features for *castle/tower/early/house* and generic wording, rather than by a circuit that represents the sentence-level contradiction created by “does not contain.”

**Confidence:** 7/10

**Reasoning:** The saved circuit shows substantial prompt-content access, but little evidence that the probe’s positive score is specifically computed from negation or from aligning the repeated proposition across the two sentences.

* **Direct lexical features dominate several of the strongest effects.**  
  * `Emb: tower (pos 13)` strongly feeds the L1 **tower detector** `1:1027`, whose autointerp label is simply “the word *tower*” (`frac_nonzero=0.00423`). This feature contributes **+0.1553** directly to the probe.  
  * `Emb: early (pos 39)` feeds L2 `2:4429`, an **early-period lexical detector** (“mentions of the beginning of a period,” `frac_nonzero=0.00689`), contributing **+0.1187**. This is notable because it fires on the second occurrence of “early,” but it is a word detector—not evidence that the model compared the first claim with its negation.
  * `Emb: castle (pos 2)` has a very large positive upstream effect (**+18.5**) on L4 `4:13244`, a sparse **castle/property association** feature (`frac_nonzero=0.00451`, promoted tokens include “homestead,” “farm,” “property”). That feature is the *largest positive direct driver* of the probe score (**+0.2871**). Its semantics are topical/property-related, not contradiction-related.
  * The L6 `6:486` contextual feature adds **+0.125**. Its label is “Scottish locations and political terms” (`frac_nonzero=0.03752`; promoted tokens include “Scotland,” “Scottish,” “Glasgow”). It receives positive input from `tower`, L4 `4:13244`, L4 `4:5749`, and the house detector. This looks like a historical British/Irish building-topic association, not a logical inference circuit.

* **There is also a strong *negative* house feature, which is lexical and countervailing rather than semantic comparison.**  
  L2 `2:1430` at “house” is the second-largest direct contribution, **−0.2207**. It is explicitly a generic/White-House-or-house feature (`frac_nonzero=0.00277`) and receives overwhelmingly from `Emb: house (pos 14)` (**+30.875**) and weakly from `Emb: tower (pos 13)`. Hence the probe direction happens to penalize a representation of the word *house* while rewarding a castle/property feature. This may reflect quirks of the probe training distribution or its residual direction, rather than an internally represented rule such as “tower house” versus “tower houses.”

* **Generic surface-form cues also directly raise the score.**  
  L0 `0:2158` at “with” contributes **+0.1914** and is exactly a *with* detector (`frac_nonzero=0.02309`), directly sourced from `Emb: with (pos 17)` with **+33.75**. Likewise, L0 `0:7360` at “an” contributes **+0.1582**, directly sourced from `Emb: an (pos 5)` (**+27.375**); and L0 `0:7513` at “together” contributes **+0.1318**, sourced from `Emb: together (pos 26)` (**+43**). These are clear non-semantic correlates of the probe score.

* **The circuit contains genuine subject/topic representations, but does not connect them through a contradiction operation.**  
  L4 `4:5749` is a sparse fortification/ancient-settlement feature (`frac_nonzero=0.00542`, promoted token “Citadel”), and it feeds L6 `6:486`; these are appropriate to *castle/tower* text. The mechanism therefore is not purely random or purely a single negation cue. But the decisive late positive features are topical associations and lexical detectors, while the negation word **“not”** does not appear among the prominent direct features or recovered embedding paths.

**Conclusion on the concern:** This graph supports the concern in a qualified form: the probe is **not primarily using a clean semantic contradiction circuit**. It is not visibly relying on a “not” detector either; instead, it combines spurious lexical/form cues (*with*, *an*, *together*), topic/style cues (castle/property, fortifications, Scottish/Irish-historical context), and opposing *house* lexical evidence. The prompt genuinely is contradictory, but this particular probe score appears to recognize the class through a distributed set of correlated surface/topic features more than through explicit proposition matching plus negation.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F2158](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) | 17 | Early lexical/form cues: with, an, together | the word "with" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2158) |
| [L0:F7360](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7360) | 5 | Early lexical/form cues: with, an, together | the word "an" and sometimes also the acronym COX | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7360) |
| [L0:F7513](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) | 26 | Early lexical/form cues: with, an, together | the word "together" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7513) |
| [L1:F1027](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) | 13 | Tower lexical detector | the word "tower" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/1027) |
| [L2:F1430](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) | 14 | House lexical detector (opposes probe) | mentions of the U.S. White House or a generic house | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1430) |
| [L2:F4429](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) | 39 | Early-period lexical detector |  mentions of the beginning of a period | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4429) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Castle/property association |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 14 | Fortification/settlement context |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L6:F486](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) | 14 | Scottish-location/political contextual feature |  Scottish locations and political terms | [view](https://neuronpedia.org/gemma-2-2b/6-gemmascope-transcoder-16k/486) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:13244 de=0.287 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L4:F13244@2` | ❌ error | — | — | Trace the strongest positive driver of the synthetic contradiction-probe score u… |
| SA-2 | `L6:F486@14` | ❌ error | — | — | Trace this positive probe-score feature to embeddings. Determine its semantic ro… |
| SA-3 | `L2:F1430@14` | ❌ error | — | — | Trace the strongest negative contribution to the probe score to embeddings; char… |
| SA-4 | `L0:F2158@17` | ❌ error | — | — | Inspect and trace this strong early positive driver. Identify the exact source t… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×8 | L4:13244, L6:486, L2:1430, L0:2158, L0:7360, L0:7513, L0:5494, L1:1027 |
| 2 | `get_upstream_features` | L4:F13244@2, k=12 → Emb:" castle"@2 (de=18.50) +11 more |
| 3 | `get_upstream_features` | L6:F486@14, k=12 → L5:F3316 (de=-2.38) +11 more |
| 4 | `get_upstream_features` | L2:F1430@14, k=12 → Emb:" house"@14 (de=30.88) +11 more |
| 5 | `get_upstream_features` | L1:F1027@13, k=12 → Emb:" tower"@13 (de=23.12) +11 more |
| 6 | `get_upstream_features` | L0:F2158@17, k=12 → Emb:" with"@17 (de=33.75) +11 more |
| 7 | `get_upstream_features` | L0:F7360@5, k=12 → Emb:" an"@5 (de=27.38) +11 more |
| 8 | `inspect_feature` ×4 | L0:9604, L4:5749, L2:4429, L0:8974 |
| 9 | `get_upstream_features` | L2:F4429@39, k=10 → Emb:" early"@39 (de=36.50) +9 more |
| 10 | `get_upstream_features` | L0:F7513@26, k=10 → Emb:" together"@26 (de=43.00) +9 more |

### Build

`build_circuit` → 15 nodes, 15 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 23,918 | 3,331 | 83,156 | 0 | $0.1305 | — | — |
| **Total** | | **23,918** | **3,331** | **83,156** | **0** | **$0.1305** | | |

**Oracle wall-clock time:** 0m 49s