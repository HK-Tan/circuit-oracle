# Circuit Oracle Report
**Date:** 2026-07-28 07:25:07 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_3 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction-probe score is driven primarily by a direct lexical/syntactic negation circuit for “does not,” with a smaller independent castle/fortification-topic signal; the traced graph does not show a feature that compares the first sentence’s specific proposition with the second sentence’s denial.

**Confidence:** 8/10

**Reasoning:** The output is a synthetic probe target (rather than a vocabulary prediction), and its top direct drivers include early and mid/late features with both positive and negative signed effects. The dominant positive interpretable route is clearly the final-sentence negation at positions 35–36:

- **Emb: ` does` (pos 35)** and especially **Emb: ` not` (pos 36)** directly excite the late negation pathway. `not` has a very large positive edge into L16:F6800 (**+12.50**) and into the earlier L4:F4492 (**+17.63**); `does` directly excites L15:F11794 (**+7.19**) and L16:F6800 (**+9.06**).
- The **Local negation form detectors** supernode consists of:
  - **L3:F3534 at pos 36**, labelled a detector for the character sequence *“n't”* / related forms (frequency **0.00775**), which positively feeds L15:F11794 (**+2.48**) and L16:F6800 (**+3.06**).
  - **L4:F4492 at pos 36**, labelled multilingual negation (frequency **0.03828**), directly driven by the `not` embedding and positively feeding L16:F6800 (**+1.09**) and L15:F11794 (**+0.68**).
- The **Negation/disagreement accumulator** contains:
  - **L15:F11794 at pos 36**, “phrases that express disagreement or negation,” frequency **0.01387**. Its strongest upstream lexical inputs are `does` and `not`; this is not evidence of sentence-to-sentence factual comparison.
  - **L16:F6800 at pos 36**, “negations ‘not’, ‘no’, and contractions with ‘t’,” frequency **0.03101**. It has a direct positive effect of **+0.208** on the probe direction, one of the strongest positive late-layer drivers found.
  
Together, these form the `does`/`not` → local-negation-features → negation/disagreement-accumulator → **Contradiction classification-probe score** branch recorded in the circuit. This is strong evidence for the user’s concern: the probe substantially relies on the explicit **“does not”** cue, a stereotyped surface marker of contradiction.

There is also a separate **castle/fortification lexical-semantic** branch:

- **Emb: ` castle` (pos 2)** strongly drives L4:F13244 (**+18.50**) and L4:F5749 (**+14.75**).
- **L4:F13244**, labelled land/property/estate terminology (frequency **0.00451**), is an imperfect but plausible domain-related detector in this castle description. It positively feeds L7:F13215 (**+2.27**).
- **L4:F5749**, labelled ancient settlements and fortifications (frequency **0.00542**), has especially strong activation evidence from fortification-related text and positively feeds L7:F13215 (**+8.25**).
- **L7:F13215**, labelled military fortifications (frequency **0.00380**) and promoting tokens such as *“fortification,” “fortifications,”* and *“fortified,”* has a positive direct effect on the probe (**+0.209**).

Thus the probe does encode some genuine lexical-semantic content about the subject being a castle/fortification. However, that branch only recognizes the topic/entity category; it does **not** demonstrate that the model retrieved the first clause *“comprises an early 17th-century tower house”*, aligned it to the later *“does not contain any early 17th-century tower houses,”* and computed their incompatibility. In particular, no traced high-impact pathway tied the earlier content words such as *“comprises,” “tower house,”* or *“early 17th-century”* to the late negation accumulator or to an explicit relation/comparison feature.

Some top direct probe effects are also clearly non-semantic or weakly relevant: e.g. L0:F2158 is simply **“with”** (frequency **0.02309**, +0.277), while L0:F10346 and L3:F232 detect **“itself”** (with negative probe effects, −0.242 and −0.228). These indicate that the linear probe direction also reads out incidental wording and template artifacts, not solely contradiction reasoning.

Overall, the saved circuit supports a **mixed but negation-dominated** account: `not`/`does` supplies the clearest causal signal; `castle` supplies a separate subject-topic signal. The available circuit evidence does not support a robust compositional contradiction mechanism based on comparing the exact two propositions.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L3:F3534](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) | 36 | Local negation form detectors | the character sequence "n't" or "nut" | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/3534) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 36 | Local negation form detectors | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L15:F11794](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) | 36 | Negation/disagreement accumulator |  phrases that express disagreement or negation | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/11794) |
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 36 | Negation/disagreement accumulator |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L4:F13244](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) | 2 | Castle/fortification lexical detectors |  terms related to land ownership and administration, possibly including slavery or other forms of forced labor | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/13244) |
| [L4:F5749](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) | 2 | Castle/fortification lexical detectors |  terms that describe ancient settlements and fortifications | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5749) |
| [L7:F13215](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) | 2 | Fortification concept feature |  terms used to describe military fortifications. | [view](https://neuronpedia.org/gemma-2-2b/7-gemmascope-transcoder-16k/13215) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:2158 de=0.277 |
| 3 | `inspect_feature` ×7 | L0:2158, L0:10346, L4:13244, L0:12378, L3:232, L4:4492, L16:6800 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F6800@36` | ❌ error | — | — | Trace this late feature driving the contradiction-probe score to embeddings. Det… |
| SA-2 | `L7:F13215@2` | ❌ error | — | — | Trace this feature driving probe score to embeddings. Determine its semantic rol… |
| SA-3 | `L4:F4492@36` | ❌ error | — | — | Trace this feature at the final sentence upstream to embeddings. Investigate if … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F6800@36, k=20 → Emb:" not"@36 (de=12.50) +19 more |
| 2 | `get_upstream_features` | L4:F4492@36, k=20 → Emb:" not"@36 (de=17.62) +19 more |
| 3 | `get_upstream_features` | L7:F13215@2, k=20 → L4:F5749 (de=8.25) +19 more |
| 4 | `get_upstream_features` | L4:F13244@2, k=20 → Emb:" castle"@2 (de=18.50) +19 more |
| 5 | `inspect_feature` ×5 | L7:13215, L2:2415, L15:11794, L3:3534, L4:5749 |
| 6 | `get_upstream_features` | L15:F11794@36, k=20 → Emb:" does"@35 (de=7.19) +19 more |
| 7 | `get_upstream_features` | L4:F5749@2, k=20 → Emb:" castle"@2 (de=14.75) +19 more |

### Build

`build_circuit` → 8 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 28,389 | 2,630 | 75,867 | 0 | $0.1294 | — | — |
| **Total** | | **28,389** | **2,630** | **75,867** | **0** | **$0.1294** | | |

**Oracle wall-clock time:** 0m 35s