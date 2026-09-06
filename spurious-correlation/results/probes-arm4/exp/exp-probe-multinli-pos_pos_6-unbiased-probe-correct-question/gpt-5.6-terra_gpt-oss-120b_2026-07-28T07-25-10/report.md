# Circuit Oracle Report
**Date:** 2026-07-28 07:25:10 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_6 | Probe: unbiased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction-probe score is driven mainly by shallow lexical/template features—especially *land*, *fire*, and “set about”—rather than by a composed representation that the second sentence negates the first; the salient negation itself is not among the leading contributors.

**Confidence:** 8/10

**Reasoning:** The saved circuit separates three positive, content-adjacent signals from substantial non-contradiction/template signals:

- **Agricultural-land lexical detector**: `Emb: land (pos 7)` strongly excites L2:F11518 at the same position (upstream direct effect **+28.38**). Its label is “the word *land* in scientific/agricultural contexts,” with low firing frequency (**frac_nonzero=0.00633**). This feature contributes **+0.252** directly to the probe. It recognizes a salient topic word in the first proposition, but does not itself encode its incompatibility with the later “not allowed” statement.

- **Fire lexical detector**: L2:F4819 at position 12 contributes **+0.179**. It is explicitly a detector for sentences containing *fire* or related terms (**frac_nonzero=0.00667**). This is evidence that the probe uses lexical content relevant to the first statement (“setting fire”), but it remains a single-word/topic detector rather than a contradiction relation feature.

- **Set-about / beginning-template feature**: L4:F5450 at position 4 contributes **+0.214**. Its interpretation is broad “starting/beginning” language (promoted tokens include *begin*, *began*, *beginning*, *started*; **frac_nonzero=0.0051**), fitting “set about.” Its strongest upstream inputs are `Emb: set (pos 3)` (**+3.31**) and `Emb: about (pos 4)` (**+2.34**), plus intermediate same-position features. Thus this positive contribution is mostly a phrase/template cue, not a semantic representation of deforestation being forbidden.

There are also notable **opposing** directions that make the probe score sensitive to incidental wording:

- L0:F3498 on `they` (position 2) is a highly specific pronoun detector (“they”/possessive; **frac_nonzero=0.02132**) and contributes **−0.621**, the single largest absolute direct effect. This is plainly unrelated to contradiction.
- L0:F2238 on `about` (position 4) contributes **−0.342** and is labeled an “about + numerical value” feature (**frac_nonzero=0.00657**), although it activates here in “set about”; again, this is a lexical/form artifact.
- L4:F12225 at position 2 is a discourse-transition feature, promoting *So*, *hence*, *therefore* (**frac_nonzero=0.0129**), with direct effect **−0.275**. It receives very large raw embedding influence from `Emb: So (pos 1)` (**+12.38**) and `Emb: they (pos 2)` (**+12.75**). Its role is rhetorical/syntactic, not contradiction reasoning.

Accordingly, the circuit supports the concern about **spurious cue usage**, though the strongest exposed spurious cues are pronoun, discourse-marker, and phrase-template features—not specifically a *not* detector. The input genuinely contains a contradiction: the first sentence says the group cleared land/set fire to forest for agriculture, while the second says they were not allowed to deforest for agricultural purposes. But the traced high-effect features do not show a dedicated cross-sentence mechanism binding the same agents/actions/purpose and detecting affirmative-versus-prohibition conflict. Instead, the probe direction reads out a mixture of shallow topic words (*land*, *fire*) and incidental form (*they*, *So*, *set about*, *about*).

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F11518](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) | 7 | Agricultural-land lexical detector |  the word "land" in scientific/agricultural contexts | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/11518) |
| [L2:F4819](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) | 12 | Fire lexical detector | sentences containing the word "fire" or similar terms | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/4819) |
| [L4:F5450](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) | 4 | Set-about / beginning-template feature |  code snippets from different languages and words related to starting or beginning something | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/5450) |
| [L4:F12225](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) | 2 | Sentence-initial 'So'/transition feature (opposes probe) |  transitional conclusion words, often used in legal or academic writing | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/12225) |
| [L0:F3498](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) | 2 | They-pronoun feature (opposes probe) |  the pronoun "they" or its possessive form. | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/3498) |
| [L0:F2238](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) | 4 | About lexical/template feature (opposes probe) |  the word "about" when followed by a numerical value | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2238) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L0:3498 de=-0.621 |
| 3 | `inspect_feature` ×2 | L0:3498, L0:2238 |

### Dispatch: 5 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L8:F8406@1` | ❌ error | — | — | Trace this high-magnitude negative contributor to the synthetic contradiction-pr… |
| SA-2 | `L6:F14744@4` | ❌ error | — | — | Trace this positive contributor to the synthetic contradiction-probe score. Iden… |
| SA-3 | `L4:F12225@2` | ❌ error | — | — | Trace this strong negative contributor to the synthetic contradiction-probe scor… |
| SA-4 | `L4:F5450@4` | ❌ error | — | — | Trace this strong positive contributor to the synthetic contradiction-probe scor… |
| SA-5 | `L2:F11518@7` | ❌ error | — | — | Trace this major positive probe-score feature upstream and characterize its sema… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×5 | L2:11518, L4:5450, L4:12225, L0:8444, L2:4819 |
| 2 | `get_upstream_features` | L4:F5450@4, k=20 → Emb:" set"@3 (de=3.31) +19 more |
| 3 | `get_upstream_features` | L4:F12225@2, k=20 → Emb:" they"@2 (de=12.75) +19 more |
| 4 | `get_upstream_features` | L2:F11518@7, k=20 → Emb:" land"@7 (de=28.38) +19 more |
| 5 | `get_upstream_features` | L6:F14744@4, k=20 → Emb:" about"@4 (de=5.81) +19 more |
| 6 | `get_upstream_features` | L8:F8406@1, k=20 → Emb:"<bos>"@0 (de=10.25) +19 more |

### Build

`build_circuit` → 12 nodes, 8 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 20,827 | 2,657 | 38,177 | 0 | $0.1015 | — | — |
| **Total** | | **20,827** | **2,657** | **38,177** | **0** | **$0.1015** | | |

**Oracle wall-clock time:** 0m 40s