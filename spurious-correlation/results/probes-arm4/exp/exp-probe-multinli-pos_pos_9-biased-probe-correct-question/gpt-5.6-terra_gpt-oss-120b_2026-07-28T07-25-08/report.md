# Circuit Oracle Report
**Date:** 2026-07-28 07:25:08 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_9 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe’s contradiction score is driven chiefly by the literal negation **“not”** in “Recorded menus do not provide…,” with smaller, largely lexical contributions from **“recorded”** and **“menu,”** rather than by a rich comparison of the two propositions.

**Confidence:** 9/10

**Reasoning:** The saved circuit shows a dominant negation pathway from **Emb: ` not` (pos 17)** into several directly and causally probe-aligned features:

- The layer-0 feature **L0:4958** is an explicit *“the word ‘not’”* detector (frac_nonzero **0.0184**). Its direct upstream attribution is overwhelmingly the ` not` embedding: **+33.5**, versus tiny contributions from `obtain` (+0.28), `provide` (+0.19), and `information` (+0.15). Thus it is essentially a token-identity feature, not a representation of the full predicate or sentence relation.
- `not` also directly excites two layer-4 abstract/multilingual negation features: **L4:4492** (*negations in various languages*, frac_nonzero **0.03828**) with **+17.38** embedding-to-feature effect, and **L4:2422** (*French/Malay/Croatian-style negation cues*, frac_nonzero **0.01567**) with **+16.13**. Although their labels are broader than English, their activation here is still directly attributable to the English `not` token.
- These feed/converge with the direct lexical feature into **L16:6800**, labelled *negations “not”, “no”, and contractions with “t”* (frac_nonzero **0.03101**). This is the largest later-layer positive feature in the probe direction (**+0.4355** direct effect on the score). Its strongest upstream source is again **Emb ` not` pos 17, +11.81**, followed by the L0 `not` detector (+2.56) and L4:4492 (+0.97). This establishes the principal causal route:
  
  `not` embedding → direct/abstract negation features → late negation signal → **probe score**.

This supports the user concern: the classification is strongly keyed to a **surface negation marker**. Negation is genuinely relevant to the text’s contradiction-like relationship—the first statement says a recorded menu *will provide information*, while the second says recorded menus *do not provide information at this time*. But the traced circuit does **not** show a substantial late mechanism encoding the shared subject (“recorded menu(s)”), the predicate reversal (“provide information” vs. “do not provide”), or temporal qualification (“at this time”) and then comparing those propositions. It primarily detects that there is a `not`.

There are additional early lexical routes:

- **Emb ` recorded` (pos 2)** strongly drives **L0:7443**, a broad *record* detector (frac_nonzero **0.01531**; embedding effect **+22.63**), and **L1:3691**, a *recording/recorded* detector (frac_nonzero **0.00733**; embedding effect **+24.75**). L1:3691 is itself a leading positive direct probe feature (**+0.8242**).
- The `recorded` embedding also directly drives **L2:8776** (**+19.5** upstream effect); this feature is autointerpreted as finance/property terminology (frac_nonzero **0.01099**), which does not semantically fit the prompt. Its positive probe effect (**+0.6367**) is therefore likely an idiosyncratic direction overlap or dataset/probe artifact, rather than contradiction reasoning.
- **Emb ` menu` (pos 3)** drives **L0:2108**, a highly selective *“menu”* detector (frac_nonzero **0.00353**, embedding effect **+25.75**). Yet this detector has a **negative** direct effect on the classification score (**−0.6250**), so the lexical menu cue acts against the selected probe direction rather than supplying an inference about the two menu statements.

Overall, the circuit contains real prompt-content features—especially lexical detectors for `not`, `recorded`, and `menu`—but the evidence favors a **spurious/shallow contradiction heuristic dominated by negation**, not a compositional contradiction detector. The presence of `not` supplies the core positive score; the repeated entity words contribute weakly or inconsistently, and no traced high-impact path represents comparison between the affirmative and negated claims.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L0:F4958](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) | 17 | Direct lexical negation detector |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4958) |
| [L4:F4492](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) | 17 | Abstract negation detectors | negations in various languages | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/4492) |
| [L4:F2422](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) | 17 | Abstract negation detectors | negations in other languages like French, Malay, and Croatian | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/2422) |
| [L16:F6800](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) | 17 | Late negation signal |  negations "not", "no", and contractions with "t".  | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/6800) |
| [L0:F7443](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) | 2 | Recorded/record lexical detectors | the word "record" appearing in various contexts | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/7443) |
| [L1:F3691](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) | 2 | Recorded/record lexical detectors |  the word "recording" in scientific or experimental documentation | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/3691) |
| [L2:F8776](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) | 2 | Recorded-token probe feature |  words related to finance and property law | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/8776) |
| [L0:F2108](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) | 3 | Menu lexical detector | the word "menu" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/2108) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L1:3691 de=0.824 |
| 3 | `inspect_feature` ×8 | L1:3691, L2:8776, L0:2108, L0:7443, L16:6800, L0:4958, L4:4492, L4:2422 |

### Dispatch: 4 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F6800@17` | ❌ error | — | — | Trace this late positive probe-driving feature to embeddings. Determine whether … |
| SA-2 | `L4:F4492@17` | ❌ error | — | — | Trace this positive probe feature upstream to embeddings; identify lexical and s… |
| SA-3 | `L4:F2422@17` | ❌ error | — | — | Trace this negative probe-driving feature upstream to embeddings and establish w… |
| SA-4 | `L2:F8776@2` | ❌ error | — | — | Trace this strong positive early probe-driving feature upstream to embeddings; d… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F6800@17, k=20 → Emb:" not"@17 (de=11.81) +19 more |
| 2 | `get_upstream_features` | L4:F4492@17, k=20 → Emb:" not"@17 (de=17.38) +19 more |
| 3 | `get_upstream_features` | L4:F2422@17, k=20 → Emb:" not"@17 (de=16.12) +19 more |
| 4 | `get_upstream_features` | L2:F8776@2, k=20 → Emb:" recorded"@2 (de=19.50) +19 more |
| 5 | `get_upstream_features` | L1:F3691@2, k=20 → Emb:" recorded"@2 (de=24.75) +19 more |
| 6 | `get_upstream_features` | L0:F4958@17, k=20 → Emb:" not"@17 (de=33.50) +19 more |
| 7 | `get_upstream_features` | L0:F2108@3, k=20 → Emb:" menu"@3 (de=25.75) +19 more |
| 8 | `get_upstream_features` | L0:F7443@2, k=20 → Emb:" recorded"@2 (de=22.62) +19 more |

### Build

`build_circuit` → 10 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 19,712 | 2,380 | 54,363 | 0 | $0.0986 | — | — |
| **Total** | | **19,712** | **2,380** | **54,363** | **0** | **$0.0986** | | |

**Oracle wall-clock time:** 0m 35s