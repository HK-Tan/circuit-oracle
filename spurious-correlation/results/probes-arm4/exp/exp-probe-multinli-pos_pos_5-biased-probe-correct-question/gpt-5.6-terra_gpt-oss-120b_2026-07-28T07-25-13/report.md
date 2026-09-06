# Circuit Oracle Report
**Date:** 2026-07-28 07:25:13 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_5 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The contradiction probe is driven chiefly by lexical negation detectors—especially the final “isn’t”—rather than by a circuit that compares the two clauses’ shared proposition about improving lawyers’ public image.

**Confidence:** 8/10

**Reasoning:** The built circuit contains two substantial *positive* negation paths into the contradiction-probe output.

1. **Final contracted negation is the clearest driver.**  
   `Emb: isn (pos 26)` and `Emb: t (pos 28)` feed the layer-0 contraction feature **L0:6236**. This is a highly selective detector for the terminal *t* in contractions such as “isn’t/doesn’t” (`frac_nonzero=0.00258`), and it promotes “not” variants. It then supports **L16:12358**, a feature labeled *“not followed within a few tokens by a form of be”* (`frac_nonzero=0.02769`), which contributes **+0.373** directly to the probe score. The immediate upstream attribution is especially diagnostic: the raw embedding for `t` at pos 28 contributes **+12.69** to L16:12358, `isn` at pos 26 adds **+5.09**, and L0:6236 adds **+7.94**. This is a nearly literal orthographic/lexical route from “isn’t” to a higher contradiction score.

2. **The first-clause “not” also creates a generic negation route.**  
   `Emb: not (pos 6)` feeds **L13:4368**, a bare *“not”* detector (`frac_nonzero=0.02195`), which in turn supports **L16:15025**. That late feature is broadly a “not in context” feature (`frac_nonzero=0.02843`) and contributes **+0.3203** to the probe. Its largest upstream input is directly the raw `not` embedding (**+12.19**); the early direct word-level feature **L0:4958** also contributes **+4.19**. Thus the probe does not need to establish that the second sentence negates the earlier claim; the presence of “not” itself supplies a strong positive signal.

3. **There is a separate lexical construction circuit for “not only … but also,” but it is countervailing rather than contradiction-sensitive.**  
   `Emb: not (pos 6)` plus `Emb: only (pos 7)` activate **L2:5627**, a specific “not only” detector (`frac_nonzero=0.00685`), with a later corroborating “not only” feature **L9:12274** (`frac_nonzero=0.00288`). These feed **L15:12905**, a rare contrast / “but … also” feature (`frac_nonzero=0.00526`, promotes “also”). Crucially, L15:12905 has **negative direct effect −0.3203** on the contradiction score. It recognizes the concessive/additive construction in the first sentence, not semantic contradiction. Its negative sign suggests the probe is partly corrected away from calling the mere occurrence of “not only” a contradiction, but the correction does not encode the actual proposition-level relation.

4. **A speech-reporting feature is also influential but irrelevant to entailment status.**  
   `Emb: said (pos 3)` directly strongly excites **L4:15629** (**+34.25** upstream), a speech-attribution feature (`frac_nonzero=0.01439`, promotes “say/saying”). L4:15629 has the single largest listed positive direct probe effect, **+0.6719**. This is a generic reporting-context cue, not evidence that *“the program will help improve lawyers’ public image”* conflicts with *“the program isn’t going to improve lawyers’ public image.”* A companion speech feature, L4:12337, pushes in the opposite direction (**−0.5078**).

The aggregate positional check reinforces this conclusion. The set of cue positions `{program, not, only, but, t, …}` carries **22.25% net signed influence** on the score, versus **3.50%** for the strongest non-cue position (`S_over_R=6.36`). But the final contraction position alone carries only **5.68%**, showing that the decision is distributed across several surface constructions rather than grounded predominantly in the final sentence’s proposition.

So the probe reaches the *correct* contradiction-oriented score on this example, but its observed causal basis is largely **spurious lexical/syntactic correlation**: “not,” “isn’t,” “not only,” contrast markers, and reporting language. The traced features do **not** identify the repeated predicate “improve,” the shared object “lawyers’ public image,” or a feature binding the first claim to its explicit negation in the second sentence.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L4:F15629](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) | 3 | Speech-attribution feature |  speech attribution, such as the word "said" and phrases like "talking about" | [view](https://neuronpedia.org/gemma-2-2b/4-gemmascope-transcoder-16k/15629) |
| [L2:F5627](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) | 7 | “not only” lexical detector |  instances of the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/5627) |
| [L9:F12274](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) | 7 | “not only” phrase feature |  the phrase "not only" | [view](https://neuronpedia.org/gemma-2-2b/9-gemmascope-transcoder-16k/12274) |
| [L15:F12905](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) | 13 | Contrast / “but … also” feature (countervailing) |  the word "but" along with surrounding words that indicate a contrasting or consequential relationship. | [view](https://neuronpedia.org/gemma-2-2b/15-gemmascope-transcoder-16k/12905) |
| [L0:F6236](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) | 28 | Contraction-negation lexical feature | the letter "t" when it follows the word "isn'" or "doesn'" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/6236) |
| [L16:F12358](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) | 28 | Negation-before-copula detector |  the word "not" followed within a few tokens by a form of the verb "to be" | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/12358) |
| [L13:F4368](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) | 6 | Bare “not” detector |  the word "not" | [view](https://neuronpedia.org/gemma-2-2b/13-gemmascope-transcoder-16k/4368) |
| [L16:F15025](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) | 6 | Negation-in-context detector |  usage of the word "not" combined with personal pronouns or related emotional or motivational language | [view](https://neuronpedia.org/gemma-2-2b/16-gemmascope-transcoder-16k/15025) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 15 features; top: L4:15629 de=0.672 |
| 3 | `inspect_feature` ×7 | L16:12358, L16:15025, L4:15629, L4:12337, L2:5627, L0:6236, L15:12905 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L16:F12358@28` | ❌ error | — | — | Trace the positive path into the probe from L16:F12358 at pos 28. Determine whet… |
| SA-2 | `L16:F15025@6` | ❌ error | — | — | Trace the positive path into the probe from L16:F15025 at pos 6. Determine seman… |
| SA-3 | `L15:F12905@13` | ❌ error | — | — | Trace this major negative contributor to the probe. Establish whether it is lexi… |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_upstream_features` | L16:F12358@28, k=20 → Emb:"t"@28 (de=12.69) +19 more |
| 2 | `get_upstream_features` | L16:F15025@6, k=20 → Emb:" not"@6 (de=12.19) +19 more |
| 3 | `get_upstream_features` | L15:F12905@13, k=20 → Emb:" only"@7 (de=5.97) +19 more |
| 4 | `get_upstream_features` | L4:F15629@3, k=20 → Emb:" said"@3 (de=34.25) +19 more |
| 5 | `get_upstream_features` | L2:F5627@7, k=20 → Emb:" only"@7 (de=21.25) +19 more |
| 6 | `get_source_influence` | {'source_positions': [28], 'depth': 2} → {'depth': 2, 'source_positions': [28], 'S_pct_of_total': 5.675, 'R_pct_of_total' |
| 7 | `get_source_influence` | {'source_positions': [5, 6, 7, 13, 28, 30], 'depth': 2} → {'depth': 2, 'source_positions': [5, 6, 7, 13, 28, 30], 'S_pct_of_total': 22.252 |
| 8 | `inspect_feature` ×5 | L13:4368, L9:12274, L15:10071, L0:4958, L3:6227 |

### Build

`build_circuit` → 14 nodes, 14 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 24,823 | 2,955 | 77,695 | 0 | $0.1258 | — | — |
| **Total** | | **24,823** | **2,955** | **77,695** | **0** | **$0.1258** | | |

**Oracle wall-clock time:** 0m 40s