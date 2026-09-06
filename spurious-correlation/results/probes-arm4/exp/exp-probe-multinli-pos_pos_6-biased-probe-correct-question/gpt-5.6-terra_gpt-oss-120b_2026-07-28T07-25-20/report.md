# Circuit Oracle Report
**Date:** 2026-07-28 07:25:20 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction-probe score is driven primarily by a lexical negation circuit centered on **“not”** in “They were **not** allowed…”, rather than by a representation of the semantic conflict between deforesting and being prohibited from deforesting.

**Confidence:** 9/10

**Reasoning:** The dominant positive mechanism in the saved circuit is `Emb: not (pos 21) → Lexical not detector → Early multilingual-negation pathway → Late not+copula detector → Output: contradiction-classification probe score`.

- The key late contributor is **L16:12358 at pos 21** (direct effect **+0.3359**). Its label is *“the word ‘not’ followed within a few tokens by a form of the verb ‘to be’”* (fraction nonzero **0.02769**). This is nearly an exact surface description of “were **not** allowed.” Its strongest upstream input is directly the **“ not” embedding at pos 21** (**+19**), not an embedding for *deforest*, *forest*, *allowed*, or their incompatibility.
- **L0:4958 at pos 21** is an explicit *“the word ‘not’”* feature (fraction nonzero **0.0184**) and sends positive signal into L16:12358 (**+6.4062**). This confirms that the high-level detector is built on direct lexical negation recognition.
- The auxiliary pathway is likewise negation-heavy:
  - **L3:8011** (fraction nonzero **0.00299**) promotes variants of **“not”** and receives its overwhelmingly strongest source from the **“not” embedding** (**+21.75**).
  - **L4:4492** is labeled *negations in various languages* (fraction nonzero **0.03828**) and receives **+19.125** directly from “not”; it feeds L16:12358 positively (**+1.3438**) and itself pushes the probe upward (**+0.3105**).
  - **L2:12021** is another negative-term / “not” detector (fraction nonzero **0.0057**), while **L3:1101** and **L4:2422** are opposing or inhibitory variants of absence/negation features. The presence of these competing signs indicates a mixed residual representation, but the net leading route still privileges the positive “not” detectors.

There is little evidence that the main positive route represents the full proposition-level contradiction: *they set fire to forest to clear land for agriculture* versus *they were not allowed to deforest for agriculture*. The one semantic-ish lexical feature among the top direct contributors is **L2:4819**, a “fire” feature, but it is modest (**+0.2617**) and no traced path establishes that it is integrated with *allowed/deforest/agriculture* into an incompatibility computation. “Agriculture” appears only as a weak upstream contributor to the late negation detector (**+1.0625**), far below the direct “not” signal.

There are also clear nuisance lexical influences:
- **L15:2080** at positions 3 and 11 positively drives the probe from the embeddings **“set”** (**+44.5**) and **“setting”** (**+45.75**). The feature is simply *“set followed by articles or prepositions”* (fraction nonzero **0.00926**) and contributes about **+0.1982** at each position. It is not contradiction-specific.
- **L0:3498**, a *“they”* pronoun detector (fraction nonzero **0.02132**), is the largest direct negative contributor at pos 2 (**−0.7852**) and also contributes negatively at the later “They” occurrence. This shows the probe direction contains sensitivity to superficial pronoun/template statistics as well.

Thus the user concern is supported: this classification is substantially driven by **spurious—or at least shortcut—lexical negation evidence**, with generic “set/setting” and pronoun signals also contributing. The text genuinely is contradictory, but the recorded causal circuit does not show robust composition of the two events; it mostly detects the second sentence’s **“were not …”** form and projects that toward the contradiction-probe direction.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 21 | Lexical not detector |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L3:F8011](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) | 21 | Early multilingual-negation pathway |  a mix of words and code fragments from different languages | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/8011) |
| [L3:F1101](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) | 21 | Early multilingual-negation pathway |  error messages and terms indicating absence or negation in software contexts. | [view](https://neuronpedia.org/gemma-2-2b/3-gemmascope-transcoder-16k/1101) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 21 | Early multilingual-negation pathway | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 21 | Early multilingual-negation pathway | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L2:F12021](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) | 21 | Early multilingual-negation pathway | "not" or negative terms, with some bonus for sports-related terms and "purpose". | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/12021) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 21 | Late not+copula detector |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 3 | Set/setting lexical detectors | the phrase "set" followed by articles or prepositions | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L15:F2080](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) | 11 | Set/setting lexical detectors | the phrase "set" followed by articles or prepositions | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/2080) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | They pronoun detector (negative probe direction) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 19 | They pronoun detector (negative probe direction) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:3498 de=-0.785 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@21` | ❌ error | — | — | Trace the strongest late-layer positive contributor to the synthetic contradicti… |
| SA-2 | `L3:F8011@21` | ❌ error | — | — | Trace this early positive feature driving the probe score, identify triggering t… |
| SA-3 | `L4:F4492@21` | ❌ error | — | — | Trace this positive feature at final text position upstream. Establish the lexic… |
| SA-4 | `L0:F3498@2` | ❌ error | — | — | Inspect this strongest direct negative contributor to the probe and identify the… |
| SA-5 | `L15:F2080@3` | ❌ error | — | — | Trace this repeated positive mid-layer contributor (also active at pos11) to det… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×7 | L16:12358, L3:8011, L4:4492, L0:3498, L15:2080, L3:1101, L4:2422 |
| 2 | `get_upstream_features` | L16:F12358@21, k=15 → Emb:" not"@21 (de=19.00) +14 more |
| 3 | `get_upstream_features` | L4:F4492@21, k=15 → Emb:" not"@21 (de=19.12) +14 more |
| 4 | `get_upstream_features` | L3:F8011@21, k=15 → Emb:" not"@21 (de=21.75) +14 more |
| 5 | `get_upstream_features` | L15:F2080@3, k=12 → Emb:" set"@3 (de=44.50) +11 more |
| 6 | `get_upstream_features` | L15:F2080@11, k=12 → Emb:" setting"@11 (de=45.75) +11 more |
| 7 | `get_upstream_features` | L0:F3498@2, k=12 → Emb:" they"@2 (de=42.75) +11 more |
| 8 | `inspect_feature` ×6 | L0:4958, L0:2238, L2:4819, L0:3820, L0:8444, L2:12021 |

### Build

`build_circuit` → 10 nodes, 12 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 25,563 | 2,697 | 83,552 | 0 | $0.1253 | — | — |
| **Total** | | **25,563** | **2,697** | **83,552** | **0** | **$0.1253** | | |

**Oracle wall-clock time:** 0m 47s