# Circuit Oracle Report
**Date:** 2026-07-28 07:25:21 UTC | **Orchestrator:** openai/gpt-5.6-terra | **Subagent:** openai/gpt-oss-120b

## Input

**Prompt:** "Dataset: multinli-pos_pos_4 | Probe: biased | Method: correct"

**System prompt:** ""

**Question:** "The circuit use spurious features (e.g.,"negation words" signals) rather than actual prompt content (lexical or semaintical) to predict contradiction."

**Top predictions:**  (100.0%)


## Oracle Analysis

**Analysis:** The probe score is driven chiefly by shallow lexical features—especially the explicit *“No one”* construction—rather than by a circuit that represents the contradiction between “ask at the tourist office” and “no one is usually at the tourist office.”

**Confidence:** 8/10

**Reasoning:** The saved circuit identifies a predominantly token-local mechanism.

- The only substantial **positive** contradiction-probe driver among the leading features is the *“No one”* pattern:
  - **Emb: ` No` (pos 16)** and **Emb: ` one` (pos 17)** feed **“one” / no-one lexical detector** (L0:4438, pos 17), which feeds **No-one construction detector** (L1:15800, pos 17), which feeds the synthetic probe score.
  - L0:4438 is exceptionally selective (`frac_nonzero=0.00114`) and its promoted tokens include *“Nobody,” “nobody,” “Everyone,” “someone”*. Its examples are overwhelmingly literal “no one” occurrences.
  - L1:15800 is likewise sparse (`frac_nonzero=0.00119`) and labelled simply *“the word ‘one’”*, but its activation examples are mostly “No one …”. Direct attribution shows its upstream sources are exactly ` No` (+5.34) and ` one` (+15.25), plus L0:4438 (+13.0). It directly raises the probe score by **+0.248**.
  - A related later feature, L2:8837 at pos 17, explicitly detects *“one/body preceded by ‘no’ or ‘every’”* (`frac_nonzero=0.01085`; promoted tokens include “nobody,” “anyone,” “Nobody”). This also confirms that the model has a clean local negated-quantifier representation. However, on this particular probe direction it has a negative direct effect (**−0.207**), so the probe weights related features inconsistently rather than using a coherent semantic contradiction variable.

- The most influential **negative** contribution is not semantic contradiction evidence at all:
  - **Pick-up lexical detector** L2:3116 at pos 2 contributes **−0.609**. It is a sparse detector (`frac_nonzero=0.00615`) for the phrasal verb *“pick up”*, with promoted tokens *“pickup/Pickup”*.
  - Its upstream attribution terminates directly at **Emb: `Pick` (pos 1)** (+50) and **Emb: ` up` (pos 2)** (+20.75). Thus, the score is strongly affected by an incidental imperative/travel phrase, not by whether the two sentences are mutually compatible.
  - The raw **“up”** feature L0:10562 (`frac_nonzero=0.01437`) itself contributes **+0.295** to the probe. This opposite-sign pair shows that the linear probe is sensitive to several overlapping surface-form directions for the same phrase, not a stable semantic representation.

- Repeated tourism content is also treated as lexical evidence/counterevidence:
  - **Tour/tours lexical detectors** L2:14413 and L2:1016 at pos 14 contribute **−0.281** and **+0.217**, respectively. They are labelled direct word-form detectors for *tour/tours*, with `frac_nonzero=0.01117` and `0.00762`.
  - Both trace primarily to **Emb: ` tours` (pos 14)** (about +28 upstream influence), with only small contextual contributions from ` tourist`, ` walking`, and ` about`.
  - This is not a mechanism that links “walking tours” in the first sentence to “find out about walking tours” in the second; it is mostly recognition of the token *tours*.

- Another non-semantic surface feature, L4:10722 at pos 9, is a *“here”* usage detector (`frac_nonzero=0.0185`) and contributes **−0.213**. It traces mainly to **Emb: ` here` (pos 9)** (+24.125). This reinforces the picture of a shallow lexical mixture.

Therefore, the user’s concern is substantially supported: the circuit has a real local negation/negative-quantifier signal—**“No one”**—but it does **not** demonstrate composition of the relevant proposition (*the tourist office is normally unattended*) with the earlier instruction (*ask at that office*). Instead, the probe score is an uneven signed combination of local `No one`, `pick up`, `up`, `tours`, and `here` detectors. The strongest feature is actually the incidental *pick up* phrase, while the repeated *tours* token also has large signed effects. This is consistent with a contradiction probe that exploits lexical correlations, particularly negation-like wording, rather than reliably encoding contradiction semantics.

## Circuit Links

Neuronpedia dashboards for each pinned feature.

| Feature | Pos | Supernode role | Autointerp label | Neuronpedia |
|---------|-----|----------------|------------------|-------------|
| [L2:F3116](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) | 2 | Pick-up lexical detector |  the phrasal verb "pick up" and variations | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/3116) |
| [L0:F10562](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) | 2 | “up” lexical feature | the word "up" | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/10562) |
| [L2:F14413](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) | 14 | Tour/tours lexical detectors | the word "tour" or "tours" | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/14413) |
| [L2:F1016](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) | 14 | Tour/tours lexical detectors |  forms of the verb "tour" and the noun "tour." | [view](https://neuronpedia.org/gemma-2-2b/2-gemmascope-transcoder-16k/1016) |
| [L0:F4438](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) | 17 | “one” / no-one lexical detector | the word "one". | [view](https://neuronpedia.org/gemma-2-2b/0-gemmascope-transcoder-16k/4438) |
| [L1:F15800](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) | 17 | No-one construction detector |  the word "one" | [view](https://neuronpedia.org/gemma-2-2b/1-gemmascope-transcoder-16k/15800) |

## Process Trace

### Scout

| # | Tool | Summary |
|---|------|---------|
| 1 | `get_top_logits` | "" (100%) |
| 2 | `get_top_features` | 12 features; top: L2:3116 de=-0.609 |
| 3 | `inspect_feature` ×5 | L2:3116, L0:10562, L0:10904, L2:14413, L1:15800 |

### Dispatch: 3 subagent(s) (concurrent)

| Label | Node | Outcome | Features | Edges | Objective |
|-------|------|---------|----------|-------|-----------|
| SA-1 | `L2:F3116@2` | ❌ error | — | — | Trace the strongest negative driver of the synthetic contradiction-probe directi… |
| SA-2 | `L2:F14413@14` | ❌ error | — | — | Trace this negative probe driver upstream to embeddings and identify whether it … |
| SA-3 | `L1:F15800@17` | ❌ error | — | — | Trace this positive probe driver to embeddings; identify exact input tokens and … |

### Post-dispatch (orchestrator)

| # | Tool | Summary |
|---|------|---------|
| 1 | `inspect_feature` ×4 | L2:8837, L2:1016, L0:2238, L4:10722 |
| 2 | `get_upstream_features` | L2:F3116@2, k=20 → Emb:"Pick"@1 (de=50.00) +19 more |
| 3 | `get_upstream_features` | L2:F14413@14, k=20 → Emb:" tours"@14 (de=28.38) +19 more |
| 4 | `get_upstream_features` | L1:F15800@17, k=20 → Emb:" one"@17 (de=15.25) +19 more |
| 5 | `inspect_feature` | L0, F4438 → "the word "one"." |
| 6 | `get_upstream_features` | L2:F8837@17, k=12 → Emb:" No"@16 (de=18.62) +11 more |
| 7 | `get_upstream_features` | L2:F1016@14, k=12 → Emb:" tours"@14 (de=27.75) +11 more |
| 8 | `get_upstream_features` | L4:F10722@9, k=12 → Emb:" here"@9 (de=24.12) +11 more |

### Build

`build_circuit` → 11 nodes, 9 edges

## Token Usage
| Role | Model | Input | Output | Cache Read | Cache Write | Cost | Outcome | Objective |
|------|-------|-------|--------|------------|-------------|------|---------|-----------|
| Orchestrator | openai/gpt-5.6-terra | 20,597 | 2,980 | 71,518 | 0 | $0.1141 | — | — |
| **Total** | | **20,597** | **2,980** | **71,518** | **0** | **$0.1141** | | |

**Oracle wall-clock time:** 0m 46s